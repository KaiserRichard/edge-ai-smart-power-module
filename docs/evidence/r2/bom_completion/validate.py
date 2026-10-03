#!/usr/bin/env python3
"""Audit BOM documentation against pinned Git sources; never modify native CAD."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
FREEZE = '47c7c072e1bf3d984dca79f112e953500f21ab26'
J502 = '41cb9e889418d50d2f5f24467e66ac7f15a90476'
BASE = 'c7f0a159f794e581f2901dabc57eaba12dcec403'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def source(commit, path):
    return git('show', f'{commit}:{path}').decode()


rows = list(csv.DictReader((HERE.parent / 'BOM_DRAFT.csv').open()))
md = (HERE.parent / 'BOM_DRAFT.md').read_text()
assert len({r['row_id'] for r in rows}) == len(rows)
assert all(None not in r and all(v is not None for v in r.values()) for r in rows)
named = [r for r in rows if r['row_id'][0] in 'BHA']
board = [r for r in rows if r['scope'] == 'board proposed']
assert len({r['mpn'] for r in named}) == len(named)
refs = {}
for r in rows:
    if r['row_id'][0] not in 'BNTO' or r['refdes'] == 'FAULT_TRIGGER':
        continue
    names = r['refdes'].split(', ')
    if r in board:
        assert len(names) == int(r['qty_per_board']), r['row_id']
    for ref in names:
        assert ref not in refs, ref
        refs[ref] = r
inventory = list(csv.DictReader(io.StringIO(source(BASE, 'docs/evidence/r2/footprints_complete/FULL_INVENTORY.csv'))))
freeze = list(csv.DictReader(io.StringIO(source(FREEZE, 'docs/evidence/r2/gate4a/FREEZE_BOM.csv'))))
passives = list(csv.DictReader(io.StringIO(source(FREEZE, 'docs/evidence/r2/gate4a/PASSIVE_COMPLETION.csv'))))
expected = {r['Refdes'] for r in inventory}
for r in freeze:
    expected.update(re.findall(r'\b(?:[CRDLQUFJ]|JP|TP)\d{3}\b', r['refdes']))
expected.update(['TP405', 'TP406'])  # S04-02 connection text, not its refdes column.
assert set(refs) == expected, (set(refs) - expected, expected - set(refs))
for r in passives:
    assert refs[r['refdes']]['mpn'] == r['new_mpn'], r['refdes']
    assert 'per Gate 4a freeze' in refs[r['refdes']]['choice_source']
by_freeze = {r['id']: r for r in freeze}
for r in board:
    for sid in set(re.findall(r'S\d\d-\d\d', r['choice_source'])):
        s = by_freeze[sid]
        candidate = r['mpn'].replace('EEU-FR', 'EEUFR')
        assert candidate in s['new_mpn'] or candidate in s['old'], (r['row_id'], sid)
critical = {
    'D101': 'SMCJ36CA', 'F101': '3403.0285.23', 'L201': '74437636351002',
    'D102': 'STPS60H100CT', 'D330': 'STPS60H100CT', 'D331': 'STPS60H100CT',
    'U319': 'SN74AHCT1G125DBVR', 'U324': 'SN74AHCT1G125DBVR',
    'U325': 'SN74LVC1G17DBVR', 'U326': 'SN74LVC1G17DBVR',
    'R301': 'TNPW06039K88BEEA', 'R305': 'TNPW12062M00BEEA',
    'R103': 'TNPW0805348KBEEA', 'R340': 'TNPW08051M00BEEA',
    'R361': 'TNPW060368K1BEEA', 'R362': 'TNPW0603249KBEEA',
    'R373': 'TNPW06031K00BEEA', 'C301': 'GRM21BR71E105KA99L',
    'C302': 'GRM21BR71E475KA73L', 'C350': 'C1608C0G1H103J080AA',
    'J502': '1776508', 'JP201': 'OPEN', 'JP501': 'OPEN',
}
critical.update({f'R{i}': 'WFMB2512R0330FEA' for i in [380,381,382,383,386,387,388,389,390,391,392,393]})
for ref, mpn in critical.items():
    assert refs[ref]['mpn'] == mpn, ref
earlier = list(csv.DictReader(io.StringIO(source('7904d82', 'docs/evidence/r2/BOM_DRAFT.csv'))))
earlier_refs = {ref:r for r in earlier if r['scope'].startswith('board') for ref in r['refdes'].split(', ')}
resolved = [ref for ref,r in earlier_refs.items() if r['mpn']=='OPEN' and refs[ref]['mpn']!='OPEN']
added_fitted = set(refs) - set(earlier_refs)
added_fitted = [ref for ref in added_fitted if refs[ref] in board]
assert len(resolved) == 42 and len(added_fitted) == 32
assert {r['refdes'] for r in rows if r['row_id'][0] == 'N'} == {'R314', 'R315', 'U307'}
assert all(r['qty_per_board'] == '0' for r in rows if r['row_id'][0] in 'NT')
harness = {'H01': ('1777989','1'), 'H05': ('3-87456-6','1'), 'H06': ('87309-9','10'),
           'H07': ('8521 002100','0.075'), 'H08': ('8521 010100','0.075'),
           'H09': ('8502 002100','0.030'), 'H10': ('8502 010100','0.280'),
           'A01': ('42819-2213','1'), 'A02': ('42816-0212','1'), 'A03': ('42815-0042','2')}
j502_text = source(J502, 'docs/evidence/r2/J502_SELECTION.md')
for r in named:
    if r['row_id'] in harness:
        assert (r['mpn'], r['qty_per_board']) == harness[r['row_id']]
        assert r['mpn'] in j502_text and 'per J502 selection' in r['choice_source']
    line = next(l for l in md.splitlines() if l.startswith('| ' + r['row_id'] + ' |'))
    cells = [s.strip() for s in re.split(r'(?<!\\)\|', line)[1:-1]]
    for idx, key in enumerate(['row_id','refdes','qty_per_board','quantity_unit','mpn','manufacturer','description','package_footprint','choice_source']):
        assert cells[idx] == r[key].replace('|', '\\|'), (r['row_id'], key)
    for idx, d in enumerate(['mouser','digikey','lcsc'], 9):
        p = r[d + '_unit_price_q10_usd']
        price = p if p in ('OPEN','N/A') else '$' + p
        assert cells[idx].split(' [')[0] == f"{price} / {r[d+'_stock']} / {r[d+'_lifecycle']}"
        if p not in ('OPEN','N/A'):
            assert float(p) >= 0 and r[d+'_url'].startswith('http')
            assert 0 < float(r[d+'_price_break_used']) <= 10
            assert r[d+'_minimum_order'] == 'OPEN' or float(r[d+'_minimum_order']) <= 10
    assert cells[12] == r['flags']
native_hashes = {}
for path in git('ls-tree', '-r', '--name-only', BASE, 'hardware').decode().splitlines():
    content = (ROOT / path).read_bytes()
    assert content == git('show', f'{BASE}:{path}'), path
    native_hashes[path] = hashlib.sha256(content).hexdigest()
assert not git('ls-files', '--others', '--exclude-standard', 'hardware').strip()
report = {
    'status': 'PASS — documentation consistency only; engineering/procurement remain BLOCKED',
    'freeze_commit': FREEZE, 'j502_commit': J502, 'resume_commit': BASE,
    'bom_csv_sha256': hashlib.sha256((HERE.parent/'BOM_DRAFT.csv').read_bytes()).hexdigest(),
    'bom_md_sha256': hashlib.sha256((HERE.parent/'BOM_DRAFT.md').read_bytes()).hexdigest(),
    'csv_rows': len(rows), 'named_board_mpns': len(board),
    'named_fitted_components': sum(int(r['qty_per_board']) for r in board),
    'distinct_board_fixture_pad_refs': len(refs), 'original_refs_accounted_for': len(inventory),
    'passive_source_mappings_checked': len(passives), 'critical_mappings_checked': len(critical),
    'earlier_open_positions_resolved': len(resolved), 'fitted_refs_added_to_earlier_draft': len(added_fitted),
    'assigned_open_mpns': [ref for ref,r in refs.items() if r['mpn']=='OPEN'],
    'unquantified_open_functions': [r['refdes'] for r in rows if r['scope']=='unquantified circuit / unresolved'],
    'native_hardware_files_unchanged': len(native_hashes), 'native_hardware_sha256': native_hashes,
}
(HERE / 'VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k!='native_hardware_sha256'}, indent=2))
