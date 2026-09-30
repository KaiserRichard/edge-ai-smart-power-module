#!/usr/bin/env python3
"""Reproduce Gate 2b presentation from the pinned electrical baseline.

Only geometry, text placement and wire/label representation are changed. Run
check_schematic_readability.py on fresh KiCad exports before accepting output.
Coordinates below are in 100 mil drawing units. No PCB operations.
"""
import argparse
import copy
import heapq
import json
import math
from pathlib import Path
import re
import subprocess
import textwrap
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = 'c47409fb2637c94ccaa685c3ac4cbbd10681d5a2'
HW = ROOT/'hardware/kicad'
UNIT = 2.54
NAMESPACE = uuid.UUID('a90c68b0-7f9f-46d1-9d67-4c9d60c345f1')

def q(s): return json.dumps(str(s), ensure_ascii=False)
def val(s): return json.loads(s) if s.startswith('"') else s
def parse(s):
    stack=[]; root=None
    for tok in re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s):
        if tok=='(':
            node=[]
            if stack: stack[-1].append(node)
            else: root=node
            stack.append(node)
        elif tok==')': stack.pop()
        else: stack[-1].append(tok)
    assert not stack
    return root

def dump(t, level=0):
    if not isinstance(t,list): return t
    if not any(isinstance(v,list) for v in t): return '('+' '.join(t)+')'
    return '('+' '.join(dump(v,level+1) if not isinstance(v,list) else '\n'+'  '*(level+1)+dump(v,level+1) for v in t)+')'

def nodes(t,key): return [x for x in t if isinstance(x,list) and x[0]==key]
def one(t,key): return next(x for x in t if isinstance(x,list) and x[0]==key)
def replace(t,key,v):
    for i,x in enumerate(t):
        if isinstance(x,list) and x[0]==key: t[i]=v; return
    t.append(v)
def atom(*a): return [str(x) for x in a]
def xy(x): return f'{float(x)*UNIT:.4f}'.rstrip('0').rstrip('.')
def at(x,y,a=0): return ['at',xy(x),xy(y),str(a)]
def effects(size=1.524,justify=None):
    e=['effects',['font',['size',str(size),str(size)]]]
    if justify: e.append(['justify',*justify.split()])
    return e

def source(name): return parse(subprocess.check_output(['git','show',f'{BASE}:hardware/kicad/{name}'],cwd=ROOT,text=True))
def prop(t,name): return next(x for x in nodes(t,'property') if val(x[1])==name)
def uid(s): return ['uuid',q(uuid.uuid5(NAMESPACE,s))]

def allpins(lib): return [p for unit in nodes(lib,'symbol') for p in nodes(unit,'pin')]

# Pin order changes are graphical only. Numbers, names and electrical types are
# taken verbatim from the baseline embedded library, never from these layouts.
PINS={
'U101': {'L':[1,2,5,3,4,6,7,12], 'R':[17,18,16,14,15,10,9], 'B':[8,25,11,13,19,20,21,22,23,24]},
'U201': {'L':[8,12,7,6,2], 'R':[10,14,13,4,5], 'B':[1,3,9,11]},
'U301': {'L':[1,4,2,5], 'R':[9,7,6,8], 'B':[3,11,10]},
'U302': {'L':[2], 'R':[6], 'B':[4,1,3,5,7,8]},
'U303': {'L':[3,4], 'R':[1], 'T':[5], 'B':[2]},
'U304': {'L':[1,2,6,7], 'R':[5,3], 'T':[8], 'B':[4]},
'U309': {'L':[1,2,6,7], 'R':[5,3], 'T':[8], 'B':[4]},
'U306': {'L':[8,5,7], 'R':[1,2,3], 'B':[4,9,6]},
'U307': {'L':[8,5,7], 'R':[1,2,3], 'B':[4,9,6]},
'U308': {'L':[5,3,4], 'R':[1], 'T':[6], 'B':[2]},
'U312': {'L':[1,2], 'R':[4], 'T':[5], 'B':[3]},
'U313': {'L':[2], 'R':[4], 'T':[5], 'B':[3,1]},
'U314': {'L':[2], 'R':[4], 'T':[5], 'B':[3,1]},
'U315': {'L':[6,5], 'R':[2,3], 'T':[1], 'B':[4]},
'U401': {'L':[10,9,8], 'R':[5,4,3], 'T':[6], 'B':[7,1,2]},
'U402': {'L':[1], 'R':[5], 'B':[2,3,4]},
'U403': {'L':[7,6,8,5], 'R':[2,3,1], 'B':[4]},
'Q101': {'L':[1,2,3], 'R':[5,6,7,8], 'B':[4]},
'Q102': {'L':[2], 'R':[3], 'B':[1]},
'Q301': {'L':[5,6,7,8], 'R':[1,2,3], 'B':[4]},
'Q302': {'L':[1,2,3], 'R':[5,6,7,8], 'B':[4]},
'Q303': {'T':[5,6,7,8], 'L':[4], 'B':[1,2,3]},
'Q304': {'L':[1], 'T':[3], 'B':[2]},
'D301': {'L':[1], 'R':[3], 'B':[2]},
'D302': {'L':[1], 'R':[3], 'B':[2]},
'J501': {'R':[1,2]}, 'J502': {'L':[1,2]}, 'J503': {'L':[2,3,4,1]},
'J301': {'L':[1,2]}, 'J302': {'L':[1,2]},
}
for ref in ('U305','U310','U311'):
    PINS[ref]={'L':[1,3,6],'R':[4],'T':[5],'B':[2]}

class Drawing:
    def __init__(self,name,key=None,paper='A3'):
        self.name=name; self.original=source(name+'.kicad_sch'); self.doc=copy.deepcopy(self.original)
        self.doc=[x for x in self.doc if not isinstance(x,list) or x[0] in ('version','generator','generator_version','uuid','paper','title_block','sheet_instances')]
        replace(self.doc,'paper',['paper',q(paper)])
        self.parts={val(prop(x,'Reference')[2]):copy.deepcopy(x) for x in nodes(self.original,'symbol')}
        self.libs={val(x[1]):copy.deepcopy(x) for x in one(self.original,'lib_symbols')[1:]}
        self.spec={} if not key else {c['ref']:c for c in json.loads((ROOT/f'docs/evidence/r2/{key}_block.json').read_text())['components']}
        self.serial=0; self.placed={}; self.libout={}; self.term={}; self.edges={}; self.blocks=[]; self.obstacles=set(); self.labels=set(); self.reserved={}
        self.text(name.replace('_',' ')+'  |  SCHEMATIC REVIEW',6,5,2.54)
        self.text('PRELIMINARY / R2 BLOCKED / NOT FOR FABRICATION',6,10,2.032)
    def add(self,s): self.doc.append(parse(s) if isinstance(s,str) else s)
    def ident(self): self.serial+=1; return uid(f'{self.name}:{self.serial}')
    def text(self,s,x,y,size=1.524): self.add(['text',q(s),at(x,y),effects(size,'left top'),self.ident()])
    def box(self,x1,y1,x2,y2,title,note):
        self.add(['rectangle',['start',xy(x1),xy(y1)],['end',xy(x2),xy(y2)],['stroke',['width','0.254'],['type','dash']],['fill',['type','none']],self.ident()])
        self.text(title,x1+2,y1+1,2.032); self.text(note,x1+2,y1+3.5)
        self.blocks.append((x1+1,y1+6,x2-1,y2-1,[]))
        return len(self.blocks)-1
    def label(self,net,p,right=False):
        if (net,p) in self.labels: return
        self.labels.add((net,p)); self.add(['label',q(net),at(*p,180 if right else 0),effects(1.524,'right bottom' if right else 'left bottom'),self.ident()])
    def port(self,net,p):
        orig=next(h for h in nodes(self.original,'hierarchical_label') if val(h[1])==net)
        h=copy.deepcopy(orig); replace(h,'at',at(*p)); replace(h,'effects',effects(1.524,'left')); self.add(h)
        end=(p[0]-3,p[1]); self.path(net,[p,end]); self.label(net,end,True)
    def path(self,net,points):
        for p,t in zip(points,points[1:]):
            assert p[0]==t[0] or p[1]==t[1],(p,t)
            p=tuple(p);t=tuple(t)
            dx=0 if p[0]==t[0] else (1 if t[0]>p[0] else -1)
            dy=0 if p[1]==t[1] else (1 if t[1]>p[1] else -1)
            cur=p
            while cur!=t:
                nxt=(cur[0]+dx,cur[1]+dy); edge=tuple(sorted((cur,nxt)))
                assert edge not in self.edges or self.edges[edge]==net,('wire overlap',net,self.edges.get(edge),edge)
                self.edges[edge]=net;cur=nxt
    def pin(self,ref,n): return self.placed[ref]['pins'][str(n)][0]
    def place(self,ref,x,y,block,vertical=False,width=12,field_at=None):
        assert ref not in self.placed,ref
        inst=self.parts[ref]; libid=val(one(inst,'lib_id')[1]); lib=copy.deepcopy(self.libs[libid]); pins=allpins(lib)
        mapping={val(one(p,'number')[1]):p for p in pins}
        kind=self.spec[ref]['kind']; simple=len(pins)==2 and kind not in ('CONNECTOR',)
        pinloc={}; rect=None
        if simple:
            if kind=='TVS_BI':
                # Compact neutral TVS block; keep both baseline passive pin IDs.
                subname=val(lib[1]).split(':')[-1]
                glyph=parse(f'(symbol {q(subname+"_0_1")} (rectangle (start -2.54 1.27) (end 2.54 -1.27) (stroke (width 0.254) (type default)) (fill (type none))))')
                for i,p in enumerate(pins):replace(p,'at',at(-2 if i==0 else 2,0,0 if i==0 else 180));replace(p,'length',['length','2.54'])
                lib=[v for v in lib if not isinstance(v,list) or v[0]!='symbol']+[glyph,['symbol',q(subname+'_1_1'),*pins]]
                replace(lib,'pin_names',['pin_names',['offset','0.762'],['hide','yes']])
            # Retain original glyph (including capacitor polarity and diode bar).
            if vertical:
                def rotate(t):
                    for c in t:
                        if not isinstance(c,list): continue
                        if c[0] in ('xy','start','end','center','at'):
                            a,b=float(c[1]),float(c[2]);c[1],c[2]=str(b),str(-a)
                            if c[0]=='at' and len(c)>3:c[3]=str((float(c[3])+270)%360)
                        else:rotate(c)
                for sub in nodes(lib,'symbol'):rotate(sub)
            for n,p in mapping.items():
                a=one(p,'at');px,py=float(a[1])/UNIT,-float(a[2])/UNIT
                angle=float(a[3]); d={0:(-1,0),90:(0,1),180:(1,0),270:(0,-1)}[angle]
                pinloc[n]=((int(round(x+px)),int(round(y+py))),d)
            rect=(x-1,y-1,x+1,y+1)
            rx,ry=(x+2,y-1.5) if vertical else (x,y-4)
            justify='left' if vertical else None
        elif kind in ('FLAG','TP'):
            n=next(iter(mapping));pinloc[n]=((x,y),(0,1));rect=(x-1,y-2,x+1,y-1);rx,ry=x,y-5;justify=None
        elif kind=='SHUNT':
            for n,p in mapping.items():
                a=one(p,'at');px,py=float(a[1])/UNIT,-float(a[2])/UNIT
                # Baseline Kelvin glyph has half-grid pins. Move consistently to integer grid.
                sx,sy=round(px),round(py);replace(p,'at',at(sx,-sy,int(float(a[3]))));pinloc[n]=((x+sx,y+sy),(-1,0) if sx<0 else (1,0))
            rect=(x-4,y-2,x+4,y+1);rx,ry=x,y-6;justify=None
        else:
            sides=PINS.get(ref)
            if sides is None:
                nums=list(mapping);sides={'L':nums[:(len(nums)+1)//2],'R':nums[(len(nums)+1)//2:]}
            assert {str(n) for ns in sides.values() for n in ns}==set(mapping),(ref,sides,set(mapping))
            w=max(width,max(len(sides.get(s,[]))*2 for s in ('T','B'))+2)
            h=max(6,max(len(sides.get(s,[]))*2 for s in ('L','R'))+ (4 if ref in ('U101','U301','U306','U307') else 2))
            w=math.ceil(w/2)*2;h=math.ceil(h/2)*2
            geom=parse(f'(symbol {q(val(lib[1]).split(":")[-1]+"_0_1")} (rectangle (start {xy(-w/2)} {xy(h/2)}) (end {xy(w/2)} {xy(-h/2)}) (stroke (width 0.254) (type default)) (fill (type background))))')
            for side,nums in sides.items():
                for i,n in enumerate(nums):
                    n=str(n);off=2*i-(len(nums)-1)
                    if side in ('L','R'):px=(-w//2-1 if side=='L' else w//2+1);py=off;angle=0 if side=='L' else 180;d=(-1,0) if side=='L' else (1,0)
                    else:px=off;py=(-h//2-1 if side=='T' else h//2+1);angle=270 if side=='T' else 90;d=(0,-1) if side=='T' else (0,1)
                    replace(mapping[n],'at',at(px,-py,angle));replace(mapping[n],'length',['length','2.54']);pinloc[n]=((x+px,y+py),d)
            unit=['symbol',q(val(lib[1]).split(':')[-1]+'_1_1'),*mapping.values()]
            lib=[v for v in lib if not isinstance(v,list) or v[0]!='symbol']+[geom,unit]
            replace(lib,'pin_names',['pin_names',['offset','1.016']])
            rect=(x-w//2,y-h//2,x+w//2,y+h//2);rx,ry=x,y-h//2-(7 if sides.get("T") else 4);justify=None
        if field_at is not None:rx,ry,justify=field_at
        for p in allpins(lib):
            for field in ('name','number'):replace(one(p,field),'effects',effects(1.524))
        replace(inst,'at',at(x,y))
        for pn,yy in [('Reference',ry),('Value',ry+1.7)]:
            pr=prop(inst,pn);replace(pr,'at',at(rx,yy));replace(pr,'effects',effects(1.524,justify))
        for pr in nodes(inst,'property'):
            if val(pr[1]) not in ('Reference','Value'):replace(pr,'at',at(x,y))
        self.add(inst);self.libout[libid]=lib
        self.placed[ref]={'pins':pinloc,'block':block,'rect':rect}
        self.blocks[block][4].append(ref)
        for xx in range(math.floor(rect[0]),math.ceil(rect[2])+1):
            for yy in range(math.floor(rect[1]),math.ceil(rect[3])+1):self.obstacles.add((xx,yy))
        # Reserve the two visible fields. Vertical passives put text beside body.
        value=val(prop(inst,'Value')[2]);tw=max(len(ref),len(value))*0.36
        lx=rx if justify else rx-tw/2
        for xx in range(math.floor(lx),math.ceil(lx+tw)+1):
            for yy in range(math.floor(ry-0.5),math.ceil(ry+2.5)+1):self.obstacles.add((xx,yy))
        for n,(p,d) in pinloc.items():
            net=self.spec[ref]['pins'][n]['net'];self.reserved[p]=net
            if net is None:self.add(['no_connect',at(*p)[:3],self.ident()]);continue
            end=(p[0]+d[0]*2,p[1]+d[1]*2)
            self.reserved[end]=net
            self.path(net,[p,end]);self.term[(ref,n)]=(net,end)
    def route(self):
        # Route each functional box independently; named inter-box links are long
        # connections. The main power chain is explicitly wired by each layout.
        for x1,y1,x2,y2,refs in self.blocks:
            groups={}
            for (r,n),(net,p) in self.term.items():
                if r in refs:groups.setdefault(net,[]).append(p)
            # Signals first; ground last can cross but never join unrelated wires.
            for net,pts in sorted(groups.items(),key=lambda item:(item[0]=='GND',len(item[1]))):
                pts=list(dict.fromkeys(pts));tree={pts[0]}
                for target in pts[1:]:
                    route=self.search(target,tree,net,(x1,y1,x2,y2))
                    self.path(net,route);tree.update(route)
                # Name each connected wire network once. Choose free space along
                # its conductors, keeping text out of bodies and value fields.
                points={p for edge,n in self.edges.items() if n==net for p in edge
                        if x1<=p[0]<=x2 and y1<=p[1]<=y2}
                candidates=[];tw=len(net)*0.38
                occupied_labels=set()
                for lname,lp in self.labels:
                    for xx in range(math.floor(lp[0]-len(lname)*0.38),math.ceil(lp[0]+len(lname)*0.38)+1):
                        for yy in (lp[1]-1,lp[1]):occupied_labels.add((xx,yy))
                for p in points:
                    if any(n!=net and p in edge for edge,n in self.edges.items()):continue
                    for right in (False,True):
                        lx=p[0]-tw if right else p[0];rx=lx+tw
                        area={(xx,yy) for xx in range(math.floor(lx),math.ceil(rx)+1) for yy in (p[1]-1,p[1])}
                        if lx<x1 or rx>x2 or p[1]<y1+1:continue
                        collisions=len(area & self.obstacles)*30+len(area & occupied_labels)*10
                        distance=min(abs(p[0]-t[0])+abs(p[1]-t[1]) for t in pts)
                        # Prefer upper segments and points close to their pins.
                        score=collisions+distance*0.2+(p[1]-y1)*0.02
                        candidates.append((score,p,right))
                if candidates:
                    _,p,right=min(candidates);self.label(net,p,right)
                else:self.label(net,pts[0])
    def search(self,start,goals,net,bounds):
        x1,y1,x2,y2=bounds
        occupancy={};directions={}
        for (a,b),n in self.edges.items():
            for p in (a,b):
                occupancy.setdefault(p,set()).add(n);directions.setdefault((p,n),set()).add('H' if a[1]==b[1] else 'V')
        heuristic=lambda p:min(abs(p[0]-g[0])+abs(p[1]-g[1]) for g in goals)
        queue=[(heuristic(start),0,start,None)];cost={(start,None):0};prev={};end=None
        while queue:
            _,g,p,d=heapq.heappop(queue)
            if g!=cost.get((p,d)):continue
            if p in goals:end=(p,d);break
            for dx,dy,nd in ((1,0,'H'),(-1,0,'H'),(0,1,'V'),(0,-1,'V')):
                t=(p[0]+dx,p[1]+dy)
                if not(x1<=t[0]<=x2 and y1<=t[1]<=y2):continue
                if t in self.obstacles and t not in goals and t!=start:continue
                if t in self.reserved and self.reserved[t]!=net:continue
                foreign=occupancy.get(t,set())-{net}
                current=occupancy.get(p,set())-{net}
                if current and (d!=nd or any(nd in directions[p,n] for n in current)):continue
                if foreign and any(nd in directions[t,n] or len(directions[t,n])!=1 for n in foreign):continue
                edge=tuple(sorted((p,t)))
                if edge in self.edges and self.edges[edge]!=net:continue
                ng=g+1+(0.8 if d and d!=nd else 0)+(8 if foreign else 0)
                state=(t,nd)
                if ng<cost.get(state,1e99):cost[state]=ng;prev[state]=(p,d);heapq.heappush(queue,(ng+heuristic(t),ng,t,nd))
        if end is None:raise RuntimeError(f'{self.name}: cannot route {net} {start} to {goals}')
        route=[]
        while end in prev:route.append(end[0]);end=prev[end]
        route.append(start);return list(reversed(route))
    def notes(self,y,width=110):
        texts=[val(t[1]) for t in nodes(self.original,'text') if '\n' in val(t[1])]
        self.text('DESIGN NOTES / EXISTING ENGINEERING LIMITATIONS',6,y,2.032)
        if self.name=='03_OUTPUT_PROTECTION':
            lines=[line for s in texts for line in s.splitlines()]
            for col,chunk in enumerate((lines[:6],lines[6:])):
                yy=y+3
                for line in chunk:
                    for ln in textwrap.wrap(line,width=145,break_long_words=False):
                        self.text(ln,6+col*107,yy);yy+=1.25
            return
        for s in texts:
            for line in s.splitlines():
                for ln in textwrap.wrap(line,width=min(width,110),break_long_words=False):y+=1.8;self.text(ln,6,y+2)
    def save(self):
        assert set(self.parts)==set(self.placed),(self.name,set(self.parts)-set(self.placed))
        self.route()
        # Remove unused routing tails; preserve every pin, label and hierarchy end.
        keep={p for info in self.placed.values() for p,di in info['pins'].values()} | {p for n,p in self.labels}
        keep.update(tuple(round(float(v)/UNIT) for v in one(h,'at')[1:3]) for h in nodes(self.doc,'hierarchical_label'))
        keep.update(tuple(round(float(v)/UNIT) for v in one(p,'at')[1:3]) for h in nodes(self.doc,'sheet') for p in nodes(h,'pin'))
        while True:
            degrees={}
            for edge,net in self.edges.items():
                for p in edge:degrees[net,p]=degrees.get((net,p),0)+1
            tails=[edge for edge,net in self.edges.items() if any(degrees[net,p]==1 and p not in keep for p in edge)]
            if not tails:break
            for edge in tails:del self.edges[edge]
        # Collapse unit edges into maximal straight runs, split at actual T nodes.
        adjacency={}
        for (a,b),net in self.edges.items():
            adjacency.setdefault((net,a),set()).add(b);adjacency.setdefault((net,b),set()).add(a)
        seen=set()
        for (net,p),near in adjacency.items():
            if len(near)>2 or (len(near)==2 and p in keep):self.add(['junction',at(*p)[:3],['diameter','0'],['color','0','0','0','0'],self.ident()])
            for t in near:
                e=tuple(sorted((p,t)))
                if e in seen:continue
                seen.add(e);end=t;prior=p
                while len(adjacency[net,end])==2 and end not in keep:
                    nxt=next(a for a in adjacency[net,end] if a!=prior)
                    if (end[0]-prior[0],end[1]-prior[1])!=(nxt[0]-end[0],nxt[1]-end[1]):break
                    seen.add(tuple(sorted((end,nxt))));prior,end=end,nxt
                self.add(['wire',['pts',['xy',xy(p[0]),xy(p[1])],['xy',xy(end[0]),xy(end[1])]],['stroke',['width','0'],['type','default']],self.ident()])
        self.doc.append(['lib_symbols',*self.libout.values()])
        if self.name=='03_OUTPUT_PROTECTION':
            # Fit A3, then quantize global connection endpoints onto the existing
            # 50-mil grid. Visible text remains at least 1.27 mm.
            def compact(tree):
                for item in tree:
                    if not isinstance(item,list):continue
                    key=item[0]
                    if key in ('at','xy','start','end','center'):
                        item[1:3]=[f'{float(v)*0.7:.6f}'.rstrip('0').rstrip('.') for v in item[1:3]]
                    elif key in ('length','offset','radius'):
                        item[1]=str(float(item[1])*0.7)
                    elif key=='size' and len(item)==3:
                        item[1:]=[str(max(1.27,float(v)*0.7)) for v in item[1:]]
                    else:compact(item)
            compact(self.doc)
            # Page margin translation applies to placed objects, not local glyphs.
            def margin(tree):
                for item in tree:
                    if not isinstance(item,list):continue
                    if item[0] in ('at','xy','start','end','center'):
                        item[1:3]=[str(round(float(v)+2.54,6)) for v in item[1:3]]
                    else:margin(item)
            for obj in self.doc:
                if isinstance(obj,list) and obj[0] in ('symbol','wire','label','hierarchical_label','no_connect','junction','text','rectangle'):
                    margin(obj)
            def snap(v):return round(float(v)/1.27)*1.27
            # Library IDs are per-reference. Offset each pin to the snapped
            # world position before snapping its placed instance.
            for inst in nodes(self.doc,'symbol'):
                loc=one(inst,'at');ix,iy=map(float,loc[1:3])
                lib=self.libout[val(one(inst,'lib_id')[1])]
                for pin in allpins(lib):
                    pinat=one(pin,'at');px,py=map(float,pinat[1:3])
                    pinat[1]=str(round(snap(ix+px)-snap(ix),6))
                    pinat[2]=str(round(snap(iy)-snap(iy-py),6))
            def snap_connections(tree):
                for item in tree:
                    if not isinstance(item,list):continue
                    if item[0] in ('at','xy'):
                        item[1:3]=[str(round(snap(v),6)) for v in item[1:3]]
                    elif item[0]!='property':snap_connections(item)
            for obj in self.doc:
                if isinstance(obj,list) and obj[0] in ('symbol','wire','label','hierarchical_label','no_connect','junction'):
                    snap_connections(obj)
            replace(self.doc,'paper',['paper',q('A3')])
        (HW/(self.name+'.kicad_sch')).write_text(dump(self.doc)+'\n')
        return self.libout

def input_sheet():
    d=Drawing('01_INPUT_PROTECTION','input')
    a=d.box(5,17,69,56,'INPUT / REVERSE PROTECTION','Fuse, TVS and external reverse-blocking stage')
    b=d.box(72,17,158,88,'EFUSE / SUPERVISION','TPS26630 controls cutoff, inrush and input current')
    c=d.box(5,59,69,88,'UVLO / OVP DIVIDERS','Existing thresholds: UV ~8.46 V; OV ~27.63 V')
    for r,x,y,v in [('F101',18,32,False),('D101',28,44,True),('C101',39,44,True),('Q101',53,33,False),('Q102',52,49,False),('#FLG101',28,28,False)]:d.place(r,x,y,a,v,width=8)
    for r,x,y,v in [('U101',112,41,False),('C102',84,33,True),('C103',139,60,True),('R105',151,56,True),('D102',150,31,True),('R106',142,73,True),('R107',142,82,True),('R108',130,72,True),('TP101',83,75,False),('TP102',127,84,False),('#FLG102',77,30,False)]:d.place(r,x,y,b,v,width=20)
    for r,x,y in [('R101',22,72),('R102',22,81),('R103',48,72),('R104',48,81)]:d.place(r,x,y,c,True)
    # Power conductors across the block boundary, attached at real pin endpoints.
    p=d.pin('Q101',5);t=d.pin('U101',1);d.path('VIN_EFUSE_IN',[p,(70,p[1]),(70,t[1]),t])
    ports=['VIN_RAW','VIN_FUSED','VIN_PROTECTED','BUCK_INPUT_PGOOD','INPUT_SHDN','GND']
    for i,n in enumerate(ports):d.port(n,(15+25*i,15))
    d.notes(92,175);return d

def buck_sheet():
    d=Drawing('02_BUCK_5V','buck')
    a=d.box(5,20,53,85,'INPUT / ENABLE','Input bypass and upstream PGOOD qualification')
    b=d.box(56,20,105,85,'BUCK CONVERTER','LM61460 with local timing and bootstrap parts')
    c=d.box(108,20,158,91,'OUTPUT / FEEDBACK','Inductor, output bank and local 5.1 V feedback')
    for r,x,y in [('C201',14,40),('C202',25,40),('C203',36,40),('C204',46,40),('R206',20,63),('R207',20,74)]:d.place(r,x,y,a,True)
    d.place('U201',78,44,b,width=16)
    for r,x,y,v in [('R201',61,72,True),('C206',76,72,True),('R204',96,62,True),('C205',96,33,True)]:d.place(r,x,y,b,v)
    d.place('L201',118,40,c)
    for i,r in enumerate(['C209','C210','C211','C212','C213','C214']):d.place(r,114+(i%3)*15,52+(i//3)*13,c,True)
    for r,x,y,v in [('R202',117,75,True),('R203',117,85,True),('C207',139,75,False),('R205',151,79,True)]:d.place(r,x,y,c,v)
    p=d.pin('U201',10);t=d.pin('L201',1);d.path('BUCK_SW',[p,(106,p[1]),(106,t[1]),t])
    p=d.pin('C204',1);t=d.pin('U201',8);d.path('VIN_PROTECTED',[p,(p[0],28),(54,28),(54,t[1]),t])
    for i,n in enumerate(['VIN_PROTECTED','BUCK_INPUT_PGOOD','VOUT_5V1','BUCK_PGOOD','GND']):d.port(n,(20+31*i,16))
    d.notes(95,175);return d

def output_sheet():
    d=Drawing('03_OUTPUT_PROTECTION','output','A2')
    a=d.box(5,20,77,51,'RAW BULK / FAULT-RISE BUFFER','Eight 470 uF capacitors remain upstream of disconnect')
    b=d.box(80,20,154,51,'OPPOSED SERIES FETS','Common sources = PROT_MID; no bypass fitted')
    c=d.box(157,20,228,51,'DRAIN BALLAST / CROWBAR','(R308 + R309) || (R310 + R311) = 33 mOhm')
    for i in range(8):d.place(f'C{330+i}',12+8*i,38,a,True)
    d.place('TP301',15,30,a,field_at=(20,27,'left'))
    for r,x,y in [('Q301',98,35),('Q302',132,35),('TP304',115,42),('TP302',150,42),('#FLG302',151,30)]:d.place(r,x,y,b,width=10)
    for r,x,y in [('R308',168,31),('R309',181,31),('R310',168,42),('R311',181,42)]:d.place(r,x,y,c)
    d.place('Q303',210,38,c,width=10)
    # Route the main rail across raw-bank, disconnect and crowbar boxes.
    p=d.pin('C330',1);t=d.pin('Q301',5);d.path('VOUT_5V1',[p,(p[0],29),(78,29),(78,t[1]),t])
    p=d.pin('Q301',1);t=d.pin('Q302',1);d.path('PROT_MID',[p,(115,p[1]),(115,t[1]),t])
    p=d.pin('Q302',5);t=d.pin('R308',1);d.path('VOUT_PROTECTED',[p,(155,p[1]),(155,t[1]),t])
    e=d.box(5,55,84,95,'INDEPENDENT AUXILIARY SUPPLIES','VIN_FUSED feeds detector and gate-drive LDO rails')
    f=d.box(87,55,136,95,'SERIES GATE DRIVE','Source-referenced LTC7001 drives the common gate')
    g=d.box(139,55,185,95,'REFERENCE / OV DETECTOR','Existing 5.325 V nominal trip; clamp to sinking reference')
    h=d.box(188,55,228,95,'CROWBAR GATE DRIVE','UCC27511 drives Q303; resistor limits gate charge current')
    d.place('D303',13,68,e);d.place('#FLG301',21,66,e)
    for r,x,y in [('C307',13,83),('R323',23,83)]:d.place(r,x,y,e,True)
    for ref,x in [('U306',39),('U307',66)]:d.place(ref,x,72,e,width=10)
    for r,x,y in [('R312',47,84),('R313',47,91),('C305',54,84),('C312',30,89),('R314',73,84),('R315',73,91),('C306',78,80),('C313',58,91)]:d.place(r,x,y,e,True)
    d.place('U301',104,75,f,width=10)
    for r,x,y,v in [('D302',121,66,False),('C301',129,76,True),('R304',117,78,False),('R305',123,88,False),('C308',92,88,True),('C309',103,88,True),('TP305',131,90,False)]:d.place(r,x,y,f,v,width=6,field_at=(116,80,'left') if r=='R304' else None)
    d.place('U302',151,68,g,width=12);d.place('U303',174,83,g,width=8,field_at=(172,90.5,None))
    for r,x,y,v in [('C303',144,88,True),('C302',158,88,True),('R301',168,66,True),('R302',168,74,True),('R303',158,79,False),('D301',180,66,False),('C304',179,91,True),('TP303',161,69,False)]:d.place(r,x,y,g,v,width=4)
    d.place('U315',200,75,h,width=8)
    for r,x,y,v in [('C310',192,89,True),('C311',204,89,True),('R306',215,72,False),('R307',219,85,True)]:d.place(r,x,y,h,v)
    j=d.box(5,99, 60,140,'SUPPLY VALID / RESET','Reset and reference delay qualify control enable')
    k=d.box(63,99,114,140,'ARM / HISTORY CLOCK','Manual ARM with RC delay; no automatic retry')
    l=d.box(117,99,174,140,'QUALIFICATION / LATCHES','Fault clears run latch; history persists until RESET')
    m=d.box(177,99,228,140,'RUN / FAULT ACTION','Run requires both latches; fault asserts crowbar and SHDN')
    for r,x,y,v in [('U308',17,115,False),('U312',43,128,False),('J302',47,112,False),('R316',30,109,True),('R318',36,109,True),('C314',9,130,True),('C315',20,132,True),('C322',54,131,True)]:d.place(r,x,y,j,v,width=8,field_at=None)
    for r,x,y,v in [('J301',76,112,False),('U313',85,124,False),('U314',104,124,False),('R319',65,118,True),('C316',73,134,True),('R320',94,112,False),('C317',96,135,True),('C323',85,135,True),('C324',108,135,True)]:d.place(r,x,y,k,v,width=6)
    for r,x,y,v in [('U310',129,112,False),('U304',133,127,False),('U309',158,127,False),('R317',145,110,True),('C321',120,120,True),('C318',120,135,True),('C320',170,135,True)]:d.place(r,x,y,l,v,width=8,field_at=(138,106,'left') if r=='U310' else (141,119,'left') if r=='U304' else None)
    for r,x,y,v in [('U305',188,115,False),('U311',201,131,False),('Q304',221,131,False),('R321',208,111,True),('R322',213,135,True),('C319',179,124,True),('C325',223,115,True)]:d.place(r,x,y,m,v,width=8,field_at=None)
    for i,n in enumerate(['VOUT_5V1','VIN_FUSED','BUCK_PGOOD','INPUT_SHDN','VOUT_PROTECTED','GND']):d.port(n,(21+38*i,16))
    # Compact guide replaces long duplicated calculation prose; full evidence remains in docs.
    d.text('HOW TO READ: DETECTOR -> LATCH -> SERIES SWITCH + CROWBAR',6,145,2.032)
    for i,line in enumerate([
        '1  U302 reference + R301/R302 divider -> U303 OV_OK (nominal trip 5.325 V).',
        '2  U308/U312 qualify supply/reset; U310 qualifies OV_OK and BUCK_PGOOD.',
        '3  ARM clock sets U304; U309 retains ARM_HISTORY until manual RESET.',
        '4  U305 RUN_GATE -> U301 -> opposed Q301/Q302: raw rail to protected rail.',
        '5  Fault clears run latch; U311 CROWBAR_ON -> U315 -> Q303 + ballast to GND.',
        '6  Q304 also asserts INPUT_SHDN. No automatic retry; RESET then ARM.',
        'OPEN: timing, SOA, stability and fault energy require review and physical tests.',
        'EVIDENCE: docs/evidence/r2/sheet03/; ERC does not validate electrical safety.'
    ]):d.text(line,6,149+i*1.4,1.85)
    return d

def monitor_sheet():
    d=Drawing('04_POWER_MONITOR','monitor')
    a=d.box(5,20,81,68,'KELVIN SHUNT / MEASUREMENT','Force path left to right; sense pins route only to differential filter')
    b=d.box(84,20,158,68,'LOCAL TELEMETRY SUPPLY','3.3 V regulator branches before the load-current shunt')
    c=d.box(5,71,158,92,'I2C DOMAIN SEPARATION','Local B side and host A side keep their existing pull-up domains')
    d.place('R401',27,34,a);d.place('U401',61,51,a,width=12)
    for r,x,y,v in [('R402',22,45,False),('R403',36,50,False),('C401',45,50,True),('C402',74,56,True),('R408',74,40,True),('TP401',68,64,False),('TP402',10,44,False),('TP403',40,41,False)]:d.place(r,x,y,a,v)
    d.place('U402',115,38,b,width=12)
    for r,x,y in [('C403',96,53),('C404',138,52)]:d.place(r,x,y,b,True)
    d.place('TP404',149,40,b)
    d.place('U403',83,83,c,width=14)
    for r,x,y in [('R404',26,83),('R405',42,83),('C406',60,83),('R406',108,83),('R407',124,83),('C405',141,83)]:d.place(r,x,y,c,True)
    for i,n in enumerate(['VOUT_PROTECTED','LOAD_5V1','3V3_HOST','SDA_HOST','SCL_HOST','GND']):d.port(n,(20+26*i,16))
    d.notes(96,175);return d

def io_sheet():
    d=Drawing('05_IO_TEST','io')
    a=d.box(5,23,56,61,'DC INPUT / J501','Bench supply enters VIN_RAW before all protection')
    b=d.box(59,23,108,61,'LOAD OUTPUT / J502','Protected and measured power leaves on LOAD_5V1')
    c=d.box(111,23,158,85,'HOST I2C / J503','Host supplies 3V3_HOST reference for its own I2C domain')
    e=d.box(5,65,108,85,'BENCH TEST ACCESS','Probe intermediate protected input and common return')
    for r,x,y in [('J501',19,41),('TP501',40,36),('#FLG501',49,47),('#FLG502',41,54)]:d.place(r,x,y,a,width=14)
    for r,x,y in [('J502',89,42),('TP503',68,36)]:d.place(r,x,y,b,width=16)
    for r,x,y in [('J503',140,44),('#FLG503',120,67)]:d.place(r,x,y,c,width=12)
    for r,x,y in [('TP502',28,79),('TP504',72,79)]:d.place(r,x,y,e)
    for i,n in enumerate(['VIN_RAW','VIN_PROTECTED','LOAD_5V1','3V3_HOST','SDA_HOST','SCL_HOST','GND']):d.port(n,(16+22*i,17))
    d.notes(91,175);return d


def root_sheet():
    d=Drawing('V1A')
    # Preserve hierarchy UUIDs, pin identities, sheet names and instance paths.
    sheets=sorted(nodes(d.original,'sheet'),key=lambda s:val(prop(s,'Sheetname')[2]));d.parts={}
    d.text('VIN_RAW  ->  01  ->  02  ->  03  ->  04  ->  J502',10,22,3.048)
    d.text('9-24 V DC input     |     5.1 V nominal / 5 A     |     I2C: 3.3 V, 100 kHz',10,29,2.032)
    positions=[(12,43,28,28),(49,43,28,28),(86,43,28,28),(123,43,28,28),(12,87,139,8)]
    power=[('VIN_RAW','VIN_PROTECTED'),('VIN_PROTECTED','VOUT_5V1'),('VOUT_5V1','VOUT_PROTECTED'),('VOUT_PROTECTED','LOAD_5V1')]
    summaries=['Input / reverse protection','Buck: LM61460 / 400 kHz','Disconnect + crowbar','INA228 / Kelvin shunt','J501 input / J502 load / J503 host']
    anchors={}
    for i,(original,(x,y,w,h)) in enumerate(zip(sheets,positions)):
        s=copy.deepcopy(original);replace(s,'at',at(x,y)[:3]);replace(s,'size',['size',xy(w),xy(h)])
        for pn,py in [('Sheetname',y-3),('Sheetfile',y+h-2)]:
            pr=prop(s,pn);replace(pr,'at',at(x+w/2,py));replace(pr,'effects',effects(2.032 if pn=='Sheetname' else 1.524))
            if pn=='Sheetfile':one(pr,'effects').append(['hide','yes'])
        pins=nodes(s,'pin');count=0
        for pin in pins:
            net=val(pin[1]);main=power[i] if i<4 else ()
            if net in main:
                side=0 if net==main[0] else 1;p=(x+side*w,y+7);angle=180 if side==0 else 0
            elif i==4:
                p=(x+8+count*19,y);count+=1;angle=90
            else:
                p=(x+2+count*6,y+h);count+=1;angle=270
            replace(pin,'at',at(*p,angle));replace(pin,'effects',effects(1.524,'left' if angle==180 else 'right' if angle==0 else 'left'))
            anchors[i,net]=p
            if net not in main:
                end=(p[0],p[1]-8 if i==4 else p[1]+3+(count%2)*3);d.path(net,[p,end]);d.label(net,end)
        d.add(s);d.text(summaries[i],x+2,y+(5 if i==4 else 13),1.524)
    for i in range(3):
        p,t=anchors[i,power[i][1]],anchors[i+1,power[i][1]]
        d.path(power[i][1],[p,t]);d.label(power[i][1],p)
    p=anchors[0,'VIN_RAW'];d.path('VIN_RAW',[(6,p[1]),p]);d.label('VIN_RAW',(6,p[1]))
    p=anchors[3,'LOAD_5V1'];d.path('LOAD_5V1',[p,(158,p[1]),(158,79)]);d.label('LOAD_5V1',(158,79));d.text('J502\nSheet 05',142,79,2.032)
    d.text('REVIEW BOUNDARY',8,100,2.032)
    d.text('Sheet 03 has no bypass. No MCU; V1B remains separate.\nR2 release and R3 PCB layout remain BLOCKED.\nERC is rule-check evidence, not electrical validation.\nReview: docs/05_SCHEMATIC_REVIEW.md; docs/R2_MANAGER_PACKET.md\nSource / pin / calculation evidence: docs/evidence/r2/',8,103,1.524)
    return d


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sheet',choices=['01','02','03','04','05','root'])
    args=parser.parse_args()
    libraries={}
    builders=dict(zip(['01','02','03','04','05','root'],[input_sheet,buck_sheet,output_sheet,monitor_sheet,io_sheet,root_sheet]))
    for build in ([builders[args.sheet]] if args.sheet else builders.values()):
        d=build();libraries.update(d.save());print('Redrawn',d.name,flush=True)
    lib=parse((HW/'V1A.kicad_sym').read_text())
    for i,s in enumerate(lib):
        if isinstance(s,list) and s[0]=='symbol' and 'V1A:'+val(s[1]) in libraries:
            replacement=copy.deepcopy(libraries['V1A:'+val(s[1])]);replacement[1]=s[1]
            old_fields={p[1] for p in nodes(s,'property')}
            replacement=[v for v in replacement if not isinstance(v,list) or (v[0]!='property' or v[1] in old_fields) and (v[0]!='embedded_fonts' or nodes(s,'embedded_fonts'))]
            lib[i]=replacement
    (HW/'V1A.kicad_sym').write_text(dump(lib)+'\n')

if __name__=='__main__':main()
