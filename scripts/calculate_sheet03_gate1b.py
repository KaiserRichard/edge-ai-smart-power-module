#!/usr/bin/env python3
"""Candidate-C feasibility screen, NOT a validated buck/device simulation.

All units are SI. --write updates only the gate_1b member of the existing
CALCULATIONS.json. Source identifiers and limitations are in the decision file.
Uses RK4 for a stiff-voltage-source fault feeding L and two C/ESR branches.
No credit for input eFuse action, source resistance, or load current.
"""
import argparse
import itertools
import json
import math
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
          input_cap=None, input_current=0.0):
    """RK4 until effective isolation. Comparator overdrive is paid before delay.

    Once ideal isolation occurs raw energy stays upstream. Report an assumed
    extra 20 mV on the downstream rail; no credit for switch/harness drop.
    This deliberately ideal switch cannot establish real MOSFET SOA.
    """
    cb, rb = cap_values(n)
    cc, rc = P["ceramic_C_min_F"], P["ceramic_ESR_ohm"]
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
    return {"bulk_count": n, "source_V": source, "L_floor_H": floor,
            "input_cap_F": input_cap, "input_feed_A": input_current,
            "vin_at_isolation_V": state[3],
            "piecewise_L": piecewise, "delay_s": delay, "time_to_detect_s": detected,
            "current_at_detect_A": i_detect, "current_at_isolate_A": state[0],
            "detect_voltage_V": v_detect_actual, "raw_peak_at_isolation_V": vpeak,
            "let_through_including_overdrive_and_local_V": peak-trip["max_V"],
            "pi_peak_screen_V": peak, "fault_margin_mV": 1000*(5.5-peak),
            "passes_fault_inequality": peak < 5.5}


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


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args=parser.parse_args()
    result=calculate()
    if args.write:
        data=json.loads(TARGET.read_text())
        data["gate_1b"]=result
        TARGET.write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
