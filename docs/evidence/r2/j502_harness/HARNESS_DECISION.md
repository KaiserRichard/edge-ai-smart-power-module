# J502 → Raspberry Pi GPIO power harness — preliminary decision

Review date: 2026-09-29. Branch: `feat/j502-gpio-harness`.

**STATUS: CONDITIONAL PASS for this preliminary selection document; BLOCKED for demonstrated power delivery and R2 release. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Recommendation and result

**DECISION:** select **Phoenix Contact `1776508` / `MSTB 2,5/ 2-GF-5,08`** for J502 and **`1777989` / `MSTB 2,5/ 2-STF-5,08`** for the mating screw-lock plug, provisionally. Its housing, screw clamps and socket contacts are an assembly: **separate J502 crimp MPN: not applicable**. Use Belden `8522 002100` red / `8522 010100` black trunk wires and Belden `8503 002100` red / `8503 010100` black fan-out wires. At the Pi use **Harwin `M20-1071000` housing + `M20-1180042` crimp sockets**, with an indexed mechanical hold-down. Parts and limits: [S3–S9](source_register.json).

**ASSUMED — proposed assembly dimensions:** AWG18 trunk, maximum **150 mm per polarity**, then AWG22 fan-out, maximum **50 mm per branch**; maximum electrical one-way wire length **200 mm**, including bend/service allowance. Populate **two positive branches** and **four ground branches**. These are proposed harness specifications, not missing system requirements silently frozen. [A1, below]

**CALCULATED — conditional hot budget:** from `VOUT_PROTECTED` to the Pi header rail, including ground return, **61.955 mΩ**, **309.773 mV drop**, **1.549 W loss** at the **ASSUMED analysis load of 5 A [U1]**. With the existing low regulator screen and the historical protection allocation, the Pi sees **4.6785 V static**, or **4.5785 V with the ASSUMED 100 mV droop reserve**. Both miss the **ASSUMED GPIO operating floor of 4.75 V**, based on documented Raspberry Pi engineer guidance [S1]. A guaranteed hardware worst case is **OPEN**: several entries are allocations and the Pi male header is unqualified.

**DECISION:** do not claim that the present setpoint delivers the required rail. The selected harness gives a concrete resistance/retention target to qualify. Reduce the verified path resistance or jointly revise regulation and output protection before release. No schematic, feedback, footprint or PCB was changed.

## Evidence labels and reused work

Every engineering quantity uses **DATASHEET** (manufacturer documentation, including nominal/test values as identified), **ASSUMED** (analysis input, proposed allocation or extension beyond documentation), or **CALCULATED** (derived from identified inputs). `OPEN` means evidence or acceptance remains missing. **U1** is this task's frozen D-30 instruction: GPIO power through physical pins **2 and 4**, multiple grounds, **5 A continuous envelope**, and **strictly <5.5 V peak**. These are REQUIREMENTS, carried as **ASSUMED analysis inputs from U1**, not newly uncertain requirements. Dates, part identifiers and source page numbers are identifiers rather than electrical values.

**OBSERVATION:** reused the connector shortlist at commit `ea6bf16cd2095b66c49c11b7806c8f6df096877c`, and Pi envelope review at `a4155dd14f9bd5a75fa5adc580874f5e431ccb01`; see [P1/P2 source files and provenance](source_register.json). The original worktrees were read without modification. The existing [connector qualification](../forensic_2026-09-14/CONNECTOR_HARNESS_QUALIFICATION.md), [drop model](../forensic_2026-09-14/PI_POWER_DELIVERY_REFINED.md), and [buck review](../BUCK_DESIGN.md) are preserved. The new option is the screw-lock version of the previously studied Phoenix family. No third-party PCB or circuit was copied.

## Pi voltage floor and contact-current answer

**EVIDENCE, not a formal GPIO datasheet:** Raspberry Pi engineer dp11's official-forum post dated 2023-11-14 documents **4.75–5.5 V** for Pi 5 and includes noise/transients in the upper bound. The discussion concerns USB power. **ASSUMED [S1]:** apply **4.75 V** as the GPIO rail operating floor for this preliminary budget; written GPIO-specific confirmation remains OPEN. The user's stricter **<5.5 V peak [U1]** controls the upper acceptance boundary. The official HAT+ specification recommends **DATASHEET 5.1 V / 5 A** for a Power HAT+, supporting the supply class but not establishing individual contact ratings [S2].

**DATASHEET [S10]:** official power documentation describes an undervoltage indication of approximately **4.63 V ±5%**. This is a warning threshold, not an operating minimum. **CALCULATED:** its upper tolerance corner is **4.8615 V**. Applicability of that exact detector tolerance to the selected Pi board/firmware and a warning-free operating criterion remain OPEN; passing the preliminary floor alone does not establish warning-free or peripheral operation. GPIO feeding also bypasses the USB-C input OVP, per Raspberry Pi engineer jdb [S11].

There is **no universal current rating for a DATASHEET 2.54 mm pitch**. The selected Harwin system is **DATASHEET 3 A/contact**, with **20 mΩ initial / 30 mΩ after conditioning** contact resistance [S7]. Its official drawing specifies a **DATASHEET 0.64 mm square mating pin**, with **5.50–6.30 mm mating length** [S8]. **OPEN:** the actual Pi 5 fitted male-header MPN, rating, plating, engagement and qualified pairing were not published in the retrieved sources. A Harwin rating cannot be transferred to an unidentified Pi male contact merely because pitch matches.

| Function | Physical Pi pins / classification | Current at analysis load / classification | Finding |
| --- | --- | --- | --- |
| Positive supply | **DATASHEET [S10]: 2, 4**; **ASSUMED [U1]: use both** | **CALCULATED: 5/2 = 2.50 A each**, equal sharing | Below the selected socket's **DATASHEET 3 A/contact**, conditional on sharing, temperature and actual mating header |
| Return, selected | **DATASHEET [S10]: 6, 9, 14, 20 are GND**; **ASSUMED [A1]: use all four** | **CALCULATED: 5/4 = 1.25 A each**, equal sharing | More return margin and less contact drop; does not improve the positive-pin rating |
| Theoretical minimum returns | **CALCULATED: ceil(5/3) = 2 GND contacts** using the selected socket rating | **CALCULATED: 2.50 A each** if equal | Not the recommended assembly; fewer grounds increase drop and sensitivity to sharing |
| One positive contact lost | **ASSUMED fault: one of the two branches open** | **CALCULATED: 5 A** in the survivor | Exceeds **DATASHEET 3 A**; no single-contact-fault tolerance claimed |

**Direct answer:** **CALCULATED 5 A through the two positive pins is within the selected female-contact headline rating only when each remains at or below DATASHEET 3 A**. It is **not yet within a verified rating of the complete Pi interface**. At the analysis load, the low-resistance positive branch must carry no more than **CALCULATED 60%**, hence the two branch resistances must have a ratio no greater than **CALCULATED 1.5:1** (`I_lowR = I_total × R_high/(R_low+R_high)`). Equal wire length helps but does not guarantee contact sharing. Measure individual branches hot, including after retention/conditioning tests; any lower derated vendor limit supersedes this headline screen.

## J502 comparison

Each J502 polarity carries the entire **ASSUMED 5 A [U1]**; its positions do not divide that current. The table reuses P1 and adds the locking derivative.

| Option | Board header; mate; termination | DATASHEET current and resistance evidence | CALCULATED connector-only drop at analysis load | Retention and decision |
| --- | --- | --- | --- | --- |
| **Selected Phoenix screw-lock** | `1776508`; `1777989`; integral screw/socket assembly, no separate crimp | **12 A nominal** each; header after-durability **1.0 mΩ**, plug **1.4 mΩ**, reported after **25 cycles** [S3/S4] | **24 mV**, using **ASSUMED additive** `2×(1.0+1.4) mΩ`; **31.2 mV** with **ASSUMED ×1.3** hot sensitivity | Screw flanges retain mate. Selected; use the larger measured-acceptance allocation below |
| Earlier Phoenix friction mate | `1757242`; `1757019`; integral screw/socket assembly, no separate crimp | **12 A nominal**; header/plug after-durability **1.4/1.4 mΩ** [P1/S5] | **28 mV** with ASSUMED additive reference planes; **36.4 mV** with ASSUMED hot multiplier | No positive plug lock; extra captive bracket needed. Not selected |
| Earlier JST shrouded VH | `B2P-VH-FB-B`; `VHR-2N`; `SVH-21T-P1.1` contacts | **7 A with AWG18**, **10 mΩ initial / 20 mΩ after-test per mated pole** [P1/S6] | **100 mV initial / 200 mV after-test**; **260 mV** with ASSUMED hot multiplier | Housing latch, but large published drop. Not selected |

Phoenix's before/after resistance values are not separate resistors. Even summing header and plug values is an **ASSUMED screening convention** because their measurement planes can overlap; none is a guaranteed complete hot-loop maximum. **ASSUMED [A2]: allocate 10 mΩ to the complete J502 loop at operating temperature**, including both mated poles and screw terminations, to be verified by four-wire measurement. This replaces the catalogue-addition screen in the main budget. No additional screw-clamp term is added there.

**DATASHEET [S4]:** selected plug accepts AWG24–12 and flexible conductor cross-sections **0.2–2.5 mm²**, stripped **7 mm**; conductor torque **0.5–0.6 N·m**. Use bare stranded trunk wire, with no solder tinning; a ferrule would require its own reviewed fit and process. Flange-lock torque is **DATASHEET 0.3 N·m [S3/S4]**, a different adjustment. Exact assembly/AWG18 hot-current derating remains OPEN. Mating/unmating must be de-energized per the vendor operating instruction.

**ASSUMED mechanical constraint:** retain a non-interchangeable family for J501, such as the prior JST VH candidate. Do not fit a COMBICON input that accepts the output plug. Screw locking provides retention, not voltage coding; J501's final selection remains OPEN. Later mechanical review must allow the **DATASHEET 20.32 mm header width [S3]**, flange fasteners, tool access and strain relief. No footprint is assigned here.

## Assembly and retention specification

**ASSUMED [A1]:** preserve J502 circuit **1 = LOAD_5V1**, circuit **2 = GND**, from the existing design [P3]. Use one trunk of each polarity and a separate insulated fan-out splice for each. Splice the positive into the two equal-length red branches and ground into four equal-length black branches. Do not put multiple conductors into a contact intended for one. The splice part/process is OPEN; its resistance is included in A2 and its inspection/pull-test procedure must be released before assembly.

| Harness element | Selected parts and evidence | Proposed construction / classification |
| --- | --- | --- |
| Trunk | Belden `8522 002100` / `8522 010100`; **DATASHEET AWG18**, nominal **6.5 Ω/1000 ft**, nominal insulation OD **2.0 mm**, operating maximum **80 °C**, bend radius **20 mm** [S9] | **ASSUMED A1:** each conductor ≤150 mm; route supply/return together, strain-relieve independently of screw terminals |
| Fan-out | Belden `8503 002100` / `8503 010100`; **DATASHEET AWG22**, nominal **16.2 Ω/1000 ft**, nominal insulation OD **1.3 mm**, operating maximum **105 °C** [S9] | **ASSUMED A1:** each branch ≤50 mm, matched positive lengths, no unsupported splice bending |
| Pi socket | Harwin `M20-1071000` + `M20-1180042`; **DATASHEET 2×10 cavities**, crimp supports **AWG22–30**, tool `Z20-320` [S7/S8] | **ASSUMED A1:** populate only physical Pi pins 2/4/6/9/14/20 for power; remaining cavities empty. Housing occupies pins 1–20, not the whole header |
| Pi hold-down | Custom insulated indexed carrier; no manufactured part or drawing yet | **ASSUMED A1:** rigid carrier secured to Pi mounting points, with asymmetric orientation/end stops preventing reversal, one-row or one-column offset; captive bar prevents vertical withdrawal; cable clamp carries harness pull |

The Harwin housing is **DATASHEET non-polarized [S8]**. It is not mechanically safe to rely on colour or insertion friction. **DATASHEET [S7]:** cable-connector shock/vibration is not tested; contact-to-housing retention and crimp pull figures do not establish assembled plug retention. The carrier geometry, cooler clearance, fasteners, applied force/vibration profile and acceptable motion are **OPEN requirements**, not invented load ratings. No unrestrained individual jumper sockets are proposed. `M20-1072000` is not selected: the inspected manufacturer drawing does not support that size [S8].

**DATASHEET [S8b]:** the selected crimp accepts insulation OD **0.90–1.60 mm**, encompassing the branch wire's **DATASHEET nominal 1.3 mm [S9]**; strip length is **3–4 mm**, and conductor crimp height **0.83–0.89 mm** for **AWG22–24**. Confirm wire diameter tolerance, setup and pull tests with the specified tool before releasing assembly. Do not force the trunk into these smaller contacts.

The budget ends at the Pi's header rail/ground solder-pad reference planes and includes the mating contacts. The internal Pi rail-to-PMIC resistance is OPEN and is not silently included. Verify both positive-pin voltages relative to Pi ground; measurement only at J502 misses ground lift. USB-C must not be attached as another source in this assembly without separate power-sharing review. D435i data remains outside this PCB. Host software's external-supply/current declaration must be configured and verified separately; it does not increase a contact rating [S12].

## Voltage-drop budget

**Boundary:** `VOUT_PROTECTED` / module ground → R401 → module copper → J502 → trunk → splice/fan-out → Pi contacts → Pi ground → complete return to module ground. The output disconnect is **upstream of this boundary** and appears separately when deriving the source voltage. No USB-C connector or PD circuit is in this path.

**ASSUMED A1 thermal/model inputs:** wire/contact operating screen **60 °C**, nominal wire DCR reference **20 °C**, copper coefficient **0.00393/°C**, wire DCR allowance **+10%**, contact hot sensitivity **×1.3**, shunt screen **100 °C** from a **25 °C** reference, and dummy-load enclosure ambient screen **40 °C**. These are proposed conditions; system ambient/enclosure and qualified hot maxima remain OPEN. The wire allowance and contact multiplier are not manufacturer tolerance guarantees. Manufacturer wire current figures in free air do not qualify this bundle.

**CALCULATED formula:** `Rwire = DCRnom × length × [1 + 0.00393 × (60−20)] × 1.10`; convert the **DATASHEET per-1000-ft DCR [S9]** to SI. `Rparallel = Rbranch/n` for identical branches; `Vdrop = I×Rloop`; `Ploss = I²×Rloop`. Separate branch/contact entries below assume every intended branch is present. All-at-maximum identical resistances give the parallel resistance screen, but do not prove safe current sharing when resistances differ.

| Path element and reference planes | Resistance (mΩ) | Drop at analysis load (mV), CALCULATED | Source/classification |
| --- | ---: | ---: | --- |
| R401 force path | **CALCULATED 2.02379** | 10.119 | `WSL27262L000FEA`: **DATASHEET 2 mΩ ±1%, ±25 ppm/°C**; `2×1.01×(1+25e−6×75)` with ASSUMED shunt temperature [S13] |
| PCB positive, after boundary to J502 | **ASSUMED 2.500** | 12.500 | A2 copper/vias hot allocation; no layout exists |
| PCB return | **ASSUMED 2.500** | 12.500 | A2 copper/vias hot allocation |
| J502 positive mated pole and clamp | **ASSUMED 5.000** | 25.000 | A2 whole-assembly measurement allocation; S3/S4 screen supports candidate only |
| J502 return mated pole and clamp | **ASSUMED 5.000** | 25.000 | A2; not a duplicate male/female resistance |
| Positive trunk | **CALCULATED 4.07184** | 20.359 | S9 DCR + A1 length, temperature and allowance |
| Return trunk | **CALCULATED 4.07184** | 20.359 | S9 + A1 |
| Positive fan-out wires in parallel | **CALCULATED 1.69138** | 8.457 | Each branch **CALCULATED 3.38276 mΩ**, divided by ASSUMED two branches |
| Ground fan-out wires in parallel | **CALCULATED 0.84569** | 4.228 | Same branch model, divided by ASSUMED four branches |
| Pi positive mating contacts in parallel | **CALCULATED 19.500** | 97.500 | **DATASHEET 30 mΩ conditioned [S7] × ASSUMED 1.3 / 2**; application to actual Pi mate OPEN |
| Pi ground mating contacts in parallel | **CALCULATED 9.750** | 48.750 | Same contact model, divided by ASSUMED four grounds |
| Remaining joints, aggregate equivalent loop | **ASSUMED 5.000** | 25.000 | A2: module/header solder joints, fan-out splices and GPIO crimps not demonstrably covered above. Excludes J502 screw clamps already included |
| **Total, protected node to Pi** | **CALCULATED 61.95454** | **309.773** | [Machine-readable arithmetic and inputs](budget.json) |

**CALCULATED:** the positive Pi contacts alone dissipate **0.24375 W each** in this hot screen; each selected ground contact **0.06094 W**. R401 dissipates **0.05059 W** and develops **10.119 mV**; retain the existing Kelvin connections and INA228 sense routing. These are load-case calculations, not thermal validation or a change to monitoring calibration. Actual resistance/reference-plane measurements must replace the aggregate allocations without double-counting or omitting joints.

### Result with the existing source screen

**DATASHEET [S14]:** LM61460 reference accuracy is **±1%** under its stated conditions; its **10 nA feedback current is typical**, not an all-condition limit. **ASSUMED from captured design [P3]:** feedback divider **100 kΩ / 24.4 kΩ**, resistor tolerance **±0.1%**. **CALCULATED nominal:** **5.09836 V**. Treating the typical current as an **ASSUMED ±10 nA screen** gives **CALCULATED 5.03827 V low**. Full regulation/load/temperature/dynamic bounds remain OPEN; this is not a guaranteed source minimum.

**ASSUMED A3:** retain the historical **10 mΩ hot output-disconnect allocation [P3]**, outside the main table; it costs **CALCULATED 50 mV**. Thus **CALCULATED `VOUT_PROTECTED,min = 4.98827 V`** and **`Vpi,min,static = 4.67850 V`**. With the **ASSUMED 100 mV dynamic reserve [P3]**, **CALCULATED `Vpi,min,dynamic-screen = 4.57850 V`**. These are the report's conditional worst cases, not measured minima. Startup, load release, ripple, switching spikes and protection interruption require waveform evidence.

**CALCULATED sensitivity:** achieving a newer **ASSUMED 6.5 mΩ** disconnect allocation instead improves either Pi result by only **17.5 mV**; it cannot close this budget. Dropping the contact multiplier or using initial contacts would improve a screen but would not establish a hot/aged bound. With the current source and protection allocations, total downstream resistance must be **CALCULATED ≤47.654 mΩ static**, or **≤27.654 mΩ with the dynamic reserve**, to reach the preliminary floor. The proposed conservative budget exceeds both.

## Setpoint and remote-sense consequence

**CALCULATED:** this harness allocation requires `VOUT_PROTECTED,min` of **5.05977 V static**, or **5.15977 V including the ASSUMED 100 mV reserve**, to deliver the preliminary **ASSUMED 4.75 V GPIO floor [S1]**. Keeping A3 and the same source-tolerance model requires nominal buck setpoints of approximately **5.17073 V static** or **5.27194 V with reserve**, before additional design margin. Equations and results are in [budget.json](budget.json).

**ASSUMED sensitivity only, not a selected setpoint:** a nominal **5.30 V** source gives **CALCULATED 4.77772 V** at the Pi with the same low-side/dynamic assumptions. Its no-load source high screen is **CALCULATED 5.36270 V**; adding an independent **ASSUMED 100 mV positive excursion** gives **5.46270 V**, leaving only **CALCULATED 37.30 mV** below the strict user ceiling. Unknown normal/fault overshoot, measurement error and protection tolerance can consume that margin. It also conflicts with the currently studied protection window: P4's **ASSUMED 5.26444 V minimum trip / 50 mV nuisance margin** cannot accommodate this high normal voltage. Therefore **do not implement an automatic setpoint increase**; regulation, fault cutoff and resistance must be reviewed together.

Remote sensing could compensate static distribution loss, but is an **architectural change**, not a harness fix. Sensing only `LOAD_5V1` leaves wire and GPIO losses uncompensated; measuring Pi voltage relative to module ground leaves ground-return error. A true remote scheme needs both rail and return sensing, independent raw-rail limiting, open-sense/unplug fail-safe behavior and loop-stability review. Feedback after a disconnect can drive the raw output upward when protection opens. Keep existing feedback local until that design is justified. No remote-sense pins or conductors are added by this decision.

## Why

The screw-lock Phoenix pair combines the earlier shortlist's low resistance with a defined way to retain the plug. The JST alternative latches, but its published contact-resistance allowance consumes too much of the rail budget. The older Phoenix pair needs a separate plug restraint.

The thick trunk keeps most wire loss small. Short, matched smaller branches fit the specified Pi sockets and distribute the return over several contacts. Both positive pins are essential; extra grounds cannot relieve an overloaded positive contact. The Pi-side carrier must stop the unkeyed housing moving or being inserted incorrectly.

The calculations also show why choosing a connector by its current number is insufficient: contact resistance, return loss and the regulator's low corner use more voltage than the present target can spare. This is a preliminary parts/assembly decision with a failed conservative voltage screen, not validated delivery.

## Open items and completion gates

1. **Pi interface:** obtain the actual male-header rating/finish/engagement or written qualification, confirm the GPIO floor and any stricter no-warning/peripheral floor, and qualify the selected socket pairing and hot branch sharing.
2. **Source/protection:** replace the regulator and disconnect screens with bounded hot/loaded values; agree dynamic/ripple allocations; jointly resolve the low-voltage result and strict peak limit. No lost-contact or longer-harness operation is approved.
3. **Mechanics/assembly:** release connector orientation drawings, splice process/MPN, crimp settings, cable clamp and indexed carrier. Confirm cooler/accessory clearance and input/output non-interchangeability. Establish retention-force, vibration and servicing requirements; no numerical force requirement is invented here.
4. **Resistance/thermal qualification:** four-wire measurements across every table boundary, cold/hot and after approved conditioning. Include J502 clamps, individual positive branches and all returns; record conductor/contact temperatures and measurement uncertainty. If any allocation is exceeded, recompute and reopen the choice.
5. **R5 sequence after R2/R3/R4 review:** visual inspection → continuity/short and pin-map checks → current-limited bench supply → no-load startup → output-rail verification → low-current dummy load → increasing load → thermal → ripple → transient/load steps → protection/fault tests → telemetry → Pi integration. **ASSUMED proposed dummy-load points: 1, 3, 5 A [P3]**. Use a representative header fixture before an expensive Pi; the actual Pi pairing still needs final validation. Check voltage at both Pi positive contacts relative to Pi ground. Establish source setting/current declaration and the intended Pi/D435i runtime load only after prior gates pass.

**Evidence completion:** [source register](source_register.json), [budget](budget.json), and [validation record](VALIDATION.md). All calculated values are conditional. R2 remains BLOCKED; no ERC/DRC or bench PASS is claimed, and no later gate is skipped.
