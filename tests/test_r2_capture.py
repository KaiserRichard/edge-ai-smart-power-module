"""Regression checks for dangerous netlist mistakes, using the exported KiCad evidence."""
import copy
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location('r2_check', ROOT/'scripts/check_r2_schematic.py')
checker = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(checker)


class CaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = ET.parse(ROOT/'docs/evidence/r2/V1A.net.xml').getroot()
        cls.specs = checker.load_specs(ROOT/'docs/evidence/r2')

    def move_pin(self, tree, ref, pin, target):
        found = False
        destination = next(n for n in tree.findall('./nets/net')
                           if n.attrib['name'].rsplit('/',1)[-1] == target)
        for net in tree.findall('./nets/net'):
            for node in list(net):
                if node.attrib.get('ref') == ref and node.attrib.get('pin') == pin:
                    net.remove(node)
                    destination.append(node)
                    found = True
                    break
            if found:
                break
        self.assertTrue(found)

    def test_review_capture_matches_contracts(self):
        self.assertEqual(checker.validate(self.tree, self.specs), [])

    def test_reversed_kelvin_sense_is_rejected(self):
        tree = copy.deepcopy(self.tree)
        self.move_pin(tree, 'U401', '10', 'INA_IN_MINUS')
        self.assertTrue(checker.validate(tree, self.specs))

    def test_host_pullup_to_live_local_rail_is_rejected(self):
        tree = copy.deepcopy(self.tree)
        self.move_pin(tree, 'R406', '1', '3V3_LOCAL')
        self.assertTrue(checker.validate(tree, self.specs))

    def test_q102_source_must_follow_input_not_ground(self):
        tree = copy.deepcopy(self.tree)
        self.move_pin(tree, 'Q102', '2', 'GND')
        self.assertTrue(checker.validate(tree, self.specs))

    def test_output_boundary_cannot_be_shortened_even_in_both_contracts(self):
        tree = copy.deepcopy(self.tree)
        specs = copy.deepcopy(self.specs)
        self.move_pin(tree, 'U402', '1', 'VOUT_5V1')
        specs['U402']['pins']['1']['net'] = 'VOUT_5V1'
        self.assertTrue(checker.validate(tree, specs))


if __name__ == '__main__':
    unittest.main()
