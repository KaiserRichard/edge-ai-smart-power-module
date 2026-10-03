# Lessons 03–05 — final Gate 4b schematic alignment

2026-10-03. Documentation-only update requested by `v1a-lab/briefs/LESSONS_0305.md`, on `docs/illustration-audit`. No engineering decisions or schematic/PCB changes.

## Evidence used

- Final schematic: `docs/evidence/r2/gate4b/V1A_GATE4B_REVIEW.pdf` on `origin/feat/r2-testboard-capture`, pinned to **838a8a45d8939f9b57af4715724bc71afc0134fc**.
- Local copy: `/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_GATE4B_SCHEMATIC_2026-10-03.pdf`. Both copies have SHA-256 **602271b03b7e11cc281ff7483e38a701fe9f85a4242eab3e5633af6c8869617c**.
- Same-commit `captured.xml`, `GATE4B_CAPTURE.md`, `SHEET03_REVIEW.md`, `SHEET04_REVIEW.md`, and `SHEET05_REVIEW.md` support the pin maps, capture status and untested-hook limits.
- Six-page order verified: 1 hierarchy, 2 input protection, 3 buck, 4 output protection, 5 monitor, 6 interfaces. Pages 4–6 also visually inspected using temporary renders outside the repository.

## Every lesson change

### 03 Output protection.md

1. Updated the status callout to Gate 4b capture CONDITIONAL PASS, electrical release BLOCKED and physical tests NOT RUN; identified the drawn architecture D blocks and separated inherited ideal-model timing from the manual-hook capture.
2. Replaced the analogy's paper-only raw dump with Q330/U330 on page 4.
3. Replaced the old review-PDF path with the final local PDF link, pinned Git source, six-page map and page-4 A0/13-block reading instructions; identified older illustrations/guide as historical.
4. Step 1: named the current page-3 blocks and inserted JP201/JP202, L201_IN and L201_OUT into the U201–L201–raw-output path.
5. Step 2: named the current page-2 blocks; corrected U101 OUT to EFUSE_OUT through JP101; added Q304 shutdown pins/block; updated D101 to the now-drawn SMCJ36CA.
6. Step 3: replaced R301 11.3 kΩ with 9.88 kΩ; traced U321 isolation, R303 and R367 loading; corrected U303 IN+ to REF_SENSE through R373 and its output to OV_COMPARATOR; replaced the obsolete simple-divider calculation with the retained conditional loaded-network screen; traced U614/U617 into U610 and replaced the U304 latch pin map with U610 NOFAULT/FAULT/reset pins.
7. Step 4: named block 4; corrected Q302 drains to SERIES_OUT through JP301; added U301 TGUP/R304 and INP; replaced DRV_7V5 with SER_DRV fed through D660/JP660, retaining the untested supply-loss limit.
8. Step 5: named block 5; added both protected ballast strings, JP330 and C340–C343; corrected U315 IN+ to DISPOSAL and recorded its DRV_HOLD supply.
9. Step 6: replaced the absent raw-dump description with block 6, both six-resistor strings, JP331, Q330/U330 pins, R384 and C330–C337; recorded that opening either dump link disables that path.
10. Added step 7 through the drawn auxiliary surge stopper, buck-boost, charger/held bank and DET5/3V3_AUX/SAFE5 regulators, with block names and relevant pins.
11. Added step 8 for J603/U644/TP320 manual fault command, J302 reset, J301/J604 arm contacts, JP600 rail validity, U640/U642/U647 observation-only sensing, TP337–340, paired gate/bootstrap returns and JP660 supply-loss access; retained the documented autonomous/partial-power limits and discharged-link handling rule.
12. Replaced the drawing-status table with the final page/block/refdes map, including the now-drawn raw dump, auxiliary supply and manual hooks.
13. Added a historical-label note beside the retained schematic illustration/generator instructions.
14. Section 4: connected the earlier approximately 100 mΩ raw-dump proposal to the captured 99 mΩ network, retaining the OPEN pulse rating.
15. Section 5a: labelled the existing trip/tolerance arithmetic as inherited teaching evidence rather than current physical validation.
16. Section 5c: described the actual nominal 33 mΩ/99 mΩ ballast networks and drawn U316/Q316/U317/U327/C358/C359 supply; retained the conditional hold-up number and OPEN startup/switching/pulse limits.
17. Trap 1: replaced the blanket missing-circuit description with drawn SW/VIN observation and J603 manual triggering, while keeping autonomous timing OPEN.
18. Trap 3: clarified that the retained policy diagram is not a claim of autonomous implementation; identified the manual reset/rail/arm hooks and absent persistent-short diagnostic.
19. Added the pinned final PDF/netlist/review provenance to the sources, retaining earlier calculation/model evidence.

### 04 Monitoring.md

1. Updated status to captured architecture D, CONDITIONAL PASS for capture, electrical release BLOCKED and physical tests NOT RUN.
2. Linked final PDF page 5, pinned its Git source, confirmed the six-page map and replaced old block/location names with KELVIN SHUNT / LOAD-SIDE BUS SENSE and LOCAL REGULATOR / HOST DOMAIN BOUNDARY.
3. Labelled the embedded page image as historical and explained the retained connections/new TP405/TP406 access; labelled the earlier filter excerpt as retained connectivity.
4. Updated the power walkthrough's block name and traced page-4 JP301 into R401, then page-6 J502 and the separate JP501 dummy-load branch.
5. Added TP402/TP403 Kelvin observations and TP405/TP406 force-rail observations with paired GND pin 2, distinguishing them from force-current terminals.
6. Updated all three supply/I2C reading steps to the final blocks; recorded U402 EN/NC as unconnected; specified 4.7 kΩ host pull-ups and the final page-6 PROTECTED LOAD / HOST TELEMETRY block.
7. Added the captured requirement to disconnect J503 during initial fault tests and the absence of telemetry-derived protection permission.
8. Replaced obsolete status provenance with the pinned final PDF/netlist/Sheet04 review, retaining the earlier analysis and illustrations.

### 05 Powering the Pi 5 through GPIO.md

1. Updated status to Gate 4b capture CONDITIONAL PASS, electrical release BLOCKED and physical tests NOT RUN, preserving the voltage requirements and integration gates.
2. Linked final page 6, pinned its Git source, confirmed the page map and current block name; distinguished recorded connector/harness notes from a released mating-face drawing.
3. Labelled the embedded page and connector excerpt as historical, with retained pin roles and newly captured fixture/harness information.
4. Changed the Pi physical-pin mapping from an external proposal to the mapping now written on page 6, retaining the distinction from TE cavity numbering.
5. Updated every row of the loop walkthrough to the final block names and connections: L201_OUT through JP202 to VOUT_5V1, Q302 SERIES_OUT through JP301, R401, J502 and U201 ground return.
6. Replaced the paper-only architecture D/crowbar/raw-dump paragraph with the captured block/refdes map and manual-hook limitations.
7. Added JP501/PF5 dummy-load force access, TP505 sense pins, J502-unplug isolation requirements and discharged-only force reconfiguration.
8. Corrected the inherited drop-budget starting point to JP202 pin 2; identified JP301/R401 in the path and the unqualified force-link/contact parasitics without recalculating the budget.
9. Updated the contact-sharing anchor to the positive/return branches now specified in the page-6 notes.
10. Retitled selection status and replaced pending/proposal-only Phoenix/TE wording with the captured owner solution A; retained historical AWG22 arithmetic, the Harwin documentary FAIL and all hot-contact limits.
11. Updated the snapshot and comparison table: Phoenix 1776508/1777989 with TE 3-87456-6/87309-9 and AWG20 is selected; Molex B remains a historical alternative. Kept both inherited conditional numerical screens distinct.
12. Recorded the page-6 Belden wire selections and maximum lengths, power-only housing and empty remaining cavities; retained unresolved telemetry integration and assembly qualification.
13. Updated the J503 walkthrough to the final block and first-fault disconnect instruction while preserving the host-reference pin map.
14. Updated self-check question/answer 4 and the visual-summary connector row from proposal/reconciliation wording to selected-but-unqualified status.
15. Added pinned final PDF/netlist/Sheet05 review and owner solution-A provenance; retained earlier proposal/calculation sources.

## Preservation and checks

- Added this changelog as the complete change list; only these three lessons and this log are edited under `docs/lessons/`.
- The owner's five Vietnamese parenthetical notes and their complete original lines are unchanged: `(vòi)`, `(cái thùng)`, `(tay vòi)`, `(bị gãy)`, `(động lượng)`. Every existing `(still open)` marker is also retained.
- Checked cited component references and pin/net mappings against the final exported netlist. U304 appears only as the explicitly retired predecessor of U610.
- No remaining paper-only/absent labels for the drawn architecture D, crowbar, raw dump, auxiliary supply or test hooks in the three edited lessons.
- `git diff --check` passes. Existing figures, figure generators, equations outside the obsolete detector walkthrough, and unrelated lessons remain unchanged.
- No ERC/DRC rerun: no schematic or PCB was edited. No new electrical validation or gate release is claimed.
- Local commit attempted with message `docs(lessons): align lessons 03-05 with final Gate 4b schematic`. Git refused creation of `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-illustrations/index.lock` with `Operation not permitted`; the four files remain uncommitted under the brief's explicit fallback. No lock/permission changes or push were attempted.
