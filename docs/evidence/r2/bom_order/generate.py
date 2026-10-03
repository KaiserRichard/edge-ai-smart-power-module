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

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'docs/evidence/r2'
EVIDENCE = OUT / 'bom_order'
FACTS = ROOT / 'third_party/bom_order/CATALOG_FACTS.json'
CHANNELS = ('lcsc', 'mouser', 'digikey')
META = json.loads((EVIDENCE / 'PROVENANCE.json').read_text())
SOURCE = list(csv.DictReader((EVIDENCE / 'SOURCE_BOM.csv').open()))
DRAFT = list(csv.DictReader((OUT / 'BOM_DRAFT.csv').open()))
QUOTES = json.loads(FACTS.read_text())
Q = {(q['mpn'], q['d']): q for q in QUOTES}
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
        if isinstance(n, int) and not not_bought:
            if isinstance(q['minimum'], int):
                n = max(n, q['minimum'])
            if isinstance(q['multiple'], int) and q['multiple'] > 0:
                n = math.ceil(n / q['multiple']) * q['multiple']
            elif q['sku'] != 'OPEN':
                notes.append('Order multiple OPEN; quantity is a planning minimum, not a confirmed pack quantity.')
        row[d + '_qty_to_order'] = 0 if not_bought else n
        applicable = [(int(t), Decimal(str(p))) for t, p in q['price_tiers'] if isinstance(n, int) and int(t) <= n]
        priced = bool(applicable) and q['sku'] != 'OPEN' and isinstance(n, int) and n > 0
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
    if row['scope'] == 'Catalog board' and row['refdes'] == 'U316':
        row['flags'] += '; pending U316 check'
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
    commercial(row);rows.append(row)

# External harness notes are not extra fitted board components. Wire is ordered by spool, never by an invented per-metre piece price.
for old in DRAFT:
    if not old['row_id'].startswith('H'):
        continue
    wire=old['quantity_unit']!='piece'
    qty=Decimal(old['qty_per_board']); base=qty*3
    extra=max(Decimal('1'),base/10) if wire else Decimal(spare(int(base)))
    row=dict(row_id=old['row_id'],scope='Harness',refdes=old['refdes'],sheets='/05_IO_TEST/ notes',qty_per_board=str(qty),
        per_board_unit='metre' if wire else 'piece',qty_3_boards=str(base),spares=str(extra),qty_to_order=1 if wire else int(base+extra),
        order_unit='100 ft spool (30.48 m)' if wire else 'piece',spare_rule='+10% cut-length allowance, min 1 m; round to whole 100 ft spool' if wire else '+10% rounded up; min 1',
        mpn=old['mpn'],captured_mpn=old['mpn'],manufacturer=old['manufacturer'],value=old['description'],footprint='Off-board',
        source_commit=META['source_commit'],notes='J502 solution A harness; assembly/contact-sharing/tooling qualification OPEN. Separate from board subtotal.')
    commercial(row);rows.append(row)

for ident, refs, count, desc in [
    ('M01','M4 bolts for seven links',14,'M4x12 A2-70 bolt; two joints per link; purchased MPN OPEN'),
    ('M02','M4 washers for seven links',28,'4.3/9/0.8 mm washer; two washers per joint; purchased MPN OPEN'),
    ('M03','M4 nuts for seven links',14,'All-metal M4 nut; one per joint; purchased MPN OPEN'),
    ('O01','Input / control / I2C mating harnesses','OPEN','Cable housings, contacts, wire, dry-contact controls and JP600/JP660 links require harness definition'),
    ('O02','Thermal / assembly accessories','OPEN','Heatsinks, live-tab insulation, thermal interface and mounting materials require thermal/layout review'),
]:
    base=3*count if isinstance(count,int) else 'OPEN';ex=spare(base) if isinstance(base,int) else 'OPEN'
    if ident.startswith('M'):
        link_order=next(r['qty_to_order'] for r in rows if r['scope']=='Custom link')
        ex=max(ex,link_order*(4 if ident=='M02' else 2)-base)
    row=dict(row_id=ident,scope='Mechanical subpart' if ident.startswith('M') else 'Unresolved accessory',refdes=refs,sheets='External / assembly',
        qty_per_board=count,per_board_unit='piece',qty_3_boards=base,spares=ex,qty_to_order=base+ex if isinstance(base,int) else 'OPEN',order_unit='piece',
        spare_rule='+10% rounded up; min 1; at least enough for all ordered link sets' if isinstance(count,int) else 'OPEN',mpn='OPEN',captured_mpn='N/A accessory',manufacturer='OPEN',value=desc,footprint='Off-board',
        source_commit=META['source_commit'],notes='Mechanical subparts constitute the custom links; not additional schematic references. Count applies only to seven board links, not external fixture pads/force cables.' if ident.startswith('M') else 'Not a complete bench-fixture BOM; unquantified costs are not zero.')
    commercial(row);rows.append(row)

for row in rows:
    for key,value in row.items():
        if isinstance(value,str):
            row[key]=' '.join(value.split()) or ('N/A' if key.endswith('_notes') else 'OPEN')
FIELDS=list(rows[0])
with (OUT/'BOM_ORDER.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)

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

lines=[f'''# V1A R2 order BOM — three boards plus spares

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**STATUS: BLOCKED for a complete order.** The procurement register is synchronized and every unavailable or unverified commercial field is marked **OPEN**. It is not a claim that all parts can be purchased today or that the R2 design is electrically released. No purchase, cart, quote request, CAD edit, merge or push was made.

**EVIDENCE — 2026-10-03:** KiCad {META['kicad_version']} BOM export from a detached `/tmp` copy of [`origin/feat/r2-testboard-capture` at `{META['source_commit'][:7]}`]({NATIVE_URL}hardware/kicad/V1A.kicad_sch). The final re-fetch added pin-review documentation only; the two BOM exports have identical SHA-256 `{META['export_sha256']}`. The source contains **366 references: 298 catalog components across 96 MPNs, seven custom links, and 61 etched PCB features**. Power flags are excluded by KiCad; the exported physical references have no DNP marks. Manufacturer fields are blank in the export; names come from the existing selection register and exact catalog identities, never invented schematic fields.

[BOM_ORDER.csv](BOM_ORDER.csv) contains every reference, footprint, quantity, supplier SKU, supplier-specific order quantity, USD unit/extended price, stock, lead time, lifecycle, source URL, observation date, crawl age and alternate disposition. [SOURCE_BOM.csv](bom_order/SOURCE_BOM.csv), [PROVENANCE.json](bom_order/PROVENANCE.json), [RECONCILIATION.json](bom_order/RECONCILIATION.json) and [TOTALS.json](bom_order/TOTALS.json) make the arithmetic and synchronization reviewable. Historical BOM_DRAFT files are preserved.

## Quantities and commercial interpretation

**DECISION:** aggregate identical exact MPNs over all five sheets before calculating spares. For each resistor, capacitor, inductor or fuse: `base = 3 × quantity per board`, `spares = max(2, ceil(base × 10%))`. Other catalog parts and custom links use `max(1, ceil(base × 10%))`. Etched pads have an instance count but **zero purchased pieces**. A link kit is supplied for all seven positions; fitting depends on the isolated-test configuration.

**CALCULATION:** each distributor quantity rounds that planning quantity up to its retrieved minimum/multiple. Unit price uses the largest displayed applicable tier, for cut tape or bulk/tube where identified. Cut-tape and Digi-Reel prices are kept distinct; no reeling fee is silently included. A minimum inferred from the first displayed tier and an assumed single-piece multiple are labeled in CSV notes. An unknown multiple remains OPEN and requires pack confirmation. Wire columns distinguish metres consumed from whole **100-foot (30.48 m) spools** ordered; one spool of each selected colour/gauge covers the three harnesses and `max(10%, 1 m)` cutting allowance.

**EVIDENCE LIMIT:** website/index snapshots, not live reservations or firm quotes. Each offer is one coherent retrieved snapshot; stock and price are not stitched from unrelated pages. Prefer complete exact-SKU evidence, then the more recent crawl. Pages with another manufacturer's same-number component, unmatched suffixes or unverified marketplace supply do not become selected offers. OPEN does not mean zero stock or EOL. Lifecycle is labeled by channel; channel withdrawal is not manufacturer EOL. Shipping, tax, duty, tariffs, reeling, assembly, PCB, custom fabrication and external test equipment are excluded from numeric subtotals. Reconfirm published prices, quantities and stock before ordering.

## JP201 / JP501 and U316 dispositions

**DECISION — identities closed:** JP201 and JP501 both resolve to **CUSTOM-FX-CU-01 RevA**, as do JP101, JP202, JP301, JP330 and JP331. This is an authored removable force-link drawing, **not a distributor MPN**. Catalog MPN is N/A; qualified fabricator, purchased stock/subpart MPNs and price remain OPEN. [Captured pin review]({NATIVE_URL}docs/evidence/r2/gate4b/PIN_REVIEW.md) and [Sheet05 review]({NATIVE_URL}docs/evidence/r2/gate4b/SHEET05_REVIEW.md) establish the exact interfaces. No 2.54 mm shunt is substituted.

The pinned [fixture drawing description](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FIX3_FIXTURE.md) specifies C110 copper 2 mm × 15 mm, span ≤30 mm, 4.5 mm holes on 20 mm pitch; M4×12 A2-70 bolts, two 4.3/9/0.8 mm washers and an all-metal M4 nut per joint. Seven links imply 14 joints per board. Accessory rows enumerate those subparts without inventing supplier codes; finishing, actual stackup, insulation, torque, contact resistance and parasitic qualification remain OPEN. These subparts make up the custom links and are not extra schematic instances.

JP201 joins native BUCK_SW to L201_IN and is removed for isolated tests. JP501 joins LOAD_5V1 to LOAD_FIXTURE; opening it does not isolate an attached J502 load. The separate force return is PF5.

**U316: pending U316 check.** The selected code remains LT4363HMS-1#PBF. Source commit `{META['source_commit'][:7]}` includes a [C1–C3 pin check]({NATIVE_URL}docs/evidence/r2/gate4b/CHECK_C1C3.md) confirming the existing -1 MSOP pinout without a circuit/MPN change. The brief's pending marker is retained; reconcile the final engineering disposition before ordering U316. Do not change to the -2 variant on a sourcing assumption.

## Sheets 03–05 synchronization

**OBSERVATION:** all 366 native references are represented once in the board register, including Sheet03's 280, Sheet04's 23 and Sheet05's 11. Compared with the earlier draft, {len(delta['added'])} references are added and {len(delta['retired'])} retired. The detailed reconciliation also records identity/feature-label changes. Obsolete AHCT/control proposals and draft DNP rows do not drive quantities. The manual source-fault hook and actual observation front end replace the old unquantified on-board FAULT_TRIGGER placeholder; the separately documented external injection fixture is outside this board BOM.

R312 is now 32.4 kohm (shared with R600); R341 is 88.7 kohm. All added R6xx/R7xx/U6xx/C6xx/C7xx parts and revised bypass counts come directly from the export. C350 remains captured as 10 nF. The Panasonic export spelling EEUFR1E221 is normalized only for distributor matching to EEU-FR1E221; [Panasonic's model page](https://na.industrial.panasonic.com/products/capacitors/aluminum-electrolytic-capacitors/series/83367/model/83695) confirms the 220 uF / 25 V bulk straight-lead part, 8 mm diameter and 3.5 mm pitch.

## Remaining procurement blockers

- **C351:** exact captured C3216X7R1H475K160AB ordering code not verified. The independently listed AC suffix is an unapproved candidate, not a spelling correction.
- **R203:** exact TNPW060324K4BEEA listing/orderability is OPEN. Preserve 24.4 kohm; do not substitute a neighbouring value without recalculating and approving the feedback network.
- **PCH1V471MCL1GS:** [Nichicon's 2026 catalog](https://www.nichicon.co.jp/_assets/images/products/catalog/corporate/digital/sh_pch.pdf) confirms the exact 470 uF / 35 V, 10×16 mm code. Supplier SKU, price, stock and lead time remain OPEN. A different bank capacitor requires ESR/ESL, fault-energy and thermal review.
- **Supply / lifecycle:** EOL/NRND capacitors, unstocked semiconductors and ballast resistors, and single-observed-source rows are flagged below. Alternates are identified where verified; **OPEN alternate** is an unresolved action, never approval to buy a constructed MPN. Package-only alternatives still require ordering-table confirmation. Distributor “Direct” or “Similar” labels do not establish electrical equivalence.
- **Custom / harness / thermal:** link fabrication and accessory codes, mating input/control/I2C harnesses, live-tab insulation/heatsinking, tools/splices and assembly costs remain OPEN. The chosen J502/Pi harness is listed separately and has unvalidated hot-contact/current-sharing behaviour. No SBC as the first load.

## Distributor totals

Each channel column is an alternative whole-build scenario. **Do not add the three distributor totals together.** Known-price subtotals include priced backorders and held U316; stock-sufficient subtotals are still not an engineering release or complete order. All custom/accessory and complete-kit totals remain **OPEN**.

| Distributor | Complete catalog-board total | Known-price subtotal USD | Coverage | Stock-sufficient priced subtotal USD | Harness subtotal USD / coverage |
|---|---|---:|---|---:|---|
''']
for d in CHANNELS:
    b=totals[d]['Catalog board'];h=totals[d]['Harness']
    lines.append(f"| {d} | {b['total']} | {Decimal(b['known_price_subtotal_usd']):.2f} | {b['priced_lines']}/{b['lines']} | {Decimal(b['stock_sufficient_priced_subtotal_usd']):.2f} ({b['stock_sufficient_priced_lines']} lines) | {Decimal(h['known_price_subtotal_usd']):.2f} / {h['priced_lines']}/{h['lines']}; complete {h['total']} |")
lines += ['\n## Parts and quantities\n','| ID | Refdes / purpose | Per board | 3-board base | Spares | Planning order | MPN | Manufacturer | Flags |','|---|---|---:|---:|---:|---|---|---|---|']
for r in rows:
    lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],r['refdes'],str(r['qty_per_board'])+' '+r['per_board_unit'],r['qty_3_boards'],r['spares'],str(r['qty_to_order'])+' '+r['order_unit'],r['mpn'],r['manufacturer'],r['flags']])+' |')
for d in CHANNELS:
    lines += ['\n## '+d+' commercial register\n','All prices below are USD per stated order unit. Lead time is the published manufacturer/factory lead time if retrieved, not an arrival promise. Dates/crawl ages and MOQ assumptions are in the CSV.\n','| ID | Distributor SKU / evidence | Order qty | Unit USD | Extended USD | Stock | Lead time | Lifecycle |','|---|---|---:|---:|---:|---|---|---|']
    for r in rows:
        url=r[d+'_source_url'];sku=r[d+'_part_number'];label=f'[{sku}]({url})' if url.startswith('https://') else sku
        lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],label,r[d+'_qty_to_order'],r[d+'_unit_price_usd'],r[d+'_extended_usd'],r[d+'_stock'],r[d+'_lead_time'],r[d+'_lifecycle']])+' |')
lines += ['\n## Alternate disposition register\n','Candidates are excluded from the order quantities and totals. Named candidates require engineering approval; OPEN candidates remain procurement blockers.\n','| ID | Selected MPN | Alternate / manufacturer | Evidence | Disposition |','|---|---|---|---|---|']
for r in rows:
    if r['scope']=='PCB feature':continue
    url=r['alternate_source'];link=f'[source]({url})' if url.startswith('https://') else 'OPEN'
    lines.append('| '+' | '.join(esc(v) for v in [r['row_id'],r['mpn'],r['alternate_mpn']+' / '+r['alternate_manufacturer'],link,r['alternate_status']])+' |')
lines += ['''
## LCSC upload and validation

[BOM_ORDER_LCSC.csv](BOM_ORDER_LCSC.csv) is a **local LCSC-upload-style candidate subset**, with LCSC part number, quantity, manufacturer part number and designators. It includes only catalog-board lines with a verified SKU, published order-quantity price, known multiple, enough observed stock, no reported NRND/EOL and no U316 hold. The other lines remain in the main CSV. Upload compatibility has not been tested against an account; no upload, cart or purchase was performed. This file is not a complete board BOM or an order authorization.

[VALIDATION.json](bom_order/VALIDATION.json) checks source coverage, uniqueness, source hash, three-board/spare arithmetic, supplier rounding, exact selected MPNs, U316 hold, CSV/Markdown prices and upload inclusion. No ERC or DRC rerun is claimed: native KiCad files were read-only. This procurement subtask does not close R2 or advance to R3/R4/R5. Rebuild with `python3 docs/evidence/r2/bom_order/generate.py`.

Catalog facts and third-party provenance are isolated in [third_party/bom_order](../../../third_party/bom_order/README.md). Referenced designs/documents were not modified or copied into CAD.
''']
(OUT/'BOM_ORDER.md').write_text('\n'.join(lines))
upload=[]
for r in rows:
    if r['scope']=='Catalog board' and r['lcsc_part_number']!='OPEN' and r['lcsc_unit_price_usd']!='OPEN' and isinstance(r['lcsc_order_multiple'],int) and isinstance(r['lcsc_stock'],int) and r['lcsc_stock']>=r['lcsc_qty_to_order'] and not any(s in r['flags'] for s in ['NRND/EOL','pending U316','EXACT-ORDER']):
        upload.append({'LCSC Part Number':r['lcsc_part_number'],'Quantity':r['lcsc_qty_to_order'],'Manufacturer Part Number':r['mpn'],'Designator':r['refdes']})
with (OUT/'BOM_ORDER_LCSC.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['LCSC Part Number','Quantity','Manufacturer Part Number','Designator']);w.writeheader();w.writerows(upload)
print(json.dumps(dict(rows=len(rows),catalog_mpns=sum(r['scope']=='Catalog board' for r in rows),upload_rows=len(upload),totals=totals),indent=2))
