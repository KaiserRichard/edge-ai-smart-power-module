#!/usr/bin/env python3
from layout_v1a_lite import *
b=load();fs={f.GetReference():f for f in b.GetFootprints()};placed={};boxes={}
def box(f):
 bb=f.GetBoundingBox(False,False);return [p.ToMM(bb.GetX()),p.ToMM(bb.GetY()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())]
def put(r,x,y,a=0):
 f=fs[r];f.SetOrientationDegrees(a);f.SetPosition(v(x,y));f.SetIsPlaced(True);f.SetNeedsPlaced(False)
 for fld in f.GetFields():fld.SetVisible(False)
 f.Reference().SetVisible(True);f.Reference().SetLayer(p.F_Fab);f.Reference().SetTextSize(v(.7,.7));f.Reference().SetTextThickness(mm(.1));f.Reference().SetPosition(v(x,y-1.8));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));placed[r]=[x,y,a];boxes[r]=box(f)
fixed={
'J501':(16,32,270),'F101':(23,27,0),'D101':(23,36,90),'Q101':(31,30,180),'Q102':(43,30,0),'C101':(48,25,0),'D106':(47,34,0),
'U201':(45,44,0),'C203':(45.95,47.2,0),'C204':(45.95,40.8,0),'C201':(45.7,50.3,0),'C202':(45.7,37.7,0),'C215':(49.5,50.3,0),'C216':(49.5,37.7,0),
'C205':(43.1,39.4,0),'R204':(41,41,90),'C206':(40.8,43.5,90),'R203':(41,46.4,0),'R202':(38,46.4,0),'C207':(38,44.1,0),'R205':(35.5,44.1,0),'R201':(42.5,50.3,90),'R206':(38,50,0),'R207':(38,52.5,0),
'L201':(57.5,44,0),'F301':(76,44,0),'J502':(84,44,270),'J503':(82,57,90),
'C217':(64,31.5,0),'C218':(74.5,31.5,0),'SCR301':(66,37,0),
'C301':(80,49,90),'C302':(84,51.5,90),
'U101':(36,21,0),'Q103':(44,18,0),'Q104':(54,17,0),'Q105':(59,17,0),'Q106':(49,17,0),'C102':(39,16,0),
'D102':(33,36.5,0),'D103':(39,36.5,0),'D104':(35,16,0),'D105':(40,21,0),
'U301':(65,55,0),'Q301':(72,52,180),'R307':(73,39,90),'R308':(70,41,0),
'TP301':(73.5,35.5,0),'TP302':(70.5,35.5,0),'TP113':(37,31,0),'TP114':(37,27.5,0),
'TP501':(17.5,23,0),'TP502':(26,22,0),'TP503':(51,33,0),'TP504':(70,47,0),'TP505':(87,54,0),'TP506':(87,58,0),
'TP507':(33,12,0),'TP508':(77,39,0),'TP110':(54,12,0),'TP111':(59,12,0),'TP112':(48,12,0),
}
fixed.update({'F101':(23,17,0),'Q101':(30,24,180),'Q102':(44,20,0),'D101':(25,39,270),'C101':(50,29,0),'D106':(47,35,0),
'C205':(42.5,39.9,0),'R204':(39.8,39.5,90),'C206':(40.8,43.8,270),
'C202':(43.8,36.7,0),'C216':(43.8,33,0),'C201':(45,50.3,0),'C215':(45,54,0),
'C217':(64,26,0),'C218':(76,26,0),'SCR301':(67,35.5,0),'F301':(74.2,40.5,0),'C301':(77,55,0),'C302':(83,55,0),'J503':(73,62,0),
'U101':(30.5,34,0),'Q103':(37,25,0),'Q104':(53,17,0),'Q105':(58,17,0),'Q106':(48,13,0),'C102':(34,39,0),
'D102':(33,30,0),'D103':(40,29,0),'D104':(30,39,90),'D105':(34.5,35,90),
'U301':(60,55,0),'Q301':(74,50,180),'R307':(75,38,0),'R308':(69,38,0),
'TP301':(77.5,34,0),'TP302':(77.5,37,0),'TP113':(41,25,0),'TP114':(40,13,0),
'TP501':(17,23,0),'TP502':(26,25,0),'TP503':(54,33,0),'TP504':(64,58,0),'TP505':(86,59,0),'TP506':(81,59,0),
'TP507':(34,59,0),'TP508':(82,37,0),'TP110':(54,12,0),'TP111':(59,12,0),'TP112':(45,13,0)})
fixed['R166']=(51,12.5,90)
for i in range(209,215):fixed['C'+str(i)]=(67.5,41+(i-209)*3,0)
for row,start in enumerate([110,118]):
 for k in range(8):fixed['R'+str(start+k)]=(18.5+k*3.4,59+row*2.3,0)
for k in range(6):fixed['R'+str(130+k)]=(18+k*3.4,45,0)
# Resolve desired positions against actual footprint boxes; primary power parts first.
order=['J501','J502','J503','U201','L201','SCR301','C217','C218','F301','F101','Q101','Q102','D101','C101','C203','C204','C205','R204','C206','C201','C202','C215','C216']
order += [r for r in fixed if r not in order]
for r in order:
 x,y,a=fixed[r];f=fs[r];f.SetOrientationDegrees(a);f.SetPosition(v(x,y));bb=box(f)
 occupied=[box(ff) for rr,ff in fs.items() if rr.startswith('MH')]+list(boxes.values())
 def free(bb):return bb[0]>=10.2 and bb[1]>=10.5 and bb[2]<=89.5 and bb[3]<=64.7 and not any(bb[0]<c[2]+.15 and bb[2]>c[0]-.15 and bb[1]<c[3]+.15 and bb[3]>c[1]-.15 for c in occupied)
 if not free(bb):
  off=sorted([(dx*.25,dy*.25) for dx in range(-48,49) for dy in range(-48,49)],key=lambda q:q[0]*q[0]+q[1]*q[1])
  for dx,dy in off:
   b2=[bb[0]+dx,bb[1]+dy,bb[2]+dx,bb[3]+dy]
   if free(b2):x+=dx;y+=dy;break
  else:raise ValueError('Cannot place '+r)
 put(r,x,y,a)

for r,f in fs.items():
 if r.startswith('MH'):boxes[r]=box(f)
clusters={'Q101':'R101 R102','Q102':'R140 R141 R142 R143','U101':'R144 R145 R146 R150 R151 R152 R153','Q104':'R160 R161 R163 R165','Q105':'R164','Q106':'R162 R166','U301':'R301 R302 R303 R304 R305 R306'}
assigned={r:anchor for anchor,rs in clusters.items() for r in rs.split()}
for r in sorted(fs):
 if r in placed or r.startswith('MH'):continue
 anchor=assigned[r];cx,cy=placed[anchor][:2];f=fs[r];best=None
 for rad in range(3,65):
  for dx,dy in set([(d,-rad) for d in range(-rad,rad+1)]+[(d,rad) for d in range(-rad,rad+1)]+[(-rad,d) for d in range(-rad,rad+1)]+[(rad,d) for d in range(-rad,rad+1)]):
   x=cx+dx*.5;y=cy+dy*.5
   for angle in [0,90]:
    f.SetOrientationDegrees(angle);f.SetPosition(v(x,y));bb=box(f)
    if bb[0]<11.5 or bb[1]<11.5 or bb[2]>88.5 or bb[3]>64:continue
    if any(bb[0]<c[2]+.35 and bb[2]>c[0]-.35 and bb[1]<c[3]+.35 and bb[3]>c[1]-.35 for c in boxes.values()):continue
    score=math.hypot(x-cx,y-cy)
    for pad in f.Pads():
     if pad.GetNetname() in ['/GND','/VOUT_5V1','/VIN_PROTECTED']:continue
     pts=[xy(q.GetPosition()) for rr in placed for q in fs[rr].Pads() if q.GetNetCode()==pad.GetNetCode()]
     if pts:score+=min(math.dist(xy(pad.GetPosition()),q) for q in pts)*.5
    if best is None or score<best[0]:best=(score,x,y,angle)
  if best and rad>12:break
 assert best,r
 put(r,*best[1:])
for label,x,y,size in [('V1A-LITE  18-26V / 5A TARGET',49,65.5,.85),('NOT FOR FABRICATION',49,67,.9),('ENGINEERING REVIEW REQUIRED',49,68.3,.8),('24V IN',17,42,.8),('PI OUT',85,36,.8),('+',17,30,.8),('+',87.5,44,.8),('F301 7A',75,43.3,.8)]:text(b,label,x,y,size)
# All test pad IDs on silk; shift away from copper opening.
for r,f in fs.items():
 if r.startswith('TP'):
  f.Reference().SetLayer(p.F_Fab);f.Reference().SetPosition(f.GetPosition()+v(0,-1.6));f.Reference().SetTextSize(v(.6,.6))
(EV/'PLACEMENT.json').write_text(json.dumps(placed,indent=2)+'\n');save(b);print('Placed',len(placed))
