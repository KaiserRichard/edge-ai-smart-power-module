# Sheet 03 preliminary architecture decision

2026-09-29. **AUTHORITATIVE for this architecture gate.** Earlier dated reviews and the separate conductor/worker branches remain evidence, not competing selections.

**STATUS: BLOCKED — NO DEFENSIBLE ARCHITECTURE SELECTED FOR CAPTURE.**

The analysis gate is complete with a no-go decision. The condition **PRELIMINARY — READY FOR SCHEMATIC REVIEW** has **not** been reached. The user's conditional continuation therefore stops before KiCad capture, implementation commit, or push. **R2 BLOCKED; R3 BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**DECISION:** Retain the open Sheet 03 boundary. A precision, latched detector with independent forward isolation and reverse blocking is the most promising development direction, but its complete circuit and governing transient bounds are not established. A component shortlist or an assumed sub-microsecond switch is insufficient to select that architecture for capture.

**Exact capture blockers:** (1) no supported maximum normal raw-rail excursion and maximum fault let-through for the same L/C/source/load corners; (2) no complete precision-detector/gate/supply/reset circuit with a defensible isolation time and fail-off startup/brownout behavior. These prevent verifying both threshold inequalities and drawing an unambiguous circuit. Final converter identity and a Pi destructive voltage-time curve are **not** prerequisites if an accepted interface bound and the strict 5.5 V peak ceiling can be met.

## 1. Work already present today

**OBSERVATION:** Initial active checkout: `feat/sheet03-output-protection`, HEAD `de1d35c07a0c0a9b368527522aa01ed11c762869`; `git status --short` showed only untracked `.claude/`. Tracked and staged diffs were empty. The active branch's latest commit was September 26. Inspection of `git worktree list`, `git log --all`, worker status/diffs and relevant files found today's work elsewhere:

| Existing work | Exact revision / state | Finding reused |
| --- | --- | --- |
| Conductor `lab/REQUIREMENTS.md`, `DECISIONS.md`, `GATES.md`, `HANDOFF.md` | `b15951ae542901a038b33fe444ac628898855ba1`, branch `lab/state-files` | D-27 replaced the 6 V screen with a 5.5 V Pi limit; D-30 froze normal input, GPIO power and intended runtime loads. No architecture/capture approval. |
| Protection primary-source review and candidate worksheet | `1a08b1a` and `7e78c2aac1bce4a269cf4249dcdb9bdf22de0b76` | Corrected HGATE current, eFuse timing endpoints, gate-stage/reference/clamp gaps. |
| Protection model continuation | `58e9ec048f19f6b2cac11fbe7ec4fbcacbffaee2`, branch `codex/brief02-protection` | Python screening reproduced; SPICE/vendor-model execution explicitly NOT RUN. Option I gives 5.494 V at assumed 0.4 µs isolation and 5.660 V at assumed 2 µs. |
| Candidate-source comparison, margin study, raw-rating follow-up and vendor-run plan | Uncommitted in sibling `v1a-wt-brief02`; file hashes recorded in the [provenance register](../../../../third_party/sheet03_source_register.json) | Several conditional lower-threshold/bulk cases improve numerical margins; the gate stage, reset contract, effective capacitance and real transient bounds remain unclosed. Do not attribute these files to the committed HEAD. |
| Pi input-envelope review | `a4155dd14f9bd5a75fa5adc580874f5e431ccb01`, branch `codex/pi5-input-envelope` | GPIO feed bypasses USB-C OVP; no permitted pulse above 5.5 V established. |
| Connector shortlist | `ea6bf16cd2095b66c49c11b7806c8f6df096877c`, branch `codex/connector-shortlist` | GPIO harness and J502 remain unselected; Phoenix output candidate is a recommendation, not qualification. |

Relevant project files are under `docs/evidence/r2/protection_analysis_2026-09-29/`, `pi5_input_envelope_2026-09-29/` and `connectors_2026-09-29/` on those branches. Their identities and relevant paths are pinned in the register; they were read without merging, editing, or committing their worktrees. No existing authoritative Sheet-03 architecture **selection** file was found. This document consolidates the gate outcome instead of duplicating their reports or rerunning the large model matrix.

**Contradictions resolved:** the old 6.0 V screen is superseded; 5.5 V is a strict rail-peak ceiling, not a detector setting. The old Mean Well 24.72 V case does not specify the future converter. The current user allocates 54.6 V pass-through containment upstream, superseding conductor S1c's previously open responsibility question. The old claim that Option I could combine approximately 5.49 V peak with 2 µs isolation is not supported by today's model. These corrections do not supply the missing physical bounds.

## 2. Consolidated source/load contract

| Quantity / reference plane | State and practical bound | Consequence |
| --- | --- | --- |
| Normal source at V1A input | **REQUIREMENT:** 9–24 V | Test both endpoints. This is neither a surge limit nor an instantaneous short-current bound. |
| Robot source | **REQUIREMENT:** 13S battery → PDB → future HV-to-approximately-12-V converter → V1A | Direct 54.6 V pass-through survival is excluded from V1A; containment belongs upstream. Converter MPN, residual abnormal voltage/time, current response, stored energy and wiring impedance remain **OPEN**. |
| Power path | **REQUIREMENT:** raw buck → Sheet 03 → `VOUT_PROTECTED` → existing 2 mΩ Kelvin shunt → `LOAD_5V1` → J502/harness → Pi 5 GPIO 5 V pins 2/4 and multiple GND pins | USB-C is not the V1A power route. No USB 3.x/D435i data routing on this PCB. J502/socket/wire implementation is **OPEN**. |
| Output envelope | **REQUIREMENT:** up to 5 A total through V1A | Includes the intended Pi/camera load. Historical 6 A/100 ms is not a new guaranteed mode. |
| Pi peak | **REQUIREMENT:** `V_Pi_peak < 5.5 V`, including transients | No pulse above this value is credited. Include local ringing and measurement/model uncertainty. Do not credit harness resistive drop at no load. |
| Raw DC regulation | **CALCULATION:** nominal 5.098361 V; existing static screen 5.038271–5.158632 V | Derived from captured feedback/reference tolerances, not a full normal-operation bound. Add ripple, line/load regulation, leakage, startup and load-release excursions. Sheets 01/02/04/05 remain unchanged. |
| Normal raw maximum | **OPEN:** `V_N = 5.158632 V + positive dynamic/error allowance` | Must establish `V_N + M_N < V_trip,min`. A 50 mV `M_N` is a retained **ASSUMED review allocation**, not a user requirement or measured noise bound. |
| Pi normal minimum / path | **OPEN** formal floor and droop allocation; retain 4.75 V and 100 mV droop as **ASSUMED screens** | Total hot loop budget is 57.654 mΩ static, or 37.654 mΩ with that droop reserve. Includes both polarities, FETs, shunt, copper, all contacts/joints and wire. No automatic setpoint increase. |
| Qualification loads | **REQUIREMENT:** idle, sustained CPU-heavy Pi 5, Pi 5 + operating D435i, representative steps within 5 A | Step slew/repetition, camera mode/power route, startup demand and actual minimum idle current **OPEN**. Use 0→5 A and 5→0 A as conservative analysis stimuli, not measured runtime waveforms. |
| Buck failure | **HYPOTHESIS:** high-side short while source remains at a valid 24 V | Independent output protection must cope; input OVP need not trip. Fault rise depends on input capacitor discharge, failed-switch impedance, L201 saturation, raw C/ESR/ESL and load release. No bounded fault slew/current follows from 9–24 V alone. |
| Capacitance before switch | **OBSERVATION:** six nominal 22 µF raw MLCCs. 60–130 µF and 85.272 µF are earlier **ASSUMED effective-C screens** | No guaranteed combined minimum. Added bulk must remain upstream of the disconnect and satisfy fault voltage, stability, startup/inrush and ripple limits. Nominal 470 µF is not 470 µF minimum. |
| Capacitance after switch | **OPEN:** protected-node + harness + Pi effective C/ESR/ESL | Historical 2–220 µF load sweep is an assumption. Raw capacitance does not hold up the Pi after isolation. Harness magnetic energy can still reach the load after the switch opens. |
| Reverse feed | **PROPOSED policy:** block sustained LOAD→raw current; quantify leakage and finite reverse pulse separately; do not authorize simultaneous Pi USB-C/GPIO sources | Keep externally precharged load as a required analysis state. Historical ≤100 µA into raw with external load ≤5.25 V is an **OPEN proposal**, not guaranteed or newly frozen. External overvoltage injected directly at the Pi is outside an upstream disconnect's protection capability. |
| Startup/fault/recovery | **PROPOSED policy:** forward FET off until detector/reference valid and raw in range; OV latches off; deliberate qualified reset; no automatic OV retry | Brownout or buck/eFuse hiccup must not silently reset and re-energize a faulty rail. Exact enable, inrush and reset circuit remains **OPEN**. Telemetry may lose power; it cannot supply the independent detector. |

**CALCULATION:** `V_Pi,min = V_raw,min − 5 A × R_loop,hot − ΔV_droop`. With the provisional floor/droop above, `(5.038271−4.75−0.100)/5 = 37.654 mΩ`. The existing shunt alone contributes nominal 10 mV / 50 mW. A 7.2 mΩ switch pair would leave approximately 28.45 mΩ after also subtracting the nominal 2 mΩ shunt, for all remaining copper/harness/contact loss. This does not qualify J502.

## 3. Three realistic candidates

All parts below are **candidates**, not a selected BOM. Manufacturer documentation and production/product pages are in the register. Availability means listed orderable/production products, not confirmed local stock, pricing or procurement approval.

### A — native LM74800 overvoltage cutoff

**Mechanism/topology:** `LM74800QDRRRQ1`, two `PSMN1R8-40YLC` N-channel MOSFETs in common-drain configuration: Q1 source=raw, drain=MID; Q2 drain=MID, source=protected. Q1 body diode points raw→MID, Q2 body diode protected→MID. DGATE controls reverse blocking, HGATE controls forward isolation; VS/C at MID and raw-sensing OV divider. No single FET provides both off-state blocking directions.

**Threshold network screen:** 33.7 kΩ top / 10.0 kΩ bottom, each ±0.1% initial tolerance; nominal 5.379470 V. Detector 1.195/1.231/1.267 V and conservative ±200 nA leakage allowance yield **5.207357–5.552085 V**, before resistor temperature/noise effects. Even the static high trip exceeds 5.5 V. This pair is a rejected calculation example, not a resistor selection.

**Behavior:** internal undervoltage/charge-pump sequencing precedes gate enhancement; intended startup is off, but a complete application still needs power-loss gate-state verification. OV opens HGATE and automatically recovers at its falling threshold; it does not latch. Native reverse control is useful but has finite response, and external prebias can power MID through Q2's diode without creating a diode-only path back to raw.

**Timing:** manufacturer maximum OV-to-HGATE-start deglitch is 5.4 µs at its test conditions. HGATE sink minimum 168 mA and source maximum 75 µA are different from DGATE's stronger reverse sink. `96 nC / 168 mA = 0.571 µs` is a **typical-charge quotient**, not a turn-off bound; approximately 5.97 µs is consequently only a screening chain. EN deglitch can itself be 6 µs and is not a fast precision shutdown solution. Latest old-divider model peak is 8.372 V; it does not represent the newly screened divider.

**Disposition:** reject as sole Pi OVP for this gate. With the retained 50 mV normal margin, even ideal resistors/no leakage/no delay give an incompatible window (§4). Removing that allocation does not establish a usable dynamic window.

### B — LTC4368 cutoff and bidirectional circuit breaker

**Mechanism/topology:** `LTC4368HMS-2#PBF` and two `PSMN1R8-40YLC` in the manufacturer's common-source arrangement: first drain=raw, sources joined, second drain=SENSE, then a separate candidate 8.2 mΩ breaker resistor to protected/VOUT. GATE drives both FETs. This resistor is additional to R401; R401 is not moved or shared. Independent raw UV/OV dividers and a gate-slew network are required.

**Threshold screen:** OV top 96.5 kΩ / bottom 10.0 kΩ, ±0.1%, 0.4925/0.5000/0.5075 V threshold, ±10 nA leakage → **nominal 5.325000 V; 5.234663–5.415646 V** before resistor drift/noise. Raw upper normal bound would need to stay below 5.184663 V with the assumed 50 mV margin. The UV setting and gate RC remain OPEN pending normal/startup bounds.

**Behavior:** gates stay off on invalid input; valid-input turn-on delay is 22–45 ms under the specified 12 V test. UV/OV automatically recover; selecting overcurrent latch behavior does not create an OV latch. At 8.2 mΩ, nominal forward/reverse breaker points are +6.10 A / −0.366 A. This is finite reverse-current interruption, not ideal-diode blocking; a simultaneous external source can feed backwards before trip. Reverse-current allowance and OV retry policy therefore require further circuitry/review.

**Timing:** UV/OV propagation maximum 2 µs is tested at VIN=12 V and **50 mV sense overdrive**. Gate fast-off maximum 6 µs uses 2.2 nF; their endpoints and actual two-FET loading must be reconciled before adding them. At the example divider, 50 mV sense overdrive is **0.5325 V raw**. The cited timing condition is already beyond the available 84.354 mV static headroom. This does not mean the part waits for 50 mV; it means that specification does not prove sufficiently early action here. SHDN also has a slow turn-off path and cannot substitute for a qualified fast input.

**Loss/stress:** conditional pair loss 0.180 W at the 4.5 V/hot resistance screen below, plus 0.205 W / 41 mV in an 8.2 mΩ resistor: **0.385 W / 77 mV at 5 A**, excluding copper/tolerance. The controller's wider input rating does not change the 40 V FET limit or establish hot linear SOA.

**Disposition:** static window exists, dynamic/reverse/recovery compliance is not demonstrated. Not selected; no guaranteed peak or 5 V isolation time can be assigned from the cited table.

### C — precision latched detector with separately driven forward FET

**Development topology:** retain a common-drain opposing FET pair and ideal-diode control of Q1; give Q2 a dedicated source-referenced fast driver. Sense raw with an independent reference/comparator; latch a fault before enabling the driver. This addresses the incomplete discrete HGATE pull-down in today's Option I worksheet.

**Concrete candidate parts:** `LM74800QDRRRQ1` for Q1 reverse control; 2 × `PSMN1R8-40YLC`; `REF5025IDGKR` high-grade reference; `TLV3201AIDBVR` comparator; `SN74LVC1G74DCTR` asynchronous latch; `LTC7001IMSE#PBF` forward driver; a dedicated high-voltage `TPS7A1633DGNR` detector supply candidate. The detector supply is taken upstream of the disconnect, never from `3V3_LOCAL`. `LTC7001` TS connects to Q2 source/protected, TGDN to Q2 gate for fast off and TGUP through the reviewed turn-on network. Its gate must **not** also be connected to LM74800 HGATE. The unused LM74800 high-side interfaces, driver supply/UVLO, clamp, validity supervisor and reset interlock need a completed application circuit. This is not an authorized pin-level implementation.

**Why credible:** LTC7001 provides a manufacturer-supported floating gate pull-down and separate slow-on/fast-off connections (Rev G, Figure 5), avoiding the proposed ground-referenced HGATE shunt that violates `HGATE ≥ OUT−0.3 V`. Its input-to-output delay maximum is 70 ns under its 10 V/1 nF test, pull-down resistance maximum 4 Ω under the 12 V test. Its 10 nF fall-time number is typical. These are **not** isolation guarantees at an as-yet unselected driver supply or nonlinear MOSFET load. A 3.3 V detector LDO cannot be assumed to run that driver; the supply implementation remains OPEN.

**Precision screen:** TLV3201 has a ±4 mV full-temperature offset limit and 5 nA bias limit under specified conditions, improving on the earlier TLV3501/TLV3601 budget problems. At 5 V its specified delay reaches 55 ns over temperature for the stated overdrive/load; 20 mV overdrive must be explicitly budgeted. Built-in hysteresis is only typical in the reviewed table. REF5025 high-grade initial ±0.05% and 3 ppm/°C drift give a 0.0495% full-span box-method drift screen, not proof of the complete detector error. Reference line/load/headroom, rising-threshold hysteresis, clamp leakage, resistor drift and startup validity remain OPEN. The earlier 3.3 V reference-supply headroom concern is preserved.

**Provisional values for numerical evaluation only:** 11.2 kΩ / 10.0 kΩ, ±0.05% initial, gives 5.300 V from 2.500 V. Reusing the old **ASSUMED total ±0.671% allocation** yields 5.264437–5.335563 V; it is not a derived bound for these parts. A 20 mV sense-overdrive allowance adds 42.4 mV at raw, giving an effective high detection point of **5.377963 V**. No final threshold/hysteresis/filter/clamp network is selected.

**Bulk/startup:** today's Nichicon candidate `PCH1V471MCL1GS` is 470 µF/35 V. Two in parallel give 940 µF nominal, 752 µF at initial −20%, or 601.6 µF under the study's sequential 0.8×0.8 endurance screen. That is not a guaranteed 1 mF bank. A complete minimum across temperature/life/frequency and stability must be established. Additional capacitance may help fault rise while worsening startup current; changing only C cannot close the gate.

**Behavior intended:** Q2 off at startup/supply invalid, fault sets latch asynchronously, bounded turn-on only after detector/reference/raw validity; sustained reverse flow blocked by Q1; latched fault retained through buck hiccup; deliberate reset with fault still dominant. A raw-fed latch that resets whenever raw collapses can automatically retry while J501 remains energized. Neither the listed flip-flop nor a delay capacitor resolves that state problem by itself.

**Disposition:** promising conditional window, **not selected**. Actual delay/peak, default-off hardware, fault-sense input protection, reference-valid startup and reset implementation are OPEN. These are capture-defining details, not merely later fabrication qualification.

### Shared MOSFET evidence and stress

**EVIDENCE:** Nexperia's 22-Aug-2012 PSMN1R8-40YLC datasheet specifies 40 V class VDS and ±20 V VGS. At 25 °C, maximum RDS(on) is 1.8 mΩ at 10 V or 2.1 mΩ at 4.5 V; at 150 °C the corresponding table maxima are 3.25/3.6 mΩ (25 A test). Thus a two-device **conditional conduction screen** at 5 A is **90–162.5 mW / 18–32.5 mV** for the 10 V rows, or **105–180 mW / 21–36 mV** for the 4.5 V rows. Use actual guaranteed gate drive, temperature and current dependence before promoting this to a circuit bound. LM74800 ideal-diode regulation can add drop at low current. Copper/driver supply loss and R401 are separate.

**New source clarification:** 96 nC total gate charge is **typical**, not a maximum. The hot 3.25 mΩ table value previously carried as unverified is now supported at its stated test point; it does not prove the assumed gate drive or SOA.

**OPEN RISK:** the forward FET can see essentially the entire raw fault voltage when protected is discharged, not half the voltage across the pair. Cold breakdown evidence is lower than the room-temperature 40 V value; select ratings against the approved minimum-temperature envelope. Include raw-bank/inductor overshoot, gate-source ringing, Miller re-turn-on and downstream harness energy. A 35 V bulk bank may become the first rating constraint. No 24 V nominal or upstream-OVP number proves these peaks are below ratings. Compare startup/interruption `VDS(t), ID(t), duration, initial Tj` against derated SOA and thermal impedance; pulsed-current/avalanche headlines are not an SOA proof. None of the candidates is qualified for these trajectories.

## 4. Threshold and let-through calculations

Results are reproduced in [CALCULATIONS.json](CALCULATIONS.json); equations below define their scope. All dynamic allocations are **ASSUMED**, with no new simulation or measurement claimed.

For divider top `Rt`, bottom `Rb`, resistor tolerance `e`, detector bounds `VL,VH` and input-current magnitude `Ierr`:

```text
Vtrip,nom = Vref,nom × (1 + Rt/Rb)
Vtrip,min = VL × (1 + Rt(1−e)/[Rb(1+e)]) − Ierr Rt(1+e)
Vtrip,max = VH × (1 + Rt(1+e)/[Rb(1−e)]) + Ierr Rt(1+e)
V_N + M_N < Vtrip,min
Vtrip,max + ΔV_overdrive + ΔV_let-through + ΔV_local + M_P < 5.5 V
```

The signed leakage treatment conservatively permits both directions. Initial resistor tolerance is included; unspecified drift/noise is not. `M_P` must cover remaining design/measurement uncertainty; no exact value is frozen. Overdrive is included once, either as a voltage allowance or in a supported timing law, never counted twice.

| Candidate / screen | Nominal / minimum / maximum trip (V) | Static margin over 5.158632 V | Headroom below 5.5 V | Window conclusion |
| --- | --- | --- | --- | --- |
| A example divider, with leakage | 5.379470 / 5.207357 / 5.552085 | 48.725 mV | **−52.085 mV** | Infeasible even before delay |
| A optimized ideal divider, no errors other than detector | Lowest possible high trip is `(5.158632+0.050)×1.267/1.195 = 5.522458` | Assumed 50 mV at low trip | **−22.458 mV** | No solution under that margin allocation; with zero margin the ideal infimum is 5.469445 V, leaving only 30.555 mV before all other errors/dynamics |
| B example divider, with leakage | 5.325000 / 5.234663 / 5.415646 | 76.031 mV | 84.354 mV | Static possibility; timing specification is not applicable at the small available overdrive |
| C **allocated**, incomplete error budget | 5.300000 / 5.264437 / 5.335563 | 105.805 mV | 164.437 mV static; **122.037 mV** after 20 mV sense overdrive | Conditional possibility, not an achieved window |

**Useful contract for C:** with that allocated threshold, `V_N < 5.214437 V` would preserve the assumed 50 mV nuisance margin. If local turn-off ringing is allocated 20 mV, the remaining allowable rise after effective detection is **102.037 mV minus M_P**. At assumed 2 µs isolation this requires average rise **<51.019 mV/µs** before reserving `M_P`; at 0.4 µs, **<255.093 mV/µs**. These are constraints on a future circuit/source envelope, not facts about V1A. For comparison, 0.1 V/µs for 2 µs plus that 20 mV local term predicts **5.597963 V**, which fails.

**Charge formulation:** after effective detection, require `integral(max(I_into_load−I_load,0) dt)/C_down,min + ESR/ESL/ringing terms < remaining headroom`. If downstream C is only the assumed 2 µF, 102.037 mV corresponds to only **0.204074 µC**, before `M_P`. The actual coupled raw/load network must determine current and capacitance participation while on; downstream harness inductance and parasitic coupling can continue charging the load after opening. Do not simply put all raw C in the post-isolation denominator.

**Fault-rise example, independent arithmetic:** for a 24 V high-side short, ideal constant 6.8 µH, initial 5.158632 V and zero initial excess capacitor current,

```text
V(t) ≈ V0 + (Vin−V0)t²/(2LC)
t_to_trip ≈ sqrt[2LC(Vtrip−V0)/(Vin−V0)]
ΔV_after_trip ≈ (Vin−V0)[2 t_to_trip t_iso + t_iso²]/(2LC)
```

At an illustrative 5.4 V trip, effective C=560 µF and 2 µs isolation, this gives **107.640 mV** further rise → **5.507640 V**. Using only `t_iso²` would incorrectly erase the inductor current built up **before** threshold. This approximation ignores saturation, ESR/ESL, finite source impedance and load release and is neither a worst-case proof nor a replacement for today's detailed model. For C=85.272 µF and 5.4 µs after the same trip it gives approximately 6.550 V, illustrating sensitivity.

**Existing model evidence, kept distinct:** the committed model uses an assumed 24.72 V source and nominal initial rail, not the frozen future source contract. Its Option I fixed high-trip 5.46 V gives **5.494228 V** at 0.4 µs and **5.660136 V** at 2 µs. The uncommitted exact-window recalculation instead uses 5.4594 V and gives approximately 5.493642/5.659484 V; these small differences are inputs, not a contradiction. Another uncommitted case (5.3 V, ±1.1%, 1 mF effective bulk, 0.4 µs) gives approximately 5.385 V with a model-only 55 mV nuisance margin. None is vendor SPICE, a bound, or validation. The old ±3% model-agreement tolerance is about 165 mV near the limit and cannot qualify a 6 mV margin.

**Normal release/startup:** an optimistic zero-extra-input-energy release estimate is `Vpeak = sqrt(V0² + L Ipk²/C)`, with ESR step and loop energy added separately. Continued buck switching can raise it further. Today's study estimates 5.1867 V with 1 mF bulk, but omits bulk ESR in that release formula. It therefore cannot establish `V_N`. The same study's 1 mF startup screen gives 4.342 A input at 9 V / assumed 3.5 ms ramp / 5 A connected load, above the source-reviewed approximately 4.181 A minimum eFuse limit; even its 7 ms case gives 3.799 A versus a proposed 90%-limit allocation of 3.763 A. These are conditional warnings that load sequencing, maximum capacitance and inrush/SOA must be designed together. Do not add bulk and assume startup is unchanged.

## 5. Failure-independence review

| State / failure | A | B | C development direction |
| --- | --- | --- | --- |
| Raw rises after buck control/power-stage fault | Its separate comparator remains functional only while its own pins/supply stay within ratings; threshold/delay rejected above | Separate raw-powered controller, but timing/overdrive proof absent | Separate reference/comparator is independent of buck control; dedicated supply and raw-sense clamp must survive the same rise |
| Detector power disappears | Manufacturer UVLO shutdown is useful; do not equate eventual gate discharge with guaranteed isolation during collapse | Native invalid-input shutdown; actual gate/current decay and prebias need verification | Driver enable must be forced low and Q2 gate clamped to its source without relying on powered logic; no complete implementation yet |
| Body-diode bypass | Opposed common-drain diodes block a diode-only through path when off | Opposed common-source diodes block a diode-only through path when off | Same common-drain orientation as A; Q2 forward isolation and Q1 reverse control must remain independent |
| External Pi/load energized | Reverse comparator responds after a finite transient; leakage via FET/controller/sense networks remains to budget | Reverse breaker deliberately permits current until its threshold/delay; not acceptable to claim zero backfeed | Q1 ideal diode can block sustained reverse flow; detector/input/driver parasitics and partially powered states still OPEN |
| Startup with raw already overvoltage | Must prevent HGATE enable; no credit from buck PGOOD | UV/OV sequencing must prevent enable; finite response remains | Detector/reference-valid hardware must precede Q2 enable. A reference ramping from zero or undefined latch output must never create a bypass interval |
| Repeated/hiccup fault | OV auto-recovery can re-expose load | UV/OV auto-recovery can re-expose load | Desired latched-off policy; raw-fed latch reset on eFuse/buck collapse defeats retention unless input-presence/reset interlock is added |

**Hard rejections:** detector powered solely from `3V3_LOCAL`; a forward-blocking single FET credited with reverse isolation; a gate pulled to ground while its source remains high; use of LM74800 EN as an assumed sub-microsecond off input; direct low-voltage comparator sensing of the fault rail without rated scaling/clamping; automatic re-enable credited as a latch. None may be captured as a shortcut.

For example, C's nominal 11.2 kΩ/10 kΩ divider produces **11.321 V** at its sense node with a 24 V raw rail. A 3.3 V comparator cannot tolerate that unprotected. Adding a clamp changes leakage, propagation, power injection and reset behavior and therefore must appear in both the threshold budget and the state review. A high-voltage LDO alone does not solve sense-pin survival.

`BUCK_INPUT_PGOOD` in the captured project is U101→U201 enable; U201's own PGOOD is currently NC. Neither is independent proof of safety after U201 fails. Any future buck-PGOOD connection is only sequencing assistance, must use a bounded pull-up domain, and must not override the independent detector. No hierarchy/sheet changes are made here.

## 6. Decision and minimum next gate

**DECISION:** no selected architecture, selected resistor network, approved timing chain, or guaranteed worst-case Pi peak. Candidate A is rejected as sole OVP; B remains unsuitable without new timing/reverse/recovery evidence; C is retained only as the focused development direction. Do not mislabel unresolved architecture as later fabrication qualification.

**Minimum next action:** one bounded R2 follow-up must close a **complete Candidate-C circuit and its input/output transient contract**, using today's evidence rather than restarting the audit:

1. Establish a conservative analytical/model envelope for maximum normal raw excursion and fault charge/slew through isolation, with stated source impedance/current/capacitor bounds, minimum L at relevant current, effective raw/downstream C and load-step slew. The final auxiliary-converter MPN may stay OPEN if its acceptance limits are explicit. Do not assume the eFuse's nominal limit is instantaneous. Meet the strict Pi peak ceiling without relying on an undocumented damage-time allowance.
2. Finish the detector supply/input clamp, rising-threshold budget, floating driver supply/gate network, fail-off validity logic and deliberate reset circuit. Verify an actual maximum threshold-to-isolation endpoint (including overdrive/Miller/current commutation), and startup/fault SOA against that envelope. The new LTC7001 direction is a source-backed lead, not a pre-approved replacement.
3. Review the two inequalities and all power states together. Only a successful decision update to **PRELIMINARY — READY FOR SCHEMATIC REVIEW**, with no critical unresolved requirement, enables the user's next gate: **single-agent KiCad capture of Sheet 03 + ERC/netlist/diff validation**.

J502 exact selection, final converter procurement and physical R5 waveform/thermal measurements can remain later OPEN items once their design acceptance bounds are established. Physical bring-up remains visual/short checks → current-limited supply → no-load rail → dummy-load steps → thermal/ripple/transient/fault → telemetry → SBC integration. No expensive Pi is used as the first load.

## 7. Evidence, provenance and validation

Manufacturer documents were referenced, not copied into a circuit. Source URLs, exact revisions, relevant sections, copyright/license limits, cache identities, required attribution and modifications (none) are in [third_party/sheet03_source_register.json](../../../../third_party/sheet03_source_register.json). New primary PDFs were readable through the official web PDF service; direct Python acquisition failed certificate verification, so no downloaded original/hash is claimed for those documents. Attempts are recorded in ignored `third_party/documents/sheet03_2026-09-29/`. Existing originals in the protection worktree were reused in place. No upstream reference source or system trust configuration was modified.

Supporting arithmetic and snapshot identities are in [CALCULATIONS.json](CALCULATIONS.json). **Validation:** repository integrity PASS; 10 existing tests PASS; retained-netlist capture checker PASS with R2 RELEASE BLOCKED; existing R2 calculator executes successfully; independent decimal corner enumeration encloses the A/B threshold intervals; nine reused original-document hashes and 17 project-evidence snapshots verified. All 13 hardware/library files match the preservation hashes. The retained netlist has 71 entries / 47 nets, with raw/protected on separate nets 35/36. No PCB exists; `git diff --check` passes.

Fresh ERC/netlist/PDF exports were not run because the capture continuation was not entered. The retained ERC has one legitimate U402.1 undriven-power error; no fresh ERC PASS is claimed. This gate changes documentation only. No KiCad edit, Gerber, component purchase, commit or push is performed. Repository/capture checks establish preservation, not electrical qualification.
