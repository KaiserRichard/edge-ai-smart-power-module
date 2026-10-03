#!/usr/bin/env python3
"""Build only the three additional Sheet 03 packages from reviewed drawings.

Uses locally cached TI RPW0010A 4225183/A (08/2019) artwork. No PCB edits.
"""
from pathlib import Path
import hashlib
import pymupdf
from build_qualified_footprints import pad, rectangle, footprint

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'hardware/kicad/V1A_Qualified.pretty'


def loops(page, color):
    segments=[]
    for d in page.get_drawings():
        if not d['color'] or any(abs(a-b)>.01 for a,b in zip(d['color'],color)):continue
        for item in d['items']:
            if item[0] in ('l','c') and all(100<p.y<410 for p in item[1:]):segments.append(list(item[1:]))
    def near(a,b):return abs(a.x-b.x)<.11 and abs(a.y-b.y)<.11
    result=[]
    while segments:
        chain=[segments.pop(0)]
        while not near(chain[0][0],chain[-1][-1]):
            for i,s in enumerate(segments):
                if near(chain[-1][-1],s[0]):chain.append(segments.pop(i));break
                if near(chain[-1][-1],s[-1]):chain.append(list(reversed(segments.pop(i))));break
            else:raise ValueError('Unclosed manufacturer copper/stencil contour')
        p=[]
        for s in chain:
            if len(s)==2:p.append(tuple(s[0]))
            else:
                for i in range(17):
                    t=i/17;u=1-t
                    p.append(tuple(u**3*s[0][k]+3*u*u*t*s[1][k]+3*u*t*t*s[2][k]+t**3*s[3][k] for k in (0,1)))
        if max(x for x,y in p)-min(x for x,y in p)>.1 and max(y for x,y in p)-min(y for x,y in p)>.1:result.append(p)
    return result


def build():
    # ADI FE20 CA: 05-08-1663 Rev L; LTC3115-1 Rev E p40.
    pads=[]
    for i in range(10):
        for n,x,y in [(i+1,-2.775,-2.925+i*.65),(20-i,2.775,-2.925+i*.65)]:
            pads.append(pad(n,rectangle(x,y,1.05,.45),'"F.Cu" "F.Mask" "F.Paste"'))
    pads.append(pad(21,rectangle(0,0,2.74,4.95),'"F.Cu" "F.Mask"'))
    # Project stencil proposal, not an ADI guarantee. R3/R4 process review required.
    for x in (-.69,.69):
        for y in (-1.66,0,1.66):pads.append(pad('',rectangle(x,y,1.05,1.30),'"F.Paste"'))
    name='ADI_FE20_EP2.74x4.95'
    (OUT/(name+'.kicad_mod')).write_text(footprint(name,'ADI LTC3115-1 Rev E p40; FE20 CA 05-08-1663 Rev L; EP21 PGND; stencil proposal requires R3 review',(2.2,3.25),(3.6,3.6),pads,(-3.7,-3.1)))
    # Wurth drawing 007.000, 2023-05-30: 1.7x2.0 pads, 4.0 mm inner gap.
    name='Wurth_7447789004'
    pads=[pad(n,rectangle(0,y,1.7,2.0),'"F.Cu" "F.Mask" "F.Paste"') for n,y in [(1,-3),(2,3)]]
    (OUT/(name+'.kicad_mod')).write_text(footprint(name,'Wurth 7447789004 drawing007.000 2023-05-30; winding pad1 at negative Y; no sensitive traces beneath',(3.65,3.65),(4.05,4.3),pads,(-1.3,-3.8)))
    # TI RPW has ten pins, including broad IN5/OUT6: there is NO extra EP11.
    path=ROOT/'third_party/gate4b/tps25947.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()=='8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4', 'Re-review revised TI drawing before regeneration'
    doc=pymupdf.open(path);copper=loops(doc[72],(0,.5,1));paste=loops(doc[73],(1,0,0))
    assert len(copper)==10 and len(paste)==12,(len(copper),len(paste))
    def bbox(p):return min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)
    # The drawing is 30x; normalize its complete copper/stencil array centers independently.
    def normalize(ps):
        boxes=[bbox(p) for p in ps];cx=(min(b[0] for b in boxes)+max(b[2] for b in boxes))/2;cy=(min(b[1] for b in boxes)+max(b[3] for b in boxes))/2
        scale=72/25.4*30
        return [[((x-cx)/scale,(y-cy)/scale) for x,y in p] for p in ps]
    copper=normalize(copper);paste=normalize(paste)
    left=[];right=[];power=[]
    for p in copper:
        x1,y1,x2,y2=bbox(p);cx=(x1+x2)/2
        (power if abs(cx)<.5 else left if cx<0 else right).append(p)
    assert len(left)==len(right)==4 and len(power)==2
    pads=[]
    for n,p in zip((1,2,3,4),sorted(left,key=lambda p:bbox(p)[1])):pads.append(pad(n,p,'"F.Cu" "F.Mask"'))
    for n,p in zip((10,9,8,7),sorted(right,key=lambda p:bbox(p)[1])):pads.append(pad(n,p,'"F.Cu" "F.Mask"'))
    for n,p in zip((5,6),sorted(power,key=lambda p:bbox(p)[0])):pads.append(pad(n,p,'"F.Cu" "F.Mask"'))
    pads += [pad('',p,'"F.Paste"') for p in paste]
    name='TI_RPW0010A_TPS25947'
    (OUT/(name+'.kicad_mod')).write_text(footprint(name,'TI RPW0010A 4225183/A 08-2019; TPS25947 SLVSFC9C pp72-74; exact copper and 0.1mm stencil contours; no extra EP',(1,1),(1.5,1.5),pads,(-1.5,-1.1)))
    print('Built ADI FE20, Wurth7447789004, TI RPW0010A; manufacturing process review OPEN')

if __name__=='__main__':build()
