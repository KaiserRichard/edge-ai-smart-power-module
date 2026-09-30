#!/usr/bin/env python3
"""Prove the Gate 2b drawing preserves baseline electrical data.

Raw XML is retained. Canonical comparison excludes only export metadata (design
source/date/tool/title blocks, library filesystem URIs), order and numeric net
codes. Full net names, every node attribute, complete components and libparts
remain. Source inventories additionally cover nonphysical flags omitted by XML.
"""
import argparse
import copy
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from make_schematic_readable import BASE, ROOT, parse, nodes, one, prop, val, allpins

EVIDENCE=ROOT/'docs/evidence/r2/sheet03/readability'
SCHEMATICS=['V1A','01_INPUT_PROTECTION','02_BUCK_5V','03_OUTPUT_PROTECTION','04_POWER_MONITOR','05_IO_TEST']


def canonical_element(element):
    return {'tag':element.tag, 'attributes':dict(sorted(element.attrib.items())),
            'text':(element.text or '').strip(),
            'children':sorted([canonical_element(c) for c in element],key=lambda v:json.dumps(v,sort_keys=True))}


def canonical_netlist(path):
    root=ET.parse(path).getroot()
    nets=[]
    for original in root.findall('./nets/net'):
        net=copy.deepcopy(original);net.attrib.pop('code',None)
        nets.append(canonical_element(net))
    return {'components':sorted([canonical_element(c) for c in root.findall('./components/comp')],key=lambda c:c['attributes']['ref']),
            'libparts':sorted([canonical_element(c) for c in root.findall('./libparts/libpart')],key=lambda c:json.dumps(c,sort_keys=True)),
            'nets':sorted(nets,key=lambda c:c['attributes']['name']),
            'library_names':sorted(c.get('logical') for c in root.findall('./libraries/library'))}


def source_inventory(doc):
    libs={val(lib[1]):lib for lib in one(doc,'lib_symbols')[1:]}
    result={}
    for inst in nodes(doc,'symbol'):
        ref=val(prop(inst,'Reference')[2]);lib=libs[val(one(inst,'lib_id')[1])]
        result[ref]={
            'instance': [c for c in inst[1:] if not isinstance(c,list) or c[0] not in ('at','property')],
            'properties':sorted([p[1:3] for p in nodes(inst,'property')]),
            'library_metadata':[c for c in lib[2:] if c[0] not in ('symbol','pin_names','pin_numbers','property')],
            'library_properties':sorted([p[1:3] for p in nodes(lib,'property')]),
            'pins':sorted([[p[1:3],one(p,'number')[1],one(p,'name')[1]] for p in allpins(lib)],key=lambda p:p[1])}
    return result


def validate_sources(root=ROOT):
    errors=[];count=0;pages=[]
    for name in SCHEMATICS:
        rel=f'hardware/kicad/{name}.kicad_sch'
        before=parse(subprocess.check_output(['git','show',f'{BASE}:{rel}'],cwd=root,text=True))
        after=parse((root/rel).read_text())
        if source_inventory(before)!=source_inventory(after):errors.append(f'Changed symbol inventory or electrical metadata: {name}')
        count+=len(nodes(after,'symbol'))
        expected='A3'
        if val(one(after,'paper')[1])!=expected:errors.append(f'Wrong page size: {name}')
        for inst in nodes(after,'symbol'):
            for field in ('Reference','Value'):
                p=prop(inst,field);font=one(one(p,'effects'),'font')
                if min(map(float,one(font,'size')[1:]))<(1.27 if name.startswith('03') else 1.5)-1e-6:errors.append(f'Text below sheet minimum: {name} {val(prop(inst,"Reference")[2])}.{field}')
        visible='\n'.join(val(t[1]) for t in nodes(after,'text'))
        if 'PRELIMINARY / R2 BLOCKED / NOT FOR FABRICATION' not in visible:errors.append(f'Missing warning: {name}')
        # Same hierarchy pin identities/directions, source files and UUIDs.
        def hierarchy(doc):
            return sorted([{'uuid':one(s,'uuid')[1], 'properties':sorted(p[1:3] for p in nodes(s,'property')),
                            'pins':sorted([p[1:3]+[one(p,'uuid')[1]] for p in nodes(s,'pin')]),
                            'instances':nodes(s,'instances')} for s in nodes(doc,'sheet')],key=lambda s:s['uuid'])
        if hierarchy(before)!=hierarchy(after):errors.append(f'Changed hierarchy identity: {name}')
        pages.append({'sheet':name,'paper':expected,'reference_value_minimum_mm':1.27 if name.startswith('03') else 1.524})
    return errors,count,pages


def dumps(value):return json.dumps(value,sort_keys=True,indent=2)+'\n'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,default=EVIDENCE/'baseline.net.xml')
    parser.add_argument('--after',type=Path,default=EVIDENCE/'readable.net.xml')
    parser.add_argument('--record',action='store_true',help='Write intentional review evidence after successful comparison')
    args=parser.parse_args()
    before,after=canonical_netlist(args.baseline),canonical_netlist(args.after)
    diff=''.join(difflib.unified_diff(dumps(before).splitlines(True),dumps(after).splitlines(True),fromfile='baseline.canonical.json',tofile='readable.canonical.json'))
    errors,count,pages=validate_sources()
    if diff:errors.append('Netlist electrical data differs')
    if errors:
        print('\n'.join(errors));print(diff);return 1
    result={'status':'PASS','baseline_commit':BASE,'electrical_netlist_identical':True,
            'canonical_diff_bytes':0,'nets':len(before['nets']),'components':len(before['components']),
            'source_symbols_including_power_flags':count,'source_inventory_identical':True,'pages':pages,
            'comparison':'Complete component/libpart XML, full net names and all node attributes; ordering normalized; only design export metadata, library URIs and numeric net codes excluded.',
            'baseline_xml_sha256':sha(args.baseline),'readable_xml_sha256':sha(args.after),
            'canonical_sha256':hashlib.sha256(dumps(before).encode()).hexdigest()}
    if args.record:
        (EVIDENCE/'baseline.canonical.json').write_text(dumps(before))
        (EVIDENCE/'readable.canonical.json').write_text(dumps(after))
        (EVIDENCE/'netlist.diff').write_text(diff)
        (EVIDENCE/'NETLIST_IDENTITY.json').write_text(dumps(result))
    print(dumps(result));return 0

if __name__=='__main__':raise SystemExit(main())
