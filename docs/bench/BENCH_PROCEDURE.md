# V1A R2 test board — owner's bench bring-up and fault-test procedure

**PRELIMINARY PROCEDURE — ALL HARDWARE RESULTS: NOT RUN**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Prepared 2026-10-03 against repository baseline `898759e45578f3767721d19eb313312b7d7733a9`.

This is a future laboratory procedure for the owner, a fourth-year electronics student. It does not release the current design for construction or energization. The [current freeze](../evidence/r2/gate4a/GATE4A_FREEZE.md) is **BLOCKED** by autonomous source-fault coverage and interlock default-off/PG recovery/hard series-driver supply loss. The external fixture is specified but **NOT BUILT / NOT QUALIFIED**. Stop at an unmet prerequisite; record BLOCKED and complete independent documentary or isolated-coupon work only. No engineering gate is closed by writing this procedure.

**No Raspberry Pi or other single-board computer (SBC) until every applicable normal, fault, thermal, harness, telemetry and source/interface test passes and the owner records integration approval.** A missing, inconclusive or not-executable test is not PASS. Use a passive header emulator and dummy loads throughout this document. Keep the Pi, USB power/data and host I2C plug physically absent during first faults.

## Read this first

The [test plan](../evidence/r2/gate4a/TEST_PLAN.md) supplies acceptance criteria. Its final FIX3 register and the following contracts supersede conflicting older paragraphs, including older 9–24 V limits, retired AHCT controls, 40 mA hold budgets and D302 connections:

- [FIX3 source trigger](../evidence/r2/gate4a/FIX3_SOURCE_TRIGGER.md), [interlock/manual controls](../evidence/r2/gate4a/FIX3_INTERLOCK.md), and [external fixture](../evidence/r2/gate4a/FIX3_FIXTURE.md).
- [Fixture BOM](../evidence/r2/gate4a/FIX3_FIXTURE_BOM.csv), [pin netlist](../evidence/r2/gate4a/FIX3_FIXTURE_NETLIST.csv), [calculated allocations](../evidence/r2/gate4a/FIX3_CALCULATIONS.json), [change register](../evidence/r2/gate4a/FREEZE_TABLE.md), and [test hooks](../evidence/r2/gate4a/TEST_HOOKS.md).
- [J502 selection](../evidence/r2/J502_SELECTION.md), [monitor domains](../evidence/r2/MONITOR_POWER_DOMAINS.md), [AGENTS.md](../../AGENTS.md), and [project context](../context/00_USER_AND_WORKSTYLE.md), [overview](../context/01_PROJECT_OVERVIEW.md), [architecture](../context/02_V1A_ARCHITECTURE.md), [engineering state](../context/03_ENGINEERING_STATE.md), [learning sequence](../context/04_LEARNING_CURRICULUM.md), [gates](../context/05_WORKFLOW_AND_GATES.md), [decisions](../context/06_DECISION_LOG.md). Earlier context descriptions of an empty Sheet 03 or 6.8 µH inductor are historical.

Use **REQUIREMENT** for an owner limit, **ASSUMPTION / PRELIMINARY** for an unqualified setting, **CALCULATION** for a derived value, **OBSERVATION / MEASURED** only with saved physical evidence, **DECISION** for a recorded choice, and **OPEN RISK / BLOCKED** for unresolved limits. A surviving part, simulation, electrical rules check (ERC), or design rules check (DRC) does not establish electrical safety.

PG means power-good; eFuse means electronic fuse; FET means field-effect transistor; I2C means Inter-Integrated Circuit. VGS is gate-to-source voltage, VDS drain-to-source voltage, ID drain current, and IL201 inductor current. A crowbar/dump deliberately drains stored rail energy through a rated switching/ballast path; opening the series switch alone does not empty the raw bank.

### Limits used on every run

Here `U` is the substantiated measurement uncertainty, including the actual probe/range/bandwidth. Apply it in the unfavorable direction.

| Item | Criterion and status |
| --- | --- |
| Normal input | **REQUIREMENT: 9–26 V at the DUT input connector**, not at the supply display. Test 9, 24 and 26 V. DUT = device under test. |
| Far-end upper voltage | **REQUIREMENT: `V_Pi_peak < 5.5 V`**. On the dummy header, `max(Vfar_measured) + Upeak < 5.5 V`, including startup, fault edge, ringing, tail and attempted restart. Check both positive contacts against the loaded far return. |
| Far-end normal full-load voltage | **REQUIREMENT: `min(Vfar_measured) − Umin >= 4.75 V at 5 A`**, including specified steady and load-step windows. Declare current tolerance and windows before acquisition; do not average away a trough. |
| 27 V | Fault/OVP-window point only. Overvoltage protection (OVP) may or may not trip at 27 V. Measure the fitted threshold first; an already isolated source does not qualify an energized high-side fault. |
| Nominal raw rail | **CALCULATED 5.098361 V**, not a guaranteed regulation band. Full regulation tolerance, standalone ripple limit, efficiency target, startup deadline, production ambient range and overload envelope remain **OPEN**. Characterize; do not invent acceptance limits. |
| DUT source containment | Conditional design contract: physical source-current extinction plus timing uncertainty **≤10 µs** from fault onset; whole-event positive replenishment **`Q+ + UQ ≤100 µC`**. Endpoint: `abs(IMAIN) + Uendpoint ≤10 mA`, remaining within that band afterward. |
| Source/component box | **PRELIMINARY qualification allocations:** total effective main local capacitance 10–30 µF; differential L201 inductance 5–12 µH through 0–100 A and declared temperatures; initial healthy IL201 ≤8 A; raw bank 2.4064–5.59656 mF; raw peak plus uncertainty ≤6.9 V. Actual source amplitude/work and every return-current interval must remain within reviewed bounds. |
| Disposal endpoint | `abs(IL201)+U ≤0.10 A` and raw/protected/far residual magnitudes plus uncertainty ≤0.3 V, then ≥1 ms without rebound. Extend the event for any recurrence. |
| Fixture emergency ceiling | **PRELIMINARY:** ≤20 µs from physical fault onset, separate from the DUT's 10 µs requirement. Its abort, a supply current limit, or unintended source sag must not supply the DUT PASS. |
| Temperature | **ASSUMED COLD = room 25±5°C**. HOT is a reviewed stabilized component-temperature condition, not a production hot rating. Ballast terminals + uncertainty ≤85°C before a pulse and <95°C including pulse rise. Other part limits below also apply. |

If an uncertainty interval overlaps a required boundary, mark INCONCLUSIVE/BLOCKED. For the upper rail limit, `peak − Upeak >=5.5 V` establishes FAIL; equality at the conservative upper bound never establishes PASS. A measured module voltage alone cannot qualify the Pi-end voltage.

## Equipment and preparation

Inventory actual model, serial number, calibration date, limits and owner in Record A. Named instruments in the design files are candidates, not an assertion that the lab owns them.

| Equipment | Needed capability / preparation |
| --- | --- |
| Main bench supply | Programmable current-limited supply for measured 9/24/26 V DUT input. For the selected fixture, PSF1 is a Rigol DP811A candidate in its 0–40 V/5 A range with a **calibrated ≤30 V terminal ceiling**. Measure output capacitance, overshoot and source/lead impedance. |
| Independent fixture/control supplies | PSF2 candidate: separate DP811A at 12 V, ≤13 V including error. Independently bounded supplies for isolated board coupons; record all reservoirs, limits and backfeed paths. PSF2 powers fixture controls only. |
| Loads | Electronic load ≥40 W and passive bank ≥50 W, each rated for the reviewed abnormal voltage/current/energy. Use 0 A, low-current steps, 2.5 A and 5 A only as prerequisites permit. Record constant-current (CC) dropout and transient behavior. |
| Dummy Pi input | Real selected harness, passive header emulator and measured capacitors. **ASSUMED nominal 1 mF**; sensitivity cases 0 intentional C, 100 µF, 470 µF, 1 mF, 2.2 mF, with **ASSUMED 2/5/50 mΩ equivalent series resistance (ESR)** where achievable. Count measured effective capacitance, including tolerance; keep it distinct from the protected-module bank. Actual Pi input C/ESR/load behavior remains OPEN. |
| Oscilloscope/acquisition | ≥200 MHz, preferably ≥2 GS/s per used voltage channel, ≥4 analog channels, sufficient memory, plus synchronized channels for ≥3 voltages and ≥3 currents at once and extra logic/gate channels as required. Verify actual per-channel rate with all channels enabled. |
| Voltage/current probes | Rated differential probes for switch/gate/far-end nodes; calibrated high-current sensors for L201/dumps and a separately qualified sensitive source-off endpoint range. Probe pulse rating, saturation, recovery and bandwidth must cover positive and negative current. A fast scope cannot correct a slow current probe. |
| Metrology | Digital multimeter (DMM), four-wire milliohm meter, bias/temperature-capable capacitance/ESR characterization, voltage/current calibration and deskew equipment. |
| Thermal | Thermocouples or equivalent at ballast terminals, FETs, inductor, eFuse, charger, connector/crimps, wires and references; controlled thermal environment. Infrared imaging supplements contact measurements and junction estimates. |
| Qualified fault equipment | Complete FIX3 fixture and passive surrogate, guarded force connections, hardware STOP/abort, independent discharge adapters, protective cover, insulated operating handles and eye protection. Applicable hot safe operating area (SOA), reverse-current and pulse ratings precede energization. |
| Later interface equipment | Current-limited host emulator/I2C adapter with reviewed isolation and pull-ups; no Pi. Separate rated 0–60 V auxiliary-only pulse fixture for T14A; the 30 V FIX3 fixture cannot perform that test. |

At nominal 5.098361 V, **CALCULATED** passive resistances 2.039344 Ω and 1.019672 Ω approximate 2.5 A and 5 A. They do not hold current constant during a fault. Measure actual load current and resistor temperature. A 2.2 mF dummy at 5.5 V stores **CALCULATED 33.275 mJ** in addition to the board banks.

### Mandatory bench rules and stop action

1. Follow R2 schematic/pin/ERC review → R3 layout/DRC/visual review → R4 fabrication-readiness authorization → R5 physical testing. Separately reviewed coupons may resolve blockers within their documented construction/stimulus limits. This procedure authorizes no new PCB, order or purchase.
2. Use the enclosed, bounded-energy fixture. Never short VIN to a switching buck node with a loose wire. Never bypass L201, U101, the series pair, the source limiter, or a permission interlock to obtain a passing trace.
3. Before changing a load, probe, capacitor, force link or fixture wire, turn **all** supplies off, isolate all sources/backfeed and verify every store discharged. Make normal control changes only through prewired insulated switches. Do not move a probe by hand during a pulse.
4. Keep protective earth connected. Draw and continuity-check the complete return diagram, including scope, load, USB/control equipment and auxiliary supplies. `FGND` joins board power return at PF5 only; `FAR_GND` returns through the real harness. No probe earth, load chassis or remote-sense return may bypass that harness return.
5. Start at the lowest separately reviewed current/energy. Increase only after reviewing the preceding raw traces, component stress and temperature. A supply current setting does not bound capacitor discharge or microsecond fault current.
6. **STOP action:** operate SF1 to STOP (or the reviewed source inhibit for non-fixture tests), turn the main source output off, and save the capture. Preserve healthy protection power for the already qualified disposal interval if it is safe to do so. For smoke, uncontrolled heating or a control-supply fault, remove all supply outputs immediately and use the independent passive discharge system. Never reach into the enclosure or pull a live force connector.
7. After current ceases, source outputs are off and connector-side discharge is verified, open the JF1 dead disconnect. Isolate PSF2, board auxiliary feeds and instrument backfeed. Only then close SFD1–4 through their prewired resistors. Verify the complete discharge record below before handling. Elapsed time or a dark LED is insufficient.
8. On FAIL/INCONCLUSIVE: no next stress step, no repeated reset into a fault, no Pi. Retain failed native waveforms, annotate the violated criterion, inspect unpowered, revise the relevant design/fixture or measurement method, and repeat affected prerequisites after review.

## Probe and manual-control map

**Verify each point by net continuity on the actual assembly before use.** The [retained Gate2 netlist](../evidence/r2/sheet03/V1A_gate2.net.xml) identifies existing TP101/301–305/401–404/501–504. It does not contain the complete FIX3 candidate. TP201/202, TP306–312 and TP405/406 are reservations: do not infer an ordered one-to-one mapping from their range. Record assigned pad/pin and photograph in Record B. A missing hook is BLOCKED, not permission to guess a pin.

| Measurement | Point/net and reference |
| --- | --- |
| Input at DUT | J501.1 / TP501 `VIN_RAW` to J501.2 local return; fixture PF1 `DUT_IN` feeds ahead of F101/aux split. |
| Main local input | TP502 / PF2 `VIN_PROTECTED` to paired return; `IMAIN_FORCE` is between U101 OUT and **all** counted main input capacitors. |
| Switching / inductor | PF3 `NATIVE_SW` = native U201 SW; PF4 `L201_IN` after isolation; TP201/202 reservations plus explicit pad mapping for both L201 terminals. Differential voltage across L201; `IL201_FORCE` link carries its current. |
| Raw / protected | TP301 `VOUT_5V1` at raw bulk; TP302 `VOUT_PROTECTED` at protected bank; each with its local paired return. Dedicated VPROT pad may supplement TP302. |
| Series gate | TP305 `PROT_GATE` relative to TP304 `PROT_MID` (common source); `PROT_BST` to `PROT_MID` for bootstrap. Measure actual individual drain/source and series current as well. Ground-referenced gate voltage is not VGS. |
| Detector / shutdown | TP303 `REF_2V5`; TP101 `INPUT_SHDN`; TP102 `INPUT_FLT`. Reserved TP306–312 expose `OV_DIV`, U303.1 comparator output, fault latch, protected crowbar VGS, `DRV_HOLD`, `DET5`, SHDN. Old `OV_FAULT` wording must be reconciled to FIX3 `FAULT`/`NOFAULT`, not a retired latch. |
| Raw/protected disposal | Separate Q330/Q303 drain-current links and source-Kelvin VGS pads; raw 99 mΩ and protected 33 mΩ ballast paths. Record each parallel string current. |
| New control pads | Named sense pads for `SER_DRV`, `DRV_HOLD`, `SAFE_IN`, `SAFE5`, `3V3_AUX`, `REF_SAFE_2V5`, `REF1V25`, `REF0V25`, `CORE_POR_RAW_N/N`, `RAILS_FAST_OK`, `READY`, `RELEASE_REQUEST/CLK`, `RELEASE_SEEN`, `NOFAULT`, `ARMED`, `PG_SEEN`, `PG_GOOD`, `MAIN_PERMISSION`, `RUN_GATE`, `DISPOSAL`, `DIAG_VIN_OK`, `SW_ZERO`, `RAW_ZERO`, `PROT_ZERO`. Pad numbers OPEN pending capture. |
| Source trigger | `SW_HIGH`, `SRC_TIMEOUT`, `VIN_GOOD_FAST`, `VIN_SEEN`, `SRC_COLLAPSE`, `SRC_TRIP`, plus physical PF4 and TP502. Probe loading belongs in the delay calculation. |
| Shunt / monitor | TP402 `SHUNT_KPLUS`, TP403 `SHUNT_KMINUS`; TP404 `3V3_LOCAL`; TP401 `ALERT_LOCAL`. TP405/406 force-node sense reservations need mapping. Never put load current through Kelvin pads. |
| Output / far end | TP503 / J502.1 `LOAD_5V1`, J502.2 return; TP504 module GND. Far sense at emulator physical +5 V pins **2 and 4**, referenced to its loaded return plane and checked for spreading among GND **6/9/14/20/25/30/34/39**. Measure positive branches separately. |
| Fixture timing | `SHOT`, `DEAD_READY`, `INJECT_CMD`, `ABORT`, `FX_READY`, `FX_ARMED`, QF1–5 source-referenced gates/currents; `FX_DRV1/2/3`, `FX12`, `FX5`, `FBST1/2/3`. |

### Controls are dry contacts, not signal-generator inputs

| Control | Exact action / ownership |
| --- | --- |
| Board ARM, J601 | Pin 1 `ARM_CONTACT`, pin 2 GND. Close 1–2 to press, open to release. It is not fixture ARM. |
| Board RESET, J602 | Pin 1 `RESET_CONTACT`, pin 2 GND. Close 1–2 to press, open to release. RESET only samples a valid diagnostic in DIAG; it does not authorize bypassing a persistent short. |
| Board S601 DIAG | C&K 7201SYZQE: closes terminals 2–1 and 5–4. Connects the 470 Ω diagnostic probe and drives SERVICE_RUN low. Main force path physically isolated. |
| Board S601 RUN | Closes 2–3 and 5–6. Terminal 3 is NC, so the probe disconnects; SERVICE_RUN becomes high. Verify break-before-make and probe disconnection. JP601.1 = R716 output, .2 = DIAG_FEED; J603.1/.2 = SAFE5/GND; J604.1/.2 = SERVICE_RUN/GND. |
| Fixture SF1 STOP / enable | **STOP = terminals 1–2 open**, STOP_RAW pulled low. Enable = 1–2 closed, tying STOP_RAW to FX5. Verify labels by continuity, not lever direction. |
| Fixture SF2 RESET | Close 1–2 to pull RESET_RAW_N low; release by opening. Clears fixture SHOT/abort memory; does not clear the board fault. |
| Fixture SF3 ARM | Close 1–2 to pull ARM_CONTACT low and create ARM_EDGE; return open before another cycle. Controls QF4/5 and QF2/3 through fixture logic. |
| Fixture SF4 FIRE | Close 1–2 to create FIRE_EDGE; return open after the shot. Starts hardware dead-time/injection/abort sequence only with genuine board PG and permission. Do not wire FIRE/SHOT/ABORT to board FAULT/SRC_TRIP/SHDN in autonomous mode. |
| Fixture PG / permission | JF2.1 receives genuine board `PG_GOOD`; JF3.1 receives `MAIN_PERMISSION`; each .2 is local FGND. Existing 1 kΩ guards and 10 kΩ pulldowns remain. Synthetic PG is isolated characterization only. |

**OPEN service-interface detail:** the released build traveler must identify the prewired physical main-force isolator and independently bounded board-auxiliary feed used for DIAG. The current fixture's PSF2 is not a board-auxiliary feed. Keep the main conductive path absent during diagnosis, retain valid controls while selecting RUN, and establish the main path only through the reviewed insulated switching arrangement with its source off. Do not insert loose force links with live control rails, defeat SHDN, or borrow fixture 12 V for an undocumented board feed. If this sequence cannot be implemented without rewiring powered hardware, service setup is BLOCKED pending its interface review.

## Numbered bring-up procedure

Every step uses the stop action above on failure. Complete Record C for ordinary runs and Record D for each fault; include setup, stimulus settings, probe map, raw files, uncertainty, result and failure action. Detailed coupon acceptance remains in the linked test plan; the checklist in Step 0 does not waive any criterion there.

### 0. Establish permission, measurement capability and isolated prerequisites

**Setup/probes/settings:** no main, series or injection force path. Read the assembly revision, signed R2–R4 records, source contract and instrument inventory. Use separately reviewed low-energy coupons for the following evidence; inspect and continuity-check each coupon before power. Apply T13 calibration to the named probes above. No completed evidence is supplied by this document.

| Required evidence | What to set up, capture and accept before dependent integrated work |
| --- | --- |
| T02/T05/T16/T17 identity/pins | Reconcile active register, BOM, lands, DNP (do not populate) parts and capture. U101 MODE open for latch-off; R301 9.88 kΩ, R305 2 MΩ/1206, R341 88.7 kΩ, R312/R600 32.4 kΩ, R609 100 kΩ, R716 470 Ω. C301 is BST–TS; C302 is REF–GND; D302 anode is SER_DRV. Review TPS7A16 IN versus EN limits separately. |
| T13 uncertainty | Zero/demagnetize current sensors, calibrate gain/offset/common mode, loading and dynamic response, deskew same-event voltage/current, verify no clipping/aliasing/saturation and record overload recovery. **Targets only:** Upeak/Umin 15 mV; Ut 25 ns; endpoint ≤1% gain +2 mA additive. Under that endpoint budget indicated current must be ≤7.920792 mA. Missing capability blocks timing/charge PASS. |
| T04L/T04 bootstrap | Separate coupon: strap both power-FET drains to their common source; no L201 or banks. Proposed accessible energy ≤2 mJ. Sweep TS 0/5.10/6.90 V and qualified rail/temperature; include extra measured 2 MΩ gate–TS challenge. Capture TP305−TP304, BST−TS, pump/leakage and off/loss decay. Both settled VGS−U ≥10 V for ≥60 s and equilibrium, VGS+U <20 V, effective C301 ≥0.5 µF. Loaded current cutoff remains a later test. |
| T06L/T06/T06F3 detector | Isolate from power controls/banks. External 1 kΩ guard with calibrated ±7.5 V source; actual DUT-side raw sweep −6.9…+6.9 V, initially slow. Proposed DUT-side stray C ≤10 nF. Capture actual raw, OV_DIV/SENSE/REF, comparator, supply and both input currents. Trip +20 mV-equivalent overdrive +U ≤5.38 V; trip minimum−U above measured normal raw peak/noise. Initially unpowered rails ≤0.3 V; fully-off abs(SENSE)+U ≤0.4 V; input currents <10 mA and all pin limits. Repeat partial-power/reference-cap discharge, then qualified measured fault slew. SAFE references: REF1V25 ±15 mV, REF0V25 ±5 mV allocations, combined shunt clamp current ≤10 mA development ceiling, node C ≤100 pF and sensing ≤1 µs. |
| T07A–F/T07F3 auxiliary | Main disconnected. Capture AUX_RAW/LIMITED/RUN/12V/PREHOLD, DRV_HOLD, SER_DRV, SAFE_IN/SAFE5, DET5, 3V3_AUX, TMR, branch currents and loaded gates at 9/24/26 V and all rail orders. Current/thermal/SOA limits precede increases. Ccharged ≤600 µF including additions, held-domain load ≤45 mA total, SAFE5 RUN ≤8 mA / DIAG ≤20 mA, rise slope+U ≤10 V/s, C374 effective ≥0.5 µF through 17.60 V; D304 ≤0.50 V, D660 ≤0.20 V at actual load/T. C602/C660 ≥5 µF. SER_DRV must exceed actual worst release threshold (11.030525 V calculated screen). Charger TJ+U <125°C; retain T07E stability/loop-margin and T07F hot-SOA conditions. The 4.513751 ms hold screen is not measured disposal ride-through. |
| T01F3-N/F source coverage | On isolated detector, replay continuous high, floating 5.1 V, onset before/after VIN_SEEN, input collapse, and 3 µs high / 1 µs low plus narrower reset pulses. Capture PF4-equivalent stimulus, SW_HIGH/SRC_TIMEOUT/VIN_SEEN/SRC_TRIP. The periodic case is a known logic counterexample; do not mark it PASS because continuous-high injection works. A separately rated bridge emulator must establish admitted damaged-bridge signatures or the discriminator/scope must be reviewed and revised. No destructive internal U201 bridge test here. Normal 9/24/26 V evidence later must show every SW_HIGH interval+U ≤3.50 µs, resetting low intervals and healthy VIN_PROTECTED ≥8.30 V. |
| T15F3/T15F3-D interlock | Execute the isolated versions of Faults F1/F2 below: all rail orders/plateaus, PG timing, hard SER_DRV collapse and diagnostic short cases. Measure physical gates and minimum asynchronous pulse widths, not only a Boolean state. Failures require circuitry before integrated use. |
| T09A/T09B ratings | Measure effective main/raw/protected/dummy C/ESR, Ldiff and DCR versus current/T. Review applicable hot FET/diode/ballast SOA, negative voltage, current sharing and repetitive pulse limits before stress. The 100 A forward screen does not bound reverse current. |
| T12F3/T12D fixture | Complete Step 11 on controller coupons/passive surrogate before connecting energized DUT force paths. This may be scheduled independently of normal-board characterization. |

**Capture:** signed evidence paths for every row and unresolved issue. **PASS to proceed:** the required construction gates and the prerequisites for the next test have actually closed. **On failure:** leave the integrated board unpowered; work only on the isolated failing block within its reviewed limits. Source-coverage and interlock blockers are not waived for convenience.

### 1. Visual and assembly inspection — T02/T05/T16

**Setup/settings:** all sources disconnected, banks verified discharged, magnification and released schematic/BOM available; no Pi. Photograph both sides, labels and fixture/harness.

1. Verify board/assembly revision and every rework against the traveler. Confirm D101 SMCJ36CA, F101 3403.0285.23, selected L201 74437636351002 (10 µH candidate), opposed BSC034 pair, both disposal paths and both output banks. Check polarity, IC pin 1, package variants, solder bridges and exposed-pad attachment.
2. Check C301/C302 separation, D302 polarity, U101 MODE open, current FIX3 population and retired control parts absent. Inspect Kelvin traces, separate raw/protected nets, local decoupling, switching/return loops and thermal paths against the reviewed layout.
3. Check connector pinning, crimp/splice tooling, strain relief and the real selected harness: Phoenix 1776508/1777989, TE 3-87456-6/87309-9, Belden 8502 AWG20 fanouts and 8521 AWG16 trunks. Inspect both positive and all eight ground contacts.

**Probes/capture:** photographs and point-to-net labels in Record B; no powered probes. **PASS:** exact assembly matches the approved revision, no unexplained substitutions/damage or bypass. **If it fails:** label and quarantine; correct and re-inspect before continuity or power.

### 2. Continuity, resistance, polarity and discharge paths

**Setup/settings:** DMM resistance/diode mode only on discharged hardware; four-wire meter for low-resistance force paths, with stimulus within component ratings.

1. Measure each power rail to its local return in both polarities; allow capacitor charging readings to settle. Check TP501, TP502, TP301, TP302, TP503, SAFE5, DET5, SER_DRV and DRV_HOLD. Record actual resistance/diode behavior; no universal ohm threshold is invented for populated rails. Investigate an unexplained persistent low reading against the circuit before power.
2. Verify no copper bypass from TP301 to TP302 around Q301/Q302. Distinguish legitimate body-diode/test-meter conduction from a short. Inspect shunt force and Kelvin connectivity separately: R401 force pads 1/4, sense pads 2/3; TP402 source sense and TP403 load sense.
3. Check J502.1 positive/J502.2 return and far header orientation. Measure harness loop/individual branches, switches, all force links, and each diagnostic sense lead. Native-SW diagnosis must sense PF3, even when QF2/3 are open.
4. With instruments attached but supplies off, test earth/USB/load return paths. Verify no parallel far-return conductor and no host/local supply tie. Verify RFD01–20, RF61–63 and SFD1–4 to their correct local/floating references.

**Capture:** resistance/diode readings, return drawing, switch continuity and photographs. **PASS:** intended connectivity and absence of unexplained shorts/backfeed paths; all discharge paths intact. **If it fails:** disconnect instruments to locate the path, repair unpowered and repeat. Do not test a suspected short by raising a supply current limit.

### 3. Current-limited first power — auxiliary/control only

**Setup:** isolate main, series and injection force paths using the reviewed interface. J502 load absent, J503 unplugged, S601 DIAG, board ARM/RESET released. Qualified coupon evidence from Step 0 is required. Set board-aux input to **9 V** at its approved feed; start with **PRELIMINARY 50 mA current limit** for a brief wiring screen, counted source energy reviewed first. This deliberately may not permit startup.

1. Attach rail/current probes while unpowered. Enable the auxiliary supply; watch actual input/current and rail polarity. If current limiting or repeated startup occurs, turn off and inspect; do not leave it cycling.
2. Only after that screen and the T07 startup envelope review, repeat with **PRELIMINARY 0.15 A auxiliary-source limit**, or the documented lower reviewed limit. The 120.543 mA calculation is a screen, not a guaranteed startup current. Any larger limit requires a revised current/energy/SOA record.
3. Let the slow hold charger finish. Verify AUX_LIMITED ≤35 V, converter/held/isolated rails, references, power-on reset (POR), READY and default SHDN/RUN state. Record rise slopes and actual startup time; no invented startup deadline applies. Do not ARM while rails are unsettled.

**Probes:** TP303, TP101, named AUX/DRV_HOLD/SER_DRV/DET5/SAFE5/3V3_AUX pads, CORE_POR, READY, actual VGS. **Capture:** complete startup plus rail values/current/temperature. **PASS:** T07F3 limits and valid references, main/series remain off, no unexpected heating/oscillation/backfeed. **If it fails:** STOP, discharge, inspect polarity/load/charger sequencing; remain in isolated work.

### 4. Diagnostic reset, no-load startup and rail verification

**Setup/settings:** completed Step 3 and interlock prerequisite. Install all wiring unpowered; use the reviewed main-force isolator/service arrangement described above. Dummy header connected with nominal measured 1 mF, load branch off; this is no external load, although bleeders/telemetry consume current. For the first main run choose **9 V at J501, PRELIMINARY 0.25 A limit** only if the measured inrush envelope permits it. A too-low limit makes startup inconclusive; inspect and revise within the reviewed source envelope before retrying.

1. Main conductive path isolated, auxiliary controls valid, S601 DIAG: verify diagnostic current ≤11.200 mA, TP502 diagnostic VIN above the generated maximum threshold (3.811471 V plus measurement margin), and native SW/TP301/TP302 residual magnitudes+U ≤0.30 V. Verify actual comparator states and no main/series current.
2. Press J602 RESET, then release. **PRELIMINARY manual dwell ≥100 ms per press/release** gives margin over the calculated 19.338–20.643 ms debounce; observe the signals rather than trusting time alone. Verify NOFAULT=1, ARMED=0 and dumps off. A healthy DIAG screen does not exclude intermittent/high-voltage faults.
3. Select S601 RUN. Confirm break-before-make, diagnostic probe disconnected, SERVICE_RUN valid and PG_GOOD=0. Through the reviewed prewired arrangement establish the main force path with main source output off, then enable the current-limited main source. No loose link insertion with energized controls.
4. Confirm READY and references have settled (calculated READY delay 97.007–103.550 ms after valid input), ARM released and RELEASE_SEEN set after the 0.991–1.058 ms release qualifier. Press and release J601 ARM deliberately. Main may start; series must wait for **genuine** PG. If PG was already high, stop and investigate the unresolved early-PG case; never force it high.
5. Record input rise, TP301 raw output, TP302 protected output, TP503 module output and far header. Verify approximately 5.098 V nominal raw rail, correct polarity, series VGS and continuous control validity. Capture turn-off/restart with no automatic re-arm. Repeat normal no-load startups at 24 and 26 V after the 9 V run passes.

**Capture:** startup inrush/current, all rail maxima/minima, PG/ARM/SHDN/RUN chronology and steady rail table. **PASS:** upper far-end inequality, reviewed rail/pin/inrush limits, no false latch/dump, no unintended series connection or restart; normal operation at 26 V. The 4.75 V minimum is assessed in the prescribed 5 A windows, not while output is intentionally off. **If it fails:** STOP and investigate rail, PG, leakage or source-current-limit behavior; do not bypass interlocks or increase the buck setpoint.

### 5. Low-current dummy load and increasing load steps — T10/T11

**Setup/settings:** same real harness and measured dummy C; far-end electronic load initially off. Attach current sensors and branch/connector temperature probes before power. **PRELIMINARY progression: 0.10 → 0.50 → 1.0 → 2.5 → 5.0 A**, holding each ≥30 s for screening and until readings are interpretable. Actual safe dwell follows thermal review. Do not advance to a current exceeding an applicable hot contact/wire rating.

1. At 9 V input, run the service/ARM sequence, enable 0.10 A and compare module versus far voltage. Advance one step at a time after checking waveforms, input current and temperatures. Repeat at 24/26 V and later HOT.
2. Set main current limit using the measured input-demand envelope at that voltage/load, including startup and auxiliary demand, below the reviewed source/board ceiling. For planning, `Iin ≈ Pout/(Vin × efficiency)` requires consistent power boundaries; add auxiliary current only if that efficiency excludes it. Record each setting. Do not confuse the nominal 4.48 A U101 input-limit calculation with 5 A output capability.
3. At each step log TP301/302/503, both far positive voltages, total and branch currents, input V/I, VGS and all critical temperatures. At 5 A apply the strict far minimum. Compute delivered efficiency from consistent input and far-end power boundaries; INA228 alone excludes several losses.
4. Measure hot loop/contact losses. T11 allocations: complete J502 pole ≤3.12 mΩ; female-crimp/mated-contact block ≤20 mΩ per contact; combined splices ≤0.5 mΩ per polarity; positive resistance ratio ≤1.05. Each measured branch current+U must also be below its applicable hot male/female rating. The preliminary fully populated ~2.01 A/contact screen does **not** qualify two contacts for 5 A; actual mate/derating evidence is a prerequisite.

**PASS:** required far voltage window, no false trip/oscillation, component/current/thermal limits respected; all requested current points actually reached. Efficiency remains characterization until its requirement is defined. **If it fails:** STOP; inspect contact imbalance, setpoint tolerance and protection/shunt/harness drops. Mark an unsafe or unreachable 5 A point BLOCKED; do not substitute 2.5 A or remove the real harness.

### 6. Thermal measurements — T15T and loaded T04/T07

**Setup/settings:** after low-current screening, increase load within reviewed ratings at 9/24/26 V, including 5 A only after contact qualification. COLD is 25±5°C room. For HOT choose and record the controlled ambient/airflow/enclosure and component targets inside all limits. **PRELIMINARY stabilization screen:** change <1°C over 5 min, then hold ≥10 min; extend if still drifting. This is not a production soak specification.

**Probes/capture:** log actual terminals/cases at U101/Q101/U201/L201, Q301/302/Q303/Q330, every ballast string, shunt, capacitors, charger, references, connectors/crimps/splices and wires. Measure VGS continuously and estimate junction temperature only using a documented thermal correlation plus uncertainty.

**PASS:** every device stays within its reviewed derated limits; D321 and ADG4612 ≤85°C for the cited leakage screens, Belden 8521 ≤80°C, housings ≤85°C, ballast limits in the limit table, U327 TJ+U <125°C and all other applicable junction limits. At 5 A the far minimum still passes and rails/gates remain valid. **If it fails:** reduce to zero and STOP, inspect heat paths/contact resistance; redesign or declare a reduced scope through engineering review. A low ambient label cannot substitute for component measurements.

### 7. Ripple and switching behavior — T10/T01F3-N

**Setup/settings:** stable 0/2.5/5 A at 9/24/26 V, COLD/HOT; nominal dummy C first, endpoints afterward. Use differential probes at TP301, TP302 and far contacts, with minimum qualified loop area. Record full-bandwidth DC-coupled waveforms for limits and separately labeled **20 MHz bandwidth** ripple captures. **PRELIMINARY views:** 1 µs/div for switching, 1 ms/div for burst/low-frequency behavior; adjust to show complete patterns without losing sample rate.

**Capture:** peak-to-peak ripple, absolute minima/maxima, spectrum if useful, native SW/PF4, SW_HIGH and TP502, actual sampling/bandwidth/load behavior. Confirm no missed long high pulse during pulse-frequency modulation (PFM), pulse-width modulation (PWM), startup, recovery or dropout.

**PASS:** far-end upper and 5 A lower inequalities, no unintended trip/oscillation, all pin limits, SW_HIGH+U ≤3.50 µs with valid low reset and healthy VIN_PROTECTED ≥8.30 V. Standalone ripple magnitude remains **OPEN** until a requirement is declared. **If it fails:** rule out measurement artifacts without discarding the original capture; investigate layout/source stability/compensation or detector discrimination. Do not slow the watchdog or suppress peaks with filtering to obtain PASS.

### 8. Normal load transients, release, startup and input return

**Setup/settings:** retain both board banks and the real harness. At 9/24/26 V, COLD/HOT, command **0↔2.5 A, 2.5↔5 A and 0↔5 A**, with **ASSUMED 10 µs and 1 ms transitions** in both directions. Record actual slew/CC response. Start with the slower and lower-current transition; repeat nominal and C/ESR endpoints. **PRELIMINARY dwell 100 ms** between transitions, lengthened for settling/thermal constraints.

**Probes/capture:** TP301/TP302/far voltage, load current, IL201, TP502, SW_HIGH, PG_GOOD, FAULT, RUN_GATE and held rails. Trigger on load edge; retain pre-trigger steady state, all overshoot/troughs and settling. Declare the current tolerance and 5 A acceptance window before the run. Include zero-load release, authorized input ramps/removal/return and prebiased dummy cases only within reviewed boundaries.

**PASS:** `peak+U <5.5 V`, `minimum−U >=4.75 V` in the specified 5 A windows, no false disposal/latch on authorized transitions, valid source discriminator and component limits. No automatic reconnection after a disarming event. **If it fails:** STOP and inspect harness/bank dynamics and compensation; re-run affected normal tests after a correction. Do not advance to high-energy faults on a normal-load failure.

### 9. Input UVLO/OVP characterization before energized 27 V faults

**Setup/settings:** dummy load only, qualified source, no high-side injection. Observe J501/TP501, TP502, TP102, TP301/302/far, SHDN, PG and held rails. First prove no false OVP at 26 V. For undervoltage lockout (UVLO), use a reviewed slow ramp down/up around the fitted threshold. **PRELIMINARY ramp 0.1 V/s**, smaller steps near a transition; record actual slope.

Sweep OVP around its fitted trip/reset threshold, including 27 V, at COLD/HOT. Historical initial-only trip calculation is 26.973873–28.289211 V, not a measured hot bound. Any sweep beyond 27 V needs explicit component/source waveform review within the fixture's ≤30 V ceiling; stop if that boundary has not been qualified. Also characterize the reviewed dynamic edge/sag cases, using measured rather than invented field slew.

**Capture:** rising/falling thresholds, hysteresis, dynamic let-through, eFuse off state, source current, output peaks, restart behavior and control hold. **PASS:** no false trip within 9–26 V normal operation, all pin/energy/voltage limits and safe-off/re-arm policy; fitted thresholds within the approved tolerance analysis. Exact hot threshold/field surge acceptance remains OPEN until that analysis exists. **If it fails:** STOP and review input thresholds, source envelope and auxiliary independence. Record “source already isolated” when applicable at 27 V; never defeat OVP to relabel it an energized pass.

### 10. Configure synchronous fault acquisition

**Setup/settings:** before any energized fault, verify T13 and record instrument ranges. Minimum same-event channels are TP301 raw voltage, TP302 protected voltage, far-end voltage and IL201; add synchronized IMAIN, series current and both dump currents for timing/energy. Add source-referenced VGS/BST, actual PG/permissions, SHDN, detector/latch and all held rails. Repeat ancillary views only with documented repeatability; separate events cannot silently establish a same-event energy balance.

Use a FIRE/SHOT trigger for acquisition convenience, but define **t0 at actual QF1 conduction / L201 voltage change**, with an explicit threshold and uncertainty. **PRELIMINARY fast window:** ≥10 µs pre-trigger and ≥50 µs post-trigger at full bandwidth; retain a second or simultaneous long record through the entire millisecond tail and later restart checks. Extend both as measured behavior requires. No clipped peak or sensor overload is acceptable.

Save native waveforms and calibrated numeric exports, settings, probe/fixture photos and temperature records. Calculate `Q+ = integral(max(IMAIN,0) dt)` across the **whole** event; do not cancel reverse charge or stop at 10 µs. Account for offset/noise before positive clipping. Include separately fed diagnostic/auxiliary work at its actual boundary. Measure MOSFET `integral(VDS × ID dt)` and each ballast `integral(I²R dt)` plus uncertainty, sharing, SOA and repetition limits. Include all initial stores and positive source work; record reverse transfers separately.

**PASS:** demonstrable Upeak/Umin/Ut/UQ/UE at the actual bandwidth/duration. If 15 mV voltage uncertainty is substantiated, measured peak must be **<5.485 V** and measured normal minimum **≥4.765 V**; otherwise use the actual larger uncertainty. Use the test plan's complete uncertainty equations, including relative voltage/current skew (`Uskew`), sensor settling and extended record duration. **If it fails:** acquisition is INCONCLUSIVE; improve metrology before another stress pulse. An arbitrary guard band cannot repair a missed peak.

### 11. Qualify the external fixture separately — T12F3/T12D

**Setup:** no DUT force connection. Controller/driver coupons first, with drains strapped to local sources and all drain-energy stores absent; then an independently rated passive surrogate. Complete visual/continuity checks and applicable hot SOA/reverse-path reviews before each energy increase. Use the exact fixture BOM/netlist and record the separately reviewed energy steps; their numeric progression is **OPEN** until actual hardware ratings are known.

1. Verify SF1 STOP, SF2 RESET, released SF3/SF4, PSF2 at 12 V and actual FX12 ≤13 V. Qualify all manual states/bounce, held controls and 0.3–1.8 V FX5 plateaus, abrupt FX12/driver-supply loss and return. Verify no uncommanded connection. Demonstrate ≥100 ms stable valid fixture supplies before ARM and loaded bootstrap at actual TS, including source-pair TS near 30 V.
2. Inspect four parallel 9.1 Ω NH250 resistors, each on its own 12×12×0.125 inch aluminum panel. Measure resistance with thermal drift; source current+U ≤14 A, FX_LIMITED no lower than −1 V for that box, source terminal voltage+U ≤30 V. Force-joint allocation ≤0.2 mΩ each, injection-loop L ≤40 nH. Count main C ≤30 µF plus fixture/stray ≤3 µF and all control coupling/feeder energy.
3. On the surrogate only, provide reviewed synthetic PG/permission stimuli, operate fixture RESET → enable SF1 → fresh SF3 ARM, confirm START_OK, then operate SF4 FIRE. Verify native isolation **by physical current**, ≤1.50 µs, before dead-ready (calculated minimum 1.871076 µs). Verify the permission recheck and injection onset ≤0.5 µs after DEAD_READY; loss of PG before it must suppress the attempt. These surrogate stimuli qualify fixture behavior only; integrated DUT runs require genuine PG/permission.
4. Defeat the surrogate's DUT-like shutdown to test the independent emergency ceiling, never disable the real DUT for this purpose. Capture QF1/QF4/5 current extinction ≤20 µs from t0, no retrigger after held/bouncing FIRE/ARM, control-loss/STOP behavior and QF1 body-diode return into VIN_PROTECTED. Confirm no fixture action steals the DUT's full 10 µs interval; earliest intended abort screen is 12.626273 µs after t0.
5. Review measured positive/negative current, VDS+U ≤50 V, abs(VGS)+U <20 V and on VGS−U ≥10 V, every hot SOA/pulse/thermal limit, reverse commutation and negative node limits. The **CALCULATED 24.032 mJ added / 189.556370 mJ coupled** pools are conditional screens, not equipment ratings. The ~98 A first positive screen does not bound the possible larger reverse interval; do not extrapolate the Ldiff qualification beyond 100 A.
6. Perform the full discharge test with DUT-like dumps disabled and enabled separately. Use Step 13's node table and floating stores; require residual magnitudes+U ≤0.3 V within 60 s and for a further 60 s without rebound.

**Capture:** all timing/current/energy/thermal/discharge evidence and faulted-control cases. **PASS:** all T12F3/T12D conditions, rated passive surrogate and calibrated measurements; no unreviewed source, return or reservoir. **If it fails:** quarantine fixture, fix and requalify before DUT force connection.

The limiter drops voltage. Establish 9/24/26 V **at the DUT**, compensating PSF1 only within ≤30 V. At a 9 V supply setpoint the limiter's maximum power screen is only 9.094 W. If a requested voltage/load cannot be held, mark **NOT EXECUTABLE** and revise the source fixture through review. Never bypass the limiter while armed or call a sagged-source run a valid 5 A containment test.

### 12. Fault-injection tests

Run the isolated versions of F1/F2 during Step 0. F1 always keeps main/series/injection force paths absent; repeat F2 on integrated dummy hardware only after all applicable prerequisites and normal tests pass. F3 is a raw-only preliminary test. F4/F5 are distinct containment modes. Every fault starts at the minimum separately reviewed energy/current; inspect traces and temperatures before increasing. Preserve the actual source/load/temperature/C/ESR/phase matrix. No Pi throughout.

#### F1. Manual RESET/ARM and persistent-short rejection — T15F3-D

**Setup/settings:** main/series/injection force paths absent, board auxiliary coupon supply bounded; S601 DIAG. Start diagnostic characterization at ≤1 mA (healthy acceptance may then be unavailable); qualify the selected 470 Ω probe before its ≤11.200 mA acceptance runs. Fit each **0/1/10/100 Ω native VIN_PROTECTED–U201 SW fault** only while all supplies are off/discharged. Use coupon fault parts within their current/thermal ratings.

**Probes:** TP502, PF3/native SW, TP301/302, DIAG_VIN_OK/SW_ZERO/RAW_ZERO/PROT_ZERO/DIAG_READY, J602 RESET, NOFAULT, ARMED, TP101, RUN_GATE and both actual series VGS.

1. With no fault, execute Step 4's DIAG/reset/release/RUN/fresh-ARM logic sequence while force paths remain isolated; verify intended transitions.
2. Repeat with each short, including fixture QF2/3 isolation open. Press, hold and bounce RESET/ARM; select DIAG/RUN through their approved sequence. A discharged raw bank alone must never establish repair.
3. Remove the fault only unpowered, recheck native sense-lead continuity, and repeat the healthy sequence. Check RESET in RUN is rejected and the probe is physically disconnected in RUN.

**Capture:** diagnostic currents/voltages, switch break-before-make, debounce/release timing and all latch/gate states. **PASS:** each persistent short rejects RESET; no main/series permission, no self-rearm; healthy reset needs valid references, diagnostic VIN above max threshold, zero nodes+U ≤0.30 V and a deliberate release/fresh ARM. **If it fails:** stop at coupon level and revise the diagnostic/interlock. This DC screen does not qualify intermittent or high-voltage-only faults.

#### F2. PG, control-rail loss, held controls and recovery — T15F3/T07B

**Setup/settings:** first isolated coupons with no force paths; later bounded integrated dummy runs at 9/24/26 V, COLD/HOT. Use reviewed prewired, limited stimuli on their named sense/supply nodes; never drive an IC output against another source. **PRELIMINARY stimuli:** 1 µs, 1 ms and 1 s rail collapse/rise, and SAFE5 plateaus 0.3–1.8 V with other rails present/absent. Direct SER_DRV short is initially a separately bounded supply/gate coupon test, not an arbitrary high-energy rail short.

| Case | Action and required result |
| --- | --- |
| Ordinary PG loss after PG_SEEN | Remove genuine PG through reviewed means; main/series off, dumps not fired solely by PG; PG return alone never rearms. |
| PG early/high near ARM | Sweep already-high/stuck-high and near-coincident PG/ARM plus brief PG-loss feedback pulses. Check asynchronous-clear pulse width/recovery against the pinned flip-flop data. Unproved veto is a current blocker; failure requires circuit revision. |
| Genuine OV or source trip plus PG loss | Apply independently bounded fault stimulus and PG loss together over relative delays. Fault wins, NOFAULT clears, both dumps remain commanded through safe decay; PG must not mask or clear the fault. |
| DET5 / 3V3_AUX / SAFE5 loss | Exercise each order, intermediate SAFE5 and return with RESET/ARM/SERVICE held/bouncing. Default SHDN/series off throughout invalid states; no phantom permission or rail backpower. |
| Main eFuse off, raw input maintained | Assert reviewed SHDN sink/open main permission; verify upstream auxiliary controls remain valid continuously. Do not replace this with whole-input removal. |
| Auxiliary stopper off / entire input removed | Exercise separately; capture loaded driver/reference hold through actual current and bank decay, followed by safe gates and no restart. |
| DRV_HOLD collapse / direct SER_DRV collapse | Test separately at bounded energy; verify isolated C660 behavior, U301 UVLO/TGDN, both actual VGS and physical current-off. No guaranteed direct-short turn-off is inferred from passive bleeds. |
| Input/rail return, persistent fault, held RESET/ARM | Maintain only the reviewed bounded fault. No automatic reconnection; full power loss requires DIAG/RESET/release/RUN/fresh ARM again. |

**Probes/capture:** all relevant rails, POR/READY/release/PG memories, FAULT, SHDN, RUN, DISPOSAL, series/dump VGS and currents on a common timebase. **PASS:** table policy, far-end upper bound whenever energy is present, all ratings, measured hold beyond required disposal plus uncertainty. Conditional rail-loss targets: SHDN crossing ≤1.30 µs, source-current endpoint+Ut ≤3.225 µs and series-current endpoint ≤3 µs from the applicable threshold. These are **PRELIMINARY allocations**, not established guarantees; record actual min/max. **If it fails:** STOP and return to coupon/circuit revision; do not make a software reset workaround.

#### F3. Raw-path preliminary pulse — buck disabled

**Setup/settings:** accepted fixture, protected force/load path absent, buck EN low, minimum bounded source energy, raw bank/L201/dump/return within reviewed ratings. Genuine PG will ordinarily be low. The standard fixture therefore vetoes FIRE; any synthetic-permission/raw-only test arrangement needs its own reviewed coupon wiring and remains explicitly synthetic. Do not jumper genuine-PG inputs on the integrated board.

**Probes/capture:** PF2/PF3/PF4, TP301, IL201, IMAIN, raw-dump current, QF gates, SW/BOOT pin differentials and negative excursions, held rails and temperatures. Apply only the documented raw-only pulse; show current and bank tail/discharge.

**PASS for this subtest only:** fixture/current/energy/return ratings, raw peak+U ≤6.9 V for a DUT raw-containment claim, complete rated disposal and no damage/overstress. **No full Architecture D or far-end containment PASS** follows from disabled buck or synthetic PG. **If it fails or the required raw-only arrangement is absent:** STOP/BLOCKED; resolve at coupon level before full stress.

#### F4. Actual-path autonomous high-side fault — mode A, T01/T08/T09/T10

**Setup/settings:** all prerequisite gates closed, accepted fixture, real U101/source/local C/L201, both board banks and real harness/dummy model fitted. All contacts/force probes installed unpowered. Repeat the 9/24/26 V and **eligible energized 27 V** × 0/2.5/5 A × COLD/HOT matrix, both onset-phase extremes and C/ESR variants. Begin with the lowest separately bounded energy and zero external load; the banks still store energy.

1. Verify temperatures, instrument headroom, energy ledger, SFD1–4 open, normal source setting/limit, SF1 STOP and FIRE/ARM released. Complete board DIAG/RESET/RUN and the reviewed physical main-source sequence without powered rewiring.
2. With qualified fixture controls stable ≥100 ms, operate SF2 RESET and release, close SF1 to enable, then fresh SF3 ARM. QF4/5 source and QF2/3 native paths may turn on; QF1 remains off. Deliberately ARM the board per Step 4 with PG initially low. Let genuine PG rise, banks settle and the selected load stabilize. Confirm genuine PG_GOOD/MAIN_PERMISSION at JF2/JF3 and actual VGS/current states.
3. Arm acquisition and operate **SF4 FIRE once**. Hardware opens QF2/3, waits its qualified dead interval, rechecks genuine PG/permission, then closes QF1. If permission is lost before DEAD_READY, record INVALID ATTEMPT; do not force PG. After injection starts, later PG loss must not prematurely open QF1 and rescue the DUT.
4. Capture t0, source/series cutoff and both dump onsets, full current tail, source recharge/negative transfers and all peaks. Leave S601 RUN so the diagnostic feed cannot replenish the output. Record ABORT even if the DUT already contained the event.
5. Establish the disposal endpoint and integrate Q+ over the complete record. The required maintained-input latch/leakage check is separate: ≥60 s and until temperatures settle, all output banks ≤0.3 V, no restart and rated leakage power. **OPEN interface:** FIX3 automatically aborts the source after each shot; an approved prewired maintained-input arrangement is needed for this check. Do not defeat ABORT or reconnect a failed path ad hoc. Without that evidence the full test remains incomplete.
6. STOP/discharge per Step 13, inspect, check shunt/force continuity and component drift, and review all waveforms/energy/temperatures before the next point. Reset only after removing/diagnosing the fault with F1's sequence.

**PASS per event:** far peak+U <5.5 V; raw peak+U ≤6.9 V; physical source extinction+Ut ≤10 µs and Q++UQ ≤100 µC; source/L/C/current domain valid; all component waveform/hot-SOA/thermal limits; valid controls through actual decay; no automatic rearm or fixture rescue. Report source, series, raw/protected disposal endpoints separately. T08 development targets are useful disposal and abs(Iseries) ≤0.10 A within 0.5 µs of actual detector-overdrive endpoint; passing those alone does not establish containment.

**If it fails:** STOP and retain evidence; do not increase energy. Fixture abort necessary to save the board = containment FAIL or incomplete/invalid result, never PASS. Continuous-high external injection cannot close the known pulsed/internal-bridge coverage gap; that remains T01F3-F evidence even if all these shots pass.

#### F5. Timed source-contract characterization — mode B

**Setup/settings:** same accepted source/banks/harness/probes as F4. Mode B adds an independently qualified timed SHDN sink at the verified TP101/INPUT_SHDN hook, with delay calibrated from physical t0 so **actual source-current endpoint+Ut ≤10 µs** and Q++UQ ≤100 µC. A 10 µs command delay is already too late to assume a 10 µs current endpoint.

**OPEN:** the FIX3 fixture CSV has no selected mode-B timed SHDN accessory. Its isolated interface, sink/current limits, default-off behavior, drive conflicts, time reference and delay range must be reviewed and recorded before this test. Do not wire FIRE/SHOT/ABORT directly to SHDN, or short comparator/latch outputs. If absent, record BLOCKED; mode A remains unchanged.

After acceptance of that accessory, repeat F4's manual sequence, record its timed assertion separately from autonomous SRC_TRIP/FAULT, and measure all physical endpoints. Do not disable or modify the autonomous protection silently. If it trips first, record the realized shorter source exposure; it does not prove the intended worst-case timed exposure.

**Capture/PASS:** same voltage, charge, component-energy, control/tail and uncertainty criteria as F4 for the **realized conditional source contract**. **Mode B alone cannot PASS autonomous containment.** **If it fails or intended exposure is not obtained:** STOP, review accessory/source timing and mark the affected point failed or incomplete. Never extend the emergency ceiling or turn off a working DUT protection to force exposure without a separately reviewed test configuration.

#### F6. Harness integrity, output faults and reverse/backfeed behavior

**Setup/settings:** first low-current, bounded dummy tests. Fit branch-open/high-resistance fault adapters only while unpowered and review the remaining contacts' maximum current. Never disconnect one positive branch live at 5 A. Use rated, prewired output-short/prebias fixtures only after current, duration, source energy and component ratings are specified; those output-overload/reverse-test envelopes are currently **OPEN**. Input reverse-polarity magnitude/duration/current/leakage acceptance also remains OPEN: use a separately reviewed bounded input coupon to establish Q101/Q102 and companion-pin behavior before any integrated reverse-input test; do not simply reverse the 26 V bench leads.

**Probes/capture:** TP301/302/503, both far positives and loaded returns, individual branch/return currents, TP402−TP403, local/host rails, SHDN/FAULT and temperatures. For a reviewed reverse-input coupon also capture TP501/TP502-equivalent nodes, input current and Q101 VGS/VDS. Test branch imbalance/contact faults within the reviewed branch-current bound. For external dummy output prebias, main off, measure any upstream reverse current and rail charging; repeat reviewed input-return cases without a Pi.

**PASS:** no contact/wire overload, alternate return or forbidden backfeed/reconnection; far upper bound and applicable normal minimum, fault isolation and all component limits. Quantitative reverse-leakage/overload limits must be declared from the reviewed interface; absent limits make that subtest BLOCKED. **If it fails:** STOP and repair harness/domain protection; do not solve it by adding an unrecorded return wire or paralleling an SBC supply.

#### F7. Auxiliary-only surge and actual upstream source — T14A/T14B

**Setup/settings:** separate aux-only coupon with every main-buck force connection absent and a reviewed **0–60 V** pulse fixture. Stage upward in energy before the **PRELIMINARY development waveform:** 26 V baseline, 10 µs rise, 58.1 V plateau for 1 ms, 10 µs fall; 10 pulses ≥60 s apart and only after temperatures return. Bound source ≤0.20 A, extra reservoir ≤1 µF and incremental positive work ≤20 mJ; count coupon stores separately.

**Probes/capture:** AUX_RAW/LIMITED, Q316 VDS/ID, TMR/RUN, DRV_HOLD/SER_DRV/BST, all control rails and local temperatures with suitable HV differential probes. **PASS:** AUX_LIMITED+U ≤35 V, applicable hot linear SOA/pin/thermal limits, no degradation, and control/disposal remains valid through loss/trip before disarmed recovery. T07F's Q316 box (≤58.1 V, ≤0.20 A, ≤1.02 ms) is a development allocation requiring actual trajectory evidence.

**If equipment/rating is missing or it fails:** BLOCKED/STOP; do not apply 58.1 V through the FIX3 fixture or to the main buck. Aux-only PASS does not qualify whole-input surge. T14B additionally needs the actual isolated 48→24 V converter model/revision, source L/R/C/current/overshoot and field envelope, D101 hot pulse evidence, and F101 total-clearing/DC-interruption coordination. That source selection remains OPEN; never connect the future robot battery directly to V1A or infer containment from an OVP threshold.

### 13. Shutdown, discharge, inspection and recovery — T12D/T12F3-D

Apply the stop sequence, independently isolate every source and backfeed, then use the prewired passive adapters. **PASS for handling: every listed residual magnitude+U ≤0.3 V within 60 s, maintained for another 60 s without rebound**, with dumps disabled and enabled in separate qualification trials. Never short a capacitor with a tool. Check all additional islands discovered on the actual assembly.

| Discharge path | Node / its own return | Value / check |
| --- | --- | --- |
| RFD01 / JFD01 | VIN_PROTECTED / FGND | 10 kΩ |
| RFD02 / JFD02 | VOUT_5V1 / FGND | 1 kΩ |
| RFD03 / JFD03 | VOUT_PROTECTED / FGND | 1 kΩ |
| RFD04 / JFD04 | FAR_5V / FAR_GND | 1 kΩ; no extra FAR_GND–FGND wire |
| RFD05/06/07, JFD05/06/07 | DRV_HOLD / AUX_12V / AUX_PREHOLD, each to FGND | 10 kΩ each |
| RFD08/09, JFD08/09 | AUX_LIMITED / VIN_AUX, each to FGND | 47 kΩ each; verify actual VIN_AUX/AUX_RAW assembly mapping |
| RFD10/11/12, JFD10/11/12 | DET5 / 3V3_AUX / REF_2V5, each to FGND | 10 kΩ each |
| RFD13/14/15/16, JFD13–16 | SAFE_IN / SAFE5 / SER_DRV / REF_SAFE_2V5, each to FGND | 10 kΩ each |
| RFD17/18, JFD17/18 | FX_LOGIC_IN / FX5, each to FGND | 10 kΩ each |
| RFD19/20 | FX_LIMITED / DUT_IN, each to FGND | 10 kΩ each |
| RF61/62/63 | FX_DRV1 / FX_DRV2 / FX_DRV3, each to FGND | 10 kΩ each |
| SFD1 + RF91 | FBST1 / L201_IN | 100 kΩ; close only after sources disconnected |
| SFD2 + RF92 | FBST2 / FX_ISO_MID | 100 kΩ, floating reference |
| SFD3 + RF93 | FBST3 / FX_SOURCE_MID | 100 kΩ, floating reference |
| SFD4 + RF94 | PROT_BST / PROT_MID | 100 kΩ, floating reference |
| Additional stores | PS outputs, FX12, AUX_RAW/VIN_AUX, U317 internal VCC and both BST–SW capacitors, U201 BOOT–SW, 3V3_LOCAL/HOST, all gate–source and common-source islands | Map and independently qualify discharge; no assumed common return or zero energy |

These are characterized loads, not pulse aborts. Confirm resistor power/temperature ratings (selected 1206 adapter allocation ≤0.125 W at ≤70°C) and actual capacitance before relying on RC estimates. A remaining charge is FAIL: maintain isolation, identify replenishment and discharge by the reviewed path before touching. After safe discharge inspect parts, four-wire force/shunt resistances, connector condition and leakage. Full power loss demands a new diagnostic/reset/ARM sequence; preserve every failed trace.

### 14. Telemetry and host-domain validation — after all fault tests

**Setup/settings:** after fault survival inspection and all applicable fault gates pass, use dummy load plus a current-limited host emulator, not a Pi. Connect J503 only unpowered: .1 GND, .2 3V3_HOST, .3 SDA_HOST, .4 SCL_HOST after confirming actual assembly pinning. Start I2C at the review's **100 kHz**, address **0x40**; record pull-ups, bus capacitance, firmware and INA228 register configuration.

1. Re-measure R401 four-wire resistance, polarity and Kelvin isolation before current. Nominal 2 mΩ gives **CALCULATED 10 mV and 50 mW at 5 A**. Verify actual tolerance, temperature coefficient, fault-pulse survival and sense-filter/pin limits.
2. At 0/0.10/0.50/1/2.5/5 A within accepted ratings, compare calibrated DMM/current reference to INA228 voltage/current/power and integrated energy over a recorded interval. Repeat relevant temperatures. Declare accuracy/error acceptance before testing; it is currently OPEN. Do not treat the ±20.48 A analog-range example as a board-current rating.
3. Capture TP402−TP403, TP404 3V3_LOCAL, TP401 ALERT, J503 host rail and SDA/SCL on both sides. Exercise host-only, local-only, both-on and both-off; add externally powered dummy output only under F6's qualified prebias boundary. Check powered-off rail injection, bus lows/rise/ACK, stuck bus and polarity.
4. Cycle local power and record resets, overflow, calibration reinitialization and accumulator gaps. Positive current is V1A's contribution across the shunt; it excludes upstream/module losses. INA228 bus voltage references module GND, so it does not replace the differential far-end voltage measurement. Unsigned ENERGY is not automatically signed net energy.

**PASS:** declared calibrated V/I/P/E accuracy and temperature range, correct sign/boundary, valid bus levels/timing, no forbidden rail/host backpower and honest reset/gap handling. **If it fails or accuracy limits remain missing:** disconnect host emulator, STOP/BLOCKED for telemetry/integration; repair/calibrate and repeat affected domain tests. No SBC connection to debug it.

### 15. Review and integration decision

**Setup/capture:** collate Records A–F, all raw evidence, failed/repeated runs and the exact hardware/fixture/source revisions. Verify normal matrix (18 combinations for 9/24/26 V × 0/2.5/5 A × COLD/HOT per chosen C/ESR), transient matrix in both directions, and fault matrix (24 nominal combinations including 27 V per mode/C/ESR, explicitly marking source-isolated/unreachable points). Extend to actual Pi C/ESR/load response and reviewed production temperatures when known. Do not relabel room testing as minimum-temperature qualification.

**PASS to propose Pi integration:** every applicable fault test including coverage, reset/rail loss, maintained-input latch, source coordination and domains passes; all normal voltage/thermal/harness/telemetry gates pass; actual Pi input range and male-header/contact rating, power-only wiring and interface policy are closed. The owner records the integration decision after engineering review. Otherwise status stays **BLOCKED — NO Pi**. No USB 3.x or D435i data route through this PCB is introduced.

At an actual gate end, update [FINAL_MANAGER_REPORT.md](../FINAL_MANAGER_REPORT.md) with STATUS, WHAT WAS DONE, EVIDENCE, DECISIONS, OPEN RISKS and NEXT GATE. Software/document checks or completion of these blank sheets are not physical validation.

### Document review record — 2026-10-03

**EVIDENCE, documentation only:** all 22 local links in this procedure resolve; numbered Steps 0–15, Faults F1–F7 and Records A–F are present. Probe identities and manual-switch polarity were cross-checked against the retained netlist and current FIX3 pin contracts. `python3 -B scripts/check_repository.py` reports 19 existing broken-link errors; running the same checker on a temporary archive of baseline `898759e` produces the identical 19 errors, with no new errors from this file. Historical/source files were preserved. No hardware, ERC/DRC or electrical test was performed; all bench result fields remain NOT RUN.

**Git handoff:** local staging for the requested commit failed because Git could not create the `wt-bench/index.lock` file (`Operation not permitted`). The procedure is left uncommitted under the task's explicit fallback; no permission or lock workaround was attempted.

## Printable records — duplicate one set per assembly and run

Use PASS / FAIL / INCONCLUSIVE / BLOCKED / NOT RUN / NOT EXECUTABLE. Explain every non-PASS. A blank cell is missing evidence, never an implicit PASS. Store evidence under `docs/bench/` in a dated run directory when tests actually occur; preserve native waveforms and failed runs. Record exact commands/software for any waveform reduction so another student can reproduce the result.

### Record A — authorization, equipment and bounds

| Field | Entry |
| --- | --- |
| Date/time/operator; owner review | ______________________________ |
| Procedure commit; board serial/revision/rework | ______________________________ |
| Source/fixture/harness/emulator revisions | ______________________________ |
| R2 / R3 / R4 authorization evidence | ______________________________ |
| Goal / hypothesis / test IDs / prerequisites | ______________________________ |
| Main and control supplies: models/serials/calibration | ______________________________ |
| Main/aux/fixture V and I settings; source output C/L/R | ______________________________ |
| Scope/options/probes/sensors: model/serial/range/calibration | ______________________________ |
| Load / meters / thermal equipment and calibration | ______________________________ |
| Approved source/current/energy/abort/return/SOA envelope | ______________________________ |
| Reviewed service isolator/aux feed / mode-B / maintained-input interface | ______________________________ |
| Actual C/ESR of main/raw/protected/dummy; Ldiff/DCR domain | ______________________________ |
| Ambient/airflow/enclosure; COLD/HOT definition | ______________________________ |
| Upeak / Umin / Ut / Uendpoint / UQ / UE / Uskew method | ______________________________ |
| Scope bandwidth/sample rate/memory/deskew/trigger/windows | ______________________________ |
| Load tolerance/settling/5 A acceptance window | ______________________________ |
| OPEN prerequisites and test exclusions; disposition | ______________________________ |

### Record B — inspection, probe map and controls

| Point/control | Actual pad/pin/net / reference | Continuity / observation | Photo/evidence | Result |
| --- | --- | --- | --- | --- |
| TP501/502, IMAIN_FORCE | __________________ | __________ | __________ | ______ |
| PF3/PF4, TP201/202, IL201 | __________________ | __________ | __________ | ______ |
| TP301/302/503, far +2/+4/GND | __________________ | __________ | __________ | ______ |
| TP304/305/BST, both dump links | __________________ | __________ | __________ | ______ |
| TP306–312 mapping / FAULT / SHDN | __________________ | __________ | __________ | ______ |
| New rails / reference / latch pads | __________________ | __________ | __________ | ______ |
| TP402/403/405/406, J503 | __________________ | __________ | __________ | ______ |
| J601/J602, S601 DIAG/RUN | __________________ | __________ | __________ | ______ |
| SF1 STOP, SF2/3/4, JF2/JF3 | __________________ | __________ | __________ | ______ |
| Earth/load/USB/far-return diagram | __________________ | __________ | __________ | ______ |
| Other / fault adapter | __________________ | __________ | __________ | ______ |

### Record C — normal-load, thermal, ripple and transient run

Run ID: __________  Prerequisite evidence: __________  Raw directory: __________

| Input at DUT / load / temperature / C–ESR case | Raw/protected/far mean | Far minimum−U / peak+U | Ripple full / 20 MHz | Result |
| --- | --- | --- | --- | --- |
| __________________________ | __________ | __________ | __________ | ______ |
| __________________________ | __________ | __________ | __________ | ______ |
| __________________________ | __________ | __________ | __________ | ______ |
| __________________________ | __________ | __________ | __________ | ______ |

| Measurement / condition | Value + uncertainty / evidence |
| --- | --- |
| Main V/I/P; far V/I/P; efficiency boundary | ______________________________ |
| Actual transition endpoints/slew/window/dwell | ______________________________ |
| Both positive branch currents / contact ratings | ______________________________ |
| Hot pole/contact/splice/loop resistance / ratio | ______________________________ |
| Component temperatures / thermal stabilization / junction method | ______________________________ |
| VGS / held rails / SW_HIGH max / minimum VIN | ______________________________ |
| Startup/PG/FAULT/SHDN; source CC or dropout observed | ______________________________ |
| Capture/settings/photos / analysis commands | ______________________________ |
| Interpretation / limitation / failure action / retest ID | ______________________________ |

### Record D — one sheet per fault event

| Field | Entry |
| --- | --- |
| Run ID / F-test / T-test / mode A or B / fault mechanism | ______________________________ |
| Initial DUT input / actual source V/I limit / load / temperature | ______________________________ |
| Main/raw/protected/far C/ESR; harness and L/current domain | ______________________________ |
| Fault adapter / energy stage / rated hot SOA evidence | ______________________________ |
| Genuine PG/permission before FIRE and DEAD_READY | ______________________________ |
| S601 probe disconnected / SF controls / all stores accounted | ______________________________ |
| t0 physical definition / trigger offset / timing uncertainty | ______________________________ |
| Raw / protected / each far positive peak + Upeak | ______________________________ |
| Source off time + Ut / endpoint current + Uendpoint | ______________________________ |
| Series current-off / useful raw and protected dump endpoints | ______________________________ |
| Maximum positive / negative IL201, source and branch currents | ______________________________ |
| Complete-event duration / Q+ / UQ / later replenishment | ______________________________ |
| Initial stores / positive work / reverse transfer / balance ± UE | ______________________________ |
| Each FET VDS/VGS/ID/energy / each ballast I²R energy / SOA margin | ______________________________ |
| Pre-pulse / peak ballast and other temperatures + uncertainty | ______________________________ |
| Loaded rail/bootstrap hold versus required safe-decay duration | ______________________________ |
| Disposal endpoint / ≥1 ms no rebound / ≥60 s maintained-input latch | ______________________________ |
| Fixture ABORT time / source sag / fixture rescue / intended exposure | ______________________________ |
| RESET/ARM/PG/rail return / persistent-fault response | ______________________________ |
| Native captures / calibrated exports / settings / photos / commands | ______________________________ |
| PASS/FAIL/etc.; exact criterion; next action / retest | ______________________________ |

### Record E — discharge and post-fault inspection

Record each node separately, including every member of grouped rows. Date/run: __________

| Node group (see Step 13) | Worst abs(V)+U at 60 s | Worst next 60 s / rebound | Individual trace IDs | Result |
| --- | --- | --- | --- | --- |
| RFD01–04 input/raw/protected/far | __________ | __________ | __________ | ______ |
| RFD05–09 held/converter/auxiliary | __________ | __________ | __________ | ______ |
| RFD10–16 logic/reference/SER_DRV | __________ | __________ | __________ | ______ |
| RFD17–20 fixture logic/source | __________ | __________ | __________ | ______ |
| FX_DRV1/2/3 and FX12 | __________ | __________ | __________ | ______ |
| SFD1/2/3/4 floating BST–TS | __________ | __________ | __________ | ______ |
| U201/U317 floating/internal stores | __________ | __________ | __________ | ______ |
| All VGS/common-source/local/host/extra islands | __________ | __________ | __________ | ______ |

Sources/backfeed physically isolated: __________  Dumps enabled/disabled trial: __________

Post-fault visual / shunt / contact / leakage findings: ______________________________

Handling released by operator after measured discharge: __________  Fault repair/retest: __________

### Record F — coverage and final disposition

| Test group | Required cases / evidence | Result / unresolved item |
| --- | --- | --- |
| Identity/continuity/instrument/isolated prerequisites | __________________ | __________________ |
| Normal 18-point matrix + C/ESR endpoints | __________________ | __________________ |
| Thermal/ripple/transients/startup/UVLO/OVP | __________________ | __________________ |
| Source discriminator normal and admitted-fault coverage | __________________ | __________________ |
| F1 diagnostic shorts / held RESET/ARM | __________________ | __________________ |
| F2 every rail/PG/recovery/hard-collapse case | __________________ | __________________ |
| F3 raw-only / F4 autonomous / F5 timed matrix | __________________ | __________________ |
| Maintained-input latch / whole-event charge and energy | __________________ | __________________ |
| F6 harness / reverse / reviewed output faults | __________________ | __________________ |
| F7 aux surge / actual source and fuse/TVS coordination | __________________ | __________________ |
| Fixture abort/defaults / independent all-store discharge | __________________ | __________________ |
| Telemetry accuracy / host-local domain matrix | __________________ | __________________ |
| Actual Pi C/ESR/input/header/interface qualification | __________________ | __________________ |

**STATUS (default BLOCKED — NO Pi):** __________

**WHAT WAS DONE / EVIDENCE:** ________________________________________________

**DECISIONS / OPEN RISKS / NEXT GATE:** _______________________________________

Owner's later integration review/date (only after all required evidence): __________________
