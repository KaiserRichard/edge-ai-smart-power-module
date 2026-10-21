"""Numerical checks only. These tests never load or save any KiCad native file."""
import importlib.util
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('gate2c', Path(__file__).resolve().parents[1] /
                                             'scripts/calculate_sheet03_gate2c.py')
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


class IndependentBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.j = calc.calculate()

    def test_unknown_application_bounds_stay_unknown(self):
        self.assertEqual(self.j['verdict'], 'BLOCKED')
        for margin in self.j['margins'].values():
            self.assertEqual(margin['classification'], 'OPEN')
            self.assertIsNone(margin['worst_case_V'])
        self.assertIsNone(self.j['timing']['actual_OV_onset_to_commutation_max_ns'])
        self.assertIsNone(self.j['energy']['actual_SOA_pass'])
        self.assertLess(self.j['energy']['resistor_terminal_headroom_C_CALCULATED'], 0)

    def test_rk4_against_analytic_RC_energy_and_I2t(self):
        capacitance, resistance, voltage = 220e-6, .033, 5.5
        tau = capacitance * resistance
        y = [voltage, 0., 0.]
        for _ in range(10000):
            y = calc.rk4(y, tau / 1000, lambda s: [-s[0] / tau,
                           (s[0] / resistance) ** 2, s[0] ** 2 / resistance])
        self.assertAlmostEqual(y[0], voltage * math.exp(-10), places=11)
        self.assertAlmostEqual(y[1], capacitance * voltage ** 2 / (2 * resistance) * (1-math.exp(-20)), places=11)
        self.assertAlmostEqual(y[2], .5 * capacitance * voltage ** 2 * (1-math.exp(-20)), places=11)

    def test_fault_time_step_convergence_and_counterexample(self):
        j = self.j
        args = (24, .3e-6, .1e-6, j['threshold']['max_V'], j['buck_static']['min_V'])
        a, b = calc.fault(*args, dt=1e-9), calc.fault(*args, dt=.5e-9)
        # Discontinuous sensitivity L model/event crossing; accept 1mV numerical uncertainty.
        self.assertLess(abs(a['Pi_peak_V'] - b['Pi_peak_V']), .001)
        self.assertLess(a['fault_margin_V'], 0)
        self.assertLess(j['finite_input_conditional_cases'][1]['fault_margin_V'], 0)

    def test_fault_pulse_energy_matches_ballast_I2t(self):
        for result in self.j['fault_conditional_cases']:
            self.assertAlmostEqual(result['ballast_initial_total_J'],
                                   .033495 * result['crowbar_initial_I2t_A2s'], places=11)

    def test_independent_resistor_corners(self):
        self.assertAlmostEqual(calc.resistor_corner_power(5.5, .033, .033), 5.5 ** 2 / (4 * .033))
        energy = self.j['energy']
        self.assertAlmostEqual(energy['per_resistor_peak_W'],
                               5.5 ** 2 / (4 * energy['ballast_R_min_ohm']))

    def test_failure_cases_not_hidden(self):
        self.assertLess(self.j['margins']['harness']['conditional_original_V'], 0)
        self.assertLess(self.j['margins']['false_trip']['conditional_30us_V'], 0)
        self.assertLess(self.j['input']['UVLO_falling_nominal_V'], self.j['input']['UVLO_rising_nominal_V'])
        self.assertGreater(self.j['timing']['complete_digital_plus_charge_PG_floor_screen_ns'], 300)


if __name__ == '__main__':
    unittest.main()
