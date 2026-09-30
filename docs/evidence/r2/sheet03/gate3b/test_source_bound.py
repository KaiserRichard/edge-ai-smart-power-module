"""Independent checks of physics, domain limits and unknown-bound handling."""
import math
import unittest
from calculate_source_bound import calculate, graph_ramp, integral, envelope_charge

class SourceBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=calculate()

    def test_constant_inductance_ramp_and_charge(self):
        points=[[0,5],[100,5]];vin=24;initial=8;t=3e-6
        got=graph_ramp(points,vin,initial,t)
        self.assertAlmostEqual(got['I_A'],initial+vin*t/5e-6)
        self.assertAlmostEqual(got['Q_C'],initial*t+vin*t*t/(2*5e-6))

    def test_weighted_integral_is_energy_not_flux(self):
        self.assertAlmostEqual(integral([[0,5],[100,5]],8,60,True),.5*5e-6*(60**2-8**2))
        self.assertAlmostEqual(integral([[0,5],[100,5]],8,60),5e-6*(60-8))

    def test_curve_end_is_not_extrapolated(self):
        got=graph_ramp([[0,5],[20,5]],28,8,20e-6)
        self.assertIsNone(got['I_A']);self.assertIsNone(got['Q_C'])
        with self.assertRaises(ValueError):integral([[0,5],[20,5]],8,21)

    def test_larger_curve_changes_current_and_charge(self):
        small=self.r['curve_models']['74437636350652']['maintained_source_fault_screens']
        large=self.r['curve_models']['74437636351002']['maintained_source_fault_screens']
        self.assertGreater(small[-2]['I_A'],large[-2]['I_A'])
        self.assertGreater(small[-2]['Q_C'],large[-2]['Q_C'])

    def test_source_energy_and_domain_conserve_at_all_corners(self):
        a=self.r['ASSUMED_source_contract']
        for s in self.r['CALCULATED_source_contract']:
            v=s['Vin_V']
            independent=.5*a['Cin_effective_max_F']*v*v+v*a['source_positive_charge_until_actual_current_isolation_C']+.5*a['Ldiff_max_H']*a['initial_L_current_A_max']**2
            self.assertAlmostEqual(independent,s['new_fault_pool_J'])
            self.assertAlmostEqual(.5*a['Ldiff_min_H']*s['conditional_L_current_ceiling_A']**2,independent)
            self.assertLess(s['conditional_L_current_ceiling_A'],80)
            self.assertLess(s['conditional_L_current_ceiling_A'],a['Ldiff_qualified_domain_A'])

    def test_old_local_cap_bank_exits_proposed_curve_domain(self):
        s=self.r['CALCULATED_source_contract'][-1]
        self.assertGreater(s['existing_Cin_60p996uF_I_screen_A'],100)

    def test_input_source_charge_is_not_output_charge(self):
        s=self.r['CALCULATED_source_contract'][-1]
        self.assertGreater(s['L_envelopes'][2]['Q_to_raw_upper_C'],self.r['ASSUMED_source_contract']['source_positive_charge_until_actual_current_isolation_C'])

    def test_capped_current_envelope_integrates_both_segments(self):
        # 8A+2A/us reaches10A at1us, then10A for2us.
        self.assertAlmostEqual(envelope_charge(8,2e6,10,3e-6),29e-6)

    def test_missing_application_bounds_are_never_zero(self):
        self.assertIsNone(self.r['actual_source_current_max_A'])
        self.assertIsNone(self.r['actual_source_energy_max_J'])
        d=self.r['D_E_rescore']
        self.assertIsNone(d['D_application_Pi_peak_V']);self.assertIsNone(d['E_application_Pi_peak_V'])
        self.assertEqual(d['actual_trip_min_max_V'],[None,None])
        self.assertIsNone(d['D_complete_store_max_J'])

    def test_last_path_choke_limit_requires_actual_off_time(self):
        d=self.r['D_E_rescore']
        self.assertLess(d['E_current_with35uH_2us_31p5V_A'],10)
        self.assertGreater(8+31.5*3e-6/35e-6,10)

    def test_series_off_does_not_dispose_of_downstream_magnetic_energy(self):
        d=self.r['D_E_rescore']
        voltage=d['E_no_absorber_choke_tail_counterexample_V']
        self.assertAlmostEqual(.5*.001*(voltage**2-5.34**2),.5*50e-6*8**2)
        self.assertLess(d['E_no_absorber_choke_tail_margin_V'],0)
        self.assertGreater(d['E_ideal_constant5p42V_choke_tail_charge_screen_C'],d['E_initial_interval_received_charge_screen_C'])
        self.assertAlmostEqual(5.42*d['E_ideal_constant5p42V_choke_tail_charge_screen_C'],.5*50e-6*10**2)
        self.assertIsNone(d['E_application_total_protected_charge_C'])

    def test_normal_nuisance_counterexamples_remain_blocking(self):
        d=self.r['D_E_rescore']
        self.assertGreater(d['normal6_false_trip_reserve_V'],0)
        self.assertLess(d['normal8_false_trip_reserve_V'],0)
        self.assertLess(d['normal6_30us_reserve_V'],0)

    def test_resistance_target_depends_on_contact_reduction(self):
        d=self.r['D_E_rescore'];r=d['E_normal_loop_target_ohm']
        self.assertLess(r,.05)
        self.assertGreater(r+.009375,.05)
        self.assertLess(d['E_existing_loop_plus_10mohm_Pi_V'],4.75)

    def test_hold_up_accounts_for_aggregate_gate_charge(self):
        s=self.r['supply_hold']
        available=s['effective_C_F']*(s['Vstart_min']-s['Vvalid_min'])
        needed=s['Icontrol_A']*s['hold_required_s']+s['Qg_aggregate_C']
        self.assertGreater(available,needed)
        self.assertAlmostEqual(s['required_C_F'],needed/.7)

if __name__=='__main__':unittest.main()
