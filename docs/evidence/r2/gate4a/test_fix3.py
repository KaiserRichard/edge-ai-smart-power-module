"""Independent arithmetic/logic regressions. No analog-race or hardware proof."""
import json
import math
from pathlib import Path
import unittest
from calculate_gate4a_fix3 import calculate, loaded_threshold


class Fix3Screens(unittest.TestCase):
    def test_loaded_divider_kcl_and_reference_intervals(self):
        # Solve KCL backwards at the nominal switch output; include the 100k load.
        vt = 1.25
        for rt, rb in [(69800.,10000.),(26100.,10000.),(49900.,10000.)]:
            node = vt + 17*vt/100000
            vin = node + rt*(node/rb+vt/100000)
            bounds = loaded_threshold(rt,rb,vt,.015)
            self.assertLessEqual(bounds[0],vin)
            self.assertGreaterEqual(bounds[1],vin)

    def test_normal_DCM_and_pulsed_failure_are_distinct(self):
        d=calculate()['source']
        self.assertGreater(d['SW_rise_V'][0],5.1)
        self.assertLess(d['SW_fall_V'][1],5.1)
        # Independently step a repeating HIGH 3us / LOW 1us logic input.
        elapsed=0.
        fired=False
        for n in range(2000):
            high=(n % 400)<300
            elapsed=elapsed+1e-8 if high else 0.
            fired |= elapsed>=d['qualifier_s'][0]
        self.assertFalse(fired)
        self.assertIsNone(d['internal_bridge_fault_coverage'])
        self.assertEqual(d['actual_complete_interval_s'],[None,None])
        self.assertLess(d['complete_conditional_interval_s'][1],10e-6)

    def test_regulator_release_and_short_diagnostic_headroom(self):
        d=calculate()['interlock']
        self.assertGreater(d['LDO_min_max_V'][0],d['threshold_intervals_V']['DET5'][1])
        self.assertGreater(d['LDO_min_max_V'][0],4.65*1.02*1.025)
        self.assertLess(d['LDO_min_max_V'][1],5.25)
        self.assertGreater(d['SER_DRV_start_V'],d['threshold_intervals_V']['SER_DRV'][1])
        self.assertLess(d['aux_input_screen_A'],.045/(.33*1.01))
        self.assertLess(d['charger_Tj_screen_C'],125)
        self.assertLess(d['historical_4700ohm_feed']['healthy_VIN_min_V'],
                        d['threshold_intervals_V']['DIAG_VIN'][0])
        self.assertGreater(d['diagnostic_feed']['healthy_VIN_min_V'],
                           d['threshold_intervals_V']['DIAG_VIN'][1])
        self.assertLess(d['diagnostic_feed']['feed_power_max_W'],.110)
        # A hard short cannot exhibit the simultaneous required voltage difference.
        for r in [0,1,10,100]:
            self.assertLess(r*d['diagnostic_current_max_A'],
                            d['threshold_intervals_V']['DIAG_VIN'][0]-
                            d['threshold_intervals_V']['ZERO'][1])

    def test_driver_reservoir_charge_conservation(self):
        d=calculate()['interlock']
        qinitial=5e-6*d['threshold_intervals_V']['SER_DRV'][0]
        qfinal=qinitial-.20e-6-math.fsum([.005*3e-9]*1000)
        self.assertGreater(qfinal/5e-6,10.5)
        self.assertGreater(d['release_recovery_s'][0],.0009)
        self.assertIsNone(d['actual_hold_s'])

    def test_generated_round3_and_unique_refs(self):
        here=Path(__file__).parent
        self.assertEqual(json.loads((here/'FIX3_CALCULATIONS.json').read_text()),calculate())
        refs=[r for row in json.loads((here/'FREEZE_MANIFEST.json').read_text())['changes']
              for r in row['refdes']]
        self.assertEqual(len(refs),len(set(refs)))


if __name__=='__main__':
    unittest.main()
