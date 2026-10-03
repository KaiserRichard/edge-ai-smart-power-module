# V1A test-board PCB layout guide — KiCad 9

**PRELIMINARY. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

For the owner moving from EasyEDA to KiCad. This is a drawing guide, not an R2/R3 release. Follow the steps when the relevant layout work is authorized. No electrical gate is closed by this document.

**OBSERVATION:** the current Gate 4B snapshot is a partial test-board capture. It uses 9–26 V input, a 10 µH Wurth 74437636351002 inductor, SMCJ36CA, Schurter 3403.0285.23, the BSC034 pair, and Architecture D. J603 supplies a manual source-fault trigger; JP600 supplies manual rail-valid permission. Autonomous source detection and the complete automatic interlock are not captured. The Gate 4a freeze remains BLOCKED. Older context, inherited JSON notes and path-budget proposals must not silently replace these choices.

**REQUIREMENT:** approximately 5.1 V / 5 A output target; no extra peak-current rating. **CALCULATED:** local setpoint 5.098361 V. Electrical behavior, thermal limits and fault containment remain **OPEN**, not measured. Keep the raw, protected and load rails separate.

1. **Open the existing project.** Open `hardware/kicad/V1A.kicad_pro`, then its schematic and PCB Editor. Retain `V1A_Qualified.pretty`, `fp-lib-table` and `sym-lib-table`. A symbol is the schematic part; a footprint is its physical land pattern; a net is an electrical connection; the ratsnest shows connections still needing copper. Save the eventual board beside the project as `V1A.kicad_pcb`.

2. **Transfer the schematic.** Choose **Tools → Update PCB from Schematic** (F8). Review the change list, update, then place the footprint group outside the planned outline. Resolve missing footprints upstream; do not substitute a similar-looking package. Repeat after approved schematic changes. Use **Help → List Hotkeys**: useful defaults are M move, R rotate, E properties, X route, V via while routing, B refill zones, Esc finish/cancel. [KiCad tutorial, Part 3](https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html#tutorial_part_3_circuit_board).

3. **Draw the outline.** Select `Edge.Cuts`; draw one closed, nonintersecting outline. Use a **PRELIMINARY** 0.5 mm placement grid, refining locally for pad access. Board dimensions and mounting holes are **OPEN**: reserve connector mating/tool access, M4 hardware and the inductor's 36 × 35.7 mm body / 34.2 mm maximum height before deciding size. A courtyard is assembly space, not a copper keep-out.

4. **Set the four-layer stack.** In **File → Board Setup → Physical Stackup**, select four copper layers. Use the requested **2/1/1/2 oz** copper, approximately **70/35/35/70 µm**. Obtain the fabricator's finished thicknesses and dielectric stack before release; **1.6 mm total thickness is only a PRELIMINARY assumption** for the via example below. [KiCad PCB Editor](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#board_setup).

    | Layer | Intended use |
    | --- | --- |
    | F.Cu — 2 oz | Components, compact switching loops, broad power and return copper |
    | In1.Cu — 1 oz | Continuous GND directly below the buck; do not route signals through it |
    | In2.Cu — 1 oz | Local VIN strap joining U201's two input sides; quiet signals outside the power area |
    | B.Cu — 2 oz | Mostly GND heat spreading and broad return copper; reviewed power reinforcement if needed |

5. **Enter rules before routing.** In Board Setup, use **Design Rules → Constraints**, **Net Classes**, and **Pre-defined Sizes**. **PRELIMINARY drawing defaults:** 0.20 mm track minimum, 0.20 mm clearance, 0.50 mm copper-to-edge, 0.60/0.30 mm via diameter/drill. Confirm heavy-copper fabrication capability, package clearances, plated slots and actual voltage/transient spacing. These defaults are not an insulation qualification. Do not shrink manufacturer pads to clear a warning.

6. **Assign net classes explicitly.** Select actual imported names, including hierarchical prefixes such as `/02_BUCK_5V/`. Check the assignment preview; avoid a broad `*V*` rule. Net-class track widths are routing defaults, not enforced minimums; custom rules and manual inspection must protect critical widths. A zone needs its own net and clearance settings. [KiCad net classes](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#board-setup-net-classes).

    **All sizes below are PRELIMINARY.** Only the two copper geometries in step 18 come from the path budget; other widths are placement/routing starting points.

    | Class / nets | Width and routing rule |
    | --- | --- |
    | `POWER_5A`: `L201_OUT`, `VOUT_5V1`, `PROT_MID`, `SERIES_OUT`, `VOUT_PROTECTED`, `LOAD_5V1`, `LOAD_FIXTURE` | Aim for 15 mm broad outer-layer copper over the module path; 10 mm for the short unsensed buck allowance. Count every pad escape and neckdown. |
    | `INPUT_POWER`: `VIN_RAW`, `VIN_FUSED`, `VIN_EFUSE_IN`, `EFUSE_OUT`, `VIN_PROTECTED` | Start with short 5 mm pours, widening where possible. Input and fault-current capability need separate verification; the output path budget does not qualify these. |
    | `SWITCH`: `BUCK_SW`, `L201_IN`, `AUX_SW1`, `AUX_SW2` | Start with 1 mm short escapes, widen to the actual power pads. Minimize exposed switching area; do not flood a whole layer. Final width/current check OPEN. |
    | `FAULT_POWER`: ballast intermediate nets, `CB_BALLAST_OUT`, `CB_DRAIN`, `RAW_BALLAST_OUT`, `RAW_DUMP_DRAIN` | Reserve broad, direct copper, initially 15 mm corridors where practical. Size each branch for its pulse and return path; **5 A rules do not qualify these nets**. |
    | `SENSE`: `SHUNT_KPLUS`, `SHUNT_KMINUS`, `INA_IN_PLUS`, `INA_IN_MINUS`, `BUCK_FB`, reference/divider nodes | 0.20 mm; short, quiet, no force current. Kelvin rules in step 20. |
    | `GATE_AUX`: gate-drive nets and auxiliary supply rails | 0.50 mm starting width; local decoupling and tight gate/source returns. Auxiliary switching nets belong in `SWITCH`. |
    | `SIGNAL`: I2C, status, ARM/reset and other logic | 0.25 mm; reference continuous GND and stay clear of switching/ballast areas. |
    | `GND` | Plan broad return zones, not a signal-width daisy chain. Use step 18's return budget. |

7. **Place the input chain first.** Put J501 at an edge, then F101, D101, Q101/Q102 and U101. D101 is a shunt from `VIN_FUSED` to GND, not a series part. Keep its surge-return route close to the input return so surge current does not cross the monitor area. Preserve the separate auxiliary feed from `VIN_FUSED` through D303.

8. **Compact the eFuse block.** Put Q101's drain beside U101 IN pins 1/2; Q102 beside Q101's gate/source. Put C101 near IN_SYS/GND, C102 near IN/GND, and the setting resistors/C103 beside their pins. Keep ILIM clear of switching fields. TI calls for power-path capacity of at least twice the actual full-load current through this input stage; do not confuse that with 5 A output. [TPS2663, §9.6, QFN Figure 9-18](https://www.ti.com/lit/ds/symlink/tps2663.pdf#page=38).

    Keep JP101 between `EFUSE_OUT` and `VIN_PROTECTED`; all main buck input capacitors are on its downstream side. D102 also remains on `VIN_PROTECTED`. Place it tightly at that protected-node return. This test-link arrangement differs from TI's uninterrupted OUT example: its commutation parasitics require review, not a copper bridge across JP101.

9. **Place the buck hot loop before the large inductor.** Open [LM61460 Figure 11-2, p49](https://www.ti.com/lit/ds/symlink/lm61460.pdf#page=49). Orient U201 so C203 spans pins 8–9 and C204 spans 12–11, immediately beside the package. Put C201/C202 behind those bypasses. Keep each capacitor → VIN → internal switches → PGND → capacitor loop short on F.Cu. Do not put JP201 or the inductor inside these input loops. This mapping follows the [captured buck contract](../evidence/r2/gate4b/buck_block.json).

10. **Place the buck support parts.** C205 and R204 belong beside CBOOT/RBOOT; C205 returns to native `BUCK_SW`, never `L201_IN`. Use TI's bootstrap routing corridor between VIN2 and RBOOT. C206 belongs beside VCC/AGND. Put R202/R203, R205/C207 and R201 on the quiet side. Take feedback from the local `VOUT_5V1` capacitor node, before protection; return R203/C206 locally to AGND. Retain the captured grounded BIAS connection. [TI layout guidance, pp47–49](https://www.ti.com/lit/ds/symlink/lm61460.pdf#page=47).

11. **Fit L201 and its links.** Arrange `U201 SW → JP201 → L201 → JP202 → raw output bank`. Keep each copper segment direct; leave bolt, strap and probe access. JP201/JP202 are removable M4 force links, not ordinary signal jumpers. **OPEN RISK:** the large inductor, PF3/PF4 and links enlarge switching geometry compared with TI's example. Review the actual loop/strap inductance and noise; never delete the links or bypass them to imitate the reference board.

12. **Place output capacitors next.** C209–C214 connect on the `VOUT_5V1` side of JP202. Place the raw bulk bank C330–C337 beside the raw power/disposal area. Keep capacitor return connections broad and close to their associated power paths. C340–C343 form the separate protected bank; do not accidentally join the positive copper of the two banks.

13. **Place Sheet 03 power protection.** Put Q301/Q302 together along the raw-to-protected path, followed by JP301. Put U301, C301, gate resistors and local bypasses close to the pair; C301/driver TS return to `PROT_MID`, not GND. Cluster raw ballast/Q330/U330/JP331 with the raw bank, and protected ballast/Q303/U315/JP330 with the protected bank. Keep each discharge loop local, with balanced copper for parallel ballast strings. Ballast is in the drains; do not move it into source returns.

14. **Place Sheet 03 supplies and controls.** Group U316/Q316/R332, U317/L301, U327/held capacitors, and detector/SAFE5 circuits as separate functional clusters. U317 is another switching converter: its own manufacturer layout review is required before routing it. Keep references/comparator dividers away from both inductors and hot ballast. Keep each logic bypass beside its supply pins. Give J301/J302/J603/J604, JP600 and JP660 accessible, clearly labelled positions. Manual controls do not establish automatic fault protection. [Gate 4B pin review](../evidence/r2/gate4b/PIN_REVIEW.md).

15. **Place the shunt, then INA228.** Put R401 in the protected output path close to J502. Its force pads are **1 = `VOUT_PROTECTED`, 4 = `LOAD_5V1`**; sense pads are **2 = `SHUNT_KPLUS`, 3 = `SHUNT_KMINUS`**. Put U401 on the quiet side, R402/R403 and C401 at its inputs, and C402 at VS/GND. Keep heat from the buck and ballast away from this group. [Monitor contract](../evidence/r2/gate4b/monitor_block.json); [INA228 Figure 10-1](https://www.ti.com/lit/ds/symlink/ina228.pdf#page=39).

16. **Finish connectors and test access.** Face J502 outward for its Phoenix 1777989 mate and screwdriver access. Put J503 near the quiet interface circuitry; preserve separate host/local 3.3 V domains. JP501 feeds `LOAD_FIXTURE`, while J502 remains on `LOAD_5V1`: removing JP501 alone does not isolate J502. Place test pads where probes can reach them without crossing hot parts; do not lengthen the buck loop for a convenient probe position.

    **Check actual return nets:** TP314 and TP334 return to `PROT_MID`; TP335 spans `CB_BALLAST_OUT`/`CB_DRAIN`; TP336 spans `RAW_BALLAST_OUT`/`RAW_DUMP_DRAIN`. These are not GND pairs. Label both pads. An earth-grounded probe clip on these returns can alter or short the circuit. Use the reviewed differential measurement arrangement. Small sense pads never carry load or injection current.

17. **Route in this order.** Route buck bypass/bootstrap loops; short switching paths; gate/source loops and local bypasses; force paths and disposal returns; Kelvin/feedback/reference routes; auxiliary/logic/I2C. Adjust placement whenever routing creates a long loop or narrow power bottleneck. Do not let an autorouter decide switching-loop geometry.

18. **Use the 5 A path budget as a resistance target.** These are **PRELIMINARY ASSUMPTIONS**, not ampacity ratings. Length is the total copper path per leg, not a fresh allowance for every net between parts. Use actual geometry when longer or narrower.

    | Copper allowance, each SEND and RETURN leg | Nominal geometry: length × width × thickness | Calculated at 85°C with stated tolerances | Hot target |
    | --- | --- | --- | --- |
    | Module copper | 30 mm × 15 mm × 70 µm | 0.895 mΩ | ≤1.0 mΩ per leg |
    | Additional unsensed buck copper | 10 mm × 10 mm × 70 µm | 0.448 mΩ | ≤0.5 mΩ per leg |

    Calculation: `R = ρ L/(w t)`, with `ρ20 = 1.724×10⁻⁸ Ωm`, copper coefficient `0.00393/K`, length +10%, width −5%, thickness −20%. At 5 A, 1 mΩ costs 5 mV and 25 mW. Only **0.105/0.052 mΩ** remains respectively for vias and spreading. Inner 1 oz copper alone does not provide the same resistance as these outer-layer examples. Include connector escapes, thermal spokes, slots and link contacts; extra test-board links were not qualified by this budget. Identify the feedback reference boundary to avoid double-counting compensated copper. [Pinned path budget](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/ebe51b9e141588d118d74daf37e65a3bd2307c1f/docs/evidence/r2/path_budget/PATH_BUDGET.md).

19. **Prefer zero series layer changes in the 5 A path.** If unavoidable, calculate the via arrays instead of assuming “one via per ampere.” **PRELIMINARY example:** 1.6 mm barrel length, 0.30 mm finished hole, 25 µm wall copper, 85°C. The conservative thin-wall estimate `Rvia ≈ ρL/(π d t)` gives **1.470 mΩ per via**.

    One entry and one exit array, **32 vias each**, give **0.092 mΩ total** with equal sharing: barely within the module reserve before spreading. For the tighter buck reserve, **64 at each end** give **0.046 mΩ**; shortening/widening copper is another option. These counts are a resistance illustration, not a qualified design or pulse-current rating. Use the real plated-hole minimum, layer span and current distribution; do not perforate the return plane with an impractical array. Signal routes can use individual 0.60/0.30 mm vias; keep Kelvin layer changes paired and minimal.

20. **Route Kelvin sensing as four separate connections.** Only pads 1/4 carry force current. Route pads 2/3 side by side through R402/R403 to U401 pins 10/9; C401 goes across the filtered inputs. Avoid detours, switch nodes, gate traces and ballast returns. No length-tuning serpentine is needed. Take U401 VBUS from `LOAD_5V1`; it is not remote buck feedback. [INA228 §10](https://www.ti.com/lit/ds/symlink/ina228.pdf#page=39).

    **CALCULATED:** 2 mΩ gives 10 mV and 50 mW at 5 A; tolerance ±1%, temperature coefficient ±25 ppm/K. Nominal ranges ±163.84/±40.96 mV correspond to ±81.92/±20.48 A, not permitted board currents. Calibration, offset/noise, temperature drift, pulse survival and measurement accuracy remain **OPEN**. [Captured monitor evidence](../evidence/r2/gate4b/monitor_block.json).

21. **Fill GND and check return paths.** Add a GND zone on In1.Cu and useful outer GND zones; refill with B. Join U201 AGND/PGND through the local ground structure with vias beside bypass returns. Keep switch/input power on the component side of that shield. Preserve continuous GND; do not split “analog” and “power” ground with a slot. Route high-current returns locally by placement and broad copper, away from detector and sense references. [LM61460 §11.1.1](https://www.ti.com/lit/ds/symlink/lm61460.pdf#page=48).

22. **Add specific keep-outs.** Use the rule-area tool and select the intended layers and blocked object types. Keep sensitive tracks out from under L201/L301 and away from switching copper on every routing layer. Preserve the buck's underlying GND shield; do not apply a blanket all-copper void. Keep unrelated copper, vias and components outside bolt/washer/tool envelopes; dimensions depend on the actual hardware and remain OPEN. Inspect every layer for a bypass around R401, Q301/Q302 or a removable force link. Do not enlarge SW copper as a heatsink.

23. **Provide thermal copper on the correct nets.** Spread heat from U101's exposed pad 25 into GND; soldering that pad is required. A **PRELIMINARY 3 × 3 field of 0.60/0.30 mm GND vias** is a placement reservation, subject to package/stencil and fabricator review. Open vias in solder pads can wick solder; agree the fill/cap or adjacent-via process. [TPS2663 §9.6](https://www.ti.com/lit/ds/symlink/tps2663.pdf#page=39).

    U201 has **no extra exposed pad 15**: use its reviewed power lands. Metal-oxide-semiconductor field-effect transistor (MOSFET) drain pads need copper on their drain nets, not GND. D102/D330/D331 tabs are their respective rail cathodes; Q316's tab is `AUX_RAW`. Avoid shorting them through a common grounded heatsink. Use solid power-pad connections where the assembly process permits; otherwise calculate thermal-spoke loss. Review hot spots, ballast pulse heating and inductor clearance; copper area alone does not validate 5 A operation. [Package/pin evidence](../evidence/r2/gate4b/PIN_REVIEW.md).

24. **Run checks after each routing session.** Refill zones, save, then **Inspect → Design Rules Checker**. Check schematic parity, unconnected items, clearances, annular rings, courtyards and outline. Resolve errors; document individual justified exclusions instead of disabling rules. Review filled copper on every layer, including narrow bridges hidden beneath pads. [KiCad DRC](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html).

    For repeatable evidence, after the board exists and zones are saved, run from the repository root:

    ```sh
    mkdir -p docs/evidence/r3/layout
    kicad-cli pcb drc --format json --severity-all --schematic-parity \
      --exit-code-violations -o docs/evidence/r3/layout/DRC.json \
      hardware/kicad/V1A.kicad_pcb
    ```

    On macOS, the executable may be `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`. Use its `pcb drc --help` for the installed version. Rerun Electrical Rules Check (ERC) after any schematic change. Neither ERC nor Design Rules Check (DRC) proves electrical safety. [KiCad 9 CLI](https://docs.kicad.org/9.0/en/cli/cli.html#pcb_drc).

25. **Inspect the physical board.** Open **View → 3D Viewer**. Check connector direction, polarity, pin 1, inductor height, capacitor spacing and tool access. Missing 3D models do not mean the space is empty: compare manufacturer drawings and print a 1:1 footprint/outline view. Mark the board **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**. Save annotated top/bottom/inner-layer views and the open-issue list under `docs/evidence/r3/layout/` when R3 is authorized.

26. **Complete this self-review before handoff.**

    - [ ] U201's two input loops follow TI; bootstrap stays on native SW; feedback stays local.
    - [ ] Every force path and return meets a recalculated resistance budget, including neckdowns, vias and straps.
    - [ ] Raw/protected/load copper and removable-link boundaries remain separate on all layers.
    - [ ] Both disposal paths have local returns and a separate pulse-current/thermal review.
    - [ ] R401 force/sense pads, INA filter and host/local supplies are correct.
    - [ ] GND is continuous; sensitive routes avoid inductors and switching/discharge paths.
    - [ ] Pad numbers, package variants, capacitor polarity, tab potentials and plated slots are reviewed.
    - [ ] DRC/parity results, visual checks, fabrication capability and remaining risks are recorded.

27. **Catch common beginner mistakes.** A disappearing ratsnest does not prove enough copper. A filled polygon may hide a thin neck or disconnected island. A net-class width does not enforce the power budget. A courtyard is not a keep-out. A paired test point is not necessarily signal/GND. More SW copper is not better cooling. A catalogue current rating or clean DRC does not qualify the assembled board. Do not restore old parts, add remote feedback, or raise the setpoint to compensate for routing loss.

28. **Hand back for engineering review.** This guide completes documentation only; **R2/R3 release remains BLOCKED**. Reconcile the partial capture, missing Gate 4B source ledger and automatic-protection limitations before gate advancement. At the actual R3 gate end, update `docs/FINAL_MANAGER_REPORT.md` with status, work, evidence, decisions, open risks and next gate. Preserve the staged bring-up order: visual → continuity/short checks → current-limited supply → no-load → rail verification → low dummy load → increasing load → thermal → ripple → transients → faults → telemetry → SBC. No Raspberry Pi as the first load; no fabrication release here.

**Evidence and provenance — read 2026-10-03.**

| Project input | Exact revision / relevant files |
| --- | --- |
| Layout brief | `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/PCB_LAYOUT_GUIDE.md`, read in full; docs-only, owner-drawn board |
| Current capture | `634dfa319139a4bfe98202cd0a888fb71319074f`: all `docs/context/*` and `docs/evidence/r2/gate4b/*`; component contracts take precedence over inherited stale notes. Archived ERC reports show zero violations; no fresh CAD checks were run for this guide. |
| Gate 4a | `898759e45578f3767721d19eb313312b7d7733a9`, `docs/evidence/r2/gate4a/GATE4A_FREEZE.md`, read using `git show origin/feat/r2-testboard-freeze:…`; blocked integrated freeze, not automatic-circuit capture evidence |
| Path budget | `ebe51b9e141588d118d74daf37e65a3bd2307c1f`, `docs/evidence/r2/path_budget/PATH_BUDGET.md` and `SOURCES.md`, read using `git show origin/feat/v1a-5a-path-budget:…`; use copper assumptions, not its unadopted Architecture E/BSC014/AWG22 proposals |

The following external documents were **REFERENCED**, not copied as circuit/CAD designs. Upstream modifications: none. TI documents retain Texas Instruments copyright; no redistribution license is inferred. KiCad documentation is © KiCad Documentation Contributors, GPL-3.0-or-later or CC-BY-3.0-or-later. Retain these manufacturer/author, URL, revision and section attributions. Downloaded TI PDFs and page renders are isolated in ignored `third_party/documents/layout_guide/`; none is committed. Instructions and calculations here are independently authored. No third-party PCB was reused.

| Source | Document revision and sections studied |
| --- | --- |
| [TI LM61460](https://www.ti.com/lit/ds/symlink/lm61460.pdf) | SNVSBD5D, July 2022; §11.1–11.2, pp47–49, Figure 11-2 visually reviewed; RJR0014A drawing 4223976/H, June 2026 |
| [TI TPS2663x / TPS26630](https://www.ti.com/lit/ds/symlink/tps2663.pdf) | SLVSE94G, June 2024; §9.6, pp38–40, QFN Figure 9-18 visually reviewed |
| [TI INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf) | SLYS021A, May 2022; §9–10, p39, Figure 10-1 visually reviewed |
| [KiCad PCB Editor](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html), [Getting Started](https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html), [CLI](https://docs.kicad.org/9.0/en/cli/cli.html) | 9.0 manuals, documentation revision `152cd19e` (based on 9.0.9); board setup/net classes, tutorial Part 3, PCB DRC. Capture evidence used KiCad 9.0.6. |

**OPEN source gap:** Gate 4B's pin review cites `third_party/gate4b/SOURCES.json`, absent in this snapshot. This guide uses its recorded pin contracts and the primary documents above; it does not claim a complete independent package audit.

## Critical placement per sheet

**Layout-preparation addendum, 2026-10-03. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**EVIDENCE:** refdes and connectivity below use capture `6d25cf28c4d246417c0a89ec89574c702850e069`, after the U316 check: 366 physical references, all five sheets complete as a test-board capture. This supersedes this guide's earlier description of the capture as partial. The current capture also contains `third_party/gate4b/SOURCES.json`; the earlier source-gap note describes the old documentation snapshot. R2 electrical release remains BLOCKED. Manual controls and observation-only sensors remain as captured.

**DECISION:** these are instructions for the owner's later placement. The preparation board has no placement or routing. Preserve the existing project classes `Default`, `HighCurrent`, `Switching`, `Kelvin`, and `Signal`; step 6's proposed names are planning categories, not the imported class names. Their widths/clearance/vias are provisional editor settings, not current ratings.

**REQUIREMENT:** for each row, place the named cluster before convenient test access or the surrounding logic. **Distance convention:** the cited layout sections specify close/short connections without a numeric part-to-part distance. No arbitrary millimetre target is attributed to a manufacturer. Mechanical tool/washer clearances and thermal separation remain **OPEN**. Dimensions in package drawings and example-board outlines are not component-separation requirements. Rows marked **DECISION** translate the captured connectivity into project placement instructions.

### Root sheet — V1A hierarchy

**OBSERVATION:** this sheet contains the five child-sheet interfaces and no physical footprint. It has no independent placement cluster or hot loop; preserve the named inter-sheet connections while placing the clusters below.

### Sheet 01 — input protection

| Critical loop or cluster | Parts that must sit together / placement constraint |
| --- | --- |
| Input surge return — **DECISION** | Keep J501 (Sheet 05), F101 and D101 together at the input. The shunt path is `VIN_FUSED → D101 → input GND return`; keep it away from quiet sensing returns. The D303 auxiliary branch leaves `VIN_FUSED` before U101. |
| Reverse-blocking/eFuse switching — **EVIDENCE** [P1] | Q101 drain pads 5–8 face U101 IN1/2. Q102 drain/source sit next to Q101 gate/source. Put C101 at U101 IN_SYS5/GND8 and C102 at IN1/2/GND. Keep gate turnoff and bypass loops compact; connect EP25 to local GND heat spreading. |
| Settings and output commutation — **EVIDENCE / DECISION** [P1] | R101/R102, R103/R104, R105, R106/R107 and C103 sit beside their UVLO, OVP, ILIM, PGTH and dVdT pins. Give R105 a quiet short return. D102 is downstream of JP101 on `VIN_PROTECTED`; cluster D102/JP101 with the power-stage return. **OPEN:** the link separates D102 from U101 OUT17/18, unlike TI's direct OUT clamp example. Assess the full link/diode commutation loop; retain the isolation boundary. |

### Sheet 02 — main buck

| Critical loop or cluster | Parts that must sit together / placement constraint |
| --- | --- |
| Two input hot loops — **EVIDENCE** [P2] | Place C203 directly at U201 VIN1/PGND1 pins 8/9 and C204 at VIN2/PGND2 pins 12/11. Put C201/C202 just behind them. Each local loop is capacitor → VIN → internal switches → PGND → capacitor. These loops do not pass through JP201 or L201. |
| Bootstrap, bypass and feedback — **EVIDENCE / DECISION** [P2] | C205/R204 sit at CBOOT14/RBOOT13; C205 returns directly to native SW10 before JP201. Use TI's corridor between VIN2 and RBOOT. C206 sits at VCC2/AGND3. R202/R203/R205/C207 and R201 stay on the quiet FB4/RT6 side; sense the local raw output-capacitor node. |
| Switched and output paths — **DECISION** | Keep `SW10 → JP201 → L201 → JP202 → C209–C214` direct, with capacitor returns near U201 PGND. PF3/PF4 and TP201/TP202 must not create long switch-node branches. The M4 links and large L201 differ from TI's example: strap inductance, loop area and probe loading remain **OPEN**. Retain the underlying GND shield; keep sensitive routes away from L201 and switching copper. |

### Sheet 03 — output protection, supplies and controls

This sheet contains several independent fast-current loops. The following groups need individual placement review; placing all of Sheet 03 in one block is insufficient.

| Critical loop or cluster | Parts that must sit together / placement constraint |
| --- | --- |
| Opposed series pair — **EVIDENCE / DECISION** [P3] | Keep Q301/Q302 common sources together on `PROT_MID`, with U301, R304/R305, C301 and D302 adjacent. C301 spans BST9–TS8; TS returns directly to the common sources. Driver charge/discharge paths go through gates and return through TS, not GND. Place C309/C306 at VCC1/GND3, and keep D660/JP660/C660 in the local `SER_DRV` feed. EP11 is GND, distinct from TS. JP301 follows Q302 and retains separation from the protected bank. |
| Protected disposal loop — **DECISION** | `C340–C343 positive → (R308/R309 parallel R310/R311) → JP330 → Q303 drain → source/GND → capacitor negatives`. Cluster D331 with that rail/return. Keep equal branch copper and short broad force returns. Put U315/C308/R306/R307 by Q303, with the gate-drive return landing at Q303 source. Keep ballast heat away from detectors and the shunt. |
| Raw disposal loop — **DECISION** | `C330–C337 positive → two ballast strings → JP331 → Q330 → local bank return`. String A is R380/R381/R382/R383/R386/R387; string B is R388–R393. Put D330 by the raw rail/return. Cluster U330/C367/C368/R384/R385 at Q330. R384/R385 are gate parts, not ballast. **EVIDENCE:** UCC27511 guidance calls for compact gate/bypass loops and a local source/star return [P4]. Neither dump may share a narrow force-return neck with sensing. **OPEN:** [P4] separates its shield plane from gate-current returns with a local star connection; reconcile that local arrangement with step 21 before routing. Do not cut the system GND plane by inference. |
| Auxiliary surge stopper — **EVIDENCE / DECISION** [P5] | Group D303, Q316, R332, U316, R333 and C378/C307. Take separate Kelvin traces from both R332 pads to U316 SNS3/OUT2; do not sense through force-copper drops. R333 belongs at Q316 gate. R330/R331 sit by FB1; C350 by TMR12. Keep the local return quiet. U316 is the checked LT4363-1 MSOP: GND7/9, UV8 tied to VCC; do not use the -2 OV pin map. |
| Auxiliary buck-boost hot loops — **EVIDENCE** [P6] | Group U317/L301/C351/C380 and C352/C377. Input bypass goes at PVIN17/PGND21; output bypass at PVOUT4/PGND21. C353/C379 bypass VCC12/PVCC14 locally. C354 goes at BST1 pin16/SW1 pin18; C355 at BST2 pin15/SW2 pin3, each with a direct Kelvin return to its SW pin. Use the **FE-package Figure 17**, not the DHD pin map. Connect PGND1/10/11/20 and EP21; give the pad a thermal path to GND and keep an uninterrupted GND plane beneath the local power components and loops. Keep R340/R341/R342, R343/C356 and R344/C357 on the quiet FB8/RT9/VC7 side; return small-signal grounds directly to IC GND. L301 and the switching/bootstrap routes must stay away from those nodes. |
| Held-bank charging — **EVIDENCE / DECISION** [P7] | D304/C375 sit at U327 IN5; C376 and C358/C359 on OUT6 `DRV_HOLD`. Keep charging current out of the local pin8 reference return. R375 sits at ILM9, R374/C374 at dVdT7, and R376–R379 by their threshold pins. Use a local quiet ground region with a star connection to power GND. TI calls for ILM parasitic capacitance below 50 pF; this is an electrical limit, not a spacing dimension. IN5/OUT6 are the thermal power lands; no EP11 exists. |
| Detector/control LDOs — **EVIDENCE / DECISION** [P8, P9] | Cluster U306/C305/R312/R313 and U600/C602/C601/R600/R601. Keep each TPS7A16 capacitor on the same side as its IC and directly returned to its GND. Place D600/R602/C600 at the SAFE supply entrance. Group U318/C365/C366, with C366 directly returned to GND2. Local input/output return regions meet at the regulator GND; reconcile these manufacturer local-return arrangements with step 21's continuous system shield before routing. |
| Quiet OV/reference cluster — **DECISION** | Group U302/C302/C303 with U303/C304, U321/C364, R301–R303/R373/R367, D301/D322, and separate D321/R361 clamp. Keep high-impedance nodes short and free of ballast/switching coupling. C302 is U302's reference-output capacitor; the shunt clamp is not that output. Cluster U322/C369/R362/R363 and U323/C370/R364/R365 by their sensed rails. |
| PG and source observations — **EVIDENCE / DECISION** [P10] | Group U607/C604, U651/C651, R622/R623/D618/D619 with D601/R604/R605/R606/C603. Place U640/C640/R640–R642/D640/D641/R651, U642/C642/R644/R645/D642/D643/R652 and U647/C647 as a quiet receiving group. R640 takes a short, high-impedance pickoff from **L201_IN after JP201**; avoid carrying a long, wide switch-node spur into the logic area. Keep comparator outputs away from inputs. These observations do not implement autonomous trip. |
| Memory, manual control and bypasses — **DECISION** | Keep U602/C609/U662/C762 together. Pair U610/C710, U611/C711, U612/C712; U614–U617 with C714–C717; U623/C723, U628/C728, U630–U633 with C730–C733; U644/C644, U654/C754, U656/C756, U661/C761. Put bypasses at supply/GND pins. Keep reset/ARM returns away from discharge copper. Leave accessible J301/J302/J603/J604/JP600, and guarded observations J605/J606. JP600 is absent by default. |

**OPEN RISKS identified while preparing placement:** U315 has C308 = 100 nF but no separately captured local few-µF bypass, whereas UCC27511 §11 recommends both; C358/C359 are shared reservoirs. U306's held-rail input has no separately dedicated bypass in its schematic group; allocate only existing compatible capacitors after engineering review. U327's local C376 = 100 nF differs from the datasheet's ≥1 µF local output-ceramic recommendation. Do not silently add or move schematic connections to resolve these. Distance to shared capacitors, effective capacitance and source impedance need review before routing. Bulk reservoirs are not automatic substitutes for local ceramics.

### Sheet 04 — power monitor

| Critical loop or cluster | Parts that must sit together / placement constraint |
| --- | --- |
| Four-wire measurement — **EVIDENCE / DECISION** [P11] | Keep R401 in the force path between `VOUT_PROTECTED` (pad1) and `LOAD_5V1` (pad4), with U401 on its quiet side. Pads2/3 are Kelvin sense only; route them together through R402/R403 to U401 IN+10/IN−9. C401 bridges the filtered inputs directly beside the IC. C402 sits at VS6/GND7. This is a small measurement loop, not a switching power loop. |
| Local regulator and I2C boundary — **EVIDENCE / DECISION** [P9, P12] | Put C403/C404 at U402 IN1/OUT5, with their returns meeting at GND2. Cluster U403 with C405 at VCCA1 and C406 at VCCB8; R406/R407 stay in the host domain and R404/R405 in the local domain. J503 is beside that interface. Keep monitor/reference copper away from hot ballast and inductors. |

### Sheet 05 — IO and test access

**DECISION:** no switching IC or local converter hot loop is captured here. J501/PF1 join Sheet 01's input cluster; J502 belongs near R401's load-force side, with a broad adjacent return. JP501/PF5/TP505 form the external dummy-load takeoff and return; give the outgoing and return conductors adjacent access. J502 remains energized when only JP501 is removed. Keep J503 near U403, away from force and surge loops. TP501–TP504 should observe their real nodes with short branches; small test pads carry no injection/load current. M4 hardware and Phoenix mate/tool envelopes remain **OPEN**, with no invented keep-out distance. Gate/bootstrap test pairs TP314/TP334 return to `PROT_MID`; TP335/TP336 span their force links and are not GND pairs.

### Placement source register

**Provenance:** all external sources below are **REFERENCED** only. No circuit or third-party PCB is copied, no upstream document is modified. Manufacturer copyright applies; no redistribution license is inferred. Preserve manufacturer, linked document, revision and section attribution. Project refdes mapping and placement decisions are independently authored. Source records and KiCad-library attribution are isolated in `third_party/layout_prep/SOURCES.md` on the capture branch; the table below makes this guide's addition self-contained.

| ID | Manufacturer document / exact revision | Relevant source section |
| --- | --- | --- |
| P1 | [TI TPS2663x](https://www.ti.com/lit/ds/symlink/tps2663.pdf), SLVSE94G, June 2024 | §9.6, pp38–40; QFN Figure 9-18 |
| P2 | [TI LM61460](https://www.ti.com/lit/ds/symlink/lm61460.pdf), SNVSBD5D, July 2022 | §11, pp47–49; Figure 11-2 |
| P3 | [ADI LTC7001](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf), Rev. G | p14, PC Board Layout Considerations |
| P4 | [TI UCC27511](https://www.ti.com/lit/ds/symlink/ucc27511.pdf), SLUSAW9F, November 2014 | §11–12, pp27–28 |
| P5 | [ADI LT4363](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf), Rev. C | pp16–17, Layout Considerations; C1–C3 pin check retains -1 MSOP |
| P6 | [ADI LTC3115-1](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc3115-1.pdf), Rev. E | pp30–32, PCB Layout Considerations, Figures 15/17 |
| P7 | [TI TPS25947](https://www.ti.com/lit/ds/symlink/tps25947.pdf), SLVSFC9C, May 2026 | §8.4, pp62–64 |
| P8 | [TI TPS7A16](https://www.ti.com/lit/ds/symlink/tps7a16.pdf), SBVS171F, October 2015 | §10, pp19–21 |
| P9 | [TI TPS709](https://www.ti.com/lit/ds/symlink/tps709.pdf), SBVS186H, July 2021 | §10.1, p16 |
| P10 | [TI TLV3201](https://www.ti.com/lit/ds/symlink/tlv3201.pdf), SBOS561C, May 2024 | §8.4, p18 |
| P11 | [TI INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf), SLYS021A, May 2022 | §9–10, p39 |
| P12 | [TI TCA9517](https://www.ti.com/lit/ds/symlink/tca9517.pdf), SCPS242D, July 2017 | §11–12, pp15–16 |

LAYOUTGUIDE-HANDBACK
