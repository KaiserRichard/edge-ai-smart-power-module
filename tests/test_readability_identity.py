"""Guard the electrical equality proof against changes hidden by formatting."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_schematic_readability import canonical_netlist, source_inventory, EVIDENCE
from make_schematic_readable import source, nodes, prop, val, one


class IdentityTests(unittest.TestCase):
    def compare_mutation(self, mutate):
        original=EVIDENCE/'baseline.net.xml'
        tree=ET.parse(original);mutate(tree.getroot())
        with tempfile.TemporaryDirectory() as scratch:
            modified=Path(scratch)/'changed.xml';tree.write(modified)
            return canonical_netlist(original)==canonical_netlist(modified)

    def test_value_change_is_rejected(self):
        self.assertFalse(self.compare_mutation(lambda root:setattr(root.find('./components/comp/value'),'text','CHANGED')))

    def test_pin_membership_change_is_rejected(self):
        self.assertFalse(self.compare_mutation(lambda root:root.find('./nets/net/node').set('pin','999')))

    def test_footprint_change_is_rejected(self):
        self.assertFalse(self.compare_mutation(lambda root:setattr(root.find('./components/comp/footprint'),'text','CHANGED')))

    def test_only_export_order_and_codes_are_ignored(self):
        def mutate(root):
            for net in root.findall('./nets/net'):net.set('code','999');net[:]=list(reversed(net[:]))
            root.find('./design/date').text='another export time'
        self.assertTrue(self.compare_mutation(mutate))

    def test_power_flags_cannot_disappear_from_source_inventory(self):
        doc=source('05_IO_TEST.kicad_sch');before=source_inventory(doc)
        flag=next(s for s in nodes(doc,'symbol') if val(prop(s,'Reference')[2]).startswith('#FLG'))
        doc.remove(flag)
        self.assertNotEqual(before,source_inventory(doc))

if __name__=='__main__':unittest.main()
