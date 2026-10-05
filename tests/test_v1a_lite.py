"""Reject dangerous protection-boundary mutations in the exported Lite netlist."""
import copy
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_v1a_lite import validate

@unittest.skipUnless('V1A-Lite / V1A' in (ROOT/'hardware/kicad/V1A.kicad_sch').read_text(),'V1A-Lite capture only')
class LiteBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.tree=ET.parse(ROOT/'docs/evidence/v1a_lite/V1A_LITE.net.xml').getroot()
    def moved(self,ref,pin,target):
        tree=copy.deepcopy(self.tree)
        dest=next(n for n in tree.findall('./nets/net') if n.get('name')==target)
        for net in tree.findall('./nets/net'):
            for node in list(net):
                if (node.get('ref'),node.get('pin'))==(ref,pin):net.remove(node);dest.append(node);return tree
        self.fail('Mutation target missing')
    def test_capture(self):self.assertEqual(validate(self.tree)['errors'],[])
    def test_fuse_must_not_disconnect_raw_crowbar(self):
        self.assertTrue(validate(self.moved('SCR301','2','/VOUT_PI'))['errors'])
    def test_latch_must_not_lose_supply_when_output_collapses(self):
        self.assertTrue(validate(self.moved('Q105','2','/VOUT_5V1'))['errors'])
    def test_cutoff_must_act_on_q103_base(self):
        self.assertTrue(validate(self.moved('Q106','3','/VOUT_PI'))['errors'])
    def test_pi_must_not_bypass_wiring_fuse(self):
        self.assertTrue(validate(self.moved('J502','1','/VOUT_5V1'))['errors'])
