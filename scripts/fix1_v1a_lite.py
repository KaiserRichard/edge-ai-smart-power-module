#!/usr/bin/env python3
"""Incremental PCB review FIX1; run only named stages, on reviewed baseline."""
from copper_v1a_lite import *
import sys
FIX=ROOT/'docs/evidence/v1a_lite/fix1';FIX.mkdir(exist_ok=True)
def fill(b):
 b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());save(b)
def label(b,s,x,y,size=1):
 text(b,s,x,y,size);list(b.GetDrawings())[-1] if False else None
 for d in b.GetDrawings():
  if isinstance(d,p.PCB_TEXT) and d.GetText()==s:d.SetTextThickness(mm(.15))
def remove_nets(b,names):
 for t in list(b.GetTracks()):
  if t.GetNetname() in names:b.RemoveNative(t)
def move(b,r,x,y,a=None):
 f=next(f for f in b.GetFootprints() if f.GetReference()==r)
 if a is not None:f.SetOrientationDegrees(a)
 f.SetPosition(v(x,y));return f
def polarity():
 b=load()
 for d in list(b.GetDrawings()):
  if isinstance(d,p.PCB_TEXT) and d.GetText() in ['+','PI OUT','DC IN']:b.RemoveNative(d)
 for s,x,y in [('J501 1 VIN+',16,28),('2 GND',16,43),('J502 1 +5V',83,38),('2 GND',84,54),('J503 +',68,64),('GND',78,64)]:label(b,s,x,y)
 fill(b)
def boot():
 b=load();remove_nets(b,['/02_BUCK_5V/BUCK_RBOOT','/02_BUCK_5V/BUCK_CBOOT'])
 # Delete only SW bootstrap branches, preserving the IC-to-inductor force copper.
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/02_BUCK_5V/BUCK_SW' and (min(t.GetStart().x,t.GetEnd().x)<mm(45) or min(t.GetStart().y,t.GetEnd().y)<mm(43.6)):b.RemoveNative(t)
 move(b,'R204',42.55,40.8,180);move(b,'C205',42.5,39.2,0)
 move(b,'C204',46.65,40.8,0)
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/VIN_PROTECTED' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and p.ToMM(t.GetWidth())<.3 and min(t.GetStart().x,t.GetEnd().x)<mm(46.3) and max(t.GetStart().y,t.GetEnd().y)>mm(38) and min(t.GetStart().y,t.GetEnd().y)<mm(42):b.RemoveNative(t)
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/GND' and ((isinstance(t,p.PCB_VIA) and math.dist(xy(t.GetPosition()),(41.4,41.4))<.01) or (not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and min(t.GetStart().y,t.GetEnd().y)<mm(42) and max(t.GetStart().y,t.GetEnd().y)>mm(41) and max(t.GetStart().x,t.GetEnd().x)<mm(43))):b.RemoveNative(t)
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/VIN_PROTECTED' and not isinstance(t,p.PCB_VIA) and (p.ToMM(t.GetWidth())<=.25 or math.dist(xy(t.GetStart()),(45.175,40.8))<.01 or math.dist(xy(t.GetEnd()),(45.175,40.8))<.01):b.RemoveNative(t)
  elif t.GetNetname()=='/GND' and ((isinstance(t,p.PCB_VIA) and any(math.dist(xy(t.GetPosition()),pt)<.01 for pt in [(46.45,41.4),(46.6,40.5)])) or (not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and min(t.GetStart().y,t.GetEnd().y)<mm(41.5) and max(t.GetStart().y,t.GetEnd().y)>mm(40) and min(t.GetStart().x,t.GetEnd().x)>mm(46) and max(t.GetStart().x,t.GetEnd().x)<mm(47))):b.RemoveNative(t)
 ps=pads(b)
 track(b,'VIN_PROTECTED',[(45.45,42.55),(45.45,41.7),(45.875,40.8)],.4)
 track(b,'GND',[(46.48,42.15),(47.425,40.8)],.4)
 track(b,'02_BUCK_5V/BUCK_RBOOT',[xy(ps['U201','13'].GetPosition()),(44.375,40.8),(43.375,40.8)],.25)
 track(b,'02_BUCK_5V/BUCK_CBOOT',[(43.875,42.4),(43.875,41.65),(41.725,41.65),(41.725,40.8),(41.725,39.2)],.25)
 track(b,'02_BUCK_5V/BUCK_SW',[(43.275,39.2),(44.9,39.2),(44.9,43.6),(46,44)],.25)
 fill(b)
def crowbar():
 b=load();b.SetCopperLayerCount(4)
 # L2 has only GND; L3 has GND plus local power spreaders.
 for ly in [p.In1_Cu,p.In2_Cu]:rect(b,'GND',10.5,10.5,89.5,69.5,ly,0,'FIX1 reference')
 rect(b,'VIN_PROTECTED',42,23,50,51,p.In2_Cu,30,'FIX1 VIN feed')
 rect(b,'VOUT_5V1',62,25,70,57,p.In2_Cu,30,'FIX1 raw force')
 # Remove the long cathode slot and its old traces, including orphan branches.
 for z in list(b.Zones()):
  if z.GetIsRuleArea():b.RemoveNative(z)
 remove_nets(b,['/03_OUTPUT_PROTECTION/SCR_GATE'])
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/GND' and min(a[0],c[0])>65 and min(a[1],c[1])>33 and max(a[1],c[1])<42 and (t.GetLayer()==p.B_Cu or isinstance(t,p.PCB_VIA)):b.RemoveNative(t)
 move(b,'SCR301',69,34,180)
 move(b,'C217',64,26,0);move(b,'C218',81,26,180)
 move(b,'R308',62.5,34,90)
 move(b,'TP301',64.25,38,0);move(b,'TP302',66.75,38,0)
 # Both banks stay directly on raw copper; force return is paired on L2.
 corridor(b,'VOUT_5V1',[(64,26),(64,30),(66.46,34),(66.46,39.5),(74.2,40.5)],3)
 corridor(b,'VOUT_5V1',[(81,26),(82.5,31),(73,31),(66.46,34)],2.5)
 corridor(b,'GND',[(69,26),(69,34)],2.0)
 corridor(b,'GND',[(76,26),(76,29),(71,29),(69,34)],1.5)
 for pt in [(69,31.5),(70,31.5),(70.5,34),(70,26),(75,26),(68,26)]:via(b,'GND',pt)
 # Separate, short K pickup branches. No slot in the underlying solid plane.
 track(b,'GND',[(69,34),(69,37),(66.75,38)],.25)
 track(b,'GND',[(69,34),(68.5,36.5),(62.5,36.5),(62.5,34.825)],.25,p.B_Cu)
 via(b,'GND',(62.5,34.825))
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,34),(62.5,33.175)],.3)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,34),(64.25,38)],.25)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,34),(63.92,32),(74,32),(77.5,36.4)],.3,p.B_Cu)
 via(b,'03_OUTPUT_PROTECTION/SCR_GATE',(77.5,36.4))
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(77.5,36.4),(77.325,37.5)],.25)
 fill(b)
 # Exact published standard no-requirement/JLC04161H-7628 dielectric values.
 s=BOARD.read_text();start=s.index('\t\t(stackup');i=start;depth=0
 for i in range(start,len(s)):
  if s[i]=='(':depth+=1
  elif s[i]==')':
   depth-=1
   if depth==0:break
 stack='\t\t(stackup\n'
 for name,kind,t in [('F.SilkS','Top Silk Screen',None),('F.Paste','Top Solder Paste',None),('F.Mask','Top Solder Mask',.01),('F.Cu','copper',.035),('dielectric 1','prepreg',.2104),('In1.Cu','copper',.0152),('dielectric 2','core',1.065),('In2.Cu','copper',.0152),('dielectric 3','prepreg',.2104),('B.Cu','copper',.035),('B.Mask','Bottom Solder Mask',.01),('B.Paste','Bottom Solder Paste',None),('B.SilkS','Bottom Silk Screen',None)]:
  stack+=f'\t\t\t(layer "{name}" (type "{kind}")'+(f' (thickness {t})' if t else '')+')\n'
 stack+='\t\t\t(copper_finish "Lead free HASL")\n\t\t\t(dielectric_constraints no)\n\t\t)'
 BOARD.write_text(s[:start]+stack+s[i+1:])
def force_cleanup():
 b=load()
 remove_nets(b,['/03_OUTPUT_PROTECTION/SCR_GATE','/CB_COLLECTOR'])
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/VOUT_5V1' and not isinstance(t,p.PCB_VIA):b.RemoveNative(t)
  elif t.GetNetname()=='/GND' and 60<min(a[0],c[0])<81 and 30<min(a[1],c[1]) and max(a[1],c[1])<39.5:b.RemoveNative(t)
  elif isinstance(t,p.PCB_VIA) and any(math.dist(a,pt)<.01 for pt in [(70,26),(68,26),(75,26),(37.75,50.15)]):b.RemoveNative(t)
 for z in list(b.Zones()):
  if z.GetNetname()=='/VOUT_5V1':b.RemoveNative(z)
 move(b,'SCR301',69,33.4,180);move(b,'R308',61,31.5,180)
 move(b,'TP301',66.5,38.35);move(b,'TP302',69.6,38.35)
 corridor(b,'VOUT_5V1',[(63.05,44),(63.05,39.5),(71.745,39.5),(74.2,40.5)],4)
 corridor(b,'VOUT_5V1',[(64,26),(64,29),(66.46,33.4),(66.46,39.5)],3)
 for i in range(209,215):
  q=pads(b)['C'+str(i),'1'];corridor(b,'VOUT_5V1',[(63.05,44),(65,44),(65,xy(q.GetPosition())[1]),xy(q.GetPosition())],2.2)
 # L3 broad raw bank connection, L2 uninterrupted adjacent return.
 zone(b,'VOUT_5V1',[(62,24),(83,24),(83,28),(70,31),(68,39),(71,39),(71,42),(69,57),(63,57)],p.In2_Cu,30)
 for pt in [(65,39.5),(66,39.5),(70.5,39.8),(71.5,39.8),(64,43),(64,45)]:via(b,'VOUT_5V1',pt)
 track(b,'GND',[(69,33.4),(71,35.3),(71,38.35),(69.6,38.35)],.25)
 track(b,'GND',[(69,33.4),(69,30),(60.175,30),(60.175,31.5)],.25,p.B_Cu)
 via(b,'GND',(60.175,31.5))
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(61.825,31.5)],.3)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(64.5,36.5),(66.5,38.35)],.25)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(63.92,32),(74,32),(77.5,36.4)],.3,p.B_Cu)
 via(b,'03_OUTPUT_PROTECTION/SCR_GATE',(77.5,36.4));track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(77.5,36.4),(77.325,37.5)],.25)
 for pt in [(70.5,33.4),(70.5,35),(70.5,27.5),(75,27.5)]:via(b,'GND',pt)
 # Removed redundant VIN signal tracks are replaced by a direct local feed.
 corridor(b,'VIN_PROTECTED',[(48,35),(54,35)],1)
 merge_zones(b);fill(b)
def bridge():
 b=load()
 # Drop only orphan routing objects reported after force-net rework.
 j=json.loads((FIX/'FORCE_DRC.json').read_text());ids={i['uuid'] for a in j['violations'] if a['type']=='via_dangling' for i in a['items']}
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString() in ids or (isinstance(t,p.PCB_VIA) and any(math.dist(xy(t.GetPosition()),q)<.01 for q in [(66,39.5),(60,32),(60.175,31.5)])):b.RemoveNative(t)
 # Keep the two local probe pads out of the main inductor-to-fuse corridor.
 move(b,'F301',74.5,43,0)
 move(b,'R308',61,30.7,180)
 # Short cathode sense runs below the gate route, separately from force copper.
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/GND' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu and min(t.GetStart().x,t.GetEnd().x)>59 and max(t.GetStart().x,t.GetEnd().x)<70 and min(t.GetStart().y,t.GetEnd().y)>=mm(30) and max(t.GetStart().y,t.GetEnd().y)<=mm(33.4):b.RemoveNative(t)
  elif t.GetNetname()=='/03_OUTPUT_PROTECTION/SCR_GATE' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and min(t.GetStart().y,t.GetEnd().y)<mm(32):b.RemoveNative(t)
 track(b,'GND',[(69,33.4),(69,35),(60.175,35),(60.175,30.7)],.25,p.B_Cu);via(b,'GND',(60.175,30.7))
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(61.825,30.7)],.3)
 corridor(b,'VOUT_5V1',[(63.05,44),(66,43),(72.045,43)],4)
 corridor(b,'VOUT_PI',[(76.955,43),(84,44)],3)
 # Old thin fuse approach duplicates the poured force path and crosses new pads.
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/VOUT_PI' and not isinstance(t,p.PCB_VIA) and max(t.GetStart().y,t.GetEnd().y)<mm(44):b.RemoveNative(t)
 merge_zones(b);fill(b)
def thermal():
 b=load()
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/GND' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu and min(t.GetStart().x,t.GetEnd().x)>mm(59) and max(t.GetStart().x,t.GetEnd().x)<mm(70) and min(t.GetStart().y,t.GetEnd().y)>=mm(30) and max(t.GetStart().y,t.GetEnd().y)<=mm(33.4):b.RemoveNative(t)
  elif isinstance(t,p.PCB_VIA) and math.dist(xy(t.GetPosition()),(72,44))<.01:b.RemoveNative(t)
 ps=pads(b)
 for r,box in [('Q101',(22,16,33.3,29)),('Q102',(42,14,52,27))]:
  n=ps[r,'2'].GetNetname()
  for ly in [p.F_Cu,p.B_Cu,p.In2_Cu]:rect(b,n,*box,ly,30,r+' FIX1 spreader')
 merge_zones(b);fill(b)
def reconnect():
 from route_v1a_lite import Router
 b=load();rr=Router(b);ps=pads(b)
 pairs=[(('R163','1'),('R307','1')),(('R307','1'),('Q301','3')),(('R307','1'),('TP508','1')),(('R206','1'),('C201','1')),(('R202','1'),('C207','1')),(('R202','1'),('C214','1')),(('R301','1'),('C214','1')),(('R306','1'),('R301','1')),(('TP504','1'),('C214','1')),(('Q301','2'),('C214','1'))]
 for a,c in pairs:
  n=ps[a].GetNetCode();ok,cnt=rr.route(n,xy(ps[a].GetPosition()),xy(ps[c].GetPosition()))
  print(a,c,ok,cnt,flush=True)
  if not ok:raise RuntimeError((a,c))
 fill(b)
def via_process():
 from route_v1a_lite import Router
 b=load();rr=Router(b);allpads=[q for f in b.GetFootprints() for q in f.Pads() if q.GetNumber() and q.IsOnLayer(p.F_Cu)]
 def land(pt):
  for q in allpads:
   bb=q.GetBoundingBox();x,y=pt
   if p.ToMM(bb.GetLeft())-.35<x<p.ToMM(bb.GetRight())+.35 and p.ToMM(bb.GetTop())-.35<y<p.ToMM(bb.GetBottom())+.35:return True
  return False
 moved=[]
 for t in list(b.GetTracks()):
  if not isinstance(t,p.PCB_VIA):continue
  old=xy(t.GetPosition())
  if not land(old):continue
  choices=[]
  for dx in range(-40,41,2):
   for dy in range(-40,41,2):
    if not dx and not dy:continue
    pt=(old[0]+dx*.1,old[1]+dy*.1)
    if not land(pt):choices.append((math.hypot(dx,dy),pt))
  for _,pt in sorted(choices):
   gx,gy=rr.grid(pt);nc=t.GetNetCode()
   if not rr.lib.freecell(gx,gy,0,nc,1) or not rr.lib.freecell(gx,gy,1,nc,1):continue
   ok,cnt=rr.route(nc,old,pt,allowvia=False)
   if not ok:continue
   t.SetPosition(v(*pt));rr.mark(t);moved.append({'net':t.GetNetname(),'old':old,'new':pt});break
  else:moved.append({'net':t.GetNetname(),'old':old,'status':'OPEN no off-land position'})
 fill(b);(FIX/'VIA_RELOCATION.json').write_text(json.dumps(moved,indent=2)+'\n');print('moved vias',len(moved))
def silk():
 b=load()
 # Replace inherited undersized board text with readable field labels.
 for d in list(b.GetDrawings()):
  if isinstance(d,p.PCB_TEXT):b.RemoveNative(d)
 for s,x,y in [('V1A-LITE FIX1 / 4L',63,17),('NOT FOR FABRICATION',48,66),('ENGINEERING REVIEW REQUIRED',48,68),('J501 1 VIN+',17,26.8),('2 GND',16,43.5),('J502',85,33),('1 +5V',85,39),('2 GND',85,52),('J503 +',68,58.5),('GND',78,58.5),('SCR K A G: RIGHT TO LEFT',71,20),('5A TARGET',79,66)]:label(b,s,x,y)
 # Keep native polarity graphics and increase process-safe stroke width.
 for f in b.GetFootprints():
  for g in f.GraphicalItems():
   if g.GetLayer() in [p.F_SilkS,p.B_SilkS] and hasattr(g,'SetWidth'):g.SetWidth(max(g.GetWidth(),mm(.15)))
 fill(b)
 j=json.loads(PRO.read_text());j['board']['design_settings']['rules'].update(min_silk_text_height=1.0,min_silk_text_thickness=.15,min_silk_clearance=.15);PRO.write_text(json.dumps(j,indent=2)+'\n')
def stitch():
 from route_v1a_lite import Router
 b=load();rr=Router(b);nc=net(b,'GND').GetNetCode();added=[]
 through=[xy(t.GetPosition()) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetCode()==nc]+[xy(q.GetPosition()) for f in b.GetFootprints() for q in f.Pads() if q.GetNetCode()==nc and q.GetDrillSize().x]
 for z in b.Zones():
  if z.GetNetCode()!=nc or z.GetLayer() not in [p.F_Cu,p.B_Cu]:continue
  pp=z.GetFilledPolysList(z.GetLayer())
  for k in range(pp.OutlineCount()):
   ch=pp.COutline(k)
   def inside(pt):return ch.PointInside(v(*pt)) and not any(pp.CHole(k,h).PointInside(v(*pt)) for h in range(pp.HoleCount(k)))
   if any(inside(pt) for pt in through):continue
   coords=[xy(ch.CPoint(i)) for i in range(ch.PointCount())];xs=[pt[0] for pt in coords];ys=[pt[1] for pt in coords];done=False
   for xx in range(math.ceil(min(xs)*4),math.floor(max(xs)*4)+1):
    for yy in range(math.ceil(min(ys)*4),math.floor(max(ys)*4)+1):
     pt=(xx/4,yy/4);gx,gy=rr.grid(pt)
     if inside(pt) and rr.lib.freecell(gx,gy,0,nc,1) and rr.lib.freecell(gx,gy,1,nc,1):
      rr.mark(via(b,nc,pt));through.append(pt);added.append(pt);done=True;break
    if done:break
   print('island',b.GetLayerName(z.GetLayer()),abs(ch.Area())/1e12,'stitched',done,flush=True)
 for d in b.GetDrawings():
  if isinstance(d,p.PCB_TEXT):
   if d.GetText()=='V1A-LITE FIX1 / 4L':d.SetPosition(v(71,13))
   elif d.GetText() in ['J503 +','GND']:d.SetPosition(v(p.ToMM(d.GetPosition().x),64.5))
 fill(b);(FIX/'STITCHING.json').write_text(json.dumps(added,indent=2)+'\n')
def via_back():
 from route_v1a_lite import Router
 b=load();rr=Router(b);j=json.loads((FIX/'VIA_RELOCATION.json').read_text())
 for a in j:
  if 'new' not in a:continue
  nc=net(b,a['net']).GetNetCode();old=a['old'];new=a['new']
  if not any(not isinstance(t,p.PCB_VIA) and t.GetNetCode()==nc and t.GetLayer()==p.B_Cu and min(math.dist(xy(t.GetStart()),old),math.dist(xy(t.GetEnd()),old))<.001 for t in b.GetTracks()):continue
  ok,cnt=rr.route(nc,old,new,1,1,False);a['bottom_reconnected']=ok
  if not ok:
   # Preserve original connectivity; flag this via for reviewed solder process.
   for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA) and t.GetNetCode()==nc and math.dist(xy(t.GetPosition()),new)<.001:t.SetPosition(v(*old))
   a['status']='OPEN relocation reverted: bottom escape unavailable'
  print(a['net'],ok,flush=True)
 for d in b.GetDrawings():
  if isinstance(d,p.PCB_TEXT) and d.GetText()=='J503 +':d.SetPosition(v(68,65))
 fill(b);(FIX/'VIA_RELOCATION.json').write_text(json.dumps(j,indent=2)+'\n')
def local_control():
 from route_v1a_lite import Router
 b=load()
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString()=='7aeba3cf-ce18-4661-be82-5fc0346674ec':b.RemoveNative(t)
 for ly in [p.F_Cu,p.B_Cu,p.In2_Cu]:
  rect(b,'VIN_PROTECTED',41.2,20.5,44,22.5,ly)
  rect(b,'VIN_PROTECTED',42.5,49,44.5,52.5,ly)
 remove_nets(b,['/02_BUCK_5V/BUCK_VCC','/02_BUCK_5V/BUCK_FB'])
 # Remove obsolete C206 and R203 ground escapes before moving their lands.
 for t in list(b.GetTracks()):
  if t.GetNetname()!='/GND' or isinstance(t,p.PCB_VIA) or t.GetLayer()!=p.F_Cu:continue
  if any(min(math.dist(xy(t.GetStart()),pt),math.dist(xy(t.GetEnd()),pt))<.1 for pt in [(40.8,44.575),(41.325,46.65)]):b.RemoveNative(t)
 move(b,'C206',41.45,43.8,-90);move(b,'R203',40.9,46.3,180)
 track(b,'02_BUCK_5V/BUCK_VCC',[(41.45,43.025),(42,43.025),(42.45,43.475),(43.15,43.475)],.3)
 track(b,'GND',[(41.45,44.575),(41.8,44),(43.15,44)],.3)
 track(b,'02_BUCK_5V/BUCK_FB',[(43.15,44.525),(42.15,44.525),(42.15,45.875),(41.725,46.3)],.25)
 merge_zones(b);fill(b)
 rr=Router(b);ps=pads(b)
 for a,c in [(('R203','1'),('R202','2')),(('R202','2'),('R205','2'))]:
  ok,cnt=rr.route(ps[a].GetNetCode(),xy(ps[a].GetPosition()),xy(ps[c].GetPosition()));print(a,c,ok,flush=True)
  if not ok:raise RuntimeError((a,c))
 fill(b)
if __name__=='__main__':globals()[sys.argv[1]]()
