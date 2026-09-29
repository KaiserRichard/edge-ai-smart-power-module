#!/usr/bin/env python3
"""Read-only portable repository checks; never substitutes for electrical review."""
import argparse
import hashlib
import json
from pathlib import Path
import re
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
