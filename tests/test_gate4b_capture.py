"""Current test-board integrity and adversarial boundary regressions.

These check the KiCad export independently of its editable block specifications.
They do not simulate analog timing, partial power, or prove electrical safety.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import check_r2_schematic as checker


class Gate4BCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = ET.parse(ROOT/'docs/evidence/r2/gate4b/captured.xml').getroot()
        cls.specs = checker.load_specs(ROOT/'docs/evidence/r2/gate4b')

    def validate(self, tree, specs):
        return checker.validate(tree, specs, 'gate4b')

    def move(self, tree, specs, ref, pin, target):
        dest = next(n for n in tree.findall('./nets/net')
                    if n.get('name').rsplit('/', 1)[-1] == target)
        for net in tree.findall('./nets/net'):
            for node in list(net):
                if (node.get('ref'), node.get('pin')) == (ref, pin):
                    net.remove(node)
                    dest.append(node)
                    specs[ref]['pins'][pin]['net'] = target
                    return
        self.fail(f'Missing mutation target {ref}.{pin}')

    def test_current_capture_and_all_footprints(self):
        self.assertEqual(self.validate(self.tree, self.specs), [])
        self.assertEqual(checker.validate_sheet03_packages(self.tree, self.specs, profile='gate4b'), [])
        self.assertEqual(checker.validate_footprint_assignments(self.tree, exclusions=set()), [])

    def test_source_hook_cannot_be_replaced_with_pg(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'U615', '1', 'PG_GOOD')
        self.assertTrue(any('U615.1' in e for e in self.validate(tree, specs)))

    def test_pg_loss_cannot_fire_disposal(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'U633', '1', 'PG_GOOD')
        self.assertTrue(any('U633.1' in e for e in self.validate(tree, specs)))

    def test_fault_priority_cannot_be_removed_from_reset(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'U610', '6', 'SAFE5')
        self.assertTrue(any('U610.6' in e for e in self.validate(tree, specs)))

    def test_pg_recovery_cannot_clock_series_arm(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'U611', '1', 'PG_GOOD')
        self.assertTrue(any('U611.1' in e for e in self.validate(tree, specs)))

    def test_series_link_cannot_bypass_opposed_pair(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'JP301', '1', 'VOUT_5V1')
        self.assertTrue(any('bypass' in e for e in self.validate(tree, specs)))

    def test_bootstrap_return_cannot_be_ground(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'C301', '2', 'GND')
        self.assertTrue(any('C301.2' in e for e in self.validate(tree, specs)))

    def test_compensation_must_return_to_feedback(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'C356', '2', 'GND')
        self.assertTrue(any('C356.2' in e for e in self.validate(tree, specs)))

    def test_exact_hold_capacitor_lead_pitch(self):
        tree = copy.deepcopy(self.tree)
        tree.find('./components/comp[@ref="C358"]/footprint').text = 'Capacitor_THT:CP_Radial_D6.3mm_P2.50mm'
        self.assertTrue(any('C358' in e for e in self.validate(tree, self.specs)))

    def test_charger_has_no_fictitious_exposed_pad(self):
        tree = copy.deepcopy(self.tree)
        p = next(p for p in tree.findall('./libparts/libpart') if p.get('part').startswith('U327_'))
        ET.SubElement(p.find('pins'), 'pin', num='11', name='EP')
        self.assertTrue(checker.validate_sheet03_packages(tree, self.specs, profile='gate4b'))

    def test_permission_cannot_be_declared_as_power(self):
        specs = copy.deepcopy(self.specs)
        specs['#FLG306']['pins']['1']['net'] = 'MANUAL_RAILS_VALID'
        self.assertTrue(any('Power declaration' in e for e in self.validate(self.tree, specs)))

    def test_kelvin_filter_cannot_become_a_ground_filter(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'C401', '2', 'GND')
        self.assertTrue(any('C401.2' in e for e in self.validate(tree, specs)))

    def test_host_reference_cannot_power_local_domain(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'U403', '8', '3V3_HOST')
        self.assertTrue(any('U403' in e for e in self.validate(tree, specs)))

    def test_output_connector_cannot_be_moved_before_protection(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'J502', '1', 'VOUT_5V1')
        self.assertTrue(any('J502.1' in e for e in self.validate(tree, specs)))

    def test_native_switch_and_injection_force_pads_stay_distinct(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move(tree, specs, 'PF4', '1', 'BUCK_SW')
        self.assertTrue(any('PF4.1' in e for e in self.validate(tree, specs)))

    def test_netclasses_cover_force_kelvin_switching_and_signal(self):
        project_path = ROOT/'hardware/kicad/V1A.kicad_pro'
        project = json.loads(project_path.read_text())
        rules = {p['pattern']: p['netclass'] for p in project['net_settings']['netclass_patterns']}
        nets = {n.get('name') for n in self.tree.findall('./nets/net') if not n.get('name').startswith('unconnected-')}
        self.assertEqual(set(rules), nets)
        expected = {'GND':'HighCurrent', 'VIN_RAW':'HighCurrent', 'VOUT_PROTECTED':'HighCurrent',
                    'RAW_A3':'HighCurrent', 'CB_DRAIN':'HighCurrent', 'PROT_MID':'HighCurrent',
                    'BUCK_SW':'Switching', 'L201_IN':'Switching', 'AUX_SW2':'Switching',
                    'SHUNT_KPLUS':'Kelvin', 'SHUNT_KMINUS':'Kelvin', 'INA_IN_PLUS':'Kelvin',
                    'INPUT_SHDN':'Signal', 'MANUAL_RAILS_VALID':'Signal'}
        by_leaf = {n.rsplit('/',1)[-1]: c for n,c in rules.items()}
        for n,c in expected.items():
            self.assertEqual(by_leaf[n], c, n)
        review = json.loads((ROOT/'docs/evidence/r2/gate4b/NET_CLASSES.json').read_text())
        self.assertEqual(review['project_sha256'], hashlib.sha256(project_path.read_bytes()).hexdigest())
        self.assertEqual(review['pdf_sha256'], hashlib.sha256((ROOT/'docs/evidence/r2/gate4b/V1A_GATE4B_REVIEW.pdf').read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
