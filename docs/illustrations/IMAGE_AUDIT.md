# Illustration audit and generation plan

KEEP: 0 existing images; REGENERATE: 12 existing images; REPLACE: 8 existing images; NEW: 5 images; DEFER: 3 images/concepts.
The inventory covers 21 source image files, each duplicated byte-for-byte in the project and the lesson vault.
Six of the images are embedded by Obsidian in Lesson 0 and Lesson 1; the embedded paths resolve to the vault's `assets/` copies.
The current system boundary is 13S battery → PDB → bought, isolated 48 V to 24 V module → V1A; that module is not selected.
Sheet 03 owner decision (2026-09-30): R2 fault-test board, architecture D, plus the Gate 3b source bound; application margins remain OPEN.
Every Sheet 03 image must say “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)”; every PCB/layout image must say “CONCEPTUAL”.
The next real milestone is P0: dummy-load fault injection with bench supply, oscilloscope and current probe; no Raspberry Pi connected.
Pi harness depiction: both 5 V pins and all 8 GND pins, short AWG16 harness; J502 is not final.
Five generation batches are supplied; first priority is the P0 bench setup, then the D architecture and current source/system boundary.
Deferred: the legacy WBR-specific distribution image, any routed-board render until routing exists, and at most one Option E comparison image.

## 1. Scope and disposition summary

This audit covers every PNG in `edge-ai-smart-power-module/assets/` and its matching copy under `Robotics Learning&Work space/assets/`. SHA-256 comparisons confirmed that all 21 PNG pairs are byte-identical, so each unique image was opened and visually reviewed once. The `.docx` file in the project asset folder is not an illustration and is outside this image count.

Disposition totals are counts of image deliverables: 12 regenerate the same teaching subject with corrected/current facts; 8 replace an image whose design premise or visual form is unsuitable; 5 new images; 3 deferred images/concepts. No current image is approved for KEEP unchanged. The first five to generate are: (1) P0 bench fault-injection setup, (2) Sheet 03 architecture D functional overview, (3) updated system/source boundary, (4) Sheet 03 fault sequence and measurement points, (5) Pi harness and pin grouping. Generate items 6–10 next: updated input fault map, timed TPS26630 input isolation, 10 µH inductor selection, buck energy-flow states, and safe bring-up sequence.

## 2. Current engineering facts and authority

Apply the project conductor’s 2026-09-30 addendum as current owner direction when it conflicts with older assets or branch notes:

- **REQUIREMENT / boundary:** 13S battery → PDB → a bought isolated 48 V to 24 V module → V1A. Exact module selection remains OPEN (PRs #11 and #13). Do not draw a direct battery-to-V1A path or select a module by implication.
- **OPEN:** input transient suppressor and fuse are under reselection. Draw them by function, without D101/F101 reference designators or a claimed selected part.
- **DECISION:** Sheet 03 is a fault-test board using architecture D: series disconnect at the V1A 5 V output, latched detector using REF5025 / TLV3201 / 74LVC1G74, LTC7001 gate drive, and two BSC034N06 MOSFETs back-to-back; include the CSD18540Q5B + UCC27511 crowbar with ballast resistors (preliminary) and the Gate 3b source bound. The negative paper margins remain OPEN and close only through dummy-load bench tests. The Pi stays disconnected until all board gates pass.
- **SOURCE-BOUND development direction:** L201 changes from 6.8 µH XAL8080 to a 10 µH alloy part; Würth 74437636351002 is a candidate, not a selected/qualified component. Depict a controlled 10–30 µF input bank and timed input isolation through TPS26630. These are development facts and allocations; do not label them validated.
- **OPEN:** exact output limiter/absorber implementation details and application fault margins. Keep margin callouts explicitly OPEN; do not repeat historical positive margins as passes.
- **Pi interface:** both 5 V pins and all eight ground pins share current through a short AWG16 harness. J502 is not final. Do not imply USB 3.x or D435i data passes through this PCB.
- **Physical state:** no PCB is routed. Layout views are CONCEPTUAL, not fabrication geometry. Add the exact Sheet 03 preliminary label to every Sheet 03 illustration.
- **Milestone:** P0 bench fault injection uses a dummy/electronic load, current-limited bench source, oscilloscope and current probe. No Pi or expensive SBC is connected.

The addendum’s owner decisions supersede stale recommendation text in the Gate 3 option comparison. The existing `feat/r2-testboard-freeze` tree was inspected, but no distinct Gate 4A document was found in its tracked file list; its manager report preserves the earlier Gate 3b status. Do not cite the old Option E recommendation as current.

## 3. Full image inventory and disposition

| Existing image | Disposition | Visual review and required action | Lesson embed |
|---|---|---|---|
| `00-v1a-kicad-sheet-map.png` | REGENERATE | Clear map, but it says input is 9–24 V and calls Sheet 03 open/blocking. Update the source boundary and current fault-test-board status; preserve the distinction between schematic sheets and real functional blocks. | Lesson 0 |
| `00-v1a-system-anatomy.png` | REGENERATE | Readable overview, but old input/module and output-protection status. Update the 48→24 module boundary, current D test architecture, and OPEN margins. | Lesson 0 |
| `01-input-fault-timescale-map.png` | REGENERATE | Useful layered-protection teaching structure. Remove selected D101/F101 part claims; show TVS and fuse by function, and include timed TPS26630 isolation as current development direction. | Lesson 1 |
| `01-input-protection-pcb-placement.png` | REPLACE | Side-by-side “good/bad” rendered boards look like an authored layout and name old parts. Replace with a clean functional placement/loop diagram explicitly marked CONCEPTUAL, without copper geometry or part numbers. | Lesson 1 |
| `01-reverse-mosfet-operating-states.png` | REPLACE | The three-panel drawing explains one old Q101/Q102 arrangement and mixes body-diode/control claims. Replace with a generic, electrically checked explanation of input reverse polarity/backfeed, or omit if the topology cannot be confirmed from current evidence. | Lesson 1 |
| `01-tps26630-functional-anatomy.png` | REGENERATE | Good block-level teaching layout, but its thresholds/settings are old and it incorrectly implies component values are settled. Show a controlled timed isolation function, preserve OPEN thresholds/settings, and label as functional concept. | Lesson 1 |
| `01-v1a-to-wbr-system-architecture.png` | REPLACE | Combines V1A, supercapacitor V1B and WBR-specific systems, with unsupported 12 V / battery assumptions. Replace with standalone V1A scope plus a small dashed future-integration boundary only. | — |
| `02-buck-high-side-on.png` | REPLACE | The file is actually the reverse-protection MOSFET graphic, not a buck high-side state. Replace with a correct buck high-side-on state and verified current direction. | — |
| `02-buck-low-side-on.png` | REPLACE | The freewheel path and explanatory voltage/current signs are internally contradictory. Replace with a correct low-side-on state reviewed against the buck topology. | — |
| `02-buck-waveforms.png` | REGENERATE | Major sign/label error: captions say negative inductor voltage gives positive current slope and positive voltage gives negative slope. Correct all state, voltage, current-ramp and duty-cycle labels; use illustrative values only when explicitly marked. | — |
| `02-inductor-selection.png` | REPLACE | Centers the obsolete 6.8 µH XAL8080 choice and duplicates “saturation current” sections. Replace with a selection tradeoff centered on the 10 µH alloy candidate and unqualified hot/lot Ldiff envelope. | — |
| `02-input-hot-loop.png` | REGENERATE | Helpful switching-loop concept, but depict LM61460 VIN/PGND pin-pair decoupling only if retained in current converter context; no board geometry. Mark layout CONCEPTUAL. | — |
| `02-lm61460-feedback-loop.png` | REGENERATE | Useful feedback explanation; retain only if the current V1A converter remains LM61460 on the active sheet. Remove any implication that an illustrative divider is the approved value. | — |
| `02-lm61460-ideal-placement.png` | REGENERATE | Detailed but shows old 6.8 µH and example passives as though they are captured. Update inductor and bank concepts, clearly mark CONCEPTUAL, and avoid package/pin geometry claims. | — |
| `02-output-capacitor-real-behavior.png` | REGENERATE | Useful DC-bias/ESR lesson, but it states an old V1A output-bank screening value. Keep generic or recalculate from current evidence; do not present nominal capacitance as qualified effective capacitance. | — |
| `02-v1a-circuit-anatomy.png` | REPLACE | The photo-like PCB and numbered selected parts imply hardware exists; annotations also contain garbled text and old values. Replace with a clean block diagram, not a fake PCB rendering. | — |
| `03-buck-power-flow-and-waveforms.png` | REGENERATE | Useful multi-panel structure. Fix waveform/state consistency and current-direction issues; show current 10 µH candidate as OPEN and label any numerical example as illustrative. | — |
| `04-protection-and-operating-states.png` | REPLACE | Old input limits, unresolved output-protection labels and a future supercapacitor/Pi shutdown sequence. Replace with current D fault containment and P0 test states; omit unapproved future backup behavior. | — |
| `05-pcb-layout-kelvin-and-thermal.png` | REGENERATE | Useful conceptual layout/Kelvin/thermal principles, but it can be mistaken for a real four-layer board. Remove implied stack/geometry as requirements and emphasize no PCB is routed. | — |
| `06-power-board-bringup-and-characterization.png` | REGENERATE | Strong test-sequence structure, but it shows the Pi and board under test together. Make P0 dummy-load testing the lead image and keep SBC integration as the final gate after all tests. | — |
| `07-wbr-power-distribution-board.png` | DEFER | WBR distribution architecture is outside V1A and must await the robot electrical/battery architecture. Keep out of the V1A lesson sequence for now. | — |

## 4. Visual review findings across the library

The set is visually consistent and generally readable at full size, but many images are dense and depend on precise small labels. Several strong-looking board renders imply a routed or fabricated PCB even though no PCB exists. Remove fake board photography and use simple functional blocks, line diagrams and explicit conceptual annotations.

Technical correctness needs priority over polish. The buck low-side image has a wrong current-ramp explanation, and the multi-cycle waveform repeats the same sign error. The “high-side-on” filename contains the reverse-MOSFET illustration. The buck anatomy and protection diagrams present obsolete values and future WBR behavior as current. Image-generation text errors are particularly risky here; prompts below demand exact short labels and manual review against the supplied text before use.

## 5. Generation and review rules

Each prompt in `BATCH_A.md` through `BATCH_E.md` is a standalone copy-paste request for one image. Save generated images outside the repository while reviewing; this branch accepts documentation only and no image binaries. After generation, a human/electrical reviewer must check every label, arrow direction, numeric value and visual implication against the listed evidence before replacing an asset or updating an Obsidian embed.

All images should use a clean technical-illustration style: white background, restrained navy/teal/orange/red palette, strong contrast, generous spacing, consistent line weights, legible large labels, no decorative pseudo-components, no fake board photography, and no invented ratings or measurements. Keep each requested image to one clear teaching objective. Render exact supplied wording; never paraphrase component identities, limits, status labels or OPEN risks. If exact text rendering fails, omit the tiny text and provide a numbered legend in the accompanying lesson rather than leave garbled labels.

For every Sheet 03 image, include the exact banner text `PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)`. For any PCB/layout concept include `CONCEPTUAL — NO PCB ROUTED`. Never claim validation, safety, fabrication readiness, or positive application margin. Keep the Raspberry Pi physically absent from the P0 setup.

## 7. Batch order and deliverables

| Order | File | Focus | First output |
|---:|---|---|---|
| 1 | [`BATCH_A.md`](BATCH_A.md) | P0 bench, source boundary, Sheet 03 D architecture, fault sequence and Pi harness (A5) | Bench fault-injection setup |
| 2 | [`BATCH_B.md`](BATCH_B.md) | Input protection and reverse-polarity concepts | Updated input fault map |
| 3 | [`BATCH_C.md`](BATCH_C.md) | Buck states, waveforms, L201 and converter teaching diagrams | Correct buck state/waveforms |
| 4 | [`BATCH_D.md`](BATCH_D.md) | System maps, buck switching-loop and feedback concepts | LM61460 input-loop concept |
| 5 | [`BATCH_E.md`](BATCH_E.md) | Conceptual layout, measurement and bring-up lessons | Safe bring-up sequence |

The five files contain 25 copy-paste prompts covering the 12 regenerations, 8 replacements and 5 new images. The optional Option E comparison is deferred and capped at one image; it must be clearly marked `NOT SELECTED` and cannot visually suggest an approved architecture. A routed-board render remains deferred until a board is actually routed and separately reviewed.

## 8. Evidence, limits and handoff

**EVIDENCE — visual:** 21 PNGs were opened at readable resolution. Project and vault copies have matching SHA-256 hashes. Six images are embedded in the accessible Lesson 0 and Lesson 1 Markdown notes. Their links use `![[assets/...]]` syntax and resolve to the vault asset copies.

**EVIDENCE — branch documents reviewed:** `feat/sheet03-gate2c` (`docs/evidence/r2/sheet03/GATE2C_REVIEW_CLOSURE.md`); `feat/sheet03-gate3-options` (`docs/evidence/r2/sheet03/GATE3_ARCHITECTURE_OPTIONS.md`); `feat/sheet03-gate3b-source-bound` (`docs/evidence/r2/sheet03/gate3b/`); `feat/v1a-5a-path-budget` (`docs/evidence/r2/path_budget/PATH_BUDGET.md`); and tracked files plus `docs/FINAL_MANAGER_REPORT.md` on `feat/r2-testboard-freeze`. Older branch reports predate the owner’s 2026-09-30 decision and are used as evidence, not as current architecture authority.

**LIMIT:** macOS denied filesystem access to `/Users/quockaiser/Documents`, so the Obsidian search covered the accessible Desktop vault and the full Research tree, not Documents. No KiCad project was opened or edited. This audit does not validate the circuit or the generated images; it sets the visual work queue and required review checks.

**NEXT:** Generate P0 first. Review it for tool placement, current-limited source, dummy load, current probe/scope measurement and explicit no-Pi boundary. Then generate the D architecture and updated source boundary. Keep all application voltage margins OPEN until dummy-load tests produce evidence.

## Image folder consolidation (2026-09-30)

At the owner's request, all images now live in one folder, `images/`, in the Obsidian vault (`~/Desktop/Research/edge-ai-smart-power-module`). Files from `assets/` kept their names; files from `new_assets/` were renamed to lowercase-hyphen names that keep their batch prefix. The lesson notes (`docs/lessons/`) link the new names.

| Old location | Old name | New name in `images/` |
| --- | --- | --- |
| `assets/` | `00-v1a-kicad-sheet-map.png` | `00-v1a-kicad-sheet-map.png` |
| `assets/` | `00-v1a-system-anatomy.png` | `00-v1a-system-anatomy.png` |
| `assets/` | `01-input-fault-timescale-map.png` | `01-input-fault-timescale-map.png` |
| `assets/` | `01-input-protection-pcb-placement.png` | `01-input-protection-pcb-placement.png` |
| `assets/` | `01-reverse-mosfet-operating-states.png` | `01-reverse-mosfet-operating-states.png` |
| `assets/` | `01-tps26630-functional-anatomy.png` | `01-tps26630-functional-anatomy.png` |
| `assets/` | `01-v1a-to-wbr-system-architecture.png` | `01-v1a-to-wbr-system-architecture.png` |
| `assets/` | `02-buck-high-side-on.png` | `02-buck-high-side-on.png` |
| `assets/` | `02-buck-low-side-on.png` | `02-buck-low-side-on.png` |
| `assets/` | `02-buck-waveforms.png` | `02-buck-waveforms.png` |
| `assets/` | `02-inductor-selection.png` | `02-inductor-selection.png` |
| `assets/` | `02-input-hot-loop.png` | `02-input-hot-loop.png` |
| `assets/` | `02-lm61460-feedback-loop.png` | `02-lm61460-feedback-loop.png` |
| `assets/` | `02-lm61460-ideal-placement.png` | `02-lm61460-ideal-placement.png` |
| `assets/` | `02-output-capacitor-real-behavior.png` | `02-output-capacitor-real-behavior.png` |
| `assets/` | `02-v1a-circuit-anatomy.png` | `02-v1a-circuit-anatomy.png` |
| `assets/` | `03-buck-power-flow-and-waveforms.png` | `03-buck-power-flow-and-waveforms.png` |
| `assets/` | `04-protection-and-operating-states.png` | `04-protection-and-operating-states.png` |
| `assets/` | `05-pcb-layout-kelvin-and-thermal.png` | `05-pcb-layout-kelvin-and-thermal.png` |
| `assets/` | `06-power-board-bringup-and-characterization.png` | `06-power-board-bringup-and-characterization.png` |
| `assets/` | `07-wbr-power-distribution-board.png` | `07-wbr-power-distribution-board.png` |
| `new_assets/` | `C1 — Buck high-side MOSFET on.png` | `c1-buck-high-side-mosfet-on.png` |
| `new_assets/` | `A1 — P0 fault-injection bench setup.png` | `a1-p0-fault-injection-bench-setup.png` |
| `new_assets/` | `A2 — Sheet 03 architecture D.png` | `a2-sheet-03-architecture-d.png` |
| `new_assets/` | `A3 — Present source boundary.png` | `a3-present-source-boundary.png` |
| `new_assets/` | `A4 — Fault-event sequence.png` | `a4-fault-event-sequence.png` |
| `new_assets/` | `A5 — Pi power harness boundary .png` | `a5-pi-power-harness-boundary.png` |
| `new_assets/` | `B1 — Input fault:timescale map.png` | `b1-input-fault-timescale-map.png` |
| `new_assets/` | `B2 — Conceptual input protection placement.png` | `b2-conceptual-input-protection-placement.png` |
| `new_assets/` | `B3 — Reverse polarity and backfeed teaching diagram.png` | `b3-reverse-polarity-and-backfeed-teaching-diagram.png` |
| `new_assets/` | `B4 — TPS26630 functional role and timing concept .png` | `b4-tps26630-functional-role-and-timing-concept.png` |
| `new_assets/` | `B5 — Standalone V1A and future integration boundary.png` | `b5-standalone-v1a-and-future-integration-boundary.png` |
| `new_assets/` | `C2 — Buck low-side:freewheel state.png` | `c2-buck-low-side-freewheel-state.png` |
| `new_assets/` | `C3 — Buck cycle waveforms.png` | `c3-buck-cycle-waveforms.png` |
| `new_assets/` | `C4 — 10 µH alloy inductor selection.png` | `c4-10-h-alloy-inductor-selection.png` |
| `new_assets/` | `C5 — Buck power flow and both states.png` | `c5-buck-power-flow-and-both-states.png` |
| `new_assets/` | `D1 — KiCad sheet map.png` | `d1-kicad-sheet-map.png` |
| `new_assets/` | `D2 — V1A system anatomy.png` | `d2-v1a-system-anatomy.png` |
| `new_assets/` | `D3 — V1A circuit anatomy without fake hardware.png` | `d3-v1a-circuit-anatomy-without-fake-hardware.png` |
| `new_assets/` | `D4 — Buck input switching loop.png` | `d4-buck-input-switching-loop.png` |
| `new_assets/` | `D5 — LM61460 feedback principle.png` | `d5-lm61460-feedback-principle.png` |
| `new_assets/` | `E1 — Capacitor behavior and effective capacitance.png` | `e1-capacitor-behavior-and-effective-capacitance.png` |
| `new_assets/` | `E2 — LM61460 placement principles.png` | `e2-lm61460-placement-principles.png` |
| `new_assets/` | `E3 — Protection states and fault response.png` | `e3-protection-states-and-fault-response.png` |
| `new_assets/` | `E4 — PCB layout principles without implying a routed board.png` | `e4-pcb-layout-principles-without-implying-a-routed-board.png` |
| `new_assets/` | `E5 — Safe bring-up and characterization.png` | `e5-safe-bring-up-and-characterization.png` |
