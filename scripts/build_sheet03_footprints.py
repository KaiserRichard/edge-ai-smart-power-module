#!/usr/bin/env python3
"""Project-owned preliminary copper patterns from cited manufacturer dimensions.

No PCB is generated. Paste coverage is conservative and remains assembly review.
"""
from pathlib import Path
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
if __name__=='__main__':build()
