"""Render the review CSV and table from the authoritative proposed-change manifest."""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).parent


def render():
    rows = json.loads((ROOT / 'FREEZE_MANIFEST.json').read_text())['changes']
    csv_text = io.StringIO()
    writer = csv.DictWriter(csv_text, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    for row in rows:
        writer.writerow({**row, 'refdes': ','.join(row['refdes'])})
    table = ('# Gate4a-FIX2 required-change register\n\n'
             '**Analysis only; NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** '
             '[FIX2_RESOLUTIONS.md](FIX2_RESOLUTIONS.md) controls round-2 deltas. '
             'Earlier decisions remain in Git and [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md). '
             'New refs are capture reservations. Generated from FREEZE_MANIFEST.json.\n\n'
             '|ID / sheet / refs|Old → proposed MPN/value or wiring|Reason / governing equation|Disposition / source|\n'
             '|---|---|---|---|\n')
    for row in rows:
        cells = [f"{row['id']} / {row['sheet']} / {','.join(row['refdes'])}",
                 f"{row['old']} → {row['new_mpn']}; {row['new_value_or_connection']}",
                 f"{row['reason']}; {row['governing_equation']}",
                 f"{row['status']}; {row['source']}"]
        table += '|' + '|'.join(cell.replace('|', '\\|') for cell in cells) + '|\n'
    return {'FREEZE_BOM.csv': csv_text.getvalue(), 'FREEZE_TABLE.md': table}


if __name__ == '__main__':
    for name, content in render().items():
        (ROOT / name).write_text(content)
