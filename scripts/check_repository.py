#!/usr/bin/env python3
"""Read-only portable repository checks; never substitutes for electrical review."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

from check_r0_r1_docs import heading_slug


def check(root):
    errors = []
    archived_links = []
    evidence = root / 'docs/evidence/repository_cleanup_2026-09-26'
    archive = json.loads((evidence / 'archive_manifest.json').read_text())
    integrity = json.loads((evidence / 'source_integrity.json').read_text())
    # Gate2 is an explicitly authorized schematic change, with its historical
    # baseline and exact ancillary diffs independently reviewed and retained.
    gate2 = root / 'docs/evidence/r2/sheet03/GATE2_SCOPE.json'
    if gate2.is_file():
        reviewed = json.loads(gate2.read_text())
        permitted = set(reviewed['allowed_ancillary_changes']) | {
            'hardware/kicad/03_OUTPUT_PROTECTION.kicad_sch',
            'hardware/kicad/V1A.kicad_sym'}
        for name, old_hash in integrity['files'].items():
            if name not in permitted and reviewed['files'].get(name) != old_hash:
                errors.append(f'Unapproved change to historical preservation record: {name}')
        integrity = reviewed
    # Gate2b permits presentation changes only. Chain the historical hashes;
    # retain exact file-set checks and require an independently exported,
    # electrically identical netlist before accepting the new source hashes.
    gate2b = root / 'docs/evidence/r2/sheet03/readability/GATE2B_SCOPE.json'
    if gate2b.is_file():
        from check_schematic_readability import canonical_netlist
        reviewed = json.loads(gate2b.read_text())
        permitted = {f'hardware/kicad/{name}.kicad_sch' for name in (
            'V1A', '01_INPUT_PROTECTION', '02_BUCK_5V',
            '03_OUTPUT_PROTECTION', '04_POWER_MONITOR', '05_IO_TEST')}
        permitted.add('hardware/kicad/V1A.kicad_sym')
        if reviewed['baseline_files'] != integrity['files']:
            errors.append('Gate2b does not preserve the historical Gate2 baseline')
        if set(reviewed['files']) != set(integrity['files']):
            errors.append('Gate2b changed the hardware file set')
        for name, old_hash in integrity['files'].items():
            if name not in permitted and reviewed['files'].get(name) != old_hash:
                errors.append(f'Non-presentation hardware change in Gate2b: {name}')
        evidence_dir = gate2b.parent
        identity = json.loads((evidence_dir / 'NETLIST_IDENTITY.json').read_text())
        for filename, field in (('baseline.net.xml', 'baseline_xml_sha256'),
                                ('readable.net.xml', 'readable_xml_sha256')):
            if hashlib.sha256((evidence_dir / filename).read_bytes()).hexdigest() != identity[field]:
                errors.append(f'Gate2b exported evidence hash mismatch: {filename}')
        baseline = canonical_netlist(evidence_dir / 'baseline.net.xml')
        current = canonical_netlist(evidence_dir / 'readable.net.xml')
        if baseline != current or (evidence_dir / 'netlist.diff').read_bytes():
            errors.append('Gate2b electrical netlist differs from baseline')
        for filename, expected in (('baseline.canonical.json', baseline),
                                   ('readable.canonical.json', current)):
            if json.loads((evidence_dir / filename).read_text()) != expected:
                errors.append(f'Gate2b canonical proof differs from XML: {filename}')
        integrity = reviewed
    # Owner-authorized completion changes only instance Footprint/MPN/Value.
    # Chain the prior hash record; retain the original electrical and drawing
    # proofs and verify new evidence, instead of relaxing preservation globally.
    completion = root / 'docs/evidence/r2/footprints_complete/FOOTPRINT_SCOPE.json'
    gate4b = root / 'docs/evidence/r2/gate4b/GATE4B_SCOPE.json'
    if completion.is_file():
        from check_footprint_completion import compare_netlists, check_sources
        reviewed = json.loads(completion.read_text())
        if reviewed['baseline_files'] != integrity['files']:
            errors.append('Footprint completion does not chain the Gate2b preservation record')
        directory = completion.parent
        proof = json.loads((directory/'NETLIST_FIELD_DIFF.json').read_text())
        for filename, field in [('baseline_1f4c2f8.xml','baseline_xml_sha256'),
                                ('completed.xml','current_xml_sha256')]:
            if hashlib.sha256((directory/filename).read_bytes()).hexdigest() != proof[field]:
                errors.append(f'Footprint completion netlist hash mismatch: {filename}')
        comparison, changes, _, _ = compare_netlists(directory/'baseline_1f4c2f8.xml', directory/'completed.xml')
        errors.extend(comparison)
        if changes != proof['changes'] or proof['status'] != 'PASS':
            errors.append('Footprint field-change ledger does not match actual XML')
        if canonical_netlist(directory/'baseline_1f4c2f8.xml') != canonical_netlist(gate2b.parent/'readable.net.xml'):
            errors.append('Footprint baseline differs electrically from retained redraw export')
        # Later authorized electrical capture must not be tested as a
        # footprint-only edit. Check that historical proof at its pinned commit.
        historical_revision = (json.loads(gate4b.read_text())['baseline_commit']
                               if gate4b.is_file() else None)
        errors.extend(check_sources(root, source_revision=historical_revision)[0])
        added = set(reviewed['files']) - set(integrity['files'])
        if added != set(reviewed['added_footprints']):
            errors.append('Footprint completion hardware additions differ from the reviewed list')
        if any(not n.startswith('hardware/kicad/V1A_Qualified.pretty/') or not n.endswith('.kicad_mod') for n in added):
            errors.append('Footprint completion added hardware outside its footprint library')
        for name, old_hash in integrity['files'].items():
            if not name.endswith('.kicad_sch') and reviewed['files'].get(name) != old_hash:
                errors.append(f'Footprint completion modified frozen hardware: {name}')
        integrity = reviewed
    if gate4b.is_file():
        import xml.etree.ElementTree as ET
        from check_r2_schematic import load_specs, validate, validate_sheet03_packages, validate_footprint_assignments
        reviewed = json.loads(gate4b.read_text())
        if reviewed['baseline_files'] != integrity['files']:
            errors.append('Gate4b does not chain the PR15 preservation record')
        for name, old_hash in integrity['files'].items():
            historical = subprocess.check_output(['git', 'show', f'{reviewed["baseline_commit"]}:{name}'], cwd=root)
            if hashlib.sha256(historical).hexdigest() != old_hash:
                errors.append(f'Gate4b pinned baseline differs from retained PR15 evidence: {name}')
            if not name.endswith(('.kicad_sch', '.kicad_sym', '.kicad_pro')) and reviewed['files'].get(name) != old_hash:
                errors.append(f'Gate4b modified an existing footprint/library table: {name}')
        added = set(reviewed['files']) - set(integrity['files'])
        if added != set(reviewed['added_footprints']):
            errors.append('Gate4b additions differ from the reviewed footprint list')
        if any(not n.startswith('hardware/kicad/V1A_Qualified.pretty/') or not n.endswith('.kicad_mod') for n in added):
            errors.append('Gate4b added hardware outside its footprint library')
        project = json.loads((root/'hardware/kicad/V1A.kicad_pro').read_text())
        old_project = json.loads(subprocess.check_output(['git', 'show',
            f'{reviewed["baseline_commit"]}:hardware/kicad/V1A.kicad_pro'], cwd=root))
        project.pop('net_settings', None)
        old_project.pop('net_settings', None)
        if project != old_project:
            errors.append('Gate4b changed project settings beyond authorized net classes')
        for name, expected in reviewed['evidence_files'].items():
            path = root/name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f'Gate4b reviewed evidence differs or is missing: {name}')
        directory = gate4b.parent
        tree = ET.parse(directory/'captured.xml').getroot()
        specs = load_specs(directory)
        errors.extend(validate(tree, specs, 'gate4b'))
        errors.extend(validate_sheet03_packages(tree, specs, profile='gate4b'))
        errors.extend(validate_footprint_assignments(tree, exclusions=set()))
        integrity = reviewed
    for name, expected in integrity['files'].items():
        path = root / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f'Hardware differs from reviewed preservation record or is missing: {name}')
    authored = {p.relative_to(root).as_posix() for p in (root/'hardware/kicad').rglob('*')
                if p.is_file() and (p.suffix in ('.kicad_sch','.kicad_sym','.kicad_mod','.kicad_pro')
                                    or p.name in ('sym-lib-table','fp-lib-table'))}
    if authored != set(integrity['files']):
        errors.append(f'Unreviewed hardware file set: {sorted(authored ^ set(integrity["files"]))}')
    if list((root / 'hardware').rglob('*.kicad_pcb')):
        errors.append('R3 boundary violation: project PCB exists')

    paths = [root / n for n in ('README.md', 'AGENTS.md', 'CLAUDE.md')]
    for directory in ('docs', 'third_party', 'software', 'measurements', 'fabrication'):
        paths.extend((root / directory).rglob('*.md'))
    # Upstream extracts retain their own links; authored registry files are checked.
    paths = [p for p in paths if 'wbr_hat/raspberry_pi' not in p.as_posix()]
    for path in paths:
        prose = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\((<[^>]+>|[^)]+)\)', prose):
            target = match.group(1).strip().strip('<>')
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            destination = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not destination.exists():
                try:
                    name = destination.relative_to(root).as_posix()
                except ValueError:
                    name = ''
                if name in archive['archived_document_files'] and 'archived external evidence' in prose.lower():
                    archived_links.append(name)
                else:
                    errors.append(f'Broken link in {path.relative_to(root)}: {target}')
            elif parts.fragment and destination.suffix == '.md':
                headings = re.findall(r'^#{1,6}\s+(.+)$', destination.read_text(), re.M)
                if unquote(parts.fragment) not in {heading_slug(h) for h in headings}:
                    errors.append(f'Broken heading link in {path.relative_to(root)}: {target}')
    json_paths = list((root / 'docs').rglob('*.json'))
    json_paths.append(root / 'third_party/documents/ti_converters/download_manifest.json')
    for path in json_paths:
        try:
            json.loads(path.read_text())
        except (ValueError, OSError) as exc:
            errors.append(f'Invalid/missing JSON: {path.relative_to(root)}: {exc}')
    return {'status': 'PASS' if not errors else 'FAIL',
            'scope': 'Repository integrity only; R2/R3 BLOCKED',
            'hardware_files_verified': len(integrity['files']),
            'markdown_files_checked': len(paths), 'json_files_checked': len(json_paths),
            'archived_external_links': sorted(set(archived_links)), 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
