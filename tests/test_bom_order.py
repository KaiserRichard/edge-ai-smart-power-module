"""Adversarial procurement checks; no claim of electrical validation."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bom_closeout', ROOT/'docs/evidence/r2/bom_order/closeout.py')
closeout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(closeout)


class BOMOrderTests(unittest.TestCase):
    def offer(self):
        r = dict(row_id='TEST', scope='Catalog board', captured_mpn='EXACT', flags='')
        for d in closeout.CHANNELS:
            r.update({d+'_part_number':'OPEN', d+'_stock':'OPEN', d+'_qty_to_order':10,
                      d+'_order_multiple':'OPEN', d+'_unit_price_usd':'OPEN'})
        r.update(mouser_part_number='EXACT-SKU', mouser_stock=12,
                 mouser_order_multiple=1, mouser_unit_price_usd='1.00')
        return r

    def capacitor(self):
        return copy.deepcopy(closeout.DECISIONS['GRM21BR71E475KA73L'])

    def check_selection(self, a):
        closeout.assert_selection(a, a['refdes'], a['footprints'])

    def test_stock_and_price_from_different_channels_cannot_close(self):
        r = self.offer()
        r.update(mouser_unit_price_usd='OPEN', digikey_part_number='EXACT-DK',
                 digikey_stock=0, digikey_order_multiple=1, digikey_unit_price_usd='1.00')
        self.assertEqual(closeout.exact_routes(r), [])
        self.assertIsNotNone(closeout.blocker(r))

    def test_stock_must_cover_pack_rounded_quantity(self):
        r = self.offer()
        r.update(mouser_qty_to_order=20, mouser_order_multiple=10)
        self.assertEqual(closeout.exact_routes(r), [])

    def test_unknown_packing_cannot_close(self):
        r = self.offer()
        r['mouser_order_multiple'] = 'OPEN'
        self.assertIsNotNone(closeout.blocker(r))

    def test_residual_stock_does_not_close_lifecycle_hold(self):
        r = self.offer()
        self.assertIsNone(closeout.blocker(r))
        r['flags'] = 'NRND/EOL(digikey)'
        self.assertIsNotNone(closeout.blocker(r))

    def test_single_failed_bias_point_blocks_selection(self):
        a = self.capacitor()
        self.check_selection(a)
        # A stale passing minimum must not hide one failing net-voltage point.
        a['bias_tests'][-1]['ratio'] = .899
        with self.assertRaises(AssertionError):
            self.check_selection(a)

    def test_timing_hold_cannot_be_overridden_by_acceptance_boolean(self):
        a = copy.deepcopy(closeout.DECISIONS['GRM188R71H104KA93D'])
        a['order_accepted'] = True
        with self.assertRaises(AssertionError):
            self.check_selection(a)

    def test_review_cannot_expand_to_unreviewed_reference_or_footprint(self):
        a = self.capacitor()
        with self.assertRaises(AssertionError):
            closeout.assert_selection(a, a['refdes']+['C999'], a['footprints'])
        with self.assertRaises(AssertionError):
            closeout.assert_selection(a, a['refdes'], ['Capacitor_SMD:C_0603_1608Metric'])

    def test_wrong_carrier_identity_is_not_an_electrical_equivalence(self):
        a = copy.deepcopy(closeout.DECISIONS['CSD18540Q5B'])
        self.check_selection(a)
        a['mpn'] = 'CSD18542KTT'
        with self.assertRaises(AssertionError):
            self.check_selection(a)


if __name__ == '__main__':
    unittest.main()
