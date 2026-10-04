#!/usr/bin/env python3
"""Independent coverage, quantity, cost and exclusion checks for the exported order files."""
import csv
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from collections import Counter
from decimal import Decimal
from pathlib import Path
from closeout import hardware_baseline_bytes

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/evidence/r2'
HERE=Path(__file__).resolve().parent
source=list(csv.DictReader((HERE/'SOURCE_BOM.csv').open()))
rows=list(csv.DictReader((OUT/'BOM_ORDER.csv').open()))
upload=list(csv.DictReader((OUT/'BOM_ORDER_LCSC.csv').open()))
meta=json.loads((HERE/'PROVENANCE.json').read_text())
facts=json.loads((ROOT/'third_party/bom_order/CATALOG_FACTS.json').read_text())
facts+=json.loads((ROOT/'third_party/bom_order/RESUME_CATALOG_FACTS.json').read_text())
facts+=json.loads((ROOT/'third_party/bom_order/CLOSE_CATALOG_FACTS.json').read_text())
facts+=json.loads((ROOT/'third_party/bom_order/CLOSE_RESUME_CATALOG_FACTS.json').read_text())
facts+=json.loads((ROOT/'third_party/bom_order/LOCK_CATALOG_FACTS.json').read_text())
facts+=json.loads((ROOT/'third_party/bom_order/R203A_CATALOG_FACTS.json').read_text())
locks=json.loads((ROOT/'third_party/bom_order/LOCK_DECISIONS.json').read_text())
lock_baseline=json.loads((HERE/'LOCK_BASELINE.json').read_text())
extra={q['row_id']:q for q in json.loads((ROOT/'third_party/bom_order/LOCK_EXTERNAL_OFFERS.json').read_text())}
accessories=json.loads((ROOT/'third_party/bom_order/LOCK_ACCESSORIES.json').read_text())
accessory_rows=list(csv.DictReader((HERE/'BOM_ACCESSORIES.csv').open()))
lock_sources=json.loads((ROOT/'third_party/bom_order/LOCK_SOURCES.json').read_text())['sources']
lock_sources.update(json.loads((ROOT/'third_party/bom_order/R203A_SOURCES.json').read_text())['sources'])
decisions=json.loads((ROOT/'third_party/bom_order/CLOSE_ALTERNATE_REVIEW.json').read_text())
decisions.update(json.loads((ROOT/'third_party/bom_order/CLOSE_STOCK_DECISIONS.json').read_text()))
baseline=json.loads((HERE/'CLOSE_BASELINE.json').read_text())
close=json.loads((HERE/'CLOSE_SUMMARY.json').read_text())
factmap={q['evidence_id']:q for q in facts}
selected_facts={(q['mpn'],q['d']):q for q in facts}
assert len(factmap)==len(facts), 'Evidence IDs must be unique'
markdown=(OUT/'BOM_ORDER.md').read_text()
totals=json.loads((HERE/'TOTALS.json').read_text())
src={r['Reference']:r for r in source}
board=[r for r in rows if r['scope'] in ['Catalog board','Custom link','PCB feature']]
refs=[ref for r in board for ref in r['refdes'].split(', ')]
assert len(source)==366 and len(src)==366
assert Counter(refs)==Counter(src.keys()), 'Missing, duplicated or extra source references'
assert hashlib.sha256((HERE/'SOURCE_BOM.csv').read_bytes()).hexdigest()==meta['export_sha256']
assert all(r['Qty']=='1' and not r['DNP'] for r in source)
assert all(all(v!='' for v in r.values()) for r in rows), 'Use OPEN / N/A, not empty fields'
assert len(set(r['row_id'] for r in rows))==len(rows)
for r in board:
    listed=r['refdes'].split(', ')
    assert int(r['qty_per_board'])==len(listed)
    assert int(r['qty_3_boards'])==3*len(listed)
    assert {src[ref]['MPN'] for ref in listed}==set(r['captured_mpn'].split('; '))
    assert {src[ref]['Footprint'] for ref in listed}==set(r['footprint'].split('; '))
    if r['scope']=='PCB feature':
        assert r['qty_to_order']=='0' and r['spares']=='0'
        continue
    captured=r['captured_mpn'].replace('EEUFR1E221','EEU-FR1E221')
    decision=decisions.get(captured)
    if r['row_id'] in locks:
        a=locks[r['row_id']]
        assert r['mpn']==a['mpn'] and r['manufacturer']==a['manufacturer']
        assert a['captured_mpn']==r['captured_mpn']
        assert set(listed)==set(a['refdes']) and set(r['footprint'].split('; '))==set(a['footprints'])
        if r['row_id']=='B011':
            assert captured=='C3216X7R1H475K160AB' and r['mpn']=='C3216X7R1H475K160AC'
            assert r['value']=='4.7uF 50V' and r['refdes']=='C351'
        elif r['row_id']=='B045':
            assert captured=='TNPW060324K4BEEA' and r['mpn']=='TNPW060324K6BEEA'
            assert r['value']=='24.6k' and r['refdes']=='R203'
            assert src['R203']['Value']=='24.4k', 'Historical export must remain intact'
            assert a['kind']=='owner_value_change' and a['owner_decision']=='A on 2026-10-04'
        else:
            assert r['mpn']==captured, 'No other board substitution authorized by lock review'
    elif decision and decision['order_accepted']:
        assert r['mpn']==decision['mpn'] and r['manufacturer']==decision['manufacturer']
        assert set(listed)==set(decision['refdes'])
        assert set(r['footprint'].split('; '))==set(decision['footprints'])
        assert decision['status']=='CONFIRMED' and decision['owner_hold']=='N/A'
        assert 'REVIEWED-ORDER-ALTERNATE' in r['flags']
    else:
        assert all(src[ref]['MPN'].replace('EEUFR1E221','EEU-FR1E221')==r['mpn'] for ref in listed)
        if decision:
            assert 'OWNER-HOLD' in r['flags']
    base=3*len(listed)
    passive=listed[0][0] in 'CRLF'
    assert int(r['spares'])==max(2 if passive else 1,math.ceil(base/10))
    assert int(r['qty_to_order'])==base+int(r['spares'])
catalog=[r for r in rows if r['scope']=='Catalog board']
assert len(catalog)==96 and sum(int(r['qty_per_board']) for r in catalog)==298
assert len(set(r['mpn'] for r in catalog))==96
u316=next(r for r in rows if r['refdes']=='U316')
assert u316['mpn']=='LT4363HMS-1#PBF' and 'U316 CONFIRMED' in u316['notes']
assert meta['u316_disposition']['status']=='CONFIRMED'
assert 'pending U316 check' not in markdown and 'pending U316 check' not in (OUT/'BOM_ORDER.csv').read_text()
assert u316['qty_per_board']=='1' and u316['qty_to_order']=='4'
links=next(r for r in rows if r['scope']=='Custom link')
assert {'JP201','JP501'}<=set(links['refdes'].split(', '))
assert links['mpn']=='CUSTOM-FX-CU-01 RevA'
for ident,per_link in [('M01',2),('M02',4),('M03',2)]:
    r=next(r for r in rows if r['row_id']==ident)
    assert int(r['qty_to_order'])>=int(links['qty_to_order'])*per_link
for r in rows:
    assert r['source_commit']==meta['source_commit']
    if r['scope']=='Harness':
        base=Decimal(r['qty_per_board'])*3
        assert Decimal(r['qty_3_boards'])==base
        if r['per_board_unit']=='metre':
            assert Decimal(r['spares'])==max(Decimal('1'),base/10)
            assert int(r['qty_to_order'])==math.ceil((base+Decimal(r['spares']))/Decimal('30.48'))
        else:
            assert int(r['spares'])==max(1,math.ceil(base/10))
            assert int(r['qty_to_order'])==base+int(r['spares'])
    for d in ['lcsc','mouser','digikey']:
        evidence=r[d+'_evidence_id']
        if evidence not in ('OPEN','N/A'):
            q=factmap[evidence]
            assert q==selected_facts[(r['mpn'],d)], 'Stale or wrong selected evidence'
            for column,key in [('part_number','sku'),('stock','stock'),('lead_time','lead_time'),
                    ('lifecycle','lifecycle'),('minimum_order','minimum'),('order_multiple','multiple'),
                    ('source_url','url'),('observed_date','observed_date'),('crawl_age','crawl_age')]:
                assert r[d+'_'+column]==' '.join(str(q[key]).split()), (r['row_id'],d,column)
        elif r['scope']!='PCB feature':
            assert r[d+'_part_number']=='OPEN' and r[d+'_stock']=='OPEN'
        unit=r[d+'_unit_price_usd'];extended=r[d+'_extended_usd']
        if unit in ['OPEN','N/A']:
            assert extended==unit
            continue
        assert r[d+'_part_number'] not in ['OPEN','N/A']
        q=factmap[r[d+'_evidence_id']]
        assert q['mpn']==r['mpn'] and q['sku']==r[d+'_part_number']
        assert q['currency']=='USD', 'Non-USD prices cannot enter USD totals'
        n=int(r[d+'_qty_to_order'])
        assert n>=int(r['qty_to_order'])
        if isinstance(q['minimum'],int):assert n>=q['minimum']
        if isinstance(q['multiple'],int):assert n%q['multiple']==0
        applicable=[(int(t),Decimal(str(p))) for t,p in q['price_tiers'] if int(t)<=n]
        tier,price=max(applicable)
        assert int(r[d+'_price_break'])==tier and Decimal(unit)==price
        assert Decimal(extended)==price*n
        assert str(extended) in (OUT/'BOM_ORDER.md').read_text()
        if r['mpn']=='BSS138':assert r['manufacturer']=='onsemi'
        if r['mpn']=='SMCJ36CA':assert r['manufacturer']=='Littelfuse'
for d in ['lcsc','mouser','digikey']:
    for scope in ['Catalog board','Harness']:
        selected=[r for r in rows if r['scope']==scope]
        priced=[r for r in selected if r[d+'_extended_usd']!='OPEN']
        assert sum((Decimal(r[d+'_extended_usd']) for r in priced),Decimal(0))==Decimal(totals[d][scope]['known_price_subtotal_usd'])
        assert len(priced)==totals[d][scope]['priced_lines']
        if len(priced)!=len(selected):assert totals[d][scope]['total']=='OPEN'
        available=[r for r in priced if r[d+'_stock'].isdigit() and int(r[d+'_stock'])>=int(r[d+'_qty_to_order'])]
        assert len(available)==totals[d][scope]['stock_sufficient_priced_lines']
        assert sum((Decimal(r[d+'_extended_usd']) for r in available),Decimal(0))==Decimal(totals[d][scope]['stock_sufficient_priced_subtotal_usd'])
    table=markdown.split('## '+d+' commercial register\n',1)[1].split('\n## ',1)[0]
    table_rows={}
    for line in table.splitlines():
        cells=[c.strip() for c in line.split('|')[1:-1]]
        if cells and cells[0] in {r['row_id'] for r in rows}:table_rows[cells[0]]=cells
    assert set(table_rows)=={r['row_id'] for r in rows}
    for r in rows:
        assert table_rows[r['row_id']][2:]==[r[d+'_'+k] for k in ['qty_to_order','unit_price_usd','extended_usd','stock','lead_time','lifecycle']]
finite_build={k for k,a in locks.items() if a['kind']=='exact_limited_build' and a['selection']=='LOCKED'}
assert finite_build=={'B001','B002','B003','B004','B013'}
def accepted_supply_identity(r):
    if any(f in r['flags'] for f in ['EXACT-ORDER','OWNER-HOLD','LOCK-OPEN']):return False
    return 'NRND/EOL' not in r['flags'] or (r['row_id'] in finite_build and r['mpn']==r['captured_mpn']==locks[r['row_id']]['mpn'])
for item in upload:
    r=next(r for r in catalog if r['mpn']==item['Manufacturer Part Number'])
    assert item['LCSC Part Number']==r['lcsc_part_number']
    assert item['Quantity']==r['lcsc_qty_to_order'] and item['Designator']==r['refdes']
    assert int(r['lcsc_stock'])>=int(item['Quantity'])
    assert accepted_supply_identity(r)
    assert r['lcsc_unit_price_usd']!='OPEN' and r['lcsc_order_multiple']!='OPEN'
eligible={r['mpn'] for r in catalog if r['lcsc_part_number']!='OPEN' and r['lcsc_unit_price_usd']!='OPEN'
    and r['lcsc_order_multiple'].isdigit() and r['lcsc_stock'].isdigit()
    and int(r['lcsc_stock'])>=int(r['lcsc_qty_to_order'])
    and accepted_supply_identity(r)}
assert len(upload)==len(eligible) and {r['Manufacturer Part Number'] for r in upload}==eligible
assert any(r['Designator']=='U316' and r['Quantity']=='4' and r['LCSC Part Number']=='C580193' for r in upload)
# Independently verify every saved bias calculation and its actual net pair.
curves=json.loads((ROOT/'third_party/bom_order/CLOSE_CAPACITOR_FACTS.json').read_text())['curves']
netlist=ET.parse(ROOT/'docs/evidence/r3/layout_prep/resume/fresh.xml').getroot()
pin_nets={}
for net in netlist.findall('./nets/net'):
    for node in net.findall('node'):
        pin_nets.setdefault(node.get('ref'),{})[node.get('pin')]=net.get('name')
def interpolate(points, voltage):
    for (v0,c0),(v1,c1) in zip(points,points[1:]):
        if v0 <= voltage <= v1:
            return c0+(c1-c0)*(voltage-v0)/(v1-v0)
    raise AssertionError(('Bias voltage outside retained samples',voltage))
bias_checks=0
for original,a in decisions.items():
    assert set(a['refdes'])=={ref for ref,item in src.items() if item['MPN']==original}
    assert {src[ref]['Footprint'] for ref in a['refdes']}==set(a['footprints'])
    if a.get('kind')=='carrier_only':
        assert original=='CSD18540Q5B' and a['mpn']=='CSD18540Q5BT'
        assert a['offer_evidence']=='Q281' and a['document_revision'].startswith('SLPS488B')
        continue
    ratios=[]
    for t in a['bias_tests']:
        assert t['nets']==pin_nets[t['refdes']], ('Bias net mismatch',t['refdes'])
        assert t['voltage_basis'] and t['voltage_label'] in ['CONFIRMED','CALCULATED','ASSUMED']
        if t['status']=='OPEN':
            assert not a['accepted'] and not a['order_accepted']
            assert t['original_ceff_uf']==t['alternate_ceff_uf']==t['ratio']=='OPEN'
            continue
        for name,key in [(original,'original_ceff_uf'),(a['mpn'],'alternate_ceff_uf')]:
            expected=interpolate(curves[name[:-1]]['points'],t['dc_voltage_v'])
            assert math.isclose(expected,t[key],rel_tol=1e-12,abs_tol=1e-15), (original,t['refdes'],key)
        ratio=t['alternate_ceff_uf']/t['original_ceff_uf']
        assert math.isclose(ratio,t['ratio'],rel_tol=1e-12)
        ratios.append(ratio);bias_checks+=1
    if a['accepted']:
        assert ratios and min(ratios)>=.9 and math.isclose(min(ratios),a['min_ratio'],rel_tol=1e-12)
        assert original[10:13]==a['mpn'][10:13], 'Nominal capacitance code changed'
        assert original[3:5]==a['mpn'][3:5], 'Metric package code changed'
        assert a['alternate_specs']['tempchar']==a['original_specs']['tempchar']
        assert float(a['alternate_specs']['rvol'])>=float(a['original_specs']['rvol'])
        assert curves[a['mpn'][:-1]]['catalog']==a['alternate_specs']
        assert a['alternate_specs']['production_status_en-us']=='B'
assert {a['mpn'] for a in decisions.values() if a['order_accepted']}=={
    'GRM21BZ71E475KE15L','GCM21BR71H105KA03L','CSD18540Q5BT'}
for ref,voltages in [('C352',[12,12.311325,12.593099]),('C601',[5.05832,5.183488]),('C602',[12,12.311325,12.593099])]:
    assert [t['dc_voltage_v'] for t in decisions['GRM32ER71H106KA12L']['bias_tests'] if t['refdes']==ref]==voltages
for path,digest in baseline['hardware_sha256'].items():
    assert hashlib.sha256(hardware_baseline_bytes(ROOT/path)).hexdigest()==digest, ('Unauthorized hardware change since close baseline',path)
for path,digest in meta['source_files'].items():
    assert hashlib.sha256(hardware_baseline_bytes(ROOT/path)).hexdigest()==digest
for path,digest in meta['bom_close_review']['evidence_sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest, ('Close evidence hash mismatch',path)
# Independently verify added same-snapshot offers, pack units and accessory kits.
def check_offer(q,needed):
    pack=q.get('units_per_pack',1)
    assert isinstance(pack,int) and pack>0
    n=math.ceil(int(needed)/pack)
    known=isinstance(q['minimum'],int) and q['minimum']>0 and isinstance(q['multiple'],int) and q['multiple']>0
    if known:n=math.ceil(max(n,q['minimum'])/q['multiple'])*q['multiple']
    prices=[(int(t),Decimal(p)) for t,p in q['price_tiers'] if int(t)<=n]
    price=max(prices)[1] if prices else None
    ready=(known and q['sku'] not in ['OPEN','N/A'] and isinstance(q['stock'],int) and q['stock']>=n
        and q['currency'] in ['USD','EUR','AUD','GBP'] and price is not None)
    return n,price,ready
additional_ready=set()
for r in rows:
    if r['row_id'] not in extra:
        assert r['additional_evidence_id']=='N/A'
        continue
    q=extra[r['row_id']]
    assert r['mpn']==q['mpn']
    n,price,ready=check_offer(q,r['qty_to_order'])
    assert int(r['additional_qty'])==n and n*q.get('units_per_pack',1)>=int(r['qty_to_order'])
    for key in ['supplier','sku','stock','currency','order_unit','units_per_pack','url','observed_date','evidence_id','notes']:
        assert r['additional_'+key]==' '.join(str(q[key]).split())
    assert r['additional_price']==(str(price) if price is not None else 'OPEN')
    assert r['additional_extended']==(str(price*n) if price is not None else 'OPEN')
    if ready:additional_ready.add(r['row_id'])
assert 'M03' not in additional_ready, 'Unconfirmed pack stock cannot close procurement'
assert additional_ready=={'B011','B014','B053','H01','H08'}
assert len(accessory_rows)==len(accessories)==10
accessory_ready={}
for a in accessories:
    r=next(r for r in accessory_rows if r['row_id']==a['row_id'])
    n,price,ready=check_offer(a,a['planning_qty'])
    assert a['kit_count']==4
    if a['order_unit']=='piece':assert a['planning_qty']==a['qty_per_kit']*4
    else:assert a['planning_qty']==1 and a['qty_per_kit']*4<30.48
    assert r['mpn']==a['mpn'] and int(r['qty_to_order'])==n
    assert r['unit_price']==(str(price) if price is not None else 'OPEN')
    assert r['extended_price']==(str(price*n) if price is not None else 'OPEN')
    assert (r['procurement_status']=='STOCKED OFFER')==ready
    accessory_ready.setdefault(a['parent'],[]).append(ready)
for ident in ['O01','O02']:
    r=next(r for r in rows if r['row_id']==ident)
    assert (r['qty_per_board'],r['qty_3_boards'],r['spares'],r['qty_to_order'])==('1','3','1','4')
for ident in ['H07','H08']:
    r=next(r for r in rows if r['row_id']==ident)
    assert r['qty_per_board']=='0.075' and Decimal(r['qty_3_boards'])+Decimal(r['spares'])+4<Decimal('30.48')
at=json.loads((HERE/'ACCESSORY_TOTALS.json').read_text())
assert Decimal(at['known_subtotal'])==sum((Decimal(r['extended_price']) for r in accessory_rows if r['extended_price']!='OPEN'),Decimal(0))
assert at['currency']=='USD' and all(a['currency']=='USD' for a in accessories)

# Lock scope and disclosed proxy, independently of the generation guard.
start_ids={r['row_id'] for r in lock_baseline['needs_owner_decision']}
assert len(start_ids)==24 and set(locks)==start_ids
assert {k for k,a in locks.items() if a['selection']=='OPEN'}==set()
for k,a in locks.items():
    r=next(r for r in rows if r['row_id']==k)
    assert a['sources'] and set(a['sources'])<=set(lock_sources)
    assert r['selection_status']==a['selection'] and r['captured_mpn']==a['captured_mpn']
    assert set(r['refdes'].split(', '))==set(a['refdes']) and set(r['footprint'].split('; '))==set(a['footprints'])
    assert a['access_date']=='2026-10-04'
    if a['kind']=='exact_limited_build':assert a['ceff_ratio']==1 and a['mpn']==a['captured_mpn']
a=locks['B011']
assert a['proxy_is_assumption'] is True and a['proxy_mpn']==a['mpn']=='C3216X7R1H475K160AC'
assert (a['nominal_uf'],a['voltage_v'],a['dielectric'],a['tolerance_percent'])==(4.7,50,'X7R',10)
assert [t['dc_voltage_v'] for t in a['bias_tests']]==[26,30.788889,35]
for t in a['bias_tests']:
    assert t['status']=='ESTIMATED_SAME_FAMILY_PROXY' and .9<=t['ratio']<=1.1
    assert set(t['nets'])==set(pin_nets[t['refdes']].values())
assert 'not measured AB equivalence' in a['bias_tests'][0]['basis']
assert next(r for r in rows if r['row_id']=='B045')['mpn']=='TNPW060324K6BEEA'
owner=(HERE/'OWNER_DECISIONS.md').read_text().splitlines()
assert len(owner)==1 and owner[0].startswith('1. **B045') and 'DECISION TAKEN: A on 2026-10-04' in owner[0] and 'LOCKED' in owner[0]
assert 'bench check, does not block layout' in (HERE/'FORCE_LINK_DRAWING.md').read_text()
for source_info in lock_sources.values():
    assert all(source_info.get(k) for k in ['owner','url','revision','relevant_source_files','access_date','license','function_studied','use','modifications','required_attribution'])

# Independently count selection holds and complete stocked offers. Backorders stay OPEN.
open_ids=set()
for r in rows:
    if r['scope']=='PCB feature':continue
    routes=[d for d in ['lcsc','mouser','digikey'] if r[d+'_part_number'] not in ['OPEN','N/A']
        and r[d+'_unit_price_usd'] not in ['OPEN','N/A'] and r[d+'_stock'].isdigit()
        and r[d+'_qty_to_order'].isdigit() and int(r[d+'_qty_to_order'])>0
        and int(r[d+'_stock'])>=int(r[d+'_qty_to_order'])
        and r[d+'_order_multiple'].isdigit() and int(r[d+'_order_multiple'])>0]
    if r['row_id'] in locks:
        a=locks[r['row_id']]
        kit_complete=all(accessory_ready.get(r['row_id'],[False]))
        is_open=a['selection']=='OPEN' or not (routes or r['row_id'] in additional_ready or kit_complete)
    else:is_open=not routes or not accepted_supply_identity(r)
    if is_open:open_ids.add(r['row_id'])
    assert (r['procurement_status']=='OPEN')==is_open
assert open_ids=={r['row_id'] for r in close['procurement_open']}
assert {r['row_id'] for r in close['needs_owner_decision']}==set()
assert close['open_before']==lock_baseline['open_after']==24 and close['open_after']==len(open_ids)
assert close['selection_open_before']==24 and close['selection_open_after']==0
assert set(close['closed_row_ids'])==start_ids-open_ids
assert set(close['newly_open_row_ids'])==open_ids-start_ids==set()
assert close['literal_open_cells_after']==sum(v=='OPEN' for r in rows for v in r.values())
assert close['rows_containing_open_after']==sum(any('OPEN' in v for v in r.values()) for r in rows)
for doc in [markdown,(HERE/'CLOSE_SUMMARY.md').read_text()]:
    assert 'Selection OPEN: 24 → 0' in doc and f'Immediate-procurement OPEN: 24 → {len(open_ids)}' in doc
assert any(r['Manufacturer Part Number']=='GRM32ER71H106KA12L' for r in upload)
assert len(upload)==40
checked_links=0
for document in [OUT/'BOM_ORDER.md']+[HERE/name for name in [
        'CLOSE_SUMMARY.md','CAPACITOR_REVIEW.md','STOCK_REVIEW.md','FORCE_LINK_DRAWING.md','CLOSE_EXECUTION.md',
        'LOCK_REVIEW.md','ACCESSORY_REVIEW.md','LOCK_EXECUTION.md']]:
    for match in re.finditer(r'\]\(([^)]+)\)',document.read_text()):
        target=match.group(1)
        if not target.startswith(('http','OPEN')) and 'VALIDATION.json' not in target:
            assert (document.parent/target).exists(),(document,target)
            checked_links+=1
assert checked_links>=7, 'Local-link check must actually visit the document links'
result=dict(status='PASS for BOM document consistency; procurement and R2 electrical release BLOCKED',source_commit=meta['source_commit'],
    references_accounted_for=len(refs),catalog_components_per_board=298,catalog_mpns=96,custom_links_per_board=7,etched_features_per_board=61,
    csv_rows=len(rows),lcsc_subset_rows=len(upload),spare_arithmetic='PASS',link_hardware_sets='PASS',source_identity_and_footprints='PASS',
    supplier_quantities_and_price_tiers='PASS',supplier_evidence_fields='PASS',currency='PASS',totals='PASS',
    markdown_commercial_tables='PASS',local_links='PASS',local_links_checked=checked_links,
    u316_confirmed_identity_and_upload='PASS',harness_spool_units='PASS',lcsc_exact_membership='PASS',
    reviewed_alternate_scope_and_bias='PASS',bias_calculations_checked=bias_checks,
    lock_scope_and_sources='PASS',selection_open_before=24,selection_open_after=0,
    family_proxy_points_checked=len(locks['B011']['bias_tests']),family_proxy_limit='Estimated same-family model; not measured AB equivalence',
    added_supplier_pack_currency_checks='PASS',accessory_subparts_checked=len(accessory_rows),
    unchanged_hardware_files=len(baseline['hardware_sha256'])-1,
    hardware_scope='PASS: original hashes match after reversing only authorized R203 Value/MPN/Source',
    authorized_hardware_change='hardware/kicad/02_BUCK_5V.kicad_sch: R203 only; PCB unchanged',
    open_rows_before=close['open_before'],open_rows_after=close['open_after'],open_count='PASS',
    erc_drc='ERC before/after 0 errors, 0 warnings; see ../r203_option_a/CHECKS.json. DRC not run: PCB unchanged',source_export_sha256=meta['export_sha256'])
(HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
