#!/usr/bin/env python3
"""Export and mark the complete hierarchy without modifying schematic sheets.

Requires KiCad9 CLI and PyMuPDF. Adds a new margin above each original vector
page; no schematic content is covered. Writes review-only PDF and manifest.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
MARK = 'PRELIMINARY — R2 BLOCKED — NOT FOR FABRICATION'
NAMES = ['V1A', '01_INPUT_PROTECTION', '02_BUCK_5V',
         '03_OUTPUT_PROTECTION', '04_POWER_MONITOR', '05_IO_TEST']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', required=True)
    parser.add_argument('--review-dir', type=Path, required=True)
    args = parser.parse_args()
    out = ROOT/'docs/evidence/r2/sheet03'
    destination = out/'V1A_GATE2_PRELIMINARY.pdf'
    with tempfile.TemporaryDirectory() as scratch:
        raw = Path(scratch)/'V1A_unmarked.pdf'
        run = subprocess.run([args.kicad_cli, 'sch', 'export', 'pdf', '--output', str(raw),
                              str(ROOT/'hardware/kicad/V1A.kicad_sch')], capture_output=True, text=True)
        if run.returncode:
            raise RuntimeError(run.stdout+run.stderr)
        source = pymupdf.open(raw)
        if len(source) != len(NAMES):
            raise ValueError(f'Expected root plus five functional sheets, got {len(source)}')
        document = pymupdf.open()
        for i, original in enumerate(source):
            expected = NAMES[i]+'.kicad_sch'
            if expected not in ''.join(original.get_text().split()):
                raise ValueError(f'Wrong sheet at page{i+1}: expected {expected}')
            page = document.new_page(width=original.rect.width, height=original.rect.height+44)
            page.show_pdf_page(pymupdf.Rect(0,44,page.rect.width,page.rect.height), source, i)
            spare, _ = page.insert_htmlbox(pymupdf.Rect(20,5,page.rect.width-20,40),
                '<div style="font-family:sans-serif;font-size:16pt;color:#a00000;'+
                'font-weight:bold;text-align:center">'+MARK+'</div>')
            if spare < 0:
                raise ValueError('Mark does not fit')
        document.set_metadata({'title':'V1A Gate2 preliminary schematic review',
                               'subject':MARK, 'creator':'KiCad9 and project review exporter'})
        document.save(destination, garbage=4, deflate=True)
    verified = pymupdf.open(destination)
    pages=[]
    for i, page in enumerate(verified):
        text = page.get_text()
        if MARK not in text or NAMES[i]+'.kicad_sch' not in ''.join(text.split()):
            raise ValueError(f'Export verification failed on page{i+1}')
        pages.append({'page':i+1,'sheet':NAMES[i],'mark_verified':True,
                      'width_pt':page.rect.width,'height_pt':page.rect.height})
    args.review_dir.mkdir(parents=True,exist_ok=True)
    copy = args.review_dir/destination.name
    shutil.copyfile(destination,copy)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    assert hashlib.sha256(copy.read_bytes()).hexdigest() == digest
    manifest={'status':'PASS','classification':'Export/page/mark verification only; R2/R3 BLOCKED',
              'page_count':len(verified),'pages':pages,'pdf':str(destination.relative_to(ROOT)),
              'review_copy':str(copy.resolve()),'sha256':digest,'copies_identical':True,
              'method':'Original vector pages retained unchanged below new44pt marking margin; no schematic edit',
              'visual_review':'See GATE2_VALIDATION.md; automatic marking checks do not imply visual review'}
    (out/'PDF_VALIDATION.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__ == '__main__':
    main()
