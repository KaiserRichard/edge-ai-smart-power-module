"""Independent Gate4a-FIX screens. No electrical validation or missing-bound defaults."""
from itertools import product
import math

def charge_uncertainty(abs_current_integral, duration, endpoint_current=10., ut=25e-9):
    """Conditional calibration ceilings; integrate the entire event, including its tail."""
    return .01*abs_current_integral + .010*duration + 2*endpoint_current*ut + .05e-6

def energy_error_without_skew(abs_power_integral, abs_current_integral, abs_voltage_integral,
                              duration, vmax=6.9, imax=100., ut=25e-9):
    """Amplitude, record-endpoint and numerical terms only; not a complete UE."""
    gv, gi, bv, bi = .0008, .01, .0106, .010
    return ((gv+gi+gv*gi)*abs_power_integral
            +(1+gi)*bv*abs_current_integral
            +(1+gv)*bi*abs_voltage_integral + bv*bi*duration
            +2*vmax*imax*ut + .0001)


def skew_total_variation_bound(vmax, relative_skew_s, current_total_variation_A):
    """Bound shift error using continuous-trace variation on the guarded record.

    Sampled variation alone need not bound the physical waveform. Calibration,
    bandwidth and interpolation evidence must supply that transfer before use.
    """
    terms = (vmax, relative_skew_s, current_total_variation_A)
    if any(not math.isfinite(x) or x < 0 for x in terms):
        raise ValueError('Skew-bound inputs must be finite and nonnegative')
    return vmax * relative_skew_s * current_total_variation_A


def energy_uncertainty(abs_power_integral, abs_current_integral, abs_voltage_integral,
                       duration, vmax=6.9, imax=100., ut=25e-9, *, u_skew=None):
    """Full conditional UE. Missing relative-skew evidence remains OPEN.

    Integral arguments must bound their values across all allowed relative shifts.
    u_skew includes the waveform-shift supremum and its reconstruction error.
    Endpoint uncertainty ut is separate; it cannot replace relative deskew.
    """
    if u_skew is None:
        return None
    if not math.isfinite(u_skew) or u_skew < 0:
        raise ValueError('u_skew must be a finite nonnegative bound')
    return energy_error_without_skew(abs_power_integral, abs_current_integral,
                                    abs_voltage_integral, duration, vmax, imax, ut) + u_skew

def loaded_divider(rt, rb, rs, rp, ron=0.0, sense=2.5, ileak=0.0):
    # KCL: leakage is conservatively lumped at the comparator pin, after rs.
    ip = sense / rp + ileak
    div = sense + (rs + ron) * ip
    return div * (1 + rt / rb) + rt * ip

def ov_latency_screen(trip):
    """Stiff source counterexample only; no claimed autonomous source response."""
    rows=[]
    for vin in (9.,24.,26.,27.):
        c=2.4064e-3; ind=10e-6; w=1/math.sqrt(ind*c); v0=5.0983606557377055
        def voltage(t):
            return vin+(v0-vin)*math.cos(w*t)+8/(c*w)*math.sin(w*t)
        lo,hi=0.,math.pi/w
        for _ in range(80):
            mid=(lo+hi)/2
            if voltage(mid)<trip:lo=mid
            else:hi=mid
        rows.append(dict(Vin_V=vin,trip_V=trip,conditional_latency_s=(lo+hi)/2,
                         raw_at10us_V=voltage(10e-6),actual_response_s=None))
    return rows

def supervisor(rt):
    f=.0025; rb=10000.; ib=25e-9
    return [.405*.98*(1+rt*(1-f)/(rb*(1+f)))-ib*rt*(1+f),
            .405*1.02*(1+rt*(1+f)/(rb*(1-f)))+ib*rt*(1+f)]

def raw_dump_network(vraw=6.881668479208298, energy=.09986508302957717):
    """Two six-resistor strings. Independent tolerance/TCR corners, no pulse rating inferred."""
    fraction=.01+50e-6*70  # 25->95 C terminal screen, not a junction model
    reqs=[]; shares=[]; powers=[]
    for signs in product((-1,1), repeat=12):
        r=[.033*(1+x*fraction) for x in signs]
        a,b=sum(r[:6]),sum(r[6:]); conductance=1/a+1/b
        reqs.append(1/conductance)
        shares.append(r[0]/a**2/conductance)
        powers.append(vraw**2*r[0]/a**2)
    cmax=5.59656e-3
    return dict(R_nom_ohm=.099,part_MPN='WFMB2512R0330FEA',part_count=12,
                branches=[['R380','R381','R382','R383','R386','R387'],
                          ['R388','R389','R390','R391','R392','R393']],
                R_initial_min_max_ohm=[.099*.99,.099*1.01],
                R_hot_screen_min_max_ohm=[min(reqs),max(reqs)],
                resistor_tolerance_plus_TCR_fraction=fraction,
                I5p5_nom_A=5.5/.099,I6p881668_at_Rmin_A=vraw/min(reqs),
                Cmax_conditional_F=cmax,RC_max_initial_s=cmax*.099*1.01,
                RC_hot_screen_max_s=cmax*max(reqs),
                ideal_decay_to0p3V_s=cmax*max(reqs)*math.log(vraw/.3),
                raw_pool_conditional_J=energy,equal_share_resistor_energy_J=energy/12,
                worst_corner_part_energy_fraction=max(shares),
                worst_corner_resistor_energy_J=energy*max(shares),
                worst_corner_resistor_initial_power_W=max(powers),
                remaining_cap_energy_at0p3V_J=.5*cmax*.3**2,
                clamp_MPN='STPS60H100CT',actual_hot_pulse_rating_J=None,
                actual_negative_excursion_V=None)

def calculate_fix():
    f=.0025
    reference_fraction=.0012125  # inherited conservative screen, incl. assumed age/noise
    # Table Vos maximum + assumed hysteresis allowance + transferred PSRR/CMRR screen.
    extra=5e-9*1000*1.0025+.004+.002+.25*10**(-65/20)+.125*10**(-60/20)
    ilo=1.125e-6  # 120nA switch +5nA comparator +1uA unqualified diode/PCB allocation
    corners=[]; gains=[]
    for signs in product((-1,1),repeat=4):
        rt,rb,rs,rp=[r*(1+s*f) for r,s in zip((9880.,1e4,1e3,1e5),signs)]
        for ron in (0.,17.):
            gains.append(loaded_divider(rt,rb,rs,rp,ron,sense=1.))
            for s,i in product((-1,1),repeat=2):
                v=2.5*(1+s*reference_fraction)+s*extra
                corners.append(loaded_divider(rt,rb,rs,rp,ron,v,i*ilo))
    return dict(
      classification='CALCULATED conditional screens/acceptance allocations; no bench results; verdict BLOCKED',
      resistor=dict(R103_58p1V_power_W=58.1**2/(348e3*(1-f)),R340_power_W=12.311325**2/(1e6*(1-f)),R367_historical1M_power_W=2.5**2/(1e6*(1-f)),tnpw0805_general85C_derated_W=.14*(125-85)/(125-70)),
      bootstrap=dict(old220k_load_10V_A=10/220e3,new2M_10V_max_A=10/(2e6*(1-f)),new2M_14V_max_A=14/(2e6*(1-f)),new2M_power14V_W=14**2/(2e6*(1-f)),table15uA_remaining_at10V_A=15e-6-10/(2e6*(1-f)),table_test_TS_V=20,applicable_pump_min_at_TS5V_A=None,Cboot_effective_target_F=.5e-6,event_Qg_table_C=82e-9,event_droop_V=82e-9/.5e-6,passive_equivalent_tau_s=2e6*(1+f)*82e-9/10,passive_equivalent_10to1V_s=2e6*(1+f)*82e-9/10*math.log(10),actual_loaded_VGS_min_V=None),
      detector=dict(old_loaded_1M_trip_corrected_V=loaded_divider(11300,10000,1000,1e6),old_loaded_20mV_increment_V=.02*loaded_divider(11300,10000,1000,1e6,sense=1),new_nominal_zero_Ron_trip_V=loaded_divider(9880,10000,1000,100000),new_nominal_17ohm_trip_V=loaded_divider(9880,10000,1000,100000,17),new_nominal_17ohm_overdrive_increment_V=.02*loaded_divider(9880,10000,1000,100000,17,sense=1),ASSUMED=dict(resistor_total_fraction=f,reference_total_fraction=reference_fraction,hysteresis_allowance_V=.002,aggregate_leakage_bound_A=ilo,rail_window_V=[4.75,5.25],temperature_screen_C=[25,85]),conditional_trip_min_max_V=[min(corners),max(corners)],conditional_20mV_overdrive_raw_upper_V=max(corners)+.02*max(gains),actual_trip_min_max_V=[None,None],fully_off_3uA_100k_max_V=3e-6*100e3*(1+f),powered_isolation_38uA_100k_estimate_V=38e-6*100e3*(1+f),reference_series_R_nom_ohm=1000.,reference_2p525V_injection_ceiling_A=2.525/(1000*(1-f)),reference_bias_extra_V=5e-9*1000*(1+f),reference_C_nom_F=4.7e-6,reference_C_effective_required_F=[1e-6,50e-6],R303_6p9V_current_ceiling_A=6.9/(1000*(1-f)),clamp_bias_low_A=(10.5-2.525)/(68100*(1+f)),clamp_bias_high_A=(12.312-2.475)/(68100*(1-f))),
      auxiliary=dict(new_driver_supervisor_min_max_V=supervisor(249e3),new_detector_supervisor_min_max_V=supervisor(100e3),new_detector_supervisor_rise_upper_V=1.03*supervisor(100e3)[1],old110k_detector_rise_upper_V=1.03*supervisor(110e3)[1],driver_supervisor_rise_upper_V=1.03*supervisor(249e3)[1],startup_9ms_typical_only_peak_input_A=(528e-6*12**2/.009+.48)/(.8*9),startup_9ms_typical_only_average_input_A=(.5*528e-6*12**2/.009+.48)/(.8*9),nominal_hold_upper_initial_energy_J=.5*440e-6*1.2*12**2,illustrative_charge_time_at_100mA_input_s=(.5*440e-6*12**2)/(.8*9*.1-.48),timer_C_only_min_max_s=[10e-9*.95*1.335/310e-6,10e-9*1.05*1.335/310e-6],actual_startup_min_max_s=[None,None],actual_hold_min_s=None),
      source=dict(nominal_4p02k_current_A=18/4.02,nominal_charge_if10us_C=(18/4.02)*10e-6,remaining_time_after_TPS_max_s=10e-6-1.5e-6,current_trigger_0to10A_at9V_12uH_s=12e-6*10/(9-5.1),OV_only_current_nominal_latency=ov_latency_screen(loaded_divider(9880,10000,1000,100000)),autonomous_trigger=None,upstream_module='Isolated48to24V; exact identity/source envelope OPEN'),
      raw_dump=raw_dump_network(),
      receiving_bank=dict(current_limit_inverted_screen_at3p5mOhm_A=.1/(.0035+.5e-6/.0012032),current_limit_inverted_screen_at7mOhm_A=.1/(.007+.5e-6/.0012032),actual_arriving_current_bound_A=None,actual_far_peak_V=None),
      harness=dict(wire='Belden8503',DCR_nominal_ohm_per_m=16.2/304.8,fanout_send_hot_assumed_ohm=(16.2/304.8)*.015/2*1.1*(1+.00393*40),fanout_return_hot_assumed_ohm=(16.2/304.8)*.035/8*1.1*(1+.00393*40),loop_without_J502_allocation_ohm=.042672940994094496-.00624,J502='PENDING feat/v1a-j502-connector',actual_hot_loop_ohm=None),
      fixture=dict(illustrative_handover_s=5e-6,raw_drop_at5A_V=5*5e-6/.0024064,actual_abort_ceiling_s=None,actual_source_energy_bound_J=None),
      measurement=dict(classification='Qualification ceilings, NOT measured uncertainties',voltage_error_allocations_V=dict(gain=.0008*5.5,offset=.003,common_mode=.002,noise_repeatability=.003,bandwidth_sampling_loading=.0026),U_voltage_target_V=.015,U_time_target_s=25e-9,source_off_current_band_A=.010,endpoint_additive_current_error_target_A=.002,endpoint_measured_limit_A=(.010-.002)/1.01,source_nominal_SW_timeout_plus_TPS_s=9e-6+1.5e-6,U_charge_example_C=charge_uncertainty(100e-6,10e-6),U_charge_2ms_example_C=charge_uncertainty(100e-6,.002),U_energy_example_J=energy_uncertainty(.1,.2,.0138,.002),U_energy_without_skew_example_J=energy_error_without_skew(.1,.2,.0138,.002),U_skew_actual_J=None,energy_additive_voltage_error_V=.0106,measured_peak_ceiling_if15mV_V=5.5-.015,measured_min_floor_if15mV_V=4.75+.015,calibration_records=None),
      aux_surge_fixture=dict(voltage_ceiling_V=58.1,pulse_plateau_s=.001,rise_fall_s=10e-6,source_current_target_A=.2,extra_source_cap_target_F=1e-6,source_work_screen_J=58.1*.2*.00102+.5*1e-6*58.1**2,actual_fixture_bound_J=None))

def render_fix_md(d):
    import json
    f=d['gate4a_fix']
    out='\n## Gate4a-FIX current screens\n\nThe sections above preserve the original energy/path screens, with the detector arithmetic corrected. Current circuit deltas, assumptions and remaining blockers are in [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md). Round-2 J502 solution A supersedes the historical harness; see the current selected-path table and round-2 section. This section is generated by [calculate_gate4a_fix.py](calculate_gate4a_fix.py). A numeric target is not a measurement.\n\n|Item|Calculated value / status|\n|---|---|\n'
    vals=[('R103 conservative58.1V power,0805',f['resistor']['R103_58p1V_power_W']),('R3052M bleed at10V maximum,A',f['bootstrap']['new2M_10V_max_A']),('C3010.5µF/82nC event droop,V',f['bootstrap']['event_droop_V']),('Old loaded1M trip corrected,V',f['detector']['old_loaded_1M_trip_corrected_V']),('Old20mV raw increment,V',f['detector']['old_loaded_20mV_increment_V']),('Current OV-only latency at9/24/26/27V,s',[r['conditional_latency_s'] for r in f['source']['OV_only_current_nominal_latency']]),('New ideal trip,V',f['detector']['new_nominal_zero_Ron_trip_V']),('New conditional trip min/max,V',f['detector']['conditional_trip_min_max_V']),('New conditional20mV-overdrive upper,V',f['detector']['conditional_20mV_overdrive_raw_upper_V']),('New supervisor held rail min/max,V',f['auxiliary']['new_driver_supervisor_min_max_V']),('New supervisorDET5 falling min/max,V',f['auxiliary']['new_detector_supervisor_min_max_V']),('New supervisorDET5 rising upper,V',f['auxiliary']['new_detector_supervisor_rise_upper_V']),('Hold charging end-of-ramp input sensitivity,A',f['auxiliary']['startup_9ms_typical_only_peak_input_A']),('Raw99mΩ conditional peak current,A',f['raw_dump']['I6p881668_at_Rmin_A']),('Raw worst resistor energy,J',f['raw_dump']['worst_corner_resistor_energy_J']),('Raw ideal discharge to0.3V,s',f['raw_dump']['ideal_decay_to0p3V_s']),('Conditional protected current allowance3.5/7mΩ,A',[f['receiving_bank']['current_limit_inverted_screen_at3p5mOhm_A'],f['receiving_bank']['current_limit_inverted_screen_at7mOhm_A']]),('Measurement target Upeak/Umin,V',.015),('Source-off measured current ceiling with1%+2mA error,A',f['measurement']['endpoint_measured_limit_A']),('Charge example uncertainty,C',f['measurement']['U_charge_example_C']),('Whole2ms charge example uncertainty,C',f['measurement']['U_charge_2ms_example_C']),('Energy partial error WITHOUT relative skew,J',f['measurement']['U_energy_without_skew_example_J']),('Complete energy uncertainty (OPEN without measured skew),J',f['measurement']['U_energy_example_J']),('Aux-only pulse source energy screen,J',f['aux_surge_fixture']['source_work_screen_J'])]
    for k,v in vals:out+=f'|{k}|{json.dumps(v)}|\n'
    out+='\nDetector equation: `Ip=Vs/R367+Ileak; Vdiv=Vs+(R303+Ron)Ip; Vraw=Vdiv(1+R301/R302)+R301Ip`. Corners enumerate four independently±0.25% resistors, Ron0…17Ω, inherited reference error0.12125%, comparator offset±4mV, **assumed** hysteresis±2mV, transferred PSRR/CMRR, additional R373 input-bias error±5.0125µV, and **assumed**1µA diode/PCB leakage plus125nA switch/comparator allowance. This conditional bound is not a guaranteed5.38V overdrive PASS; the missing hysteresis/dynamic/leakage transfer is T06.\n\nRaw decay is ideal RC with maximum conditional bank and independent initial/tolerance plus TCR resistor corners; FET resistance, continued source current, harness coupling and hot resistance change the measured time. Timing minima/maxima, actual source bound, loadedVGS, clamp/negative peaks and calibration remain JSONnull. No computed conditional number fills them.\n'
    return out
