# Gate 3 — Sheet 03 fault-containment architecture options

**STATUS: BLOCKED for electrical release; architecture comparison complete; owner selection and component qualification pending. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Root is the single decision/document owner. Read-only source research was delegated; it did not touch CAD or own architecture decisions. This branch starts at `0677fea0a32fc87b740949d589abe1588e55934c` (`origin/feat/sheet03-gate2c`). Native KiCad files are not opened, saved or checked by this task; another owner is editing them. “Gate 3” here means this requested architecture analysis, not authorization to skip R2 and start the repository's R3 PCB gate.

## Frozen requirements and evidence discipline

REQUIREMENT: input 9–24 V; GPIO-powered Pi (D-30); `V_Pi,peak < 5.5 V`, including let-through; `V_Pi >= 4.75 V at 5 A`; `V_normal,max + margin < V_trip,min`; `V_trip,max + dV_let-through < 5.5 V`. No USB-C OVP credit, rail-setpoint increase, relaxed voltage ceiling or unapproved remote sense is used.

OPEN: the proposed robot 24 V rail and 48 V→24 V converter have no selected model. Their tolerance/trim/startup, current-limit response, output store, fault ceiling/time, return paths and isolation need an interface contract. Normal 24 V is a maximum requirement, not permission for a nominal 24 V converter to exceed it. Primary pass-through containment remains allocated upstream; this analysis does not invent a 48 V maximum fault rating for V1A.

Labels throughout: **DATASHEET** = specification at its stated conditions; **CALCULATED ** = arithmetic within listed inputs; **ASSUMED** = proposed allocation/unqualified premise; **OPEN** = missing applicable bound. Every finite architecture voltage below is a conditional screen, not the application worst case. Actual worst-case Pi peaks remain **OPEN** and are `null` in [the calculation record](gate3/OPTIONS_CALCULATIONS.json). A negative screen is **BLOCKING**, never rounded into PASS. A positive screen only states what a proposed qualified implementation would have to achieve.

Baseline evidence: [Gate2c closure](GATE2C_REVIEW_CLOSURE.md), [architecture history](SHEET03_ARCHITECTURE_DECISION.md), [calculations](GATE2_CALCULATIONS.md), [historical JSON](CALCULATIONS.json), [decision index](../../../context/06_DECISION_LOG.md). Historical evidence is preserved.

## Common comparison basis

CALCULATED, inherited conditional screens: raw static 5.038271–5.158632 V; normal release maximum 5.261614 V using ASSUMED 20 µs excess-current interval; trip 5.293568–5.356563 V with unqualified hysteresis/reference/passive allocations; normal margin after ASSUMED 10 mV reserve **+21.954 mV**. These are not complete tolerance guarantees. At a 30 µs normal-response assumption the same nuisance margin is **−2.979 mV, BLOCKING**.

The reduced hot-loop screen is 55.367741 mΩ: Pi 4.761433 V, only **+11.433 mV**. The maximum static loop budget from the inherited raw minimum is `(5.038271−4.75)/5 = 57.654280 mΩ`. Just **2.286540 mΩ** additional series resistance exhausts its spare margin. All added fuses, shunts, FETs, contacts and returns must fit the total budget. Actual hot VGS/RDS, harness and normal voltage limits remain OPEN. The earlier 100 mV dynamic reserve is an ASSUMED target; it is not frozen or already achieved.

The original source sensitivity 24 V / 0.1 µH floor / 0.4 µs crowbar action gives CALCULATED 502.457 A and 6.271942 V, **−771.942 mV**: evidence that the old assumptions cannot qualify the existing architecture. It is not numerically transferred to changed circuits. Charged local input C, initial L current, replenishment, raw/protected capacitors, harness inductance and any backfeed must each have a destination.

Comparisons include no-load, 5 A, startup/prebias, ARM inrush, load release, brownout and a persistent failed-short buck. Test measurement uncertainty must fit the positive reserve; no Pi is used as the first fault load.

## Comparison on the same criteria

All voltage/energy numbers here are **CALCULATED within ASSUMED target boxes**, never confirmed application maxima. Actual worst-case Pi peak is **OPEN/BLOCKING for all five**. “Removes” means only after the stated bounds/components/tests are qualified.

| Option | Pi peak / normal-margin evidence | Energy/current destination | Timing/supply | Gate2c disposition / decision |
| --- | --- | --- | --- | --- |
| A bounded-source crowbar | On-interval module 5.461834 V (+38.166 mV), Pi/harness after isolation OPEN; 2 µs action 5.504414 V BLOCKING. Recomputed normal 5.266252 V/+17.316 mV false-trip reserve; inherited Pi 5 A 4.761433 V/+11.433 mV | Qualified source ≤ 150 µC, Cin ≤ 20 µF, Ldiff floor through 60 A ->59.135 A; all-store 97.487 mJ to rated crowbar/ballast/dump. Hot acceptance OPEN | Application min/max OPEN; targets 20 µs source off, 1 µs crowbar, 2 µs series; direct rail/hold-up needed | Can address B01; leaves harness, complete timing/supply/SOA and hot-terminal proof. Useful ingredient, heavy qualification |
| B fuse-blowing crowbar | Pi peak OPEN; example 7 A fuse reduces Pi 5 A to 4.716433 V (−33.567 mV BLOCKING); same tight trip window | Fuse/SCR/ballast/arc/dump; 11 A²s example requires 0.363 J ballast plus bypass pulses. Available current and 24 VDC clearing max OPEN | SCR typical 2 µs not maximum; full clamp+prearc+arc max OPEN; indefinite clearing incompatible with finite hold-up | Present eFuse cannot assure blowing a normally rated fuse; no B01/B02/B03 closure. Reject as primary direction |
| C two-stage | Unprotected 6.12 V DC (−620 mV BLOCKING), LC sensitivity 7.081 V; independent protection still needed. Same output/harness margins conditional | Intermediate local 1.142 mJ, example all-mid store 6.086 mJ, plus both inductors/source; final rated dump/absorber still required | Both stage control/isolation and final action max OPEN; 6 V cannot feed 7.6 V LDO | Reduces excitation, leaves timing/supply/terminal/harness blockers; illustrative 87.4% /3.675 W loss. No standalone containment |
| D module disconnect+absorber | Module 5.460 V/+40 mV; full Pi peak OPEN. Two-cap harness counterexample 5.542140 V (−42.140 mV BLOCKING), even Pi C 1 mF. Output resistance budget unchanged only if no extra series loss | Protected active absorber + distinct raw dump; source/store contract mandatory; 116.847 mJ source/raw/module subtotal excludes separate Pi C; total store OPEN; 0.2 J hot dump target OPEN | Targets 0.5 µs useful clamp/2 µs isolation; actual min/max OPEN; driver/reference hold-up and clamp-active shutdown required | Avoids bulk-discharge ballast premise; leaves coupled harness, current, timing and hot SOA. **Runner-up only with full harness contract** |
| E independent Pi-end | Proposed full local clamp 5.420 V/+80 mV; series-only fallback 5.476563 V/+23.437 mV; 220 µF or 60 A overshoot are BLOCKING. Proposed 50 mΩ total gives Pi 5 A 4.788271 V/+38.271 mV; nuisance reserve 17.316 mV detector/23.748 mV clamp | Protected-side 10 A transient ceiling and local C/absorber; 0.771 mJ received-energy subcase. Separate input-side cable/bulk/source/dump envelope remains OPEN; 0.2 J hot target is not a rating | Local full timing min/max OPEN; 5 µs isolation and ≤ 20 mV total clamp overshoot targets; separate qualified auxiliary power/default-off/hold-up | Addresses protected-plane/harness problem if qualified. Highest hardware/wiring effort, finite design contract. **Recommended direction; approval required** |

| Option | ASSUMED incremental placements / USD planning budget | Normal efficiency/thermal cost and recurring cost |
| --- | --- | --- |
| A |25–45 /$15–40 including source/dump/common fixes; larger qualified magnetics | Input shunt/pass loss, auxiliary/dump thermal qualification; minimal input C can impair input stability |
| B |12–25 plus mechanics /$8–35 excluding common fixes |7 A cold-fuse example 0.225 W/output drop; hot/holder worse; every crowbar firing can consume a fuse |
| C |15–25 /$8–20 for conversion only; protection extra | Illustrative two-stage 3.675 W vs single 1.772 W, +1.903 W; thermal coupling and stage interaction |
| D |20–35 /$15–35 plus common supply fixes, offset by removed crowbar parts | Low series loss required; short hot absorber/dump pulses, protected C startup cost |
| E |30–55 /$20–50 plus PCB/auxiliary feed; source changes shared | Additional hot loop resistance/inrush, driver consumption/heat; no sacrificial consumable expected |

Budgets are **ASSUMED engineering allowances**, not supplier quotes/BOMs or confirmed stock. Counts are estimates of placed functions/passives, not the final netlist; shared source/supply components must not be counted twice. Exact supplier pricing, availability and BOM cost remain OPEN; no purchase or quotation was requested.

## A — keep crowbar, explicitly bound the source

**Topology proposal:** eFuse → independent current-limiter/pass FET → minimal qualified buck-local input C → failed buck switch/L201 → existing series disconnect/crowbar. Retain independent detector power. Add a rated upstream inductive dump path; limiting incoming current does not remove that obligation.

### Source, current, energy and voltage

DATASHEET: [LM61460 Rev D §9.2.2.5](https://www.ti.com/lit/ds/symlink/lm61460.pdf) requires at least 10 µF ceramic input capacitance and adjacent 100 nF bypass at each VIN/PGND pair. Zero/negligible input C is not an acceptable proposal. ASSUMED nominal 10.2 µF ×1.2×1.15 gives 14.076 µF upper screen. Even its initial 24 V store alone permits CALCULATED **39.069 A** with an ASSUMED constant 5.44 µH floor and 6 A initial current—well beyond the existing inductor's **DATASHEET typical** 14 A saturation point. That low-current floor cannot be extrapolated through the pulse.

ASSUMED qualification targets, not selected parts:

| Target | Allocation and required evidence |
| --- | --- |
| Effective local input C | 10–20 µF including every bypass; guarantee minimum for switching/stability and maximum for energy over voltage/temperature/life |
| Source charge after fault until physical isolation | `Q_source,+ <=150 µC`, including limiter response overshoot; isolation ≤ 20 µs from fault onset. A settled 5 A limit does not prove this integral |
| L201 differential inductance | 5.44–8.16 µH over 0–60 A and full temperature; replace/resize only after approval. No existing MPN is claimed to meet it |
| Initial current / rail | ≤ 6.1 A (proposed; normal ripple/transient maximum must be qualified); input ≤ 24 V; raw node nonnegative throughout commutation |
| Raw bank | effective C ≥ 2.4064 mF; bulk ≤ 5.4144 mF plus ceramic ≤ 182.16 µF; ESR ≤ 4 mΩ—each still needs qualification |
| Action | effective crowbar conductance ≤ 1 µs after the specified detector overdrive; series current isolation ≤ 2 µs; local ringing ≤ 20 mV |
| Downstream C / backfeed | ≤ 220 µF; no independent downstream source for this pulse calculation |

CALCULATED within those targets:

`E_available,L <= 0.5 Cin,max Vin² + Vin Q_source,+ + 0.5 Ldiff,max I0²`

`= 5.760 mJ + 3.600 mJ + 0.151817 mJ = 9.511817 mJ`.

For positive current, passive nonnegative raw voltage and no other energy source, `W_L(I)=integral(i Ldiff(i) di) >=0.5 Ldiff,min I²`; hence **I_L <=59.135 A**, rounded conservatively to the ASSUMED 60 A design envelope. This needs a guaranteed Ldiff floor over the entire trajectory, not an Isat headline. A reverse/precharged/negative-node event needs its own energy bound.

After the inherited maximum trip, include 42.691 mV raw overdrive before the comparator delay condition, `60 A×1 µs/Craw,min`, incremental ESR from `dI/dt<=24/Ldiff,min`, and 20 mV ringing. CALCULATED on-interval raw/module-node upper screen **5.461834 V**, margin **+38.166 mV**. Threshold crossing already includes pre-crossing ESR; only its further rise is added. At **2 µs** crowbar action the same conservative bound becomes **5.504414 V, −4.414 mV: BLOCKING**. Complete application timing and V_Pi, max remain OPEN.

Once fully conducting, the ASSUMED maximum 40.095 mΩ crowbar path gives `60×R =2.4057 V`, below the ceiling. That steady load-line does not establish its turn-on transient. Raw bulk helps during the on interval; it is not credited as Pi capacitance after series isolation. The harness still needs the D/E energy check.

CALCULATED total-store ceiling at an assumed 5.5 V output ceiling is **97.487287 mJ**, including bulk/ceramics, protected C, local input store, source charge and initial L. Energy can split between crowbar, dump clamp, pass-FET and wiring; every trajectory must close. Conservatively dumping all of it through ballast gives **2.999147 A²s** at minimum ballast resistance. Independent ±corner sharing gives at most **25.5639% /24.9215 mJ per resistor**, not exactly one quarter.

**Proposed rated destinations:** keep CSD18540Q5B plus qualified ballast only if their hot waveforms are accepted, and add an upstream active dump FET/clamp with explicit ≥ 0.2 J hot-event qualification. Existing Vishay WFMB2512 maximum terminal temperature is **DATASHEET 95°C**; ASSUMED terminal target ≤ 85°C and ≥ 50 mJ applicable hot single-pulse capacity per element leave a proposed reserve. Neither temperature nor that pulse capacity is confirmed. At inherited ASSUMED 125°C terminals the old network remains BLOCKING. MOSFET energy/I²t is not an invented fuse rating: apply actual VDS–ID–time against hot SOA, junction and package limits.

### Limiter candidate, timing and supplies

[ADI LTC4218 Rev H](https://www.analog.com/media/en/technical-documentation/data-sheets/4218fh.pdf) is a research candidate, not selected. DATASHEET operating range 2.9–26.5 V; sense threshold 14.25–15.75 mV under its conditions. ASSUMED 3 mΩ±1% gives CALCULATED settled **4.702970–5.303030 A**. Its 1 µs sense-to-gate maximum uses a 60 mV step, VFB=0 and 1.5 nF gate test; actual gate/current removal and source-charge bound are OPEN. Timer shutdown uses a weak gate pull-down; timer expiry is not physical isolation. Its 26.5 V ceiling also fails to cover the inherited abnormal OVP upper screen 28.289 V; a higher-rated stage or explicit input clamp is needed for that separate contract. No datasheet current-limit maximum is relabeled as an instantaneous current ceiling.

The 20 µs fault-onset deadline requires an independent source-current/fault trigger; the present voltage detector may not cross promptly with large Craw. Timing chain minimum/maximum: fault→limiter sensing/response→source current isolation is **OPEN/OPEN**; OV onset→divider/overdrive→comparator→qualification/latch→crowbar driver→effective clamp and parallel series turn-off are **OPEN/OPEN**. The proposed 20/1/2 µs bounds above are qualification targets. Retained stage specifications and supply test conditions are tabulated later; partial sums are not total delays.

Supply validity: keep auxiliaries before the eFuse; add direct driver-rail qualification, fail-off gate paths and hold-up through source removal/inductive decay. The current PG floor 6.175 V does not qualify the old timing. At falling input UVLO, driver headroom may already be lost. Do not release SHDN/crowbar merely because CTRL_ENABLE collapses while stored energy remains.

### Normal margins, complexity, blockers and bench closure

Upstream limiting adds input loss; ASSUMED 3 mΩ shunt alone costs about 29.7 mW at 3.147 A /9 V, plus pass-FET and wiring loss. Steady load, maximum low-input startup/inrush and limiter/buck input-filter stability must fit its minimum current and dropout. The output static harness margin stays at inherited conditional +11.433 mV only if the path/regulation is preserved. Recomputing normal release with ASSUMED 6.1 A, 20 µs, 8.16 µH, 2.4064 mF, 4 mΩ ESR and 20 mV ripple gives CALCULATED normal 5.266252 V and nuisance reserve+17.316 mV after 10 mV. At 30 µs it becomes 5.291601 V/−8.033 mV: BLOCKING. D/E adopting this source/normal box use these more conservative values.

ASSUMED incremental planning allowance: 12–20 source-limit parts, larger qualified inductor, dump clamp and common supply fixes; roughly 25–45 placements total and **US$15–40**. These are engineering budgets, not quotes, guaranteed availability or a selected BOM. Actual cost/size/thermal design OPEN.

Would remove B01 only after the source integral, saturation floor and dump destination are qualified. B02/B03/M01/M03/M04/M05/M06/m03 remain or require the common fixes below; resistor-terminal conflict is removed only by rated temperature/construction, not new arithmetic. Bench: max-C/min-L hot/cold short injection; measure limiter integral and true source isolation, Pi peak, gate/driver/reference rails, raw-node undershoot and dump VDS; normal 9 V startup/inrush, input-loop stability, 5 A→0 release, resistor terminals, FET hot SOA trajectory and repeated pulses. Supplier maxima remain necessary beyond a successful prototype.

## B — fuse-blowing crowbar

**Topology proposal:** real fuse in a coordinated fault-current path, crowbar on its load side, independent detector, and rated inductive clamp. There are three distinct placements: fuse before local input C leaves its discharge bypassing the fuse; fuse after local input C includes that discharge but inserts impedance into the buck switching loop; output fuse with downstream crowbar includes source-fed output current but carries 5 A normally. Protected capacitors discharge through the crowbar without necessarily traversing the fuse. Fuse current I²t and total crowbar current I²t are therefore not automatically equal.

### Supplier sizing and hard conflicts

DATASHEET: [Littelfuse Fuseology](https://www.littelfuse.com/assetdocs/fuseology-selection-guide?assetguid=fa4aa360-f6c4-4eec-88a6-3d7ec3fe57d5) recommends usual 25% operating-current derating, with additional temperature/pulse considerations. ASSUMED efficiency 90% at inherited 25.491803 W means CALCULATED 3.147136 A at 9 V; preliminary input rating ≥ 4.196182 A, hence a 5 A screen. At the output, 5 A/0.75 requires ≥ 6.666667 A, hence a 7 A screen. Neither is a selected qualified fuse.

| Real supplier candidate / exact revision | DATASHEET pulse / interruption evidence | What is still missing |
| --- | --- | --- |
| [Littelfuse 451/453, GD 18-Sep-2023](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1) | 5 A nominal melting 5.566 A²s/cold R12.5 mΩ; 7 A nominal melting 10.32 A²s/cold R9 mΩ. Breaking 300 A at 32 VDC for ≤ 5 A; 400 A for ≥ 6.3 A | Nominal melting is not max total clearing. The inherited 502 A sensitivity exceeds these interrupt ratings; it cannot be approved without a new bounded source |
| [Eaton FWP-A 14F, 720025 Oct2025](https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/bussmann-iec-high-speed-semi-conductors-fuses/bussmann-iec-ferrule-high-speed-fuses/eaton-bussmann-series-fwp-ferrule-high-speed-fuses-datasheet-720025-en-gb.pdf) | FWP-5A14F prearc 2 A²s, clearing 11 A²s at 700 V; FWP-10A14F prearc 4/clearing 22 A²s. [10 A product](https://www.eaton.com/us/en-us/skuPage.FWP-10A14F.html) lists 50 kA at 700 VDC | Official clearing tables/catalog context differs on AC applicability; no guaranteed total-clearing 24 VDC maximum for the actual capacitive/current-limited pulse. Use 11 A²s only as an ASSUMED coordination example, not transferable rating |
| [Mersen FD27GB66V5T, July2026](https://www.mersen.com/sites/default/files/medias/PIM/files/DS-Semiconductor-Protection-Cylindrical-Fuses-Protistor-Size-27x60-gR-GRB-660VDC-Mersen-EN.pdf) | 5 A/660 VDC, 50 kA at rated DC/L/R15 ms; prearc curve has±8% current band. Dissipation 1.1 W atIn; 27×60 mm/80 g | Genuine DC curve, but no total-clearing I²t in this document. Supplier 24 VDC arc duration/clearing coordination remains OPEN; also a substantial size/drop cost |

The present eFuse's CALCULATED settled maximum ≈4.819820 A is below the 5 A input fuse rating and far below the 7 A output fuse rating. It is an upper screen, not a minimum current that guarantees melting. Local capacitors can produce a spike, but no guaranteed pulse integral follows from their capacitance alone. Current limiting/hiccup may starve the fuse before it clears. Reducing an input fuse to 3.15 A violates the operating-current derating screen at 9 V. **Guaranteed fuse clearing with this source is OPEN/BLOCKING.** B only becomes independent of the eFuse if an available-current minimum and applicable clearing maximum are contractually established.

CALCULATED extra output-fuse drop using the 7 A candidate's nominal cold 9 mΩ: **45 mV/0.225 W**. Inherited Pi minimum falls to **4.716433 V, −33.567 mV: BLOCKING** before hot resistance/holder loss. This fuse requires a new lower-resistance harness/path allocation. The Mersen5 A output candidate's1.1 W at 5 A corresponds to approximately 220 mV loss at its listed conditions; it also needs derating and is not a low-loss solution.

### Rated destinations and pulse calculation

DATASHEET: [Littelfuse Sxx20x/Sxx25x, BO10-Dec-2020](https://www.littelfuse.com/assetdocs/switching-thyristor-sxx20x-sxx25x-datasheet?assetguid=7CCAA6CD-4318-4C16-B5CE-306D14D88055), 25 A SCR: single half-cycle 300 A/50 Hz or 350 A/60 Hz at initial 25°C; fusing 510 A²s at 8.3 ms; allowable on-current slew 150 A/µs at 125°C. Turn-on 2 µs is **typical**, at specified trigger/load conditions, not a maximum. Gate current/spreading, holding and recovery still constrain the pulse. No SCR MPN is selected. [ST TYN612 Rev11](https://www.st.com/resource/en/datasheet/tyn612.pdf) offers a smaller cold 98 A²s/145 A 8.3 ms example; its ratings likewise do not guarantee a hot DC-capacitor pulse.

ASSUMED example: qualified maximum fuse-current integral 11 A²s; equal 33 mΩ ballast (two series pairs in parallel); crowbar receives the same fuse-fed current. CALCULATED ballast 0.363 J /0.09075 J per equal element, plus protected-capacitor discharge and every current bypassing the fuse. Cold SCR ratio510/11=46.364 is only cross-condition sizing arithmetic. Peak/slew/temperature/duration limits must also pass, and a larger circuit integral changes this result. At constant ASSUMED 100 A the clearing-integral screen lasts 1.1 ms; this is not a datasheet clearing time.

A possible ballast construction to investigate is [Vishay LTO50, 50050 08-Dec-2021](https://www.vishay.com/docs/50050/lto50.pdf): TO-220, resistance down to 10 mΩ, 50 W at case 25°C, working-temperature ceiling 150°C. Its p3 supplier pulse curve gives an ASSUMED conservative graphical reading around 1.3 J/1 ms at the stated cold conditions. The [pulse note 50060](https://www.vishay.com/docs/50060/pulsecapabilities.pdf) describes single tests at 25°C. The 0.09075 J nominal example fits that cold screen; actual available low-ohm value, ±5/10% tolerance, guaranteed hot TCR, parasitic inductance, pulse rise, repetition and mounting remain OPEN. This is a proposed replacement construction, not permission to transfer the cold curve to 125°C or to alter the existing ballast.

Energy destination: supplier-coordinated SCR/pulse ballast, fuse arc chamber and an independently rated inductive dump. Each capacitor-bypass pulse is included separately. Use `E_R=R integral(I_R²dt)` and `E_SCR=integral(V_AK I_A dt)`; SCR surge I²t is not resistor energy, and fuse prearc is not total arc clearing. Until the source and maximum clearing time/integral are bounded, **fault energy/current upper bounds and V_Pi, max are OPEN**. The initial OV interval requires the same fast independent clamp argument as A/D/E; a fuse cannot undo an earlier Pi overshoot.

### Timing, supply, normal behavior and remaining blockers

Complete min/max chain: OV→detector/logic→SCR trigger/spreading→effective crowbar→fuse prearc→arc extinction→store/inductor decay is **OPEN/OPEN**. The SCR's typical 2 µs cannot replace the historical assumed 0.3 µs crowbar action. Retaining a fast MOSFET clamp while a slower SCR/fuse takes over adds a transfer/SOA problem. Supplies must remain qualified through that transfer; an SCR self-holds without gate power only while current exceeds its holding requirement. Brownout can unlatch it and later expose a still-failed buck, so retrigger/arm/reset policy is necessary.

Normal startup/repetitive inrush must survive the fuse pulse derating; nuisance crowbar firing now becomes a destructive consumable event. Trip tolerance/normal voltage margin stays OPEN; fuse loss worsens the 5 A margin as calculated. Terminal limits are fixed only through applicable construction/thermal evidence. Removes dependence on electronic latch-off only after independent clearing qualification; leaves B01/B02/B03/M01/M03/M04 and false-fire/reset blockers, with M05 replaced by a larger coordinated pulse/arc problem.

ASSUMED incremental budget: fuse/holder, SCR/trigger, pulse ballast and dump/snubber, roughly 12–25 placements plus mechanics; **US$8–35**, excluding common supply fixes and replacement fuses. Exact price OPEN. Bench: hot 5 A fuse/holder drop and temperature; 9/24 V repeated startup/inrush; minimum and maximum available fault-current short tests; Pi peak before fuse clearing; full DC arc extinction/no restrike; hot SCR turn-on/slew and transfer; gate-power loss/holding/retrigger; eFuse/fuse interaction and pulse repetition. Use fresh fuses/dummy loads; a few successful clearing trials do not replace a supplier clearing maximum.

## C — two-stage conversion

**Topology proposal:** 9–24 V→6 V intermediate→5.1 V, with independent final output protection retained. A final-stage high-side short now connects the lower intermediate reservoir through its inductor. Conversion is source reduction, not itself a sub 5.5 V clamp.

### Voltage/current/energy and normal margins

ASSUMED intermediate 6.00 V±2% full static target gives 5.88–6.12 V; intermediate ripple/startup/load release and fault OVP must be added/qualified. A sustained final high-side short exposes 6.12 V, giving **−620 mV, BLOCKING** without independent protection. In an ideal undamped maintained-source LC example starting at 5.158632 V, first voltage crest `2Vin−V0` is CALCULATED **7.081368 V** even with zero initial excess current. This is a counterexample model, not a predicted prototype peak. Merely putting the intermediate below 5.5 V does not eliminate resonant overshoot either.

DATASHEET [LM61460 Rev D](https://www.ti.com/lit/ds/symlink/lm61460.pdf) has a recommended output relation ≤ 0.95VIN. Using ASSUMED ±1% intermediate tolerance and the inherited final static upper 5.158632 V requires CALCULATED intermediate nominal ≥**5.484989 V**; guaranteeing intermediate high<5.5 requires nominal<**5.445545 V**. The **−39.445 mV nominal window is BLOCKING** for this implementation before dynamics. A typical dropout number cannot resolve the 5 A worst case. Different converter/dropout data would need a new full normal/fault tolerance proof.

CALCULATED local 60.996 µF upper screen at 6.12 V stores **1.142284 mJ**, versus 17.566848 mJ at 24 V (about 15.38× less). However ASSUMED first-stage output store 264 µF plus that local input store gives total 324.996 µF /**6.086265 mJ**; all intermediate capacitance must count. Also include the first-stage inductor and charge delivered until it is physically isolated. For positive final current, `Ipk<=sqrt[2(E_intermediate+E_first_L+Vmid Qcontinued+E_final_L0)/Ldiff,min]` is available only after every term and the nonlinear inductance floor are bounded. The existing final choke's high-current floor is still OPEN.

Both stages can use a full 24 V-rated converter family such as LM61460 as research candidates. Selecting a final-stage IC rated only 17 V creates an upstream-first-stage-short overrating problem; a separate intermediate clamp/isolator or full source-rated final stage is needed. Do not assume the healthy first-stage current limit is a maximum pulse, nor its 6 A output headline an energy bound. A first-stage-short fault requires its own independent test/containment argument.

### Efficiency, thermal cost and normal behavior

ASSUMED ηfirst92%, ηfinal95%, at inherited 25.491803 W raw output: CALCULATED ηcombined**87.4%**, first-stage loss**2.333346 W**, final-stage loss**1.341674 W**, total**3.675020 W**. Compare ASSUMED single-stage 93.5%: loss 1.772157 W; the example adds**1.902862 W** before auxiliaries/protection/harness. These efficiencies are illustrative targets, not datasheet minima or measured V1A values. They cannot be read directly from curves with different voltages/L/C/bias. Total module efficiency and ambient/enclosure thermal limits are OPEN; stage losses go to their own IC/inductor/copper, not all to one IC thermal resistance.

The example draws CALCULATED 3.240758 A at 9 V before auxiliaries/inrush. Check startup against the eFuse minimum limit, stage sequencing and intermediate charging; two soft-start loops can interact. Final normal voltage/trip/harness windows stay at inherited conditional values if output setting/path are unchanged. Cascade conversion does not recover the 11.433 mV harness margin or qualify the 20 µs load-release assumption. Avoid output setpoint/remote-sense changes as a hidden way to compensate losses.

### Timing, supplies, rated destination and blockers

Complete fault→final detector/clamp/series isolation minimum/maximum remains **OPEN/OPEN**; intermediate lowering may lengthen voltage-rise time but does not remove any unbounded delay. First-stage current-limit/OVP/physical-off chain is separately **OPEN/OPEN**. The final clamp/dump stage must still be selected and sized from its residual intermediate energy/current bound, as in D/E. Rated destinations: source-isolation pass FET, both stage magnetics/capacitors under their ratings, and a qualified final absorber/dump MOSFET. Without a timed source stop the healthy first stage can supply continuing energy indefinitely; no finite absorber rating follows from the local store alone.

Keep protection auxiliaries upstream on the original input domain. A 6 V intermediate cannot supply the existing 7.623 V driver LDO in regulation. Use qualified boost/driver power and direct rail supervision/hold-up if an alternate supply is proposed. Startup/reset, partially powered sensing, independent fault latch and eFuse shutdown remain necessary.

Would reduce B01 excitation only after intermediate voltage/store/current are qualified; leaves saturation, B02/B03/M01/M03/M04/M05/M06/m03 for the retained protection. Does not remove the resistor-terminal conflict. ASSUMED incremental 15–25 conversion placements and **US$8–20**, excluding the required independent protection and common fixes; adds another hot IC/inductor and PCB area. Exact parts/cost OPEN.

Bench: each stage's high-side-short separately with dummy loads; intermediate overshoot/C/impedance bounds; coupled-loop stability and 9 V startup/brownout; final Pi fault voltage and complete action delays; both stages'5 A efficiency/thermal/ripple at 9/24 V; load release, ARM/prebias/inrush and recovery. No efficiency or transient behavior is validated here.

## D — series disconnect with local output absorber

**Topology proposal:** independent precision detector → latched opposed series FETs; protected-side active shunt clamp holds the local output during commutation; separate raw-side dump path accepts L201 current after opening. This avoids deliberately discharging the entire output bank as the principal protection mechanism. It still needs A's qualified source/store bound or an equally strong independent transient-current/energy contract.

### Two different clamps; supplier candidates

The protected-node clamp must keep the Pi below 5.5 V. The raw-side clamp can use a higher voltage to force inductor current down, but must stay inside raw capacitor, regulator, MOSFET and driver ratings. It cannot bypass the opposed pair. A TVS across the raw side is not a Pi clamp.

DATASHEET: [Vishay SMBJ Rev09-Jan-2024](https://www.vishay.com/docs/88392/smbj.pdf) SMBJ5.0A has 5 V standoff, 6.40–7.07 V breakdown at 10 mA and 9.2 V clamp maximum at 65.2 A/10–1000 µs/25°C. [TI TVS0500 Rev C](https://www.ti.com/lit/ds/symlink/tvs0500.pdf), despite flat-clamp technology, has 7.5 V minimum breakdown and 9.2 V maximum clamp at 43 A/8–20 µs/25°C. **Both are BLOCKING as 5.5 V Pi protectors.** Flat clamp describes curve shape, not a 5 V absolute peak.

An integrated active surge stopper also needs enough accuracy. DATASHEET [LT4363 Rev C](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf) FB1.25/1.275/1.30 V yields CALCULATED 5.254902–5.465098 V for a nominal 5.36 V clamp before divider/leakage errors. Its low corner is below recomputed normal 5.266252 V plus 10 mV. The nominal required merely to clear that lower bound is >5.381777 V, whose high corner is >5.487302 V, leaving <12.698 mV for every other error/dynamic term. Actual overshoot is unbounded for this application; do not select it from its headline.

Similarly [LTC4367 Rev D](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4367.pdf) ±1.5% comparator plus ASSUMED ±0.2% divider arms gives CALCULATED 5.226152–5.424504 V at 5.325 V nominal; false-trip margin **−50.100 mV, BLOCKING**. Gate discharge maximum 6 µs plus comparator maximum 2 µs can be combined only under their specific capacitance/overdrive tests, not as the actual dual-FET isolation maximum. Its UV/OV auto-recovery needs an added manual-fault latch.

Therefore D proposes a purpose-designed precision active absorber with its own qualified full error/overdrive/response budget; **no surveyed part is already shown to satisfy it**.

### Conditional output screen and harness failure

ASSUMED qualification targets: full static clamp 5.34–5.38 V; total effective response ≤ 0.5 µs from its upper-threshold crossing, including analog overdrive, amplifier/gate settling and useful conductance; protected-arriving current ≤ 60 A throughout, independently qualified including raw-bank bypass discharge, voltage differences/prebias, ESR/ESL, clamp turn-on and FET commutation current; A's L201 bound alone does not establish this; protected local C ≥ 1 mF, ESR ≤ 0.5 mΩ; local commutation ringing ≤ 20 mV; series current isolation ≤ 2 µs. These are separate from inherited detector trip tolerances, and no maximum is credited by assumption alone.

CALCULATED module-node bound:

`Vmodule <=5.38 +60×0.5µs/1mF +60×0.5mΩ +20mV =5.460 V`, reserve **+40 mV**.

Its clamp low 5.34 V is above recomputed normal 5.266252 V+10 mV by 63.748 mV; disconnect nuisance margin is +17.316 mV conditionally. If clamp activity prevents another detector threshold from crossing, clamp activity must itself latch physical isolation/shutdown. The active-clamp control loop must remain inactive during permitted normal transients and not interact adversely with buck regulation.

**That module result is not the Pi result.** ASSUMED harness ≤ 2 µH, current ≤ 10 A when opening, Pi effective C ≥ 220 µF, no downstream damping credited and an extra 10 mV Pi-local ringing allowance give this restricted L-only energy-transfer screen:

`VPi,L-only =sqrt(Vmodule² + Lh Ih²/Cpi) +10mV =5.552625 V`.

Margin **−52.625 mV: BLOCKING**. Harness current 10 A is itself an unqualified bound, not inferred from the 60 A source envelope. With only ASSUMED 2 µF and 5 A/2 µH, the corresponding undamped energy envelope reaches 7.403486 V before extra ring—an illustration of why unknown Pi capacitance cannot be set to 220 µF by convenience.

The L-only expression is a **restricted idealization**: it assumes no other node does positive work on Pi after isolation. D leaves its protected-module capacitor connected through the harness, so the expression omits an energy source and cannot establish a general required Pi C or a positive 1 mF acceptance.

Include both capacitors and the initial voltage difference. A lossless hypothetical state-box counterexample, with protected-moduleCm=1.5 mF, Pi Cp=1 mF, module capacitor 5.38 V, Pi 4.761433 V, Lh=2 µH and Ih=5 A, gives:

`Ceq=Cm Cp/(Cm+Cp)`

`Vavg=(Cm Vm+Cp Vp)/(Cm+Cp)`

`VPi,peak=Vavg + Cm/(Cm+Cp) sqrt[(Vm−Vp)² + Lh Ih²/Ceq] =5.542140 V`.

Margin **−42.140 mV, BLOCKING**, without additional ringing. This is a conditional initial-state sensitivity, not a claimed reachable worst-case trajectory; the listed bounds do not exclude it. The module node drops during energy transfer, so its shunt clamp can remain inactive while Pi overshoots. D requires the complete two-capacitor/clamp/harness/load-release trajectory, initial-state reachability and damping contract. Merely increasing Pi C to 1 mF does not close it. AC damping or a much shorter, characterized harness may help; adding DC series damping must still satisfy the normal resistance budget. If that cannot be qualified, move the absorber to the Pi as in E.

### Current, energy and rated destination

A's source contract bounds positive L201 current to ≤ 60 A. D additionally needs the separate protected-arriving-current contract above: the raw output bank can discharge through the series FET while bypassing L201. Source/raw-bank/initial-L plus protected-module C ≤ 1.5 mF gives a conditional **116.847287 mJ subtotal, excluding separate Pi capacitance**. The complete all-store bound is **OPEN** until Pi C,max and backfeed are specified. For example, adding a qualified separate Pi C,max=1 mF at 5.5 V would add 15.125 mJ, giving 131.972287 mJ; the 1 mF counterexample is not itself a maximum-C specification. Include every isolated-side initial-voltage/capacitor corner whenever reset/discharge or reverse transfer can send it into a dump. A's existing upper-output ceiling only applies where the conditional clamp actually protects; raw input-side storage ratings must survive the isolated fault.

CALCULATED protected clamp incoming energy ≤ `5.460×60×2µs =0.6552 mJ`, plus inductive/capacitive energy actually entering its node. Holding a rail need not dump its entire capacitor store, unlike a crowbar; deliberately discharging it adds that store explicitly. Allocate **ASSUMED 0.01 J** qualified hot-event capacity for the protected absorber and **0.2 J** for the source/dump path, then compare real trajectories and event repetition against applicable curves. These budgets are requirements on selected parts, not existing ratings.

A continuing source adds energy during current decay. For an ideal fixed raw clamp `Vc>Vin`, `td=L I/(Vc−Vin)` and `Edump=0.5 L I²×Vc/(Vc−Vin)`. ASSUMED raw clamp 28.5–31.5 V gives multiplier 6.333 at its low end against 24 V; ASSUMED Lmax 8.16 µH/60 A yields CALCULATED **93.024 mJ** for the sustained-source L-only decay example. This example must not be added blindly to the source-integral energy ceiling—those are different overlapping bounds—but it disproves budgeting only 0.5LI² while 24 V remains connected. Use maximum clamp for VDS and minimum clamp for decay/energy; raw 35 V capacitors have only 3.5 V before overshoot/derating at the 31.5 V target. All those ratings remain OPEN.

DATASHEET [Nexperia PSMN4R8-100YSE, 25-Jun-2021](https://assets.nexperia.com/documents/data-sheet/PSMN4R8-100YSE.pdf) supplies actual 125°C SOA curves, making it a research candidate for a shunt/dump device. Its 325 mJ single-avalanche rating is only the stated 52.6 A/95 µs/initial 25°C test; it is not the proposed hot 0.2 J acceptance. Determine VDS/ID/time, initial junction, mounting and repetition from the actual event and use hot SOA. As a replacement series pair its 11 mΩ/device at 175°C/VGS10 V would add 42 mV relative to the inherited 13.6 mΩ pair allowance, giving Pi 4.719433 V/**−30.567 mV BLOCKING**. Strong SOA does not grant low enough normal resistance; no substitution is selected.

### Timing, validity, complexity and tests

Min/max for precision-clamp onset→effective conduction and detector→series current isolation are **OPEN/OPEN**; the 0.5/2 µs figures are target maxima. Raw dump commutation/decay and source isolation add independent endpoints. LT4363's OV propagation typical 0.25/max 1 µs uses FB0→1.5 V, OUT0 and VCC12 V; it is not a small-overdrive 5 V clamp bound. Do not count gate discharge as proven current interruption.

Supply validity: detector/driver powered from qualified independent input-domain auxiliaries; default-off source-referenced gate paths; direct rail supervisor/hold-up through source isolation and dump. The active clamp must retain safe action during brownout; a raw-input dump path must remain effective even after series gate power disappears. Failure of the regulator/ref/clamp path itself needs a fail-off policy; a controller whose PG falls too late does not establish valid hot SOA/response.

Normal DC margin can retain the inherited conditional 11.433 mV only with no extra series loss or compensating resistance reduction. New protected C changes ARM inrush and control-loop/load-step behavior. Eliminates the main bulk-discharge ballast event and thus its 95°C terminal premise if that network is removed by approved redesign; does not automatically close B01/B02/B03/M01/M03/M04/M06 or harness energy. Separate absorber thermal/SOA qualification replaces M05; it is not automatically CLOSED.

ASSUMED incremental 20–35 placements, absorbers/bulk/supervisors and some crowbar parts removed, **US$15–35**, plus common driver-supply fixes; exact BOM/thermal/cost OPEN. Bench: source-bound and separate raw-bank discharge/current-envelope confirmation, zero/5 A injected short, both clamp nodes and individualFETVDS/current/gate trajectories, worst harnessL/C/initial current, local and Pi overshoot, hot/cold clamp accuracy and SOA/repetition; partial-rail/prebias/reset faults; normal ARM/startup/bulk loop interaction, ripple/load release and 5 A connector drop/temperature.

## E — independent protection at the Pi end

**Topology proposal:** protection immediately before GPIO5 V/GND entry: high-voltage-rated opposed disconnect, independent precision OV/fault latch, qualified transient-current limiting, Pi-side local capacitor/active absorber, and cable-input-side dump path. No wire may bypass it. Keep the module's upstream current/store containment; location alone does not bound current or eliminate source energy.

### Conditional Pi-node bounds

ASSUMED targets: **10 A maximum arriving at the protected Pi node during every transient**, including limiter delay/overshoot and charged-cap discharge; physical isolation ≤ 5 µs; effective local Pi-side C ≥ 1 mF, ESR ≤ 5 mΩ; all residual local ringing ≤ 20 mV. The 10 A bound requires a qualified fast limiter and, if necessary, a series impedance/magnetic element with a guaranteed trajectory. It is **not** inferred from either 5 A load rating or a 10 A settled setting. Its input-side current can be much larger before isolation and must go into the upstream dump, not the GPIO capacitor.

Using the inherited conditional trip upper 5.356563 V, a conservative series-only fallback charge/ESR screen is:

`VPi <=5.356563 +10A×5µs/1mF +10A×5mΩ +20mV =5.476563 V`.

CALCULATED margin **+23.437 mV**. Overdrive and all sense-to-current-isolation behavior must be included within that 5 µs target; if the inherited comparator cannot supply a bound from threshold crossing, add its overdrive explicitly and re-evaluate. With 220 µF instead, the screen is**5.653835 V/−153.835 mV: BLOCKING**. With 60 A overshoot instead of 10 A it is**5.976563 V/−476.563 mV: BLOCKING**. Any target violated blocks the fallback proof; an unqualified limiter is not a bypass around B01.

The primary proposed absorber has ASSUMED **full static 5.30–5.40 V** clamp limits and **≤ 20 mV total dynamic/physical overshoot**, including response, capacitor ESR/ESL, wiring and measurement uncertainty. This is a separate whole-loop qualification requirement, not just a comparator tolerance. If proved, CALCULATED target **5.420 V**, reserve **+80 mV**. Using A's recomputed normal envelope, clamp-low nuisance screen is `5.30−5.266252−10mV =+23.748 mV`; independent disconnect nuisance screen is +17.316 mV conditionally. Do not add the 20 mV overshoot a second time to the 5.420 V target.

Source/detector maxima, actual active-clamp stability/overshoot and VPi, max remain **OPEN**. The active clamp must set a fault indication that latches current isolation/source shutdown even if its lower clamp prevents another OV comparator from crossing. Clamp activity may not become indefinite dissipation into a persistent 24 V short. Sensing input OV and protected-output clamp activity provides two bounded shutdown triggers; the earliest applicable path must have a physical isolation bound.

### Harness/source energy and rated destination

The absorber is on the Pi side of the isolating FET and within the protected GPIO power loop. Cable-inductor current after opening is diverted into a separate input-side dump; energy already on the Pi side is intercepted locally. This makes the actual protected plane visible/measurable and avoids relying on an unknown Pi capacitor behind a long cable. It does not protect a wire added downstream that bypasses the stage, or a separate energized USB-C/other backfeed.

ASSUMED protected-side equivalent magnetic energy ≤ 0.5×10 µH×(10 A)², independently qualified; this is distinct from the upstream cable-input boundary and 5 µs isolation: CALCULATED incoming active-clamp energy ≤ `5.42×10×5µs +0.5×10µH×10² =0.771 mJ`. Proposed **≥ 0.01 J hot pulse capacity** leaves an allocation reserve, but exact VDS–ID–time/hot SOA and repeated faults still need supplier acceptance/bench evidence. Local 1.5 mF maximum store at 5.42 V is 22.0323 mJ; add it if the chosen reset/crowbar deliberately dumps it. A voltage-holding clamp normally dissipates excess delivered energy, not all initial capacitor energy.

The independent limiter's pass-FET can dissipate much more than 0.771 mJ: its stress is `integral[(Vin−Vout) I dt]`. ASSUMED input 24 V/10 A/5 µs/near 5.4 V gives a rectangular 0.930 mJ screen before transition/cable energy. Its true maximum input current, response and source reservoir remain OPEN; qualify its own SOA, not only the shunt clamp. The 0.771 mJ figure bounds a protected-absorber subcase; it does not bound cable-input current. Upstream source/cable-input dump retains an **ASSUMED 0.2 J** capacity target. Its delivered-energy/peak-current contract must explicitly include cable-inputL/current, continued-source work, module bulk/local-input-cap bypass and limiter transition stress. Adopt A's charge ≤ 150 µC, physical source-off ≤ 20 µs and qualified Ldiff through 60 A, then independently bound cable current from raw-bulk discharge; A's L201 current bound alone does not bound that discharge. An output-bank-side current limiter or equivalent qualified input-side current/energy path may be needed. Until that contract exists, actual delivered dump energy remains OPEN. No internal low-voltage eFuse with 23 V recommended maximum is accepted for a 24 V sustained fault.

Named candidate hot-SOA devices are the Nexperia family studied in D, but none is selected; lowRDS, gate charge and source-referenced turn-off must also fit. Source charge and saturated-L missing from the current design must be bounded by A's approach or an independently qualified input-side absorber/limiter combination. A second unbounded copy of the present Sheet03 circuit would leave B01/B02 untouched.

### Timing and rail validity from startup through fault

Independent path: local input/OV or clamp-activity detection→latch→gate driver→limiter/series current interruption→input-dump/cable decay. Complete minimum/maximum **OPEN/OPEN**; proposed isolation maximum 5 µs and active-clamp total overshoot 20 mV are distinct qualification targets. Stage specs cannot be combined across unsupported conditions. Power-up into pre-existing 24 V must hold the FETs off before precision sensing settles; safe behavior cannot depend on the failed buck's PGOOD.

A Pi-end stage normally sees about 5.1 V, so the old 7.623 V LDO cannot be copied there. Proposed supply uses an independent current-limited auxiliary feed from the original input domain, with its own protection and return definition, plus a qualified local driver converter/supervisor/hold-up. A self-powered alternative adds control current to the 5 A V1A load envelope and needs an explicit budget. It is not silently credited while demanding 5 A at the Pi.

[ADI LTC3115-1 Rev E](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf) is a supply research candidate: DATASHEET 2.7–40 V input/output permits a boost/buck driver rail from either normal 5.1 V or bounded 24 V; it is not already a validated 10 V fault supply. Required output accuracy, input step response, switching-noise interaction, startup and failure containment remain OPEN. Local auxiliary source failure must produce default-off gates and retain enough energy for the clamp/dump action, not automatic re-arm.

### Normal 5 A margin, complexity and blocker disposition

ASSUMED combined hot loop target **≤ 50 mΩ**, including module protection, shunt, PCB, cable, all contacts/returns and new local stage. CALCULATED inherited raw minimum minus 5 A drop gives Pi **4.788271 V/+38.271 mV**. This is a proposed lower-resistance redesign, not the existing 55.367741 mΩ path. Adding an ASSUMED 10 mΩ stage to the existing path instead gives Pi 4.711433 V/**−38.567 mV BLOCKING**. New gate-drive shunt/FET loss and extra connector resistance must be recovered elsewhere; the raw voltage setting stays unchanged. Local 1 mF adds ≥ 5.1 mC charging at startup; qualified maximum C, inrush timing/current and ARM sequence are required. The 100 mV dynamic reserve remains unclosed, not claimed.

Would resolve the reference-plane/harness-energy part of B01/B03 if local absorber/dump are qualified; could remove bulk-discharge ballast/terminal premise by an approved active-clamp redesign. Leaves transient input bounds, B02/supply/powered-off sequencing and normal-path verification until qualified. Local independence reduces reliance on the remote failed converter/PG, but does not alone close M01/M03/M04. Common policy fixes below still apply.

ASSUMED added 30–55 placements for local limiter/disconnect, reference/detector/latch, absorber, controlled C and supply/supervisor; **US$20–50** plus auxiliary conductor/connector and small PCB. Source containment/common module changes are shared costs and must not be double counted. Exact MPNs/cost/thermal realization OPEN. Bench: fault injection with cable attached; measure at GPIO and both sides of local isolation, limiter overshoot, source-charge integral, clamp current/voltage and gates; worstL/C/zero-load/5 A/prebias; hot SOA/repetition/cooldown; local supply startup/24 V step/UVLO/power disappearance; connector/keying/bypass/backfeed checks, 5 A drop/temperature and normal load-release/inrush false-fire tests.

## Fixes needed in every architecture

These are **PROPOSED fixes**, not applied schematic changes. Re-check each resulting logic and rail state; changing architecture does not waive them.

| Gate2c item | Proposed fix | Acceptance evidence / residual risk |
| --- | --- | --- |
| M06 BUCK_PGOOD-loss false crowbar firing | Separate independent OV_FAULT latch from RUN/PG qualification. PGOOD-low forces series disconnect/run permission low, but does not fire a crowbar or blow a fuse. Only confirmed independent OV or a dedicated clamp-activity/current-fault latch commands energy disposal/source shutdown | Truth table and race/glitch proof for cold start, ARM, healthy undervoltage, inrush, 5→0 release, genuineOV+PG loss, reset and brownout. Verify no PG condition masks OV. Clamp activity must force timed isolation even if another OV comparator never trips |
| m03 PG pull-up above 5 V | Pull both TPS7A16 open-drain PGs to a qualified rail with worst high ≤ 5 V, e.g.3.3 V, then level-buffer/translate to the detector logic where needed | Check every VIH/VIL, input/clamp/current limit and partial-power state. A 3.3 V pull-up is not automatically a valid high at every 5 V logic input. DET_5V upper 5.117398 V is not acceptable just because an absmax is higher |
| M03 powered-off clamp/backpower | Use fault-voltage-rated sense scaling plus a clamp whose return remains defined while reference/comparator supplies are off; add qualified isolation/buffer and series-current limiting as needed. Do not use the unpowered precision reference as an unspecified current sink | Bound input pin voltage AND injection current, reference/load disturbance, leakages/errors, startup/decay/24 V prebias and reset recovery. Verify positive/negative faults and every alternative powered port. Do not credit internal ESD diodes as a designed sustained energy path |
| M01 driver rail supervision | Directly supervise the actual driver/loaded bootstrap/gate-drive rail with threshold/hysteresis/maximum response chosen from qualified timing/SOA. Block ARM while invalid; use gate-to-source default-off discharge independent of powered logic, with isolated hold-up for required clamp/dump action | Supervisor min/max thresholds and response, reset loading, high-side BST−TS/VGS under load, gate charge and full fault/UVLO trajectory. ExistingPG floor 6.175 V and falling input UVLO7.619–8.168 V do not assure driver timing |
| M02 brownout history / shutdown release | Maintain fault shutdown until source/store energy is safe; define manual RESET/ARM and power-cycle interlock. A control-rail failure must default off, not erase a latch then reconnect to a persistent short | Startup into pre-existingOV, cold and warm reset, source hiccup, held ARM, supply loss during clamp/dump and returned input. If fault history is deliberately lost on full power loss, demand fresh deliberate ARM; never claim nonvolatile retention |
| M05 resistor-terminal envelope | If using WFMB2512, keep its terminals below DATASHEET 95°C with verified reserve, or propose a construction with applicable hot pulse/terminal ratings | Measure actual terminal temperatures and supplier hot pulse/repetition acceptance. Element/junction temperature limits and cold pulse plots do not supersede terminal limits |

ASSUMED supply example for the stronger SOA candidates: start ≥ 10.5 V, useful-drive threshold ≥ 10 V, effective hold-up C ≥ 10 µF, control load ≤ 25 mA, total dynamic gate charge ≤ 480 nC and required action hold-up ≥ 150 µs. CALCULATED required C**8.46 µF**; nominal allocation supports **180.8 µs** after gate charge at 0.5 V usable droop. Neither load/charge/C/rail thresholds nor this duration is qualified. D's sustained-source decay example is 108.8 µs; source/isolation plus decay fits the 150 µs allocation only if all timing/source conditions hold. Loaded gate VGS/BST−TS, not merely VCC, must meet the chosen FET's rated resistance/SOA conditions. The hold-up diode must prevent the falling upstream rail from draining the store.

An indefinitely unblown B fuse cannot be covered by finite hold-up; an SCR may self-hold only under its holding-current conditions. A supervisor response must finish useful gate action before supply falls below the timing floor. Startup enables only after reference precision, rail validity and detector input-pin conditions—not merely a PG transition—are established. E's auxiliary wiring/self-powered current budget needs explicit owner review.

## Common timing evidence and missing endpoints

The following DATASHEET numbers are inherited from Gate2c and remain test-conditioned. See its [source register](../../../../third_party/sheet03_gate2c_source_register.json). Complete application minima/maxima are OPEN for **every option**; no zero delay fills a blank.

| Retained/candidate stage | DATASHEET minimum / typical / maximum | Condition and why it does not close the option |
| --- | --- | --- |
| TLV3201 falling output | OPEN/45/55 ns | 5 V, 20 mV overdrive, 15 pF; includes neither sense settling nor time to reach overdrive |
| SN74LVC1G11 each gate | 1/OPEN/4.6 ns | Specified 5 V supply/load/full temperature; apply each intervening gate |
| SN74LVC1G74 asynchronous clear | 1.6/OPEN/6.1 ns | Specified 5 V table; no latch/startup guarantee below valid supply |
| UCC27511 output | 4/15/26 ns at 4.5 V; 4/13/23 ns at 12 V | Stated tied-output/load tests; actual split output/hot MOSFET/other rail not automatically covered |
| LTC7001 propagation | OPEN/35/70 ns | 10 V driver/bootstrap and 1 nF; actual dual-FET plateau/current interruption OPEN |
| TPS26630 SHDN crossing→off | 0.8/1/1.5 µs | Does not include Q304/SHDN crossing, upstream capacitors or L tail |
| TPS26630 hot short | OPEN/1 µs/OPEN | Typical current threshold/response; does not imply permanent latch-off |
| TPS26630 active-limit timeout | 129/162/202 ms | Thermal protection may act earlier; irrelevant as a fast Pi isolation bound |
| LTC4218 limiter sense→gate | OPEN/OPEN/1 µs specified maximum | Stated overdrive/CGATE/FB test; weak timed gate pull-down and actual current-off endpoint separate |
| Fuse/SCR effective clamp→complete arc isolation | OPEN/OPEN/OPEN | Supplier coordination must cover source minimum/maximum, DC waveform, temperature and stores bypassing fuse |
| D/E precision absorber and series limiter | OPEN/OPEN/OPEN | Proposed procurement targets 0.5/2/5 µs are not surveyed-part guarantees |

For A, B and retained C protection, use the parallel crowbar/series/SHDN equations in Gate2c, including analog overdrive, all gates, gate charge and commutation. B adds SCR spreading and fuse arc time; C adds upstream-stage isolation/current control. D/E need both local-clamp conductance and actual series-current isolation endpoints. Source-stop, raw/input dump and load-side magnetic tail are distinct events. A fast gate-voltage edge alone proves neither safe VDS nor safe Pi voltage.

## Decision and qualification contract

**RECOMMENDED: E — independent Pi-end precision disconnect and local energy absorber. Runner-up: D — module-side disconnect/absorber, only with the complete harness/capacitor trajectory contract.** This is a proposed architecture direction, not a qualified BOM or a release. Current application worst-case voltages remain OPEN and R2/R3 stay BLOCKED.

E puts detection and absorption at the frozen GPIO protection plane, intercepts the energy on that side of the switch, and permits a defined local C instead of treating an unknown Pi/harness as a capacitor specification. It has more wiring/control hardware and must recover its normal DC resistance/auxiliary budget. It wins over a conditional module-node PASS that leaves a Pi-node counterexample. D is simpler mechanically and can reuse module layout, but the retained protected-module capacitor, cable inductance/current, initial voltage difference, damping and Pi C must be jointly bounded. A is useful as a **source-bound ingredient**, not a demonstrated alternative Pi-side guarantee. B needs a fundamentally coordinated fuse source and sacrifices normal voltage; C reduces excitation while adding losses and still needs D/E.

Before any schematic change, owner approval must accept the following development contract or revise its proposed allocations without weakening the frozen requirements:

1. Pi-end series stage rated for bounded 24 V high-side-short input plus the separately approved source transient contract; genuine opposed isolation, default-off and no bypass/backfeed route.
2. Protected transient current ≤ 10 A including response overshoot, not just a settled limit. Identify and qualify the limiter, local input C and any required nonsaturating seriesL/impedance.
3. Effective Pi-side C ≥ 1 mF and ESR ≤ 5 mΩ across bias/temperature/life; controlled maximum C and inrush; physical isolation ≤ 5 µs from the specified trigger including sense/overdrive/gate/commutation.
4. Precision active absorber full limits 5.30–5.40 V and total overshoot ≤ 20 mV at GPIO; independent clamp-active fault/source-stop path. The proposed 5.420 V primary peak and 5.476563 V series fallback only follow after their different contracts are proved.
5. Source delivered-charge/isolation/Ldiff and raw bulk discharge bounds; input-side cable-current/inductance and maximum dump energy/voltage. The 0.2 J target does not replace those bounds or a hot SOA trajectory.
6. Direct driver/reference qualification and loaded-gate timing,≥ 150 µs conditional hold-up (recalculate for actual events), safe partial-power clamp/reset and explicit auxiliary power/return budget.
7. Full hot 5 A loop ≤ 50 mΩ without increasing raw setpoint; normal maximum/trip uncertainty and no false firing under the approved load-release/startup tests.
8. Exact supplier-supported pulse/SOA/terminal ratings and measured current/voltage waveforms with dummy loads before R2 release. Owner-approved source interface still awaits the upstream converter model.

## EXPLANATION FOR THE DESIGNER

A buck normally connects its input to the inductor for only part of each switching cycle. If its high-side transistor fails short, the switch is permanently on. The path becomes input reservoir capacitors → failed transistor → L201 → output capacitors and load. Normal PWM/current-limit control cannot turn a piece of shorted silicon off. A valid 24 V input will not trip input overvoltage protection just because the 5 V output is in danger.

The local input capacitors are a battery for the first microseconds. Their energy is `E=1/2 C V²`: the inherited 60.996 µF upper screen holds 17.567 mJ at 24 V. At 6.12 V the same capacitance holds 1.142 mJ. An eFuse upstream can stop further charging but cannot remove energy already on its downstream side. A current limiter placed before those capacitors has the same limitation. Its finite response also delivers some charge before current settles; that integral must be bounded.

The inductor resists current change. With constantL, its magnetic energy is `E=1/2 L I²` and current slope is `dI/dt=(Vin−Vout)/L`. Saturation makes the differential inductance fall, sometimes sharply, so current rises much faster for the same voltage. The nonlinear stored energy uses`integral(i Ldiff(i) di)`; inserting nominal 6.8 µH into 0.5LI² at hundreds of amps is not valid. A typical 14 A saturation entry is a test-defined percentage drop, not a guaranteed floor above 14 A. That missing floor is why an assumed 0.5 µH result cannot qualify a 0.1 µH corner.

The crowbar diverts current away from the load; its ballast limits the capacitor-discharge spike. It still needs enough speed to avoid overshoot and enough conductance to hold voltage while incoming current persists. Increasing ballast helps pulse survival but raises the remaining voltage; increasing outputC slows voltage rise but adds inrush/stored energy and changes buck dynamics. A series switch stops conduction only after gate discharge/current commutation, and the inductor must then send its energy into an explicitly rated clamp/dump path.

A bounds this by limiting replenishment, minimizing—not removing—required local inputC and qualifying the inductor throughout the pulse. It keeps the crowbar but demands strong current/energy and thermal evidence. B turns the fault into a deliberate large current that blows a real fuse; that works only if enough current is available and the crowbar survives until the arc is extinguished. A source that limits below the fuse's normal rating defeats that strategy. C reduces the voltage driving the fault and capacitor energy, but a 6 V source still violates 5.5 V and can ring higher; the second conversion stage adds heat.

D opens the series path and uses a local active absorber for let-through, with a separate higher-voltage input-side dump for magnetic energy. A “5 V TVS” is unsuitable when its actual clamp is 9.2 V. The amplifier/reference/MOSFET loop must have enough precision and speed for the small normal/fault window. D's module clamp can hold its own node while a cable and two charged capacitors ring above the limit at the Pi. Resistance can damp that oscillation, but large DC resistance would violate 4.75 V at 5 A; a full coupled model and qualified damping are needed.

E puts the last independent switch/absorber right at the GPIO entry. It sees and absorbs the voltage that matters rather than relying on a remote node measurement. It does not make current disappear: the cable/input side still needs its dump, the limiter still needs a proven transient ceiling, and the added FETs/shunt/wires still consume normal voltage. This is why E is recommended as a direction while its numerical results remain conditional and all application maxima remain OPEN.

## Validation, provenance and checkpoints

EVIDENCE: [conditional calculations](gate3/OPTIONS_CALCULATIONS.json) reproduce the principal finite examples; [calculator](../../../../scripts/calculate_sheet03_gate3_options.py) reads historical JSON only and preserves unknown application maxima as `null`. [Twelve targeted tests](../../../../tests/test_sheet03_gate3_options.py) check energy conservation, independent ballast corners, negative source/current/C/normal-voltage cases, cascade power balance and the two-capacitor harness counterexample. They verify arithmetic, not electronics.

Run from this worktree:

```sh
python3 -B scripts/calculate_sheet03_gate3_options.py --write
python3 -B -m unittest discover -s tests -p test_sheet03_gate3_options.py -v
git diff 0677fea --name-only -- hardware/kicad
```

The hardware diff must be empty. No ERC/DRC, native-file inspection, export, SPICE or bench test was performed or claimed. Historical Gate2c JSON/reports/contracts and all hardware remain unchanged. Manufacturer material is referenced only; selected unmodified PDF archives stay ignored under `third_party/documents/sheet03_gate3/`. Exact document revisions/URLs, sections, archive hashes where downloaded, license/reuse state and attribution are in [the provenance register](../../../../third_party/sheet03_gate3_source_register.json). Entries explicitly disclose unavailable exact revisions or application ratings; those stay OPEN.

Independent review also requires D to bound raw-bank discharge separately from L201 current and includes separate Pi capacitance when budgeting total stores. Independent arithmetic review corrected A's6 A initial-current allocation: the 24 V/360 kHz/5.44 µH normal ripple screen can peak 6.034 A, so the proposal now uses 6.1 A and recalculates normal release. It also removed an unjustified positive D Pi C-only result by including the retained module capacitor and initial voltage difference. These corrections are part of the final result; no hardware was changed.

Checkpoints pushed after each option: `03e82e8` A; `ce71adb` B; `adf6dd6` C; `6ffbe69` D; `05b3339` E. Final review/corrections/comparison follow in the closure commit. See [validation record](gate3/VALIDATION.json) for preserved-history/hardware metadata evidence and test result. The draft PR targets `feat/sheet03-output-protection`; no merge is authorized.

RECOMMENDATION: E — independent Pi-end precision disconnect and local energy absorber — needs owner approval before any schematic change.
