#!/usr/bin/env python3
"""Check an exported KiCad XML netlist against R2 pin contracts and boundaries.

This checks capture integrity, not electrical safety, fault let-through or PCB layout.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def load_specs(spec_dir):
    return {c['ref']: c for block in ('input', 'buck', 'output', 'monitor', 'io')
            for c in json.loads((spec_dir / f'{block}_block.json').read_text())['components']}


def validate(tree, specs):
    errors = []
    nets = {}
    for net in tree.findall('./nets/net'):
        for node in net.findall('node'):
            key = (node.attrib['ref'], node.attrib['pin'])
            if key in nets:
                errors.append(f'Duplicate exported pin: {key}')
            nets[key] = net.attrib['name']
    actual_refs = {c.attrib['ref'] for c in tree.findall('./components/comp')}
    wanted_refs = {ref for ref, c in specs.items() if c['kind'] != 'FLAG'}
    if actual_refs != wanted_refs:
        errors.append(f'Component mismatch: {actual_refs ^ wanted_refs}')
    expected_groups = {}
    for ref, c in specs.items():
        if c['kind'] == 'FLAG':
            continue
        for number, pin in c['pins'].items():
            actual = nets.get((ref, number), '')
            wanted = pin['net']
            if wanted is None:
                if actual and not actual.startswith('unconnected-'):
                    errors.append(f'{ref}.{number}: intentional NC was connected to {actual}')
            elif actual.rsplit('/', 1)[-1] != wanted:
                errors.append(f'{ref}.{number}: expected {wanted}, got {actual or "MISSING"}')
            else:
                expected_groups.setdefault(wanted, set()).add(actual)
    for name, real_nets in expected_groups.items():
        if len(real_nets) != 1:
            errors.append(f'Hierarchy split {name} across {sorted(real_nets)}')

    # Independent, manufacturer-derived invariants also catch corrupted JSON contracts.
    critical = {
        ('U201', '1'): 'GND', ('U201', '8'): 'VIN_PROTECTED',
        ('U201', '12'): 'VIN_PROTECTED', ('U201', '10'): 'BUCK_SW',
        ('U201', '4'): 'BUCK_FB', ('R202', '1'): 'VOUT_5V1',
        ('U101', '5'): 'VIN_FUSED', ('U101', '16'): 'BUCK_INPUT_PGOOD',
        ('Q101', '1'): 'VIN_FUSED', ('Q101', '2'): 'VIN_FUSED',
        ('Q101', '3'): 'VIN_FUSED', ('Q101', '4'): 'INPUT_BGATE',
        ('Q101', '5'): 'VIN_EFUSE_IN', ('Q101', '8'): 'VIN_EFUSE_IN',
        ('Q102', '1'): 'INPUT_DRV', ('Q102', '2'): 'VIN_FUSED',
        ('Q102', '3'): 'INPUT_BGATE',
        ('R401', '1'): 'VOUT_PROTECTED', ('R401', '2'): 'SHUNT_KPLUS',
        ('R401', '3'): 'SHUNT_KMINUS', ('R401', '4'): 'LOAD_5V1',
        ('U401', '8'): 'LOAD_5V1', ('U401', '9'): 'INA_IN_MINUS',
        ('U401', '10'): 'INA_IN_PLUS', ('U401', '1'): 'GND', ('U401', '2'): 'GND',
        ('U402', '1'): 'VOUT_PROTECTED', ('U402', '5'): '3V3_LOCAL',
        ('U403', '1'): '3V3_HOST', ('U403', '8'): '3V3_LOCAL',
        ('U403', '2'): 'SCL_HOST', ('U403', '3'): 'SDA_HOST',
        ('U403', '6'): 'SDA_LOCAL', ('U403', '7'): 'SCL_LOCAL',
        ('R406', '1'): '3V3_HOST', ('R407', '1'): '3V3_HOST',
        ('R408', '1'): '3V3_LOCAL', ('U401', '3'): 'ALERT_LOCAL',
    }
    for key, wanted in critical.items():
        if nets.get(key, '').rsplit('/', 1)[-1] != wanted:
            errors.append(f'Critical boundary violation: {key} must be on {wanted}')

    # A review stub may contain test points, but never a bypass element.
    output_parts = [c for c in specs.values() if c['ref'].startswith(('U3', 'Q3', 'R3', 'J3', 'D3'))]
    if output_parts:
        errors.append('Output protection release blocker changed: requires a new independent review')
    protected = nets.get(('U402', '1'))
    raw = nets.get(('R202', '1'))
    for ref, c in specs.items():
        if c['kind'] in ('R', 'L', 'F', 'D', 'CONNECTOR'):
            touched = {nets.get((ref, n)) for n in c['pins']}
            if raw in touched and protected in touched:
                errors.append(f'Forbidden bypass across output protection: {ref}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, required=True)
    parser.add_argument('--spec-dir', type=Path, default=ROOT / 'docs/evidence/r2')
    args = parser.parse_args()
    errors = validate(ET.parse(args.netlist).getroot(), load_specs(args.spec_dir))
    if list((ROOT / 'hardware').rglob('*.kicad_pcb')):
        errors.append('R3 scope violation: authored PCB found')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print('PASS: pin contracts, hierarchy, Kelvin polarity, power domains and open output boundary.')
    print('R2 RELEASE BLOCKED: capture integrity is not electrical validation.')


if __name__ == '__main__':
    main()
