#!/usr/bin/env python3
"""Reproduce the three R2 project footprints from reviewed manufacturer drawings.

Requires PyMuPDF for TI's vector copper/stencil artwork. Does not edit schematics.
See docs/evidence/r2/forensic_2026-09-14/CRITICAL_FOOTPRINT_QUALIFICATION.md.
"""
import argparse
import hashlib
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[1]


def drawing_loops(page, color):
    """Join only the reviewed colored pad outlines; approximate cubic fillets."""
    segments = []
    for drawing in page.get_drawings():
        if drawing['color'] is None or any(abs(a-b) > .01 for a,b in zip(drawing['color'], color)):
            continue
        for item in drawing['items']:
            if item[0] in ('l', 'c') and all(100 < p.y < 490 for p in item[1:]):
                segments.append(list(item[1:]))
    def near(a, b):
        return abs(a.x-b.x) < .015 and abs(a.y-b.y) < .015
    polygons = []
    while segments:
        chain = [segments.pop(0)]
        while not near(chain[0][0], chain[-1][-1]):
            end = chain[-1][-1]
            for i, segment in enumerate(segments):
                if near(end, segment[0]):
                    chain.append(segments.pop(i))
                    break
                if near(end, segment[-1]):
                    chain.append(list(reversed(segments.pop(i))))
                    break
            else:
                raise ValueError('Manufacturer outline failed to close')
        polygon = []
        for points in chain:
            if len(points) == 2:
                polygon.append(tuple(points[0]))
            else:
                for i in range(17):
                    t = i/17
                    u = 1-t
                    polygon.append(tuple(u**3*points[0][k]+3*u*u*t*points[1][k]+3*u*t*t*points[2][k]+t**3*points[3][k] for k in (0,1)))
        polygons.append(polygon)
    return polygons


def rectangle(x, y, w, h):
    return [(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)]


def pad(number, polygon, layers, anchor=None):
    # A small anchor inside the copper avoids adding unintended metal to custom shapes.
    if anchor is None:
        def inside(x, y):
            crossings = 0
            for (ax,ay),(bx,by) in zip(polygon,polygon[1:]+polygon[:1]):
                if (ay > y) != (by > y) and x < (bx-ax)*(y-ay)/(by-ay)+ax:
                    crossings += 1
            return crossings % 2 == 1
        xmin, xmax = min(x for x,y in polygon), max(x for x,y in polygon)
        ymin, ymax = min(y for x,y in polygon), max(y for x,y in polygon)
        candidates = [((xmin+xmax)/2,(ymin+ymax)/2)]
        candidates += [(xmin+(xmax-xmin)*i/10,ymin+(ymax-ymin)*j/10)
                       for i in range(1,10) for j in range(1,10)]
        anchor = next((x,y) for x,y in candidates
                      if all(inside(x+dx,y+dy) for dx in [-.006,.006] for dy in [-.006,.006]))
    x,y = anchor
    points = ' '.join(f'(xy {px-x:.5f} {py-y:.5f})' for px,py in polygon)
    return (f'  (pad "{number}" smd custom (at {x:.5f} {y:.5f}) (size 0.01 0.01) '
            f'(layers {layers}) (solder_mask_margin 0.05) '
            f'(options (clearance outline) (anchor rect)) '
            f'(primitives (gr_poly (pts {points}) (width 0) (fill yes))))')


def footprint(name, description, body, courtyard, pads, marker):
    lines = [f'(footprint "{name}" (version 20241229) (generator "qualified_r2")',
             '  (layer "F.Cu") (attr smd)', f'  (descr "{description}")',
             f'  (fp_text reference "REF**" (at 0 {-courtyard[1]-1:.3f}) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))',
             f'  (fp_text value "{name}" (at 0 {courtyard[1]+1:.3f}) (layer "F.Fab") (effects (font (size 0.65 0.65) (thickness 0.1))))']
    for layer, size, width in [('F.Fab',body,.1),('F.CrtYd',courtyard,.05)]:
        x,y = size
        lines.append(f'  (fp_rect (start {-x} {-y}) (end {x} {y}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))')
    x,y = marker
    lines.append(f'  (fp_circle (center {x} {y}) (end {x+.12} {y}) (stroke (width 0.12) (type default)) (fill none) (layer "F.SilkS"))')
    return '\n'.join(lines+pads+[')', ''])


def build(output):
    source = ROOT/'third_party/documents/r2/TI_LM61460_SNVSBD5D.pdf'
    expected = '2c8a0bf340c70aa3ac29e586146804d7651822e14bee0897f6415ee9e56be84d'
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise ValueError('TI PDF changed: re-review vector coordinates before regeneration')
    document = pymupdf.open(source)
    scale = 72/25.4*25
    copper = drawing_loops(document[55], (0,.5,1))
    paste = drawing_loops(document[56], (1,0,0))
    assert len(copper) == 14 and len(paste) == 15
    mapping = [1,2,3,4,5,6,7,8,9,14,13,10,12,11]
    # Derive centers from dimensioned pad 13 and SW10; page origins differ.
    def normalized(polygons, index13, index10):
        p13, p10 = polygons[index13], polygons[index10]
        cx = (min(x for x,y in p13)+max(x for x,y in p13))/2+.625*scale
        cy = (min(y for x,y in p10)+max(y for x,y in p10))/2
        return [[((x-cx)/scale,(y-cy)/scale) for x,y in polygon] for polygon in polygons]
    copper = normalized(copper,10,11)
    paste = normalized(paste,10,11)
    pads = [pad(n,p,'"F.Cu" "F.Mask"') for n,p in zip(mapping,copper)]
    pads += [pad('',p,'"F.Paste"') for p in paste]
    name = 'TI_RJR0014A_LM61460'
    result = {name:footprint(name,'TI RJR0014A; 4223976-H 06-2026 pp55-57; no EP15; 0.1 mm stencil example', (2,1.75),(2.5,2.25),pads,(-2.65,-1.9))}
    # SLPS549B p9: top-view land pattern, rotated relative to p8 top-view outline.
    pads = [pad(n,rectangle(x,1.435,.5,.63),'"F.Cu" "F.Mask"') for n,x in zip([1,2,3,4],[-.975,-.325,.325,.975])]
    # Drain base + fingers exactly union to the manufacturer comb. All 5-8 are drain.
    pads.append(pad(5,rectangle(0,-.39,2.45,1.9),'"F.Cu" "F.Mask"'))
    pads += [pad(n,rectangle(x,-1.50,.5,.5),'"F.Cu" "F.Mask"') for n,x in zip([8,7,6,5],[-.975,-.325,.325,.975])]
    for x in [-.975,-.325,.325,.975]:
        for y in [-1.435,1.435]:
            pads.append(pad('',rectangle(x,y,.34,.45),'"F.Paste"'))
    for x in [-.635,.635]:
        pads.append(pad('',rectangle(x,-.2625,1.02,1.445),'"F.Paste"'))
    name = 'TI_Q3_CSD19537Q3'
    result[name] = footprint(name,'TI Q3 SON 3.3x3.3; SLPS549B pp8-9; source 1-3 gate 4 drain 5-8; common drain pad 5', (1.65,1.65),(1.95,2.0),pads,(-1.6,1.95))
    # Vishay 30131 p2 isometric land drawing: w spans both banks;
    # a=force length, b=bank width, c=force/sense gap, d=sense length.
    pads = []
    for x,force,sense in [(-2.465,1,2),(2.465,4,3)]:
        pads.append(pad(force,rectangle(x,.89,2.69,5.71),'"F.Cu" "F.Mask" "F.Paste"'))
        pads.append(pad(sense,rectangle(x,-3.3,2.69,.89),'"F.Cu" "F.Mask" "F.Paste"'))
    name = 'Vishay_WSL2726_Kelvin_1Fplus_2Splus_3Sminus_4Fminus'
    result[name] = footprint(name,'Vishay 30131 rev29-Jun-2026 p2; project pin numbering; narrow sense terminals at negative Y; no polarity marking implied',(3.45,3.3),(4.1,4.05),pads,(-4.25,-3.3))
    output.mkdir(parents=True,exist_ok=True)
    for name,content in result.items():
        (output/(name+'.kicad_mod')).write_text(content)
    print(f'Built {len(result)} footprints in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    build(parser.parse_args().output_dir)
