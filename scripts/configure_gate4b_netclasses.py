#!/usr/bin/env python3
"""Assign reviewed net categories from a fresh export; does not create a PCB.

Track/via dimensions are ASSUMED editor presets, not rated copper geometry.
R3 must establish stackup, continuous/pulse current, voltage and thermal rules.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HIGH_CURRENT = {
    'VIN_RAW', 'VIN_FUSED', 'VIN_EFUSE_IN', 'EFUSE_OUT', 'VIN_PROTECTED',
    'L201_OUT', 'VOUT_5V1', 'PROT_MID', 'SERIES_OUT', 'VOUT_PROTECTED',
    'LOAD_5V1', 'LOAD_FIXTURE', 'GND', 'CB_R_A', 'CB_R_B',
    'CB_BALLAST_OUT', 'CB_DRAIN', 'RAW_BALLAST_OUT', 'RAW_DUMP_DRAIN',
}
SWITCHING = {'BUCK_SW', 'L201_IN', 'AUX_SW1', 'AUX_SW2'}
KELVIN = {'SHUNT_KPLUS', 'SHUNT_KMINUS', 'INA_IN_PLUS', 'INA_IN_MINUS'}


def classify(net):
    leaf = net.rsplit('/', 1)[-1]
    if leaf in SWITCHING:
        return 'Switching'
    if leaf in KELVIN:
        return 'Kelvin'
    if leaf in HIGH_CURRENT or re.fullmatch(r'RAW_[AB][1-5]', leaf):
        return 'HighCurrent'
    return 'Signal'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, required=True)
    args = parser.parse_args()
    p = ROOT/'hardware/kicad/V1A.kicad_pro'
    project = json.loads(p.read_text())
    default = next(c for c in project['net_settings']['classes'] if c['name'] == 'Default')
    classes = [default]
    for priority, (name, width) in enumerate([('HighCurrent', 2.0), ('Switching', 1.0), ('Kelvin', .2), ('Signal', .2)]):
        c = copy.deepcopy(default)
        c.update(name=name, priority=priority, track_width=width)
        classes.append(c)
    nets = sorted(n.get('name') for n in ET.parse(args.netlist).findall('./nets/net')
                  if not n.get('name').startswith('unconnected-'))
    project['net_settings']['classes'] = classes
    project['net_settings']['netclass_patterns'] = [dict(pattern=n, netclass=classify(n)) for n in nets]
    p.write_text(json.dumps(project, indent=2)+'\n')
    print(f'Assigned {len(nets)} named nets; widths are provisional editor presets only.')


if __name__ == '__main__':
    main()
