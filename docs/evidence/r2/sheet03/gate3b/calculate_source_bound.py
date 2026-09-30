#!/usr/bin/env python3
"""Gate3b conditional bounds; JSON input only, no native CAD access.

Published graph readings are ASSUMED differential-L proxies. They cannot
supply a guaranteed application maximum. Finite targets never replace OPEN.
"""
import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / 'CALCULATIONS.json'
CURVES = {
    '7443763540068': {'L_uH': 6.8, 'DCR20_max_mohm': 1.2,
                     'points_A_uH': [[0, 6.8], [5, 6.8], [20, 6.8], [40, 6.8], [60, 6.775]]},
    '74437636350652': {'L_uH': 6.5, 'DCR20_max_mohm': .418,
                      'points_A_uH': [[0, 6.5], [5, 6.5], [20, 6.4], [40, 6.2], [60, 5.8], [80, 5.3], [100, 4.7], [120, 4.1]]},
    '74437636351002': {'L_uH': 10., 'DCR20_max_mohm': .682,
                      'points_A_uH': [[0, 10.], [5, 10.], [20, 9.8], [40, 9.25], [60, 8.4], [80, 7.5], [100, 6.6]]},
}

def integral(points, start, stop, weight_current=False):
    """Exact integration of a piecewise linear proxy; no extrapolation."""
    if start < points[0][0] or stop > points[-1][0] or stop < start:
        raise ValueError('Integration outside documented proxy domain')
    result = 0.
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        lo, hi = max(start, x0), min(stop, x1)
        if hi <= lo:
            continue
        slope = (y1 - y0) / (x1 - x0)
        intercept = y0 - slope * x0
        if weight_current:
            result += intercept * (hi**2 - lo**2)/2 + slope * (hi**3 - lo**3)/3
        else:
            result += intercept * (hi - lo) + slope * (hi**2 - lo**2)/2
    return result * 1e-6

def graph_ramp(points, voltage, initial, time):
    # ASSUMED maintained Vin, output>=0; use output=0 for ramp/charge screen.
    target = voltage * time
    if target > integral(points, initial, points[-1][0]):
        return {'I_A': None, 'Q_C': None, 'domain': 'OPEN: model exits tabulated proxy domain'}
    lo, hi = initial, points[-1][0]
    for _ in range(70):
        mid = (lo + hi)/2
        if integral(points, initial, mid) < target:
            lo = mid
        else:
            hi = mid
    current = (lo + hi)/2
    return {'I_A': current, 'Q_C': integral(points, initial, current, True)/voltage,
            'L_energy_change_J': integral(points, initial, current, True),
            'source_work_J': integral(points, initial, current, True),
            'domain': 'ASSUMED graph proxy only; not an application bound'}

def envelope_charge(initial, slope, ceiling, time):
    crossover = max(0., (ceiling - initial)/slope)
    ramp_time = min(time, crossover)
    return initial*ramp_time + .5*slope*ramp_time**2 + ceiling*max(0., time-crossover)

def calculate():
    baseline = json.loads(BASELINE.read_text())['gate_2c']
    voltages = [24., 27.63, baseline['input']['OVP_max_V']]
    curves = {}
    for mpn, part in CURVES.items():
        nominal = part['L_uH'] * 1e-6
        normal = []
        for vin in (9., 24., voltages[-1]):
            vo = baseline['24V_vs_12V']['partial_loss_screens'][0]['output_V']
            ripple = vo*(1-vo/vin)/(nominal*400e3)
            ripple_hi = vo*(1-vo/vin)/(nominal*.8*360e3)
            hot_dcr = part['DCR20_max_mohm'] * 1.393 / 1000
            normal.append({'Vin_V': vin, 'ripple_nominal_App': ripple,
                           'ripple_Lminus20pct_f360kHz_App': ripple_hi,
                           'copper20_W_at5A_with_ripple': (25+ripple*ripple/12)*part['DCR20_max_mohm']/1000,
                           'copper120_W_with_assumed_copper_TCR': (25+ripple*ripple/12)*hot_dcr})
        curves[mpn] = {'classification': 'CALCULATED with ASSUMED typical graph proxy at20C; tolerance/temp/pulse transfer OPEN',
                       'part': part, 'normal': normal,
                       'maintained_source_fault_screens': [
                           {'Vin_V': vin, 'time_from_fault_s': time, **graph_ramp(part['points_A_uH'], vin, 8., time)}
                           for vin in voltages for time in (2e-6, 5e-6, 10e-6, 20e-6)],
                       'application_fault_current_max_A': None, 'actual_reaction_min_max_s': [None, None]}
    target = {'classification': 'ASSUMED qualification contract, not selected/qualified implementation',
              'Cin_effective_min_F': 10e-6, 'Cin_effective_max_F': 30e-6,
              'source_positive_charge_until_actual_current_isolation_C': 100e-6,
              'physical_source_current_off_s_max': 10e-6,
              'Ldiff_min_H': 5e-6, 'Ldiff_max_H': 12e-6,
              'Ldiff_qualified_domain_A': 100., 'initial_L_current_A_max': 8.,
              'initial_output_voltage_V_max': 5.5, 'raw_cap_bank_max_F': .0054144+182.16e-6}
    shared = []
    for vin in voltages:
        cap = .5*target['Cin_effective_max_F']*vin**2
        source = vin*target['source_positive_charge_until_actual_current_isolation_C']
        l_initial = .5*target['Ldiff_max_H']*8**2
        pool = cap+source+l_initial
        current = math.sqrt(2*pool/target['Ldiff_min_H'])
        raw = .5*target['raw_cap_bank_max_F']*5.5**2
        slope = vin/target['Ldiff_min_H']
        shared.append({'Vin_V': vin, 'local_input_energy_J': cap, 'continued_source_work_J': source,
                       'initial_L_energy_J': l_initial, 'new_fault_pool_J': pool,
                       'conditional_L_current_ceiling_A': current, 'within_100A_domain': current<=100,
                       'raw_initial_cap_energy_J': raw, 'source_plus_raw_initial_pool_J': pool+raw,
                       'L_envelopes': [{'time_s': t, 'I_upper_A': min(8+slope*t, current),
                                        'Q_to_raw_upper_C': envelope_charge(8, slope, current, t)}
                                       for t in (2e-6, 5e-6, 10e-6, 20e-6)],
                       'existing_Cin_60p996uF_I_screen_A': math.sqrt(2*(.5*60.996e-6*vin**2+source+l_initial)/5e-6),
                       'source_limit_does_not_bound_Cin_discharge_A_at0p1uH': math.sqrt(8**2+2*cap/.1e-6)})
    worst = shared[-1]
    normal6 = baseline['buck_static']['max_V']+.020+6*.004+(6*20e-6+.5*12e-6*6**2/baseline['buck_static']['min_V'])/.0024064
    normal8 = baseline['buck_static']['max_V']+.020+8*.004+(8*20e-6+.5*12e-6*8**2/baseline['buck_static']['min_V'])/.0024064
    d_module = 5.38+80*.5e-6/1e-3+80*.0005+.020
    nonfet = baseline['margins']['harness']['reduced_R_ohm']-.0136
    e_loop = nonfet-(.024375-.015)+.0048+.00386+.00606+.0025
    s = {'classification': 'CALCULATED only within stated ASSUMED contracts; application proof OPEN',
         'new_qualified_trip_target_V': [5.300, 5.340], 'actual_trip_min_max_V': [None, None],
         'normal_release_6A_20us_V': normal6, 'normal_release_8A_20us_V': normal8,
         'normal6_false_trip_reserve_V': 5.300-normal6-.010,
         'normal8_false_trip_reserve_V': 5.300-normal8-.010,
         'normal6_30us_reserve_V': 5.300-normal6-6*10e-6/.0024064-.010,
         'D_module_target_peak_V_at80A': d_module, 'D_module_margin_V': 5.5-d_module,
         'D_protected_interval_energy_J_at80A': d_module*80*2e-6,
         'D_source_raw_module_subtotal_J': worst['source_plus_raw_initial_pool_J']+.5*.0015*5.5**2,
         'D_complete_store_max_J': None, 'D_application_Pi_peak_V': None,
         'E_breaker_threshold_A_at_35_45mV_and6mohm_pm1pct': [.035/.00606, .045/.00594],
         'E_REQUIRED_full_current_trip_max_A': 8., 'E_required_physical_off_s': 2e-6,
         'E_required_Lfloor_H_at_31p5V': 31.5*2e-6/(10-8),
         'E_Lfloor_proposal_H': 35e-6, 'E_Lmax_proposal_H': 50e-6,
         'E_current_with35uH_2us_31p5V_A': 8+31.5*2e-6/35e-6,
         'E_received_absorber_energy_screen_J': 5.42*10*5e-6+.5*50e-6*10**2,
         'E_total_initial_pool_with1p5mF_Pi_J': worst['source_plus_raw_initial_pool_J']+.5*.0015*5.5**2,
         'E_series_contract_screen_using_NEW5p34_target_V': 5.34+10*5e-6/1e-3+10*.005+.020,
         'E_application_Pi_peak_V': None, 'E_normal_loop_target_ohm': e_loop,
         'E_Pi_5A_screen_V': baseline['buck_static']['min_V']-5*e_loop,
         'E_100ASE_two_pairs_before_new_shunt_L_ohm': nonfet+4*.0024,
         'E_existing_loop_plus_10mohm_Pi_V': baseline['buck_static']['min_V']-5*(baseline['margins']['harness']['reduced_R_ohm']+.010)}
    return {'classification': 'Conditional engineering study; not validated or qualified electrical behavior',
            'baseline_commit': '65a8698', 'actual_source_current_max_A': None,
            'actual_source_energy_max_J': None, 'actual_input_transient_ceiling_V': None,
            'curve_models': curves, 'ASSUMED_source_contract': target, 'CALCULATED_source_contract': shared,
            'D_E_rescore': s,
            'supply_hold': {'classification': 'CALCULATED with ASSUMED load/charge/rail values; hot gate/supply validity OPEN',
                            'Vstart_min': 11.2, 'Vvalid_min': 10.5, 'Icontrol_A': .025,
                            'Qg_aggregate_C': 4*509e-9, 'hold_required_s': .001, 'effective_C_F': 47e-6,
                            'required_C_F': (.025*.001+4*509e-9)/.7,
                            'available_hold_s': (47e-6*.7-4*509e-9)/.025}}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args=parser.parse_args()
    rendered=json.dumps(calculate(), indent=2, sort_keys=True)+'\n'
    if args.write:
        (HERE/'SOURCE_BOUND_CALCULATIONS.json').write_text(rendered)
    else:
        print(rendered, end='')
if __name__=='__main__':
    main()
