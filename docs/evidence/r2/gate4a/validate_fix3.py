"""Reproducible documentary/numerical audit; never electrical qualification."""
import argparse
import hashlib
import io
import json
import subprocess
import unittest
from pathlib import Path

import calculate_gate4a_fix3
import render_fix3_fixture
import validate_fix2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate():
    # Retain the earlier import/archive/calculation checks without writing its
    # obsolete round-2 status, Git text or visual-review assertions.
    previous = validate_fix2.validate()
    inputs = json.loads((HERE / 'FIX3_INPUTS.json').read_text())
    for r in inputs['briefs']:
        assert sha(Path(r['path']).read_bytes()) == r['sha256'], r
    for commit in inputs['partial_commits_inspected']:
        subprocess.run(['git', 'merge-base', '--is-ancestor', commit, 'HEAD'],
                       cwd=ROOT, check=True)
    archive = HERE / 'history/9471e14'
    archived = []
    for p in sorted(archive.iterdir()):
        if p.name == 'README.md':
            continue
        assert p.read_bytes() == validate_fix2.git_object(
            '9471e14', 'docs/evidence/r2/gate4a/' + p.name), p
        archived.append(p.name)
    for name, expected in render_fix3_fixture.render().items():
        assert (HERE/name).read_text() == expected, name
    data = calculate_gate4a_fix3.calculate()
    assert json.loads((HERE/'FIX3_CALCULATIONS.json').read_text()) == data
    assert data['source']['internal_bridge_fault_coverage'] is None
    assert data['source']['actual_complete_interval_s'] == [None, None]
    assert data['interlock']['actual_loss_interval_s'] == [None, None]
    assert data['fixture']['actual_abort_s'] is None
    assert data['fixture']['actual_hot_SOA_margin'] is None
    source_file = ROOT/'third_party/gate4a_fix3/SOURCES.json'
    sources = json.loads(source_file.read_text())['sources']
    caches = []
    for r in sources:
        for field in ('url', 'revision', 'relevant_source', 'license', 'use',
                      'modifications_to_authored_design', 'required_attribution'):
            assert r[field], (r['id'], field)
        if r['cache_path']:
            assert sha((ROOT/r['cache_path']).read_bytes()) == r['sha256'], r
            caches.append(r['cache_path'])
    stream = io.StringIO()
    tests = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.defaultTestLoader.discover(str(HERE), pattern='test*.py'))
    assert tests.wasSuccessful(), stream.getvalue()
    changed = subprocess.check_output(['git','diff','--name-only',inputs['resume_commit']],
                                      cwd=ROOT,text=True).splitlines()
    untracked = subprocess.check_output(['git','ls-files','--others','--exclude-standard'],
                                        cwd=ROOT,text=True).splitlines()
    assert not any(p.endswith(('.kicad_sch','.kicad_pcb','.kicad_pro')) for p in changed+untracked)
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    parts,pins = render_fix3_fixture.build()
    return dict(
        classification='Documentary/numerical/connectivity verification only; no electrical validation',
        date='2026-10-01',resume_base_commit=inputs['resume_commit'],
        validation_command='python3 -B docs/evidence/r2/gate4a/validate_fix3.py --write',
        baseline_test_result='At692d30f:19 tests passed; final fixture regressions bring total to22',
        unit_tests_pass=tests.testsRun,register_rows=previous['register_rows'],
        register_unique_reserved_refs=previous['register_unique_reserved_refs'],
        external_fixture_BOM_entries=len(parts),external_fixture_pin_records=len(pins),
        checks=['Round-1/2 archive bytes, pinned Git imports and available manufacturer caches',
                'Round-2 freeze archive at9471e14 unchanged',
                'Current brief hashes and all three supplied partial commits preserved',
                'Generated freeze and fixture registers and calculation artifacts match',
                'Source periodic-pulse counterexample retained; actual timing/coverage remain null',
                'Resistor package/tolerance corrections and fixture force/signal connectivity',
                'Full winding-TCR current screen and independent emergency timing envelope',
                'No fixture signal drives board FAULT/SRC_TRIP/SHDN; no FAR_GND bypass',
                'Whitespace and no native CAD changes'],
        pinned_inputs_verified=previous['pinned_inputs_verified'],
        connector_files_verified=previous['connector_files_verified'],
        source_handoff_verified=previous['source_handoff_verified'],
        optional_BOM_handoff=previous['optional_BOM_handoff'],
        historical_archive_files_preserved=previous['historical_archive_files_preserved'],
        round2_archive_files_preserved=archived,
        manufacturer_caches_unavailable=previous['manufacturer_caches_unavailable'],
        round3_manufacturer_caches_verified=caches,
        round3_web_only_or_inherited_sources=[r['id'] for r in sources if not r['cache_path']],
        owner_PDF='One page regenerated; visually inspected, readable with no clipping',
        plot_visual_review='Vishay30201 p4 mounted derating visually inspected; BSC local download failed, no new visual SOA approval',
        native_CAD_changes=False,ERC_DRC_run=False,physical_tests_run=False,
        original_BLOCKING_findings_closed=4,original_BLOCKING_findings_total=12,
        actual_electrical_safety_verdict='BLOCKED',
        integrated_capture_blockers=['Autonomous source coverage for admitted pulsed/internal bridge faults',
                                     'Interlock partial-supply default-off, PG recovery/clear width and direct SER_DRV loss'],
        external_fixture_disposition='Construction candidate documented; hot SOA/reverse current/control-loss/parasitics NOT QUALIFIED; pre-energization gate only',
        git=dict(pull='Not attempted; existing pinned remote-tracking refs used',
                 local_item_checkpoints='Items1/2/3 each failed creating index.lock: Operation not permitted; explicit brief fallback',
                 push='Not attempted; conductor publishes',
                 changes='Uncommitted; supplied partial commits preserved; no permission bypass'),
        artifact_sha256={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir())
                         if p.is_file() and p.name!='VALIDATION.json'},
        round3_source_register_sha256=sha(source_file.read_bytes()),
        manager_report_sha256=sha((ROOT/'docs/FINAL_MANAGER_REPORT.md').read_bytes()))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=validate()
    if args.write:
        (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('unit_tests_pass','register_rows',
        'external_fixture_BOM_entries','external_fixture_pin_records',
        'integrated_capture_blockers','actual_electrical_safety_verdict')},indent=2))
