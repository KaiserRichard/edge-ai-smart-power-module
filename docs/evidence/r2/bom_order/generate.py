#!/usr/bin/env python3
"""Rebuild the order documents from the pinned KiCad export and recorded catalog facts."""
import csv
import hashlib
import json
import math
import re
from collections import defaultdict, Counter
from decimal import Decimal
from pathlib import Path
from closeout import (DECISIONS, LOCKS, ACCESSORIES, assert_selection, summary,
                      lock_identity, lock_annotation, offer_terms, blocker, eligible_lcsc)

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'docs/evidence/r2'
EVIDENCE = OUT / 'bom_order'
FACTS = ROOT / 'third_party/bom_order/CATALOG_FACTS.json'
CHANNELS = ('lcsc', 'mouser', 'digikey')
META = json.loads((EVIDENCE / 'PROVENANCE.json').read_text())
SOURCE = list(csv.DictReader((EVIDENCE / 'SOURCE_BOM.csv').open()))
DRAFT = list(csv.DictReader((OUT / 'BOM_DRAFT.csv').open()))
QUOTES = json.loads(FACTS.read_text())
QUOTES += json.loads((FACTS.parent / 'RESUME_CATALOG_FACTS.json').read_text())
QUOTES += json.loads((FACTS.parent / 'CLOSE_CATALOG_FACTS.json').read_text())
QUOTES += json.loads((FACTS.parent / 'CLOSE_RESUME_CATALOG_FACTS.json').read_text())
QUOTES += json.loads((FACTS.parent / 'LOCK_CATALOG_FACTS.json').read_text())
Q = {(q['mpn'], q['d']): q for q in QUOTES}
ALT_REVIEW = json.loads((FACTS.parent / 'ALTERNATE_REVIEW.json').read_text())
NATIVE_URL = META['source_repository'] + '/blob/' + META['source_commit'] + '/'

def norm(mpn):
    return mpn.replace('EEUFR1E221', 'EEU-FR1E221')

def natural(ref):
    return re.sub(r'\d+', lambda m: m.group().zfill(6), ref)

def manufacturer(mpn):
    old = next((r['manufacturer'] for r in DRAFT if r['mpn'] == mpn and r['manufacturer'] != 'OPEN'), None)
    if old:
        return old
    if mpn.startswith(('TNPW', 'CRCW')):
        return 'Vishay'
    if mpn.startswith(('TPS', 'SN74')):
        return 'Texas Instruments'
    return 'OPEN'

def quote(mpn, channel):
    return Q.get((mpn, channel), dict(sku='OPEN', stock='OPEN', lifecycle='OPEN', minimum='OPEN', multiple='OPEN',
        price_tiers=[], lead_time='OPEN', url='OPEN', observed_date='2026-10-03', crawl_age='N/A', evidence_id='OPEN',
        notes=['No exact manufacturer/MPN listing verified in the recorded searches.']))

def spare(qty, passive=False):
    return max(2 if passive else 1, math.ceil(Decimal(str(qty)) / 10))

def commercial(row):
    mpn = row['mpn']
    flags = []
    observed = []
    has_price = []
    for d in CHANNELS:
        q = quote(mpn, d)
        n = row['qty_to_order']
        not_bought = row['scope'] == 'PCB feature'
        for field, key in [('part_number','sku'), ('stock','stock'), ('lead_time','lead_time'), ('lifecycle','lifecycle'),
                           ('minimum_order','minimum'), ('order_multiple','multiple'), ('source_url','url'),
                           ('observed_date','observed_date'), ('crawl_age','crawl_age'), ('evidence_id','evidence_id')]:
            row[d + '_' + field] = 'N/A' if not_bought else q[key]
        notes = list(q['notes'])
        if q.get('identity_source_url'):
            notes.append('SKU/alias identity source: '+q['identity_source_url'])
        if isinstance(n, int) and not not_bought:
            if isinstance(q['minimum'], int):
                n = max(n, q['minimum'])
            if isinstance(q['multiple'], int) and q['multiple'] > 0:
                n = math.ceil(n / q['multiple']) * q['multiple']
            elif q['sku'] != 'OPEN':
                notes.append('Order multiple OPEN; quantity is a planning minimum, not a confirmed pack quantity.')
        row[d + '_qty_to_order'] = 0 if not_bought else n
        applicable = [(int(t), Decimal(str(p))) for t, p in q['price_tiers'] if isinstance(n, int) and int(t) <= n]
        priced = bool(applicable) and q.get('currency') == 'USD' and q['sku'] != 'OPEN' and isinstance(n, int) and n > 0
        tier, price = max(applicable) if priced else ('OPEN', None)
        row[d + '_price_break'] = 'N/A' if not_bought else tier
        row[d + '_unit_price_usd'] = 'N/A' if not_bought else str(price) if priced else 'OPEN'
        row[d + '_extended_usd'] = 'N/A' if not_bought else str(price * n) if priced else 'OPEN'
        row[d + '_notes'] = 'Etched copper; included in PCB, no purchased part.' if not_bought else '; '.join(notes)
        if priced:
            has_price.append(d)
        if isinstance(q['stock'], int) and not not_bought:
            if q['stock'] == 0:
                flags.append('OOS(' + d + ')')
            else:
                observed.append(d)
                if isinstance(n, int) and q['stock'] < n:
                    flags.append('SHORTFALL(' + d + ')')
        if re.search(r'Obsolete|End of Life|Not For New|NRND', q['lifecycle'], re.I):
            flags.append('NRND/EOL(' + d + ')')
        if re.search(r'Discontinued|Restricted', q['lifecycle'], re.I):
            flags.append('CHANNEL-RESTRICTION(' + d + ')')
    if not_bought:
        row.update(flags='NOT PURCHASED', lifecycle='N/A', alternate_mpn='N/A', alternate_manufacturer='N/A', alternate_source='N/A', alternate_status='N/A')
        return
    if len(observed) == 1:
        flags.append('SINGLE-OBSERVED(' + observed[0] + ')')
    if not observed:
        flags.append('NO-CONFIRMED-STOCK')
    if not has_price:
        flags.append('NO-VERIFIED-PRICE')
    lives = [d + ': ' + row[d + '_lifecycle'] for d in CHANNELS if row[d + '_lifecycle'] != 'OPEN']
    row['lifecycle'] = '; '.join(lives) or 'OPEN'
    row['flags'] = '; '.join(flags) or 'No supply flag in retrieved evidence'
    # Catalog alternates are proposals only. Preserve the selected MPN and its quantities.
    candidates = []
    for d in CHANNELS:
        q = quote(mpn, d)
        for a in q.get('alternate_candidates', []):
            candidates.append((a, q['url']))
    candidates.sort(key=lambda p: (int(p[0].get('stock', '0')) > 0, p[0].get('classification') == 'Direct'), reverse=True)
    row.update(alternate_mpn='OPEN', alternate_manufacturer='OPEN', alternate_source='OPEN',
        alternate_status='OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized.')
    if candidates:
        a, url = candidates[0]
        row.update(alternate_mpn=a['mpn'], alternate_manufacturer=a['manufacturer'], alternate_source=url,
            alternate_status='UNAPPROVED catalog candidate (' + a['classification'] + '); recheck package/pins, ratings, timing and application. Not in order quantities.')
    overrides = {
        'C3216X7R1H475K160AB': ('C3216X7R1H475K160AC', 'TDK', 'Suffix AC is a catalog candidate, not an alias for AB; verify DC-bias capacitance, package and compensation. Stock remains a separate issue.'),
        'TNPW0805348KBEEA': ('ERA-6AEB3483V', 'Panasonic Industry', '348 kohm, 0.1%, 25 ppm/K, 0805 candidate; 0.125 W rating differs. Verify voltage and power margins.'),
        'TNPW0805365KBEEA': ('ERA-6AEB3653V', 'Panasonic Industry', '365 kohm, 0.1%, 25 ppm/K, 0805 candidate; 0.125 W rating differs. Verify voltage and power margins.'),
        'INA228AIDGSR': ('INA228AIDGST', 'Texas Instruments', 'Same device/package family with different packing suffix; verify exact ordering table and availability.'),
        'TPS26630RGER': ('TPS26630RGET', 'Texas Instruments', 'Different packing suffix candidate; preserve latch-off device variant and RGE package. No confirmed availability guarantee.'),
        'TPS7A1601DGNR': ('TPS7A1601DGNT', 'Texas Instruments', 'Different packing suffix candidate; verify ordering table and DGN thermal pad. No confirmed availability guarantee.'),
    }
    if mpn in overrides:
        a, maker, note = overrides[mpn]
        evidence = next((quote(a, d)['url'] for d in ('digikey', 'mouser', 'lcsc') if quote(a, d)['sku'] != 'OPEN'), 'OPEN')
        row.update(alternate_mpn=a, alternate_manufacturer=maker, alternate_source=evidence, alternate_status='UNAPPROVED: ' + note)
    if mpn == 'PCH1V471MCL1GS':
        row.update(alternate_mpn='PCH1V471MCL1GS', alternate_manufacturer='Nichicon',
            alternate_source='https://www.nichicon.co.jp/_assets/images/products/catalog/corporate/digital/sh_pch.pdf',
            alternate_status='Alternate sourcing route: manufacturer/distributor quote for exact part. Different electrical MPN OPEN; pulse/ESR/ESL/thermal requalification required.')
    if mpn in ('TNPW060324K4BEEA', 'C3216X7R1H475K160AB'):
        row['flags'] += '; EXACT-ORDER-CODE-UNCONFIRMED'
    if row['scope'] == 'Custom link':
        row.update(alternate_mpn='CUSTOM-FX-CU-01 RevA', alternate_manufacturer='Qualified fabricator OPEN',
            alternate_source=NATIVE_URL+'docs/evidence/r2/gate4b/PIN_REVIEW.md',
            alternate_status='Build-to-drawing sourcing only; no compatible catalog jumper verified. Identity closed; procurement and qualification OPEN.')
    if row['alternate_mpn'] == 'OPEN' and len(observed) >= 2:
        row['alternate_status'] += ' Same-MPN alternate distributor route: ' + ', '.join(observed) + '.'
    # A second stocked channel for the captured part avoids an unnecessary
    # electrical substitution. NRND/EOL still needs a replacement candidate.
    sufficient = [d for d in CHANNELS if row[d+'_part_number'] != 'OPEN'
        and isinstance(row[d+'_stock'], int) and isinstance(row[d+'_qty_to_order'], int)
        and row[d+'_stock'] >= row[d+'_qty_to_order']]
    if row['scope'] in ('Catalog board', 'Harness') and len(sufficient) >= 2 and 'NRND/EOL' not in row['flags']:
        row.update(alternate_mpn=mpn, alternate_manufacturer=row['manufacturer'],
            alternate_source=row[sufficient[-1]+'_source_url'],
            alternate_status='SAME-MPN alternate sourcing: '+', '.join(sufficient)+
            ' each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution.')
    elif row['alternate_mpn'] == 'OPEN' and row['scope'] in ('Catalog board', 'Harness'):
        routes = [d for d in CHANNELS if row[d+'_part_number'] != 'OPEN' and d not in sufficient]
        if routes and sum(row[c+'_part_number'] != 'OPEN' for c in CHANNELS) >= 2:
            d = routes[-1]
            row.update(alternate_mpn=mpn, alternate_manufacturer=row['manufacturer'],
                alternate_source=row[d+'_source_url'],
                alternate_status='SAME-MPN backup sourcing: '+d+' '+row[d+'_part_number']+
                '; observed stock '+str(row[d+'_stock'])+'. Backorder/stock confirmation required; '
                'no stocked replacement established. Different component MPN remains OPEN.')
    if mpn in ALT_REVIEW:
        a = ALT_REVIEW[mpn]
        row.update(alternate_mpn=a['mpn'], alternate_manufacturer=a['manufacturer'],
            alternate_source=a['source_url'], alternate_status=a['disposition'])
    if row['captured_mpn'] in DECISIONS and row['row_id'] not in LOCKS:
        a = DECISIONS[row['captured_mpn']]
        row.update(alternate_mpn=a['mpn'], alternate_manufacturer=a['manufacturer'],
            alternate_source=a['source_url'], alternate_status=a['disposition'])
        if a['order_accepted']:
            row['flags'] += '; REVIEWED-ORDER-ALTERNATE'
            row['notes'] += ' CONFIRMED order alternate from captured '+row['captured_mpn']+' to '+mpn+'. Hardware identity preserved; see bom_order/CAPACITOR_REVIEW.md and STOCK_REVIEW.md.'
            if a.get('kind') != 'carrier_only':
                row['lifecycle'] += '; manufacturer: In Production (SimSurfing B, 2026-10-04)'
        else:
            row['flags'] += '; OWNER-HOLD'
            row['notes'] += ' OPEN: '+a['owner_hold']
    if mpn == 'INA228AIDGSR':
        row['alternate_status'] = 'OPEN / REJECTED: INA228AIDGST obsolete/restricted in newer source; no accepted alternate. See STOCK_REVIEW.md.'
    if row['scope'] == 'Custom link':
        row['alternate_source'] = 'bom_order/FORCE_LINK_DRAWING.md'
        row['notes'] += ' Make-or-quote drawing: bom_order/FORCE_LINK_DRAWING.md; calculated 8 A continuous screen is conditional, installed rating OPEN.'

groups = defaultdict(list)
for r in SOURCE:
    ref = r['Reference']
    key = ('PCB feature', r['Footprint']) if ref.startswith(('TP', 'PF')) else ('Custom link' if r['MPN'].startswith('CUSTOM') else 'Catalog board', norm(r['MPN']))
    groups[key].append(r)
rows = []
for (scope, key), items in sorted(groups.items(), key=lambda p: natural(p[1][0]['Reference'])):
    refs = sorted([r['Reference'] for r in items], key=natural)
    mpn = key if scope != 'PCB feature' else ('CUSTOM-FX-PAD-M4 RevA' if refs[0].startswith('PF') else 'N/A etched copper')
    count = len(items)
    passive = refs[0][0] in 'CRLF'
    extra = 0 if scope == 'PCB feature' else spare(3 * count, passive)
    row = dict(row_id='B%03d'%(len(rows)+1),scope=scope,refdes=', '.join(refs),sheets='; '.join(sorted({META['sheet_map'][r] for r in refs})),
        qty_per_board=count,per_board_unit='PCB feature' if scope=='PCB feature' else 'piece',qty_3_boards=3*count,spares=extra,
        qty_to_order=0 if scope=='PCB feature' else 3*count+extra,order_unit='piece',
        spare_rule='N/A' if scope=='PCB feature' else '+10% rounded up; min '+str(2 if passive else 1),
        mpn=mpn,captured_mpn='; '.join(sorted({r['MPN'] for r in items})),manufacturer=manufacturer(mpn) if scope=='Catalog board' else 'Project-defined',
        value='; '.join(sorted({r['Value'] for r in items})),footprint='; '.join(sorted({r['Footprint'] for r in items})),
        source_commit=META['source_commit'],notes='Captured physical reference; electrical/fabrication release remains blocked.')
    if scope=='Custom link':
        row['notes']='Seven removable M4/C110 link positions; procurement is for a complete configuration kit, not an instruction to fit every link. JP201 and JP501 identities closed to project drawing; catalog MPN N/A, fabrication quote OPEN.'
    if mpn=='EEU-FR1E221':
        row['notes']+=' Captured EEUFR1E221 is Panasonic manufacturer spelling; EEU-FR1E221 is distributor spelling; bulk straight-lead 8 mm diameter / 3.5 mm pitch.'
    if refs == ['U316']:
        assert META['u316_disposition']['mpn'] == mpn and META['u316_disposition']['status'] == 'CONFIRMED'
        row['notes']+=' U316 CONFIRMED: LT4363HMS-1#PBF, 12-pin MSOP, -1 variant. Resume brief supersedes original pending check; C1-C3 pin review PASS. No U316-specific hold.'
    if mpn in DECISIONS and DECISIONS[mpn]['order_accepted']:
        a = DECISIONS[mpn]
        assert_selection(a, refs, row['footprint'].split('; '))
        row.update(mpn=a['mpn'], manufacturer=a['manufacturer'])
    lock_identity(row);commercial(row);lock_annotation(row);rows.append(row)

# External harness notes are not extra fitted board components. Wire is ordered by spool, never by an invented per-metre piece price.
for old in DRAFT:
    if not old['row_id'].startswith('H'):
        continue
    wire=old['quantity_unit']!='piece'
    qty=Decimal(old['qty_per_board']); base=qty*3
    extra=max(Decimal('1'),base/10) if wire else Decimal(spare(int(base)))
    row=dict(row_id=old['row_id'],scope='Harness',refdes=old['refdes'],sheets='/05_IO_TEST/ notes',qty_per_board=str(qty),
        per_board_unit='metre' if wire else 'piece',qty_3_boards=str(base),spares=str(extra),qty_to_order=math.ceil((base+extra)/Decimal('30.48')) if wire else int(base+extra),
        order_unit='100 ft spool (30.48 m)' if wire else 'piece',spare_rule='+10% cut-length allowance, min 1 m; round to whole 100 ft spool' if wire else '+10% rounded up; min 1',
        mpn=old['mpn'],captured_mpn=old['mpn'],manufacturer=old['manufacturer'],value=old['description'],footprint='Off-board',
        source_commit=META['source_commit'],notes='J502 solution A harness; assembly/contact-sharing/tooling qualification OPEN. Separate from board subtotal.')
    lock_identity(row);commercial(row);lock_annotation(row);rows.append(row)

for ident, refs, count, desc in [
    ('M01','M4 bolts for seven links',14,'M4x12 A2-70 bolt; two joints per link'),
    ('M02','M4 washers for seven links',28,'4.3/9/0.8 mm washer; two washers per joint'),
    ('M03','M4 nuts for seven links',14,'All-metal M4 nut; one per joint'),
    ('O01','Input / control / I2C mating harnesses',1,'Cable housings, contacts, wire, dry-contact controls and JP600/JP660 links require harness definition'),
    ('O02','Thermal / assembly accessories',1,'Heatsinks, live-tab insulation, thermal interface and mounting materials require thermal/layout review'),
]:
    base=3*count if isinstance(count,int) else 'OPEN';ex=spare(base) if isinstance(base,int) else 'OPEN'
    if ident.startswith('M'):
        link_order=next(r['qty_to_order'] for r in rows if r['scope']=='Custom link')
        ex=max(ex,link_order*(4 if ident=='M02' else 2)-base)
    row=dict(row_id=ident,scope='Mechanical subpart' if ident.startswith('M') else 'Accessory kit',refdes=refs,sheets='External / assembly',
        qty_per_board=count,per_board_unit='piece',qty_3_boards=base,spares=ex,qty_to_order=base+ex if isinstance(base,int) else 'OPEN',order_unit='piece',
        spare_rule='+10% rounded up; min 1; at least enough for all ordered link sets' if isinstance(count,int) else 'OPEN',mpn='OPEN',captured_mpn='N/A accessory',manufacturer='OPEN',value=desc,footprint='Off-board',
        source_commit=META['source_commit'],notes='Mechanical subparts constitute the custom links; not additional schematic references. Count applies only to seven board links, not external fixture pads/force cables.' if ident.startswith('M') else 'Not a complete bench-fixture BOM; unquantified costs are not zero.')
    if ident.startswith('O'):
        row.update(order_unit='project kit (buy listed subparts)', per_board_unit='kit',
                   value='Defined kit: see bom_order/ACCESSORY_REVIEW.md and BOM_ACCESSORIES.csv',
                   notes='Three board kits plus one complete spare kit; order component rows once, never the parent kit as another item.')
    lock_identity(row);commercial(row);lock_annotation(row);rows.append(row)

for row in rows:
    row['procurement_status'] = 'OPEN' if blocker(row) else ('N/A' if row['scope']=='PCB feature' else 'STOCKED OFFER')
    for key,value in row.items():
        if isinstance(value,str):
            row[key]=' '.join(value.split()) or ('N/A' if key.endswith('_notes') else 'OPEN')
FIELDS=list(rows[0])
with (OUT/'BOM_ORDER.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerows(rows)
close = summary(rows)
(EVIDENCE/'CLOSE_SUMMARY.json').write_text(json.dumps(close,indent=2)+'\n')

oldrefs={ref.strip():r for r in DRAFT for ref in r['refdes'].split(',') if re.fullmatch(r'[A-Z]+\d+',ref.strip())}
newrefs={r['Reference']:r for r in SOURCE}
delta=dict(added=sorted(newrefs.keys()-oldrefs.keys(),key=natural),retired=sorted(oldrefs.keys()-newrefs.keys(),key=natural),
    changed_mpn=[dict(refdes=ref,old=oldrefs[ref]['mpn'],new=newrefs[ref]['MPN']) for ref in sorted(newrefs.keys()&oldrefs.keys(),key=natural) if norm(oldrefs[ref]['mpn'])!=norm(newrefs[ref]['MPN'])])
(EVIDENCE/'RECONCILIATION.json').write_text(json.dumps(delta,indent=2)+'\n')

totals={}
for d in CHANNELS:
    totals[d]={}
    for scope in ('Catalog board','Harness'):
        subset=[r for r in rows if r['scope']==scope]
        known=[r for r in subset if r[d+'_extended_usd']!='OPEN']
        available=[r for r in known if isinstance(r[d+'_stock'],int) and r[d+'_stock']>=r[d+'_qty_to_order']]
        totals[d][scope]=dict(total='OPEN' if len(known)<len(subset) else str(sum(Decimal(r[d+'_extended_usd']) for r in known)),
            known_price_subtotal_usd=str(sum((Decimal(r[d+'_extended_usd']) for r in known),Decimal(0))),priced_lines=len(known),lines=len(subset),
            stock_sufficient_priced_subtotal_usd=str(sum((Decimal(r[d+'_extended_usd']) for r in available),Decimal(0))),stock_sufficient_priced_lines=len(available))
(EVIDENCE/'TOTALS.json').write_text(json.dumps(totals,indent=2)+'\n')

def esc(s):
    return str(s).replace('|','/').replace('\n',' ')


# Two counts prevent a selected backorder from masquerading as a stocked offer.
selection_count = f"{close['selection_open_before']} → {close['selection_open_after']}"
order_count = f"{close['open_before']} → {close['open_after']}"
owner_text = (EVIDENCE/'OWNER_DECISIONS.md').read_text().strip()
summary_lines = [
    '# BOM lock summary — 2026-10-04', '', '**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**', '',
    f"**Selection OPEN: {selection_count}. Immediate-procurement OPEN: {order_count}.**",
    '', '23 of the 24 starting rows have reasoned component or build-to-drawing defaults. B045 is the sole value-change decision. Backorders, unpriced quotes and unconfirmed stock remain visible supply gaps; they are not requests for the owner to choose a component.',
    '', 'The procurement count includes complete offers in their published currencies, without conversion or mixing regional snapshots. NRND/EOL labels remain visible; the five exact Murata selections have an explicit finite-three-board disposition. The previous 27→24 review is preserved in LOCK_BASELINE.json and the original CLOSE evidence.',
    '', '| Row | Chosen MPN | Selection | Reason | Route |', '|---|---|---|---|---|']
for r in rows:
    if r['row_id'] in LOCKS:
        summary_lines.append('| '+' | '.join(esc(r[k]) for k in ['row_id','mpn','selection_status','selection_reason','selected_route'])+' |')
summary_lines += ['', '## Needs owner decision', '', owner_text, '', '## Supply gaps', '',
    '| Row | Selected MPN | Remaining supply action |', '|---|---|---|']
for r in close['procurement_open']:
    summary_lines.append('| '+' | '.join(esc(r[k]) for k in ['row_id','mpn','reason'])+' |')
summary_lines += ['', '[Lock review](LOCK_REVIEW.md) records lands, ratings, frozen functions and the disclosed C351 family proxy. [Accessory definition](ACCESSORY_REVIEW.md) and [sub-BOM](BOM_ACCESSORIES.csv) close the harness/thermal identities. [Force-link drawing](FORCE_LINK_DRAWING.md): installed current, contact resistance, torque and pulse envelope are **bench check, does not block layout**.',
    '', 'Run `python3 docs/evidence/r2/bom_order/validate.py` and `python3 -m unittest tests.test_bom_order`. [VALIDATION.json](VALIDATION.json) and [LOCK_EXECUTION.md](LOCK_EXECUTION.md) record results and Git limitations. Hardware and captured source identities are unchanged. R2 electrical release remains BLOCKED; no later gate is advanced.']
(EVIDENCE/'CLOSE_SUMMARY.md').write_text('\n'.join(summary_lines)+'\n')

accessory_rows=[]
for p in ACCESSORIES:
    terms=offer_terms(p,p['planning_qty'])
    accessory_rows.append({**{k:v for k,v in p.items() if k!='price_tiers'},
        'qty_to_order':terms['qty'],'unit_price':terms['price'],'extended_price':terms['extended'],
        'procurement_status':'STOCKED OFFER' if terms['ready'] else 'OPEN'})
with (EVIDENCE/'BOM_ACCESSORIES.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(accessory_rows[0]),lineterminator='\n');w.writeheader();w.writerows(accessory_rows)
accessory_total = dict(currency='USD', known_subtotal=str(sum((Decimal(r['extended_price']) for r in accessory_rows if r['extended_price']!='OPEN'),Decimal(0))),
    complete_total='OPEN' if any(r['extended_price']=='OPEN' for r in accessory_rows) else str(sum(Decimal(r['extended_price']) for r in accessory_rows)),
    scope='O01/O02 purchased subparts only; shared H07/H08 wire not charged twice; no parent-kit cost added')
(EVIDENCE/'ACCESSORY_TOTALS.json').write_text(json.dumps(accessory_total,indent=2)+'\n')

lines=[f'''# V1A R2 order BOM — three boards plus spares

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**Selection OPEN: {selection_count}. Immediate-procurement OPEN: {order_count}.** Complete immediate ordering remains BLOCKED by the supply gaps below and B045. A locked MPN or build-to-drawing selection does not assert stock or electrical validation. No purchase, login, cart, quote request, CAD edit or push was made.

[Close summary](bom_order/CLOSE_SUMMARY.md), [lock review](bom_order/LOCK_REVIEW.md), [owner decision](bom_order/OWNER_DECISIONS.md), and [accessory definition](bom_order/ACCESSORY_REVIEW.md) are the current dispositions. Earlier CAPACITOR_REVIEW.md and STOCK_REVIEW.md findings are retained as historical evidence; the lock review supersedes their component-selection holds for its 23 locked rows. Three previously accepted order alternates remain unchanged; C351 now selects the separately reviewed TDK AC suffix. Every captured MPN, nominal value, reference and footprint is preserved in its own CSV fields.

**EVIDENCE:** KiCad {META['kicad_version']} export from [source commit `{META['source_commit']}`]({NATIVE_URL}hardware/kicad/V1A.kicad_sch), SHA-256 `{META['export_sha256']}`. The export contains **366 references: 298 catalog components across 96 MPNs, seven custom links and 61 etched PCB features**. Each is represented once. [SOURCE_BOM.csv](bom_order/SOURCE_BOM.csv), [PROVENANCE.json](bom_order/PROVENANCE.json), [RECONCILIATION.json](bom_order/RECONCILIATION.json) preserve the source audit; historical BOM_DRAFT is unchanged.

## Quantities and commercial interpretation

Catalog resistor/capacitor/inductor/fuse spares are `max(2, ceil(3 × per-board quantity × 10%))`; other parts use a minimum one spare. Distributor quantities independently round to the published or explicitly assumed minimum/multiple. Etched copper is not purchased. Three harness/thermal kits plus one complete spare kit are broken down in [BOM_ACCESSORIES.csv](bom_order/BOM_ACCESSORIES.csv); buy those subparts once, not the parent row as well. H07/H08 spools also supply the four input lead sets; their frozen J502 cut lengths are unchanged. [Accessory totals](bom_order/ACCESSORY_TOTALS.json) are separate from the three-channel scenarios.

Every offer has a URL, access date, crawl age and commercial assumptions. These are dated public snapshots, not reservations or firm quotations. Unknown data remains OPEN. The added supplier columns retain USD/EUR/AUD without exchange-rate assumptions; never combine their stock with another channel's price. No numeric total includes an unknown cost. Shipping, taxes, assembly, PCB fabrication and fixture equipment remain outside the totals; Newark prices already include the duties shown on its pages. Reconfirm offers before an eventual purchase.

## Force links and accessories

[CUSTOM-FX-CU-01 RevA](bom_order/FORCE_LINK_DRAWING.md) is an authored make-to-drawing selection for 24 C110 straps, 30×15×2 mm, holes4.5 mm on20 mm centers, tin1–5 µm. Selected hardware: Würth00944 12 bolts48, RS PRO527381 washers96 minimum (bag250), RS PRO6655609 all-metal nuts48 minimum (two packs25). Fabricator quote and commercial pack confirmation remain supply actions. Installed current, contact resistance, joint torque, creep, pulse/thermal performance and parasitics are **bench check, does not block layout**; the conditional8 A calculation is not a validated rating or fabrication approval.

O01 mates the actual JST VH/XH input/control/I2C headers, defines four dry-contact controls and two removable manual links, and labels every net. O02 selects individual Boyd507302B00000G sinks plus4880SG insulating mounting kits for D102/D330/D331. Their physical envelopes are layout inputs; thermal capability remains an R3/R5 check. The D2PAK Q316 uses its PCB thermal path, not a TO-220 accessory. No SBC is the first test load.

**U316: CONFIRMED — LT4363HMS-1#PBF**, four pieces; existing -1/MSOP12 disposition retained. The source [pin review]({NATIVE_URL}docs/evidence/r2/gate4b/PIN_REVIEW.md) remains the pin/land evidence. No protection threshold, timing component, current limit, Kelvin connection or telemetry identity is silently changed.

## Lock decisions

| ID | Selected MPN | Selection | Reason | Procurement |
|---|---|---|---|---|''']
for r in rows:
    if r['row_id'] in LOCKS:
        lines.append('| '+' | '.join(esc(r[k]) for k in ['row_id','mpn','selection_status','selection_reason','procurement_status'])+' |')
lines += ['\n## Owner decision\n',owner_text,'\n## Remaining supply gaps\n','| ID | MPN | Action |','|---|---|---|']
for r in close['procurement_open']:
    lines.append('| '+' | '.join(esc(r[k]) for k in ['row_id','mpn','reason'])+' |')
lines += ['\n## Additional supplier offers\n','Prices are in the stated currency per stated pack/spool/piece; stock has the same unit. E006 stock unit is unconfirmed and excluded from closure. These offers are alternatives to the preferred-channel columns, never additional quantities.\n',
    '| ID | Supplier / SKU | Quantity / unit | Unit price | Extended | Stock | Source |','|---|---|---|---|---|---|---|']
for r in rows:
    if r['additional_evidence_id']!='N/A':
        lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],r['additional_supplier']+' / '+r['additional_sku'],str(r['additional_qty'])+' '+r['additional_order_unit'],r['additional_currency']+' '+r['additional_price'],r['additional_currency']+' '+r['additional_extended'],r['additional_stock'],f"[{r['additional_evidence_id']}]({r['additional_url']})"])+ ' |')
lines += ['\n## Distributor totals\n','Each channel is an alternative whole-build scenario. Do not add the three scenarios or duplicate a row already sourced elsewhere. These incomplete USD subtotals include priced backorders.\n',
    '| Distributor | Complete catalog-board total | Known-price subtotal USD | Coverage | Stock-sufficient priced subtotal USD | Harness subtotal USD / coverage |',
    '|---|---|---:|---|---:|---|']
for d in CHANNELS:
    b=totals[d]['Catalog board'];h=totals[d]['Harness']
    lines.append(f"| {d} | {b['total']} | {Decimal(b['known_price_subtotal_usd']):.2f} | {b['priced_lines']}/{b['lines']} | {Decimal(b['stock_sufficient_priced_subtotal_usd']):.2f} ({b['stock_sufficient_priced_lines']} lines) | {Decimal(h['known_price_subtotal_usd']):.2f} / {h['priced_lines']}/{h['lines']}; complete {h['total']} |")
lines += ['\n## Parts and quantities\n','| ID | Refdes / purpose | Per board | 3-board base | Spares | Planning order | MPN | Manufacturer | Flags |','|---|---|---:|---:|---:|---|---|---|---|']
for r in rows:
    lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],r['refdes'],str(r['qty_per_board'])+' '+r['per_board_unit'],r['qty_3_boards'],r['spares'],str(r['qty_to_order'])+' '+r['order_unit'],r['mpn'],r['manufacturer'],r['flags']])+' |')
for d in CHANNELS:
    lines += ['\n## '+d+' commercial register\n','All prices below are USD per stated order unit; dates, assumptions and evidence IDs are in CSV.\n','| ID | Distributor SKU / evidence | Order qty | Unit USD | Extended USD | Stock | Lead time | Lifecycle |','|---|---|---:|---:|---:|---|---|---|']
    for r in rows:
        url=r[d+'_source_url'];sku=r[d+'_part_number'];label=f'[{sku}]({url})' if url.startswith('https://') else sku
        lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],label,r[d+'_qty_to_order'],r[d+'_unit_price_usd'],r[d+'_extended_usd'],r[d+'_stock'],r[d+'_lead_time'],r[d+'_lifecycle']])+' |')
lines += ['\n## Alternate disposition register\n','Only explicitly accepted earlier alternates and LOCK_DECISIONS selections enter quantities. Other catalog suggestions remain unapproved. SAME-MPN entries are backup suppliers; never duplicate quantities.\n','| ID | Selected MPN | Alternate / manufacturer | Evidence | Disposition |','|---|---|---|---|---|']
for r in rows:
    if r['scope']=='PCB feature':continue
    url=r['alternate_source'];link=f'[source]({url})' if url.startswith(('https://','bom_order/')) else 'OPEN'
    lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],r['mpn'],r['alternate_mpn']+' / '+r['alternate_manufacturer'],link,r['alternate_status']])+' |')
lines += ['''
## LCSC upload and validation

[BOM_ORDER_LCSC.csv](BOM_ORDER_LCSC.csv) is a local upload-style candidate subset, not a complete order or electrical release. It requires one coherent LCSC SKU, enough stock, priced rounded quantity, known multiple and accepted selection. Finite-build exact Murata lifecycle decisions are explicit exceptions, so the five locked capacitor identities can qualify without hiding their NRND/EOL labels. Other lifecycle holds and B045 remain excluded. No upload or account interaction occurred.

Rebuild with `python3 docs/evidence/r2/bom_order/generate.py`; validate with `python3 docs/evidence/r2/bom_order/validate.py` and `python3 -m unittest tests.test_bom_order`. [VALIDATION.json](bom_order/VALIDATION.json) checks coverage, quantities, currency/pack arithmetic, offers, scoped alternates, disclosed proxy, hardware hashes, counts and exact upload membership. These are document checks. No ERC/DRC rerun is claimed because hardware was read-only; R2 remains blocked and no gate is skipped.

Third-party facts and attribution are isolated in [third_party/bom_order](../../../third_party/bom_order/README.md). [LOCK_EXECUTION.md](bom_order/LOCK_EXECUTION.md) records execution and commit limitations.
''']
(OUT/'BOM_ORDER.md').write_text('\n'.join(lines))
upload=[]
for r in rows:
    if eligible_lcsc(r):
        upload.append({'LCSC Part Number':r['lcsc_part_number'],'Quantity':r['lcsc_qty_to_order'],'Manufacturer Part Number':r['mpn'],'Designator':r['refdes']})
with (OUT/'BOM_ORDER_LCSC.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['LCSC Part Number','Quantity','Manufacturer Part Number','Designator'],lineterminator='\n');w.writeheader();w.writerows(upload)
print(json.dumps(dict(rows=len(rows),catalog_mpns=sum(r['scope']=='Catalog board' for r in rows),upload_rows=len(upload),
    selection_open=close['selection_open_after'],procurement_open=close['open_after']),indent=2))
