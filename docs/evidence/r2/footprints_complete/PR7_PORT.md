# PR #7 port and baseline

NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.

Read PR #7 https://github.com/KaiserRichard/edge-ai-smart-power-module/pull/7 and commit `8535cffe2151794ae352d25e19f9262a549dbc1b` log/diff and audit before editing. Its only schematic changes were ten bare-copper test-point assignments on Sheets 01/04/05. Port those individual fields into redraw `1f4c2f821793506871b9abe6227b1deba419d27e`, without replacing old sheet files or cherry-picking obsolete ERC evidence. Baseline has 154 physical components and 24 blanks (ten test pads plus fourteen other parts); additional generic J301/J302 MPNs will be made concrete. D101 stays untouched and OPEN for the TVS study. F101/L201 stay untouched.

Sheet 01: TP101/TP102 use PR #7's unmodified `TestPoint:TestPoint_Pad_D1.5mm`: copper diameter 1.5 mm, pad 1, no paste. MPN and manufacturer datasheet are not applicable to etched copper test access; do not invent a purchased component. Existing test-point values and geometry are preserved. F101/D101 are the requested exclusions.

No KiCad GUI/editor processes were present at startup (`pgrep -fl 'kicad|eeschema|pcbnew'` returned no processes). All edits use an isolated worktree and CLI.
