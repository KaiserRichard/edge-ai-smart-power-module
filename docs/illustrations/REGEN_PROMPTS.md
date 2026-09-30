# Regeneration prompts — eight rejected lesson images

2026-09-30. Documentation only, on `docs/illustration-audit`. Generate one image per fenced prompt, following the format of [Batch A](BATCH_A.md), [Batch D](BATCH_D.md), and [Batch E](BATCH_E.md). Each prompt is self-contained. The target names below are the **new names in `images/`** from the [audit rename table](IMAGE_AUDIT.md), not the older numbered assets.

**OBSERVATION:** all eight current PNGs were opened and visually inspected in `/Users/quockaiser/Desktop/Research/V1A-Lessons/images/`. The error lists describe those images. No image was edited, moved, or replaced in this task. Review each eventual generation before replacing the corresponding lesson image; retain its exact target filename.

**REQUIREMENT:** these are teaching illustrations, not electrical validation or authorization for a later engineering gate. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Evidence and precedence

The brief and newer Gate 4a evidence supersede the older 9–24 V ceiling, pending TVS/fuse selection, and empty-Sheet-03 descriptions in some context/audit/batch documents. Gate 4a is R2 analysis, not the R4 fabrication-readiness gate. Its proposed changes are not all captured or qualified.

| Evidence ID | Exact revision and files inspected | Use here |
| --- | --- | --- |
| CTX | Illustration branch baseline `3d5b5cb2fbaf59f85af978bd8db1a7bd88eb5cee`: `docs/context/00_USER_AND_WORKSTYLE.md` through `06_DECISION_LOG.md`, `docs/evidence/r2/BUCK_DESIGN.md`, `docs/evidence/r2/MONITOR_POWER_DOMAINS.md` | Standalone scope, local feedback, four-terminal Kelvin sensing, evidence vocabulary and bring-up order; historical selections/status yield to G4. |
| G4-BASIS | `feat/r2-testboard-freeze` at `2774400c0ad9481d4ee8aa149cb2a9b877149b48`: [gate4a/BASIS.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2774400c0ad9481d4ee8aa149cb2a9b877149b48/docs/evidence/r2/gate4a/BASIS.md) | Normal input 9–26 V; architecture D; owner-selected D101/F101; application qualification remains OPEN. |
| G4-CHANGE | Same commit: [FREEZE_TABLE.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2774400c0ad9481d4ee8aa149cb2a9b877149b48/docs/evidence/r2/gate4a/FREEZE_TABLE.md), [TIMING_AND_LOGIC.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2774400c0ad9481d4ee8aa149cb2a9b877149b48/docs/evidence/r2/gate4a/TIMING_AND_LOGIC.md) | Retained local regulation, qualification-candidate inductor, parallel fault actions, proposed separate raw dump, fault/PG/reset distinctions and unresolved implementation. |
| G4-BENCH | Same commit: [TEST_HOOKS.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2774400c0ad9481d4ee8aa149cb2a9b877149b48/docs/evidence/r2/gate4a/TEST_HOOKS.md), [TEST_PLAN.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2774400c0ad9481d4ee8aa149cb2a9b877149b48/docs/evidence/r2/gate4a/TEST_PLAN.md) | Dummy load/emulator, force/return wiring, differential voltage measurements, current-probe placement, bounded fixture and pre-power/test sequence. |
| G4-SHEETS | Same commit: [hardware/kicad/V1A.kicad_sch](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2774400c0ad9481d4ee8aa149cb2a9b877149b48/hardware/kicad/V1A.kicad_sch), its five `Sheetfile` properties and tracked child filenames | One root plus five child sheets, 01–05. No Sheets 06–08. |
| TVS | `feat/v1a-input-tvs` at `84c991fe224c299e34751a3418640600f577a739`: [TVS_RESELECTION.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/84c991fe224c299e34751a3418640600f577a739/docs/evidence/aux_converter/TVS_RESELECTION.md), [TVS_SOURCES.md](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/84c991fe224c299e34751a3418640600f577a739/docs/evidence/aux_converter/TVS_SOURCES.md) | D101 Littelfuse SMCJ36CA and F101 Schurter 3403.0285.23 provenance; G4-BASIS supersedes this earlier report's 9–24 V ceiling. |

Branch evidence was read with `git show`; no branches were merged. Reproduce any cross-branch read with `git show <full-commit>:<path>`. Manufacturer attribution/revisions remain in the existing evidence registers: e.g. TI LM61460 SNVSBD5D, Littelfuse SMCJ JC.02/27/25 v.2, and Schurter UMT-H 21.07.2026. This document references those internal engineering reviews; it copies no third-party schematic, PCB, source file, or manufacturer artwork.

| Fact to preserve | Correct interpretation |
| --- | --- |
| Input | **REQUIREMENT:** 9–26 V DC at the V1A input. The approximately 5.1 V rail is the buck output. Neither is a measured rating. |
| D101 / F101 | **DECISION:** Littelfuse SMCJ36CA / Schurter 3403.0285.23, owner-selected for proposed capture; hot clamp, clearing and installed qualification OPEN. D101 is a shunt TVS at `VIN_FUSED` to GND, not a series power block or a 36 V regulator. F101 is in series ahead of `VIN_FUSED`. |
| Output path | **DECISION:** architecture D: `VOUT_5V1` → opposed BSC034N06 series pair → `VOUT_PROTECTED` → R401 2 mΩ force path → `LOAD_5V1` → J502/harness/dummy load. INA228 senses the shunt; load current does not flow through its sense inputs. |
| Fault disposal | Protected crowbar: CSD18540Q5B, UCC27511 and drain ballast. **PROPOSAL / OPEN:** Gate 4a adds a separate raw-side dump because opening the series pair disconnects the protected crowbar from upstream L201/raw-bank energy. Source isolation and independent trigger implementation also need qualification. |
| Feedback / L201 | Feedback senses local `VOUT_5V1`, before the disconnect. L201 development direction is 10 µH alloy; Würth 74437636351002 is a qualification candidate, not a bench-qualified selection. |
| Physical state / testing | No routed PCB. Planned tests use dummy loads and reviewed fixtures. No Raspberry Pi/SBC, host I2C or USB connection during fault tests; integration follows all applicable gates. |

## A1 — P0 fault-injection bench setup (REGENERATE)

Target filename: `a1-p0-fault-injection-bench-setup.png`

**OBSERVATION — exactly what is wrong:**

- The input arrow says `5 V IN` and the source display says `5.00 V`. That misidentifies the full V1A input; 9–26 V belongs at the input and approximately 5.1 V at the output.
- The supply's positive/negative cables visually merge into one teal stroke. The board-to-load path is a single arrow while the load's two leads also merge below it. Separate positive and return circuits cannot be traced.
- The voltage probe has only one visible measurement connection, with no defined return/reference. Its connection to the scope channel is also unclear. This is insufficient for a reproducible voltage measurement.
- The green board has invented packages, component placement and screw terminals, despite the conceptual label. The scope displays an unprovided step waveform. Neither is project evidence.
- There is no depicted bounded fault fixture or clear distinction between a planned fault and ordinary supply/load wiring. A current-limited supply alone does not bound all capacitor/fault energy.

**EVIDENCE:** G4-BASIS, G4-BENCH, G4-CHANGE.

```text
Create one landscape 16:9 engineering training illustration titled “P0 — Dummy-Load Fault-Injection Bench”. Intended replacement filename: a1-p0-fault-injection-bench-setup.png. Include the exact top banner “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)” and a large red label “NO RASPBERRY PI CONNECTED”.

Show a current-limited programmable bench supply, a plain rectangular “V1A — architecture D” boundary, a send/return harness ending at a passive header emulator, and an electronic dummy load. Label the source connection “V1A INPUT: 9–26 V DC”. Label the output “Approximately 5.1 V nominal — qualification OPEN”. Leave instrument screens blank or write “record measurements”; do not invent a setpoint, current limit or waveform.

Draw four explicit power connections: supply + to V1A INPUT+; supply − to V1A GND; V1A LOAD_5V1 through the send harness to dummy-load +; dummy-load − through the return harness to V1A GND. Keep positive and return conductors distinct. Put a current-probe clamp around the output positive conductor ONLY, with its positive-current arrow toward the dummy load and its signal cable ending at the oscilloscope. Put a differential voltage probe across dummy-load + and the same far-end loaded return; draw both measurement tips and its separate scope cable. Label “No instrument-earth bypass of harness return”. Add a separate temperature-measurement icon aimed at the test-board boundary.

Inside the V1A boundary, use functional boxes: “Input protection” → “LM61460 buck” → “Architecture D series disconnect” → “2 mΩ shunt” → “LOAD_5V1”. Do not draw a physical PCB. Add a small note “D101: SMCJ36CA; F101: Schurter 3403.0285.23 — selected for review, qualification OPEN”. Keep this note separate from wiring.

Show an unconnected amber planning callout, not a jumper wire: “Bounded-energy fault fixture — implementation/review OPEN”. Add “Fault energy includes stored capacitance; current limit alone is insufficient”. Keep detailed injector circuitry out of this overview. Show the operator sequence: “1 Visual + continuity checks”; “2 Current-limited 9–26 V input”; “3 No-load startup + rail checks”; “4 Dummy-load steps”; “5 Reviewed fault injection”; “6 Record voltage/current/temperature”. Add “PLAN ONLY — bench gates required” and “CONCEPTUAL — NO PCB ROUTED”.

MUST NOT show: 5 V or 5.00 V at the V1A input; joined +/− leads; a one-tip voltage measurement; a clamp around both send and return; a direct source wire into the output that bypasses the buck/disconnect; a Pi/SBC or host-data connection; an unbounded fault jumper; a fabricated PCB or invented waveform/result.

Style: white background, clean vector linework, navy text, teal power, grey returns, orange measurement signals and red fault boundaries. Large sparse labels, visible junction dots, no ambiguous crossings, no decorative components or tiny text. This is a wiring overview for a planned test, not proof of safe or validated hardware.
```

## E5 — Safe bring-up and characterization (REGENERATE)

Target filename: `e5-safe-bring-up-and-characterization.png`

**OBSERVATION — exactly what is wrong:**

- Step 3 and the central bench both show `5.00 V`; the source caption says `(5 V)` and the input arrow says `Input (5 V from bench)`. All mislabel V1A's 9–26 V input. The displayed `0.50 A` is an invented current-limit setting.
- In the central bench, only one output power wire is clearly traceable from the board. The load leads and current-probe cable are not separated clearly; the clamp is drawn above the lead rather than enclosing it. The scope lacks a visible voltage-reference connection.
- Step 1 and the bench show photo-like populated boards unsupported by a routed V1A design. The conceptual badge does not fix that visual claim.
- The step-5 `V, I` plot shows both quantities increasing with load, which suggests rising regulated output voltage and invents a response. The scope traces are also unprovided. Step 4 has overlapping/garbled output-voltage text.
- Step 7 already places the Pi behind a gate; preserve that separation, but make telemetry completion a prerequisite of the final integration gate.

**EVIDENCE:** CTX bring-up sequence; G4-BASIS and G4-BENCH.

```text
Create a vertical seven-step flow titled “V1A Validation — Dummy Load Before SBC”. Intended replacement filename: e5-safe-bring-up-and-characterization.png. Include “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)” and “CONCEPTUAL — NO PCB ROUTED”. This is a planned sequence, with no completed-test checkmarks or results.

Use these seven headings exactly: “1 Visual inspection”; “2 Continuity and short checks”; “3 Current-limited bench supply”; “4 No-load startup and output check”; “5 Low-current dummy load, then increasing load”; “6 Ripple, transient, thermal and fault tests”; “7 Telemetry checks, then SBC integration”. Keep the headings readable and do not repeat overlapping text.

Under steps 1–2, show abstract inspection and unpowered-meter icons. Under step 3, label the source “V1A INPUT: 9–26 V DC”; label its control “Current limit per reviewed test plan”, with no numeric setting. Under step 4 show the load physically disconnected and label “Check raw, protected and auxiliary rails”. Under step 5 show a dummy load and “Approximately 5.1 V nominal output — qualification OPEN”, with no response plot. In step 6 show the sub-order “Thermal → ripple → load transients → reviewed fault tests”, and “Bounded-energy fixture required; fixture design OPEN”.

Use one simple bench inset for the loaded tests: supply + → V1A INPUT+; supply − → V1A GND; V1A LOAD_5V1 → send harness → dummy-load +; dummy-load − → return harness → V1A GND. Show separate positive and return conductors. A current probe must encircle only the positive output wire. A differential voltage probe must have two tips across the dummy-load input and its far-end loaded return. Their separate signal cables go to the scope, not to load terminals. Show a temperature instrument separately. Leave screens blank. Add “Check instrument grounds; no bypass of the harness return” and “Change connections only with power off and stored energy discharged”.

Use a plain functional rectangle for “V1A architecture D”; no component placement. A small text-only design note may read “D101 SMCJ36CA; F101 Schurter 3403.0285.23 — qualification OPEN”. Put a prominent “NO Pi/SBC during fault tests” boundary around steps 1–6. Step 7 first contains “Validate telemetry with bench interface”; then a closed gate “Only after all previous tests and telemetry pass”; only beyond that gate show one Pi icon labeled “Future integration”. No wire may connect that Pi to the fault-test inset.

MUST NOT show: a 5 V V1A input, a 5.00 V supply display, an invented 0.50 A limit, a missing load return, a probe signal cable used as a power lead, a clamp floating above the wire, rising Vout-versus-load curves, fabricated waveforms or populated V1A PCB photographs, or a Pi connected before the telemetry/integration gate.

Style: clean white-background vector process diagram, navy headings, teal power, grey returns, orange instruments and red fault-test boundary. Large exact text, generous spacing, no numeric acceptance thresholds or claims of measured safety/performance. Footer: “PLAN ONLY — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED”.
```

## E4 — PCB layout principles without implying a routed board (REGENERATE)

Target filename: `e4-pcb-layout-principles-without-implying-a-routed-board.png`

**OBSERVATION — exactly what is wrong:**

- Panel 1 connects the lower input-capacitor rail to the line labeled SW, not PGND. Its red “high di/dt” arrows run toward the inductor/output capacitor and do not identify the compact input commutation loop correctly.
- Panel 3 draws a two-terminal shunt with taps on the force wires. It does not show the separate force and sense terminals required by the project's four-terminal Kelvin shunt. Its direct `From buck` label also omits the intervening output-protection boundary in a V1A reading.
- Panel 4 draws different component pads over one continuous copper slab without distinguishing electrical nets from heat flow. This can be read as shared electrical copper, including under the inductor/capacitor terminals.
- The title and footer say to apply the principles *after* routing; switching-loop, Kelvin and thermal constraints must guide placement/routing and then be reviewed.

**EVIDENCE:** CTX buck/monitor reviews, G4-CHANGE.

```text
Create a landscape four-panel teaching illustration titled “Layout Principles — Before and During PCB Routing”. Intended replacement filename: e4-pcb-layout-principles-without-implying-a-routed-board.png. Use the bold banner “CONCEPTUAL — NO PCB ROUTED”. Draw abstract circuit/thermal concepts, not a board or package layout.

Panel 1, “Compact input commutation loop”: draw a synchronous-buck half bridge as two generic internal switch symbols. Connect local CIN between VIN and PGND. High-side switch connects VIN to SW; low-side switch connects SW to PGND; L connects SW to VOUT; COUT connects VOUT to PGND. Highlight a CLOSED dashed outline around CIN, the high-side switch, the low-side switch and the short PGND return only. Label “High di/dt commutation loop; minimize area”. Keep L and COUT outside the highlighted loop. Explain with a short note “Loop boundary, not simultaneous switch conduction”. Show both switches without claiming they are on together. Every capacitor has one lead at each intended node; never bridge its plates with a wire.

Panel 2, “Short high-current paths”: use thick separate forward and return paths between an abstract protected-output source and load. Mark “Keep send and return close; minimize resistance and loop area”. Use no dimensions, copper weight or guaranteed ampacity. This panel is independent of panel 1; do not create an invented V1A bypass between panels.

Panel 3, “Four-terminal Kelvin shunt”: draw one abstract R401, “2 mΩ”, with FOUR DISTINCT terminals labeled FORCE+, SENSE+, SENSE− and FORCE−. Thick load current runs from “VOUT_PROTECTED” into FORCE+ and out FORCE− toward “LOAD_5V1”. Two thin sense wires start at the separate SENSE+ and SENSE− terminals and end at a box “INA228 sense interface”, with corresponding + and − inputs. These wires carry no load current. Label “Functional view; input filter omitted”. Do not attach sense wires to remote power copper or interchange their polarity. This is terminal intent, not a physical footprint or pin-number drawing.

Panel 4, “Heat flow without electrical shorts”: show one generic power component and separate net-specific copper regions, with a surrounding translucent thermal halo. Orange arrows indicate heat spreading only, with the legend “Heat flow — not electrical wiring”. Keep conductors on different nets visibly separated; do not join all component terminals to a common slab. Add “Thermal paths and any vias depend on the selected package and reviewed stack-up”. No fixed layer count, via count, geometry or temperature result.

MUST NOT show: input capacitors from VIN to SW; a VIN-to-PGND wire bypassing CIN; the inductor/output capacitor inside the input commutation-loop highlight; both buck switches conducting together; two-terminal force-wire taps labeled four-terminal Kelvin sensing; raw buck output substituted for VOUT_PROTECTED; electrically shorted thermal copper; principles deferred until routing is finished; or an approved/routed PCB.

Style: uncluttered vector panels, white background, dark electrical wires with clear junction dots, teal load-current arrows, purple sense paths and orange heat-flow arrows. Large labels. Footer: “Apply manufacturer layout guidance during design; review actual placement, returns and thermal paths before release”.
```

## D5 — LM61460 feedback principle (REGENERATE)

Target filename: `d5-lm61460-feedback-principle.png`

**OBSERVATION — exactly what is wrong:**

- The red input-power arrow terminates at `Buck controller`; only a blue `PWM / control` arrow connects that box to `Power stage / switch node`. The drawn power stage has no input-power connection. This wrongly makes the PWM signal appear to supply the output power.
- The controller/power-stage split does not identify those functions as internal to LM61460. The power stage also lacks a defined power return.
- The resistor divider itself is correctly drawn from output to ground, with FB at the midpoint; preserve it. However, `Regulated output` is not identified as local `VOUT_5V1`, before the protection/shunt/harness, so the drawing does not establish the project's actual feedback boundary.

**EVIDENCE:** CTX architecture/buck review; G4-CHANGE retains local regulation.

```text
Create a landscape conceptual diagram titled “Buck Feedback — Local Output Regulation”. Intended replacement filename: d5-lm61460-feedback-principle.png. Show one large functional boundary labeled “LM61460 — controller + integrated power switches”. This is an electrical principle, not a pinout or PCB.

Inside the boundary, draw a small controller and a synchronous half bridge. The power-stage connections are explicit: VIN_PROTECTED feeds the high-side switch; that switch ends at SW; the low-side switch connects SW to PGND. PGND returns to the input source. A local CIN is connected across VIN_PROTECTED and PGND. The controller drives the switches using thin dashed control arrows only. The energy path comes from VIN_PROTECTED through the high-side power switch, not through the control arrows. Do not draw both switches on simultaneously.

Outside the boundary, SW → L → a junction labeled “VOUT_5V1 — local regulated output”. COUT connects from that junction to the power return. Continue the output rightward to a dashed text box “Downstream protection, shunt and load — outside feedback loop”. Do not detail Sheet 03 in this image.

Draw a vertical divider from VOUT_5V1 through R_TOP to a clearly dotted FB junction, then through R_BOTTOM to the quiet analog ground reference. Connect that ground reference to the same circuit ground in the abstract topology; do not imply a separate floating ground or a specified PCB tie location. A thin purple sense line connects ONLY the divider midpoint to the controller's FB input. Label “FB — sensitive analog node” and “Keep feedback away from SW”. The upper resistor must remain between VOUT_5V1 and FB. Do not connect FB directly to the output. Route the sense line well away from the switching-node drawing.

Use two short explanatory statements: “Output falls → controller increases energy delivery” and “Output rises → controller reduces energy delivery”. Add “Local sensing does not compensate downstream protection or harness drops”. Omit resistor/capacitor values and exact nominal-voltage precision. Footer: “Illustrative feedback principle; check captured values and final layout against the current schematic and datasheet”.

MUST NOT show: input power stopping at a controller with an unpowered power stage; PWM/control arrows carrying load power; separate external LM61460 power switches implied by the drawing; FB wired directly to VOUT or SW; sensing beyond the disconnect/shunt/harness; an absent power return; or fabricated PCB geometry.

Style: white background, clean vector symbols, thick teal power paths, dark return wires and thin purple signal paths. Use junction dots only where wires connect. Give power and signal arrows a clear legend; keep all labels large and sparse.
```

## E1 — Capacitor behavior and effective capacitance (REGENERATE)

Target filename: `e1-capacitor-behavior-and-effective-capacitance.png`

**OBSERVATION — exactly what is wrong:**

- The `Parallel capacitors` panel uses blue component bodies with a wire entering each body's top and both drawn lower leads on the lower bus. This reads as a three-terminal object or both real capacitor leads on the same node; it does not unambiguously show a two-terminal capacitor across two distinct nets.
- The ideal capacitor and series ESR–C–ESL model are correctly recognizable; preserve their topology. The DC-bias curve is labeled conceptual, but its generic title can imply that every ceramic dielectric has the same DC-bias behavior. Qualify the example as Class II ceramic and keep it unscaled.

**EVIDENCE:** CTX buck review distinguishes nominal/effective capacitance, bias and qualification. This is generic teaching, not a V1A bank drawing.

```text
Create a landscape four-panel teaching infographic titled “A Ceramic Capacitor’s Nominal Value Is Not Its Effective Value”. Intended replacement filename: e1-capacitor-behavior-and-effective-capacitance.png. Use schematic symbols rather than realistic capacitor bodies.

Panel 1, “Ideal C and real impedance”: show an ideal TWO-TERMINAL capacitor symbol. Beside it, show the simplified two-terminal real model as terminal A → ESR resistor → ideal C → ESL inductor → terminal B, all in series. Label “ESR: equivalent series resistance” and “ESL: equivalent series inductance”. No conductor may cross the dielectric gap or bypass any element. Note “Simplified equivalent circuit”.

Panel 2, “Class II ceramic: conceptual DC-bias effect”: draw a qualitative falling curve with horizontal axis “DC bias” and vertical axis “Effective capacitance”. Include “Conceptual — not a part-specific curve”. No numeric ticks, percentages or universal loss factor. Add “Behavior depends on dielectric and exact part”. Do not imply this same curve applies to every ceramic dielectric.

Panel 3, “Capacitors in parallel”: draw exactly two standard non-polar capacitor symbols C_A and C_B as separate vertical branches. Use two visibly separated horizontal rails labeled “NODE A” and “NODE B”. For EACH capacitor, its upper plate has exactly one wire to NODE A and its lower plate exactly one wire to NODE B. The plates are separated by a visible gap. Put junction dots at the four rail connections. There is NO direct wire between NODE A and NODE B and no third component lead. This is a generic two-capacitor example, not the V1A bank count. Add “Nominal parallel sum: C_A + C_B” and “Effective sum uses each capacitor at the same operating conditions”.

Panel 4, “Check the operating conditions”: list “DC bias”, “Tolerance”, “Temperature”, “Aging” and “Frequency”. Explain briefly “ESR and ESL also affect impedance; nominal capacitance alone is insufficient”. Footer exactly: “Use the exact manufacturer curve and operating conditions”.

MUST NOT show: both leads of a capacitor on the same rail; a third lead entering a capacitor body; a wire shorting the two rails or bridging capacitor plates; a series string labeled parallel; a V1A bank count or effective-capacitance number; or an unqualified curve presented as universal manufacturer data.

Style: white background, clean vector circuit symbols, black wires, clear junction dots, blue conceptual curve and large concise labels. No photo-like parts, model numbers, invented measurements or precision.
```

## E2 — LM61460 placement principles (REGENERATE)

Target filename: `e2-lm61460-placement-principles.png`

**OBSERVATION — exactly what is wrong:**

- In the input-capacitor group, an extra left-hand wire joins the VIN rail directly to the grounded lower rail. It bypasses the capacitor symbols and shorts the depicted input supply to PGND.
- The purple feedback line connects regulated VOUT directly to FB. The required divider is absent, so this teaches the wrong connection for the project's adjustable LM61460 circuit.
- The red dashed “short switching loop” reaches SW through free space but does not identify the input capacitor/half-bridge/PGND commutation loop. It can be mistaken for an additional electrical connection or a complete current path.
- The rectangular pseudo-package with positioned pads can be read as a physical pin arrangement. The L201 “not selected” text also needs the more precise current status: 10 µH development direction, qualification candidate, qualification OPEN.

**EVIDENCE:** CTX buck review; G4-CHANGE S02-01 through S02-04.

```text
Create a landscape teaching diagram titled “LM61460 Placement Principles”. Intended replacement filename: e2-lm61460-placement-principles.png. Include “CONCEPTUAL — NO PCB ROUTED”. Use a functional power-stage drawing with translucent placement zones, not an IC footprint or board render. Ports are functional labels, with no physical pins, pads or package outline.

Define distinct nodes VIN_PROTECTED, PGND, SW, VOUT_5V1 and FB. Local CIN connects from VIN_PROTECTED to PGND through its capacitor symbol only; there is NO uninterrupted wire between these rails. Inside an “LM61460 — integrated switches” boundary, high-side switch connects VIN_PROTECTED to SW and low-side switch connects SW to PGND. SW connects through L201 to VOUT_5V1. COUT connects VOUT_5V1 to PGND. Connect the input source and output load to their corresponding positive and return nodes. Show representative capacitor symbols only, labeled “bank represented; count/value omitted”.

Shade a compact red zone around local CIN, the internal half bridge and its PGND return. Label “High di/dt commutation loop — minimize area”. Use a closed dashed boundary, not a fake wire/current path, and keep L201/COUT outside that loop. Add “Provide local bypass at each VIN/PGND pair; consult actual pinout”. Do not draw both switches on together. Shade the inductor/output forward and return paths teal for “High DC current”; keep the SW copper concept compact.

Draw the feedback divider explicitly: VOUT_5V1 → R_TOP → FB junction → R_BOTTOM → quiet analog ground reference. Thin purple wiring goes from the divider midpoint to LM61460 FB. The ground reference belongs to the same circuit ground; this diagram does not prescribe a physical ground split or tie location. Place this divider/sense route in a separate purple “Sensitive feedback” zone, away from SW and the inductor. Label “Local sense before output protection — not remote sense”.

Label the inductor “L201: 10 µH alloy development direction” with a second line “Würth 74437636351002 — qualification candidate; OPEN”. Do not draw its package or claim final placement. Footer: “Check exact pinout, footprint and layout against the current datasheet and captured schematic”.

MUST NOT show: any direct VIN-to-PGND short or bypass around CIN; VOUT wired straight to FB without R_TOP; feedback taken from SW or beyond output protection; the output inductor/capacitor inside the input commutation-loop highlight; an open dashed arrow mistaken for a wire; invented pad positions, trace dimensions or capacitor counts; or a qualified/routed board.

Style: restrained vector line diagram, white background, dark electrical connections, explicit junction dots, red/teal/purple translucent zones and large labels. Separate electrical wires from explanatory leaders and zone boundaries. No decorative circuitry or invented test results.
```

## E3 — Protection states and fault response (REPLACE)

Target filename: `e3-protection-states-and-fault-response.png`

**OBSERVATION — exactly what is wrong:**

- `Fault detected` conflates overvoltage, undervoltage and “other protection event”, with a solid arrow straight to the crowbar. Ordinary power-good loss/undervoltage must not be taught as an instruction to fire the crowbar.
- The crowbar has arrows from detection, the latch and the series-disconnect state, with no legend distinguishing commands, states or timing. This obscures independent/parallel actions and could imply the series switch must finish opening before crowbar action.
- The named `REF5025 → TLV3201 → 74LVC1G74 → LTC7001` chain is placed under all fault detection. REF5025 is a comparator reference and LTC7001 drives the series pair; the drawing does not distinguish the UCC27511 protected-crowbar branch.
- Timed TPS26630 source isolation and Gate 4a's separate proposed raw-side dump are missing. The protected crowbar cannot absorb upstream L201/raw-bank energy through an already-open opposed pair.
- The return loop says manual review/re-arm but does not state persistent-fault inhibition, safe stored-energy state, valid rails or a fresh ARM edge. Those are material conditions, not an automatic return to normal.

**EVIDENCE:** G4-BASIS, G4-CHANGE and G4-BENCH. The new logic/raw dump is a proposal with unresolved capture and timing, not a completed implementation.

```text
Create a landscape engineering state-and-action diagram titled “Protection States and Fault Response — Architecture D”. Intended replacement filename: e3-protection-states-and-fault-response.png. Use the exact banner “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)” and footer “Dummy load only — Pi disconnected”. Add “Functional policy/proposals — implementation and timing OPEN”.

Separate three areas: operating states, fault-response actions, and a small power-topology inset. Use solid black arrows only for state transitions, dashed purple arrows only for commands, and solid teal lines only for power connections. Add that legend. Horizontal positions do not represent elapsed time.

States: “Unpowered / disarmed” → “Rails valid + fresh ARM; buck starting; series OFF” → “Armed normal; buck PG valid; series ON”. Genuine overvoltage leads to “FAULT HELD — no automatic restart”. Show a separate ordinary-PG-loss branch to “Disarmed; series OFF; crowbars OFF”. Write “PG loss alone does not fire crowbars; a simultaneous genuine fault retains priority”. From FAULT HELD, go to “Record voltage/current/temperature” → “Manual review”. Permit a return to disarmed only through “Fault removed + stored energy safe + rails valid; reset, then fresh ARM”. A persistent fault, returning input or held ARM must not lead directly to normal.

Fault actions are PARALLEL branches, with no completion arrow from one actuator to another. Show REF5025 feeding the reference input of a TLV3201 raw-output overvoltage detector, and a separate “VOUT_5V1 divider” feeding its sense input. Detector/qualification logic feeds “74LVC1G74 fault latch — holds fault”. One command removes RUN to “LTC7001 → 2 × BSC034N06, back-to-back; series OFF”; note “RUN removal need not wait for latch propagation”. A second latched-fault command goes to “UCC27511 → CSD18540Q5B + drain ballast; protected crowbar”. A third dashed amber branch says “Separate raw-node dump — Gate 4a proposal; implementation/qualification OPEN”. Do not invent pin-level logic, rail voltages, thresholds or delays.

Include a separate amber box “Independent source-fault trigger → TPS26630 SHDN; timed source isolation — implementation/bounds OPEN”. Do not make the raw-output OV detector the sole guaranteed source-cutoff trigger. Add “Bench-timed cutoff is a conditional test mode, not proof of autonomous containment”.

In the power inset, draw LM61460/L201 → VOUT_5V1 → architecture-D opposed series pair → VOUT_PROTECTED → 2 mΩ shunt → LOAD_5V1 → dummy load, with its GND return. From VOUT_PROTECTED draw a SHUNT branch through drain ballast and the protected crowbar switch to GND. From VOUT_5V1 draw a separate dashed amber raw-dump-to-GND branch labeled “PROPOSED / OPEN”. No line may bypass the series pair. Keep command arrows visually distinct from these connections. Label “Protected crowbar cannot receive upstream energy after series isolation”. TPS26630 belongs upstream of the buck, not in the 5 V output path.

Add “Actual fault-onset timing, source energy, clamp behavior and voltage margins remain OPEN” and “CONCEPTUAL — NO PCB ROUTED”.

MUST NOT show: undervoltage/PG loss alone firing a crowbar; series-off completion as a prerequisite for crowbar action; LTC7001 driving the crowbar; REF5025 carrying load power; a crowbar in series with the load; an open series pair still feeding upstream energy to the protected crowbar; the raw dump or independent source trigger as captured/qualified; automatic retry into a persistent fault; Option E, supercapacitor backup, a Pi or invented fault waveforms.

Style: clean white-background vector blocks, readable sparse labels, distinct command/state/power legends and amber proposed items. Planned behavior only; no PASS checkmarks, safety claim or numeric margin.
```

## D1 — KiCad sheet map (REGENERATE)

Target filename: `d1-kicad-sheet-map.png`

**OBSERVATION — exactly what is wrong:**

- `Sheet 06 I/O and Control`, `Sheet 07 Test Access` and `Sheet 08 Power and Ground` are invented. The checked root contains exactly five child sheets, 01–05.
- `Sheet 05 Load Connector` is an incorrect/narrow sheet identity. The real sheet is `05_IO_TEST.kicad_sch` and includes load/host connections and test access; it is not just an output connector.
- The picture calls itself a hierarchy map but omits the actual root and filenames, then mixes power-flow arrows and support-function arrows. It must distinguish file hierarchy from the functional current path.
- The monitoring block is placed in the main power chain without identifying the shunt as the series element and INA228 as a sense branch. Clarify that distinction so the map cannot be read as load current flowing through monitor inputs.

**EVIDENCE:** G4-SHEETS and CTX overview for hierarchy; G4-BASIS/G4-CHANGE/TVS for current annotations.

```text
Create a landscape hierarchy-and-function map titled “V1A Schematic Sheets and Their Functions”. Intended replacement filename: d1-kicad-sheet-map.png. Use three separated bands: external source context; actual KiCad file hierarchy; functional power flow. Different line styles must distinguish hierarchy from electrical flow.

In the external-source band, show exactly “13S battery” → “PDB” → “Bought isolated 48 V → 24 V module — NOT SELECTED” → “V1A input: 9–26 V DC”. Label the entire band “External integration context; module fault behavior OPEN”. Do not connect the battery directly to V1A or choose a converter model.

For the ACTUAL FILE HIERARCHY, show one root box “V1A.kicad_sch” and exactly FIVE child boxes connected by thin grey parent-child lines with no power arrows. Render these five filenames exactly, with the descriptions beneath:
“01_INPUT_PROTECTION.kicad_sch” — “Input fuse, TVS, reverse protection, TPS26630”.
“02_BUCK_5V.kicad_sch” — “LM61460; local approximately 5.1 V regulation”.
“03_OUTPUT_PROTECTION.kicad_sch” — “Architecture D; independent output fault protection”.
“04_POWER_MONITOR.kicad_sch” — “2 mΩ Kelvin shunt, INA228, local supply and I2C interface”.
“05_IO_TEST.kicad_sch” — “Load/host connectors and test access”.

Attach the exact banner “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)” to child 03. Attach a small text-only note to child 01: “D101: Littelfuse SMCJ36CA; F101: Schurter 3403.0285.23 — owner-selected; qualification OPEN”. These identities describe the newer proposed capture basis, not proof that all replacements are fitted in the checked schematic. Add “Hierarchy verified; change proposals are not all captured”. Do not draw component-level wiring inside the hierarchy boxes.

In the separate FUNCTIONAL POWER FLOW band, use solid teal arrows: “Input protection” → “LM61460 / VOUT_5V1” → “D series disconnect” → “VOUT_PROTECTED” → “R401 force path, 2 mΩ” → “LOAD_5V1 / J502 / dummy load”. Below R401, use two thin purple sense lines to “INA228”; it must not carry the load current in series. Show I2C and test access as support annotations associated with existing Sheets 04/05, not as new sheets. Do not expand the full fault circuit in this hierarchy illustration.

Status notes: “Application margins OPEN”; “CONCEPTUAL — NO PCB ROUTED”; “Pi disconnected until all applicable dummy-load, fault and telemetry gates pass”. Footer: “NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED”.

MUST NOT show: Sheet 06, Sheet 07 or Sheet 08; a separate power/ground sheet; a sixth child sheet; Sheet 05 named only Load Connector; root V1A.kicad_sch counted as an extra functional child; hierarchy lines used as wires; load current through INA228 inputs; a 5 V or obsolete 9–24 V V1A input; SMBJ26CA or F101 OPEN presented as the current selection; an empty/unimplemented Sheet 03; or a routed board/validated design.

Style: clean vector blocks, white background, navy labels, grey hierarchy lines, teal power arrows, purple sensing and amber OPEN notes. Keep filenames readable and exact, with generous space. Do not invent pins, component values, connector models, extra sheets or completed-gate marks.
```

## Review before replacing the lesson files

Check each generated image against its prompt, not just its caption: trace every supply/return, capacitor terminal, FB divider and Kelvin connection; verify each state/command arrow and every sheet filename. Reject any generation that reintroduces a listed error, adds unsupported ratings, or implies a proposal is captured/validated. Confirm the eight filenames above match the lesson targets exactly. Replacement of images and publication are outside this documentation-only task; no electrical gate is closed by these prompts.
