# V1A-Lite Phase C3 — Option 3B series eFuse + raw-node backup crowbar

**2026-10-05 — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**DECISION / SELECTED:** Option3B replaces Option1R as the owner's architecture. **TPS26630RGET is selected for calculation and costing only. No examined candidate is qualified against every requirement. R1 release and Phase D/R2 implementation remain BLOCKED.** The proposed Pi charging argument is conditional on a current limit already being established. It is not a valid worst-case bound from fault inception. The selected implementation also fails full-temperature threshold and5A voltage-drop screens. Completing this study does not mean the hardware passed.

KNOWN: full brief `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/V1A_LITE_PHASE_C3.md` read, starting branch `feat/v1a-lite-cost-reduction`, HEAD `b20b51c`. Direct work; no sub-agents. Calculations/documents only, no CAD/library edits, purchases or push. Existing C/C2 reports and outputs remain historical evidence. Input requirements remain18–26V normal,24V nominal, continuous54.6–64V upstream fault,5A output, Pi≥4.75V and<5.5V. Fault-source impedance/current limit, peak load, ambient, actual Pi capacitance and harness remain OPEN.

Labels: **KNOWN** cited fact/requirement; **CALCULATED** model/arithmetic; **ASSUMED** sensitivity/accounting input; **PROPOSED** future implementation; **SELECTED** analysis candidate, not qualification; **OPEN** missing bound. PASS/FAIL are restricted to each named screen. These correspond to project OBSERVATION, REQUIREMENT, CALCULATION, ASSUMPTION, HYPOTHESIS, EVIDENCE, DECISION and OPEN RISK labels.

Reproduce: `python3 docs/evidence/v1a_lite/calculate_phase_c.py --c3`. The existing script dispatches to the additive [C3 extension](calculate_phase_c3.py), which reuses C/C2 buck, crowbar and RK4 functions without regenerating historical outputs. Evidence: [JSON](PHASE_C3_OPTION3B.json), [BOM](PHASE_C3_BOM.csv), [purchase model](PHASE_C3_PURCHASE_MODEL.csv), [verification](PHASE_C3_VERIFICATION.json), [source register](../../../third_party/v1a_lite_phase_c3/SOURCES.md). Datasheet page numbers below are printed pages. Price observations are dated2026-10-05, not order reservations.

## 1. Candidate screen and decision

| Candidate / authoritative evidence | KNOWN limiting facts | Decision / procurement |
| --- | --- | --- |
| TI TPS2596x, SLVSET8A pp1,5–7 |21V absolute IN,2A class; fixed5.7V clamp option is too high |FAIL voltage/current; no price can remedy these |
| TI TPS259470LRPWR, SLVSFC9C pp7–11 |28V absolute IN,5.5A class, adjustable OVLO |FAIL29–29.26V exposure; inherited Phase B option3A cannot be independently protected by its own unbounded crowbar |
| **TI TPS26630RGET**, SLVSE94G pp2,5–9 |4.5–60V operating,67V IN/OUT absolute; adjustable OVP;0.6–6A;31mΩ class;14µs maximum specified OVP delay |SELECTED study candidate. LCSC[C2864391](https://www.lcsc.com/product-detail/C2864391.html):500 stock,$6.9453 at1+,MOQ1. RGER[C1850276](https://www.lcsc.com/product-detail/C1850276.html):stock0,$9.0636 reference. Neither is a low-cost success |
| Other TPS2663x, same p2 |31 has2× pulse support;32/33/35/36 have35/39V clamps;37 lacks needed OVP |30 avoids intentional2× pulse mode and provides adjustable cutoff; variants do not fix voltage-drop problem |
| TI TPS259830LNRGER, SLVSHH5C pp4,7–10 |30V IN absolute,26V operating;2.7mΩ typical; OVLO reference1.10–1.25V; OVP2.6µs typical, current-limit response588µs typical, no maxima in table |Rejected despite better loss: no divider gain can simultaneously give min trip>5.25 and max trip<5.5 (`5.25/1.10=4.773 >5.5/1.25=4.400`). LCSC[C20607218](https://www.lcsc.com/product-detail/C20607218.html):2974 stock,$4.1892 at1+. ON circuit-breaker variant[C20611808](https://www.lcsc.com/product-detail/C20611808.html):684,$5.4158; does not supply assumed steady limiting.30V absolute is not26–29V functional qualification |
| SG Micro SGM2546, December2025 pp1–7 |7A class but28V IN absolute |FAIL raw29V; no stock/price qualification pursued for rejected electrical candidate |
| Diodes AP22615, DS41022 Rev7-2 pp1,4–5 |3A continuous,4A adjustable ceiling; **IN6V absolute**;28V catalog number applies to OUT |FAIL. Do not misread OUT rating as input survival |
| onsemi NIS6150/D Rev5 pp3–4 |IN10V,1A continuous; lowest OVP clamp5.7–6.5V |FAIL voltage/current/threshold despite20µs maximum OVP response |
| Silergy SQ24802K2 Rev1.0 pp1,3–4 |18V absolute,1–5A limit,14V clamp |FAIL; public manufacturer PDF viewed, local fetch unavailable |
| Richtek RT1720 + external N-FET, DS1720-01 p5 indexed; current official product page |5V minimum, FB1.20–1.30V indexed, controller nowEOL; regulates external FET with fault timer |Not selected.5V minimum conflicts with inherited4.985V rail-low screen; reference span exceeds5.25–5.5V window. Full official PDF currently404, timing/stock/price OPEN |

EVIDENCE: manufacturer documents/URLs/revisions and local hashes are recorded in the source register. Supplier descriptions never override datasheets. Search was a bounded candidate survey, not proof that no suitable part exists anywhere. Rejected candidates have no claimed buyable price. **No single part was found that simultaneously meets the complete voltage, threshold, response, drop, stock and budget requirements.**

DECISION on fallback: use the67V candidate to study an independent series path; do not claim a28V eFuse is safe merely because it is electrically “behind” a shunt crowbar. Its IN is the same raw node until a series element or a proved clamp limits it. C2 has no worst-case clamp bound. A low-resistance external60V N-FET plus precision OVP/current controller could solve drop, but requires a specified comparator/reference, gate supply, turnoff driver, shunt, linear SOA and reset proof; RT1720 does not close these. Such a redesigned architecture is OPEN and not hidden as a zero-cost substitute in the BOM.

## 2. Proposed force path, control and input correction

```text
VIN_RAW -> F101 -> Q101 reverse PFET -> S_COMMON -> Q102 cutoff PFET
                                                    -> VIN_PROTECTED -> LM61460/L201 -> VOUT_5V1
                                                                                           |
                                                               raw25V MLCCs +2x1000uF10V + SCR301
                                                                                           |
                                                                                          GND
VOUT_5V1 -> Q302 reverse-blocking NFET -> U302 TPS26630 IN -> OUT/VOUT_PROTECTED
                                                               -> F301 -> LOAD_5V1 -> Pi
                                                                                 |
                                                          C301/C302 +C303/C304 at Pi entry
```

PROPOSED U302 connections follow TPS2663 pp3–4,17–23 and reference reverse-blocking circuit Fig8-7. Q302 **CSD18540Q5B** source=VOUT_5V1/IN_SYS, drain=U302 IN, gate=B_GATE; Q303 **JSCJ2N7002** drain=B_GATE, source=IN_SYS, gate=DRV. Q303 is required for fast Q302 gate discharge; B_GATE alone is a weak drive. The selected signal FET has60V VDS,±20V VGS and50pF maximum Ciss in its own sheet pp1–2. This is a rated-parts screen; Q302 gate-charge turnoff and reverse energy remain OPEN. Q302 blocks the discharge of Pi-side reservoirs back into the raw SCR when off; a lone internal eFuse FET must not be presumed to do that.

PROPOSED OVP senses **raw VOUT_5V1**, using R32034.8k/R32110k. This implements protection of the output rail by cutting its input supply, matching the manufacturer arrangement. It is **not an independent remote Pi-pin comparator**. A Pi-side-only sense connection would create a different feedback/restart topology and is not silently substituted. UVLO is tied to IN_SYS (rated for this voltage), not GND: grounding UVLO selects the internal≈15V threshold and would prevent5V operation. MODE left open selects latch response for overload/thermal faults. SHDN left open uses its internal pullup; verify exact unused-pin treatment at capture. IMON/FLT/PGOOD may remain unused with test access; PGTH referenced to OUT. C305/C306 are local100nF50V IN/OUT bypasses; C307100nF50V sets dVdT. The raw bank also bypasses IN_SYS. Pin1/2 IN, pin3 B_GATE, pin4 DRV, pin5 IN_SYS, pin6 UVLO, pin7 OVP, pin8 GND, pin9 dVdT, pin10 ILIM, pin11 MODE, pin12 SHDN, pin13 IMON, pin14/17 OUT, pin15 PGTH, pin16 PGOOD, pin18 FLT and exposed-pad GND must be checked against the RGE drawing before any symbol use; NC pins remain NC.

KNOWN/CALCULATED voltage survival: at29.26V raw and5.25V protected, positive IN–OUT stress≈24.01V; at discharged OUT it is29.26V. TPS2663 p5 rates IN and OUT individually to67V and supports60V forward cutoff; no smaller positive IN–OUT absolute limit is listed. Thus the **power-pin DC screen passes**, with37.74V to67V. Negative IN_SYS–OUT transient permission applies with the external blocking FET; it is not an internal reverse-current guarantee. After raw crowbar firing, Q302 sees approximately Pi voltage in reverse.60V Q302 and67V eFuse ratings do not prove switching/inductive/pin survival.

**FAIL discovered auxiliary-pin exposure:** an unprotected5.376V OVP divider places **6.531V on OVP at29.26V raw**, exceeding the5.5V OVP-pin absolute maximum (recommended4V). Costed D302 **BZT52C3V3-7-F** is a PROPOSED shunt, cathode=OVP, anode=GND. At nominal3.3V clamp, available current≈0.416mA. Its5mA zener test does not qualify its knee, leakage or dynamic clamp at this current.1µA leakage already moves raw trip34.8mV; leakage has not been bounded at1.2V over temperature. Therefore full-device survival is **OPEN**, despite the power-pin PASS. A proved low-leakage clamp or different detector is a prerequisite, not an optional improvement.

SELECTED input correction: replace **both Q101/Q102 with IRFR6215TRPBF**,150V P-channel DPAK, G1/D2+tab/S3. Preserve common sources, separate12V gate clamps, F101, BournsSMCJ64CA on VIN_FUSED, protected TVS3300 and the upstream-powered C2 latch.103V TVS rated clamp is now47V below150V: **PASS nameplate coordination**, resolving the specific C2 FAIL.64V off-state margin86V; a powered reverse combination64+36=100V leaves50V. Real TVS pulse current, hot clamp, ringing, polarity and source energy are still OPEN. Lowering standoff below64V would conflict with continuous fault tolerance and was not selected.

KNOWN manufacturer IRFR6215 sheet2016-05-31 pp1–2:0.295Ω max25°C,0.58Ω max150°C atVGS=−10V; Qg66nC/Qgd35nC maximum at the stated test;150V/±20V ratings. At inherited1.574A, two FETs dissipate **1.462W cold /2.874W at150°C resistance**. At50°C ambient, using50°C/W PCB-mounted figure gives an illustrative≈122°C per device at the hot-loss input; actual input current, copper and electrothermal fixed point are unresolved. The18V end of the input range and added series losses require a fresh input-current/efficiency solution;1.574A is only the inherited comparison point. A voltage-rating upgrade is not a thermal approval. LCSC reference$0.9375 each, stock0: procurement OPEN.

CALCULATED gate-charge screen repeats C2's expressly ASSUMED scaling:66nC×13.35/10=88.11nC, at≥1mA pullup current to|VGS|=1V gives88.11µs, plus20µs latch/storage allowance→108.11µs. Keep **150µs** as the report's cutoff sensitivity, not a guaranteed maximum. The previous IRF9540 SOA/thermal curves cannot be assigned to the new die. Recheck IRFR6215 Fig8/11 at the actual24/64V trajectory and hot case. Literal Q101-only shutdown remains ineffective because its body diode passes positive input: the persistent latch must inhibit **Q102 through Q103**, independent of buckEN/FB/VCC/PGOOD. C2 latch capture/hold-up/reset and control-rail loading risks persist.

## 3. Threshold, current limit, normal drop and startup

CALCULATED eFuse nominal trip=`1.2×(1+34.8/10)=5.376V`. Use TI1.176–1.224V threshold and±150nA input leakage, independent0.1%/25ppm resistors over−40…125°C (`e=0.0035`). Result **5.234694–5.518680V**, **before** D302 leakage. Margins at5.17/5.25V normal are+64.69/−15.31mV. Upper threshold exceeds5.5V even in a slow no-load overvoltage, where current limiting may never engage. These are FAIL screens; capacitor size cannot repair a static threshold conflict. Actual board thermal range is OPEN, not silently narrowed.

CALCULATED ideal zero-error divider gain would need `4.4643<gain<4.4935` to fit5.25–5.5V with the eFuse's±2% reference alone. That≈0.65% total ratio window is consumed by resistor drift/leakage. A tighter-TCR divider and qualified low-leakage clamp are PROPOSED remedies requiring new exact parts/calculations. There is no useful noise/dynamic reserve in the present choice. Raising buck voltage to compensate series drop also worsens this threshold conflict and is not authorized as a new requirement.

SELECTED RILIM=`3×1k+100Ω=3.1kΩ`, all precision parts already used elsewhere. Nominal limit **5.806A**; interpolating TI±7% and applying±0.35% resistor screen gives **5.381–6.235A**. This clears5A DC by only0.381A at the low screen. TI's exact3k test gives5.58–6.42A at IN−OUT=1V; the3.1k interpolation and high-differential limiting envelope are **OPEN qualification**, not separately guaranteed measurements. No2× pulse variant is selected. MODE=open latches after timed overload/thermal shutdown; it does **not** make every OVP event latch. TI specifies current-limit duration129–202ms; thermal shutdown can intervene earlier. OVP recovers when its pin falls below hysteresis, so the separate upstream latch remains essential.

CALCULATED eFuse loss at5A is0.761W at30.44mΩ typical,1.125W at45mΩ85°C maximum,1.325W at53mΩ full-temperature maximum. At assumed50°C ambient,31.4°C/W JEDEC gives73.9/85.3/91.6°C illustrative junction estimates. This is not a2-layer board thermal model; neighboring buck/FET heating and actual copper must be measured. Using cold F3019mΩ and an **ASSUMED6.6mΩ hot Q302 screen** (2×3.3mΩ4.5V-gate25°C maximum) costs another78mV. Inherited minimum buck rail including ripple is4.98549V:

| eFuse resistance | Pi at5A, before any harness/contact loss | Remaining wire/contact resistance to4.75V |
| --- | ---: | ---: |
|30.44mΩ typical |4.75529V |1.058mΩ |
|45mΩ at85°C maximum |4.68249V |negative13.502mΩ |
|53mΩ full-temperature maximum |4.64249V |negative21.502mΩ |

**FAIL5A minimum-voltage screen.** Even omitting Q302 and all harness loss,53mΩ eFuse plus9mΩ fuse gives4.67549V. Connector nameplate current is insufficient: contact resistance, crimp and wire length must fit a budget that is currently negative. At nominal5.065V and typical eFuse resistance, total modeled drop≈0.230V gives4.835V, explaining why a typical-room-temperature prototype could appear to work while failing corners. eFuse loss alone is≈3.0–5.2% of25.5W; actual whole-module efficiency remains unvalidated. Retain C/C2 buck ripple/inductor/core-loss evidence with its assumptions; output capacitors and startup need new loop validation.

PROPOSED startup:100nF±10% dVdT capacitor with datasheet current/gain bounds gives379–643V/s, nominal5.1V ramp10.2ms. Maximum new Pi bank initial capacitance is2.5034mF including C301/C302; charge demand≈1.609A. If a5A load is already active,6.609A exceeds the5.381A low-limit screen: startup may current-limit or thermally time out. Pi startup load profile is OPEN; do not assume it waits until the rail is valid. Keeping total at5.381A with5A load would require≥33.50ms ramp and≈423nF minimum nominal timing capacitance at the stated tolerances, before other allowances; this is an unselected sensitivity. Check UVLO, ramp recovery, inrush energy≈32.56mJ, buck soft-start and the raw2mF load as a coupled system.

## 4. What the dV/dt argument proves, and what it does not

CALCULATED charge conservation is always `C dV/dt=I_into_cap−Iload` for an ideal capacitor. Substituting `I_into_cap=Ilim` requires an established limiter and a bound on its overshoot. TPS2663 p9 specifies soft-short fast-trip4.5µs maximum **after** current exceeds its≈2×IOL threshold; hot-short1µs is typical and the45A threshold is typical. Neither specifies maximum settling time of the analog current-limit loop for an incoming raw-node voltage rise. Existing raw and buck-input capacitors also supply current independent of the source's sustained current limit. Therefore **FAIL as an unconditional argument**. The required integral is:

```text
Qprelimit + integral(max(Ipass−Iload,0) dt) < Cmin (5.5−Vpi_start)
plus terminal ESR/ESL and interconnect-energy excursions.
```

KNOWN timing to compare: TPS2663 **p8 OVP_tOFF(dly)8.5/11/14µs min/typ/max over−40…125°C**, tested from OVP20mV above its threshold **to FLT falling**, Fig7-1 p13. At the high divider corner the20mV overdrive is not reached until raw≈**5.60877V**. Time to reach that level, filter behavior on a short pulse, and current-tail/commutation are not magically included. The14µs number is a published maximum for that measurement; final Pi protection still needs a defensible switch-current waveform. The script stores missing loop, crowbar and latch maxima as`null`.

SELECTED capacitance study: keep two raw EEUFR1A102; add **two further EEUFR1A1021000µF10V** at the Pi entry, after F301, with existing C301/C302. Initial−20% gives1600µF bulk. Assume40µF effective local ceramics, bulk28mΩ each (catalog impedance used as ESR), no ceramic ESL. Do not count raw capacitance as Pi-side reservoir, or count unspecified Pi onboard capacitance as guaranteed. Physical placement at the Pi entry is part of this proposal; a remote board capacitor does not automatically clamp the actual pins.

| ASSUMED no-load, start5.25V, established6.235A limit | Ideal-cap window to5.5V | Separate-ESR window | Pi after14µs |
| --- | ---: | ---: | ---: |
|1×1000µF bulk +40µF ceramics |33.682µs |12.349µs |5.512254V — FAIL |
|2×1000µF bulk +40µF ceramics |65.761µs |43.907µs |5.386303V — conditional PASS |
|2× bulk,5A load maintained |332.058µs |310.204µs |5.276994V — conditional PASS |

CALCULATED bare ideal minimum for14µs and0.25V headroom is349.145µF; it ignores ESR and pre-limit charge. The two-bulk ESR model leaves29.907µs against14µs **only when the clock starts at5.25V and limiting is already established**. Twice the assumed ESR raises the14µs result to5.469383V. Ambient/cold/endurance impedance, actual MLCC bias, trace inductance, measurement bandwidth and current transient remain OPEN. The analytic response used for `Cc || (Rb+Cb)` is:

```text
ΔV(t)=I t/(Cc+Cb)+I Rb [Cb/(Cc+Cb)]² [1−exp(−t/τ)]
τ=Rb Cc Cb/(Cc+Cb)
```

CALCULATED falsification sensitivity: an ASSUMED45A pre-limit pulse lasting1µs produces **5.780926V** in the same two-bulk model, before subsequent current limiting.45A is not a guaranteed device or system limit; it shows that an unbounded early pulse cannot be ignored. A2µH harness carrying5A stores25µJ, enough to raise an isolated40µF ceramic from5.25V to5.36773V if its energy transfers losslessly. Do not add that rise blindly to another peak; solve the coupled network. Required design proof is a bounded charge/energy trajectory and a worst-case static threshold, not just nominal `Ilim/C`.

## 5. High-side-short sequence, actual ordering and backup failure

PROPOSED backup threshold is retuned above normal operation: keep R3011k, R302100Ω; replace R30330Ω with100Ω and add R309100Ω, all0.1%, upper total1.3k; retain R3041k lower. Nominal5.7385V; reusing C's TL431/reference/temperature screen gives **5.597684–5.870160V**. Low threshold is347.68mV above5.25V, compared with C2's−66mV margin at5.25V. This is a deliberate **backup raw-energy crowbar** setting, not a second5.5V Pi limiter. Keep TL431BIDBZR, BC807-40,215 and TYN612RG, and trigger C2's upstream latch from CB_COLLECTOR. Recheck SCR gate drive with the latch branch drawing current; a higher trigger voltage does not guarantee cold SCR latching or maximum delay.

CALCULATED illustrative sequence uses24V stiff source,2µH saturated-inductor sensitivity,40µF raw ceramics/3mΩ,1600µF raw bulk/14mΩ,1600µF Pi bulk/14mΩ plus40µF ceramics, initial raw5.25V and inherited6.322A inductor current,5A prior load followed by complete release. Healthy series resistance44mΩ, no harness L in this particular illustration; Pi initially5.03V. Current limit and turnoff are idealized as stated, SCR establishment delay ASSUMED2µs. This is not a manufacturer eFuse model.

| Event after high-side short | Immediate-limiter24V example |
| --- | ---: |
|Pass current first exceeds6.235A; model then caps it |1.390µs |
|Raw reaches eFuse maximum threshold+20mV pin overdrive |3.180µs |
|Raw reaches backup maximum threshold |4.990µs |
|SCR begins modeled clamp; same trigger requests input latch |7.000µs |
|Hypothetical eFuse14µs one-shot completes |17.180µs |
|Q102 off under150µs latch sensitivity |about155–157µs |
|Modeled early Pi peak / raw peak |5.13959V /6.18078V |

**OBSERVATION: the crowbar fires before the nominal eFuse OVP delay finishes in this example.** One cannot prescribe “eFuse trip, then crowbar” by block names alone. The crowbar can remove OVP overdrive before its delay completes, so the table's17.18µs switch opening is an explicitly optimistic one-shot assumption; real OVP filtering/recovery needs qualification. Reverse blocker response also becomes important immediately when raw collapses. The external latch must capture the short trigger while raw disappears and keep Q102 off; its completion cannot be inferred from the eFuse MODE setting.

CALCULATED early sensitivities with limiter engagement delays0/5/20µs give Pi peaks5.13959/5.26425/5.31183V at24V and5.13641/5.29835/5.31977V at29.26V, **because the assumed2µs crowbar acts early**. These results do not prove independent series protection. To isolate that dependency, the JSON also includes a delayed-crowbar case; see the verification/report addendum below. The waveform solver stops at100µs and assumes a50A source ceiling only after SCR firing; it does not claim the actual source has that limit or that late stored-energy stress is qualified.

**eFuse fails short:** Q302 is a reverse blocker, so its body diode still supplies a forward fault even if its gate is off. The Pi is then connected to raw through wiring/fuse impedance. In a sufficiently slow rise or negligible-impedance limit, Pi tracks raw and exceeds5.5V **before even the lowest backup trigger5.59768V**. Minimum excess≈97.7mV before detector delay; highest threshold is5.87016V. Thus backup cannot satisfy the5.5V ceiling under this failure. This is a FAIL guarantee screen, not a claim that every waveform fails.

CALCULATED finite-interface failure model includes C303/C304, cold fuse9mΩ+ASSUMED10mΩ wiring,0.2/1/2µH harness, the same source/L/raw C, and instantaneous SCR0.85V+30mΩ clamp after ASSUMED0.5/2/5µs. Selected results:

| Source / harness | SCR delay | Pi peak | Result |
| --- | ---: | ---: | --- |
|24V /0.2µH |0.5µs |5.31752V |conditional PASS |
|24V /0.2µH |2µs |5.37482V |conditional PASS |
|24V /0.2µH |5µs |5.51701V |FAIL |
|29.26V /0.2µH |5µs |5.53377V |FAIL |
|29.26V /1µH |5µs |5.34074V |conditional PASS |

OPEN maximum Pi-pin peak: no finite qualification bound follows without real source, harness, effective caps, device response and ground inductance. If crowbar/latch also fail, Pi can approach raw input and ring above it. Do not infer a safe ceiling from the largest value in this limited grid. Failed-open eFuse removes Pi power; failed OV divider/clamp can prevent cutoff or cause nuisance shutdown; shorted ILIM resistor must not be treated as a safe6A setting. Startup/hiccup or input removal can clear latch state; USB/external5V backfeed and power-off paths must be excluded/qualified.

RAW CAP / SCR consequence: retain six25V raw MLCCs and two10V raw bulk as requested. Early listed peaks<10V are conditional; an uncontained26–29V raw fault exceeds both ratings. C2's capacitor/SCR current-rise, hot I²t and recovery findings remain. The added Pi bank is isolated only with a working reverse blocker; in eFuse-short/reverse-blocker-failure cases its energy can enter the SCR. At6V, all output capacitors at positive initial tolerance store≈94.35mJ (raw+Pi5.2418mF). With10nH local loop, `(6−0.85)/10nH≈515A/µs`, still far above the50A/µs gate-conditioned SCR rating. Q102 cutoff removes future source feed but cannot erase buck-input/output reservoir energy. No C2 thermal curve for the older PFET is reused. Fuse clearing is not credited; full SCR pulse/SOA/latch persistence and near-zero anode-current recovery remain OPEN.

## 6. Costed Option3B BOM and sourcing

SELECTED changes are enumerated by reference in [PHASE_C3_BOM.csv](PHASE_C3_BOM.csv): two150V PFET replacements; U302 TPS26630RGET; Q302 CSD18540Q5B/Q303 JSCJ2N7002 reverse-blocking driver; R32034.8k/R32110k OVP divider; D3023.3V pin-clamp proposal; R322–R3253.1k ILIM chain; C305/C306 bypass and C307 timing100nF; two additional Pi-side EEUFR1A102; R303/R309 backup retune. Original raw2mF,25V MLCCs, buck, inductor, input fuse/TVS, F301 wiring fuse and persistent latch stay. Capacitor voltage/footprint, Q302/Q303 package and pin mapping require independent R2 review.

KNOWN dated supplier facts: TPS26630RGET$6.9453, stock500; IRFR6215TRPBF$0.9375 reference, stock0; CSD18540Q5B$2.3114 reference, stock0;34.8k resistor$0.0673 at10+,stock0; JSCJ2N7002$0.0179 at50+,stock1,074,050. Existing C/C2 price/stock snapshots are inherited, not all refreshed. MMBTA42 and TVS3300 sourcing remain OPEN. SMCJ64CA retains the explicit$0.50 allowance; do not substitute a differently rated suffix or vendor.

ASSUMED FX=26,500VND/USD, not a live exchange quote. A=installed core at recorded applicable small-lot unit allocation; B adds23,685.70VND installed interfaces and10,600VND one allocated PCB. C aggregates identical MPNs, buys `n+max(1,ceil(25%n))` rounded to MOQ; local C uses `n+1`, exact critical parts and saved local generic/connector sourcing. All four FR capacitors still fit a five-piece purchase with a spare. Safety-critical C307 shares MPN with50V bypasses, so that MPN is purchased exactly; it is not replaced by unqualified local generic timing capacitance. Remaining generic100nF boot-cap lot is charged once in full. No resistor/purchase lot is charged twice.

| CALCULATED planning total | VND |
| --- | ---: |
|A installed core|**650,445.15**|
|B with installed interfaces/allocated PCB|**684,730.85**|
|C conventional purchasing|**2,159,363.80**|
|C using local sourcing policy|**1,855,943.15**|
|Conventional over1,000,000|**1,159,363.80**|
|Local over1,000,000|**855,943.15**|

| Cost outside core procurement | Conventional C | Local C |
| --- | ---: | ---: |
|Five-PCB lot |53,000|53,000|
|Connector lots /three local kits |263,502.75|4,719|
|Wire/heat-shrink |35,000|20,000|
|Freight/import/tax reserve |180,000|80,000 components+120,000 PCB|
|Local delivery reserve |—|20,000|
|Manual assembly/consumables reserve |50,000|50,000|
|Rework reserve |50,000|50,000|
|Thermal hardware/qualification contingency |40,000|40,000|

CALCULATED core purchase cash=1,487,861.05VND conventional /1,418,224.15VND local. Reserves total320,000/360,000VND respectively, shown separately. Compared with C2, increases are555,371.10/578,028.60VND. Both exceed the1,000,000VND ceiling. Removing local delivery and thermal contingency would still leave795,943.15VND over budget; neither reserve is waived.

OPEN complete landed cost: no cart or purchase quote; shipping/import, exact connector qualification, hot input-FET copper/heatsink work, precise OVP redesign, latch reset/hold-up and a lower-drop series solution can increase costs. Stock0 lines are not purchasable merely because a price exists. This is a costed analysis BOM, **not a fabrication/purchase BOM release**.

## 7. Phase D schematic change list — PROPOSED, not executed

1. Input sheet: replace Q101/Q102 TO220 symbols/footprints with exact150V DPAK parts; keep orientation, separate gate clamps and F101/SMCJ64CA. Preserve Q104/Q105/Q106 regenerative latch powered upstream of Q102, Q103 base inhibition and test points; confirm no dependence on buck control pins. Recalculate gate/thermal/SOA, startup into64V and latch reset. Protected TVS3300 stays after cutoff. Never place it directly across continuous64V.
2. Buck sheet: retain LM61460AANRJRR and reviewed frequency/FB network, BIAS=GND,6.8µH inductor, six25V raw MLCCs and two raw1000µF caps. Do not change setpoint to conceal eFuse drop. Preserve manufacturer hot-loop geometry, input bypass and return paths. Revalidate loop stability and effective capacitance with the changed series load/inrush.
3. Output sheet: add U302 RGE24 exact pin mapping, Q302/Q303 reverse block and IN_SYS/IN split; define VOUT_PROTECTED explicitly between eFuse OUT and F301. Use raw OVP sense,3.1k ILIM,UVLO tied IN_SYS,MODE open,dVdT100nF and proper unused pins. Resolve D302 pin-clamp/leakage failure **before capture release**. Put bypasses next to power pins, OVP/ILIM return Kelvin to quiet GND; do not share SCR return copper with detection references.
4. Raw backup: SCR301 anode, U301 divider top and Q301 emitter remain directly on VOUT_5V1, before all output series elements. Change R303 to100Ω/add R309100Ω; document5.7385V backup function and inability to protect Pi under eFuse-short. Keep CB_COLLECTOR→R163 latch trigger. No fuse/link may disconnect raw SCR from raw capacitors. Recheck SCR gate pulse, holding/latching, di/dt and discharge paths.
5. Pi interface: F301 remains7A wiring backup. Add C303/C304 after F301 **at the actual Pi power entry**; C301/C302 local ceramics remain. If a cable separates this bank from the Pi pins, replace the current model with that geometry. Verify10×16mm/5mm-pitch FR footprint/polarity, retention and vibration clearance; define harness/contacts/rating and test at pins. Add test access to raw, eFuse IN/OUT, OVP, ILIM, B_GATE, DRV and latch signals.
6. Gate review: resolve every FAIL/OPEN below, especially hot5A drop,staticOVP corners,pin clamp and finite limiter delay, before R1 electrical release/R2 implementation. Reconcile BOM/netlist/package/pin1/tab mappings independently. Run ERC after schematic changes, then R3 layout/DRC and visual outputs only after preceding gates. No new ERC/DRC is applicable to this document-only task.
7. Bench evidence after authorized hardware work: visual→continuity/shorts→current-limited bench supply→no-load startup→rail verification→small dummy load→5A load steps→thermal→ripple→load release/startup→fault/protection/latch→telemetry N/A for Lite→SBC last. Use a sacrificial fixture/electronic load for high-side-short and fail-short tests, never the Pi as the first fault load. Capture IN/OUT/actual Pi/OVP/SCR-gate/Q102-gate and current at sufficient bandwidth over temperature, source corners and reset/hiccup states. No USB3 or D435i data is routed through this PCB.

## 8. Verification and handback

EVIDENCE: standard-library reproducer, independent analytic/ODE capacitance comparison, smaller-step transient convergence, deterministic regeneration, accounting/MOQ/reference checks and historical/CAD scope checks are recorded in PHASE_C3_VERIFICATION.json. These are numerical/document checks, not electrical safety validation. Git outcome is recorded separately in PHASE_C3_GIT_LOG.txt. Nothing pushed or bought. The source register documents retrieval failures instead of inventing datasheet evidence.

CALCULATED independent-series stress sensitivity (SCR deliberately unavailable during the100µs model window): at29.26V, limiter engagement0/5/20µs yields Pi peaks**5.17565/5.29835/5.90116V**. In the20µs case Pi crosses5.5V at10.24µs, before hypothetical eFuse opening at16.84µs: **FAIL**. This explicitly removes the early-crowbar assistance from the earlier healthy examples.20µs is a sensitivity, not a claimed device delay. The raw LC model subsequently reaches≈35.33V; once it crosses10V (≈21.93µs), continued ideal-capacitor results are mathematical extrapolations beyond the bulk rating, not a physical failure prediction. Timing qualification cannot be replaced by these favorable or unfavorable assumed examples.

OPEN reverse-path nuance: the failed-short table assumes a conducting series path during SCR commutation, as can occur if the same eFuse failure disables its DRV control. If Q302 still switches off correctly, the reverse-discharge trajectory changes. Forward exposure remains through Q302's body diode, and the slow-ramp threshold counterexample still defeats a universal5.5V claim. Actual Pi-pin grounding, clamping, ringing and partial IC failure behavior require separate fault testing.

KNOWN Git outcome: authorized staging failed with exit128: `Unable to create /Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-lite/index.lock: Operation not permitted`. Per the brief, C3 remains **uncommitted**, HEAD `b20b51c`; commit was not run after staging failed. No permissions/locks changed and no push. See [Git attempt log](PHASE_C3_GIT_LOG.txt).

## PASS / FAIL / OPEN table

| Check (limited scope) | Result |
| --- | --- |
|150V FET vs 103V rated TVS clamp|**PASS**|
|eFuse IN and positive IN OUT voltage at 29p26V|**PASS**|
|raw OVP pin without added clamp|**FAIL**|
|OVP pin clamp leakage and dynamic survival|**OPEN**|
|6A class current limit static screen|**PASS**|
|14us datasheet max at stated test conditions|**PASS**|
|Pi cap two bulk 14us ideal limit ESR screen|**PASS**|
|current limit from fault inception argument|**FAIL**|
|guaranteed Pi peak below5p5V|**OPEN**|
|efuse nuisance at5p25V full temperature screen|**FAIL**|
|efuse static high trip below5p5V|**FAIL**|
|backup crowbar nuisance at5p25V static screen|**PASS**|
|Pi min4p75 at5A hot series drop screen|**FAIL**|
|startup5A plus cap charge below low limit|**FAIL**|
|eFuse short backup Pi5p5V protection|**FAIL**|
|raw caps latch SCR input FET hot SOA|**OPEN**|
|complete in stock low cost BOM|**OPEN**|
|C under1000000VND|**FAIL**|
|local C under1000000VND|**FAIL**|
|documents calculations PhaseD list|**PASS**|
|R1 release and PhaseD capture|**OPEN**|
