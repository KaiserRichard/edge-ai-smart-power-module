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

## Checkpoint status

A analysis complete; B/C/D/E and final comparison/recommendation pending. No schematic change is authorized.
