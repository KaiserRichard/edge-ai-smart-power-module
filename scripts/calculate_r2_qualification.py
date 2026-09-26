#!/usr/bin/env python3
"""Reproduce fuse input-current and candidate harness loss sensitivity screens."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT/'docs/evidence/r2/forensic_2026-09-14/qualification_assumptions.json'


def calculate(c):
    wire = 2*c['wire_one_way_m']*c['wire_nominal_ohm_per_1000ft']/304.8*1000
    wire_hot = wire*(1+c['copper_temperature_coefficient_per_C_assumed']*(c['wire_hot_temperature_C_assumed']-c['wire_reference_temperature_C_assumed']))
    fixed = c['output_switch_mOhm_assumed']+c['pcb_loop_mOhm_assumed']+c['shunt_mOhm_datasheet_nominal']+c['adapter_joints_mOhm_assumed']+c['pi_contacts_loop_mOhm_assumed']
    phoenix = c['phoenix_header_loop_mOhm_additive_screen']+c['phoenix_mate_loop_mOhm_additive_screen']
    scenarios = [
        ('Phoenix additive room screen',phoenix,wire),
        ('Phoenix additive hot sensitivity',phoenix*c['contact_hot_multiplier_assumed'],wire_hot),
        ('JST VH initial room maximum screen',c['jst_vh_mated_loop_initial_mOhm_datasheet_max'],wire),
        ('JST VH after-test room maximum screen',c['jst_vh_mated_loop_after_test_mOhm_datasheet_max'],wire),
        ('JST VH after-test hot sensitivity',c['jst_vh_mated_loop_after_test_mOhm_datasheet_max']*c['contact_hot_multiplier_assumed'],wire_hot)]
    results = []
    for name,contact,cable in scenarios:
        total = (fixed+contact+cable)/1000
        points = []
        for current in c['loads_A']:
            drop = current*total
            points.append(dict(current_A=current,drop_V=drop,loss_W=current**2*total,
                               pi_nominal_V=c['nominal_regulation_V']-drop,
                               pi_static_low_V=c['static_low_regulation_V_assumed']-drop,
                               pi_static_low_minus_droop_V=c['static_low_regulation_V_assumed']-drop-c['dynamic_droop_V_assumed']))
        results.append(dict(scenario=name,connector_loop_mOhm=contact,wire_loop_mOhm=cable,total_loop_mOhm=total*1000,points=points))
    return dict(classification='CALCULATED sensitivity only; no measured or guaranteed end-to-end result',
                wire_room_mOhm=wire,wire_hot_mOhm=wire_hot,fixed_assumed_plus_nominal_shunt_mOhm=fixed,
                fuse_input_currents=[dict(vin_V=v,efficiency_assumed=e,input_A=c['output_W_requirement']/(v*e)) for v in c['input_V_requirement'] for e in c['efficiencies_assumed']],
                harness_scenarios=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=DEFAULT)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    values = calculate(json.loads(args.config.read_text()))
    values['config_sha256'] = hashlib.sha256(args.config.read_bytes()).hexdigest()
    text = json.dumps(values,indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(text)
    else:
        print(text,end='')


if __name__ == '__main__':
    main()
