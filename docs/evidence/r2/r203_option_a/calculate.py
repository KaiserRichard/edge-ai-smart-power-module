#!/usr/bin/env python3
"""R203 option A: reproduce conditional screens without rewriting historical evidence."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
FREEZE = '898759e45578f3767721d19eb313312b7d7733a9'
SOURCE = 'docs/evidence/r2/gate4a/CALCULATIONS.json'


def band(bottom, fraction, bias=0):
    # Enumerated extrema: the same top resistor enters divider gain and bias.
    return [
        .99 * (1 + 100000 * (1-fraction) / (bottom * (1+fraction))) - bias*100000*(1-fraction),
        1.01 * (1 + 100000 * (1+fraction) / (bottom * (1-fraction))) + bias*100000*(1+fraction),
    ]


def calculate():
    source = subprocess.check_output(['git', 'show', FREEZE + ':' + SOURCE], cwd=ROOT)
    frozen = json.loads(source)
    path = frozen['selected_path']
    loop = sum(r['send_mohm'] + r['return_mohm'] for r in path['itemised_rows'])
    assert abs(loop - path['results']['0.02']['loop_mOhm']) < 1e-12
    assert abs(band(24400, .0025, 10e-9)[0] - path['source_min_assumed_V']) < 1e-12
    cold = band(24600, .001, 10e-9)
    hot = band(24600, .001 + 25e-6 * 60, 10e-9)
    paths = []
    for label, resistance, excursion in [
        ('Frozen path, static', loop, 0),
        ('Frozen path, 20 mV trough', loop, .020),
        ('100 mV total excursion sensitivity (includes ripple)', loop, .100),
        ('6 V gate-drive sensitivity, 20 mV trough', loop+6.8, .020),
    ]:
        pi = hot[0] - 5*resistance/1000 - excursion
        paths.append(dict(case=label, hot_loop_mohm=resistance,
                          negative_excursion_V=excursion, pi_min_CALCULATED_V=pi,
                          margin_mV=(pi-4.75)*1000, result='PASS' if pi >= 4.75 else 'FAIL'))
    detector = frozen['gate4a_fix']['detector']
    trip_min, trip_max = detector['conditional_trip_min_max_V']
    overdrive = detector['conditional_20mV_overdrive_raw_upper_V']
    return dict(
        classification='CALCULATED within inherited assumptions; not tested or guaranteed',
        source=dict(commit=FREEZE, path=SOURCE, sha256=hashlib.sha256(source).hexdigest(),
                    connector_commit=path['connector_commit']),
        requirements=dict(pi_min_V=4.75, load_A=5, pi_fault_strict_max_V=5.5),
        divider=dict(R202_ohm=100000, R203_ohm=24600, nominal_V=1+100000/24600,
                     previous_nominal_V=1+100000/24400,
                     initial_reference_resistor_band_V=band(24600, .001),
                     initial_with_ASSUMED_10nA_band_V=cold,
                     hot_with_ASSUMED_10nA_band_V=hot,
                     reference_fraction=.01, initial_resistor_fraction=.001,
                     tcr_ppm_per_K=25, ASSUMED_hot_divider_C=85,
                     ASSUMED_FB_current_A=10e-9, actual_regulation_band_V=None),
        path=dict(itemised_rows=path['itemised_rows'], loop_mohm=loop,
                  drop_5A_mV=5*loop, loss_5A_W=25*loop/1000,
                  cold_divider_pi_with20mV_V=cold[0]-5*loop/1000-.020,
                  max_total_negative_excursion_mV=(hot[0]-5*loop/1000-4.75)*1000,
                  previous_hot_pi_with20mV_V=path['results']['0.02']['Vfar_end_CALCULATED_V'],
                  cases=paths, actual_pi_min_V=None),
        ov=dict(nominal_trip_V=detector['new_nominal_zero_Ron_trip_V'],
                conditional_trip_band_V=[trip_min,trip_max],
                min_trip_above_initial_setpoint_max_mV=(trip_min-cold[1])*1000,
                min_trip_above_hot_setpoint_max_mV=(trip_min-hot[1])*1000,
                min_trip_above_hot_max_plus20mV_mV=(trip_min-hot[1]-.020)*1000,
                pi_fault_headroom_at_max_trip_mV=(5.5-trip_max)*1000,
                conditional_overdrive_upper_V=overdrive,
                margin_to5p38_overdrive_allocation_mV=(5.38-overdrive)*1000,
                pi_fault_headroom_after_overdrive_mV=(5.5-overdrive)*1000,
                pi_fault_headroom_after_overdrive_and20mV_local_allowance_mV=(5.5-overdrive-.020)*1000,
                inherited_107p620mV_release_plus10mV_reserve_sensitivity_mV=(trip_min-hot[1]-.107620-.010)*1000,
                actual_fault_peak_V=None),
        limitations=[
            'TI reference limit is FPWM-conditioned; U201 is auto-mode. Full operating regulation and maximum FB current remain OPEN.',
            '20 mV trough and hot contact/FET/copper values are qualification targets, not measurements. 100 mV is an inherited sensitivity, not a newly frozen requirement.',
            'Gate4A selected D with BSC034 pair 13.6 mOhm and J502 solution A. Earlier E/6 mOhm pair proposals and old 5.325 V detector are not current.',
            'OV threshold headroom excludes delay/energy/ESL/harness overshoot. The retained 5.713245 V receiving-bank sensitivity already fails 5.5 V; no fault-containment PASS is transferred.',
        ])


if __name__ == '__main__':
    result = calculate()
    (HERE/'CALCULATIONS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('path','limitations')}, indent=2))
    print(json.dumps(result['path']['cases'], indent=2))
