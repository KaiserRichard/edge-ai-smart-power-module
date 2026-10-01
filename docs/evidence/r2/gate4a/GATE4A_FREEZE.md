# Gate4a-FIX3 — final resumed design disposition

**VERDICT: BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Continued `a323a48`, `6caa8f9` and `692d30f`; no restart, native CAD edit, physical test or gate advancement. This report and the three linked FIX3 circuit contracts supersede conflicting round-1/2 status and wiring descriptions. Those reports and `history/9471e14` remain historical evidence.

## OWNER EXPLANATION — one page

**Two board issues still prevent integrated test-board freeze:** source-fault coverage, and default-off/PG recovery behavior. All three requested items now have concrete circuit candidates. The external fixture's qualification is a separate bench gate and does not block capture of isolated board hooks.

The source circuit uses TLV3201 hysteretic SW sensing, an LTC6994 4 µs qualifier, input-collapse memory, and a latched command to TPS26630 SHDN and both dumps. Its conditional source-current ceiling is 7.534151 µs. A repeating 3 µs high/1 µs low SW waveform with VIN=9 V evades both new detectors. That logic counterexample is not a measured damaged buck; it prevents claiming universal 10 µs coverage. T01F3 must establish fault signatures or drive a discriminator revision. U101 MODE is open for latch-off.

The interlock now specifies SAFE5, fast monitors, fault/ARM/release memory, a 470 Ω diagnostic probe and a physical DIAG/RUN switch. It rejects the specified 0/1/10/100 Ω persistent shorts within its DC screen. R609 is corrected to 100 kΩ for POR loading. Intermediate SAFE5 states, early/stuck-high PG and feedback pulse width, and direct SER_DRV collapse still need isolated T15F3 evidence or circuit revision. The conditional 4.514 ms hold calculation is not measured ride-through.

The separate fixture has 191 BOM entries and 557 pin records, with source resistors, opposed abort/isolation switches, hardware timers, dead disconnect, force pads and discharge paths. Resistor identities, hot-winding drift and the final PG check were corrected. Its conditional 18.773 µs emergency abort must never supply the DUT's 10 µs containment result. Hot SOA, reverse-current behavior, actual parasitics and instrument inventory remain unqualified. Hooks permit isolated evaluation with main/series/injection links absent.

Architecture D, 9–26 V input, SMCJ36CA, Schurter 3403.0285.23, the BSC034 pair and isolated upstream 48→24 V intent stay fixed. J502 solution A remains selected. Four-PCH/harness voltage, bootstrap, thermal, surge/source and calibration questions retain named tests. No Pi, fabrication or electrical-safety approval is given.

**Twenty-two numerical/connectivity tests pass; no hardware tests ran.** Forty register rows are synchronized. Local item commits were attempted but Git denied creation of index.lock; changes remain uncommitted under the brief's explicit fallback. No pull, push or permission bypass occurred.

## Review item → resolution → evidence

“Candidate selected” means concrete parts/nets, not validated behavior. Original independent-review closure remains **4/12** (R4A-02/03/05/11); no new hardware closure is claimed. External equipment and application measurements are not automatically board-capture blockers. The two explicit board limitations below still are.

| Review item | Current resolution and remaining disposition | Evidence / closure |
|---|---|---|
| R4A-01 source trigger | **Candidate selected; board freeze BLOCKED by coverage.** U640…647, 200k timer, VIN_SEEN and Q304/resistive SHDN default. Conditional 7.534151 µs; pulsed/internal-bridge case unproved. | [Source pin contract](FIX3_SOURCE_TRIGGER.md); S01-03/07; T01F3-N/F; actual timing/charge null |
| R4A-02 resistor identities | Original 348k/1M selections corrected to 0805. Fixture 2M moved to 1206 and 1Ω to supported 1% option. Exact ranges separate from lands. | S01-06/S03-13; fixture RF11…13/RF21…23; Vishay28758 pp1–4; T02/T16 |
| R4A-03 buffer identity | Original identity correction retained as history. AHCT translators are now DNP; SAFE5 comparator/ADG PG path replaces them. No inherited slew/sequence PASS transfers. | S03-05; [interlock](FIX3_INTERLOCK.md); T06F3/T15F3 |
| R4A-04 bootstrap | R3052M retained; U301 now uses isolated SER_DRV and 143k UVLO setting. Actual loaded TS≈5 V pump/turn-off remains a measurement. | S03-01/07; T04L/T04/T15F3 |
| R4A-05 capacitor references | C301 BST–TS and C302 REF–GND remain distinct; D302 anode moves to SER_DRV. Effective capacitance remains required. | S03-17; T05/T04/T06 |
| R4A-06 detector | Existing 9.88k/10k/1k/100k and reference-input protection retained; SAFE5 monitors add separate shunt/clamps/isolation. Dynamic/partial-power validity untested. | S03-02/03; FIX3_INTERLOCK; T06/T06F3 |
| R4A-07 auxiliary validity | Controlled charger/compensation retained; R34188.7k and R31232.4k restore static headroom. Total45mA, Ccharged≤600µF, hold4.513751ms are allocations. Fast monitor construction supplied; hard-loss/default-off remains board issue. | S03-11…18; FIX3_INTERLOCK; T07F3/T15F3 plus T07A…F |
| R4A-08 physical timing | Source and rail-loss budgets explicit; all actual source/series/dump min/max still OPEN. Conditional sums do not close arbitrary fault onset. | FIX3_SOURCE_TRIGGER; FIX3_INTERLOCK; CALCULATIONS; T08/T01F3/T15F3 |
| R4A-09 energy/returns | Raw99mΩ/protected33mΩ paths retained. Fixture adds24.032mJ; worst connected screen189.556370mJ. First positive current does not bound return current. Hot SOA/negative waveform remains pre-energization evidence. | RAW_NODE_ENERGY; FIX3_FIXTURE; T09A/B/C/T12F3 |
| R4A-10 receiving bank | Four PCH remain a measurement candidate. Prior5.713245V/5.542140V adverse screens retained; no capacitance-based waiver. | S03-10; T10: full-event far peak+U<5.5V, normal5A minimum−U≥4.75V |
| R4A-11 harness | Pinned J502 solution A/TE/Belden8502 selection retained. Hot current sharing, mixed mate, crimps and actual Pi header remain assembly/integration gates. | FIX2 F2-01; J502_SELECTION; T11/T16 |
| R4A-12 fixture | **External circuit/BOM/wiring selected.** Limiter, hardware abort, dead disconnect, force links and all-store discharge explicit. Application ratings/control-loss are T12F3; they block energized use, not board-hook capture. | [Fixture report](FIX3_FIXTURE.md); [BOM](FIX3_FIXTURE_BOM.csv); [pin netlist](FIX3_FIXTURE_NETLIST.csv); SFX-01/02 |
| R4A-13 uncertainty | Round-2 skew correction retained; actual inventory/calibration still OPEN. Every event needs measured Upeak/Ut/UQ/UE. | T13; numerical counterexample regression; no fabricated sensor accuracy |
| R4A-14 surge | 58.1V aux-only pulse needs a separate rated60V fixture; this30V injector is not that equipment. Actual upstream module/field surge remain OPEN. | T14A/B; no main-buck58.1V exposure |
| R4A-15 state/defaults | **Concrete candidate; board freeze BLOCKED.** Pin-level fault-priority reset/ARM/diagnostic and state table provided. Partial SAFE5, PG recovery/clear width and hard SER_DRV loss unresolved. | [Interlock contract](FIX3_INTERLOCK.md); S06-01; T15F3; thermal T15T |
| R4A-16 assembly | Forty-row delta register plus separate191-entry fixture BOM. Native captured netlist/lands and full procurement/assembly qualification are future work. | FREEZE_MANIFEST; PASSIVE_COMPLETION; T16; no CAD/ERC claim |
| R4A-17 TPS7A16 citation | IN60V versus EN40V corrected; active U306 input/enable use held supply, U600 uses SAFE_IN. | S03-12/S06-01; TI SBVS171F; T17 |
| Check N1/N2/N3/H1 | Skew term required, current R367 power/rating and current-limit prose corrected in round2; old uncommitted statements explicitly historical. | FIX2_RESOLUTIONS; historical archives; current VALIDATION |

## Three-item handback and exact remaining work

1. **Autonomous source trigger:** no unnamed discriminator remains, but an admitted fault can fail to provide the required signature. T01F3-N/F determines normal/fault separation, including pre-VIN_SEEN onset and internal low-side pulses. Failure requires another discriminator or an explicitly reviewed fault-scope change. The isolated detector can be captured with force paths absent; the present circuit cannot receive an unconditional integrated freeze.
2. **Rail loss/reset/ARM/persistent short:** a real diagnostic and state circuit replace the former labels. T15F3 checks early PG/recovery/minimum clear width, SAFE5 brownout with other rails present, and direct SER_DRV loss at real gates. Those are targeted unresolved cases, not a generic promise to test later. Failures require circuitry before integrated operation. Coupon capture with drain-energy paths absent is possible.
3. **Rated fixture:** separate equipment now has exact component/pin selections, drawing, calculations and rating references. Hot switching/return SOA and measured parasitics/abort remain OPEN. No fully qualified worst-case fixture rating is claimed. T12F3 closes these before use; this equipment's build/qualification cannot hold the board-hook capture decision hostage.

The earlier B02/M01…M06 requirements map respectively to R4A-08, R4A-04/07/15, R4A-03/15, R4A-06, R4A-15, R4A-09/15 and R4A-15 above. Source/L/C, raw/protected/harness and normal-path questions remain T01/T09/T10/T11; whole-input surge is T14B. No original blocker disappears by changing labels.

## Evidence, precedence and next gate

Authoritative current circuits are [FIX3_SOURCE_TRIGGER.md](FIX3_SOURCE_TRIGGER.md), [FIX3_INTERLOCK.md](FIX3_INTERLOCK.md) and [FIX3_FIXTURE.md](FIX3_FIXTURE.md). [FREEZE_MANIFEST.json](FREEZE_MANIFEST.json) generates the table/CSV; it is a delta register, not a reconciled native assembly. [TEST_PLAN.md](TEST_PLAN.md) incorporates the FIX3 acceptance register. [VALIDATION.json](VALIDATION.json) records numerical/connectivity checks, pinned inputs, source hashes and preserved archives. The one-page owner PDF is regenerated from the section above.

**NEXT:** resolve the two board limitations on isolated coupons, then review the integrated R2 capture decision. R2 schematic/pin review/ERC, R3 layout/DRC/visual, R4 fabrication review and R5 staged dummy-load bring-up remain sequential. Board capture, external fixture acceptance, electrical validation, fabrication and Pi integration are distinct decisions. The source module, actual instruments and hot application ratings remain external/pre-energization prerequisites.

**Git:** local commit attempts after each of items1/2/3 failed at `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-gate4a/index.lock` with `Operation not permitted`. The requested fallback leaves changes uncommitted. Supplied partial commits remain intact. No pull/push or lock/permission manipulation.

VERDICT: BLOCKED — autonomous source-fault coverage; interlock default-off/PG recovery and hard SER_DRV-loss behavior. External fixture qualification blocks energized testing, not isolated board-hook capture.
