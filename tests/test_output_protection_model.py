"""Regression checks for the output-protection screening model (not electrical qualification)."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
module_spec = importlib.util.spec_from_file_location('protection_model', ROOT/'scripts/analyze_output_protection.py')
model = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(model)

WORST = dict(cin=40e-6, craw=60e-6, i_load=0.3, c_load=2e-6, lossy=False, t_end=40e-6)


class ProtectionModelTests(unittest.TestCase):
    def test_every_input_is_labelled_and_sourced(self):
        labels = {'KNOWN', 'CALCULATED', 'ASSUMED', 'AMBIGUOUS', 'INFERRED'}
        for name, (_, label, source) in model.INPUTS.items():
            self.assertIn(label, labels, name)
            self.assertTrue(source, name)

    def test_lm74800_only_finding_is_reproduced(self):
        run = model.high_side_short(model.OPTIONS['A_lm74800_ov_only'], **WORST)
        self.assertGreater(run['peak_load_V'], 6.0)

    def test_recommended_option_stays_below_screen_at_worst_corner(self):
        run = model.high_side_short(model.OPTIONS['I_470uF_bulk_plus_precision_fast_gate_off'], **WORST)
        self.assertLess(run['peak_load_V'], 5.6)

    def test_bulk_reduces_load_release_estimate(self):
        bare = max(r['raw_peak_V'] for r in model.load_release(0.0))
        bulk = max(r['raw_peak_V'] for r in model.load_release(470e-6))
        self.assertLess(bulk, bare)


if __name__ == '__main__':
    unittest.main()
