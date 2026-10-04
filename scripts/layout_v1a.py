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
 for a,c in [((10,10),(290,10)),((290,10),(290,225)),((290,225),(10,225)),((10,225),(10,10))]:
  e=p.PCB_SHAPE();e.SetShape(p.SHAPE_T_SEGMENT);e.SetStart(v(*a));e.SetEnd(v(*c));e.SetLayer(p.Edge_Cuts);e.SetWidth(mm(.05));b.Add(e)
 # Board-only NPTH mechanical holes; excluded from BOM and schematic parity.
 for i,(x,y) in enumerate([(15,15),(285,15),(15,220),(285,220)],1):
  f=p.FOOTPRINT(b);f.SetReference('MH'+str(i));f.SetValue('M3 NPTH - preliminary');f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES);f.SetPosition(v(x,y));b.Add(f)
  pad=p.PAD(f);pad.SetAttribute(p.PAD_ATTRIB_NPTH);pad.SetShape(p.PAD_SHAPE_CIRCLE);pad.SetSize(v(3.2,3.2));pad.SetDrillSize(v(3.2,3.2));pad.SetLayerSet(p.LSET.AllCuMask());pad.SetPosition(v(x,y));f.Add(pad)
  f.Reference().SetVisible(False);f.Value().SetVisible(False)
 title=b.GetTitleBlock();title.SetTitle('V1A test board - preliminary placed/routed study');title.SetComment(0,'NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED');b.SetTitleBlock(title)
 text(b,'V1A TEST BOARD  /  9-26 V INPUT  /  5 A TARGET',148,16,1.5)
 text(b,'NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED',148,21,1.4)
 text(b,'MANUAL CONTROLS: NO AUTOMATIC PROTECTION QUALIFICATION',147,217,1.2)
 return {f.GetReference():f for f in b.GetFootprints()}

PLACED={}
def put(fps,r,x,y,a=0):
 f=fps[r];f.SetOrientationDegrees(a);f.SetPosition(v(x,y));f.SetIsPlaced(True);f.SetNeedsPlaced(False);PLACED[r]=[x,y,a]
 f.Value().SetVisible(False)
 for fld in f.GetFields():
  if fld.GetName() not in ('Reference',):fld.SetVisible(False)
 f.Reference().SetTextSize(v(.85,.85));f.Reference().SetTextThickness(mm(.13));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetPosition(v(x,y-2.5))

def mechanics(b):
 fps=setup(b)
 for r,x,y,a in [('J501',17,81,270),('J502',277,76,90),('J503',284,118,90),('J301',105,210,0),('J302',125,210,0),('J603',145,210,0),('J604',165,210,0),('J605',185,210,0),('J606',205,210,0),('JP600',228,210,0)]:put(fps,r,x,y,a)
 return fps

def box(f):
 bb=f.GetBoundingBox(False,False);return [p.ToMM(bb.GetX()),p.ToMM(bb.GetY()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())]
def collision(f,fps,gap=.3):
 a=box(f)
 if a[0]<19 or a[1]<27 or a[2]>282 or a[3]>204:return True
 for r in PLACED:
  if r==f.GetReference():continue
  c=box(fps[r])
  if a[0]<c[2]+gap and a[2]>c[0]-gap and a[1]<c[3]+gap and a[3]>c[1]-gap:return True
 return False

def place(b):
 fps=mechanics(b)
 fixed={
 'F101':(32,75,0),'PF1':(25,61,0),'D101':(33,87,90),'Q101':(47,75,270),'Q102':(45,81,0),'U101':(54,75,0),'JP101':(61,57,0),'D102':(74,64,0),'PF2':(77,46,0),
 'U201':(67,91,0),'C203':(67.95,94,0),'C204':(67.95,88,0),'C201':(68,97.8,0),'C202':(69,84,0),'C205':(65.9,86,0),'R204':(63.1,88,90),'C206':(62,90,90),'R201':(63.5,96,0),'R202':(61,94,0),'R203':(60,91.7,0),'R205':(58,94,90),'C207':(58,97.5,90),
 'JP201':(88,91,0),'PF3':(78,106,0),'PF4':(98,106,0),'L201':(121,85.25,90),'JP202':(155,79.5,0),
 'Q301':(190,79.5,180),'Q302':(199,79.5,0),'JP301':(224,79.5,0),'R401':(262,79.5,0),
 'U301':(193,67,270),'C301':(196.4,69,90),'R304':(191,72,90),'R305':(195,75,90),'D302':(199.5,64,0),'C309':(190,63,0),'C306':(186,65,90),'JP660':(179,61,0),'D660':(177,67,0),'C660':(182,68,90),
 'JP501':(270,140,270),'PF5':(282,151,0),
 'JP331':(176,49,180),'Q330':(150,49,180),'U330':(144,43,0),'R384':(147.3,44,90),'R385':(145.5,48,90),'C368':(140.5,40,90),'C367':(143.5,38,0),'D330':(133,57,0),
 'JP330':(232,49,0),'Q303':(251,49,0),'U315':(257,43,180),'R306':(255,46,90),'R307':(256,49,90),'C308':(260.5,40,90),'D331':(266,51,0),
 'Q316':(35,132,180),'R332':(49,131,90),'U316':(56,130,0),'R333':(49,137,0),'C378':(37,142,0),'C307':(53,124,90),'D303':(37,110,90),'C350':(61.5,127,90),
 'U317':(73,137,0),'L301':(73,128,90),'C351':(80,136,90),'C380':(77.8,133.8,90),'C352':(65.5,137,90),'C377':(60.5,138,90),'C353':(76,143.5,0),'C379':(80.5,141,90),'C354':(79,130,90),'C355':(67,132,90),
 'U327':(96,137,0),'D304':(91,131,0),'C375':(93,137,90),'C376':(98.8,137,90),'C358':(110,131,90),'C359':(122,131,90),'R375':(98,133.5,90),'R374':(98,141,90),'C374':(101,143,90),
 'U306':(133,137,180),'C305':(138,137,90),'U318':(141,148,0),'C365':(137,145,90),'C366':(145,145,90),
 'U600':(105,157,180),'C601':(111,157,90),'C602':(99,157,90),'D600':(96,152,0),'R602':(98,148,0),'C600':(95,147,90),
 'U302':(159,141,0),'C302':(164,141,90),'C303':(154.5,140,90),'U303':(175,141,0),'C304':(177,137.5,0),'U321':(175,150,0),'C364':(180.5,148.5,90),'D321':(162,153,0),
 'U322':(147,156,0),'C369':(149,152.5,0),'U323':(158,162,0),'C370':(160,158.5,0),
 'U640':(106,115,0),'C640':(107.5,111.5,0),'U642':(115,115,0),'C642':(116.5,111.5,0),'U647':(110,124,0),'C647':(115.5,123.5,90),'R640':(104,102,90),
 'U607':(184,166,0),'C604':(185.5,162.5,0),'U651':(194,168,0),'C651':(199.5,166.5,90),
 'U401':(260,66,90),'R402':(259,71.5,90),'R403':(263,71.5,90),'C401':(261,68.5,0),'C402':(256,63.5,0),
 'U402':(248,69,0),'C403':(244.5,67,90),'C404':(250,62,0),'U403':(271,105,180),'C405':(275,108,90),'C406':(267,108,90),
 }
 # Main MLCC bank, power points north, ground south. Six across two rows.
 for i in range(6):fixed['C'+str(209+i)]=(173+(i%3)*6.5,85+(i//3)*8.5,270)
 # Raw bank beside its discharge strings. Protected bank beside the output rail.
 for i in range(8):fixed['C'+str(330+i)]=(143+(i%4)*13,65+(i//4)*-35,270)
 for i in range(4):fixed['C'+str(340+i)]=(214+i*13,96,90)
 # Two matched 6-resistor paths along the raw bank's upper edge.
 for row,refs in enumerate([[380,381,382,383,386,387],[388,389,390,391,392,393]]):
  for j,n in enumerate(refs):fixed['R'+str(n)]=(191+j*8.5,30+row*7,0)
 for r,z in {'R308':(216,41,270),'R309':(216,50,270),'R310':(225,41,270),'R311':(225,59,270)}.items():fixed[r]=z
 # Logic ICs and dedicated bypass pairs, quiet bottom region.
 logic=[602,662,614,628,615,616,617,610,623,612,630,631,611,632,633,644,654,656,661]
 caps={602:609,662:762,614:714,628:728,615:715,616:716,617:717,610:710,623:723,612:712,630:730,631:731,611:711,632:732,633:733,644:644,654:754,656:756,661:761}
 for i,n in enumerate(logic):
  x=110+(i%7)*19;y=177+(i//7)*12
  fixed['U'+str(n)]=(x,y,0);fixed['C'+str(caps[n])]=(x+2,y-4,0)
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
  # Candidate positions on a preliminary 0.5 mm placement grid; never alter pads.
  for rad in range(3,45):
   cand=[]
   for d in range(-rad,rad+1):cand.extend([(cx+d*.5,cy-rad*.5),(cx+d*.5,cy+rad*.5),(cx-rad*.5,cy+d*.5),(cx+rad*.5,cy+d*.5)])
   for x,y in cand:
    for a in (0,90,180,270):
     f.SetOrientationDegrees(a);f.SetPosition(v(x,y))
     if collision(f,fps):continue
     score=math.hypot(x-cx,y-cy)
     for pad in f.Pads():
      net=pad.GetNetname()
      if net.endswith('/GND') or net.endswith('/SAFE5') or net.startswith('unconnected'):continue
      pts=[q for rr,q in allpads.get(net,[]) if rr==anchor]
      if pts:score+=min(math.dist(xy(pad.GetPosition()),q) for q in pts)
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
 for label,x,y in [('INPUT / SURGE',35,52),('BUCK / SWITCH LINKS',91,119),('RAW BANK / DUMP',156,23.5),('SERIES ISOLATION',205,86),('PROTECTED BANK',236,110),('KELVIN MONITOR',258,56),('AUX SURGE / CONVERTER',58,154),('MANUAL LOGIC / OBSERVATIONS',178,207)]:text(b,label,x,y,.9)
 EV.joinpath('PLACEMENT.json').write_text(json.dumps(PLACED,indent=2)+'\n')
 print('Placed',len(PLACED),'electrical footprints')
 return fps

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('step',choices=['mechanical','placement']);args=a.parse_args();b=load()
 if args.step=='mechanical':mechanics(b)
 else:place(b)
 save(b)
