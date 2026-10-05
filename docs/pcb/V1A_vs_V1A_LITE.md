---
title: "Old V1A to V1A-Lite — what changed, and why"
tags: [v1a, v1a-lite, lesson, schematic, pcb, protection]
---

# Old V1A to V1A-Lite — what changed, and why

The old V1A was a research board with many ways to isolate, observe and control a fault. V1A-Lite keeps the buck converter, replaces the surrounding protection with simpler discrete circuits, and removes onboard monitoring. The saving comes with fewer functions and new qualification work.

> [!warning] Engineering status
> **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
> **KNOWN:** the cited bench plan is **NOT RUN**. Selecting or drawing a circuit does not validate its behavior. A planned test is not a replacement protection component. An electrical rules check (ERC) or design rules check (DRC) cannot prove fault safety. Use a dummy load before any Pi integration.

## How to use this lesson

Read each comparison table with the corresponding schematic page open. A **block** is a group of components doing one job. A **refdes**, such as U201, identifies a component within one version. The same refdes can mean a completely different part in the other version.

**KNOWN — source snapshots and page numbering:**

- **Old circuit authority:** Git tag `v1a-research-schematic`, resolving to `5f371fd7c59e90a5037004b9309bff63b0d95e71`; its `hardware/kicad/*.kicad_sch` files were read with `git show`. The older `docs/context/*` notes are background, not substitutes for this captured circuit.
- **Old PDF page guide:** `docs/schematic/V1A_research_schematic_f11ffbb.pdf` read from `origin/main` at `3c98267a73a4ddf69c00cc45b7fcc891e8b45dec`. Viewer pages: root **1**, input **2**, buck **3**, output protection **4**, monitor **5**, IO/test **6**. This PDF is a separately named snapshot; the tag governs any disagreement.
- **Lite circuit authority:** the worktree schematics at `ee31d04ecba90d29bc69620b0de4659958434001` on `learn/v1a-lite-hand-route`, and [V1A_Lite_schematic.pdf](../schematic/V1A_Lite_schematic.pdf). Viewer pages: root **1**, input **2**, buck **3**, output protection **4**, IO/test **5**. There is **no active Sheet 04**.
- **Learning background:** the read-only [lesson vault](</Users/quockaiser/Desktop/Research/V1A-Lessons/lessons/00-INDEX.md>), especially the glossary, schematic reading guide and output-protection walkthrough. Its older pictures describe their own snapshots.

**KNOWN — an easy trap:** the tagged buck and the old PDF both show R203 as **24.6 kΩ**, although an old note still says **24.4 kΩ** and **5.098361 V**. Those note values are stale. The comparison below uses the component fields, not the stale note. Some context notes also predate the populated output-protection sheet.

The evidence labels mean:

| Label | Meaning here |
| --- | --- |
| **KNOWN** | A captured component/value, recorded requirement, source identity or documented decision. It does not mean measured hardware performance. |
| **CALCULATED** | Arithmetic or a model result, with the stated inputs and limits. |
| **ASSUMED** | A planning convention or a trial input used to explore behavior. |
| **OPEN** | A missing bound, untested behavior or unresolved qualification. |

All refdes, net names, sheet/PDF locations and test identifiers below are **KNOWN document identifiers**. Component values in the comparison tables are **KNOWN captured nominal values**, not measured values. **KEPT** means the named function/core remains; **CHANGED** means its implementation or scope changes; **REMOVED** means the old function or block is absent; **NEW** means a newly introduced block or interface. A changed block can contain removed subfunctions, which are covered in the removal ledger.

## First, follow the power path

**KNOWN — old V1A:** J501 → F101 → reverse-blocking Q101 with Q102/U101 control → U101 input eFuse → JP101 → LM61460 and L201 with research links → opposed output Q301/Q302 → JP301 → R401 measurement shunt → J502. Separate MOSFET discharge branches serve the raw and protected output rails. Sheet 03 also contains auxiliary supplies, memory and manual test controls.

**KNOWN — Lite:** J501 → F101 → Q101 reverse-polarity FET → Q102 forward-cutoff FET → LM61460 and L201 → raw `VOUT_5V1` → F301 → `VOUT_PI` → J502. SCR301 branches from the raw output to GND. The output detector also sends `CB_COLLECTOR` to the input latch, which requests Q102 off. There is no output series transistor or measurement shunt.

**KNOWN — requirement change:** old normal input was **9–26 V**. Lite is intended for **18–26 V**, nominal **24 V**, from an external auxiliary supply. The cited Lite studies examine **54.6–64 V** upstream fault exposure; that is not permission to operate the buck from that voltage or to connect this board directly to a robot battery. Final robot architecture is outside this lesson. Lite's recorded load target remains **5 A**, with settled Pi-terminal voltage **≥4.75 V** and positive peaks **<5.5 V**, including measurement uncertainty. **OPEN:** compliance, peak-current duration, source fault envelope and operating environment.

> [!info] PROMPT F-LITE-1
> **Save as:** `images/flite-1-old-and-lite-power-paths.png`
> **What to show:** Create a clear educational comparison for a fourth-year EE student. Two horizontal power paths on a white background. Old: input eFuse, LM61460 buck, opposed output switches, Kelvin shunt, load; show separate raw/protected MOSFET dump branches and an auxiliary-controls box. Label old source sensing “observation/manual test hooks; no proven autonomous source trip.” Lite: input reverse Q101 and cutoff Q102, LM61460, raw node, F301, load; SCR301 connects raw node to GND before F301. Add a thin control arrow from raw detector/CB_COLLECTOR to upstream latch, then Q102. Put “KNOWN topology; OPEN qualification” on both panels. Use purple for input, orange for raw, blue for load and red for fault commands. The drawing is conceptual, not a wiring guide.
> **MUST NOT show:** a Lite output eFuse, an output series MOSFET, INA228 in Lite, a fuse between raw capacitors and SCR301, automatic validation, USB/data routing, or a Pi used during fault tests.

![[flite-1-old-and-lite-power-paths.png|700]]

## Sheet 01 — input protection

An **eFuse** is an electronic protection controller with a semiconductor power path. A normal fuse opens by melting. Replacing an eFuse with a fuse and discrete transistors does not preserve all its functions.

| Old V1A (block, refdes, PDF page) | V1A-Lite (block, refdes, PDF page) | Status (KEPT / CHANGED / REMOVED / NEW) |
| --- | --- | --- |
| Input backup fuse F101, Schurter 3403.0285.23, **12.5 A** time lag; p. 2 | F101, Littelfuse 0451003.MRL, **3 A**; p. 2. Its clearing must match the actual source and wiring. | CHANGED |
| Upstream transient suppressor D101 SMCJ36CA; p. 2 | D101 SMCJ64CA upstream; D106 TVS3300 at `VIN_PROTECTED`; p. 2. A TVS diverts a transient; it cannot absorb an arbitrary continuous fault. | CHANGED |
| Reverse-input N-channel Q101 CSD19537Q3, small Q102 BSS138 and eFuse control; p. 2 | Common-source P-channel Q101/Q102 IRFR6215TRPBF, **150 V** parts, separate D102/D103 gate clamps; p. 2 | CHANGED |
| Input overvoltage cutoff inside U101 TPS26630, divider R103/R104; p. 2 | U101 **TL431BIDBZR**, R150–R153 detector, Q103 and Q102 cutoff network; p. 2. U101 has changed identity. | CHANGED |
| U101 current limit, R105; controlled startup slew, C103; overload timing/latch behavior; p. 2 | No equivalent input electronic current limiter or programmed slew block; F101 is retained backup only; p. 2 | REMOVED |
| U101 undervoltage/PGOOD qualification, R101/R102 and R106/R107; fault observation R108/TP102; p. 2 | No input-eFuse PGOOD/FLT outputs. Buck uses its own EN divider R206/R207 on p. 3. | REMOVED |
| `INPUT_SHDN` into old U101; Q304 and manual/fault logic on p. 4; input TP101 on p. 2 | `CB_COLLECTOR` → R163 → Q104/Q105 regenerative latch → Q106 inhibits Q103 → Q102 off; p. 2 | CHANGED |
| No equivalent discrete input-latch supply block; old protection supplies are on p. 4 | R110–R125/D104/C102 create upstream `CTRL12`; latch resistors R160–R166 and TP110–TP114 expose its state; p. 2 | NEW |
| C101/C102 **1 µF / 100 V** input capacitors and D102 STPS60H100CT negative-return diode; p. 2 | C101 **100 µF / 50 V** protected-input reservoir; C102 now belongs to `CTRL12`. Old high-current D102 diode function is absent; new D102 is a gate zener; p. 2 | CHANGED |
| JP101 removable force link and TP103 eFuse-output access; p. 2 | Continuous force connection; supply observations TP501–TP503 on p. 5 | REMOVED |

**KNOWN:** Q101 and Q102 in Lite have different jobs even though they use the same part. Turning Q101 off alone does not interrupt positive input current: its body diode still conducts toward their common-source node. Q102 must open to stop forward power. **OPEN:** hot-plug current, cold start into an excessive input, cutoff timing, reverse/backfeed behavior and transistor safe operating area. *Safe operating area* means allowed voltage, current, duration and temperature together; a voltage rating alone is insufficient.

## Sheet 02 — LM61460 buck

You already know the buck's main job: switch the input, use the inductor to shape current, and use feedback to regulate the output. That remains. The surrounding capacitors, inductor and startup interface have changed enough that the old ripple and fault calculations cannot simply be reused.

| Old V1A (block, refdes, PDF page) | V1A-Lite (block, refdes, PDF page) | Status (KEPT / CHANGED / REMOVED / NEW) |
| --- | --- | --- |
| U201 LM61460AANRJRR core; R201 **33.2 kΩ** timing resistor; p. 3 | Same U201 and R201; p. 3 | KEPT |
| Local output feedback R202/R203 **100 kΩ / 24.6 kΩ**; p. 3 | Same ratio and local raw-output sensing; R203 ordering part changes; p. 3 | KEPT |
| Feedforward C207/R205 **22 pF / 1 kΩ**, bootstrap R204 **0 Ω**, grounded BIAS, C205 native-switch-node return and C206 VCC bypass; p. 3 | Same functions/nominal settings; some parts and capacitor voltage ratings change; p. 3 | KEPT |
| L201 Würth 74437636351002, **10 µH** research inductor; p. 3 | L201 Bourns SRP1265A-6R8M, **6.8 µH**; p. 3 | CHANGED |
| C201/C202 **2 × 10 µF / 50 V**, plus C203/C204 local bypass; p. 3 | C201/C202/C215/C216 **4 × 10 µF / 50 V**, with C203/C204 bypass; p. 3 | CHANGED |
| C209–C214 **6 × 22 µF / 50 V** ceramics; p. 3 | C209–C214 **6 × 47 µF / 25 V** ceramics; p. 3. Effective capacitance under bias remains OPEN. | CHANGED |
| Raw bulk C330–C337, **8 × 470 µF / 35 V**, on p. 4 | Raw bulk C217/C218, **2 × 1000 µF / 10 V**, now on p. 3; electrically beside the raw crowbar node | CHANGED |
| Buck EN shares `BUCK_INPUT_PGOOD`; R206/R207 **100 kΩ / 24.9 kΩ**; buck `BUCK_PGOOD` feeds Sheet 03; p. 3 | Independent EN divider R206/R207 **100 kΩ / 24.6 kΩ**; U201 PGOOD explicitly unconnected; p. 3 | CHANGED |
| JP201/JP202, force pads PF2/PF3/PF4 and TP201–TP204 isolate/instrument the inductor path; p. 3 | Continuous switch/inductor/output path; no research force links; p. 3. External fixture and component-pin probing require review. | REMOVED |

**CALCULATED — nominal setpoint**, using the retained ideal feedback reference of **1 V**:

$$V_{raw}=1\left(1+\frac{100}{24.6}\right)=5.06504\ \mathrm{V}.$$

The net name `VOUT_5V1` remains a name; it does not mean the setpoint is exactly **5.1 V** (**KNOWN:** legacy naming). Feedback observes the raw output, so it does not automatically correct the fuse, copper, contact and cable drops between that point and the Pi.

**KNOWN:** the smaller inductor is a different magnetic component, not just the old part at a lower price. **OPEN:** inductance under fault current, effective output capacitance, startup charging, loop stability, ripple and heating. The old assumed research fault-current envelope does not transfer to Lite.

## Sheet 03 — output protection

This is the biggest change. The old sheet separately **detected**, **remembered**, **disconnected** and **discharged**. Lite combines a raw-output SCR discharge path with an upstream cutoff latch. Its output wiring fuse has a different job from the old output transistor switch.

| Old V1A (block, refdes, PDF page) | V1A-Lite (block, refdes, PDF page) | Status (KEPT / CHANGED / REMOVED / NEW) |
| --- | --- | --- |
| Auxiliary surge stopper U316 LT4363/Q316/R332 and D303; p. 4, block 1 | No separate auxiliary surge-stopper branch; p. 4 absent | REMOVED |
| Auxiliary buck-boost U317 LTC3115/L301 and compensation; p. 4, block 2 | No auxiliary switching converter; p. 4 absent | REMOVED |
| Held driver supply U327 TPS259470, C358/C359, D304; `SER_DRV` feed D660/JP660; p. 4, blocks 3/4 | No held gate-driver rail; input latch instead uses `CTRL12` on p. 2 | REMOVED |
| Opposed output Q301/Q302, LTC7001 U301, JP301; p. 4, block 4 | No active series output disconnect or equivalent reverse-current blocker; raw rail reaches load through F301; p. 4 | REMOVED |
| Protected MOSFET crowbar Q303/U315, ballast R308–R311 and return diode D331; p. 4, block 5 | No separate protected-side MOSFET dump; SCR301 is on the raw side; p. 4 | REMOVED |
| Raw MOSFET dump Q330/U330, ballast R380–R383 and R386–R393, return diode D330; p. 4, block 6 | One SCR301 TYN612RG raw shunt, without the old power-ballast strings; p. 4 | CHANGED |
| Protected bank C340–C343 **4 × 470 µF / 35 V**; p. 4 | C301/C302 **2 × 47 µF / 16 V** on `VOUT_PI`; p. 4. Raw bulk replacement is on Lite p. 3. | CHANGED |
| Detector/logic supplies U306 TPS7A1601, U318 TPS70933, U600 TPS7A1601; p. 4, blocks 7/9 | No `DET5`, `3V3_AUX` or `SAFE5`; output detector derives operating current from the observed raw rail; p. 4 | REMOVED |
| Precision reference U302 REF5025, fast comparator U303 TLV3201 and input network; p. 4, block 8 | U301 TL431BIDBZR, divider R301–R304, PNP Q301 BC807 and R305–R308 drive network; p. 4 | CHANGED |
| Guarded analog switches U321/U647/U651, supervisors U322/U323/U602, PG receiver U607 and surrounding logic; p. 4, blocks 7–12 | No manual-valid/PG permission chain; p. 4 absent | REMOVED |
| Fault/main-arm/series-arm memories U610/U611/U612, reset/arm controls J302/J301/J604, manual-valid JP600 and logic; p. 4, blocks 10/11 | Manual controls absent; fault memory is implemented differently by Q104/Q105/Q106 on input p. 2 | CHANGED |
| Manual source trigger J603; observation comparators U640/U642, U647 and TP337–TP340; p. 4, blocks 10/12 | No onboard source-sensing research fixture; use a reviewed external fault injector | REMOVED |
| No corresponding output wiring fuse in the old force path; p. 4 | F301 0451007.MRL, **7 A**, raw output to `VOUT_PI`; p. 4. It is wiring backup, not the SCR-clearing mechanism. | NEW |
| Old dump-current links JP330/JP331, guarded outputs J605/J606 and numerous paired observations; p. 4, block 13 | No dump links/guarded outputs. TP301/TP302 now observe SCR gate/cathode; TP508 observes `CB_COLLECTOR` on p. 5. | CHANGED |

**KNOWN — two critical connections:** SCR301, the output detector's upper divider, Q301 emitter and all raw output capacitors share `VOUT_5V1`. F301 is only in the load branch. If F301 opens, the SCR and detector must remain connected to the raw capacitors. Also, the command to stop input power acts on Q102, independently of the buck's EN, FB, VCC and PGOOD signals.

**OPEN:** there is no demonstrated maximum remote-load peak yet. Disconnecting the input does not erase energy already stored in the buck input capacitors, inductor or output capacitors. The actual SCR pulse and the remote cable/capacitor response still matter.

## Sheet 04 — monitor removed

Telemetry means measurements sent to a host. It helps observe a system; it is not the same function as a fast independent protection circuit.

| Old V1A (block, refdes, PDF page) | V1A-Lite (block, refdes, PDF page) | Status (KEPT / CHANGED / REMOVED / NEW) |
| --- | --- | --- |
| U401 INA228 voltage/current/power/energy monitor; ALERT R408/TP401; p. 5 | No onboard measurement IC or ALERT; no Sheet 04 or corresponding PDF page | REMOVED |
| R401 WSL27262L000FEA Kelvin shunt, **2 mΩ**; filter R402/R403/C401; TP402/TP403 and rail probes TP405/TP406; p. 5 | Continuous output connection, no shunt or replacement resistor; no Sheet 04 | REMOVED |
| U402 TPS70933 local supply, C403/C405/C406 and TP404; monitor decoupling C402/C404; p. 5 | No local telemetry supply/load; no Sheet 04 | REMOVED |
| U403 TCA9517, local/host pullups R404–R407; p. 5; J503 host connector on p. 6 | No I2C endpoint, level buffer or host-reference rail; old host connector absent | REMOVED |

**CALCULATED:** removing the nominal **2 mΩ** shunt avoids its **10 mV** drop and **50 mW** dissipation at **5 A**, from `V = IR` and `P = I²R`. That does not make the replacement copper lossless. **KNOWN:** Lite gives up automatic current, voltage, power and accumulated-energy reporting. External instruments now provide the measurements; no test restores onboard telemetry.

## Sheet 05 — connectors, harness and bench access

| Old V1A (block, refdes, PDF page) | V1A-Lite (block, refdes, PDF page) | Status (KEPT / CHANGED / REMOVED / NEW) |
| --- | --- | --- |
| J501 JST B2P-VH-FB-B(LF)(SN), input; p. 6 | Same exact J501 header; p. 5. Normal input requirement has narrowed. | KEPT |
| J502 Phoenix 1776508 with cable mate 1777989; p. 6 | J502 JST B2P-VH-FB-B(LF)(SN), same part family as input; p. 5 | CHANGED |
| J503 B4B-XH-A host I2C connector; p. 6 | Host interface absent; do not plug a telemetry cable into Lite J503 | REMOVED |
| Dummy-load force takeoff JP501/PF5; p. 6 | J503 is now a copper dummy-load solder-pad pair on `VOUT_PI`/GND; p. 5 | NEW |
| PF1/PF5 force pads and removable JP501; p. 6 | No research force-pad/link arrangement; use the specified connectors/dummy-load pads | REMOVED |
| TP501–TP505 observe old input/load/fixture nets; p. 6 | TP501–TP508 observe input, fused input, protected input, raw output, Pi output, GND, `CTRL12`, `CB_COLLECTOR`; p. 5 | CHANGED |
| Old external TE full-header harness described in p. 6 notes | Revised JST/Harwin harness specified in [PI_HARNESS.md](../evidence/v1a_lite/PI_HARNESS.md), outside the schematic; J502 on p. 5 | CHANGED |

**KNOWN — refdes reuse warning:** old TP301 was raw voltage; Lite TP301 is the **SCR gate**. Old TP502 was protected input; Lite TP502 is **fused input**. Old TP504 was GND; Lite TP504 is **raw output**. Read the new net label before connecting a probe. Test pads carry measurement current only, never the load or SCR discharge current.

**KNOWN — current harness decision:** Pi physical pins **2/4** carry positive power and **6/9** carry returns. The document specifies a JST VHR-2N cable mate, an **AWG18, 150 mm maximum** trunk and matched **AWG22, 50 mm maximum** fanout branches. The Harwin mating housing needs an external mechanical key/carrier because it is not inherently polarized. These are construction specifications, not qualification results. **OPEN:** actual Pi male-contact rating, hot/aged resistance, branch sharing, retention and single-contact-loss response.

> [!warning] Conflicting dated harness numbers
> **KNOWN:** BENCH_TESTS test **5** still says **40 mΩ** hot and **4.95 V** at J502. The later PCB FIX1 section in PI_HARNESS explicitly supersedes that allocation with **25 mΩ** hot/aged round trip.
> **CALCULATED:** at **5 A**, the newer allocation drops **125 mV**, requiring at least **4.875 V** at J502 before further measurement-uncertainty allowance. Use the revised harness allocation when preparing test 5, and retain direct remote-voltage acceptance. The old test text has not been edited by this lesson. **OPEN:** measured compliance; neither allocation is proof that the board/harness achieves it.

## Every removed function: what takes over, and which test checks it?

This ledger follows the [Phase C removed-function table](../evidence/v1a_lite/PHASE_C_CALCULATIONS.md#7-removed-function-ledger-and-bench-qualification--plan-delivered--tests-open), updated for the actual Option 1R capture. **KNOWN:** source shutdown and fault memory, initially dropped by Option 1, are now restored in a different form. Raw bulk capacitance is partly restored too. They must not be described as wholly absent from current Lite.

All test numbers here refer to the **current [BENCH_TESTS.md](../evidence/v1a_lite/BENCH_TESTS.md#ordered-tests)**, not the earlier numbered list inside Phase C. **KNOWN:** all are planned, not run. “Acceptable” below means either a deliberate loss of optional functionality or a conditional engineering choice. Where protection evidence is missing, acceptance remains **OPEN**.

| Removed function / old implementation | Why it was there | Why dropping it can be acceptable in Lite — and the limit | Current bench test number and coverage |
| --- | --- | --- | --- |
| Input electronic current limit and overload timer, U101/R105 | Limit fault current and manage overloads without relying solely on melting a fuse | Fuse/source behavior may provide a simpler qualified solution. **OPEN:** F101 is not an equivalent limiter, and a source in current limit may never clear it. | **9** characterizes source current/hiccup; **12** tests shorts, overloads and fuse clearing; **6/11** check resulting heat/SCR stress. |
| Input programmed slew/inrush control, U101/C103 | Slow capacitor charging and reduce hot-plug stress | Only conditionally acceptable if the actual source, capacitor bank and FETs tolerate startup. No controlled-slew guarantee is retained. | **3–4** first power/startup/inrush; **9** cold connection and hot SOA; **6** thermal consequences. Settling/inrush bounds remain OPEN. |
| Input-eFuse UVLO, PGOOD and FLT supervision | Keep the buck disabled until input is acceptable and report faults | Independent buck EN is simpler. It does not reproduce the old interlock or establish the lower normal-input limit as a UVLO threshold. | **4** slow/fast ramps and rails; **10/12** dips, restart and source hiccup. No old FLT output is validated. |
| Old input eFuse OV/reverse implementation, including its negative-return diode | Disconnect excessive input and manage reverse/commutation paths | The job moves to TL431, opposed P-FETs and TVSs. Old active reverse-current/negative-return behavior cannot be assumed. | **9** input OV, FET stress and protected-bank reversal; **12** reverse input/backfeed. Dynamic behavior remains OPEN. |
| Old `INPUT_SHDN`/manual source-command path | Request upstream source removal during research faults | The old path is gone, but source removal is restored by `CB_COLLECTOR` and Q102. The old manual source contact was not a proven automatic detector. | **8/10** real fault trigger and persistent cutoff; **9** actual Q102 current/voltage. A logic transition alone is insufficient. |
| Opposed output MOSFETs and LTC7001 driver | Isolate the load from raw output and block reverse flow when off | Owner selected a cheaper shunt/cutoff architecture. **OPEN:** no equivalent output isolation or reverse blocker is claimed. | **8** remote output peak; **12** backfeed/open F301/restart; **11** discharge current paths. |
| Precision reference/fast comparator implementation | Obtain a narrow threshold window and fast OV response | TL431 reduces cost and supply complexity. **OPEN:** a guaranteed fast enough response has not been established. | **7** normal-high envelope; **8** temperature-dependent trip and complete response to clamp; **11** actual gate behavior. |
| Separate protected/raw MOSFET dump branches, power ballast and return diodes | Dispose of stored energy with controlled pulse paths on both sides of the output switch | One raw SCR replaces the disposal arrangement; there is no longer an output transistor separating two banks. **OPEN:** capacitor discharge can be very sharp without old ballast. | **8** raw/remote voltage and reversal implications; **11** gate current, anode peak, current rise, energy and recovery; **12** F301-open topology. |
| Old large raw/protected reservoir arrangement | Supply load steps and provide fault-response time | Lower-cost banks plus restored raw bulk may suffice for the selected load. They do not inherit the old hold-up, effective capacitance or voltage survival. | **4** startup; **5/7** load/transient/ripple; **8/11** fault containment and discharge. |
| Auxiliary surge stopper, buck-boost, HV LDOs and held driver rails | Keep detector, driver and memory supplies valid through power collapse | Most powered control blocks disappear. Output detection uses raw-rail power; the input latch uses upstream `CTRL12`. **OPEN:** no old hold-up guarantee survives. | **4** supply startup; **8/10** fault collapse, trigger capture and latch hold; **9** high-input stress. |
| Manual ARM/RESET, debounce and arm memories | Give the researcher explicit enable/reset sequencing | A simpler power chain is the documented choice. Fault memory remains as Q104/Q105; manual arming and a reset button do not. | **10** input-removal reset, dips and hold; **12** restart. Reset interval/hiccup immunity remain OPEN. |
| Guarded analog switches, supervisors and PG permission logic | Manage partially powered control paths and observe supply validity | Fewer domains remove many old dependencies. **OPEN:** surviving detectors/latch still need power-sequence qualification. | **4/9/10** startup, cold OV, partial supply and brownout behavior; **12** backfeed. The old ledger's open-ground injection is not explicitly specified in the current plan: dedicated coverage remains OPEN, not silently passed. |
| SW_HIGH/VIN_GOOD_FAST observations, manual source fixture and guarded outputs | Observe research conditions and support controlled injection | A reviewed external injector and external probes can provide the necessary experiment. The old observation comparators were not autonomous source protection. | **8–9** reviewed fault fixtures and source waveforms; **1–2** access/isolation inspection. Native SW/component-pin access needs fixture review. |
| INA228 measurements and ALERT | Provide automatic diagnostics and accumulated energy | Explicit owner removal reduces cost; external measurements suffice for bench characterization. Onboard reporting is deliberately lost. | **5–7** external V/I/efficiency/thermal/ripple records; **12** marks telemetry N/A. External instrument calibration is in the setup section. |
| Kelvin shunt and RC sense filter | Measure current without power-trace error | No onboard current sensor remains; continuous copper reduces series drop. This does not remove the need to measure current externally. | **2** continuous force path; **5** four-wire drop/current measurements; **11** wideband fault-current measurement. |
| Local TPS70933 telemetry rail and decoupling | Power INA228 and the local bus domain | The loads are gone and Lite protection does not depend on that rail. | **1–2** part/net inventory; **4** surviving rails; **12** backfeed. No absent rail is claimed “tested.” |
| TCA9517, pullups, host-reference interface and old J503 | Connect separate host/local I2C domains | There is no I2C function to interface. Lite J503 has a new power-test purpose. | **1–2** interface identity and continuity; **12** backfeed/telemetry N/A. No I2C protocol test is applicable. |
| Custom force links and large research force pads | Isolate stages, insert current measurement and support coupon experiments | Continuous copper reduces joints and assembly work. Isolation for injection now belongs to the external fixture. | **1–2** actual path/fixture isolation; **8–9** reviewed injection; **5/11** distinct force-current and sense connections. |
| Research inductor and high-voltage capacitor fault capability | Explore a larger fault-current/energy envelope | Cheaper parts can serve the narrower application only after their own ratings and fault containment are established. **OPEN:** raw ceramics/bulk cannot tolerate an uncontained input pass-through. | **5–7** normal operation; **8/11** saturated-inductor/capacitor fault effects; **9** input containment. |
| Old connector/harness/board/thermal qualification assumptions | Establish current capacity and acceptable drop for the old physical implementation | Those assumptions belong to old parts and geometry. Lite requires its own evidence rather than inheriting an old acceptance. | **1–2** construction/polarity; **5–6** hot drop/sharing/temperature; **7–8** remote transients; **12** single-contact faults. |

**KNOWN — bench order remains:** inspect → continuity → current-limited first power → no-load/rail verification → dummy-load steps → thermal → ripple/transients → output OV → input OV → latch → SCR stress → remaining faults. Pi integration is test **13**, only after tests **1–12**, the review blockers and missing acceptance bounds are closed. The test source and fixture must have a reviewed energy limit; a bench supply's current setting does not limit an already charged local capacitor's discharge.

## What stayed the same

- **KNOWN:** U201 is still LM61460AANRJRR. R201 remains **33.2 kΩ**, the recorded nominal switching setup being approximately **400 kHz**. This preserves the converter core, not every surrounding design assumption.
- **KNOWN:** feedback remains **100 kΩ / 24.6 kΩ**, sensing the local raw rail. **CALCULATED:** nominal output is **5.06504 V**. Lite does not quietly raise the setpoint to hide cable loss.
- **KNOWN:** the feedforward network remains **22 pF with 1 kΩ**; RBOOT remains nominal **0 Ω**; BIAS remains grounded; bootstrap returns to native SW. Equivalent nominal values do not imply identical part ratings.
- **KNOWN:** the independent output-fault objective remains. If the buck's high-side transistor fails short, commanding that damaged buck off is not sufficient. Lite's protection command uses its own detector, SCR and input switch.
- **KNOWN:** power returns share GND electrically. Switching-current loops, SCR pulse returns and quiet feedback/detector sense paths still need deliberate physical routing. A shared net label is not zero impedance.
- **KNOWN:** no USB 3.x or D435i data goes through this PCB. Dummy-load qualification precedes the expensive SBC. **OPEN:** source energy, thermal behavior, ripple, fault peaks and harness performance require measurements.

## New things you need to learn

### TL431 detectors: one on input, one on raw output

A TL431 is an adjustable **shunt regulator**: it controls current flowing from its cathode toward its anode according to the REF-pin voltage. Here it is used as a threshold detector. It is not automatically equivalent to the old fast comparator and precision reference.

**KNOWN:** Lite U101 watches the input-side common-source node using R150–R153. U301 watches raw output using R301–R304. Their refdes match old IC names but their functions/packages are different.

**CALCULATED — ideal divider examples**, using the analysis reference **2.495 V**, before reference-current and tolerance corrections:

- Input: upper **102 kΩ**, lower **10 kΩ** → `2.495 × (1 + 102/10)` = **27.944 V**.
- Output: upper **1 kΩ + 100 Ω + 30 Ω = 1.13 kΩ**, lower **1 kΩ** → `2.495 × (1 + 1.13/1)` = **5.31435 V**.

The reference input draws some current, so divider resistance creates an extra error. Temperature, cathode current, transistor drive and resistor tolerance also move the trip point. **CALCULATED:** C2 retains an output threshold screen of approximately **5.18387–5.43587 V** under its stated assumptions. **OPEN:** actual full-corner threshold and maximum response delay. A slow ramp can measure a trip threshold but cannot prove the peak during a fast buck failure.

### SCR crowbar: trigger, latch, then stop its current

**SCR** means *silicon-controlled rectifier*. A positive gate trigger can turn it on. After it latches, it can stay on without continued gate drive while its anode current remains above the holding level. Removing the gate command alone does not turn it off as it would a MOSFET.

**KNOWN:** Lite U301 sinks current through R305 from Q301's base. Q301 is a PNP transistor that supplies SCR gate current through R307. R308 returns the gate to cathode/GND. The same Q301 collector node, `CB_COLLECTOR`, also triggers the input latch. TP508 is before R307; TP301 is the actual SCR gate.

**KNOWN:** the selected part is **TYN612RG**, not the more sensitive **TYN612TRG**. The bench plan quotes RG's trigger-current maximum as **15 mA at 25°C**. **OPEN:** full-temperature trigger margin, gate rise time and pulse survival. A transistor-drive calculation does not establish those results.

The crowbar deliberately makes a low-impedance path across the raw rail. That pulls voltage down but creates a current pulse. The input cutoff must stop continued energy delivery, and all stored energy must have a tolerable path. F301 cannot clear the local raw-capacitor-to-SCR discharge because it is outside that loop. Test **11** measures current rise, peak, energy and recovery; tests **8/10** check the load peak and upstream shutdown.

### P-FET cutoff and a transistor latch

A **P-channel MOSFET** turns on when its gate is sufficiently below its source. Bringing gate and source together turns it off. Its body diode still conducts in one direction, so orientation matters even when the gate says “off.”

**KNOWN — intended sequence:**

1. An output OV event activates Q301 and `CB_COLLECTOR`.
2. R163 supplies a set pulse to Q104. Q104 turns on Q105.
3. Q105 feeds Q104 through R161: positive feedback keeps the latch set after the initiating pulse disappears.
4. Q105 also drives Q106 through R162. Q106 clamps Q103's base, stopping Q103 from pulling Q102's gate down.
5. Q102's source-to-gate pullup turns Q102 off, interrupting forward input power.

**KNOWN:** `CTRL12` is supplied upstream of Q102 so cutoff does not immediately remove the latch's own source. The name is not a guarantee of a fixed **12 V** rail: **CALCULATED:** C2's latched-state model gives approximately **10.27 V** at nominal **24 V** input, under its transistor/clamp assumptions. **OPEN:** actual control voltage and capture/hold margins.

**OPEN:** the crowbar may collapse the raw voltage so quickly that its set pulse is short. The latch must capture that pulse, remain set during permitted source hiccup, and reset only after deliberate power removal. It is not nonvolatile memory. Test **10** establishes capture width, actual Q102 interruption, hold and reset interval; none follows just from drawing positive feedback.

> [!info] PROMPT F-LITE-2
> **Save as:** `images/flite-2-detect-discharge-and-stop-input.png`
> **What to show:** A conceptual event sequence for the actual Lite circuit. Raw-output rise → TL431 U301 senses → PNP Q301 supplies CB_COLLECTOR. Split that event into two concurrent branches: R307 → SCR301 gate → raw capacitors discharge; and R163 → Q104/Q105 latch → Q106 inhibits Q103 → Q102 opens input. Show CTRL12 supplied upstream of Q102. Show Q101's forward body-diode route as the reason Q101 alone cannot stop positive input. Put F301 only between raw output and the dummy load. Label “KNOWN intended connections; OPEN timing, capture and stress.” Mark response order within each branch, without implying either branch has a proved completion time.
> **MUST NOT show:** the SCR turning off merely because gate drive disappears, F301 clearing the raw SCR loop, Q101 alone stopping forward input, a latch powered downstream of Q102, numerical timing guarantees, or measured waveforms.

![[flite-2-detect-discharge-and-stop-input.png|700]]

## Cost comparison: what the two headline numbers mean

These are dated design-accounting results from the repository, not current supplier quotations.

| Scope | Evidence label and amount | Interpretation |
| --- | --- | --- |
| Old captured design, priced parts subtotal | **CALCULATED:** **US$184.6509/board**, approximately **US$185**, or **4,893,249 VND** in Phase A | Incomplete known-price subtotal: some catalog parts and custom links were unpriced. |
| Lite Phase D installed core | **CALCULATED:** **379,299.80 VND**, approximately **380k VND** | Core subtotal after changing the input FETs to IRFR6215TRPBF; excludes the input/output headers. |
| Lite installed purchased components including J501/J502 | **CALCULATED:** **387,816.90 VND** | More useful installed-board parts subtotal, still not a delivered build price. |
| Planning currency conversion | **ASSUMED:** **26,500 VND per US$1** | Historical accounting convention; not a live exchange rate. |
| Complete prototype cost | **OPEN** | Harness/mates/carrier, PCB fabrication, assembly, thermal hardware, shipping/tax, purchase-lot minimums, spares and contingencies are outside the simple installed-part comparison. |

**CALCULATED:** the known old Sheet 03 subtotal alone was **US$122.5651**. The old L201 line was **US$21.84**, and its raw ceramic bank C209–C214 was **US$20.40**. Removing auxiliary supplies, output drivers, research logic and telemetry, then changing the inductor/capacitors, explains the large cost reduction. It is not just one cheaper IC.

**KNOWN:** Lite's retained D101 price contribution includes a historical **13,250 VND allowance**, not a freshly verified price. Phase C2/C3 also found full first-build purchasing scenarios over the recorded budget ceiling, even though installed core parts looked inexpensive. Minimum purchase quantities and non-BOM items matter. Do not turn “about 380k core parts” into “a complete qualified board costs 380k.” See [Phase A](../evidence/v1a_lite/PHASE_A_AUDIT.md#c–d-bom-and-cost-baseline), [Phase D reconciliation](../evidence/v1a_lite/PHASE_D_CAPTURE.md#bom-reconciliation-and-deviations) and the [current installed BOM](../evidence/v1a_lite/V1A_LITE_BOM.csv).

## Architecture decision history: Option 1 → C2 failures → 3B tried → back to 1R

### Option 1: simplify the old research design

**KNOWN — decision history:** Phase B compared cheaper protection choices. Phase C studied selected Option 1: retain the LM61460, remove telemetry/research controls, and use a TL431/PNP/SCR output crowbar with fuses. In that original arrangement, the output fuse sat before the crowbar.

The problems were physical. A current-limited source might keep the SCR hot without ever melting a fuse. If the output fuse opened first, it could disconnect the crowbar from the raw capacitor bank. Detector delay could also let output voltage exceed the load limit before the clamp became effective. Low cost did not close those faults.

### C2 / Option 1R: correct the topology, then expose what is still missing

**KNOWN:** C2 moved the crowbar and detector directly onto the raw capacitor node, left F301 in the load branch, added raw bulk capacitance and introduced persistent input shutdown. It explicitly corrected the proposed Q101-only shutdown to Q102 shutdown.

**CALCULATED — examples of unresolved C2 screens:**

- With the selected bulk model, allowed post-threshold delay was only approximately **0.416–0.937 µs** across the reported sensitivities. Those are model allowances, not guaranteed TL431/SCR response times.
- One saturated-inductor/reduced-capacitance case reached approximately **5.513 V** even with an **ASSUMED 0.5 µs** clamp delay, already above the **KNOWN <5.5 V** load ceiling. Remote harness ringing added a separate problem.
- The modeled **103 V** upstream TVS clamp exceeded the then-selected FETs' **100 V** rating. Raw **25 V** ceramics and **10 V** bulk could not survive an uncontained higher-voltage pass-through.

**OPEN:** nuisance trips during normal load release, SCR current-rise/energy survival, input-switch hot SOA, latch pulse capture and reset persistence. Added capacitance buys time in some models but also adds startup demand and discharge energy. C2 did not establish electrical release.

### Option 3B: try an eFuse between raw output and the Pi

**KNOWN:** C3 temporarily selected an additional series TPS26630 eFuse, reverse-blocking FET and Pi-side bulk, while keeping a higher-threshold raw backup crowbar. The idea was to limit the charging current into the Pi-side capacitor so the voltage would rise more slowly while the eFuse disconnected.

**CALCULATED — why that study did not qualify the design:** the full-temperature eFuse trip screen was approximately **5.235–5.519 V**, so its upper trip already exceeded the **KNOWN <5.5 V** ceiling. The hot series-drop screen gave approximately **4.642 V** at **5 A** before harness loss, below the **KNOWN 4.75 V** minimum. A capacitor calculation using current limit from the start ignored the unbounded current before limiting settled. If the eFuse failed short, the raised backup-crowbar threshold could itself exceed the allowed Pi voltage. Startup charging, pin stress and cost also remained problematic.

This experiment showed why adding a protection IC is not automatically an improvement. Its own resistance, threshold errors, timing conditions and failure modes have to fit the whole system.

### Return to 1R: the circuit you now have

**KNOWN — later owner decision:** [Phase D](../evidence/v1a_lite/PHASE_D_CAPTURE.md) records authorization to capture Option 1R. It uses C2's raw crowbar/bulk/latch architecture and imports C3's input-FET correction to **150 V IRFR6215TRPBF**. It does **not** capture the C3 output eFuse, extra output reverse-blocking switch, extra Pi bulk or raised backup threshold.

The return to 1R is a documented architecture choice, not evidence that C2's timing, pulse, thermal and latch concerns disappeared. The current bench plan maps them to tests **7–11**, with remaining faults in test **12**. **KNOWN:** later layout work exists in this worktree; older schematic/Phase D “no PCB work” notes describe their dated capture scope. This lesson neither reopens layout work nor declares an electrical/fabrication gate passed.

> [!info] PROMPT F-LITE-3
> **Save as:** `images/flite-3-option-history-and-evidence.png`
> **What to show:** Four illustrated cards, left to right: “Option 1 — low-cost fuse/SCR concept”; “C2 / 1R — raw crowbar + bulk + input latch; unresolved timing/stress”; “3B — series eFuse tried; threshold/drop/early-current problems”; “Current 1R — C2 topology + C3 input-FET correction; bench qualification OPEN.” Use brief plain-English captions, small conceptual blocks and a distinct “decision” versus “evidence” legend. End with a dummy-load bench, not a finished product. Do not use numeric electrical values; emphasize why each decision was made. Include “KNOWN history; OPEN physical validation.”
> **MUST NOT show:** a green safety approval, a fabricated/validated board, all C2 failures fixed, the 3B output eFuse inside current Lite, supplier shopping carts, or measured test results.

![[flite-3-option-history-and-evidence.png|700]]

## Check your understanding

1. Can Lite's F301 disconnect the SCR from the raw capacitors?
2. Why must the fault latch turn off Q102 rather than only Q101?
3. What did removing Sheet 04 save, and what capability was lost?
4. Does the retained feedback divider guarantee the same voltage at the Pi?
5. Why does a low nominal trip threshold not prove a safe fault peak?

> [!question]- Answers
> 1. **KNOWN topology:** no. F301 is in the load branch; raw capacitors, detector and SCR stay together.
> 2. **KNOWN topology:** Q101's body diode can still pass positive input. Q102 provides forward interruption.
> 3. **KNOWN:** fewer parts and one less series measurement element; onboard V/I/power/energy/ALERT/I2C are lost. External instrumentation takes over during testing.
> 4. **KNOWN:** no. It controls raw voltage; copper, fuse, contacts and cable drop voltage before the load. **OPEN:** worst-case remote compliance.
> 5. **KNOWN principle:** voltage can continue rising during response, and stored energy/cable effects matter. **OPEN:** the actual bounded threshold-to-clamp trajectory.

## Evidence and reading trail

**KNOWN:** this lesson references project-owned circuits and existing engineering evidence; it does not copy or adapt a third-party circuit into CAD. Existing manufacturer source revisions, licenses, reuse and attribution remain in the linked evidence's `third_party/` source registers. No manufacturer files were changed. Image embeds above are placeholders for the supplied ChatGPT prompts; no pictures have been generated.

| Source | What it establishes for this lesson |
| --- | --- |
| `git show v1a-research-schematic:hardware/kicad/<sheet>.kicad_sch` | Old actual components, connections, manual research hooks and sheet membership |
| `git show origin/main:docs/schematic/V1A_research_schematic_f11ffbb.pdf` | Old viewer-page locations; retained stale feedback note distinguished from actual R203 |
| [Lite root schematic](../../hardware/kicad/V1A.kicad_sch) and [Lite PDF](../schematic/V1A_Lite_schematic.pdf) | Actual current hierarchy, parts, rails and removed monitor page |
| [Phase A audit](../evidence/v1a_lite/PHASE_A_AUDIT.md) | Old component inventory, dependencies and dated incomplete price baseline |
| [Phase B architecture](../evidence/v1a_lite/PHASE_B_ARCHITECTURE.md) | Original options, cost-down rationale and their limitations |
| [Phase C calculations](../evidence/v1a_lite/PHASE_C_CALCULATIONS.md) | Original Option 1, detector calculations and removed-function ledger |
| [Phase C2 revision](../evidence/v1a_lite/PHASE_C2_REVISION.md) | Raw-crowbar placement, input latch, bulk, failure screens and unresolved bounds |
| [Phase C3 Option 3B](../evidence/v1a_lite/PHASE_C3_OPTION3B.md) | Tried series eFuse, its failure screens and input-FET correction |
| [Phase D capture](../evidence/v1a_lite/PHASE_D_CAPTURE.md) | Later return to 1R, current schematic choices and installed-cost reconciliation |
| [Bench tests](../evidence/v1a_lite/BENCH_TESTS.md) | Current test numbers, measurements, OPEN acceptance bounds and NOT RUN status |
| [Pi harness](../evidence/v1a_lite/PI_HARNESS.md) | Revised physical interface and superseding hot/aged resistance allocation |

VSLITE-HANDBACK
