#!/usr/bin/env python3
"""Candidate-C feasibility screen, NOT a validated buck/device simulation.

All units are SI. --write updates only the selected gate member of the existing
CALCULATIONS.json; --gate 1d preserves historical gate_1b/gate_1c results.
Source identifiers and limitations are in the decision file. A sensitivity
calculation is never promoted to a datasheet guarantee by this program.
Uses RK4 for a stiff-voltage-source fault feeding L and two C/ESR branches.
No credit for input eFuse action, source resistance, or load current.
"""
import argparse
import itertools
import json
import math
import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs/evidence/r2/sheet03/CALCULATIONS.json"

# DATASHEET components combined with explicitly ASSUMED design requirements.
P = {
    "v_source_V": 30.0,  # ASSUMED abnormal-interface ceiling, NOT TPS OVP clamp
    "v_start_V": 5.038271401729418,
    "v_dc_max_V": 5.158632237795172,
    "ripple_positive_V": 0.020,  # ASSUMED acceptance limit
    "normal_margin_V": 0.010,  # ASSUMED review allocation, supersedes 50 mV
    "normal_initial_current_A": 6.0,  # 5 A plus ripple allowance
    "normal_loop_reaction_s": 20e-6,  # ASSUMED; eight 400-kHz periods
    "normal_L_max_H": 6.8e-6 * 1.2,
    "fault_L_low_current_H": 6.8e-6 * 0.8,
    "fault_knee_A": 14.0,  # typical 30%-drop point, NOT guaranteed knee
    "fault_L_floor_H": 0.5e-6,  # ASSUMED sensitivity corner; not vendor guarantee
    "ceramic_C_min_F": 60e-6,  # ASSUMED DC/temperature effective minimum
    "ceramic_ESR_ohm": 0.002,  # ASSUMED bank/connection screen
    "bulk_unit_nominal_F": 470e-6,
    "bulk_initial_factor": 0.8,  # DATASHEET initial tolerance
    "bulk_endurance_factor": 0.8,  # DATASHEET change relative to initial
    "bulk_unit_ESR_ohm": 0.028,  # DATASHEET cold/after-endurance test point
    "bulk_count": 8,  # design exploration, NOT approved capacitor population
    "post_isolation_allowance_V": 0.020,  # ASSUMED Pi-local ESL/harness bound
    "detector_overdrive_V": 0.020,  # TLV3201 55 ns test condition
    "isolation_requirement_s": 2e-6,  # ASSUMED sense-lag + logic + switch budget
    "dt_s": 0.5e-9,
}


def threshold(rt=11300.0, rb=10000.0, tighter_ref=False):
    # REF5025 high-grade: 500 ppm initial, 3 ppm/K box over 165 K,
    # 5 ppm/V line over 2.5 V, 50 ppm/mA for <=0.1 mA load.
    # Extra 200 ppm is an ASSUMED combined aging/noise/thermal-cycle allocation.
    ref_error = (0.0005 + 3e-6 * 165 + 5e-6 * 2.5 + 50e-6 * 0.1 + 0.0002)
    if tighter_ref:
        ref_error = 0.0005  # sensitivity only, no substituted part claimed
    # Procurement requirement: 0.1%, <=10 ppm/K; maximum |T-25|=100 K.
    r_error = 0.001 + 10e-6 * 100
    # TLV3201 full-temperature offset 4 mV; internal hysteresis has no max.
    # Reserve an extra +/-2 mV for it (ASSUMED acceptance requirement).
    input_error = 0.004 + 0.002
    # Comparator bias 5 nA and BAS116 clamp reverse leakage 80 nA.
    bias = 85e-9
    values = []
    for a, b, c, d, e in itertools.product((-1, 1), repeat=5):
        rtop, rbottom = rt * (1 + a*r_error), rb * (1 + b*r_error)
        vref = 2.5 * (1 + c*ref_error)
        values.append((vref + d*input_error) * (1 + rtop/rbottom) + e*bias*rtop)
    return {"nominal_V": 2.5*(1+rt/rb), "min_V": min(values),
            "max_V": max(values), "divider_gain_max": 1+rt*(1+r_error)/(rb*(1-r_error)),
            "reference_fraction_bound": ref_error, "resistor_fraction_bound": r_error,
            "comparator_offset_plus_hysteresis_V": input_error,
            "clamp_plus_input_bias_A": bias, "corner_count": len(values)}


def cap_values(n):
    return (n * P["bulk_unit_nominal_F"] * P["bulk_initial_factor"] * P["bulk_endurance_factor"],
            P["bulk_unit_ESR_ohm"]/n)


def normal_bound(n, loop_s=None):
    """Conservative charge+ESR bound: full I for t_loop, then triangular decay.

    The bank charging above its initial voltage is <=Q/Cbulk. Terminal voltage
    is <= bulk capacitor voltage + Ipeak*Rbulk; ceramic can only help here.
    Assumes no further buck pulses after t_loop. This is a required measured
    behavior, not an inferred guaranteed LM61460 loop response.
    """
    c, r = cap_values(n)
    i = P["normal_initial_current_A"]
    t = P["normal_loop_reaction_s"] if loop_s is None else loop_s
    tail = P["normal_L_max_H"]*i/P["v_start_V"]
    q = i*t + 0.5*i*tail
    dynamic = q/c + i*r
    return {"C_bulk_min_F": c, "ESR_bulk_ohm": r, "excess_charge_C": q,
            "decay_time_s": tail, "release_bound_V": dynamic,
            "normal_max_V": P["v_dc_max_V"]+P["ripple_positive_V"]+dynamic}


def fault(n, trip, delay, floor=None, source=None, dt=None, piecewise=True,
          input_cap=None, input_current=0.0, ceramic_C=None, include_state=False):
    """RK4 until effective isolation. Comparator overdrive is paid before delay.

    Once ideal isolation occurs raw energy stays upstream. Report an assumed
    extra 20 mV on the downstream rail; no credit for switch/harness drop.
    This deliberately ideal switch cannot establish real MOSFET SOA.
    """
    cb, rb = cap_values(n)
    cc = P["ceramic_C_min_F"] if ceramic_C is None else ceramic_C
    rc = P["ceramic_ESR_ohm"]
    floor = P["fault_L_floor_H"] if floor is None else floor
    source = P["v_source_V"] if source is None else source
    dt = P["dt_s"] if dt is None else dt
    gain = trip["divider_gain_max"]
    v_detect = trip["max_V"] + P["detector_overdrive_V"]*gain
    state = (P["normal_initial_current_A"], P["v_start_V"], P["v_start_V"], source)
    g = 1/rc + 1/rb

    def voltage(y):
        return (y[0] + y[1]/rc + y[2]/rb)/g

    def rhs(y):
        i, vc, vb, vin = y
        v = voltage(y)
        ell = P["fault_L_low_current_H"] if piecewise and i < P["fault_knee_A"] else floor
        return ((vin-v)/ell, (v-vc)/(rc*cc), (v-vb)/(rb*cb),
                0.0 if input_cap is None else (input_current-i)/input_cap)

    def add(y, k, scale):
        return tuple(a+scale*b for a, b in zip(y, k))

    detected = None
    vpeak = voltage(state)
    t = 0.0
    while t < 200e-6:
        v = voltage(state)
        if detected is None and v >= v_detect:
            detected = t
            i_detect = state[0]
            v_detect_actual = v
        if detected is not None and t >= detected+delay:
            break
        k1 = rhs(state)
        k2 = rhs(add(state, k1, dt/2))
        k3 = rhs(add(state, k2, dt/2))
        k4 = rhs(add(state, k3, dt))
        state = tuple(y+dt*(a+2*b+2*c+d)/6 for y,a,b,c,d in zip(state,k1,k2,k3,k4))
        t += dt
        vpeak = max(vpeak, voltage(state))
    if detected is None:
        raise RuntimeError("Fault did not reach detection threshold within screen")
    peak = vpeak+P["post_isolation_allowance_V"]
    result = {"bulk_count": n, "source_V": source, "L_floor_H": floor,
            "input_cap_F": input_cap, "input_feed_A": input_current,
            "vin_at_isolation_V": state[3],
            "piecewise_L": piecewise, "delay_s": delay, "time_to_detect_s": detected,
            "current_at_detect_A": i_detect, "current_at_isolate_A": state[0],
            "detect_voltage_V": v_detect_actual, "raw_peak_at_isolation_V": vpeak,
            "let_through_including_overdrive_and_local_V": peak-trip["max_V"],
            "pi_peak_screen_V": peak, "fault_margin_mV": 1000*(5.5-peak),
            "passes_fault_inequality": peak < 5.5}
    if include_state:
        result["state_at_action"] = dict(zip(("inductor_A", "ceramic_V", "bulk_V", "input_V"), state))
    return result


def calculate():
    tr = threshold()
    base = fault(P["bulk_count"], tr, P["isolation_requirement_s"])
    normal = normal_bound(P["bulk_count"])
    normal["false_trip_margin_mV"] = 1000*(tr["min_V"]-normal["normal_max_V"]-P["normal_margin_V"])
    sweep = []
    for n, delay in itertools.product((2,4,8,16,32), (0.2e-6,0.5e-6,1e-6,2e-6,6e-6)):
        row = fault(n, tr, delay)
        row["false_trip_margin_mV"] = 1000*(tr["min_V"]-normal_bound(n)["normal_max_V"]-P["normal_margin_V"])
        sweep.append(row)
    source_corners = [fault(8,tr,2e-6,floor=l,source=v) for l,v in
                      itertools.product((0.25e-6,0.5e-6,1e-6,3.808e-6), (24.0,28.3,30.0))]
    lo,hi = 0.0,5e-6
    for _ in range(32):
        mid=(lo+hi)/2
        if fault(8,tr,mid)["passes_fault_inequality"]: lo=mid
        else: hi=mid
    ovp = []
    for a,b,c,d in itertools.product((-1,1),repeat=4):
        rt,rb=348000*(1+a*.001),15800*(1+b*.001)
        ovp.append(1.2*(1+c*.02)*(1+rt/rb)+d*150e-9*rt)
    levers = {"tighter_reference_only":fault(8,threshold(tighter_ref=True),2e-6),
              "lower_nominal_5p25":fault(8,threshold(rt=11000),2e-6)}
    levers["lower_nominal_5p25"]["false_trip_margin_mV"] = 1000*(threshold(rt=11000)["min_V"]-normal["normal_max_V"]-P["normal_margin_V"])
    # Ideal ground shunt: switching peak only, not an SCR/FET+fuse qualification.
    crowbar=[fault(8,tr,t) for t in (0.2e-6,0.5e-6,2e-6)]
    finite_input=[fault(8,tr,2e-6,source=v,input_cap=c,input_current=i)
                  for v,c,i in itertools.product((24.0,28.3,30.0),
                       (19.448e-6,52.8e-6),(0.0,4.82))]
    return {"verdict":"BLOCKED", "blocker_id":"B1_FAULT_INTERRUPTION_ENVELOPE",
        "classification":"CALCULATED conditional screens; no SPICE or bench validation",
        "inputs":P,"threshold":tr,"normal":normal,"candidate_C":base,
        "input_ovp_V":{"nominal":1.2*(1+348000/15800),"min":min(ovp),"max":max(ovp)},
        "delay_ceiling_s_strict":lo,"capacitance_and_delay_sweep":sweep,
        "source_and_saturation_sweep":source_corners,"levers":levers,
        "finite_input_cap_sensitivity":finite_input,
        "ideal_crowbar_switching_screens":crowbar,
        "fet_5A":{"pair_25C_Rmax_ohm":.0068,"pair_25C_loss_W":25*.0068,
            "assumed_hot_multiplier":2,"assumed_hot_loss_W":25*.0068*2},
        "integration_check":{"half_step":fault(8,tr,2e-6,dt=P['dt_s']/2)}}


def raw_corners(nominal):
    """Same signed 10-nA FB allowance as PR6; typical, NOT a guaranteed limit."""
    return {
        "nominal_V": nominal,
        "min_V": .99*(1+(nominal-1)*.999/1.001)-10e-9*100000*1.001,
        "max_V": 1.01*(1+(nominal-1)*1.001/.999)+10e-9*100000*1.001,
    }


def shunt_interval(initial, rq, cc, duration=1.8e-6, dt=.5e-9):
    """Conditional interval from ideal crowbar ON to ideal series OFF.

    Holds the input at 30V and L at the explicitly UNQUALIFIED 0.5uH floor;
    does not credit eFuse shutdown. No load C/ESL, nonlinear FET or Qg model.
    A finite resistance does not instantaneously force the raw rail to ground.
    """
    cb, rb = cap_values(8)
    rc = P["ceramic_ESR_ohm"]
    y = (initial["inductor_A"], initial["ceramic_V"], initial["bulk_V"])
    g = 1/rc+1/rb+1/rq

    def v(s):
        return (s[0]+s[1]/rc+s[2]/rb)/g

    def rhs(s):
        raw = v(s)
        return ((30-raw)/.5e-6, (raw-s[1])/(rc*cc), (raw-s[2])/(rb*cb))

    def add(s, k, scale):
        return tuple(a+scale*b for a,b in zip(s,k))

    peak_v, peak_i, integral = v(y), v(y)/rq, 0.0
    for _ in range(round(duration/dt)):
        old_i = v(y)/rq
        k1 = rhs(y)
        k2 = rhs(add(y,k1,dt/2))
        k3 = rhs(add(y,k2,dt/2))
        k4 = rhs(add(y,k3,dt))
        y = tuple(a+dt*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4))
        raw = v(y)
        peak_v, peak_i = max(peak_v,raw), max(peak_i,raw/rq)
        integral += .5*dt*(old_i**2+(raw/rq)**2)
    return {"duration_s":duration,"raw_peak_after_on_V":peak_v,
            "crowbar_peak_A":peak_i,"crowbar_interval_I2t_A2s":integral,
            "inductor_at_series_off_A":y[0]}


def calculate_gate1c():
    """Design rejection and conditional co-design, not a hardware qualification.

    Reuses Gate 1b's threshold, normal-release and RK4 functions unchanged at
    their defaults. Unsupported maxima are null, never a fabricated number.
    The source references G1C-* map to third_party/sheet03_source_register.json.
    """
    tr = threshold()
    ovp = []
    for a, b, c, d in itertools.product((-1, 1), repeat=4):
        rt, rb = 348000*(1+a*.001), 15800*(1+b*.001)
        ovp.append(1.2*(1+c*.02)*(1+rt/rb)+d*150e-9*rt)
    ov_gain = 1+348000*1.001/(15800*.999)
    timed_ovp_start = max(ovp)+.020*ov_gain
    cc = 6*22e-6*.8*.85*.9*.9
    cb_min, rb = cap_values(8)
    cb_max = 8*470e-6*1.2*1.2
    cin_max_screen = 2*22e-6*1.2*1.15
    normal = normal_bound(8)
    normal["false_trip_margin_mV"] = 1000*(tr["min_V"]-normal["normal_max_V"]-.010)
    no_bulk_normal = P["v_dc_max_V"]+.020+normal["excess_charge_C"]/cc+6*.002
    sources = (24.0, max(ovp), 30.0)
    cases = [fault(8, tr, delay, source=vin, ceramic_C=cc, include_state=True)
             for vin, delay in itertools.product(sources, (.2e-6, 2e-6))]
    # Worst among these assumed source screens, NOT an all-condition bound.
    ideal_shunt = cases[-2]
    series = cases[-1]
    st = ideal_shunt["state_at_action"]
    q_r = .0118  # CSD17308Q3 maximum at 25 C, VGS=4.5 V, ID=10 A ONLY.
    rc = P["ceramic_ESR_ohm"]
    # KCL at ideal turn-on, preserving both capacitor internal voltages.
    # i_Q=i_L+i_Ccer+i_Cbulk. This is not i_L + Vraw/RQ (double counts).
    crowbar_cases = []
    for ballast in (0.0, .033, .050):
        rq = q_r+ballast
        v = (st["inductor_A"]+st["ceramic_V"]/rc+st["bulk_V"]/rb)/(1/rq+1/rc+1/rb)
        iq = v/rq
        ic = (st["ceramic_V"]-v)/rc
        ib = (st["bulk_V"]-v)/rb
        assert abs(iq-st["inductor_A"]-ic-ib) < 1e-9
        # Bulk-only isolated RC discharge integral. Minimum ESR=0 sensitivity
        # maximizes this integral for FIXED assumed RQ; RQ has no minimum spec.
        i2t = cb_max*st["bulk_V"]**2/(2*rq)
        interval = shunt_interval(st,rq,cc)
        interval["pi_peak_through_series_off_V"] = max(
            ideal_shunt["pi_peak_screen_V"], interval["raw_peak_after_on_V"]+.020)
        interval["conditional_pi_margin_mV"] = 1000*(5.5-interval["pi_peak_through_series_off_V"])
        crowbar_cases.append({
            "ballast_ohm": ballast, "assumed_mosfet_ohm": q_r,
            "terminal_after_ideal_on_V": v, "total_crowbar_A": iq,
            "inductor_contribution_A": st["inductor_A"],
            "ceramic_discharge_A": ic, "bulk_discharge_A": ib,
            "headroom_to_167A_pulse_A": 167-iq,
            "bulk_only_zero_ESR_I2t_A2s": i2t,
            "bulk_only_RQ_energy_J": q_r*i2t,
            "bulk_only_ballast_energy_J": ballast*i2t,
            "bulk_only_time_constant_s": rq*cb_max,
            "finite_shunt_until_series_off": interval,
            "disposition": "DIRECT SHUNT REJECTED" if ballast == 0 else
                "BALLAST SENSITIVITY ONLY: current commutation, pulse resistor and SOA not designed",
        })

    # Select the 33 mOhm ballast as the conditional development point: it is
    # below the CSD17308 167 A / 100 us headline current in this screen and
    # retains positive Pi headroom. This is not a production SOA approval;
    # the missing pulse-rated ballast and MOSFET SOA are the single blocker.
    selected_crowbar = next(x for x in crowbar_cases if x["ballast_ohm"] == .033)
    series_only = {
        "architecture": "Candidate C series-only common-source pair",
        "parts": ["REF5025IDGKR", "TLV3201AIDBVR", "SN74LVC1G74DCTR",
                  "LTC7001IMSE#PBF", "2 x BSC034N06NSATMA1"],
        "effective_fault_delay_s": P["isolation_requirement_s"],
        "pi_peak_V": series["pi_peak_screen_V"],
        "pi_margin_mV": series["fault_margin_mV"],
        "failure_mode": "series pair alone does not absorb the pre-isolation inductor/capacitor energy",
    }
    crowbar_candidate = {
        "architecture": "Candidate C plus latched low-side crowbar",
        "parts": ["CSD17308Q3", "UCC27511DBVR", "33 mOhm pulse ballast (value screen only)",
                  "same detector/latch and series pair as Candidate C"],
        "detector_to_crowbar_test_sum_s": (55+6.1+26+22)*1e-9,
        "conditional_effective_crowbar_on_s": .2e-6,
        "conditional_series_off_s": 1.8e-6,
        "vout_protected_peak_V": selected_crowbar["finite_shunt_until_series_off"]["raw_peak_after_on_V"],
        "pi_peak_V": selected_crowbar["finite_shunt_until_series_off"]["pi_peak_through_series_off_V"],
        "pi_margin_mV": selected_crowbar["finite_shunt_until_series_off"]["conditional_pi_margin_mV"],
        "crowbar_peak_A": selected_crowbar["finite_shunt_until_series_off"]["crowbar_peak_A"],
        "crowbar_I2t_A2s_screen": selected_crowbar["finite_shunt_until_series_off"]["crowbar_interval_I2t_A2s"],
        "device_pulse_headroom_A": selected_crowbar["headroom_to_167A_pulse_A"],
        "failure_mode": "conditional screen passes Pi/current headline but pulse SOA and ballast pulse rating are unqualified",
    }

    # Reproduce PR6 terms, retaining its classifications, without requiring its
    # branch/worktree at execution time. Source pin: 54d3bc67.../budget.json.
    wire_factor = (1+.00393*(60-20))*1.1
    trunk = 6.5/304.8*.15*wire_factor*1000
    branch = 16.2/304.8*.05*wire_factor*1000
    terms = {"shunt": 2*1.01*(1+25e-6*75), "pcb_positive": 2.5,
        "pcb_return": 2.5, "j502_positive": 5, "j502_return": 5,
        "trunk_positive": trunk, "trunk_return": trunk,
        "positive_branch_wires": branch/2, "ground_branch_wires": branch/4,
        "positive_gpio_contacts": 30*1.3/2, "ground_gpio_contacts": 30*1.3/4,
        "other_joints_equivalent_loop": 5}
    downstream = sum(terms.values())/1000
    series_r = .0068*2  # Gate1b's assumed hot multiplier, not a vendor max.
    original = raw_corners(1+100000/24400)
    # Feasible dimensional changes retaining PR6's actual contact family. Each
    # reduced allocation remains a design target, not a measured resistance.
    reduced = dict(terms)
    reduced.update(pcb_positive=1, pcb_return=1,
        j502_positive=3.12, j502_return=3.12,
        trunk_positive=trunk/2, trunk_return=trunk/2,
        positive_branch_wires=branch/4, ground_branch_wires=branch/16,
        ground_gpio_contacts=30*1.3/8, other_joints_equivalent_loop=2)
    reduced_r = sum(reduced.values())/1000+series_r
    release = normal["release_bound_V"]+.020
    raised = raw_corners(5.2)
    raised_tr = threshold(rt=11700)  # 5.425 V nominal, sensitivity only.
    raised_no_delay = raised_tr["max_V"]+.020*raised_tr["divider_gain_max"]+.020

    def path_option(name, low, high, resistance, trip=tr, extra_release=0.0):
        return {"option": name, "total_raw_to_pi_ohm": resistance,
            "pi_static_5A_V": low-5*resistance,
            "pi_static_5A_margin_mV": 1000*(low-5*resistance-4.75),
            "pi_5A_with_100mV_reserve_V": low-5*resistance-.100,
            "pi_5A_with_reserve_margin_mV": 1000*(low-5*resistance-.100-4.75),
            "pi_normal_max_0A_screen_V": high+release+extra_release,
            "normal_margin_mV": 1000*(trip["min_V"]-high-release-extra_release-.010),
            "trip": trip,
            "pi_fault_margin_mV": None,
            "reason_null": "No datasheet-bounded complete energy/interruption path; see B1C",
            "current_sweep": [{"load_A": i, "pi_static_min_V": low-i*resistance,
                               "pi_static_max_V": high-i*resistance} for i in range(6)]}

    cut = path_option("a: retain setpoint, reduce path resistance (chosen direction)",
                      original["min_V"], original["max_V"], reduced_r)
    # Shunt/switch/harness resistance cannot be credited in the 0 A fault case.
    cut["conditional_ideal_shunt_fault_margin_mV"] = ideal_shunt["fault_margin_mV"]
    cut["conditional_series_fault_margin_mV"] = series["fault_margin_mV"]
    up = path_option("b: 5.2 V local setpoint, existing path, existing trip", raised["min_V"],
                     raised["max_V"], downstream+series_r)
    up["retuned_trip"] = raised_tr
    up["retuned_normal_margin_mV"] = 1000*(raised_tr["min_V"]-raised["max_V"]-release-.010)
    up["retuned_fault_zero_delay_margin_mV"] = 1000*(5.5-raised_no_delay)
    remote = path_option("c: ideal differential remote regulation at original Pi setpoint",
        original["min_V"], original["max_V"], 0,
        extra_release=5*(downstream+series_r))
    remote["raw_high_at_5A_V"] = original["max_V"]+5*(downstream+series_r)
    remote["local_detector_normal_5A_margin_mV"] = 1000*(tr["min_V"]-remote["raw_high_at_5A_V"]-.010)
    remote["load_release_assumption"] = "Full I*R compensation remains during response; no harness-drop credit at 0 A"
    remote["fault_zero_delay_margin_mV"] = 1000*(5.5-tr["max_V"]-.020*tr["divider_gain_max"]-.020)
    ilim = {"min_A":4.185/1.001,"max_A":4.815/.999}
    source_power = 24*ilim["max_A"]
    ce = []
    for vin in sources:
        for ell in (.1e-6, .5e-6, 3.28e-6):
            ce.append(fault(8, tr, .2e-6, source=vin, floor=ell, ceramic_C=cc))
    return {
        "verdict": "BLOCKED",
        "blocker_id": "B1C_UNCOORDINATED_FAULT_ENERGY_PATH",
        "blocker": "Design a rated source-to-shunt energy-limiting/commutation path: direct low-Qg shunt exceeds pulse rating; ballast and source isolation must jointly meet the Pi window.",
        "readiness_scope": "Preliminary schematic review; bench tests are later qualification, not this gate's blocker",
        "worst_case_pi_peak_V": series["pi_peak_screen_V"],
        "worst_case_pi_margin_mV": series["fault_margin_mV"],
        "classification": "Manufacturer limits plus explicitly conditional design screens, not a validated transient simulation",
        "source_envelope": {"single_buck_short_normal_input_max_V":24,
            "single_fault_classification":"REQUIREMENT 9-24 V at input; the high-side-short normal-input bound is 24 V at LM61460 VIN",
            "max_vin_reaching_lm61460_normal_short_V":24.0,
            "max_vin_reaching_lm61460_abnormal_screen_V":max(ovp),
            "abnormal_screen_status":"TPS26630 OVP is a threshold/FLT response, not a voltage clamp; values above the 24 V normal-input requirement need a source/transient contract",
            "ovp_initial_tolerance_V":{"min":min(ovp),"max":max(ovp)},
            "OVP_timing_max_s":14e-6,"OVP_timing_endpoint":"OVP 20 mV above threshold to FLT low, NOT a guaranteed output-voltage clamp",
            "voltage_for_timing_test_high_corner_V":timed_ovp_start,
            "30V_screen_required_ramp_limit_V_per_us":(30-timed_ovp_start)/14,
            "30V_status":"SENSITIVITY ONLY; slew, ringing and source amplitude not bounded by TPS26630 cutoff",
            "source":"G1C-TPS2663 pp6-9,20; divider capture R103/R104"},
        "inductor": {"part":"XAL8080-682MED", "L0_min_H":6.8e-6*.8,
            "curve_readings_A_uH":[[0,6.5],[5,6.0],[10,5.3],[14,4.6],[16.5,4.2]],
            "curve_classification":"Approximate visual readings, typical 25 C; tolerance is specified at zero bias only",
            "30percent_point_A":14, "30percent_tolerance_screen_H":6.8e-6*.8*.7,
            "effective_L_screen_at_16p5A_H":4.2e-6*.8,
            "effective_L_guaranteed_beyond_curve_H":None,
            "positive_L_floor_beyond_curve_H":None,
            "old_0p5uH_status":"Rejected as datasheet bound; retained sensitivity only",
            "source":"G1C-XAL8080 pp1-2, footnotes2,5,8 and 6.8uH L-vs-current panel; curve readings are typical, not a guaranteed saturation bound"},
        "capacitance": {"captured_output_parts":"C209-C214: 6 x C5750X7R1H226M250KB; zero raw bulk capacitors",
            "captured_nominal_F":132e-6,"captured_bulk_F":0,
            "ceramic_screen_F":cc,"ceramic_screen_factors":{"initial":.8,"temperature":.85,"bias":.9,"aging_allocation":.9},
            "ceramic_status":"Conservative design estimate at <=5.5V; not a guaranteed combined minimum. TDK p1 bias approximately 0 percent at 5V; curves reference data.",
            "proposed_bulk_part":"8 x PCH1V471MCL1GS (not captured)",
            "proposed_bulk_min_F":cb_min,"proposed_bulk_max_F":cb_max,
            "bulk_limit_conditions":"Initial +/-20 percent, endurance +/-20 percent relative to initial at restored20C; not an all-temperature C guarantee",
            "bulk_bank_ESR_max_screen_ohm":rb,"bulk_bank_ESR_min_ohm":None,
            "input_C_max_screen_F":cin_max_screen,"input_C_max_status":"Nominal x1.2x1.15 design screen; bias decreases are ignored; not combined manufacturer guarantee",
            "source":"G1C-TDK p1; G1C-PCH pp1-2"},
        "threshold_tolerance":tr, "normal_with_proposed_bulk":normal,
        "normal_captured_MLCC_only":{"peak_screen_V":no_bulk_normal,
            "false_trip_margin_mV":1000*(tr["min_V"]-no_bulk_normal-.010),
            "classification":"Same assumed6A/20us release stimulus as Gate1b; shows bulk cannot be silently credited to capture"},
        "fault_screens":cases,"L_sensitivity":ce,
        "comparison": {"series_only":series_only,"crowbar_assisted":crowbar_candidate,
            "selection":"Crowbar-assisted Candidate C is the preliminary development direction; it is not capture-ready because the pulse-rated commutation/SOA path is not closed."},
        "conditional_shunt_delay_ceiling_s":delay_ceiling(tr, cc, 30),
        "crowbar":{"part":"CSD17308Q3", "driver":"UCC27511DBVR, independent5V supply",
            "pin_level_candidate":{"drain":"VOUT_PROTECTED","source":"33 mOhm ballast to detector ground",
                "gate":"UCC27511 OUT through 2.2 ohm provisional resistor; 10 kohm provisional gate-source pulldown",
                "driver_IN":"CROWBAR_ON","driver_VDD":"independent 5 V detector rail","driver_GND":"detector ground"},
            "conditional_effective_on_s":.2e-6,
            "timing_components_s":{"TLV3201_max_at_20mV":55e-9,"latch_max_5V_125C":6.1e-9,
                "driver_max_4p5V_1p8nF":26e-9,"driver_rise_max_same_test":22e-9},
            "timing_sum_test_conditions_only_s":(55+6.1+26+22)*1e-9,
            "timing_gap":"Divider RC, actual high-current gate charge, validity gating and commutation are not covered by adding disparate test times",
            "Qg_max_4p5V_10A_C":5.1e-9,"pulse_limit_25C_A":167,
            "pulse_limit_conditions":"<=100us, duty<=1 percent; also comply with Fig10 SOA and temperature",
            "manufacturer_I2t_rating_A2s":None,
            "rectangular_167A_100us_integral_NOT_rating_A2s":167**2*100e-6,
            "pulse_screens":crowbar_cases,
            "stored_energy_screens_J":{"raw_bulk":.5*cb_max*st["bulk_V"]**2,
                "raw_ceramic":.5*(132e-6*1.2*1.15)*st["ceramic_V"]**2,
                "buck_input_caps_24V":.5*cin_max_screen*24**2},
            "additional_energy":"Inductor, source before/after current limiting, and downstream back-discharge must be added; local capacitor energies are not total fault energy",
            "selected_ballast_ohm":.033,
            "selected_screen":crowbar_candidate,
            "source":"G1C-CSD17308 pp1,3,7 Fig10; G1C-UCC27511 pp9-10; G1C-TLV3201 pp3-5; G1C-SN74LVC1G74 p7"},
        "efuse":{"part":"TPS26630RGER","captured_MODE":"pin11 NC => latch after limiting/thermal timeout",
            "R105_ohm":4020,"resistor_tolerance_fraction":.001,"current_limit":ilim,
            "normal_overload_timer_max_s":.202,"startup_thermal_regulation_timeout_max_s":2.9,
            "thermal_shutdown_typ_C":165,"overload_near_short_power_24V_W":source_power,
            "hypothetical_202ms_energy_without_thermal_shutdown_J":source_power*.202,
            "settled_limit_202ms_I2t_A2s":ilim["max_A"]**2*.202,
            "SHDN_entry_max_s":1.5e-6,
            "proposed_end_fault":"FAULT latch also pulls U101 pin12 SHDN low; hold until manual reset. Upstream detector supply must remain alive after OUT removal.",
            "SOA_disposition":"Integrated thermal protection described by vendor; no external-FET-style SOA plot or licence to dissipate24V*4.82A for202ms. Stored output/input energy is downstream of it.",
            "source":"G1C-TPS2663 pp7-9,22-25,27-28",
            "next_fault_sequence":"TPS26630 first limits at the R105-programmed current; pin 11 NC selects latch-off after the overload timer/thermal action. The crowbar fault latch also asserts U101 SHDN; source removal is therefore the TPS26630 latch/thermal path and upstream source disconnect, not the crowbar alone."},
        "reset_startup":{"startup_state":"crowbar and series pair OFF until detector supply-valid, reference-valid, comparator-good and BUCK_PGOOD are true",
            "fault_state":"OV clears the latch; no automatic retry; manual ARM/reset is required after raw voltage is valid",
            "load_release_screen_margin_mV":normal["false_trip_margin_mV"],
            "captured_MLCC_only_release_margin_mV":1000*(tr["min_V"]-no_bulk_normal-.010),
            "false_crowbar_controls":"BUCK_PGOOD qualification, detector-valid gating, comparator hysteresis allocation and latch clear dominance; exact reset interlock remains OPEN",
            "source":"G1C-TLV3201 pp3-5; G1C-SN74LVC1G74 p7/function table; G1C-LM61460 pp40-41"},
        "harness":{"PR6_commit":"54d3bc67fd64f4bd947440518d90e76673faf5db",
            "original_terms_mOhm":terms,"original_downstream_ohm":downstream,
            "original_drop_5A_mV":5000*downstream,
            "PR6_10mOhm_series_pi_static_V":original["min_V"]-5*(downstream+.010),
            "gate1b_13p6mOhm_series_pi_static_V":original["min_V"]-5*(downstream+series_r),
            "reduced_terms_mOhm":reduced,"series_hot_screen_ohm":series_r,
            "selected_direction":"a: cut path resistance, retain local regulation and raw-node OVP. No remote feedback or feedback-resistor edit selected.",
            "required_total_R_with_100mV_reserve_ohm":(original["min_V"]-4.75-.1)/5,
            "options":[cut,up,remote]},
        "numerical_check":{"half_step":fault(8,tr,.2e-6,source=30,ceramic_C=cc,dt=P['dt_s']/2)},
    }


def delay_ceiling(tr, ceramic_C, source):
    lo, hi = 0.0, 5e-6
    for _ in range(24):
        mid = (lo+hi)/2
        if fault(8,tr,mid,source=source,ceramic_C=ceramic_C)["passes_fault_inequality"]:
            lo = mid
        else:
            hi = mid
    return lo


def calculate_gate1d():
    """Audit applicability of the pulse model before selecting production parts.

    This is a consistency check, not a nonlinear MOSFET simulation. In
    particular, calculating VGS from the old current does NOT predict the real
    current when the old RDS(on) assumption is invalid.
    """
    prior = calculate_gate1c()
    screen = prior["crowbar"]["selected_screen"]
    peak = screen["crowbar_peak_A"]
    i2t = screen["crowbar_I2t_A2s_screen"]
    ballast = .033
    # DATASHEET: WFMB2512 +/-1%, component TCR +/-50ppm/K, -55..150C.
    # ASSUMED review initial temperature 25C and hot screen 125C, not a
    # replacement for the project's OPEN thermal operating contract.
    r_error = .01 + 50e-6 * 100
    rmin, rmax = ballast*(1-r_error), ballast*(1+r_error)
    state = prior["fault_screens"][-2]["state_at_action"]
    cc = prior["capacitance"]["ceramic_screen_F"]
    sweep = []
    for r in (0.0, .0033, .010, rmin, ballast, rmax, .050):
        row = shunt_interval(state, r+.0118, cc)
        pi = max(screen["pi_peak_V"], row["raw_peak_after_on_V"]+.020)
        sweep.append({"ballast_ohm": r, "classification": "INVALID-DRIVE MODEL SENSITIVITY ONLY",
                      "peak_A": row["crowbar_peak_A"],
                      "ideal_5V_gate_VGS_at_peak_V": 5-r*row["crowbar_peak_A"],
                      "pi_peak_screen_V": pi, "pi_margin_screen_mV": 1000*(5.5-pi),
                      "below_167A_headline": row["crowbar_peak_A"] < 167,
                      "supports_4p5V_RDS_test_condition": 5-r*row["crowbar_peak_A"] >= 4.5})
    # Conservative visually-read point BELOW the published 2512 curve at
    # 100us (approximately 2000W). Extend the actual pulse in time, rather
    # than extrapolating a curve below its shortest plotted duration.
    resistor_envelope_W, resistor_envelope_s = 1000.0, 100e-6
    peak_power = peak**2*rmax
    # Permitted correction: put ballast between protected node and drain,
    # source AND driver GND at detector GND. Test parts and hot-resistance
    # screens instead of treating the original wiring failure as dispositive.
    alternatives = []
    for part, r25, pulse, qg in (("CSD17308Q3", .0118, 167, 5.1e-9),
                                ("CSD17577Q5A", .0058, 280, 17e-9),
                                ("CSD18540Q5B", .0033, 400, 26e-9)):
        corners = []
        for delay, rq, rr in itertools.product((.2e-6, .3e-6, .4e-6, .5e-6),
                                               (0.0, r25, 2*r25), (rmin, rmax)):
            before = fault(8, prior["threshold_tolerance"], delay,
                           ceramic_C=cc, include_state=True)
            after = shunt_interval(before["state_at_action"], rq+rr, cc,
                                   duration=P["isolation_requirement_s"]-delay)
            pi = max(before["pi_peak_screen_V"], after["raw_peak_after_on_V"]+.020)
            corners.append({"assumed_effective_on_s": delay, "assumed_RDS_ohm": rq,
                            "ballast_ohm": rr, "peak_A": after["crowbar_peak_A"],
                            "I2t_A2s": after["crowbar_interval_I2t_A2s"],
                            "ballast_energy_J": rr*after["crowbar_interval_I2t_A2s"],
                            "pi_peak_V": pi, "pi_margin_mV": 1000*(5.5-pi),
                            "normal_false_trip_margin_mV": prior["normal_with_proposed_bulk"]["false_trip_margin_mV"],
                            "harness_5A_V": prior["harness"]["options"][0]["pi_static_5A_V"],
                            "harness_margin_mV": prior["harness"]["options"][0]["pi_static_5A_margin_mV"]})
        alternatives.append({"part": part, "connection": "drain-side ballast; grounded source",
                             "DATASHEET_RDS_4p5V_25C_ohm": r25,
                             "DATASHEET_ID_pulse_A": pulse, "DATASHEET_Qg_4p5V_max_C": qg,
                             "ASSUMED_hot_R_multiplier": 2,
                             "zero_RDS_case": "current upper sensitivity; not a manufacturer minimum",
                             "corners": corners,
                             "disposition": "Grounded-source correction restores drive. CSD18540 selected below; other parts retained as comparisons. Timing qualification remains OPEN."})
    # Upper current/power from the drain-ballast load line at an ASSUMED 5.5V
    # node ceiling. Do NOT use this ceiling to prove the ceiling itself.
    ceiling = 5.5
    load_line = {"ASSUMED_node_ceiling_V": ceiling,
                 "current_upper_A": ceiling/rmin,
                 "MOSFET_power_upper_W": ceiling**2/(4*rmin),
                 "ballast_power_upper_W": ceiling**2/rmin,
                 "limitation": "Useful for SOA comparison only AFTER timing/voltage ceiling is established; circular as proof of Pi protection"}
    # Gate1c timing is accepted for PRELIMINARY review, not newly qualified.
    # Four33mOhm parts (R+R)||(R+R) retain33mOhm with lower element stress.
    powers = []
    for a,b,c,d in itertools.product((rmin,rmax), repeat=4):
        powers.extend((ceiling**2*a/(a+b)**2, ceiling**2*b/(a+b)**2,
                       ceiling**2*c/(c+d)**2, ceiling**2*d/(c+d)**2))
    per_res_peak = max(powers)
    resistor_hot_factor = (170-125)/(170-70)
    downstream = 220e-6  # inherited ASSUMED downstream sensitivity, OPEN
    tau_max = (rmax+.0066)*downstream
    tail_at_100us_A = ceiling/rmin*math.exp(-98e-6/tau_max)
    soa_power = load_line["MOSFET_power_upper_W"]
    ztheta_screen = .05*.8  # Fig1 normalized100us curve BELOW0.05
    accepted_rows = [x for x in alternatives[-1]["corners"] if x["assumed_effective_on_s"] == .3e-6]
    return {
        "verdict": "PRELIMINARY — READY FOR SCHEMATIC REVIEW",
        "gate_status": "CONDITIONAL PASS",
        "closed_blocker_id": "B1C_UNCOORDINATED_FAULT_ENERGY_PATH",
        "closure_scope": "Pulse part selection within user-accepted Gate1c preliminary envelope; R2/R3 release remains BLOCKED",
        "architecture_authorization": "Candidate C plus crowbar accepted for preliminary development by GATE_1D_2.md; Gate 2 only if Gate 1d passes",
        "gate_2_authorized": True,
        "classification": "DATASHEET pulse/SOA comparison plus CALCULATED load-line bounds and ASSUMED timing/temperature/tail screens; not bench validation",
        "threshold": prior["threshold_tolerance"],
        "legacy_conditional_screen": {
            "pi_peak_V": screen["pi_peak_V"], "pi_margin_mV": screen["pi_margin_mV"],
            "harness_5A_V": prior["harness"]["options"][0]["pi_static_5A_V"],
            "harness_margin_mV": prior["harness"]["options"][0]["pi_static_5A_margin_mV"],
            "normal_false_trip_margin_mV": prior["normal_with_proposed_bulk"]["false_trip_margin_mV"],
            "status": "OPEN review items; positive arithmetic is not an achieved circuit window",
        },
        "drive_consistency": {
            "mosfet": "CSD17308Q3", "driver": "UCC27511DBVR",
            "connection": "Drain at protected; source through ballast to GND; driver GND at detector GND",
            "assumed_supply_V": 5.0, "ballast_ohm": ballast,
            "legacy_peak_A": peak, "legacy_source_at_peak_V": peak*ballast,
            "ideal_gate_VGS_upper_at_legacy_peak_V": 5-peak*ballast,
            "RDS_model_ohm": .0118, "RDS_datasheet_test_VGS_V": 4.5,
            "RDS_datasheet_test_ID_A": 10, "RDS_datasheet_test_TA_C": 25,
            "lowest_RDS_specified_VGS_V": 3.0,
            "threshold_max_at_250uA_V": 1.6,
            "max_I_for_4p5V_VGS_with_ideal_5V_driver_A": (5-4.5)/ballast,
            "max_I_for_3V_VGS_with_ideal_5V_driver_A": (5-3)/ballast,
            "applicable": False,
            "source": "G1D-CSD17308 pp1,3; G1D-UCC27511 pp6,9,18-19",
        },
        "mosfet_pulse_review": {
            "selected_for_capture": False, "candidate": "CSD17308Q3",
            "headline_A": 167, "headline_duration_s": 100e-6,
            "legacy_peak_headroom_A": 167-peak,
            "legacy_model_duration_s": 1.8e-6,
            "legacy_I2t_A2s": i2t, "manufacturer_I2t_A2s": None,
            "legacy_ohmic_VDS_at_peak_V": peak*.0118,
            "legacy_ohmic_energy_J": i2t*.0118,
            "SOA": "SLPS262C p7 Fig10, single pulse, TA=25C unless stated, max RthetaJC=4.5C/W; shortest plotted curve 10us. Need actual ID/VDS/temperature trajectory, not a 167A-only comparison.",
            "limitation": "No SOA pass: gate drive is inconsistent; turn-on trajectory and downstream discharge tail are not in the 1.8us ideal-resistor interval.",
        },
        "ballast_pulse_review": {
            "candidate": "WFMB2512R0330FEA", "selection": "Provisional pulse candidate for the old interval only; no capture release",
            "source": "G1D-WFM, document30387 Rev04-Aug-2022 pp1-3, p3 Single Pulse chart (unnumbered)",
            "nominal_ohm": ballast, "initial_tolerance_fraction": .01,
            "component_TCR_ppm_per_K": 50, "assumed_temperature_delta_K": 100,
            "R_screen_min_ohm": rmin, "R_screen_max_ohm": rmax,
            "legacy_interval_energy_J": ballast*i2t,
            "fixed_legacy_waveform_hot_energy_J": rmax*i2t,
            "fixed_legacy_waveform_hot_peak_W": peak_power,
            "conservative_100us_envelope_W": resistor_envelope_W,
            "conservative_100us_envelope_J": resistor_envelope_W*resistor_envelope_s,
            "derived_envelope_I2t_A2s_not_vendor_rating": resistor_envelope_W*resistor_envelope_s/rmax,
            "peak_power_margin_factor": resistor_envelope_W/peak_power,
            "interval_energy_margin_factor": resistor_envelope_W*resistor_envelope_s/(rmax*i2t),
            "assessment": "Old interval fits inside a conservative 100us rectangular pulse screen. Not a sub-100us curve extrapolation or total-fault qualification; terminal-temperature pulse derating, inductance, real waveform and post-isolation tail remain OPEN.",
        },
        "ballast_sensitivity": sweep,
        "corrected_connection_candidates": alternatives,
        "corrected_load_line": load_line,
        "selected_implementation": {
            "mosfet": "CSD18540Q5B", "driver": "UCC27511DBVR on independent7.5V rail",
            "ballast": "4 x WFMB2512R0330FEA, (R+R)||(R+R), effective33mOhm",
            "connection_correction": "VOUT_PROTECTED -> ballast bank -> MOSFET drain; source and driver GND to detector ground",
            "gate_network": "OUTH through1ohm, OUTL direct,10kohm gate-source;1uF+100nF driver decoupling",
            "accepted_effective_on_s": .3e-6, "accepted_series_off_from_detection_s": 2e-6,
            "worst_pi_peak_V": max(x["pi_peak_V"] for x in accepted_rows),
            "worst_pi_margin_mV": min(x["pi_margin_mV"] for x in accepted_rows),
            "worst_model_peak_A": max(x["peak_A"] for x in accepted_rows),
            "worst_model_I2t_A2s": max(x["I2t_A2s"] for x in accepted_rows),
            "harness_margin_mV": prior["harness"]["options"][0]["pi_static_5A_margin_mV"],
            "normal_false_trip_margin_mV": prior["normal_with_proposed_bulk"]["false_trip_margin_mV"],
            "timing_estimate": {
                "ASSUMED_rail_min_V": 7.35, "DATASHEET_Qg_max_test_C": 26e-9,
                "ASSUMED_total_pullup_ohm": 11+1+1.6,
                "CALCULATED_charge_to4p5V_s": 26e-9*(11+1+1.6)/(7.35-4.5),
                "CALCULATED_detector_latch_driver_charge_sum_s": (55+6.1+26)*1e-9+26e-9*(11+1+1.6)/(7.35-4.5),
                "scope": "Conservative constant-current screen using4.5V DC driver resistance and actual maxQg test value; selected0.3us screen exceeds this charge estimate; inherited0.2us result retained for comparison. Actual nonlinearQg/rail/filter/logic/commutation remains OPEN, not a new prerequisite for preliminary capture."},
        },
        "selected_full_pulse_review": {
            "ASSUMED_initial_FET_T_C": 125, "ASSUMED_initial_resistor_terminal_T_C": 125,
            "ASSUMED_downstream_C_max_F": downstream,
            "ASSUMED_no_external_power_source": True,
            "initial_interval_s": 2e-6, "rectangular_envelope_s": 100e-6,
            "load_line_current_upper_A": ceiling/rmin,
            "pulse_ID_margin_A": 400-ceiling/rmin,
            "MOSFET_power_upper_W": soa_power,
            "DATASHEET_Fig1_normalized_Z_upper_reading": .05,
            "DATASHEET_RthetaJC_max_C_per_W": .8,
            "CALCULATED_delta_T_upper_C": soa_power*ztheta_screen,
            "CALCULATED_Tj_upper_C": 125+soa_power*ztheta_screen,
            "CALCULATED_margin_to175C_C": 175-125-soa_power*ztheta_screen,
            "SOA_comparison": "SLPS488B p6 Fig10:100us curve approximately400A at2..5.5V; thermal derating(175-125)/(175-25)=1/3 gives133A. Load line atVDS>=2V hasID<=107.7A. Lower-VDS ohmic branch checked with power/thermal envelope and400A pulse limit; do not derate the RDS boundary as a thermal power limit.",
            "resistor_per_element_peak_W": per_res_peak,
            "resistor_conservative_25C_100us_W": 1000,
            "ASSUMED_pulse_derating_factor": resistor_hot_factor,
            "resistor_hot_100us_W": 1000*resistor_hot_factor,
            "resistor_power_margin_factor": 1000*resistor_hot_factor/per_res_peak,
            "resistor_hot_100us_energy_J_each": .1*resistor_hot_factor,
            "resistor_envelope_energy_J_each": per_res_peak*100e-6,
            "CALCULATED_RC_tail_tau_max_s": tau_max,
            "CALCULATED_current_after100us_A": tail_at_100us_A,
            "CALCULATED_remaining_tail_energy_J": .5*downstream*ceiling**2*math.exp(-2*98e-6/tau_max),
            "tail_note": "First100us envelope includes turn-on and full meaningful downstream discharge; beyond100us residual power is below DC ratings. Raw bulk is upstream after2us; initial interval already includes its feed. Larger/external downstream stores require recalculation; accepted sensitivity is not a measured Pi capacitance.",
            "OPEN": "thermal-interface realization, pulse derating confirmation, parasitic inductance, actual downstream C and inherited timing/source assumptions remain release/bench-review items",
        },
        "driver_alternatives": [
            {"part": "UCC27511DBVR", "supply_screens_V": [5.0, 7.5],
             "assessment": "Grounded source fixes VGS; 7.5V independent rail improves headroom and is within4.5..18V operation. 26ns propagation/22ns rise maxima are for1.8nF at4.5V; 23ns/12ns at12V. Actual nonlinear140..160A FET charge/commutation is not bounded by those tests. Rail implementation/validity remains OPEN."},
            {"part": "LMG1020YFFR", "supply_screens_V": [5.0],
             "assessment": "4.1ns maximum rising propagation uses100pF. 7A peak source and375ps rise are typical, not a guaranteed high-current gate-charge completion time; need actual device/load trajectory. No7.5V use: recommended4.75..5.4V."},
            {"part": "UCC27614DBVR", "supply_screens_V": [5.0, 7.5, 12.0],
             "assessment": "27ns propagation/6ns rise maxima use12V and1.8nF; 4.5ohm PMOS DC max uses12V/-50mA. Peak10A is typical and not a minimum gate current. 12V needs boost or another independent source at9V input; 5/7.5V tests cannot inherit12V timing maxima."},
        ],
        "effective_on_ceiling_s": prior["conditional_shunt_delay_ceiling_s"],
        "actual_pi_peak_V": None,
        "actual_pi_peak_reason": "No measured peak; selected corrected implementation has a conditional calculated peak above. Original source-ballast wiring is rejected.",
        "open_items": ["39.33mV conditional fault margin", "11.43mV static harness margin and unmet100mV reserve",
                       "source transient and saturated-inductor bounds", "effective capacitance and proposed8x470uF bank",
                       "reset/reference/supply-valid interlock and independent rails", "startup/inrush and series-FET SOA",
                       "crowbar turn-on and full discharge tail; parasitic inductance and terminal temperature",
                       "series common-source/common-drain inconsistency in prior prose", "remaining R2 fuse/TVS/connector/thermal qualifications"],
    }


def calculate_gate2(netlist):
    """Read actual exported values; retain earlier gate records as history."""
    tree = ET.parse(netlist).getroot()
    components = {c.get('ref'): c for c in tree.findall('./components/comp')}
    used = {}

    def value(ref):
        text = components[ref].findtext('value')
        match = re.fullmatch(r'([\d.]+)([kMmun]?)(?:F(?: .*)?)?', text)
        if not match:
            raise ValueError(f'Unsupported captured value {ref}: {text}')
        result = float(match[1])*{'':1,'k':1e3,'M':1e6,'m':1e-3,'u':1e-6,'n':1e-9}[match[2]]
        used[ref] = {'captured_text': text, 'SI_value': result}
        return result

    previous = json.loads(TARGET.read_text())
    tr = threshold(value('R301'), value('R302'))
    # Preserve the accepted fault model only when its other captured inputs
    # still match. A changed model input must not inherit the previous margins.
    if (value('R202'), value('R203')) != (100000,24400):
        raise ValueError('Buck divider changed; revise inherited fault initial conditions')
    raw = raw_corners(1+value('R202')/value('R203'))
    caps = [value(f'C{n}') for n in range(330,338)]
    if any(not math.isclose(c,470e-6) for c in caps):
        raise ValueError('Bulk bank changed; revise fault model')
    for ref, part in [('U302','REF5025IDGKR'),('U303','TLV3201AIDBVR'),
                      ('U315','UCC27511DBVR'),('Q303','CSD18540Q5B')]:
        if part not in ET.tostring(components[ref],encoding='unicode'):
            raise ValueError(f'{ref}: selected device changed; review model assumptions')
    r = [value(f'R{n}') for n in range(308,312)]
    ballast = (r[0]+r[1])*(r[2]+r[3])/sum(r)
    if not math.isclose(ballast,.033):
        raise ValueError('Ballast changed; redo Gate1d full pulse selection')
    cc = previous['gate_1c']['capacitance']['ceramic_screen_F']
    before = fault(8,tr,.3e-6,ceramic_C=cc,include_state=True)
    corners=[]
    for rq,rr in itertools.product((0,.0033,.0066),(ballast*.985,ballast*1.015)):
        after=shunt_interval(before['state_at_action'],rq+rr,cc,duration=1.7e-6)
        peak=max(before['pi_peak_screen_V'],after['raw_peak_after_on_V']+.020)
        corners.append({'ASSUMED_RDS_ohm':rq,'ballast_ohm':rr,'pi_peak_V':peak,
                        'pi_margin_mV':1000*(5.5-peak)})
    normal=normal_bound(8)
    normal['false_trip_margin_mV']=1000*(tr['min_V']-normal['normal_max_V']-.010)

    def ldo(top,bottom):
        rt,rb=value(top),value(bottom)
        # SBVS171F p6: overall +/-2%, IFB +/-0.1uA. Resistors:
        # ASSUMED 0.1% plus 10ppm/K*100K, pending exact MPNs.
        values=[1.193*(1+a*.02)*(1+rt*(1+b*.002)/(rb*(1+c*.002)))
                +d*.1e-6*rt*(1+b*.002)
                for a,b,c,d in itertools.product((-1,1),repeat=4)]
        return {'nominal_V':1.193*(1+rt/rb),'min_V':min(values),'max_V':max(values),
                'DATASHEET_overall_fraction':.02,'DATASHEET_FB_current_A':.1e-6,
                'ASSUMED_resistor_fraction':.002,
                'condition':'Regulation only, VIN >= nominal output +0.5V; dropout, supply collapse and thermal limits OPEN'}

    rails={'detector':ldo('R312','R313'),'driver':ldo('R314','R315')}
    resistance=previous['gate_1c']['harness']['options'][0]['total_raw_to_pi_ohm']
    harness_min=raw['min_V']-5*resistance
    charge=26e-9*(11+value('R306')+1.6)/(rails['driver']['min_V']-4.5)
    # This estimates the inherited charge term only; new combinational stages,
    # filtering and nonlinear current/charge are explicitly not bounded here.
    ovp=[]
    rt,rb=value('R103'),value('R104')
    for a,b,c,d in itertools.product((-1,1),repeat=4):
        top,bottom=rt*(1+a*.001),rb*(1+b*.001)
        ovp.append(1.2*(1+c*.02)*(1+top/bottom)+d*150e-9*top)
    return {'classification':'CALCULATED from KiCad-exported values using DATASHEET limits and explicit ASSUMED envelopes; not physical validation',
            'netlist':str(netlist.relative_to(ROOT)),'netlist_sha256':hashlib.sha256(netlist.read_bytes()).hexdigest(),
            'captured_values':used,'threshold':tr,'raw_buck':raw,'normal':normal,
            'input_ovp':{'nominal_V':1.2*(1+rt/rb),'min_V':min(ovp),'max_V':max(ovp)},
            'rails':rails,'raw_bulk_nominal_F':sum(caps),'raw_bulk_min_screen_F':sum(caps)*.8*.8,
            'ballast_equivalent_ohm':ballast,'fault_corners':corners,
            'pi_peak_V':max(c['pi_peak_V'] for c in corners),
            'fault_margin_mV':min(c['pi_margin_mV'] for c in corners),
            'harness':{'ASSUMED_total_path_ohm':resistance,'pi_5A_min_V':harness_min,
                       'static_margin_mV':1000*(harness_min-4.75),'with_100mV_reserve_margin_mV':1000*(harness_min-4.85)},
            'gate_drive':{'ASSUMED_required_rail_min_V':7.35,'regulated_rail_headroom_V':rails['driver']['min_V']-7.35,
                          'charge_to_4p5V_screen_s':charge,'old_partial_detector_latch_driver_charge_sum_s':(55+6.1+26)*1e-9+charge,
                          'ASSUMED_effective_crowbar_on_s':.3e-6,'ASSUMED_effective_series_off_s':2e-6,
                          'OPEN':'The captured multi-gate latch chain, filter, actual nonlinear gate charge, falling-rail validity and commutation need complete timing qualification; this partial sum is not an end-to-end bound.'},
            'margin_change':'Gate1c used0.20us crowbar action; Gate1d/2 use0.30us for the larger selected FET charge screen, increasing modeled peak by20.940mV and reducing margin39.328mV to18.388mV. No measured timing is claimed.',
            'OPEN':['18.388mV fault margin and inherited timing/source/L/C assumptions','11.431mV harness margin; 100mV reserve unmet','startup/reset, auxiliary dropout/reverse/transient behavior, thermal and SOA','remaining R2/R3 release criteria']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--gate", choices=("1b", "1c", "1d", "2"), default="1b")
    parser.add_argument('--netlist', type=Path, default=ROOT/'docs/evidence/r2/sheet03/V1A_gate2.net.xml')
    args=parser.parse_args()
    result=(calculate_gate2(args.netlist.resolve()) if args.gate == '2' else
            {"1b": calculate, "1c": calculate_gate1c, "1d": calculate_gate1d}[args.gate]())
    if args.write:
        data=json.loads(TARGET.read_text())
        data["gate_"+args.gate]=result
        if args.gate == '2':
            data['classification']='CALCULATED SCREENS ONLY; preliminary Sheet03 captured, R2/R3 release BLOCKED; no bench validation. Earlier gate members are preserved historical records.'
        TARGET.write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
