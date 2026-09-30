#!/usr/bin/env python3
"""Apply verifier-requested presentation corrections to the reviewed drawings.

No values, footprints, pin identities or project/ERC settings are edited.
Run fresh exports, identity/ERC checks and rendered-PDF review after use.
"""
import argparse
from make_schematic_readable import *

READABLE_BASE = '2cd138f77190be0871c4b7bc9863db48079f5b74'

def reviewed(name):
    return parse(subprocess.check_output(['git','show',f'{READABLE_BASE}:hardware/kicad/{name}.kicad_sch'],cwd=ROOT,text=True))

def component(doc, ref):
    return next(s for s in nodes(doc,'symbol') if val(prop(s,'Reference')[2])==ref)

def field(doc, ref, name, x, y, justify=None):
    p=prop(component(doc,ref),name)
    replace(p,'at',['at',str(x),str(y),'0'])
    replace(p,'effects',effects(1.524,justify))

def move_label(doc, net, old, new):
    label=next(l for l in nodes(doc,'label') if val(l[1])==net and tuple(map(float,one(l,'at')[1:3]))==old)
    one(label,'at')[1:3]=list(map(str,new))

def write(doc,name):
    (HW/(name+'.kicad_sch')).write_text('\n'.join(line.rstrip() for line in dump(doc).splitlines())+'\n')

def fix_01():
    name='01_INPUT_PROTECTION';d=reviewed(name)
    for net,y in [('INPUT_PGTH',109.22),('INPUT_ILIM',114.3),('INPUT_DVDT',119.38)]:
        move_label(d,net,(320.04,y),(325.12,y))
    field(d,'C103','Value',363.22,157.48)
    write(d,name)

def fix_02():
    name='02_BUCK_5V';d=reviewed(name)
    field(d,'C212','Value',307.34,165.608,'left')
    field(d,'C213','Value',345.44,165.608,'left')
    write(d,name)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sheet',required=True,choices=['01','02'])
    a=p.parse_args();{'01':fix_01,'02':fix_02}[a.sheet]()
