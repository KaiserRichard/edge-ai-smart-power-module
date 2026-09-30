#!/usr/bin/env python3
"""Prove footprint assignment preserves the entire exported electrical design.

Only instance Footprint, MPN and Value values may differ. Export metadata/order
normalization is inherited from the independently tested Gate2b canonicalizer.
Source checking permits only those property string values: positions, wires,
UUIDs, flags, library definitions, ERC settings and all graphics remain exact.
"""
import argparse
import copy
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from build_sheet03_preliminary import children
from check_schematic_readability import canonical_netlist

ROOT = Path(__file__).resolve().parents[1]
BASE = '1f4c2f821793506871b9abe6227b1deba419d27e'
EVIDENCE = ROOT / 'docs/evidence/r2/footprints_complete'
EXCLUSIONS = {'F101', 'D101', 'L201'}
ALLOWED = {'Footprint', 'MPN', 'Value'}


def strip_component_fields(canonical):
    result = copy.deepcopy(canonical)
    for comp in result['components']:
        kept = []
        for child in comp['children']:
            if child['tag'] in ('footprint', 'value'):
                continue
            if child['tag'] == 'property' and child['attributes'].get('name') == 'MPN':
                continue
            if child['tag'] == 'fields':
                child['children'] = [f for f in child['children']
                                     if f['attributes'].get('name') not in ALLOWED]
            kept.append(child)
        comp['children'] = kept
    return result


def field_values(path):
    result = {}
    for c in ET.parse(path).findall('./components/comp'):
        fields = {'Footprint': c.findtext('footprint', ''), 'Value': c.findtext('value', ''),
                  'MPN': next((p.get('value', '') for p in c.findall('property')
                               if p.get('name') == 'MPN'), '')}
        # KiCad repeats the same properties in <fields>; catch disagreement.
        for f in c.findall('./fields/field'):
            if f.get('name') in fields and (f.text or '') != fields[f.get('name')]:
                raise ValueError(f'{c.get("ref")}: inconsistent duplicated {f.get("name")}')
        result[c.get('ref')] = fields
    return result


def compare_netlists(before, after):
    a, b = canonical_netlist(before), canonical_netlist(after)
    errors = []
    if strip_component_fields(a) != strip_component_fields(b):
        errors.append('Electrical data differs outside allowed Footprint/MPN/Value fields')
    av, bv = field_values(before), field_values(after)
    changes = []
    for ref in sorted(av.keys() | bv.keys()):
        if ref not in av or ref not in bv:
            errors.append(f'Component added/removed: {ref}')
            continue
        for field in sorted(ALLOWED):
            if av[ref][field] != bv[ref][field]:
                changes.append({'ref': ref, 'field': field, 'before': av[ref][field], 'after': bv[ref][field]})
                if ref in EXCLUSIONS:
                    errors.append(f'Excluded component changed: {ref}.{field}')
    return errors, changes, a, b


def normalized_source(text):
    for a, b, form in reversed(list(children(text))):
        if not form.startswith('(symbol'):
            continue
        for x, y, field in reversed(list(children(form))):
            match = re.match(r'\(property "(Footprint|MPN|Value)" ("(?:\\.|[^"\\])*")', field)
            if match:
                field = field[:match.start(2)] + '"<allowed-field-value>"' + field[match.end(2):]
                form = form[:x] + field + form[y:]
        text = text[:a] + form + text[b:]
    return text


def check_sources(root=ROOT):
    errors, evidence = [], []
    for path in sorted((root / 'hardware/kicad').glob('*.kicad_sch')):
        rel = path.relative_to(root).as_posix()
        before = subprocess.check_output(['git', 'show', f'{BASE}:{rel}'], cwd=root, text=True)
        after = path.read_text()
        same = normalized_source(before) == normalized_source(after)
        if not same:
            errors.append(f'Non-field schematic source change: {rel}')
        evidence.append({'file': rel, 'non_field_bytes_identical': same})
    for rel in ['hardware/kicad/V1A.kicad_pro', 'hardware/kicad/V1A.kicad_sym',
                'hardware/kicad/fp-lib-table', 'hardware/kicad/sym-lib-table']:
        before = subprocess.check_output(['git', 'show', f'{BASE}:{rel}'], cwd=root)
        if before != (root / rel).read_bytes():
            errors.append(f'Frozen project/library settings changed: {rel}')
    return errors, evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, default=EVIDENCE / 'baseline_1f4c2f8.xml')
    parser.add_argument('--netlist', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    errors, changes, a, b = compare_netlists(args.baseline, args.netlist)
    source_errors, sources = check_sources()
    errors.extend(source_errors)
    report = {'status': 'FAIL' if errors else 'PASS', 'baseline_commit': BASE,
              'allowed_fields': sorted(ALLOWED), 'changes': changes,
              'non_field_source_checks': sources, 'project_erc_settings_unchanged': not source_errors,
              'baseline_xml_sha256': hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
              'current_xml_sha256': hashlib.sha256(args.netlist.read_bytes()).hexdigest(), 'errors': errors}
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, value in [('baseline.canonical.json', a), ('completed.canonical.json', b), ('NETLIST_FIELD_DIFF.json', report)]:
            (args.output_dir / name).write_text(json.dumps(value, indent=2) + '\n')
        diff = difflib.unified_diff(json.dumps(a, indent=2).splitlines(True), json.dumps(b, indent=2).splitlines(True),
                                    fromfile='1f4c2f8.canonical', tofile='footprints-complete.canonical')
        (args.output_dir / 'canonical_netlist.diff').write_text(''.join(diff))
    print(json.dumps(report, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
