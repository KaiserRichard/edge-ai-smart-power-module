"""Synthetic KiCad boards: resistance, real connectivity, conservative screening."""
import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_5a_path as pc

NETS = ['VOUT_5V1', 'PROT_MID', 'SERIES_OUT', 'VOUT_PROTECTED', 'LOAD_5V1', 'GND', 'SHUNT_KPLUS']


def code(net):
    return NETS.index(net)+1


def pad(pin, x, y, net, layer='F.Cu', size=.01, kind='smd', drill=None, angle=0, shape='rect'):
    hole = '' if drill is None else f'(drill {drill})'
    return (f'(pad "{pin}" {kind} {shape} (at {x} {y} {angle}) (size {size} {size}) '
            f'(layers "{layer}") {hole} (net {code(net)} "{net}"))')


def fp(ref, pads, x=0, y=0, angle=0, layer='F.Cu'):
    return f'(footprint "test" (layer "{layer}") (at {x} {y} {angle}) (property "Reference" "{ref}") {pads})'


def track(net, a, b, width=1, layer='F.Cu'):
    return (f'(segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width {width}) '
            f'(layer "{layer}") (net {code(net)}))')


def via(net, xy, drill=.3, size=.6, layers='"F.Cu" "B.Cu"'):
    return (f'(via (at {xy[0]} {xy[1]}) (size {size}) (drill {drill}) '
            f'(layers {layers}) (net {code(net)}))')


def zone(net, points, layer='F.Cu', filled=True):
    pts = ' '.join(f'(xy {x} {y})' for x, y in points)
    return (f'(zone (net {code(net)}) (net_name "{net}") (layer "{layer}") '
            f'(polygon (pts {pts})) '+(f'(filled_polygon (layer "{layer}") (pts {pts}))' if filled else '')+')')


def board(contents='', inner=False):
    layer_list = '(0 "F.Cu" signal) '+('(2 "In1.Cu" power) ' if inner else '')+'(31 "B.Cu" signal)'
    nets = ' '.join(f'(net {i+1} "{n}")' for i, n in enumerate(NETS))
    return f'(kicad_pcb (version 20241229) (general (thickness 1.6)) (layers {layer_list}) {nets} {contents})'


def full_board(width=1, length=.1, routed=True, return_layer='F.Cu'):
    # One copper segment per series leg; colocated equivalent pins keep the
    # expected resistance analytically independent of the graph implementation.
    body = []
    for i in range(209, 215):
        body.append(fp(f'C{i}', pad('1', 0, 0, 'VOUT_5V1')+pad('2', 0, 10, 'GND')))
    body.append(fp('Q301', ''.join(pad(str(i), length, 0, 'VOUT_5V1') for i in range(5, 9))+
                   ''.join(pad(str(i), 0, 2, 'PROT_MID') for i in range(1, 4))))
    body.append(fp('Q302', ''.join(pad(str(i), length, 2, 'PROT_MID') for i in range(1, 4))+
                   ''.join(pad(str(i), 0, 4, 'SERIES_OUT') for i in range(5, 9))))
    body.append(fp('JP301', pad('1', length, 4, 'SERIES_OUT')+pad('2', 0, 6, 'VOUT_PROTECTED')))
    body.append(fp('R401', pad('1', length, 6, 'VOUT_PROTECTED')+pad('4', 0, 8, 'LOAD_5V1')))
    body.append(fp('J502', pad('1', length, 8, 'LOAD_5V1')+pad('2', length, 10, 'GND')))
    if routed:
        body += [track(n, (0, i*2), (length, i*2), width, return_layer if n == 'GND' else 'F.Cu')
                 for i, n in enumerate(NETS[:6])]
    return board(' '.join(body))


def resistance_between(contents, start, end, net='GND', start_layer='F.Cu', end_layer='F.Cu', settings=None, inner=False):
    settings = settings or pc.Settings()
    b = pc.read_board(board(contents, inner), settings)
    g, _ = pc.build_graph(b, settings)
    u, v = g.node(net, start_layer, start), g.node(net, end_layer, end)
    return g.shortest([u], [v]), b


class ResistanceTests(unittest.TestCase):
    def test_independent_si_trace_resistance(self):
        # 10 mm x 1 mm x 70 um, 20 C: 2.462857... mOhm.
        expected = 1.724e-8 * .010 / (.001 * .000070) * 1000
        self.assertAlmostEqual(pc.Settings(temp_c=20).resistance(10, 1, 'F.Cu'), expected)

    def test_temperature_and_layer_thickness(self):
        cold, hot = pc.Settings(temp_c=20), pc.Settings(temp_c=85)
        self.assertAlmostEqual(hot.resistance(10, 1, 'F.Cu')/cold.resistance(10, 1, 'F.Cu'), 1+.00393*65)
        self.assertAlmostEqual(hot.resistance(10, 1, 'In1.Cu'), 2*hot.resistance(10, 1, 'B.Cu'))

    def test_via_annulus_units(self):
        expected = 1.724e-8 * .0016 / (math.pi*(.0003+.000025)*.000025) * 1000
        self.assertAlmostEqual(pc.Settings(temp_c=20).barrel(1.6, .3), expected)

    def test_thermal_legacy_envelope_is_explicit(self):
        # Invert published I=.024*DT^.44*A^.725 for a chosen 10 C case.
        area = (5/(.024*10**.44))**(1/.725)
        self.assertAlmostEqual(pc.thermal_rise(area*.0254**2/.07, 70), 10)
        self.assertGreater(pc.thermal_rise(.5, 35), pc.thermal_rise(1, 70))

    def test_frozen_rows_replaced_not_double_counted(self):
        budget = pc.frozen_budget()
        self.assertEqual(budget['copper_mohm'], {'send': 1.5, 'return': 1.5})
        self.assertAlmostEqual(sum(budget['fixed_mohm'].values()), 38.85554624343832)
        self.assertAlmostEqual(budget['buck_min_V']-5*budget['frozen_loop_mohm']/1000-.02, 4.76404324089521)


class ConnectivityTests(unittest.TestCase):
    def test_full_path_known_resistance_voltage_and_thermal(self):
        r = pc.check(full_board())
        self.assertEqual(r['status'], 'CONDITIONAL PASS')
        unit = 1.724e-8*(1+.00393*65)*.0001/(.001*.000070)*1000
        self.assertAlmostEqual(r['copper_mohm']['send'], unit*5)
        self.assertAlmostEqual(r['copper_mohm']['return'], unit)
        total = 38.85554624343832+6*unit
        self.assertAlmostEqual(r['total_loop_mohm'], total)
        self.assertAlmostEqual(r['drop_5A_mV'], total*5)
        self.assertAlmostEqual(r['pi_min_V'], 4.993320972112401-total*.005-.02)
        self.assertEqual(len(r['thermal_traces']), 6)

    def test_no_copper_is_open_even_colocated_pads(self):
        r = pc.check(full_board(routed=False))
        self.assertEqual(r['status'], 'OPEN')
        self.assertTrue(all(v['status'] == 'OPEN' for v in r['legs']))
        self.assertIsNone(r['pi_min_V'])
        self.assertIsNone(r['total_loop_mohm'])

    def test_return_wrong_layer_is_open(self):
        r = pc.check(full_board(return_layer='B.Cu'))
        self.assertEqual(r['legs'][-1]['status'], 'OPEN')
        self.assertIsNone(r['pi_min_V'])

    def test_send_copper_allocation_can_fail_before_voltage(self):
        r = pc.check(full_board(length=1.2))
        self.assertEqual(r['status'], 'FAIL')
        self.assertEqual(r['copper_exceeded'], ['send'])
        self.assertGreater(r['margin_mV'], 0)

    def test_pi_voltage_failure(self):
        r = pc.check(full_board(length=10, width=.1))
        self.assertEqual(r['status'], 'FAIL')
        self.assertLess(r['pi_min_V'], 4.75)

    def test_voltage_failure_independent_of_copper_allocation(self):
        budget = copy.deepcopy(pc.frozen_budget())
        budget['buck_min_V'] = 4.8
        r = pc.check(full_board(), budget=budget)
        self.assertEqual(r['status'], 'FAIL')
        self.assertEqual(r['copper_exceeded'], [])

    def test_copper_boundaries_are_inclusive(self):
        r = pc.check(full_board())
        budget = copy.deepcopy(pc.frozen_budget())
        budget['copper_mohm'] = r['copper_mohm']
        self.assertEqual(pc.check(full_board(), budget=budget)['status'], 'CONDITIONAL PASS')

    def test_missing_force_pin_cannot_use_kelvin(self):
        text = full_board().replace('(pad "4" smd rect', '(pad "3" smd rect')
        r = pc.check(text)
        self.assertEqual(r['status'], 'OPEN')
        self.assertTrue(any('R401 LOAD_5V1' in issue for issue in r['issues']))

    def test_all_mosfet_pins_must_be_connected(self):
        text = full_board().replace('(pad "8" smd rect (at 0.1 0 ', '(pad "8" smd rect (at 40 0 ', 1)
        self.assertEqual(pc.check(text)['legs'][0]['status'], 'OPEN')

    def test_disconnected_net_island_not_counted(self):
        contents = track('GND', (0, 0), (10, 0))+track('GND', (50, 50), (500, 50), .01)
        result, _ = resistance_between(contents, (0, 0), (10, 0))
        self.assertAlmostEqual(result[0], pc.Settings().resistance(10, 1, 'F.Cu'))

    def test_parallel_routes_receive_no_sharing_credit(self):
        contents = (track('GND', (0, 0), (10, 0))+track('GND', (0, 0), (0, 10))+
                    track('GND', (0, 10), (10, 0)))
        result, _ = resistance_between(contents, (0, 0), (10, 0))
        self.assertAlmostEqual(result[0], pc.Settings().resistance(10, 1, 'F.Cu'))

    def test_t_junction_and_crossing_split_lengths(self):
        contents = track('GND', (0, 0), (10, 0))+track('GND', (5, -5), (5, 5))
        result, _ = resistance_between(contents, (0, 0), (5, 5))
        self.assertAlmostEqual(result[0], pc.Settings().resistance(10, 1, 'F.Cu'))

    def test_different_net_crossing_never_connects(self):
        contents = track('GND', (0, 0), (10, 0))+track('LOAD_5V1', (5, -5), (5, 5))
        result, _ = resistance_between(contents, (0, 0), (5, 5))
        self.assertIsNone(result)

    def test_via_connects_layers_with_resistance(self):
        contents = track('GND', (0, 0), (5, 0))+via('GND', (5, 0))+track('GND', (5, 0), (10, 0), layer='B.Cu')
        result, _ = resistance_between(contents, (0, 0), (10, 0), end_layer='B.Cu')
        self.assertAlmostEqual(result[0], pc.Settings().resistance(10, 1, 'F.Cu')+pc.Settings().barrel(1.6, .3))
        self.assertEqual(sum(e['kind'] == 'barrel' for e in result[1]), 1)

    def test_blind_via_depth_is_open(self):
        _, b = resistance_between(via('GND', (5, 0), layers='"F.Cu" "In1.Cu"'), (0, 0), (10, 0), inner=True)
        self.assertIn('blind/buried/custom via depth OPEN', b.issues[0])

    def test_plated_pad_is_not_free_layer_change(self):
        contents = fp('J', pad('1', 5, 0, 'GND', '*.Cu', size=1, kind='thru_hole', drill=.3))
        contents += track('GND', (0, 0), (5, 0))+track('GND', (5, 0), (10, 0), layer='B.Cu')
        result, _ = resistance_between(contents, (0, 0), (10, 0), end_layer='B.Cu')
        self.assertAlmostEqual(result[0], pc.Settings().resistance(10, 1, 'F.Cu')+pc.Settings().barrel(1.6, .3))

    def test_track_midpoint_terminal(self):
        contents = fp('C', pad('1', 5, 0, 'GND'))+track('GND', (0, 0), (10, 0))
        result, _ = resistance_between(contents, (0, 0), (5, 0))
        self.assertAlmostEqual(result[0], pc.Settings().resistance(5, 1, 'F.Cu'))

    def test_rotated_footprint_pad_position(self):
        b = pc.read_board(board(fp('X', pad('1', 2, 0, 'GND', angle=90), 10, 10, 90)), pc.Settings())
        self.assertAlmostEqual(b.pads[0].xy[0], 10)
        self.assertAlmostEqual(b.pads[0].xy[1], 8)

    def test_back_layer_does_not_mirror_local_coordinates_twice(self):
        b = pc.read_board(board(fp('X', pad('1', -2, 1, 'GND', 'B.Cu'), 10, 10, layer='B.Cu')), pc.Settings())
        self.assertEqual(b.pads[0].xy, (8, 11))

    def test_arc_uses_arc_length_not_chord(self):
        arc = f'(arc (start 0 0) (mid 5 -5) (end 10 0) (width 1) (layer "F.Cu") (net {code("GND")}))'
        result, b = resistance_between(arc, (0, 0), (10, 0))
        self.assertAlmostEqual(b.thermal[0]['length_mm'], 5*math.pi)
        self.assertGreaterEqual(result[0], pc.Settings().resistance(5*math.pi, 1, 'F.Cu'))


class ZoneTests(unittest.TestCase):
    RECT = [(-1, -2), (11, -2), (11, 2), (-1, 2)]

    def endpoints(self, a=(0, 0), b=(10, 0)):
        return fp('A', pad('1', *a, 'GND'))+fp('B', pad('1', *b, 'GND'))

    def test_filled_zone_has_finite_resistance(self):
        result, _ = resistance_between(self.endpoints()+zone('GND', self.RECT), (0, 0), (10, 0))
        self.assertAlmostEqual(result[0], pc.Settings().resistance(10, 1, 'F.Cu'))
        self.assertTrue(any(e['kind'] == 'zone' for e in result[1]))

    def test_unfilled_outline_is_open(self):
        result, b = resistance_between(self.endpoints()+zone('GND', self.RECT, filled=False), (0, 0), (10, 0))
        self.assertIsNone(result)
        self.assertIn('unfilled zone', b.issues[0])

    def test_zone_on_wrong_layer_is_open(self):
        result, _ = resistance_between(self.endpoints()+zone('GND', self.RECT, layer='B.Cu'), (0, 0), (10, 0))
        self.assertIsNone(result)

    def test_disconnected_filled_islands_remain_open(self):
        left = [(-1, -1), (4, -1), (4, 1), (-1, 1)]
        right = [(6, -1), (11, -1), (11, 1), (6, 1)]
        result, _ = resistance_between(self.endpoints()+zone('GND', left)+zone('GND', right), (0, 0), (10, 0))
        self.assertIsNone(result)

    def test_neck_limits_width(self):
        points = [(-1, -2), (3, -2), (3, -.2), (7, -.2), (7, -2), (11, -2),
                  (11, 2), (7, 2), (7, .2), (3, .2), (3, 2), (-1, 2)]
        result, _ = resistance_between(self.endpoints()+zone('GND', points), (0, 0), (10, 0))
        self.assertIsNotNone(result)
        self.assertGreater(result[0], pc.Settings().resistance(10, 1, 'F.Cu'))
        self.assertTrue(any(e.get('width_mm', 1) <= .4000001 for e in result[1]))

    def test_concave_zone_routes_around_slot(self):
        points = [(-1, -2), (11, -2), (11, 2), (6, 2), (6, -1), (4, -1), (4, 2), (-1, 2)]
        settings = pc.Settings(zone_grid_mm=.5)
        result, _ = resistance_between(self.endpoints()+zone('GND', points), (0, 0), (10, 0), settings=settings)
        self.assertIsNotNone(result)
        self.assertGreater(result[0], settings.resistance(10, 1, 'F.Cu'))
        self.assertEqual(pc.corridor_width((0, 0), (10, 0), points, 1), 0)

    def test_linked_hole_not_bridged(self):
        points = [(-1, -3), (11, -3), (11, 3), (-1, 3), (-1, -3),
                  (4, -1), (4, 1), (6, 1), (6, -1), (4, -1), (-1, -3)]
        self.assertFalse(pc.inside((5, 0), points))
        self.assertEqual(pc.corridor_width((0, 0), (10, 0), points, 1), 0)
        result, _ = resistance_between(self.endpoints()+zone('GND', points), (0, 0), (10, 0), settings=pc.Settings(zone_grid_mm=.5))
        self.assertIsNotNone(result)
        self.assertGreater(result[0], pc.Settings().resistance(10, 1, 'F.Cu'))

    def test_grid_resource_limit_is_open(self):
        _, b = resistance_between(self.endpoints()+zone('GND', self.RECT), (0, 0), (10, 0), settings=pc.Settings(max_zone_nodes=5))
        self.assertTrue(any('node limit' in v for v in b.issues))


class InputAndCliTests(unittest.TestCase):
    def run_cli(self, text, *args):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'test.kicad_pcb'
            p.write_text(text)
            return subprocess.run([sys.executable, str(ROOT/'scripts/check_5a_path.py'), str(p), *args],
                                  capture_output=True, text=True)

    def test_parser_quoted_escapes(self):
        self.assertEqual(pc.parse('(x "a (b) \\"c\\"" ; comment\n (y 2))')[1], 'a (b) "c"')

    def test_parser_rejects_truncated_and_extra_roots(self):
        for text in ('(x', '(x))', '(x) (y)', 'bad', '(x "bad)'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                pc.parse(text)

    def test_custom_force_pad_rectangle(self):
        p = ('(pad "1" smd custom (at 0 0) (size .01 .01) (layers "F.Cu") (net 6 "GND") '
             '(primitives (gr_poly (pts (xy -2 -3) (xy 2 -3) (xy 2 3) (xy -2 3)) (width 0) (fill yes))))')
        b = pc.read_board(board(fp('R401', p)), pc.Settings())
        self.assertEqual(b.pads[0].width, 4)
        self.assertEqual(b.issues, [])

    def test_hierarchical_net_aliases_are_not_shorted(self):
        text = full_board().replace('(net 6 "GND")', '(net 6 "/A/GND")', 1)
        text = text.replace('(version 20241229)', '(version 20241229) (net 99 "/B/GND")')
        # Update pad names too, preserving the declared identities.
        text = text.replace('(net 6 "GND")', '(net 6 "/A/GND")')
        r = pc.check(text)
        self.assertEqual(r['status'], 'OPEN')
        self.assertTrue(any('ambiguous hierarchical' in v for v in r['issues']))

    def test_cli_pass_exit_zero_json(self):
        p = self.run_cli(full_board(), '--json')
        self.assertEqual(p.returncode, 0, p.stdout+p.stderr)
        self.assertEqual(json.loads(p.stdout)['status'], 'CONDITIONAL PASS')

    def test_cli_fail_exit_one(self):
        p = self.run_cli(full_board(width=.1, length=10), '--json')
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)['status'], 'FAIL')

    def test_cli_malformed_input_open_no_traceback(self):
        p = self.run_cli('(kicad_pcb', '--json')
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)['status'], 'OPEN')
        self.assertEqual(p.stderr, '')

    def test_cli_invalid_dimensions_open(self):
        for args in (('--copper-um-outer', '0'), ('--temp-c', 'nan'), ('--via-plating-um', '-1'), ('--zone-grid-mm', '0')):
            with self.subTest(args=args):
                p = self.run_cli(full_board(), '--json', *args)
                self.assertEqual(p.returncode, 1)
                self.assertEqual(json.loads(p.stdout)['status'], 'OPEN')

    def test_current_board_open_and_read_only(self):
        path = ROOT/'hardware/kicad/V1A.kicad_pcb'
        original = path.read_bytes()
        r = pc.check(original.decode())
        self.assertEqual(r['status'], 'OPEN')
        self.assertEqual(len(r['legs']), 6)
        self.assertTrue(all(v['status'] == 'OPEN' for v in r['legs']))
        self.assertEqual(r['issues'], [])
        self.assertIsNone(r['pi_min_V'])
        self.assertEqual(path.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
