#!/usr/bin/env python3
"""Owner-authorized Phase D capture. Writes selected sheet/root; never touches PCB.
Standard symbols are resolved from the installed KiCad library. Electrical intent
is explicit in build_parts(); verify independently against C/C2 and fresh XML.
"""
import argparse, copy, csv, io, json, re, subprocess, uuid
from pathlib import Path
from make_schematic_readable import parse,dump as sexpr_dump,nodes,one,val,prop,allpins,q
def dump(node):
 return "\n".join(line.rstrip() for line in sexpr_dump(node).splitlines())
ROOT=Path(__file__).resolve().parents[1]; HW=ROOT/'hardware/kicad'; EV=ROOT/'docs/evidence/v1a_lite'
K=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport'); NS=uuid.UUID('f00e46f5-5a58-4686-bd01-f53dd1562bd8')
def uid(s):return str(uuid.uuid5(NS,s))
def fx(size=1.27,justify='',hide=False):return f'(effects (font (size {size} {size}))'+(f' (justify {justify})' if justify else '')+(' (hide yes)' if hide else '')+')'
def pr(n,v,x,y,hide=False):return f'(property {q(n)} {q(v)} (at {x} {y} 0) {fx(hide=hide)})'
BOM={}
for row in csv.DictReader(io.StringIO((EV/'PHASE_C2_BOM.csv').read_text())):
 for ref in row['ref'].split():BOM[ref]=dict(row)
for row in csv.DictReader(io.StringIO((EV/'PHASE_C3_BOM.csv').read_text())):
 if row['ref'] in ('Q101','Q102'):BOM[row['ref']]=dict(row,scope='COMMON_INPUT')
CACHE={}
def symbol(lid):
 lib,name=lid.split(':')
 if lib not in CACHE:CACHE[lib]={val(s[1]):s for s in nodes(parse((K/'symbols'/f'{lib}.kicad_sym').read_text()),'symbol')}
 def resolve(n):
  s=copy.deepcopy(CACHE[lib][n]); ex=nodes(s,'extends')
  if ex:
   base=resolve(val(ex[0][1])); bn=val(base[1]); base[1]=q(n)
   for u in nodes(base,'symbol'):u[1]=q(val(u[1]).replace(bn+'_',n+'_',1))
   for p in nodes(s,'property'):
    base=[x for x in base if not(isinstance(x,list) and x[0]=='property' and x[1]==p[1])];base.append(p)
   s=base
  return s
 return resolve(name)
# Keep the existing manufacturer-mapped LM61460 symbol, for which this KiCad
# installation has no standard symbol. Snapshot it before any sheet regeneration.
LMFILE=EV/'PHASE_D_LM61460_SYMBOL.kicad_sym'
if not LMFILE.exists():
 d=parse((HW/'02_BUCK_5V.kicad_sch').read_text()); s=next(s for s in nodes(d,'symbol') if val(prop(s,'Reference')[2])=='U201'); lid=val(one(s,'lib_id')[1]); l=next(s for s in one(d,'lib_symbols')[1:] if val(s[1])==lid);LMFILE.write_text(dump(l)+'\n')
PARTS={1:[],2:[],3:[],5:[]}
def add(sheet,ref,value,lid,fp,pins,**extra):
 row=BOM.get(ref,{})
 PARTS[sheet].append(dict(ref=ref,value=value,lid=lid,fp=fp,pins={str(k):v for k,v in pins.items()},mpn=row.get('mpn','PCB_FEATURE'),manufacturer=row.get('manufacturer','PCB'),source=row.get('source','Project-owned copper feature'),lcsc=(re.search(r'/(C\d+)\.html',row.get('source','')).group(1) if re.search(r'/(C\d+)\.html',row.get('source','')) else 'OPEN' if row else 'N/A'),price=row.get('unit_vnd','0'),scope=row.get('scope','PCB_FEATURE'),**extra))
def r(sh,ref,v,a,b):add(sh,ref,v,'Device:R','Resistor_SMD:R_'+('0805_2012Metric' if BOM[ref]['mpn'].startswith('0805') else '0603_1608Metric'),{1:a,2:b})
def c(sh,ref,v,a,b='GND',case='0603',polar=False):
 fp=('Capacitor_THT:CP_Radial_D10.0mm_P5.00mm' if ref in ('C217','C218') else 'Capacitor_THT:CP_Radial_D8.0mm_P3.50mm') if polar else f'Capacitor_SMD:C_{case}_'+{'0402':'1005','0603':'1608','0805':'2012','1206':'3216','1210':'3225'}[case]+'Metric'
 add(sh,ref,v,'Device:C_Polarized' if polar else 'Device:C',fp,{1:a,2:b})
def transistor(ref,sh,kind,b,e,coll):add(sh,ref,BOM[ref]['mpn'],'Transistor_BJT:'+kind,'Package_TO_SOT_SMD:SOT-23',{1:b,2:e,3:coll})
def z(ref,v,k,a):add(1,ref,v,'Device:D_Zener','Diode_SMD:D_SOD-123',{1:k,2:a})
def tp(sh,ref,net):add(sh,ref,net,'Connector:TestPoint','TestPoint:TestPoint_Pad_D2.0mm',{1:net},feature=True)
def build_parts():
 add(1,'F101','3A / 125V','Device:Fuse','Fuse:Fuse_Littelfuse-NANO2-451_453',{1:'VIN_RAW',2:'VIN_FUSED'})
 add(1,'D101','SMCJ64CA','Device:D_TVS','Diode_SMD:D_SMC',{1:'VIN_FUSED',2:'GND'})
 for ref,drain,gate in [('Q101','VIN_FUSED','REV_GATE'),('Q102','VIN_PROTECTED','CUT_GATE')]:add(1,ref,'IRFR6215TRPBF','Transistor_FET:Q_PMOS_GDS','Package_TO_SOT_SMD:TO-252-2',{1:gate,2:drain,3:'S_COMMON'})
 z('D102','12V','S_COMMON','REV_GATE');z('D103','12V','S_COMMON','CUT_GATE')
 r(1,'R101','10k','REV_GATE','REV_PULL');r(1,'R102','10k','REV_PULL','GND')
 add(1,'D106','TVS3300DRVR','Power_Protection:TVS3300DRV','Package_DFN_QFN:DFN-6-1EP_2x2mm_P0.65mm_EP1x1.6mm',{1:'GND',2:'GND',3:'GND',4:'VIN_PROTECTED',5:'VIN_PROTECTED',6:'VIN_PROTECTED',7:'GND'})
 c(1,'C101','100uF / 50V','VIN_PROTECTED',polar=True)
 # Ballast: two eight-resistor strings, net 4k.
 for start,prefix in [(110,'BA'),(118,'BB')]:
  for i in range(8):r(1,f'R{start+i}','1k','S_COMMON' if i==0 else f'{prefix}{i}', 'CTRL12' if i==7 else f'{prefix}{i+1}')
 z('D104','12V','CTRL12','GND');c(1,'C102','1uF / 16V','CTRL12',case='0805')
 r(1,'R150','100k / 0.1%','S_COMMON','OVIN_D1');r(1,'R151','1k / 0.1%','OVIN_D1','OVIN_D2');r(1,'R152','1k / 0.1%','OVIN_D2','OVIN_REF');r(1,'R153','10k / 0.1%','OVIN_REF','GND')
 add(1,'U101','TL431BIDBZR','Reference_Voltage:TL431DBZ','Package_TO_SOT_SMD:SOT-23',{1:'OVIN_K',2:'OVIN_REF',3:'GND'})
 r(1,'R144','1k','CTRL12','OVIN_K');z('D105','3.3V','OVIN_K','BASE_SHIFT');r(1,'R145','10k','BASE_SHIFT','IN_NPN_BASE');r(1,'R146','100k','IN_NPN_BASE','GND')
 transistor('Q103',1,'MMBTA42','IN_NPN_BASE','GND','GATE_SINK')
 for i in range(6):r(1,f'R{130+i}','100R','CUT_GATE' if i==0 else f'GS{i}','GATE_SINK' if i==5 else f'GS{i+1}')
 for start,prefix in [(140,'PUA'),(142,'PUB')]:
  r(1,f'R{start}','1k','S_COMMON',prefix);r(1,f'R{start+1}','1k',prefix,'CUT_GATE')
 transistor('Q104',1,'MMBTA42','SET_LATCH','GND','LATCH_NCOL');transistor('Q105',1,'BC807','LATCH_PBASE','CTRL12','LATCH_H');transistor('Q106',1,'MMBTA42','CLAMP_BASE','GND','IN_NPN_BASE')
 for ref,a,b in [('R160','LATCH_PBASE','LATCH_NCOL'),('R161','LATCH_H','SET_LATCH'),('R162','LATCH_H','CLAMP_BASE'),('R163','CB_COLLECTOR','SET_LATCH')]:r(1,ref,'10k',a,b)
 for ref,a,b in [('R164','CTRL12','LATCH_PBASE'),('R165','SET_LATCH','GND'),('R166','CLAMP_BASE','GND')]:r(1,ref,'100k',a,b)
 for ref,net in [('TP110','SET_LATCH'),('TP111','LATCH_H'),('TP112','IN_NPN_BASE')]:tp(1,ref,net)
 add(2,'U201','LM61460AANRJRR','V1A:U201_LM61460AANRJRR','V1A_Qualified:TI_RJR0014A_LM61460',{1:'GND',2:'BUCK_VCC',3:'GND',4:'BUCK_FB',5:None,6:'BUCK_RT',7:'BUCK_EN',8:'VIN_PROTECTED',9:'GND',10:'BUCK_SW',11:'GND',12:'VIN_PROTECTED',13:'BUCK_RBOOT',14:'BUCK_CBOOT'})
 add(2,'L201','6.8uH / SRP1265A','Device:L','V1A_Lite:Bourns_SRP1265A',{1:'BUCK_SW',2:'VOUT_5V1'})
 for n in [201,202,215,216]:c(2,f'C{n}','10uF / 50V','VIN_PROTECTED',case='1210')
 for n in [203,204]:c(2,f'C{n}','100nF / 50V','VIN_PROTECTED')
 c(2,'C205','100nF / 16V','BUCK_CBOOT','BUCK_SW');c(2,'C206','1uF / 16V','BUCK_VCC',case='0805');c(2,'C207','22pF / C0G','VOUT_5V1','FF_MID',case='0402')
 for n in range(209,215):c(2,f'C{n}','47uF / 25V','VOUT_5V1',case='1206')
 for n in [217,218]:c(2,f'C{n}','1000uF / 10V','VOUT_5V1',polar=True)
 for ref,v,a,b in [('R201','33.2k','BUCK_RT','GND'),('R202','100k / 0.1%','VOUT_5V1','BUCK_FB'),('R203','24.6k / 0.1%','BUCK_FB','GND'),('R204','0R','BUCK_RBOOT','BUCK_CBOOT'),('R205','1k','FF_MID','BUCK_FB'),('R206','100k','VIN_PROTECTED','BUCK_EN'),('R207','24.6k / 0.1%','BUCK_EN','GND')]:r(2,ref,v,a,b)
 add(3,'F301','7A / wiring backup','Device:Fuse','Fuse:Fuse_Littelfuse-NANO2-451_453',{1:'VOUT_5V1',2:'VOUT_PI'})
 add(3,'SCR301','TYN612RG','Triac_Thyristor:TIC106','Package_TO_SOT_THT:TO-220-3_Vertical',{1:'GND',2:'VOUT_5V1',3:'SCR_GATE'})
 add(3,'U301','TL431BIDBZR','Reference_Voltage:TL431DBZ','Package_TO_SOT_SMD:SOT-23',{1:'OVOUT_K',2:'OVOUT_REF',3:'GND'})
 transistor('Q301',3,'BC807','CB_PBASE','VOUT_5V1','CB_COLLECTOR')
 for ref,v,a,b in [('R301','1k / 0.1%','VOUT_5V1','OVOUT_D1'),('R302','100R / 0.1%','OVOUT_D1','OVOUT_D2'),('R303','30R / 1%','OVOUT_D2','OVOUT_REF'),('R304','1k / 0.1%','OVOUT_REF','GND'),('R305','500R','CB_PBASE','OVOUT_K'),('R306','10k','VOUT_5V1','CB_PBASE'),('R307','100R','CB_COLLECTOR','SCR_GATE'),('R308','1k','SCR_GATE','GND')]:r(3,ref,v,a,b)
 for n in [301,302]:c(3,f'C{n}','47uF / 16V','VOUT_PI',case='1210')
 for ref,rail,v in [('J501','VIN_RAW','24V INPUT'),('J502','VOUT_PI','PI 5V OUTPUT')]:add(5,ref,v,'Connector_Generic:Conn_01x02','V1A_Qualified:JST_B2P_VH_FB_B_P3.96_THT',{1:rail,2:'GND'})
 for ref,net in [('TP501','VIN_RAW'),('TP502','VIN_FUSED'),('TP503','VIN_PROTECTED'),('TP504','VOUT_5V1'),('TP505','VOUT_PI'),('TP506','GND'),('TP507','CTRL12'),('TP508','CB_COLLECTOR')]:tp(5,ref,net)
 add(5,'J503','DUMMY LOAD + / -','Connector_Generic:Conn_01x02','V1A_Lite:Dummy_Load_Pads',{1:'VOUT_PI',2:'GND'},feature=True)
 # Genuine incoming supply/return. VIN_PROTECTED annotation expresses the
 # supply carried through passive fuse/PFET elements; independently checked.
 for ref,rail in [('#FLG01','VIN_RAW'),('#FLG02','GND'),('#FLG03','VIN_PROTECTED')]:add(5,ref,'PWR_FLAG','power:PWR_FLAG','',{1:rail},flag=True)
NAMES={1:'01_INPUT_PROTECTION',2:'02_BUCK_5V',3:'03_OUTPUT_PROTECTION',5:'05_IO_TEST'}
PORTS={1:['VIN_RAW','VIN_FUSED','VIN_PROTECTED','CTRL12','CB_COLLECTOR','GND'],2:['VIN_PROTECTED','VOUT_5V1','GND'],3:['VOUT_5V1','VOUT_PI','CB_COLLECTOR','GND'],5:['VIN_RAW','VIN_FUSED','VIN_PROTECTED','VOUT_5V1','VOUT_PI','CTRL12','CB_COLLECTOR','GND']}
NOTES={1:['F101 -> Q101 drain; common sources -> Q102 drain -> VIN_PROTECTED. 18-26V normal / 24V nominal.', 'Q101 reverse blocking; Q102 forward cutoff. 150V FETs, separate 12V VGS clamps. D101 upstream; D106 downstream.', 'R110-117 and R118-125: parallel 8k strings = 4k. R130-135: 600R. R140-143: parallel 2k strings = 1k.', 'CTRL12 is upstream of Q102. Q104/Q105 regenerative latch drives Q106 to clamp Q103 base.', 'Reset intended ONLY by input removal. Capture, hold-up, brownout, hot SOA and maximum shutdown time OPEN.'],2:['100k / 24.6k feedback: nominal 5.065V. BIAS grounded; PGOOD intentionally NC; EN independent of fault latch.', 'C217/C218 bulk on raw rail with six 25V MLCCs. No fuse or link separates this bank from SCR301.', 'Follow TI dual input loops, quiet AGND/FB return and native SW bootstrap connection. Layout not authorized.', 'Effective capacitance, inrush, loop stability, ripple and thermal limits require bench qualification.'],3:['SCR301 anode, Q301 emitter and divider top are directly on VOUT_5V1. No series fuse to raw capacitors.', 'F301 is fitted in Pi branch only: wiring backup, NOT crowbar clearing. VOUT_PI replaces historical LOAD_5V1.', 'CB_COLLECTOR triggers Sheet01 R163 and SCR gate simultaneously. Latch shuts Q102 independent of buck controls.', 'Kelvin detector ground/sense away from SCR pulse return. TYN612 tab = anode; insulation/thermal hardware OPEN.', 'Pi <5.5V, SCR pulse/di-dt, nuisance trips and raw/bulk containment remain OPEN. No Pi during fault tests.'],5:['J501: 24V nominal auxiliary input. J502: dedicated Pi POWER harness only; pin1 positive, pin2 GND.', 'J503: soldered dummy/electronic-load leads; PCB copper pads, no purchased connector or extra series element.', 'No Sheet04, telemetry or R401. VOUT_PI runs directly from F301 to J502/J503; no shunt or removable link.', 'Power flags identify incoming supply/return and the real switched supply through F101/Q101/Q102.', 'Bench: inspect -> continuity -> current limit -> no load -> rail -> dummy load steps -> thermal/ripple -> transients', '-> OV/crowbar/latch/fault qualification -> Pi ONLY after all gates pass. Harness/backfeed/current rating OPEN.']}
class Drawing:
 def __init__(self,name):self.name=name;self.items=[];self.libs={};self.n=0
 def key(self):self.n+=1;return uid(f'{self.name}:{self.n}')
 def text(self,t,x,y,size=1.27):self.items.append(f'(text {q(t)} (at {x} {y} 0) {fx(size,"left top")} (uuid {q(self.key())}))')
 def wire(self,x,y,xx,yy):self.items.append(f'(wire (pts (xy {x} {y}) (xy {xx} {yy})) (stroke (width 0) (type default)) (uuid {q(self.key())}))')
 def label(self,t,x,y,right=False):self.items.append(f'(label {q(t)} (at {x} {y} {180 if right else 0}) {fx(1.016,"right bottom" if right else "left bottom")} (uuid {q(self.key())}))')
 def part(self,p,x,y):
  ref=p['ref'];lid=p['lid'];lib=parse(LMFILE.read_text()) if lid.startswith('V1A:') else symbol(lid)
  lib[1]=q(lid);self.libs[lid]=dump(lib)
  pins=allpins(lib);assert set(p['pins'])=={val(one(a,'number')[1]) for a in pins},(ref,p['pins'],[(val(one(a,'number')[1]),val(one(a,'name')[1])) for a in pins])
  flag=p.get('flag',False);physical='no' if flag else 'yes';bom='no' if flag or p.get('feature') else 'yes'
  # Fields placed above body; enough vertical clearance for all pin labels.
  ph=max([abs(float(one(a,'at')[2])) for a in pins]+[4]);fy=y-ph-14
  props=[pr('Reference',ref,x,fy,flag),pr('Value',p['value'],x,fy+2.54,flag),pr('Footprint',p['fp'],x,y,True),pr('MPN',p['mpn'],x,y,True),pr('LCSC',p['lcsc'],x,y,True),pr('Manufacturer',p['manufacturer'],x,y,True),pr('Source',p['source'],x,y,True),pr('Unit_VND',p['price'],x,y,True),pr('Cost_scope',p['scope'],x,y,True)]
  self.items.append(f'(symbol (lib_id {q(lid)}) (at {x} {y} 0) (unit 1) (in_bom {bom}) (on_board {physical}) (dnp no) (uuid {q(uid(ref))}) '+ ' '.join(props)+f' (instances (project "V1A" (path "/{uid("V1A")}/{uid(self.name)}" (reference {q(ref)}) (unit 1)))))')
  done=set()
  for pin in pins:
   num=val(one(pin,'number')[1]);net=p['pins'][num];at=one(pin,'at');px=x+float(at[1]);py=y-float(at[2]);angle=int(at[3]);pos=(px,py)
   if pos in done:continue
   done.add(pos)
   if net is None:self.items.append(f'(no_connect (at {px} {py}) (uuid {q(self.key())}))');continue
   dx,dy={0:(-5.08,0),180:(5.08,0),90:(0,5.08),270:(0,-5.08)}[angle]
   xx=round(px+dx,4);yy=round(py+dy,4);self.wire(px,py,xx,yy);self.label(net,xx,yy,right=dx<0)
 def save(self):
  footer='(sheet_instances (path "/" (page "1")))' if self.name=='V1A' else ''
  s=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(uid(self.name))}) (paper "A2") (title_block (title {q("V1A-Lite / "+self.name)}) (date "2026-10-05") (rev "1R-D") (comment 1 "NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED") (comment 2 "Capture only; electrical qualification OPEN; no PCB work")) (lib_symbols '+ ' '.join(self.libs.values())+') '+' '.join(self.items)+footer+')'
  (HW/f'{self.name}.kicad_sch').write_text(dump(parse(s))+'\n')
def sheet(n):
 d=Drawing(NAMES[n]);d.text('V1A-Lite 1R / '+NAMES[n],15.24,12.7,2.54)
 for i,t in enumerate(NOTES[n]):d.text(t,15.24,20.32+i*3.81)
 # Labelled cells preserve standard electronic glyphs and exact pin identities.
 # A2 sheet makes the dense 16-part ballast explicit rather than collapsing BOM.
 for i,p in enumerate(PARTS[n]):
  if n==2 and i==0:d.part(p,83.82,104.14);continue
  idx=i-1 if n==2 else i
  ybase=170.18 if n==2 else 83.82
  d.part(p,40.64+(idx%7)*76.2,ybase+(idx//7)*33.02)
 for i,net in enumerate(PORTS[n]):
  x=22.86+i*71.12;y=398.78
  d.items.append(f'(hierarchical_label {q(net)} (shape passive) (at {x} {y} 0) {fx(1.016,"left")} (uuid {q(d.key())}))');d.wire(x,y,x-5.08,y);d.label(net,x-5.08,y,right=True)
 d.save()
def root(completed):
 d=Drawing('V1A');d.text('V1A-Lite / OPTION 1R / PHASE D SCHEMATIC CAPTURE',20.32,20.32,3)
 d.text('18-26V normal (24V nominal) -> input cutoff -> LM61460 -> raw SCR crowbar -> wiring fuse -> Pi power',20.32,30.48,1.7)
 d.text('Owner selected 2026-10-05. Historical research design: v1a-research-schematic / v1a-research-layout-wip.',20.32,38.1)
 d.text('NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED. No electrical safety or bench validation claimed.',20.32,45.72,1.7)
 d.text('Sheet04 telemetry removed. No I2C, USB3 or D435i routing. All power returns are GND; Kelvin geometry is an R3 gate.',20.32,53.34)
 for idx,n in enumerate(completed):
  x=55.88+(idx%2)*266.7;y=83.82+(idx//2)*134.62;name=NAMES[n];ports=PORTS[n];ps=[]
  for i,net in enumerate(ports):
   yy=y+15.24+i*10.16;ps.append(f'(pin {q(net)} passive (at {x} {yy} 180) {fx(1.27,"left")} (uuid {q(d.key())}))');d.wire(x,yy,x-15.24,yy);d.label(net,x-15.24,yy,right=True)
  d.items.append(f'(sheet (at {x} {y}) (size 185.42 111.76) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid {q(uid(name))}) '+pr('Sheetname',name,x+80,y-3.81)+pr('Sheetfile',name+'.kicad_sch',x+80,y+115.57)+' '+' '.join(ps)+f' (instances (project "V1A" (path "/{uid("V1A")}" (page "{idx+2}")))))')
 d.text('CB_COLLECTOR: Sheet03 PNP collector -> Sheet01 R163 -> SET_LATCH. Fault inhibition acts on Q102 via Q106/Q103.',20.32,370.84)
 d.text('F301-open leaves SCR301, detector and raw capacitors on the same VOUT_5V1 node. VOUT_PI is downstream of F301.',20.32,378.46)
 d.save()
def footprint():
 out=HW/'V1A_Lite.pretty';out.mkdir(exist_ok=True)
 for name,pads,bounds,desc in [('Bourns_SRP1265A',[(1,-5.55,0,3.1,5),(2,5.55,0,3.1,5)],(7.35,6.65),'Bourns SRP1265A Rev06/24 p1: outer14.2 inner8.0 land height5.0; 6.8uH lead-frame'),('Dummy_Load_Pads',[(1,-5,0,5,5),(2,5,0,5,5)],(8,3),'Project-owned exposed copper solder pads for dummy-load leads; current/strain relief qualification OPEN')]:
  w,h=bounds
  # Assemble below to avoid parenthesis ambiguity.
  parts=[f'(footprint "{name}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (descr {q(desc)}) (attr smd)',f'(fp_text reference "REF**" (at 0 {-h-2}) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))',f'(fp_text value "{name}" (at 0 {h+2}) (layer "F.Fab") (effects (font (size 1 1) (thickness .15))))',f'(fp_rect (start {-w} {-h}) (end {w} {h}) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))']
  if name=='Bourns_SRP1265A':parts.append('(fp_rect (start -6.75 -6.25) (end 6.75 6.25) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))')
  for num,x,y,sx,sy in pads:parts.append(f'(pad "{num}" smd rect (at {x} {y}) (size {sx} {sy}) (layers "F.Cu" "F.Mask"'+(' "F.Paste"' if name=='Bourns_SRP1265A' else '')+'))')
  (out/(name+'.kicad_mod')).write_text('\n'.join(parts)+')\n')
 table=HW/'fp-lib-table';d=parse(table.read_text())
 if not any(val(one(l,'name')[1])=='V1A_Lite' for l in nodes(d,'lib')):d.append(parse('(lib (name "V1A_Lite") (type "KiCad") (uri "${KIPRJMOD}/V1A_Lite.pretty") (options "") (descr "Phase D manufacturer-derived lands; review required"))'));table.write_text(dump(d)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--sheet',type=int,choices=[1,2,3,5],required=True);args=ap.parse_args()
 assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='feat/v1a-lite-cost-reduction'
 build_parts();footprint();sheet(args.sheet)
 completed=[n for n in [1,2,3,5] if n<=args.sheet];root(completed)
 (EV/f'PHASE_D_SHEET{args.sheet:02}_INTENT.json').write_text(json.dumps(PARTS[args.sheet],indent=2)+'\n')
 print('Captured',NAMES[args.sheet],len(PARTS[args.sheet]),'symbols')
