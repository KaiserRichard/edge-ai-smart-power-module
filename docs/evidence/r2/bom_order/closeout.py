"""BOM-close decision overlay; captured CAD identities remain immutable."""
import json
import math
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
THIRD = ROOT / 'third_party/bom_order'
DECISIONS = json.loads((THIRD / 'CLOSE_ALTERNATE_REVIEW.json').read_text())
DECISIONS.update(json.loads((THIRD / 'CLOSE_STOCK_DECISIONS.json').read_text()))
BASELINE = json.loads((HERE / 'CLOSE_BASELINE.json').read_text())
CHANNELS = ('lcsc', 'mouser', 'digikey')
LOCKS = json.loads((THIRD / 'LOCK_DECISIONS.json').read_text())
LOCK_BASELINE = json.loads((HERE / 'LOCK_BASELINE.json').read_text())
EXTERNAL = {q['row_id']: q for q in json.loads((THIRD / 'LOCK_EXTERNAL_OFFERS.json').read_text())}
ACCESSORIES = json.loads((THIRD / 'LOCK_ACCESSORIES.json').read_text())


def assert_lock(a, row):
    """The lock brief authorizes scoped defaults, never new CAD values or lands."""
    assert a['captured_mpn'] == row['captured_mpn']
    assert set(a['refdes']) == set(row['refdes'].split(', ')), 'Lock reference scope mismatch'
    assert set(a['footprints']) == set(row['footprint'].split('; ')), 'Lock footprint mismatch'
    assert a['selection'] in ('LOCKED', 'OPEN') and a['sources']
    if a['kind'] in ('exact', 'exact_limited_build'):
        assert a['mpn'] == a['captured_mpn'].replace('EEUFR1E221', 'EEU-FR1E221')
    elif a['kind'] == 'family_proxy':
        assert a['captured_mpn'] == 'C3216X7R1H475K160AB'
        assert a['mpn'] == a['proxy_mpn'] == 'C3216X7R1H475K160AC'
        assert (a['nominal_uf'], a['voltage_v'], a['dielectric'], a['tolerance_percent']) == (4.7, 50, 'X7R', 10)
        assert a['proxy_is_assumption'] is True and a['land_check']
        assert {t['refdes'] for t in a['bias_tests']} == {'C351'}
        assert [t['dc_voltage_v'] for t in a['bias_tests']] == [26, 30.788889, 35]
        assert all(.9 <= t['ratio'] <= 1.1 and t['status'] == 'ESTIMATED_SAME_FAMILY_PROXY' for t in a['bias_tests'])
    elif a['kind'] == 'drawing':
        assert a['mpn'] == a['captured_mpn'] == 'CUSTOM-FX-CU-01 RevA'
    elif a['kind'] in ('mechanical', 'kit'):
        assert row['captured_mpn'] == 'N/A accessory' and row['footprint'] == 'Off-board'
    else:
        assert a['kind'] == 'hard_stop' and a['selection'] == 'OPEN'
        assert a['mpn'] == row['captured_mpn']


def lock_identity(row):
    a = LOCKS.get(row['row_id'])
    if a:
        assert_lock(a, row)
        row.update(mpn=a['mpn'], manufacturer=a['manufacturer'])


def offer_terms(q, needed):
    """Never combine offers, currencies, pieces and packs to create availability."""
    pack = q.get('units_per_pack', 1)
    qty = math.ceil(int(needed) / pack)
    minimum, multiple = q['minimum'], q['multiple']
    known_pack = isinstance(minimum, int) and minimum > 0 and isinstance(multiple, int) and multiple > 0
    if known_pack:
        qty = math.ceil(max(qty, minimum) / multiple) * multiple
    prices = [(int(n), Decimal(p)) for n, p in q['price_tiers'] if int(n) <= qty]
    price = max(prices)[1] if prices else None
    ready = (known_pack and q['sku'] not in ('OPEN', 'N/A') and isinstance(q['stock'], int)
             and q['stock'] >= qty and q['currency'] in ('USD', 'EUR', 'AUD', 'GBP') and price is not None)
    return dict(qty=qty, price=str(price) if price is not None else 'OPEN',
                extended=str(price * qty) if price is not None else 'OPEN', ready=ready,
                supplied_units=qty * pack)


def kit_ready(ident):
    parts = [p for p in ACCESSORIES if p['parent'] == ident]
    return bool(parts) and all(offer_terms(p, p['planning_qty'])['ready'] for p in parts)


def lock_annotation(row):
    a = LOCKS.get(row['row_id'])
    row['selection_status'] = a['selection'] if a else ('N/A' if row['scope'] == 'PCB feature' else 'PREVIOUSLY SELECTED')
    row['selection_reason'] = a['reason'] if a else 'N/A: retained prior reviewed selection'
    row['selected_route'] = a['procurement_route'] if a else 'See distributor columns'
    row['lock_review'] = 'bom_order/LOCK_REVIEW.md' if a else 'N/A'
    if a:
        row['notes'] += ' BOM_LOCK_ALL default: ' + a['reason']
        row.update(alternate_mpn=a['mpn'], alternate_manufacturer=a['manufacturer'],
                   alternate_source='bom_order/LOCK_REVIEW.md',
                   alternate_status=a['selection'] + ': ' + a['reason'])
        row['flags'] += '; LOCK-' + a['selection']
    q = EXTERNAL.get(row['row_id'])
    fields = ('supplier', 'sku', 'stock', 'currency', 'qty', 'order_unit', 'units_per_pack', 'price', 'extended', 'url', 'observed_date', 'evidence_id', 'notes')
    values = dict(q, **offer_terms(q, row['qty_to_order'])) if q else {}
    for field in fields:
        row['additional_' + field] = values.get(field, 'N/A')


def lifecycle_cleared(row):
    a = LOCKS.get(row['row_id'])
    return bool(a and a['kind'] == 'exact_limited_build' and a['selection'] == 'LOCKED'
                and row['mpn'] == row['captured_mpn'] == a['mpn'])


def eligible_lcsc(row):
    return (row['scope'] == 'Catalog board' and 'lcsc' in exact_routes(row)
            and not any(s in row['flags'] for s in ('EXACT-ORDER', 'OWNER-HOLD', 'LOCK-OPEN'))
            and ('NRND/EOL' not in row['flags'] or lifecycle_cleared(row)))

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
    lock = LOCKS.get(row['row_id'])
    if lock:
        if lock['selection'] == 'OPEN':
            return lock['reason']
        q = EXTERNAL.get(row['row_id'])
        if exact_routes(row) or (q and q['mpn'] == row['mpn'] and offer_terms(q, row['qty_to_order'])['ready']):
            return None
        if lock['kind'] == 'kit' and kit_ready(row['row_id']):
            return None
        return 'Selection LOCKED; supply only: ' + lock['procurement_route']
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
    old = {r['row_id'] for r in LOCK_BASELINE['needs_owner_decision']}
    new = {r['row_id'] for r in holds}
    return dict(access_date='2026-10-04', definition='Immediate procurement OPEN: no complete stocked exact/accepted offer, or unresolved selection. Explicit finite-build lifecycle decisions accepted; additional suppliers and original currencies retained separately. Quote/backorder is not stocked.',
        open_before=LOCK_BASELINE['open_after'], open_after=len(holds),
        selection_open_before=len(old), selection_open_after=sum(a['selection']=='OPEN' for a in LOCKS.values()),
        selection_locked_row_ids=sorted(k for k,a in LOCKS.items() if a['selection']=='LOCKED'),
        closed_row_ids=sorted(old-new), newly_open_row_ids=sorted(new-old),
        literal_open_cells_before=LOCK_BASELINE['literal_open_cells_after'],
        literal_open_cells_after=sum(v == 'OPEN' for r in rows for v in r.values()),
        rows_containing_open_before=LOCK_BASELINE['rows_containing_open_after'],
        rows_containing_open_after=sum(any('OPEN' in str(v) for v in r.values()) for r in rows),
        procurement_open=holds,
        needs_owner_decision=[h for h in holds if h['row_id'] in LOCKS and LOCKS[h['row_id']]['selection']=='OPEN'],
        selected_alternates=[dict(row_id=r['row_id'], original=r['captured_mpn'], alternate=r['mpn'],
            reason=DECISIONS[r['captured_mpn']]['reason'], routes=exact_routes(r))
            for r in rows if r['captured_mpn'] in DECISIONS and DECISIONS[r['captured_mpn']]['order_accepted']],
        exact_stock_closures=[dict(row_id=r['row_id'], mpn=r['mpn'], routes=exact_routes(r))
            for r in rows if r['row_id'] in old-new and r['captured_mpn'] not in DECISIONS])
