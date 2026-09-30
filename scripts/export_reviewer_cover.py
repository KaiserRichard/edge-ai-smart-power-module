#!/usr/bin/env python3
"""Render the one-page reviewer note as a standalone A4 PDF with PyMuPDF."""
import html
from pathlib import Path
import re
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/evidence/r2/sheet03'

def inline(text):
    text=html.escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    text=re.sub(r'`(.+?)`',r'<code>\1</code>',text)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',text)

def main():
    source=(OUT/'REVIEWER_COVER_NOTE.md').read_text()
    chunks=[];kind=None
    for block in source.strip().split('\n\n'):
        lines=block.splitlines()
        if lines[0].startswith('# '):chunks.append('<h1>'+inline(lines[0][2:])+'</h1>')
        elif lines[0].startswith('- '):chunks.append('<ul>'+''.join('<li>'+inline(l[2:])+'</li>' for l in lines)+'</ul>')
        elif re.match(r'\d+\. ',lines[0]):chunks.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',l))+'</li>' for l in lines)+'</ol>')
        else:chunks.append('<p>'+inline(' '.join(lines))+'</p>')
    css='body {font-family: sans-serif; font-size: 10pt; line-height: 1.25; color: #17202a;} h1 {font-size: 16pt; margin-bottom: 10pt;} p {margin: 8pt 0;} li {margin-bottom: 6pt;} ul,ol {padding-left: 17pt; margin: 8pt 0;} a {color: #244f7a;} code {font-size: 8pt;}'
    story=pymupdf.Story(html=''.join(chunks),user_css=css)
    pdf=OUT/'REVIEWER_COVER_NOTE.pdf'
    writer=pymupdf.DocumentWriter(str(pdf))
    rect=pymupdf.paper_rect('a4');content=rect+ (42,38,-42,-38)
    device=writer.begin_page(rect);more,_=story.place(content);story.draw(device);writer.end_page();writer.close()
    if more:raise RuntimeError('Cover note exceeds one page; shorten or adjust formatting')
    doc=pymupdf.open(pdf);assert len(doc)==1
    text=doc[0].get_text()
    for s in ['307','300','125','95','768','89.5','2.98','NOT FOR FABRICATION']:assert s in text,s
    uri=re.search(r'\[Detailed findings and assumptions\]\(([^)]+)\)',source).group(1)
    for box in doc[0].search_for('Detailed findings and assumptions'):
        doc[0].insert_link({'kind':pymupdf.LINK_URI,'from':box,'uri':uri})
    doc.saveIncr()
    print(f'{pdf}: 1 page, required numbers/warning present')

if __name__=='__main__':main()
