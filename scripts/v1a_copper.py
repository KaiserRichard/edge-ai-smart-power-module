#!/usr/bin/env python3
"""Authored V1A copper geometry; no electrical release. Run after placement."""
import json, math
from pathlib import Path
import pcbnew as p
from layout_v1a import BOARD, EV, v, xy, mm, save

def board():
 b=p.LoadBoard(str(BOARD));m=p.GetSettingsManager();m.LoadProject(str(BOARD.with_suffix('.kicad_pro')));b.SetProject(m.GetProject(str(BOARD.with_suffix('.kicad_pro'))));b.SynchronizeNetsAndNetClasses(False);return b

def pads(b):return {(f.GetReference(),q.GetNumber()):q for f in b.GetFootprints() for q in reversed(list(f.Pads())) if q.GetNumber()}
def net(b,n):
 if not n.startswith('/'):n='/'+n
 return b.FindNet(n)
def track(b,n,points,w=.2,layer=p.F_Cu):
 nc=net(b,n).GetNetCode() if isinstance(n,str) else n
 for a,c in zip(points,points[1:]):
  if math.dist(a,c)<.00001:continue
  t=p.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetWidth(mm(w));t.SetLayer(layer);t.SetNetCode(nc);b.Add(t)
def via(b,n,pt,d=.6,dr=.3):
 nc=net(b,n).GetNetCode() if isinstance(n,str) else n
 q=p.PCB_VIA(b);q.SetPosition(v(*pt));q.SetWidth(mm(d));q.SetDrill(mm(dr));q.SetViaType(p.VIATYPE_THROUGH);q.SetLayerPair(p.F_Cu,p.B_Cu);q.SetNetCode(nc);b.Add(q);return q

def zone(b,n,pts,layer=p.F_Cu,priority=10,name=''):
 z=p.ZONE(b);z.SetLayer(layer);z.SetNetCode(net(b,n).GetNetCode());z.SetLocalClearance(mm(.2));z.SetMinThickness(mm(.2));z.SetPadConnection(p.ZONE_CONNECTION_FULL);z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS);z.SetAssignedPriority(priority);z.SetZoneName(name or n)
 poly=z.Outline();poly.NewOutline()
 for x,y in pts:poly.Append(mm(x),mm(y))
 b.Add(z);return z

def rect(b,n,x1,y1,x2,y2,layer=p.F_Cu,priority=10,name=''):return zone(b,n,[(x1,y1),(x2,y1),(x2,y2),(x1,y2)],layer,priority,name)
def corridor(b,n,pts,w,layer=p.F_Cu,name=''):
 for a,c in zip(pts,pts[1:]):
  dx=c[0]-a[0];dy=c[1]-a[1];l=math.hypot(dx,dy)
  if l<1e-5:continue
  nx=-dy/l*w/2;ny=dx/l*w/2;ex=dx/l*.15;ey=dy/l*.15
  zone(b,n,[(a[0]-ex+nx,a[1]-ey+ny),(c[0]+ex+nx,c[1]+ey+ny),(c[0]+ex-nx,c[1]+ey-ny),(a[0]-ex-nx,a[1]-ey-ny)],layer,name=name)

def merge_zones(b):
 groups={}
 for z in list(b.Zones()):
  key=(z.GetLayer(),z.GetNetname())
  if key not in groups:groups[key]=z
  else:
   groups[key].Outline().BooleanAdd(z.Outline());b.RemoveNative(z)
 for i,z in enumerate(groups.values()):
  z.Outline().Simplify();z.SetAssignedPriority(0 if z.GetNetname()=='/GND' else 10+i)

def power(b):
 for t in list(b.GetTracks()):b.RemoveNative(t)
 for z in list(b.Zones()):b.RemoveNative(z)
 fps={f.GetReference():f for f in b.GetFootprints()}
 fps['Q101'].SetOrientationDegrees(270);fps['L301'].SetOrientationDegrees(270)
 ps=pads(b)
 def pos(r,k):return xy(ps[r,str(k)].GetPosition())
 def link(a,c,w,points=None,layer=p.F_Cu):
  pa=ps[a[0],str(a[1])];pc=ps[c[0],str(c[1])];assert pa.GetNetCode()==pc.GetNetCode(),(a,c)
  corridor(b,pa.GetNetname(),[pos(*a)]+(points or [])+[pos(*c)],w,layer,name=f'{a[0]}.{a[1]} to {c[0]}.{c[1]}')
 # Input force copper. Small eFuse pins have separate explicit short escapes.
 link(('J501',1),('F101',1),3,[(17,53)])
 link(('J501',1),('PF1',1),3,[(17,44)])
 link(('F101',2),('Q101',1),2,[(31,57),(31,63.025)])
 link(('F101',2),('D101',1),3,[(36,57)])
 link(('F101',2),('D303',1),2,[(21,57),(21,113)])
 link(('Q101',5),('U101',1),.4)
 link(('Q101',5),('U101',2),.4)
 link(('U101',17),('JP101',1),.3,[(46,63.25),(46,73),(29,73)])
 link(('U101',18),('U101',17),.3)
 # Reinforce the long OUT escape after the fine-pitch section.
 corridor(b,'01_INPUT_PROTECTION/EFUSE_OUT',[(46,63.25),(46,73),(29,73),(29,78)],3)
 link(('JP101',2),('D102',2),4,[(40,98)])
 link(('D102',2),('C201',1),3,[(50,94)])
 link(('C201',1),('C203',1),.6)
 link(('C202',1),('C204',1),.6)
 link(('C203',1),('U201',8),.35)
 link(('C204',1),('U201',12),.35)
 link(('C203',2),('U201',9),.4)
 link(('C204',2),('U201',11),.4)
 # Local buried VIN strap: two small arrays, separate from the GND shield.
 for r in ['C201','C202']:
  q=pos(r,1)
  for dx in [-.6,0,.6]:via(b,'VIN_PROTECTED',(q[0]+dx,q[1]))
 link(('C201',1),('C202',1),2,layer=p.In2_Cu)
 # Switching force links have separate copper on either side; never bridge straps.
 link(('U201',10),('JP201',1),1,[(57,81)])
 link(('JP201',1),('PF3',1),3)
 link(('JP201',2),('L201',1),4)
 link(('JP201',2),('PF4',1),3)
 link(('L201',2),('JP202',1),5)
 # Main regulated path, all force segments on F.Cu.
 link(('JP202',2),('Q301',5),5)
 link(('Q302',5),('JP301',1),5)
 link(('JP301',2),('R401',1),5)
 link(('R401',4),('J502',1),3)
 for k in [1,2,3]:link(('Q301',k),('Q302',k),.5)
 # A common source bus fills the area between all three parallel source leads.
 rect(b,'03_OUTPUT_PROTECTION/PROT_MID',166.1,68.4,170.9,71.9)
 # Six ceramics immediately beyond the output link.
 for i in range(209,215):link(('JP202',2),('C'+str(i),1),2,[(154,78),(pos('C'+str(i),1)[0],78)])
 # Raw bank bus and two independently routed ballast strings.
 for i in range(330,338):
  q=pos('C'+str(i),1);link(('JP202',2),('C'+str(i),1),3,[(154,48),(q[0],48)])
 for row,seq in enumerate([[380,381,382,383,386,387],[388,389,390,391,392,393]]):
  link(('C330',1),('R'+str(seq[0]),1),3,[(110,20+row*7)])
  for a,c in zip(seq,seq[1:]):link(('R'+str(a),2),('R'+str(c),1),3)
  link(('R'+str(seq[-1]),2),('JP331',1),3,[(46,20+row*7),(43,50),(87,50)])
 link(('JP331',2),('Q330',5),4)
 link(('C330',1),('D330',2),3,[(102,32)])
 # Protected bank and symmetrical two-resistor disposal strings.
 for i in range(340,344):
  q=pos('C'+str(i),1);link(('JP301',2),('C'+str(i),1),4,[(203,84),(q[0],84)])
 for a,c in [(308,309),(310,311)]:
  link(('C340',1),('R'+str(a),1),3,[(166,87),(166,pos('R'+str(a),1)[1])])
  link(('R'+str(a),2),('R'+str(c),1),3)
  link(('R'+str(c),2),('JP330',1),3,[(189,pos('R'+str(c),2)[1])])
 link(('JP330',2),('Q303',5),4)
 link(('C342',1),('D331',2),3)
 link(('J502',1),('JP501',1),5,[(235,70.39),(235,154),(212,154)])
 # PF5 is the external-load GND bolt, not LOAD_FIXTURE. JP501 pad 2 is its force takeoff.
 # Auxiliary force section. The fine converter pins are escaped individually.
 link(('D303',2),('Q316',2),3)
 link(('Q316',3),('R332',1),3)
 link(('R332',2),('C351',1),1.5,[(57,123),(77,123)])
 link(('C351',1),('U317',17),.3)
 link(('C352',1),('U317',4),.3)
 link(('U317',18),('L301',1),.35,[(75,125),(75,120)])
 link(('U317',3),('L301',2),.35,[(64,125),(64,120)])
 link(('U317',17),('C380',1),.3)
 link(('U317',4),('C377',1),.3)
 # Tie all repeated force pins directly; no thin daisy-chain to a single lead.
 for r in ['Q101','Q301','Q302','Q303','Q330']:
  groups={}
  for (ref,k),q in ps.items():
   if ref==r and q.GetNetname() in {a['pattern'] for a in json.loads(BOARD.with_suffix('.kicad_pro').read_text())['net_settings']['netclass_patterns'] if a['netclass']=='HighCurrent'}:groups.setdefault(q.GetNetname(),[]).append(q)
  for name,qs in groups.items():
   pts=sorted([xy(q.GetPosition()) for q in qs]);corridor(b,name,pts,.4 if r=='Q101' else .5)
 # GND plane and bottom spreader are solid connections; signals may later carve B.Cu.
 for ly in [p.In1_Cu,p.B_Cu]:rect(b,'GND',10.75,10.75,239.25,204.25,ly,0,'GND continuous shield' if ly==p.In1_Cu else 'GND return / heat spreader')
 # Exposed-pad fields: preliminary via-in-pad process needs fabrication review.
 for r,k,offsets in [('U101',25,[(x,y) for x in [-.7,0,.7] for y in [-.7,0,.7]]),('U317',21,[(x,y) for x in [-.65,.65] for y in [-1.7,-.85,0,.85,1.7]]),('U301',11,[(0,-.4),(0,.4)])]:
  x,y=pos(r,k)
  for dx,dy in offsets:via(b,'GND',(x+dx,y+dy))
 merge_zones(b)
 b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());save(b)

if __name__=='__main__':power(board())
