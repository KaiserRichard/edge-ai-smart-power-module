#!/usr/bin/env python3
"""Read-only Phase D checks of KiCad-exported XML against C2 + selected C3 PFETs.
No analog simulation, safety qualification, PCB edits or procurement operations.
"""
import argparse,csv,hashlib,io,json,re,subprocess
from decimal import Decimal
from pathlib import Path
import xml.etree.ElementTree as ET
from make_schematic_readable import parse,nodes,one,val,prop,allpins
ROOT=Path(__file__).resolve().parents[1]
K=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')
EV=ROOT/'docs/evidence/v1a_lite'
def fields(c):return {f.get('name'):f.text or '' for f in c.findall('./fields/field')}
def expected(root):
 rows={}
 for r in csv.DictReader(io.StringIO((root/'docs/evidence/v1a_lite/PHASE_C2_BOM.csv').read_text())):
  if r['scope'] in ('THERMAL_C_ONLY','UNPRICED'):continue
  for ref in r['ref'].split():
   if re.fullmatch(r'(?:R|C|U|Q|D|F|L|SCR|J)\d+',ref):rows[ref]=r
 for r in csv.DictReader(io.StringIO((root/'docs/evidence/v1a_lite/PHASE_C3_BOM.csv').read_text())):
  if r['ref'] in ('Q101','Q102'):rows[r['ref']]=dict(r,scope='COMMON_INPUT')
 return rows

def validate(tree,root=ROOT):
 errors=[];checks=[]
 def check(ok,message):
  (checks if ok else errors).append(message)
 comps={c.get('ref'):c for c in tree.findall('./components/comp')}
 pin={};nets={}
 for n in tree.findall('./nets/net'):
  name=n.get('name');nets[name]={(x.get('ref'),x.get('pin')) for x in n.findall('node')}
  for x in nets[name]:pin[x]=name
 def p(ref,num):return pin.get((ref,str(num)))
 def members(net,required):
  target=next((name for name in nets if name==f'/{net}'),None)
  check(target is not None and set(required)<=nets.get(target,set()),f'{net} contains required direct pin connections')
 members('VIN_RAW',[('J501','1'),('F101','1')]);members('VIN_FUSED',[('F101','2'),('D101','1'),('Q101','2')])
 members('VIN_PROTECTED',[('Q102','2'),('D106','4'),('D106','5'),('D106','6'),('C101','1'),('U201','8'),('U201','12'),('R206','1')])
 members('VOUT_5V1',[('L201','2'),('SCR301','2'),('R301','1'),('Q301','2'),('F301','1'),('R202','1'),('C217','1'),('C218','1')]+[(f'C{n}','1') for n in range(209,215)])
 members('VOUT_PI',[('F301','2'),('J502','1'),('J503','1'),('C301','1'),('C302','1')])
 members('GND',[('J501','2'),('J502','2'),('J503','2'),('SCR301','1'),('U101','3'),('U301','3'),('U201','1'),('U201','3'),('U201','9'),('U201','11')])
 check(p('SCR301',2)!=p('J502',1),'F301 separates Pi branch only; crowbar remains attached with fuse open')
 check(p('Q101',3)==p('Q102',3)==p('R110',1)==p('R118',1)==p('R150',1),'Common-source PFETs and controller supply upstream of cutoff')
 check(p('Q101',1)!=p('Q102',1),'Independent reverse and cutoff gates')
 for d,qref in [('D102','Q101'),('D103','Q102')]:check(p(d,1)==p(qref,3) and p(d,2)==p(qref,1),d+' clamps its own source/gate')
 check(p('Q103',1)==p('Q106',3)==p('R145',2)==p('R146',1),'Latch clamps Q103 base to inhibit Q102')
 check(p('Q104',1)==p('R161',2)==p('R163',2)==p('R165',1),'Latch SET positive feedback and OV trigger')
 check(p('Q105',3)==p('R161',1)==p('R162',1),'LATCH_H feeds regenerative and inhibit branches')
 check(p('Q105',2)==p('C102',1)==p('D104',1)==p('R144',1),'Latch supply is CTRL12')
 check(p('Q301',3)==p('R307',1)==p('R163',1),'One OV event drives SCR and upstream latch')
 check(p('R307',2)==p('SCR301',3)==p('R308',1),'SCR gate drive and gate/cathode bleed')
 check(p('U201',10)==p('L201',1)==p('C205',2),'Bootstrap capacitor returns to native SW')
 check(p('R204',1)==p('U201',13) and p('R204',2)==p('C205',1)==p('U201',14),'RBOOT/CBOOT wiring')
 check(p('U201',2)==p('C206',1) and len(nets[p('U201',2)])==2,'VCC has bypass only, no protection load')
 check(p('U201',4)==p('R202',2)==p('R203',1)==p('R205',2),'Feedback remains independent of protection')
 check(p('C207',1)==p('L201',2) and p('C207',2)==p('R205',1),'Feedforward series RC from raw output')
 check(p('U201',7)==p('R206',2)==p('R207',1),'Independent EN divider')
 check(p('U201',5) is None or 'unconnected-' in p('U201',5),'PGOOD unused')
 # Component and exact-MPN inventory is independently derived from original BOM.
 exp=expected(root);fitted={ref for ref,c in comps.items() if fields(c).get('MPN')!='PCB_FEATURE'}
 check(fitted==set(exp),f'Exact Phase C2 purchased-reference inventory ({len(exp)} parts)')
 total=Decimal(0);core=Decimal(0)
 for ref,row in exp.items():
  if ref not in comps:continue
  c=comps[ref];f=fields(c);check(f.get('MPN')==row['mpn'],f'{ref} exact MPN')
  lcsc=re.search(r'/(C\d+)\.html',row['source']);check(f.get('LCSC')==(lcsc.group(1) if lcsc else 'OPEN'),f'{ref} LCSC field')
  price=Decimal(row['unit_vnd']);check(Decimal(f['Unit_VND'])==price,f'{ref} inherited dated price')
  total+=price
  if ref not in ('J501','J502'):core+=price
 check(core==Decimal('348655.20')+2*(Decimal('24843.75')-Decimal('9521.45')),'C2 core + exactly two selected C3 PFET deltas')
 check(not any(ref.startswith(('U4','R4','C4')) for ref in comps),'Telemetry/shunt removed')
 check(not any('POWER_MONITOR' in s.get('name','') for s in tree.findall('./design/sheet')),'Four functional sheets, no Sheet04')
 # Every symbol pin, including an NC, must have a physical pad. No extra
 # numbered pads may silently be absent from the symbol (exposed pads included).
 for n in (1,2,3,5):
  path=next((root/'hardware/kicad').glob(f'{n:02}_*.kicad_sch'));doc=parse(path.read_text());libs={val(s[1]):s for s in one(doc,'lib_symbols')[1:]}
  for s in nodes(doc,'symbol'):
   ref=val(prop(s,'Reference')[2])
   if ref.startswith('#'):continue
   fp=val(prop(s,'Footprint')[2]);lib,name=fp.split(':')
   file=(root/'hardware/kicad'/f'{lib}.pretty'/f'{name}.kicad_mod') if lib.startswith('V1A') else (K/'footprints'/f'{lib}.pretty'/f'{name}.kicad_mod')
   check(file.exists(),f'{ref} footprint exists')
   if not file.exists():continue
   pads={val(p[1]) for p in nodes(parse(file.read_text()),'pad') if val(p[1])}
   pins={val(one(p,'number')[1]) for p in allpins(libs[val(one(s,'lib_id')[1])])}
   check(pads==pins,f'{ref} physical pad numbers match all symbol pins')
 # Preserve experimental PCB exactly at the owner-pinned start revision.
 before=subprocess.check_output(['git','show','9c37897:hardware/kicad/V1A.kicad_pcb'],cwd=root)
 check(before==(root/'hardware/kicad/V1A.kicad_pcb').read_bytes(),'PCB byte-identical to 9c37897')
 pro=json.loads((root/'hardware/kicad/V1A.kicad_pro').read_text())
 check(pro['erc']['erc_exclusions']==[],'No ERC exclusions')
 beforepro=json.loads(subprocess.check_output(['git','show','9c37897:hardware/kicad/V1A.kicad_pro'],cwd=root))
 check(pro['erc']==beforepro['erc'],'ERC rules unchanged from baseline')
 report=(root/'docs/evidence/v1a_lite/PHASE_D_ERC.rpt').read_text()
 check('Errors 0  Warnings 0' in report,'Final ERC zero errors and warnings')
 return {'status':'PASS' if not errors else 'FAIL','scope':'capture and static connectivity only; not electrical validation','checks_passed':len(checks),'errors':errors,'purchased_part_count':len(fitted),'pcb_feature_count':len(comps)-len(fitted),'core_vnd':str(core),'installed_purchased_vnd':str(total),'pcb_sha256':hashlib.sha256(before).hexdigest()}
def export_bom(tree,path):
 cols=['Reference','Value','MPN','Manufacturer','Footprint','LCSC','Quantity','Unit_VND','Extended_VND','Scope','Source','Price_basis']
 with path.open('w',newline='') as out:
  w=csv.DictWriter(out,fieldnames=cols);w.writeheader()
  for c in tree.findall('./components/comp'):
   f=fields(c);w.writerow(dict(Reference=c.get('ref'),Value=c.findtext('value'),MPN=f['MPN'],Manufacturer=f['Manufacturer'],Footprint=c.findtext('footprint'),LCSC=f['LCSC'],Quantity=1,Unit_VND=f['Unit_VND'],Extended_VND=f['Unit_VND'],Scope=f['Cost_scope'],Source=f['Source'],Price_basis='Copper feature; no purchased part' if f['MPN']=='PCB_FEATURE' else 'C2 dated planning estimate; Q101/Q102 C3 correction; not a current quote'))
def run(root=ROOT):return validate(ET.parse(root/'docs/evidence/v1a_lite/V1A_LITE.net.xml').getroot(),root)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write-evidence',action='store_true');args=ap.parse_args();t=ET.parse(EV/'V1A_LITE.net.xml').getroot();result=validate(t)
 if args.write_evidence:
  export_bom(t,EV/'V1A_LITE_BOM.csv');(EV/'PHASE_D_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2));raise SystemExit(result['status']!='PASS')
