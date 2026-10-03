#!/usr/bin/env python3
"""Check KiCad's resolved PDF classes against project rules and raw XML.

Requires PyMuPDF. Keeps the raw KiCad XML unchanged even where 9.0.6 emits
Default for child-sheet nets. Checks all named nets, not only sample labels.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT/'docs/evidence/r2/gate4b'


def main():
    project_path = ROOT/'hardware/kicad/V1A.kicad_pro'
    project = json.loads(project_path.read_text())
    expected = {p['pattern']: p['netclass'] for p in project['net_settings']['netclass_patterns']}
    xml = {n.get('name'): n.get('class') for n in ET.parse(EV/'captured.xml').findall('./nets/net')
           if not n.get('name').startswith('unconnected-')}
    pdf_path = EV/'V1A_GATE4B_REVIEW.pdf'
    pdf = pymupdf.open(pdf_path)
    resolved = {}
    for i in range(1, pdf.xref_length()):
        obj = pdf.xref_object(i)
        n = re.search(r'Net = ([^"\n]+)', obj)
        c = re.search(r'Resolved netclass = ([^"\n]+)', obj)
        if n and c:
            resolved.setdefault(n[1], set()).add(c[1])
    assert set(resolved) == set(expected) == set(xml), 'Netclass review must cover every named net'
    assert all(resolved[n] == {c} for n,c in expected.items()), 'Resolved PDF class differs from project'
    with (EV/'NET_CLASSES.csv').open('w') as out:
        w = csv.writer(out)
        w.writerow(['net', 'project_class', 'kicad_pdf_resolved_class', 'raw_kicad_xml_class'])
        for n,c in sorted(expected.items()):
            w.writerow([n,c,next(iter(resolved[n])),xml[n]])
    result = dict(status='PASS: all named nets resolve to assigned classes in native KiCad PDF',
                  named_nets=len(expected), counts=dict(Counter(expected.values())),
                  raw_xml_class_mismatches=sum(xml[n] != c for n,c in expected.items()),
                  limitation='KiCad 9.0.6 XML emits Default for local child-sheet nets; raw export retained. Recheck PCB import in authorized R3.',
                  project_sha256=hashlib.sha256(project_path.read_bytes()).hexdigest(),
                  pdf_sha256=hashlib.sha256(pdf_path.read_bytes()).hexdigest())
    (EV/'NET_CLASSES.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
