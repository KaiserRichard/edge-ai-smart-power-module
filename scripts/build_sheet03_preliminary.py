#!/usr/bin/env python3
"""Scoped Gate2 capture from reviewed pin contracts; no PCB or other-sheet rebuild.

Uses existing project-owned drawing helpers. Only Sheet03 is generated. Ancillary
edits are hierarchical ports, U201.5 PGOOD connection, and root status wording.
"""
import json
import re
from pathlib import Path
from build_r2_schematic import Sheet, normalize, library_symbol, uid, q, fx
ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware/kicad'
SPEC=ROOT/'docs/evidence/r2/output_block.json'


def children(text):
    """Direct child spans of a parent S-expression, preserving all other bytes."""
    depth=0; start=None; quoted=False; escape=False
    for i,ch in enumerate(text):
        if quoted:
            if escape: escape=False
            elif ch=='\\': escape=True
            elif ch=='"': quoted=False
            continue
        if ch=='"': quoted=True
        elif ch=='(':
            depth+=1
            if depth==2: start=i
        elif ch==')':
            if depth==2: yield start,i+1,text[start:i+1]
            depth-=1
    assert depth==0 and not quoted


def append_forms(path, forms):
    text=path.read_text().rstrip()
    path.write_text(text[:-1]+'\n'+'\n'.join(forms)+'\n)\n')


def port(name,net,direction,x,y):
    helper=Sheet(name,name)
    helper.graphics.append(f'(hierarchical_label {q(net)} (shape {direction}) (at {x} {y} 0) {fx(1.016,"left")} (uuid {q(uid(name+":newport:"+net))}))')
    # Unique serial namespace, without colliding with original drawing helpers.
    helper.serial=3000+sum(map(ord,net))
    helper.wire(x,y,x-7.62,y);helper.label(net,x-7.62,y,True)
    return helper.graphics


def add_hierarchy():
    first=HW/'01_INPUT_PROTECTION.kicad_sch'
    second=HW/'02_BUCK_5V.kicad_sch'
    if '(hierarchical_label "VIN_FUSED"' not in first.read_text():
        append_forms(first,port('01_INPUT_PROTECTION','VIN_FUSED','output',35.56,40.64)+port('01_INPUT_PROTECTION','INPUT_SHDN','input',132.08,40.64))
    if '(hierarchical_label "BUCK_PGOOD"' not in second.read_text():
        s=second.read_text()
        instance=next(t for a,b,t in children(s) if t.startswith('(symbol\n') and '(property "Reference" "U201"' in t)
        x,y=map(float,re.search(r'\(at ([\d.]+) ([\d.]+) 0\)',instance).groups())
        px,py=round(x-22.86,4),round(y+5.08,4)
        target=next((a,b) for a,b,t in children(s) if t.startswith('(no_connect') and re.search(r'\(at '+f'{px:g} {py:g}'+r'\)',t))
        s=s[:target[0]]+s[target[1]:];second.write_text(s)
        helper=Sheet('02_BUCK_5V','PGOOD');helper.serial=9000
        helper.wire(px,py,px-7.62,py);helper.label('BUCK_PGOOD',px-7.62,py,True)
        append_forms(second,helper.graphics+port('02_BUCK_5V','BUCK_PGOOD','output',35.56,40.64))
    top=HW/'V1A.kicad_sch';s=top.read_text()
    additions={'01_INPUT_PROTECTION':[('VIN_FUSED','output',4),('INPUT_SHDN','input',5)],
               '02_BUCK_5V':[('BUCK_PGOOD','output',4)],
               '03_OUTPUT_PROTECTION':[('VIN_FUSED','input',2),('GND','passive',3),('BUCK_PGOOD','input',4),('INPUT_SHDN','output',5)]}
    helper=Sheet('V1A','top');helper.serial=12000
    replacements=[]
    for a,b,t in children(s):
        if not t.startswith('(sheet\n'):continue
        name=re.search(r'\(property "Sheetname" "([^"]+)"',t)[1]
        if name not in additions:continue
        x,y=map(float,re.search(r'\(at ([\d.]+) ([\d.]+)\)',t).groups())
        pins=[]
        for net,direction,index in additions[name]:
            if f'(pin "{net}"' in t:continue
            py=round(y+12.7+index*7.62,4)
            pins.append(f'(pin {q(net)} {direction} (at {x:g} {py:g} 180) {fx(1.016,"left")} (uuid {q(uid(name+":"+net))}))')
            helper.wire(x,py,x-7.62,py);helper.label(net,x-7.62,py,True)
        replacements.append((a,b,t[:-1]+'\n'+'\n'.join(pins)+'\n)'))
    for a,b,t in reversed(replacements):s=s[:a]+t+s[b:]
    s=s.replace('OPEN CIRCUIT - NO BYPASS FITTED','PRELIMINARY DISCONNECT + CROWBAR').replace('-> OPEN disconnect','-> preliminary protection')
    top.write_text(s)
    if helper.graphics:append_forms(top,helper.graphics)


def build():
    spec=json.loads(SPEC.read_text());parts=normalize(spec)
    sh=Sheet('03_OUTPUT_PROTECTION','03 OUTPUT PROTECTION - PRELIMINARY',spec['ports'])
    sh.serial=15000
    sh.text('03 OUTPUT PROTECTION | Candidate C + crowbar | PRELIMINARY - R2 BLOCKED - NOT FOR FABRICATION',15.24,15.24,2.54)
    sh.add_ports()
    # A1 pin-contract sheet. Large spacing preserves readable labels and notes.
    large=[c for c in parts if len(c['pins'])>2]
    small=[c for c in parts if len(c['pins'])<=2]
    for i,c in enumerate(large):sh.component(c,63.5+(i%8)*99.06,81.28+(i//8)*66.04)
    start=81.28+((len(large)+7)//8)*66.04
    for i,c in enumerate(small):sh.component(c,45.72+(i%10)*78.74,start+(i//10)*25.4)
    bottom=start+((len(small)+9)//10)*25.4
    sh.text('\n'.join(spec['schematic_notes']),15.24,bottom,1.524)
    sh.save(HW)
    path=HW/'03_OUTPUT_PROTECTION.kicad_sch'
    s=path.read_text().replace('(paper "A3")','(paper "A1")').replace('(date "2026-09-12")','(date "2026-09-29")')
    path.write_text(s)
    lib=HW/'V1A.kicad_sym';old=lib.read_text().rstrip();new=[]
    for c in parts:
        sym=library_symbol(c)
        # New symbols can be rebuilt safely; do not touch historical symbols.
        name=q(c['symbol_name'])
        matches=[(a,b) for a,b,t in children(old) if t.startswith('(symbol '+name+' ')]
        for a,b in reversed(matches):old=old[:a]+old[b:]
        new.append(sym)
    lib.write_text(old[:-1]+'\n'+'\n'.join(new)+'\n)\n')
    add_hierarchy()
    print(f'Captured {len(parts)} Sheet03 components; ancillary hierarchy only; no PCB.')

if __name__=='__main__':build()
