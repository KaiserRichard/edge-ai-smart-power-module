#!/usr/bin/env python3
"""Conditional Gate3 architecture bounds; reads JSON only, never native CAD.

Targets are proposals, not guaranteed component/application ratings. Unknown
application maxima are always null. No manufacturer circuit is reproduced.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/r2/sheet03/gate3/OPTIONS_CALCULATIONS.json'

def energy(c,v):return .5*c*v*v

def current_energy_bound(e,l_min):
    if l_min<=0:raise ValueError('A positive differential-inductance floor is required')
    return math.sqrt(2*e/l_min)

def charge_peak(v,i,t,c,esr,ring):
    if c<=0:raise ValueError('A positive effective capacitance floor is required')
    return v+i*t/c+i*esr+ring

def two_cap_harness_peak(cmodule,cpi,vmodule,vpi,l,current):
    # Lossless post-isolation module C and Pi C connected through L.
    # Charge fixes common mode; magnetic+electric differential energy fixes swing.
    ceq=cmodule*cpi/(cmodule+cpi)
    vcommon=(cmodule*vmodule+cpi*vpi)/(cmodule+cpi)
    swing=math.sqrt((vmodule-vpi)**2+l*current**2/ceq)
    return vcommon+cmodule/(cmodule+cpi)*swing

def sharing_max(rmin,rmax):
    result=0
    for a,b,c,d in itertools.product((rmin,rmax),repeat=4):
        conductance=1/(a+b)+1/(c+d)
        for r,branch in ((a,a+b),(b,a+b),(c,c+d),(d,c+d)):
            result=max(result,r/(branch*branch)/conductance)
    return result

def calculate():
    baseline=json.loads((ROOT/'docs/evidence/r2/sheet03/CALCULATIONS.json').read_text())['gate_2c']
    trip=baseline['threshold'];buck=baseline['buck_static'];normal=baseline['margins']['false_trip']['normal_20us_V'];pi_old=4.75+baseline['margins']['harness']['conditional_reduced_V']
    # All allocations below are ASSUMED proposed qualification targets.
    a={'Cin_min_F':10e-6,'Cin_max_F':20e-6,'positive_source_charge_until_isolation_C':150e-6,
       'input_V_max':24.,'source_isolation_deadline_s':20e-6,'Ldiff_min_H':5.44e-6,'Ldiff_max_H':8.16e-6,
       'initial_inductor_A_max':6.1,'rounded_fault_current_A_max':60.,'Craw_min_F':.0024064,
       'Craw_bulk_max_F':.0054144,'Craw_ceramic_max_F':182.16e-6,'Cprotected_max_F':220e-6,
       'raw_ESR_max_ohm':.004,'crowbar_action_after_overdrive_s_max':1e-6,'series_isolation_s_max':2e-6,
       'raw_overdrive_V':.020*(1+11.3e3*1.002/(10e3*.998)),'ring_V_max':.020,
       'ballast_R_min_ohm':.032505,'ballast_R_max_ohm':.033495,'crowbar_Rtotal_max_ohm':.040095,
       'resistor_terminal_target_C_max':85.,'proposed_hot_single_pulse_J_per_resistor':.05}
    input_e=energy(a['Cin_max_F'],24.)+24.*a['positive_source_charge_until_isolation_C']
    li0=energy(a['Ldiff_max_H'],a['initial_inductor_A_max'])
    e_total=input_e+li0
    i_bound=current_energy_bound(e_total,a['Ldiff_min_H'])
    # While raw node is nonnegative, dI/dt <= Vin/Ldiff_min. Detector
    # threshold includes pre-crossing ESR; only subsequent ESR rise is added.
    di=24./a['Ldiff_min_H']*a['crowbar_action_after_overdrive_s_max']
    release_q=6.1*20e-6+.5*8.16e-6*6.1**2/buck['min_V']
    normal_a=buck['max_V']+.020+6.1*.004+release_q/a['Craw_min_F']
    normal_a_30=normal_a+6.1*10e-6/a['Craw_min_F']
    normal=normal_a  # D/E adopt A source contract and this more conservative normal screen.
    peak_a=trip['max_V']+a['raw_overdrive_V']+60*a['crowbar_action_after_overdrive_s_max']/a['Craw_min_F']+di*a['raw_ESR_max_ohm']+a['ring_V_max']
    peak_a_2us=trip['max_V']+a['raw_overdrive_V']+60*2e-6/a['Craw_min_F']+24/a['Ldiff_min_H']*2e-6*a['raw_ESR_max_ohm']+a['ring_V_max']
    out_e=energy(a['Craw_bulk_max_F']+a['Craw_ceramic_max_F']+a['Cprotected_max_F'],5.5)
    fault_e=out_e+e_total
    share=sharing_max(a['ballast_R_min_ohm'],a['ballast_R_max_ohm'])
    d={'incoming_A_max':60.,'Cprotected_min_F':1e-3,'Cprotected_max_F':1.5e-3,'protected_ESR_max_ohm':.0005,
       'clamp_low_V':5.34,'clamp_high_V':5.38,'effective_clamp_response_s_max':.5e-6,
       'series_current_isolation_s_max':2e-6,'local_ring_V_max':.020,
       'harness_L_max_H':2e-6,'harness_current_A_max':10.,'Pi_C_min_F':220e-6,'extra_Pi_ring_V':.010,
       'raw_dump_clamp_min_V':28.5,'raw_dump_clamp_max_V':31.5,'dump_hot_energy_target_J':.2}
    v_module=charge_peak(d['clamp_high_V'],60,.5e-6,1e-3,.0005,.020)
    # LTC4367 uses a nominal 0.5V OV threshold, not the retained 2.5V detector.
    ov_ratio=5.325/.5-1
    ltc4367_min=.5*.985*(1+ov_ratio*.998/1.002)
    ltc4367_max=.5*1.015*(1+ov_ratio*1.002/.998)
    pi_energy=math.sqrt(v_module*v_module+d['harness_L_max_H']*d['harness_current_A_max']**2/d['Pi_C_min_F'])+d['extra_Pi_ring_V']
    pi_small=math.sqrt(v_module*v_module+2e-6*5**2/2e-6)
    pi_required_c=2e-6*10**2/((5.5-.01)**2-v_module*v_module)
    e={'incoming_A_max':10.,'isolation_s_max':5e-6,'Pi_C_min_F':1e-3,'Pi_C_max_F':1.5e-3,
       'ESR_max_ohm':.005,'local_ring_V_max':.020,'clamp_low_V':5.30,'clamp_high_V':5.40,
       'total_clamp_overshoot_V_max':.020,'harness_L_max_H':10e-6,
       'hot_output_absorber_energy_target_J':.01,'upstream_dump_energy_target_J':.2,
       'normal_total_loop_R_max_ohm':.050,'10A_bound_includes_limiting_overshoot':True}
    v_e=charge_peak(trip['max_V'],10,5e-6,1e-3,.005,.020)
    v_e_220=charge_peak(trip['max_V'],10,5e-6,220e-6,.005,.020)
    v_e_fail=charge_peak(trip['max_V'],60,5e-6,1e-3,.005,.020)
    mid=6.12;cout=324.996e-6;pout=baseline['24V_vs_12V']['partial_loss_screens'][0]['output_V']*5
    eta1=.92;eta2=.95;p2=pout/eta2;pinput=p2/eta1
    return {'status':'ANALYSIS COMPLETE; ALL APPLICATION QUALIFICATION OPEN','baseline_commit':'0677fea',
      'classification':'CALCULATED conditional extrema within expressly ASSUMED target boxes; not application worst cases',
      'frozen_requirements':{'Vin_V':[9,24],'Pi_peak_V_strict_ceiling':5.5,'Pi_5A_V_floor':4.75,'GPIO_power':True},
      'baseline':{'buck_min_V':buck['min_V'],'buck_max_V':buck['max_V'],'normal_max_20us_V':baseline['margins']['false_trip']['normal_20us_V'],
        'trip_min_V':trip['min_V'],'trip_max_V':trip['max_V'],'Pi_reduced_path_min_V':pi_old,
        'normal_10mV_margin_V':trip['min_V']-baseline['margins']['false_trip']['normal_20us_V']-.010,'existing_application_worst_case_V':None},
      'A':{'ASSUMED_targets':a,'CALCULATED':{'input_energy_J':input_e,'initial_L_energy_J':li0,
        'positive_L_current_energy_bound_A':i_bound,'normal_release_screen_V':normal_a,'normal_false_trip_margin_V':trip['min_V']-normal_a-.010,'normal_30us_screen_V':normal_a_30,'normal_30us_margin_V':trip['min_V']-normal_a_30-.010,'on_interval_module_peak_screen_V':peak_a,'fault_margin_V':5.5-peak_a,
        'on_interval_module_peak_2us_action_V':peak_a_2us,'fault_margin_2us_V':5.5-peak_a_2us,
        'fully_on_crowbar_loadline_V_max':60*a['crowbar_Rtotal_max_ohm'],
        'all_stores_energy_ceiling_J':fault_e,'ballast_I2t_energy_upper_A2s':fault_e/a['ballast_R_min_ohm'],
        'single_resistor_fraction_max':share,'single_resistor_energy_upper_J':fault_e*share,
        'Cin14p076uF_initial_only_current_A':math.sqrt(6**2+14.076e-6*24**2/5.44e-6)},
        'application_VPi_peak_max_V':None,'guaranteed_application_action_time_min_max_s':[None,None]},
      'B':{'ASSUMED':{'fuse_clearing_integral_A2s':11.,'equal_ballast_ohm':.033,'eta_normal':.90,'output_fuse_cold_R_ohm':.009},
        'CALCULATED':{'input_9V_A':pout/(9*.9),'input_fuse_rating_at75pct_A':pout/(9*.9)/.75,
        'output_fuse_rating_at75pct_A':5/.75,'output_fuse_drop_V':5*.009,'Pi_with_extra_fuse_V':pi_old-5*.009,
        'Pi_margin_with_extra_fuse_V':pi_old-5*.009-4.75,'ballast_J_at11A2s':.033*11,
        'each_equal_ballast_J_at11A2s':.033*11/4,'SCR_cold_I2t_ratio_510_over_11':510/11,
        'constant100A_clearing_screen_s':11/100**2},'application_VPi_peak_max_V':None,
        'guaranteed_24VDC_total_clearing_s_max':None},
      'C':{'ASSUMED':{'mid_nom_V':6.,'mid_tolerance_fraction':.02,'local_C_max_F':60.996e-6,'all_mid_C_max_F':cout,
        'eta_first':eta1,'eta_final':eta2,'single_eta_comparison':.935},'CALCULATED':{'mid_V_range':[5.88,6.12],
        'local_input_energy_J':energy(60.996e-6,mid),'all_mid_input_energy_J':energy(cout,mid),
        'maintained_mid_DC_fault_margin_V':5.5-mid,'lossless_stiff_source_LC_screen_V':2*mid-buck['max_V'],
        'combined_eta':eta1*eta2,'output_W':pout,'first_stage_loss_W':pinput-p2,'final_stage_loss_W':p2-pout,
        'total_loss_W':pinput-pout,'single_loss_comparison_W':pout*(1/.935-1),
        'additional_loss_vs_single_W':pinput-pout-pout*(1/.935-1),'normal_input_A_at9V':pinput/9,
        'mid_for95pct_duty_nom_min_V':buck['max_V']/(.95*.99),'mid_nom_max_for5p5_V':5.5/1.01},
        'application_VPi_peak_max_V':None},
      'D':{'ASSUMED_targets':d,'CALCULATED':{'module_peak_screen_V':v_module,'module_margin_V':5.5-v_module,
        'LT4363_nominal_clamp_min_to_clear_normal_V':(normal+.010)*1.275/1.25,
        'LT4363_high_corner_at_that_nominal_V':(normal+.010)*1.30/1.25,
        'LTC4367_trip_range_before_other_errors_V':[ltc4367_min,ltc4367_max],
        'LTC4367_false_trip_margin_V':ltc4367_min-normal-.010,
        'source_raw_module_store_subtotal_excluding_Pi_J':fault_e-energy(a['Cprotected_max_F'],5.5)+energy(d['Cprotected_max_F'],5.5),
        'complete_all_store_energy_max_J':None,
        'restricted_L_only_Pi_peak_screen_V':pi_energy,'restricted_L_only_Pi_fault_margin_V':5.5-pi_energy,
        'Pi_2uF_5A_2uH_energy_screen_V':pi_small,'restricted_L_only_required_Pi_C_F':pi_required_c,'two_cap_counterexample_peak_V':two_cap_harness_peak(1.5e-3,1e-3,5.38,pi_old,2e-6,5),'two_cap_counterexample_margin_V':5.5-two_cap_harness_peak(1.5e-3,1e-3,5.38,pi_old,2e-6,5),
        'local_clamp_interval_energy_J':v_module*60*2e-6,'sustained_source_dump_multiplier_at_min_clamp':28.5/(28.5-24),
        'dump_L_only_plus_source_J':energy(8.16e-6,60)*28.5/(28.5-24),
        'raw_dump_max_voltage_vs35V_bulk_margin_V':35-31.5,'sustained_source_dump_decay_s':8.16e-6*60/(28.5-24)},'application_VPi_peak_max_V':None},
      'E':{'ASSUMED_targets':e,'CALCULATED':{'series_only_letthrough_peak_screen_V':v_e,'series_only_margin_V':5.5-v_e,
        'active_clamp_peak_target_V':5.40+.020,'active_clamp_margin_V':5.5-5.42,
        'active_clamp_false_fire_margin_V':5.30-normal-.010,'220uF_peak_screen_V':v_e_220,
        '220uF_margin_V':5.5-v_e_220,'60A_peak_screen_V':v_e_fail,'60A_margin_V':5.5-v_e_fail,
        'output_absorber_received_energy_J':5.42*10*5e-6+energy(10e-6,10),
        'Pi_5A_at50mohm_screen_V':buck['min_V']-.05*5,
        'Pi_5A_at50mohm_margin_V':buck['min_V']-.05*5-4.75},'application_VPi_peak_max_V':None},
      'supply_hold_up':{'ASSUMED':{'Vstart_min':10.5,'Vvalid_min':10.,'C_effective_min_F':10e-6,
        'control_A_max':.025,'aggregate_gate_charge_C_max':480e-9,'required_action_hold_s':150e-6},
        'CALCULATED':{'minimum_C_F':(.025*150e-6+480e-9)/.5,'hold_s_after_gate_charge':(10e-6*.5-480e-9)/.025},
        'actual_supply_validity':None}}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=calculate();rendered=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:OUT.write_text(rendered)
    print(rendered)
if __name__=='__main__':main()
