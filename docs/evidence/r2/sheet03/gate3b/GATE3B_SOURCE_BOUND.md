# Gate 3b — V1A Sheet 03 source bound

**Analysis complete; source qualification BLOCKED. Recommend neither D nor E for implementation approval yet. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** The owner decides alone; no senior reviewer or reviewer approval is required. Architecture choice does not replace missing electrical evidence.

Branch `feat/sheet03-gate3b-source-bound`, based on `65a8698`. Work is analysis only. No `.kicad_sch`, `.kicad_pcb` or `.kicad_sym` file was opened or saved. All new authored files stay under this directory. The accidental path-budget task was skipped; the resistance work below is only the Gate 3b E feasibility check.

Frozen requirements: input 9–24 V; GPIO Pi power D-30; Pi peak strictly below 5.5 V including let-through; Pi at least 4.75 V at 5 A; normal maximum plus the approved margin below trip minimum; trip maximum plus let-through below 5.5 V. The likely upstream 48→24 V converter remains OPEN. No setpoint, architecture, parts or wiring is changed here.

Numeric discipline: **ASSUMED** identifies a proposed allocation, graph reading or unqualified application transfer. **CALCULATED** identifies arithmetic under named assumptions/tolerances/source conditions. **OPEN** identifies a missing applicable bound. Published manufacturer specifications are cited with conditions; a typical curve or tested gate endpoint does not prove an application maximum. Every negative margin/domain failure remains BLOCKING. Application current, voltage, energy and reaction minima/maxima remain `null` where unknown.

## OWNER EXPLANATION — one page

The recommended development route is **b: stop incoming energy with an independent timed input stage, control the local input capacitor bank, and qualify the larger 10 µH metal-alloy L201 candidate**. It is not yet a qualified circuit. A buck high-side transistor that fails short permanently joins the input to L201 and the output. Normal switching control cannot turn that short off. The input capacitors already downstream of an input limiter discharge through the failed switch; stopping the upstream supply does not remove that stored energy.

An inductor limits how fast current rises: `di/dt=VL/Ldiff`. Saturation reduces its differential inductance, so nominal inductance is insufficient for a fault. Manufacturer curves were found beyond 60 A for three real parts, but all are much larger than the present part. The 10 µH alloy candidate's typical curve is about 8.4 µH at 60 A and 6.6 µH at 100 A. Those are **ASSUMED graph readings**, not guaranteed hot/lot/fault limits. The proposed acceptance envelope is **ASSUMED Ldiff≥5 µH through 100 A**, with upper L≤12 µH and initial healthy current≤8 A. Larger L lowers ripple, but can also violate the buck's low-ripple guideline and worsen load-release overshoot; its control behavior must be qualified.

Energy accounting makes the proposal concrete. **ASSUMED** effective local C≤30 µF, physical source-off≤10 µs and positive replenishment charge≤100 µC give, at the **CALCULATED inherited conditional OVP corner 28.289211 V**:

`Enew≤0.5 C Vin² + Vin Qsource +0.5 Lmax I0²`

`=12.004+2.829+0.384 =15.217 mJ`.

With the proposed L floor, `Ipeak≤sqrt(2Enew/Lmin)=78.018 A`, **CALCULATED within that ASSUMED contract**, rounded to an 80 A design target. At normal 24 V the same screen is 67.599 A. No finite actual fault-current maximum is claimed: the magnetic floor, charge, cutoff and source-voltage ceiling are still OPEN. A nominal OVP setting is not a physical clamp during its delay. Persistent leakage/retry energy also needs a separate continuous dissipation contract.

Charge is `integral(I dt)`, and its boundary matters. The proposed 100 µC limits replenishment into the buck input; local caps can still produce a **CALCULATED output-inductor charge envelope of 362.892 µC over 10 µs** at the conditional upper corner. The initial raw output capacitor bank adds an **ASSUMED/CALCULATED 84.648 mJ**. That bank can discharge downstream while bypassing L201, so it needs its own current path and dump rating. A proposed 0.2 J hot dump capacity is a component requirement, not an existing rating.

D puts the disconnect/absorber at the module, so it still must control raw-bank bypass and the coupled module-capacitor/harness/Pi-capacitor trajectory. E puts the final stage at GPIO, but enforcing its proposed 10 A limit needs a real current breaker, a qualified last-path choke and no bypass charge. A concrete controller/choke contract and **CALCULATED 49.613 mΩ** hot-loop target were developed, but the actual magnetic, contact, gate and timing limits remain OPEN. The larger components and extra control power trade space/wiring against measurable bounds. The defensible owner decision now is to fund/choose those qualification steps, not approve either architecture as electrically closed.

## Numbers and evidence table

| Item | Classification / inputs | Result and consequence |
| --- | --- | --- |
| Input screens | REQUIREMENT normal 24 V; requested nominal OVP 27.63 V; CALCULATED inherited resistor/leakage corner 28.289211 V | Actual cutoff-transient/source ceiling OPEN. [Baseline](BASELINE_AND_SCOPE.json). |
| Published replacement candidates | ASSUMED graph readings; manufacturer curves/conditions cited | 7443763540068 ferrite, 74437636350652 alloy, 74437636351002 alloy; traces past 60 A, all large THT. No guaranteed Ldiff envelope. [Part/normal/fault comparison](INDUCTOR_CANDIDATES.md). |
| Gate 3's old 60 A box | CALCULATED using ASSUMED Cin 20 µF /Q 150 µC /I0 = 6.1 A /Lmin 5.44 µH | 59.135 A at 24 V; about 66.2 A at 27.63 V. The old through-60-A qualification premise fails at OVP corners. |
| Proposed source envelope | ASSUMED Cin 10–30 µF; Q+≤100 µC; actual source-current off≤10 µs; Ldiff 5–12 µH through 100 A; I0≤8 A | All applicable maxima remain OPEN. LTC4218 is outside requested voltage range; timed TPS26630 or higher-voltage hardware stage needs qualification. [Limiter/cap comparison](INPUT_LIMITER_AND_ENERGY.md). |
| New source energy/current | CALCULATED under that contract | 24 /27.63 /28.289211 V: 11.424 /14.598 /15.217 mJ and 67.599 /76.415 /78.018 A. Replenishment and output-inductor charges are different. |
| Keeping existing local bank | CALCULATED under ASSUMED 60.996 µF upper screen, otherwise same proposed contract | About 105 A at upper corner exits the 100 A model domain: BLOCKING for this contract. |
| D receiving store | CALCULATED source/raw plus ASSUMED module Cmax 1.5 mF at initial 5.5 V | 122.553 mJ subtotal; Pi Cmax/cable stores/receiving peak OPEN. Protected 80 A /2 µs subcase≤160 µC /0.8768 mJ requires independent raw-bank current qualification. |
| D module/Pi peak | CALCULATED with separately ASSUMED 80 A protected arrival and 0.5 µs active clamp; inherited two-cap sensitivity | Module 5.480 V /+20 mV; Pi sensitivity 5.542140 V /−42.140 mV BLOCKING. Actual Pi maximum OPEN. |
| E arriving-current mechanism | ASSUMED full breaker trip≤8 A, actual off≤2 µs, maximum positive VL≤31.5 V, Ldiff≥35 µH through 10 A | CALCULATED 9.8 A before unsensed injection. TPS48111 candidate test max does not prove the complete 2 µs endpoint. Actual 10 A limit OPEN. |
| E receiving energy | CALCULATED under ASSUMED 10 A /5 µs /5.42 V and lastLmax 50 µH | Initial-interval arrival charge ≤50 µC; total protected charge OPEN; energy ≤2.771 mJ; source/raw initial packet 99.865 mJ; adding Pi Cmax 1.5 mF and initial last-L current ≤8 A gives 124.153 mJ as a subtotal before other cable/input stores. Hot ratings OPEN. |
| New trip and clamp | ASSUMED full rising trip 5.300–5.340 V, clamp 5.30–5.40 V with total overshoot≤20 mV | No inherited 5.356563 V credit. Actual full trip/clamp/timing OPEN. New last-choke tail gives a 5.632 V sensitivity even with ideal source opening: active absorber required. [D/E re-score](D_E_RESCORE.md). |
| E loop | CALCULATED with ASSUMED contact/FET/shunt/choke targets | 49.612741 mΩ /Pi 4.790208 V. Only 0.387259 mΩ spare to 50 mΩ goal. Adding 10 mΩ to unchanged loop gives 4.711433 V: BLOCKING. |
| B02 /M01 | CALCULATED inherited PG-floor charge transfer | Partial307.351 ns already exceeds old 300 ns allocation, without settling/commutation. Actual chain min/max OPEN. Proposed rail/logic/hold-up fixes detailed in [common fixes](COMMON_PROPOSED_FIXES.md). |
| M05 | Published terminal 95°C; inherited ASSUMED 125°C | CALCULATED −30 K terminal margin: BLOCKING. Proposed ≤85°C or applicable new construction; hot pulse proof OPEN. |
| Raw-node normal nuisance | CALCULATED with ASSUMED larger L/6 A /20 µs box and new trip-min 5.300 V /10 mV reserve | +19.685 mV; 30 µs gives −5.249 mV;8 A /20 µs gives −18.794 mV. Negative cases BLOCKING; added E choke/GPIO healthy release remains OPEN. |

Every complete fault/OV→physical isolation minimum/maximum is OPEN/OPEN; the finite times above are target/model inputs. The linked documents provide exact conditions, full reaction/curve-domain calculations, destinations, startup/UVLO policies and tests. [Reproducible JSON](SOURCE_BOUND_CALCULATIONS.json) and [calculator](calculate_source_bound.py) retain those distinctions.

## DECISIONS FOR THE OWNER

Each decision is yours alone. Recommendations are development choices; they neither apply a schematic change nor convert an OPEN limit into a confirmed rating.

| Decision | 2–3 options and consequences | Recommended option and reason |
| --- | --- | --- |
| 1. Approve a containment architecture now? | **D now:** simpler packaging, but raw-bank current and Pi/harness peak unresolved. **E now:** local protection plane, but 10 A/full trip/normal path unresolved. **Neither yet:** retain electrical BLOCKED while qualifying source and remaining receiving paths. | **Neither yet.** Neither has an applicable worst-case proof; choosing one now cannot close the shared prerequisite. |
| 2. Source-bound method | **Inductor alone:** slows rise, no finite energy without timed shutdown. **Timed hardware source isolation +controlled C +qualified L:** bounds replenishment and local stored energy. **Passive source choke before final input FET:** may bound charge analytically but adds loss/energy/filter/commutation work. | **Timed source isolation +controlled C +qualified L.** It explicitly accounts for the capacitor the limiter misses and has a measurable charge/off-time acceptance contract. |
| 3. Replacement-inductor tradeoff | **Keep 8 mm part:** smallest, missing high-current evidence remains. **Large 6.5/6.8 µH parts:** similar normal ripple; softer alloy or ferrite knee require different floors. **Large 10 µH alloy:** best researched 5 µH through 100 A acceptance candidate; low DCR but reduced ripple/revised load release. | **Study 10 µH alloy 74437636351002.** It offers published domain beyond the conditional 78 A screen; accept footprint/control qualification work before selecting it. |
| 4. Local input bank | **Keep current 44.2 µF nominal bank:** higher stored energy, exits proposed 100 A envelope at upper corner. **Qualified effective 10–30 µF:** fits proposed source packet; bias/life/minC and buck/limiter stability must be shown. **Follow generic LTC4364 ≥100 µF electrolytic case:** easier reference-rule compliance, much larger energy; redesign the source/dump contract. | **Qualified 10–30 µF only if a viable controller/cap implementation is demonstrated.** If not, revise the bank and energy contract; never delete bypassing or assert nominal C is the minimum. |
| 5. Input-stage implementation | **Qualify existing TPS26630 with independent fast latched trigger:** least added hardware, response/charge still OPEN. **Prototype higher-voltage external stage:** explicit full range/current design, more SOA/supply/cascade/C-loop work. **Reuse LTC4218:** nominal 24 V fits, but requested OVP corners exceed its operating range. | **Try qualifying existing TPS26630 first against the Q/off contract.** It already covers the voltage range and avoids the added limiter's capacitor/cascade conflict; move to a higher-voltage stage if it cannot meet the contract. Reject LTC4218 for this envelope. |
| 6. E current allocation | **Keep 10 A:** smaller output pulse but needs large very-low-DCR last choke and tight current/off proof. **Investigate 20 A with more C/lower ESR:** smaller requiredL, larger pulse/inrush; existing 1 mF/5 mΩ case gives 5.560 V BLOCKING with new 5.340 V target. | **Keep 10 A as the first qualification target, without freezing it as a requirement.** It limits GPIO let-through; reconsider 20 A only after a full new C/ESR/absorber contract is calculated and qualified. |
| 7. Normal resistance budget | **Add E to old path:** misses 4.75 V in the 10 mΩ example. **Lower RDS pairs + qualified contact reduction + local shunt/choke:** conditional 49.613 mΩ plan, gate/SOA/magnetic/contact work. **Retain D with characterized harness:** avoids second-stage loss, but must eliminate its Pi overshoot counterexample. | **For any E continuation, pursue the explicit contact/FET/shunt/choke plan first.** It exposes the required savings and remaining 0.387 mΩ target reserve; stop/recalculate if a real component or joint exceeds it. |
| 8. Driver supply and fault power | **Keep existing PG/LDO permission:** cited timing not assured at PG floor/UVLO. **Independent boost/buck driver supply, direct loaded-rail monitors and hold-up:** added control hardware, usable gate conditions/default-off. **Self-power Pi-end stage from 5 V without extra budget:** consumes the frozen load envelope and loses independence unless explicitly re-budgeted. | **Independent supply +direct qualification +hold-up.** It addresses M01/B02 and makes the control-power/return budget visible; owner must choose auxiliary wiring for E. |
| 9. Ballast construction | **Retain 2512 with verified ≤85°C terminals/hot pulse:** keeps circuit concept; thermal premise must change. **Rated hot pulse construction:** more mounting/space/parasitics; obtain applicable waveform rating. **Remove bulk crowbar viaD/E absorber:** moves energy/SOA requirement to active parts, after architecture qualification. | **Retain only if the ≤85°C/hot pulse proof is achievable; otherwise change construction.** The 95°C ceiling is fixed manufacturer evidence; architecture relocation cannot silently erase the energy. |
| 10. Evidence before electrical release | **Manufacturer/applicable-envelope work +dummy-load fault/startup/thermal tests:** cost/time but can close missing limits. **Models only:** useful screening, no actual maxima. | **Applicable bounds plus dummy-load tests.** Models cannot confirm source transients, hot L/SOA, pin injection, current sharing or full physical timing. No Pi is the first fault load. |

## Validation, provenance and checkpoint history

Read baseline sources: [Gate3](../GATE3_ARCHITECTURE_OPTIONS.md), [Gate2c](../GATE2C_REVIEW_CLOSURE.md), [historical JSON](../CALCULATIONS.json), [decision index](../../../../context/06_DECISION_LOG.md). They remain historical evidence. [Source register](SOURCES.json) pins new primary-document revisions, URLs, functions, license/reuse state and graph limitations. No raw manufacturer material or complete circuit is copied into this branch; authored notes stay under the required directory.

Run from the worktree:

```sh
python3 -B docs/evidence/r2/sheet03/gate3b/calculate_source_bound.py --write
python3 -B -m unittest discover -s docs/evidence/r2/sheet03/gate3b -p test_source_bound.py -v
git diff 65a8698 --name-only -- hardware
```

Fourteen targeted tests check conservation, charge boundaries, curve-domain rejection, sensitivity counterexamples, the last-path current-rise rule and unknown maxima. They are arithmetic evidence, not electrical validation. No ERC/DRC, export, simulation, bench test, purchase or merge is claimed. [Validation record](VALIDATION.json) records link/JSON/history/hardware metadata checks.

Pushed checkpoints: `f24a66b` setup; `7ed087a` Task1a; `95e6d5b` Task1b; `c6ca3ae` Task2; `68808d8` Task3. Final owner package and evidence follow in a closure checkpoint. The draft PR targets `feat/sheet03-gate3-options`; no merge.

VERDICT: BLOCKED — recommend neither D nor E yet; pursue timed source isolation + controlled local C + qualified 10 µH L201, then re-score receiving paths.
