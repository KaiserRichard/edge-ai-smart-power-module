# Gate4a-FIX2 — resumed test-board freeze review

**VERDICT: BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Continued 7098411, 81aac81 and 74d5b10; earlier work and failed screens are retained. Analysis only: no KiCad edits, physical tests or gate advancement. The independent check has 12 original BLOCKING findings, four CLOSED and eight PARTLY/OPEN; this continuation does not claim new original-finding closure.

## OWNER EXPLANATION — one page

**Capture remains blocked by three unfinished constructions:** the autonomous source trigger, fast rail-loss/reset/ARM logic, and the complete rated fault fixture. Naming future tests does not supply those circuits.

Architecture D, 9–26 V normal input, SMCJ36CA, Schurter 3403.0285.23, the BSC034 pair and an isolated upstream 48→24 V module remain fixed. J502 solution A is selected: Phoenix header/plug, TE sockets/housing and Belden trunks/fan-outs. Hot assembly and actual Pi mating remain unqualified. No Pi or fabrication release is given.

This continuation preserves the partial work and makes these concrete changes:

- Reconciles CSV/Markdown with the intended U316 ENOUT→U317 RUN circuit and restores the omitted connector provenance. The recovered baseline failed its register test; the corrected package passes.
- Completes U317 compensation connections and changes R345 from 464 kΩ to 383 kΩ. With the declared leakage allocation, the upper startup screen falls from 8.531 V to 7.262 V. U327 controlled charging and the 10 nF stopper timer remain test candidates. Startup, loop response, hot SOA and held-rail behavior still need T07A–E.
- Corrects the executable energy-uncertainty calculation. Relative voltage/current skew is separate from record-endpoint timing; total uncertainty stays OPEN until that term is supplied. A regression reproduces the reviewer's counterexample.
- Extends the dump review to the connected output banks: 174.086 mJ under the effective 2.2 mF dummy allocation, or 180.741 mJ at +20% dummy capacitance. The earlier 99.865 mJ raw subtotal cannot qualify either dump against every coupled transfer.
- Specifies isolated bootstrap and detector measurements, explicit U301 pins, and numerical pass criteria. These component measurements can proceed through separately reviewed coupon gates without an energized high-current path. They do not prove the missing system interlock.

The full fault test still needs a source limiter, independent abort/discharge and rated force connections. The upstream source study selects no compliant module, the optional Sheet 03 qualification file is absent, and actual instruments/calibrations remain unknown. Four-PCH/harness peak and normal delivery remain T10/T11: **fault peak+U <5.5 V; normal 5 A minimum−U ≥4.75 V**. Failed historical trajectories remain evidence.

**Fourteen numerical tests pass; no hardware was tested.** Full original-finding closure stays 4/12. The owner should review F2-03…08 and the remaining construction list before authorizing further capture. Local staging/commit attempts were denied at index.lock; the brief's fallback leaves the changes uncommitted for the conductor. No push was attempted.

## Review item → resolution → evidence

“Paper corrected” closes only the stated documentary/selection defect. “Bench required” is a specified candidate awaiting physical evidence. “Construction blocked” cannot be discharged by writing a test name. No row is a hardware PASS.

| Review item | Resolution and remaining disposition | Evidence / closure |
|---|---|---|
| R4A-01 source trigger | **Construction blocked:** retain TPS26630/4.02k/latch-off/SHDN sinks; no autonomous discriminator selected. OV-only and blind SW-timeout shortcuts fail the documented screens. | FIX_RESOLUTIONS R4A-01; CALCULATIONS `gate4a_fix.source`; T01/T01P |
| R4A-02 resistor identities | **Paper corrected:** R1030805/348k, R3400805/1M; current R3670603/100k. New lands require capture audit. | FREEZE_TABLE S01-06/S03-03/S03-13; Vishay28758; T02/T16 |
| R4A-03 buffer identity | **Paper corrected; bench required:** U319/U324 SN74AHCT1G125DBVR, preceding Schmitt conditioners, explicit bypass/pulldowns/pins. | S03-05; FIX_RESOLUTIONS pin table; T03/T15 |
| R4A-04 bootstrap load | **Selection corrected; bench required:** R3052MΩ; max screened bleed5.013 µA at10 V. Explicit U301 pins and T04L load-line coupon added; actual TS≈5 V pump equilibrium remains unqualified. | S03-01/07; F2-07; T04L/T04/T07 |
| R4A-05 C301/C302 | **Paper corrected:** C301 BST–TS and separate C302 REF–GND, C3011µF25 V; C3024.7µF25 V with1…50µF effective required. | S03-17; pinned exported netlist; T05/T04 |
| R4A-06 detector | **Arithmetic/selection corrected; bench required:**9.88k/10k/1k/100k,68.1k shunt bias, separate positive/negative clamps, DET5-powered switch and R3731k reference-input protection. Conditional overdrive5.356874 V; partial-power/normal margin still OPEN. | S03-02/03; independent Thevenin check; T06 |
| R4A-07 aux | **Candidate construction selected; bench and rail-loss construction required:** U327 slow charger, U316 ENOUT/RUN interlock, 10 nF C350 timer, compensation branches, 383k RUN top and 249k/100k monitor tops are specified. Startup current, pass-FET SOA and fast loss of AUX3V3/DRV_HOLD remain open. | S03-11…15/18; AUX_BRANCH_FIX; FIX2_RESOLUTIONS F2-02/F2-05; T07A/B/C/D/E |
| R4A-08 B02 timing | **Bench required with blocked prerequisites:** parallel physical endpoints and test-conditioned partial sums distinguished; complete guaranteed min/max remain OPEN/OPEN. | TIMING_AND_LOGIC; T08 plus T01/T04/T06/T07/T12/T13/T15 |
| R4A-09 energy/returns | **Bench required; hot-rating prerequisite blocked:** raw99mΩ dump from twelve33mΩ parts and STPS60H100CT returns selected as candidates; coupled pool174.086483mJ at effective dummy2.2mF gives15.003120/44.404903mJ separate raw/protected part screens; hot ratings remain open. | S01-04/S03-09; RAW_NODE_ENERGY; F2-06; T09A/B/C |
| R4A-10 bank/harness peak | **Bench required:** retain four PCH as test candidate, withdraw inherited C/ESR margin; keep adverse historical trajectory. | S03-10; CALCULATIONS protected_node; T10 |
| R4A-11 wire | **Selection/handoff corrected; assembly bench required:**8521 AWG16 trunks and8502 AWG20 fan-outs are tied to the selected Phoenix/TE J502 solution; current sharing, crimps, mates and hot derating remain T11/T16. | J502_SELECTION; FIX2_RESOLUTIONS F2-01; T11/T16 |
| R4A-12 fixture | **Construction blocked:** QF2/QF3 break-before-make isolation proposal prevents direct injection into connected native low-side; abort/source-limit/discharge/force connections and numerical ratings still missing. | TEST_HOOKS; FIX_RESOLUTIONS R4A-12; T12 |
| R4A-13 uncertainty | **Paper budget corrected; inventory/calibration blocked:**15 mV/25 ns targets; full-event UQ, corrected energy errors and a separate2mA endpoint-error target. | F2-04; CALCULATIONS full UE null without skew; TEST_PLAN T13; no actual calibrations |
| R4A-14 aux surge | **Development test defined; external evidence/fixture blocked:** separate58.1 V bounded aux pulse; no main-buck exposure; real upstream surge/fuse/TVS coordination OPEN. | T14A/B; FIX_RESOLUTIONS R4A-14 |
| R4A-15 pins/thermal | **Partial paper correction; construction blocked:** named new-IC pins/bypass and component-local limits recorded; POR/fault/reset/freshARM/rail-loss ownership and persistent-short diagnosis unresolved. | S03-03/04/05/14/15; TIMING_AND_LOGIC; T15L/T15T |
| R4A-16 assembly | **Partly resolved; assembly blocked:** C350, generic passives and the J502 handoff are identified; new lands/approval sheets, complete fixture assembly and actual mate remain unresolved. | PASSIVE_COMPLETION; J502_SELECTION; FIX2_RESOLUTIONS F2-01/F2-02/F2-03/F2-05; T16 |
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

The [manifest](FREEZE_MANIFEST.json) is the authoritative **37-row proposed-change register**; [CSV](FREEZE_BOM.csv) and [table](FREEZE_TABLE.md) are reproducibly rendered by `render_freeze_register.py`. This is not a fully reconciled captured assembly. Current [round-2 decisions](FIX2_RESOLUTIONS.md), [calculations](CALCULATIONS.md), [test plan](TEST_PLAN.md) and [validation](VALIDATION.json) carry the current state. The 931e369 archive is unchanged; the prior validation is preserved under `history/47c7c07/VALIDATION.json`. Earlier failed Git statements describe those sessions; 47c7c07/7098411/81aac81/74d5b10 are already committed by the conductor.

**Next:** finish the source discriminator, fast rail-loss/reset/ARM construction and rated fixture. Obtain applicable source/component/instrument evidence; execute the named isolated and integrated tests through the sequential R2 capture/ERC, R3 layout/DRC/visual, R4 fabrication review and R5 bring-up gates. Measurement-only limits do not independently prohibit isolated test hooks, but no integrated capture freeze is issued while essential circuits are absent.

This session's local `git add`/`git commit` attempts were denied creating the worktree index.lock. No lock removal, permission bypass, pull or push was attempted. The worktree diff and provenance are ready for the conductor to review and commit under the explicit fallback.

VERDICT: BLOCKED — autonomous source trigger; fast rail-loss/reset/ARM/persistent-short lockout; complete rated fixture/abort/discharge. Source/component/instrument evidence and named measurements remain open.
