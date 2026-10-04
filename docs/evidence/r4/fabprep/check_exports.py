#!/usr/bin/env python3
"""Four-layer export/assembly regression on a synthetic board, never V1A.
Run with bundled KiCad Python. The current V1A smoke test is recorded separately.
"""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile
import pcbnew as p

ROOT=Path(__file__).resolve().parents[4]
v=lambda x,y:p.VECTOR2I(p.FromMM(x),p.FromMM(y))


def main():
    tmp=Path(tempfile.mkdtemp(prefix='v1a-fab-export-fixture-'))
    spec=importlib.util.spec_from_file_location('rule_probes',Path(__file__).with_name('check_rules.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    b=mod.board();b.GetDesignSettings().SetAuxOrigin(v(5,7))
    for i,(ref,flags,bottom,angle) in enumerate([
        ('C103',p.FP_SMD,False,90),('D301',p.FP_SMD,True,180),
        ('R203',p.FP_SMD,False,270),
        ('R990',p.FP_SMD|p.FP_EXCLUDE_FROM_BOM,False,0),
        ('R991',p.FP_SMD|p.FP_EXCLUDE_FROM_POS_FILES,False,0),
        ('R992',p.FP_SMD|p.FP_DNP,False,0)]):
        f=p.FOOTPRINT(b);f.SetReference(ref);f.SetValue('FIXTURE ONLY')
        f.SetFPID(p.LIB_ID('Synthetic','Fixture'));f.SetAttributes(flags)
        f.SetPosition(v(10+i*5,20));f.Reference().SetVisible(False);f.Value().SetVisible(False)
        pad=p.PAD(f);pad.SetNumber('1');pad.SetPosition(f.GetPosition())
        pad.SetAttribute(p.PAD_ATTRIB_SMD);pad.SetShape(p.PAD_SHAPE_RECT);pad.SetSize(v(1,1))
        layers=p.LSET();layers.AddLayer(p.F_Cu);layers.AddLayer(p.F_Mask);layers.AddLayer(p.F_Paste)
        pad.SetLayerSet(layers);f.Add(pad)
        if bottom:f.Flip(f.GetPosition(),True)
        f.SetOrientationDegrees(angle);b.Add(f)
    # At least one real hole to check drill/map exports in the fixture package.
    mod.via(b,40,40)
    pcb=tmp/'fixture.kicad_pcb';p.SaveBoard(str(pcb),b,True)
    out=tmp/'package with spaces'
    log=tmp/'export.log'
    with log.open('w') as stream:
        result=subprocess.run([str(ROOT/'scripts/export_fab_package.sh'),str(pcb),str(out)],stdout=stream,stderr=subprocess.STDOUT)
    assert result.returncode==0,log.read_text()
    manifest=json.loads((out/'MANIFEST.json').read_text())
    def csvrows(name):
        with (out/'assembly'/name).open(newline='') as stream:
            return list(csv.DictReader(stream))
    bom=csvrows('BOM_JLC.csv');cpl=csvrows('CPL_JLC.csv');raw={r['Ref']:r for r in csvrows('POSITIONS_KICAD.csv')}
    assert list(bom[0])==['Comment','Designator','Footprint','LCSC Part #']
    assert list(cpl[0])==['Designator','Mid X','Mid Y','Layer','Rotation']
    assert {r['Designator'] for r in bom}=={r['Designator'] for r in cpl}=={'C103','D301','R203'}
    codes={r['Designator']:r['LCSC Part #'] for r in bom}
    assert codes=={'C103':'C77055','D301':'C48502','R203':''},codes
    assert len(csvrows('EXCLUDED.csv'))==3
    for row in cpl:
        native=raw[row['Designator']]
        assert float(row['Mid X'].removesuffix('mm'))==float(native['PosX'])
        assert float(row['Mid Y'].removesuffix('mm'))==float(native['PosY'])
        assert float(row['Rotation'])==float(native['Rot'])%360
        assert row['Layer']==native['Side'].capitalize()
    assert next(r for r in cpl if r['Designator']=='C103')['Mid X']=='10.000000mm' # aux origin ignored
    assert next(r for r in cpl if r['Designator']=='D301')['Mid X']=='15.000000mm' # no bottom-X negation
    assert next(r for r in cpl if r['Designator']=='D301')['Layer']=='Bottom'
    assert manifest['inventory']['copper_layers']==['F.Cu','In1.Cu','In2.Cu','B.Cu']
    assert len(list((out/'pdf').glob('*.pdf')))==len(list((out/'png').glob('*.png')))==13
    assert (out/'gerbers/fixture-In1_Cu.g1').is_file()
    assert (out/'gerbers/fixture-In2_Cu.g2').is_file()
    with zipfile.ZipFile(out/manifest['zip']) as archive:
        assert archive.testzip() is None
        assert all(not x.endswith(('.pdf','.csv','.png')) for x in archive.namelist())
        assert 'NOT_FOR_FABRICATION.txt' in archive.namelist()
    assert manifest['input_unchanged'] and not manifest['fabrication_released']
    assert manifest['render']['status']=='EXPORTED',manifest['render']
    rerun=subprocess.run([str(ROOT/'scripts/export_fab_package.sh'),str(pcb),str(out)],capture_output=True,text=True)
    assert rerun.returncode==2 and 'never overwritten' in rerun.stderr
    print(json.dumps({'passed':True,'fixture_only':True,'outdir':str(out),'kicad_version':manifest['kicad_version'],
        'checks':['four actual copper layers / G1 G2','13 PDF/PNG layer pairs','3D rendered',
        'exact CSV headers','BOM=CPL population','LCSC mapping; unmapped R203 blank',
        'DNP/BOM/position exclusions','native top/bottom XY and CCW angles','absolute origin despite nonzero aux origin',
        'no bottom-X negation','zip contents / CRC','input hashes unchanged','nonempty output rejected'],
        'manifest_sha256':__import__('hashlib').sha256((out/'MANIFEST.json').read_bytes()).hexdigest()},indent=2))


if __name__=='__main__':main()
