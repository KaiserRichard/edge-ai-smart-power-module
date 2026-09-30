#!/usr/bin/env python3
"""V1A TVS/fuse documentary calculations; no KiCad file access.

Writes only the new TVS_CALCULATIONS.json beside this script.
--check compares the saved deterministic record without writing.
Finite results are conditional on labelled assumptions, not hardware validation.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def divider(vin, rt, rb):
    # Initial +/-0.1% and TPS2663 +/-150 nA; drift/MPNs OPEN.
    values = []
    for et, eb, ileak in itertools.product((-.001,.001),(-.001,.001),(-150e-9,150e-9)):
        top, bottom = rt*(1+et), rb*(1+eb)
        vp = (vin/top-ileak)/(1/top+1/bottom)
        values.append((vp,vin-vp,(vin-vp)**2/top,vp**2/bottom))
    return dict(pin_max_V=max(v[0] for v in values),top_max_V=max(v[1] for v in values),
                top_max_W=max(v[2] for v in values),bottom_max_W=max(v[3] for v in values))


def build():
    captured=json.loads((ROOT/'docs/evidence/r2/sheet03/CALCULATIONS.json').read_text())['gate_2c']
    ovp=captured['input']['OVP_min_V']
    assert math.isclose(ovp,26.973872559387452,abs_tol=1e-12)
    modules=[
        dict(MPN='RSD-100C-24',OVP_trigger_max_V=32.4,complete_fault_peak_V=None,ripple_pp_V=.150,
             dc_fraction_screen=.02+.0003*25,temperature_screen='0..50 C only; outside OPEN',
             output_A=4.2,power_nom_W=100.8,standard_downward_trim=False),
        dict(MPN='RSD-200C-24',OVP_trigger_max_V=32.4,complete_fault_peak_V=None,ripple_pp_V=.150,
             dc_fraction_screen=.02+.0003*25,temperature_screen='0..50 C only; outside OPEN',
             output_A=8.4,power_nom_W=201.6,standard_downward_trim=False),
        dict(MPN='TEP 150-4815WI',OVP_trigger_max_V=33.6,complete_fault_peak_V=None,ripple_pp_V=.200,
             dc_fraction_screen=.01+.002+.004+.0002*45,temperature_screen='ASSUMED -20..60 C',
             output_A=6.3,power_nom_W=151.2,standard_downward_trim=False),
        dict(MPN='TEP 200-7215UIR',OVP_trigger_max_V=31.2,complete_fault_peak_V=None,ripple_pp_V=.200,
             dc_fraction_screen=.01+.002+.001+.0002*45,temperature_screen='ASSUMED -20..60 C',
             output_A=8.4,power_nom_W=201.6,standard_downward_trim=True),
    ]
    tvs=[]
    # Littelfuse exact electrical rows at25 C; Vishay comparison kept distinct.
    electrical=[(30,33.3,36.8,48.4,12.4,31.0,12.4,31.0),
                (33,36.7,40.6,53.3,11.3,28.2,11.3,28.1),
                (36,40.0,44.2,58.1,10.4,25.9,10.3,25.8)]
    for wm,brmin,brmax,vc,ismb,ismc,vsmb,vsmc in electrical:
        for family,ip,vip,power in [('SMBJ',ismb,vsmb,600),('SMCJ',ismc,vsmc,1500)]:
            tvs.append(dict(MPN=f'{family}{wm}CA',manufacturer='Littelfuse',bidirectional=True,
                classification='Manufacturer table at25 C; application transfer ASSUMED',
                VRWM_V=wm,VBR_min_V=brmin,VBR_max_V=brmax,VBR_test_A=.001,
                VC_max_V=vc,IPP_A=ip,Vishay_comparison_IPP_A=vip,
                leakage_max_at_VRWM_A=1e-6,peak_pulse_power_W=power,
                waveform='10/1000 us, nonrepetitive, specified mounting/temperature',
                clamp_margin_to_67V_V=67-vc,
                standoff_margin_to_module_OVP_trigger_max_V={m['MPN']:wm-m['OVP_trigger_max_V'] for m in modules},
                additional_overshoot_after_assumed_1V_margin_V={m['MPN']:wm-m['OVP_trigger_max_V']-1 for m in modules},
                actual_hot_VC_max_V=None,actual_hot_leakage_max_A=None))
    selected=next(t for t in tvs if t['MPN']=='SMCJ36CA')
    # ASSUMED TVS-current waveform; half-current at1 ms after pulse start.
    peak, rise, half_time, ceiling = 5.,10e-6,.001,60.
    tau=(half_time-rise)/math.log(2)
    q=peak*(rise/2+tau)
    i2t=peak**2*(rise/3+tau/2)
    pulse=dict(classification='CALCULATED within ASSUMED 5 A TVS current waveform, not a source guarantee',
        peak_A=peak,rise_s=rise,half_time_from_start_s=half_time,exponential_tau_s=tau,
        integrated_charge_C=q,integrated_I2t_A2s=i2t,
        energy_at_58p1V_J=q*58.1,energy_at_60V_J=q*ceiling,
        assumed_energy_envelope_J=.45,node_peak_acceptance_V=ceiling,
        assumed_initial_Tj_C=85,assumed_linear_pulse_power_derating=(150-85)/(150-25),
        SMCJ_derated_power_screen_W=1500*(150-85)/(150-25),
        SMBJ_derated_power_screen_W=600*(150-85)/(150-25),
        peak_power_at_node_ceiling_W=peak*ceiling,
        actual_hot_energy_rating_J=None,actual_source_fault_energy_J=None)
    assert pulse['energy_at_60V_J']<pulse['assumed_energy_envelope_J']
    assert pulse['peak_power_at_node_ceiling_W']<pulse['SMCJ_derated_power_screen_W']
    # Counterexample only: VBR temp coefficient is not a guaranteed VC coefficient.
    hot_sensitivity=58.1*(1+.001*(85-25))+2
    fuse_rows=[]
    for mpn,rated,breaking,i2t_typ,drop in [
        ('3403.0281.23',5,1500,100,115),('3403.0283.23',8,1500,95,79),
        ('3403.0284.23',10,1500,180,73),('3403.0285.23',12.5,1000,340,63)]:
        # ASSUMED rounded-down graph factors, manufacturer general70% continuous use.
        hold60=rated*.70*.80
        hold85=rated*.70*.70
        fuse_rows.append(dict(MPN=mpn,family='Schurter UMT-H',rated_A=rated,
            rated_DC_V=125,DC_breaking_A=breaking,typical_melting_I2t_at_10x_A2s=i2t_typ,
            typical_drop_at_rated_current_mV=drop,
            conservative_hold_screen_60C_A=hold60,conservative_hold_screen_85C_A=hold85,
            meets_assumed_5A_at_85C=hold85>=5,actual_hot_hold_A=None,
            max_total_DC_clearing_I2t_A2s=None,
            assumed_60C_graph_factor=.80,assumed_85C_graph_factor=.70,
            continuous_utilisation=.70))
    selected_fuse=next(f for f in fuse_rows if f['MPN']=='3403.0285.23')
    assert selected_fuse['rated_DC_V']>=67.2
    assert selected_fuse['meets_assumed_5A_at_85C']
    stress=[]
    detmin=captured['supplies']['DET_5V']['min_V']
    drvmin=captured['supplies']['DRV_7V5']['min_V']
    for v in [24.,33.6,35.,36.,58.1,60.,67.2]:
        stress.append(dict(node_V=v,classification='CALCULATED voltage-only and assumed10 mA/LDO screen; diode drop not credited',
            efuse_abs_margin_V=67-v,efuse_operating_margin_V=60-v,
            C101_C102_100V_margin_V=100-v,Q101_VDS_100V_screen_margin_V=100-v,
            LDO_input_abs_margin_V=62-v,LDO_EN_recommended_margin_V=40-v,
            C307_50V_margin_V=50-v,R323_10k_1pct_max_W=v*v/(10000*.99),
            detector_LDO_10mA_W=(v-detmin)*.010,driver_LDO_10mA_W=(v-drvmin)*.010,
            UVLO=divider(v,332000,54900),OVP=divider(v,348000,15800)))
    normal=[]
    for m in modules:
        v=24+24*m['dc_fraction_screen']+m['ripple_pp_V']+.150
        normal.append(dict(MPN=m['MPN'],classification='CALCULATED with ASSUMED150 mV step; ripple typical-only for TEP200',
            temperature_screen=m['temperature_screen'],dc_allowance_V=24*m['dc_fraction_screen'],
            full_pp_ripple_positive_allowance_V=m['ripple_pp_V'],assumed_healthy_startup_or_load_step_V=.150,
            normal_peak_screen_V=v,headroom_to_user_26p97_V=26.97-v,
            nuisance_margin_after_assumed_1V_V=26.97-v-1,
            excess_above_frozen_24V_V=v-24,actual_normal_peak_V=None))
    trim=dict(classification='CALCULATED enquiries; complete bounds OPEN',
        proposed_23V_3pct_plus_100mV_ripple_150mV_step_V=23*1.03+.100+.150,
        same_with_full_200mV_ripple_V=23*1.03+.200+.150,
        setpoint_ceiling_with_3pct_200mV_ripple_150mV_step_V=(24-.2-.15)/1.03,
        TEP200_23V_nominal24_referenced_2p2pct_200mV_ripple_150mV_step_V=23+24*.022+.200+.150,
        TEP200_23V_usable_power_before_derating_W=23*8.4)
    capacities={str(other):(25.5/.9+other)*1.25 for other in [0,50,100]}
    scores=[]
    for m in modules:
        known_mismatches=[]
        if not m['standard_downward_trim']:
            known_mismatches.append('Standard fixed/upward-only setting fails frozen24 V normal-peak ceiling')
        if m['MPN'].startswith('RSD-'):
            known_mismatches.append('67.2 V/1 s primary surge specification fails proposed100 V/1 s without qualified PDB suppression')
        if m['MPN']=='RSD-100C-24':
            known_mismatches.append('Hypothetical23 V capacity96.6 W fails +50 W scenario97.916667 W before hot derating')
        if m['MPN']=='TEP 150-4815WI':
            known_mismatches.append('Nominal151.2 W fails +100 W scenario160.416667 W before hot derating')
        scores.append(dict(MPN=m['MPN'],new_TVS_standoff_screen='CONDITIONAL voltage screen',
            OVP_trigger_max_V=m['OVP_trigger_max_V'],standard_downward_trim=m['standard_downward_trim'],
            allowance_after_36V_catalogue_minus_1V_margin_V=36-m['OVP_trigger_max_V']-1,
            allowance_after_35V_proposed_board_target_minus_1V_margin_V=35-m['OVP_trigger_max_V']-1,
            actual_module_fault_peak_V=None,actual_board_continuous_withstand_V=None,
            capacity_at_hypothetical_23V_W=23*m['output_A'],
            known_interface_mismatches=known_mismatches,
            standalone_recommendation='NONE: full normal/fault/thermal/interface bounds OPEN'))
    return dict(classification='CALCULATED within labelled ASSUMED screens; electrical qualification BLOCKED',
        base_commit='50c94e05a4896b6d95ec13019e4c722a6ae2c1bf',
        frozen_normal_input_V=[9,24],frozen_Pi_load_A=5,frozen_Pi_peak_strictly_below_V=5.5,
        initial_only_efuse_OVP_min_V=ovp,normal_nuisance_comparison_V=26.97,
        assumed_standoff_margin_V=1,assumed_nuisance_margin_V=1,
        user_comparison_figures_are_complete_peaks_only_if_guaranteed=True,
        TVS_candidates=tvs,selected_D101='Littelfuse SMCJ36CA',
        proposed_continuous_board_fault_target_V=35,catalogue_standoff_V=36,
        proven_V1A_continuous_withstand_V=None,pulse_envelope=pulse,
        hot_clamp_sensitivity=dict(classification='ASSUMED sensitivity only, not manufacturer hot VC maximum',
            VBR_coefficient_misapplied_to_VC_per_K=.001,temperature_C=85,layout_overshoot_V=2,
            illustrative_node_V=hot_sensitivity,actual_hot_node_peak_V=None),
        component_stress=stress,F101_candidates=fuse_rows,selected_F101='Schurter 3403.0285.23',
        assumed_F101_local_max_C=85,required_source_DC_interrupt_envelope_V=67.2,
        actual_prospective_short_current_A=None,actual_circuit_L_over_R_s=None,
        normal_module_budgets=normal,trim_screens=trim,module_rescores=scores,
        assumed_power_capacity_targets_W=capacities,recommended_standalone_module=None,
        next_enquiry_candidate='TEP 200-7215UIR',
        verdict='NEW D101 SMCJ36CA, F101 3403.0285.23, V1A WITHSTANDS OPEN V continuous, RECOMMENDED MODULE NONE')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data=build()
    encoded=json.dumps(data,indent=2,allow_nan=False)+'\n'
    output=HERE/'TVS_CALCULATIONS.json'
    if args.check:
        if output.read_text()!=encoded:
            raise SystemExit('FAIL: saved calculation record differs from recomputation')
        print('PASS: deterministic TVS/fuse/normal-operation calculations')
    else:
        if output.exists() and not output.name.startswith('TVS_'):
            raise SystemExit('Refusing to overwrite a baseline calculation')
        output.write_text(encoded)
        print('Wrote',output.relative_to(ROOT))
    print(data['verdict'])
    print('Pulse screen:',data['pulse_envelope']['energy_at_60V_J'],'J; hot hold screen:',
          data['F101_candidates'][-1]['conservative_hold_screen_85C_A'],'A')


if __name__=='__main__':
    main()
