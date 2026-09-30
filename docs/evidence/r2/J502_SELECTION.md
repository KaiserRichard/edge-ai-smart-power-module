# V1A J502 / Pi harness selection

2026-09-30. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**STATUS: CONDITIONAL PASS for component proposals and arithmetic; BLOCKED for a qualified hot 5 A claim.** No KiCad changes or gate advancement. The two complete proposals below meet the calculated hot acceptance budget, subject to its explicitly unproved bounds. Neither is represented as a datasheet-guaranteed or tested Pi assembly.

## OWNER EXPLANATION — one-page briefing

The Pi end stays fixed: its 40-pin, 2.54 mm GPIO header supplies 5 V through physical pins **2 and 4**, with return through **6/9/14/20/25/30/34/39**. At 5 A, every extra milliohm in the complete outgoing-and-return path costs 5 mV. The required voltage at the loaded Pi header is **at least 4.75 V**.

The rejected Harwin contact allows 30 mΩ after conditioning, above the 20 mΩ allocation. Its small crimp also cannot accept AWG16. My proposed replacement is a **TE 3-87456-6 full 2×20 housing with ten gold 87309-9 sockets**, fed by **75 mm AWG16 trunks and separate AWG20 pigtails**. TE publishes 12 mΩ termination resistance and a 3 A contact rating; the contact accepts AWG20. Both 5 V pins carry about 2.5 A only when their branches share evenly. The actual hot Pi mating pair still requires qualification.

There are two complete assembly choices:

| Proposal | Module connector | Calculated Pi voltage, architecture E, hot / 5 A / 20 mV trough | Principal tradeoff |
|---|---|---:|---|
| **A — recommended first** | Keep Phoenix **1776508 + 1777989** | **4.785 V**, 34.9 mV reserve | Preserves the board interface; must establish ≤3.12 mΩ per complete hot pole. |
| **B — fallback** | Gold Molex Mini-Fit Sr. **42819-2213 + 42816-0212 + 42815-0042** | **4.776 V**, 26.1 mV reserve | Published low-resistance contact system and AWG16 crimp; larger connector, new footprint and assembly process required later. |

Both numbers include the path-budget proposal for a **≤6 mΩ hot module FET pair** and architecture E's **≤10 mΩ additional Pi-entry protection stage**. Those changes are not implemented here. With the inherited 13.6 mΩ module-FET screen, the respective E voltages become **4.747 V and 4.738 V: both fail**. Connector selection alone does not complete the E redesign. A 100 mV negative excursion also makes both E proposals fail.

**Recommendation:** advance A to supplier/mechanical review and dummy-load qualification, retaining B if the Phoenix assembly misses its resistance allocation. Keep the regulator setpoint and protection thresholds unchanged. Measure the complete hot/conditioned assembly, every active pin's current and temperature, and the actual Pi header's geometry/plating/rating before integration. An ordinary low-resistance catalogue entry does not establish a hot mixed-manufacturer mate. No Pi was powered and no hardware behavior was validated.

---

## 1. Inputs, scope and interpretation

**REQUIREMENT:** ≥4.75 V at the loaded Pi GPIO power/ground endpoint at 5 A; use the fixed pins above. Do not replace the Pi header, add alternative Pi power contacts, or route USB data. Retain the inherited strict fault ceiling below 5.5 V. This report selects candidates; it does not resolve the fault architecture.

**EVIDENCE:** independent `VERIFY_FOOTPRINTS.md`, dated 2026-09-30, at the requested external path; PATH_BUDGET at commit `ebe51b9e141588d118d74daf37e65a3bd2307c1f`, [pinned report](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/ebe51b9e141588d118d74daf37e65a3bd2307c1f/docs/evidence/r2/path_budget/PATH_BUDGET.md). Repository baseline `51d1c2ff1f7eca4f20eef137c1595e4b9e052a75`. Exact input paths/hashes are in [INPUT_PROVENANCE.json](j502_selection/INPUT_PROVENANCE.json). The fetched branch was read, not merged.

**OBSERVATION:** the previous selection fails its datasheet resistance criterion; it is not evidence that every physical Harwin sample has high resistance. The footprint-only work and earlier ERC evidence are retained as history.

**ASSUMPTION** means a proposed acceptance allocation or inherited screen, never a supplier guarantee. **CALCULATION** means arithmetic within those assumptions. **OPEN RISK** means an applicable bound is absent; qualified minimum voltages remain `null` in [CALCULATIONS.json](j502_selection/CALCULATIONS.json). Electrical release cannot be made to pass by renaming assumptions as worst-case evidence.

## 2. Exact parts and manufacturer limits

Source IDs resolve to manufacturer URLs, revisions, reviewed sections, retrieval limitations and attribution in [SOURCES.json](../../../third_party/j502_selection/SOURCES.json). These are real orderable-part identities, not a stock or purchasing commitment.

### Common Pi-end assembly — used in both solutions

| Item / quantity | Exact MPN | Evidence and fit |
|---|---|---|
| Full Pi socket housing / 1 | **TE 3-87456-6** | 40 positions, two rows, 2.54 mm pitch/row spacing; 50.93 mm catalogue length, 6.1 mm height. Drawing 87456 **S5, 2025-04-14**; source T1. Covers the complete header with one body. |
| Female socket / 10 | **TE 87309-9** | Gold 0.76 µm mating finish, phosphor bronze, high-pressure MOD V contact; 24–20 AWG, insulation diameter 1.75 mm, 0.64 mm square post; 3 A catalogue rating. Sources T2/T3. The loose-piece **1-87309-4** is a sourcing alternative, subject to its own tooling/drawing check. |
| Positive pigtails / 2 × 15 mm | **Belden 8502 002100** | Red, AWG20 stranded tinned copper; nominal OD 1.5 mm, below the stated 1.75 mm contact limit; verify actual lot/tolerance and crimp. |
| Return pigtails / 8 × 35 mm | **Belden 8502 010100** | Black, same AWG20 construction. Longer ground branches span the full header. |
| Positive / return trunks, each 75 mm | **Belden 8521 002100 / 8521 010100** | Red / black, AWG16 stranded tinned copper, nominal OD 2.5 mm. Goes into J502, never into the Pi crimp. |

**EVIDENCE — resistance reference planes matter:** TE 108-25020 Rev B, 2025-02-21, gives **12 mΩ maximum termination resistance for phosphor bronze**, with resistance rechecked in the conditioning sequences. Figure 3 measures across a mated post/contact/termination and a short wire span; it is broader than the sliding contact interface. Its separate AWG20 crimp table gives **2 mΩ initial / 3 mΩ final**, tested at 3 A. Adding those figures to 12 mΩ as independent losses would overlap measurement spans. The copy inspected is the **PRELIMINARY** Rev B attachment to manufacturer PCN-25-236488 hosted by DigiKey; obtain the released applicable specification before procurement release. The current T2 product record independently lists 12 mΩ and 3 A. [TE PCN/specification T3](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6616/PCN-25-236488.pdf).

**DECISION — proposed tighter combined target:** allocate **≤20 mΩ hot and conditioned per Pi mated-contact-plus-female-crimp block**. This contains, rather than adds, the female crimp. Measure from the free conductor immediately behind the crimp to the male pin immediately above its PCB attachment; the separate attachment allowance covers the remaining connection to the Pi board. Keep the complete wire length as its own conservative allowance. The original budget allocated 20 mΩ to mating alone plus 0.5 mΩ equivalent for female crimps; this proposal removes that separate 0.5 mΩ only because the new combined block must pass the tighter test. If measurements use different endpoints, reconcile them before summing.

The 12 mΩ TE figure qualifies its specified mating system at the stated conditions, **not** the unidentified Pi male header at 60°C. No thermal multiplier turns it into such a guarantee. The proposed 20 mΩ combined bound needs supplier applicability evidence and hot/conditioned measurements on the actual mate.

### Solution A — retain Phoenix J502, change the external harness

| Item / quantity | Exact MPN | Rating / resistance evidence |
|---|---|---|
| Existing board header / 1 | **Phoenix 1776508**, MSTB 2,5/2-GF-5,08 | 12 A nominal. Live record lists 1.0 mΩ in its durability test. |
| Cable plug / 1 | **Phoenix 1777989**, MSTB 2,5/2-STF-5,08 | 12 A nominal; integral screw clamps, no separately purchased crimp contacts. AWG24–12 accepts the AWG16 trunks. Record gives 1.3 mΩ and 1.4 mΩ after cycling. |
| Pi housing / contacts / wires | Common assembly above | TE 3-87456-6 + ten 87309-9; Belden 8521 trunks and 8502 branches, exact colour/order codes above. |

**OPEN RISK:** Phoenix's test readings do not establish non-overlapping series elements or a complete hot pole maximum. Retain the inherited **≤3.12 mΩ/pole including clamp** as an acceptance target only. Do not add 1.0, 1.3 and 1.4 mΩ as three series losses. [P1 header](https://www.phoenixcontact.com/en-sg/products/pcb-header-mstb-25-2-gf-508-1776508), [P2 plug](https://www.phoenixcontact.com/en-nl/products/pcb-connector-mstb-25-2-stf-508-1777989).

**Assembly:** use the permitted bare-stranded termination or a separately qualified ferrule process; no assumed ferrule MPN is hidden in this BOM. Strip 7 mm and apply the specified conductor torque 0.5–0.6 N·m; flange retention torque is a separate 0.3 N·m operation. Support the cable, retain both flanges and do not mate under load. The candidate needs no J502 footprint substitution. No native file was edited.

### Solution B — separate high-current board connector

| Item / quantity | Exact MPN | Rating / fit evidence |
|---|---|---|
| Board header / 1 | **Molex 42819-2213** (`0428192213`) | Mini-Fit Sr., 2 circuits, one row, vertical, 10 mm pitch; 0.76 µm gold mating finish; 1.57 mm recommended PCB, 3.50 mm tails. |
| Cable housing / 1 | **Molex 42816-0212** (`0428160212`) | Two-circuit polarized/latching receptacle, with break-off terminal-position-assurance feature described in drawing SD-42816-XXX2 Rev F1. |
| Female crimp / 2 | **Molex 42815-0042** (`0428150042`) | Gold, AWG14–16, maximum insulation OD 3.33 mm; accepts nominal 2.5 mm Belden 8521. Drawing SD-42815-020 Rev C, 2018-05-04. |
| Pi housing / contacts / wires | Common assembly above | Identical TE Pi socket, AWG16 trunks and AWG20 fan-out. Only J502's complete interface changes. |

**EVIDENCE:** PS-42815-001, part 001, **Rev E2, 2026-01-06**, gives the two-circuit wire-to-board assembly **13 A with AWG16** at the stated room-temperature/30°C-rise test. The 50 A headline uses larger wire and is not the AWG16 rating. Gold contact resistance is **1.0 mΩ maximum initially and at rated-current measurement**; specified durability/environmental tests use **Δ1.0 mΩ** criteria, not a new absolute 1 mΩ guarantee. Crimp resistance is separately **1.0 mΩ maximum**. Gold durability is 100 cycles. Hot derating and transfer to this assembly remain OPEN. [M1 specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/428/42815/PS-42815-001-001.pdf).

**ASSUMPTION:** qualify **≤4.0 mΩ per complete hot J502 pole**, including header/contact/crimp but excluding its separately budgeted PCB solder joint. A conservative feasibility screen is `(1 initial + 1 conditioning change + 1 crimp) × 1.3 = 3.9 mΩ`, leaving 0.1 mΩ allocation reserve. The factor is inherited engineering screening, not a manufacturer hot guarantee; conditioning sequences and test reference planes must be reconciled. Any included overlap stays reserve, never claimed as an additional measured resistor.

**Assembly:** crimp one AWG16 trunk into each 42815-0042; engage contact retention and the housing's TPA as directed. Use matched gold header and socket variants. Assign the reviewed connector cavities to LOAD_5V1 and GND on a future harness drawing and continuity-test them. Its pitch, header holes, retention features, body and wire-bend envelope require a **new engineering-reviewed footprint/layout later**; it is not a Phoenix drop-in. Its much larger power-contact margin does not increase the Pi pin rating. Stock, tooling, exact current PCB thickness and final fit remain OPEN. No such board change is authorized or performed by this report.

### Wire ratings and the fan-out process

| Wire | Manufacturer nominal DCR | Catalogue current condition | Temperature / stationary bend radius |
|---|---:|---|---|
| Belden 8521 AWG16 | 4.0 Ω/1000 ft | 22 A, one conductor in free air at 30°C | 80°C insulation; 25 mm radius |
| Belden 8502 AWG20 | 9.8 Ω/1000 ft | 14 A, same free-air condition | 105°C insulation; 15 mm radius |

These are manufacturer catalogue values, **not harness bundle ampacity or guaranteed maximum DCR**. See [W1](https://www.belden.com/products/cable/electronic-wire-cable/lead-wire-hook-up-wire/8521), [W2](https://www.belden.com/products/cable/electronic-wire-cable/lead-wire-hook-up-wire/8502). Lengths in this report are maximum conductor lengths including termination take-up, not connector spacing. Keep the 15 mm positive branches straight; they cannot contain an arbitrary tight bend. Fit the ground star and strain relief physically before freezing lengths.

**Proposed process:** separately insulated, qualified ultrasonic welded fan-outs: one AWG16 to two AWG20 for SEND, one AWG16 to eight AWG20 for RETURN. These are process joints, not purchased contact MPNs. The return side contains about 4.14 mm² of branch copper versus about 1.31 mm² in its trunk; it needs a suitable splice tooling/process, not an improvised eight-wire crimp. Qualify total splice resistance **≤0.5 mΩ per polarity** including every sub-joint. If the harness shop uses several splices or a bus, all of them share that allocation. Splice recipe, insulation sleeve, mechanical carrier and process qualification remain **OPEN**; this is a component-selection BOM, not a released assembly instruction. Do not force AWG16 into a Pi socket or put multiple wires into a terminal approved only for one.

## 3. Recomputed complete hot loop

**Inherited ASSUMPTIONS:** source minimum **5.0261432547 V** from the pinned hot divider/regulator screen; wire and contacts 60°C, module copper/divider 85°C, FET junction 150°C, shunt 100°C. Proposed negative ripple trough 20 mV; 100 mV is a separate total-excursion sensitivity, not an additional subtraction. Actual regulator/load-regulation bounds, feedback bias maximum, enclosure temperature and ripple/transient requirements remain OPEN.

`R_wire = (nominal Ω/1000 ft ÷ 304.8) × length_m × 1.10 × [1 + 0.00393 × (60−20)]`

The +10% DCR screen and 20°C reference are inherited assumptions; vendor maximum DCR/reference-temperature confirmation remains OPEN. `V_Pi = V_source_min − 5 × R_loop − excursion`. Both SEND and RETURN count. No added resistance inside the Pi beyond the defined GPIO endpoint is silently assigned zero.

| Proposed hot element | A SEND mΩ | A RETURN mΩ | B change |
|---|---:|---:|---|
| Unsensed buck copper | 0.500000 | 0.500000 | Same |
| Module FET pair | 6.000000 | 0 | Same; proposed replacement/requalification, not installed |
| 2 mΩ shunt, +1%, +25 ppm/K at 100°C | 2.023788 | 0 | Same |
| Module traces/vias | 1.000000 | 1.000000 | Same |
| J502 complete pole including termination | 3.120000 | 3.120000 | **4.000000 per leg** |
| AWG16, 75 mm each trunk | 1.252874 | 1.252874 | Same |
| AWG20, 15 mm/2; 35 mm/8 | 0.306954 | 0.179057 | Same |
| Pi mating + female crimp, ≤20 mΩ each | 10.000000 | 2.500000 | Same |
| Pi male attachment, ≤0.48 mΩ each | 0.240000 | 0.060000 | Same |
| All fan-out splices | 0.500000 | 0.500000 | Same |
| Module connector solder joints | 0.100000 | 0.100000 | Same |
| **D loop sum** | **34.255546 total** | | **36.015546 total** |
| E additional complete stage | **+10.000000 total** | | **+10.000000 total** |

All non-wire/shunt maxima in that table are acceptance allocations. D locates the final stage at the module. E retains this path and adds its entire Pi-entry stage, including its copper/terminations, within 10 mΩ. No additional plug, copper bus or filter is free. Retain the 2 mΩ shunt and Kelvin routing; proposed FET drive/timing/SOA qualification belongs to the existing path/protection work, not this connector change.

| Proposal / architecture | Loop mΩ | 5 A drop mV | Static Pi V | Pi V with 20 mV trough | Margin above 4.75 V | Pi V with 100 mV total excursion |
|---|---:|---:|---:|---:|---:|---:|
| A / D | 34.255546 | 171.278 | 4.854866 | **4.834866** | +84.866 mV | 4.754866 |
| A / E | 44.255546 | 221.278 | 4.804866 | **4.784866** | +34.866 mV | **4.704866 — fails** |
| B / D | 36.015546 | 180.078 | 4.846066 | **4.826066** | +76.066 mV | **4.746066 — fails** |
| B / E | 46.015546 | 230.078 | 4.796066 | **4.776066** | +26.066 mV | **4.696066 — fails** |

**CALCULATION:** the 20 mV case permits **51.228651 mΩ** total; the 100 mV case permits **35.228651 mΩ**. Proposed A improves the previous recommended 35.072941 mΩ D screen by **0.817395 mΩ**: about 0.317395 from AWG20 replacing AWG22 and 0.500000 from the explicitly tighter combined Pi termination acceptance. This is not a measured improvement. B adds 1.76 mΩ versus A because its complete-pole allocation is more conservative; a higher ampere rating alone does not imply a smaller allocated voltage drop.

**Critical counterexample:** keeping the old 13.6 mΩ hot FET-pair screen adds 7.6 mΩ / 38 mV. A/E becomes **4.746866 V**, B/E **4.738066 V** with the 20 mV trough. Both fail. Keeping the old FETs at a weaker real gate drive can be worse. Do not claim these are connector-only fixes for E.

**CALCULATION — heat/sensitivity:** at equal sharing each positive 20 mΩ combined Pi block dissipates 0.125 W; each ground block 7.81 mW. A's J502 is 78 mW per pole; B's is 100 mW per pole. Entire E path losses are 1.106 W / 1.150 W, distributed among components. Another 10 mm on both trunks costs 1.670 mV; another 10 mm on every pigtail costs 1.279 mV; +1 mΩ at each Pi block costs 3.125 mV; +1 mΩ at each J502 pole costs 10 mV. None of these watts establishes an acceptable temperature rise.

## 4. Pin map, current sharing and mechanical acceptance

The following are **Pi physical coordinates**, viewed from the Pi component side: row A has odd pins, row B even pins, stations 1–20 run from the pin-1 end. They are not an assertion that TE's moulded cavity numbering equals Pi numbering; the wire-entry view is mirrored. Transfer these coordinates to a verified mating-face assembly drawing.

| Pi physical pin | Coordinate | Connect to | Equal-share current at 5 A |
|---:|---|---|---:|
| 2 | B1 | J502 LOAD_5V1, positive branch 1 | 2.500 A |
| 4 | B2 | J502 LOAD_5V1, positive branch 2 | 2.500 A |
| 6 | B3 | GND branch 1 | 0.625 A |
| 9 | A5 | GND branch 2 | 0.625 A |
| 14 | B7 | GND branch 3 | 0.625 A |
| 20 | B10 | GND branch 4 | 0.625 A |
| 25 | A13 | GND branch 5 | 0.625 A |
| 30 | B15 | GND branch 6 | 0.625 A |
| 34 | B17 | GND branch 7 | 0.625 A |
| 39 | A20 | GND branch 8 | 0.625 A |

Leave all other cavities electrically unconnected in this **power-only** harness, including the 3.3 V pins. A full housing occupies the GPIO interface: if the existing I2C/reference harness needs those pins, incorporate its separately reviewed contacts/map in the same housing or reopen the interface. Do not add a stacking adapter without counting its contacts and reviewing its ratings. This selection does not implement telemetry wiring.

**OPEN RISK — current derating:** 3 A is a catalogue rating, not approval for two adjacent Pi positive contacts in a hot housing. T3 Figure 4 gives a base current around 4.4 A below roughly 75°C ambient and AWG20 multipliers 0.587 at 50% loading / 0.456 at 100% loading. These illustrate about **2.58 A / 2.01 A** respectively. The 100%-loaded screen cannot deliver 5 A through two pins. Ten populated cavities out of forty does not establish the local thermal loading pattern: pins 2/4 are adjacent. Obtain the applicable loading/ambient rating and the actual Pi male-pin limit; use the lower bound. The preliminary curve is guidance, not a release rating for this mate.

For two positive branches, `I_lowR = 5 R_high/(R_low+R_high)`. A 3 A limit allows resistance ratio ≤1.5, but a 2.58 A hot limit would allow only about 1.066. **Proposed process target:** match complete positive branches to ratio ≤1.05, giving a calculated maximum 2.561 A; still obtain a hot rating above that measured current. Include Pi plane spreading in the current test. No vendor maximum resistance alone establishes this ratio. One open positive contact forces 5 A through the survivor: single-contact loss is **not qualified**, and the main 5 A current limit does not protect a 3 A survivor. Establish fault detection/derating or reject the 5 A operating claim.

**Assembly acceptance:** verify the real Pi revision, pin cross-section, mating length, plating compatibility, contact wipe and lack of bottoming; 2.54 mm pitch alone is insufficient. Use TE application specification **114-25003 Rev N** and part-specific crimp tooling/height; inspect conductor and insulation crimps and pull-test process samples. Provide an indexed insulating carrier fixed to Pi mounting features, preventing reversal, row/column offset and lift under cable load. A bare Pi header supplies no keyed shroud. Check cooler/HAT clearance and cable bend radii. Never probe sockets with oversized meter tips. Measure insulation diameter on the selected wire lot; nominal diameter is not a tolerance guarantee.

## 5. Alternatives screened out of the two proposals

- **Harwin M20-1180042:** retain the independent FAIL against its 20 mΩ target; 30 mΩ conditioned is not fixed by fitting thicker trunk wire. Historical sources are registered under `third_party/footprints_complete/`.
- **Amphenol Mini-PV 65043-017LF + 48236-000LF, Belden 8503 AWG22:** real full 2×20 housing and gold crimp alternative, 3 A family rating. The 2022 presentation states 15 mΩ, while BUS-12-067 Rev K specifies **Δ2 mΩ** after environment; a newer brochure's <2 mΩ statement must not be mistaken for an absolute hot limit. Useful second-source research, but absolute reference planes, crimp maximum, hot current and Pi mate applicability remain unresolved. Do not claim this already closes the same criterion that rejected Harwin.
- **Two-pole JST VH:** eVH states 10 mΩ initial / 20 mΩ after tests; the existing shrouded/AWG18 combination is rated 7 A. At 20 mΩ each pole, the board connector alone loses 200 mV at 5 A, replacing A's 31.2 mV allocation with a much larger loss even before heating. A/E would be about **4.616 V** with that substitution. Parallel VH poles would be a different harness/copper design, not a two-pole substitution.
- **Molex SL 70058 / generic IDC ribbon:** no IDC assembly is credited with 2.5 A per Pi positive merely because it has forty contacts. The inspected SL specification/test summary does not supply a ≤20 mΩ hot Pi guarantee; one test summary permits 30 mΩ initial and Δ10 mΩ. No such alternative is counted as a passing proposal.

## DECISIONS FOR THE OWNER

| Decision | Recommendation and consequence |
|---|---|
| Which complete solution to qualify first? | **A: TE 3-87456-6 + ten 87309-9, AWG20 pigtails, existing Phoenix J502 and AWG16 trunk.** Lowest board impact; demand the complete hot Phoenix ≤3.12 mΩ measurement. |
| What if the Phoenix target cannot be substantiated? | **B: matched-gold Mini-Fit Sr. 42819-2213 / 42816-0212 / 42815-0042**, qualify ≤4 mΩ/pole. It has an explicit 13 A AWG16 test rating, costs 8.8 mV more under this conservative allocation, and requires later CAD/mechanical review. |
| Is the rejected Harwin selection closed? | **Superseded as the recommended candidate, not electrically closed.** Obtain applicable TE released specification and Pi male-header evidence, then qualify the combined ≤20 mΩ hot/conditioned block and actual per-pin current. |
| Can either solution alone approve architecture E at 5 A? | **No.** E also needs the pinned ≤6 mΩ module pair and complete added stage ≤10 mΩ, with driver/fault/source review. Old module-FET screen fails with both connectors. |
| Can voltage be raised to avoid this work? | **Keep the inherited setpoint and trip window.** No setpoint/OVP change is credited. If the required negative excursion is 100 mV, reopen both E budgets. |
| When can the Pi be connected? | Only after the existing R2/R3/R4 gates and dummy-load-first R5 sequence below pass. No fabrication or integration approval is implied. |

## 6. Qualification handoff and completion evidence

**NEXT EVIDENCE:** agree actual ambient/contact temperatures, duty/life, conditioning cycles and measurement uncertainty; resolve supplier mixed-mate suitability and loaded-pin derating; build an indexed coupon/harness; prove hot source/FET/E-stage bounds. Four-wire measurements must cover both complete J502 poles, each of the ten Pi terminations, all splices, and the full loop with non-overlapping endpoints. Use an uncertainty guard band below each resistance/voltage limit, not a reading exactly at the limit. Check unequal-current and intermittent/open-contact behavior. Preserve the source-independent fault containment review; lower path resistance can increase ringing and does not prove fault safety.

**REQUIRED bring-up order:** visual inspection → continuity/short checks → current-limited bench supply → no-load startup → output-rail verification → low-current dummy/electronic load → increasing load steps → thermal measurements → ripple measurements → transient/load tests → protection/fault tests → telemetry validation → SBC integration only after prior gates pass. Use a representative header/coupon and electronic load for initial harness testing; the expensive SBC is not the first load. No physical tests were performed here.

**Verification:** run `python3 docs/evidence/r2/j502_selection/calculate.py --check`. The calculation independently compares the explicit parallel branch network to the table, checks all ten power positions and records both passing 20 mV and failing 100 mV E cases. See [VALIDATION.md](j502_selection/VALIDATION.md) for scope/link/provenance checks. No ERC/DRC was rerun because neither schematic nor PCB changed; past rule-check passes do not qualify these assemblies.

**Gate disposition:** WHAT WAS DONE — two complete connector/wire proposals, manufacturer-limit audit, recomputed D/E loops, owner recommendation and assembly/qualification notes. EVIDENCE — pinned inputs, source register, reproducible calculations. DECISION — qualify A first; keep B as the concrete board-side fallback. OPEN RISKS — actual hot mating/current/assembly/source/protection bounds. NEXT GATE — finish R2 engineering review; R3 and fabrication remain blocked. Publication handoff is a local commit only; the conductor owns push and draft PR creation.
