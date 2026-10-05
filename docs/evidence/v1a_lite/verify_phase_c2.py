#!/usr/bin/env python3
"""Numerical/accounting verification only. No electrical qualification.

Requires numpy for the independent matrix-exponential cross-check; the
calculation reproducer itself uses only the standard library.
"""
import ast
import contextlib
import csv
from decimal import Decimal
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('phase_c', HERE/'calculate_phase_c.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
D = Decimal


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_bytes(relative):
    return subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT)


def verify():
    old_names = ('PHASE_C_CALCULATIONS.md', 'PHASE_C_CALCULATIONS.json',
                 'PHASE_C_BOM.csv', 'PHASE_C_PURCHASE_MODEL.csv')
    for name in old_names:
        assert (HERE/name).read_bytes() == git_bytes('docs/evidence/v1a_lite/'+name)
    old_tree = ast.parse(git_bytes('docs/evidence/v1a_lite/calculate_phase_c.py'))
    new_tree = ast.parse((HERE/'calculate_phase_c.py').read_text())
    new_functions = {n.name:n for n in new_tree.body if isinstance(n, ast.FunctionDef)}
    for n in old_tree.body:
        if isinstance(n, ast.FunctionDef) and n.name != 'main':
            assert ast.dump(n) == ast.dump(new_functions[n.name]), n.name
    outputs = ('PHASE_C2_REVISION.json', 'PHASE_C2_BOM.csv', 'PHASE_C2_PURCHASE_MODEL.csv')
    before = {n:sha(HERE/n) for n in outputs}
    with contextlib.redirect_stdout(io.StringIO()):
        result = c.calculate_c2()
    assert before == {n:sha(HERE/n) for n in outputs}, 'non-deterministic C2 output'

    # Independent linear-state solution: exp(A*t) via eigen-decomposition.
    # It does not use the reproducer's RK4 or threshold-event interpolation.
    baseline = c.crowbar(); rc=.003; rb=.014; cc=110e-6; cb=1600e-6; L=4.352e-6
    conductance=1/rc+1/rb; ai=1/conductance; ac=(1/rc)/conductance; ab=(1/rb)/conductance
    A=np.array([[-ai/L,-ac/L,-ab/L],
                [ai/(rc*cc),(ac-1)/(rc*cc),ab/(rc*cc)],
                [ai/(rb*cb),ac/(rb*cb),(ab-1)/(rb*cb)]])
    ev, basis=np.linalg.eig(A)
    initial=np.array([baseline['initial_fault_a'],baseline['initial_fault_v']-24,
                      baseline['initial_fault_v']-24])
    coeff=np.linalg.solve(basis,initial)
    def voltage(t):
        state=np.real(basis@(np.exp(ev*t)*coeff))
        return float(24+np.dot([ai,ac,ab],state))
    def crossing(target):
        lo,hi=0,30e-6
        for _ in range(80):
            mid=(lo+hi)/2
            if voltage(mid)<target: lo=mid
            else: hi=mid
        return (lo+hi)/2
    tt=crossing(baseline['static_trip_screen_v'][1])
    exact_allow=(crossing(5.5)-tt)*1e6
    exact_peak=voltage(tt+.5e-6)
    row=result['selected_fault']
    assert abs(exact_allow-row['allowed_delay_us'])<1e-5
    assert abs(exact_peak-row['pi_peak_unity_interface_v']['0.5'])<1e-6
    half=c.c2_esr_fault(24,L,cc,cb,rb,dt=5e-9)
    assert abs(half['allowed_delay_us']-row['allowed_delay_us'])<1e-5
    pi=c.c2_pi_fault(.5,1e-6,.059)
    pi_half=c.c2_pi_fault(.5,1e-6,.059,dt=5e-9)
    assert abs(pi['pi_peak_v']-pi_half['pi_peak_v'])<.002

    bom=list(csv.DictReader((HERE/'PHASE_C2_BOM.csv').open()))
    purchases=list(csv.DictReader((HERE/'PHASE_C2_PURCHASE_MODEL.csv').open()))
    core=[r for r in bom if r['scope'] not in ('CONNECTORS','UNPRICED','THERMAL_C_ONLY')]
    core_cost=sum(D(r['unit_vnd'])*int(r['qty']) for r in core)
    assert core_cost==D(result['totals']['A_core_vnd'])
    installed_interfaces=sum(D(r['extended_vnd']) for r in bom if r['scope']=='CONNECTORS')
    assert core_cost+installed_interfaces+10600==D(result['totals']['B_core_board_connectors_vnd'])
    imported_cash=sum(D(r['cost_vnd']) for r in purchases if r['method']=='phase_c_spares')
    local_cash=sum(D(r['cost_vnd']) for r in purchases if r['method']=='local_plan_spares')
    assert imported_cash+D('263502.75')+408000==D(result['totals']['C_first_build_vnd'])
    assert local_cash+D('437719')==D(result['totals']['C_local_sourcing_vnd'])
    local_rows=[r for r in purchases if r['method']=='local_plan_spares' and r['unit_usd']=='local lot']
    assert sum(D(r['cost_vnd']) for r in local_rows)==18200
    for r in purchases:
        if r['unit_usd'] != 'local lot':
            assert int(r['buy'])>=int(r['target'])
            assert D(r['unit_usd'])*int(r['buy'])*26500==D(r['cost_vnd'])
    refs=[ref for r in bom if r['scope'] not in ('UNPRICED','THERMAL_C_ONLY') for ref in r['ref'].split()]
    assert len(refs)==len(set(refs))
    for r in bom:
        if r['scope'] not in ('UNPRICED','THERMAL_C_ONLY'):
            assert len(r['ref'].split())==int(r['qty'])
    basis_data=json.loads((ROOT/'third_party/v1a_lite_phase_c2/LOCAL_SOURCING_BASIS.json').read_text())
    sibling=Path(basis_data['source'])
    assert sha(sibling)==basis_data['sha256'], 'sibling sourcing plan changed'
    names=subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=ROOT,text=True).splitlines()
    assert not any(n.endswith(('.kicad_sch','.kicad_pcb','.kicad_pro','.kicad_sym','.kicad_mod')) for n in names)
    for n in names:
        assert n.startswith(('docs/','third_party/v1a_lite_phase_c2/')), n
    out=dict(label='EVIDENCE: numerical and accounting tests only; hardware NOT RUN',
             checks={k:'PASS' for k in ['historical_C_evidence_unchanged','original_calculation_functions_reused',
                                       'deterministic_regeneration','independent_matrix_exponential',
                                       'RK4_step_halving','BOM_unique_references','A_B_C_arithmetic',
                                       'local_shared_lots_charged_once','minimum_purchase_quantities',
                                       'sibling_source_unchanged','no_CAD_changes']},
             matrix_solution=dict(allowed_delay_us=exact_allow,peak_at_0p5us_v=exact_peak),
             pi_step_halving=dict(dt10ns_peak_v=pi['pi_peak_v'],dt5ns_peak_v=pi_half['pi_peak_v']),
             output_sha256=before,reproducer_sha256=sha(HERE/'calculate_phase_c.py'),
             verifier_sha256=sha(Path(__file__)),ERC='N/A no CAD edits',DRC='N/A no PCB edits',
             hardware_tests='NOT RUN; no fabrication or purchases')
    (HERE/'PHASE_C2_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    verify()
