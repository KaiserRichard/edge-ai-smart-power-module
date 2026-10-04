# Gate 4b — V1A R2 test-board schematic capture

2026-10-03. **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

**STATUS: CONDITIONAL PASS for the authorized schematic capture and review package. R2 electrical release: BLOCKED.** All physical tests are **NOT RUN**. ERC and connectivity checks do not establish electrical safety.

## WHAT WAS DONE

Continued the supplied partial work through `f2e80c2` and `74b9dc8`; did not restart. This resume addressed the two Sheet01/02 review findings, rechecked each sheet sequentially, and completed the previously missing reconciliation/inventory/validation artifacts and manager update. Sheet01/04 remain unchanged; Sheet02 exports L201_IN, Sheet03 restores the frozen observation front end, and Sheet02/03/05 explicitly describe bench proof as future acceptance. Earlier review/ERC records remain historical evidence.

**REQUIREMENT / DECISION:** architecture D test board; 9–26 V input; D101 SMCJ36CA; F101 Schurter 3403.0285.23; Phoenix J502 1776508 with 1777989 mate. Owner option A, 2026-10-01, permits manual test hooks for autonomous source-fault triggering and unresolved brownout/PG-recovery/series-driver-loss behavior. It does not validate those functions.

| Sheet | Captured circuit / final evidence |
|---|---|
| 01 — input protection | 21 physical references: exact fuse/TVS, reverse protection, TPS26630 in latch-off mode, revised STPS commutation diode and exact passives. JP101 isolates/measures main source current before local buck input capacitance. [Current checkpoint](SHEET01_RESUME2_REVIEW.md); [fresh ERC](sheet01_resume2_erc.json) clean. |
| 02 — buck | 31 references: LM61460, selected Wurth 10 µH land, exact input ceramics, retained feedback/raw ceramics, native-SW and winding-current force links with paired sense/force access. L201_IN exported to the Sheet03 sensor. [Current checkpoint](SHEET02_RESUME2_REVIEW.md); [fresh ERC](sheet02_resume2_erc.json) clean. |
| 03 — output protection/control | 280 references: upstream auxiliary surge stopper/buck-boost, controlled held-bank charger, detector and control supplies, PG receiver, common-source series pair, protected crowbar, independent raw dump, bulk banks, manual controls and frozen SW/VIN observation front end. [Detailed review](SHEET03_REVIEW.md); [fresh ERC](sheet03_resume2_erc.json) clean. |
| 04 — telemetry | 23 references: 2 mΩ Kelvin shunt/INA228, symmetric differential filter, force observations, local regulator and separate host/local I2C domains. [Detailed review](SHEET04_REVIEW.md); [final ERC](sheet04_resume2_erc.json) clean. |
| 05 — interfaces | 11 references: retained J501/J502/J503 maps, selected external harness notes, M4 input/return and dummy-load force access. [Detailed review](SHEET05_REVIEW.md); [final ERC](sheet05_resume2_erc.json) clean. |

There are **366 physical references**, including PCB test pads/custom force interfaces, plus **12 nonphysical power-source declarations**. Relative to PR15: 123 physical references retained, 31 intentionally retired with obsolete Sheet03 circuits, 243 added. All physical references have assigned footprints; none uses an unresolved generic procurement placeholder. Custom identifiers are authored mechanical interfaces, not claims of purchasable complete assemblies.

The force path is `VOUT_5V1 → Q301 → PROT_MID → Q302 → JP301 → VOUT_PROTECTED → R401 force pads → LOAD_5V1 → J502`. Independent checks reject passive bypasses around the opposed pair. Raw and protected dump paths remain separate; no connector is moved upstream of protection.

## Test hooks and their limits

The native sheets now say **FUTURE ACCEPTANCE REQUIRED: “TEST HOOK — design proven on bench”. UNTESTED CANDIDATE; evidence NOT RUN.** This corrects the unsupported statement identified by the independent review while retaining the exact required phrase as a quoted future acceptance target.

| Hook | Captured function / limitation |
|---|---|
| U640 / U642 / U647 / TP337–340 | Frozen hysteretic SW and loaded VIN sensing front end, including clamps/isolation, for observation only. R640 senses the real L201_IN after JP201; R644 senses VIN_PROTECTED. Outputs never command SRC_TRIP or permission. |
| J603 / TP320 | Dry-contact source-fault command through U644; no autonomous fault discriminator. Manual actuation cannot prove fault-onset response ≤10 µs or positive charge ≤100 µC. |
| J302 | Manual reset of fault memory, with asynchronous fault priority under valid supplies. Persistent-short diagnosis is absent: repair/isolate/discharge and verify before reset. |
| JP600 / TP318 | Manual rail-valid link, absent by default; R729 pulls invalid. Bench rail verification precedes fitting. It cannot detect a later brownout. |
| J301 / J604 | Separate MAIN ARM and SERIES ARM dry contacts. Genuine PG qualifies series permission. In stable-supply logic, PG loss clears series memory; recovery alone supplies no clock edge. Bounce, timing races and partial power remain OPEN. |
| JP660 / TP313 / TP314 / TP334 | Removable SER_DRV feed and driver/gate/bootstrap observations for supply-loss characterization. Gate/bootstrap observations return to PROT_MID, not instrument earth. Reservoirs remain charged after a feed is removed. |
| JP101 / JP201 / JP202 / JP301 | M4 force isolation/current access for source, native switch, inductor and series path. These are not small signal-header shunts. |
| JP330 / JP331 | Independent protected/raw disposal-current access; opening a link disables that dump. |
| J605 / J606 | Guarded observations of genuine PG and MAIN_PERMISSION, not synthetic permission inputs. |
| JP501 / PF5 | Dummy-load force takeoff/return. Removing JP501 does not isolate an attached J502 load; J502 must also be unplugged for the documented isolated configuration. |

**DECISION:** isolated characterization starts with main/series/injection force connections absent. Reconfigure only after sources are disconnected and every store is measured discharged. External fixture circuitry remains separately documented at the pinned freeze; no fixture abort is credited as successful DUT containment.

## Review finding closure

[REVIEW_RESOLUTIONS.md](REVIEW_RESOLUTIONS.md) records both findings against the untouched external review. The source interface is now physically connected through the hierarchy and the frozen analog endpoint. Option A still replaces autonomous qualification/trip memory with the manual hook. Neither this repair nor clean ERC proves fault coverage. The bench-proof annotation now explicitly says the required outcome is unachieved.

## Pin, footprint and freeze evidence

- [Pin/land review](PIN_REVIEW.md) and independent [pin identities](PIN_CONTRACTS.json) distinguish pin numbers/names/EPs by exact package. [Manufacturer provenance](../../../../third_party/gate4b/SOURCES.json) preserves document revisions, URLs, reference/adaptation and retrieval limits.
- Eight new project footprints cover F101, L201, L301, U317, U327 and paired/force interfaces. All 14 existing PR15 project footprints and both library tables remain byte-identical. C358/C359's earlier wrong radial land was already corrected in `f2e80c2` to 8 mm diameter / 3.5 mm pitch.
- [Freeze coverage](FREEZE_COVERAGE.md) disposes all 40 rows, including external items and option-A substitutions. [Input provenance](INPUT_PROVENANCE.json) pins actual Git objects; [delta](CAPTURE_DELTA.json) preserves the complete reference/field/pin comparison.
- [Captured assembly inventory](CAPTURED_BOM.csv) is exported from the native XML. The separate BOM draft is stale for Sheets03–05; its quantities, old AHCT/control circuitry and earlier R312/R341 values are not silently applied here. Stock, pricing and assembly release are outside this handback.

## ERC, tests, net classes and drawings

**EVIDENCE:** KiCad CLI **9.0.6**, all severities including exclusions: **zero ERC violations** across all six sheets. No ERC severity setting or exclusion was changed from PR15. Power flags describe only real external or fitted component source paths, listed in PIN_REVIEW and independently checked; none asserts PG, RUN or MANUAL_RAILS_VALID. ERC cannot prove a strap fitted or a power device functioning.

The **50 regression tests** pass, including three new source-sensing boundary mutations. The fresh-netlist checker verifies the capture, manufacturer pin identities, every footprint's copper-pad numbers and independent power/control/Kelvin boundaries. Repository preservation checks chain the original records through PR15 to the authorized Gate4b scope, instead of applying the old footprint-only rule to new circuitry. See [final validation](FINAL_VALIDATION.json), [repository check](REPOSITORY_CHECK.json) and [scope](GATE4B_SCOPE.json).

| Net class | Named nets | Assignment / layout qualification |
|---|---:|---|
| HighCurrent | 29 | Input/output/load force paths, dump branches and GND. 2.0 mm editor width is **ASSUMED**, not rated copper. |
| Switching | 4 | BUCK_SW, L201_IN, AUX_SW1, AUX_SW2. 1.0 mm editor width is **ASSUMED**; high-current SW geometry still requires sizing. |
| Kelvin | 4 | SHUNT_KPLUS/MINUS and INA_IN_PLUS/MINUS. 0.2 mm preset; carry sense current only. |
| Signal | 121 | Remaining named control, reference and auxiliary nets. 0.2 mm preset; auxiliary/gate traces still require individual current/loop review. |

**EVIDENCE / LIMITATION:** all **158 named nets** resolve to the assigned classes in native PDF properties and exact project patterns. KiCad 9.0.6's raw XML labels **144 child-sheet nets Default** despite the project/PDF resolution; the original XML is retained without falsifying its class fields. [Class ledger](NET_CLASSES.csv) exposes both values. Verify actual class inheritance at authorized R3 PCB import. Class names/presets do not establish clearances, ampacity, pulse capacity, copper thickness, via count or thermal limits.

Full six-page PDF: [V1A_GATE4B_REVIEW.pdf](V1A_GATE4B_REVIEW.pdf). Native netlist: [captured.xml](captured.xml). Every page is marked **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**. Hierarchy is A3; Sheet01 A1; Sheet02/04/05 A2; Sheet03 A0 portrait. All six page renders were visually reviewed, with detailed review of the restored Sheet03 sensing front end and revised root interfaces. Functional groups use named-net connections. Print at native scale or zoom; reduced A4 print comfort has not been validated. No PCB or DRC/fabrication outputs were produced.

## 12 V source note

**OWNER INPUT:** V1A may be fed by the proposed 12 V isolated MEAN WELL DDR-60L-12. **CALCULATION:** the brief's 28.33 W input-demand screen is **3.15 A at 9 V** and **about 2.36 A at 12 V**. The design already covers the 9 V worst case; **the eFuse current limit, F101, TVS and input-trace design basis do not change for 12 V**. Actual V1A thermal behavior at 12 V remains **OPEN**. The proposed source's real impedance/transients and system compatibility still require the existing source review; these arithmetic values are not measured efficiency or temperature.

## OPEN RISKS and next gate

| OPEN item | Required closure |
|---|---|
| Autonomous source-fault coverage | Select/prove the autonomous qualifier/collapse-memory function and measure physical source cutoff/positive charge. Frozen analog sensing alone does not implement that function. Manual-trigger results cannot close autonomous timing. |
| Brownout/PG recovery/SER_DRV loss | Isolated rail-order, intermediate-voltage, held/bouncing-contact and race testing at actual gates/currents; circuit revision if required. No persistent-short diagnostic is fitted. |
| Bootstrap, detector and auxiliary supply | Actual-TS pump/leakage, detector partial-power/injection/settling, effective capacitance, startup/current-limit/compensation, hold through disposal and component thermal limits. Include the restored front end in SAFE5 load, shared-clamp/reference and probe-capacitance qualification. |
| Fault-energy containment | Hot MOSFET/diode/resistor ratings, negative return, nonlinear L/C/ESR/ESL, current sharing, source/series/dump endpoints and complete far-end peak. Four protected PCH parts remain a measurement candidate. |
| Normal power performance | Full 9–26 V operating/thermal/ripple/load-transient/efficiency limits, including **12 V thermal behavior**, regulator stability and inrush under actual loads. |
| Source/fuse/TVS coordination | Real source/surge/fault-current envelope, installed fuse hold/clearing and TVS hot clamp; no 58.1 V direct main-buck exposure is authorized. |
| Connectors, fixture and measurement | Hot complete J502/Pi contacts, current sharing/single-contact loss, indexed harness/tooling/splices, force-link copper/bolts/parasitics, bounded fixture/abort/discharge and calibrated instruments. |
| Telemetry and layout | Shunt pulse/thermal/tolerance/TCR and measurement calibration; host/local partial-power behavior; later copper/current, switching-loop, Kelvin/return, decoupling and thermal-path review. |

**NEXT GATE:** engineering review of this R2 test-board capture and the isolated-coupon/fixture test plan. R3 layout and R4 fabrication readiness are not released. Preserve the required bring-up order: visual inspection → continuity/short checks → current-limited bench supply → no-load startup → rail verification → low-current dummy load → increasing load → thermal → ripple → transient/load → protection/fault → telemetry → SBC only after all preceding gates pass. No Pi as the first load.

**Git handback:** local checkpoint attempts failed creating `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-gate4b/index.lock` with `Operation not permitted`. Per the brief, all this resume's schematic/script/review/evidence changes remain uncommitted for Claude. Existing commits remain intact; no lock manipulation, push, merge, purchase or gate advancement occurred.
