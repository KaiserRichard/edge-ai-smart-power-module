# Start here: V1A-Lite hand-routing practice

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

This branch is your practice copy. The reviewed board is on `feat/v1a-lite-cost-reduction`. “Reviewed” does not mean released for fabrication or electrically validated.

## 1. Open your practice project

Run in a terminal:

```sh
cd /Users/quockaiser/Desktop/Research/wt-handroute
git status --short
git switch learn/v1a-lite-hand-route
git branch --show-current
open hardware/kicad/V1A.kicad_pro
```

If Git reports conflicting local changes, preserve them before switching. Do not use a forced switch or reset. In KiCad Project Manager, open the schematic or PCB by double-clicking its file.

**KNOWN:** the practice starting commit is `ee31d04ecba90d29bc69620b0de4659958434001`. It contains the FIX2 board, after the R2 review. The starting PCB SHA256 is `01e7046e4072d0dfcc3dd750141c8a14cbf554cbbac3dc0db5ca3a1d246d1066`. Coordinates in these guides refer to that board; they change when you move parts.

## 2. Choose your lesson

1. Read [Schematic editing](V1A_LITE_SCHEMATIC_EDITING.md) before changing connections, part values, footprints or sourcing fields.
2. Follow [PCB placement and hand routing](V1A_LITE_PCB_GUIDE.md) for the physical layout.
3. Work on one small block, check it, and save a named practice checkpoint. Keep new evidence under a new `docs/evidence/handroute/` session folder. Do not overwrite earlier review evidence.
4. Keep the project, child sheets, local libraries, `.kicad_pro` and `.kicad_dru` together. A PCB file alone does not carry all project rules.

**KNOWN:** this guide-writing task changed documentation only. It did not edit KiCad files or buy anything. The guides describe actions for you to practise later.

**OPEN:** continuous current, temperatures, fault protection, electrical spacing, harness and populated mechanical fit still need qualification. Practice does not advance R2–R5 or authorize fabrication. At a future gate review, update `docs/FINAL_MANAGER_REPORT.md` with status, work, evidence, decisions, open risks and next gate.
