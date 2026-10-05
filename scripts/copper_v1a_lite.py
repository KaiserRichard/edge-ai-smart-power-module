#!/usr/bin/env python3
from layout_v1a_lite import *
def pads(b):return {(f.GetReference(),q.GetNumber()):q for f in b.GetFootprints() for q in reversed(list(f.Pads())) if q.GetNumber()}
def net(b,n):
 if not n.startswith('/'):n='/'+n
 z=b.FindNet(n)
 if z is None:raise ValueError(n)
 return z

def track(b,n,pts,w=.25,layer=p.F_Cu):
 nc=net(b,n).GetNetCode() if isinstance(n,str) else n
 for a,c in zip(pts,pts[1:]):
  if math.dist(a,c)<1e-6:continue
  t=p.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetWidth(mm(w));t.SetLayer(layer);t.SetNetCode(nc);b.Add(t)
def via(b,n,pt,d=.6,dr=.3):
 nc=net(b,n).GetNetCode() if isinstance(n,str) else n
 q=p.PCB_VIA(b);q.SetPosition(v(*pt));q.SetWidth(mm(d));q.SetDrill(mm(dr));q.SetViaType(p.VIATYPE_THROUGH);q.SetLayerPair(p.F_Cu,p.B_Cu);q.SetNetCode(nc);b.Add(q);return q

def zone(b,n,pts,layer=p.F_Cu,priority=10,name=''):
 z=p.ZONE(b);z.SetLayer(layer);z.SetNetCode(net(b,n).GetNetCode());z.SetLocalClearance(mm(.2));z.SetMinThickness(mm(.15));z.SetPadConnection(p.ZONE_CONNECTION_FULL);z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS);z.SetAssignedPriority(priority);z.SetZoneName(name or n)
 poly=z.Outline();poly.NewOutline()
 for x,y in pts:poly.Append(mm(x),mm(y))
 b.Add(z);return z

def rect(b,n,x1,y1,x2,y2,layer=p.F_Cu,priority=10,name=''):return zone(b,n,[(x1,y1),(x2,y1),(x2,y2),(x1,y2)],layer,priority,name)
def corridor(b,n,pts,w,layer=p.F_Cu,name=''):
 for a,c in zip(pts,pts[1:]):
  dx=c[0]-a[0];dy=c[1]-a[1];l=math.hypot(dx,dy)
  if l<1e-5:continue
  nx=-dy/l*w/2;ny=dx/l*w/2;ex=dx/l*.1;ey=dy/l*.1
  zone(b,n,[(a[0]-ex+nx,a[1]-ey+ny),(c[0]+ex+nx,c[1]+ey+ny),(c[0]+ex-nx,c[1]+ey-ny),(a[0]-ex-nx,a[1]-ey-ny)],layer,name=name)
def merge_zones(b):
 groups={}
 for z in list(b.Zones()):
  if z.GetIsRuleArea():continue
  key=(z.GetLayer(),z.GetNetname())
  if key not in groups:groups[key]=p.SHAPE_POLY_SET(z.Outline())
  else:groups[key].BooleanAdd(z.Outline())
  b.RemoveNative(z)
 names=sorted(set(n for ly,n in groups))
 for (ly,n),poly in groups.items():
  poly.Simplify()
  for k in range(poly.OutlineCount()):
   q=p.ZONE(b);q.SetLayer(ly);q.SetNetCode(net(b,n).GetNetCode());q.SetLocalClearance(mm(.2));q.SetMinThickness(mm(.15));q.SetPadConnection(p.ZONE_CONNECTION_FULL);q.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS);q.SetAssignedPriority(0 if n=='/GND' else 10+names.index(n));q.SetZoneName(n+' copper')
   q.Outline().AddOutline(poly.COutline(k))
   for h in range(poly.HoleCount(k)):q.Outline().AddHole(poly.CHole(k,h),0)
   b.Add(q)
def power():
 b=load()
 for t in list(b.GetTracks()):b.RemoveNative(t)
 for z in list(b.Zones()):b.RemoveNative(z)
 ps=pads(b)
 def pos(r,k):return xy(ps[r,str(k)].GetPosition())
 def link(a,c,w,pts=None,layer=p.F_Cu,pour=True):
  q=ps[a[0],str(a[1])];assert q.GetNetCode()==ps[c[0],str(c[1])].GetNetCode(),(a,c)
  path=[pos(*a)]+(pts or [])+[pos(*c)]
  (corridor if pour else track)(b,q.GetNetname(),path,w,layer)
 # Direct force route; input surge path terminates near connector return.
 link(('J501',1),('F101',1),2.5,[(16,17)])
 link(('F101',2),('Q101',2),3)
 link(('Q101',2),('D101',1),3,[(27,28),(25,32)])
 link(('Q101',3),('Q102',3),1.2)
 link(('Q102',2),('C101',1),3,[(48,24)])
 link(('C101',1),('D106',5),2.2)
 # Symmetric capacitor landing, HF parts directly at both power pin pairs.
 for c,vin,gnd in [('C203',8,9),('C204',12,11)]:
  link((c,1),('U201',vin),.4,[(45.45,41.2)] if c=='C204' else None,pour=False);link((c,2),('U201',gnd),.4,pour=False)
 for a,c in [('C201','C203'),('C202','C204'),('C215','C201'),('C216','C202')]:link((a,1),(c,1),1.1)
 link(('D106',5),('C202',1),2,[(49.3,36.7)])
 # Bottom VIN strap beside, not beneath, U201. Four vias per capacitor landing.
 for c in ['C201','C202']:
  x,y=pos(c,1)
  rect(b,'VIN_PROTECTED',x-.85,y-.95,x+.85,y+.95,p.B_Cu)
  for dx in [-.4,.4]:
   for dy in [-.6,.6]:via(b,'VIN_PROTECTED',(x+dx,y+dy))
 link(('C202',1),('C201',1),1.5,[(48.7,pos('C202',1)[1]),(48.7,pos('C201',1)[1])],p.B_Cu)
 # Small SW island and direct inductor connection.
 link(('U201',10),('L201',1),.8)
 corridor(b,'02_BUCK_5V/BUCK_SW',[(48,44),pos('L201',1)],2.3)
 track(b,'02_BUCK_5V/BUCK_SW',[pos('C205',2),(44.3,39.9),(44.3,41.6),(44.9,41.6),(44.9,43.6),(46,44)],.2)
 track(b,'02_BUCK_5V/BUCK_CBOOT',[pos('U201',14),(43.875,41.65),(42.7,41.65),(41.725,40.7),pos('C205',1)],.2)
 link(('R204',2),('C205',1),.2,pour=False)
 link(('C206',1),('U201',2),.25,[(41.6,43.475)],pour=False)
 link(('C206',2),('U201',3),.25,[(41.45,44.75),(41.45,44)],pour=False)
 link(('U201',4),('R203',1),.2,[(42,44.525),(42,45.7),(39.675,45.7)],pour=False)
 track(b,'02_BUCK_5V/BUCK_RBOOT',[pos('U201',13),(44.3,43.25)],.2)
 via(b,'02_BUCK_5V/BUCK_RBOOT',(44.3,43.25))
 track(b,'02_BUCK_5V/BUCK_RBOOT',[(44.3,43.25),(39.8,41.5)],.2,p.B_Cu)
 via(b,'02_BUCK_5V/BUCK_RBOOT',(39.8,41.5))
 track(b,'02_BUCK_5V/BUCK_RBOOT',[(39.8,41.5),pos('R204',1)],.2)
 # BOOT SW return uses the pin gap on the top layer.
 link(('L201',2),('F301',1),4,[(63.05,39.5),(71.745,39.5)])
 link(('F301',2),('J502',1),3)
 for i in range(209,215):link(('L201',2),('C'+str(i),1),2.2,[(65.0,44),(65.0,pos('C'+str(i),1)[1])])
 link(('L201',2),('SCR301',2),3.5,[(65.5,39),(69.54,39)])
 link(('SCR301',2),('C217',1),3,[(64,35.5)])
 link(('SCR301',2),('C218',1),3,[(76,35.5)])
 for c in ['C301','C302']:link(('J502',1),(c,1),2.2,[(78,52),(pos(c,1)[0],52)])
 link(('J502',1),('J503',1),3,[(78,52),(73,52),(73,61.5)])
 # Ground pours are continuous except clearance around actual copper/drills.
 for ly in [p.F_Cu,p.B_Cu]:rect(b,'GND',10.5,10.5,89.5,69.5,ly,0,'GND return and heat spreading')
 # Thermal vias use electrical pin potentials; the LM61460 has no exposed GND pad.
 # Ground vias in free spaces under/adjacent to package, no false EP15.
 for pt in [(43.9,44),(46.6,46.7),(46.6,40.5),(47.4,46.7),(47.4,40.5),(48.5,48.4),(48.5,39.6)]:via(b,'GND',pt)
 # DPAK drain tabs conduct heat to isolated bottom drain spreaders, not ground.
 for r in ['Q101','Q102']:
  x,y=pos(r,2);n=ps[r,'2'].GetNetname()
  rect(b,n,x-3,y-2.7,x+3,y+2.7,p.B_Cu,30,r+' drain heat spreader')
  for dx in [-2,0,2]:
   for dy in [-1.8,0,1.8]:via(b,n,(x+dx,y+dy))
 # SCR gate stays out of raw-current copper via the bottom control layer.
 gate='03_OUTPUT_PROTECTION/SCR_GATE'
 via(b,gate,(77.5,36.4));track(b,gate,[pos('R307',2),(77.325,36.5),(77.5,36.4)],.25)
 via(b,gate,pos('TP301',1))
 track(b,gate,[pos('SCR301',3),(74,33.5),(76,33.5),pos('TP301',1),(77.5,36.4)],.3,p.B_Cu)
 via(b,gate,(68.2,37));track(b,gate,[pos('R308',1),(68.2,37)],.25)
 track(b,gate,[(68.2,37),(70.6,37.3),(72.08,37.3),pos('SCR301',3)],.3,p.B_Cu)
 # Cathode Kelvin probe: isolated sense stub; force current remains in planes.
 sense=[pos('SCR301',1),(67,37.5),(70.5,41.5),(pos('TP302',1)[0],41.5),pos('TP302',1)]
 track(b,'GND',sense,.2,p.B_Cu);via(b,'GND',pos('TP302',1))
 # Keep filled copper off the sense stub, without blocking other routed tracks.
 for a,c in zip(sense,sense[1:]):
  dx=c[0]-a[0];dy=c[1]-a[1];ll=math.hypot(dx,dy);nx=-dy/ll*.5;ny=dx/ll*.5
  z=p.ZONE(b);z.SetIsRuleArea(True);z.SetLayer(p.B_Cu);z.SetDoNotAllowCopperPour(True);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False)
  z.Outline().NewOutline()
  for x,y in [(a[0]+nx,a[1]+ny),(c[0]+nx,c[1]+ny),(c[0]-nx,c[1]-ny),(a[0]-nx,a[1]-ny)]:z.Outline().Append(mm(x),mm(y))
  b.Add(z)
 x,y=pos('TP302',1)
 z=p.ZONE(b);z.SetIsRuleArea(True);z.SetLayer(p.F_Cu);z.SetDoNotAllowCopperPour(True);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False);z.Outline().NewOutline()
 for xx,yy in [(x-1.5,y-1.5),(x+1.5,y-1.5),(x+1.5,y+1.5),(x-1.5,y+1.5)]:z.Outline().Append(mm(xx),mm(yy))
 b.Add(z)
 x,y=pos('R308',2);via(b,'GND',(x,y+.9));track(b,'GND',[(x,y),(x,y+.9)],.3)
 # Output ceramic returns: multiple vias per bank; bulk/SCR pins are plated.
 for i in range(209,215):
  x,y=pos('C'+str(i),2)
  for dy in [-.65,.65]:via(b,'GND',(x+.8,y+dy));track(b,'GND',[(x,y),(x+.8,y+dy)],.5)
 
 names=sorted(set(z.GetNetname() for z in b.Zones() if not z.GetIsRuleArea()))
 for z in b.Zones():
  if z.GetIsRuleArea():continue
  z.SetAssignedPriority(0 if z.GetNetname()=='/GND' else 10+names.index(z.GetNetname()))
 merge_zones(b);b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());save(b)
if __name__=='__main__':power()
