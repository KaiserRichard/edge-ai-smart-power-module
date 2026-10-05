# V1A-Lite Phase C2 — revised Option 1R

**2026-10-05 — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**DECISION / SELECTED: C2 analysis delivered; R1 electrical release and Phase D/R2 capture remain BLOCKED.** Moving the SCR to the raw node removes the output-fuse-first disconnection. Adding bulk capacitance helps but does not establish the Pi voltage limit. The literal Q101 shutdown in the brief cannot interrupt positive input current in Phase C's common-source pair; Q102 must be inhibited. The minimum corrected latch concept is documented and costed below, with the literal request separately marked FAIL. No gate is advanced by this analysis.

KNOWN: followed the complete `V1A_LITE_PHASE_C2.md`, starting at `b5461b0bc5eaae874c3c3ed869dfb03d5295827b` on `feat/v1a-lite-cost-reduction`, directly without sub-agents. Read the Phase C report, JSON, script and BOM and the read-only sibling sourcing plan. Requirements remain 18–26 V normal, 24 V nominal auxiliary supply, continuous 54.6–64 V upstream fault, 5 A output, Pi pins ≥4.75 V and <5.5 V. The source current limit, impedance, hiccup, harness, ambient and actual protection delays remain OPEN. Nothing bought; no schematic/PCB/library edits.

Labels: KNOWN = cited requirement/fact; CALCULATED = arithmetic/model; ASSUMED = sensitivity or accounting input, not a requirement; PROPOSED = future implementation; SELECTED = analysis/cost choice, not qualification; OPEN = no guaranteed bound. PASS/FAIL refer only to the named screen. OBSERVATION, EVIDENCE, DECISION and OPEN RISK are used with these labels. Untested behavior is never validated.

Reproduce: `python3 docs/evidence/v1a_lite/calculate_phase_c.py --c2`. The original script is extended, reusing its `buck`, `crowbar`, `lc_fault`, input labels and dated price data. C2 writes [JSON](PHASE_C2_REVISION.json), [BOM](PHASE_C2_BOM.csv) and [purchase model](PHASE_C2_PURCHASE_MODEL.csv). Historical Phase C outputs are unchanged. [Source register](../../../third_party/v1a_lite_phase_c2/SOURCES.md) identifies document revisions, files, licenses, reuse and attribution. No new ERC/DRC is applicable without CAD changes.

## 1. Architecture disposition and independent latch

SELECTED force path for analysis:

```text
VIN_RAW -> F101 -> Q101(reverse blocking) -> S_COMMON -> Q102(forward cutoff)
                                                        -> VIN_PROTECTED
                                                        -> buck/L201 -> VOUT_5V1 -> F301 -> LOAD_5V1 -> Pi
                                                                        |                    |
                                            raw ceramics + C217/C218 + SCR301              C301/C302
                                                                        |                    |
                                                                       GND ---------------- GND
```

SELECTED: SCR anode, U301 upper divider and Q301 emitter all move to **VOUT_5V1**, directly at raw output capacitors. SCR cathode returns to power GND; detector sense return is Kelvin-connected away from SCR current. No fuse, removable link or input-switch-controlled connection is allowed between raw caps and SCR. Keep **F301=0451007.MRL, 7 A**, only in the Pi branch for backup wiring protection. At 5 A the manufacturer's 75% nominal-use screen needs ≥6.67 A before additional temperature derating; reducing to a 5 A fuse would not establish 5 A continuous service. Its cold loss/drop remains 0.225 W/45 mV. Clearing under source-limited overload and exact wire ampacity remain OPEN. It is neither the crowbar-clearing fuse nor the Pi OV limiter. F101=0451003.MRL remains backup; its total-clearing I²t is not replaced with nominal melting I²t.

**CALCULATED / FAIL literal Q101 command:** Q101 drain is VIN_FUSED, source S_COMMON. Its body diode conducts VIN_FUSED→S_COMMON even with VGS=0. Thus no finite time-to-source-removal follows from switching Q101 off. Q102's opposing diode blocks forward input. Keep both IRF9540NPBF devices and their gate clamps; the corrected shutdown inhibits **Q102**, without touching buck EN/FB/VCC/PGOOD. Refdes are not silently swapped to hide this discrepancy.

PROPOSED, costed correction: a regenerative Q104/Q105 latch supplied by **CTRL12 upstream of Q102**, with Q106 clamping the existing Q103 gate-sink base. One transistor alone does not provide nonvolatile fault memory. The three small transistors reuse existing MPNs and purchase lots:

| Ref / SELECTED MPN | PROPOSED connection |
| --- | --- |
| Q104 / MMBTA42-TP | NPN emitter GND; collector via R160 to Q105 base; base SET_LATCH |
| Q105 / BC807-40,215 | PNP emitter CTRL12; collector LATCH_H; base via R164=100k to CTRL12 |
| Q106 / MMBTA42-TP | NPN emitter GND; collector IN_NPN_BASE (Q103 base); base via R162 from LATCH_H |
| R160 / 0805W8F1002T5E | 10k, Q105 base to Q104 collector |
| R161 / same | 10k, LATCH_H to SET_LATCH, positive feedback |
| R162 / same | 10k, LATCH_H to Q106 base |
| R163 / same | 10k, existing Q301 collector CB_COLLECTOR to SET_LATCH; samples the same OV event as SCR drive |
| R164–R166 / 0603WAF1003T5E | 100k Q105 B–E, Q104 B–E and Q106 B–E respectively |

CALCULATED DC hypothesis uses VBE=0.7 V, VCEsat=0.2 V and ideal clamp, both ASSUMED. At 18/24/26 V the latched CTRL12 is approximately **7.93/10.27/11.05 V**; each 10k latch branch supplies **0.703/0.937/1.015 mA**. Q106 sinks approximately **0.403/0.615/0.686 mA** from the old base network. At 64 V, U101 is also ON: CTRL12=12 V, TL431 load 9.5 mA plus latch load ≈3.337 mA leaves only ≈0.163 mA nominal zener current. The 4k ballast still dissipates 0.676 W split over its 16 resistors. Static current availability is a limited PASS, not proof of saturation, noise immunity or latch capture. A few tens of µA can return through R163 after output collapse; verify that SCR gate remains below its trigger threshold.

OPEN: the very short OV/SCR-gate pulse must set the regenerative latch before raw voltage collapses; transistor gain, storage, C102 rail dynamics and brownout behavior are not bounded. Keeping CTRL12 upstream prevents Q102 shutdown from erasing its own command. Reset is intended only when input power is removed and C102 discharges; **there is no proved minimum removal time or guaranteed immunity to source hiccup resetting the latch**. No automatic release on output recovery is permitted. An upstream-powered latch with qualified hold-up/reset may be required; its extra hardware is OPEN/unpriced. F101 opening also removes latch power. Pi/USB backfeed must not retain or re-energize rails; USB data is never routed through this PCB.

## 2. Latch-to-input-off timing and FET turn-off stress

KNOWN from IRF9540N p2: Qg max97 nC, Qgd max51 nC at ID=−11 A, VDS=−80 V, VGS=−10 V. Phase C's34 nC was only a typical-charge assumption. Datasheet switching delays use a5.1Ω gate driver and cannot be used for this1k pullup. These maxima do not cover arbitrary drain current, temperature and13.35 V initial gate excursion.

CALCULATED conservative gate-charge screen: scale97 nC by13.35/10 →129.495 nC (**ASSUMED scaling**). Once Q103 releases, the1k source-gate pullup supplies at least1 mA until |VGS| falls to1 V. `tgate≤129.495nC/1mA=129.495µs` within that assumed charge envelope. Add ASSUMED20µs latch/clamp/storage allowance →**149.495µs**, rounded to **150µs**; also calculate **1ms** as a slower cutoff sensitivity. At a2–4 V plateau, the51 nC Miller portion alone takes12.75–25.5µs. Guaranteed delay is **OPEN**, especially at high fault current. Q101-only source isolation remains FAIL regardless of this gate timing.

CALCULATED Q102 rectangular overlap screen `E=Vin×I×t`. All VDS can appear across Q102; dividing it equally between the two FETs is invalid. Q101 can still heat from channel current before interruption. At ASSUMED case50°C, graph-read padded Zjc=0.16 K/W at150µs or0.45 K/W at1ms gives the following **fixed-case thermal screens**, not a no-heatsink maximum:

| Vin / I | E at150µs | Tj at150µs | E at1ms | Tj at1ms |
| --- | ---: | ---: | ---: | ---: |
| 24 V / 3 A | 10.8 mJ | 61.5°C | 72.0 mJ | 82.4°C |
| 24 V / 10 A | 36.0 mJ | 88.4°C | 240.0 mJ | 158.0°C |
| 24 V / 50 A | 180.0 mJ | 242.0°C | 1200.0 mJ | 590.0°C |
| 64 V / 3 A | 28.8 mJ | 80.7°C | 192.0 mJ | 136.4°C |
| 64 V / 10 A | 96.0 mJ | 152.4°C | 640.0 mJ | 338.0°C |
| 64 V / 50 A | 480.0 mJ | 562.0°C | 3200.0 mJ | 1490.0°C |

OPEN SOA: manufacturer Fig8 is single-pulse, case25°C, Tj175°C. Visually the1ms curve allows order25 A at24 V and10 A at64 V; these are graphical estimates, not precision limits. A simple temperature scaling would reduce them at a hot case and does not qualify linear-mode stability. The150µs design cannot inherit the100µs curve directly. At64 V/50 A even the150µs thermal screen exceeds175°C (**FAIL screen**); source current therefore cannot be left unbounded. At3–10 A some numerical thermal screens pass, but actual VDS/ID/time trajectory, startup inrush, body-diode behavior, layout inductance and hot SOA remain OPEN. Q101's previous hot117mΩ×2 model adds I²×0.234×t per conducting device outside the overlap interval; do not double-count it inside a full Vin×I bound.

KNOWN unchanged blocker: SMCJ64CA's103 V rated clamp exceeds the100 V FET rating. The64 V DC rating screen is not surge coordination. At64 V the intended input OV detector should already open Q102; the64 V stress calculations cover delayed interruption/fault exposure, not permitted64 V buck operation. Buck36 V recommended/42 V absolute and50 V input capacitors remain unchanged constraints.

## 3. Bulk capacitance, trip threshold and actual Pi-node risk

| Candidate / KNOWN catalog | LCSC price observed / minimum | Electrical catalog facts | Decision |
| --- | --- | --- | --- |
| Panasonic EEUFR1A102 | $0.1751 at5+, buy5;110 in stock in direct snapshot | 1000µF±20%,10 V;28mΩ **impedance** at100kHz/20°C;1.79 A ripple at100kHz/105°C;10×16mm,5mm pitch | SELECTED two C217/C218; also evaluate one |
| Panasonic 6SEPC470M+TS | $1.0743 at1+, stock0 (reference price only) | 470µF±20%,6.3 V;8mΩ ESR at100–300kHz/20°C;5.7 A ripple at100kHz/105°C;8×13mm | Compared one/two; not selected: cost/stock/rating headroom |

EVIDENCE: [Panasonic FR-A](https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1259.pdf), [FR offer](https://www.lcsc.com/product-detail/C407868.html), [SEPC offer](https://www.lcsc.com/product-detail/C1578723.html). Direct supplier JSON is saved. Indexed $0.376/out-of-stock FR pages were stale and were not used. The6.3 V option has only0.8 V headroom above5.5 V;10 V has4.5 V. Neither is rated for an uncontained24 V short.

ASSUMED fault model: reuse Phase C initial voltage5.14613 V and inductor current6.32156 A at simultaneous load release/HS short. Source24/26 V, L4.352µH and saturated sensitivity2µH; raw effective ceramics110µF and40µF; bulk−20% initial capacitance. New25 V ceramics do **not** inherit a guaranteed110µF from the old16 V Murata model. These are sensitivity values only. Use raw bank ESR3mΩ and separate bulk branches; the FR28mΩ impedance is modeled as an ESR, with frequency/cold/endurance/ESL still OPEN.

CALCULATED state equations (load removed):

```text
Vraw = (IL + Vcer/Rcer + Vbulk/Rbulk) / (1/Rcer + 1/Rbulk)
dIL/dt = (Vin−Vraw)/L
 dVcer/dt = (Vraw−Vcer)/(Rcer Ccer)
dVbulk/dt = (Vraw−Vbulk)/(Rbulk Cbulk)
```

CALCULATED total post-threshold allowance starts at the **high trip5.43587 V**, includes detector+PNP+SCR establishment/commutation, and ends at5.5 V. A zero-impedance Pi interface makes Vpi=Vraw only for the following comparison. It is not a real Pi-pin bound:

| 24 V,4.352µH,110µF raw | Allowable delay | Vpi proxy at0.5µs | at2µs | at5µs |
| --- | ---: | ---: | ---: | ---: |
| 1× EEUFR1A102 | 0.6143µs | 5.48782 V | 5.65550 V | 6.03330 V |
| 2× EEUFR1A102 | 0.9367µs | 5.46983 V | 5.57543 V | 5.80254 V |
| 1× 6SEPC470M+TS | 0.7973µs | 5.47544 V | 5.60712 V | 5.92825 V |
| 2× 6SEPC470M+TS | 1.0910µs | 5.46454 V | 5.55788 V | 5.77736 V |

CALCULATED: the ideal lumped1710µF comparison would suggest **1.5902µs**, versus **0.9367µs** with separate ESR branches. Across the selected two-FR24/26 V,L/C sensitivities, allowance spans **0.4164–0.9367µs**. At26 V/2µH/40µF, even the0.5µs raw-node proxy reaches5.5130 V (**FAIL sensitivity**). Thus bulk improves the Phase C0.3807µs screen but cannot justify an arbitrary2–5µs response. Maximum raw voltage in the selected5µs sensitivity grid is **6.266 V**; this is not a bound for an unspecified delay.

KNOWN timing evidence: [TI TL431 SLVS543S](https://www.ti.com/lit/ds/symlink/tl431.pdf) gives response examples, not a guaranteed maximum comparator delay for this circuit. [ST TYN612 Rev11](https://www.st.com/resource/en/datasheet/tyn612.pdf) has no specified `tgt` maximum. Both maximum-delay fields are therefore `null` (**OPEN**) in the JSON, and0.5/2/5µs are ASSUMED sensitivities. No typical waveform is promoted to a maximum. SCR gate-current/cold latching issues from Phase C remain; the added latch trigger takes about0.4mA from Q301's collector and requires a fresh drive check.

CALCULATED normal/nuisance review: retain Phase C buck ratio/reference high5.13730 V, typical FB-current shift1mV and ripple screen15.65mVpp. With ASSUMED25mV release overshoot, high normal=5.17113 V;100mV gives5.24613 V. Against low trip5.18387 V, margins=+12.74mV /−62.26mV. Lowering R30330Ω to27Ω yields only5.56mV margin at25mV overshoot;24.9Ω leaves0.53mV;20Ω or a short already nuisance-trips in that screen. SELECTED retain30Ω/1.13k upper divider. No guaranteed positive lowering margin exists with an unbounded load release. An ASSUMED10mV noise/measurement reserve favors retaining30Ω, not lowering it. Even that reserve is not established over all corners.

OPEN new capacitor effect on normal operation: conservative ripple screens ignoring help from bulk give approximately 31.10mVpp for40µF raw and16.36mVpp for110µF. At40µF,25mV release margin drops to5.02mV. Actual PFM/light-load behavior, loop stability, ripple, biased C and overshoot must be measured after the added2mF bulk. At maximum normal stressed ripple, bank RMS≈0.763 A: even pessimistically assigning it all to one FR is below1.79 A at its catalog conditions. Frequency/temperature sharing and pulsed fault current are separate checks. Charging2mF to5.1 V adds26.01mJ nominal output stored energy and10.2mC charge; startup/current limit and soft-start need rechecking.

CALCULATED actual Pi-node sensitivity: add cable inductance0.2/1/2µH, series resistance9mΩ (cold fuse only) or59mΩ (fuse+ASSUMED50mΩ harness),40µF at the Pi, initial harness current5 A and complete load release. Integrate `Lh dIh/dt=Vraw−Vpi−Rh Ih`, `Cp dVpi/dt=Ih` alongside the raw/bulk states. SCR is an ASSUMED abrupt0.85 V+30mΩ clamp after the chosen delay. After firing, a50 A source-current ceiling is **ASSUMED only** to restrict this40µs illustrative window; no UENPO specification is inferred. ESL, semiconductor current spreading, reverse clamping and a real SBC are not modeled.

| Total delay0.5µs / cable | Pi peak at9mΩ | Pi peak at59mΩ |
| --- | ---: | ---: |
| 0.2µH | 5.5844 V | 5.4170 V |
| 1µH | 5.9269 V | 5.7018 V |
| 2µH | 6.1351 V | 5.9069 V |

**FAIL sensitivity / OPEN guarantee:** e.g.1µH/59mΩ reaches5.7018 V despite raw≈5.4711 V. Energy already in the harness/remote cap can overshoot at the Pi after raw clamping. These assumed harness values are not a claim about the final harness. Keeping F301 does not stop this current immediately. Added capacitance and latch do not establish Pi<5.5 V; resolve the real interconnect/decoupling/load waveform and damping before release. The59mΩ example also exceeds Phase C's≈47mΩ normal5 A path budget; it is a sensitivity, not a selected harness.

## 4. Raw capacitor voltage and fuse-first fault

CALCULATED / PASS topology-only: opening F301 leaves SCR301, the raw detector and C217/C218 continuously connected to VOUT_5V1. The specific Phase C path that disconnected protection from six raw caps is removed. Input shutdown then eliminates continuing source energy **only if Q102 actually opens and the latch persists**. A latched SCR does not behave as an ideal fixed-voltage clamp at unbounded current.

OPEN absolute containment: listed raw peaks under stated early-response assumptions are below16 V (and mostly below10 V), but there is no maximum detector delay, bounded source/ESL pulse or guaranteed gate trigger. Failed/late clamp, unlatching/retrigger, input-cutoff failure and external backfeed still permit raw voltage to approach the input or ring higher. A two-fault model is not silently made a new requirement; these paths identify why an unconditional “never exceeds rating” claim cannot be issued.

SELECTED risk-reduction candidate per C2 instruction: replace six C209–C214 with **GRM31CR61E476ME44L**,47µF25 V X5R±20%,**1206** (formerly1210). [Murata-authored sheet](https://datasheet.lcsc.com/datasheet/pdf/ba010764fbc88dc26754373c1e83b2ef.pdf?productCode=C403725), [LCSC offer](https://www.lcsc.com/product-detail/C403725.html). Price$0.6136 at1+, six installed=97,562.40 VND versus49,846.50 VND before: **+47,715.90 VND A/B**. Eight purchased under Phase C's spare rule=130,083.20 VND; seven under local plan=113,822.80 VND. The remaining two16 V Pi-side caps require their own voltage verification. New footprint, DC bias, tolerance and85°C body limit must be reviewed.

**FAIL rating fallback:**25 V covers a flat24 V only with1 V nominal margin; it does **not** cover26 V normal input,29.260 V upper input-trip screen, or64 V exposure. The new10 V bulk caps remain weaker if the crowbar does not contain the event. Merely raising the raw MLCC rating cannot qualify1R. If clamp-independent survival is required through29 V, at least a reviewed35 V-class reservoir/MLCC solution would be needed, plus ringing margin; it is outside this exact6.3/10 V bulk proposal and not silently substituted. C2's25 V candidate is costed explicitly, not described as fabrication-safe.

## 5. SCR pulse energy, holding current and no-heatsink temperature

KNOWN TYN612RG: ITSM140 A/10ms or145 A/8.3ms half-sine and I²t98 A²s at initial25°C; gate-conditioned dI/dt50 A/µs; IH maximum30mA and IL maximum60mA at25°C. Vto0.85 V/Rd30mΩ are the125°C on-state model. These are waveform/test-condition ratings; peak140 A is not a universal shorter-pulse ceiling, and98 A²s does not qualify arbitrary hot rectangular pulses. No `tgt`/turn-off recovery maximum is available in the reviewed sheet.

CALCULATED energy inventory at assumed clamp ceiling5.5 V: positive-tolerance output capacitance=2.8418mF (six new±20% raw MLCCs, two old±10% Pi MLCCs and two±20% bulk caps), storing42.982mJ. Protected input cap screen=164µF (120µF electrolytic +44µF ceramics), storing47.232mJ at24 V or335.872mJ at64 V. These upper initial-tolerance lumped screens do not guarantee voltage/temperature-dependent C. A64 V charged50 V reservoir is itself a failed input-containment case.

CALCULATED source-only pulse up to Q102 cutoff: `I²t=I² toff`, `E=(0.85 I+0.030 I²) toff`. At3/10/50 A and150µs: I²t=0.00135/0.015/0.375 A²s; energy=0.423/1.725/17.625mJ. At1ms:0.009/0.100/2.500 A²s;2.82/11.50/117.50mJ. Fuse clearing is not credited. These values alone omit the dominant capacitive pulses.

CALCULATED stored-energy sensitivity: model output discharge through31mΩ (30mΩ SCR model+ASSUMED1mΩ loop), initial I=(5.5−0.85)/0.031=150 A and I²t=0.99108 A²s. This uses an on-state resistance model, **not a guaranteed minimum resistance limiting the peak**. Model input reservoir discharge after opening via4.352µH and41.5mΩ (SCR+inductor). At24 V/10 A initial current, the input pulse reaches118.37 A and first zero occurs≈82.73µs after cutoff. Source limit upstream does not prevent this reservoir discharge. Input LC reversal is another unqualified capacitor stress; the first-zero model stops when SCR current becomes negative.

CALCULATED overlap-safe arithmetic for the three modeled positive components uses `(a+b+c)²≤3(a²+b²+c²)`. The following I²t/energy screens deliberately overestimate possible overlap; they are not self-consistent full-circuit simulations. “Temperature estimate” instead uses the illustrative time sequence (output discharge at firing, source rectangle until cutoff, input discharge after cutoff), and **must not be presented as a maximum**.

| Vin / source I / cutoff | Overlap I²t screen | E_SCR screen | No-sink Tj estimate at initial50°C |
| --- | ---: | ---: | ---: |
| 24 V / 3 A / 0.15ms | 4.7373 A²s | 159.12mJ | 88.2°C |
| 24 V / 10 A / 0.15ms | 4.7861 A²s | 161.48mJ | 90.4°C |
| 24 V / 50 A / 0.15ms | 6.0643 A²s | 205.06mJ | 107.3°C |
| 24 V / 10 A / 1ms | 5.0411 A²s | 176.35mJ | 77.7°C |
| 24 V / 50 A / 1ms | 12.4393 A²s | 432.43mJ | 103.5°C |
| 64 V / 10 A / 0.15ms | 16.1176 A²s | 510.72mJ | 206.1°C |

ASSUMED thermal method: graph-read ST Fig4 Zjc≈0.221 K/W at1ms and0.65 K/W at10ms; below1ms extrapolate `Zjc=0.221 sqrt(t/1ms)`. Convolve power steps with this step response and add adiabatic case rise using **ASSUMED0.1 J/K package heat capacity**, no external heatsink. The sub-ms extrapolation, case capacity, current waveform and uniform SCR turn-on are **unverified**; the vendor's free-air Fig5 starts at10ms. JSON also retains an independent2–10mJ/K effective thermal-capacity sensitivity and a rounded1.8 K/W≤10ms source-rectangle-only Zja screen. Those models illustrate uncertainty, not interchangeable maximum temperatures. A64 V/10 A event estimate above125°C fails this illustrative model;24 V examples cannot be qualified merely because some estimates fall below125°C. Hot initial temperature and repeated events reduce margin.

**FAIL di/dt sensitivity / OPEN pulse qualification:** ASSUMED10nH local loop gives(5.5−0.85)/10nH≈465 A/µs versus the50 A/µs gate-conditioned rating. Raw ceramics bypass bulk ESR. To reach50 A/µs the ideal required loop inductance is93nH, and adding inductance can worsen clamp/Pi overshoot. This is not permission to add a series fuse or arbitrary inductor. Qualify gate rise, loop parasitics, current distribution, peak pulse and waveform-specific ITSM/I²t. The added bulk increases total stored energy and can worsen the SCR's initial pulse even while slowing the pre-trip rise.

OPEN holding-current guarantee:30mA is an **IH maximum**, not a minimum; merely calculating current<30mA does not prove every device unlatches. Input off-state leakage, external5 V backfeed and gate bias must be excluded or diverted so anode current is driven essentially to zero long enough for recovery. For the isolated24 V/10 A RLC screen, anode supply current reaches zero≈82.73µs after150µs cutoff, i.e.≈233µs after the latch signal in this model. Output RC tail to an ASSUMED1µA takes≈1.66ms. These are residual-energy times, not manufacturer recovery guarantees. With gate drive gone, no backfeed and continued input isolation, finite stored energy dissipates and SCR conduction ceases; subsequent supply removal resets the latch. Actual IH minimum, recovery, leakage, brownout memory and zero-current duration remain OPEN. F301 is not relied upon to open for this sequence.

DECISION: the indefinite-current thermal defect can be removed **conditionally** by a proven persistent latch and effective Q102 cutoff; the literal Q101-only implementation leaves it unresolved. Single-event no-heatsink survival is **OPEN** because the early pulses and source/case envelope are unqualified. Keep40,000 VND thermal contingency until measured qualification supports deleting it; show the zero-contingency cost separately.

## 6. Revised BOM, A/B/C and local-sourcing reconciliation

SELECTED [C2 BOM](PHASE_C2_BOM.csv) adds two FR bulk caps; replaces six raw MLCCs with25 V1206 parts; adds Q104/Q106 MMBTA42-TP,Q105 BC807-40,215,four10k and three100k resistors. SCR,TL431s,input FETs,both fuses,buck,L and trip divider remain exact previous MPNs. The latch is a proposed correction to the brief's Q101 reference, not a qualified circuit. All changed safety parts retain exact-MPN control; local passive candidates below are a separate cost scenario requiring approval of electrical equivalence. Old Phase C BOM/history remain available.

ASSUMED accounting:26,500 VND/USD; A is installed core, B adds installed connector/mate/contacts23,685.70 VND and one allocated bare board10,600 VND. C includes actual minimum-lot purchases and a five-board order. Phase C spare rule is `n+max(1,ceil(25% n))`; local-plan rule is `n+1`. Both aggregate identical MPNs before MOQ rounding. The40,000 thermal line is a contingency, not installed heatsink evidence. One versus two FR caps still buys the same five-piece lot, so the second cap adds4,640.15 VND A/B and no current minimum-lot C cost.

| CALCULATED planning scope | VND |
| --- | ---: |
| A installed core | **348,655.20** |
| B core + installed interfaces + allocated PCB | **382,940.90** |
| C Phase C purchasing/overhead convention | **1,603,992.70** |
| C above1,000,000 | **+603,992.70 — FAIL** |
| C using sibling local-sourcing approach | **1,277,914.55** |
| Local C above1,000,000 | **+277,914.55 — FAIL** |
| Local C if40k thermal contingency removed after qualification | 1,237,914.55 |
| Above plus local pickup instead of20k delivery | 1,217,914.55 |

CALCULATED reconciliation: original Phase C C1,492,247.50 → C2 **+111,745.20 VND**, to1,603,992.70. Read-only sibling plan1,155,929.75 → C2 local **+121,984.80 VND**, to1,277,914.55. Local core procurement is840,195.55 VND: inherited18,200 local generic lots plus821,995.55 exact-MPN procurement. It is recomputed from the revised quantities rather than adding a guessed latch allowance. The25 V replacement splits old/new MLCC lots; the new transistor/resistor quantities still fit their existing minimum lots. Upstream TVS is two units at ASSUMED$0.50 (26,500 VND), still a failed coordination candidate. An acceptable redesign is unpriced.

| ASSUMED cost outside core | Conventional C | Local C |
| --- | ---: | ---: |
| Five bare PCBs | 53,000 | 53,000 |
| Connector purchase lots / local3 kits | 263,502.75 | 4,719 |
| Wire, heat-shrink, strain relief | 35,000 | 20,000 |
| Component shipping/import reserve | included below | 80,000 |
| PCB shipping/tax reserve | included below | 120,000 |
| Combined conventional freight/tax | 180,000 | — |
| Local delivery reserve | — | 20,000 |
| Manual assembly/consumables | 50,000 | 50,000 |
| Rework contingency | 50,000 | 50,000 |
| Thermal qualification contingency | 40,000 | 40,000 |

CALCULATED local freight/delivery+assembly+rework+thermal allowances total360,000 VND, listed separately rather than hidden in component cost. Removing the thermal allowance alone still leaves237,914.55 VND above budget; removing local delivery as well leaves217,914.55 VND above. No reserve is silently waived. The historical local connector/passive offers were not refreshed; exact mechanical/rating verification remains OPEN. Local shared100nF and50-piece resistor lots are charged once. Safety-critical capacitors,precision resistors,fuses,semiconductors stay exact. Current TVS3300DRVR/MMBTA42 stock, source fault limits, hot thermal hardware, shipping/tax and any required reset/hold-up/redesign remain OPEN and can increase totals. These are planning costs, not buyable complete landed quotes.

## 7. Phase D schematic change list for1R — proposed only

1. **Sheet01/input:** retain Phase C two-FET orientation,F101,clamps,divider and ballast. Resolve Q101/Q102 naming conflict in the architect review; apply the output fault inhibit to forward-blocking Q102 by clamping Q103 base. Add Q104/Q105/Q106,R160–R166 exactly as §1; nets SET_LATCH and LATCH_H; supply CTRL12 upstream of cutoff. Document reset-on-input-removal and qualify startup/brownout; do not use EN/FB. Add sense pads TP110 SET_LATCH,TP111 LATCH_H,TP112 Q106 collector/IN_NPN_BASE. Review10k/100k leakage, feedback, return paths and pulse capture.
2. **Sheet02/buck:** add polarized C217/C218 EEUFR1A102 across VOUT_5V1/GND beside raw bank and SCR loop,10×16mm/5mm pitch. Change C209–C214 to GRM31CR61E476ME44L,1206. Requalify effective C, loop response,inrush,ripple and85°C MLCC body temperature. Keep BIAS=GND, existing RT/FB/EN independent connections and manufacturer switching-loop geometry. No output change is released by a catalog voltage rating alone.
3. **Sheet03/protection:** connect SCR301 anode directly to raw node before F301; move U301 divider top and Q301 emitter to raw. Keep same ground-referenced detector,PNP and SCR gate parts, and1k+100Ω+30Ω/1k threshold. Route CB_COLLECTOR trigger to R163. Keep F301 only VOUT_5V1→LOAD_5V1. C301/C302 remain Pi side; check their remote energy/backfeed and branch resistance. Mark fuse “wiring backup; not crowbar clearing.” No fuse/link between raw caps and SCR. Keep separate Kelvin sense/quiet-ground routes and current return geometry.
4. **Sheet05/root/interfaces:** add the fault-trigger interface from output protection to input latch; no removed research control is implicitly retained. Preserve VIN_RAW,VIN_PROTECTED,VOUT_5V1,LOAD_5V1,GND meanings; no duplicate ambiguous force nets. Retain output connector/harness test access; no telemetry,I2C,USB3 or D435i data routing. Update removed-function ledger: input shutdown and fault memory are now proposed restorations, and bulk reservoirs are partly restored.
5. **Before R2 release:** independently check exact package,pin numbering,polarity,voltage/current/thermal ratings and tab potentials; reconcile every reference with C2 BOM; export native netlist and verify raw-crowbar continuity for F301 open. Verify latch persists with output zero,Q102 gate reaches source,and no EN/FB dependency. Run ERC after each schematic change and inspect all pages. No schematic change occurred in C2; no ERC PASS is claimed. Only after R2 approval may R3 layout/DRC/visual review proceed.
6. **Required closure evidence:** bounded source/cap/harness model, guaranteed or qualified worst-case OV timing,Pi-node transient,normal nuisance-trip margin,SCR gate pulse/di/dt,I²t/thermal/recovery,latch capture/reset,hot Q102 SOA,upstream TVS coordination,raw/bulk rating containment,loop stability,and full landed costs. Preserve the project sequence: visual→continuity→limited bench supply→no-load→rail verification→small dummy load→load steps→thermal→ripple→transient→fault/latch→telemetry N/A→SBC only after earlier gates pass. Never first-test OV with an expensive SBC.

## 8. PASS / FAIL / OPEN ledger

| Check (limited scope) | Result |
| --- | --- |
| 01 raw crowbar no intervening fuse topology | **PASS** |
| 02 literal Q101 only input isolation | **FAIL** |
| 03 Q102 latch static bias screen | **PASS** |
| 04 power removal only reset and max cutoff delay | **OPEN** |
| 05 selected 24V 0p5us unity interface screen | **PASS** |
| 06 selected 24V 2us unity interface screen | **FAIL** |
| 07 guaranteed Pi pin less than 5p5V | **OPEN** |
| 07b Pi 1uH 59mohm 0p5us sensitivity | **FAIL** |
| 08 normal nuisance trip 100mV screen | **FAIL** |
| 09 F301 open no longer disconnects raw SCR | **PASS** |
| 10 25V caps at uncontained 26 to 29V | **FAIL** |
| 11 guaranteed raw cap voltage containment | **OPEN** |
| 12 SCR local 10nH di dt screen | **FAIL** |
| 13 SCR I2t temperature no heatsink qualification | **OPEN** |
| 14 SCR holding current zero current and backfeed | **OPEN** |
| 15 FET 24V 64V turnoff hot SOA | **OPEN** |
| 16 existing 103V TVS to 100V FET | **FAIL** |
| 17 cost C under 1000000 | **FAIL** |
| 18 local cost C under 1000000 | **FAIL** |
| 19 Phase D change list and C2 evidence | **PASS** |
| 20 R1 release hardware qualification | **OPEN** |

EVIDENCE / verification: [C2 verification](PHASE_C2_VERIFICATION.json) records deterministic regeneration, numerical convergence and an independent matrix-exponential check of the early ESR model, BOM/MOQ/local-lot accounting and unchanged historical/CAD scope. This is numerical/document evidence, not electrical validation. KNOWN Git result: authorized staging failed with `Unable to create .../.git/worktrees/wt-lite/index.lock: Operation not permitted` (exit128). Per the brief, leave all C2 work **uncommitted**; HEAD remains `b5461b0`. See [Git log](PHASE_C2_GIT_LOG.txt). No permissions/lock changes, push or purchase.

**DECISION: R1 release and Phase D implementation BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

LITEC2-HANDBACK
