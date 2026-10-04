#!/usr/bin/env python3
"""Read-only V1A 5 A path screen, using only Python's standard library.

CALCULATED under ASSUMED geometry/material/thermal conditions, not validation.
See docs/pcb/PATH_CHECK.md for the model, exclusions and source provenance.
"""
import argparse
from collections import defaultdict
from dataclasses import dataclass, field
import hashlib
import heapq
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOCATIONS = ROOT / 'docs/evidence/r2/r203_option_a/CALCULATIONS.json'
PATH_NETS = {'VOUT_5V1', 'PROT_MID', 'SERIES_OUT', 'VOUT_PROTECTED', 'LOAD_5V1', 'GND'}
COPPER_ROWS = {'unsensed_buck_copper', 'module_PCB'}
EPS = 1e-7  # mm; equality tolerance, never a routing clearance
RHO20 = 1.724e-8  # ohm m, ASSUMED annealed copper
ALPHA = 0.00393  # / K at 20 C, ASSUMED


def parse(text):
    """Parse one S-expression, rejecting truncation and malformed tokens."""
    tokens = re.findall(r';[^\n]*|\s+|[()]|"(?:\\.|[^"\\])*"|[^\s()";]+|"', text)
    stack, roots = [], []
    for token in tokens:
        if token.isspace() or token.startswith(';'):
            continue
        if token == '(':
            item = []
            (stack[-1] if stack else roots).append(item)
            stack.append(item)
        elif token == ')':
            if not stack:
                raise ValueError('unexpected closing parenthesis')
            stack.pop()
        else:
            if not stack:
                raise ValueError('token outside S-expression')
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    if stack or len(roots) != 1 or not roots[0]:
        raise ValueError('incomplete or multiple S-expressions')
    return roots[0]


def children(node, name):
    return [x for x in node if isinstance(x, list) and x and x[0] == name]


def one(node, name, default=None):
    return next(iter(children(node, name)), default)


def value(node, name, default=None):
    item = one(node, name)
    return item[1] if item and len(item) > 1 else default


def number(x):
    v = float(x)
    if not math.isfinite(v):
        raise ValueError('non-finite dimension/value')
    return v


def positive(x):
    v = number(x)
    if v <= 0:
        raise ValueError('dimension must be positive')
    return v


def point(node, name):
    v = one(node, name)
    if not v or len(v) < 3:
        raise ValueError(f'missing {name} coordinate')
    return number(v[1]), number(v[2])


def rotate(p, degrees):
    # KiCad file coordinates have downward Y; positive orientation is CCW.
    a = math.radians(degrees)
    return p[0]*math.cos(a) + p[1]*math.sin(a), -p[0]*math.sin(a) + p[1]*math.cos(a)


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def projection(p, a, b):
    d = sub(b, a)
    length2 = d[0]**2+d[1]**2
    t = 0 if length2 == 0 else max(0, min(1, sum(x*y for x, y in zip(sub(p, a), d))/length2))
    q = a[0]+t*d[0], a[1]+t*d[1]
    return t, q, math.dist(p, q)


def intersection(a, b, c, d):
    u, v = sub(b, a), sub(d, c)
    det = cross(u, v)
    if abs(det) < 1e-12:
        return None
    t, s = cross(sub(c, a), v)/det, cross(sub(c, a), u)/det
    if -EPS <= t <= 1+EPS and -EPS <= s <= 1+EPS:
        return a[0]+t*u[0], a[1]+t*u[1]
    return None


def sides(poly):
    return zip(poly, poly[1:]+poly[:1])


def inside(p, poly):
    # Even/odd works with KiCad's linked hole contours too. Boundary is excluded.
    hit = False
    for a, b in sides(poly):
        if (a[1] > p[1]) != (b[1] > p[1]):
            if p[0] < (b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:
                hit = not hit
    return hit


def clearance(p, poly):
    return min(projection(p, a, b)[2] for a, b in sides(poly))


def corridor_width(a, b, poly, cap):
    """Width of a straight capsule wholly within the saved copper polygon."""
    if not inside(a, poly) or not inside(b, poly):
        return 0.0
    distance = math.inf
    for c, d in sides(poly):
        if intersection(a, b, c, d) is not None:
            return 0.0
        distance = min(distance, projection(a, c, d)[2], projection(b, c, d)[2],
                       projection(c, a, b)[2], projection(d, a, b)[2])
    return min(cap, 2*distance)


@dataclass
class Settings:
    copper_um_outer: float = 70
    copper_um_inner: float = 35
    temp_c: float = 85
    via_plating_um: float = 25
    zone_grid_mm: float = 1
    zone_width_cap_mm: float = 1
    max_zone_nodes: int = 40000

    def __post_init__(self):
        for name, v in vars(self).items():
            if not math.isfinite(v) or (name != 'temp_c' and v <= 0):
                raise ValueError(f'invalid {name}')
        if self.temp_c < -50 or self.temp_c > 200:
            raise ValueError('temp-c must be within the screening range -50..200 C')

    def thickness(self, layer):
        return self.copper_um_outer if layer in ('F.Cu', 'B.Cu') else self.copper_um_inner

    @property
    def rho(self):
        return RHO20*(1+ALPHA*(self.temp_c-20))

    def resistance(self, length_mm, width_mm, layer):
        return self.rho * length_mm * 1e9 / (positive(width_mm)*self.thickness(layer))  # mOhm

    def barrel(self, length_mm, drill_mm):
        plating_mm = self.via_plating_um/1000
        area_mm2 = math.pi*(positive(drill_mm)+plating_mm)*plating_mm
        return self.rho*length_mm*1e6/area_mm2  # mOhm


def thermal_rise(width_mm, thickness_um, current=5):
    """Conservative IPC-2152-style screen using the legacy internal envelope.

    TI SNVA766 Eq.3: I = .024 * dT**.44 * A_mil2**.725.
    Applied to BOTH outer and inner traces; no plane/airflow cooling credit.
    This is explicitly not an implementation of the IPC-2152 chart dataset.
    """
    area = positive(width_mm)*(positive(thickness_um)/1000)/(0.0254**2)
    return (current/(0.024*area**0.725))**(1/0.44)


@dataclass
class Pad:
    ref: str
    pin: str
    net: str
    xy: tuple
    layers: list
    poly: list
    width: float
    drill: float = 0


@dataclass
class Trace:
    ident: str
    net: str
    layer: str
    a: tuple
    b: tuple
    width: float
    length: float


@dataclass
class Board:
    layers: list
    thickness: float
    pads: list = field(default_factory=list)
    traces: list = field(default_factory=list)
    vias: list = field(default_factory=list)
    zones: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    thermal: list = field(default_factory=list)


def pad_outline(p):
    w, h = point(p, 'size')
    positive(w); positive(h)
    shape = p[3]
    if shape == 'custom':
        primitives = one(p, 'primitives', [])
        polys = children(primitives, 'gr_poly')
        if len(polys) != 1 or len(primitives) != 2 or value(polys[0], 'fill') != 'yes':
            raise ValueError('unsupported custom pad; requires one filled gr_poly')
        poly = [point(['p', xy], 'xy') for xy in children(one(polys[0], 'pts', []), 'xy')]
        if len(poly) < 3 or not inside((0, 0), poly):
            raise ValueError('custom pad anchor outside polygon')
        return poly, 2*clearance((0, 0), poly)
    if shape == 'rect':
        return [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)], min(w, h)
    if shape in ('roundrect', 'oval', 'circle'):
        r = min(w, h)/2 if shape != 'roundrect' else min(w, h)*number(value(p, 'roundrect_rratio', .25))
        if not 0 <= r <= min(w, h)/2:
            raise ValueError('invalid roundrect radius')
        if r == 0:
            return [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)], min(w, h)
        poly = []
        for cx, cy, start in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90),
                              (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
            for j in range(9):
                angle = math.radians(start+90*j/8)
                poly.append((cx+r*math.cos(angle), cy+r*math.sin(angle)))
        return poly, min(w, h)
    raise ValueError(f'unsupported pad shape {shape}')


def arc_parts(t):
    a, m, b = point(t, 'start'), point(t, 'mid'), point(t, 'end')
    u, v = sub(m, a), sub(b, a)
    det = 2*cross(u, v)
    if abs(det) < 1e-12:
        raise ValueError('degenerate arc')
    uu, vv = sum(x*x for x in u), sum(x*x for x in v)
    center = add(a, ((uu*v[1]-vv*u[1])/det, (u[0]*vv-v[0]*uu)/det))
    r = math.dist(a, center)
    angle = lambda p: math.atan2(p[1]-center[1], p[0]-center[0])
    start, middle, end = angle(a), angle(m), angle(b)
    sweep = (end-start) % (2*math.pi)
    if (middle-start) % (2*math.pi) > sweep:
        sweep -= 2*math.pi
    n = max(1, math.ceil(abs(sweep)/math.radians(5)))
    points = [a]+[(center[0]+r*math.cos(start+sweep*i/n), center[1]+r*math.sin(start+sweep*i/n))
                  for i in range(1, n)]+[b]
    return points, r*abs(sweep), 2*r*(1-math.cos(sweep/(2*n)))


def read_board(text, settings):
    root = parse(text)
    if root[0] != 'kicad_pcb':
        raise ValueError('expected kicad_pcb root')
    layers = [v[1] for v in one(root, 'layers', [])[1:] if isinstance(v, list) and v[1].endswith('.Cu')]
    if not layers or layers[0] != 'F.Cu' or layers[-1] != 'B.Cu':
        raise ValueError('missing/unsupported copper layer order')
    board = Board(layers, positive(value(one(root, 'general', []), 'thickness', 1.6)))
    if value(one(root, 'general', []), 'thickness') is None:
        board.issues.append('board thickness missing (1.6 mm assumption requires review)')
    nets = {v[1]: v[2] for v in children(root, 'net')}
    names = defaultdict(set)
    for name in nets.values():
        names[name.rsplit('/', 1)[-1]].add(name)
    for name in PATH_NETS:
        if len(names[name]) > 1:
            board.issues.append(f'ambiguous hierarchical net {name}: {sorted(names[name])}')

    def net(item):
        n = one(item, 'net')
        if not n:
            return ''
        name = n[2] if len(n) > 2 else nets.get(n[1], '')
        if len(n) > 2 and n[1] in nets and nets[n[1]] != n[2]:
            raise ValueError('conflicting net number/name')
        return name.rsplit('/', 1)[-1]

    for fp in children(root, 'footprint'):
        ref = next((p[2] for p in children(fp, 'property') if p[1] == 'Reference'), '')
        if not ref:
            ref = next((p[2] for p in children(fp, 'fp_text') if p[1] == 'reference'), '')
        at = one(fp, 'at', ['at', '0', '0'])
        origin, angle = (number(at[1]), number(at[2])), number(at[3]) if len(at) > 3 else 0
        for p in children(fp, 'pad'):
            name = net(p)
            if name not in PATH_NETS or p[2] == 'np_thru_hole':
                continue
            copper = one(p, 'layers', [])[1:]
            pad_layers = layers[:] if '*.Cu' in copper else [v for v in copper if v in layers]
            if not pad_layers:
                continue
            try:
                if one(p, 'drill') and one(p, 'drill')[1] == 'oval':
                    raise ValueError('slotted plated pad requires manual barrel analysis')
                if one(p, 'offset') or one(one(p, 'drill', []), 'offset'):
                    raise ValueError('offset pad/drill requires manual analysis')
                if 'remove_unused_layers' in p or one(p, 'padstack'):
                    raise ValueError('custom/removed-layer padstack requires manual analysis')
                poly, width = pad_outline(p)
                xy = add(origin, rotate(point(p, 'at'), angle))
                # Pad angle in a board file is already absolute; position is local.
                pat = one(p, 'at')
                pad_angle = number(pat[3]) if len(pat) > 3 else 0
                poly = [add(xy, rotate(v, pad_angle)) for v in poly]
                drill = positive(value(p, 'drill')) if one(p, 'drill') else 0
                if drill:
                    width = min(width, (width-drill)/2)
                    positive(width)
                board.pads.append(Pad(ref, p[1], name, xy, pad_layers, poly, width, drill))
            except ValueError as exc:
                board.issues.append(f'{ref}.{p[1]}: {exc}')

    for i, t in enumerate(children(root, 'segment')+children(root, 'arc')):
        name = net(t)
        if name not in PATH_NETS:
            continue
        layer, width = value(t, 'layer'), positive(value(t, 'width'))
        if layer not in layers:
            raise ValueError(f'trace on undefined layer {layer}')
        ident = value(t, 'uuid', value(t, 'tstamp', f'trace-{i}'))
        if t[0] == 'arc':
            pts, length, width_loss = arc_parts(t)
        else:
            pts = [point(t, 'start'), point(t, 'end')]
            length, width_loss = math.dist(*pts), 0
        if length <= EPS:
            continue
        actual_width = positive(width-width_loss)
        for a, b in zip(pts, pts[1:]):
            board.traces.append(Trace(ident, name, layer, a, b, actual_width, length/(len(pts)-1)))
        board.thermal.append(dict(id=ident, net=name, layer=layer, length_mm=length, width_mm=width,
                                  thickness_um=settings.thickness(layer),
                                  rise_5A_C=thermal_rise(width, settings.thickness(layer)),
                                  classification='CALCULATED / ASSUMED legacy internal-envelope screen'))

    for i, v in enumerate(children(root, 'via')):
        name = net(v)
        if name not in PATH_NETS:
            continue
        span = one(v, 'layers', [])[1:]
        if span != ['F.Cu', 'B.Cu'] or 'blind' in v or 'micro' in v or one(v, 'padstack'):
            board.issues.append(f'{name} via {i}: blind/buried/custom via depth OPEN')
            continue
        if 'remove_unused_layers' in v:
            board.issues.append(f'{name} via {i}: removed-layer annuli unsupported')
            continue
        drill, size = positive(value(v, 'drill')), positive(value(v, 'size'))
        if size <= drill:
            raise ValueError('via diameter must exceed drill')
        board.vias.append(dict(id=f'via-{i}', net=name, xy=point(v, 'at'), drill=drill, size=size))

    for i, z in enumerate(children(root, 'zone')):
        name = net(z)
        if name not in PATH_NETS or one(z, 'keepout'):
            continue
        fills = children(z, 'filled_polygon')
        if not fills:
            board.issues.append(f'{name} zone {i}: unfilled zone; outline is not copper')
        for j, fill in enumerate(fills):
            layer = value(fill, 'layer', value(z, 'layer'))
            poly = [point(['p', v], 'xy') for v in children(one(fill, 'pts', []), 'xy')]
            if len(poly) < 3 or layer not in layers:
                board.issues.append(f'{name} zone {i}: unsupported filled polygon/layer')
                continue
            board.zones.append(dict(id=f'zone-{i}-{j}', net=name, layer=layer, poly=poly))
    return board


class Graph:
    def __init__(self):
        self.nodes, self.index, self.adj = [], {}, defaultdict(list)

    def node(self, net, layer, xy):
        key = (net, layer, round(xy[0], 7), round(xy[1], 7))
        if key not in self.index:
            self.index[key] = len(self.nodes)
            self.nodes.append((net, layer, xy))
        return self.index[key]

    def edge(self, a, b, resistance, kind, ident, **data):
        if a == b:
            return
        detail = dict(kind=kind, id=ident, resistance_mohm=resistance, **data)
        self.adj[a].append((b, resistance, detail))
        self.adj[b].append((a, resistance, detail))

    def shortest(self, sources, targets):
        targets = set(targets)
        queue = [(0.0, i) for i in set(sources)]
        heapq.heapify(queue)
        distance, prev = {i: 0.0 for _, i in queue}, {}
        while queue:
            d, u = heapq.heappop(queue)
            if d != distance[u]:
                continue
            if u in targets:
                path = []
                while u in prev:
                    u, edge = prev[u]
                    path.append(edge)
                return d, list(reversed(path))
            for v, cost, detail in self.adj[u]:
                alt = d+cost
                if alt < distance.get(v, math.inf):
                    distance[v], prev[v] = alt, (u, detail)
                    heapq.heappush(queue, (alt, v))
        return None


def build_graph(board, settings):
    g = Graph()
    pad_nodes = {}
    for i, p in enumerate(board.pads):
        pad_nodes[i] = [g.node(p.net, layer, p.xy) for layer in p.layers]
        if p.drill:
            # Full board thickness for every layer hop: intentionally conservative
            # without dielectric stack depths. No zero-ohm plated-hole shortcuts.
            for a, b in zip(pad_nodes[i], pad_nodes[i][1:]):
                g.edge(a, b, settings.barrel(board.thickness, p.drill), 'barrel', f'{p.ref}.{p.pin}')
    for v in board.vias:
        ids = [g.node(v['net'], layer, v['xy']) for layer in board.layers]
        for a, b in zip(ids, ids[1:]):
            g.edge(a, b, settings.barrel(board.thickness, v['drill']), 'barrel', v['id'])
    by_layer = defaultdict(list)
    for t in board.traces:
        g.node(t.net, t.layer, t.a); g.node(t.net, t.layer, t.b)
        by_layer[t.net, t.layer].append(t)
    for group in by_layer.values():
        for i, t in enumerate(group):
            for other in group[i+1:]:
                hit = intersection(t.a, t.b, other.a, other.b)
                if hit is not None:
                    g.node(t.net, t.layer, hit)
    base_nodes = list(enumerate(g.nodes))
    for t in board.traces:
        cuts = []
        for i, (net, layer, xy) in base_nodes:
            if (net, layer) == (t.net, t.layer):
                along, _, dist = projection(xy, t.a, t.b)
                if dist <= EPS:
                    cuts.append((along, i))
        cuts.sort()
        for (a, u), (b, v) in zip(cuts, cuts[1:]):
            length = (b-a)*t.length
            g.edge(u, v, settings.resistance(length, t.width, t.layer), 'trace', t.ident,
                   length_mm=length, width_mm=t.width, layer=t.layer)

    # Saved fill only. Grid nodes + all terminals form a visibility graph. Every
    # edge is a contained finite-width strip; obstacles/holes can never be jumped.
    for zone in board.zones:
        poly, net, layer = zone['poly'], zone['net'], zone['layer']
        xs, ys = zip(*poly)
        step = settings.zone_grid_mm
        x0, x1 = math.floor(min(xs)/step), math.ceil(max(xs)/step)
        y0, y1 = math.floor(min(ys)/step), math.ceil(max(ys)/step)
        if (x1-x0+1)*(y1-y0+1) > settings.max_zone_nodes:
            board.issues.append(f"{zone['id']}: zone grid exceeds node limit; adjust --zone-grid-mm")
            continue
        terminals = [(i, xy) for i, (n, l, xy) in base_nodes
                     if (n, l) == (net, layer) and inside(xy, poly) and clearance(xy, poly) > EPS]
        grid = {}
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                xy = x*step, y*step
                if inside(xy, poly) and clearance(xy, poly) > EPS:
                    grid[x, y] = g.node(net, layer, xy)

        def zone_edge(u, v):
            a, b = g.nodes[u][2], g.nodes[v][2]
            width = corridor_width(a, b, poly, settings.zone_width_cap_mm)
            if width > EPS and u != v:
                length = math.dist(a, b)
                g.edge(u, v, settings.resistance(length, width, layer), 'zone', zone['id'],
                       length_mm=length, width_mm=width, layer=layer)

        for (x, y), u in grid.items():
            for dx, dy in ((1, 0), (0, 1), (1, 1), (1, -1)):
                v = grid.get((x+dx, y+dy))
                if v is not None:
                    zone_edge(u, v)
        for index, (u, xy) in enumerate(terminals):
            # Exact direct visibility avoids grid quantisation for straight paths.
            for v, _ in terminals[index+1:]:
                zone_edge(u, v)
            gx, gy = round(xy[0]/step), round(xy[1]/step)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    v = grid.get((gx+dx, gy+dy))
                    if v is not None:
                        zone_edge(u, v)

    # Pad spreading is a lumped strip approximation, not a zero-ohm pad area.
    # Include grid nodes inside lands to reach saved thermal spokes around holes.
    for i, p in enumerate(board.pads):
        xs, ys = zip(*p.poly)
        bounds = min(xs)-EPS, max(xs)+EPS, min(ys)-EPS, max(ys)+EPS
        for u in pad_nodes[i]:
            layer = g.nodes[u][1]
            for v, (net, l, xy) in enumerate(g.nodes):
                if (net == p.net and l == layer and bounds[0] <= xy[0] <= bounds[1]
                        and bounds[2] <= xy[1] <= bounds[3]
                        and (inside(xy, p.poly) or clearance(xy, p.poly) <= EPS)):
                    # Reject concave-pad shortcuts through a cutout. Contacts
                    # exactly on the outline remain conservatively unresolved.
                    if corridor_width(p.xy, xy, p.poly, p.width) <= EPS:
                        continue
                    length = math.dist(p.xy, xy)
                    g.edge(u, v, settings.resistance(length, p.width, layer), 'pad', f'{p.ref}.{p.pin}',
                           length_mm=length, width_mm=p.width, layer=layer)
    return g, pad_nodes


def frozen_budget(path=ALLOCATIONS):
    raw = Path(path).read_bytes()
    data = json.loads(raw)
    rows = data['path']['itemised_rows']
    if {r['element'] for r in rows if r['element'] in COPPER_ROWS} != COPPER_ROWS:
        raise ValueError('missing frozen copper allocation rows')
    summed = sum(number(r['send_mohm'])+number(r['return_mohm']) for r in rows)
    if not math.isclose(summed, data['path']['loop_mohm'], abs_tol=1e-9):
        raise ValueError('frozen itemized allocation does not sum to loop_mohm')
    trough = next(c['negative_excursion_V'] for c in data['path']['cases'] if c['case'] == 'Frozen path, 20 mV trough')
    copper = {side: sum(r[side+'_mohm'] for r in rows if r['element'] in COPPER_ROWS) for side in ('send', 'return')}
    fixed = {side: sum(r[side+'_mohm'] for r in rows if r['element'] not in COPPER_ROWS) for side in ('send', 'return')}
    return dict(source=str(path), sha256=hashlib.sha256(raw).hexdigest(), rows=rows,
                copper_mohm=copper, fixed_mohm=fixed, frozen_loop_mohm=summed,
                buck_min_V=data['divider']['hot_with_ASSUMED_10nA_band_V'][0],
                trough_V=trough, pi_floor_V=data['requirements']['pi_min_V'], load_A=data['requirements']['load_A'])


def check(text, settings=None, budget=None):
    settings, budget = settings or Settings(), budget or frozen_budget()
    b = read_board(text, settings)
    g, pads = build_graph(b, settings) if b.traces or b.zones else (Graph(), {})
    issues = list(b.issues)

    def terminals(ref, pins, net):
        matches = [i for i, p in enumerate(b.pads) if p.ref == ref and p.pin in pins and p.net == net]
        found = {b.pads[i].pin for i in matches}
        if found != set(pins):
            issues.append(f'{ref} {net}: missing/wrong-net pads {sorted(set(pins)-found)}')
        return matches

    def leg(name, side, start, end):
        paths = []
        # Require each physical terminal to reach the other endpoint group, and
        # take the largest single-terminal shortest resistance. No sharing credit.
        for group, other in ((start, end), (end, start)):
            targets = [node for p in other for node in pads.get(p, [])]
            for p in group:
                result = g.shortest(pads.get(p, []), targets)
                if result is None:
                    return dict(net=name, side=side, status='OPEN', resistance_mohm=None,
                                reason=f'unrouted/disconnected {b.pads[p].ref}.{b.pads[p].pin}', path=[])
                paths.append(result)
        if not start or not end or not paths:
            return dict(net=name, side=side, status='OPEN', resistance_mohm=None,
                        reason='required endpoint missing', path=[])
        resistance, path = max(paths, key=lambda v: v[0])
        return dict(net=name, side=side, status='CALCULATED', resistance_mohm=resistance, path=path)

    caps = [f'C{i}' for i in range(209, 215)]
    cap_pos = sum((terminals(ref, ['1'], 'VOUT_5V1') for ref in caps), [])
    cap_gnd = sum((terminals(ref, ['2'], 'GND') for ref in caps), [])
    legs = [
        leg('VOUT_5V1', 'send', cap_pos, terminals('Q301', ['5', '6', '7', '8'], 'VOUT_5V1')),
        leg('PROT_MID', 'send', terminals('Q301', ['1', '2', '3'], 'PROT_MID'), terminals('Q302', ['1', '2', '3'], 'PROT_MID')),
        leg('SERIES_OUT', 'send', terminals('Q302', ['5', '6', '7', '8'], 'SERIES_OUT'), terminals('JP301', ['1'], 'SERIES_OUT')),
        leg('VOUT_PROTECTED', 'send', terminals('JP301', ['2'], 'VOUT_PROTECTED'), terminals('R401', ['1'], 'VOUT_PROTECTED')),
        leg('LOAD_5V1', 'send', terminals('R401', ['4'], 'LOAD_5V1'), terminals('J502', ['1'], 'LOAD_5V1')),
        leg('GND', 'return', terminals('J502', ['2'], 'GND'), cap_gnd),
    ]
    # J502's physical connector has exactly one force pin per pole in this V1A.
    # Kelvin sense pads never stand in for R401 force pads.
    copper = {side: (sum(v['resistance_mohm'] for v in legs if v['side'] == side)
                     if all(v['status'] == 'CALCULATED' for v in legs if v['side'] == side) else None)
              for side in ('send', 'return')}
    total = drop = pi = margin = None
    exceeded = [side for side in copper if copper[side] is not None and copper[side] > budget['copper_mohm'][side]+1e-9]
    if all(v is not None for v in copper.values()):
        total = sum(copper.values())+sum(budget['fixed_mohm'].values())
        drop = total*budget['load_A']  # mV
        pi = budget['buck_min_V']-drop/1000-budget['trough_V']
        margin = (pi-budget['pi_floor_V'])*1000
    if issues or any(v['status'] == 'OPEN' for v in legs):
        status = 'OPEN'
    elif exceeded or margin < 0:
        status = 'FAIL'
    else:
        status = 'CONDITIONAL PASS'
    return dict(status=status, classification='CALCULATED under ASSUMED conditions; not electrically validated',
                board_sha256=hashlib.sha256(text.encode()).hexdigest(), settings=vars(settings), budget=budget,
                issues=issues, legs=legs, copper_mohm=copper, copper_exceeded=exceeded,
                total_copper_mohm=sum(copper.values()) if all(v is not None for v in copper.values()) else None,
                total_loop_mohm=total, drop_5A_mV=drop, pi_min_V=pi, margin_mV=margin,
                thermal_traces=b.thermal,
                assumptions=[
                    '70/35 um defaults are ASSUMED finished copper; temp-c is copper temperature, not ambient.',
                    'rho20=1.724e-8 ohm m, alpha20=0.00393/K; via plating default 25 um; drill is finished bore.',
                    'Through-hole layer hops each charged full board thickness; blind/buried depths remain OPEN.',
                    'Minimum-resistance single corridor at 5 A; no parallel current-sharing credit.',
                    'Zone width=min(cap,2*minimum clearance along edge); saved fills only; grid may miss narrow paths.',
                    'Pad spreading uses a land-width strip (annulus-limited for holes); solder covered by frozen allocation.',
                    'Thermal: IPC-2152-style conservative screen, legacy IPC-2221 internal envelope k=.024 on ALL layers; no chart corrections.',
                    'Thermal rise is per trace at full 5 A, independent of DC copper temperature; cooling and mutual heating OPEN.',
                    'JP301 fitted link is ASSUMED; its unbudgeted contact/bulk resistance is OPEN, not board copper.',
                    'Endpoint is C209-C214 output bank; upstream inductor/JP202 and regulator dynamics excluded.',
                ])


def report(result):
    print('NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED')
    print(f"STATUS: {result['status']} — {result['classification']}")
    for leg in result['legs']:
        r = leg['resistance_mohm']
        detail = f'{r:.6f} mOhm' if r is not None else 'OPEN: '+leg['reason']
        print(f"{leg['side']:6} {leg['net']:16} copper: {detail}")
        if r is not None:
            totals = defaultdict(float)
            for e in leg['path']:
                totals[e['kind']] += e['resistance_mohm']
            print('       '+', '.join(f'{k}={v:.6f} mOhm' for k, v in sorted(totals.items())))
    for side, r in result['copper_mohm'].items():
        amount = 'OPEN' if r is None else f'{r:.6f} mOhm'
        print(f"CALCULATED {side} copper: {amount}; allocation {result['budget']['copper_mohm'][side]:.6f} mOhm")
    print(f"ASSUMED frozen non-copper allocations: {sum(result['budget']['fixed_mohm'].values()):.9f} mOhm")
    for key, title, unit in [('total_copper_mohm', 'total copper', 'mOhm'),
                              ('total_loop_mohm', 'total SEND+RETURN', 'mOhm'),
                              ('drop_5A_mV', 'drop at 5 A', 'mV'), ('pi_min_V', 'worst-case Pi including trough', 'V'),
                              ('margin_mV', 'margin vs 4.75 V', 'mV')]:
        v = result[key]
        print(f"CALCULATED {title}: "+('OPEN (no complete path)' if v is None else f'{v:.9f} {unit}'))
    for side in result['copper_exceeded']:
        print(f'FAIL: {side} copper exceeds frozen allocation')
    for issue in result['issues']:
        print('OPEN: '+issue)
    print('CALCULATED / ASSUMED IPC-2152-style per-trace screen (legacy internal envelope):')
    if not result['thermal_traces']:
        print('  OPEN: no routed path traces; no temperature rise can be assigned')
    for t in result['thermal_traces']:
        print(f"  {t['id']} {t['net']} {t['layer']} L={t['length_mm']:.4f} mm W={t['width_mm']:.4f} mm "
              f"Cu={t['thickness_um']:g} um: rise@5A={t['rise_5A_C']:.3f} C")
    for assumption in result['assumptions']:
        print('ASSUMED: '+assumption)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('board', type=Path)
    for name, default in [('copper-um-outer', 70), ('copper-um-inner', 35), ('temp-c', 85),
                          ('via-plating-um', 25), ('zone-grid-mm', 1), ('zone-width-cap-mm', 1)]:
        parser.add_argument('--'+name, type=float, default=default)
    parser.add_argument('--json', action='store_true', help='machine-readable report on stdout')
    args = parser.parse_args(argv)
    try:
        settings = Settings(**{k: v for k, v in vars(args).items() if k not in ('board', 'json')})
        result = check(args.board.read_text(), settings)
    except (OSError, ValueError, KeyError, IndexError, TypeError, StopIteration, OverflowError, RecursionError) as exc:
        result = dict(status='OPEN', error=f'{type(exc).__name__}: {exc}')
        if args.json:
            print(json.dumps(result, indent=2, allow_nan=False))
        else:
            print('STATUS: OPEN — input/model error: '+result['error'])
        return 1
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
    else:
        report(result)
    return 0 if result['status'] == 'CONDITIONAL PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
