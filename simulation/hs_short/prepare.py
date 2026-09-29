#!/usr/bin/env python3
"""Generate open ngspice cases and collect external runs; stdlib only.

Generation does not execute ngspice or establish syntax/numerical correctness.
No manufacturer model is included. See README.md for the evidence boundary.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'docs/evidence/r2/protection_analysis_2026-09-29'
spec = importlib.util.spec_from_file_location('protection_model', ROOT / 'scripts/analyze_output_protection.py')
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

OPTIONS = {
    'A': 'A_lm74800_ov_only',
    'B2': 'B2_A_plus_1000uF_bulk',
    'I': 'I_470uF_bulk_plus_precision_fast_gate_off',
    'H': 'H_470uF_bulk_plus_precision_crowbar',
}
RESULT_FILES = {'baseline': 'baseline_model_results.json', 'reviewed': 'protection_model_results.json'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parameters(inputs, option, corner, maxstep=2e-9):
    p = lambda key: model.v(key, inputs)
    cin, craw, iload, cload, lossy = corner
    # Use the same explicit profile bound as Python, including reviewed RILIM tolerance.
    ilim = p('efuse_iol_max_A')
    return {
        'VSOURCE': p('vin_source_max_V'), 'REFUSE': p('efuse_ron_ohm'),
        'ILIMIT': ilim, 'CINPUT': cin, 'CRAW': craw, 'CLOAD': cload,
        'VINITIAL': p('vraw_static_V')[1], 'ILOAD': iload,
        'RLOSS': (p('buck_hs_rdson_ohm') + p('L_dcr_max_ohm')) if lossy else 0,
        'LNOM': p('L_nom_H'), 'ISAT': p('L_isat_A'), 'LSAT': p('L_sat_ratio'),
        'CBULK': option.get('bulk_F', 0), 'RBULK': p('bulk_esr_ohm'),
        'VTRIP': option['trip_V'], 'DELAY_US': option['delay_s'] * 1e6,
        'REVERSE_US': p('ideal_diode_off_s') * 1e6,
        'RPATH': 2 * p('fet_rds_hot_ohm') + p('shunt_ohm'),
        'DISCONNECT': int(option['action'] == 'disconnect'),
        'RCROWBAR': p('crowbar_ohm'), 'LCROWBAR': p('crowbar_loop_H'),
        'LOAD_FLOOR': p('load_rolloff_voltage_V'),
        'MAXSTEP': maxstep, 'TSTOP': p('fault_duration_s'),
    }


def render_case(case_id, inputs, option, corner, maxstep=2e-9):
    lines = [f'V1A high-side short {case_id} -- NOT RUN; screening only',
             '* Authored behavioral netlist; Sheet 03 OPEN; R2/R3 BLOCKED.',
             '* CALCULATED parameter expressions from labelled inputs below.',
             '* ASSUMED numerical MAXSTEP, TSTOP and ideal event controls.',
             '* ASSUMED option trip, delay, bulk and ideal disconnect/crowbar.',
             '* Initial conditions reproduce Python, not a settled physical operating point.']
    lines.append('* Input labels and exact sources: manifest.json profiles and dated INPUTS.md.')
    lines.append(f'* ASSUMED sweep corner (Cin,Craw,Iload,Cload,lossy)={corner!r}')
    lines.append(f'* ASSUMED architecture configuration={option!r}')
    lines.extend(f'.param {key}={value:.16g}' for key, value in parameters(inputs, option, corner, maxstep).items())
    lines.extend(['.include "model.inc"', '.end', ''])
    return '\n'.join(lines)


def generate(directory=HERE, evidence=EVIDENCE, maxstep=2e-9):
    directory.mkdir(parents=True, exist_ok=True)
    if directory.resolve() != HERE.resolve():
        shutil.copyfile(HERE / 'model.inc', directory / 'model.inc')
    manifest = {
        'classification': 'KNOWN: generated run matrix; CALCULATED Python peaks; SPICE NOT RUN',
        'status': 'NOT RUN', 'ngspice_version': None,
        'acceptance': 'ASSUMED: abs(SPICE - Python) / abs(Python) <= 0.03 at every corner',
        'acceptance_fraction': 0.03,
        'reason': 'ngspice unavailable; installation prohibited by continuation overrides',
        'core_sha256': sha256(directory / 'model.inc'),
        'generator_sha256': sha256(Path(__file__)),
        'python_script_sha256': sha256(ROOT / 'scripts/analyze_output_protection.py'),
        'python_result_sha256': {},
        'profiles': {profile: {k: {'value': value, 'label': label, 'source': source}
                              for k, (value, label, source) in model.get_inputs(profile).items()}
                     for profile in ('baseline', 'reviewed')},
        'maxstep_s': {'value': maxstep, 'label': 'ASSUMED'},
        'cases': [],
    }
    for profile in ('baseline', 'reviewed'):
        inputs = model.get_inputs(profile)
        options = model.build_options(inputs)
        python_path = evidence / RESULT_FILES[profile]
        result = json.loads(python_path.read_text())
        manifest['python_result_sha256'][profile] = sha256(python_path)
        for short, name in OPTIONS.items():
            rows = result['high_side_short'][name]['runs']
            for number, corner in enumerate(model.corners(inputs)):
                case_id = f'{profile}_{short}_c{number:02d}'
                path = directory / f'{case_id}.cir'
                path.write_text(render_case(case_id, inputs, options[name], corner, maxstep))
                row = rows[number]
                expected_key = (round(corner[0]*1e6), round(corner[1]*1e6), corner[2], round(corner[3]*1e6), corner[4])
                actual_key = tuple(row[k] for k in ('cin_uF', 'craw_uF', 'i_load_A', 'c_load_uF', 'lossy'))
                if expected_key != actual_key:
                    raise ValueError(f'Python corner ordering mismatch: {case_id}')
                manifest['cases'].append({
                    'id': case_id, 'profile': profile, 'option': name,
                    'corner': dict(zip(('cin_F', 'craw_F', 'i_load_A', 'c_load_F', 'lossy'), corner)),
                    'netlist': path.name, 'sha256': sha256(path),
                    'python_peak_load_V': {'value': row['peak_load_unrounded_V'], 'label': 'CALCULATED'},
                    'spice_status': 'NOT RUN', 'spice_peak_load_V': None,
                    'relative_error': None, 'acceptance': 'NOT RUN',
                })
    (directory / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def parse_measurement(log, name):
    matches = re.findall(r'^\s*' + re.escape(name) + r'\s*=\s*([-+0-9.eE]+)', log, flags=re.M | re.I)
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one ngspice {name} measurement')
    value = float(matches[0])
    if not math.isfinite(value):
        raise ValueError(f'Invalid {name} measurement')
    if re.search(r'(?im)^.*(?:\berror\b|timestep too small|doanalyses:|unknown parameter|no such function).*$', log):
        raise ValueError('ngspice log contains analysis/parser failure')
    return value


def parse_peak(log):
    peak = parse_measurement(log, 'peak_load')
    if peak <= 0:
        raise ValueError('Invalid peak_load measurement')
    return peak


def check_states(log, disconnect):
    names = ('initial_action', 'initial_connected', 'final_action',
             'final_connected', 'final_reverse_latch')
    states = {name: parse_measurement(log, name) for name in names}
    close = lambda a, b: abs(a - b) < 1e-5
    if not close(states['initial_action'], 0) or not close(states['initial_connected'], 1):
        raise ValueError('False startup action/disconnect')
    for name in ('final_action', 'final_connected'):
        if not any(close(states[name], expected) for expected in (0, 1)):
            raise ValueError(f'Invalid final logic state: {name}')
    if (disconnect and states['final_action'] > 0.5) or states['final_reverse_latch'] > 1e-6:
        if not close(states['final_connected'], 0):
            raise ValueError('Final state fails isolation/latch consistency')
    return states


def comparison(peak, reference, limit=0.03):
    if not math.isfinite(peak) or peak <= 0:
        raise ValueError('Invalid SPICE peak')
    if not math.isfinite(reference) or reference <= 0:
        raise ValueError('Invalid Python reference peak')
    error = abs(peak - reference) / reference
    return error, 'PASS' if error <= limit else 'FAIL'


def run_external(directory, output, executable):
    """For an authorized ngspice-equipped environment only; never installs software."""
    binary = shutil.which(executable)
    if binary is None:
        raise SystemExit('ngspice executable unavailable; no runs attempted')
    output.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((directory / 'manifest.json').read_text())
    if sha256(directory / 'model.inc') != manifest['core_sha256']:
        raise ValueError('Core hash changed; regenerate the matrix first')
    for case in manifest['cases']:
        if sha256(directory / case['netlist']) != case['sha256']:
            raise ValueError(f'Netlist hash changed: {case["id"]}')
    version = subprocess.run([binary, '--version'], capture_output=True, text=True)
    (output / 'ngspice_version.txt').write_text(version.stdout + version.stderr)
    report = copy.deepcopy(manifest)
    report['status'] = 'RUN ATTEMPTED'
    report['reason'] = None
    report['ngspice_version'] = version.stdout + version.stderr
    report['classification'] = 'SIMULATED only for completed ngspice runs; comparison is numerical agreement, not qualification'
    for case in report['cases']:
        result = subprocess.run([binary, '-b', case['netlist']], cwd=directory,
                                capture_output=True, text=True)
        log = result.stdout + result.stderr
        (output / f'{case["id"]}.log').write_text(log)
        case['exit_code'] = result.returncode
        case['command'] = [binary, '-b', case['netlist']]
        case['spice_status'] = 'ERROR'
        case['acceptance'] = 'NOT RUN'
        try:
            if result.returncode:
                raise ValueError(f'ngspice exit {result.returncode}')
            peak = parse_peak(log)
            case['state_checks'] = check_states(log, case['option'] != OPTIONS['H'])
            error, status = comparison(peak, case['python_peak_load_V']['value'])
            case.update(spice_status='SIMULATED', spice_peak_load_V=peak,
                        relative_error=error, acceptance=status)
        except ValueError as exc:
            case['error'] = str(exc)
        # Preserve progress if the external batch is interrupted.
        (output / 'comparison_results.json').write_text(json.dumps(report, indent=2) + '\n')
    report['status'] = 'PASS' if all(c['acceptance'] == 'PASS' for c in report['cases']) else 'FAIL'
    (output / 'comparison_results.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=HERE)
    parser.add_argument('--maxstep', type=float, default=2e-9)
    parser.add_argument('--run', action='store_true', help='explicitly execute externally available ngspice')
    parser.add_argument('--executable', default='ngspice')
    parser.add_argument('--output', type=Path, help='new external-run evidence directory; required with --run')
    args = parser.parse_args()
    if not 0 < args.maxstep <= 2e-9:
        parser.error('--maxstep must be positive and no greater than 2e-9 s')
    if args.run:
        if args.output is None:
            parser.error('--run requires --output')
        result = run_external(args.directory.resolve(), args.output.resolve(), args.executable)
    else:
        result = generate(args.directory.resolve(), maxstep=args.maxstep)
    print(f'{len(result["cases"])} cases: {result["status"]}')
    return 1 if result['status'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
