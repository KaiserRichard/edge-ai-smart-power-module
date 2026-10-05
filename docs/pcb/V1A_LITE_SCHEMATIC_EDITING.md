# V1A-Lite: edit the schematic in KiCad 9

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

This lesson is for your practice branch. Start with [README_HAND_ROUTE.md](README_HAND_ROUTE.md). Use the [PCB guide](V1A_LITE_PCB_GUIDE.md) after schematic edits.

**KNOWN** = saved design fact or documented requirement. **CALCULATED** = arithmetic/model, not measured behavior. **OPEN** = untested behavior, missing bound or unfinished review. A label applies to the values in its paragraph/table. Editing successfully is not electrical qualification.

## 1. Open the complete project

1. In this worktree, switch to `learn/v1a-lite-hand-route` as shown in the start page. Check Git status first so you can identify your own changes.
2. Open `hardware/kicad/V1A.kicad_pro` in KiCad Project Manager. Double-click `V1A.kicad_sch` to open the root schematic.
3. Keep the local `sym-lib-table`, `fp-lib-table`, `V1A.kicad_sym`, `V1A_Qualified.pretty` and `V1A_Lite.pretty`. Do not replace missing local symbols with similar-looking standard symbols.
4. Save a practice checkpoint before electrical changes. Preserve historical evidence; save new review outputs in a new `docs/evidence/handroute/` session folder.

A **symbol** is the circuit drawing of a part. A **footprint** is its physical copper-pad pattern. A **reference designator** (refdes) identifies the part, such as R202. An **MPN** is the manufacturer's exact part number. An **LCSC** number identifies a distributor item; it is not an electrical specification.

**KNOWN baseline:** commit `ee31d04ecba90d29bc69620b0de4659958434001`, with the FIX2 PCB. The reviewed design branch is `feat/v1a-lite-cost-reduction`. Earlier C/C2 documents contain historical proposals that differ from the captured design: old FETs, net names and capacitor ratings must not silently replace the current schematic.

## 2. Navigate the hierarchy

The root sheet connects blocks. A **hierarchical sheet** is a child page with named ports connecting it to the parent. Double-click a sheet box, or select it in the hierarchy navigator. Use the navigator to return to the root.

**KNOWN active hierarchy: one root plus four child sheets.**

| File in `hardware/kicad/` | What you edit there |
| --- | --- |
| `V1A.kicad_sch` | Root block connections, including power rails and the crowbar-to-latch event. |
| `01_INPUT_PROTECTION.kicad_sch` | F101, D101–D106, Q101–Q106, U101, C101/C102, input divider, ballast and latch resistors; TP110–TP114. |
| `02_BUCK_5V.kicad_sch` | U201, L201, R201–R207, C201–C207 and C209–C218. C208 is not populated. |
| `03_OUTPUT_PROTECTION.kicad_sch` | F301, SCR301, U301, Q301, R301–R308, C301/C302, TP301/TP302. |
| `05_IO_TEST.kicad_sch` | J501/J502/J503, TP501–TP508 and power flags. |

There is no active Sheet 04 telemetry block in Lite. Do not restore it by following the older V1A guide.

1. Find R202 in Sheet 02 and read its properties. Then find it in the PCB using cross-probing.
2. Trace the force path: `VIN_RAW → F101 → VIN_FUSED → Q101 → S_COMMON → Q102 → VIN_PROTECTED → buck/L201 → VOUT_5V1 → F301 → VOUT_PI`.
3. Trace the independent protection branch: raw output feeds U301's divider, Q301 and SCR301; `CB_COLLECTOR` also sets the input latch. Ground is shared, but actual return geometry matters.
4. Check both child and root connections when changing a sheet port. A local label normally connects within its sheet; a hierarchical label connects through a matching sheet pin; a global label reaches across the design. A decorative text label connects nothing.

**KNOWN actual PCB names** include `/VIN_FUSED`, `/VIN_PROTECTED`, `/VOUT_5V1`, `/VOUT_PI`, `/CTRL12`, `/CB_COLLECTOR`, `/GND`, `/01_INPUT_PROTECTION/CUT_GATE` and `/02_BUCK_5V/BUCK_FB`. The prefix shows hierarchy. Older `LOAD_5V1` prose does not rename today's `VOUT_PI` net.

## 3. Make one deliberate part edit

1. Read the danger table below. Record the old/new value, exact MPN, footprint and reason before changing an electrical part. If the required calculation is missing, mark the exercise **OPEN**.
2. Hover the symbol and press **E** for **Symbol Properties**. Confirm its Reference and sheet. Do not accidentally open or edit its text alone.
3. Edit **Value** if the displayed electrical value changes. Include useful tolerance/rating information consistent with the existing style.
4. Edit **Footprint** only after checking the exact package drawing, pad numbering, polarity and physical size. Use the footprint chooser/preview. A matching pin count does not prove a matching pin map.
5. Keep **MPN**, **Manufacturer**, **LCSC**, **Source**, and any **Distributor/Distributor_SKU** fields consistent with the same exact part. Keep `Unit_VND`/`Cost_scope` honest if you maintain cost data; a historical price is not a fresh quote. Do not invent a missing catalog number.
6. Confirm, save, and compare the diff. Run ERC after schematic changes. If the part's electrical behavior changed, update its calculation/review before treating ERC as useful supporting evidence.

Changing a Value field does not change MPN, footprint, pin mapping or a simulation model automatically. Changing MPN text does not change the symbol's pins. If a new device has a different pin map, use a verified symbol and footprint, then recheck every connection.

**KNOWN project example:** R203 is `24.6k / 0.1%`, MPN `RT0603BRD0724K6L`, LCSC `C861250`, footprint `Resistor_SMD:R_0603_1608Metric`. Use it for a read-only properties exercise; do not round it to a nearby stock value. R202 is `100k / 0.1%`. **CALCULATED:** their ratio gives **5.065041 V**, not exactly 5.1 V.

**KNOWN sourcing exception:** D101 is exact **Bourns SMCJ64CA**, with schematic LCSC field `N/A - Mouser sourced`, distributor SKU `652-SMCJ64CA`. The assembly CSV intentionally leaves its LCSC entry blank. Do not substitute a same-named part from another maker to fill that blank.

## 4. Use the Symbol Fields Table carefully

1. Open **Tools → Edit Symbol Fields**. Show Reference, Value, Footprint, MPN, Manufacturer, LCSC and Source.
2. Turn grouping off for a one-part edit. Find the intended refdes, and use the row's schematic highlight to confirm it. A grouped-row edit can change many parts.
3. Edit one cell, review adjacent fields, apply the changes and save. Do not bulk-fill a distributor number across equal-value parts with different tolerance, package or ratings.
4. Check exclusions: **DNP** means do not populate; **Exclude from BOM** affects purchasing; **Exclude from board** affects PCB transfer. These are different choices. A protection part must not disappear just to make the BOM simpler.

The table also exports the BOM. The official [KiCad 9 Schematic Editor manual](https://docs.kicad.org/9.0/en/eeschema/eeschema.html) documents properties, hierarchy, annotation, ERC and the fields table. Menus may vary slightly with installed patch release or custom hotkeys.

## 5. Add a part and connect it

1. State its purpose first. Select the correct sheet. Press **A** and choose a verified symbol; press **R** to rotate before placement if needed. Keep pins on the schematic connection grid.
2. Press **E** and assign the value, exact footprint and sourcing fields. Check symbol pin numbers against the package drawing. For a transistor, identify base/gate, emitter/source, collector/drain and any live tab.
3. Use **W** to wire from pin endpoints. A wire that merely looks close is not connected. Place junctions for intended branches; inspect crossings rather than assuming they connect.
4. Use a suitable label for the intended scope. If you add a child-sheet interface, add its matching parent sheet pin and wire the root connection too.
5. Keep unused pins intentionally unconnected only when the datasheet/design allows it. Use the no-connect marker; do not hide a missed wire with one.
6. Annotate new parts, run ERC, inspect the changed page and root, then update the PCB through F8. Place the new footprint and route it deliberately.

Copying a symbol can carry old values and sourcing fields. Recheck them. Adding a capacitor to a detector or gate is an electrical change: it can delay protection, even if the symbol is easy to place.

## 6. Delete a part without leaving a hidden mistake

1. Check what changes electrically. Deleting a series part normally opens a path; deleting a shunt part removes a branch. Do not automatically wire across a removed fuse or switch.
2. Select the symbol and press Delete. Inspect remaining wires, junctions, labels and sheet ports; remove only items that are no longer intended.
3. Update calculations and the function/removal note. Preserve older evidence in Git/history.
4. Run ERC. Later, inspect the F8 removal list and stale tracks/zones on the PCB. A deleted schematic symbol can otherwise leave a physical footprint or misleading copper behind.

**KNOWN example to protect:** removing F301 from the circuit is not a cosmetic exercise. It changes wiring protection and the raw/Pi boundary. Never bridge F301 merely to eliminate an unconnected marker.

## 7. Annotate new parts; keep existing identities

**Annotation** assigns unique references, such as R301 instead of R?.

1. Open **Tools → Annotate Schematic** after adding parts.
2. Preserve existing annotations; annotate only unannotated symbols. Keep this project's sheet families: input in the 100 series, buck in the 200 series, output in the 300 series, IO in the 500 series. Check for an unused number rather than guessing from a drawing gap.
3. Confirm no duplicate or unresolved references remain. Some KiCad settings auto-annotate new symbols; still review the result.
4. Do not reset all annotations. The PCB links, BOM, test maps, calculations and review findings refer to these existing identities. A deliberate renumbering needs a complete reference-map update.

Do not delete and recreate a symbol just to edit its value. KiCad normally links schematic symbols and footprints by a unique internal ID; recreating a symbol changes that ID.

## 8. Run ERC and read the result

**ERC** means Electrical Rules Check. It finds connection/type problems such as an undriven power input or an unconnected pin. It does not calculate temperature, thresholds, transistor stress or protection timing.

1. Save the whole hierarchy. Open **Inspect → Electrical Rules Checker** and run it for the project.
2. Read every error and warning. Double-click a result to zoom to its marker; inspect the actual pins, labels and wire endpoints.
3. For **unconnected pin**, determine whether a wire was missed. For **power input not driven**, check where the supply really enters. A `PWR_FLAG` tells ERC about a real source; it does not create power.
4. For **conflicting pin types**, inspect the symbol's intended function and datasheet. Do not turn all pins into passive pins to silence ERC. Fix the circuit or verified symbol definition.
5. Check annotated references and footprint assignments separately. Run again after corrections and save the report. Document any individually justified exclusion; do not weaken project severities.

**KNOWN baseline:** U201 pin **5 PGOOD** is intentionally unused with a no-connect marker. Power flags are on VIN_RAW, VIN_PROTECTED and GND. Preserve those meanings; do not add flags to hide disconnected rails. Historical FIX2 ERC reports **0 errors / 0 warnings**; that result does not cover your edits.

**KNOWN command form**, from the repository root:

```sh
mkdir -p docs/evidence/handroute/session-01
KICAD_CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
"$KICAD_CLI" sch erc --severity-all --exit-code-violations \
  -o docs/evidence/handroute/session-01/ERC.rpt hardware/kicad/V1A.kicad_sch
```

Use a new session name for later changes. Run `sch erc --help` if your installation differs. No new ERC/DRC pass is claimed by this guide-writing task: it made no CAD changes.

## 9. Update PCB from Schematic — F8

1. Save the schematic. Open the PCB from the same project. Choose **Tools → Update PCB from Schematic**, or **F8**.
2. Read the proposed changes **before** clicking Update PCB. Match every addition, net change, field update, replacement or deletion to your intended edit.
3. Normally keep **Re-link footprints to schematic symbols based on their reference designators** unchecked. Existing unique IDs should maintain the links. Use refdes relinking only as a deliberate repair after checking identities.
4. If you deliberately changed the footprint assignment, review the **Replace footprints with those specified in the schematic** option. A replacement can invalidate local routing, pad mapping and custom geometry. Do not refresh all local footprints from libraries without reviewing board-specific pad/mask/paste work.
5. If you deleted parts, review **Delete footprints with no symbols** and its proposed list. Preserve intentional board-only holes MH1–MH4. Do not accept unexplained deletions. Cancel an unexpected change list and diagnose it first.
6. Apply the expected update. Place new footprints outside/near their intended block, then finish placement. Check old routes, isolated copper and pad escapes after any changed net or footprint.
7. Refill with **B**, save, run **DRC with schematic parity**, and visually inspect the edited area on every affected layer. Repeat the copper/thermal/protection checks affected by the edit.

F8 transfers schematic connectivity and part information. It can add/update/remove footprints according to the options. It does not place a good buck loop, repair all stale routes, calculate current capacity or qualify the circuit. Existing routes may remain geometrically wrong after a pad/net change. See [KiCad forward annotation](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#forward-and-back-annotation).

## 10. Re-export a review BOM and schematic PDF

1. Save and run ERC first. Create a new evidence session directory; do not overwrite `docs/evidence/v1a_lite/fab/` or an older review report for practice.
2. For a GUI BOM, open **Tools → Generate Bill of Materials** (the fields-table export view). Show Reference, Value, Footprint, MPN, Manufacturer and LCSC. Group only when all exact-part identity fields agree. Preview the CSV before exporting.
3. Keep copper features/test pads and board-only holes separate from purchased parts. **KNOWN starting inventory:** **100 purchased refs**; **93 SMT**, with **C101, C217, C218, D101, J501, J502, SCR301** as the seven manual parts. Your intentional edits may change those counts; explain the difference.
4. For a PDF, use **File → Plot**, choose PDF and all sheets. Keep the drawing sheet and fabrication warning. Open the exported PDF and check hierarchy, page count, legible values, junctions and warnings.
5. If the PCB changed, BOM/PDF alone do not refresh fabrication files. Regenerate and review placement/layer outputs in the new session when needed, following the PCB guide. Keep all outputs review-only.

**KNOWN equivalent CLI forms** (installed help checked):

```sh
"$KICAD_CLI" sch export bom \
  --fields 'Reference,Value,Footprint,MPN,Manufacturer,LCSC,Source' \
  --labels 'Reference,Value,Footprint,MPN,Manufacturer,LCSC,Source' \
  -o docs/evidence/handroute/session-01/BOM_REVIEW.csv \
  hardware/kicad/V1A.kicad_sch
"$KICAD_CLI" sch export pdf \
  -o docs/evidence/handroute/session-01/SCHEMATIC_REVIEW.pdf \
  hardware/kicad/V1A.kicad_sch
```

This explicit-field CSV is an inspection BOM, not a supplier-ready purchase file. Inspect exclusions, PCB_FEATURE rows and D101's external source. The unchanged hierarchy should export **KNOWN: five pages**. Check the [KiCad CLI reference](https://docs.kicad.org/9.0/en/cli/cli.html) and installed help if an option differs.

## 11. DANGER: edits that require calculations again

These are **KNOWN current parts/nets**. Calculation values are marked separately. A substitution needs exact package, pin, tolerance, temperature coefficient, voltage/current/pulse and thermal checks. A same-value part is not automatically equivalent.

Calculation files used below:

- **C:** [PHASE_C_CALCULATIONS.md](../evidence/v1a_lite/PHASE_C_CALCULATIONS.md).
- **C2:** [PHASE_C2_REVISION.md](../evidence/v1a_lite/PHASE_C2_REVISION.md).
- **S1:** [SCH_REVIEW_R1.md](../evidence/v1a_lite/SCH_REVIEW_R1.md).
- **FIX1:** [PCB_FIX1_REPORT.md](../evidence/v1a_lite/PCB_FIX1_REPORT.md), with current geometry/results in [LAYOUT_EXPLAINED.md](../evidence/v1a_lite/LAYOUT_EXPLAINED.md) and [FIX2 copper report](../evidence/v1a_lite/fix2/COPPER_RESISTANCE_0.1.json).

Read these files; write any new calculation in a new evidence session. Do not run old generators over historical outputs. C/C2 use the old IRF9540 for some FET calculations; replace those inputs with the actual IRFR6215 before using that model.

| DANGER parts / nets | What must be checked again | Calculation/review to reopen |
| --- | --- | --- |
| **U301 TL431BIDBZR; R301=1k, R302=100Ω, R303=30Ω, R304=1k**; OVOUT_REF, raw VOUT_5V1 | Upper divider totals 1.13k. **CALCULATED ideal trip 5.31435 V**, before REF-current shift. Tolerance/TCR, TL431 grade, reference return, normal-high/noise margin and detector delay all matter. Do not lower trip or add filtering casually. | C §4; C2 §3; S1 finding 1. |
| **SCR301 TYN612RG, Q301 BC807-40,215; R305=500Ω, R306=10k, R307=100Ω, R308=1k**; SCR_GATE, CB_COLLECTOR | Gate current/rise, latching/holding, pulse di/dt, I²t (current-squared integrated over time), thermal energy and recovery. RG is not the lower-trigger-current TRG grade. R163 also loads the driver. No fuse between SCR and raw bank. | C §4–5; C2 §3–5; S1 findings 1/4; [CROWBAR_REVIEW.md](../evidence/v1a_lite/fix1/CROWBAR_REVIEW.md). |
| **U101 TL431BIDBZR; R150=100k, R151/R152=1k each, R153=10k**; S_COMMON, OVIN_REF | **CALCULATED 27.944 V ideal (~28 V)**. Recheck threshold corners, REF current, cold-start/running cutoff delay and protected-input peak; divider change can expose U201. | C §1–2; C2 §2; S1 finding 2. |
| **Q104/Q106 MMBTA42-TP, Q105 BC807-40,215; R160–R163=10k, R164–R166=100k**; SET_LATCH, LATCH_H, CTRL12, IN_NPN_BASE | Short-pulse capture, regeneration, brownout retention/reset, CTRL12 load and Q103 inhibition. Keep upstream supply and effective Q102 shutdown; output-derived power or Q101-only shutdown changes the protection concept. | C2 §1–2; S1 finding 3. |
| **Q101/Q102 IRFR6215TRPBF; Q103 MMBTA42-TP; D102/D103; R101/R102, R130–R135, R140–R146**; REV_GATE, CUT_GATE, S_COMMON | Current-selected **150 V DPAK** pin/body-diode orientation, gate clamp/drive, turn-off charge, hot RDS(on), linear SOA, reversal/backfeed and thermal loss. The old **100 V TO-220 IRF9540** results are not qualification. | C §1–2/5 and C2 §2 as model structure only; S1 finding 2; FIX1 actual-part thermal analysis. |
| **R110–R125=1k each, D104=12 V, D105=3.3 V, C102=1µF/16 V**, with R144–R146 | Ballast uses two parallel strings, each eight resistors. Recheck working voltage, pulse/continuous dissipation, CTRL12 regulation under latch/detector load, startup and reset. Do not replace a distributed string with one small resistor. | C §2; C2 §1; S1 findings 2–3. |
| **R202=100k/0.1%, R203=24.6k/0.1%**, BUCK_FB | **CALCULATED output 5.065041 V**. Recheck low Pi voltage and high normal voltage versus crowbar threshold, including tolerance/TCR/ripple/transients. Remote-sense rewiring is a control-loop change. | C §3–4; C2 §3; S1 finding 1; FIX2 copper and [PI_HARNESS.md](../evidence/v1a_lite/PI_HARNESS.md). |
| **U201 LM61460AANRJRR, L201 SRP1265A-6R8M, R201=33.2k, C207=22pF, R205=1k** | Switching frequency, ripple/peak current, saturation, loss, stability and load-release/PFM overshoot. Different regulator suffixes can change behavior. | C §3/5; C2 §3; S1 findings 1/4; TI LM61460 Rev D. |
| **R204=0Ω, C205=100nF/16 V, C206=1µF/16 V; R206=100k, R207=24.6k**; BUCK_CBOOT, BUCK_SW, BUCK_VCC, BUCK_EN, BIAS | BOOT is referenced to SW; VCC is not a protection supply. BIAS stays GND. The EN divider is not an 18 V UVLO. Recheck pin limits, startup and switching if changed. | C §3; S1 finding 8; TI Rev D pin/layout sections. |
| **F101 0451003.MRL 3 A; F301 0451007.MRL 7 A**; VIN_FUSED, VOUT_PI | Voltage and breaking capacity, hot derating/resistance, total clearing time/energy, actual source hiccup and wire/contact coordination. A 5 A load does not imply a 5 A fuse. F301 is wiring backup, not guaranteed crowbar clearing. | C §1/4/5; C2 §1/4/5; PI_HARNESS; FIX1/FIX2 voltage budget. |
| **D101 Bourns SMCJ64CA; D106 TVS3300DRVR; D102–D105 zeners** | Standoff, exact pulse-clamp conditions, energy, hot leakage, polarity and gate/device limits. D101 is before the FETs; D106 is downstream. Do not equate 64 V standoff with 64 V clamping. | C §1–2; S1 finding 2; [spacing/assembly note](../evidence/v1a_lite/fix1/SPACING_AND_ASSEMBLY.md). |
| **C209–C214 47µF/25 V GRM31CR61E476ME44L, C217/C218 1000µF/10 V EEUFR1A102; C301/C302 47µF/16 V** | Effective capacitance under voltage, tolerance, ESR/ESL, ripple heating, stability, inrush, SCR discharge energy and voltage containment. Raw 25 V ceramics do not protect the 10 V bulk or survive an uncontained 26–29 V fault automatically. | C §3–5 using current identities; C2 §3–5; S1 findings 1/4. |
| **C101 100µF/50 V; C201/C202/C215/C216 10µF/50 V; C203/C204 100nF/50 V** | Input effective C, hot-loop ripple, inrush, cutoff rise-time budget, stored fault energy and reverse voltage. They cannot be assumed to survive direct 64 V. | C §1–3; C2 §2/5; S1 findings 2/4. |
| **J501/J502 and J503**, VOUT_PI/GND, harness | Actual pad mapping, contact/wire ratings, hot/aged round-trip resistance, fault coordination, keying and remote overshoot. **KNOWN allocation ≤25 mΩ harness**, not the obsolete 40 mΩ. | PI_HARNESS; C2 §3; FIX2 voltage budget; PCB guide §§14–16. |

## 12. Pin-map checks that ERC will not do for you

**KNOWN captured mapping, verify again for any replacement:**

| Part | Pins to preserve |
| --- | --- |
| U101/U301 TL431 **DBZ** | 1 cathode K, 2 REF, 3 anode A=GND. Do not assume a TL432 has the same mapping. |
| Q101/Q102 DPAK | 1 gate, 2 drain/tab, 3 source. Their sources are common; drains remain different live nets. |
| SCR301 TO-220 | 1 cathode=GND, 2 anode/tab=raw VOUT, 3 gate. |
| Q103/Q104/Q106; Q105/Q301 | 1 base, 2 emitter, 3 collector; emitter nets differ by circuit. |
| U201 RJR | 1 BIAS=GND; 2 VCC; 3 AGND; 4 FB; 5 PGOOD NC; 6 RT; 7 EN/SYNC; 8/12 VIN; 9/11 PGND; 10 SW; 13 RBOOT; 14 CBOOT. No EP15. |
| J501/J502 | 1 positive rail, 2 GND. J503 likewise has positive pad 1 and GND pad 2. |

A correct-looking symbol name does not establish these mappings. For example, an embedded generic SCR symbol may retain a library name while its **Value/MPN** specifies TYN612RG. Check the actual pins, not the symbol's historical library name alone.

## 13. Finish the practice change

1. Review `git diff --stat` and the schematic/board diff. Explain every electrical, field, footprint and net change. Do not accidentally include cache/build files or unrelated edits.
2. Keep the new calculations, ERC, DRC/parity, BOM/PDF and visual review tied to the same saved revision. Record remaining **OPEN** issues.
3. Keep practice commits focused if you choose to commit your exercise. Do not push or order hardware as part of this lesson.
4. Respect the gate order: environment/reference audit → requirements → schematic → PCB → fabrication review → physical validation. A new circuit change can reopen earlier review work. At a gate completion, update `docs/FINAL_MANAGER_REPORT.md` as required by AGENTS.md.
5. **OPEN release items:** output trip window/response, input cutoff survival, latch retention and SCR stress remain unqualified. Thermal, spacing, harness and assembly limits also remain open. ERC/DRC cannot close them. Follow the staged [bench plan](../evidence/v1a_lite/BENCH_TESTS.md), with the later harness/thermal corrections, only after the required review; use a dummy load before any SBC.

## 14. Sources and scope of this lesson

**KNOWN:** native files, fields, pins and project rules were read at `ee31d04`. C, C2, S1, FIX1 and FIX2 are linked above; the [PCB guide's reading trail](V1A_LITE_PCB_GUIDE.md#20-reading-trail-and-provenance) records the full source set. All sources were read-only. No KiCad file was edited by this guide-writing task.

Official KiCad 9 schematic/PCB/CLI documentation was referenced for software operations, accessed 2026-10-05. Manuals credit the KiCad Documentation Contributors and offer GPL-3.0-or-later or CC-BY-3.0-or-later; displayed documentation revision is `152cd19e` where shown. Installed CLI **9.0.6** help was also checked. No manual text, third-party circuit or PCB artwork was copied into CAD and no upstream source was changed. Manufacturer document identities, licenses and required attribution remain in [Phase D sources](../../third_party/v1a_lite_phase_d/SOURCES.md), [C2 sources](../../third_party/v1a_lite_phase_c2/SOURCES.md), [C3 manifest](../../third_party/v1a_lite_phase_c3/DOCUMENT_MANIFEST.json) and the PCB guide. Manufacturer copyright remains; no redistribution license is inferred.
