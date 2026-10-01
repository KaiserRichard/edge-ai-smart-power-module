#!/usr/bin/env python3
"""Check an exported KiCad XML netlist against R2 pin contracts and boundaries.

This checks capture integrity, not electrical safety, fault let-through or PCB layout.
"""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def load_specs(spec_dir):
    return {c['ref']: c for block in ('input', 'buck', 'output', 'monitor', 'io')
            for c in json.loads((spec_dir / f'{block}_block.json').read_text())['components']}


def validate(tree, specs, profile="gate2"):
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

    if profile == "gate4b":
        from check_gate4b_contracts import validate as validate_gate4b
        return errors + validate_gate4b(tree, specs)

    # Gate2 authorizes this concrete capture, not arbitrary replacement of the
    # old open stub. These invariants are independent of the editable pin JSON.
    sheet03 = {
        ('U201','5'): 'BUCK_PGOOD', ('U101','12'): 'INPUT_SHDN',
        ('U301','1'): 'DRV_7V5', ('U301','2'): 'GND', ('U301','3'): 'GND',
        ('U301','4'): 'RUN_GATE', ('U301','5'): 'GND',
        ('U301','6'): 'PROT_GATE', ('U301','7'): 'TGUP_SLOW',
        ('U301','8'): 'PROT_MID', ('U301','9'): 'PROT_BST', ('U301','11'): 'GND',
        ('U302','2'): 'DET_5V', ('U302','4'): 'GND', ('U302','6'): 'REF_2V5',
        ('U303','1'): 'OV_OK', ('U303','2'): 'GND', ('U303','3'): 'REF_2V5',
        ('U303','4'): 'OV_SENSE', ('U303','5'): 'DET_5V',
        ('U315','1'): 'DRV_7V5', ('U315','2'): 'CB_GATE_UP',
        ('U315','3'): 'CB_GATE', ('U315','4'): 'GND',
        ('U315','5'): 'GND', ('U315','6'): 'CROWBAR_ON',
        ('R301','1'): 'VOUT_5V1', ('R301','2'): 'OV_DIV',
        ('R302','1'): 'OV_DIV', ('R302','2'): 'GND',
        ('R303','1'): 'OV_DIV', ('R303','2'): 'OV_SENSE',
        ('R304','1'): 'TGUP_SLOW', ('R304','2'): 'PROT_GATE',
        ('R305','1'): 'PROT_GATE', ('R305','2'): 'PROT_MID',
        ('R306','1'): 'CB_GATE_UP', ('R306','2'): 'CB_GATE',
        ('R307','1'): 'CB_GATE', ('R307','2'): 'GND',
        ('D301','1'): 'OV_DIV', ('D301','3'): 'REF_2V5',
        ('D302','1'): 'DRV_7V5', ('D302','3'): 'PROT_BST',
        ('D303','1'): 'VIN_FUSED', ('D303','2'): 'VIN_AUX',
        ('C301','1'): 'PROT_BST', ('C301','2'): 'PROT_MID',
        ('Q304','1'): 'CROWBAR_ON', ('Q304','2'): 'GND', ('Q304','3'): 'INPUT_SHDN',
    }
    for ref, source, gate, drain in (
            ('Q301','PROT_MID','PROT_GATE','VOUT_5V1'),
            ('Q302','PROT_MID','PROT_GATE','VOUT_PROTECTED'),
            ('Q303','GND','CB_GATE','CB_DRAIN')):
        sheet03.update({(ref,str(n)): source for n in (1,2,3)})
        sheet03[(ref,'4')] = gate
        sheet03.update({(ref,str(n)): drain for n in (5,6,7,8)})
    logic = {
        'U304': ['ARM_CLOCK','DET_5V','ARM_LATCH_N','GND','ARM_LATCH','QUALIFIED','DET_5V','DET_5V'],
        'U309': ['ARM_DELAYED','ARM_LATCH',None,'GND','ARM_HISTORY','CTRL_ENABLE','DET_5V','DET_5V'],
        'U305': ['ARM_LATCH','GND','ARM_HISTORY','RUN_GATE','DET_5V','QUALIFIED'],
        'U310': ['CTRL_ENABLE','GND','OV_OK','QUALIFIED','DET_5V','BUCK_PGOOD'],
        'U311': ['ARM_HISTORY','GND','ARM_LATCH_N','CROWBAR_ON','DET_5V','CTRL_ENABLE'],
        'U312': ['SUPPLY_OK','RESET_N','GND','CTRL_ENABLE','DET_5V'],
        'U313': [None,'ARM_N','GND','ARM_CLOCK','DET_5V'],
        'U314': [None,'ARM_RC','GND','ARM_DELAYED','DET_5V'],
        'U308': ['SUPPLY_OK','GND','RESET_N','REF_DELAY','REF_2V5','DET_5V'],
        'U306': ['DET_5V','DET_FB','SUPPLY_OK','GND','VIN_AUX',None,'DET_DELAY','VIN_AUX','GND'],
        'U307': ['DRV_7V5','DRV_FB','SUPPLY_OK','GND','VIN_AUX',None,'DRV_DELAY','VIN_AUX','GND'],
    }
    for ref, assignments in logic.items():
        for n, wanted in enumerate(assignments,1):
            if wanted is not None:
                sheet03[(ref,str(n))] = wanted
            elif nets.get((ref,str(n)), '').startswith('unconnected-') is False:
                errors.append(f'Sheet03 independent NC violation: {ref}.{n}')
    for ref, a, b in [('R308','VOUT_PROTECTED','CB_R_A'),('R309','CB_R_A','CB_DRAIN'),
                      ('R310','VOUT_PROTECTED','CB_R_B'),('R311','CB_R_B','CB_DRAIN')]:
        sheet03[(ref,'1')], sheet03[(ref,'2')] = a, b
    for n in range(330,338):
        sheet03[(f'C{n}','1')], sheet03[(f'C{n}','2')] = 'VOUT_5V1', 'GND'
    for key, wanted in sheet03.items():
        if nets.get(key, '').rsplit('/',1)[-1] != wanted:
            errors.append(f'Sheet03 independent boundary violation: {key} must be on {wanted}')
    # Do not grant a clean ERC by declaring an unfitted source. Require both
    # named declarations AND their complete physical paths checked above.
    for ref, wanted in [('#FLG301','VIN_AUX'),('#FLG302','VOUT_PROTECTED')]:
        c = specs.get(ref, {})
        if c.get('pins',{}).get('1',{}).get('net') != wanted or c.get('kind') != 'FLAG':
            errors.append(f'Missing/wrong conditional source declaration: {ref}')
    protected = nets.get(('U402', '1'))
    raw = nets.get(('R202', '1'))
    if raw == protected:
        errors.append('Raw/protected nets directly merged')
    for ref, c in specs.items():
        if c['kind'] in ('R', 'L', 'F', 'D', 'CONNECTOR'):
            touched = {nets.get((ref, n)) for n in c['pins']}
            if raw in touched and protected in touched:
                errors.append(f'Forbidden bypass across output protection: {ref}')
    # Detect multiple passive elements forming a bypass. Ignore capacitors and
    # the ground return; transistor channels are the ONLY accepted power path.
    graph = {}
    for c in tree.findall('./components/comp'):
        ref = c.attrib['ref']
        if not ref.startswith(('R','L','F','D','J')): continue
        touched = {v for (r,p),v in nets.items() if r == ref
                   and v.rsplit('/',1)[-1] != 'GND' and not v.startswith('unconnected-')}
        for a in touched:
            graph.setdefault(a,set()).update(touched - {a})
    seen, pending = set(), [raw]
    while pending:
        node = pending.pop()
        if node in seen: continue
        seen.add(node); pending.extend(graph.get(node,set()) - seen)
    if protected in seen:
        errors.append('Passive bypass path around opposed MOSFETs')
    return errors


def validate_sheet03_packages(tree, specs, footprints=None, profile="gate2"):
    """Verify manufacturer pin identities and every copper pad independently.

    Manufacturer ledger is separate from the connection specification, so a
    corrupted symbol and connection JSON cannot quietly agree on a bad pinout.
    """
    ledger_dir = 'gate4b' if profile == 'gate4b' else 'sheet03'
    ledger = json.loads((ROOT/f'docs/evidence/r2/{ledger_dir}/PIN_CONTRACTS.json').read_text())
    libraries = {(c.get('lib'),c.get('part')): c for c in tree.findall('./libparts/libpart')}
    errors=[]
    for c in tree.findall('./components/comp'):
        if c.find('sheetpath').get('names') != '/03_OUTPUT_PROTECTION/': continue
        ref=c.get('ref'); spec=specs[ref]
        lib=c.find('libsource'); symbol=libraries.get((lib.get('lib'),lib.get('part')))
        if symbol is None:
            errors.append(f'{ref}: exported library symbol missing')
            continue
        actual={p.get('num'): p.get('name') for p in symbol.findall('./pins/pin')}
        expected=ledger['parts'].get(spec['part'])
        if expected is None and spec['kind'] in ('IC', 'MOSFET', 'D', 'TVS'):
            errors.append(f'{ref}: missing independent manufacturer pin ledger')
        if expected and actual != expected['pins']:
            errors.append(f'{ref}: symbol pin identity differs from manufacturer ledger')
        if set(actual) != set(spec['pins']):
            errors.append(f'{ref}: symbol/spec pin count differs')
        fp=c.findtext('footprint','')
        if not fp or fp != spec['footprint']:
            errors.append(f'{ref}: missing/wrong footprint assignment')
            continue
        if footprints is not None:
            library,name=fp.split(':')
            path=(ROOT/'hardware/kicad/V1A_Qualified.pretty' if library == 'V1A_Qualified'
                  else footprints/(library+'.pretty'))/(name+'.kicad_mod')
            if not path.is_file():
                errors.append(f'{ref}: footprint file missing: {fp}'); continue
            # Parse complete pad forms: stock KiCad footprints span lines.
            from build_sheet03_preliminary import children
            pads = set()
            for _, _, form in children(path.read_text()):
                if not form.startswith('(pad '):
                    continue
                number = re.match(r'\(pad "([^"]*)"', form)[1]
                layers = re.search(r'\(layers ([^)]+)\)', form)[1]
                if number and any(layer in layers for layer in ('F.Cu', 'B.Cu', '*.Cu')):
                    pads.add(number)
            # Empty numbers belong to paste-only apertures, never electrical pins.
            if pads != set(actual):
                errors.append(f'{ref}: footprint pads {sorted(pads)} != symbol pins {sorted(actual)}')
    return errors


def validate_footprint_assignments(tree, footprints=None, exclusions=None):
    """All physical symbols need real footprints except the three owner holds.

    Existing generic passive lands are real geometry, not full BOM qualification.
    The exclusion does not authorize selection or a change of the held parts.
    """
    from check_footprint_completion import EXCLUSIONS
    if exclusions is None: exclusions = EXCLUSIONS
    from build_sheet03_preliminary import children
    libraries = {(c.get('lib'), c.get('part')): c for c in tree.findall('./libparts/libpart')}
    errors = []
    for c in tree.findall('./components/comp'):
        ref, fp = c.get('ref'), c.findtext('footprint', '').strip()
        placeholder = not fp or ':' not in fp or bool(re.search(r'(?i)(?:OPEN|TBD|PLACEHOLDER|UNASSIGNED)', fp))
        if placeholder:
            if ref not in exclusions:
                errors.append(f'{ref}: empty/placeholder footprint is not an authorized exclusion')
            continue
        if footprints is None:
            continue
        library, name = fp.split(':', 1)
        path = (ROOT/'hardware/kicad/V1A_Qualified.pretty' if library == 'V1A_Qualified'
                else footprints/(library+'.pretty'))/(name+'.kicad_mod')
        if not path.is_file():
            errors.append(f'{ref}: footprint file missing: {fp}')
            continue
        lib = c.find('libsource')
        symbol = libraries.get((lib.get('lib'), lib.get('part')))
        if symbol is None:
            errors.append(f'{ref}: missing exported library definition')
            continue
        pins = {p.get('num') for p in symbol.findall('./pins/pin')}
        pads = set()
        for _, _, form in children(path.read_text()):
            if not form.startswith('(pad '):
                continue
            n = re.match(r'\(pad "([^"]*)"', form)[1]
            layers = re.search(r'\(layers ([^)]+)\)', form)[1]
            if n and any(layer in layers for layer in ('F.Cu', 'B.Cu', '*.Cu')):
                pads.add(n)
        if pads != pins:
            errors.append(f'{ref}: footprint copper numbers {sorted(pads)} != symbol pins {sorted(pins)}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, required=True)
    parser.add_argument('--spec-dir', type=Path)
    parser.add_argument('--profile', choices=('gate2','gate4b'), default='gate4b', help='Gate2 preserves historical PR15 evidence; Gate4B checks current capture')
    parser.add_argument('--footprints', type=Path, help='KiCad installed footprint root; additionally verify all physical copper-pad numbers')
    args = parser.parse_args()
    spec_dir=args.spec_dir or ROOT/('docs/evidence/r2/gate4b' if args.profile=='gate4b' else 'docs/evidence/r2')
    tree, specs = ET.parse(args.netlist).getroot(), load_specs(spec_dir)
    errors = (validate(tree, specs, args.profile) + validate_sheet03_packages(tree, specs, args.footprints, args.profile)
              + validate_footprint_assignments(tree, args.footprints, set() if args.profile=="gate4b" else None))
    if list((ROOT / 'hardware').rglob('*.kicad_pcb')):
        errors.append('R3 scope violation: authored PCB found')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print('PASS: pin contracts, hierarchy, Kelvin polarity, power domains, Sheet03 control and no-bypass boundaries.')
    print('R2 RELEASE BLOCKED: capture integrity is not electrical validation.')


if __name__ == '__main__':
    main()
