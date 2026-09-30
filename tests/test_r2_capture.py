"""Regression checks for dangerous netlist mistakes, using the exported KiCad evidence."""
import copy
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))

ROOT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location('r2_check', ROOT/'scripts/check_r2_schematic.py')
checker = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(checker)


class CaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = ET.parse(ROOT/'docs/evidence/r2/sheet03/readability/readable.net.xml').getroot()
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

    def test_ucc27511_input_pin_error_rejected_even_when_spec_agrees(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move_pin(tree, 'U315', '6', 'GND')
        specs['U315']['pins']['6']['net'] = 'GND'
        self.assertTrue(any('U315' in e for e in checker.validate(tree, specs)))

    def test_series_fet_source_reference_must_not_follow_output_drain(self):
        tree, specs = copy.deepcopy(self.tree), copy.deepcopy(self.specs)
        self.move_pin(tree, 'U301', '8', 'VOUT_PROTECTED')
        specs['U301']['pins']['8']['net'] = 'VOUT_PROTECTED'
        self.assertTrue(any('U301' in e for e in checker.validate(tree, specs)))

    def test_manufacturer_pin_identity_rejects_swapped_driver_outputs(self):
        tree = copy.deepcopy(self.tree)
        part = next(p for p in tree.findall('./libparts/libpart')
                    if p.get('part').startswith('U315_'))
        next(p for p in part.findall('./pins/pin') if p.get('num') == '2').set('name', 'OUTL')
        self.assertTrue(checker.validate_sheet03_packages(tree, self.specs))

    def test_current_manufacturer_pin_identities(self):
        self.assertEqual(checker.validate_sheet03_packages(self.tree, self.specs), [])

    def test_series_fet_footprint_has_every_physical_terminal(self):
        # Infineon Rev2.3 p1: 1..3 source, 4 gate, 5..8 drain.
        from build_sheet03_preliminary import children
        import re
        path = ROOT/'hardware/kicad/V1A_Qualified.pretty/Infineon_BSC034N06NS_8pin.kicad_mod'
        pads = {}
        for _, _, form in children(path.read_text()):
            if form.startswith('(pad ') and 'F.Cu' in form:
                n = re.match(r'\(pad "([^"]+)"', form)[1]
                xy = tuple(map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+)',form).groups()))
                pads.setdefault(n, []).append(xy)
        self.assertEqual(set(pads), {str(i) for i in range(1,9)})
        for n, y in [('8',-1.995),('7',-.665),('6',.665),('5',1.995)]:
            self.assertTrue(any(x > 2 and actual_y == y for x, actual_y in pads[n]))


if __name__ == '__main__':
    unittest.main()
