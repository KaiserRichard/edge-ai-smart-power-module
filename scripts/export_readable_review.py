#!/usr/bin/env python3
"""Export native A3 review pages and 96-dpi images for 100% inspection.

Requires KiCad 9 CLI and PyMuPDF. Unlike the historical exporter, no margin,
scale or postprocessing is added: warning marks are part of the source sheets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/r2/sheet03'
NAMES=['V1A','01_INPUT_PROTECTION','02_BUCK_5V','03_OUTPUT_PROTECTION','04_POWER_MONITOR','05_IO_TEST']
MARK='PRELIMINARY / R2 BLOCKED / NOT FOR FABRICATION'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli',required=True)
    args=parser.parse_args()
    pdf=OUT/'V1A_REVIEW_READABLE.pdf'
    run=subprocess.run([args.kicad_cli,'sch','export','pdf','--output',str(pdf),str(ROOT/'hardware/kicad/V1A.kicad_sch')],capture_output=True,text=True)
    if run.returncode:raise RuntimeError(run.stdout+run.stderr)
    document=pymupdf.open(pdf)
    assert len(document)==6
    pages=[]
    for i,(page,name) in enumerate(zip(document,NAMES)):
        paper='A3'
        expected=(420,297)
        dimensions=(page.rect.width*25.4/72,page.rect.height*25.4/72)
        assert all(abs(a-b)<0.1 for a,b in zip(dimensions,expected)),(name,dimensions)
        text=' '.join(page.get_text().split())
        assert MARK in text,(name,'missing warning')
        assert name+'.kicad_sch' in text.replace(' ',''),(name,'wrong page')
        image=OUT/'readability'/f'page_{i+1:02d}_{name}_100pct.png'
        pix=page.get_pixmap(matrix=pymupdf.Matrix(96/72,96/72),alpha=False)
        pix.save(image)
        pages.append({'page':i+1,'sheet':name,'paper':paper,'width_mm':round(dimensions[0],3),'height_mm':round(dimensions[1],3),
                      'warning_verified':True,'image':image.relative_to(ROOT).as_posix(),'image_pixels':[pix.width,pix.height],
                      'image_dpi':96,'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
    result={'status':'PASS','pdf':pdf.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'page_count':6,'pages':pages,'method':'Native KiCad vector export; exact landscape A3; no scaling or added margin.',
            'image_method':'96 pixels per physical inch: 100% CSS/display scaling reference. Readability also depends on display DPI and viewer settings.',
            'visual_review':'Human-agent inspection recorded separately in GATE2B_FIX_REVIEW.md; image generation alone is not visual review.'}
    (OUT/'readability/PDF_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
