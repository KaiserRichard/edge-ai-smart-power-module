#!/usr/bin/env python3
"""Finish review labels/page; no copper edits."""
from copper_v1a_lite import *
b=load()
for d in b.GetDrawings():
 if isinstance(d,p.PCB_TEXT):
  if d.GetText()=='PI OUT':d.SetPosition(v(86,34))
  if d.GetText()=='+' and p.ToMM(d.GetPosition().x)>80:d.SetPosition(v(85,52))
# Board fabricator sees a clear warning on both board drawing and package README.
save(b)
s=BOARD.read_text();s=re.sub(r'\(paper "[^"]+"[^\n]*\)', '(paper "User" 100 80)',s,count=1);BOARD.write_text(s)
