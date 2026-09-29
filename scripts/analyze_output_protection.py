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
EVIDENCE = ROOT / 'docs/evidence/r2/protection_analysis_2026-09-29'
OUT = EVIDENCE / 'protection_model_results.json'
BASELINE_OUT = EVIDENCE / 'baseline_model_results.json'

# name: (value, label, source)
BASELINE_INPUTS = {
    'vin_source_max_V': (24.72, 'ASSUMED', 'GST60A24 24 V x 1.03 tolerance, Mean Well GST60A spec'),
    'efuse_iol_nom_A': (4.48, 'CALCULATED', 'TPS26630 I(OL)=18/R_ILIM(kOhm), R105 4.02 kOhm; SLVSE94G'),
    'efuse_iol_tol': (0.07, 'KNOWN', 'SLVSE94G: +/-7 % current-limit accuracy'),
    'efuse_ron_ohm': (0.0345, 'KNOWN', 'SLVSE94G RON max 34.5 mOhm at 25 C'),
    'buck_hs_rdson_ohm': (0.041, 'ASSUMED', 'LM61460 SNVSBD5D intact HS RDS(on) typ applied to failure; failed-short resistance UNKNOWN'),
    'L_nom_H': (6.8e-6, 'KNOWN', 'XAL8080-682 nominal, +/-20 %'),
    'L_dcr_max_ohm': (0.0146, 'CALCULATED', 'back-calculated from calculate_r2.py max-DCR copper loss'),
    'L_isat_A': (14.0, 'ASSUMED', 'saturation knee not verified (Coilcraft drawing download failed)'),
    'L_sat_ratio': (0.7, 'ASSUMED', 'inductance above knee, soft-saturation screen'),
    'vraw_static_V': ((5.038271401729418, 5.098360655737705, 5.158632237795172), 'CALCULATED', 'calculate_r2.py'),
    'cin_eff_F': ((15e-6, 40e-6), 'ASSUMED', '2x22 uF X7R at 24 V; DC-bias minimum OPEN (CAPACITOR_QUALIFICATION.md)'),
    'craw_eff_F': ((60e-6, 130e-6), 'ASSUMED', '6x22 uF X7R at 5.1 V; nominal 132 uF, bias/aging minimum OPEN'),
    'fet_rds_hot_ohm': (3.25e-3, 'ASSUMED', 'Historical PSMN1R8-40YLC hot-resistance claim; fresh primary source unavailable'),
    'shunt_ohm': (2e-3, 'KNOWN', 'WSL27262L000FEA'),
    'ideal_diode_off_s': (0.875e-6, 'ASSUMED', 'Known LM74800 tDGATE_OFF(dly) max, SNOSD95C, applied to current reversal without actual gate model'),
    'lm74800_ov_deglitch_s': (5.4e-6, 'UNKNOWN', 'Historical AMBIGUOUS classification: SNOSD95C row 3.98/5.4 us; max column then unconfirmed'),
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


def get_inputs(profile='reviewed'):
    """Independent labelled inputs; baseline preserves the 2026-09-26 numbers.

    The reviewed profile changes evidence and selected values, not model topology.
    An ASSUMED use of a known table row is not a manufacturer-guaranteed model.
    """
    if profile not in ('baseline', 'reviewed'):
        raise ValueError(f'Unknown profile: {profile}')
    inputs = dict(BASELINE_INPUTS)
    inputs.update({
        'load_current_corners_A': ((0.3, 5.0), 'ASSUMED', '2026-09-26 PROTECTION_ANALYSIS.md section 2; actual load envelope OPEN'),
        'load_capacitance_corners_F': ((2e-6, 220e-6), 'ASSUMED', '2026-09-26 REQUIREMENT_ENVELOPE_PROPOSED.md L6; actual Pi network UNKNOWN'),
        'bulk_capacitance_corners_F': ((0.0, 470e-6, 1000e-6), 'ASSUMED', 'Historical comparison values; effective bank minima not qualified; OPTION_I_CANDIDATES.md'),
        'load_rolloff_voltage_V': (1.0, 'ASSUMED', 'Numerical constant-current load becomes conductance below this voltage; not a Pi load model'),
        'load_screen_levels_V': ((5.5, 6.0), 'ASSUMED', 'Historical reporting thresholds retained for comparison; current user limit is separately labelled load_fault_limit_V'),
        'load_fault_limit_V': (5.5, 'KNOWN', 'User REQUIREMENT in BRIEF_02_AMENDMENT_1.md (2026-09-29); replaces 6 V screen and requires explicit margin'),
        'integration_step_s': (2e-9, 'ASSUMED', 'Historical Euler integration step; numerical setting, not device timing'),
        'fault_duration_s': (120e-6, 'ASSUMED', 'Historical fault observation interval; cannot establish indefinite fault hold'),
        'release_inductance_scales': ((0.8, 1.0, 1.2), 'ASSUMED', 'Inherited +/-20% screen; Coilcraft primary download blocked'),
        'release_peak_currents_A': ((5.0, 6.139), 'ASSUMED', 'Historical release envelope; 6.139 A inherited ripple estimate, not measured peak'),
        'startup_soft_start_s': ((3.5e-3, 7e-3), 'ASSUMED', 'Uses LM61460 tSS limits as a linear full-output ramp; actual endpoint is 90% reference'),
        'startup_input_V': (9.0, 'ASSUMED', 'Proposed minimum operating corner; REQUIREMENT_ENVELOPE_PROPOSED.md S1b'),
        'startup_load_A': (5.0, 'ASSUMED', 'Proposed continuous load; REQUIREMENT_ENVELOPE_PROPOSED.md L2'),
        'startup_efficiency': (0.88, 'ASSUMED', 'Historical efficiency estimate at startup; no converter control/efficiency model'),
        'startup_current_limit_fraction': (0.9, 'ASSUMED', 'Brief criterion 5 proposed input-current margin'),
        'q302_gate_charge_C': (96e-9, 'ASSUMED', 'Nexperia primary download HTTP 403; inherited charge, maximum and test conditions UNKNOWN'),
        'hgate_sink_min_A': (0.168, 'KNOWN', 'TI LM7480-Q1 SNOSD95C p6 minimum sink under specified conditions; not a constant waveform'),
        'hgate_source_max_A': (75e-6, 'KNOWN', 'TI LM7480-Q1 SNOSD95C p6 maximum; Task 1 visual primary-source review'),
        'precision_isolation_sensitivity_s': (2e-6, 'ASSUMED', 'Brief criterion 3 proposed worst-case allocation, not demonstrated circuit delay'),
    })
    if profile == 'reviewed':
        inputs.update({
            'efuse_iol_nom_A': (4.5, 'KNOWN', 'TI TPS2663 SLVSE94G p7 typical at RILIM=4.02 kOhm; direct table basis'),
            'efuse_iol_tol': (0.07, 'KNOWN', 'TI TPS2663 SLVSE94G p7: 4.185/4.5/4.815 A MIN/TYP/MAX; excludes external resistor tolerance'),
            'efuse_ilim_resistor_tol': (0.001, 'KNOWN', 'Captured R105 specified +/-0.1%; TPS2663_SOURCE_REVIEW.md tolerance screen'),
            'efuse_iol_max_A': (4.815 / 0.999, 'CALCULATED', 'SLVSE94G p7 4.815 A / (1 - 0.001), conditional inverse-resistance scaling; not a new guaranteed row'),
            'efuse_iol_min_A': (4.185 / 1.001, 'CALCULATED', 'SLVSE94G p7 4.185 A / (1 + 0.001), conditional inverse-resistance scaling; not a new guaranteed row'),
            'efuse_ron_ohm': (0.053, 'KNOWN', 'TI TPS2663 SLVSE94G p7 maximum -40 to +125 C at 0.6 to 6 A; 34.5 mOhm is 25 C only'),
            'buck_hs_rdson_ohm': (0.041, 'ASSUMED', 'Intact LM61460 SNVSBD5D p6 typical is 41 mOhm; failed-short resistance UNKNOWN; retained comparison value'),
            'L_nom_H': (6.8e-6, 'KNOWN', 'Inherited XAL8080-682 nominal from captured BOM; no fresh Coilcraft tolerance/saturation verification'),
            'fet_rds_hot_ohm': (3.25e-3, 'ASSUMED', 'Inherited PSMN1R8-40YLC hot resistance; Nexperia primary download HTTP 403, condition/maxima unverified'),
            'ideal_diode_off_s': (0.875e-6, 'ASSUMED', 'Known SNOSD95C p6 tDGATE_OFF max uses 10 nF and +30 to -100 mV step; applying to path current is ASSUMED'),
            'lm74800_ov_deglitch_s': (5.4e-6, 'KNOWN', 'TI SNOSD95C p7 visually confirmed MAX; ends at HGATE falling, not full isolation'),
            'lm74800_en_off_max_s': (6e-6, 'KNOWN', 'TI SNOSD95C p7 MAX HGATE deglitch; ends at HGATE falling, not full isolation'),
            'hgate_discharge_s': (96e-9 / 0.168, 'CALCULATED', 'ASSUMED Qg=96 nC / KNOWN sink minimum 168 mA; charge quotient only, not worst-case isolation'),
        })
    else:
        # Preserve both multiplication order and exact historical floating values.
        inputs['efuse_iol_max_A'] = (4.48 * (1 + 0.07), 'CALCULATED', 'Historical equation-based rounded 4.48 A times 1.07; no resistor scaling')
        inputs['efuse_iol_min_A'] = (4.48 * (1 - 0.07), 'CALCULATED', 'Historical equation-based rounded 4.48 A times 0.93; no resistor scaling')
    return inputs


INPUTS = get_inputs('reviewed')


def v(name, inputs=None):
    return (INPUTS if inputs is None else inputs)[name][0]


def corners(inputs=None):
    """The historical five-dimensional, 32-corner fault comparison."""
    return list(itertools.product(v('cin_eff_F', inputs), v('craw_eff_F', inputs),
                                  v('load_current_corners_A', inputs),
                                  v('load_capacitance_corners_F', inputs), (False, True)))


def high_side_short(opt, cin, craw, i_load, c_load, lossy, dt=None, t_end=None, *, inputs=None):
    """Hard short of the buck high-side switch at t=0 with the source at its maximum."""
    val = lambda name: v(name, inputs)
    dt = val('integration_step_s') if dt is None else dt
    t_end = val('fault_duration_s') if t_end is None else t_end
    if dt <= 0 or t_end <= 0 or cin <= 0 or craw <= 0 or c_load <= 0:
        raise ValueError('Integration times and capacitances must be positive')
    vs = val('vin_source_max_V')
    i_lim = val('efuse_iol_max_A')
    r_hs = val('buck_hs_rdson_ohm') if lossy else 0.0
    dcr = val('L_dcr_max_ohm') if lossy else 0.0
    r_path = 2 * val('fet_rds_hot_ohm') + val('shunt_ohm')
    cb, rb = opt.get('bulk_F', 0.0), val('bulk_esr_ohm')
    vcin, vraw, vb, vload = vs, val('vraw_static_V')[1], val('vraw_static_V')[1], val('vraw_static_V')[1]
    il = i_load
    connected, crowbar, t_cross, t_act, rev_t = True, False, None, None, None
    peak_load = peak_raw = vload
    peak_il = il
    above = {'5V5': 0.0, '6V0': 0.0}
    e_crowbar = 0.0
    peak_i_cb = i_cb = 0.0
    load_floor = val('load_rolloff_voltage_V')
    low_screen, high_screen = val('load_screen_levels_V')
    t = 0.0
    while t < t_end:
        i_src = min(max((vs - vcin) / val('efuse_ron_ohm'), 0.0), i_lim)
        L = val('L_nom_H') if abs(il) <= val('L_isat_A') else val('L_nom_H') * val('L_sat_ratio')
        il += (vcin - il * (r_hs + dcr) - vraw) / L * dt
        vcin += (i_src - il) / cin * dt
        i_b = (vraw - vb) / rb if cb else 0.0
        vb += i_b / cb * dt if cb else 0.0
        if crowbar:
            i_cb += (vraw - i_cb * val('crowbar_ohm')) / val('crowbar_loop_H') * dt
        i_path = (vraw - vload) / r_path if connected else 0.0
        if connected and opt.get('ideal_diode') and i_path < 0:
            rev_t = t if rev_t is None else rev_t
            if t - rev_t >= val('ideal_diode_off_s'):
                connected = False
                i_path = 0.0
        elif i_path >= 0:
            rev_t = None
        vraw += (il - i_b - i_cb - i_path) / craw * dt
        i_ld = i_load if vload > load_floor else i_load * vload / load_floor
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
        above['5V5'] += dt if vload > low_screen else 0.0
        above['6V0'] += dt if vload > high_screen else 0.0
        t += dt
    return {
        'cin_uF': round(cin * 1e6), 'craw_uF': round(craw * 1e6), 'i_load_A': i_load,
        'c_load_uF': round(c_load * 1e6), 'lossy': lossy,
        'crossing_us': None if t_cross is None else round(t_cross * 1e6, 2),
        'peak_load_V': round(peak_load, 3), 'us_above_5V5': round(above['5V5'] * 1e6, 1),
        'peak_load_unrounded_V': peak_load,
        'margin_to_limit_mV': round((val('load_fault_limit_V') - peak_load) * 1000, 3),
        'us_above_6V0': round(above['6V0'] * 1e6, 1), 'peak_raw_V_120us': round(peak_raw, 2),
        'peak_inductor_A': round(peak_il, 1), 'peak_crowbar_A': round(peak_i_cb, 1),
        'crowbar_energy_mJ_120us': round(e_crowbar * 1e3, 2),
    }


def build_options(inputs=None):
    val = lambda name: v(name, inputs)
    options = {
        'A_lm74800_ov_only': {'trip_V': val('lm74800_trip_worst_high_V'), 'action': 'disconnect',
                              'delay_s': val('lm74800_ov_deglitch_s') + val('hgate_discharge_s'), 'ideal_diode': True},
        'B1_A_plus_470uF_bulk': {'trip_V': val('lm74800_trip_worst_high_V'), 'action': 'disconnect', 'bulk_F': val('bulk_capacitance_corners_F')[1],
                                 'delay_s': val('lm74800_ov_deglitch_s') + val('hgate_discharge_s'), 'ideal_diode': True},
        'B2_A_plus_1000uF_bulk': {'trip_V': val('lm74800_trip_worst_high_V'), 'action': 'disconnect', 'bulk_F': val('bulk_capacitance_corners_F')[2],
                                  'delay_s': val('lm74800_ov_deglitch_s') + val('hgate_discharge_s'), 'ideal_diode': True},
        'C_precision_crowbar_plus_ideal_diode': {'trip_V': val('precision_trip_worst_high_V'), 'action': 'crowbar',
                                                 'delay_s': val('precision_detect_s'), 'ideal_diode': True},
        'D_precision_detector_to_lm74800_en': {'trip_V': val('precision_trip_worst_high_V'), 'action': 'disconnect',
                                               'delay_s': val('precision_detect_s') + val('lm74800_en_off_max_s')
                                               + val('hgate_discharge_s'), 'ideal_diode': True},
        'E_D_plus_470uF_bulk': {'trip_V': val('precision_trip_worst_high_V'), 'action': 'disconnect', 'bulk_F': val('bulk_capacitance_corners_F')[1],
                                'delay_s': val('precision_detect_s') + val('lm74800_en_off_max_s')
                                + val('hgate_discharge_s'), 'ideal_diode': True},
        'G_precision_detector_fast_gate_pulldown': {'trip_V': val('precision_trip_worst_high_V'), 'action': 'disconnect',
                                                    'delay_s': val('precision_detect_s') + val('fast_gate_off_s'),
                                                    'ideal_diode': True},
        'H_470uF_bulk_plus_precision_crowbar': {'trip_V': val('precision_trip_with_bulk_worst_high_V'),
                                                'action': 'crowbar', 'bulk_F': val('bulk_capacitance_corners_F')[1],
                                                'delay_s': val('precision_detect_s'), 'ideal_diode': True},
        'I_470uF_bulk_plus_precision_fast_gate_off': {'trip_V': val('precision_trip_with_bulk_worst_high_V'),
                                                      'action': 'disconnect', 'bulk_F': val('bulk_capacitance_corners_F')[1],
                                                      'delay_s': val('precision_detect_s') + val('fast_gate_off_s'),
                                                      'ideal_diode': True},
        'F_precision_crowbar_no_ideal_diode': {'trip_V': val('precision_trip_worst_high_V'), 'action': 'crowbar',
                                               'delay_s': val('precision_detect_s'), 'ideal_diode': False},
    }
    return options


OPTIONS = build_options(INPUTS)

def load_release(bulk_F=0.0, *, inputs=None):
    """Ideal-controller energy-transfer estimate of a full load release. Not a bound: a real
    peak-current-mode loop that keeps switching for part of a cycle makes it larger, finite
    load slew makes it smaller."""
    rows = []
    for c, lf, ipk in itertools.product(v('craw_eff_F', inputs),
                                       v('release_inductance_scales', inputs),
                                       v('release_peak_currents_A', inputs)):
        L = v('L_nom_H', inputs) * lf
        v0 = v('vraw_static_V', inputs)[2]
        dv = math.sqrt(v0 ** 2 + L * ipk ** 2 / (c + bulk_F)) - v0
        rows.append({'craw_uF': round(c * 1e6), 'L_uH': round(L * 1e6, 2), 'i_peak_A': ipk,
                     'overshoot_V': round(dv, 4), 'raw_peak_V': round(v0 + dv, 4)})
    return rows


def startup(bulk_F, i_load, vin=None, eff=None, *, inputs=None):
    """Input current during buck soft start with the load already connected."""
    rows = {}
    vin = v('startup_input_V', inputs) if vin is None else vin
    eff = v('startup_efficiency', inputs) if eff is None else eff
    for t_ss in v('startup_soft_start_s', inputs):
        c_total = v('craw_eff_F', inputs)[1] + bulk_F
        i_charge = c_total * v('vraw_static_V', inputs)[2] / t_ss
        p_in = v('vraw_static_V', inputs)[2] * (i_load + i_charge) / eff
        rows[f'tss_{t_ss * 1e3:g}ms'] = {'charge_A': round(i_charge, 3), 'input_A_at_9V': round(p_in / vin, 3),
                                        'efuse_min_limit_A': round(v('efuse_iol_min_A', inputs), 3)}
    return rows


MODEL_COVERAGE = [
    'ASSUMED instantaneous current-limited source; no TPS26630 fast-trip, off/restart, bandwidth, OVP, overload timer or thermal model.',
    'ASSUMED initially charged input/raw/load capacitors, with inductor current initialized to load current; not a solved DC operating point.',
    'ASSUMED failed high-side resistance uses intact typical resistance in lossy corners; lossless corners set it and DCR to zero.',
    'ASSUMED discontinuous inductance change at an unverified saturation knee; no hysteresis, flux continuity model or core loss.',
    'ASSUMED lumped capacitor values/ESR; no voltage dependence, tolerance trajectory, ESL or parasitic layout ringing.',
    'ASSUMED ideal detector/latching state and fixed switch delays; no gate/Miller waveform, comparator overdrive or power-state reset.',
    'ASSUMED no re-enable within the observation window; this is programmed behavior, not evidence for physical recovery policy.',
    'ASSUMED reverse turnoff maps a gate-voltage timing row to path-current reversal; no ideal-diode loop dynamics.',
    'UNKNOWN failed converter low-side conduction, shoot-through, damage propagation, SOA and load-network dynamics.',
    'UNKNOWN load-release control-loop response and bulk stability; energy transfer estimate only.',
    'ASSUMED linear full-output soft-start ramp and fixed efficiency; source tSS actually ends at 90% reference.',
    'UNKNOWN startup with delayed BUCK_PGOOD enable, load capacitor inrush, hot plug and indefinite raw-side fault hold.',
]


def summarize_runs(opt, inputs):
    runs = [high_side_short(opt, *corner, inputs=inputs) for corner in corners(inputs)]
    worst = max(runs, key=lambda r: r['peak_load_unrounded_V'])
    return {'option': opt, 'worst_peak_load_V': worst['peak_load_V'], 'worst_case': worst,
            'min_margin_to_limit_mV': min(r['margin_to_limit_mV'] for r in runs),
            'max_us_above_5V5': max(r['us_above_5V5'] for r in runs),
            'max_us_above_6V0': max(r['us_above_6V0'] for r in runs),
            'max_peak_crowbar_A': max(r['peak_crowbar_A'] for r in runs),
            'max_peak_inductor_A': max(r['peak_inductor_A'] for r in runs), 'runs': runs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the dated evidence JSON')
    parser.add_argument('--profile', choices=('baseline', 'reviewed'), default='reviewed',
                        help='baseline reproduces historical numbers; reviewed applies Task 1 inputs')
    args = parser.parse_args()
    inputs = get_inputs(args.profile)
    results = {'classification': 'CALCULATED; lumped screening model, not a qualification bound',
               'profile': args.profile,
               'profile_evidence': 'Historical numerical reproduction only' if args.profile == 'baseline' else 'Task 1 reviewed values with remaining assumptions explicit',
               'spice_status': 'NOT RUN', 'vendor_model_status': 'NOT RUN',
               'model_coverage': MODEL_COVERAGE,
               'inputs': {k: {'value': val, 'label': lab, 'source': src} for k, (val, lab, src) in inputs.items()},
               'high_side_short': {}, 'load_release': {}, 'startup_9V_5A': {}}
    print(f'Profile {args.profile}; CALCULATED screening only; SPICE NOT RUN', flush=True)
    for name, opt in build_options(inputs).items():
        result = summarize_runs(opt, inputs)
        results['high_side_short'][name] = result
        print(f"{name:40s} worst load peak {result['worst_peak_load_V']:.3f} V, "
              f"margin to 5.5 V {result['min_margin_to_limit_mV']:.3f} mV, "
              f"max crowbar {result['max_peak_crowbar_A']} A", flush=True)
    if args.profile == 'reviewed':
        opt = dict(build_options(inputs)['I_470uF_bulk_plus_precision_fast_gate_off'])
        opt['delay_s'] = v('precision_isolation_sensitivity_s', inputs)
        result = summarize_runs(opt, inputs)
        results['timing_sensitivity'] = {'classification': 'CALCULATED using ASSUMED 2 us total isolation delay',
                                         'I_2us_total_isolation': result}
        print(f"I_2us_total_isolation worst load peak {result['worst_peak_load_V']:.3f} V", flush=True)
    for bulk in v('bulk_capacitance_corners_F', inputs):
        rows = load_release(bulk, inputs=inputs)
        key = f'bulk_{round(bulk * 1e6)}uF'
        results['load_release'][key] = {'worst_raw_peak_V': max(r['raw_peak_V'] for r in rows), 'rows': rows}
        results['startup_9V_5A'][key] = startup(bulk, v('startup_load_A', inputs), inputs=inputs)
        print(f"load release {key}: worst raw peak {results['load_release'][key]['worst_raw_peak_V']} V; "
              f"startup {results['startup_9V_5A'][key]}")
    if args.write:
        output = BASELINE_OUT if args.profile == 'baseline' else OUT
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(results, indent=1) + '\n')
        print(f'wrote {output.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
