"""BOM-close decision overlay; captured CAD identities remain immutable."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
THIRD = ROOT / 'third_party/bom_order'
DECISIONS = json.loads((THIRD / 'CLOSE_ALTERNATE_REVIEW.json').read_text())
DECISIONS.update(json.loads((THIRD / 'CLOSE_STOCK_DECISIONS.json').read_text()))
BASELINE = json.loads((HERE / 'CLOSE_BASELINE.json').read_text())
CHANNELS = ('lcsc', 'mouser', 'digikey')

# Explanations reference the sourced reviews; they never authorize a substitution.
OWNER_REASONS = {
    'B009': 'Exact PCH1V471MCL1GS supplier quote required; another bank capacitor changes ESR/ESL, energy and fault behavior.',
    'B011': 'C3216X7R1H475K160AB ordering code unverified; AC candidate needs bias, lands and converter review.',
    'B014': 'Exact straight-lead EEU-FR1E221 stock absent; another part needs lead-fit, ESR and hold-up review.',
    'B015': 'Exact Littelfuse SMCJ36CA stock absent; Diodes same-number candidate needs hot-clamp/pulse/fuse coordination review.',
    'B026': 'Approve force-link finishing/tolerances, joint stack/torque and installed current envelope; fabricator quote required.',
    'B038': 'Exact 348 kohm resistor stock absent; ERA-6AEB3483V power/voltage/thermal margins affect protection threshold.',
    'B045': 'Exact 24.4 kohm order code unverified; rounding changes output setpoint and Sheet03 path budget.',
    'B053': '53 exact WFMB2512R0330FEA ballast parts unavailable; 1 W WSL candidate needs WFM-land, pulse, thermal and sharing review.',
    'B068': 'Exact 365 kohm resistor stock absent; Panasonic candidate also lacks stock and threshold power/voltage/TCR review.',
    'B080': 'TPS26630RGER/RGET stock absent; preserve latch-off variant, timing, current limit and RGE pinout.',
    'B093': 'INA228AIDGSR stock absent; obsolete/restricted AIDGST proposal rejected. Different monitor needs range/pin/telemetry review.',
    'H01': 'Exact 1777989 stock absent in newer Mouser/DigiKey snapshots; confirm source for the selected mating plug.',
    'H05': 'Exact 3-87456-6 housing stock absent; marketplace supply is not accepted; confirm exact housing source.',
    'H08': 'Exact 8521 010100 needs one coherent supplier SKU/stock/USD price/pack offer for a 100 ft spool.',
    'M01': 'Choose and quote exact M4x12 A2-70 bolt code after force-link joint-stack approval (48 required).',
    'M02': 'Choose and quote exact 4.3/9/0.8 mm washer code and finish (96 required).',
    'M03': 'Choose and quote exact all-metal M4 nut code/finish after stack/torque review (48 required).',
    'O01': 'Define input/control/I2C mating harnesses, contacts, wire and manual links before quantities and sourcing.',
    'O02': 'Define thermal interfaces, live-tab insulation and mounting after thermal/layout review before sourcing.',
}


def assert_selection(decision, refs, footprints):
    """Reject incomplete evidence or scope expansion before changing an order identity."""
    assert decision['order_accepted'] is True
    assert decision['status'] == 'CONFIRMED' and decision['owner_hold'] == 'N/A'
    assert set(refs) == set(decision['refdes']), 'Alternate reference scope mismatch'
    assert set(footprints) == set(decision['footprints']), 'Alternate footprint mismatch'
    if decision.get('kind') == 'carrier_only':
        assert decision['original_mpn'] == 'CSD18540Q5B' and decision['mpn'] == 'CSD18540Q5BT'
        assert decision['document_revision'] and decision['offer_evidence']
    else:
        assert decision['accepted'] is True
        assert decision['alternate_specs']['production_status_en-us'] == 'B'
        assert float(decision['alternate_specs']['rvol']) >= float(decision['original_specs']['rvol'])
        assert decision['alternate_specs']['tempchar'] == decision['original_specs']['tempchar']
        assert set(t['refdes'] for t in decision['bias_tests']) == set(refs)
        assert decision['min_ratio'] >= .90
        assert all(t['status'] == 'CALCULATED' and t['ratio'] >= .90 for t in decision['bias_tests'])


def exact_routes(row):
    routes = []
    for d in CHANNELS:
        stock, qty = str(row[d+'_stock']), str(row[d+'_qty_to_order'])
        multiple = str(row[d+'_order_multiple'])
        if (row[d+'_part_number'] not in ('OPEN', 'N/A')
                and stock.isdigit() and qty.isdigit() and int(qty) > 0 and int(stock) >= int(qty)
                and multiple.isdigit() and int(multiple) > 0
                and row[d+'_unit_price_usd'] not in ('OPEN', 'N/A')):
            routes.append(d)
    return routes


def blocker(row):
    if row['scope'] == 'PCB feature':
        return None
    decision = DECISIONS.get(row['captured_mpn'])
    if decision and not decision['order_accepted']:
        return decision['owner_hold'].removeprefix('OPEN: ').removeprefix('OPEN: ')
    if any(flag in row['flags'] for flag in ('NRND/EOL', 'EXACT-ORDER', 'OWNER-HOLD')):
        return OWNER_REASONS.get(row['row_id'], 'Resolve lifecycle/exact-code/owner hold before order acceptance.')
    if not exact_routes(row):
        return OWNER_REASONS.get(row['row_id'], 'Obtain one exact/accepted MPN offer with SKU, enough stock, USD price and known order multiple.')
    return None


def summary(rows):
    holds = [dict(row_id=r['row_id'], mpn=r['mpn'], refdes=r['refdes'], reason=reason)
             for r in rows if (reason := blocker(r))]
    old = set(BASELINE['open_order_row_ids'])
    new = {r['row_id'] for r in holds}
    return dict(access_date='2026-10-04', definition=BASELINE['open_definition'],
        open_before=BASELINE['open_order_rows'], open_after=len(holds),
        closed_row_ids=sorted(old-new), newly_open_row_ids=sorted(new-old),
        literal_open_cells_before=BASELINE['literal_open_cells'],
        literal_open_cells_after=sum(v == 'OPEN' for r in rows for v in r.values()),
        rows_containing_open_before=BASELINE['rows_containing_open'],
        rows_containing_open_after=sum(any('OPEN' in str(v) for v in r.values()) for r in rows),
        needs_owner_decision=holds,
        selected_alternates=[dict(row_id=r['row_id'], original=r['captured_mpn'], alternate=r['mpn'],
            reason=DECISIONS[r['captured_mpn']]['reason'], routes=exact_routes(r))
            for r in rows if r['captured_mpn'] in DECISIONS and DECISIONS[r['captured_mpn']]['order_accepted']],
        exact_stock_closures=[dict(row_id=r['row_id'], mpn=r['mpn'], routes=exact_routes(r))
            for r in rows if r['row_id'] in old-new and r['captured_mpn'] not in DECISIONS])
