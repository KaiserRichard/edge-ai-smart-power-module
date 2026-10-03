#!/usr/bin/env python3
"""Reconcile the resumed capture to pinned inputs; never grants electrical release.

Reads Git objects, the KiCad XML and native files. --write records the audited
scope and assembly inventory; it does not edit CAD, run KiCad, commit or push.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from check_r2_schematic import (load_specs, validate, validate_sheet03_packages,
                                validate_footprint_assignments)

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / 'docs/evidence/r2/gate4b'
BASELINE = '51d1c2ff1f7eca4f20eef137c1595e4b9e052a75'
FREEZE = '898759e45578f3767721d19eb313312b7d7733a9'
J502 = '41cb9e889418d50d2f5f24467e66ac7f15a90476'
BOM = '6e5017c9bf61b59a65a6a45a9f8cec0686fcb3f6'
ADDITIONS = {
    'ADI_FE20_EP2.74x4.95', 'ForceLink_M4_P20', 'ForcePad_M4',
    'Schurter_UMT_H_15.4x5.35', 'SensePair_P2.54',
    'TI_RPW0010A_TPS25947', 'Wurth_74437636351002', 'Wurth_7447789004',
}
RETIRED = set('U304 U305 U307 U308 U309 U310 U311 U312 U313 U314 '
              'R314 R315 R318 R319 R320'.split()) | {f'C{i}' for i in range(310, 326)}
EXCEPTIONS = {
    'S03-04': ('OWNER OPTION A', 'Old logic absent; U610/U611/U612 and manual controls replace the unresolved interlock.'),
    'S03-05': ('FIX3 SUPERSEDED', 'Only R316/R317 retained from row; real PG uses U607/U651. AHCT chain is absent.'),
    'S03-06': ('FIX3 SUPERSEDED', 'Q304 retained; R647–R650 implement resistive SHDN permission/default and fault sink.'),
    'S03-12': ('FIX3 SUPERSEDED', 'U307/R314/R315 absent; U306 IN/EN on DRV_HOLD; C307/R323 on AUX_LIMITED.'),
    'S01-07': ('SENSING CAPTURED / OWNER OPTION A', 'Frozen R640/R644 SW/VIN front end with U640/U642/U647 captured for observation; J603/U644 remains manual source trigger. Autonomous qualifier/collapse memory absent; no 10 us/100 uC claim.'),
    'S06-01': ('OWNER OPTION A', 'SAFE5/real PG/manual reset and arm captured on Sheet03. Fast interlock/diagnostic reservation superseded by JP600/JP660 hooks.'),
    'SXX-01': ('RETAINED / RETIRED', 'Exact MPNs for retained passives; 19 capacitors/resistors belonging to retired logic absent.'),
    'S04-05': ('EXTERNAL HARNESS', 'Selected TE/Belden solution A documented on Sheet05; no fictitious PCB harness component.'),
    'SFX-01': ('EXTERNAL FIXTURE', 'Independent discharge adapters remain off-board and require qualification.'),
    'SFX-02': ('EXTERNAL FIXTURE', 'Only DUT PF1–PF5 captured; full fixture stays in its separate pinned BOM/netlist.'),
}
EXPECTED_MISSING = {
    'S01-07': set('FAULT_TRIGGER U641 U643 U645 U646 R643 C641 C643 C645 C646'.split()),
    'S03-04': set('U304 U309 U305 U310 U311 U312 U313 U314 U320 C371'.split()),
    'S03-05': set('U319 U324 C360 C361 R368 R369 U325 U326 C362 C363 R394 R395'.split()),
    'S03-06': set('Q305 R324 R325 Q306 R326 D305'.split()),
    'S03-12': set('U307 R314 R315'.split()),
    'SXX-01': {f'C{i}' for i in range(310, 326)} | {'R318', 'R319', 'R320'},
}


def git_bytes(revision, path):
    return subprocess.check_output(['git', 'show', f'{revision}:{path}'], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory(tree):
    pins = {}
    for net in tree.findall('./nets/net'):
        for node in net.findall('node'):
            pins.setdefault(node.get('ref'), {})[node.get('pin')] = net.get('name').rsplit('/', 1)[-1]
    return {c.get('ref'): {
        'value': c.findtext('value'), 'mpn': c.findtext('fields/field[@name="MPN"]'),
        'footprint': c.findtext('footprint'), 'pins': pins.get(c.get('ref'), {}),
        'sheet': c.find('sheetpath').get('names'),
    } for c in tree.findall('./components/comp')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    tree = ET.parse(EV/'captured.xml').getroot()
    specs = load_specs(EV)
    errors = validate(tree, specs, 'gate4b')
    errors += validate_sheet03_packages(tree, specs, profile='gate4b')
    errors += validate_footprint_assignments(tree, exclusions=set())
    current = inventory(tree)
    previous = inventory(ET.fromstring(git_bytes(BASELINE, 'docs/evidence/r2/footprints_complete/completed.xml')))
    removed = set(previous) - set(current)
    if removed != RETIRED:
        errors.append(f'Unexpected PR15 retirements: {sorted(removed ^ RETIRED)}')
    manifest_path = 'docs/evidence/r2/gate4a/FREEZE_MANIFEST.json'
    manifest = json.loads(git_bytes(FREEZE, manifest_path))
    rows = []
    for change in manifest['changes']:
        ident = change['id']
        present = set(change['refdes']) & set(current)
        missing = set(change['refdes']) - present
        if ident not in EXCEPTIONS and missing:
            errors.append(f'{ident}: missing required capture references {sorted(missing)}')
        if ident in EXPECTED_MISSING and missing != EXPECTED_MISSING[ident]:
            errors.append(f'{ident}: retirement list differs from reviewed disposition')
        status, note = EXCEPTIONS.get(ident, ('CAPTURED', 'Captured selection; application qualification remains OPEN.'))
        rows.append(dict(id=ident, disposition=status, present_refs=sorted(present),
                         absent_reserved_refs=sorted(missing), note=note))
    if len(rows) != 40 or len({r['id'] for r in rows}) != 40:
        errors.append('Expected all 40 pinned freeze rows exactly once')
    # Per-reference passives come directly from the freeze, not capture JSON.
    passive_path = 'docs/evidence/r2/gate4a/PASSIVE_COMPLETION.csv'
    for row in csv.DictReader(io.StringIO(git_bytes(FREEZE, passive_path).decode())):
        ref = row['refdes']
        if ref not in RETIRED and (ref not in current or current[ref]['mpn'] != row['new_mpn']):
            errors.append(f'{ref}: does not match pinned passive MPN {row["new_mpn"]}')
    old_scope = json.loads((ROOT/'docs/evidence/r2/footprints_complete/FOOTPRINT_SCOPE.json').read_text())
    files = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes())
             for p in (ROOT/'hardware/kicad').rglob('*') if p.is_file()
             and (p.suffix in ('.kicad_sch', '.kicad_sym', '.kicad_pro', '.kicad_mod')
                  or p.name in ('sym-lib-table', 'fp-lib-table'))}
    added = set(files) - set(old_scope['files'])
    expected_added = {f'hardware/kicad/V1A_Qualified.pretty/{n}.kicad_mod' for n in ADDITIONS}
    if added != expected_added or set(old_scope['files']) - set(files):
        errors.append('Hardware file set differs from the eight reviewed footprint additions')
    for name, digest in old_scope['files'].items():
        if sha(git_bytes(BASELINE, name)) != digest:
            errors.append(f'PR15 evidence baseline hash mismatch: {name}')
        if not name.endswith(('.kicad_sch', '.kicad_sym', '.kicad_pro')) and files.get(name) != digest:
            errors.append(f'Existing footprint or library table modified: {name}')
    project = json.loads((ROOT/'hardware/kicad/V1A.kicad_pro').read_text())
    old_project = json.loads(git_bytes(BASELINE, 'hardware/kicad/V1A.kicad_pro'))
    project.pop('net_settings'); old_project.pop('net_settings')
    if project != old_project:
        errors.append('Project settings changed outside net classes')
    if list((ROOT/'hardware').rglob('*.kicad_pcb')):
        errors.append('No PCB layout authorized')
    result = dict(status='FAIL' if errors else 'PASS', scope='Capture reconciliation only; R2 electrical release BLOCKED',
                  physical_references=len(current), added_references=len(set(current)-set(previous)),
                  retired_references=sorted(removed), freeze_rows=rows, errors=errors)
    if args.write and not errors:
        (EV/'FREEZE_RECONCILIATION.json').write_text(json.dumps(result, indent=2)+'\n')
        changes = {r: {'before': previous[r], 'after': current[r]} for r in sorted(set(previous)&set(current))
                   if previous[r] != current[r]}
        delta = dict(baseline_commit=BASELINE, changed=changes,
                     added={r: current[r] for r in sorted(set(current)-set(previous))},
                     retired={r: previous[r] for r in sorted(removed)})
        (EV/'CAPTURE_DELTA.json').write_text(json.dumps(delta, indent=2)+'\n')
        with (EV/'CAPTURED_BOM.csv').open('w') as out:
            writer = csv.writer(out)
            writer.writerow(['refdes', 'sheet', 'mpn_or_project_feature', 'value', 'footprint', 'kind', 'qualification'])
            for ref, c in sorted(current.items()):
                writer.writerow([ref, c['sheet'], c['mpn'], c['value'], c['footprint'], specs[ref]['kind'],
                                 'PRELIMINARY TEST BOARD; NOT FOR PROCUREMENT/FABRICATION'])
        inputs = []
        for revision, names in [
            (FREEZE, ['GATE4A_FREEZE.md','FREEZE_TABLE.md','FREEZE_BOM.csv','FIX_RESOLUTIONS.md',
                      'TEST_PLAN.md','CALCULATIONS.md','CALCULATIONS.json','FIX3_CALCULATIONS.json',
                      'FIX3_SOURCE_TRIGGER.md','FIX3_INTERLOCK.md','FIX3_FIXTURE.md',
                      'FREEZE_MANIFEST.json','PASSIVE_COMPLETION.csv']),
            (J502, ['J502_SELECTION.md']), (BOM, ['BOM_DRAFT.md','SHEET03_PART_QUALIFICATION.md'])]:
            for name in names:
                path = 'docs/evidence/r2/' + ('gate4a/' if revision == FREEZE else '') + name
                inputs.append(dict(commit=revision, path=path, sha256=sha(git_bytes(revision, path))))
        (EV/'INPUT_PROVENANCE.json').write_text(json.dumps(inputs, indent=2)+'\n')
        evidence = [p for p in EV.iterdir() if p.suffix in ('.json','.xml','.pdf','.csv','.md')
                    and p.name not in ('GATE4B_SCOPE.json','FINAL_VALIDATION.json','REPOSITORY_CHECK.json')]
        scope = dict(baseline_commit=BASELINE,
                     authorization='GATE4B.md plus GATE4B_RESUME.md; owner option A 2026-10-01; capture only',
                     baseline_files=old_scope['files'], files=files, added_footprints=sorted(added),
                     evidence_files={p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in sorted(evidence)})
        (EV/'GATE4B_SCOPE.json').write_text(json.dumps(scope, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'freeze_rows'}, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
