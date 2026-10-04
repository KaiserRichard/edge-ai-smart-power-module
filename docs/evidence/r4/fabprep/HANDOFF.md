# FAB_PREP handoff — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**STATUS: PASS for requested rule/export preparation and execution tests;
CONDITIONAL PASS for engineering handoff; fabrication release BLOCKED.**
Worked directly, without sub-agents, on `feat/v1a-fab-prep` from `5f371fd`.
No PCB/schematic/project edits, installs, uploads, logins, orders or pushes.

## Files

1. `hardware/kicad/V1A.kicad_dru` — KiCad 9 fabrication and voltage rules.
2. `docs/pcb/FAB_RULES.md` — stack assumptions, limits, sources, calculations,
   actual net mapping, 1 oz comparison and remaining review items.
3. `scripts/export_fab_package.sh` — requested two-argument entry point.
4. `scripts/export_fab_package.py` — CLI orchestration, BOM/CPL conversion,
   review status, hashes and zip assembly.
5. `scripts/fab_pdf_to_png.swift` — native macOS 150 dpi PDF rasterization.
6. `docs/pcb/EXPORT_PACKAGE.md` — usage, formats and OPEN rotation/centroid issues.
7. `third_party/fabprep/SOURCES.md` — URLs, access dates, revisions and attribution.
8. `docs/evidence/r4/fabprep/NET_RULE_TARGETS.json` — fresh schematic connections.
9. `docs/evidence/r4/fabprep/check_rules.py` — isolated native rule probes.
10. `docs/evidence/r4/fabprep/RULE_CHECK.json` — 95 probe results and board DRC summary.
11. `docs/evidence/r4/fabprep/check_exports.py` — synthetic four-layer/export regression.
12. `docs/evidence/r4/fabprep/EXPORT_CHECK.json` — final current-board smoke evidence,
    artifact hashes, zip/CSV checks and four-layer fixture results.
13. `docs/evidence/r4/fabprep/HANDOFF.md` — this handoff and Git result.
14. `docs/FINAL_MANAGER_REPORT.md` — appended rules/export checkpoint reports.

Generated fabrication/visual files stay in the temporary output directories;
only intentional engineering evidence is retained in the repository.

## Test result

**EVIDENCE:** installed KiCad **9.0.6**. Native custom-rule probes: **95/95 PASS**,
including all four copper layers and both A/B object orders. Current-board
DRC reads the rules but reports **2,191 violations, 213 unconnected items**.
Exporter DRC additionally checks schematic parity and finds **one mismatch**:
PCB R203 = 24.4k versus current schematic R203 = 24.6k. Hardware remains unchanged;
the exported BOM uses the current schematic's 24.6k value and records the mismatch.

Final command, **exit 0**:

```sh
scripts/export_fab_package.sh hardware/kicad/V1A.kicad_pcb '/tmp/v1a fabprep final'
```

Resolved output: `/private/tmp/v1a fabprep final/`.

| Artifact | Result |
|---|---|
| Gerbers | 9 actual-board layers + job metadata; X2, Protel names, 4.6 mm coordinates |
| Drills | 2 Excellon files (PTH/NPTH) + 2 PDF maps |
| JLC BOM / CPL | 351 identical populated reference sets; exact requested headers |
| LCSC mapping | 181 exact mapped references; 170 blank/unmapped, explicitly OPEN |
| Population exclusions | 15 references, individually documented |
| Layer review | 11 PDFs + 11 PNGs at 150 dpi, including F.Fab/B.Fab |
| 3D | CLI render succeeded; PNG retained |
| Zip | 13 members including review-only notice; CRC and all artifact hashes checked |
| Source preservation | PCB, project, all six schematics, custom rules and procurement CSV unchanged during export |

**EVIDENCE:** synthetic four-layer fixture also passes: G1/G2 inner Gerbers,
13 PDF/PNG pairs, render, populated BOM=CPL, exclusions, known/blank LCSC codes,
top/bottom native positions and angles, absolute origin despite a nonzero
auxiliary origin, no bottom-X negation, zip integrity, unchanged input and
rejection of nonempty output directories. The final assembly implementation
was also checked against all four fixture CSVs byte-for-byte.
Fixture output path and manifest hash are in `EXPORT_CHECK.json`.

**VISUAL OBSERVATION:** current-board F.Cu/B.Cu/F.SilkS plots show the origin pile
clipped by the page; native 3D shows coincident footprints and an automatically
displayed substrate despite no Edge.Cuts. The separate fixture renders spaced
pads on its synthetic rectangular outline. These are export checks only;
no actual layout or assembly acceptance is implied. Final BOM-only correction
leaves all reviewed source geometry unchanged.

## OPEN handoff items

- Actual PCB is still a **two-layer**, unplaced, unrouted import without outline
  or zones. Layout worker must implement/review the intended four-layer,
  1.6 mm, 70/35/35/70 µm stack.
- Reconcile R203 into the PCB in the layout worker's authorized scope.
- Review conservative voltage clearances at fine-pitch packages; resolve DRC
  without blanket waivers. Surge/driver peaks, reverse faults and source/fuse/
  TVS coordination remain engineering questions.
- Confirm exact stack, copper/current/thermal limits, zone fills, mask/slots,
  footprints/polarity, Gerber CAM interpretation and all prior gate blockers.
- Resolve all 170 missing LCSC routes and manual/THT/mechanical assembly scope.
- **JLC rotation offsets and centroids are OPEN for every part.** Zero offsets
  were applied; JLC per-part library/placement preview was not accessed.
- Follow the established current-limited/dummy-load bring-up gates before SBC use.

No R2/R3/R4 gate is closed by these artifacts.

## Git

The brief explicitly authorizes one local commit per step and no push.
Step 1 staging failed with:

```text
fatal: Unable to create '/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-fabprep/index.lock': Operation not permitted
```

Per the brief, leave that step uncommitted. No alternate index, permission
change or lock workaround was attempted. Step 2 commit result is recorded below.

**Step 2 result:** authorized staging again failed with the same `index.lock`
`Operation not permitted` error (exit 128). Both steps remain uncommitted.
Branch/HEAD remain `feat/v1a-fab-prep` / `5f371fd`. No push.
