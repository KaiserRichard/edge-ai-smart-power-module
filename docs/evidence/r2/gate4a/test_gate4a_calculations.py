import csv
import json
import math
import unittest
from pathlib import Path
import calculate_gate4a as calc


class PhysicalCalculationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, _ = calc.calculate()

    def test_local_store_energy_conservation_before_and_after_commutation(self):
        meta, rows, state = calc.raw_waveform()
        a = meta['ASSUMED']
        independent_cap_peak = math.sqrt(a['Vraw0_V']**2 + (a['Cin_F']*a['Vin0_V']**2+a['L_H']*a['I0_A']**2)/a['Craw_F'])
        self.assertAlmostEqual(meta['peak_Vraw_CALCULATED_V'], independent_cap_peak, places=12)
        self.assertLess(meta['max_energy_residual_J'], 1e-12)
        self.assertAlmostEqual(rows[-1]['IL_A'], 0, places=10)
        self.assertGreater(meta['first_current_zero_s'], meta['input_ground_diode_start_s'])

    def test_analytic_state_satisfies_independent_kcl_and_inductor_ode(self):
        meta, _, state = calc.raw_waveform()
        a = meta['ASSUMED']; h = 1e-10
        for t in [meta['input_ground_diode_start_s']*.4, (meta['input_ground_diode_start_s']+meta['first_current_zero_s'])/2]:
            vi, vo, i = state(t); minus = state(t-h); plus = state(t+h)
            deriv = [(p-m)/(2*h) for p,m in zip(plus,minus)]
            self.assertAlmostEqual(deriv[1]*a['Craw_F'], i, places=6)
            self.assertAlmostEqual(deriv[2]*a['L_H'], vi-vo, places=6)
            if t<meta['input_ground_diode_start_s']:
                self.assertAlmostEqual(deriv[0]*a['Cin_F'], -i, places=6)

    def test_exported_netlist_places_raw_bulk_and_crowbar_on_distinct_sides(self):
        nets = self.data['netlist_energy_boundaries']
        raw = {n['ref'] for n in nets['/VOUT_5V1']}
        protected = {n['ref'] for n in nets['/VOUT_PROTECTED']}
        for r in range(330,338):
            self.assertIn(f'C{r}',raw); self.assertNotIn(f'C{r}',protected)
        self.assertTrue({'L201','Q301','R301','R202'} <= raw)
        self.assertTrue({'Q302','R308','R310','R401'} <= protected)

    def test_unknown_electrical_bounds_remain_open(self):
        self.assertIsNone(self.data['raw_node']['actual_terminal_peak_V'])
        self.assertIsNone(self.data['protected_node']['actual_far_end_peak_V'])
        self.assertIsNone(self.data['selected_path']['hot_Rpair_actual_ohm'])
        self.assertEqual(self.data['detector']['complete_path_min_max_s']['source'], [None,None])
        self.assertTrue(all(r['time_to_nominal_OV_s']>10e-6 for r in self.data['OV_trigger_latency_sensitivity']))

    def test_selected_cap_bank_does_not_inherit_old_contract(self):
        p=self.data['protected_node']
        self.assertGreater(p['candidate_Cnom_F'],p['legacy_Cmax_target_F'])
        self.assertGreater(p['published_initial_parallel_ESR20C100kHz_max_ohm'],p['legacy_ESR_target_ohm'])
        self.assertGreater(p['legacy_conditional_at_candidate14mOhm_parallel_ESR_V'],5.5)

    def test_recovered_machine_registers_and_regenerated_artifact_match(self):
        p=Path(__file__).parent
        manifest=json.loads((p/'FREEZE_MANIFEST.json').read_text())['changes']
        with (p/'FREEZE_BOM.csv').open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),len(manifest))
        for r,m in zip(rows,manifest):
            self.assertEqual(r,{**m,'refdes':','.join(m['refdes'])})
        self.assertEqual(json.loads((p/'CALCULATIONS.json').read_text()),self.data)


if __name__ == '__main__':
    unittest.main()
