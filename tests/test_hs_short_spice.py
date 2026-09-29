"""Offline preparation checks; these do NOT parse or execute SPICE."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('hs_short_prepare', ROOT / 'simulation/hs_short/prepare.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class SpicePreparationTests(unittest.TestCase):
    def test_all_requested_profiles_options_and_corners_share_python_inputs(self):
        count = 0
        for profile in ('baseline', 'reviewed'):
            inputs = prepare.model.get_inputs(profile)
            options = prepare.model.build_options(inputs)
            corners = prepare.model.corners(inputs)
            self.assertEqual(len(corners), 32)
            for name in prepare.OPTIONS.values():
                for corner in corners:
                    params = prepare.parameters(inputs, options[name], corner)
                    self.assertEqual(params['ILIMIT'], inputs['efuse_iol_max_A'][0])
                    self.assertEqual(params['CINPUT'], corner[0])
                    self.assertEqual(params['CRAW'], corner[1])
                    self.assertEqual(params['ILOAD'], corner[2])
                    self.assertEqual(params['CLOAD'], corner[3])
                    self.assertEqual(params['VINITIAL'], inputs['vraw_static_V'][0][1])
                    self.assertAlmostEqual(params['DELAY_US'] * 1e-6, options[name]['delay_s'])
                    # Lossless removes only the shorted HS and inductor resistance.
                    if not corner[4]:
                        self.assertEqual(params['RLOSS'], 0)
                        self.assertGreater(params['REFUSE'], 0)
                        self.assertGreater(params['RPATH'], 0)
                        self.assertGreater(params['RBULK'], 0)
                    count += 1
        self.assertEqual(count, 256)

    def test_peak_parser_rejects_missing_duplicate_nonfinite_or_failed_runs(self):
        for log in ('', 'peak_load = nan', 'peak_load = 1e999', 'peak_load = -1',
                    'peak_load = 5.4\npeak_load = 5.4',
                    'peak_load = 5.4\nError: timestep too small'):
            with self.subTest(log=log), self.assertRaises(ValueError):
                prepare.parse_peak(log)
        self.assertEqual(prepare.parse_peak('peak_load = 5.400000e+00 at= 1e-5\n'), 5.4)

    def test_comparison_cannot_pass_absent_or_over_limit_results(self):
        self.assertEqual(prepare.comparison(5.4, 5.4)[1], 'PASS')
        self.assertEqual(prepare.comparison(5.7, 5.4)[1], 'FAIL')
        with self.assertRaises(ValueError):
            prepare.comparison(5.4, 0)
        for peak in (float('nan'), float('inf'), -1):
            with self.assertRaises(ValueError):
                prepare.comparison(peak, 5.4)

    def test_latch_state_checks_reject_false_startup_and_reconnection(self):
        good = ('initial_action = 0\ninitial_connected = 1\nfinal_action = 1\n'
                'final_connected = 0\nfinal_reverse_latch = 0\n')
        prepare.check_states(good, disconnect=True)
        for bad in (good.replace('initial_action = 0', 'initial_action = 1'),
                    good.replace('final_connected = 0', 'final_connected = 1')):
            with self.assertRaises(ValueError):
                prepare.check_states(bad, disconnect=True)


if __name__ == '__main__':
    unittest.main()
