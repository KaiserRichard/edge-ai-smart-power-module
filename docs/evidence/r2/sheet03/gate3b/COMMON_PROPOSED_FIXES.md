# Task 2 — common fixes, proposed only

**Analysis complete; B02/M01/M05 qualification remains BLOCKED.** None of these changes is applied to CAD. The owner decides alone; supplier ratings and measured implementation limits are technical evidence dependencies, not reviewer approval steps.

## B02 — actual min/max endpoints

The table is inherited manufacturer evidence from [Gate2c](../GATE2C_REVIEW_CLOSURE.md); transfer to actual supply/load/temperature is ASSUMED unless specified. Application minima/maxima remain OPEN wherever a condition or endpoint is missing.

| Stage | Manufacturer min / typ / max used as calculation inputs | Actual endpoint/condition |
| --- | --- | --- |
| OV starts → divider settles → comparator overdrive | OPEN / OPEN / OPEN | Sense capacitance, reference dynamics and fault slew; no zero-time substitute |
| TLV3201 falling output | OPEN / 45 / 55 ns | Stated 5 V, 20 mV overdrive, 15 pF; actual rail can be below that test condition |
| QUALIFIED gate | 1 / OPEN / 4.6 ns | Stated 5 V logic/load/full temperature |
| Fault latch asynchronous clear | 1.6 / OPEN / 6.1 ns | Stated 5 V/load; power-up state and brownout separate |
| Crowbar command gate | 1 / OPEN / 4.6 ns | Stated 5 V/load |
| UCC27511 | 4 / 15 / 26 ns at 4.5 V; 4 / 13 / 23 ns at 12 V | Tied outputs and stated load; actual split output/hot gate is different |
| Crowbar gate → useful clamp/current commutation | OPEN / OPEN / OPEN | Threshold voltage is not a high-current clamp endpoint |
| Parallel RUN gate | 1 / OPEN / 4.6 ns | Does not need to await fault-latch output |
| LTC7001 propagation | OPEN / 35 / 70 ns | VCC=BST=10 V, TS=0, 1 nF; loaded bootstrap/actual gate removal OPEN |
| Opposed series FETs → actual current zero/redirected | OPEN / OPEN / OPEN | Gate plateau, parasitics, inductive destination and SOA |
| Q304 → SHDN threshold | OPEN / OPEN / OPEN | Actual drive/current/capacitance |
| TPS26630 after SHDN crossing | 0.8 / 1 / 1.5 µs | Test-conditioned endpoint, not fault-onset→isolation |

`tcrowbar = toverdrive + tcomparator + tQUALIFIED + tlatch + tcommand + tdriver + tgate + tcommutation`

`tseries = toverdrive + tcomparator + tQUALIFIED + tRUN + tdriver + tgateoff + tinterruption`

`tsource = toverdrive_or_independent_fault_trigger + tlogic + tSHDN_cross + tinputoff + tcommutation`.

Each complete minimum/maximum is **OPEN/OPEN**. Parallel paths are evaluated separately; do not add them in series or let a typical fast-short delay replace a missing maximum.

CALCULATED inherited rail/charge screen: at regulated driver minimum 7.440269 V, `26 nC /[(Vrail−4.5 V)/(11+1+1.6 Ω)] =120.261 ns`; partial digital-plus-charge total 216.561 ns. At the ASSUMED/transferred PG floor 6.175423 V, the corresponding gate time is 211.051 ns and partial total 307.351 ns. It already exceeds the historical ASSUMED 300 ns allocation by 7.351 ns, before overdrive and commutation: **BLOCKING**. No complete maximum exists at that floor. The detector PG floor 4.050918 V also fails to establish the cited 5 V timing conditions.

PROPOSED ways back under a justified budget:

1. Replace gross-PG permission with direct loaded-rail qualification and an independent boost/buck driver supply. Use at least the rail for which the selected FET/driver resistance, charge and timing evidence applies; do not interpolate propagation to an untested rail.
2. Feed an independent OV/current fault directly into the fast current-off command; retain a parallel latch for persistent shutdown. Remove unnecessary logic depth only after proving its truth table and reset/partial-power behavior. No PGOOD dependence in the OV detection path.
3. Select FETs jointly for hot RDS, hot SOA and actual required charge. Low RDS can raise gate charge and slow cutoff. Qualify sense-overdrive→useful conduction/current-off with the actual gate/bootstrap/PCB.
4. Allocate timing against the new current/C/ESR bounds. CALCULATED D screen at ASSUMED 80 A, 1 mF, 0.5 mΩ ESR, 5.38 V upper clamp and 20 mV ringing requires useful clamp within 0.75 µs merely to stay below 5.5 V; the proposed 0.5 µs leaves 20 mV. This is not a complete Pi/harness proof. E's new current-slope breaker contract targets 2 µs physical off, independently of its slower OV path; both remain OPEN.

## M01 — directly supervise usable drive and detector rails

PROPOSED: independently supervise the actual driver rail and detector rail, then block ARM/RUN while either is invalid. Bootstrap/source-referenced VGS needs a separately verified bound; a VCC supervisor alone does not guarantee loaded VGS. Passive gate-to-source discharge and a fail-off shutdown request must work when logic is unpowered. Separate stored driver energy and an effective dump path must remain after supply disappearance.

A new driver target above the old rail requires a boost/buck supply at frozen 9 V input; raising the old LDO divider cannot create it. [LTC3115-1 Rev E](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf) is a research candidate, not a validated fault supply. The exact converter, rail accuracy, startup, load, filter and fault supply are OPEN.

ASSUMED hold-up allocation: driver starts ≥11.2 V, useful VCC ≥10.5 V, loaded VGS≥10 V, control≤25 mA, effective C≥47 µF, required duration≥1 ms, aggregate gate charge≤2.036 µC. The charge allocation equals four published 509 nC maxima at their stated cold test conditions if those devices are selected; its hot/application transfer remains OPEN. CALCULATED `Creq=(Icontrol thold+Qg)/ΔV =38.623 µF`; allocation supports 1.23456 ms for 0.7 V droop. Count converter/controller current, leakage, simultaneous gates and clamp/dump drive. Nominal C is not effective C. The original 480 nC /150 µs example is not carried over to these larger-gate candidates.

Supervisor specification must include maximum delay after the specified overdrive and supply slope, threshold tolerance/hysteresis, gate-action latency and rail droop before action. Keep permission valid only while all timing conditions apply. A [TPS3700 SBVS187G, February 2019](https://www.ti.com/lit/ds/symlink/tps3700.pdf) direct-divider monitor is a research candidate, but its propagation figures are nominal, not guaranteed maxima. Its negative threshold includes hysteresis; do not derive UV from only the positive-threshold accuracy. This candidate does not close M01.

A source-stop deadline reduces continuing energy but does not guarantee magnetic decay duration. CALCULATED hypothetical stiff-source decay for 12 µH /80 A at raw clamp 31.5 V versus 28.289211 V is about 299 µs; lower clamp headroom greatly lengthens it. Finite local C/source-off changes the trajectory and must be modeled rather than adding overlapping energy bounds. The 1 ms hold allocation is a proposed reserve, not a demonstrated required maximum. Qualification must cover UVLO, startup, falling input, existing 7.618701–8.168235 V conditional falling UVLO, source hiccup and persistent failed short.

## PG, fault/reset and powered-off sense

PROPOSED logic policy:

- PG pull-ups: both TPS7A16 PG outputs and buck PG use a qualified 3.3 V rail. Verify all VIH/VIL and partial-power pin currents; buffer/translate if 3.3 V does not guarantee a high to the selected 5 V logic. Existing detector upper screen 5.117398 V exceeds the PG recommended 5 V ceiling. Absolute maximum is not permission.
- Independent OV_FAULT/current/clamp-activity latch: PG-low disables RUN/ARM permission but does **not** set the crowbar/fuse fault. Only a qualified OV or dedicated clamp/current event commands disposal and latched source shutdown. A lower active clamp must itself latch isolation if it prevents another OV threshold from crossing.
- Default off and reset: loss of either qualified rail removes RUN and maintains source shutdown until stored energy is safe. A persistent high-side short must not automatically reconnect when PG or supply returns. Full power loss may erase volatile history, so require fresh deliberate ARM; a held ARM signal must not bypass the interlock.
- Powered-off clamp: scale the sense input for the bounded raw fault voltage, add a clamp with a defined return while reference/comparator supplies are absent, and isolate/limit injection into those pins. Do not dump current into an unpowered precision reference or rely on ESD diodes. Include clamp leakage in the new trip error stack and test positive/negative prebias and alternate powered ports.

These are functional proposals, not a captured truth table. Validate races/glitches, manual reset, cold start, ordinary PG loss, healthy brownout, load release, clamp activity, genuine OV plus PG loss, and returned input while the buck remains shorted.

## M05 — ballast terminal and construction

[Vishay WFM, document30387, 2022-08-04](https://www.vishay.com/docs/30387/wfm.pdf) limits the 2512 terminal to 95°C. The inherited ASSUMED 125°C terminal premise exceeds it by CALCULATED 30 K: **BLOCKING** even before a pulse. PROPOSED terminal target ≤85°C leaves ASSUMED 10 K reserve; ambient/enclosure and actual terminal temperature remain OPEN.

Options: retain only with applicable hot pulse/terminal/repetition proof; move to a pulse resistor construction with a real hot rating; or eliminate the main crowbar ballast through an owner-selected disconnect/absorber architecture. [Vishay LTO50 document50050, 2021-12-08](https://www.vishay.com/docs/50050/lto50.pdf) is a construction research candidate, but its cold single-pulse graph is not a hot rating. A new construction trades footprint/mounting/inductance against pulse capacity. Removing ballast transfers the requirement to the active absorber/dump; it does not remove fault energy.

Measure terminals and obtain applicable waveform/pulse/SOA acceptance. Use component energy `integral(V I dt)` and actual resistor current sharing; do not invent MOSFET I²t ratings or allocate exactly one quarter under independent resistor corners. All common fixes remain proposals awaiting the owner's implementation choice and the required technical evidence.
