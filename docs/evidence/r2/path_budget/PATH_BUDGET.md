# V1A 5 A path budget

2026-09-30. **PRELIMINARY — electrical release BLOCKED — NOT FOR FABRICATION.** Analysis only; no native KiCad file opened, saved or checked. Base `65a86982fc4a48502d3a6da1cd710e796b3d8734`. Requirements and numbers below use physical header pin numbering.

## OWNER EXPLANATION — one-page briefing

V1A converts a **REQUIREMENT 9–24 V** input to about **CALCULATED 5.10 V nominal**, then sends **REQUIREMENT 5 A** through protection, a current sensor, connectors and a short cable to the Pi5 GPIO header. The return path loses voltage too. The Pi must still receive **REQUIREMENT at least 4.75 V**. This report studies that delivery path; fault containment remains a separate unresolved engineering review.

Voltage lost is current times resistance. At **REQUIREMENT 5 A**, every **ASSUMED 1 mΩ** costs **CALCULATED 5 mV**. The inherited reduced hot path totals **CALCULATED 55.37 mΩ**, costing **276.84 mV**. Its largest losses are the Pi mating contacts (**121.88 mV**) and the module's two series transistors (**68.00 mV**). All wire sections together cost only **25.64 mV**. The current sensor costs **10.12 mV**. These are calculations inside assumptions, not measured losses.

The earlier source calculation leaves only **CALCULATED 11.43 mV** above the required floor. Adding E's **ASSUMED 10 mΩ** disconnect stage would lose another **CALCULATED 50 mV**. A thicker cable alone cannot recover that. The original longer cable with fewer grounds was worse: **CALCULATED 89.50 mV below** the floor.

Heat makes the problem tighter. Copper increases about **ASSUMED 0.39% per °C**. A wire at **ASSUMED 60°C** has **CALCULATED 15.72%** more resistance than at the **ASSUMED 20°C** reference. Transistor resistance rises with junction temperature; connector ageing and local heating matter too. Including assumed hot feedback-resistor drift lowers the buck's minimum screen from **CALCULATED 5.038 V to 5.026 V**. Real maximum losses and source tolerances still need qualification.

The recommended combination uses both 5 V pins and all eight grounds, a short thicker trunk, lower-loss series transistors, and a Pi mating contact qualified to **ASSUMED ≤20 mΩ hot and conditioned**. It keeps the existing sensor and nominal setpoint. Its target totals are **CALCULATED 35.07 mΩ for D**, with the final disconnect at the module, and **45.07 mΩ for E**, with an additional disconnect/absorber at the Pi. With an **ASSUMED 20 mV ripple trough**, the corresponding Pi screens are **CALCULATED 4.831 V and 4.781 V**.

More grounds help, but the reduced baseline already uses eight. There are only two ordinary 5 V header pins. Better transistors require driver and fault-timing work; better contacts require mating and thermal evidence. Raising the voltage or sensing remotely spends the narrow overvoltage-protection margin. Neither is recommended as a shortcut.

**OPEN:** the fitted Pi male-header rating, hot mated-contact maximum, real transistor gate voltage and regulator operating bounds. Until these are supplied, neither architecture has a verified worst-case pass. The calculations give component acceptance targets the owner can defend and test.

## Requirements, endpoints and evidence labels

**REQUIREMENT:** `V_Pi_GPIO >=4.75 V at 5 A`, worst-case hot copper, maximum contact resistance and minimum regulation. Retain the inherited strict fault ceiling `<5.5 V` and the fixed detector window. D-30 supplies physical pins **2 and 4 (5 V)** plus multiple GND pins through J502 and a short harness; no USB-C protection is credited. Architecture selection and implementation are not authorized by this report.

**ASSUMED** means an engineering screen or proposed acceptance target. **CALCULATED** means arithmetic using the stated assumptions/tolerances; a cited manufacturer's finite specification applies only at its test conditions. **OPEN** means no applicable bound; it is never assigned zero. Every finite voltage/loop total below is **CALCULATED within ASSUMED inputs**, not an established application maximum. Actual worst-case results remain `null` in [PATH_CALCULATIONS.json](PATH_CALCULATIONS.json).

Voltage endpoint: the loaded Pi GPIO 5 V pins relative to its loaded GPIO GND pins. Resistance inside the Pi beyond those pins is **OPEN** and not silently added as zero; a GPIO-voltage pass does not prove the PMIC/internal rail floor. Inter-pin plane spreading can also change current sharing and needs measurement.

The complete loop starts at the buck's regulated output reference, follows SEND to the Pi, then follows RETURN to the corresponding source return. Historical 55.37 mΩ begins at the documented raw-node voltage. The physical feedback pickoff/reference plane is **OPEN** without CAD/layout inspection. This study conservatively allocates an extra **ASSUMED 0.5 mΩ SEND +0.5 mΩ RETURN** for unsensed buck copper. Copper already inside the local feedback boundary is compensated and must not be counted again. The added allowance is explicitly separate from the inherited total.

Local evidence: [source reconciliation](SOURCE_AUDIT.md), [exact input identities](INPUT_PROVENANCE.json), [primary-source register](SOURCES.md), [prior electrical review](../sheet03/GATE2C_REVIEW_CLOSURE.md), [D/E architecture comparison](../sheet03/GATE3_ARCHITECTURE_OPTIONS.md), [D-30](../../../context/06_DECISION_LOG.md). PR #6 harness records were read at `54d3bc67fd64f4bd947440518d90e76673faf5db` with `git show`; they were not merged.

## Source and temperature budget

**ASSUMED thermal box:** wire/mating contacts60°C; module copper and feedback resistors85°C; FET junction150°C; shunt100°C. Actual enclosure temperatures, ambient envelope, thermal gradients, duty/life and measurement uncertainty are **OPEN**. These are deliberately distinct temperatures, not one measured hot condition.

**CALCULATED regulator stack:** `Vout = VFB(1+Rt/Rb)+IFB Rt`; inherited divider100 kΩ/24.4 kΩ. [TI S01](SOURCES.md) specifies VFB ±1% under its stated FPWM/VIN conditions over the table's temperature range. Initial divider tolerance **ASSUMED ±0.1% each**; IFB allowance **ASSUMED ±10 nA**, although the datasheet supplies only a typical10 nA. Feedback resistor MPN, actual TCR, regulator mode, full-load regulation/thermal headroom and bias maximum remain **OPEN**.

| CALCULATED source screen / permitted loop | 25°C divider stack | Hot divider stack |
|---|---:|---:|
| Raw static min / nominal / max V | 5.038271 /5.098361 /5.158632 | 5.026143 /5.098361 /5.171095 |
| ASSUMED each divider resistor tolerance | ±0.1% | ±0.25%: initial0.1% +25 ppm/K ×60 K |
| Loop ceiling at 5 A, static mΩ | 57.654280 | 55.228651 |
| With ASSUMED 20 mV negative ripple trough, mΩ | 53.654280 | 51.228651 |
| With ASSUMED 100 mV total negative excursion, mΩ | 37.654280 | 35.228651 |

The 20 mV and100 mV cases are sensitivity/acceptance proposals, not additional frozen requirements or measured ripple. The 100 mV case includes ripple; do not subtract it twice. No finite true minimum can be claimed until the OPEN source bounds close. E's inherited **ASSUMED ≤50 mΩ** target gives **CALCULATED 4.776143 V** in the hot/20 mV screen, only **+26.143 mV**; it does not by itself assure all transients.

## Itemised send and return budget

The table below reconstructs the inherited reduced case and adds the disclosed buck-copper allowance. All resistances are mΩ. Entries show **min /typ /max at 25°C and hot**; `OPEN` is a missing bound/typical value. A finite maximum marked A is **ASSUMED**, C is **CALCULATED** within that assumption. The actual application maximum is **OPEN for every unqualified row**, including rows with a vendor table maximum at different conditions. There is consequently no guaranteed sum of minima, typical values or maxima.

- **ASSUMED wire model:** manufacturer nominal DCR referenced to20°C; ±10% screen, `R(T)=R20[1+0.00393(T−20)]`. Belden8522 AWG18:6.5 Ω/1000 ft; 8503 AWG22:16.2 Ω/1000 ft. Nominal DCR is not a vendor maximum. Equal branch length/resistance is assumed; maximum parallel equivalent stays bounded if every intact branch meets its own maximum.
- **ASSUMED contact model:** hot factor1.3; no fabricated manufacturer typical or minimum. Harwin's30 mΩ conditioned test maximum becomes a39 mΩ screen, not a guaranteed hot Pi mate maximum. Each interface is counted once; female crimp and male pin attachment targets are separate reference planes.
- **ASSUMED PCB model:** allocation at 85°C, back-scaled to25°C with copper ratio 1.231256. Joint allocations are screened with factor1.3. These targets require four-wire measurements after build and conditioning.
- **CALCULATED shunt:** 2 mΩ, initial±1%, component TCR±25 ppm/K,100°C hot. Nominal temperature drift is zero for the central screen; worst signs apply at extremes. Force-terminal/pad resistance beyond the sense reference planes is **OPEN**, to be included in the PCB/joint allocation and measured end to end.

| Element | Leg | 25°C min /typ /max mΩ | Hot min /typ /max mΩ | Basis |
|---|---|---:|---:|---|
| Buck output copper | SEND | OPEN /OPEN /0.406 | OPEN /OPEN /0.500 | A: hot acceptance target |
| Buck return copper | RETURN | OPEN /OPEN /0.406 | OPEN /OPEN /0.500 | A: hot acceptance target |
| Module series FET pair | SEND | OPEN /5.600 /6.800 | OPEN /11.200 /13.600 | C:10 V; A:150°C ×2 |
| 2 mOhm current shunt | SEND | 1.980 /2.000 /2.020 | 1.976 /2.000 /2.024 | C:±1%, ±25 ppm/K;100°C |
| Module PCB traces / vias | SEND | OPEN /OPEN /0.812 | OPEN /OPEN /1.000 | A: hot acceptance target |
| J502 complete mated pole and clamp | SEND | OPEN /OPEN /2.400 | OPEN /OPEN /3.120 | A: hot acceptance target |
| Trunk wire AWG18 75 mm | SEND | 1.468 /1.631 /1.794 | 1.666 /1.851 /2.036 | C:nominal DCR; A:±10%,60°C |
| Module PCB traces / vias | RETURN | OPEN /OPEN /0.812 | OPEN /OPEN /1.000 | A: hot acceptance target |
| J502 complete mated pole and clamp | RETURN | OPEN /OPEN /2.400 | OPEN /OPEN /3.120 | A: hot acceptance target |
| Trunk wire AWG18 75 mm | RETURN | 1.468 /1.631 /1.794 | 1.666 /1.851 /2.036 | C:nominal DCR; A:±10%,60°C |
| AWG22 fan-out 25 mm, 2 parallel | SEND | 0.610 /0.677 /0.745 | 0.692 /0.769 /0.846 | C:nominal DCR; A:±10%,60°C |
| Pi mated contacts, 2 parallel | SEND | OPEN /OPEN /15.000 | OPEN /OPEN /19.500 | A: hot acceptance target |
| Pi female crimps, 2 parallel | SEND | OPEN /OPEN /0.308 | OPEN /OPEN /0.400 | A: hot acceptance target |
| Pi male pin / solder attachment, 2 parallel | SEND | OPEN /OPEN /0.185 | OPEN /OPEN /0.240 | A: hot acceptance target |
| AWG22 fan-out 25 mm, 8 parallel | RETURN | 0.152 /0.169 /0.186 | 0.173 /0.192 /0.211 | C:nominal DCR; A:±10%,60°C |
| Pi mated contacts, 8 parallel | RETURN | OPEN /OPEN /3.750 | OPEN /OPEN /4.875 | A: hot acceptance target |
| Pi female crimps, 8 parallel | RETURN | OPEN /OPEN /0.077 | OPEN /OPEN /0.100 | A: hot acceptance target |
| Pi male pin / solder attachment, 8 parallel | RETURN | OPEN /OPEN /0.046 | OPEN /OPEN /0.060 | A: hot acceptance target |
| Fan-out splice | SEND | OPEN /OPEN /0.385 | OPEN /OPEN /0.500 | A: hot acceptance target |
| Module solder joints | SEND | OPEN /OPEN /0.077 | OPEN /OPEN /0.100 | A: hot acceptance target |
| Fan-out splice | RETURN | OPEN /OPEN /0.385 | OPEN /OPEN /0.500 | A: hot acceptance target |
| Module solder joints | RETURN | OPEN /OPEN /0.077 | OPEN /OPEN /0.100 | A: hot acceptance target |

**CALCULATED hot subtotals:** SEND 43.865398 mΩ /219.327 mV; RETURN 12.502343 mΩ /62.512 mV at 5 A. 

**CALCULATED totals:** inherited downstream41.767741 mΩ +series pair 13.6 mΩ =**55.367741 mΩ**. Add unsensed buck-copper allocation1 mΩ →**56.367741 mΩ**. The joint split is a new **ASSUMED allocation** totaling the inherited2 mΩ; the historical source did not prove those individual values. Separate J502 crimps are **not applicable**: the chosen Phoenix plug uses integral screw clamps, included in its complete-pole target.

**OPEN Pi internal plane:** no applicable published Pi5 resistance or transfer matrix was found in the official [hardware/pinout sources S13](SOURCES.md). Do not claim zero, invent a layer stack, or add connector specification twice. Verify the loaded pin voltages and current distribution on the actual board revision before integration.

### Contact maximum versus a test reading

[Phoenix S06/S07](SOURCES.md) list 12 A nominal for selected1776508/1777989. Header durability readings are1.0 mΩ; plug before/after-cycle readings1.3/1.4 mΩ. R1/R2 represent test states. Adding header1.0 +plug1.4, then multiplying by1.3, gives **CALCULATED 3.12 mΩ/polarity** as an **ASSUMED screen**; reference-plane overlap and guaranteed complete-contact hot maxima are **OPEN**. Original PR #6 used an **ASSUMED 5 mΩ/polarity** allocation. Neither is described as a datasheet maximum. Four-wire qualification must include male/female mating, clamp, torque, permitted wire/ferrule and conditioning, without overlapping measurement spans.

[Harwin S08/S09](SOURCES.md) specify20 mΩ initial and30 mΩ conditioned maximum, and3 A/contact at their stated conditions. The Pi's actual male-header MPN, plating, mating length and derated hot rating are **OPEN**. Matching pitch does not transfer a qualified mate rating. Existing M20-1071000 is2×10, so one housing covers pins 1–20 only. Eight grounds need access to pins 21–40 as well: a second correctly indexed2×10 housing with retained support, or a fully reviewed Pi-entry board/socket. Do not pretend the existing housing reaches all grounds. Mechanical clearance/retention remain **OPEN**.

### FET resistance at the real gate voltage

The existing common-source BSC034N06NS pair does not divide current: both devices carry5 A. [Infineon S02](SOURCES.md) gives per-device 25°C typ/max2.8/3.4 mΩ at VGS 10 V and4.0/5.1 mΩ at 6 V. There is no guaranteed4.5 V row. Inherited hot factor2 gives **CALCULATED pair 13.6 mΩ at 10 V** or **20.4 mΩ at 6 V** within an **ASSUMED 150°C multiplier**. Table/curve transfer to actual current and Tj remains **OPEN**.

**OPEN real VGS:** regulated driver rail7.440–7.807 V and PG floor6.175 V are inherited **CALCULATED screens**, not MOSFET VGS. [LTC7001 S04](SOURCES.md) drives from its BST−TS supply. Its approximately12 V pumped supply and30 µA pump are not a loaded hot minimum. Qualify BST−TS and gate−source at each FET during steady5 A, startup, leakage, brownout and fault shutdown. Below the selected characterized drive level the resistance/timing claim is **OPEN**; VGS threshold is not full enhancement.

Proposed BSC014N06NS candidate [S03](SOURCES.md):25°C per-device typ/max1.2/1.45 mΩ at 10 V;1.6/2.2 mΩ at 6 V. With **ASSUMED ×2** hot scaling, pair screen is5.8 mΩ at 10 V; this report allocates **ASSUMED ≤6 mΩ hot** including0.2 mΩ reserve. At6 V the screen becomes8.8 mΩ. Application hot RDS, VDS overshoot, SOA and Tj qualification are still **OPEN**.

**CALCULATED drive cost:** listed test maximum pair Qg rises82→208 nC, **2.54×**; these charges are defined under the datasheet test, not complete application timing bounds. Manufacturer bootstrap sizing gives `CB > Qg/1 V`, hence **CALCULATED >208 nF effective** for the pair before any added gate capacitor (`+10 CG`), leakage and hold-up allowance. Effective capacitance, minimum loaded drive and complete turn-off time remain **OPEN**. A nominal capacitor or unchanged old timing sum is insufficient. The candidate is a research option, not an authorized replacement.

### Copper, sensing and heat

**ASSUMED prospective geometry:** module each leg30 mm×15 mm×70 µm copper; buck unsensed each leg10 mm×10 mm×70 µm. Using ASSUMED ρ20=1.724×10⁻⁸ Ωm, maximum length+10%, minimum width−5%, thickness−20%, and85°C gives **CALCULATED 0.895/0.448 mΩ per leg** respectively, leaving **0.105/0.052 mΩ** within the proposed1.0/0.5 mΩ allocation for vias and spreading. Actual width, thickness, neckdowns, via barrels and feedback boundary are **OPEN**. Resistance feasibility is not a copper ampacity or switch-loop-layout sign-off.

**CALCULATED shunt load:** at 5 A, nominal10 mV/50 mW; hot upper screen10.119 mV/50.595 mW. Keep Kelvin sense separate from force current; verify the monitor's range, offset/noise, gain and calibration. Changing to1 mΩ halves nominal signal to5 mV and increases this family's component TCR from25 to75 ppm/K [Vishay S05](SOURCES.md); hot upper screen1.015681 mΩ. Monitor accuracy after a change remains **OPEN**.

## Options: changed total, cost and effort

All totals/voltages are **CALCULATED** from hot source minimum5.026143 V, without a dynamic subtraction, within the **ASSUMED** targets above. D includes the extra1 mΩ buck-copper allowance; E retains that whole module path and adds **ASSUMED 10 mΩ**. Single changes below start from audited reduced D56.367741 mΩ. Dollar figures are **ASSUMED incremental planning allowances per assembly**, not quotes/stock evidence; procurement prices and quantities are **OPEN**. Prototype/engineering labor is excluded; effort describes required work. The combined allowance excludes E's additional protection PCB/auxiliary assembly; that total cost is OPEN here (the inherited architecture study separately estimated an ASSUMED $20–50).

| Change | D total mΩ /Pi V | E total mΩ /Pi V | ASSUMED incremental USD / effort |
|---|---:|---:|---|
| Reduced baseline, audited | 56.367741 /4.744305 | 66.367741 /4.694305 | No change / no recovered margin |
| AWG16 trunk75 mm; AWG22 SEND15/RETURN35 mm | 54.547941 /4.753404 | 64.547941 /4.703404 | $1–5 / low–medium harness work |
| AWG18 trunk50 mm; AWG22 SEND15/RETURN35 mm | 54.756753 /4.752359 | 64.756753 /4.702359 | $0–3 / low; mechanical routing review |
| Lower module FET loss only | 48.767741 /4.782305 | 58.767741 /4.732305 | $2–8 / high driver/timing/SOA review |
| Qualified lower-loss Pi mate only | 44.492741 /4.803680 | 54.492741 /4.753680 | $3–15 / high mating/thermal qualification |
| Better J502 or parallel poles only | 52.127741 /4.765505 | 62.127741 /4.715505 | $2–10 / medium–high interface change |
| Remove/output-relocate sensing to input | 54.343953 /4.754423 | 64.343953 /4.704423 | $0–10 / high sensor/protection changes |
| Move shunt along same loop | 56.367741 /4.744305 | 66.367741 /4.694305 | $0–3 / layout effort, zero resistance saving |
| Change shunt to1 mΩ only | 55.359634 /4.749345 | 65.359634 /4.699345 | $0–2 / medium gain/noise/calibration work |
| Combined recommended set | 35.072941 /4.850779 | 45.072941 /4.800779 | $6–28 / high; excludes E protection assembly |

Parallel-pin comparison starts from original PR #6, rather than applying eight grounds twice: **CALCULATED original+new buck allowance D76.554538/E86.554538 mΩ**. ASSUMED incremental cost for four additional contacts, the second2×10 housing, fan-out wire and retained support: $2–8 plus medium harness/mechanical effort; exact price OPEN. Changing only four→eight grounds gives **D71.256694/E81.256694 mΩ**, gaining26.489 mV, still failing. Using both positive pins instead of one reduces inherited positive contact+branch+termination equivalent by **CALCULATED 20.985690 mΩ/104.928 mV** at the reduced geometry; both are already in the baseline. CALCULATED hypothetical one-positive-pin totals D77.353430/E87.353430 mΩ return to the audited two-pin totals D56.367741/E66.367741 mΩ when the second5 V branch is added. ASSUMED extra contact/wire allowance $1–4 with medium harness work; this is already included in the recommended two-pin construction. A single positive pin would also exceed the cited3 A test rating. The header has no third ordinary5 V pin; signal/3.3 V pins cannot become additional supply contacts.

Moving the shunt farther along the same SEND path saves **CALCULATED 0 mV**. Moving sensing to the9–24 V input can remove its output-loop drop, but measures input current rather than Pi current; converter loss and stored energy break direct output-power/current interpretation. An input shunt adds its own input drop and low-input regulation/thermal implications. A new sensor/gain/telemetry design is **OPEN**, so this is not equivalent to preserving output measurement.

The better-J502 row is a **qualification target ≤1 mΩ per complete hot pole**, achievable only with a selected approved connector or properly qualified parallel poles. The present two-pin J502 cannot gain parallel poles without an interface change. Do not stuff extra conductors into a clamp beyond its documented configuration. A retention upgrade alone is insufficient: inherited JST VH20 mΩ conditioned/contact ×ASSUMED1.3 would make a52 mΩ connector loop; **CALCULATED total D102.128/E112.128 mΩ**, much worse [S15](SOURCES.md).

The better-Pi-contact row requires **ASSUMED ≤20 mΩ per complete hot/conditioned mate** and applicable per-pin current derating. Existing Harwin conditioned30 mΩ ×1.3 does not meet that target. Samtec SSW is a research family, not a selected Pi mate: its4.7 A test energizes one pin per row; Pi2/4 share one row. Its Δ15 mΩ criterion is change in resistance, not an absolute maximum. Sample power-test resistance is not a guaranteed limit [S14](SOURCES.md). Obtain a supplier-approved mate/limit and qualify the actual board/harness; cost/availability remain **OPEN**.

### Remote sensing — resistance unchanged, regulation and fault behavior changed

An ideal **ASSUMED differential** sense at the Pi keeps physical resistance unchanged and makes the ideal static Pi minimum **CALCULATED 5.026143 V**. The raw buck voltage rises by `I×R`; only the feedback boundary changes. With the existing loop, that raw maximum screen becomes **CALCULATED 5.452934 V** at 5 A, already beyond fixed trip minimum5.293568 V. With the recommended reduced path it becomes **5.346460 V (D)** or **5.396460 V (E)**: both still violate the retained raw-detector normal window. Planning cost **ASSUMED $3–15** for sense conductors/interface/supervision, plus high control/protection qualification effort; voltage regulation is conditionally feasible but the unchanged protection architecture is incompatible.

LM61460 has a single-ended FB input referenced to AGND. Extending only the positive sense trace leaves return loss uncompensated. Simply referencing the divider bottom to remote GND can introduce ground-lift gain error; it is not a validated differential sense receiver. An amplifier/interface introduces offset, drift, common-mode and fault limits that are **OPEN**. [TI S01 §11.1](SOURCES.md) requires a short clean FB/AGND layout; its compensation discussion does not validate a harness in the loop.

**ASSUMED stability illustration:**0.6 µH harness and1 mF Pi-side capacitance give **CALCULATED LC resonance6.50 kHz**. Actual harness L/C/ESR, buck output C, sense filtering, converter compensation, control-to-output poles and phase/gain margins over9–24 V/0–5 A/startup are **OPEN**. Closing feedback around a cable and E's pass/current-limiter dynamics requires measured/simulated loop stability, load-step testing and a defined disconnected state. Routing and wire strain relief must preserve separate Kelvin sense; power-return voltage is not a clean reference.

**ASSUMED fault/load-release sensitivity:** retain full `I×R` correction while the loop responds and reuse the inherited **107.620 mV** release increment. This increment is an assumed sensitivity allowance, not a re-derived transient maximum. Recommended E gives **CALCULATED 5.504080 V** before any new limit acts, a negative counterexample to `<5.5 V`; D gives5.454080 V but still crosses its fixed trip. Open sense, unplugging the harness or opening either disconnect can drive the buck upward as it chases a missing remote voltage. Require local raw OVP, loss-of-sense detection, bounded fallback, default-off/anti-windup behavior and independent Pi-end protection/power. A failed-short buck cannot be controlled by feedback. Moving or raising a detector to accommodate remote sense spends fault headroom and requires a new protection proof. **DECISION recommendation: retain local regulation.**

### Raising the setpoint — millivolts purchased with trip margin

Inherited **CALCULATED conditional** trip5.293568–5.356563 V is fixed. D/E's revised normal20 µs release screen5.266252 V left17.316 mV after an **ASSUMED 10 mV** nuisance reserve. The assumed hot-divider stack raises its upper screen to5.278715 V, reducing that reserve to **CALCULATED 4.853 mV**. Threshold hot/reference/full-application qualification is still **OPEN**.

For this sensitivity, keep100 kΩ top resistor, adjust the bottom resistor conceptually, and retain the same **ASSUMED 107.620 mV** dynamic increment. No feedback values were edited. Costs **ASSUMED $0–1** component allowance but high review/validation effort because limits interact.

| ASSUMED nominal increase mV | CALCULATED hot source minimum V | CALCULATED hot normal upper V | CALCULATED nuisance reserve mV |
|---:|---:|---:|---:|
| 0.000 | 5.026143 | 5.278715 | +4.853 |
| 10.000 | 5.035994 | 5.288866 | -5.298 |
| 20.000 | 5.045845 | 5.299016 | -15.448 |
| 100.000 | 5.124649 | 5.380221 | -96.653 |
| 101.639 | 5.126264 | 5.381885 | -98.317 |

With the expanded hot screen, only about **CALCULATED +4.78 mV nominal** remains before the assumed nuisance reserve reaches zero; uncertainty can exhaust it. Raising a trip is outside the frozen limit. It would reduce strict fault headroom millivolt for millivolt at its high end. In the inherited5.2 V/retuned-trip example, maximum trip5.457360 V leaves only **CALCULATED 42.640 mV** before dynamic let-through, and its zero-delay fault screen was already negative. No unapproved setpoint/threshold change receives pass credit. **DECISION recommendation: keep nominal 5.098361 V and cut resistance.**

## Recommended fix set and both architecture results

**ASSUMED proposed acceptance set, not an implemented BOM:** both 5 V pins; all eight grounds; each polarity75 mm Belden8521 AWG16 trunk; AWG22 fan-outs15 mm per positive pin /35 mm per ground pin; matched positive branches; retained strain relief/indexing. Module hot FET pair≤6 mΩ at qualified loaded VGS≥10 V and Tj≤150°C; module PCB≤1 mΩ/leg; unsensed buck copper≤0.5 mΩ/leg; J502 complete hot pole≤3.12 mΩ; Pi complete hot/conditioned mate≤20 mΩ/contact with a qualified hot current rating; itemised joint/crimp/attachment loop≤2 mΩ. Keep2 mΩ shunt and original nominal regulator/OV trip. A hard-built75 mm harness requires bend-radius and fan-out mechanical review; the35 mm ground branches allow span across the full header, whereas a single15 mm ground star cannot reach all eight pins; these lengths are conductor lengths, not connector-to-connector straight-line distance.

| Proposed D element | Leg | 25°C min /typ /max mΩ | Hot min /typ /max mΩ | CALCULATED upper drop at 5 A mV |
|---|---|---:|---:|---:|
| Buck output copper | SEND | OPEN /OPEN /0.406 | OPEN /OPEN /0.500 | 2.500 |
| Buck return copper | RETURN | OPEN /OPEN /0.406 | OPEN /OPEN /0.500 | 2.500 |
| Module series FET pair | SEND | OPEN /2.400 /3.000 | OPEN /4.800 /6.000 | 30.000 |
| 2 mOhm current shunt | SEND | 1.980 /2.000 /2.020 | 1.976 /2.000 /2.024 | 10.119 |
| Module PCB traces / vias | SEND | OPEN /OPEN /0.812 | OPEN /OPEN /1.000 | 5.000 |
| J502 complete mated pole and clamp | SEND | OPEN /OPEN /2.400 | OPEN /OPEN /3.120 | 15.600 |
| Trunk wire AWG16 75 mm | SEND | 0.903 /1.004 /1.104 | 1.025 /1.139 /1.253 | 6.264 |
| Module PCB traces / vias | RETURN | OPEN /OPEN /0.812 | OPEN /OPEN /1.000 | 5.000 |
| J502 complete mated pole and clamp | RETURN | OPEN /OPEN /2.400 | OPEN /OPEN /3.120 | 15.600 |
| Trunk wire AWG16 75 mm | RETURN | 0.903 /1.004 /1.104 | 1.025 /1.139 /1.253 | 6.264 |
| AWG22 fan-out 15 mm, 2 parallel | SEND | 0.366 /0.406 /0.447 | 0.415 /0.461 /0.507 | 2.537 |
| Pi mated contacts, 2 parallel | SEND | OPEN /OPEN /7.692 | OPEN /OPEN /10.000 | 50.000 |
| Pi female crimps, 2 parallel | SEND | OPEN /OPEN /0.308 | OPEN /OPEN /0.400 | 2.000 |
| Pi male pin / solder attachment, 2 parallel | SEND | OPEN /OPEN /0.185 | OPEN /OPEN /0.240 | 1.200 |
| AWG22 fan-out 35 mm, 8 parallel | RETURN | 0.213 /0.237 /0.261 | 0.242 /0.269 /0.296 | 1.480 |
| Pi mated contacts, 8 parallel | RETURN | OPEN /OPEN /1.923 | OPEN /OPEN /2.500 | 12.500 |
| Pi female crimps, 8 parallel | RETURN | OPEN /OPEN /0.077 | OPEN /OPEN /0.100 | 0.500 |
| Pi male pin / solder attachment, 8 parallel | RETURN | OPEN /OPEN /0.046 | OPEN /OPEN /0.060 | 0.300 |
| Fan-out splice | SEND | OPEN /OPEN /0.385 | OPEN /OPEN /0.500 | 2.500 |
| Module solder joints | SEND | OPEN /OPEN /0.077 | OPEN /OPEN /0.100 | 0.500 |
| Fan-out splice | RETURN | OPEN /OPEN /0.385 | OPEN /OPEN /0.500 | 2.500 |
| Module solder joints | RETURN | OPEN /OPEN /0.077 | OPEN /OPEN /0.100 | 0.500 |

**CALCULATED recommended D hot subtotals:** SEND 25.644075 mΩ /128.220 mV; RETURN 9.428866 mΩ /47.144 mV at 5 A. 

All recommended cold upper entries are calculated allocation screens, not supplier maxima. The reproducible full-precision cold/hot min/typ/max record is in [PATH_CALCULATIONS.json](PATH_CALCULATIONS.json); as above, unknown minima/typical values remain `null`. Calculated D25°C upper loop **26.326195 mΩ**; its actual cold/hot sum is **OPEN** until qualified.

D places its final disconnect and protected absorber at the module; its existing series pair is replaced/requalified within the6 mΩ target, rather than adding an uncounted stage. If D needs a genuinely additional limiter/pass FET or series shunt, add its actual maximum just as for E. Moving an absorber to a shunt branch creates no normal5 A series drop; auxiliary consumption, leakage and thermal coupling still require bounds.

E retains the full module path and adds a Pi-entry disconnect/limiter/absorber. **ASSUMED additional hot ≤10 mΩ allocation:**

| Additional E element | Leg | 25°C min /typ /max mΩ | Hot min /typ /max mΩ | Label / condition |
|---|---|---:|---:|---|
| Series FET pair | SEND | OPEN /2.400 /3.000 | OPEN /4.800 /6.000 | CALCULATED/ASSUMED candidate, same drive caveats as module |
| New1 mΩ limiter shunt | SEND | 0.990 /1.000 /1.010 | 0.984 /1.000 /1.015681 | CALCULATED ±1%, ±75 ppm/K,100°C; limiter threshold design OPEN |
| Local SEND copper | SEND | OPEN /OPEN /0.406 | OPEN /OPEN /0.500 | ASSUMED85°C target |
| Local RETURN copper | RETURN | OPEN /OPEN /0.406 | OPEN /OPEN /0.500 | ASSUMED85°C target |
| Local SEND joints / cable-entry termination | SEND | OPEN /OPEN /0.385 | OPEN /OPEN /0.500 | ASSUMED1.3 hot factor target; include added entry contact |
| Local RETURN joints / cable-entry termination | RETURN | OPEN /OPEN /0.385 | OPEN /OPEN /0.500 | ASSUMED1.3 hot factor target; include added entry contact |
| Unallocated resistance reserve | whole loop | not a physical component | 0.984319 upper allowance | ASSUMED remainder to10 mΩ; no fabricated measured loss |

The10 mΩ cap includes all added force-terminal, PCB, contacts and sense/limiter losses. A connector or controller that requires more resistance must replace an allocation or trigger recomputation; it is not free. The active absorber is a shunt function. Feed auxiliary power independently from the9–24 V input via a qualified protected feed/return, as the architecture study proposes. **OPEN** auxiliary current, absorber leakage and input/buck headroom; no extra load is hidden in the5 A budget. If50 mA were taken through the entire E path, an **ASSUMED** example gives **CALCULATED another2.254 mV** loss plus extra source load; measure/model actual branch reference planes.

| Architecture / proposed reserve | CALCULATED total hot mΩ | CALCULATED Pi V | CALCULATED margin mV | Conditional result / qualified result |
|---|---:|---:|---:|---|
| D: static | 35.072941 | 4.850779 | +100.779 | MEETS within assumptions /OPEN |
| D: ASSUMED20 mV trough | 35.072941 | 4.830779 | +80.779 | MEETS within assumptions /OPEN |
| D: ASSUMED100 mV total excursion | 35.072941 | 4.750779 | +0.779 | MEETS within assumptions /OPEN |
| E: static | 45.072941 | 4.800779 | +50.779 | MEETS within assumptions /OPEN |
| E: ASSUMED20 mV trough | 45.072941 | 4.780779 | +30.779 | MEETS within assumptions /OPEN |
| E: ASSUMED100 mV total excursion | 45.072941 | 4.700779 | -49.221 | FAILS within assumptions /OPEN |

**CALCULATED** recommended hot dissipation: D0.877 W total path; E1.127 W, including0.250 W for the added10 mΩ cap. These are distributed losses, not one device's temperature. Each hot20 mΩ positive header contact at an equal2.5 A dissipates0.125 W; inherited39 mΩ would dissipate0.244 W. Thermal rise, derating and neighbour heating are **OPEN** and require qualification.

At **ASSUMED VGS6 V**, changing the module pair allocation6→8.8 mΩ adds **CALCULATED 14 mV** loss: D static4.836779 V; E4.786779 V, or4.766779 V after the20 mV trough. If both module and E's local pair need8.8 mΩ, E becomes **CALCULATED 50.672941 mΩ/4.752779 V after20 mV**, exceeding E's50 mΩ target with only2.779 mV remaining. Below6 V the applicable bound is **OPEN**, rather than extrapolated from gate threshold.

Keeping inherited39 mΩ Pi mating screens with all other recommended changes gives **CALCULATED D46.947941 mΩ/4.791404 V**, but **E56.947941 mΩ/4.741404 V: fails static**. Thus the low-loss Pi mate is an essential part of the E fix set, not an optional cosmetic connector change.

The100 mV total-negative-excursion case leaves D only **CALCULATED +0.779 mV** and makes E **−49.221 mV**, failing. If the owner chooses100 mV as a required operating reserve, do not approve this E set. Reduce its total below the **CALCULATED 35.228651 mΩ** ceiling, or produce a tighter proven regulation/transient bound. Qualified targets≤35 mΩ for E would leave only1.143 mV reserve; a practical proposal≤30 mΩ would leave26.143 mV but needs a new aggressive connector/series-stage design. Neither target is achieved here.

The DC result does not close fault containment. D's inherited coupled-harness example reached **CALCULATED 5.542140 V**, despite1 mF at the Pi. For an illustrative0.6 µH/1 mF single LC pair, critical series damping is **CALCULATED 49.0 mΩ**; lowering resistance below that can increase ringing. The actual coupled network, capacitor ESR and active limits differ and remain **OPEN**. Do not retain loss as an improvised protection mechanism. E's independent local absorber/supply/timing and both architectures' source/energy/SOA bounds still need the separate electrical review.

## Per-pin current and connector rating

All currents below are **CALCULATED with ASSUMED equal, intact branch sharing** at total5 A. Three amperes is the [Harwin S08/S09](SOURCES.md) contact test rating, not the actual Pi male-header/hot-pair rating. Applicability and hot derating are **OPEN**, so the complete connector rating verdict remains **OPEN**.

| Physical Pi pin | Function | Original PR #6 A | Reduced/recommended A | Cited female contact rating A | Reduced-case headroom A | Actual hot Pi mate rating |
|---|---|---:|---:|---:|---:|---|
| 2 | 5 V | 2.500 | 2.500 | 3.000 | 0.500 | OPEN |
| 4 | 5 V | 2.500 | 2.500 | 3.000 | 0.500 | OPEN |
| 6 | GND | 1.250 | 0.625 | 3.000 | 2.375 | OPEN |
| 9 | GND | 1.250 | 0.625 | 3.000 | 2.375 | OPEN |
| 14 | GND | 1.250 | 0.625 | 3.000 | 2.375 | OPEN |
| 20 | GND | 1.250 | 0.625 | 3.000 | 2.375 | OPEN |
| 25 | GND | unconnected | 0.625 | 3.000 | 2.375 | OPEN |
| 30 | GND | unconnected | 0.625 | 3.000 | 2.375 | OPEN |
| 34 | GND | unconnected | 0.625 | 3.000 | 2.375 | OPEN |
| 39 | GND | unconnected | 0.625 | 3.000 | 2.375 | OPEN |

J502 has one 5 A SEND contact and one 5 A RETURN contact, versus its cited12 A nominal rating: **CALCULATED 41.7% utilization** under comparable test conditions. Its actual assembled60°C derating/temperature rise is **OPEN**, particularly at clamp/fan-out points. Wire catalogue free-air ratings are not harness bundle ratings; the AWG22 positive branches also carry2.5 A each, not5 A each.

Current sharing is not proved by a maximum contact resistance. For two positive branches, `I_lowR=5 R_high/(R_low+R_high)`. To keep every pin≤3 A requires **CALCULATED `R_high/R_low ≤1.5`**, including contact, crimp, fan-out and Pi spreading. An **ASSUMED ratio2** gives **CALCULATED 3.333 A** in the lower-resistance pin, above3 A. A single open positive contact forces5 A through the survivor and exceeds that rating. If the actual hot male mate is rated only2 A, two pins cannot carry5 A under the frozen interface at all.

For eight grounds, one low-resistance branch against seven equal high branches gives `I=5k/(k+7)`; a3 A per-pin limit would require **CALCULATED k≤10.5**. That illustrative inequality is not a plane-sharing proof. Measure every active pin current and temperature across tolerance/conditioning and reject a harness with excessive asymmetry. Single-positive-contact fault tolerance is **OPEN**; protection must not assume the surviving contact is rated5 A. Adding ballast just to force sharing can defeat the voltage budget: contact range0…39 mΩ would require **CALCULATED ≥78 mΩ per positive branch** for ratio≤1.5, adding195 mV equivalent loss. Zero here is an extreme mathematical sensitivity, not an asserted contact minimum.

## DECISIONS FOR THE OWNER

These are recommendations for the next engineering decision, not approvals or implementation changes.

| Decision | 2–3 options and consequence | Recommended option / reason |
|---|---|---|
| Final protection location | **D:** less path loss/board effort, coupled-harness fault peak OPEN. **E:** independent GPIO-entry containment, extra≤10 mΩ cap/auxiliary/mechanical work. | **E with the combined resistance targets**, matching the prior architecture recommendation; its local protection addresses the harness endpoint. DC feasibility does not waive fault blockers. |
| GPIO contact system | **Keep current Harwin screen:** E misses4.75 V after other fixes. **Qualify lower-loss full mate:** target hot≤20 mΩ/contact and actual hot pin rating. **Change Pi power interface:** would require changing frozen D-30/user requirements. | **Qualify the full Pi mate first.** It is the largest loss and the central rating uncertainty. Obtain supplier approval and actual board-revision evidence; stop if the two5 V pins cannot carry5 A. |
| Harness construction | **Original150/50 mm AWG18/22, four grounds:** fails. **75/25 mm AWG18/22, eight grounds:** inherited reduced screen, little spare margin. **75 mm AWG16 trunk with15/35 mm positive/ground AWG22 branches, eight grounds:** about 9.099 mV better than reduced. | **Short AWG16 trunk with AWG22 fan-out and all grounds.** Retain both positive pins, matched branches, keyed/indexed support and strain relief; qualify crimps/torque/thermal rise. |
| Module and E FET pair | **Retain old13.6 mΩ module screen:** too much combined loss. **Target≤6 mΩ pair at≥10 V loaded gate:** highest benefit but Qg/timing/SOA work. **Use6 V characterized drive:** modeled8.8 mΩ pair, greatly reduces spare E margin. | **≤6 mΩ hot pair with guaranteed loaded gate drive.** Candidate BSC014N06NS is research only; require hot RDS/timing/hold-up/SOA evidence before selection. |
| Output current sensing | **Keep2 mΩ:**10.119 mV hot drop, retained signal/telemetry. **1 mΩ:**saves 5.041 mV, halves signal and needs recalibration. **Remove or move toinput:**saves 10.119 mV output loss but changes measured quantity/protection. | **Keep2 mΩ.** The combined set fits while preserving useful measurement; component relocation within the loop offers no saving. |
| Regulation strategy | **Local unchanged:**combined resistance fix, preserves current interface. **Remote sense:**physical loss unchanged; loop/open-sense/raw-trip redesign. **Higher setpoint:**+10 mV already exceeds modeled hot nuisance reserve. | **Local unchanged nominal and trip.** Fix loss without spending an already narrow protection window; select feedback-resistor TCR and qualify full operating bounds. |
| Dynamic operating reserve | **Static4.75 V only:**does not establish ripple trough. **Qualify20 mV total trough for this screen:**D/E conditional floors4.831/4.781 V. **Require100 mV total excursion:**E fails; D has only0.779 mV. | **Treat20 mV as a provisional test target, not a changed requirement.** Obtain the real Pi load/ripple/response envelope before release; if100 mV is needed, reopen the budget and lower E resistance. |
| J502 resistance evidence | **Assume catalogue readings:**no worst-case proof. **Qualify selected pair≤3.12 mΩ/pole:**retains current interface but demanding hot test. **Select≤1 mΩ/pole interface:**saves21.2 mV with connector/board changes. | **Qualify current pair first, retain≤1 mΩ alternative if it misses.** Use complete non-overlapping four-wire reference planes, permitted terminations and conditioning. |

## Completion criteria and remaining evidence

The requested analysis and comparisons are complete. Electrical qualification remains **BLOCKED**. Required evidence: regulator operating minimum/maximum and actual resistor TCR; loaded FET VGS/hot RDS and source-independent timing/SOA; complete conditioned/hot J502/Pi/crimp/attachment limits; actual Pi male part/rating/plane sharing; built copper/feedback boundaries; exact E stage/auxiliary loss; realistic ripple/load envelope and uncertainty. All are **OPEN**, not filled with vendor typicals.

Use a current-limited supply and dummy/electronic load first. Apply the repository's staged bring-up sequence: continuity/no-load, progressively loaded/hot resistance and per-pin current measurements, ripple/load steps, then fault/independent-protection testing; integrate the Pi only after these pass. This is a qualification plan, not performed testing. No expensive SBC was energized and no procurement/fabrication action was taken.

Reproduce arithmetic with `python3 docs/evidence/r2/path_budget/calculate_path_budget.py --check`. [VALIDATION.md](VALIDATION.md) records document/link/scope checks and the independent arithmetic review. No ERC/DRC was invoked because the user explicitly restricted the task to analysis and forbade native CAD access. The manager-status fields are recorded in that permitted directory rather than editing files outside scope.

**VERDICT: MEETS 4.75 V (neither) under the frozen qualified worst-case criterion. Neither architecture is qualified; both meet the conditional static/20 mV screen. Recommended fix set: both 5 V/all 8 GND pins, qualified hot≤20 mΩ Pi mate, 75 mm AWG16 trunk/15 mm positive /35 mm ground AWG22 fan-outs, ≤6 mΩ hot module FET pair, retain2 mΩ shunt/local setpoint, qualified copper/J502/joint targets, and E added stage≤10 mΩ. CALCULATED conditional result: both D and E meet; actual worst-case remains OPEN.**
