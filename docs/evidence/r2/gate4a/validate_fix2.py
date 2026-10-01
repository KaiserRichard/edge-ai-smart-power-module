"""Verify the resumed documentary package. No electrical or CAD checks are implied."""
import argparse
import hashlib
import io
import json
import subprocess
import unittest
from pathlib import Path

import calculate_gate4a
import render_freeze_register

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_object(commit, path):
    return subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=ROOT)


def validate():
    historical = json.loads((HERE / 'history/47c7c07/VALIDATION.json').read_text())
    assert (HERE / 'history/47c7c07/VALIDATION.json').read_bytes() == git_object(
        '47c7c07', 'docs/evidence/r2/gate4a/VALIDATION.json')
    for name in historical['historical_archive_files_preserved']:
        assert (HERE / 'history/931e369' / name).read_bytes() == git_object(
            '931e369', 'docs/evidence/r2/gate4a/' + name), name
    for record in historical['pinned_inputs_verified']:
        assert sha(git_object(record['commit'], record['path'])) == record['sha256'], record
    inputs = json.loads((HERE / 'FIX2_INPUTS.json').read_text())
    for record in inputs['connector_files']:
        raw = (ROOT / record['path']).read_bytes()
        assert sha(raw) == record['sha256'], record
        assert raw == git_object(inputs['connector_commit'], record['path']), record
    upstream = inputs['upstream_source_handoff_check']
    assert sha(git_object(upstream['commit'], upstream['path'])) == upstream['sha256']
    bom = inputs['optional_sheet03_qualification']
    for record in bom['imports']:
        raw = (ROOT / record['path']).read_bytes()
        assert sha(raw) == record['sha256'], record
        assert raw == git_object(bom['commit'], record['source_path']), record
    external_checked = []
    for record in inputs['briefs'] + [inputs['independent_check']]:
        path = Path(record['path'])
        if path.exists():
            assert sha(path.read_bytes()) == record['sha256'], record
            external_checked.append(record['path'])
    assert sha(Path(inputs['review']).read_bytes()) == inputs['review_sha256']
    external_checked.append(inputs['review'])

    rows = json.loads((HERE / 'FREEZE_MANIFEST.json').read_text())['changes']
    refs = [ref for row in rows for ref in row['refdes']]
    assert len(refs) == len(set(refs)), 'Reserved refs collide across register rows'
    for name, expected in render_freeze_register.render().items():
        assert (HERE / name).read_text() == expected, name
    data, _ = calculate_gate4a.calculate()
    assert json.loads((HERE / 'CALCULATIONS.json').read_text()) == data
    assert (HERE / 'CALCULATIONS.md').read_text() == calculate_gate4a.render_md(data)
    for group, keys in {
        'pg_input_bias': ('actual_off_voltage_V', 'actual_loss_to_safe_off_s'),
        'fixture_discharge': ('actual_connected_decay_s', 'actual_all_stores_discharged'),
        'power_device_screen': ('actual_hot_SOA_margin', 'actual_branch_current_bound_A'),
    }.items():
        assert all(data['gate4a_fix2'][group][key] is None for key in keys), group

    cache_checked, cache_missing = [], []
    for record in json.loads((ROOT / 'third_party/gate4a_downloads.json').read_text()):
        if not record.get('path'):
            continue  # Historical web-only sources have no promised cache/hash.
        file = ROOT / record['path']
        if file.exists():
            assert sha(file.read_bytes()) == record['sha256'], file
            cache_checked.append(record['path'])
        else:
            cache_missing.append(record['path'])
    round2_sources = json.loads((ROOT / 'third_party/gate4a_fix2/SOURCES.json').read_text())
    for record in round2_sources['sources']:
        if record['cache_path']:
            assert sha((ROOT / record['cache_path']).read_bytes()) == record['sha256'], record

    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=2).run(
        unittest.defaultTestLoader.discover(str(HERE), pattern='test_gate4a_calculations.py'))
    assert result.wasSuccessful(), (result.failures, result.errors)
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
    assert not any(name.endswith(('.kicad_sch', '.kicad_pcb', '.kicad_pro')) for name in changed)

    artifacts = {f.name: sha(f.read_bytes()) for f in sorted(HERE.iterdir())
                 if f.is_file() and f.name != 'VALIDATION.json'}
    report = dict(
        classification='Numerical/documentary verification only; no electrical validation',
        date='2026-10-01', resume_base_commit=inputs['resume_commit'],
        validation_command='python3 -B docs/evidence/r2/gate4a/validate_fix2.py --write',
        unit_tests_pass=result.testsRun,
        baseline_test_result='Atcffb770:14/14 pass; earlier74d5b10 RUN register failure is historical',
        register_rows=len(rows), register_unique_reserved_refs=len(refs),
        checks=['Reproduced N1 skew counterexample and mandatory unknown-skew handling',
                'Independent protected/raw resistor-energy integrals and connected-store sum',
                'RUN leakage KCL, preserved failed old-divider screen and null actual stability',
                'All prior numerical, topology and unknown-bound checks',
                'Exact generated CSV/Markdown/JSON; no cross-row refdes collisions',
                'Pinned inputs/imports/archive bytes and available manufacturer-cache hashes',
                'New Sheet03 qualification/source snapshots match BOM commit023e107',
                'PG input-bias, passive discharge and power-device screens retain null actual bounds',
                'Git diff whitespace; no native CAD changes'],
        pinned_inputs_verified=historical['pinned_inputs_verified'],
        connector_files_verified=inputs['connector_files'],
        source_handoff_verified=upstream,
        optional_BOM_handoff=bom,
        external_inputs_hash_checked=external_checked,
        historical_archive_files_preserved=historical['historical_archive_files_preserved'],
        round1_validation_archive='history/47c7c07/VALIDATION.json',
        manufacturer_cache_hashes_verified=cache_checked,
        manufacturer_caches_unavailable=cache_missing,
        round2_web_only_sources=[s['id'] for s in round2_sources['sources'] if not s['cache_path']],
        owner_PDF='One page exported and visually reviewed; current owner section, no clipping',
        plot_visual_review='Q316 original datasheet p5 SOA/thermal page visually reviewed; no new physical/CAD plots; historical ideal-model CSV/SVG unchanged',
        native_CAD_changes=False, ERC_DRC_run=False, physical_tests_run=False,
        original_BLOCKING_findings_closed=4, original_BLOCKING_findings_total=12,
        actual_electrical_safety_verdict='BLOCKED',
        git=dict(pull='Not attempted; local remote-tracking refs pinned',
                 local_item_checkpoints='F2-09/F2-10/F2-11/F2-12 staging FAILED: index.lock Operation not permitted; explicit brief fallback',
                 push='Not attempted; conductor publishes',
                 changes='This continuation uncommitted; supplied partial commits retained'),
        artifact_sha256=artifacts,
        round2_source_register_sha256=sha((ROOT / 'third_party/gate4a_fix2/SOURCES.json').read_bytes()),
        manager_report_sha256=sha((ROOT / 'docs/FINAL_MANAGER_REPORT.md').read_bytes()))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = validate()
    if args.write:
        (HERE / 'VALIDATION.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: result[k] for k in ('unit_tests_pass', 'register_rows',
                                           'register_unique_reserved_refs',
                                           'manufacturer_caches_unavailable',
                                           'actual_electrical_safety_verdict')}, indent=2))
