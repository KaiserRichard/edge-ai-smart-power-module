#!/usr/bin/env python3
"""Incremental resume corrections. Named stages only; never rebuild baseline."""
from fix1_v1a_lite import *

def probes():
 b=load();ps=pads(b)
 # Preserve former common-source junction tracks; move only probe footprints.
 for ref in ['TP113','TP114']:
  f=ps[ref,'1'].GetParentFootprint();f.Flip(f.GetPosition(),False)
  f.SetPosition(v(35.8,19.5 if ref=='TP114' else 22))
 track(b,'01_INPUT_PROTECTION/CUT_GATE',[(37.35,18.15),(35.8,19.5)],.25,p.B_Cu)
 track(b,'01_INPUT_PROTECTION/S_COMMON',[(37.95,23.3),(35.8,22)],.25,p.B_Cu)
 fill(b)

def offland():
 b=load()
 # Remaining ground vias in wettable lands are redundant to local ground pours.
 # Signal vias: move to nearby B.Cu escape vertices, with a short F.Cu dogbone.
 shifts={(25,31.2):(25.9,31.2),(25.35,29):(26.6,29),
 (45.9,24.65):(47.2,24.65),(50,21.8):(51.4,21.8),
 (25,32.85):(25.9,32.85),(57.1,18):(58.2,18)}
 remove=[(32,20)]
 shifts.update({(69,40.5):(70.2,41),(46.7,47.55):(47.8,47.55),(30.85,18.65):(31.5,19.95),(41.7,49.1):(41.75,48.6)})
 log=[]
 for t in list(b.GetTracks()):
  if not isinstance(t,p.PCB_VIA):continue
  old=xy(t.GetPosition())
  if any(math.dist(old,a)<.01 for a in remove):b.RemoveNative(t);log.append({'old':old,'action':'remove redundant ground via'});continue
  dest=next((new for a,new in shifts.items() if math.dist(old,a)<.01),None)
  if dest is None:continue
  t.SetPosition(v(*dest))
  for ly in [p.F_Cu,p.B_Cu]:track(b,t.GetNetCode(),[old,dest],.2,ly)
  log.append({'old':old,'new':dest})
 fill(b);(FIX/'RESUME_VIA_CHANGES.json').write_text(json.dumps(log,indent=2)+'\n')

def tidy_probes():
 b=load();move(b,'TP114',35.8,18.8)
 for t in b.GetTracks():
  if not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu and math.dist(xy(t.GetEnd()),(35.8,19.5))<.01:t.SetEnd(v(35.8,18.8))
 # Prune the old gate test-pad leaf until its first real branch/land.
 pos=(40.,13.)
 while True:
  incident=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and min(math.dist(xy(t.GetStart()),pos),math.dist(xy(t.GetEnd()),pos))<.001]
  if len(incident)!=1:break
  t=incident[0];other=xy(t.GetEnd()) if math.dist(xy(t.GetStart()),pos)<.001 else xy(t.GetStart());b.RemoveNative(t);pos=other
  if any(math.dist(xy(q.GetPosition()),pos)<.001 for f in b.GetFootprints() for q in f.Pads()):break
  if any(isinstance(q,p.PCB_VIA) and math.dist(xy(q.GetPosition()),pos)<.001 for q in b.GetTracks()):break
 fill(b)

def local_returns():
 b=load()
 for t in b.GetTracks():
  if t.GetNetname()!='/GND':continue
  if isinstance(t,p.PCB_VIA) and math.dist(xy(t.GetPosition()),(41.75,48.6))<.01:t.SetPosition(v(42.1,48.7))
  elif not isinstance(t,p.PCB_VIA) and math.dist(xy(t.GetEnd()),(41.75,48.6))<.01:t.SetEnd(v(42.1,48.7))
 # Put the gate resistor directly below the SCR lands, clear of force bridge.
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if t.GetNetname()=='/GND' and t.GetLayer()==p.B_Cu and not isinstance(t,p.PCB_VIA) and min(a[0],c[0])>59 and max(a[0],c[0])<70 and min(a[1],c[1])>29 and max(a[1],c[1])<36:b.RemoveNative(t)
  elif t.GetNetname()=='/03_OUTPUT_PROTECTION/SCR_GATE' and t.GetLayer()==p.F_Cu and min(math.dist(a,(61.825,30.7)),math.dist(c,(61.825,30.7)))<.01:b.RemoveNative(t)
 move(b,'R308',66.5,35.8,0)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(64.5,35.8),(65.675,35.8)],.3)
 track(b,'GND',[(69,33.4),(69,35.8),(67.325,35.8)],.3)
 # Move existing GND access beside raw ripple TP504; Pi return remains J503.2.
 move(b,'TP506',66.5,58.5)
 track(b,'GND',[(66.5,58.5),(68.975,56)],.3)
 fill(b)

def local_finish():
 b=load()
 # Detour the existing two-via EN bottom segment around the new off-land GND via.
 for t in list(b.GetTracks()):
  if not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu and t.GetNetname()=='/02_BUCK_5V/BUCK_EN':b.RemoveNative(t)
  elif not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and t.GetNetname()=='/03_OUTPUT_PROTECTION/SCR_GATE':b.RemoveNative(t)
  elif not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and t.GetNetname()=='/GND' and (min(math.dist(xy(t.GetStart()),(69,35.8)),math.dist(xy(t.GetEnd()),(69,35.8)))<.01 or math.dist(xy(t.GetStart()),(66.5,58.5))<.01):b.RemoveNative(t)
 track(b,'02_BUCK_5V/BUCK_EN',[(40.3,48.8),(40.3,47.8),(42.85,47.8),(42.85,48.05)],.2,p.B_Cu)
 move(b,'R308',63.3,36.6,0)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(62.475,35),(62.475,36.6),(62.475,38.35),(66.5,38.35)],.3)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(77.5,36.4),(77.325,37.5)],.25)
 track(b,'GND',[(69,33.4),(69,36.6),(64.125,36.6)],.3)
 move(b,'TP504',60,60.5);move(b,'TP506',63.25,60.5)
 track(b,'VOUT_5V1',[(63.25,58.5),(60,59),(60,60.5)],.3)
 track(b,'GND',[(63.25,60.5),(64.5,59),(69.8,57),(68.975,56)],.3)
 fill(b)

def scr_side():
 b=load()
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and t.GetNetname()=='/03_OUTPUT_PROTECTION/SCR_GATE':b.RemoveNative(t)
  elif not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and t.GetNetname()=='/GND' and min(math.dist(a,(69,36.6)),math.dist(c,(69,36.6)))<.01:b.RemoveNative(t)
  elif isinstance(t,p.PCB_VIA) and math.dist(a,(60,60))<.01:b.RemoveNative(t)
 move(b,'R308',73,34.5,90)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(63.92,33.4),(64.5,36.5),(66.5,38.35)],.25)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(77.5,36.4),(77.325,37.5)],.25)
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(73,35.325),(73,36.3)],.3);via(b,'03_OUTPUT_PROTECTION/SCR_GATE',(73,36.3))
 track(b,'03_OUTPUT_PROTECTION/SCR_GATE',[(73,36.3),(73,32)],.3,p.B_Cu)
 track(b,'GND',[(73,33.675),(71,33.675),(69,33.4)],.3)
 fill(b)

def mask_finish():
 b=load()
 for t in list(b.GetTracks()):
  a=xy(t.GetStart());c=xy(t.GetEnd())
  if isinstance(t,p.PCB_VIA) and any(math.dist(a,pt)<.01 for pt in [(46.6,46.7),(64,60)]):b.RemoveNative(t)
  elif isinstance(t,p.PCB_VIA) and math.dist(a,(47,13.6))<.01:
   t.SetPosition(v(47,14.65))
   for ly in [p.F_Cu,p.B_Cu]:track(b,'GND',[(47,13.6),(47,14.65)],.25,ly)
  elif not isinstance(t,p.PCB_VIA) and t.GetNetname()=='/CB_COLLECTOR' and t.GetLayer()==p.F_Cu and math.dist(a,(70.2,32.05))<.01 and math.dist(a,c)>7:
   b.RemoveNative(t);track(b,'CB_COLLECTOR',[a,(75.2,32.05),(75.2,36.5),c],.2)
 fill(b)

def identification():
 b=load();placed=[]
 def box(q,margin=0):
  z=q.GetBoundingBox();return (p.ToMM(z.GetLeft())-margin,p.ToMM(z.GetTop())-margin,p.ToMM(z.GetRight())+margin,p.ToMM(z.GetBottom())+margin)
 def overlap(a,c):return a[0]<c[2] and a[2]>c[0] and a[1]<c[3] and a[3]>c[1]
 for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
  ref=f.GetReference()
  if not (ref.startswith('TP') or ref in ['Q101','Q102','U201','SCR301']):continue
  ly=p.B_SilkS if f.IsFlipped() else p.F_SilkS
  obs=[]
  for other in b.GetFootprints():
   if other.IsFlipped()==f.IsFlipped():
    for g in other.GraphicalItems():
     if g.GetLayer() in ([p.B_CrtYd,p.B_SilkS] if f.IsFlipped() else [p.F_CrtYd,p.F_SilkS]):obs.append(box(g,.2))
   for q in other.Pads():
    if q.IsOnLayer(p.B_Cu if f.IsFlipped() else p.F_Cu):obs.append(box(q,.2))
  obs += [box(d,.2) for d in b.GetDrawings() if d.GetLayer()==ly]
  tx=p.PCB_TEXT(b);tx.SetText(ref);tx.SetLayer(ly);tx.SetTextSize(v(1,1));tx.SetTextThickness(mm(.15));tx.SetMirrored(f.IsFlipped())
  x,y=xy(f.GetPosition());choices=[]
  for dx in range(-12,13):
   for dy in range(-12,13):
    if dx*dx+dy*dy<9:continue
    choices.append((dx*dx+dy*dy,(x+dx*.5,y+dy*.5)))
  found=False
  for _,pos in sorted(choices):
   tx.SetPosition(v(*pos));bb=box(tx)
   if bb[0]<11 or bb[1]<11 or bb[2]>89 or bb[3]>69:continue
   if any(overlap(bb,o) for o in obs):continue
   b.Add(tx);placed.append({'ref':ref,'layer':b.GetLayerName(ly),'pos':pos});found=True;break
  if not found:placed.append({'ref':ref,'status':'OPEN no uncluttered local silk location'})
 # Fab fields moved to their own body centers; paired probes use small readable fields.
 for f in b.GetFootprints():
  if f.GetReference().startswith('TP') or f.GetReference() in ['U301','SCR301','R308']:
   field=f.Reference();field.SetPosition(f.GetPosition());field.SetTextSize(v(.8,.8));field.SetTextThickness(mm(.12));field.SetLayer(p.B_Fab if f.IsFlipped() else p.F_Fab)
 fill(b);(FIX/'SILK_IDENTIFICATION.json').write_text(json.dumps(placed,indent=2)+'\n')

def assembly_text():
 b=load();removed=0
 for f in b.GetFootprints():
  for g in list(f.GraphicalItems()):
   if isinstance(g,p.PCB_TEXT) and g.GetLayer() in [p.F_Fab,p.B_Fab] and g.GetText()=='${REFERENCE}':f.RemoveNative(g);removed+=1
  if f.GetReference().startswith('TP'):
   f.Reference().SetTextSize(v(.6,.6));f.Reference().SetTextThickness(mm(.08))
 save(b);print('Removed duplicate Fab reference fields',removed)

if __name__=='__main__':globals()[sys.argv[1]]()
