#!/usr/bin/env python3
"""Independent Gate2c analysis. Reads exported XML only; never opens KiCad files.

All finite electrical results are conditional calculations, not protection guarantees.
Unknown application maxima remain None. See the evidence document for source conditions.
Stdlib only. Run with --write to append gate_2c and replace its generated MD section.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/evidence/r2/sheet03'
XML = EVIDENCE / 'V1A_gate2.net.xml'
MARKER = '<!-- GATE2C GENERATED END -->'


def value(text):
    m = re.match(r'([\d.]+)\s*([numkM]?)', text)
    return float(m[1]) * {'': 1, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3,
                          'k': 1e3, 'M': 1e6}[m[2]]


def captured():
    return {c.get('ref'): {'classification': 'ASSUMED as-fitted nominal from captured XML; not measured',
                          'source': 'V1A_gate2.net.xml',
                          'text': c.findtext('value'), 'SI': value(c.findtext('value'))}
            for c in ET.parse(XML).findall('./components/comp')
            if c.get('ref').startswith(('R', 'C', 'L'))}


def divider(top, bottom, vmin, vmax, resistor_error, bias=0):
    """Independent extrema of V=Vthreshold*(1+Rt/Rb)+Ib*Rt."""
    v = [vt * (1 + top * (1 + st * resistor_error) /
                        (bottom * (1 + sb * resistor_error))) + ib * top * (1 + st * resistor_error)
         for vt, st, sb, ib in itertools.product((vmin, vmax), (-1, 1), (-1, 1), (-bias, bias))]
    return min(v), max(v)


def rail(top, bottom):
    # TPS7A16 overall accuracy +/-2%, IFB +/-100nA; assumed resistor total +/-0.2%.
    lo, hi = divider(top, bottom, 1.193 * .98, 1.193 * 1.02, .002, 100e-9)
    return {'nominal_V': 1.193 * (1 + top / bottom), 'min_V': lo, 'max_V': hi}


def rk4(y, dt, fun):
    a = fun(y)
    b = fun([v + dt * d / 2 for v, d in zip(y, a)])
    c = fun([v + dt * d / 2 for v, d in zip(y, b)])
    d = fun([v + dt * d for v, d in zip(y, c)])
    return [v + dt * (aa + 2 * bb + 2 * cc + dd) / 6
            for v, aa, bb, cc, dd in zip(y, a, b, c, d)]


def fault(vin, action, floor, trip, initial, cb_r=.040095, dt=1e-9,
          finite_input=False, efuse_off=1e-6, continued_limit=0, trace=False,
          efuse_origin='overdrive'):
    """Shorted buck high-side FET screen, no credit for its internal limit.

    y=(I_L,Vcer,Vbulk,Vinput,I2t,Eballast,Esupply).
    Ideal input until efuse_off AFTER comparator-overdrive crossing, then finite
    input C with optional explicitly assumed continued current. Input C includes
    two 22uF and two 100nF caps, upper initial/temp factor 1.2*1.15.
    No wiring inductance, source impedance, nonlinear switches or clamp dynamics.
    Abrupt differential-L floor is a sensitivity model, NOT Coilcraft evidence.
    """
    cc = 6 * 22e-6 * .8 * .85 * .9 * .9
    cb = 8 * 470e-6 * .8 * .8
    cin = (2 * 22e-6 + 2 * 100e-9) * 1.2 * 1.15
    ec, eb = .002, .0035  # ASSUMED ESR screens, not guaranteed minima/maxima.
    ballast = .033495
    y = [6., initial, initial, vin, 0., 0., 0.]
    t, trigger, peak, peak_i, peak_q = 0., None, initial, 6., 0.
    cb_time = off_time = supply_off_time = math.inf
    samples = []

    def node(state, conducting):
        i, vc, vb = state[:3]
        return (i + vc / ec + vb / eb) / (1 / ec + 1 / eb + (1 / cb_r if conducting else 0))

    # ASSUMED 20mV comparator overdrive, multiplied by maximum divider gain.
    target = trip + .020 * (1 + 11300 * 1.002 / (10000 * .998))
    while t < (trigger + 2e-6 if trigger is not None else 80e-6):
        conducting = t >= cb_time - 1e-16
        if finite_input and efuse_origin == 'hot_short_current' and y[0] >= 45 and supply_off_time == math.inf:
            supply_off_time = t + efuse_off
        supply_disconnected = finite_input and t >= supply_off_time - 1e-16
        u = node(y, conducting)
        if trigger is None and u >= target:
            trigger = t
            cb_time, off_time = t + action, t + 2e-6
            if finite_input and efuse_origin == 'overdrive':
                supply_off_time = t + efuse_off
        peak, peak_i = max(peak, u), max(peak_i, y[0])
        iq = u / cb_r if conducting else 0.
        peak_q = max(peak_q, iq)
        if trace and (not samples or t - samples[-1][0] >= 20e-9):
            samples.append([t, u, y[0], iq, y[3]])
        h = min(dt, cb_time - t if cb_time > t + 1e-16 else dt,
                off_time - t if off_time > t + 1e-16 else dt)
        if finite_input and t < supply_off_time - 1e-16:
            h = min(h, supply_off_time - t)
        if h < 1e-16:
            break

        def deriv(s):
            u = node(s, conducting)
            inductance = 6.8e-6 * .8 if s[0] <= 14 else floor
            current_cb = u / cb_r if conducting else 0.
            feed = continued_limit if supply_disconnected else s[0]
            return [(s[3] - u) / inductance, (u - s[1]) / ec / cc,
                    (u - s[2]) / eb / cb, (feed - s[0]) / cin,
                    current_cb ** 2, current_cb ** 2 * ballast, feed * s[3]]

        y = rk4(y, h, deriv)
        t += h
    # The pre-crowbar terminal is also the ideal Pi voltage. 20mV allowance is assumed.
    result = {'classification': 'CALCULATED conditional sensitivity; no optimized worst-case claim',
              'vin_V': vin, 'crowbar_action_s': action, 'L_floor_H': floor,
              'series_off_s_after_overdrive': 2e-6, 'finite_input': finite_input,
              'efuse_response_delay_s': efuse_off if finite_input else None,
              'efuse_delay_origin': efuse_origin if finite_input else None,
              'efuse_absolute_off_s': supply_off_time if finite_input and supply_off_time != math.inf else None,
              'continued_input_A': continued_limit if finite_input else None,
              'comparator_overdrive_crossing_s': trigger, 'Pi_peak_V': peak + .020,
              'fault_margin_V': 5.5 - peak - .020, 'inductor_peak_A': peak_i,
              'crowbar_peak_A': peak_q, 'crowbar_initial_I2t_A2s': y[4],
              'ballast_initial_total_J': y[5],
              'actual_application_worst_case': None,
              'limitations': 'No saturated-L guarantee, eFuse hot-short max, commutation/supply/capacitance/source bound.'}
    return (result, samples) if trace else result


def resistor_corner_power(v, rmin, rmax):
    # Drain-side branches (r1+r2)||(r3+r4); individual pulse maxima at independent corners.
    powers = []
    for r in itertools.product((rmin, rmax), repeat=4):
        powers.extend([v ** 2 * r[0] / (r[0] + r[1]) ** 2,
                       v ** 2 * r[1] / (r[0] + r[1]) ** 2,
                       v ** 2 * r[2] / (r[2] + r[3]) ** 2,
                       v ** 2 * r[3] / (r[2] + r[3]) ** 2])
    return max(powers)


def calculate():
    cap = captured()
    r = lambda key: cap[key]['SI']
    referr = .0005 + 3e-6 * 165 + 5e-6 * 2.5 + 50e-6 * .1 + .0002
    triplo, triphi = divider(r('R301'), r('R302'), 2.5 * (1 - referr) - .006,
                            2.5 * (1 + referr) + .006, .002, 85e-9)
    bucklo, buckhi = divider(r('R202'), r('R203'), .99, 1.01, .001, 10e-9)
    ovplo, ovphi = divider(r('R103'), r('R104'), 1.176, 1.224, .001, 150e-9)
    uvlor = divider(r('R101'), r('R102'), 1.176, 1.224, .001, 150e-9)
    uvlof = divider(r('R101'), r('R102'), 1.09, 1.15, .001, 150e-9)
    input_pgr = divider(r('R106'), r('R107'), 1.176, 1.224, .001, 150e-9)
    input_pgf = divider(r('R106'), r('R107'), 1.09, 1.15, .001, 150e-9)
    det, drv = rail(r('R312'), r('R313')), rail(r('R314'), r('R315'))
    bulkmin, bulkmax = 8 * r('C330') * .8 * .8, 8 * r('C330') * 1.2 * 1.2
    lmax = r('L201') * 1.2
    normal = lambda delay: buckhi + .020 + (6 * delay + .5 * 6 * lmax * 6 / bucklo) / bulkmin + 6 * .0035
    wire = (1 + .00393 * (60 - 20)) * 1.1
    trunk, branch = 6.5 / 304.8 * .15 * wire, 16.2 / 304.8 * .05 * wire
    shunt = .002 * 1.01 * (1 + 25e-6 * 75)
    original = shunt + .005 + .010 + 2 * trunk + .75 * branch + .02925 + .005 + .0136
    reduced = shunt + .002 + .00624 + trunk + (1 / 4 + 1 / 16) * branch + .0195 + .004875 + .002 + .0136
    gatecharge = lambda supply: 26e-9 / ((supply - 4.5) / (11 + r('R306') + 1.6))
    logic_ns = 55 + 4.6 + 6.1 + 4.6 + 26
    rmin, rmax = .033 * (1 - .01 - 50e-6 * 100), .033 * (1 + .01 + 50e-6 * 100)
    cases = [fault(v, a, l, triphi, bucklo) for v, a, l in
             ((30., .3e-6, .5e-6), (30., .4e-6, .5e-6), (24., .3e-6, .5e-6),
              (24., .4e-6, .5e-6), (24., .3e-6, .1e-6), (24., .4e-6, .1e-6))]
    finite = [fault(24., .3e-6, l, triphi, bucklo, finite_input=True, efuse_off=e,
                    continued_limit=f, efuse_origin=origin) for l, e, f, origin in
              ((.5e-6, 1e-6, 0, 'overdrive'), (.1e-6, 1e-6, 0, 'overdrive'),
               (.1e-6, 1e-6, 4.815 / .999, 'overdrive'), (.1e-6, 1.8e-6, 0, 'overdrive'),
               (.5e-6, 1e-6, 0, 'hot_short_current'), (.1e-6, 1e-6, 0, 'hot_short_current'))]
    pwm = []
    aux_loss = []
    # Exact 12V/24V comparison is a LOSS SCREEN; switching edge time is assumed.
    # Typical efficiency curves for captured 400kHz show 13.5V, not 12V.
    vout = 1 * (1 + r('R202') / r('R203'))
    for vin in (12., 24.):
        duty = vout / vin
        ripple = (vin - vout) * duty / (r('L201') * 400e3)
        irms2 = 5 ** 2 + ripple ** 2 / 12
        condtyp = irms2 * (.041 * duty + .021 * (1 - duty))
        condmax = irms2 * (.082 * duty + .045 * (1 - duty))
        switching = .5 * vin * 5 * 10e-9 * 400e3
        pwm.append({'classification': 'CALCULATED (typical only); assumed 10ns total switching edge',
                    'vin_V': vin, 'output_V': vout, 'output_A': 5., 'duty': duty,
                    'ripple_A_pp': ripple, 'switch_conduction_typ_W': condtyp,
                    'switch_conduction_max_screen_W': condmax,
                    'assumed_switching_W': switching,
                    'inductor_copper_25C_W': irms2 * .0145,
                    'IC_partial_loss_typ_W': condtyp + switching,
                    'actual_total_loss_W': None})
        # Illustrative 20mA auxiliary load split equally; assumed diode drop 0.5V.
        aux_loss.append({'classification': 'CALCULATED (typical only, ASSUMED 10mA per rail/0.5V diode)',
                         'vin_V': vin, 'detector_LDO_W': (vin - .5 - det['nominal_V']) * .01,
                         'driver_LDO_W': (vin - .5 - drv['nominal_V']) * .01,
                         'aux_bleed_W': (vin - .5) ** 2 / r('R323'),
                         'actual_thermal_max': None})
    pmax = resistor_corner_power(5.5, rmin, rmax)
    return {'classification': 'Independent CALCULATED conditional screens; actual worst case OPEN',
            'source_register': 'third_party/sheet03_gate2c_source_register.json',
            'source_conditions_and_assumptions': 'docs/evidence/r2/sheet03/GATE2C_REVIEW_CLOSURE.md',
            'equations_and_model': 'scripts/calculate_sheet03_gate2c.py',
            'verdict': 'BLOCKED', 'baseline': 'c47409fb2637c94ccaa685c3ac4cbbd10681d5a2',
            'netlist_sha256': hashlib.sha256(XML.read_bytes()).hexdigest(),
            'captured_values': cap,
            'threshold': {'classification': 'CALCULATED (worst-case within ASSUMED stack only)',
                          'formula': '(Vref +/- offset+hysteresis)*(1+Rt/Rb) +/- Ib*Rt',
                          'nominal_V': 2.5 * (1 + r('R301') / r('R302')),
                          'min_V': triplo, 'max_V': triphi, 'reference_fraction': referr,
                          'R303_bias_extra_V_screen': 5e-9 * r('R303') * (1 + r('R301') / r('R302')),
                          'actual_worst_case_V': None},
            'buck_static': {'classification': 'CALCULATED (typical only: IFB has no maximum)',
                            'min_V': bucklo, 'max_V': buckhi},
            'input': {'classification': 'CALCULATED (worst-case with ASSUMED +/-0.1% resistors, no drift)',
                      'OVP_nominal_V': 1.2 * (1 + r('R103') / r('R104')),
                      'OVP_min_V': ovplo, 'OVP_max_V': ovphi,
                      'UVLO_rising_nominal_V': 1.2 * (1 + r('R101') / r('R102')),
                      'UVLO_rising_V': uvlor, 'UVLO_falling_V': uvlof,
                      'UVLO_falling_nominal_V': 1.122 * (1 + r('R101') / r('R102')),
                      'input_PGOOD_rising_V': input_pgr, 'input_PGOOD_falling_V': input_pgf,
                      'ILIM_formula_nominal_A': 18 / (r('R105') / 1000),
                      'ILIM_min_A': 4.185 / 1.001, 'ILIM_max_A': 4.815 / .999,
                      '24V_tolerance_headroom_to_OVP_min_fraction': ovplo / 24 - 1,
                      'selected_converter': None, 'module_isolated': None,
                      'converter_fault_containment': 'OPEN: exact converter not supplied'},
            'supplies': {'classification': 'CALCULATED regulated screen; dropout/ramp validity OPEN',
                         'DET_5V': det, 'DRV_7V5': drv,
                         'PG_driver_floor_screen_V': .83 * drv['min_V'],
                         'PG_detector_floor_screen_V': .83 * det['min_V'],
                         'TPS3808_reference_reset_V': [2.33 * .985, 2.33 * 1.015],
                         'TPS3808_release_nominal_s': r('C314') * 1e9 / 175 + .0005,
                         'TPS3808_release_assumed_scaled_s': [r('C314') / 180e-9 * .62 * .8,
                                                            r('C314') / 180e-9 * 1.44 * 1.2]},
            'timing': {'classification': 'DATASHEET stage tests; APPLICATION MAXIMUM OPEN',
                       'TLV3201_fall_ns': [None, 45, 55],
                       'SN74LVC1G11_per_stage_ns': [1., None, 4.6],
                       'SN74LVC1G74_async_clear_ns': [1.6, None, 6.1],
                       'UCC27511_INplus_ns_4p5V': [4, 15, 26],
                       'UCC27511_INplus_ns_12V': [4, 13, 23],
                       'LTC7001_propagation_ns_10V': [None, 35, 70],
                       'TPS26630_SHDN_to_off_us': [.8, 1., 1.5],
                       'TPS26630_hot_short_us': [None, 1., None],
                       'TPS26630_soft_short_us': [2.2, 3.2, 4.5],
                       'TPS26630_limit_timeout_ms': [129, 162, 202],
                       'gate_to_4p5V_regulated_charge_screen_ns': gatecharge(drv['min_V']) * 1e9,
                       'complete_digital_plus_charge_regulated_screen_ns': logic_ns + gatecharge(drv['min_V']) * 1e9,
                       'complete_digital_plus_charge_PG_floor_screen_ns': logic_ns + gatecharge(.83 * drv['min_V']) * 1e9,
                       'actual_OV_onset_to_commutation_max_ns': None,
                       'actual_OV_onset_to_series_off_max_ns': None},
            'fault_conditional_cases': cases, 'finite_input_conditional_cases': finite,
            'energy': {'classification': 'CALCULATED within ASSUMED voltage/C/time/temperature envelope',
                       'resistor_initial_terminal_C_ASSUMED': 125,
                       'resistor_terminal_max_C_DATASHEET': 95,
                       'resistor_terminal_headroom_C_CALCULATED': 95 - 125,
                       'resistor_terminal_envelope_status': 'BLOCKING: inherited assumption exceeds datasheet maximum',
                       'L_initial_6A_nominal_J': .5 * r('L201') * 6 ** 2,
                       'L_11p5A_linear_max_J': .5 * lmax * 11.5 ** 2,
                       'L_14A_linear_nominal_J': .5 * r('L201') * 14 ** 2,
                       'actual_saturated_L_energy_J': None,
                       'input_cap_screen_max_F': (2 * r('C201') + r('C203') + r('C204')) * 1.2 * 1.15,
                       'input_cap_24V_screen_J': .5 * (2 * r('C201') + r('C203') + r('C204')) * 1.2 * 1.15 * 24 ** 2,
                       'bulk_min_screen_F': bulkmin, 'bulk_max_screen_F': bulkmax,
                       'raw_bulk_5p5V_max_screen_J': .5 * bulkmax * 5.5 ** 2,
                       'ballast_R_min_ohm': rmin, 'ballast_R_max_ohm': rmax,
                       'crowbar_ceiling_current_A': 5.5 / rmin,
                       'FET_loadline_peak_W': 5.5 ** 2 / (4 * rmin),
                       'downstream_220uF_energy_J': .5 * 220e-6 * 5.5 ** 2,
                       'downstream_I2t_upper_A2s': 220e-6 * 5.5 ** 2 / (2 * rmin),
                       'raw_bulk_I2t_upper_A2s': bulkmax * 5.5 ** 2 / (2 * rmin),
                       'per_resistor_100us_rectangle_J': pmax * 100e-6,
                       'per_resistor_peak_W': pmax,
                       'assumed_hot_resistor_100us_limit_J': 1000 * .45 * 100e-6,
                       'assumed_FET_100us_rise_K': 5.5 ** 2 / (4 * rmin) * .8 * .05,
                       'actual_SOA_pass': None, 'actual_resistor_pulse_pass': None},
            'margins': {
                'fault': {'classification': 'OPEN', 'claimed_V': .018388, 'worst_case_V': None,
                          'conditional_selected_V': cases[0]['fault_margin_V']},
                'harness': {'classification': 'OPEN', 'claimed_V': .011431, 'worst_case_V': None,
                            'reduced_R_ohm': reduced, 'original_R_ohm': original,
                            'conditional_reduced_V': bucklo - 5 * reduced - 4.75,
                            'conditional_original_V': bucklo - 5 * original - 4.75},
                'false_trip': {'classification': 'OPEN', 'claimed_V': .021954, 'worst_case_V': None,
                               'conditional_20us_V': triplo - normal(20e-6) - .010,
                               'conditional_30us_V': triplo - normal(30e-6) - .010,
                               'normal_20us_V': normal(20e-6),
                               'allowed_loop_delay_s': (triplo - normal(0) - .010) * bulkmin / 6}},
            '24V_vs_12V': {'classification': 'CALCULATED (typical only); APPLICATION THERMAL OPEN',
                          'captured_BIAS': 'GND; datasheet application curves use output bias; efficiency transfer OPEN',
                          'partial_loss_screens': pwm,
                          'auxiliary_loss_screens': aux_loss,
                          '24V_efficiency_graph_assumed_reading': [.935, .945],
                          '13p5V_efficiency_graph_assumed_reading': [.94, .95],
                          '12V_400kHz_efficiency': None,
                          '24V_total_buck_loss_screen_W': [vout * 5 * (1 / .945 - 1), vout * 5 * (1 / .935 - 1)],
                          'actual_24V_module_compatibility': None}}


def markdown(j):
    e, m, i, s = j['energy'], j['margins'], j['input'], j['supplies']
    lines = ['# Gate 2c — independent bounds override', '',
             '**BLOCKED — PRELIMINARY — NOT FOR FABRICATION.**', '',
             'This section supersedes positive-margin interpretations of the historical Gate2 screen below.',
             'Run `python3 -B scripts/calculate_sheet03_gate2c.py --write`. Only exported XML is read.',
             'Historical JSON members are retained; actual worst-case margins are `null` / **OPEN**.',
             'Sources, tolerance conditions, timelines and proposed changes: [review closure](GATE2C_REVIEW_CLOSURE.md).', '',
             'Finite entries below are **CALCULATED conditional screens**. Divider/resistor corners are extrema within explicitly **ASSUMED** tolerance stacks; fault curves are sensitivities, not optimized extrema.',
             'They do not establish the application worst case. Efficiency/loss screens are **CALCULATED (typical only)**.', '',
             '| Margin | Historical claimed CALCULATED screen | Independent conditional calculation | Application worst case |',
             '|---|---:|---:|---|',
             f"| Fault | {m['fault']['claimed_V']*1e3:.3f} mV | {m['fault']['conditional_selected_V']*1e3:.3f} mV, historical source/L/timing box | OPEN |",
             f"| Harness | {m['harness']['claimed_V']*1e3:.3f} mV | {m['harness']['conditional_reduced_V']*1e3:.3f} mV, reduced path | OPEN |",
             f"| False trip | {m['false_trip']['claimed_V']*1e3:.3f} mV | {m['false_trip']['conditional_20us_V']*1e3:.3f} mV, assumed response | OPEN |", '',
             f"**BLOCKING conditional counterexamples:** retained harness {m['harness']['conditional_original_V']*1e3:.3f} mV; assumed longer load release {m['false_trip']['conditional_30us_V']*1e3:.3f} mV. Also, the inherited ASSUMED resistor-terminal temperature exceeds the DATASHEET maximum by CALCULATED 30 K. These are premise conflicts, not measured device behavior.", '',
             '| Conditional shorted-high-side sensitivity — ASSUMED inputs | CALCULATED Pi peak | CALCULATED margin | CALCULATED L peak |',
             '|---|---:|---:|---:|']
    for f in j['fault_conditional_cases']:
        lines.append(f"| {f['vin_V']:g} V, {f['crowbar_action_s']*1e6:g} µs action, {f['L_floor_H']*1e6:g} µH floor | {f['Pi_peak_V']:.6f} V | {f['fault_margin_V']*1e3:.3f} mV | {f['inductor_peak_A']:.3f} A |")
    lines += ['', 'Negative cases are **BLOCKING** evidence against claiming the assumed floor/timing as a guaranteed bound.', '',
              '| CALCULATED input/supply screen | Result |', '|---|---|',
              f"| Input OVP, resistor initial tolerance only | {i['OVP_nominal_V']:.6f} V nominal; {i['OVP_min_V']:.6f}–{i['OVP_max_V']:.6f} V |",
              f"| Falling UVLO | {i['UVLO_falling_nominal_V']:.6f} V nominal; {i['UVLO_falling_V'][0]:.6f}–{i['UVLO_falling_V'][1]:.6f} V |",
              f"| eFuse ILIM | {i['ILIM_formula_nominal_A']:.6f} A formula nominal; {i['ILIM_min_A']:.6f}–{i['ILIM_max_A']:.6f} A |",
              f"| DET_5V regulated | {s['DET_5V']['min_V']:.6f}–{s['DET_5V']['max_V']:.6f} V |",
              f"| DRV_7V5 regulated / PG floor screen | {s['DRV_7V5']['min_V']:.6f}–{s['DRV_7V5']['max_V']:.6f} V / {s['PG_driver_floor_screen_V']:.6f} V |",
              f"| Supervisor release, nominal external capacitor | {s['TPS3808_release_nominal_s']:.6f} s typical equation; maximum application delay OPEN |", '',
              '| CALCULATED energy/pulse screen, ASSUMED ceiling and isolation | Result |', '|---|---:|',
              f"| Initial nominal inductor energy | {e['L_initial_6A_nominal_J']*1e6:.3f} µJ |",
              f"| Input capacitors at nominal rail, conditional upper C | {e['input_cap_24V_screen_J']*1e3:.3f} mJ |",
              f"| Raw bulk energy at assumed ceiling | {e['raw_bulk_5p5V_max_screen_J']*1e3:.3f} mJ |",
              f"| Downstream tail I²t ceiling | {e['downstream_I2t_upper_A2s']:.6f} A²s |",
              f"| Raw-bulk-only I²t ceiling, if still connected | {e['raw_bulk_I2t_upper_A2s']:.6f} A²s |",
              f"| Each ballast rectangle | {e['per_resistor_100us_rectangle_J']*1e3:.6f} mJ |", '',
              '**24 V rail:** nominal operation is plausible; exact converter tolerance/trim/OVP/isolation and fault containment remain OPEN pending its model. No fallback-module shortlist is justified yet.', '',
              MARKER, '', '## Historical Gate 2 screen — preserved, superseded', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    j = calculate()
    if args.write:
        path = EVIDENCE / 'CALCULATIONS.json'
        history = json.loads(path.read_text())
        history['gate_2c'] = j
        path.write_text(json.dumps(history, indent=2, allow_nan=False) + '\n')
        path = EVIDENCE / 'GATE2_CALCULATIONS.md'
        old = path.read_text()
        if MARKER in old:
            old = old.split(MARKER, 1)[1].split('## Historical Gate 2 screen — preserved, superseded', 1)[1].lstrip()
        path.write_text(markdown(j) + old)
    else:
        print(json.dumps(j, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
