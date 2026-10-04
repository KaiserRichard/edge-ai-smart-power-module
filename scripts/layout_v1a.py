#!/usr/bin/env python3
"""Deterministic V1A test-board placement/power geometry. KiCad bundled Python.
Not a fabrication release. No schematic, footprint source or rule severities changed.
"""
import argparse, json, math, re
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
CAD=ROOT/'hardware/kicad'; EV=ROOT/'docs/evidence/r3/layout'
BOARD=CAD/'V1A.kicad_pcb'
def v(x,y): return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def xy(q): return (p.ToMM(q.x),p.ToMM(q.y))
def mm(x): return p.FromMM(x)

def load():
 from make_schematic_readable import parse,dump,nodes,prop,val
 import tempfile
 doc=parse(BOARD.read_text())
 doc=[n for n in doc if not (isinstance(n,list) and (n[0] in ('gr_line','gr_text','gr_rect','gr_circle','zone','segment','via','arc') or (n[0]=='footprint' and val(prop(n,'Reference')[2]).startswith('MH'))))]
 with tempfile.NamedTemporaryFile(suffix='.kicad_pcb',mode='w',delete=False) as tmp:
  tmp.write(dump(doc)); seed=tmp.name
 b=p.LoadBoard(seed)
 Path(seed).unlink()
 return b

def save(b):
 p.SaveBoard(str(BOARD),b,True)
 # pcbnew's SWIG stackup descriptor is opaque. Write the native stackup explicitly.
 s=BOARD.read_text(); start=s.index('\t(setup\n'); pos=start+len('\t(setup\n')
 if '\t\t(stackup\n' not in s:
  stack='\t\t(stackup\n'
  for name,kind,t in [('F.SilkS','Top Silk Screen',None),('F.Paste','Top Solder Paste',None),('F.Mask','Top Solder Mask',.01),('F.Cu','copper',.07),('dielectric 1','prepreg',.18),('In1.Cu','copper',.035),('dielectric 2','core',1.01),('In2.Cu','copper',.035),('dielectric 3','prepreg',.18),('B.Cu','copper',.07),('B.Mask','Bottom Solder Mask',.01),('B.Paste','Bottom Solder Paste',None),('B.SilkS','Bottom Silk Screen',None)]:
   stack+=f'\t\t\t(layer "{name}" (type "{kind}")'+(f' (thickness {t})' if t else '')+')\n'
  stack+='\t\t\t(copper_finish "None")\n\t\t\t(dielectric_constraints no)\n\t\t)\n'
  s=s[:pos]+stack+s[pos:]; BOARD.write_text(s)

def text(b,s,x,y,size=1,layer=p.F_SilkS):
 t=p.PCB_TEXT(b);t.SetText(s);t.SetPosition(v(x,y));t.SetTextSize(v(size,size));t.SetTextThickness(mm(.15));t.SetLayer(layer);b.Add(t);return t

def setup(b):
 b.SetCopperLayerCount(4)
 for a,c in [((10,10),(240,10)),((240,10),(240,205)),((240,205),(10,205)),((10,205),(10,10))]:
  e=p.PCB_SHAPE();e.SetShape(p.SHAPE_T_SEGMENT);e.SetStart(v(*a));e.SetEnd(v(*c));e.SetLayer(p.Edge_Cuts);e.SetWidth(mm(.05));b.Add(e)
 # Board-only NPTH mechanical holes; excluded from BOM and schematic parity.
 for i,(x,y) in enumerate([(15,15),(235,15),(15,200),(235,200)],1):
  f=p.FOOTPRINT(b);f.SetReference('MH'+str(i));f.SetValue('M3 NPTH - preliminary');f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES);f.SetPosition(v(x,y));b.Add(f)
  pad=p.PAD(f);pad.SetAttribute(p.PAD_ATTRIB_NPTH);pad.SetShape(p.PAD_SHAPE_CIRCLE);pad.SetSize(v(3.2,3.2));pad.SetDrillSize(v(3.2,3.2));pad.SetLayerSet(p.LSET.AllCuMask());pad.SetPosition(v(x,y));f.Add(pad)
  f.Reference().SetVisible(False);f.Value().SetVisible(False)
 title=b.GetTitleBlock();title.SetTitle('V1A test board - preliminary placed/routed study');title.SetComment(0,'NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED');b.SetTitleBlock(title)
 text(b,'V1A TEST BOARD  /  9-26 V INPUT  /  5 A TARGET',119,198,1.1)
 text(b,'NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED',119,201,1.0)
 text(b,'MANUAL CONTROLS: NO AUTOMATIC PROTECTION QUALIFICATION',119,195,0.8)
 return {f.GetReference():f for f in b.GetFootprints()}

PLACED={}
BOXES={}
def put(fps,r,x,y,a=0):
 f=fps[r];f.SetOrientationDegrees(a);f.SetPosition(v(x,y));f.SetIsPlaced(True);f.SetNeedsPlaced(False);PLACED[r]=[x,y,a];BOXES[r]=box(f)
 f.Value().SetVisible(False)
 for fld in f.GetFields():
  if fld.GetName() not in ('Reference',):fld.SetVisible(False)
 f.Reference().SetTextSize(v(.85,.85));f.Reference().SetTextThickness(mm(.13));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetPosition(v(x,y-2.5))

def mechanics(b):
 fps=setup(b)
 for r,x,y,a in [('J501',17,64.5,270),('J502',230,70.39,270),('J503',234,137,90),('J301',35,188,0),('J302',59,188,0),('J603',83,188,0),('J604',107,188,0),('J605',131,188,0),('J606',155,188,0),('JP600',187,188,0)]:put(fps,r,x,y,a)
 return fps

def box(f):
 bb=f.GetBoundingBox(False,False);return [p.ToMM(bb.GetX()),p.ToMM(bb.GetY()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())]
def collision(f,fps,gap=.3):
 a=box(f)
 if a[0]<19 or a[1]<19 or a[2]>232 or a[3]>184:return True
 for r in PLACED:
  if r==f.GetReference():continue
  c=BOXES[r]
  if a[0]<c[2]+gap and a[2]>c[0]-gap and a[1]<c[3]+gap and a[3]>c[1]-gap:return True
 return False

def place(b):
 fps=mechanics(b)
 fixed={
 'F101':(26,43,0),'PF1':(21,32,0),'D101':(26,57,90),'Q101':(35,49,0),'Q102':(32,54,0),'U101':(42,49,0),'JP101':(53,31,0),'D102':(70,43,0),'PF2':(75,29,0),
 'U201':(54,66,0),'C203':(54.95,69,0),'C204':(54.95,63,0),'C201':(55,72.8,0),'C202':(56,59,0),'C205':(52.9,61,0),'R204':(50.1,63,90),'C206':(49,65,90),'R201':(50.5,71,0),'R202':(48,69,0),'R203':(47,66.7,0),'R205':(45,69,90),'C207':(45,72.5,90),
 'JP201':(75,66,0),'PF3':(65,79,0),'PF4':(85,79,0),'L201':(109,60.25,90),'JP202':(144,54.5,0),
 'Q301':(164,54.5,180),'Q302':(173,54.5,0),'JP301':(194,54.5,0),'R401':(211,54.5,0),
 'U301':(168,44,270),'C301':(171.4,46,90),'R304':(165,48,90),'R305':(169,50,0),'D302':(174.5,41,0),'C309':(165,40,0),'C306':(161,42,90),'JP660':(166,32,0),'D660':(177,33,0),'C660':(180,38,90),
 'JP501':(212,136,270),'PF5':(220,151,0),
 'JP331':(79,43,180),'Q330':(59,43,180),'U330':(55,37,0),'R384':(57.5,39,90),'R385':(54,42,90),'C368':(51,34,90),'C367':(54,32,0),'D330':(91,31,0),
 'JP330':(199,101,0),'Q303':(221,101,0),'U315':(220,94,180),'R306':(224,97,90),'R307':(226,100,90),'C308':(224,91,90),'D331':(208,88,0),
 'Q316':(32,104,180),'R332':(46,103,90),'U316':(53,102,0),'R333':(46,109,0),'C378':(34,114,0),'C307':(50,96,90),'D303':(29,82,90),'C350':(58.5,99,90),
 'U317':(70,109,0),'L301':(70,100,270),'C351':(77,108,90),'C380':(74.8,105.8,90),'C352':(62.5,109,90),'C377':(57.5,110,90),'C353':(73,115.5,0),'C379':(77.5,113,90),'C354':(76,102,90),'C355':(64,104,90),
 'U327':(93,107,0),'D304':(88,101,0),'C375':(90,107,90),'C376':(95.8,107,90),'C358':(107,101,90),'C359':(119,101,90),'R375':(95,103.5,90),'R374':(95,111,90),'C374':(98,113,90),
 'U306':(132,108,180),'C305':(137,108,90),'U318':(143,109,0),'C365':(139,115,90),'C366':(147,106,90),
 'U600':(105,122,180),'C601':(111,122,90),'C602':(99,122,90),'D600':(96,117,0),'R602':(90,118,0),'C600':(86,120,90),
 'U302':(153,124,0),'C302':(158,124,90),'C303':(148.5,123,90),'U303':(171,124,0),'C304':(173,120.5,0),'U321':(176,135,0),'C364':(181.5,133.5,90),'D321':(157,135,0),
 'U322':(137,124,0),'C369':(139,120.5,0),'U323':(150,141,0),'C370':(152,137.5,0),
 'U640':(98,87,0),'C640':(99.5,83.5,0),'U642':(112,87,0),'C642':(113.5,83.5,0),'U647':(132,91,0),'C647':(137.5,90.5,90),'R640':(91,77,90),
 'U607':(172,153,0),'C604':(173.5,149.5,0),'U651':(189,151,0),'C651':(194.5,149.5,90),
 'U401':(211,40,270),'R402':(210.5,45.5,90),'R403':(212.5,45.5,90),'C401':(211.5,43.5,0),'C402':(207,38,0),
 'U402':(195,40,0),'C403':(191.5,38,90),'C404':(197,33,0),'U403':(213,119,180),'C405':(217,122,90),'C406':(209,122,90),
 }
 for i in range(6):fixed['C'+str(209+i)]=(148+(i%3)*6.5,66+(i//3)*8.5,270)
 for i in range(8):fixed['C'+str(330+i)]=(108+(i%4)*13,27+(i//4)*14,90)
 for i in range(4):fixed['C'+str(340+i)]=(178+i*13,77,90)
 for row,refs in enumerate([[380,381,382,383,386,387],[388,389,390,391,392,393]]):
  for j,n in enumerate(refs):fixed['R'+str(n)]=(99-j*8.5,20+row*7,180)
 for r,z in {'R308':(173,92,0),'R309':(182,92,0),'R310':(173,99,0),'R311':(182,99,0)}.items():fixed[r]=z
 logic=[602,662,614,628,615,616,617,610,623,612,630,631,611,632,633,644,654,656,661]
 caps={602:609,662:762,614:714,628:728,615:715,616:716,617:717,610:710,623:723,612:712,630:730,631:731,611:711,632:732,633:733,644:644,654:754,656:756,661:761}
 for i,n in enumerate(logic):
  x=29+(i%7)*17;y=135+(i//7)*12
  fixed['U'+str(n)]=(x,y,0);fixed['C'+str(caps[n])]=(x+2,y-4,0)
 # Compact the signal floor while allowing the actual force-link courtyards.
 for r,(x,y,a) in list(fixed.items()):
  if y>=90: fixed[r]=(x,y+20,a)
  elif r in ['U201','C203','C204','C201','C202','C205','R204','C206','R201','R202','R203','R205','C207','JP201','PF3','PF4','L201','JP202','Q301','Q302','JP301','R401','U301','C301','R304','R305','D302','C309','C306','JP660','D660','C660','U401','R402','R403','C401','C402','U402','C403','C404','U640','C640','U642','C642','R640'] or (r.startswith('C') and 209<=int(r[1:])<=214) or (r.startswith('C') and 340<=int(r[1:])<=343):
   fixed[r]=(x,y+15,a)
 fixed.update({'F101':(27,53,0),'D101':(26,66,90),'Q101':(35,64,270),'Q102':(34,70,0),'U101':(42,64,0),'JP101':(29,88,270),'D102':(42,99,0),'PF1':(19,44,0),'PF2':(47,107,0),
 'D303':(24,113,90),'JP331':(77,43,180),'Q330':(55,43,180),'U330':(51,36,0),'R384':(52,40,90),'R385':(50,43,90),'C368':(47,34,90),'C367':(50,31,0),
 'JP301':(193,69.5,0),'R401':(214,69.5,0),'U401':(214,55,270),'R402':(213.5,60.5,90),'R403':(215.5,60.5,90),'C401':(214.5,58.7,0),'C402':(210,53,0),
 'JP501':(212,164,270),'PF5':(224,180,0),'U403':(223,139,180),'C405':(227,142,90),'C406':(219,142,90),
 'R640':(87,103,90),'U640':(97,108,0),'C640':(98.5,104.5,0),'U642':(113,106,0),'C642':(114.5,102.5,0),
 'C203':(54.95,84.15,0),'C204':(54.95,77.85,0),'C202':(58,73.5,0),'C205':(52.9,75,0),'R204':(50.5,77.5,90),'C206':(49,80.4,90),'R203':(46,81.7,0),
 'C309':(163,53,0),'D330':(93,37,0),'C330':(110,26,90),'C334':(110,40,90),
 'R306':(225,116,90),'C401':(215,58.9,0),'C367':(49,28,0)})
 fixed.update({'PF3':(65,95.5,0),'PF4':(85,95.5,0),'PF5':(226,182,0),'C202':(57,73.5,0),'R204':(49.7,76.5,90),'R384':(50,39,90),'D330':(98,52,0),'JP330':(201,121,0),'D331':(208,104,0),'R402':(213.5,61.5,90),'R403':(215.5,61.5,90),'C401':(215,59.1,0)})
 for i in range(209,212):fixed['C'+str(i)]=(148+(i-209)*6.5,82,270)
 for i in range(340,344):fixed['C'+str(i)]=(178+(i-340)*13,92,270)
 fixed.update({'R384':(50,39.3,90),'JP330':(202,121,0),'Q303':(222,121,0),'R307':(228,120,270)})
 for i in range(212,215):fixed['C'+str(i)]=(148+(i-212)*6.5,90.5,270)
 for r,z in fixed.items():put(fps,r,*z)
 # Assign all remaining passives/testpoints to their explicit functional cluster.
 clusters={
 'U101':'C101 C102 C103 R101 R102 R103 R104 R105 R106 R107 R108 TP101 TP102 TP103',
 'U201':'R206 R207 TP201 TP202 TP203 TP204 TP502',
 'U301':'R322 R709 R710 R711 R723 TP304 TP305 TP313 TP314 TP319 TP334',
 'U315':'R321 R712 R713 TP309 TP335', 'U330':'TP315 TP336',
 'U316':'R323 R330 R331 TP329 TP330',
 'U317':'R340 R341 R342 R343 R344 R345 R346 C356 C357 TP331',
 'U327':'R376 R377 R378 R379 TP310 TP327 TP328 TP332',
 'U306':'R312 R313 R316 R370 TP311 TP324','U318':'TP333',
 'U600':'R600 R601 R603 TP316','U302':'R361 R373 TP303',
 'U303':'R301 R302 R303 R367 D301 D322 TP306 TP307','U321':'R717 R718',
 'U322':'R362 R363 R371 TP322','U323':'R364 R365 R372 TP323',
 'U607':'D601 C603 R604 R605 R606 R622 R623 D618 D619 R317 TP317',
 'U640':'R641 R642 R651 D640 D641 TP337 TP339',
 'U642':'R644 R645 R652 D642 D643 TP338 TP340',
 'U602':'R609 TP321','U610':'R649 R650 Q304 R647 R648 TP308 TP312',
 'U654':'R707','U656':'R708','U644':'R727 TP320','U661':'R728',
 'JP600':'R729 TP318','J605':'R730','J606':'R731',
 'U401':'R408 TP401 TP402 TP403','U402':'TP404 TP405 TP406','U403':'R404 R405 R406 R407',
 'J501':'TP501','J502':'TP302 TP503 TP504','JP501':'TP505','C210':'TP301',
 }
 assigned={r:anchor for anchor,refs in clusters.items() for r in refs.split()}
 allpads={}
 for r in PLACED:
  for pad in fps[r].Pads():
   if pad.GetNumber():allpads.setdefault(pad.GetNetname(),[]).append((r,xy(pad.GetPosition())))
 unplaced=sorted((r for r in fps if r not in PLACED and not r.startswith('MH')),key=lambda r:(r.startswith('TP'),r))
 for r in unplaced:
  f=fps[r];anchor=assigned.get(r)
  if not anchor:raise ValueError('No functional placement assignment: '+r)
  cx,cy=xy(fps[anchor].GetPosition());best=None
  shapes=[]
  for angle in [0,90,180,270]:
   f.SetPosition(v(0,0));f.SetOrientationDegrees(angle)
   bb=box(f);pp=[]
   for pad in f.Pads():
    netname=pad.GetNetname()
    if netname in ['/GND','/03_OUTPUT_PROTECTION/SAFE5'] or netname.startswith('unconnected'):continue
    pts=[q for rr,q in allpads.get(netname,[]) if rr==anchor]
    if pts:pp.append((xy(pad.GetPosition()),pts))
   shapes.append((angle,bb,pp))
  occupied=list(BOXES.values())
  for rad in range(3,60):
   cand=set()
   for d in range(-rad,rad+1):cand.update([(cx+d*.5,cy-rad*.5),(cx+d*.5,cy+rad*.5),(cx-rad*.5,cy+d*.5),(cx+rad*.5,cy+d*.5)])
   for x,y in sorted(cand):
    for a,bb,pp in shapes:
     aa=[bb[0]+x,bb[1]+y,bb[2]+x,bb[3]+y]
     if aa[0]<19 or aa[1]<19 or aa[2]>232 or aa[3]>184:continue
     if any(aa[0]<c[2]+.3 and aa[2]>c[0]-.3 and aa[1]<c[3]+.3 and aa[3]>c[1]-.3 for c in occupied):continue
     score=math.hypot(x-cx,y-cy)
     for (px,py),pts in pp:score+=min(math.hypot(px+x-qx,py+y-qy) for qx,qy in pts)
     if best is None or score<best[0]:best=(score,x,y,a)
   if best and rad>math.hypot(best[1]-cx,best[2]-cy)*2+4:break
  if not best:raise ValueError('No free placement: '+r)
  put(fps,r,*best[1:])
  for pad in f.Pads():
   if pad.GetNumber():allpads.setdefault(pad.GetNetname(),[]).append((r,xy(pad.GetPosition())))
 # References on assembly layer initially; silk labels are added in verified free space.
 for f in fps.values():
  if f.GetReference().startswith('MH'):continue
  f.Reference().SetLayer(p.F_Fab)
 for label,x,y in [('INPUT / SURGE',28,24),('BUCK / SWITCH LINKS',63,101),('RAW BANK',122,16),('SERIES ISOLATION',183,82),('PROTECTED BANK',190,103),('KELVIN MONITOR',211,30),('AUXILIARY POWER',51,144),('MANUAL LOGIC',117,183)]:text(b,label,x,y,.9)
 EV.joinpath('PLACEMENT.json').write_text(json.dumps(PLACED,indent=2)+'\n')
 print('Placed',len(PLACED),'electrical footprints')
 return fps

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('step',choices=['mechanical','placement']);args=a.parse_args();b=load()
 if args.step=='mechanical':mechanics(b)
 else:place(b)
 save(b)
