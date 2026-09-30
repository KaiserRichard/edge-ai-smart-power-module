# Gate 3 — Sheet 03 fault-containment architecture options

**STATUS: BLOCKED for electrical release; architecture analysis in progress. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Root is the single decision/document owner. Read-only source research was delegated; it did not touch CAD or own architecture decisions. This branch starts at `0677fea0a32fc87b740949d589abe1588e55934c` (`origin/feat/sheet03-gate2c`). Native KiCad files are not opened, saved or checked by this task; another owner is editing them. “Gate 3” here means this requested architecture analysis, not authorization to skip R2 and start the repository's R3 PCB gate.

## Frozen requirements and evidence discipline

REQUIREMENT: input 9–24 V; GPIO-powered Pi (D-30); `V_Pi,peak < 5.5 V`, including let-through; `V_Pi >= 4.75 V at 5 A`; `V_normal,max + margin < V_trip,min`; `V_trip,max + dV_let-through < 5.5 V`. No USB-C OVP credit, rail-setpoint increase, relaxed voltage ceiling or unapproved remote sense is used.

OPEN: the proposed robot 24 V rail and 48 V→24 V converter have no selected model. Their tolerance/trim/startup, current-limit response, output store, fault ceiling/time, return paths and isolation need an interface contract. Normal 24 V is a maximum requirement, not permission for a nominal 24 V converter to exceed it. Primary pass-through containment remains allocated upstream; this analysis does not invent a 48 V maximum fault rating for V1A.

Labels throughout: **DATASHEET** = specification at its stated conditions; **CALCULATED** = arithmetic within listed inputs; **ASSUMED** = proposed allocation/unqualified premise; **OPEN** = missing applicable bound. Every finite architecture voltage below is a conditional screen, not the application worst case. Actual worst-case Pi peaks remain **OPEN** and are `null` in [the calculation record](gate3/OPTIONS_CALCULATIONS.json). A negative screen is **BLOCKING**, never rounded into PASS. A positive screen only states what a proposed qualified implementation would have to achieve.

Baseline evidence: [Gate2c closure](GATE2C_REVIEW_CLOSURE.md), [architecture history](SHEET03_ARCHITECTURE_DECISION.md), [calculations](GATE2_CALCULATIONS.md), [historical JSON](CALCULATIONS.json), [decision index](../../../context/06_DECISION_LOG.md). Historical evidence is preserved.

## Common comparison basis

CALCULATED, inherited conditional screens: raw static 5.038271–5.158632 V; normal release maximum 5.261614 V using ASSUMED 20 µs excess-current interval; trip 5.293568–5.356563 V with unqualified hysteresis/reference/passive allocations; normal margin after ASSUMED 10 mV reserve **+21.954 mV**. These are not complete tolerance guarantees. At a 30 µs normal-response assumption the same nuisance margin is **−2.979 mV, BLOCKING**.

The reduced hot-loop screen is 55.367741 mΩ: Pi 4.761433 V, only **+11.433 mV**. The maximum static loop budget from the inherited raw minimum is `(5.038271−4.75)/5 = 57.654280 mΩ`. Just **2.286540 mΩ** additional series resistance exhausts its spare margin. All added fuses, shunts, FETs, contacts and returns must fit the total budget. Actual hot VGS/RDS, harness and normal voltage limits remain OPEN. The earlier 100 mV dynamic reserve is an ASSUMED target; it is not frozen or already achieved.

The original source sensitivity 24 V / 0.1 µH floor / 0.4 µs crowbar action gives CALCULATED 502.457 A and 6.271942 V, **−771.942 mV**: evidence that the old assumptions cannot qualify the existing architecture. It is not numerically transferred to changed circuits. Charged local input C, initial L current, replenishment, raw/protected capacitors, harness inductance and any backfeed must each have a destination.

Comparisons include no-load, 5 A, startup/prebias, ARM inrush, load release, brownout and a persistent failed-short buck. Test measurement uncertainty must fit the positive reserve; no Pi is used as the first fault load.

## A — keep crowbar, explicitly bound the source

**Topology proposal:** eFuse → independent current-limiter/pass FET → minimal qualified buck-local input C → failed buck switch/L201 → existing series disconnect/crowbar. Retain independent detector power. Add a rated upstream inductive dump path; limiting incoming current does not remove that obligation.

### Source, current, energy and voltage

DATASHEET: [LM61460 Rev D §9.2.2.5](https://www.ti.com/lit/ds/symlink/lm61460.pdf) requires at least 10 µF ceramic input capacitance and adjacent 100 nF bypass at each VIN/PGND pair. Zero/negligible input C is not an acceptable proposal. ASSUMED nominal 10.2 µF ×1.2×1.15 gives 14.076 µF upper screen. Even its initial 24 V store alone permits CALCULATED **39.069 A** with an ASSUMED constant 5.44 µH floor and 6 A initial current—well beyond the existing inductor's **DATASHEET typical** 14 A saturation point. That low-current floor cannot be extrapolated through the pulse.

ASSUMED qualification targets, not selected parts:

| Target | Allocation and required evidence |
| --- | --- |
| Effective local input C | 10–20 µF including every bypass; guarantee minimum for switching/stability and maximum for energy over voltage/temperature/life |
| Source charge after fault until physical isolation | `Q_source,+ <=150 µC`, including limiter response overshoot; isolation ≤20 µs from fault onset. A settled 5 A limit does not prove this integral |
| L201 differential inductance | 5.44–8.16 µH over 0–60 A and full temperature; replace/resize only after approval. No existing MPN is claimed to meet it |
| Initial current / rail | ≤6 A; input ≤24 V; raw node nonnegative throughout commutation |
| Raw bank | effective C ≥2.4064 mF; bulk ≤5.4144 mF plus ceramic ≤182.16 µF; ESR ≤4 mΩ—each still needs qualification |
| Action | effective crowbar conductance ≤1 µs after the specified detector overdrive; series current isolation ≤2 µs; local ringing ≤20 mV |
| Downstream C / backfeed | ≤220 µF; no independent downstream source for this pulse calculation |

CALCULATED within those targets:

`E_available,L <= 0.5 Cin,max Vin² + Vin Q_source,+ + 0.5 Ldiff,max I0²`

`= 5.760 mJ + 3.600 mJ + 0.146880 mJ = 9.506880 mJ`.

For positive current, passive nonnegative raw voltage and no other energy source, `W_L(I)=integral(i Ldiff(i) di) >=0.5 Ldiff,min I²`; hence **I_L <=59.120 A**, rounded conservatively to the ASSUMED 60 A design envelope. This needs a guaranteed Ldiff floor over the entire trajectory, not an Isat headline. A reverse/precharged/negative-node event needs its own energy bound.

After the inherited maximum trip, include 42.691 mV raw overdrive before the comparator delay condition, `60 A×1 µs/Craw,min`, incremental ESR from `dI/dt<=24/Ldiff,min`, and 20 mV ringing. CALCULATED upper screen **5.461834 V**, margin **+38.166 mV**. Threshold crossing already includes pre-crossing ESR; only its further rise is added. At **2 µs** crowbar action the same conservative bound becomes **5.504414 V, −4.414 mV: BLOCKING**. Complete application timing and V_Pi,max remain OPEN.

Once fully conducting, the ASSUMED maximum 40.095 mΩ crowbar path gives `60×R =2.4057 V`, below the ceiling. That steady load-line does not establish its turn-on transient. Raw bulk helps during the on interval; it is not credited as Pi capacitance after series isolation. The harness still needs the D/E energy check.

CALCULATED total-store ceiling at an assumed 5.5 V output ceiling is **97.48235 mJ**, including bulk/ceramics, protected C, local input store, source charge and initial L. Energy can split between crowbar, dump clamp, pass-FET and wiring; every trajectory must close. Conservatively dumping all of it through ballast gives **2.998996 A²s** at minimum ballast resistance. Independent ±corner sharing gives at most **25.5639% /24.9203 mJ per resistor**, not exactly one quarter.

**Proposed rated destinations:** keep CSD18540Q5B plus qualified ballast only if their hot waveforms are accepted, and add an upstream active dump FET/clamp with explicit ≥0.2 J hot-event qualification. Existing Vishay WFMB2512 maximum terminal temperature is **DATASHEET 95°C**; ASSUMED terminal target ≤85°C and ≥50 mJ applicable hot single-pulse capacity per element leave a proposed reserve. Neither temperature nor that pulse capacity is confirmed. At inherited ASSUMED 125°C terminals the old network remains BLOCKING. MOSFET energy/I²t is not an invented fuse rating: apply actual VDS–ID–time against hot SOA, junction and package limits.

### Limiter candidate, timing and supplies

[ADI LTC4218 Rev H](https://www.analog.com/media/en/technical-documentation/data-sheets/4218fh.pdf) is a research candidate, not selected. DATASHEET operating range 2.9–26.5 V; sense threshold 14.25–15.75 mV under its conditions. ASSUMED 3 mΩ±1% gives CALCULATED settled **4.702970–5.303030 A**. Its 1 µs sense-to-gate maximum uses a 60 mV step, VFB=0 and 1.5 nF gate test; actual gate/current removal and source-charge bound are OPEN. Timer shutdown uses a weak gate pull-down; timer expiry is not physical isolation. Its 26.5 V ceiling also fails to cover the inherited abnormal OVP upper screen 28.289 V; a higher-rated stage or explicit input clamp is needed for that separate contract. No datasheet current-limit maximum is relabeled as an instantaneous current ceiling.

Timing chain minimum/maximum: fault→limiter sensing/response→source current isolation is **OPEN/OPEN**; OV onset→divider/overdrive→comparator→qualification/latch→crowbar driver→effective clamp and parallel series turn-off are **OPEN/OPEN**. The proposed 20/1/2 µs bounds above are qualification targets. Retained stage specifications and supply test conditions are tabulated later; partial sums are not total delays.

Supply validity: keep auxiliaries before the eFuse; add direct driver-rail qualification, fail-off gate paths and hold-up through source removal/inductive decay. The current PG floor 6.175 V does not qualify the old timing. At falling input UVLO, driver headroom may already be lost. Do not release SHDN/crowbar merely because CTRL_ENABLE collapses while stored energy remains.

### Normal margins, complexity, blockers and bench closure

Upstream limiting adds input loss; ASSUMED 3 mΩ shunt alone costs about 29.7 mW at 3.147 A /9 V, plus pass-FET and wiring loss. Steady load, maximum low-input startup/inrush and limiter/buck input-filter stability must fit its minimum current and dropout. The output static harness and nuisance margins stay at the inherited conditional +11.433/+21.954 mV only if its existing path/regulation is preserved; the 30 µs release counterexample remains BLOCKING.

ASSUMED incremental planning allowance: 12–20 source-limit parts, larger qualified inductor, dump clamp and common supply fixes; roughly 25–45 placements total and **US$15–40**. These are engineering budgets, not quotes, guaranteed availability or a selected BOM. Actual cost/size/thermal design OPEN.

Would remove B01 only after the source integral, saturation floor and dump destination are qualified. B02/B03/M01/M03/M04/M05/M06/m03 remain or require the common fixes below; resistor-terminal conflict is removed only by rated temperature/construction, not new arithmetic. Bench: max-C/min-L hot/cold short injection; measure limiter integral and true source isolation, Pi peak, gate/driver/reference rails, raw-node undershoot and dump VDS; normal 9 V startup/inrush, input-loop stability, 5 A→0 release, resistor terminals, FET hot SOA trajectory and repeated pulses. Supplier maxima remain necessary beyond a successful prototype.

## B — fuse-blowing crowbar

**Topology proposal:** real fuse in a coordinated fault-current path, crowbar on its load side, independent detector, and rated inductive clamp. There are three distinct placements: fuse before local input C leaves its discharge bypassing the fuse; fuse after local input C includes that discharge but inserts impedance into the buck switching loop; output fuse with downstream crowbar includes source-fed output current but carries 5 A normally. Protected capacitors discharge through the crowbar without necessarily traversing the fuse. Fuse current I²t and total crowbar current I²t are therefore not automatically equal.

### Supplier sizing and hard conflicts

DATASHEET: [Littelfuse Fuseology](https://www.littelfuse.com/assetdocs/fuseology-selection-guide?assetguid=fa4aa360-f6c4-4eec-88a6-3d7ec3fe57d5) recommends usual 25% operating-current derating, with additional temperature/pulse considerations. ASSUMED efficiency 90% at inherited 25.491803 W means CALCULATED 3.147136 A at 9 V; preliminary input rating ≥4.196182 A, hence a 5 A screen. At the output, 5 A/0.75 requires ≥6.666667 A, hence a 7 A screen. Neither is a selected qualified fuse.

| Real supplier candidate / exact revision | DATASHEET pulse / interruption evidence | What is still missing |
| --- | --- | --- |
| [Littelfuse 451/453, GD 18-Sep-2023](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1) | 5 A nominal melting 5.566 A²s/cold R12.5 mΩ; 7 A nominal melting 10.32 A²s/cold R9 mΩ. Breaking 300 A at32 VDC for≤5 A; 400 A for≥6.3 A | Nominal melting is not max total clearing. The inherited 502 A sensitivity exceeds these interrupt ratings; it cannot be approved without a new bounded source |
| [Eaton FWP-A14F,720025 Oct2025](https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/bussmann-iec-high-speed-semi-conductors-fuses/bussmann-iec-ferrule-high-speed-fuses/eaton-bussmann-series-fwp-ferrule-high-speed-fuses-datasheet-720025-en-gb.pdf) | FWP-5A14F prearc2 A²s, clearing11 A²s at700 V; FWP-10A14F prearc4/clearing22 A²s. [10 A product](https://www.eaton.com/us/en-us/skuPage.FWP-10A14F.html) lists50 kA at700 VDC | Official clearing tables/catalog context differs on AC applicability; no guaranteed total-clearing24 VDC maximum for the actual capacitive/current-limited pulse. Use11 A²s only as an ASSUMED coordination example, not transferable rating |
| [Mersen FD27GB66V5T, July2026](https://www.mersen.com/sites/default/files/medias/PIM/files/DS-Semiconductor-Protection-Cylindrical-Fuses-Protistor-Size-27x60-gR-GRB-660VDC-Mersen-EN.pdf) | 5 A/660 VDC,50 kA at rated DC/L/R15 ms; prearc curve has±8% current band. Dissipation1.1 W atIn;27×60 mm/80 g | Genuine DC curve, but no total-clearing I²t in this document. Supplier24 VDC arc duration/clearing coordination remains OPEN; also a substantial size/drop cost |

The present eFuse's CALCULATED settled maximum ≈4.819820 A is below the 5 A input fuse rating and far below the 7 A output fuse rating. It is an upper screen, not a minimum current that guarantees melting. Local capacitors can produce a spike, but no guaranteed pulse integral follows from their capacitance alone. Current limiting/hiccup may starve the fuse before it clears. Reducing an input fuse to3.15 A violates the operating-current derating screen at9 V. **Guaranteed fuse clearing with this source is OPEN/BLOCKING.** B only becomes independent of the eFuse if an available-current minimum and applicable clearing maximum are contractually established.

CALCULATED extra output-fuse drop using the 7 A candidate's nominal cold9 mΩ: **45 mV/0.225 W**. Inherited Pi minimum falls to **4.716433 V, −33.567 mV: BLOCKING** before hot resistance/holder loss. This fuse requires a new lower-resistance harness/path allocation. The Mersen5 A output candidate's1.1 W at5 A corresponds to approximately220 mV loss at its listed conditions; it also needs derating and is not a low-loss solution.

### Rated destinations and pulse calculation

DATASHEET: [Littelfuse Sxx20x/Sxx25x, BO10-Dec-2020](https://www.littelfuse.com/assetdocs/switching-thyristor-sxx20x-sxx25x-datasheet?assetguid=7CCAA6CD-4318-4C16-B5CE-306D14D88055),25 A SCR: single half-cycle300 A/50 Hz or350 A/60 Hz at initial25°C; fusing510 A²s at8.3 ms; allowable on-current slew150 A/µs at125°C. Turn-on2 µs is **typical**, at specified trigger/load conditions, not a maximum. Gate current/spreading, holding and recovery still constrain the pulse. No SCR MPN is selected. [ST TYN612 Rev11](https://www.st.com/resource/en/datasheet/tyn612.pdf) offers a smaller cold98 A²s/145 A8.3 ms example; its ratings likewise do not guarantee a hot DC-capacitor pulse.

ASSUMED example: qualified maximum fuse-current integral11 A²s; equal33 mΩ ballast (two series pairs in parallel); crowbar receives the same fuse-fed current. CALCULATED ballast0.363 J /0.09075 J per equal element, plus protected-capacitor discharge and every current bypassing the fuse. Cold SCR ratio510/11=46.364 is only cross-condition sizing arithmetic. Peak/slew/temperature/duration limits must also pass, and a larger circuit integral changes this result. At constant ASSUMED100 A the clearing-integral screen lasts1.1 ms; this is not a datasheet clearing time.

A possible ballast construction to investigate is [Vishay LTO50,50050 08-Dec-2021](https://www.vishay.com/docs/50050/lto50.pdf): TO-220, resistance down to10 mΩ,50 W at case25°C, working-temperature ceiling150°C. Its p3 supplier pulse curve gives an ASSUMED conservative graphical reading around1.3 J/1 ms at the stated cold conditions. The [pulse note50060](https://www.vishay.com/docs/50060/pulsecapabilities.pdf) describes single tests at25°C. The 0.09075 J nominal example fits that cold screen; actual available low-ohm value,±5/10% tolerance, guaranteed hot TCR, parasitic inductance, pulse rise, repetition and mounting remain OPEN. This is a proposed replacement construction, not permission to transfer the cold curve to125°C or to alter the existing ballast.

Energy destination: supplier-coordinated SCR/pulse ballast, fuse arc chamber and an independently rated inductive dump. Each capacitor-bypass pulse is included separately. Use `E_R=R integral(I_R²dt)` and `E_SCR=integral(V_AK I_A dt)`; SCR surge I²t is not resistor energy, and fuse prearc is not total arc clearing. Until the source and maximum clearing time/integral are bounded, **fault energy/current upper bounds and V_Pi,max are OPEN**. The initial OV interval requires the same fast independent clamp argument as A/D/E; a fuse cannot undo an earlier Pi overshoot.

### Timing, supply, normal behavior and remaining blockers

Complete min/max chain: OV→detector/logic→SCR trigger/spreading→effective crowbar→fuse prearc→arc extinction→store/inductor decay is **OPEN/OPEN**. The SCR's typical2 µs cannot replace the historical assumed0.3 µs crowbar action. Retaining a fast MOSFET clamp while a slower SCR/fuse takes over adds a transfer/SOA problem. Supplies must remain qualified through that transfer; an SCR self-holds without gate power only while current exceeds its holding requirement. Brownout can unlatch it and later expose a still-failed buck, so retrigger/arm/reset policy is necessary.

Normal startup/repetitive inrush must survive the fuse pulse derating; nuisance crowbar firing now becomes a destructive consumable event. Trip tolerance/normal voltage margin stays OPEN; fuse loss worsens the5 A margin as calculated. Terminal limits are fixed only through applicable construction/thermal evidence. Removes dependence on electronic latch-off only after independent clearing qualification; leaves B01/B02/B03/M01/M03/M04 and false-fire/reset blockers, with M05 replaced by a larger coordinated pulse/arc problem.

ASSUMED incremental budget: fuse/holder, SCR/trigger, pulse ballast and dump/snubber, roughly12–25 placements plus mechanics; **US$8–35**, excluding common supply fixes and replacement fuses. Exact price OPEN. Bench: hot5 A fuse/holder drop and temperature;9/24 V repeated startup/inrush; minimum and maximum available fault-current short tests; Pi peak before fuse clearing; full DC arc extinction/no restrike; hot SCR turn-on/slew and transfer; gate-power loss/holding/retrigger; eFuse/fuse interaction and pulse repetition. Use fresh fuses/dummy loads; a few successful clearing trials do not replace a supplier clearing maximum.

## Checkpoint status

A/B complete; C/D/E and final comparison/recommendation pending. No schematic change is authorized.
