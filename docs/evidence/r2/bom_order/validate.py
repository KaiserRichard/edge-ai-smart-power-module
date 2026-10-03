#!/usr/bin/env python3
"""Independent coverage, quantity, cost and exclusion checks for the exported order files."""
import csv
import hashlib
import json
import math
import re
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/evidence/r2'
HERE=Path(__file__).resolve().parent
source=list(csv.DictReader((HERE/'SOURCE_BOM.csv').open()))
rows=list(csv.DictReader((OUT/'BOM_ORDER.csv').open()))
upload=list(csv.DictReader((OUT/'BOM_ORDER_LCSC.csv').open()))
meta=json.loads((HERE/'PROVENANCE.json').read_text())
facts=json.loads((ROOT/'third_party/bom_order/CATALOG_FACTS.json').read_text())
facts+=json.loads((ROOT/'third_party/bom_order/RESUME_CATALOG_FACTS.json').read_text())
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
    assert all(src[ref]['MPN'].replace('EEUFR1E221','EEU-FR1E221')==r['mpn'] for ref in listed)
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
for item in upload:
    r=next(r for r in catalog if r['mpn']==item['Manufacturer Part Number'])
    assert item['LCSC Part Number']==r['lcsc_part_number']
    assert item['Quantity']==r['lcsc_qty_to_order'] and item['Designator']==r['refdes']
    assert int(r['lcsc_stock'])>=int(item['Quantity'])
    assert not any(flag in r['flags'] for flag in ['NRND/EOL','EXACT-ORDER'])
    assert r['lcsc_unit_price_usd']!='OPEN' and r['lcsc_order_multiple']!='OPEN'
eligible={r['mpn'] for r in catalog if r['lcsc_part_number']!='OPEN' and r['lcsc_unit_price_usd']!='OPEN'
    and r['lcsc_order_multiple'].isdigit() and r['lcsc_stock'].isdigit()
    and int(r['lcsc_stock'])>=int(r['lcsc_qty_to_order'])
    and not any(flag in r['flags'] for flag in ['NRND/EOL','EXACT-ORDER'])}
assert len(upload)==len(eligible) and {r['Manufacturer Part Number'] for r in upload}==eligible
assert any(r['Designator']=='U316' and r['Quantity']=='4' and r['LCSC Part Number']=='C580193' for r in upload)
checked_links=0
for match in re.finditer(r'\]\(([^)]+)\)',markdown):
    target=match.group(1)
    if not target.startswith(('http','OPEN')) and 'VALIDATION.json' not in target:
        assert (OUT/target).exists(),target
        checked_links+=1
assert checked_links>=7, 'Local-link check must actually visit the document links'
result=dict(status='PASS for BOM document consistency; procurement and R2 electrical release BLOCKED',source_commit=meta['source_commit'],
    references_accounted_for=len(refs),catalog_components_per_board=298,catalog_mpns=96,custom_links_per_board=7,etched_features_per_board=61,
    csv_rows=len(rows),lcsc_subset_rows=len(upload),spare_arithmetic='PASS',link_hardware_sets='PASS',source_identity_and_footprints='PASS',
    supplier_quantities_and_price_tiers='PASS',supplier_evidence_fields='PASS',currency='PASS',totals='PASS',
    markdown_commercial_tables='PASS',local_links='PASS',local_links_checked=checked_links,
    u316_confirmed_identity_and_upload='PASS',harness_spool_units='PASS',lcsc_exact_membership='PASS',
    erc_drc='Not run: CAD read-only; no schematic or PCB changes',source_export_sha256=meta['export_sha256'])
(HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
