#!/usr/bin/env python3
"""Recompute R2 screening calculations; all assumptions are explicit in the report."""
import argparse
import itertools
import json
import math
from pathlib import Path


def divider_bounds(top, bottom, threshold, tolerance=0.001, leakage=150e-9):
    values = [v * (1 + rt / rb) + leak * rt
              for rt, rb, v, leak in itertools.product(
                  [top * (1-tolerance), top * (1+tolerance)],
                  [bottom * (1-tolerance), bottom * (1+tolerance)],
                  threshold, [-leakage, leakage])]
    return [min(values), max(values)]


def calculate():
    vout = 1 + 100e3 / 24.4e3
    points = []
    for vin in (9, 12, 24):
        duty = vout / vin
        ripple = vout * (1-duty) / (6.8e-6 * 400e3)
        # 10% additional L loss with bias is an assumption for sensitivity screening.
        worst = vout * (1-duty) / (6.8e-6 * 0.8 * 0.9 * 360e3)
        points.append(dict(vin_V=vin, duty=duty, on_time_ns=duty/400e3*1e9,
                           ripple_A=ripple, peak_A=5+ripple/2,
                           rms_A=math.sqrt(25+ripple**2/12),
                           valley_A=5-ripple/2, corner_ripple_A=worst,
                           corner_peak_A=5+worst/2,
                           input_A_at_90pct=25.5/(vin*0.9),
                           cin_rms_A=5*math.sqrt(duty*(1-duty))))
    cin = 2*22e-6*0.65*0.8*0.85
    cout = 6*22e-6*0.95*0.8*0.85
    return dict(
        classification='CALCULATION; not measurement or guaranteed L/C production limits',
        output_nominal_V=vout,
        output_divider_and_reference_corner_V=divider_bounds(100e3,24.4e3,[0.99,1.01],leakage=10e-9),
        buck_points=points,
        min_inductance_eq10_uH=0.32*vout/360e3*1e6,
        assumed_corner_inductance_uH=6.8*0.8*0.9,
        minimum_ripple_at_9V_Lmax_fmax_A=vout*(1-vout/9)/(6.8e-6*1.2*440e3),
        on_time_at_24V_fmax_ns=(vout/24)/440e3*1e9,
        effective_cin_screen_uF=cin*1e6,effective_cout_screen_uF=cout*1e6,
        ripple_screen_mV=(points[-1]['corner_ripple_A']/(8*360e3*cout)+points[-1]['corner_ripple_A']*0.002)*1000,
        inductor_copper_loss_at_25C_maxDCR_W=(25+points[-1]['corner_ripple_A']**2/12)*0.0145,
        whole_module_loss_budget_at_90pct_W=25.5*(1/0.9-1),
        input_uvlo_rising_V=divider_bounds(332e3,54.9e3,[1.176,1.224]),
        input_uvlo_falling_V=divider_bounds(332e3,54.9e3,[1.09,1.15]),
        input_ovp_rising_V=divider_bounds(348e3,15.8e3,[1.176,1.224]),
        input_ovp_falling_V=divider_bounds(348e3,15.8e3,[1.09,1.15]),
        input_pg_rising_V=divider_bounds(56.2e3,10e3,[1.176,1.224]),
        input_pg_falling_V=divider_bounds(56.2e3,10e3,[1.09,1.15]),
        input_ilim_nominal_A=18000/4020,
        input_ilim_corner_A=[18000/4020*0.93/1.001,18000/4020*1.07/0.999],
        input_ramp_24V_nominal_ms=24*100e-9/(25*2e-6)*1000,
        input_ramp_24V_corner_ms=[24*90e-9/(26*2.225e-6)*1000,24*110e-9/(23.5*1.775e-6)*1000],
        input_inrush_caponly_nominal_A=44e-6*25*2e-6/100e-9,
        input_inrush_caponly_corner_A=44e-6*1.2*26*2.225e-6/90e-9,
        shunt_drop_mV=5*0.002*1000,shunt_loss_W=25*0.002,
        shunt_analog_range_A=0.04096/0.002,
        current_lsb_A=10/(2**19),shunt_cal=4*13107.2e6*(10/(2**19))*0.002,
        filter_corner_Hz=1/(2*math.pi*20*100e-9),
        local_bus_rise_at_100pF_ns=0.8473*10e3*100e-12*1e9,
        host_bus_rise_at_200pF_ns=0.8473*4.7e3*200e-12*1e9,
        lm74800_min_trip_for_normal_5p162V=5.162*(1.267/1.195),
        fault_example_current_increase_5p4us_A=(24-5.1)/6.8e-6*5.4e-6,
        fault_example_cap_rise_100uF_5p4us_V=(24-5.1)/6.8e-6*(5.4e-6)**2/(2*100e-6))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    values = calculate()
    result = json.dumps(values,indent=2)+'\n'
    if args.output:
        if args.output.exists():
            parser.error('Output exists; use a new path and compare before replacing evidence.')
        args.output.write_text(result)
    else:
        print(result,end='')


if __name__ == '__main__':
    main()
