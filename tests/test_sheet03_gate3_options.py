"""Independent physical guardrails for conditional architecture arithmetic."""
import math
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from calculate_sheet03_gate3_options import calculate,current_energy_bound,sharing_max,two_cap_harness_peak

class ArchitectureBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=calculate()

    def test_unknown_application_maxima_are_not_zero(self):
        for option in 'ABCDE':self.assertIsNone(self.r[option]['application_VPi_peak_max_V'])
        self.assertIsNone(self.r['B']['guaranteed_24VDC_total_clearing_s_max'])
        self.assertIsNone(self.r['supply_hold_up']['actual_supply_validity'])

    def test_no_current_bound_without_positive_inductance(self):
        with self.assertRaises(ValueError):current_energy_bound(.01,0)

    def test_A_bound_conserves_worst_initial_and_input_energy(self):
        c=self.r['A']['CALCULATED'];i=c['positive_L_current_energy_bound_A']
        supplied=.5*20e-6*24**2+150e-6*24+.5*8.16e-6*6.1**2
        self.assertAlmostEqual(.5*5.44e-6*i*i,supplied,places=12)
        self.assertLess(i,60)
        # Historical larger C breaks this particular 60A qualification box.
        self.assertGreater(math.sqrt(2*(.5*60.996e-6*24**2+150e-6*24+.5*8.16e-6*36)/5.44e-6),60)

    def test_A_longer_action_is_blocking(self):
        c=self.r['A']['CALCULATED'];self.assertGreater(c['fault_margin_V'],0);self.assertLess(c['fault_margin_2us_V'],0)

    def test_A_longer_normal_response_is_blocking(self):
        c=self.r['A']['CALCULATED']
        self.assertGreater(c['normal_false_trip_margin_V'],0)
        self.assertLess(c['normal_30us_margin_V'],0)

    def test_ballast_energy_cannot_assume_quarter_at_independent_corners(self):
        self.assertAlmostEqual(sharing_max(.033,.033),.25)
        c=self.r['A']['CALCULATED'];self.assertGreater(c['single_resistor_fraction_max'],.25)
        self.assertLess(c['single_resistor_fraction_max'],.26)
        self.assertGreater(c['single_resistor_energy_upper_J'],c['all_stores_energy_ceiling_J']/4)

    def test_C_DC_and_low_intermediate_window_fail(self):
        c=self.r['C']['CALCULATED'];self.assertLess(c['maintained_mid_DC_fault_margin_V'],0)
        self.assertGreater(c['mid_for95pct_duty_nom_min_V'],c['mid_nom_max_for5p5_V'])
        # Loss must conserve power across cascade, not add nominal efficiencies.
        eta=self.r['C']['ASSUMED']['eta_first']*self.r['C']['ASSUMED']['eta_final']
        self.assertAlmostEqual(c['total_loss_W'],c['output_W']/eta-c['output_W'])
        self.assertAlmostEqual(c['total_loss_W'],c['first_stage_loss_W']+c['final_stage_loss_W'])

    def test_D_module_pass_does_not_close_Pi_harness(self):
        c=self.r['D']['CALCULATED'];self.assertGreater(c['module_margin_V'],0);self.assertLess(c['restricted_L_only_Pi_fault_margin_V'],0)
        # Independently invert capacitor energy headroom for required C.
        v=c['module_peak_screen_V'];self.assertAlmostEqual(c['restricted_L_only_required_Pi_C_F'],.5*2e-6*10**2/(.5*((5.5-.01)**2-v*v)))

    def test_D_remaining_module_cap_is_an_additional_energy_source(self):
        c=self.r['D']['CALCULATED']
        # Independent capacitor charge and differential-mode energy calculation.
        vp=self.r['baseline']['Pi_reduced_path_min_V']
        cm,cp=.0015,.001
        common=(cm*5.38+cp*vp)/(cm+cp)
        ceq=cm*cp/(cm+cp)
        ediff=.5*ceq*(5.38-vp)**2+.5*2e-6*5**2
        expected=common+cm/(cm+cp)*math.sqrt(2*ediff/ceq)
        self.assertAlmostEqual(c['two_cap_counterexample_peak_V'],expected)
        self.assertGreater(expected,5.5)
        self.assertGreater(two_cap_harness_peak(cm,cp,5.38,vp,2e-6,5),5.5)

    def test_E_smaller_C_and_unlimited_overshoot_are_blocking(self):
        c=self.r['E']['CALCULATED'];self.assertGreater(c['series_only_margin_V'],0)
        self.assertLess(c['220uF_margin_V'],0);self.assertLess(c['60A_margin_V'],0)
        self.assertLess(self.r['B']['CALCULATED']['Pi_margin_with_extra_fuse_V'],0)

    def test_D_store_subtotal_does_not_bound_unknown_separate_Pi_C(self):
        a=self.r['A']['ASSUMED_targets'];d=self.r['D']['ASSUMED_targets']
        subtotal=self.r['A']['CALCULATED']['input_energy_J']+self.r['A']['CALCULATED']['initial_L_energy_J']
        subtotal+=.5*(a['Craw_bulk_max_F']+a['Craw_ceramic_max_F']+d['Cprotected_max_F'])*5.5**2
        self.assertAlmostEqual(self.r['D']['CALCULATED']['source_raw_module_store_subtotal_excluding_Pi_J'],subtotal)
        self.assertIsNone(self.r['D']['CALCULATED']['complete_all_store_energy_max_J'])

    def test_supply_charge_budget_covers_only_its_assumed_load_and_duration(self):
        supply=self.r['supply_hold_up'];a=supply['ASSUMED'];c=supply['CALCULATED']
        available=a['C_effective_min_F']*(a['Vstart_min']-a['Vvalid_min'])
        needed=a['control_A_max']*a['required_action_hold_s']+a['aggregate_gate_charge_C_max']
        self.assertGreater(available,needed)
        self.assertAlmostEqual(c['hold_s_after_gate_charge'],(available-a['aggregate_gate_charge_C_max'])/a['control_A_max'])
        self.assertIsNone(supply['actual_supply_validity'])

if __name__=='__main__':unittest.main()
