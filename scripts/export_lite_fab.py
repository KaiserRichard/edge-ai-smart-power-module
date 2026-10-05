#!/usr/bin/env python3
"""V1A-Lite review exporter; KiCad bundled Python, no installs.
Adapted from the project-owned wt-fabprep exporter; does not modify CAD.

Reads the PCB only. A zero exit code means exports completed, never fabrication
approval. Original board/project/schematic/rules and procurement files are hashed.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
LCSC = ROOT / 'docs/evidence/v1a_lite/V1A_LITE_BOM.csv'
WARNING = 'NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref_key(ref):
    return [(0, int(x)) if x.isdigit() else (1, x) for x in re.split(r'(\d+)', ref)]


def write_csv(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_lcsc(path):
    mapping = {}
    with path.open(newline='', encoding='utf-8-sig') as stream:
        for row in csv.DictReader(stream):
            if row['MPN'] == 'PCB_FEATURE':
                continue
            ref, code = row['Reference'], row['LCSC']
            if not re.fullmatch(r'C[0-9]+', code):
                if ref != 'D101' or code != 'N/A - Mouser sourced':
                    raise ValueError('Unexpected sourcing gap: ' + ref)
                code = ''  # Never invent an LCSC code for the selected Bourns TVS.
            if ref in mapping:
                raise ValueError('Duplicate component: ' + ref)
            mapping[ref] = (code, row['MPN'])
    if len(mapping) != 100:
        raise ValueError('Expected 100 purchased Lite components')
    return mapping


def assemble(board, raw_pos, out, mapping, schematic):
    """Keep native CLI coordinates/angles; apply no speculative JLC offsets."""
    components = {}
    if schematic:
        root = ET.parse(schematic).getroot()
        components = {c.get('ref'): c for c in root.findall('./components/comp')}
    fps = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if not ref or ref in fps:
            raise ValueError('Empty/duplicate PCB designator: ' + ref)
        fps[ref] = fp
    with raw_pos.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if not {'Ref', 'Val', 'Package', 'PosX', 'PosY', 'Rot', 'Side'}.issubset(reader.fieldnames or []):
            raise ValueError('Unexpected KiCad position headers')
        positions = {}
        for row in reader:
            if row['Ref'] in positions or row['Ref'] not in fps:
                raise ValueError('Invalid/duplicate position reference: ' + row['Ref'])
            positions[row['Ref']] = row
    bom, cpl, omissions, missing_lcsc, rotation = [], [], [], [], []
    # One BOM row per placed reference; procurement quantities/spares are not used.
    for ref in sorted(fps, key=ref_key):
        fp = fps[ref]
        if fp.IsDNP() or fp.IsExcludedFromBOM() or fp.IsExcludedFromPosFiles():
            reasons = [name for name, flag in [('DNP', fp.IsDNP()),
                ('exclude_from_bom', fp.IsExcludedFromBOM()),
                ('exclude_from_position_files', fp.IsExcludedFromPosFiles())] if flag]
            omissions.append({'Designator': ref, 'Reason': ', '.join(reasons)})
            continue
        if ref not in positions:
            raise ValueError('Assembly footprint missing from native position export: ' + ref)
        row = positions[ref]
        if row['Side'].lower() not in ('top', 'bottom'):
            raise ValueError('Unexpected placement side: ' + row['Side'])
        x, y, angle = [float(row[key]) for key in ('PosX', 'PosY', 'Rot')]
        if not all(math.isfinite(n) for n in (x, y, angle)):
            raise ValueError('Nonfinite placement for ' + ref)
        code, mpn = mapping.get(ref, ('', ''))
        # The board can lag an authorized schematic BOM update. Preserve its
        # physical geometry, flag parity, and use the current schematic value.
        value = components[ref].findtext('value') if ref in components else fp.GetValue()
        comment = value + ('; ' + mpn if mpn and mpn != value else '')
        bom.append({'Comment': comment, 'Designator': ref,
                    'Footprint': fp.GetFPID().GetLibItemName(), 'LCSC Part #': code})
        cpl.append({'Designator': ref, 'Mid X': f'{x:.6f}mm', 'Mid Y': f'{y:.6f}mm',
                    'Layer': row['Side'].capitalize(), 'Rotation': f'{angle % 360:.6f}'})
        if not code:
            missing_lcsc.append(ref)
        rotation.append({'Designator': ref, 'Footprint': fp.GetFPIDAsString(),
            'LCSC Part #': code, 'Native Rotation': row['Rot'],
            'Applied Offset': '0', 'Status': 'OPEN — verify JLC zero-angle, pin 1/polarity and centroid'})
    write_csv(out/'BOM_JLC.csv', ['Comment','Designator','Footprint','LCSC Part #'], bom)
    write_csv(out/'CPL_JLC.csv', ['Designator','Mid X','Mid Y','Layer','Rotation'], cpl)
    write_csv(out/'EXCLUDED.csv', ['Designator','Reason'], omissions)
    write_csv(out/'ROTATION_REVIEW.csv', ['Designator','Footprint','LCSC Part #',
        'Native Rotation','Applied Offset','Status'], rotation)
    mismatches = []
    if schematic:
        for ref in sorted(set(components) | {r for r,f in fps.items() if not f.GetAttributes() & pcbnew.FP_BOARD_ONLY}, key=ref_key):
            if ref not in fps or ref not in components:
                mismatches.append({'ref': ref, 'issue': 'Reference absent from PCB or schematic'})
                continue
            comp, fp = components[ref], fps[ref]
            for field, pcb_value, sch_value in [('value', fp.GetValue(), comp.findtext('value')),
                ('footprint', fp.GetFPIDAsString(), comp.findtext('footprint'))]:
                if pcb_value != sch_value:
                    mismatches.append({'ref': ref, 'field': field, 'pcb': pcb_value, 'schematic': sch_value})
        for ref, (code, mpn) in mapping.items():
            if ref in components:
                fields = {f.get('name'): f.text for f in components[ref].findall('./fields/field')}
                captured = fields.get('MPN')
                if captured and captured != mpn:
                    mismatches.append({'ref':ref, 'field':'LCSC source MPN', 'csv':mpn, 'schematic':captured})
    if {r['Designator'] for r in bom} != set(mapping):
        raise ValueError('Assembly/BOM purchased reference mismatch')
    return {'bom_rows': len(bom), 'cpl_rows': len(cpl), 'excluded': omissions,
            'comment_source': 'fresh schematic value when available; otherwise PCB value; LCSC MPN appended',
            'missing_lcsc': missing_lcsc, 'rotation_offsets': 'OPEN for all populated references; zero applied',
            'source_comparison': mismatches,
            'lcsc_references_not_on_board': sorted(set(mapping)-set(fps), key=ref_key)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', type=Path, required=True)
    parser.add_argument('pcb', type=Path)
    parser.add_argument('outdir', type=Path)
    args = parser.parse_args()
    pcb, out = args.pcb.resolve(), args.outdir.resolve()
    if not pcb.is_file() or pcb.suffix != '.kicad_pcb':
        parser.error('Input must be an existing .kicad_pcb file')
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        parser.error('Output directory must be absent or empty; existing packages are never overwritten')
    mapping = read_lcsc(LCSC)
    sources = [pcb, LCSC] + sorted(pcb.parent.glob('*.kicad_sch'))
    sources += [p for p in (pcb.with_suffix('.kicad_pro'), pcb.with_suffix('.kicad_dru')) if p.is_file()]
    before = {str(p): sha(p) for p in sources}
    board = pcbnew.LoadBoard(str(pcb))
    if board is None:
        parser.error('KiCad could not load the board')
    out.mkdir(parents=True, exist_ok=True)
    for name in ('gerbers','drill','assembly','pdf','png','render','logs','review'):
        (out/name).mkdir()
    status = out/'STATUS.txt'
    status.write_text(WARNING + '\nEXPORT INCOMPLETE\n')
    commands = []
    def run(label, argv, allowed=(0,), timeout=300):
        print(label, flush=True)
        result = subprocess.run([str(x) for x in argv], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, timeout=timeout)
        log = out/'logs'/(label+'.log')
        log.write_text(result.stdout)
        commands.append({'step':label,'argv':[str(x) for x in argv],
                         'returncode':result.returncode,'log':str(log.relative_to(out))})
        (out/'review/COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
        if result.returncode not in allowed:
            raise RuntimeError(f'{label} failed ({result.returncode}); see {log}')
        return result
    cli = args.kicad_cli
    version = run('version',[cli,'--version']).stdout.strip()
    if not version.startswith('9.'):
        raise RuntimeError('This exporter is checked for KiCad 9; got '+version)
    count = board.GetCopperLayerCount()
    copper = ['F.Cu'] + [f'In{i}.Cu' for i in range(1,count-1)] + ['B.Cu']
    layers = copper + ['F.Paste','B.Paste','F.SilkS','B.SilkS','F.Mask','B.Mask','Edge.Cuts']
    review_layers = layers + ['F.Fab','B.Fab']
    inventory = {'copper_layers':copper,'thickness_mm':pcbnew.ToMM(board.GetDesignSettings().GetBoardThickness()),
        'footprints':len(list(board.GetFootprints())),
        'tracks_and_vias':len(list(board.GetTracks())), 'zones':len(list(board.Zones())),
        'edge_graphics':sum(d.GetLayer()==pcbnew.Edge_Cuts for d in board.GetDrawings()),
        'unique_footprint_positions':len({(f.GetPosition().x,f.GetPosition().y) for f in board.GetFootprints()})}
    risks = ['JLC rotation/centroid offsets OPEN for every component; no offsets assumed verified.',
        'Electrical review findings 1–4 remain blocking; R4 fabrication release is BLOCKED.',
        'Saved copper fills match zero-error native DRC; two-layer thermal/EMI performance remains unqualified.',
        '3D model completeness, pad numbering and polarity require review; a render is not validation.',
        'TP113/114 and TP301/302 lead geometry requires differential-probe review; do not infer ideal Kelvin accuracy.',
        'Vias in capacitor/FET solder lands require reviewed tenting/fill and assembly process; no premium via process assumed.',
        'First-build landed cost below 1,000,000 VND is unverified; no purchase, quote or upload performed.']
    if count != 2:
        raise RuntimeError('Lite export requires the reviewed two-layer board')
    if inventory['edge_graphics']==0:
        risks.append('PCB has no Edge.Cuts outline; empty outline Gerber is a review artifact only.')
    if inventory['unique_footprint_positions']<=1:
        risks.append('All footprint anchors coincide; current board is unplaced and layer plots can clip at the page origin.')
    if inventory['thickness_mm'] != 1.6:
        risks.append('Actual board thickness differs from assumed 1.6 mm.')
    drc_args = [cli,'pcb','drc','--format','json','--severity-all','--exit-code-violations',
                '-o',out/'review/DRC.json']
    schematic = pcb.with_suffix('.kicad_sch')
    if schematic.is_file():
        drc_args.append('--schematic-parity')
    drc_result = run('drc',drc_args+[pcb],allowed=(0,5))
    drc = json.loads((out/'review/DRC.json').read_text())
    drc_summary = {key:len(drc.get(key,[])) for key in ('violations','unconnected_items','schematic_parity')}
    if drc_result.returncode == 5:
        raise RuntimeError('Refuse final export with DRC findings: '+json.dumps(drc_summary))
    sch_xml = None
    if schematic.is_file():
        sch_xml = out/'review/SCHEMATIC.xml'
        run('schematic-netlist',[cli,'sch','export','netlist','--format','kicadxml','-o',sch_xml,schematic])
    else:
        risks.append('No sibling schematic available; source/BOM parity remains OPEN.')
    # Absolute origin in every export. Keep X2/net attributes and Protel defaults.
    run('gerbers',[cli,'pcb','export','gerbers','--layers',','.join(layers),
        '--precision','6','--subtract-soldermask','-o',str(out/'gerbers')+'/',pcb])
    run('drill',[cli,'pcb','export','drill','--format','excellon','--drill-origin','absolute',
        '--excellon-units','mm','--excellon-zeros-format','decimal','--excellon-oval-format','alternate',
        '--excellon-separate-th','--generate-map','--map-format','pdf',
        '-o',str(out/'drill')+'/',pcb])
    raw_pos = out/'assembly/POSITIONS_KICAD.csv'
    run('positions',[cli,'pcb','export','pos','--format','csv','--units','mm','--side','both',
        '--exclude-dnp','-o',raw_pos,pcb])
    assembly = assemble(board,raw_pos,out/'assembly',mapping,sch_xml)
    if assembly['missing_lcsc']:
        risks.append(f"{len(assembly['missing_lcsc'])} assembly references have blank LCSC Part #; sourcing/assembly route OPEN.")
    if assembly['source_comparison']:
        risks.append('PCB/schematic/LCSC source differences require reconciliation; see manifest source_comparison.')
    for layer in review_layers:
        run('pdf-'+layer,[cli,'pcb','export','pdf','--layers',layer,'--mode-single',
            '--black-and-white','--drill-shape-opt','0','-o',out/'pdf'/(layer+'.pdf'),pcb])
    # Native macOS rasterization on white at 150 dpi; module cache stays in temp.
    with tempfile.TemporaryDirectory(prefix='v1a-fab-swift-cache-') as cache:
        run('layer-pngs',['/usr/bin/swift','-module-cache-path',cache,
            ROOT/'scripts/lite_pdf_to_png.swift',out/'pdf',out/'png'])
    render_help = run('render-availability',[cli,'pcb','render','--help'],allowed=(0,1,2))
    render = {'available':render_help.returncode==0,'status':'UNAVAILABLE'}
    if render['available']:
        rendered = run('render',[cli,'pcb','render','--width','1600','--height','1000',
            '--side','top','--rotate','20,0,15','--background','opaque','--quality','basic',
            '--output',out/'render/PCB_3D.png',pcb],allowed=tuple(range(-128,256)))
        render['status'] = 'EXPORTED' if rendered.returncode==0 and (out/'render/PCB_3D.png').is_file() else 'FAILED'
        render['returncode'] = rendered.returncode
    if render['status'] != 'EXPORTED':
        risks.append('3D render '+render['status']+'; see logs, no board repair or invented outline attempted.')
    files = sorted((out/'gerbers').glob('*'))
    drills = sorted((out/'drill').glob('*.drl'))
    if not files or not drills or not list((out/'drill').glob('*.pdf')):
        raise RuntimeError('Required Gerber, Excellon or drill-map exports missing')
    expected_ext = ['.gtl']+[f'.g{i}' for i in range(1,count-1)]+['.gbl','.gtp','.gbp','.gto','.gbo','.gts','.gbs','.gm1']
    for ext in expected_ext:
        if not any(p.suffix.lower()==ext for p in files):
            raise RuntimeError('Missing expected Protel Gerber layer '+ext)
    for layer in review_layers:
        for folder, ext in [('pdf','.pdf'),('png','.png')]:
            path = out/folder/(layer+ext)
            if not path.is_file() or path.stat().st_size==0:
                raise RuntimeError('Missing layer review output '+str(path))
    after = {str(p):sha(p) for p in sources}
    if before != after:
        raise RuntimeError('Input changed during export; package is inconsistent, rerun into a new directory')
    archive = out/(pcb.stem+'_GERBERS_DRILL_REVIEW_ONLY.zip')
    # Only manufacturing data plus a clear release-status notice, never maps/CPL/BOM/PDFs.
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for path in files+drills:
            z.write(path,path.name)
        z.writestr('NOT_FOR_FABRICATION.txt',WARNING+'\nReview exports only.\n'+'\n'.join(risks)+'\n')
    manifest = {'status':WARNING,'export_completed':True,'fabrication_released':False,
        'generated_utc':datetime.now(timezone.utc).isoformat(),'kicad_version':version,
        'exporter_sha256':{p.name:sha(p) for p in (ROOT/'scripts/export_lite_fab.py',ROOT/'scripts/lite_pdf_to_png.swift')},
        'input_sha256':before,'input_unchanged':True,'inventory':inventory,'gerber_layers':layers,
        'origin':'absolute; native KiCad XY; no bottom-X negation; positive CCW angle modulo 360',
        'assumed_target_stack':'2-layer / 1.6 mm / 35-35 um; thermal qualification OPEN',
        'drc':drc_summary,'assembly':assembly,'render':render,'open_risks':risks,
        'zip':archive.name,'artifacts_sha256':{str(p.relative_to(out)):sha(p)
        for p in sorted(out.rglob('*')) if p.is_file() and p != status}}
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'README.md').write_text('# V1A-Lite fabrication export review\n\n**'+WARNING+'**\n\n'
        'Export commands completed. This is not a fabrication-ready package.\n\n'
        + '\n'.join('- **OPEN:** '+r for r in risks)+'\n\n'
        'BOM and CPL use identical populated reference sets. Through-hole parts are included for assembly review. '
        'EXCLUDED.csv records board flags; blank LCSC numbers remain unresolved. '
        'D101 retains Bourns SMCJ64CA / Mouser 652-SMCJ64CA and has a blank LCSC field; it is not orderable through this JLC BOM. Through-hole assembly service and all rotations remain OPEN.\n\n'
        'Per-layer PDF/PNG views use native page coordinates; all bottom layers are unmirrored. '
        'The zip contains actual enabled copper layers, mask, silk, paste, outline, job metadata, '
        'separate PTH/NPTH Excellon files and the review-only notice. Drill maps remain outside the zip.\n\n'
        'Inspect MANIFEST.json, review/DRC.json, assembly/ROTATION_REVIEW.csv and logs. '
        'Source hashes were verified unchanged. No data was sent to JLCPCB.\n')
    status.write_text(WARNING+'\nEXPORT COMPLETE — REVIEW ONLY\n')
    print(f'Export complete: {out}\n{WARNING}',flush=True)
    for risk in risks:
        print('OPEN: '+risk,flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print('Export failed: '+str(exc),file=sys.stderr)
        sys.exit(1)
