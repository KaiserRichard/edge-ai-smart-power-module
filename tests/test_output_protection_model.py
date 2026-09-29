"""Regression checks for the output-protection screening model (not electrical qualification)."""
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location('protection_model', ROOT/'scripts/analyze_output_protection.py')
model = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(model)

WORST = dict(cin=40e-6, craw=60e-6, i_load=0.3, c_load=2e-6, lossy=False, t_end=40e-6)
HISTORICAL = ROOT / 'docs/evidence/r2/protection_analysis_2026-09-26/protection_model_results.json'
HISTORICAL_SHA256 = '9f3d5fa06a141019b94e742dd9685bd6f35e08a770af63a8c3f0251c2c396956'


class ProtectionModelTests(unittest.TestCase):
    def test_every_input_is_labelled_and_sourced(self):
        labels = {'KNOWN', 'CALCULATED', 'ASSUMED', 'UNKNOWN', 'INFERRED'}
        for profile in ('baseline', 'reviewed'):
            for name, (_, label, source) in model.get_inputs(profile).items():
                self.assertIn(label, labels, (profile, name))
                self.assertTrue(source, (profile, name))

    def test_profile_current_limits_use_distinct_documented_bases(self):
        baseline = model.get_inputs('baseline')
        reviewed = model.get_inputs('reviewed')
        self.assertEqual(model.v('efuse_iol_max_A', baseline), 4.48 * 1.07)
        self.assertEqual(model.v('efuse_iol_min_A', baseline), 4.48 * (1 - 0.07))
        self.assertEqual(model.v('efuse_iol_nom_A', reviewed), 4.5)
        self.assertEqual(model.v('efuse_iol_max_A', reviewed), 4.815 / 0.999)
        self.assertEqual(model.v('efuse_iol_min_A', reviewed), 4.185 / 1.001)
        self.assertEqual(model.v('efuse_ron_ohm', baseline), 0.0345)
        self.assertEqual(model.v('efuse_ron_ohm', reviewed), 0.053)

    def test_review_resolves_deglitch_but_not_missing_device_evidence(self):
        inputs = model.get_inputs('reviewed')
        self.assertEqual(inputs['lm74800_ov_deglitch_s'][:2], (5.4e-6, 'KNOWN'))
        for name in ('q302_gate_charge_C', 'fet_rds_hot_ohm', 'buck_hs_rdson_ohm',
                     'L_isat_A', 'L_sat_ratio', 'cin_eff_F', 'craw_eff_F',
                     'ideal_diode_off_s', 'fast_gate_off_s', 'precision_detect_s'):
            self.assertEqual(inputs[name][1], 'ASSUMED', name)
        self.assertAlmostEqual(model.v('hgate_discharge_s', inputs), 96e-9 / 0.168)
        self.assertEqual(model.v('hgate_source_max_A', inputs), 75e-6)

    def test_defaults_are_reviewed_and_profile_mutation_is_isolated(self):
        self.assertEqual(model.INPUTS, model.get_inputs('reviewed'))
        self.assertEqual(model.OPTIONS, model.build_options(model.INPUTS))
        altered = model.get_inputs('reviewed')
        altered['efuse_ron_ohm'] = (1.0, 'ASSUMED', 'test perturbation')
        self.assertEqual(model.v('efuse_ron_ohm'), 0.053)
        with self.assertRaises(ValueError):
            model.get_inputs('unreviewed_typo')

    def test_profiles_keep_the_same_32_physical_corners(self):
        baseline = model.corners(model.get_inputs('baseline'))
        self.assertEqual(len(baseline), 32)
        self.assertEqual(len(set(baseline)), 32)
        self.assertEqual(baseline, model.corners(model.get_inputs('reviewed')))

    def test_historical_evidence_is_unchanged_and_writes_are_dated(self):
        self.assertEqual(hashlib.sha256(HISTORICAL.read_bytes()).hexdigest(), HISTORICAL_SHA256)
        self.assertEqual(model.OUT.parent.name, 'protection_analysis_2026-09-29')
        self.assertEqual(model.BASELINE_OUT.parent, model.OUT.parent)
        self.assertNotEqual(model.OUT, HISTORICAL)

    def test_baseline_reproduces_archived_runs_and_algebraic_estimates(self):
        historical = json.loads(HISTORICAL.read_text())
        inputs = model.get_inputs('baseline')
        options = model.build_options(inputs)
        for option in ('A_lm74800_ov_only', 'B2_A_plus_1000uF_bulk',
                       'I_470uF_bulk_plus_precision_fast_gate_off',
                       'H_470uF_bulk_plus_precision_crowbar'):
            archived = historical['high_side_short'][option]
            self.assertEqual(options[option], archived['option'])
            for index in (0, 31):
                expected = archived['runs'][index]
                run = model.high_side_short(options[option], *model.corners(inputs)[index], inputs=inputs)
                self.assertEqual({key: run[key] for key in expected}, expected)
        for bulk in (0.0, 470e-6, 1000e-6):
            key = f'bulk_{round(bulk * 1e6)}uF'
            self.assertEqual(model.load_release(bulk, inputs=inputs), historical['load_release'][key]['rows'])
            self.assertEqual(model.startup(bulk, 5.0, inputs=inputs), historical['startup_9V_5A'][key])

    def test_lm74800_only_finding_is_reproduced(self):
        run = model.high_side_short(model.OPTIONS['A_lm74800_ov_only'], **WORST)
        self.assertGreater(run['peak_load_V'], 6.0)

    def test_option_i_comparative_delay_leaves_negligible_5v5_margin(self):
        run = model.high_side_short(model.OPTIONS['I_470uF_bulk_plus_precision_fast_gate_off'], **WORST)
        self.assertLess(run['peak_load_V'], 5.5)
        self.assertGreater(run['margin_to_limit_mV'], 0)
        self.assertLess(run['margin_to_limit_mV'], 10)
        # A numerical margin is not a robust bound or a qualification PASS.
        self.assertEqual(model.INPUTS['load_fault_limit_V'][1], 'KNOWN')

    def test_two_microsecond_isolation_fails_new_load_limit(self):
        opt = dict(model.OPTIONS['I_470uF_bulk_plus_precision_fast_gate_off'])
        opt['delay_s'] = model.v('precision_isolation_sensitivity_s')
        run = model.high_side_short(opt, **WORST)
        self.assertGreater(run['peak_load_V'], 5.5)
        self.assertLess(run['margin_to_limit_mV'], 0)

    def test_peak_is_numerically_consistent_at_half_step(self):
        opt = model.OPTIONS['I_470uF_bulk_plus_precision_fast_gate_off']
        normal = model.high_side_short(opt, **WORST)
        fine = model.high_side_short(opt, dt=1e-9, **WORST)
        self.assertLess(abs(normal['peak_load_V'] - fine['peak_load_V']), 0.002)

    def test_invalid_integration_parameters_fail_instead_of_hanging(self):
        with self.assertRaises(ValueError):
            model.high_side_short(model.OPTIONS['A_lm74800_ov_only'], dt=0, **WORST)

    def test_bulk_reduces_load_release_estimate(self):
        bare = max(r['raw_peak_V'] for r in model.load_release(0.0))
        bulk = max(r['raw_peak_V'] for r in model.load_release(470e-6))
        self.assertLess(bulk, bare)


if __name__ == '__main__':
    unittest.main()
