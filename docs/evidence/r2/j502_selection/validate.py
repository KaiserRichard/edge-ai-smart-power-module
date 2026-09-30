#!/usr/bin/env python3
"""Audit J502 documentary evidence; PASS is not electrical qualification.

Uses only the standard library. Needs the pinned Git objects, external task
inputs and the two hashed review PDFs in the ignored third-party cache.
Run at any location; --output optionally records the results as JSON.
"""
import argparse
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def close(actual, expected):
    assert abs(D(str(actual)) - expected) < D('1e-10'), (actual, str(expected))


def audit():
    provenance = json.loads((HERE / 'INPUT_PROVENANCE.json').read_text())
    for entry in provenance['inputs']:
        data = (git('show', entry['commit'] + ':' + entry['path'])
                if 'commit' in entry else Path(entry['path']).read_bytes())
        assert len(data) == entry['bytes'], entry['path']
        assert digest(data) == entry['sha256'], entry['path']

    calc = json.loads((HERE / 'CALCULATIONS.json').read_text())
    # Separate derivation from the pinned divider stack, not calculate.py.
    top = D(100000) * D('.9975')
    bottom = D(24400) * D('1.0025')
    source = D('.99') * (1 + top / bottom) - D('1e-8') * top
    close(calc['source_min_screen_V'], source)
    path_input = next(e for e in provenance['inputs']
                      if e['path'].endswith('/PATH_CALCULATIONS.json'))
    inherited = json.loads(git('show', path_input['commit'] + ':' + path_input['path']))
    close(inherited['raw_static_hot_feedback_screen']['min_V'], source)
    assert inherited['raw_static_hot_feedback_screen']['actual_worst_case_min_V'] is None

    # Reconstruct conductances for individual branches before summing the loop.
    factor = D('1.10') * (1 + D('.00393') * 40)
    trunk_ohm = D(4) / D('304.8') * D('.075') * factor
    branch_ohms = [D('9.8') / D('304.8') * length * factor + D('.02048')
                   for length in (D('.015'), D('.035'))]
    pi_loop = 1 / sum(1 / branch_ohms[0] for _ in range(2))
    pi_loop += 1 / sum(1 / branch_ohms[1] for _ in range(8))
    fixed = (D('.001') + D('.006') + D('.002') * D('1.01') *
             (1 + D('.000025') * 75) + D('.002') + D('.001') + D('.0002'))
    report = (HERE.parent / 'J502_SELECTION.md').read_text()
    checked_cases = []
    for name, pole in [('A_TE_Phoenix', D('.00312')),
                       ('B_TE_MiniFitSr_gold', D('.004'))]:
        for architecture, added in [('D', D(0)), ('E', D('.010'))]:
            loop = fixed + 2 * trunk_ohm + pi_loop + 2 * pole + added
            row = calc['options'][name]['results'][architecture]
            close(row['loop_mohm'], loop * 1000)
            close(row['drop_mV'], 5 * loop * 1000)
            close(row['path_loss_W'], 25 * loop)
            for key, excursion in [('Pi_static_V', D(0)),
                                   ('Pi_20mV_trough_V', D('.020')),
                                   ('Pi_100mV_total_excursion_V', D('.100'))]:
                expected = source - 5 * loop - excursion
                close(row[key], expected)
                assert f'{expected:.6f}' in report, (name, architecture, key)
            old_pair = source - 5 * (loop + D('.0076')) - D('.020')
            close(row['Pi_20mV_with_old_13p6mohm_FET_pair_V'], old_pair)
            assert f'{old_pair:.6f}' in report
            assert f'{loop * 1000:.6f}' in report
            assert row['actual_qualified_hot_min_V'] is None
            if architecture == 'E':
                assert row['Pi_20mV_trough_V'] >= 4.75
                assert row['Pi_100mV_total_excursion_V'] < 4.75
                assert old_pair < D('4.75')
            checked_cases.append(name + '/' + architecture)

    expected_pins = {2: '5V', 4: '5V', **{p: 'GND' for p in (6, 9, 14, 20, 25, 30, 34, 39)}}
    assert calc['physical_Pi_pins'] == {str(p): net for p, net in expected_pins.items()}
    pin_rows = re.findall(r'^\| (\d+) \| ([AB]\d+) \| ([^|]+) \| ([\d.]+) A \|$', report, re.M)
    assert len(pin_rows) == 10
    assert {int(p) for p, *_ in pin_rows} == set(expected_pins)
    for pin, coordinate, destination, current in pin_rows:
        p = int(pin)
        assert coordinate == ('A' if p % 2 else 'B') + str((p + 1) // 2)
        assert ('GND' if p not in (2, 4) else 'LOAD_5V1') in destination
        assert D(current) == (D('.625') if p not in (2, 4) else D('2.5'))

    sources = json.loads((ROOT / 'third_party/j502_selection/SOURCES.json').read_text())['sources']
    assert len({s['id'] for s in sources}) == len(sources)
    cached_pdfs = []
    for source_entry in sources:
        for field in ('url', 'revision', 'reviewed_sections', 'owner', 'license',
                      'use', 'modifications', 'required_attribution'):
            assert source_entry.get(field), (source_entry['id'], field)
        assert urlparse(source_entry['url']).scheme == 'https'
        if source_entry.get('sha256'):
            path = ROOT / source_entry['local_review_file']
            assert digest(path.read_bytes()) == source_entry['sha256'], str(path)
            cached_pdfs.append(source_entry['id'])

    local_links = 0
    documents = [HERE.parent / 'J502_SELECTION.md', HERE / 'VALIDATION.md',
                 ROOT / 'third_party/j502_selection/README.md', ROOT / 'docs/FINAL_MANAGER_REPORT.md']
    for document in documents:
        content = document.read_text()
        if document.name == 'FINAL_MANAGER_REPORT.md':
            content = content.split('## J502 / Pi harness selection — 2026-09-30', 1)[1]
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
            if urlparse(target).scheme or target.startswith('#'):
                continue
            assert (document.parent / target.split('#')[0]).is_file(), (str(document), target)
            local_links += 1

    # A comparison of every tracked file also proves native CAD and other
    # upstream/reference material stayed unchanged from the requested base.
    changed = set(git('diff', '--name-only', provenance['base_commit'], '--').decode().splitlines())
    changed.update(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
    for path in changed:
        assert path in ('docs/FINAL_MANAGER_REPORT.md', 'docs/evidence/r2/J502_SELECTION.md') or path.startswith(
            ('docs/evidence/r2/j502_selection/', 'third_party/j502_selection/')), path
    subprocess.run(['git', '-C', str(ROOT), 'diff', '--check', provenance['base_commit']], check=True)
    return dict(status='PASS — documentary checks only; hot qualification remains OPEN',
                inputs_verified=len(provenance['inputs']), independent_decimal_cases=checked_cases,
                physical_Pi_positions_verified=10, source_records_checked=len(sources),
                cached_PDF_hashes_verified=cached_pdfs, local_links_verified=local_links,
                scope_base=provenance['base_commit'], changed_files=sorted(changed),
                native_CAD_changes=0, qualification_status='BLOCKED',
                pdf_visual_review='Manual evidence in VALIDATION.md, not performed by this script')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(audit(), indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(result)
    print(result, end='')
