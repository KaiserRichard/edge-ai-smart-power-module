#!/usr/bin/env python3
"""Author reviewed capacitor/connector lands; never regenerate schematics.

Dimensions and deliberate assembly allowances are explained in
docs/evidence/r2/FOOTPRINTS_COMPLETE.md. Manufacturer sources/revisions/hashes
are pinned under third_party/footprints_complete; no third-party PCB is copied.
"""
import argparse
from pathlib import Path


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


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--part',choices=['tdk','xh2','xh4'],required=True)
    args=p.parse_args()
    name,text = tdk() if args.part=='tdk' else xh(int(args.part[-1]))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/(name+'.kicad_mod')).write_text(text)
    print(name)


if __name__=='__main__':main()
