#!/usr/bin/env python3
"""Import the current schematic into an unplaced KiCad 9 board, or verify it.

Run using KiCad's bundled Python (pcbnew required). This is an XML-netlist
equivalent of the initial Update PCB from Schematic transfer, not placement.
Existing boards are verified only, so this cannot overwrite an owner's layout.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import pcbnew
from make_schematic_readable import nodes, one, parse, prop, val

ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / 'hardware/kicad'
EV = ROOT / 'docs/evidence/r3/layout_prep'
BOARD = CAD / 'V1A.kicad_pcb'
PROJECT = CAD / 'V1A.kicad_pro'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dimensions(netclass):
    return {key: pcbnew.ToMM(getattr(netclass, method)()) for key, method in [
        ('track_width', 'GetTrackWidth'), ('clearance', 'GetClearance'),
        ('via_diameter', 'GetViaDiameter'), ('via_drill', 'GetViaDrill'),
        ('microvia_diameter', 'GetuViaDiameter'), ('microvia_drill', 'GetuViaDrill')]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', required=True, type=Path)
    parser.add_argument('--footprints', required=True, type=Path,
                        help='Installed KiCad standard footprint directory')
    parser.add_argument('--evidence-dir', type=Path, default=EV,
                        help='Output directory; use a new directory to retain earlier evidence')
    args = parser.parse_args()
    evidence = args.evidence_dir
    evidence.mkdir(parents=True, exist_ok=True)
    original_project = PROJECT.read_bytes()
    netlist = evidence / 'fresh.xml'
    result = subprocess.run([str(args.kicad_cli), 'sch', 'export', 'netlist',
                             '--format', 'kicadxml', '-o', str(netlist),
                             str(CAD / 'V1A.kicad_sch')], capture_output=True, text=True)
    (evidence / 'netlist_export.log').write_text(result.stdout + result.stderr)
    result.check_returncode()
    root = ET.parse(netlist).getroot()
    components = {c.get('ref'): c for c in root.findall('./components/comp')}
    nets = {n.get('name'): n for n in root.findall('./nets/net')}
    node_nets = {(n.get('ref'), n.get('pin')): (name, n)
                 for name, net in nets.items() for n in net.findall('node')}
    root_uuid = re.search(r'\(uuid "([^"]+)"\)',
                          (CAD / 'V1A.kicad_sch').read_text())[1]
    attributes = {}
    for path in CAD.glob('*.kicad_sch'):
        for symbol in nodes(parse(path.read_text()), 'symbol'):
            ref = val(prop(symbol, 'Reference')[2])
            attributes[ref] = {'exclude_bom': one(symbol, 'in_bom')[1] == 'no',
                               'dnp': one(symbol, 'dnp')[1] == 'yes'}
    project = json.loads(original_project)
    rules = {c['name']: c for c in project['net_settings']['classes']}
    assignments = {p['pattern']: p['netclass']
                   for p in project['net_settings']['netclass_patterns']}
    named_nets = {n for n in nets if not n.startswith('unconnected-')}
    assert named_nets == set(assignments), 'Project assignment coverage differs from fresh schematic'
    manager = pcbnew.GetSettingsManager()
    source_libraries = {}
    paths = {}
    for ref, c in components.items():
        paths[ref] = '/' + root_uuid + c.find('sheetpath').get('tstamps') + c.findtext('tstamps')
        library, item = c.findtext('footprint').split(':', 1)
        base = CAD / 'V1A_Qualified.pretty' if library == 'V1A_Qualified' else args.footprints / (library + '.pretty')
        source = base / (item + '.kicad_mod')
        assert source.is_file(), f'Missing footprint: {source}'
        source_libraries[c.findtext('footprint')] = {'path': str(source), 'sha256': sha(source)}

    created = not BOARD.exists()
    if created:
        # KiCad 9.0.6's SetProject on a freshly constructed BOARD can crash;
        # round-trip an empty board first to initialize its design settings.
        with tempfile.TemporaryDirectory(prefix='v1a-layoutprep-') as tmp:
            seed = Path(tmp) / 'empty.kicad_pcb'
            assert pcbnew.SaveBoard(str(seed), pcbnew.BOARD(), True)
            board = pcbnew.LoadBoard(str(seed))
        assert manager.LoadProject(str(PROJECT))
        board.SetProject(manager.GetProject(str(PROJECT)))
        board.SetFileName(str(BOARD))
        title = board.GetTitleBlock()
        title.SetTitle('V1A schematic import only — all footprints unplaced')
        title.SetComment(0, 'NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED')
        board.SetTitleBlock(title)
        board_nets = {}
        for name in nets:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
            board_nets[name] = net
        for ref, c in components.items():
            lib_id = c.findtext('footprint')
            library, item = lib_id.split(':', 1)
            fp = pcbnew.FootprintLoad(str(Path(source_libraries[lib_id]['path']).parent), item)
            assert fp is not None, lib_id
            fp.SetFPID(pcbnew.LIB_ID(library, item))
            fp.SetReference(ref)
            fp.SetValue(c.findtext('value'))
            fp.SetExcludedFromBOM(attributes[ref]['exclude_bom'])
            fp.SetDNP(attributes[ref]['dnp'])
            fp.SetPath(pcbnew.KIID_PATH(paths[ref]))
            props = {p.get('name'): p.get('value') for p in c.findall('property')}
            fp.SetSheetname(props['Sheetname'])
            fp.SetSheetfile(props['Sheetfile'])
            for field in c.findall('./fields/field'):
                name, value = field.get('name'), field.text or ''
                if name == 'Footprint':
                    continue
                existing = fp.GetFieldByName(name)
                if existing is None:
                    existing = pcbnew.PCB_FIELD(fp, fp.GetNextFieldId(), name)
                    existing.SetText(value)
                    existing.SetVisible(False)
                    fp.AddField(existing)
                else:
                    existing.SetText(value)
            fp.SetIsPlaced(False)
            fp.SetNeedsPlaced(True)
            # Intentionally retain each library's origin and orientation.
            assert fp.GetPosition() == pcbnew.VECTOR2I(0, 0)
            board.Add(fp)
            for pad in fp.Pads():
                if not pad.GetNumber():
                    continue  # unnumbered paste apertures are not copper pins
                name, node = node_nets[(ref, pad.GetNumber())]
                pad.SetNet(board_nets[name])
                pad.SetPinFunction(node.get('pinfunction', ''))
                pad.SetPinType(node.get('pintype', ''))
        board.SynchronizeNetsAndNetClasses(False)
        # True is essential: SaveBoard otherwise rewrites project settings.
        assert pcbnew.SaveBoard(str(BOARD), board, True)

    board = pcbnew.LoadBoard(str(BOARD))
    assert manager.LoadProject(str(PROJECT))
    board.SetProject(manager.GetProject(str(PROJECT)))
    board.SynchronizeNetsAndNetClasses(False)
    fps = {f.GetReference(): f for f in board.GetFootprints()}
    assert set(fps) == set(components), 'Board reference set differs from schematic'
    checked_pads = 0
    for ref, fp in fps.items():
        c = components[ref]
        assert fp.GetValue() == c.findtext('value'), ref
        assert fp.IsExcludedFromBOM() == attributes[ref]['exclude_bom'], ref
        assert fp.IsDNP() == attributes[ref]['dnp'], ref
        assert fp.GetFPID().GetUniStringLibId() == c.findtext('footprint'), ref
        assert fp.GetPath().AsString() == paths[ref], (ref, fp.GetPath().AsString(), paths[ref])
        actual_pins = set()
        for pad in fp.Pads():
            if pad.GetNumber():
                actual_pins.add(pad.GetNumber())
                assert pad.GetNetname() == node_nets[(ref, pad.GetNumber())][0], (ref, pad.GetNumber())
                checked_pads += 1
        assert actual_pins == {pin for r, pin in node_nets if r == ref}, ref
        assert fp.GetPosition() == pcbnew.VECTOR2I(0, 0), 'Existing board has placement; stop'
        assert fp.GetOrientationDegrees() == 0 and not fp.IsPlaced(), ref
    assert not list(board.GetTracks()) and not list(board.Zones()) and not list(board.GetDrawings())
    actual_classes = {str(k): dimensions(v) for k, v in board.GetAllNetClasses().items()}
    assert set(actual_classes) == set(rules), (actual_classes, rules)
    for name, dims in actual_classes.items():
        assert all(abs(value - rules[name][key]) < 1e-9 for key, value in dims.items()), name
    resolved = {}
    for name in named_nets:
        net = board.FindNet(name)
        cls = net.GetNetClassSlow()
        assert cls.GetName() == assignments[name], (name, cls.GetName(), assignments[name])
        assert dimensions(cls) == actual_classes[assignments[name]], name
        resolved[name] = assignments[name]
    assert PROJECT.read_bytes() == original_project, 'Project unexpectedly changed'
    report = {
        'status': 'PASS: import connectivity, schematic UUID paths and board-resolved net classes',
        'scope': 'Unplaced import only; no R3 layout or fabrication release',
        'kicad_version': pcbnew.GetBuildVersion(),
        'schematic_baseline': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'footprints': len(fps), 'numbered_pads_checked': checked_pads,
        'nets_including_no_connects': len(nets), 'named_nets': len(named_nets),
        'class_counts': dict(Counter(resolved.values())), 'classes_mm': actual_classes,
        'resolved_named_nets': dict(sorted(resolved.items())),
        'placement': 'All footprint anchors at (0,0), 0 degrees; none marked placed',
        'tracks_and_vias': 0, 'zones': 0, 'board_drawings_and_outline': 0,
        'project_changed': False, 'project_sha256': sha(PROJECT), 'board_sha256': sha(BOARD),
        'schematic_sha256': {p.name: sha(p) for p in sorted(CAD.glob('*.kicad_sch'))},
        'netlist_sha256': sha(netlist), 'footprint_sources': source_libraries,
    }
    (evidence / 'IMPORT_CHECK.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{"Created" if created else "Verified"} {len(fps)} unplaced footprints; '
          f'{checked_pads} numbered pads; {len(named_nets)} named nets; all {len(rules)} classes match.')


if __name__ == '__main__':
    main()
