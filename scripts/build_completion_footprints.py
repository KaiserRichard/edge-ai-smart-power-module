#!/usr/bin/env python3
"""Author reviewed capacitor/connector lands; never regenerate schematics.

Dimensions and deliberate assembly allowances are explained in
docs/evidence/r2/FOOTPRINTS_COMPLETE.md. Manufacturer sources/revisions/hashes
are pinned under third_party/footprints_complete; no third-party PCB is copied.
"""
import argparse
from pathlib import Path
from build_sheet03_preliminary import children

ROOT = Path(__file__).resolve().parents[1]


def frame(name, description, body, courtyard, attr):
    x1,y1,x2,y2 = courtyard
    lines = [f'(footprint "{name}" (version 20241229) (generator "v1a_footprint_completion")',
             '  (layer "F.Cu")', f'  (attr {attr})', f'  (descr "{description}")',
             f'  (fp_text reference "REF**" (at {(x1+x2)/2:g} {y1-1:g}) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))',
             f'  (fp_text value "{name}" (at {(x1+x2)/2:g} {y2+1:g}) (layer "F.Fab") (effects (font (size 0.6 0.6) (thickness 0.1))))']
    for rect,layer,width in [(body,'F.Fab',.1),(courtyard,'F.CrtYd',.05)]:
        a,b,c,d=rect
        lines.append(f'  (fp_rect (start {a:g} {b:g}) (end {c:g} {d:g}) (stroke (width {width:g}) (type solid)) (fill none) (layer "{layer}"))')
    return lines


def tdk():
    name = 'TDK_C5750_2220_A4.45_B1.30_C4.50'
    lines = frame(name, 'TDK C5750X7R1H226M250KB; US C-series catalog B11 Apr2011 p72 (PDF70), corroborated product record 2026-09-30; A inner gap4.45 B pad length1.30 C pad width4.50; nonpolar; no EP; process review required',
                  (-2.85,-2.5,2.85,2.5),(-3.8,-2.95,3.8,2.95),'smd')
    for n,x in [(1,-2.875),(2,2.875)]:
        lines.append(f'  (pad "{n}" smd rect (at {x} 0) (size 1.3 4.5) (layers "F.Cu" "F.Mask" "F.Paste") (solder_mask_margin 0.05))')
    return name, '\n'.join(lines+[')',''])


def xh(n):
    name=f'JST_B{n}B_XH_A_P2.50_THT'
    a=(n-1)*2.5
    # Same mounting-surface orientation as JST p2, rotated 180 degrees:
    # pin1 left, subsequent circuits +X, lock/front edge at negative Y.
    lines=frame(name, f'JST B{n}B-XH-A(LF)(SN); eXH.pdf retrieved2026-09-30 PDF metadata2025-07-30 pp2,4,5; no boss; pin1 square; mate XHP-{n} plus SXH-001T-P0.6; copper annulus and courtyard project choices',
                (-2.45,-2.35,a+2.45,3.4),(-2.95,-2.85,a+2.95,3.9),'through_hole')
    drill=1.0 if n==2 else .95
    for i in range(n):
        lines.append(f'  (pad "{i+1}" thru_hole {"rect" if i==0 else "oval"} (at {i*2.5:g} 0) (size 1.7 2) (drill {drill:g}) (layers "*.Cu" "*.Mask"))')
    lines.append('  (fp_text user "1" (at 0 -2.55) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.12))))')
    lines.append(f'  (fp_line (start -2.55 -2.45) (end {a+2.55:g} -2.45) (stroke (width 0.12) (type solid)) (layer "F.SilkS"))')
    return name,'\n'.join(lines+[')',''])


def vh():
    original='JST_VH_B2P-VH-FB-B_1x02_P3.96mm_Vertical'
    name='JST_B2P_VH_FB_B_P3.96_THT'
    text=(ROOT/'third_party/footprints_complete'/(original+'.kicad_mod')).read_text()
    text=text.replace(original,name)
    for a,b,form in reversed(list(children(text))):
        if form.startswith('(descr '):
            desc='JST B2P-VH-FB-B(LF)(SN); eVH.pdf metadata2026-01-09 pp1-4; pitch3.96 drill1.70 boss1.45; mate VHR-2N plus SVH-21T-P1.1; adapted unchanged geometry from KiCad f64dbd7 CC-BY-SA-4.0 with design exception; KiCad library contributors'
            text=text[:a]+'(descr "'+desc+'")'+text[b:]
        elif form.startswith('(model '):
            text=text[:a]+text[b:]
    return name,text


def phoenix():
    name='Phoenix_1776508_MSTB_2_GF_5.08'
    lines=frame(name, 'Phoenix Contact1776508 MSTB2.5/2-GF-5.08; Nov12,2013 p6 drilling drawing plus current product record2026-09-30; mate1777989; project terminal1 atleft; PTH1.40 pitch5.08; optional board fixing NPTH2.40; no EP/paste',
                (-7.62,-2,12.7,10),(-8.12,-2.5,13.2,10.5),'through_hole')
    for n,x in [(1,0),(2,5.08)]:
        lines.append(f'  (pad "{n}" thru_hole {"rect" if n==1 else "circle"} (at {x} 0) (size 2.8 2.8) (drill 1.4) (layers "*.Cu" "*.Mask"))')
    for x in [-5.08,10.16]:
        lines.append(f'  (pad "" np_thru_hole circle (at {x} 2.5) (size 2.4 2.4) (drill 2.4) (layers "*.Cu" "*.Mask"))')
    lines.append('  (fp_text user "1 +" (at 0 -2.2) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    lines.append('  (fp_rect (start -7.62 10) (end 12.7 20) (stroke (width 0.1) (type solid)) (fill none) (layer "Dwgs.User"))')
    lines.append('  (fp_text user "MATE / TOOL ACCESS - REVIEW" (at 2.54 21) (layer "Dwgs.User") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    return name,'\n'.join(lines+[')',''])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--part',choices=['tdk','xh2','xh4','vh','phoenix'],required=True)
    args=p.parse_args()
    name,text = {'tdk':tdk,'xh2':lambda:xh(2),'xh4':lambda:xh(4),'vh':vh,'phoenix':phoenix}[args.part]()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/(name+'.kicad_mod')).write_text(text)
    print(name)


if __name__=='__main__':main()
