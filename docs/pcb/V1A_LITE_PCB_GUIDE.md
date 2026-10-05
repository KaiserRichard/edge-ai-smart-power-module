# V1A-Lite: place and route the PCB by hand

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Use this with [Start here](README_HAND_ROUTE.md) and [Schematic editing](V1A_LITE_SCHEMATIC_EDITING.md). This is a practice lesson, not a release checklist that grants manufacturing permission.

**KNOWN** means a saved-board fact or a documented requirement. **CALCULATED** means arithmetic or a model, not a measurement. **OPEN** means a missing requirement, untested behavior or unfinished review. Labels apply to all values in their table or paragraph. Proposed drawing choices are stated as practice choices, not new electrical requirements.

## 1. Know which board you are reading

**KNOWN:** this guide uses commit `ee31d04`, PCB SHA256 `01e7046e4072d0dfcc3dd750141c8a14cbf554cbbac3dc0db5ca3a1d246d1066`. It is the FIX2 board. [R1](../evidence/v1a_lite/PCB_REVIEW_R1.md) reviewed an older two-layer board; [R2](../evidence/v1a_lite/PCB_REVIEW_R2.md) reviewed FIX1. Their findings remain useful, but their moved-part coordinates are historical.

**KNOWN:** outline corners are `(10,10)` and `(90,70)`: **80 × 60 mm**. Coordinates here are absolute **millimetres, top view, X right and Y down**, including bottom features. They are not placement-file coordinates or distances from the drill origin. A footprint anchor is its placement point; it is not always the body centre.

**KNOWN requirements:** normal input **18–26 V**, output **5 A target**, Pi terminals **≥4.75 V and <5.5 V** including the required fault envelope. **54.6–64 V is an upstream fault**, never a normal buck supply. **CALCULATED:** nominal raw output is **5.065041 V**. **OPEN:** peak-current allowance, source fault current, thermal environment and complete operating compliance.

Lite has no current shunt, INA228, I2C, eFuse or removable force links. J503 is now a dummy-load pad pair. Do not transplant the older V1A guide's circuit or copper budget. Do not route USB 3.x or D435i data here or assume a WBR battery architecture.

## 2. KiCad 9 beginner tools

A **net** is one electrical connection. A **track** is a narrow copper route. A **via** joins copper layers. A **zone** is a filled copper area. A **ratsnest** line shows a connection that still needs copper. A **courtyard** reserves assembly space around a part.

**KNOWN KiCad defaults:** hover the intended item before a hotkey. On Mac, use Command for Ctrl and Option for Alt; check **Help → List Hotkeys** if your keys differ.

| Job | Tool / action |
| --- | --- |
| Find a part | Find tool; search `U201`. Use schematic cross-probing if labels are hidden. |
| Read exact pad/net/location | Select a pad; read the information panel. `E` opens properties. |
| Move / rotate | `M` / `R`. Confirm which footprint or text is selected. |
| Start a track | Hover a pad, press `X`, click corners, finish on the destination pad; `Esc` leaves the tool. |
| Interactive router | Open router settings. **Shove** moves other movable tracks; **Walk Around** leaves them in place. Inspect any displaced critical routes. |
| Change layer while routing | `V` places a via; choose the destination layer. It is not a free current-capacity upgrade. |
| Select a layer | Click its name in the Appearance panel. Visibility and active layer are different settings. |
| Fill copper | Add Filled Zone, select its layer and net, draw its boundary; `B` refills all zones. |
| Measure | Inspect → Measure Tool. Use mm and absolute coordinates; Space resets only the local ruler. |
| Follow connectivity | Highlight Net tool on a pad/track. Confirm the displayed net name. |
| See the assembly | View → 3D Viewer, `Alt+3`. |
| Check geometry | Inspect → Design Rules Checker (DRC). |

[KiCad 9 PCB Editor manual](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html) explains these controls. The installed CLI checked for this guide is **KNOWN: 9.0.6**.

## 3. Work in this order

1. Open the project from this worktree. Read the schematic before moving parts. If it needs electrical edits, finish the schematic lesson and ERC first.
2. Save a practice checkpoint. Keep the outline, mounting holes and connector access as your mechanical frame.
3. Check the stack and project rules below. Do not turn off a rule to make routing easier.
4. Place the input force path; reserve space for its detector and gate network.
5. Place U201 and its two local input bypasses. Then place BOOT, VCC, FB parts, L201 and raw capacitors.
6. Place the SCR beside the raw bank. Then place its driver, detector, F301 and Pi-side capacitors. Place the input latch as a compact control group.
7. Route the local switching/bypass loops first, then crowbar/gate loops, broad force paths and returns, quiet sensing, and remaining control signals.
8. Refill; check every layer; add accessible probes, readable silk and mechanical envelopes. Run DRC and the path checks.
9. Save review evidence before moving to the next block. Recheck any earlier route moved by the interactive router.

For your first reroute, select and delete only the intended track segments, using the selection filter to protect footprints and zones. Keep the schematic nets. A ratsnest line should return. Draw the new route and refill. Do not delete every track/via or run a board builder to create a blank exercise: that also removes reviewed thermal and return structures.

## 4. Keep the actual four-layer stack

Open **Board Setup → Physical Stackup**.

**KNOWN saved stack:** nominal board thickness **1.6 mm**; FR4 dielectric gaps **0.2104 / 1.065 / 0.2104 mm**. Copper thicknesses below are the model inputs, not guaranteed finished minimums.

| Layer | Copper | Use in this board / rule |
| --- | ---: | --- |
| F.Cu | 35 µm | Components, input hot loops, compact SW, broad power routes and local GND. |
| In1.Cu — L2 | 15.2 µm | GND reference/shield. Keep it connected under U201 and the SCR/capacitor area; no signal tracks or live-net islands. |
| In2.Cu — L3 | 15.2 µm | Separate VIN_FUSED, VIN_PROTECTED and raw-output power/heat regions, plus GND fill. Its GND fragments are not a continuous reference plane. |
| B.Cu | 35 µm | GND return/heat spreading, separate live FET drain copper, control routes and bottom test pads. |

**KNOWN manufacturer comparison:** TI recommends **2/1/1/2 oz** in LM61460 §11.1.1. This board uses approximately **1/0.5/0.5/1 oz**, with the actual thicknesses above. Four layers alone do not satisfy that thermal recommendation. **OPEN:** finished copper/plating tolerances, cooling and temperature qualification. Do not change to two layers or thicker copper without recalculating resistance, thermal paths, clearances and fabrication assumptions.

## 5. Find the real blocks

**KNOWN current footprint anchors, mm:** use this map to find a group, then inspect individual pads.

| Block | References and where to start |
| --- | --- |
| Input force path | J501 `(16,32)`, F101 `(23,17)`, D101 `(25,39)`, Q101 `(30,24)`, Q102 `(44,20)`, C101 `(50,29)`, D106 `(48.25,35)` |
| Input detector/gate drive | U101 `(30.5,34)`, Q103 `(38.75,25.5)`, D102–D105, C102 `(34,39)`; R101/R102, R110–R125, R130–R135, R140–R146, R150–R153 |
| Fault latch | Q104 `(53,17)`, Q105 `(58,17)`, Q106 `(48,13)`, R160–R166; TP110–TP114 |
| Buck | U201 `(45,44)`, L201 `(57.5,44)`; C201–C207, C209–C218; R201–R207 |
| Crowbar force loop | SCR301 anchor `(69,33.4)`; C217 anchor `(64,26)`, C218 anchor `(81,26)`; raw ceramics C209–C214 along `x67.5, y41–56` |
| Output detector/driver | U301 `(60,55)`, Q301 `(74,50)`, R301–R308; R301 now `(63,57.6)`, R308 `(73,34.5)` |
| Pi branch | F301 `(74.5,43)`, C301 `(77,55)`, C302 `(83,55)`, J502 `(84,44)`, J503 `(73,61.5)` |

## 6. Input: fuse, TVS, then cutoff

1. Highlight `/VIN_RAW` at J501.1 `(16,32)`. Follow it through **F101** to `/VIN_FUSED`.
2. Find **D101**. It is a **shunt**: a branch from VIN_FUSED to GND, after F101 and before both FETs. It is not a series component. Give its surge current a short, broad return to J501.2 `(16,35.96)`, away from detector ground.
3. Follow Q101 drain pad 2 `(28.74,24)` → its source pad 3 `(35.04,21.72)` → Q102 source pad 3 `(38.96,22.28)` → Q102 drain pad 2 `(45.26,20)`. The two sources share `S_COMMON`.
4. Keep C101 and D106 on `/VIN_PROTECTED`, downstream of Q102. Keep D106's clamp loop local to the protected rail and return. Never move the protected TVS directly across the fault input.
5. Put each source/gate clamp D102/D103 near its FET terminals. Keep the Q102 gate pullup R140–R143 and sink path through R130–R135/Q103 compact. The resistor strings share voltage/power; do not collapse them into one small resistor.

**WHY:** Q101 handles reverse polarity; **Q102 must stop forward input**. Opening Q101 alone leaves a forward body-diode path. Their drain copper is also their heat spreader: Q101 is VIN_FUSED, Q102 is VIN_PROTECTED. Neither drain/tab is GND.

**KNOWN:** the current pair is **IRFR6215TRPBF, 150 V DPAK**, not the old IRF9540 used in C/C2. **OPEN:** 64 V cold-start, turn-off delay, hot safe operating area (SOA: allowed voltage/current/time stress), surge ringing and reverse/backfeed behavior. Read schematic-review findings 2–3 before changing this block.

## 7. Input spacing: do not confuse DRC with insulation approval

1. Inspect the live input area near F101/D101/Q101/Q102 and D101's high land `(25,35.6)`, including all new L3 copper.
2. List the largest voltage between each pair of nearby nets. Include gate/source relationships, reversed input and pulse faults, not just net names.
3. Use the approved environment and coating classification before choosing electrical clearance rules. **Clearance** is an air gap; **creepage** follows an insulating surface.

**KNOWN existing manufacturing rules:** default clearance **0.15 mm**, Power **0.20 mm**, copper-to-edge **0.50 mm**. `/VIN_FUSED` is presently assigned **Default**, although its power zones have their own clearances. Audit the assignment and each zone; the word “Power” is not automatically applied to every force net.

**KNOWN historical review classification, not fresh standards certification:** R1 and [FIX1 spacing note](../evidence/v1a_lite/fix1/SPACING_AND_ASSEMBLY.md) quote IPC-2221B November 2012: for the **51–100 V** row, **B2 0.64 mm**, **B4 0.13 mm**, **A6 0.50 mm**. B2 concerns uncoated external conductors; B4 has coating/environment conditions; A6 covers exposed assembly features. At the cited **103 V pulse** case, the review records **B4 0.40 mm / A6 0.80 mm** from a different row. Do not extrapolate the lower row or treat soldermask as automatic coating qualification.

**OPEN:** environment, contamination/condensation, altitude, coating, materials and complete voltage-pair envelopes. These numbers are a reading aid, not chosen release clearances. The TVS's quoted 103 V is a specified pulse condition, not a universal clamp maximum. Use the exact pulse envelope for the new check. If the B4 basis is unavailable, the applicable uncoated rule must be reviewed and encoded; do not guess a universal gap or waive spacing.

## 8. Place the two buck input hot loops

A **hot loop** carries rapidly changing current. Even a short conductor has **inductance**, which opposes current change and can create a voltage spike.

**KNOWN current pad centres, mm:**

| Local loop | VIN pad | PGND pad | Bypass pads: 1 positive, 2 GND |
| --- | --- | --- | --- |
| C203 at U201 lower side | U201.8 `(45.45,45.45)` | U201.9 `(46.48,45.05)` | C203.1 `(45.175,47.2)`; .2 `(46.725,47.2)` |
| C204 at U201 upper side | U201.12 `(45.45,42.55)` | U201.11 `(46.48,42.15)` | C204.1 `(45.875,40.8)`; .2 `(47.425,40.8)` |

1. Place each bypass beside its own VIN/PGND pair. Route `capacitor + → VIN → internal switches → PGND → capacitor −` with short, broad F.Cu copper.
2. Put the larger input ceramics C201/C202/C215/C216 behind these local bypasses. C101 bulk does not replace them.
3. Connect both VIN sides through the protected-input strap on the lower power layer. Preserve the GND shield immediately under the IC.
4. Inspect the loop, not just the distance from a capacitor body to U201. Do not make switching return current travel around a slot or through a single remote via.

**WHY:** a short paired supply/return loop reduces switching spikes and noise. L201 is outside this input hot loop. Follow **TI SNVSBD5D §11, pp47–49**, especially Figure 11-2; the source register below identifies the read-only local PDF.

## 9. Keep SW compact; route BOOT locally

1. Find **U201.10 SW `(46,44)`** and **L201.1 `(51.95,44)`**. Join them with short, broad copper. L201.2 `(63.05,44)` is the raw DC output.
2. Keep FB, detector and latch routes away from SW and the inductor, on every routing layer. Do not add a large SW heatsink, bottom SW pour, long probe spur or unnecessary SW via.
3. Find **U201.13 RBOOT `(44.375,42.4)`** and **.14 CBOOT `(43.875,42.4)`**. R204 is the local **0 Ω** link: pad 1 `(44.025,40.85)` is RBOOT; pad 2 `(42.375,40.85)` is CBOOT.
4. Find C205: pad 1 `(42.825,39.35)` is CBOOT; pad 2 `(44.375,39.35)` returns to **native SW**, not GND or the output. Keep both capacitor legs short, widening where pin clearance allows.
5. Preserve the SW bootstrap branch through the gap between VIN2 and RBOOT, under U201 near `x44.9`. Do not recreate R1's bottom RBOOT detour. Compare actual pin-to-capacitor routes after refill.

**KNOWN FIX2 geometry:** RBOOT path **1.660 mm**, CBOOT pin-to-cap path **4.616 mm**, capacitor-to-SW path **5.945 mm**, all top-side; unconstrained capacitor branches were widened to **0.40 mm**, with **0.25 mm** in the tight corridor. These are comparison measurements, not TI maximum-length limits. The main SW zone alone is **11.135 mm²**, excluding pads/tracks; it stayed unchanged through FIX2. **OPEN:** startup and ringing qualification.

## 10. VCC, FB and ground

1. Find U201.2 VCC `(43.15,43.475)` and C206.1 `(41.1,42.8)`. Keep this bypass route short and broad. C206.2 `(41.1,44.7)` returns locally to AGND, U201.3 `(43.15,44)`.
2. Find U201.4 FB `(43.15,44.525)`. Keep R203.1 `(41.675,46.2)` close to it; R203.2 `(40.025,46.2)` returns locally to AGND. R202 `(37.25,46.4)`, R205 `(35.25,44.1)` and C207 `(38,44.1)` stay on the quiet left side.
3. Take R202's upper sense connection from the raw output capacitor node `/VOUT_5V1`, before F301. Keep the longer output-sense route away from SW. Do not move it to `/VOUT_PI` as an informal voltage-drop fix.
4. Remove redundant feedback branches. Keep R201 at RT and R206/R207 at EN out of switching fields. Preserve grounded BIAS and the unused PGOOD pin as captured.
5. Join AGND and PGND through the local ground structure and nearby bypass-return vias. Keep L2 connected. Guide large input/output/crowbar returns away from quiet sense connections by placement and broad copper; do not cut L2 into “analog” and “power” islands.

**KNOWN:** R202/R203 are **100 kΩ / 24.6 kΩ**; C207/R205 are **22 pF / 1 kΩ**. FIX2 VCC path is **2.248 mm**, FB pin-to-R203 path **2.842 mm**. Total FB tree length is a different quantity. **CALCULATED:** `1 × (1 + 100/24.6) = 5.065041 V`. **OPEN:** loop stability, light-load behavior and transients after capacitor/layout changes.

## 11. Thermal vias and copper

1. Add heat paths at U201's **real VIN and GND lands**, on their correct nets. **KNOWN: this RJR package has 14 pins and no separate ground EP15.** Do not invent an exposed pad.
2. Preserve each input FET's separate F/B/L3 drain spreader. A GND via in either drain pad is a short, not cooling.
3. Keep via holes outside open solder lands and paste windows. Inspect both faces. **KNOWN selected process:** ordinary off-land tented through vias; tenting covers a hole with mask where possible, not filled/capped via-in-pad.
4. Use the current **0.60/0.30 mm diameter/drill** as the project via default, not a “one via per ampere” rule. Calculate arrays from actual plating, current sharing and pulse duty. Avoid narrow thermal spokes on force connections unless their loss and soldering process are reviewed.

**KNOWN FIX2 audit:** no via-hole/open-land overlaps; minimum audited gap about **0.142 mm**. This is saved geometry, not guaranteed manufactured mask registration.

**CALCULATED thermal screen:** the illustrative **50°C ambient** and **10 W/m²K cooling** case gives Q101/Q102/U201 about **181.0/181.6/206.8°C**. The model fails its assumed envelope; these are not reliable operating-temperature predictions. **OPEN:** efficiency, actual heat, enclosure/airflow, derating and hot SOA. Even the proposed initial **2 A** characterization ceiling is conditional, not an approved rating. Follow [thermal mitigation](../evidence/v1a_lite/fix1/THERMAL_MITIGATION.md), not the silk “5A TARGET”, when planning a later reviewed test.

## 12. Keep detector and latch groups quiet

1. Around U101 `(30.5,34)`, keep R150–R153's REF connection short and quiet. Place its ground reference and C102/D104 control supply return away from D101 surge current. Keep D105/R144–R146 and Q103 close enough to avoid long gate-control loops.
2. Group Q104/Q105 with R160/R161/R164/R165; place Q106/R162/R166 near the Q103 base it inhibits. R163 carries the crowbar event into `SET_LATCH`. Do not route that sensitive event beside SW or through hot resistor-bank copper.
3. Keep `CTRL12` supplied from **S_COMMON upstream of Q102**, through R110–R125. Output collapse must not remove the latch supply by a routing shortcut.
4. Spread ballast resistor heat while preserving the two equal series strings. Do not put the precision dividers in their hot exhaust area.

**CALCULATED:** input divider **102 kΩ / 10 kΩ** gives approximately **27.944 V ideal**; it is not a guaranteed 28 V switch. **OPEN:** detector timing, pulse capture, latch retention during supply dips, reset interval and noise margin. A compact layout supports qualification; it does not prove these behaviors.

## 13. Place the crowbar at the raw capacitors

A **crowbar** deliberately shorts the faulty output through an SCR. **Force current** is the large load/fault current. A **Kelvin sense** connection is a separate small-current pickup from the terminal being measured, avoiding force-path voltage drop.

1. Locate SCR301: **KNOWN** K/cathode pad 1 `(69,33.4)` is GND; A/anode pad 2 `(66.46,33.4)` and the metal tab are raw VOUT; G/gate pad 3 `(63.92,33.4)` is SCR_GATE.
2. Pair broad anode copper from C209–C214/C217/C218 with a nearby broad cathode-to-capacitor-negative return. C217 minus `(69,26)` faces the cathode; C218 minus `(76,26)` faces inward. Keep local ground stitching and L2 continuity.
3. Keep **no fuse or removable link between the raw bank and SCR**. U301's upper divider and Q301 emitter also stay on raw VOUT. F301 follows only in the Pi branch. Removing F301 must leave raw capacitors, detector and SCR connected.
4. Keep Q301/R307 gate drive compact. Return R308.2 `(73,33.675)` directly toward the cathode, separate from force-current entry. Preserve nearby gate/cathode measurement access.
5. For detector sensing, use C214 positive `(66.025,56)` and negative `(68.975,56)` as the selected terminal pair. Route R301's pickup and the U301/R304 reference return together, outside SCR force current. A separately drawn GND track merged into the GND zone is **not** an isolated Kelvin return.

**KNOWN:** FIX2 moves R301's pickup toward C214 and adds return-routing work. **OPEN:** the saved review still does not establish an isolated detector Kelvin return or its dynamic accuracy. U301.3 `(60.9375,55)` and R304.2 `(56.5,54.175)` need that review. If a distinct sense net/net-tie is needed, change it deliberately in the schematic, run ERC, update the PCB, and review the connection point. Do not isolate it by cutting the shielding plane.

**WHY:** a ground spike can appear to the detector as an output-voltage change. A poor gate return can alter SCR firing. The short force loop also needs a pulse check: **CALCULATED sensitivity**, an assumed **10 nH** loop gives about **465 A/µs**. The inherited TYN612 limit is **KNOWN: 50 A/µs under specified gate conditions**, not a universal allowable waveform. Do not add arbitrary trace inductance to “fix” it. Gate rise/current, both capacitor reservoirs, source energy until Q102 opens, recovery, repeated faults and remote overshoot remain **OPEN**. See [crowbar review](../evidence/v1a_lite/fix1/CROWBAR_REVIEW.md).

## 14. Route the 5 A path by resistance, not a width slogan

1. Trace **L201.2 → raw copper → F301.1 `(72.045,43)` → fuse → F301.2 `(76.955,43)` → J502.1 `(84,44)`**. Inspect the return from J502.2 `(84,47.96)` to the output bank and buck ground.
2. Keep a broad route through the former obstruction near `(69.5,39.65)` and the current corridor near `x69.5, y41–45`. R308 or a GND-via clearance must not pinch that route again.
3. **KNOWN drawing baseline:** the fix used a nominal **4 mm** authored corridor with L3 support. The Power net-class track default is only **1 mm**. Neither number proves 5 A capability. A zone's drawn boundary is not its final usable width.
4. Refill and measure the narrowest **filled** necks. Count every pad escape, thermal spoke, layer transfer and GND return. Prefer keeping the main force path on broad outer copper, with reviewed parallel reinforcement.

**CALCULATED example only:** for copper, `R = ρL/(w t)`, with `ρ20 = 0.01724 Ω·mm²/m`. Use L in metres, width and thickness in mm. A **20 mm × 5 mm × 0.035 mm** strip is **1.970 mΩ at 20°C**, or **2.473 mΩ at assumed 85°C** using `R85 = R20 × [1 + 0.00393 × 65]`. At **5 A** it drops **12.36 mV**. This is one strip; add its return and all other series resistance. It is not a temperature/current rating. Each **1 mΩ** costs **5 mV and 25 mW** at **5 A**.

**CALCULATED FIX2 filled-copper reference**, [0.1 mm mesh](../evidence/v1a_lite/fix2/COPPER_RESISTANCE_0.1.json):

| Path | At 20°C | At assumed 85°C | Drop at 5 A / 85°C |
| --- | ---: | ---: | ---: |
| L201.2 to F301.1 | 1.073683 mΩ | 1.347956 mΩ | 6.740 mV |
| C214 to J502, positive and return, excluding fuse body | 4.378396 mΩ | 5.496858 mΩ | 27.484 mV |

These rows are different source-terminal models; do not add them. L201 supplies DC current; capacitor injections sample bank spreading. The mesh assumes **18 µm barrel plating**, nominal copper and ideal terminal contacts. It excludes joints, fuse body and switching behavior. It is not a guaranteed upper bound or an ampacity test.

**KNOWN harness allocation:** total hot/aged harness round trip **≤25 mΩ**, including mates, cable and splices. The older **40 mΩ** figure in historical bench prose is superseded by [PI_HARNESS.md](../evidence/v1a_lite/PI_HARNESS.md). At **5 A**, J502 must stay at least **4.875 V** before measurement uncertainty for this allocation to deliver **4.75 V** remotely.

**CALCULATED conditional budget:**

```text
Vraw,min = 0.99 × [1 + (100k × 0.999)/(24.6k × 1.001)]
         = 5.006350 V
Vpi      = 5.006350 − 5 × (0.025 + 0.009 + 0.005496858)
         = 4.808866 V
Margin   = 58.866 mV above 4.75 V
```

The terms are the harness allocation, **cold** fuse resistance screen, and sampled hot copper. **OPEN:** hot fuse, joints, minimum copper/plating, ripple, load steps, temperature drift and uncertainty. FIX1's extra-loss sensitivity already fell below the requirement. Preserve margin; do not increase R202/R203's setpoint without repeating the crowbar trip-window analysis. No Pi until remote dummy-load qualification passes.

## 15. Leave real probe access

**KNOWN FIX2 pad centres, mm; all are sense-only test pads:**

| Pad | Net | Face and position |
| --- | --- | --- |
| TP501 / TP502 / TP503 | VIN_RAW / VIN_FUSED / VIN_PROTECTED | Front `(17,23)` / `(23.5,25)` / `(54,35)` |
| TP110 / TP111 / TP112 | SET_LATCH / LATCH_H / IN_NPN_BASE | Front `(54,12.25)` / `(59,12.25)` / `(44.25,13)` |
| TP113 / TP114 | S_COMMON / CUT_GATE | **Bottom** `(37.2,21.6)` / `(37.2,18.4)` |
| TP301 / TP302 | SCR_GATE / cathode GND | Front `(66.5,38.35)` / `(69.6,38.35)` |
| TP504 / TP506 | raw VOUT_5V1 / GND | **Bottom** `(65.9,56)` / `(69.35,56)` |
| TP505 | VOUT_PI | Front `(86,59)` |
| TP507 / TP508 | CTRL12 / CB_COLLECTOR | Front `(34,59)` / `(83,37)` |

1. Leave room for the probe body, fingers and bottom-board access, not just its tip. Use the intended populated assembly and fixture envelope.
2. Measure Q102 gate-to-source as **TP114 minus TP113** with a rated differential probe. An earth-grounded clip on S_COMMON or CUT_GATE can short the circuit.
3. TP508 is **before R307**, not the SCR gate. Use TP301/302 for gate-to-cathode measurement; use designated adjacent component-terminal pickups for fast edges when pad branches add error.
4. Use a short spring/differential pickup at C214 for fast ripple. Pad proximity alone does not establish the measurement response or Kelvin isolation. Do not recreate a long cathode-sense slot in the return plane.
5. Use J503's force pads for a suitable reviewed dummy-load connection; use remote harness terminals when measuring Pi-node drop/transients. Never pass load/injection current through a small test pad.

**KNOWN pair spacing:** Q102 **3.20 mm**, SCR **3.10 mm**, raw ripple **3.45 mm**. **OPEN:** populated access, probe loading and high-frequency accuracy. Follow [BENCH_TESTS.md](../evidence/v1a_lite/BENCH_TESTS.md), with the updated harness allocation and approved thermal limits.

## 16. Silk, polarity and mechanics

**KNOWN connector map:**

| Connector | Positive pad | Return pad | Required readable meaning |
| --- | --- | --- | --- |
| J501 | 1 `(16,32)` VIN_RAW | 2 `(16,35.96)` GND | `J501 1 VIN+`, `2 GND` |
| J502 | 1 `(84,44)` VOUT_PI | 2 `(84,47.96)` GND | `J502 1 +5V`, `2 GND` |
| J503 | 1 `(68,61.5)` VOUT_PI | 2 `(78,61.5)` GND | `J503 +`, `GND` |

1. Put each label beside its actual pad/end, visible outside the fitted body. Verify connector mating-face polarity with the harness drawing and unpowered continuity. J502.1 is **not Pi physical pin 1**.
2. Retain C217 positive at `(64,26)` and C218 positive at `(81,26)`; C218 is rotated. Retain SCR K/A/G right-to-left and device pin-1 marks.
3. **KNOWN configured silk minimums:** text height **1.0 mm**, stroke **0.15 mm**, clearance to pads **0.15 mm**. Keep a clear practice revision and the fabrication warning. Inspect silk after mask openings are subtracted in plots.
4. Explain short labels: FIX2 `Q1/Q2/U2` mean Q101/Q102/U201. Its back legend carries TP110/111/301/302 where local marks are omitted. Keep leader marks/legend unambiguous when parts move; update coordinates and the assembly drawing. Do not call this complete local identification.
5. **KNOWN holes:** centres `(14,14)/(86,14)/(14,66)/(86,66)`, **3.2 mm NPTH**. NPTH means no plated barrel. **OPEN:** screw heads, washers, insulating hardware, connector mating/strain relief and probe envelopes. Define these from chosen hardware before adding keepouts.
6. Reserve an insulated cooling envelope for SCR301 if pulse/repetition analysis requires it. Its metal tab is live anode. Missing connector/custom models in 3D are not evidence of empty space or fit.

## 17. Turn every review finding into a check

**KNOWN review mapping:** R1 items 1–11 correspond to R2 items 1–11. R2's zero layout blockers did not close electrical or fabrication gates. FIX2 improved geometry later; retain these rules for every reroute.

| Review item | Rule you apply | Guide section / remaining limit |
| --- | --- | --- |
| R1/R2 1 polarity | Match printed positive/GND to actual pads and cable mating face. | 16; physical continuity still required. |
| R1/R2 2 BOOT | Keep RBOOT top-only and compact both C205 legs; compare terminal paths. | 9; ringing/startup OPEN. |
| R1/R2 3 crowbar | Broad paired raw-bank/SCR loop, direct K return, no intervening fuse; bound gate/anode pulse and recovery. | 13; pulse qualification OPEN. |
| R1/R2 4 voltage/copper | No R308/via obstruction; rerun L201 path, return and complete hot voltage allocation. | 14; cold-fuse assumption is insufficient. |
| R1/R2 5 thermal | Correct live drain/VIN/GND spreaders, actual stack and selected FET model; verify coupled loss/cooling. | 4, 11; thermal screen failed. |
| R1/R2 6 probes | Pair terminal pickups, preserve return plane, check front/bottom probe bodies. | 15; close pad centres alone are insufficient. |
| R1/R2 7 quiet control | Local VCC/FB/AGND; detector sense and return from raw capacitor terminals. | 10, 13; isolated Kelvin claim remains OPEN. |
| R1/R2 8 spacing | Define environment/coating and full net-pair voltage envelope, then encode electrical spacing. | 7; manufacturing DRC is limited. |
| R1/R2 9 silk | Process-sized warning/revision/polarity plus unambiguous local ID or legend; readable Fab drawing. | 16; some local IDs remain omitted. |
| R1/R2 10 via process | Keep holes out of open lands on both faces; retain standard off-land process. | 11; inspect actual solder/voids later. |
| R1/R2 11 assembly | Check each package's supplier pin-1, anchor and rotation; no blanket angle offset. | 18; supplier acceptance OPEN. |
| R1 12 topology/geometry | Preserve fuse→TVS→opposed FET order, raw SCR topology, actual pin maps, hole/edge rules and matching exports. | 6, 8, 13, 18; do not restore old EP or shunt. |
| R1 12 / R2 12 planes/SW | L2 remains GND-only and connected; no enlarged SW island or FB over SW. | 4, 9–10; EMI remains unmeasured. |
| R1 12 / R2 13 file integrity | Regenerate from the exact practice revision; match layers, drills, BOM/CPL sets and hashes. | 18; stale review package cannot represent your edits. |
| R1 12 / R2 14 mechanics | Check chosen screws, washers, connector/probe bodies and live-tab insulation/cooling. | 16, 18; absent models cannot close fit. |

## 18. Check your work after each session

1. Press **B**, save, then open **Inspect → Design Rules Checker**. Include schematic parity (PCB agrees with schematic), all severities and all track errors. Double-click each result to locate it. Check violations, unconnected items and parity separately. Repair causes; do not suppress whole rule classes.
2. Keep `V1A.kicad_pro` and `V1A.kicad_dru` beside the board. **KNOWN project minima:** track **0.15 mm**, default clearance **0.15 mm**, Power clearance **0.20 mm**, via **0.60/0.30 mm** with **0.15 mm** annulus, general hole spacing/clearance **0.25 mm**, copper-edge **0.50 mm**, mask web **0.10 mm**. Custom rules require component-hole spacing **0.45 mm**, plated component annulus **0.20 mm** and plated component hole-to-copper **0.28 mm**. An annulus is the copper ring around a drilled hole. Preserve compatible mask-process assumptions.
3. Inspect filled copper layer by layer. Follow both send and return. Look under pads for necks, isolated islands, thermal spokes and accidental bypasses. Check L2 beneath buck/control and SCR/caps. Highlighting GND does not prove a quiet return.
4. Recalculate the path using your filled board. Compare the actual L201 source path as well as capacitor-bank samples. Use minimum copper/plating and hot losses when their bounds become available. The optional calculation workflow below is a screen, not a current rating.
5. Open **Alt+3**, rotate to both faces, and compare with F.Fab/B.Fab and a full-size print. Check connector latches, capacitor polarity, SCR pins/tab, solder access and actual screw/probe envelopes.
6. For a later review export, keep all **four** copper layers, PTH and NPTH drills, and a clear review-only notice. Check each output against the saved board. After assembly-affecting edits, regenerate BOM/CPL and record per-package rotation acceptance in a new copy of the checklist.
7. **KNOWN baseline inventory:** **120 footprints**, comprising **100 purchased parts**, **15 test pads**, **J503**, and **four holes**. Baseline assembly split is **93 SMT / seven manual**: C101, C217, C218, D101, J501, J502, SCR301. D101 is exact external Bourns SMCJ64CA; blank LCSC in the assembly CSV is intentional. Native angles and THT lead anchors are not accepted supplier centroids. Reconcile changes instead of forcing future counts to match.
8. Save DRC, copper calculations, annotated views, board hash and OPEN list in a new session folder. Set meaningful practice revision metadata; the old job metadata `rev?` must not become a release identity.

**KNOWN CLI form**, from the repository root after refill/save; use a new session name each time:

```sh
mkdir -p docs/evidence/handroute/session-01
KICAD_CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
"$KICAD_CLI" pcb drc --format json --severity-all --all-track-errors \
  --schematic-parity --exit-code-violations \
  -o docs/evidence/handroute/session-01/DRC.json hardware/kicad/V1A.kicad_pcb
shasum -a 256 hardware/kicad/V1A.kicad_pcb
```

On another system, use its installed `kicad-cli`. Check `pcb drc --help` for that installation. [KiCad CLI reference](https://docs.kicad.org/9.0/en/cli/cli.html).

### Optional: repeat the existing copper calculation

1. Read [extract_lite_copper.py](../../scripts/extract_lite_copper.py) and [calculate_lite_copper.py](../../scripts/calculate_lite_copper.py). They assume the current outline, four-layer stack, net names and terminal references. Do not use them unchanged after changing those assumptions.
2. Refill and save in KiCad. Use a new session directory, so historical FIX1/FIX2 evidence stays intact.
3. On this Mac, with a C++ compiler and the existing NumPy/Pillow Python environment available, run:

```sh
KICAD_PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
PYTHONDONTWRITEBYTECODE=1 "$KICAD_PY" scripts/extract_lite_copper.py \
  --out docs/evidence/handroute/session-01/COPPER_GEOMETRY.json
c++ -O3 -std=c++17 -dynamiclib scripts/lite_resistance_solver.cpp \
  -o /tmp/lite-resistance.dylib
python3 scripts/calculate_lite_copper.py --grid 0.1 \
  --evidence docs/evidence/handroute/session-01
python3 scripts/calculate_lite_copper.py --grid 0.2 \
  --evidence docs/evidence/handroute/session-01
```

4. Compare `geometry_board_sha256` with your saved board hash. Compare both meshes, solver residuals, L201→F301 resistance, return resistance and the location of current crowding. A small residual means the numerical solver converged, not that its physical assumptions are correct. Update the full voltage budget separately.
5. If a tool/dependency is unavailable or your geometry no longer fits the model, record the calculation **OPEN**. Do not borrow an old PASS. Do not run `layout_v1a_lite.py import`, placement, routing or FIX scripts: those can overwrite your hand work.

## 19. What not to change without another review

1. Keep the input body-diode direction, Q102 shutdown, upstream latch supply, raw crowbar connection and F301 boundary.
2. Recheck all calculations before changing the FB/OV dividers, TL431 grade, SCR/gate parts, FETs, fuses, TVSs, L201, capacitor bank or voltage rating. See the schematic guide's danger table.
3. Recheck thermal, current and pulse behavior before changing stack, copper width, vias, switching loops, sense pickup, ground return, mounting or cooling.
4. Keep the staged bring-up sequence: inspection → continuity → current-limited supply → no-load startup → rail checks → low dummy load → increasing load → thermal → ripple → transients → faults → telemetry **N/A in Lite** → SBC only after all applicable gates pass. Missing acceptance limits stay **OPEN**.

## 20. Reading trail and provenance

**KNOWN project sources:** current native schematic/PCB/project/rules at `ee31d04`; [LAYOUT_EXPLAINED](../evidence/v1a_lite/LAYOUT_EXPLAINED.md), [LAYOUT_PROGRESS](../evidence/v1a_lite/LAYOUT_PROGRESS.md), R1/R2 linked above, [PCB_FIX1_REPORT](../evidence/v1a_lite/PCB_FIX1_REPORT.md), [PHASE_C_CALCULATIONS](../evidence/v1a_lite/PHASE_C_CALCULATIONS.md), [PHASE_C2_REVISION](../evidence/v1a_lite/PHASE_C2_REVISION.md), [SCH_REVIEW_R1](../evidence/v1a_lite/SCH_REVIEW_R1.md), harness and bench notes. Current CAD/FIX2 establish saved geometry; earlier reports establish historical reasoning and unresolved risks. Do not rerun historical calculation generators over their archived outputs.

**KNOWN reference-only use:** the old `/Users/quockaiser/Desktop/Research/V1A-Lessons/PCB_LAYOUT_GUIDE.md` supplied teaching style, not Lite topology or ratings. TI **LM61460 SNVSBD5D, July 2022 Rev D**, [official PDF](https://www.ti.com/lit/ds/symlink/lm61460.pdf), **§11 pp47–49**, was read from `/Users/quockaiser/Desktop/Research/wt-datasheets/third_party/datasheets/LM61460AANRJRR.pdf` and its existing `/private/tmp/liteb/LM61460AANRJRR.txt` extraction. Studied functions: input loops, BOOT, VCC/FB, ground and heat flow. No source, circuit or PCB artwork was modified/copied in this documentation task. TI copyright remains; no redistribution license asserted. Retain attribution to TI/document/section. Existing manufacturer/footprint/license records stay isolated under [FIX1 sources](../../third_party/v1a_lite_pcb_fix1/SOURCES.md), [layout sources](../../third_party/v1a_lite_layout/SOURCES.md) and [C3 manifest](../../third_party/v1a_lite_phase_c3/DOCUMENT_MANIFEST.json).

**KNOWN software sources:** official KiCad 9 manuals linked above, accessed 2026-10-05, documentation revision `152cd19e` where displayed (manual based on 9.0.9); installed 9.0.6 CLI help checked separately. Referenced for UI/commands only; no third-party design reused or upstream source changed. KiCad Documentation Contributors license their manuals under GPL-3.0-or-later or CC-BY-3.0-or-later. This guide independently applies the tools to the project; no manual or datasheet file is redistributed.
