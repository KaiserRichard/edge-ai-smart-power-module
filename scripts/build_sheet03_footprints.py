#!/usr/bin/env python3
"""Project-owned preliminary copper patterns from cited manufacturer dimensions.

No PCB is generated. Paste coverage is conservative and remains assembly review.
"""
from pathlib import Path
import re
from build_sheet03_preliminary import children
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'hardware/kicad/V1A_Qualified.pretty'
def pad(n,x,y,w,h,layers='"F.Cu" "F.Mask"'):
 return f'(pad "{n}" smd rect (at {x:g} {y:g}) (size {w:g} {h:g}) (layers {layers}))'
def save(name,desc,body,pads,marker):
 x,y=body;mx,my=marker
 lines=[f'(footprint "{name}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (attr smd)',f'(descr "{desc}; PRELIMINARY - NOT FOR FABRICATION")',f'(fp_text reference "REF**" (at 0 {-y-1.1}) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',f'(fp_text value "{name}" (at 0 {y+1.1}) (layer "F.Fab") (effects (font (size 0.6 0.6) (thickness 0.1))))',f'(fp_rect (start {-x} {-y}) (end {x} {y}) (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))',f'(fp_rect (start -3.8 -2.9) (end 3.8 2.9) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))',f'(fp_circle (center {mx} {my}) (end {mx+.15} {my}) (stroke (width 0.15) (type default)) (fill none) (layer "F.SilkS"))']
 (OUT/(name+'.kicad_mod')).write_text('\n'.join(lines+pads+[')'])+'\n')
def build():
 # SLPS488B p9 rotated board view: right row1(bottom)..4(top); left8..5.
 pads=[pad(5,-.941,0,3.85,4.52)]
 for n,y in [(5,-1.905),(6,-.635),(7,.635),(8,1.905)]:pads.append(pad(n,-3.161,y,.59,.71))
 for n,y in [(1,1.905),(2,.635),(3,-.635),(4,-1.905)]:
  pads.append(pad(n,2.77,y,1.372,.71));pads.append(pad('',2.77,y,1.25,.55,'"F.Paste"'))
 for x in [-1.763,-.119]:
  for y in [-1.569,-.523,.523,1.569]:pads.append(pad('',x,y,1.294,.746,'"F.Paste"'))
 for y in [-1.905,-.635,.635,1.905]:pads.append(pad('',-3.08,y,.5,.5,'"F.Paste"'))
 save('TI_Q5B_CSD18540Q5B','TI SLPS488B April2017 pp8-9; copper dimensions match Fig7.2; adapted reduced paste; assembly review OPEN',(3.05,2.55),pads,(3.55,2.55))
 pads=[pad(1,-2.975,0,1.55,3.60,'"F.Cu" "F.Paste" "F.Mask"'),pad(2,2.975,0,1.55,3.60,'"F.Cu" "F.Paste" "F.Mask"')]
 save('Vishay_WFM2512','Vishay30387 Rev04-Aug-2022 p2;2512 land a1.55 b3.60 l4.40mm',(3.175,1.59),pads,(-3.55,2.15))
 # TI DCT0008A is wider than the generic SOT-23-8 used in the interrupted
 # capture. SCES794G appended drawing4220784/D, pp19-21: 3.8mm row centers.
 pads=[]
 for n,y in [(1,-.975),(2,-.325),(3,.325),(4,.975)]:
  pads.append(pad(n,-1.9,y,1.1,.4,'"F.Cu" "F.Paste" "F.Mask"'))
 for n,y in [(8,-.975),(7,-.325),(6,.325),(5,.975)]:
  pads.append(pad(n,1.9,y,1.1,.4,'"F.Cu" "F.Paste" "F.Mask"'))
 save('TI_DCT0008A_SN74LVC1G74','TI4220784-D Oct2025 pp19-21;DCT0008A;8pads0.65pitch;1.1x0.4;row centers3.8',(1.5,1.5),pads,(-2.8,-1.5))
 # Vishay86406 Rev1.1 p1 numbers ANODE=1/CATHODE=2. Do not use a generic
 # cathode=1 symbol/footprint for this manufacturer's package pin contract.
 pads=[pad(1,-1.65,0,.9,1.2,'"F.Cu" "F.Paste" "F.Mask"'),pad(2,1.65,0,.9,1.2,'"F.Cu" "F.Paste" "F.Mask"')]
 save('Vishay_BAT46W_A1_K2','Vishay86406 Rev1.1 pp1,4;SOD123;1anode2cathode;0.9x1.2 lands;assembly review',(1.35,.8),pads,(-2.35,-.8))
 p=OUT/'Vishay_BAT46W_A1_K2.kicad_mod'
 p.write_text(p.read_text().rstrip()[:-1]+'\n(fp_line (start 0.9 -0.8) (end 0.9 0.8) (stroke (width 0.15) (type default)) (layer "F.Fab"))\n)\n')
 # Adapt only the numbered drain fingers from the isolated KiCad source.
 # Drain copper is internally common; all four physical pins remain present.
 src=ROOT/'third_party/kicad_gate2/Infineon_PG-TDSON-8_6.15x5.15mm.kicad_mod'
 text=src.read_text()
 for a,b,t in reversed(list(children(text))):
  if not t.startswith('(pad "5"'):continue
  xy=re.search(r'\(at ([-\d.]+) ([-\d.]+)',t)
  x,y=map(float,xy.groups())
  if x>2:
   number={-1.995:8,-.665:7,.665:6,1.995:5}[round(y,3)]
   text=text[:a]+t.replace('(pad "5"',f'(pad "{number}"',1)+text[b:]
 text=text.replace('Infineon_PG-TDSON-8_6.15x5.15mm','Infineon_BSC034N06NS_8pin')
 text=re.sub(r'\(descr "[^"]*"\)','(descr "Adapted KiCad9.0.6 land; Infineon BSC034N06NS Rev2.3 p1 pins1-3S4G5-8D; all8pins retained; NOT FOR FABRICATION")',text, count=1)
 # Original stock model name is retained: geometry did not change.
 text=text.replace('Infineon_BSC034N06NS_8pin.step','Infineon_PG-TDSON-8_6.15x5.15mm.step')
 (OUT/'Infineon_BSC034N06NS_8pin.kicad_mod').write_text(text)
 # PCH1V471MCL1GS is10x16mm, NOT10x10.2 or10x12.5. Its10.3mm base and
 # 4.6mm terminal spacing match the10mm-diameter family; use the reviewed
 # stock land geometry but remove the wrong-height3D model. See pin review.
 text=(ROOT/'third_party/kicad_gate2/CP_Elec_10x12.5.kicad_mod').read_text()
 for a,b,t in reversed(list(children(text))):
  if t.startswith('(model '):text=text[:a]+text[b:]
 text=text.replace('CP_Elec_10x12.5','Nichicon_PCH_10x16')
 text=re.sub(r'\(descr "[^"]*"\)','(descr "Nichicon PCH May2024 pp1-2;PCH1V471MCL1GS10x16mm;10.3base;4.6terminal gap;adapted KiCad10mm land;assembly review OPEN")',text,count=1)
 (OUT/'Nichicon_PCH_10x16.kicad_mod').write_text(text)
if __name__=='__main__':build()
