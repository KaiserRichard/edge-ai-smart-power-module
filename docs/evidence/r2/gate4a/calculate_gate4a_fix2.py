"""Round-2 design screens. Assumed envelopes are not measured qualifications."""
import copy
import hashlib
import json
import math
from itertools import product
from pathlib import Path


def apply_fix2(data):
    source = Path(__file__).parent.parent / 'j502_selection/CALCULATIONS.json'
    raw = source.read_bytes()
    connector = json.loads(raw)
    items = copy.deepcopy(connector['options']['A_TE_Phoenix']['items'])
    pair = next(row for row in items if row['element'] == 'module_FET_pair_proposed')
    pair['send_mohm'] = 13.6  # Owner's BSC034 pair; retain the assumed hot multiplier.
    loop = sum(row['send_mohm'] + row['return_mohm'] for row in items)
    data['historical_round1_selected_path'] = copy.deepcopy(data['selected_path'])
    selected = data['selected_path']
    selected['itemised_rows'] = items
    selected['connector_commit'] = '41cb9e889418d50d2f5f24467e66ac7f15a90476'
    selected['connector_calculations_sha256'] = hashlib.sha256(raw).hexdigest()
    selected['J502_status'] = 'SELECTED solution A; hot assembly qualification T11/T16 NOT RUN'
    selected['source_min_assumed_V'] = connector['source_min_screen_V']
    for key, row in selected['results'].items():
        voltage = connector['source_min_screen_V'] - 5 * loop / 1000 - float(key)
        row.update(loop_mOhm=loop, loss_5A_V=5 * loop / 1000,
                   dissipation_5A_W=25 * loop / 1000,
                   Vfar_end_CALCULATED_V=voltage, margin_to4p75_V=voltage - 4.75,
                   conditional_meets=voltage >= 4.75)
    selected['at6Vgate_and_ASSUMED2x_hot'].update(
        loop_mOhm=loop + 6.8,
        Vfar_end_after20mV_V=connector['source_min_screen_V'] - 5*(loop+6.8)/1000 - .02)
    data['gate4a_fix']['historical_round1_harness'] = data['gate4a_fix'].pop('harness')
    data['gate4a_fix2'] = dict(
        classification='CALCULATED design screens; actual electrical bounds remain OPEN',
        harness=dict(wire='Belden8502 AWG20 branches; Belden8521 AWG16 trunks',
                     J502='Phoenix1776508/1777989; TE3-87456-6/87309-9 at dummy/Pi end',
                     current_loop_assumed_ohm=loop/1000,
                     max_positive_current_at_ratio1p05_A=5*1.05/2.05,
                     reserve_after20mV_and15mV_uncertainty_V=selected['results']['0.02']['margin_to4p75_V']-.015,
                     actual_hot_loop_ohm=None), auxiliary=auxiliary_charger(),
        converter=converter_completion(), coupled_energy=coupled_energy(data),
        bootstrap_load_test=bootstrap_load_test(), pg_input_bias=pg_input_bias(),
        fixture_discharge=fixture_discharge(data), power_device_screen=power_device_screen())


def power_device_screen():
    return dict(classification='Datasheet-conditioned screens; no hot SOA qualification',
                series_pair_R25_at10V_ohm=2*.0034,
                series_pair_R25_at6V_ohm=2*.0051,
                series_pair_Qg_table_C=2*41e-9,
                bootstrap_table_charge_droop_at0p5uF_V=2*41e-9/.5e-6,
                pass_fet_VDS_target_V=58.1, pass_fet_ID_target_A=.2,
                pass_fet_power_if_targets_met_W=58.1*.2,
                pass_fet_energy_at1p02ms_J=58.1*.2*1.02e-3,
                pass_fet_bulk_thermal_TJ_if_case85_C=85+58.1*.2*.53,
                actual_hot_SOA_margin=None, actual_branch_current_bound_A=None)


def fixture_discharge(data):
    # Proposed test limits. RC times assume a separated reservoir, no replenishment.
    specs = [
        ('VIN_PROTECTED', 1e4, 28.289211046948948, 30e-6),
        ('VOUT_5V1', 1e3, 6.9, 5.59656e-3),
        ('VOUT_PROTECTED', 1e3, 6.9, 2.7072e-3),
        ('FAR_5V', 1e3, 6.9, 2.64e-3),
        ('DRV_HOLD', 1e4, 12.311325, 600e-6),
        ('AUX_12V', 1e4, 12.311325, 26e-6),
        ('AUX_PREHOLD', 1e4, 12.311325, 1.2e-6),
        ('AUX_LIMITED', 47e3, 35., 10e-6),
        ('VIN_AUX', 47e3, 58.1, 2.4e-6),
        ('DET5', 1e4, 5.25, 10e-6),
        ('3V3_AUX', 1e4, 3.4, 10e-6),
        ('REF_2V5', 1e4, 2.525, 10e-6),
    ]
    rows = []
    for n, (node, r, v, c) in enumerate(specs, 1):
        rows.append(dict(ref=f'RFD{n:02d}', node=node, R_ohm=r,
                         V_ceiling_assumed_V=v, C_ceiling_assumed_F=c,
                         power_upper_screen_W=v*v/(r*.9975),
                         current_upper_screen_A=v/(r*.9975),
                         isolated_time_to0p3_screen_s=r*1.0025*c*math.log(v/.3)))
    # Downstream LDO/reference bleeds are conservatively counted one-for-one at hold.
    added_hold = sum(rows[i]['current_upper_screen_A'] for i in (4,9,10,11))
    all_added_hold = added_hold + pg_input_bias()['added_pulldown_current_at3p4V_A']
    # Far bleed is included in the specified terminal load; conservatively apply
    # both other output bleeds through the entire loop (overstates their path loss).
    extra_output = 2*5.5/(1e3*.9975)
    extra_drop = extra_output*data['selected_path']['results']['0']['loop_mOhm']/1000
    return dict(classification='Passive fixture selection; isolated RC screens, no abort or coupled-decay guarantee',
                rows=rows, fixture_resistor_ambient_ceiling_C=70.,
                review_power_ceiling_per_resistor_W=.125,
                hold_domain_added_current_screen_A=added_hold,
                prior40mA_plus_all_added_hold_current_A=.040+all_added_hold,
                prior40mA_plus_all_added_hold_time_screen_s=(300e-6*(11.121343-10.5)-2.036e-6)/(.040+all_added_hold),
                additional_output_path_drop_screen_V=extra_drop,
                fixture_normal_min_after20mV_screen_V=data['selected_path']['results']['0.02']['Vfar_end_CALCULATED_V']-extra_drop,
                actual_connected_decay_s=None, actual_all_stores_discharged=None)


def pg_input_bias():
    # DC table transfers and declared board/capacitance allocations only.
    rmin, rmax = 10e3*.9975, 10e3*1.0025
    leakage = (10+1+1)*1e-6  # LVC Ioff, AHCT II, board/probe allocation.
    high_current = 2*3.4/rmin
    return dict(classification='Fully-off DC screen; no brownout/transition guarantee',
                input_off_screen_V=leakage*rmax,
                margin_to_AHCT_VIL_screen_V=.8-leakage*rmax,
                added_pulldown_current_at3p4V_A=high_current,
                AHCT_two_device_delta_ICC_table_A=2*.0015,
                AHCT_two_device_ICC_table_A=2*10e-6,
                old_40mA_plus_new_pulldown_hold_s=(300e-6*(11.121343-10.5)-2.036e-6)/(.040+high_current),
                RC_example_C_assumed_F=30e-12,
                passive_2V_to0p8V_example_s=rmax*30e-12*math.log(2/.8),
                actual_off_voltage_V=None, actual_loss_to_safe_off_s=None)


def coupled_energy(data):
    """Screen either destination against the entire connected pool, no survival claim."""
    raw = data['raw_node']['total_raw_dump_pool_upper_J']
    protected = data['protected_node']['initial_protected_energy_upper_J']
    voltage = data['raw_node']['terminal_screen_CALCULATED_V']
    rerr = .0135
    shares = []
    resistances = []
    for signs in product((-1, 1), repeat=4):
        rs = [.033*(1+s*rerr) for s in signs]
        a,b = sum(rs[:2]),sum(rs[2:])
        conductance=1/a+1/b
        shares.append(rs[0]/a**2/conductance)
        resistances.append(1/conductance)
    raw_fraction=data['gate4a_fix']['raw_dump']['worst_corner_part_energy_fraction']
    scenarios=[]
    for dummy_cap in (.0022,.00264):
        pool=raw+protected+.5*dummy_cap*5.5**2
        scenarios.append(dict(dummy_effective_C_upper_assumed_F=dummy_cap,
                              pool_assumed_J=pool,
                              one_raw_resistor_energy_screen_J=raw_fraction*pool,
                              one_protected_resistor_energy_screen_J=max(shares)*pool))
    return dict(classification='Conditional all-bank allocation; fixture/cable/other stores still OPEN',
                raw_only_pool_J=raw, protected_initial_J=protected,
                protected_max_part_fraction=max(shares),
                protected_ballast_min_max_ohm=[min(resistances),max(resistances)],
                protected_current_at_terminal_screen_A=voltage/min(resistances),
                scenarios=scenarios, actual_total_energy_J=None,
                actual_energy_partition=None, actual_rating_margin=None)


def bootstrap_load_test():
    # Test limits only. They deliberately do not reuse the TS=20V pump guarantee.
    bleed=10/(2e6*.9975)
    return dict(classification='T04L low-energy load-line qualification targets; NOT measured',
                R305_bleed_at10V_screen_A=bleed,
                other_external_leakage_ceiling_target_A=5e-6,
                pump_at_actual_TS_required_min_A=bleed+5e-6,
                external_load_emulator_R_test_ohm=2e6,
                test_resistor_increment_at10V_screen_A=bleed,
                probe_loading_must_be_included=True,
                actual_hot_pump_current_A=None, actual_external_leakage_A=None)


def converter_completion():
    from calculate_gate4a import divider_screen
    # Leakage and effective-capacitance limits are qualification allocations.
    rt, rb, rfb, rff, cfb, cff = 383e3, 100e3, 15e3, 15e3, 1e-9, 33e-12
    rerr, cerr = .0025, .0518  # resistor 0.1%+60K*25ppm; C0G 5%+60K*30ppm
    z1 = 1/(2*math.pi*rfb*cfb)
    z2 = 1/(2*math.pi*(1e6+rff)*cff)
    pff = 1/(2*math.pi*rff*cff)
    def corners(nominal):
        return [nominal/((1+rerr)*(1+cerr)), nominal/((1-rerr)*(1-cerr))]
    return dict(
        classification='Circuit selection and conditional passive-network screens; no stability PASS',
        R345_ohm=rt, R346_ohm=rb,
        adverse_RUN_ENOUT_leakage_target_A=3e-6,
        old464k_RUN_rising_screen_V=divider_screen(1.16,1.26,464e3,rb,rerr,3e-6),
        RUN_rising_screen_V=divider_screen(1.16,1.26,rt,rb,rerr,3e-6),
        ENOUT_sink_upper_at35V_screen_A=35/(rt*(1-rerr))+1e-6,
        compensation=dict(R343_RFB_ohm=rfb, C356_CFB_F=cfb,
                          R344_RFF_ohm=rff, C357_CFF_F=cff,
                          zero1_nominal_Hz=z1, zero2_nominal_Hz=z2,
                          feedforward_pole_nominal_Hz=pff,
                          zero1_corner_Hz=corners(z1), zero2_corner_Hz=corners(z2),
                          feedforward_pole_corner_Hz=corners(pff),
                          actual_loop_phase_margin_deg=None),
        output_Ceff_target_F=[10e-6,26e-6],
        LC_resonance_sensitivity_Hz=[1/(2*math.pi*math.sqrt(5.64e-6*26e-6)),
                                     1/(2*math.pi*math.sqrt(3.76e-6*10e-6))],
        actual_RUN_release_V=None, actual_stability=None)


def auxiliary_charger():
    # Allocations to be independently measured in T07D, not fabricated guarantees.
    from calculate_gate4a import divider_screen
    cbank, slew, control = 600e-6, 10., .040
    output_current = cbank*slew + control
    vin, efficiency, vout = 7.5, .75, 12.311325
    return dict(
        charger_MPN='TPS259470LRPWR',
        Cdvd_nominal_F=1e-6, Cdvd_effective_floor_target_F=.5e-6,
        nominal_slew_from_TI_equation_V_per_s=2000/1e6*1000,
        conditional_current_over_C_slew_V_per_s=3.82e-6/.5e-6,
        qualified_slew_ceiling_target_V_per_s=slew,
        total_charged_C_ceiling_target_F=cbank,
        control_current_ceiling_target_A=control,
        capacitor_charge_current_ceiling_A=cbank*slew,
        total_output_current_screen_A=output_current,
        input_screen_assumptions=dict(Vaux_floor_V=vin,efficiency_floor=efficiency,
                                     converter_and_branch_overhead_A=.005,
                                     charger_IQ_max_at_test_condition_A=.000610),
        auxiliary_input_current_screen_A=vout*(output_current+.000610)/(vin*efficiency)+.005,
        stopper_test_condition_min_current_A=.045/(.33*1.01),
        charger_EN_rising_screen_V=divider_screen(1.183,1.223,365e3,48.7e3,.0025,.1e-6),
        charger_OV_rising_screen_V=divider_screen(1.183,1.223,365e3,33.2e3,.0025,.1e-6),
        charger_power_conservative_screen_W=vout*output_current,
        TJ_if_TA85_and_74p5CperW_screen_C=85+74.5*vout*output_current,
        # Existing illustrative LT4363 calculation incorrectly started TMR at zero.
        timer_nominal_OC_310uA_from0p5_s=10e-9*(1.375-.5)/310e-6,
        timer_testpoint_min_with_start0p5_s=10e-9*.95*(1.335-.5)/310e-6,
        timer_initial_voltage_actual_V=None,
        startup_actual_s=None, slew_actual_V_per_s=None,
        hold_actual_s=None, Q316_hot_SOA_qualification=None)


def render_fix2_md(data):
    path = data['selected_path']
    text = ('\n## Round 2 — completed connector handoff\n\n'
            'Solution A is imported unchanged from connector commit `41cb9e8`. '
            'The owner-selected BSC034 pair retains its **assumed** 13.6 mΩ hot allocation; '
            'the connector report\'s alternative 6 mΩ pair and architecture E are not adopted. '
            'Previous path rows are retained under `historical_round1_selected_path` in JSON. '
            'J502 selection is complete; contact derating, splices and actual mixed mate remain T11/T16.\n\n'
            f"Current loop screen: {path['results']['0']['loop_mOhm']:.9f} mΩ. "
            f"At 5 A with a 20 mV trough: {path['results']['0.02']['Vfar_end_CALCULATED_V']:.9f} V; "
            f"with 100 mV: {path['results']['0.1']['Vfar_end_CALCULATED_V']:.9f} V (FAIL screen). "
            'No hot assembly or Pi qualification is asserted.\n'
            '\n## Round 2 — controlled hold charging\n\n'
            'U327 TPS259470LRPWR follows D304 and drives DRV_HOLD. '
            'C374 1 µF / R374 100 Ω set a nominal 2 V/s ramp. '
            'T07D must demonstrate ≤10 V/s over all starts/restarts, '
            '≤600 µF charged capacitance, ≤40 mA controls, and valid component temperatures. '
            'These are qualification allocations, not guaranteed startup specifications.\n\n'
            f"Aux input screen: {data['gate4a_fix2']['auxiliary']['auxiliary_input_current_screen_A']*1000:.6f} mA "
            'at 7.5 V after branch loss and 75% efficiency, including 5 mA overhead; '
            'the transferred stopper floor is 135.014 mA at its datasheet test condition. '
            'The actual 9 V transfer and the converter\'s own local-capacitor startup remain T07A/C. '
            'U327 worst flat power sensitivity is 0.566321 W; with 85°C ambient and '
            '74.5°C/W it gives 127.191°C, above the 125°C operating ceiling. '
            'Therefore the added charger requires local ambient ≤70°C for the initial coupon '
            '(112.191°C sensitivity), plus measured junction/board correlation; no hot PASS is inferred.\n\n'
            'LT4363 TMR starts around 0.5 V in regulated operation: '
            '`tOC=C*(Voff−Vstart)/ITMR`. At 10 nF, 1.375 V and 310 µA, '
            'this is 28.226 µs, not the historical 43.065 µs zero-start screen. '
            'Initial timer voltage and stress-dependent charging are measured in T07; '
            'the old calculation remains explicitly historical.\n'
            '\n## Round 2 — U317 RUN and compensation completion\n\n'
            'F2-05 assigns the VC–FB and output–FB compensation branches. '
            'R345 changes from 464 kΩ to 383 kΩ because the old divider fails '
            'the declared 7.5 V low-line allocation with 3 µA adverse leakage.\n\n'
            f"Old/new conditional RUN rising ranges: {data['gate4a_fix2']['converter']['old464k_RUN_rising_screen_V']} / "
            f"{data['gate4a_fix2']['converter']['RUN_rising_screen_V']} V. "
            'The 3 µA leakage ceiling must be qualified in T07E. '
            'Selected passive-network zeros are 10.610330 / 4.751603 kHz and '
            'the feedforward pole is 321.525138 kHz. These are network frequencies, '
            'not loop crossover or stability margins. Actual margins remain OPEN.\n'
            '\n## Round 2 — coupled-bank energy and bootstrap measurements\n\n'
            'F2-06 screens either dump against all initially connected output banks plus Enew. '
            f"For effective dummy C≤2.2 mF, the conditional pool is {data['gate4a_fix2']['coupled_energy']['scenarios'][0]['pool_assumed_J']*1e3:.6f} mJ; "
            f"one raw resistor receives at most {data['gate4a_fix2']['coupled_energy']['scenarios'][0]['one_raw_resistor_energy_screen_J']*1e3:.6f} mJ "
            f"and one protected resistor {data['gate4a_fix2']['coupled_energy']['scenarios'][0]['one_protected_resistor_energy_screen_J']*1e3:.6f} mJ "
            'inside the fixed topology/tolerance model. These are separate worst allocations; '
            'do not add them as simultaneous dissipated energies. Missing fixture/cable stores and '
            'actual partition/SOA remain OPEN. A nominal 2.2 mF dummy at +20% raises the pool to '
            f"{data['gate4a_fix2']['coupled_energy']['scenarios'][1]['pool_assumed_J']*1e3:.6f} mJ.\n\n"
            'F2-10 adds 10 kOhm pulldowns at both AHCT inputs. The fully-off DC screen is '
            f"{data['gate4a_fix2']['pg_input_bias']['input_off_screen_V']:.6f} V; the extra load is "
            f"{data['gate4a_fix2']['pg_input_bias']['added_pulldown_current_at3p4V_A']*1e3:.6f} mA. "
            'This does not bound intermediate-rail behavior or input transition time. '
            'Both AHCT parts also require the existing TTL-high delta-ICC load in the 40 mA ledger.\n\n'
            'T04L requires actual-TS pump margin after R305 plus all external leakage and probe load. '
            'The non-bleed 5 µA qualification allocation needs ≥10.012531 µA pump capability '
            'at 10 V, in the actual circuit; the TS=20 V table point is not substituted.\n')
    text += ('\n## Round 2 — passive fixture discharge adapters\n\n'
             'F2-11/SFX-01 selects independent bleeders; resistor local ambient is limited to 70 C '
             'and review power to 0.125 W per 1206 part. These are external fixture limits. '
             'Rows assume separated capacitances and zero replenishment. Connected decay remains OPEN.\n\n'
             '|Ref / node|R (ohm)|V screen|C ceiling (uF)|P upper (mW)|Isolated time to 0.3 V (s)|\n'
             '|---|---:|---:|---:|---:|---:|\n')
    for r in data['gate4a_fix2']['fixture_discharge']['rows']:
        text += (f"|{r['ref']} / {r['node']}|{r['R_ohm']:.0f}|{r['V_ceiling_assumed_V']:.6f}|"
                 f"{r['C_ceiling_assumed_F']*1e6:.3f}|{r['power_upper_screen_W']*1e3:.6f}|"
                 f"{r['isolated_time_to0p3_screen_s']:.6f}|\n")
    text += ('\nAdded held-domain current (DRV_HOLD and downstream LDO/reference bleeds): '
             f"{data['gate4a_fix2']['fixture_discharge']['hold_domain_added_current_screen_A']*1e3:.6f} mA. "
             'Include it in the total control allocation; do not extend the old hold result unchanged. '
             'Converter-input/prehold bleeds are additional upstream loads. '
             'A far-end bleed returns only to FAR_GND and creates no local-ground bypass.\n')
    f = data['gate4a_fix2']['fixture_discharge']
    text += (f"\nIf all prior loads already use 40 mA, the PG and held-domain bleeds raise it to "
             f"{f['prior40mA_plus_all_added_hold_current_A']*1e3:.6f} mA; the illustrative hold time falls to "
             f"{f['prior40mA_plus_all_added_hold_time_screen_s']*1e3:.6f} ms. "
             'This fails the existing total-current allocation; it must not be treated as an increased allowance. '
             'For normal-load bookkeeping, conservatively applying the two additional output bleeds '
             'at 5.5 V through the entire selected loop gives an extra '
             f"{f['additional_output_path_drop_screen_V']*1e3:.6f} mV drop and "
             f"{f['fixture_normal_min_after20mV_screen_V']:.9f} V far-end sensitivity after the 20 mV trough. "
             'The far bleed is already included in the 5 A terminal load. Actual regulation/thermal margins remain OPEN.\n')
    text += ('\n## Round 2 — manufacturer-conditioned power-device screens\n\n'
             'F2-12 reconfirms the BSC034 pair: 6.8 mOhm at 10 V gate, '
             '10.2 mOhm at 6 V gate at the 25 C table points; 82 nC pair gate charge '
             'at the specified test point gives 0.164 V on a 0.5 uF effective bootstrap. '
             'No hot or actual gate-charge transfer is guaranteed by these values.\n\n'
             'Q316 at separately qualified VDS<=58.1 V and ID<=0.20 A gives '
             '11.62 W, 11.8524 mJ for 1.02 ms, and 91.1586 C bulk-junction sensitivity '
             'using fixed case85 C and 0.53 C/W. This is not a hot linear-SOA approval. '
             'Local input reservoirs can violate the branch-current target despite a 0.20 A source setting.\n')
    return text
