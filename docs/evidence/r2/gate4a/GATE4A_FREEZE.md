# Gate4a-FIX — resumed test-board freeze review

**VERDICT: BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Resumed from `0a81d2820449b678d5fef369774fbaf2eef0a9b3`; valid partial fixes retained. This is analysis only. No KiCad edits, physical tests, fabrication approval or advancement to R3/R4/R5 occurred. The review contains12 BLOCKING,4 MAJOR and1 MINOR numbered findings; all17 are covered even though the brief calls them14 blockers.

## OWNER EXPLANATION — one page

The owner’s **architecture D test board** remains: input protection and buck, module-side opposed BSC034 pair, protected crowbar and2 mΩ telemetry shunt. Normal input is **9–26 V**, D101 remains **SMCJ36CA**, F101 remains **Schurter3403.0285.23**, and an isolated48→24 V module is upstream. Its exact identity/source envelope is OPEN. **J502 is PENDING** in the separate connector job. No Pi is used before fault, normal and interface gates pass.

The review exposed real selection defects. The partial work repaired resistor packages, selected two documented AHCT1G125 buffers, separated bootstrap C301 from reference C302, reduced the bootstrap bleed load with2 MΩ, selected Belden8503 AWG22 fanouts, and corrected TPS7A16’s IN/EN limits. Those fixes are retained. The resumed detector uses9.88k/10k/1k/100k: its conditional20 mV-overdrive upper point is **5.356863 V**, replacing the partial proposal’s failing5.390878 V. Lowering the threshold reduces nuisance-trip headroom; normal peaks, partial-power leakage and loaded timing remain measurements, not PASS claims.

A high-side short feeds L201 and the raw bank. The main source must stop within **10 µs of physical fault onset**, with **whole-event positive charge≤100 µC**. Even the revised nominal output threshold takes15.94–29.56 µs in illustrative OV-only cases. An autonomous discriminator is still missing; fixture timing cannot replace it. Reset/ARM/POR arbitration is also incomplete. A discharged raw node cannot reveal whether the unpowered buck still has a short, so a repair/diagnostic lockout must accompany reset.

Under the declared source/C/L assumptions, new energy is15.217 mJ, raw-cap peak6.550 V and the ESR/ringing screen6.882 V. After the series pair opens, raw energy needs its own destination. The retained candidate raw dump now uses100 mΩ ballast and STPS60H100CT negative-return candidates; its pool is99.865 mJ and ideal decay to0.3 V is1.771 ms. Hot pulse/SOA, negative excursions and physical decay are unproved. The protected four-PCH bank cannot inherit the old0.5 mΩ ESR contract: the legacy sensitivity is5.713245 V and the historical5.542140 V far-end counterexample remains evidence.

The upstream auxiliary architecture supplies controls independently of the main eFuse. Its startup current-limit/timer, rail-loss action and actual loaded bootstrap still need closure. The conditional hold screen is4.609 ms; it is not a guaranteed disposal interval. A complete rated fault fixture also needs its independent energy limiter, abort/discharge circuitry and numerical limits.

The test plan now assigns every finding a named check, measured quantity and PASS criterion. At a **substantiated**15 mV voltage uncertainty, fault peak must be<5.485 V and normal5 A minimum≥4.765 V at the real harness endpoint. Current-tail uncertainty must cover the full record; a10 µs calculation cannot certify a2 ms event. No calibration or hardware results exist. **The remaining construction and external-evidence gaps prevent freezing this board for capture.**

## Review item → resolution → evidence

“Paper corrected” closes only the stated documentary/selection defect. “Bench required” is a specified candidate awaiting physical evidence. “Construction blocked” cannot be discharged by writing a test name. No row is a hardware PASS.

| Review item | Resolution and remaining disposition | Evidence / closure |
|---|---|---|
| R4A-01 source trigger | **Construction blocked:** retain TPS26630/4.02k/latch-off/SHDN sinks; no defensible autonomous discriminator selected. Revised OV-only latency still exceeds10 µs. | FIX_RESOLUTIONS R4A-01; CALCULATIONS `gate4a_fix.source`; T01 |
| R4A-02 resistor identities | **Paper corrected:** R1030805/348k, R3400805/1M; current R3670603/100k. New lands require capture audit. | FREEZE_TABLE S01-06/S03-03/S03-13; Vishay28758; T02/T16 |
| R4A-03 buffer identity | **Paper corrected; bench required:** U319/U324 SN74AHCT1G125DBVR, preceding Schmitt conditioners, explicit bypass/pulldowns/pins. | S03-05; FIX_RESOLUTIONS pin table; T03/T15 |
| R4A-04 bootstrap load | **Selection corrected; bench required:** R3052MΩ; max screened bleed5.013 µA at10 V. Actual TS≈5 V pump equilibrium remains unqualified. | S03-07; CALCULATIONS bootstrap; T04/T07 |
| R4A-05 C301/C302 | **Paper corrected:** C301 BST–TS and separate C302 REF–GND, each1µF25 V exact MPN. | S03-17; pinned exported netlist; T05/T04 |
| R4A-06 detector | **Arithmetic/selection corrected; bench required:**9.88k/10k/1k/100k,68.1k shunt bias, separate positive/negative clamps and DET5-powered switch. Conditional overdrive5.356863 V; partial-power/normal margin still OPEN. | S03-02/03; independent Thevenin check; T06 |
| R4A-07 aux | **Construction blocked:** revised249k/110k monitor tops and explicit supplies retained; controlled charge/timer/fast rail-loss construction and hot SOA missing. | S03-11…15; AUX_BRANCH_FIX; T07A/B |
| R4A-08 B02 timing | **Bench required with blocked prerequisites:** parallel physical endpoints and test-conditioned partial sums distinguished; complete guaranteed min/max remain OPEN/OPEN. | TIMING_AND_LOGIC; T08 plus T01/T04/T06/T07/T12/T13/T15 |
| R4A-09 energy/returns | **Bench required; hot-rating prerequisite blocked:** raw100mΩ dump and STPS60H100CT returns selected as candidates; each pulse/negative waveform must fit rated construction. | S01-04/S03-09; RAW_NODE_ENERGY; T09A/B |
| R4A-10 bank/harness peak | **Bench required:** retain four PCH as test candidate, withdraw inherited C/ESR margin; keep adverse historical trajectory. | S03-10; CALCULATIONS protected_node; T10 |
| R4A-11 wire | **Paper corrected; handoff/bench required:**8503 AWG22 fanouts,8521 trunks, current sharing/crimps/mates; J502 PENDING. | S04-04/05; T11; path expression excludes assumed J502 allocation |
| R4A-12 fixture | **Construction blocked:** QF2/QF3 break-before-make isolation proposal prevents direct injection into connected native low-side; abort/source-limit/discharge/force connections and numerical ratings still missing. | TEST_HOOKS; FIX_RESOLUTIONS R4A-12; T12 |
| R4A-13 uncertainty | **Paper budget corrected; inventory/calibration blocked:**15 mV/25 ns targets; full-tail UQ and all additive voltage/cross-product energy errors included. | CALCULATIONS measurement; TEST_PLAN T13; no actual calibrations |
| R4A-14 aux surge | **Development test defined; external evidence/fixture blocked:** separate58.1 V bounded aux pulse; no main-buck exposure; real upstream surge/fuse/TVS coordination OPEN. | T14A/B; FIX_RESOLUTIONS R4A-14 |
| R4A-15 pins/thermal | **Partial paper correction; construction blocked:** named new-IC pins/bypass and component-local limits recorded; POR/fault/reset/freshARM/rail-loss ownership and persistent-short diagnosis unresolved. | S03-03/04/05/14/15; TIMING_AND_LOGIC; T15L/T15T |
| R4A-16 assembly | **Selection work retained; assembly blocked:** identified C350 and41 remaining generic passives; timer value, new lands/approval sheets, added circuits and fixture/J502 handoffs unresolved. | PASSIVE_COMPLETION; FREEZE_MANIFEST; T16 |
| R4A-17 TPS7A16 | **Paper corrected:** IN60 V, EN40 V recommended; both new inputs DRV_HOLD. Original EN/cap/resistor rejection remains. | SOURCES; AUX_BRANCH_FIX; T17 |

## Original freeze blockers retained

| Original gap | Current coverage and remaining action |
|---|---|
| Source isolation, independent C/L/work bounds | R4A-01/09/12/14; implement discriminator, source/fixture limits and characterize C/L before accepting100 µC/10 µs. |
| B02 and M01 usable supply/bootstrap/hold | R4A-04/07/08/15; startup, loaded VGS, rail-loss action and current endpoints require completed construction plus T04/T07/T08. |
| M02/M04/M06 PG/fault/reset/default SHDN | R4A-03/15; remove false PG-to-crowbar coupling, complete fault priority/POR/ARM and persistent-short lockout; T03/T15. |
| M03 powered-off detector | R4A-06; explicit current-limited ground-return clamp candidate, T06 all rail orders and normal peak margin. |
| M05 raw/protected hot pulse/negative energy | R4A-09/15;100mΩ raw vs33mΩ protected ballast kept distinct; documented hot limits and T09/T15T. |
| Protected bank, actual arrival, historical far-end peak | R4A-10/11; T10/T11 real-harness/dummy matrix; no inherited0.5mΩ or80 A protected-arrival guarantee. |
| Normal path/hot RDS/regulation/connector | R4A-04/11/16; conditional42.673mΩ includes historical6.24mΩ J502 allocation; final choice PENDING.100mV trough screen remains4.712779 V, below4.75 V. |
| Main58.1 V let-through, new pins/lands, rated assembly | R4A-12/14/16; main-source coordination and component review precede capture release. |

## Evidence, next work and Git handback

Current [freeze table](FREEZE_TABLE.md), [CSV](FREEZE_BOM.csv) and [manifest](FREEZE_MANIFEST.json) contain36 change rows (the35-row baseline plus passive-completion row). [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md) gives circuit decisions/equations; [CALCULATIONS.md](CALCULATIONS.md)/[JSON](CALCULATIONS.json) are reproducible. [TEST_PLAN.md](TEST_PLAN.md) owns named acceptance and dependency order. [VALIDATION.json](VALIDATION.json) records numerical/document checks only. The original baseline remains byte-preserved under [history/931e369](history/931e369/README.md); partial work remains in Git commit0a81d28. Failed paper screens have not been deleted.

The next engineering work is to finish the autonomous discriminator, reset/POR/ARM/rail-loss circuitry, controlled aux startup and complete rated fixture, obtain source/J502/instrument handoffs, then perform the defined coupon/rating reviews. These are substantive unfinished items. A test name does not make an absent circuit ready for capture. Native recapture/ERC, layout/DRC/visual, fabrication review and physical qualification remain sequential future gates.

`git pull --ff-only` was attempted but denied writing the worktree FETCH_HEAD. The first item checkpoint `git add` was denied creating the worktree index.lock, so no local commit could be made. Per the resume brief, all resumed changes remain uncommitted; no push was attempted. No Git permission bypass or index repair was attempted. The conductor can review the working diff and commit/publish it from an authorized environment.

VERDICT: BLOCKED — autonomous source trigger; aux startup/SOA/rail-loss construction; reset/POR/ARM/persistent-short lockout; rated fixture/abort/discharge; hot-pulse/measurement evidence and source/J502/instrument handoffs remain open.
