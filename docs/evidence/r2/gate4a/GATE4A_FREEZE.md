# Gate4a-FIX — resumed test-board freeze review

**VERDICT: BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Resumed from both `0a81d2820449b678d5fef369774fbaf2eef0a9b3` and `2b99ac7bd60d352a4b418cd75e0fc8f66e345b4d`; valid partial fixes retained. This is analysis only. No KiCad edits, physical tests, fabrication approval or advancement to R3/R4/R5 occurred. The review contains12 BLOCKING,4 MAJOR and1 MINOR numbered findings; all17 are covered even though the brief calls them14 blockers.

## OWNER EXPLANATION — one page

**The test board remains BLOCKED for capture.** Architecture D, 9–26 V normal input, D101 SMCJ36CA, F101 Schurter3403.0285.23, the BSC034 series pair and the isolated48→24 V upstream route remain fixed. **J502 selection is complete for the candidate assembly:** Phoenix 1776508/1777989, TE 3-87456-6 with ten 87309-9 sockets, Belden 8521 trunks and 8502 fan-outs; hot contact, splice, mating and derating evidence remain T11/T16. No Pi is permitted before the fault, normal and interface gates pass.

Both partial commits were retained and checked. Their valid resistor, buffer, bootstrap, harness and detector corrections remain. This resume adds four corrections:

- **Comparator:** R3731k limits current from the charged reference capacitor into IN+ when DET5 disappears. C302 becomes4.7µF, with1…50µF effective required; the previous1µF nominal part could fall below the reference’s minimum. Conditional detector trip is5.219922…5.314622V; the upper20mV-overdrive point is5.356874V. Actual normal margin and rail decay still need T06.
- **Raw dump:** twelve33mΩ resistors form two six-part strings,99mΩ total. Vishay’s pulse curves apply to33mΩ, while the prior100mΩ elements required separate testing. The conditional99.865mJ pool gives at most8.607mJ per resistor in the tolerance/TCR model. Hot pulse/SOA and negative commutation remain unproved.
- **Auxiliary startup:** U327 `TPS259470LRPWR` now follows D304 with R374=100 Ω and C374=1 µF for controlled DRV_HOLD charging; U316 ENOUT gates U317 RUN. C350 is the identified 10 nF timer candidate. Startup current, pass-FET SOA and fast rail-loss ownership remain T07/T14/T15 evidence gates.
- **Measurement:** the10mA source-off endpoint now has a separate≤2mA additive-error target, and T13 separately bounds interchannel voltage/current skew in the integrated energy. Charge acceptance covers the complete discharge event; maintained-input shutdown leakage has its own sustained test.

The **10µs/100µC source contract still lacks an autonomous discriminator**. Revised output-OV latency exceeds10µs in the illustrative cases. A blind SW timeout also fails a dropout example before accounting for all delays. Reset/ARM/POR and fast rail-loss ownership remain incomplete. Those are missing circuits, so assigning test names cannot close them.

The rated fault fixture still lacks its independent limiter, abort/discharge and force connections. Source-module identity, instrument calibration and applicable hot component evidence remain open. The four-PCH protected bank and real harness require measurement against **fault peak<5.5V** and **normal5A minimum≥4.75V**, including uncertainty. The historical5.542140V adverse result remains evidence.

All17 review findings and original freeze gaps have decisions, equations, evidence and named closure criteria. Ten calculation tests pass; no hardware was tested. **The remaining construction and external-evidence gaps prevent FROZEN FOR TEST-BOARD CAPTURE.** Git rejected the pull and every local checkpoint; this resume’s changes are uncommitted.

## Review item → resolution → evidence

“Paper corrected” closes only the stated documentary/selection defect. “Bench required” is a specified candidate awaiting physical evidence. “Construction blocked” cannot be discharged by writing a test name. No row is a hardware PASS.

| Review item | Resolution and remaining disposition | Evidence / closure |
|---|---|---|
| R4A-01 source trigger | **Construction blocked:** retain TPS26630/4.02k/latch-off/SHDN sinks; no autonomous discriminator selected. OV-only and blind SW-timeout shortcuts fail the documented screens. | FIX_RESOLUTIONS R4A-01; CALCULATIONS `gate4a_fix.source`; T01/T01P |
| R4A-02 resistor identities | **Paper corrected:** R1030805/348k, R3400805/1M; current R3670603/100k. New lands require capture audit. | FREEZE_TABLE S01-06/S03-03/S03-13; Vishay28758; T02/T16 |
| R4A-03 buffer identity | **Paper corrected; bench required:** U319/U324 SN74AHCT1G125DBVR, preceding Schmitt conditioners, explicit bypass/pulldowns/pins. | S03-05; FIX_RESOLUTIONS pin table; T03/T15 |
| R4A-04 bootstrap load | **Selection corrected; bench required:** R3052MΩ; max screened bleed5.013 µA at10 V. Actual TS≈5 V pump equilibrium remains unqualified. | S03-07; CALCULATIONS bootstrap; T04/T07 |
| R4A-05 C301/C302 | **Paper corrected:** C301 BST–TS and separate C302 REF–GND, C3011µF25 V; C3024.7µF25 V with1…50µF effective required. | S03-17; pinned exported netlist; T05/T04 |
| R4A-06 detector | **Arithmetic/selection corrected; bench required:**9.88k/10k/1k/100k,68.1k shunt bias, separate positive/negative clamps, DET5-powered switch and R3731k reference-input protection. Conditional overdrive5.356874 V; partial-power/normal margin still OPEN. | S03-02/03; independent Thevenin check; T06 |
| R4A-07 aux | **Candidate construction selected; bench and rail-loss construction required:** U327 slow charger, U316 ENOUT/RUN interlock, 10 nF C350 timer and 249k/100k monitor tops are specified. Startup current, pass-FET SOA and fast loss of AUX3V3/DRV_HOLD remain open. | S03-11…15/18; AUX_BRANCH_FIX; FIX2_RESOLUTIONS F2-02; T07A/B/C/D |
| R4A-08 B02 timing | **Bench required with blocked prerequisites:** parallel physical endpoints and test-conditioned partial sums distinguished; complete guaranteed min/max remain OPEN/OPEN. | TIMING_AND_LOGIC; T08 plus T01/T04/T06/T07/T12/T13/T15 |
| R4A-09 energy/returns | **Bench required; hot-rating prerequisite blocked:** raw99mΩ dump from twelve33mΩ parts and STPS60H100CT returns selected as candidates; each pulse/negative waveform must fit rated construction. | S01-04/S03-09; RAW_NODE_ENERGY; T09A/B |
| R4A-10 bank/harness peak | **Bench required:** retain four PCH as test candidate, withdraw inherited C/ESR margin; keep adverse historical trajectory. | S03-10; CALCULATIONS protected_node; T10 |
| R4A-11 wire | **Selection/handoff corrected; assembly bench required:**8521 AWG16 trunks and8502 AWG20 fan-outs are tied to the selected Phoenix/TE J502 solution; current sharing, crimps, mates and hot derating remain T11/T16. | J502_SELECTION; FIX2_RESOLUTIONS F2-01; T11/T16 |
| R4A-12 fixture | **Construction blocked:** QF2/QF3 break-before-make isolation proposal prevents direct injection into connected native low-side; abort/source-limit/discharge/force connections and numerical ratings still missing. | TEST_HOOKS; FIX_RESOLUTIONS R4A-12; T12 |
| R4A-13 uncertainty | **Paper budget corrected; inventory/calibration blocked:**15 mV/25 ns targets; full-event UQ, corrected energy errors and a separate2mA endpoint-error target. | CALCULATIONS measurement; TEST_PLAN T13; no actual calibrations |
| R4A-14 aux surge | **Development test defined; external evidence/fixture blocked:** separate58.1 V bounded aux pulse; no main-buck exposure; real upstream surge/fuse/TVS coordination OPEN. | T14A/B; FIX_RESOLUTIONS R4A-14 |
| R4A-15 pins/thermal | **Partial paper correction; construction blocked:** named new-IC pins/bypass and component-local limits recorded; POR/fault/reset/freshARM/rail-loss ownership and persistent-short diagnosis unresolved. | S03-03/04/05/14/15; TIMING_AND_LOGIC; T15L/T15T |
| R4A-16 assembly | **Partly resolved; assembly blocked:** C350, generic passives and the J502 handoff are identified; new lands/approval sheets, complete fixture assembly and actual mate remain unresolved. | PASSIVE_COMPLETION; J502_SELECTION; FIX2_RESOLUTIONS F2-01/F2-02; T16 |
| R4A-17 TPS7A16 | **Paper corrected:** IN60 V, EN40 V recommended; both new inputs DRV_HOLD. Original EN/cap/resistor rejection remains. | SOURCES; AUX_BRANCH_FIX; T17 |

## Original freeze blockers retained

| Original gap | Current coverage and remaining action |
|---|---|
| Source isolation, independent C/L/work bounds | R4A-01/09/12/14; implement discriminator, source/fixture limits and characterize C/L before accepting100 µC/10 µs. |
| B02 and M01 usable supply/bootstrap/hold | R4A-04/07/08/15; startup, loaded VGS, rail-loss action and current endpoints require completed construction plus T04/T07/T08. |
| M02/M04/M06 PG/fault/reset/default SHDN | R4A-03/15; remove false PG-to-crowbar coupling, complete fault priority/POR/ARM and persistent-short lockout; T03/T15. |
| M03 powered-off detector | R4A-06; explicit current-limited ground-return clamp candidate, T06 all rail orders and normal peak margin. |
| M05 raw/protected hot pulse/negative energy | R4A-09/15;99mΩ raw vs33mΩ protected ballast kept distinct; documented hot limits and T09/T15T. |
| Protected bank, actual arrival, historical far-end peak | R4A-10/11; T10/T11 real-harness/dummy matrix; no inherited0.5mΩ or80 A protected-arrival guarantee. |
| Normal path/hot RDS/regulation/connector | R4A-04/11/16; selected J502 path screen is41.855546mΩ with4.796866V at a20mV trough, while hot contact, splice, regulation and100mV-trough evidence remain open. |
| Main58.1 V let-through, new pins/lands, rated assembly | R4A-12/14/16; main-source coordination and component review precede capture release. |

## Evidence, next work and Git handback

Current [freeze table](FREEZE_TABLE.md), [CSV](FREEZE_BOM.csv) and [manifest](FREEZE_MANIFEST.json) contain36 change rows (the35-row baseline plus passive-completion row). [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md) gives circuit decisions/equations; [CALCULATIONS.md](CALCULATIONS.md)/[JSON](CALCULATIONS.json) are reproducible. [TEST_PLAN.md](TEST_PLAN.md) owns named acceptance and dependency order. [VALIDATION.json](VALIDATION.json) records numerical/document checks only. The original baseline remains byte-preserved under [history/931e369](history/931e369/README.md); partial work remains in Git commits0a81d28 and2b99ac7. Failed paper screens have not been deleted.

The next engineering work is to finish the autonomous discriminator, reset/POR/ARM/rail-loss circuitry, controlled aux startup and complete rated fixture, obtain source/J502/instrument handoffs, then perform the defined coupon/rating reviews. These are substantive unfinished items. A test name does not make an absent circuit ready for capture. Native recapture/ERC, layout/DRC/visual, fabrication review and physical qualification remain sequential future gates.

`git pull --ff-only` was attempted but denied writing the worktree FETCH_HEAD. Every item checkpoint `git add` was denied creating the worktree index.lock, so no local commit could be made. Per the resume brief, all resumed changes remain uncommitted; no push was attempted. No Git permission bypass or index repair was attempted. The conductor can review the working diff and commit/publish it from an authorized environment.

VERDICT: BLOCKED — autonomous source trigger; aux startup/SOA/rail-loss construction; reset/POR/ARM/persistent-short lockout; rated fixture/abort/discharge; hot-pulse/measurement evidence and source/J502/instrument handoffs remain open.
