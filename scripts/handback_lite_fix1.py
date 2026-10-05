#!/usr/bin/env python3
"""Read-only FIX1 handback audit and conditional thermal mitigation screen.

Run with KiCad's bundled Python. Never edits CAD or claims release approval.
"""
import csv
import hashlib
import json
import math
import zipfile
from pathlib import Path

import pcbnew as p

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'docs/evidence/v1a_lite'
F = E / 'fix1'
BOARD = ROOT / 'hardware/kicad/V1A.kicad_pcb'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, data):
    (F / name).write_text(json.dumps(data, indent=2) + '\n')


def xy(point):
    return [p.ToMM(point.x), p.ToMM(point.y)]


def audit():
    board = p.LoadBoard(str(BOARD))
    refs = {f.GetReference(): f for f in board.GetFootprints()}
    selected = ['J501', 'J502', 'J503', 'Q101', 'Q102', 'U201', 'R204',
                'C205', 'C206', 'R202', 'R203', 'R205', 'C207', 'SCR301',
                'C217', 'C218', 'C209', 'C214', 'R308', 'L201', 'F301',
                'U301', 'R303', 'R304']
    selected += sorted(r for r in refs if r.startswith('TP'))
    result = {'board_sha256': sha(BOARD), 'layers': board.GetCopperLayerCount(),
              'footprints': {}, 'control_tracks': {}, 'board_silk': [],
              'L2_zone_nets': [], 'L2_signal_tracks': []}
    for ref in selected:
        f = refs[ref]
        result['footprints'][ref] = {
            'position_mm': xy(f.GetPosition()), 'angle_deg': f.GetOrientationDegrees(),
            'layer': board.GetLayerName(f.GetLayer()),
            'pads': [{'number': q.GetNumber(), 'net': q.GetNetname(),
                      'position_mm': xy(q.GetPosition())} for q in f.Pads()]}
    for t in board.GetTracks():
        if not isinstance(t, p.PCB_VIA) and t.GetLayer() == p.In1_Cu:
            result['L2_signal_tracks'].append(t.GetNetname())
        if any(t.GetNetname().endswith('/' + n) for n in
               ['BUCK_RBOOT', 'BUCK_CBOOT', 'BUCK_VCC', 'BUCK_FB', 'SCR_GATE']):
            result['control_tracks'].setdefault(t.GetNetname(), []).append({
                'via': isinstance(t, p.PCB_VIA), 'start': xy(t.GetStart()),
                'end': xy(t.GetEnd()), 'width_mm': p.ToMM(t.GetWidth(p.F_Cu) if isinstance(t, p.PCB_VIA) else t.GetWidth()),
                'layer': board.GetLayerName(t.GetLayer())})
    for z in board.Zones():
        if not z.GetIsRuleArea() and z.GetLayer() == p.In1_Cu:
            result['L2_zone_nets'].append(z.GetNetname())
    for t in board.GetDrawings():
        if isinstance(t, p.PCB_TEXT) and t.GetLayer() in [p.F_SilkS, p.B_SilkS]:
            result['board_silk'].append({'text': t.GetText(), 'pos': xy(t.GetPosition()),
                'size_mm': xy(t.GetTextSize()), 'stroke_mm': p.ToMM(t.GetTextThickness())})
    assert result['layers'] == 4
    assert set(result['L2_zone_nets']) == {'/GND'}
    assert not result['L2_signal_tracks']
    assert all(min(t['size_mm']) >= 1 and t['stroke_mm'] >= .15 for t in result['board_silk'])
    write('HANDBACK_BOARD_AUDIT.json', result)
    with (F / 'PROBE_MAP.csv').open('w', newline='') as stream:
        w = csv.writer(stream)
        w.writerow(['Reference', 'Net', 'X_mm', 'Y_mm', 'Side', 'Use'])
        for ref in sorted(r for r in refs if r.startswith('TP')):
            f = refs[ref]
            q = next(iter(f.Pads()))
            use = 'Rated differential probe' if ref in ['TP113', 'TP114'] else 'See BENCH_TESTS.md'
            w.writerow([ref, q.GetNetname(), *xy(q.GetPosition()),
                        'bottom' if f.IsFlipped() else 'top', use])
    return result


def mitigation():
    thermal = json.loads((F / 'THERMAL_SCREEN.json').read_text())
    assert thermal['board_sha256'] == sha(BOARD)
    r = .58
    scenarios = []
    for case in thermal['scenarios']:
        # Stored columns are responses to each unit source, not rows.
        columns = case['source_to_board_K_W_columns']
        matrix = [[columns[j][i] for j in range(3)] for i in range(3)]
        for i, resistance in enumerate([1.4, 1.4, 19.2]):
            matrix[i][i] += resistance
        rows = []
        for output in [1, 2, 3, 5]:
            pout = (1 + 100 / 24.6) * output
            current = (18 - math.sqrt(18**2 - 8*r*pout/.9)) / (4*r)
            fet = current**2 * r
            # Conditional loss ceiling: actual U201 loss must be measured/bounded.
            umax = min((60 - fet * (row[0] + row[1])) / row[2] for row in matrix)
            power = [fet, fet, .75]
            tj = [50 + sum(a*b for a, b in zip(row, power)) for row in matrix]
            rows.append({'output_A': output, 'input_A_assumed_90pct_buck_efficiency': current,
                         'loss_W_per_FET_at_0.58ohm': fet,
                         'U201_max_loss_W_for_all_junctions_at_most_110C': umax,
                         'U201_loss_W_assumed_for_bench_screen': .75,
                         'conditional_junction_C': tj,
                         'conditional_status': 'PASS' if max(tj) <= 110 else 'FAIL'})
        scenarios.append({'h_W_m2K_assumed': case['h'], 'load_scenarios': rows,
                          'five_A_junction_rise_K': [t-50 for t in case['junction_C_estimate']],
                          'U201_C_with_zero_FET_heat_and_2.417W': 50 + matrix[2][2]*2.417})
    result = {'board_sha256': sha(BOARD), 'classification': 'CALCULATED / ASSUMED; bench proposal only',
              'ambient_C_assumed': 50, 'junction_screen_C_assumed': 110,
              'scenarios': scenarios,
              'proposal': 'After engineering approval, start no-load then low-load dummy testing; provisional ceiling 2 A only if U201 loss <=0.75 W and reviewed temperatures/uncertainty pass. No new product current rating.',
              'limitations': ['Fixed 0.58 ohm requires adequate gate drive and temperature <=150C',
                             'Buck efficiency 90% is assumed, not a guaranteed low-load bound',
                             '0.75 W U201 loss is a proposed acceptance allocation, not a predicted loss',
                             'Other component heat and the coarse thermal model require bench calibration',
                             'No FET substitution or schematic change; lower FET resistance alone cannot fix U201 self-heating at the inherited 2.417 W screen']}
    write('THERMAL_MITIGATION.json', result)
    return result


def package():
    fab = E / 'fab'
    manifest = json.loads((fab / 'MANIFEST.json').read_text())
    checks = []
    def check(name, condition):
        checks.append({'check': name, 'pass': bool(condition)})
    for name, expected in manifest['input_sha256'].items():
        check('input ' + name, sha(Path(name)) == expected)
    for name, expected in manifest['artifacts_sha256'].items():
        check('artifact ' + name, sha(fab / name) == expected)
    for name, expected in manifest['exporter_sha256'].items():
        check('exporter ' + name, sha(ROOT / 'scripts' / name) == expected)
    for name, key in [('COPPER_GEOMETRY.json', 'sha256'),
                      ('COPPER_RESISTANCE_0.1.json', 'geometry_board_sha256'),
                      ('THERMAL_SCREEN.json', 'board_sha256'),
                      ('VOLTAGE_BUDGET.json', 'board_sha256')]:
        check('calculation board identity ' + name,
              json.loads((F / name).read_text())[key] == sha(BOARD))
    with zipfile.ZipFile(fab / manifest['zip']) as archive:
        loose = list((fab / 'gerbers').glob('*')) + list((fab / 'drill').glob('*.drl'))
        check('ZIP exact member set', set(archive.namelist()) ==
              {x.name for x in loose} | {'NOT_FOR_FABRICATION.txt'})
        check('ZIP bytes match loose manufacturing files',
              all(archive.read(x.name) == x.read_bytes() for x in loose))
    def rows(name):
        with (fab / 'assembly' / name).open() as f:
            return list(csv.DictReader(f))
    bom, cpl = rows('BOM_JLC.csv'), rows('CPL_JLC.csv')
    check('100 BOM/CPL refs', len(bom) == len(cpl) == 100 and
          {x['Designator'] for x in bom} == {x['Designator'] for x in cpl})
    smt = rows('CPL_JLC_SMT_REVIEW.csv')
    manual = {'C101','D101','SCR301','C217','C218','J501','J502'}
    check('93 SMT refs, seven manual parts excluded', len(smt) == 93 and
          not ({x['Designator'] for x in smt} & manual))
    check('seven manual refs exact', {x['Designator'] for x in rows('MANUAL_ASSEMBLY.csv')} == manual)
    for path in [fab / 'review/DRC.json', F / 'HANDBACK_DRC.json']:
        drc = json.loads(path.read_text())
        check(str(path.relative_to(E)), all(not drc[k] for k in
                                           ['violations','unconnected_items','schematic_parity']))
    check('ERC zero', 'ERC messages: 0' in (F / 'HANDBACK_ERC.rpt').read_text())
    result = {'board_sha256': sha(BOARD), 'fabrication_released': False,
              'checks': checks, 'all_pass': all(x['pass'] for x in checks)}
    write('PACKAGE_VERIFICATION.json', result)
    assert result['all_pass'], [c for c in checks if not c['pass']]
    return result


if __name__ == '__main__':
    audit()
    mitigation()
    result = package()
    print('Read-only board audit, thermal proposal, probe map and', len(result['checks']), 'package checks complete.')
