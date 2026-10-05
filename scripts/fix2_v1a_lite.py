#!/usr/bin/env python3
"""Named, incremental FIX2 edits; KiCad bundled Python. No schematic edits."""
from fix1_v1a_lite import *
FIX=ROOT/'docs/evidence/v1a_lite/fix2'
def boot2():
 b=load();remove_nets(b,['/02_BUCK_5V/BUCK_RBOOT','/02_BUCK_5V/BUCK_CBOOT'])
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/02_BUCK_5V/BUCK_SW' and (min(t.GetStart().x,t.GetEnd().x)<mm(45) or min(t.GetStart().y,t.GetEnd().y)<mm(43.6)):b.RemoveNative(t)
 move(b,'R204',43.2,40.85,180);move(b,'C205',43.6,39.35,0)
 track(b,'02_BUCK_5V/BUCK_RBOOT',[(44.375,42.4),(44.375,41.35),(44.025,40.85)],.25)
 track(b,'02_BUCK_5V/BUCK_CBOOT',[(43.875,42.4),(43.875,41.65),(42.375,41.65)],.25)
 track(b,'02_BUCK_5V/BUCK_CBOOT',[(42.375,41.65),(42.375,40.85),(42.825,39.35)],.4)
 track(b,'02_BUCK_5V/BUCK_SW',[(44.375,39.35),(44.9,39.35),(44.9,40.4)],.4)
 track(b,'02_BUCK_5V/BUCK_SW',[(44.9,40.4),(44.9,43.35)],.25)
 track(b,'02_BUCK_5V/BUCK_SW',[(44.9,43.35),(44.9,43.6),(46,44)],.4)
 fill(b)

def keepout(b,pts,name):
 z=p.ZONE(b);z.SetIsRuleArea(True);z.SetLayer(p.F_Cu);z.SetZoneName(name)
 z.SetDoNotAllowCopperPour(True);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False)
 poly=z.Outline();poly.NewOutline()
 for x,y in pts:poly.Append(mm(x),mm(y))
 b.Add(z)
def guard(b,pts,w,name):
 for a,c in zip(pts,pts[1:]):
  dx=c[0]-a[0];dy=c[1]-a[1];ll=math.hypot(dx,dy);nx=-dy/ll*w/2;ny=dx/ll*w/2;ex=dx/ll*w/2;ey=dy/ll*w/2
  keepout(b,[(a[0]-ex+nx,a[1]-ey+ny),(c[0]+ex+nx,c[1]+ey+ny),(c[0]+ex-nx,c[1]+ey-ny),(a[0]-ex-nx,a[1]-ey-ny)],name)
def control2():
 b=load();remove_nets(b,['/02_BUCK_5V/BUCK_VCC'])
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/GND' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and 40<min(a[0],c[0]) and max(a[0],c[0])<43.3 and 43.8<min(a[1],c[1]) and max(a[1],c[1])<46.5:b.RemoveNative(t)
 move(b,'C206',41.1,43.75,-90)
 track(b,'02_BUCK_5V/BUCK_VCC',[(41.1,42.8),(42.15,43.475),(43.15,43.475)],.3)
 track(b,'GND',[(41.1,44.7),(41.65,44),(43.15,44)],.35)
 # Preserve outer divider/FF routing; shorten its pin-side branch.
 for t in list(b.GetTracks()):
  if t.GetNetname()=='/02_BUCK_5V/BUCK_FB' and min(t.GetStart().x,t.GetEnd().x)>=mm(41.675):b.RemoveNative(t)
 move(b,'R203',40.85,46.2,180)
 track(b,'02_BUCK_5V/BUCK_FB',[(43.15,44.525),(42.2,44.525),(42.2,45.675),(41.675,46.2),(41.65,46.3)],.25)
 track(b,'GND',[(40.025,46.2),(40.025,45.8),(41.1,44.7)],.4)
 fill(b)
def detector2():
 from route_v1a_lite import Router
 b=load();ps=pads(b)
 # Move only the high-side detector divider entry beside the selected capacitor.
 # Existing raw routes also serve R202/R306: keep those intact at the old node.
 move(b,'R301',63.0,57.6,180)
 remove_nets(b,['/03_OUTPUT_PROTECTION/OVOUT_D1'])
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/GND' and 55<min(a[0],c[0]) and max(a[0],c[0])<62 and 53.3<min(a[1],c[1]) and max(a[1],c[1])<55.5:b.RemoveNative(t)
 # Replace old long raw probe leaf with off-land terminal access from below.
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/VOUT_5V1' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and min(a[0],c[0])>=60 and max(a[0],c[0])<=66.1 and min(a[1],c[1])>=56:b.RemoveNative(t)
  elif t.GetNetname()=='/VOUT_5V1' and not isinstance(t,p.PCB_VIA) and math.dist(a,(59.175,52))<.001 and math.dist(c,(59.15,52))<.001:b.RemoveNative(t)
 for ref,x in [('TP504',66.025),('TP506',68.975)]:
  f=ps[ref,'1'].GetParentFootprint()
  if not f.IsFlipped():f.Flip(f.GetPosition(),False)
  f.SetPosition(v(x,56));n=ps[ref,'1'].GetNetname()
  via(b,n,(x,57.6));track(b,n,[(x,56),(x,57.6)],.35,p.F_Cu);track(b,n,[(x,56),(x,57.6)],.35,p.B_Cu)
 # Surface-only Kelvin ground, with no local stitching to the power plane.
 ret=[(56.5,54.175),(57.2,54.175),(57.2,55),(60.9375,55),(61.9,55.6),(61.2,56.7),(61.2,58.6),(67.5,58.6),(68.975,56)]
 track(b,'GND',ret,.3)
 guard(b,ret[:-1]+[(68.6,56.66)],.8,'FIX2 detector Kelvin ground: F pour excluded')
 for ref,num in [('R304','2'),('U301','3')]:
  q=ps[ref,num];bb=q.GetBoundingBox();x1=p.ToMM(bb.GetLeft())-.25;x2=p.ToMM(bb.GetRight())+.25;y1=p.ToMM(bb.GetTop())-.25;y2=p.ToMM(bb.GetBottom())+.25
  keepout(b,[(x1,y1),(x2,y1),(x2,y2),(x1,y2)],'FIX2 detector ground pad isolation')
 sense=[(63.825,57.6),(64.6,57.6),(66.025,56)]
 track(b,'VOUT_5V1',sense,.3);guard(b,sense[:-1]+[(65.5,56.59)],.8,'FIX2 raw Kelvin pickup')
 fill(b)
 rr=Router(b);ps=pads(b)
 ok,cnt=rr.route(ps['R301','2'].GetNetCode(),xy(ps['R301','2'].GetPosition()),xy(ps['R302','1'].GetPosition()))
 if not ok:raise RuntimeError('Detector divider route')
 fill(b)

def probes2():
 b=load()
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/VOUT_5V1' and not isinstance(t,p.PCB_VIA) and math.dist(c,(59.175,52))<.001 and math.dist(a,(59.15,52))<.001:b.RemoveNative(t)
  elif not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu and any(math.dist(a,pt)<.001 or math.dist(c,pt)<.001 for pt in [(35.8,22),(35.8,18.8)]):b.RemoveNative(t)
 move(b,'TP113',37.2,21.6);move(b,'TP114',37.2,18.4)
 track(b,'01_INPUT_PROTECTION/S_COMMON',[(37.95,23.3),(37.2,21.6)],.25,p.B_Cu)
 track(b,'01_INPUT_PROTECTION/CUT_GATE',[(37.35,18.15),(37.2,18.4)],.25,p.B_Cu)
 for ref,x,oldx in [('TP504',65.9,66.025),('TP506',69.1,68.975)]:
  move(b,ref,x,56);track(b,pads(b)[ref,'1'].GetNetname(),[(x,56),(oldx,56)],.35,p.B_Cu)
 fill(b)

def tidy2():
 b=load()
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString() in ['3d160e54-6cb8-4033-8824-9f8344a0cd2c','ba5aaa92-f295-45bb-9bb3-cca7aacbe5a5','f6fa1557-cbf2-41f7-898c-3f43b9a0f914']:b.RemoveNative(t)
 fill(b)
def silk2():
 b=load();placed=[]
 for d in list(b.GetDrawings()):
  if isinstance(d,p.PCB_TEXT):
   if d.GetLayer()==p.B_SilkS or d.GetText().startswith('TP') or d.GetText().isdigit() or d.GetText() in ['Q101','Q102','U201','Q1','Q2','U2']:b.RemoveNative(d)
   elif d.GetText()=='V1A-LITE FIX1 / 4L':d.SetText('V1A-LITE FIX2 / 4L')
 def box(q,margin=0):
  z=q.GetBoundingBox();return (p.ToMM(z.GetLeft())-margin,p.ToMM(z.GetTop())-margin,p.ToMM(z.GetRight())+margin,p.ToMM(z.GetBottom())+margin)
 def overlap(a,c):return a[0]<c[2] and a[2]>c[0] and a[1]<c[3] and a[3]>c[1]
 def tx(s,x,y,ly):
  t=p.PCB_TEXT(b);t.SetText(s);t.SetLayer(ly);t.SetTextSize(v(1,1));t.SetTextThickness(mm(.15));t.SetMirrored(ly==p.B_SilkS);t.SetPosition(v(x,y));return t
 # Back-side legend gives full references/net names; short local marks identify lands.
 legend=['PROBE MAP: TPxxx / XY mm','XY: NATIVE TOP VIEW mm']
 for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
  if not f.GetReference().startswith('TP'):continue
  q=list(f.Pads())[0];x,y=xy(q.GetPosition());name=q.GetNetname().split('/')[-1]
  legend.append(f'{f.GetReference()[2:]} {name} {x:g},{y:g}')
 legend+=['Q1=Q101 Q2=Q102 U2=U201','FAST RAW: C214 TERMINALS','FAST SCR: SCR301 G / K','Q102: DIFFERENTIAL PROBE']
 for i,s in enumerate(legend):b.Add(tx(s,44.5,31+i*1.75,p.B_SilkS))
 b.Add(tx('TPxxx MAP ON BACK',28,63.5,p.F_SilkS))
 for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
  ref=f.GetReference()
  if not (ref.startswith('TP') or ref in ['Q101','Q102','U201']):continue
  ly=p.B_SilkS if f.IsFlipped() else p.F_SilkS;obs=[]
  for other in b.GetFootprints():
   if other.IsFlipped()==f.IsFlipped():
    for g in other.GraphicalItems():
     if g.GetLayer() in ([p.B_CrtYd,p.B_SilkS] if f.IsFlipped() else [p.F_CrtYd,p.F_SilkS]):obs.append(box(g,.16))
   for q in other.Pads():
    if q.IsOnLayer(p.B_Cu if f.IsFlipped() else p.F_Cu):obs.append(box(q,.2))
  obs += [box(d,.2) for d in b.GetDrawings() if d.GetLayer()==ly]
  mark=ref[2:] if ref.startswith('TP') else {'Q101':'Q1','Q102':'Q2','U201':'U2'}[ref]
  t=tx(mark,0,0,ly);x,y=xy(f.GetPosition());choices=[]
  for dx in range(-40,41):
   for dy in range(-40,41):
    if dx*dx+dy*dy<9:continue
    choices.append((dx*dx+dy*dy,(x+dx*.25,y+dy*.25)))
  for _,pos in sorted(choices):
   t.SetPosition(v(*pos));bb=box(t)
   if bb[0]<10.5 or bb[1]<10.5 or bb[2]>89.5 or bb[3]>69.5:continue
   if any(overlap(bb,o) for o in obs):continue
   
   if ref.startswith('TP') and math.dist(pos,(x,y))>4:
    placed.append({'ref':ref,'status':'on-board back legend with exact XY; local mark omitted to avoid ambiguous displacement'});break
   b.Add(t);placed.append({'ref':ref,'mark':mark,'layer':b.GetLayerName(ly),'pos':pos,'pad_or_anchor':(x,y),'distance':math.dist(pos,(x,y))});break
  else:raise RuntimeError('No silk position '+ref)
 fill(b);(FIX/'SILK_IDENTIFICATION.json').write_text(json.dumps(placed,indent=2)+'\n')

def offland2():
 b=load()
 for t in list(b.GetTracks()):
  if not isinstance(t,p.PCB_VIA):continue
  old=xy(t.GetPosition());dest=None
  if math.dist(old,(37.35,18.15))<.001:dest=(38.65,18.7)
  elif math.dist(old,(63.5,54.45))<.001:dest=(62.3,53.9)
  if dest:
   t.SetPosition(v(*dest))
   for ly in [p.F_Cu,p.B_Cu]:track(b,t.GetNetCode(),[old,dest],.2,ly)
 # Direct terminal-to-via and via-to-contact gate pickup; old drive escape preserved.
 track(b,'01_INPUT_PROTECTION/CUT_GATE',[(38.96,17.72),(38.65,18.7)],.25)
 track(b,'01_INPUT_PROTECTION/CUT_GATE',[(38.65,18.7),(37.2,18.4)],.25,p.B_Cu)
 move(b,'TP506',69.35,56)
 track(b,'GND',[(69.35,56),(68.975,56)],.35,p.B_Cu)
 fill(b)

def divider_via2():
 b=load()
 for t in list(b.GetTracks()):
  if t.GetNetname()!='/03_OUTPUT_PROTECTION/OVOUT_D1':continue
  if isinstance(t,p.PCB_VIA) and math.dist(xy(t.GetPosition()),(62.3,53.9))<.001:t.SetPosition(v(64.35,54.325))
  elif not isinstance(t,p.PCB_VIA) and any(math.dist(xy(pt),(62.3,53.9))<.001 for pt in [t.GetStart(),t.GetEnd()]):b.RemoveNative(t)
 for ly in [p.F_Cu,p.B_Cu]:track(b,'03_OUTPUT_PROTECTION/OVOUT_D1',[(63.5,54.45),(64.35,54.325)],.2,ly)
 fill(b)
if __name__=='__main__':globals()[sys.argv[1]]()
