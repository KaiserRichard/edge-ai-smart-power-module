#!/usr/bin/env python3
"""Independent numerical/accounting checks; no hardware qualification or CAD writes."""
import sys
sys.dont_write_bytecode=True
import ast
import contextlib
import csv
import io
import json
import math
import subprocess
from decimal import Decimal
from pathlib import Path
import calculate_phase_c3 as c
H=c.HERE;R=c.ROOT;D=Decimal

def verify():
    evidence={}
    # Historical evidence is checked byte-for-byte without re-running C/C2 writers.
    old=[]
    for stem in ('PHASE_C_','PHASE_C2_'):
        for p in sorted(H.glob(stem+'*')):
            rel=str(p.relative_to(R))
            prior=subprocess.check_output(['git','show','b20b51c:'+rel],cwd=R)
            assert p.read_bytes()==prior,rel
            old.append(rel)
    prev=ast.parse(subprocess.check_output(['git','show','b20b51c:docs/evidence/v1a_lite/calculate_phase_c.py'],cwd=R))
    now=ast.parse((H/'calculate_phase_c.py').read_text())
    def funcs(tree):return {n.name:ast.dump(n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name!='main'}
    assert funcs(prev)==funcs(now)
    evidence['historical_artifacts_unchanged']=old
    evidence['C_C2_functions_unchanged']='PASS'
    names=['PHASE_C3_OPTION3B.json','PHASE_C3_BOM.csv','PHASE_C3_PURCHASE_MODEL.csv']
    before={n:c.sha(H/n) for n in names}
    with contextlib.redirect_stdout(io.StringIO()):j=c.calculate_c3()
    assert before=={n:c.sha(H/n) for n in names}
    evidence['deterministic_regeneration']='PASS'
    # Independent midpoint ODE integration of two capacitor states, compared
    # to analytic transfer function. No reuse of cap_step algebra in integrator.
    current=j['current_limit']['max_a'];cc=40e-6;cb=1600e-6;rb=.014
    v1=v2=0.;dt=1e-9
    def rates(a,b):return ((current-(a-b)/rb)/cc,(a-b)/(rb*cb))
    for _ in range(14000):
        a,b=rates(v1,v2);x,y=rates(v1+a*dt/2,v2+b*dt/2);v1+=x*dt;v2+=y*dt
    err=abs(v1-c.cap_step(14e-6,current));assert err<1e-8,err
    # Independent charge conservation at the same instant.
    charge_error=abs(cc*v1+cb*v2-current*14e-6);assert charge_error<1e-12
    evidence['analytic_vs_independent_midpoint_cap_error_v']=err
    evidence['capacitor_charge_conservation_error_c']=charge_error
    convergence=[]
    for case in [dict(vin=24,ilim=current),dict(vin=29.26,ilim=current,limit_delay_us=20,scr_delay_us=1000),dict(vin=29.26,failed_short=True,scr_delay_us=5,harness_l=.2e-6)]:
        a=c.fault_model(**case,dt=1e-8);b=c.fault_model(**case,dt=5e-9)
        delta=abs(a['pi_peak_v']-b['pi_peak_v']);assert delta<.002,(case,delta)
        assert a['screen']==b['screen']
        convergence.append(dict(case=case,pi_delta_v=delta,screen=a['screen']))
    evidence['transient_step_halving']=convergence
    rows=list(csv.DictReader((H/'PHASE_C3_BOM.csv').open()))
    physical=[r for r in rows if r['scope'] not in ('THERMAL_C_ONLY','UNPRICED')]
    refs=[v for r in physical for v in r['ref'].split()];assert len(refs)==len(set(refs))
    core=[r for r in physical if r['scope']!='CONNECTORS']
    assert sum(D(r['extended_vnd']) for r in core)==D(j['costs']['A_core_vnd'])
    for r in physical:assert int(r['qty'])*D(r['unit_vnd'])==D(r['extended_vnd'])
    counts={}
    for r in core:counts[r['mpn']]=counts.get(r['mpn'],0)+int(r['qty'])
    purchases=list(csv.DictReader((H/'PHASE_C3_PURCHASE_MODEL.csv').open()))
    for p in purchases:
        n=counts[p['mpn']];assert int(p['installed'])==n
        target=n+(max(1,math.ceil(.25*n)) if p['method']=='phase_c_spares' else 1)
        assert int(p['target'])==target
        assert int(p['buy'])>=target,(p['mpn'],p['buy'],target)
    for method,key in [('phase_c_spares','conventional_core_purchase_vnd'),('local_plan_spares','local_core_purchase_vnd')]:
        assert sum(D(p['cost_vnd']) for p in purchases if p['method']==method)==D(j['costs'][key])
    co=j['costs']
    assert D(co['C_first_build_vnd'])==D(co['conventional_core_purchase_vnd'])+sum(D(v) for v in co['conventional_fixed_vnd'].values())+sum(co['conventional_reserves_vnd'].values())
    assert D(co['C_local_sourcing_vnd'])==D(co['local_core_purchase_vnd'])+sum(co['local_fixed_vnd'].values())+sum(co['local_reserves_vnd'].values())
    assert D(co['B_core_board_connectors_vnd'])-D(co['A_core_vnd'])==D('34285.70')
    exact_timing=[p for p in purchases if p['method']=='local_plan_spares' and p['mpn']=='GRM188R71H104KA93D'][0]
    assert exact_timing['unit_usd']!='local lot'
    evidence['BOM_reference_quantities_costs_MOQ_reserves']='PASS'
    for r in json.loads((c.SRC/'DOCUMENT_MANIFEST.json').read_text()):
        if r['file']:assert c.sha(c.SRC/r['file'])==r['sha256']
    evidence['source_PDF_hashes']='PASS'
    changed=subprocess.check_output(['git','diff','--name-only','b20b51c'],cwd=R,text=True).splitlines()
    assert not any(x.endswith(('.kicad_sch','.kicad_pcb','.kicad_pro','.kicad_sym','.kicad_mod')) for x in changed)
    untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
    assert not any(x.endswith(('.kicad_sch','.kicad_pcb','.kicad_pro','.kicad_sym','.kicad_mod')) for x in untracked)
    evidence['CAD_changes']='NONE; ERC/DRC not applicable'
    evidence['scope']='Numerical evidence only. Electrical release BLOCKED.'
    evidence['reproducer_hashes']=j['reproducer_sha256']
    evidence['verifier_sha256']=c.sha(Path(__file__))
    (H/'PHASE_C3_VERIFICATION.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':verify()
