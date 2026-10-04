#!/usr/bin/env python3
"""Native KiCad boundary probes; all fixture boards are created in a temp dir.
Run with KiCad's bundled Python. Never edits the project board.
"""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import pcbnew as p

ROOT = Path(__file__).resolve().parents[4]
CLI = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
mm = p.FromMM
v = lambda x, y: p.VECTOR2I(mm(x), mm(y))


def board():
    b = p.BOARD()
    b.SetCopperLayerCount(4)
    for name in ('/GND', '/TEST', '/VIN_PROTECTED', '/VIN_FUSED',
                 '/03_OUTPUT_PROTECTION/AUX_RAW', '/02_BUCK_5V/BUCK_CBOOT'):
        b.Add(p.NETINFO_ITEM(b, name))
    for a, z in [((0, 0), (50, 0)), ((50, 0), (50, 50)),
                 ((50, 50), (0, 50)), ((0, 50), (0, 0))]:
        s = p.PCB_SHAPE(b); s.SetShape(p.SHAPE_T_SEGMENT)
        s.SetStart(v(*a)); s.SetEnd(v(*z)); s.SetLayer(p.Edge_Cuts)
        s.SetWidth(mm(0.05)); b.Add(s)
    return b


def track(b, x, y, net='/GND', width=0.2, layer=p.F_Cu):
    t = p.PCB_TRACK(b); t.SetStart(v(x,y)); t.SetEnd(v(x+5,y))
    t.SetWidth(mm(width)); t.SetLayer(layer); t.SetNet(b.FindNet(net)); b.Add(t)


def via(b, x, y, drill=0.3, diameter=0.6):
    a=p.PCB_VIA(b); a.SetPosition(v(x,y)); a.SetWidth(mm(diameter))
    a.SetDrill(mm(drill)); a.SetViaType(p.VIATYPE_THROUGH)
    a.SetLayerPair(p.F_Cu,p.B_Cu); a.SetNet(b.FindNet('/GND')); b.Add(a)


def pad(b, x, y, diameter=0.81, drill=0.3, smd=False):
    f=p.FOOTPRINT(b); f.SetReference('J'+str(len(list(b.GetFootprints()))+1))
    f.SetPosition(v(x,y)); f.Reference().SetVisible(False); f.Value().SetVisible(False)
    a=p.PAD(f); a.SetNumber('1'); a.SetPosition(v(x,y)); a.SetSize(v(diameter,diameter))
    a.SetShape(p.PAD_SHAPE_CIRCLE)
    a.SetAttribute(p.PAD_ATTRIB_SMD if smd else p.PAD_ATTRIB_PTH)
    a.SetLayerSet(p.LSET.FrontMask() if smd else p.LSET.AllCuMask())
    if smd:
        ls=p.LSET(); ls.AddLayer(p.F_Cu); ls.AddLayer(p.F_Mask); a.SetLayerSet(ls)
    else:
        a.SetDrillSize(v(drill,drill))
    a.SetNet(b.FindNet('/GND')); f.Add(a); b.Add(f)


def main():
    results=[]
    with tempfile.TemporaryDirectory(prefix='v1a-fab-rules-') as tmp:
        tmp=Path(tmp)
        def check(name, build, kind, fails):
            b=board(); build(b)
            src=tmp/(name+'.kicad_pcb'); p.SaveBoard(str(src),b,True)
            shutil.copyfile(ROOT/'hardware/kicad/V1A.kicad_dru',src.with_suffix('.kicad_dru'))
            out=src.with_suffix('.json')
            r=subprocess.run([CLI,'pcb','drc','--format','json','--severity-all','--exit-code-violations','-o',str(out),str(src)],capture_output=True,text=True)
            assert r.returncode in (0,5), (name,r.stdout,r.stderr)
            j=json.loads(out.read_text()); violations=j['violations']
            assert not any('rule' in a['type'] for a in violations), violations
            hits=[a['description'] for a in violations if a['type']==kind]
            assert bool(hits)==fails, (name,kind,fails,violations)
            results.append({'probe':name,'type':kind,'expected_violation':fails,'matched':hits,'pass':True})
        for layer in (p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu):
            for net, limit in [('/TEST',0.2),('/VIN_PROTECTED',0.25),('/VIN_FUSED',0.64),('/03_OUTPUT_PROTECTION/AUX_RAW',0.64),('/02_BUCK_5V/BUCK_CBOOT',0.64)]:
                for reverse in (False,True):
                    for delta in (-0.01,0.01):
                        first,second=(net,'/GND') if reverse else ('/GND',net)
                        name='space_%s_%s_%s_%s'%(layer,net.split('/')[-1],reverse,delta)
                        check(name,lambda b: (track(b,10,10,first,layer=layer),track(b,10,10.2+limit+delta,second,layer=layer)), 'clearance',delta<0)
        for w in (0.19,0.21):
            check('width_'+str(w),lambda b:track(b,10,10,width=w),'track_width',w<0.2)
        check('via_drill_bad',lambda b:via(b,10,10,0.29),'drill_out_of_range',True)
        check('via_ring_bad',lambda b:via(b,10,10,0.32),'annular_width',True)
        check('via_ring_good',lambda b:via(b,10,10),'annular_width',False)
        for d in (0.80,0.82):
            check('pth_ring_'+str(d),lambda b:pad(b,10,10,d),'annular_width',d<0.808)
        for gap in (0.19,0.21):
            check('via_holes_'+str(gap),lambda b:(via(b,10,10),via(b,10.3+gap,10)),'hole_to_hole',gap<0.2)
        for gap in (0.44,0.46):
            check('pad_holes_'+str(gap),lambda b:(pad(b,10,10),pad(b,10.3+gap,10)),'hole_to_hole',gap<0.45)
        for gap in (0.49,0.51):
            check('edge_'+str(gap),lambda b:track(b,10,0.1+gap),'copper_edge_clearance',gap<0.5)
        for gap in (0.14,0.16):
            def silk(b):
                pad(b,10,10,1,smd=True)
                s=p.PCB_SHAPE(b); s.SetShape(p.SHAPE_T_SEGMENT)
                s.SetStart(v(9.8,10.5+gap+0.075)); s.SetEnd(v(10.2,10.5+gap+0.075))
                s.SetWidth(mm(0.15)); s.SetLayer(p.F_SilkS); b.Add(s)
            check('silk_'+str(gap),silk,'silk_over_copper',gap<0.15)
    print(json.dumps({'kicad_version':p.GetBuildVersion(),'checks':len(results),'passed':True,'results':results},indent=2))


if __name__=='__main__': main()
