"""Independent dimensional expectations and adversarial completion gates."""
import copy
from pathlib import Path
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_sheet03_preliminary import children
from check_footprint_completion import compare_netlists, normalized_source
from check_r2_schematic import validate_footprint_assignments

EVIDENCE = ROOT/'docs/evidence/r2/footprints_complete'


def pads(name):
    result = []
    for _, _, form in children((ROOT/'hardware/kicad/V1A_Qualified.pretty'/(name+'.kicad_mod')).read_text()):
        if not form.startswith('(pad '):
            continue
        result.append({'number': re.match(r'\(pad "([^"]*)"',form)[1],
                       'at': tuple(map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+)',form).groups())),
                       'size': tuple(map(float,re.search(r'\(size ([-\d.]+) ([-\d.]+)',form).groups())),
                       'drill': float(re.search(r'\(drill ([-\d.]+)',form)[1]) if '(drill ' in form else None,
                       'form': form})
    return result


class CompletionTests(unittest.TestCase):
    def test_all_nonexcluded_physical_footprints_present(self):
        tree = ET.parse(EVIDENCE/'completed.xml').getroot()
        self.assertEqual(validate_footprint_assignments(tree), [])

    def test_each_nonexcluded_empty_and_placeholder_is_rejected(self):
        original = ET.parse(EVIDENCE/'completed.xml').getroot()
        for comp in original.findall('./components/comp'):
            if comp.get('ref') in {'D101','F101','L201'}:
                continue
            for bad in ['', 'OPEN', 'SomeLib:TBD']:
                tree = copy.deepcopy(original)
                c = next(c for c in tree.findall('./components/comp') if c.get('ref') == comp.get('ref'))
                c.find('footprint').text = bad
                self.assertTrue(validate_footprint_assignments(tree), (comp.get('ref'),bad))

    def test_exclusions_are_exact_not_a_prefix_wildcard(self):
        tree = ET.parse(EVIDENCE/'completed.xml').getroot()
        f = next(c for c in tree.findall('./components/comp') if c.get('ref') == 'F101')
        f.set('ref','F102')
        self.assertTrue(validate_footprint_assignments(tree))

    def compare_mutation(self, mutate):
        tree = ET.parse(EVIDENCE/'completed.xml')
        mutate(tree.getroot())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'mutated.xml';tree.write(path)
            return compare_netlists(EVIDENCE/'baseline_1f4c2f8.xml',path)[0]

    def test_pin_net_and_library_changes_cannot_hide_behind_fields(self):
        for mutate in [lambda r:r.find('./nets/net/node').set('pin','999'),
                       lambda r:r.find('./nets/net').set('name','changed'),
                       lambda r:r.find('./libparts/libpart/pins/pin').set('name','changed'),
                       lambda r:r.find('./components/comp/sheetpath').set('names','changed')]:
            self.assertTrue(self.compare_mutation(mutate))

    def test_nonallowed_properties_are_preserved(self):
        def mutate(root):
            next(p for p in root.findall('./components/comp/property') if p.get('name')=='Rating').set('value','changed')
        self.assertTrue(self.compare_mutation(mutate))

    def test_held_parts_cannot_be_selected_through_field_allowlist(self):
        def mutate(root):
            f=next(c for c in root.findall('./components/comp') if c.get('ref')=='F101')
            ET.SubElement(f,'footprint').text='Fuse:Selected'
            next(p for p in f.findall('./fields/field') if p.get('name')=='Footprint').text='Fuse:Selected'
        self.assertTrue(self.compare_mutation(mutate))

    def test_source_position_and_wires_are_not_normalized_away(self):
        text=(ROOT/'hardware/kicad/02_BUCK_5V.kicad_sch').read_text()
        self.assertNotEqual(normalized_source(text),normalized_source(text.replace('(at ','(at 999 ',1)))
        self.assertNotEqual(normalized_source(text),normalized_source(text.replace('(wire','(changed_wire',1)))

    def test_tdk_b11_land_dimensions_and_nonpolar_numbering(self):
        p=pads('TDK_C5750_2220_A4.45_B1.30_C4.50')
        self.assertEqual([v['number'] for v in p],['1','2'])
        self.assertEqual([v['at'] for v in p],[(-2.875,0),(2.875,0)])
        self.assertTrue(all(v['size']==(1.3,4.5) and v['drill'] is None for v in p))
        self.assertAlmostEqual(p[1]['at'][0]-p[0]['at'][0]-1.3,4.45)
        self.assertTrue(all('"F.Paste"' in v['form'] for v in p))

    def test_jst_distinct_two_and_four_circuit_hole_diameters(self):
        for n,drill in [(2,1.0),(4,.95)]:
            p=pads(f'JST_B{n}B_XH_A_P2.50_THT')
            self.assertEqual([v['number'] for v in p],[str(i+1) for i in range(n)])
            self.assertEqual([v['at'] for v in p],[(i*2.5,0) for i in range(n)])
            self.assertTrue(all(v['drill']==drill and v['size']==(1.7,2) for v in p))
            self.assertIn('thru_hole rect',p[0]['form'])
            self.assertTrue(all('Paste' not in v['form'] for v in p))

    def test_vh_shrouded_boss_and_power_pins(self):
        p=pads('JST_B2P_VH_FB_B_P3.96_THT')
        boss=next(v for v in p if not v['number'])
        self.assertEqual((boss['at'],boss['drill']),((-1.5,-3.4),1.45))
        power=[v for v in p if v['number']]
        self.assertEqual([v['at'] for v in power],[(0,0),(3.96,0)])
        self.assertTrue(all(v['drill']==1.7 and v['size']==(2.7,2.7) for v in power))

    def test_phoenix_holes_do_not_create_extra_electrical_pins(self):
        p=pads('Phoenix_1776508_MSTB_2_GF_5.08')
        power=[v for v in p if v['number']];holes=[v for v in p if not v['number']]
        self.assertEqual([v['number'] for v in power],['1','2'])
        self.assertEqual([v['at'] for v in power],[(0,0),(5.08,0)])
        self.assertTrue(all(v['drill']==1.4 for v in power))
        self.assertEqual([v['at'] for v in holes],[(-5.08,2.5),(10.16,2.5)])
        self.assertTrue(all(v['drill']==2.4 and 'np_thru_hole' in v['form'] for v in holes))


if __name__ == '__main__':unittest.main()
