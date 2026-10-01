"""Export the current owner section as one page. Requires PyMuPDF."""
from pathlib import Path
import re
import pymupdf

ROOT = Path(__file__).parent


def export():
    source = (ROOT / 'GATE4A_FREEZE.md').read_text()
    body = source.split('## OWNER EXPLANATION — one page\n', 1)[1].split('\n## Review item', 1)[0]
    body = re.sub(r'\*\*(.*?)\*\*', r'\1', body.strip())
    body = body.replace('→', ' to ').replace('…', '-').replace('−', '-').replace('–', '-')
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    font = Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    if not font.is_file():
        raise RuntimeError('Supply an equivalent Unicode font before exporting this report')
    page.insert_font(fontname='Report', fontfile=str(font))
    page.insert_text((42, 45), 'Gate4a-FIX2 | Owner handback', fontsize=17, fontname='Report')
    page.insert_text((42, 66), '2026-10-01  |  Analysis only  |  NOT FOR FABRICATION',
                     fontsize=9, fontname='Report', color=(.55, .12, .10))
    remaining = page.insert_textbox(pymupdf.Rect(42, 86, 553, 799), body,
                                    fontsize=10.3, lineheight=1.17, fontname='Report')
    if remaining < 0:
        raise RuntimeError(f'Owner explanation exceeds one page by {-remaining:.1f} points')
    doc.set_metadata({'title': 'Gate4a-FIX2 owner explanation',
                      'subject': 'Blocked test-board capture; no electrical validation',
                      'author': 'Edge AI Smart Power Module project'})
    doc.save(ROOT / 'OWNER_EXPLANATION.pdf', garbage=4, deflate=True)
    return remaining


if __name__ == '__main__':
    print(f'One owner page exported; {export():.1f} pt remaining')
