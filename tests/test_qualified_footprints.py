"""Independent dimensional checks against cited manufacturer land drawings."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT/'hardware/kicad/V1A_Qualified.pretty'


def read_pads(name):
    result = []
    for line in (LIB/(name+'.kicad_mod')).read_text().splitlines():
        if not line.strip().startswith('(pad '):
            continue
        number = re.search(r'\(pad "([^"]*)"',line)[1]
        x,y = map(float,re.search(r'\(at ([-\d.]+) ([-\d.]+)\)',line).groups())
        points = [(float(px)+x,float(py)+y) for px,py in re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)',line)]
        layers = re.search(r'\(layers ([^)]+)\)',line)[1]
        result.append((number,points,layers))
    return result


def bounds(polygons):
    points = [p for poly in polygons for p in poly]
    return min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)


class FootprintTests(unittest.TestCase):
    def assert_bounds(self,actual,expected):
        for a,b in zip(actual,expected):
            self.assertAlmostEqual(a,b,delta=.0001)

    def test_rjr_all_fourteen_labelled_land_extents(self):
        # TI 4223976/H p56; notably BIAS1 upper left, SW10 right, no EP15.
        expected = {
            '1':(-2.2,-1.95,-1.5,-.95),'2':(-2.2,-.65,-1.5,-.4),
            '3':(-2.2,-.15,-1.5,.15),'4':(-2.2,.4,-1.5,.65),
            '5':(-2.2,.95,-1.5,1.95),'6':(-1.25,1.25,-1,1.95),
            '7':(-.75,1.25,-.5,1.95),'8':(.25,.95,.65,1.95),
            '9':(1.4,.95,2.2,1.95),'10':(-.2,-.2,2.2,.2),
            '11':(1.4,-1.95,2.2,-.95),'12':(.25,-1.95,.65,-.95),
            '13':(-.75,-1.95,-.5,-1.25),'14':(-1.25,-1.95,-1,-1.25)}
        pads = {n:p for n,p,l in read_pads('TI_RJR0014A_LM61460') if 'F.Cu' in l}
        self.assertEqual(set(pads),set(expected))
        for number,box in expected.items():
            self.assert_bounds(bounds([pads[number]]),box)

    def test_rjr_stencil_keeps_split_sw_apertures(self):
        paste = [p for n,p,l in read_pads('TI_RJR0014A_LM61460') if 'F.Paste' in l]
        self.assertEqual(len(paste),15)
        sw = sorted([bounds([p]) for p in paste if abs(bounds([p])[1]+.2)<.0001])
        self.assertEqual(len(sw),2)
        self.assert_bounds(sw[0],(-.2,-.2,.9,.2))
        self.assert_bounds(sw[1],(1.1,-.2,2.2,.2))

    def test_q3_every_source_gate_drain_number_and_clearance(self):
        # TI SLPS549B p9 top board view: 1-4 lower row, 8-5 upper row.
        pads = [(n,p) for n,p,l in read_pads('TI_Q3_CSD19537Q3') if 'F.Cu' in l]
        self.assertEqual({n for n,p in pads},{str(n) for n in range(1,9)})
        for n,x in zip(['1','2','3','4'],[-.975,-.325,.325,.975]):
            self.assert_bounds(bounds([p for number,p in pads if number==n]),(x-.25,1.12,x+.25,1.75))
        drain = bounds([p for n,p in pads if n in ['5','6','7','8']])
        self.assert_bounds(drain,(-1.225,-1.75,1.225,.56))
        self.assertAlmostEqual(1.12-drain[3],.56)
        for n,x in zip(['8','7','6'],[-.975,-.325,.325]):
            self.assert_bounds(bounds([p for number,p in pads if number==n]),(x-.25,-1.75,x+.25,-1.25))

    def test_q3_stencil_is_not_full_drain_copper(self):
        paste = [p for n,p,l in read_pads('TI_Q3_CSD19537Q3') if 'F.Paste' in l]
        self.assertEqual(len(paste),10)
        sizes = [(round(bounds([p])[2]-bounds([p])[0],3),round(bounds([p])[3]-bounds([p])[1],3)) for p in paste]
        self.assertEqual(sizes.count((1.02,1.445)),2)
        self.assertEqual(sizes.count((.34,.45)),8)

    def test_vishay_kelvin_wide_force_narrow_sense_contract(self):
        pads = {n:bounds([p]) for n,p,l in read_pads('Vishay_WSL2726_Kelvin_1Fplus_2Splus_3Sminus_4Fminus') if 'F.Cu' in l}
        self.assertEqual(set(pads),{'1','2','3','4'})
        expected = {'1':(-3.81,-1.965,-1.12,3.745),'2':(-3.81,-3.745,-1.12,-2.855),
                    '3':(1.12,-3.745,3.81,-2.855),'4':(1.12,-1.965,3.81,3.745)}
        for n,box in expected.items():
            self.assert_bounds(pads[n],box)
        self.assertAlmostEqual(pads['1'][1]-pads['2'][3],.89)
        self.assertAlmostEqual(pads['4'][2]-pads['1'][0],7.62)


if __name__ == '__main__':
    unittest.main()
