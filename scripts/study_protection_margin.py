#!/usr/bin/env python3
"""Amended 5.5 V margin study; CALCULATED screens, no selected architecture."""
import argparse
import hashlib
import json
from pathlib import Path

import analyze_output_protection as model

OUT = model.EVIDENCE / 'margin_study_results.json'
TARGET_MV = 100.0  # ASSUMED evaluation objective, not an approved requirement.
NUISANCE_MV = 50.0  # ASSUMED acceptance allocation in the original brief.


def scenarios():
    """Every entry is an ASSUMED numerical experiment, not a part specification.

    Delay is total from the effective threshold to ideal isolation. The optional
    overdrive allowance raises that threshold exactly once, as in Task 4's budget.
    """
    rows = []

    def add(name, nominal=5.4, error=0.011, delay_us=0.4, bulk_uF=470,
            esr_mohm=20, overdrive_mV=0, initial_high=False, l_scale=1.0):
        rows.append(dict(id=name, nominal_V=nominal, static_error_fraction=error,
                         delay_s=delay_us*1e-6, bulk_F=bulk_uF*1e-6,
                         bulk_esr_ohm=esr_mohm*1e-3, sense_overdrive_V=overdrive_mV*1e-3,
                         reference_V=2.5, initial_high=initial_high, inductance_scale=l_scale))

    add('exact_window_2us', delay_us=2)
    add('exact_window_1us', delay_us=1)
    add('exact_window_0p4us')
    add('exact_window_0p2us', delay_us=0.2)
    add('lower_5p35', nominal=5.35)
    add('lower_5p325', nominal=5.325)
    add('lower_5p30', nominal=5.3)
    add('bulk_1000', bulk_uF=1000)
    add('bulk_2200', bulk_uF=2200)
    add('lower_and_bulk', nominal=5.3, bulk_uF=1000)
    add('lower_and_bulk_1us', nominal=5.3, bulk_uF=1000, delay_us=1)
    add('tighter_window', nominal=5.325, error=0.00671)
    add('tighter_with_overdrive', nominal=5.325, error=0.00671, overdrive_mV=10)
    add('combined_with_overdrive', nominal=5.3, error=0.00671, bulk_uF=1000, overdrive_mV=10)
    add('combined_low_esr', nominal=5.3, error=0.00671, bulk_uF=1000, overdrive_mV=10, esr_mohm=5)
    add('combined_100mohm', nominal=5.3, error=0.00671, bulk_uF=1000, overdrive_mV=10, esr_mohm=100)
    add('combined_initial_high_Llow', nominal=5.3, error=0.00671, bulk_uF=1000,
        overdrive_mV=10, initial_high=True, l_scale=0.8)
    add('combined_initial_high_Lhigh', nominal=5.3, error=0.00671, bulk_uF=1000,
        overdrive_mV=10, initial_high=True, l_scale=1.2)
    return rows


def thresholds(row):
    nominal, error = row['nominal_V'], row['static_error_fraction']
    return {'static_low_V': nominal*(1-error), 'static_high_V': nominal*(1+error),
            'raw_overdrive_V': row['sense_overdrive_V']*nominal/row['reference_V'],
            'effective_high_V': nominal*(1+error) + row['sense_overdrive_V']*nominal/row['reference_V']}


def settings(row):
    inputs = model.get_inputs('reviewed')
    inputs['bulk_esr_ohm'] = (row['bulk_esr_ohm'], 'ASSUMED', 'Margin-study ESR sensitivity; no qualified part')
    inputs['L_nom_H'] = (model.v('L_nom_H', inputs)*row['inductance_scale'], 'ASSUMED', 'Margin-study fault-only L sensitivity; Coilcraft source unavailable')
    if row['initial_high']:
        low, _, high = model.v('vraw_static_V', inputs)
        inputs['vraw_static_V'] = ((low, high, high), 'ASSUMED', 'Fault initial raw/load voltage set to calculated static-high sensitivity')
    option = dict(action='disconnect', ideal_diode=True, bulk_F=row['bulk_F'],
                  trip_V=thresholds(row)['effective_high_V'], delay_s=row['delay_s'])
    return inputs, option


def evaluate(row):
    inputs, option = settings(row)
    fault = model.summarize_runs(option, inputs)
    # Do not multiply the release tolerance sweep a second time by the fault-only L sensitivity.
    release_inputs = model.get_inputs('reviewed')
    release = max(r['raw_peak_V'] for r in model.load_release(row['bulk_F'], inputs=release_inputs))
    limits = thresholds(row)
    nuisance = 1000*(limits['static_low_V'] - release)
    startup = model.startup(row['bulk_F'], model.v('startup_load_A'), inputs=inputs)
    allowance = model.v('startup_current_limit_fraction')*model.v('efuse_iol_min_A')
    return {'id': row['id'], 'parameter_classification': 'ASSUMED; evaluation only', 'parameters': row,
            'result_classification': 'CALCULATED; no electrical acceptance', 'thresholds': limits,
            'fault': fault, 'release_peak_estimate_V': release,
            'nuisance_margin_estimate_mV': nuisance,
            'nuisance_excess_over_50mV': nuisance-NUISANCE_MV,
            'meets_joint_numerical_objectives_only': fault['min_margin_to_limit_mV'] >= TARGET_MV and nuisance >= NUISANCE_MV,
            'startup_screen': startup, 'startup_90pct_allowance_A': allowance,
            'stored_bulk_energy_J_at_24p72V': 0.5*row['bulk_F']*24.72**2,
            'stored_bulk_energy_J_at_28p3V': 0.5*row['bulk_F']*28.3**2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    report = {'classification': 'CALCULATED sensitivity study, not a bound or architecture selection',
              'limit_V': {'value':5.5,'label':'KNOWN','source':'BRIEF_02_AMENDMENT_1.md user requirement'},
              'target_margin_mV': {'value':TARGET_MV,'label':'ASSUMED','source':'Evaluation objective: move beyond near-zero margin; residual electrical/model uncertainties unbounded'},
              'nuisance_margin_mV': {'value':NUISANCE_MV,'label':'ASSUMED','source':'Original brief criterion 1; vendor load-release peak required'},
              'static_error_alternative': 'ASSUMED 0.671% allocation from committed OPTION_I_CANDIDATES.md; not a component guarantee',
              'spice_status':'NOT RUN','vendor_status':'NOT RUN','electrical_acceptance':'NOT DEMONSTRATED',
              'python_model_sha256':hashlib.sha256(Path(model.__file__).read_bytes()).hexdigest(),
              'study_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'limitations': model.MODEL_COVERAGE + [
                  'Release estimate treats bulk as ideal parallel capacitance, omitting its ESR and control loop; nuisance margin may be overstated.',
                  'Startup excludes load capacitance, input-path losses and PGOOD connection dynamics; uses evaluated effective bulk, not its unknown maximum tolerance.',
                  'Optional 10 mV sense overdrive uses the ideal nominal divider; final feedback/clamp network gain and delay need verification.',
                  'Proposed 100 mV study target is not an uncertainty bound. Exact parts, area, monetary cost and worst-case performance remain UNKNOWN.'],
              'scenarios':[]}
    for row in scenarios():
        result = evaluate(row); report['scenarios'].append(result)
        print(f"{row['id']:34s} peak {result['fault']['worst_peak_load_V']:.3f} V; "
              f"margin {result['fault']['min_margin_to_limit_mV']:.3f} mV; "
              f"nuisance estimate {result['nuisance_margin_estimate_mV']:.3f} mV", flush=True)
    if args.write:
        OUT.write_text(json.dumps(report,indent=1)+'\n'); print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
