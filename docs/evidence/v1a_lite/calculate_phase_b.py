import csv,json,pathlib,decimal,math
D=decimal.Decimal
root=pathlib.Path(__file__).resolve().parents[3]
obs=json.loads((root/'third_party/v1a_lite_phase_b/LCSC_OBSERVATIONS.json').read_text())
parts=json.loads((root/'docs/evidence/v1a_lite/PHASE_B_PARTS.json').read_text())
rows=[]
for p in parts:
 o=obs[p['code']];tiers=o['productPriceList'];eligible=[t for t in tiers if t['ladder']<=10];t=eligible[-1] if eligible else tiers[0]
 unit=D(t['productPrice']);q=p['qty'];ext=q*unit
 rows.append(dict(scope=p['scope'],ref=p['ref'],mpn=o['productModel'],manufacturer=o['brandNameEn'],value=p['value'],qty=q,quote_qty=10,unit_usd_at_qty10=str(unit) if eligible else 'OPEN',costing_unit_usd=str(unit),costing_break=t['ladder'],extended_usd=str(ext),extended_vnd=str(ext*26500),supplier='LCSC',source=o['url'],access_date=o['access_date'],stock=o['stockNumber'],moq=o['minBuyNumber'],package_size=o['minPacketNumber'],vietnam_availability='OPEN local stock; cross-border LCSC import proposed',safety_critical=p['safety'],substitute_allowed=p['substitute'],label='PROPOSED / CALCULATED',notes=p.get('notes','')+(' Actual minimum-lot price normalized per installed part; no ten-piece offer.' if not eligible else '')))
with (root/'docs/evidence/v1a_lite/PHASE_B_BOM.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
for s in sorted(set(r['scope'] for r in rows)):
 print(s,sum(D(r['extended_usd']) for r in rows if r['scope']==s),sum(D(r['extended_vnd']) for r in rows if r['scope']==s))

# Cost models: an installed board, versus actual minimum lots for one build and spares.
# minPacketNumber in the source is reel/package size, NOT a purchase increment.
# Use minBuyNumber as a provisional cut-tape increment; checkout verification OPEN.
from collections import Counter
choices={'1':['OPT1','CROWBAR'],'2':['OPT2'],'3A':['OPT3'],'3B':['OPT3','CROWBAR']}
connector_specs=[
 dict(ref='JIN JOUT',mpn='B2P-VH-FB-B(LF)(SN)',manufacturer='JST',qty=2,unit='0.1607',buy=5,supplier='LCSC',url='https://www.lcsc.com/product-detail/C158006.html',date='2026-10-03',moq=5,stock='35200'),
 dict(ref='JIN_MATE JOUT_MATE',mpn='VHR-2N',manufacturer='JST',qty=2,unit='0.11',buy=3,supplier='DigiKey',url='https://www.digikey.com/en/products/detail/jst-sales-america-inc/VHR-2N/608624',date='2026-10-04',moq=1,stock='94705'),
 dict(ref='CONTACT1 CONTACT2 CONTACT3 CONTACT4',mpn='SVH-41T-P1.1',manufacturer='JST',qty=4,unit='0.08810',buy=100,supplier='DigiKey',url='https://www.digikey.com/en/products/detail/jst-sales-america-inc/SVH-41T-P1-1/26213078',date='2026-10-04',moq=100,stock='OPEN')]
connector_inst=sum(D(x['unit'])*x['qty'] for x in connector_specs)*26500
connector_buy=sum(D(x['unit'])*x['buy'] for x in connector_specs)*26500
for c in connector_specs:
 row={k:'' for k in rows[0]}
 row.update(scope='CONNECTORS',ref=c['ref'],mpn=c['mpn'],manufacturer=c['manufacturer'],value='Required connector/harness component; not core PCB',qty=c['qty'],quote_qty=10,unit_usd_at_qty10=c['unit'] if c['moq']<=10 else 'OPEN',costing_unit_usd=c['unit'],costing_break=c['moq'],extended_usd=str(D(c['unit'])*c['qty']),extended_vnd=str(D(c['unit'])*c['qty']*26500),supplier=c['supplier'],source=c['url'],access_date=c['date'],stock=c['stock'],moq=c['moq'],package_size='OPEN',vietnam_availability='OPEN local; imported offer reused from Phase A/R2',safety_critical='yes',substitute_allowed='no',label='PROPOSED / CALCULATED',notes='Archived BOM_ORDER/BOM_ACCESSORIES offer; price freshness and mating rating OPEN; contact price normalized from 100-piece minimum.')
 rows.append(row)
with (root/'docs/evidence/v1a_lite/PHASE_B_BOM.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
purchases=[];totals={}
for opt,scopes in choices.items():
 q=Counter()
 for p in parts:
  if p['scope'].startswith('COMMON_') or p['scope'] in scopes:q[p['code']]+=p['qty']
 core=D(0);cash=D(0)
 for code,n in sorted(q.items()):
  o=obs[code];tiers=o['productPriceList']
  installed_tier=([t for t in tiers if t['ladder']<=10] or tiers[:1])[-1]
  core+=n*D(installed_tier['productPrice'])
  needed=n+max(1,math.ceil(n*.25));moq=o['minBuyNumber'];buy=math.ceil(max(needed,moq)/moq)*moq
  tier=[t for t in tiers if t['ladder']<=buy][-1];cost=buy*D(tier['productPrice']);cash+=cost
  purchases.append(dict(option=opt,mpn=o['productModel'],code=code,installed_qty=n,required_with_spares=needed,provisional_buy_qty=buy,moq=moq,price_break=tier['ladder'],unit_usd=tier['productPrice'],extended_vnd=str(cost*26500),stock=o['stockNumber'],source=o['url'],notes='OPEN procurement' if not o['stockNumber'] else 'MOQ used as provisional order increment; verify'))
 A=core*26500;B=A+connector_inst+D(10600)
 sink=D(40000) if opt in ('1','3B') else D(0)
 C=cash*26500+connector_buy+D(53000+35000+180000+50000+50000)+sink
 totals[opt]={'A_core_vnd':str(A),'B_core_board_connectors_vnd':str(B),'C_first_build_vnd':str(C),'core_purchase_with_spares_vnd':str(cash*26500),'connectors_installed_vnd':str(connector_inst),'connector_purchase_vnd':str(connector_buy),'sink_allowance_vnd':str(sink),'headroom_to_1000000_vnd':str(D(1000000)-C),'budget_status':'FAIL: over hard ceiling; quotes/stock also OPEN'}
with (root/'docs/evidence/v1a_lite/PHASE_B_PURCHASE_MODEL.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(purchases[0]),lineterminator="\n");w.writeheader();w.writerows(purchases)
(root/'docs/evidence/v1a_lite/PHASE_B_TOTALS.json').write_text(json.dumps(totals,indent=2)+'\n')
print(json.dumps(totals,indent=2))

# Screening arithmetic only; no validated electrical behavior is implied.
L=4.352e-6; C=110e-6; v0=5.124; i0=6.345
faults=[]
for name,vt,delay in [('1',5.43,.5),('1',5.43,2),('2',5.45,5),('3',5.418,1.2)]:
 for vin in (24,28):
  a=(vin-v0)/(L*C); tt=(-i0/C+math.sqrt((i0/C)**2+2*a*(vt-v0)))/a
  it=i0+(vin-v0)*tt/L; d=delay*1e-6
  peak=vt+it*d/C+(vin-vt)*d*d/(2*L*C)
  faults.append(dict(option=name,vin=vin,trip=vt,delay_us=delay,threshold_time_us=tt*1e6,current_at_trip_a=it,peak_v=peak,passes_frozen_ceiling=peak<5.5))
calc={'label':'CALCULATED sensitivity only; L/C/source/timing ASSUMED, no qualification',
 'fault_inputs':dict(L_H=L,C_F=C,V0_V=v0,I0_A=i0),'faults':faults,
 'crowbar_static_trip_v':[(2.483-.034-.008)*(1+1128.6/1001),(2.507+.034)*(1+1131.4/999)+6.5e-6*1131.4],
 'input_static_trip_v':[(2.483-.034-.026)*(1+110000*.999/(10000*1.001)),(2.507+.034)*(1+110000*1.001/(10000*.999))+6.5e-6*110000*1.001],
 'efuse_static_trip_v':[1.183*(1+34200*.999/(10000*1.001))-.1e-6*34200*1.001,1.223*(1+34200*1.001/(10000*.999))+.1e-6*34200*1.001],
 'scr_watts_by_current_a':{str(i):.85*i+.03*i*i for i in (2.2,3,5,6)},
 'input_charge_limit_C':92e-6*(36-31.3),'input_15A_25us_peak_v':31.3+15*25e-6/92e-6}
(root/'docs/evidence/v1a_lite/PHASE_B_CALCULATIONS.json').write_text(json.dumps(calc,indent=2)+'\n')
