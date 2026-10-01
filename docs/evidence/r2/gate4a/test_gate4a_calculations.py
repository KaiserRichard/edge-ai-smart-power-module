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

    def test_loaded_detector_against_independent_thevenin_solution(self):
        from calculate_gate4a_fix import loaded_divider
        # Solve the source divider as a Thevenin equivalent, not the KCL implementation.
        for rt, rb, rs, rp, ron, leak in [(11300.,10000.,1000.,1e6,0.,0.),
                                          (9880.,10000.,1000.,1e5,17.,1.125e-6)]:
            vraw=loaded_divider(rt,rb,rs,rp,ron,2.5,leak)
            rth=rt*rb/(rt+rb)+rs+ron
            vs=(vraw*rb/(rt+rb)-leak*rth)/(1+rth/rp)
            self.assertAlmostEqual(vs,2.5,places=12)
        detector=self.data['gate4a_fix']['detector']
        self.assertLess(detector['conditional_20mV_overdrive_raw_upper_V'],5.38)
        self.assertEqual(detector['actual_trip_min_max_V'],[None,None])

    def test_recovered_machine_registers_and_regenerated_artifact_match(self):
        p=Path(__file__).parent
        manifest=json.loads((p/'FREEZE_MANIFEST.json').read_text())['changes']
        with (p/'FREEZE_BOM.csv').open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),len(manifest))
        for r,m in zip(rows,manifest):
            self.assertEqual(r,{**m,'refdes':','.join(m['refdes'])})
        self.assertEqual(json.loads((p/'CALCULATIONS.json').read_text()),self.data)

    def test_measurement_error_cannot_discard_tail_or_additive_voltage_errors(self):
        from calculate_gate4a_fix import charge_uncertainty, energy_error_without_skew
        short=charge_uncertainty(100e-6,10e-6)
        tail=charge_uncertainty(100e-6,.002)
        self.assertAlmostEqual(short,1.65e-6,places=12)
        self.assertAlmostEqual(tail-short,.010*(.002-10e-6),places=12)
        self.assertGreater(energy_error_without_skew(.1,.2,.0138,.002),.00349)
        self.assertIsNone(self.data['gate4a_fix']['measurement']['calibration_records'])

    def test_relative_skew_counterexample_exceeds_old_endpoint_only_budget(self):
        from calculate_gate4a_fix import energy_error_without_skew, skew_total_variation_bound
        # Integrate a single sinusoid period numerically, then repeat 10,000 times.
        # This is the independent check's mathematical example, not a DUT trace.
        frequency, duration, delta, samples = 5e6, .002, 4e-9, 4096
        period = 1/frequency
        def energy(shift):
            terms = []
            for k in range(samples):
                t = (k+.5)*period/samples
                v = 3.45*(1+math.cos(2*math.pi*frequency*t))
                i = 10*(1+math.sin(2*math.pi*frequency*(t+shift)))
                terms.append(v*i)
            return math.fsum(terms)*duration/samples
        actual_error = abs(energy(delta)-energy(0))
        self.assertAlmostEqual(energy(0), .069, places=12)
        self.assertAlmostEqual(actual_error, .0345*math.sin(2*math.pi*frequency*delta), places=12)
        self.assertGreater(actual_error, energy_error_without_skew(.1,.2,.0138,.002))
        variation = 40*frequency*duration
        conservative = skew_total_variation_bound(6.9, delta, variation)
        self.assertAlmostEqual(conservative, .01104, places=12)
        self.assertGreater(conservative, actual_error)

    def test_missing_skew_bound_cannot_be_reported_as_complete_energy_uncertainty(self):
        from calculate_gate4a_fix import energy_uncertainty, energy_error_without_skew
        self.assertIsNone(energy_uncertainty(.1,.2,.0138,.002))
        self.assertIsNone(self.data['gate4a_fix']['measurement']['U_energy_example_J'])
        base=energy_error_without_skew(.1,.2,.0138,.002)
        self.assertAlmostEqual(energy_uncertainty(.1,.2,.0138,.002,u_skew=.01104),base+.01104)
        for invalid in (-1., float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                energy_uncertainty(.1,.2,.0138,.002,u_skew=invalid)

    def test_raw_dump_energy_sharing_by_independent_time_integration(self):
        # Integrate each resistor loss in a capacitor discharge; check the proposed
        # worst-corner share against energy conservation without using its formula.
        f=.0135
        resistors=[.033*(1+f)]+[.033*(1-f)]*5+[.033*(1+f)]*6
        branch=[sum(resistors[:6]),sum(resistors[6:])]
        capacitance=.00559656; v0=6.881668479208298
        req=1/(1/branch[0]+1/branch[1]); tau=req*capacitance
        dt=20*tau/20000
        energy=[0.]*12
        for n in range(20001):
            voltage=v0*math.exp(-n*dt/tau)
            weight=.5 if n in (0,20000) else 1.
            for k,r in enumerate(resistors):
                energy[k]+=weight*dt*(voltage/branch[k//6])**2*r
        initial=.5*capacitance*v0*v0
        self.assertAlmostEqual(sum(energy)/initial,1.,places=6)
        raw=self.data['gate4a_fix']['raw_dump']
        self.assertAlmostEqual(energy[0]/sum(energy),raw['worst_corner_part_energy_fraction'],places=10)
        self.assertLess(raw['worst_corner_resistor_energy_J'],.009)
        self.assertIsNone(raw['actual_hot_pulse_rating_J'])

    def test_supervisor_startup_includes_rising_hysteresis(self):
        aux=self.data['gate4a_fix']['auxiliary']
        self.assertGreater(aux['old110k_detector_rise_upper_V'],5.)
        self.assertLess(aux['new_detector_supervisor_rise_upper_V'],4.75)
        self.assertLess(aux['new_detector_supervisor_min_max_V'][0],4.75)
        self.assertIsNone(aux['actual_startup_min_max_s'][0])
        # Startup monitor selection cannot silently become a fast rail-floor proof.

    def test_RUN_divider_leakage_screen_at_low_line(self):
        c=self.data['gate4a_fix2']['converter']
        self.assertGreater(c['old464k_RUN_rising_screen_V'][1],7.5)
        self.assertLess(c['RUN_rising_screen_V'][1],7.5)
        # Independent Norton/KCL calculation at the least favorable high corner.
        rt,rb=383e3*1.0025,100e3*.9975
        run_voltage=(7.5/rt-3e-6)/(1/rt+1/rb)
        self.assertGreater(run_voltage,1.26)
        self.assertLess(c['ENOUT_sink_upper_at35V_screen_A'],.1e-3)
        self.assertIsNone(c['actual_stability'])
        self.assertIsNone(c['actual_RUN_release_V'])

    def test_coupled_pool_and_protected_resistor_energy_by_independent_integral(self):
        c=self.data['gate4a_fix2']['coupled_energy']
        # Assemble the pool from physical stores, not the raw-only subtotal.
        energy=(.5*(5.59656e-3+2.7072e-3+2.2e-3)*5.5**2
                +.5*30e-6*28.289211046948948**2
                +28.289211046948948*100e-6+.5*12e-6*8**2)
        self.assertAlmostEqual(c['scenarios'][0]['pool_assumed_J'],energy,places=12)
        self.assertGreater(energy,c['raw_only_pool_J'])
        # A zero-source discharge tests sharing independently of corner enumeration.
        rs=[.033*1.0135,.033*.9865,.033*1.0135,.033*1.0135]
        a,b=sum(rs[:2]),sum(rs[2:]); req=1/(1/a+1/b)
        cap=2*energy/5.5**2; tau=req*cap; steps=20000; dt=20*tau/steps
        ej=math.fsum((5.5*math.exp(-(n+.5)*dt/tau)/a)**2*rs[0]*dt for n in range(steps))
        self.assertAlmostEqual(ej/energy,c['protected_max_part_fraction'],places=6)
        self.assertIsNone(c['actual_rating_margin'])


if __name__ == '__main__':
    unittest.main()
