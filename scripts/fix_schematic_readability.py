#!/usr/bin/env python3
"""Apply verifier-requested presentation corrections to the reviewed drawings.

No values, footprints, pin identities or project/ERC settings are edited.
Run fresh exports, identity/ERC checks and rendered-PDF review after use.
"""
import argparse
from make_schematic_readable import *

READABLE_BASE = '2cd138f77190be0871c4b7bc9863db48079f5b74'

def reviewed(name):
    return parse(subprocess.check_output(['git','show',f'{READABLE_BASE}:hardware/kicad/{name}.kicad_sch'],cwd=ROOT,text=True))

def component(doc, ref):
    return next(s for s in nodes(doc,'symbol') if val(prop(s,'Reference')[2])==ref)

def field(doc, ref, name, x, y, justify=None):
    p=prop(component(doc,ref),name)
    replace(p,'at',['at',str(x),str(y),'0'])
    replace(p,'effects',effects(1.524,justify))

def move_label(doc, net, old, new):
    label=next(l for l in nodes(doc,'label') if val(l[1])==net and tuple(map(float,one(l,'at')[1:3]))==old)
    one(label,'at')[1:3]=list(map(str,new))

def write(doc,name):
    (HW/(name+'.kicad_sch')).write_text('\n'.join(line.rstrip() for line in dump(doc).splitlines())+'\n')

def fix_01():
    name='01_INPUT_PROTECTION';d=reviewed(name)
    for net,y in [('INPUT_PGTH',109.22),('INPUT_ILIM',114.3),('INPUT_DVDT',119.38)]:
        move_label(d,net,(320.04,y),(325.12,y))
    field(d,'C103','Value',363.22,157.48)
    write(d,name)

def fix_02():
    name='02_BUCK_5V';d=reviewed(name)
    field(d,'C212','Value',307.34,165.608,'left')
    field(d,'C213','Value',345.44,165.608,'left')
    write(d,name)

def arrange_output_text(d):
    """Place visible annotations in free panel space without shrinking text."""
    bounds=[tuple(map(float,one(b,'start')[1:]+one(b,'end')[1:])) for b in nodes(d,'rectangle')]
    def panel(p):
        return min(range(len(bounds)),key=lambda i:max(bounds[i][0]-p[0],0,p[0]-bounds[i][2])**2+max(bounds[i][1]-p[1],0,p[1]-bounds[i][3])**2)
    def pos(o):return tuple(map(float,one(o,'at')[1:3]))
    wires=[tuple(tuple(map(float,p[1:])) for p in one(w,'pts')[1:]) for w in nodes(d,'wire')]
    def intersect(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
    def wire_hit(b,wire):
        (x,y),(xx,yy)=wire
        return intersect(b,(min(x,xx)-.05,min(y,yy)-.05,max(x,xx)+.05,max(y,yy)+.05))
    bodies=[];pins=[];libs={val(l[1]):l for l in one(d,'lib_symbols')[1:]}
    for s in nodes(d,'symbol'):
        x,y=pos(s);lib=libs[val(one(s,'lib_id')[1])]
        # Package bodies and every pin corridor include their adjacent pin text.
        for unit in nodes(lib,'symbol'):
            for r in nodes(unit,'rectangle'):
                a=one(r,'start');b=one(r,'end');bodies.append((x+float(a[1])-.5,y-float(a[2])-.5,x+float(b[1])+.5,y-float(b[2])+.5))
        for p in allpins(lib):
            a=one(p,'at');px=x+float(a[1]);py=y-float(a[2]);ang=int(float(a[3]));length=float(one(p,'length')[1]);dx,dy={0:(1,0),180:(-1,0),90:(0,-1),270:(0,1)}[ang]
            ex,ey=px+dx*length,py+dy*length
            pins.append((min(px,ex)-.6,min(py,ey)-1.5,max(px,ex)+.6,max(py,ey)+1.1))
        if not any(nodes(u,'rectangle') for u in nodes(lib,'symbol')):bodies.append((x-2.5,y-2.5,x+2.5,y+2.5))
    occupied=[]
    for t in nodes(d,'text'):
        x,y=pos(t)
        if 38<y<252:occupied.append((x,y,x+len(val(t[1]))*.91,y+2.4))
    # Shorter panel captions preserve whitespace below the headings.
    replacements={
      'Existing 5.325 V nominal trip; clamp to sinking reference':'Nominal trip 5.325 V; reference clamp',
      'Fault clears run latch; history persists until RESET':'Run latch + ARM history; manual RESET',
      'Run requires both latches; fault asserts crowbar and SHDN':'Run permission / crowbar / input shutdown',
      'Source-referenced LTC7001 drives the common gate':'LTC7001 -> PROT_GATE / PROT_MID above',
      'UCC27511 drives Q303; resistor limits gate charge current':'UCC27511 -> CB_GATE / Q303 above'}
    for t in nodes(d,'text'):
        if val(t[1]) in replacements:t[1]=q(replacements[val(t[1])])
    occupied=[]
    for t in nodes(d,'text'):
        x,y=pos(t)
        if 38<y<252:occupied.append((x,y,x+len(val(t[1]))*.91,y+2.4))
    local_obstacles={i:[r for r in bodies+pins if intersect(r,b)] for i,b in enumerate(bounds)}
    local_wires={i:[w for w in wires if wire_hit(b,w)] for i,b in enumerate(bounds)}
    def cost(b,extra=()):
        return sum(1000 for r in local_obstacles[i] if intersect(b,r))+sum(500 for r in occupied if intersect(b,r))+sum(100 for w in local_wires[i] if wire_hit(b,w))
    # Explicit aligned bulk field rows, outside every capacitor lead/plate.
    for i in range(8):
        r='C'+str(330+i);x,y=pos(component(d,r));field(d,r,'Reference',x,83.5);field(d,r,'Value',x,86.7)
        occupied.append((x-6.8,82.4,x+6.8,87.7))
    # Most crowded/long parts are assigned first; each remains near its symbol.
    symbols=[s for s in nodes(d,'symbol') if not val(prop(s,'Reference')[2]).startswith('C33')]
    symbols.sort(key=lambda s:len(val(prop(s,'Value')[2])),reverse=True)
    failures=[]
    for s in symbols:
        ref=val(prop(s,'Reference')[2]);value=val(prop(s,'Value')[2]);x,y=pos(s);i=panel((x,y));x1,y1,x2,y2=bounds[i]
        width=max(len(ref),len(value))*1.40+.8
        old=pos(prop(s,'Reference'));candidates=[]
        for yy in [old[1]]+[y1+9+j*1.27 for j in range(int((y2-y1-12)/1.27)+1)]:
            for xx in [old[0]]+[x1+1+width/2+j*1.27 for j in range(max(0,int((x2-x1-width-2)/1.27)+1))]:
                b=(xx-width/2,yy-1.25,xx+width/2,yy+4.3)
                if b[0]<x1+1 or b[2]>x2-1 or b[1]<y1+8 or b[3]>y2-1:continue
                c=cost(b);distance=abs(xx-x)+abs(yy-y)
                candidates.append((c+distance*.7+abs(yy-old[1])*.15,xx,yy,b,c))
        if not candidates:failures.append(ref);continue
        _,xx,yy,b,c=min(candidates);field(d,ref,'Reference',round(xx,4),round(yy,4));field(d,ref,'Value',round(xx,4),round(yy+3,4));occupied.append(b)
        if c:failures.append((ref,c))
    # Existing conductor networks are traced geometrically; move labels only on
    # their own connected wires. A fresh netlist must still prove the result.
    def on(p,w):
        (x,y),(xx,yy)=w
        return abs((p[0]-x)*(yy-y)-(p[1]-y)*(xx-x))<.001 and min(x,xx)-.001<=p[0]<=max(x,xx)+.001 and min(y,yy)-.001<=p[1]<=max(y,yy)+.001
    junctions={pos(j) for j in nodes(d,'junction')}
    adjacency={j:{j} for j in range(len(wires))};endmap={}
    for j,w in enumerate(wires):
        for p in w:endmap.setdefault(p,set()).add(j)
    for indices in endmap.values():
        for j in indices:adjacency[j].update(indices)
    for p in junctions:
        indices={j for j,w in enumerate(wires) if on(p,w)}
        for j in indices:adjacency[j].update(indices)
    def connected(p):
        selected={j for j,w in enumerate(wires) if on(p,w)};todo=list(selected)
        while todo:
            j=todo.pop()
            for k in adjacency[j]-selected:selected.add(k);todo.append(k)
        return selected
    labels=[l for l in nodes(d,'label') if pos(l)[1]>38]
    labels.sort(key=lambda l:len(val(l[1])),reverse=True)
    for l in labels:
        text=val(l[1]);old=pos(l);i=panel(old);x1,y1,x2,y2=bounds[i];width=len(text)*1.40+.6;candidates=[]
        network=connected(old);points={old}
        for j in network:
            a,b=wires[j]
            if panel(((a[0]+b[0])/2,(a[1]+b[1])/2))!=i:continue
            length=abs(b[0]-a[0])+abs(b[1]-a[1]);dx=0 if a[0]==b[0] else (1 if b[0]>a[0] else -1);dy=0 if a[1]==b[1] else (1 if b[1]>a[1] else -1)
            points.update((round(a[0]+dx*k*1.27,6),round(a[1]+dy*k*1.27,6)) for k in range(round(length/1.27)+1))
        for x,y in points:
            if any(on((x,y),w) for j,w in enumerate(wires) if j not in network):continue
            for right in [False,True]:
                left=x-width if right else x
                b=(left,y-2.45,left+width,y-.25)
                if b[0]<x1+1 or b[2]>x2-1 or b[1]<y1+8 or b[3]>y2-1:continue
                c=cost(b);distance=abs(x-old[0])+abs(y-old[1]);candidates.append((c+distance*.5,x,y,right,b,c))
        if not candidates:candidates=[(1e9,*old,False,(old[0],old[1]-2.45,old[0]+width,old[1]-.25),9999)]
        _,x,y,right,b,c=min(candidates)
        if c:
            # Open a new annotation corridor from this conductor network. Route
            # on the original 50-mil grid, away from all foreign conductors.
            grid=1.27
            def gp(p):return (round(p[0]/grid),round(p[1]/grid))
            def mp(p):return (round(p[0]*grid,6),round(p[1]*grid,6))
            active=[r for r in bodies+pins+occupied if intersect(r,bounds[i])]
            foreign=[w for j,w in enumerate(wires) if j not in network and wire_hit(bounds[i],w)]
            low=(math.ceil((x1+1)/grid),math.ceil((y1+8)/grid));high=(math.floor((x2-1)/grid),math.floor((y2-1)/grid))
            blocked=set();goals={}
            for gx in range(low[0],high[0]+1):
                for gy in range(low[1],high[1]+1):
                    px,py=mp((gx,gy))
                    if any(r[0]-.1<px<r[2]+.1 and r[1]-.1<py<r[3]+.1 for r in active):blocked.add((gx,gy));continue
                    for rr in (False,True):
                        left=px-width if rr else px
                        bb=(left,py-2.45,left+width,py-.25)
                        if bb[0]<x1+1 or bb[2]>x2-1 or bb[1]<y1+8 or bb[3]>y2-1 or cost(bb):continue
                        goals.setdefault((gx,gy),[]).append((rr,bb))
            foreign_map={};foreign_ends={gp(p) for w in foreign for p in w};junction_grid={gp(p) for p in junctions}
            for w in foreign:
                a,bb=w;aa,zz=gp(a),gp(bb);dx=0 if aa[0]==zz[0] else (1 if zz[0]>aa[0] else -1);dy=0 if aa[1]==zz[1] else (1 if zz[1]>aa[1] else -1);length=abs(zz[0]-aa[0])+abs(zz[1]-aa[1])
                for k in range(length+1):foreign_map.setdefault((aa[0]+dx*k,aa[1]+dy*k),set()).add('H' if dx else 'V')
            sources={gp(p) for p in points if gp(p) not in foreign_map}
            queue=[(0,g,'') for g in sources];heapq.heapify(queue);distance={(g,''):0 for g in sources};previous={};chosen=None
            while queue:
                dist,g,direction=heapq.heappop(queue);state=(g,direction)
                if distance.get(state)!=dist:continue
                if g in goals and g not in foreign_map:
                    route=[g];cur=state
                    while cur in previous:cur=previous[cur];route.append(cur[0])
                    route=list(reversed(route));segments=list(zip(map(mp,route),map(mp,route[1:])))
                    options=[(rr,bb) for rr,bb in goals[g] if not any(wire_hit(bb,w) for w in segments)]
                    if options:chosen=(g,route,*options[0]);break
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    ng=(g[0]+dx,g[1]+dy);ndirection='H' if dx else 'V'
                    if not(low[0]<=ng[0]<=high[0] and low[1]<=ng[1]<=high[1]) or ng in blocked:continue
                    if g in foreign_map and (ndirection!=direction or ndirection in foreign_map[g]):continue
                    if ng in foreign_map and (ndirection in foreign_map[ng] or ng in foreign_ends or ng in junction_grid):continue
                    nd=dist+1+(6 if ng in foreign_map else 0);nextstate=(ng,ndirection)
                    if nd<distance.get(nextstate,1e9):distance[nextstate]=nd;previous[nextstate]=state;heapq.heappush(queue,(nd,ng,ndirection))
            if chosen:
                g,route,right,b=chosen;x,y=mp(g);c=0
                turns=[mp(route[0])]
                for a,bb,cc in zip(route,route[1:],route[2:]):
                    if (bb[0]-a[0],bb[1]-a[1])!=(cc[0]-bb[0],cc[1]-bb[1]):turns.append(mp(bb))
                turns.append(mp(route[-1]))
                for a,bb in zip(turns,turns[1:]):
                    if a==bb:continue
                    newwire=['wire',['pts',['xy',str(a[0]),str(a[1])],['xy',str(bb[0]),str(bb[1])]],['stroke',['width','0'],['type','default']],uid('03_OUTPUT_PROTECTION'+text+str(a)+str(bb))]
                    d.append(newwire);j=len(wires);wires.append((a,bb));local_wires[i].append((a,bb));adjacency[j]={j}|network
                    for k in network:adjacency[k].add(j)
                    network.add(j)
                start=turns[0]
                if start not in junctions:
                    d.append(['junction',['at',str(start[0]),str(start[1])],['diameter','0'],['color','0','0','0','0'],uid('03_OUTPUT_PROTECTION'+text+'junction'+str(start))]);junctions.add(start)
        replace(l,'at',['at',str(x),str(y),'180' if right else '0']);replace(l,'effects',effects(1.524,'right bottom' if right else 'left bottom'));occupied.append(b)
        if c:failures.append(('label',text,c))
    print('Text placement residuals:',failures,flush=True)
    # KiCad connections at new T nodes are explicit wire endpoints as well as
    # junction dots. Split the existing conductor without changing its geometry.
    splitpoints={pos(j) for j in nodes(d,'junction')}|{pos(l) for l in nodes(d,'label')}
    for w in list(nodes(d,'wire')):
        ends=tuple(tuple(map(float,p[1:])) for p in one(w,'pts')[1:])
        inner=[p for p in splitpoints if p not in ends and on(p,ends)]
        if not inner:continue
        points=[ends[0]]+sorted(inner,key=lambda p:abs(p[0]-ends[0][0])+abs(p[1]-ends[0][1]))+[ends[1]]
        d.remove(w)
        for j,(a,b) in enumerate(zip(points,points[1:])):
            new=copy.deepcopy(w);one(new,'pts')[1:]=[['xy',str(a[0]),str(a[1])],['xy',str(b[0]),str(b[1])]];replace(new,'uuid',uid('split'+one(w,'uuid')[1]+str(j)));d.append(new)
    # Trim unused original label tails after annotation moves. Every physical
    # pin, hierarchy endpoint, label and junction remains a protected point.
    protected={pos(l) for l in nodes(d,'label')+nodes(d,'hierarchical_label')+nodes(d,'junction')}
    for s in nodes(d,'symbol'):
        x,y=pos(s)
        for p in allpins(libs[val(one(s,'lib_id')[1])]):
            a=one(p,'at');protected.add((round(x+float(a[1]),6),round(y-float(a[2]),6)))
    while True:
        wire_nodes=nodes(d,'wire');wire_points=[tuple(tuple(map(float,p[1:])) for p in one(w,'pts')[1:]) for w in wire_nodes]
        changed=False
        for j,(w,ends) in enumerate(zip(wire_nodes,wire_points)):
            for k,p in enumerate(ends):
                if p in protected or any(p in other for n,other in enumerate(wire_points) if n!=j):continue
                keep=[v for v in protected if on(v,ends)]
                if keep:
                    v=min(keep,key=lambda v:abs(v[0]-p[0])+abs(v[1]-p[1]));one(w,'pts')[k+1][1:]=list(map(str,v))
                    if tuple(map(float,one(w,'pts')[1][1:]))==tuple(map(float,one(w,'pts')[2][1:])):d.remove(w)
                else:d.remove(w)
                changed=True;break
            if changed:break
        if not changed:break

def fix_03():
    name='03_OUTPUT_PROTECTION';d=reviewed(name)
    boxes=nodes(d,'rectangle')
    # Power remains across the top; actual control circuit now reads left to right.
    shifts=[(0,0),(0,0),(0,0),(0,78.74),(146.05,0),(-237.49,0),(13.97,78.74),(143.51,0),(140.97,0),(-110.49,-78.74),(-111.76,-78.74)]
    bounds=[tuple(map(float,one(b,'start')[1:]+one(b,'end')[1:])) for b in boxes]
    def location(o):
        if o[0]=='wire':
            pts=one(o,'pts')[1:];return tuple(sum(float(p[i]) for p in pts)/len(pts) for i in [1,2])
        if nodes(o,'at'):return tuple(map(float,one(o,'at')[1:3]))
        return None
    def translate(tree,dx,dy):
        for a in tree:
            if not isinstance(a,list):continue
            if a[0] in ('at','xy','start','end','center'):
                a[1:3]=[str(round(float(a[1])+dx,6)),str(round(float(a[2])+dy,6))]
            else:translate(a,dx,dy)
    for o in d:
        if not isinstance(o,list) or o[0] not in ('symbol','wire','label','junction','no_connect','text'):continue
        p=location(o)
        if p is None or p[1]<38 or p[1]>252:continue
        def dist(b):
            x1,y1,x2,y2=b;return max(x1-p[0],0,p[0]-x2)**2+max(y1-p[1],0,p[1]-y2)**2
        i=min(range(11),key=lambda i:dist(bounds[i]));translate(o,*shifts[i])
    for i,b in enumerate(boxes):translate(b,*shifts[i])
    # Panel extents provide independent margins for the larger technical text.
    newbounds={4:(302.26,100.33,407.924,173.99),5:(11.43,100.33,97.155,173.99),6:(349.25,179.07,407.924,251.46),9:(100.076,99.822,203.835,173.99),10:(205.486,99.822,298.45,173.99)}
    for i,bound in newbounds.items():
        one(boxes[i],'start')[1:]=list(map(str,bound[:2]));one(boxes[i],'end')[1:]=list(map(str,bound[2:]))
    def fonts(tree):
        for a in tree:
            if not isinstance(a,list):continue
            if a[0]=='size' and len(a)==3 and all(float(v)<2 for v in a[1:]):a[1:]=['1.524','1.524']
            else:fonts(a)
    for o in d:
        if isinstance(o,list) and o[0] in ('symbol','lib_symbols','label','hierarchical_label','text'):fonts(o)
    # Clear the drawing frame; replace the long stacked footer with two columns.
    for t in nodes(d,'text'):
        s=val(t[1])
        if 'SCHEMATIC REVIEW' in s:replace(t,'at',['at','13.208','14.5','0'])
    d[:]=[o for o in d if not(isinstance(o,list) and o[0]=='text' and float(one(o,'at')[2])>258)]
    def note(s,x,y,size=1.524):d.append(['text',q(s),['at',str(x),str(y),'0'],effects(size,'left top'),uid(name+s)])
    note('CONTROL: DETECTOR -> LATCHES -> FAULT ACTION -> GATE DRIVERS',13.208,256,1.778)
    for i,s in enumerate(['U303 OV_OK -> U310 QUALIFIED -> U304/U309 latches -> U305 RUN_GATE.',
                          'RUN_GATE -> U301 -> Q301/Q302 above: PROT_GATE / PROT_MID.',
                          'U311 CROWBAR_ON -> U315 below -> Q303 above via CB_GATE.',
                          'Q304 asserts INPUT_SHDN. RESET then ARM; no automatic retry.']):note(s,13.208,261+4*i)
    for i,s in enumerate(['Nominal OV trip: 5.325 V. Timing / SOA / fault energy remain OPEN.',
                          'VIN_FUSED -> independent detector and driver supplies below.',
                          'Evidence: docs/evidence/r2/sheet03/.',
                          'ERC does not validate electrical safety.']):note(s,158,261+4*i)
    arrange_output_text(d)
    field(d,'C320','Reference',181.61,163.432)
    field(d,'C320','Value',181.61,166.432)
    field(d,'C324','Reference',322.58,242.172)
    field(d,'C324','Value',322.58,245.172)
    move_label(d,'ARM_CLOCK',(107.95,115.57),(190.5,119.38))
    a=next(l for l in nodes(d,'label') if val(l[1])=='ARM_CLOCK' and tuple(map(float,one(l,'at')[1:3]))==(190.5,119.38))
    one(a,'at')[3]='180';replace(a,'effects',effects(1.524,'right bottom'))
    for j,(a,b) in enumerate(zip([(104.14,115.57),(104.14,109.22),(190.5,109.22)],[(104.14,109.22),(190.5,109.22),(190.5,119.38)])):
        d.append(['wire',['pts',['xy',str(a[0]),str(a[1])],['xy',str(b[0]),str(b[1])]],['stroke',['width','0'],['type','default']],uid('03_ARM_CLOCK_route'+str(j))])
    d.append(['wire',['pts',['xy','107.95','115.57'],['xy','104.14','115.57']],['stroke',['width','0'],['type','default']],uid('03_ARM_CLOCK_clearance')])
    move_label(d,'QUALIFIED',(148.59,111.76),(161.29,114.3))
    d.append(['wire',['pts',['xy','148.59','111.76'],['xy','148.59','114.3']],['stroke',['width','0'],['type','default']],uid('03_QUALIFIED_clearance')])
    d.append(['wire',['pts',['xy','148.59','114.3'],['xy','161.29','114.3']],['stroke',['width','0'],['type','default']],uid('03_QUALIFIED_clearance2')])
    write(d,name)
    # Keep the editable library's graphical representation in sync with its cache.
    lib=parse((HW/'V1A.kicad_sym').read_text());updated={val(x[1]).split(':',1)[1]:x for x in one(d,'lib_symbols')[1:]}
    for i,x in enumerate(lib):
        if isinstance(x,list) and x[0]=='symbol' and val(x[1]) in updated:
            fonts(x)
    (HW/'V1A.kicad_sym').write_text('\n'.join(line.rstrip() for line in dump(lib).splitlines())+'\n')


def fix_04():
    name='04_POWER_MONITOR';d=reviewed(name)
    for net,y in [('SCL_LOCAL',124.46),('SDA_LOCAL',129.54)]:
        move_label(d,net,(177.8,y),(190.5,y))
        d.append(['wire',['pts',['xy','177.8',str(y)],['xy','190.5',str(y)]],['stroke',['width','0'],['type','default']],uid(name+net+'clearance')])
    # The separator repeats these signals. Clear its crossing supply/return
    # routes too; perpendicular crossings have no junction and add no pins.
    for net,y in [('SCL_LOCAL',203.2),('SDA_LOCAL',208.28)]:
        move_label(d,net,(185.42,y),(177.8,y))
        d.append(['wire',['pts',['xy','185.42',str(y)],['xy','177.8',str(y)]],['stroke',['width','0'],['type','default']],uid(name+net+'separator-clearance')])
    for net,y in [('SCL_HOST',205.74),('SDA_HOST',210.82)]:
        move_label(d,net,(236.22,y),(248.92,y))
        d.append(['wire',['pts',['xy','236.22',str(y)],['xy','248.92',str(y)]],['stroke',['width','0'],['type','default']],uid(name+net+'separator-clearance')])
    write(d,name)


def fix_05():
    name='05_IO_TEST';d=reviewed(name)
    # Move the entire host-reference return to the left of the label column.
    for w in nodes(d,'wire'):
        points=one(w,'pts')[1:]
        for a in points:
            if float(a[1])==330.2 and float(a[2]) in (104.14,175.26):a[1]='314.96'
    write(d,name)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sheet',required=True,choices=['01','02','03','04','05'])
    a=p.parse_args();{'01':fix_01,'02':fix_02,'03':fix_03,'04':fix_04,'05':fix_05}[a.sheet]()
