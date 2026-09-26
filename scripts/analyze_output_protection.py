#!/usr/bin/env python3
"""V1A output-protection screening model: buck high-side short, load release, startup.

CALCULATION ONLY. Lumped, piecewise-linear Euler model with explicit assumptions. It is a
screen for comparing architectures, not a qualification bound: no LM61460 control loop, no
low-side/shoot-through path, no capacitor C(V), no MOSFET switching dynamics, no layout
parasitics. Every input carries an evidence label; see PROTECTION_ANALYSIS.md.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/evidence/r2/protection_analysis_2026-09-26/protection_model_results.json'

# name: (value, label, source)
INPUTS = {
    'vin_source_max_V': (24.72, 'ASSUMED', 'GST60A24 24 V x 1.03 tolerance, Mean Well GST60A spec'),
    'efuse_iol_nom_A': (4.48, 'CALCULATED', 'TPS26630 I(OL)=18/R_ILIM(kOhm), R105 4.02 kOhm; SLVSE94G'),
    'efuse_iol_tol': (0.07, 'KNOWN', 'SLVSE94G: +/-7 % current-limit accuracy'),
    'efuse_ron_ohm': (0.0345, 'KNOWN', 'SLVSE94G RON max 34.5 mOhm at 25 C'),
    'buck_hs_rdson_ohm': (0.041, 'KNOWN', 'LM61460 SNVSBD5D HS RDS(on) typ; failed-short resistance UNKNOWN'),
    'L_nom_H': (6.8e-6, 'KNOWN', 'XAL8080-682 nominal, +/-20 %'),
    'L_dcr_max_ohm': (0.0146, 'CALCULATED', 'back-calculated from calculate_r2.py max-DCR copper loss'),
    'L_isat_A': (14.0, 'ASSUMED', 'saturation knee not verified (Coilcraft drawing download failed)'),
    'L_sat_ratio': (0.7, 'ASSUMED', 'inductance above knee, soft-saturation screen'),
    'vraw_static_V': ((5.038271401729418, 5.098360655737705, 5.158632237795172), 'CALCULATED', 'calculate_r2.py'),
    'cin_eff_F': ((15e-6, 40e-6), 'ASSUMED', '2x22 uF X7R at 24 V; DC-bias minimum OPEN (CAPACITOR_QUALIFICATION.md)'),
    'craw_eff_F': ((60e-6, 130e-6), 'ASSUMED', '6x22 uF X7R at 5.1 V; nominal 132 uF, bias/aging minimum OPEN'),
    'fet_rds_hot_ohm': (3.25e-3, 'KNOWN', 'PSMN1R8-40YLC max at VGS 10 V, Tj 150 C'),
    'shunt_ohm': (2e-3, 'KNOWN', 'WSL27262L000FEA'),
    'ideal_diode_off_s': (0.875e-6, 'KNOWN', 'LM74800 tDGATE_OFF(dly) max, SNOSD95C 7.6'),
    'lm74800_ov_deglitch_s': (5.4e-6, 'AMBIGUOUS', 'SNOSD95C row 3.98/5.4 us; max column not confirmed'),
    'lm74800_en_off_max_s': (6.0e-6, 'KNOWN', 'tEN_OFF(deg)_HGATE 3/4.6/6 us'),
    'hgate_discharge_s': (0.571e-6, 'CALCULATED', 'Qg 96 nC / 168 mA sink, PSMN1R8-40YLC + SNOSD95C'),
    'lm74800_trip_worst_high_V': (5.7936, 'CALCULATED', '348k/97.6k 0.1 % divider, VOVR 1.267 V max'),
    'precision_trip_worst_high_V': (5.50, 'ASSUMED', 'target for a +/-1.1 % precision detector; parts OPEN'),
    'precision_trip_with_bulk_worst_high_V': (5.46, 'ASSUMED', '5.40 V nominal +/-1.1 %, usable only with bulk'),
    'precision_detect_s': (0.3e-6, 'ASSUMED', 'fast comparator + driver; parts OPEN'),
    'crowbar_ohm': (0.01, 'ASSUMED', 'crowbar switch + copper'),
    'crowbar_loop_H': (10e-9, 'ASSUMED', 'crowbar loop inductance incl. MLCC ESL; layout OPEN'),
    'fast_gate_off_s': (0.1e-6, 'ASSUMED', 'discrete gate pull-down of Q302; circuit OPEN'),
    'bulk_esr_ohm': (0.02, 'ASSUMED', 'hybrid-polymer class bank ESR'),
}


def v(name):
    return INPUTS[name][0]


def high_side_short(opt, cin, craw, i_load, c_load, lossy, dt=2e-9, t_end=120e-6):
    """Hard short of the buck high-side switch at t=0 with the source at its maximum."""
    vs = v('vin_source_max_V')
    i_lim = v('efuse_iol_nom_A') * (1 + v('efuse_iol_tol'))
    r_hs = v('buck_hs_rdson_ohm') if lossy else 0.0
    dcr = v('L_dcr_max_ohm') if lossy else 0.0
    r_path = 2 * v('fet_rds_hot_ohm') + v('shunt_ohm')
    cb, rb = opt.get('bulk_F', 0.0), v('bulk_esr_ohm')
    vcin, vraw, vb, vload = vs, v('vraw_static_V')[1], v('vraw_static_V')[1], v('vraw_static_V')[1]
    il = i_load
    connected, crowbar, t_cross, t_act, rev_t = True, False, None, None, None
    peak_load = peak_raw = vload
    peak_il = il
    above = {'5V5': 0.0, '6V0': 0.0}
    e_crowbar = 0.0
    peak_i_cb = i_cb = 0.0
    t = 0.0
    while t < t_end:
        i_src = min(max((vs - vcin) / v('efuse_ron_ohm'), 0.0), i_lim)
        L = v('L_nom_H') if abs(il) <= v('L_isat_A') else v('L_nom_H') * v('L_sat_ratio')
        il += (vcin - il * (r_hs + dcr) - vraw) / L * dt
        vcin += (i_src - il) / cin * dt
        i_b = (vraw - vb) / rb if cb else 0.0
        vb += i_b / cb * dt if cb else 0.0
        if crowbar:
            i_cb += (vraw - i_cb * v('crowbar_ohm')) / v('crowbar_loop_H') * dt
        i_path = (vraw - vload) / r_path if connected else 0.0
        if connected and opt.get('ideal_diode') and i_path < 0:
            rev_t = t if rev_t is None else rev_t
            if t - rev_t >= v('ideal_diode_off_s'):
                connected = False
                i_path = 0.0
        elif i_path >= 0:
            rev_t = None
        vraw += (il - i_b - i_cb - i_path) / craw * dt
        i_ld = i_load if vload > 1.0 else i_load * vload
        vload += (i_path - i_ld) / c_load * dt
        if t_cross is None and vraw >= opt['trip_V']:
            t_cross = t
            t_act = t + opt['delay_s']
        if t_act is not None and t >= t_act:
            if opt['action'] == 'disconnect':
                connected = False
            else:
                crowbar = True
        e_crowbar += vraw * i_cb * dt
        peak_i_cb = max(peak_i_cb, i_cb)
        peak_load, peak_raw, peak_il = max(peak_load, vload), max(peak_raw, vraw), max(peak_il, il)
        above['5V5'] += dt if vload > 5.5 else 0.0
        above['6V0'] += dt if vload > 6.0 else 0.0
        t += dt
    return {
        'cin_uF': round(cin * 1e6), 'craw_uF': round(craw * 1e6), 'i_load_A': i_load,
        'c_load_uF': round(c_load * 1e6), 'lossy': lossy,
        'crossing_us': None if t_cross is None else round(t_cross * 1e6, 2),
        'peak_load_V': round(peak_load, 3), 'us_above_5V5': round(above['5V5'] * 1e6, 1),
        'us_above_6V0': round(above['6V0'] * 1e6, 1), 'peak_raw_V_120us': round(peak_raw, 2),
        'peak_inductor_A': round(peak_il, 1), 'peak_crowbar_A': round(peak_i_cb, 1),
        'crowbar_energy_mJ_120us': round(e_crowbar * 1e3, 2),
    }


OPTIONS = {
    'A_lm74800_ov_only': {'trip_V': v('lm74800_trip_worst_high_V'), 'action': 'disconnect',
                          'delay_s': v('lm74800_ov_deglitch_s') + v('hgate_discharge_s'), 'ideal_diode': True},
    'B1_A_plus_470uF_bulk': {'trip_V': v('lm74800_trip_worst_high_V'), 'action': 'disconnect', 'bulk_F': 470e-6,
                             'delay_s': v('lm74800_ov_deglitch_s') + v('hgate_discharge_s'), 'ideal_diode': True},
    'B2_A_plus_1000uF_bulk': {'trip_V': v('lm74800_trip_worst_high_V'), 'action': 'disconnect', 'bulk_F': 1000e-6,
                              'delay_s': v('lm74800_ov_deglitch_s') + v('hgate_discharge_s'), 'ideal_diode': True},
    'C_precision_crowbar_plus_ideal_diode': {'trip_V': v('precision_trip_worst_high_V'), 'action': 'crowbar',
                                             'delay_s': v('precision_detect_s'), 'ideal_diode': True},
    'D_precision_detector_to_lm74800_en': {'trip_V': v('precision_trip_worst_high_V'), 'action': 'disconnect',
                                           'delay_s': v('precision_detect_s') + v('lm74800_en_off_max_s')
                                           + v('hgate_discharge_s'), 'ideal_diode': True},
    'E_D_plus_470uF_bulk': {'trip_V': v('precision_trip_worst_high_V'), 'action': 'disconnect', 'bulk_F': 470e-6,
                            'delay_s': v('precision_detect_s') + v('lm74800_en_off_max_s')
                            + v('hgate_discharge_s'), 'ideal_diode': True},
    'G_precision_detector_fast_gate_pulldown': {'trip_V': v('precision_trip_worst_high_V'), 'action': 'disconnect',
                                                'delay_s': v('precision_detect_s') + v('fast_gate_off_s'),
                                                'ideal_diode': True},
    'H_470uF_bulk_plus_precision_crowbar': {'trip_V': v('precision_trip_with_bulk_worst_high_V'),
                                            'action': 'crowbar', 'bulk_F': 470e-6,
                                            'delay_s': v('precision_detect_s'), 'ideal_diode': True},
    'I_470uF_bulk_plus_precision_fast_gate_off': {'trip_V': v('precision_trip_with_bulk_worst_high_V'),
                                                  'action': 'disconnect', 'bulk_F': 470e-6,
                                                  'delay_s': v('precision_detect_s') + v('fast_gate_off_s'),
                                                  'ideal_diode': True},
    'F_precision_crowbar_no_ideal_diode': {'trip_V': v('precision_trip_worst_high_V'), 'action': 'crowbar',
                                           'delay_s': v('precision_detect_s'), 'ideal_diode': False},
}


def load_release(bulk_F=0.0):
    """Ideal-controller energy-transfer estimate of a full load release. Not a bound: a real
    peak-current-mode loop that keeps switching for part of a cycle makes it larger, finite
    load slew makes it smaller."""
    rows = []
    for c, lf, ipk in itertools.product(v('craw_eff_F'), (0.8, 1.0, 1.2), (5.0, 6.139)):
        L = v('L_nom_H') * lf
        v0 = v('vraw_static_V')[2]
        dv = math.sqrt(v0 ** 2 + L * ipk ** 2 / (c + bulk_F)) - v0
        rows.append({'craw_uF': round(c * 1e6), 'L_uH': round(L * 1e6, 2), 'i_peak_A': ipk,
                     'overshoot_V': round(dv, 4), 'raw_peak_V': round(v0 + dv, 4)})
    return rows


def startup(bulk_F, i_load, vin=9.0, eff=0.88):
    """Input current during buck soft start with the load already connected."""
    rows = {}
    for t_ss in (3.5e-3, 7e-3):
        c_total = v('craw_eff_F')[1] + bulk_F
        i_charge = c_total * v('vraw_static_V')[2] / t_ss
        p_in = v('vraw_static_V')[2] * (i_load + i_charge) / eff
        rows[f'tss_{t_ss * 1e3:g}ms'] = {'charge_A': round(i_charge, 3), 'input_A_at_9V': round(p_in / vin, 3),
                                        'efuse_min_limit_A': round(v('efuse_iol_nom_A') * (1 - v('efuse_iol_tol')), 3)}
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the dated evidence JSON')
    args = parser.parse_args()
    corners = list(itertools.product(v('cin_eff_F'), v('craw_eff_F'), (0.3, 5.0), (2e-6, 220e-6), (False, True)))
    results = {'classification': 'CALCULATION; lumped screening model, not a qualification bound',
               'inputs': {k: {'value': val, 'label': lab, 'source': src} for k, (val, lab, src) in INPUTS.items()},
               'high_side_short': {}, 'load_release': {}, 'startup_9V_5A': {}}
    for name, opt in OPTIONS.items():
        runs = [high_side_short(opt, *c) for c in corners]
        worst = max(runs, key=lambda r: r['peak_load_V'])
        results['high_side_short'][name] = {
            'option': opt, 'worst_peak_load_V': worst['peak_load_V'], 'worst_case': worst,
            'max_us_above_6V0': max(r['us_above_6V0'] for r in runs),
            'max_peak_crowbar_A': max(r['peak_crowbar_A'] for r in runs),
            'max_peak_inductor_A': max(r['peak_inductor_A'] for r in runs),
            'runs': runs}
        print(f"{name:40s} worst load peak {worst['peak_load_V']:.3f} V, "
              f"max >6.0 V {results['high_side_short'][name]['max_us_above_6V0']} us, "
              f"max crowbar {results['high_side_short'][name]['max_peak_crowbar_A']} A")
    for bulk in (0.0, 470e-6, 1000e-6):
        rows = load_release(bulk)
        key = f'bulk_{round(bulk * 1e6)}uF'
        results['load_release'][key] = {'worst_raw_peak_V': max(r['raw_peak_V'] for r in rows), 'rows': rows}
        results['startup_9V_5A'][key] = startup(bulk, 5.0)
        print(f"load release {key}: worst raw peak {results['load_release'][key]['worst_raw_peak_V']} V; "
              f"startup {results['startup_9V_5A'][key]}")
    if args.write:
        OUT.write_text(json.dumps(results, indent=1) + '\n')
        print(f'wrote {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
