# V1A-Lite Phase C — Option 1 calculation and design review

**2026-10-05. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**DECISION: Phase C analysis delivered; R1 electrical release and Phase D implementation remain BLOCKED.** The selected baseline does not yet establish input fault survival or the Pi voltage ceiling. Budget C also fails the stated ceiling.

KNOWN: owner selected Option 1. This analysis starts at `6cfe313` on `feat/v1a-lite-cost-reduction`, follows the complete `V1A_LITE_PHASE_C.md`, and uses Phase A audit and Phase B architecture/BOM/calculations/script. Work is direct, without sub-agents. No schematic, PCB or library edits, purchases or push are authorized here. This is an R1 calculation review, not an R2 capture release.

REQUIREMENT / KNOWN: 24 V auxiliary input, **18–26 V normal**, continuous **54.6–64 V upstream fault**, 5.1 V-class / 5 A output, independent fuse/SCR OV protection, Pi connector **≥4.75 V and <5.5 V**, no telemetry. Phase C resolves Phase B's 26/28 V normal-range conflict in favor of 26 V. The upstream identity is UENPO S4-T482410; its actual current limit, hiccup waveform, reservoir capacitance and failed-switch source impedance remain OPEN. No current rating is inferred from its model number.

Labels apply to every value in their paragraph/table: KNOWN = owner requirement or cited fact; SELECTED = owner architecture or exact analysis-BOM choice (not qualification); CALCULATED = reproducible arithmetic; ASSUMED = sensitivity/accounting input; PROPOSED = future change/test; OPEN = missing bound. PASS means the named limited check only. FAIL means the stated screen fails; it is not a prediction that every prototype fails. OPEN is not PASS. OBSERVATION/EVIDENCE/DECISION/OPEN RISK headings retain these distinctions.

Reproduce with `python3 docs/evidence/v1a_lite/calculate_phase_c.py`. JSON contains labeled inputs and derived results. Sources and access dates: [Phase C register](../../../third_party/v1a_lite_phase_c/SOURCES.md). Historical Phase A/B evidence is preserved.

## 1. Input ratings and TVS — partial DC PASS; surge coordination FAIL

SELECTED analysis topology:

```text
J501 VIN_RAW -> F101 -> VIN_FUSED -> Q101 D; Q101 S = S_COMMON = Q102 S
                         | D101 bidirectional TVS               Q102 D -> VIN_PROTECTED
                         |                                                | D106 TVS3300
                        GND                                               | input capacitors
```

DECISION / SELECTED: two **IRF9540NPBF** P-FETs are necessary. A single reverse-oriented P-FET has a forward body-diode path and cannot interrupt positive input OV. Q101 provides reverse-polarity blocking; Q102's opposing diode provides forward cutoff. Each needs its own source-to-gate zener. This retains Phase B's common-source topology and the owner's 100 V P-FET class.

| SELECTED part / exposure | KNOWN rating or CALCULATED stress | Disposition |
| --- | --- | --- |
| J501/J502 JST B2P-VH-FB-B(LF)(SN), VHR-2N, SVH-41T-P1.1 | Family 250 V; actual mated wire/current/temperature rating OPEN | Voltage nominally adequate; exact harness qualification OPEN |
| F101 0451003.MRL | 3 A, 125 V marking; manufacturer's 2–5 A entry includes 10 kA at 75 VDC | 64 V nominal interrupt-voltage screen PASS; prospective current/agency conditions OPEN; AC marking alone not used |
| D101 **Bourns SMCJ64CA** across VIN_FUSED/GND | Bidirectional, 64 V standoff; 71.1–78.6 V breakdown, 103 V maximum clamp at 14.6 A specified pulse | Does not intentionally avalanche at ±64 V. **FAIL as a guaranteed clamp for 100 V FETs**; even before wiring overshoot |
| Q101/Q102 IRF9540NPBF | 100 V VDS, ±20 V VGS; 64 V off-state gives 36 V nominal headroom | DC voltage screen PASS only. Powered reverse with 36 V retained source and −64 V drain reaches 100 V: no margin |
| D102/D103/D104 BZT52C12-7-F | Q101/Q102 VGS clamps / CTRL12 shunt; 11.4–12.7 V at 5 mA, positive 6–10 mV/°C coefficient | Not exposed directly across 64 V; actual-current and hot clamp verification OPEN |
| Q103 MMBTA42-TP | Manufacturer indexed 300 V VCEO | Nominal 64 V collector screen PASS; exact current/gain/storage/thermal behavior OPEN |
| U101 TL431BIDBZR; D105 BZT52C3V3-7-F; C102 GRM21BR71C105KA01L | TL431 cathode recommended max 36 V /absolute max 37 V, control capacitor 16 V; supplied through ballasted CTRL12 | Conditional on intact clamp. Reverse supply blocked by Q101; no direct raw-input connection |
| R101/R102 10 kΩ 0805 gate pull-down chain | At 64 V / 12 V clamp, 0.1352 W total, 26 V and 0.0676 W each | Hot derating and maximum working voltage OPEN |
| R110–R125 control ballast, R130–R135 gate ballast, R140–R143 gate-source pullup, R144–R147 control resistors | Detailed current, power and divider exposures in §2 | No 0603 is assumed to dissipate a full multiwatt chain loss |
| R150–R153 OV divider | 100 kΩ +1 kΩ +1 kΩ upper, 10 kΩ lower; upper 100 kΩ sees approximately 57 V /33 mW at 64 V | Working-voltage nominal screen adequate for precision 0603; temperature/pin behavior OPEN |
| D106 TVS3300DRVR after Q102 | 33 V standoff; ≤40 V for specified 15 A 8/20 µs test, 42 V buck absolute max | Cannot ensure buck's 36 V operating limit. Pulse/wiring margin OPEN. Never place this part directly across 64 V |
| C101 EEUFR1H101; C201/C202/C215/C216 GRM32ER71H106KA12L; C203/C204 GRM188R71H104KA93D | All 50 V; behind cutoff | Adequate only when cutoff limits VIN_PROTECTED. **FAIL if directly exposed to 64 V**. Electrolytic must not see negative voltage |
| U201 LM61460 and R206/R207 EN divider | Buck 36 V recommended /42 V absolute; EN 42 V absolute | Cutoff timing essential; 100 V upstream FET marking does not protect these pins by itself |

OPEN RISK: a 64 V TVS standoff is a test condition, not a guaranteed zero-current condition over all temperatures. Leakage heating at hot ±64 V, tolerances on the owner bus and surge waveform must be specified. The SMCJ64CA price is an explicit estimate pending an exact quote; it is costed as a **rejected surge-coordination candidate**, not purchase approval. Raising standoff to 70 V worsens the clamp margin; using 60 V standoff violates the continuous-fault intent. A higher-voltage FET or a bounded lower-current clamp solution requires a reviewed revision. No surge amplitude/duration requirement is invented here.

EVIDENCE: [Bourns SMCJ datasheet](https://www.bourns.com/data/global/pdfs/SMCJ.pdf), [Infineon FET](https://www.infineon.com/dgdl/Infineon-IRF9540N-DataSheet-v01_01-EN.pdf?fileId=5546d462533600a401535611cfa21dc8), [Littelfuse 451/453](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1), [TI TVS3300](https://www.ti.com/lit/ds/symlink/tvs3300.pdf). Accessed 2026-10-05 or inherited read-only source as registered.

## 2. Exact input cutoff concept — static screen PASS; guaranteed cutoff OPEN

SELECTED: Q101/Q102 **IRF9540NPBF** (TO-220 G=1, D/tab=2, S=3); U101 **TL431BIDBZR**; Q103 **MCC MMBTA42-TP**; D102/D103/D104 **BZT52C12-7-F**; D105 **BZT52C3V3-7-F**. Q101 drain at VIN_FUSED and source at S_COMMON; Q102 source at S_COMMON and drain at VIN_PROTECTED. D102/D103 cathodes at source, anodes at their respective gates. Q101 gate uses R101+R102=20 kΩ to GND. Controller observes S_COMMON, so opening Q102 does not remove OV detection.

SELECTED E96 divider: R150 **TNPW0603100KBEEA** 100 kΩ, R151/R152 **RT0603BRD071KL** 1 kΩ each in series above REF, R153 **TNPW060310K0BEEA** 10 kΩ below REF. Every constituent is an E96 value, 0.1%. This replaces Phase B's 110 kΩ/10 kΩ. Nominal ideal trip is **27.944 V**, or **28.148 V** with typical 2 µA REF current.

ASSUMED temperature screen: −40…85°C, precision-resistor TCR ±25 ppm/°C independently, maximum displacement from 25°C of 65°C. Exact TCR suffix qualification and actual system ambient are OPEN. Use combined resistor error `e=0.001+65×25e−6=0.002625`. KNOWN TL431BI reference limits at 10 mA are 2.483–2.507 V; pessimistically add ±34 mV full-range deviation, REF current 0…6.5 µA, and ASSUMED 26 mV lowering reserve for cathode movement. [TI TL431 §6.12](https://www.ti.com/lit/ds/symlink/tl431.pdf).

CALCULATED:

```text
Vtrip_low = (2.483−0.034−0.026) × [1+102k(1−e)/(10k(1+e))] =27.0082 V
Vtrip_high = (2.507+0.034) × [1+102k(1+e)/(10k(1−e))]
             +6.5µA×102k(1+e) =29.2604 V
```

CALCULATED static screen: minimum trip is 1.008 V above 26 V normal; high trip leaves 6.740 V to 36 V. **PASS only for this conditional threshold screen.** U101 cathode current changes during switching; this is not a guaranteed production threshold. SELECTED no positive-feedback hysteresis. Ideal release uses the same 27.944 V reference crossing; the same 27.008–29.260 V envelope is the best static release screen, not a promised hysteresis band. Actual release, chatter and delayed re-enable are OPEN. A fixed numeric hysteresis cannot be claimed for this network.

SELECTED detector connections: S_COMMON → R110–R125 → CTRL12; D104 and C102 from CTRL12 to GND. R110–R117 form one 8×1 kΩ series string; R118–R125 a second parallel string: net 4 kΩ. All are **0603WAF1001T5E**. This doubles Phase B's resistor count to halve individual dissipation. CTRL12 → R144 1 kΩ → U101 cathode; cathode → D105 cathode, D105 anode → R145 10 kΩ → Q103 base. R146 100 kΩ base-to-GND. Q103 emitter to GND; collector via R130–R135 (6×100 Ω **0603WAF1000T5E**) to Q102 gate. Q102 gate-source pullup is R140–R143, two parallel strings of 2×1 kΩ, net 1 kΩ; this replaces the overstressed single 0603. U101 anode is GND. R147 is unused/reserved, not a purchased part.

CALCULATED DC model assumes 12 V clamp, 3.3 V level shift, 0.7 V NPN VBE and 2.5 V conducting TL431 cathode. The rail is **not** always 12 V:

| Vin | CTRL12 with TL431 OFF / ON | TL431 current if ON | Ballast power ON / each of 16 |
| ---: | ---: | ---: | ---: |
| 18 V | 12 /5.60 V | 3.10 mA | 0.0384 /0.00240 W |
| 24 V | 12 /6.80 V | 4.30 mA | 0.0740 /0.00462 W |
| 26 V | 12 /7.20 V | 4.70 mA | 0.0884 /0.00552 W |
| 27.944 V | 12 /7.5888 V | 5.0888 mA | 0.1036 /0.00647 W |
| 54.6 V | 12 /12 V | 9.50 mA | 0.4537 /0.02836 W |
| 64 V | 12 /12 V | 9.50 mA | 0.6760 /0.04225 W |

CALCULATED normal OFF-model NPN base drive is about 0.720 mA after base bleed. At 18 V only 1.5 mA feeds CTRL12; remaining nominal zener current is about 0.773 mA, below its 5 mA characterization. At 26 V Q103 must sink approximately `(26−12−0.2)/600=23 mA`; forced gain ≈32. Saturation at this drive and cold temperature is not established by a gain measurement at high VCE. Low gate drive raises FET resistance, so the 117 mΩ loss model remains conditional. The TL431's ≥0.7 mA regulation-current screen passes once ON, but does not replace its 10 mA threshold test conditions or prove fast comparator behavior.

CALCULATED at 64 V: detector-feed power is 0.832 W (52 V×13 mA resistor loss plus clamp/cathode consumption). D104 nominal dissipation is 42 mW with 9.5 mA cathode load, or 156 mW for a disconnected load. R144 dissipates 90.25 mW at 9.5 mA: **hot 0603 derating remains OPEN**. Q101 gate chain dissipates 135.2 mW total, clamp about 31.2 mW. Q102 pullup dissipates 144 mW total at 12 V, 36 mW in each replacement resistor. At hot assumed 13.35 V clamp it becomes 178.2 mW total. Detector divider power is approximately 36.6 mW at 64 V including REF-current effects only approximately. Gate-sink ballast can see **4.47 W total /0.745 W each** while Q103 remains on after a 64 V step; resistor pulse-energy ratings must be verified.

KNOWN/ASSUMED gate clamp: the Diodes table gives 12.7 V upper at 5 mA/25°C; adding 10 mV/°C×65°C gives a conservative **13.35 V screen**, below ±20 V, before dynamic-current effects. Its differential impedance near that test is 25 Ω; this is not a global high-current clamp equation. The 3.3 V level-shift diode has 3.1–3.5 V limits at 5 mA, while this base network uses sub-mA current. Consequently the digital-looking ON/OFF description is only a circuit hypothesis. [Diodes DS18004](https://www.diodes.com/_files/datasheets/ds18004.pdf).

CALCULATED timing model: with ASSUMED minimum effective input C=92 µF, allowable excess charge from high trip to 36 V is **620.05 µC** (to 42 V: **1172.05 µC**). `dV/dt=(Iin−Ibuck)/C`; table currents below are **excess charging current**, not a UENPO rating. The model starts at the high trip crossing and excludes gate capacitive feedthrough, ESL and wiring ringing.

| ASSUMED excess current | CALCULATED dV/dt | Allowed time to 36 V | Peak after ASSUMED 25 µs |
| ---: | ---: | ---: | ---: |
| 3 A | 0.03261 V/µs | 206.68 µs | 30.076 V |
| 15 A | 0.16304 V/µs | 41.34 µs | 33.336 V |
| 100 A | 1.08696 V/µs | 6.20 µs | 56.434 V: FAIL without clamp |

ASSUMED Phase B Miller-charge example of 34 nC and a 2–4 V plateau into 1 kΩ implies **8.5–17 µs**, before TL431 propagation, Q103 storage and gate tail. The 25 µs total is not a guaranteed device delay. D106 may limit the failed 100 A screen only within its own pulse capability; its clamp is above 36 V and its 15 A rating is not permission to absorb 100 A. A source step into an already-on FET need not follow a slow input threshold sweep. **OPEN: VIN never exceeding 36 V /42 V absolute cannot be proved without bounded source impedance/current and measured worst-case timing.**

OPEN SOA: the Infineon plot is a case-temperature/single-pulse envelope, not a hot repetitive linear-use guarantee. Required trajectory checks are turn-off at up to 64 V with the actual drain current, startup C charging, threshold chatter and hot-plug/reversal. A conservative rectangular overlap estimate is `64×I×25µs`: **4.8 /24 /160 mJ** for the above currents; energy alone is insufficient. At 26 V, 92 µF stores **31.10 mJ**; abrupt startup can require comparable FET dissipation and unbounded peak current. No numeric hot SOA margin is claimed. Stable 64 V OFF is a leakage/heating problem (not 64 V×normal load current); leakage at the actual hot VDS and any source ringing is OPEN.

OPEN cold-start: Q102 defaults OFF through its source pullup, but Q103 can begin conduction while CTRL12 and U101 settle. REF may already indicate OV when the cathode supply first becomes active; this does not prove a glitch-free OFF state. No startup interlock or UV-valid latch exists. Test cold connection directly to 54.6/64 V, slow ramps, partial disconnect and repetitive crossings.

OPEN reverse-polarity behavior: for an initially discharged board, Q101's diode blocks negative VIN_FUSED; the bidirectional D101 does not deliberately short −64 V. Control is isolated at S_COMMON. Reversal while S_COMMON is charged can leave Q101 temporarily enhanced; the circuit is not active ideal-diode reverse-current protection. With a retained 26 V source node, −64 V implies 90 V VDS before spikes; retained 36 V consumes all 100 V rating. Check gate positive clamp, body-diode recovery, backfeeding via Q102's diode, control discharge, and no negative C101/U201 voltage. **Reverse steady-state screening alone is not a transient PASS.**

## 3. LM61460 recalculation — component screens PASS; 5 A performance OPEN

SELECTED U201 **LM61460AANRJRR**, L201 **SRP1265A-6R8M**, R202 **TNPW0603100KBEEA** 100 kΩ and R203 **RT0603BRD0724K6L** 24.6 kΩ. The ratio is retained exactly as requested; the lower resistor uses the cheaper Phase B identity. CALCULATED nominal output `1 V×(1+100k/24.6k)=5.06504065 V`; “5.1 V” remains the output class, not an exact 5.100 V setting.

CALCULATED ±1% FB reference and ±0.1% resistor-only bounds at reference temperature are 5.00635–5.12391 V (Phase B); adding the ASSUMED independent ±25 ppm/°C over 65°C gives **4.99332–5.13730 V**. KNOWN FB current is 10 nA **typical**, adding about 1 mV; its unspecified maximum is OPEN. TI's ±1% condition is FPWM. This exact auto-mode part's light-load PFM ripple/regulation requires separate testing; do not apply the FPWM bound to every no-load state. [TI §§7.4, 9.2.2.2](https://www.ti.com/lit/ds/symlink/lm61460.pdf).

SELECTED R201 **TNPW060333K2BEEA** 33.2 kΩ. CALCULATED using TI equation2, `RRT[kΩ]=(1/f[kHz]−3.3e−5)×1.346e4`, frequency ≈**400.069 kHz**. KNOWN table range is 360–440 kHz; ASSUMED screen 356.4–444.4 kHz adds a conservative 1% resistor/model reserve. At 26 V/444.4 kHz the required ON time is ≈441 ns, comfortably above the 70 ns specified minimum-ON-time maximum. Minimum-OFF-time 85 ns is also nonbinding over 18–26 V. Startup/dropout and PFM have different waveforms.

KNOWN Bourns data at 25°C: **6.8 µH ±20%, 18 A Isat at 20% inductance drop, 11.5 A Irms at 40°C rise, 11.5 mΩ maximum DCR**. SELECTED this exact MPN, not the previous 10 µH part. CALCULATED ripple uses 5.1 V conservatively: `ΔI=Vo(1−Vo/Vin)/(L f)`, `Ipk=5+ΔI/2`, `Irms=sqrt(25+ΔI²/12)`. ASSUMED stressed L=6.8×0.8×0.8=**4.352 µH**, f=356.4 kHz. [Bourns Rev06/24](https://www.bourns.com/docs/product-datasheets/srp1265a.pdf).

| CALCULATED Vin | Nominal ripple /peak | Stressed ripple /peak | Stressed Irms |
| ---: | ---: | ---: | ---: |
| 18 V | 1.344 /5.672 A | 2.356 /6.178 A | 5.046 A |
| 24 V | 1.477 /5.738 A | 2.589 /6.295 A | 5.056 A |
| 26 V | 1.507 /5.754 A | 2.643 /6.322 A | 5.058 A |
| 36 V, boundary screen only | 1.609 /5.805 A | 2.822 /6.411 A | 5.066 A |

CALCULATED normal peaks fit below minimum 8.9 A low-duty HS limit. KNOWN TI's maximum HS current limit is **11.5 A**, with duty dependence; catalog Isat 18 A exceeds that recommendation. **PASS catalog comparison only**: Bourns' typical/current-definition data do not guarantee minimum hot differential inductance during fault. Low-side valley limit is 6.1–8.1 A. A physically shorted HS switch bypasses both limits. The fault-current analysis must not assume 18 A is a hard current limiter or retain constant L beyond saturation.

CALCULATED TI equation11 minimum L at duty<50% is **2.862 µH**, below stressed 4.352 µH. Minimum ripple at 18 V, L=8.16 µH, f=444.4 kHz is **1.008 A**, above the 0.6 A rule-of-thumb floor (10% of 6 A device rating). Nominal ripple is approximately 22–25% of 6 A; use device rating in TI's ripple-selection equation. Startup at duty>50% requires equation10 and separate loop checks.

| SELECTED capacitors | KNOWN nominal / CALCULATED or ASSUMED effective C | Ripple/rating disposition |
| --- | --- | --- |
| C201/C202/C215/C216 **GRM32ER71H106KA12L**, four 10 µF/50 V X7R | ASSUMED 40% bias retention×0.9 tolerance×0.85 temperature = **12.24 µF** total | Above TI's 10 µF target only conditionally; bias model unavailable/EOL part, procurement and guaranteed effective minimum OPEN |
| C203/C204 **GRM188R71H104KA93D**, two 100 nF/50 V X7R | Local HF bypass at both VIN/PGND pairs; not counted in minimum bulk C | Exact placement and spike/ripple heating OPEN |
| C101 **EEUFR1H101**, 100 µF/50 V | ASSUMED ≥80 µF initial; cold/ESR/aging minimum OPEN | Damping bulk after Q102; do not assign all switching RMS to it. Exact frequency/temperature ripple-current rating verification OPEN |
| C209–C214 **GRM32ER61C476KE15L**, six 47 µF/16 V X5R | KNOWN typical manufacturer model 29.728753 µF each at 5.1 V, 28.008429 at 5.5 V; CALCULATED 122.809/115.703 µF after 0.9×0.85×0.9 | ASSUMED 120 µF normal, 110 µF fault screen; no production minimum guarantee. X5R maximum body temperature85°C; raw-side fault rating FAIL if F301 opens first |
| C301/C302 same 47 µF/16 V MPN | Two local protected parts; about 40 µF conservative screen | SCR-loop location matters; cannot simply add them through unknown fuse/cable inductance |
| C205 **GRM188R71C104KA01D** | 100 nF/16 V X7R, CBOOT to native SW | Differential rating; not from BOOT to GND |
| C206/C102 **GRM21BR71C105KA01L** | 1 µF/16 V X7R, VCC bypass /input-control bypass | Biased effective minimum OPEN; C102 is not an independent protection hold-up supply |

CALCULATED ideal input capacitor RMS `5√[D(1−D)]` is **2.253 /2.045 /1.985 A** at 18/24/26 V; TI's conservative general screen is 2.5 A. Equal sharing would be 0.563 A per bulk ceramic at 18 V, but layout makes sharing unequal. Stressed output ripple RMS is **0.763 A total at 26 V**, or 0.127 A per raw ceramic under equal sharing. MLCCs have no convenient blanket current rating here: verify impedance/loss and temperature rise for the actual package, frequency and layout. No ripple-current PASS is asserted for C101 or the ceramics without this evidence.

CALCULATED with ASSUMED raw-bank ESR=3 mΩ, C=120 µF: `ΔVo≈ΔIL/(8 f C)+ΔIL×ESR` = **15.65 mV p-p** at 26 V stressed; excludes spikes/ESL and PFM. Adding half-ripple, typical FB-current shift and ASSUMED 25 mV /100 mV release overshoot to static high gives **5.17113 /5.24613 V**. There is no measured “maximum normal” yet. At the low corner, subtracting half-ripple leaves **47.10 mΩ total path budget at 5 A** before load-step droop; a 9 mΩ cold output fuse leaves **38.10 mΩ** for hot-fuse increment, both conductors, connectors and harness. A 5 A/10 µs unsupported step on 120 µF plus ESR gives **0.4317 V** droop: the capacitors alone do not establish Pi ≥4.75 V.

SELECTED stability starting point: C207 **C0402C220J4GACTU** 22 pF C0G in series with R205 **0603WAF1001T5E** 1 kΩ from raw output to FB. CALCULATED ideal zero≈72.34 kHz, pole≈366.42 kHz (before series-resistor correction); LC resonance≈5.57 kHz, capacitor ESR zero≈442.10 kHz. These satisfy useful datasheet starting screens; TI's tables use specific L/C and capacitor derating. PROPOSED verify ≥45° phase margin /≥10 dB gain margin over line, load, tolerance and temperature; these are proposed acceptance criteria, not owner requirements or current results. Fuse/local load capacitance adds poles/zeros; retune CFF only with evidence. Loop stability is OPEN.

SELECTED pin handling without TPS26630:

- U201 VIN1/VIN2 to VIN_PROTECTED; compact paired VIN/PGND bypass loops. AGND joins PGND quietly per TI; detector/SCR return current must not share the FB sense path.
- BIAS remains GND. Feeding it from a raw output capable of approaching 24–29 V after HS short violates its 16 V absolute rating. This sacrifices some efficiency.
- VCC only uses C206 to AGND, no TL431/SCR load. R204=0 Ω **0603WAF100JT5E** joins RBOOT to CBOOT; C205 joins CBOOT to native SW. Removed force link must never separate bootstrap return from SW.
- R206=100 kΩ **0603WAF1003T5E** from VIN_PROTECTED and R207=24.6 kΩ **RT0603BRD0724K6L** to GND; rename midpoint BUCK_EN. CALCULATED EN=3.554/5.133 V at18/26 V and7.108 V at36 V, below42 V absolute. Nominal enable/release input≈6.397/4.606 V using1.263 V and28% hysteresis; this is **not an18 V UVLO**. Tolerance/IEN/startup/brownout remain OPEN.
- PGOOD is unused and explicitly NC at U201.5; remove off-sheet BUCK_PGOOD and its removed-sheet pullup. No permission interlock may continue to depend on it.

PROPOSED layout review later: follow TI dual hot loops and return paths, short SW/inductor connection, quiet FB sensing before F301, continuous power return and exposed-pad thermal vias. No layout/schematic work is performed in Phase C.

## 4. Output OV crowbar — static window conditional; dynamic screen FAIL

SELECTED connections: VOUT_5V1 → F301 **0451007.MRL** → LOAD_5V1, with C301/C302 and SCR301 **TYN612RG** across LOAD_5V1/GND. U301 **TL431BIDBZR** senses LOAD_5V1 through R301/R302/R303=1 kΩ+100 Ω+30 Ω and R304=1 kΩ to GND. R301/R304 **RT0603BRD071KL**, R302 **TNPW0603100RBEEA**, R303 **0603WAF1300T5E**. Q301 **BC807-40,215** PNP emitter at LOAD_5V1; its base through R305=500 Ω **0603WAF1501T5E** to TL431 cathode, R306=10 kΩ **0805W8F1002T5E** emitter-to-base. Collector through R307=100 Ω **0603WAF1000T5E** to SCR gate; R308=1 kΩ **0603WAF1001T5E** gate-to-cathode. TL431 anode and SCR cathode return to local power GND, with a separate quiet sense connection. This detector is independent of buck FB/VCC/PGOOD.

CALCULATED ideal trip **5.31435 V**; typical REF-current addition about2.26 mV. Using the same conservative TL431 temperature expansion, ASSUMED 8 mV cathode-shift reserve, ±0.1%/25 ppm precision parts and ±1%/100 ppm 30 Ω segment over65°C gives **5.18387–5.43587 V**. These are conditional screens at the reference's characterized conditions; actual several-mA base current and analog transition remain OPEN.

CALCULATED static fault headroom at high trip is **64.13 mV** to5.5 V. Against §3 normal high: with ASSUMED25 mV load-release overshoot, nuisance margin is only **12.74 mV**; at100 mV overshoot it is **−62.26 mV (FAIL)**. Before allowing load-release overshoot, only **37.74 mV** remains above ratio/reference/ripple/typical-bias high. Actual PFM peak, maximum FB current, ground bounce and loop transient must fit within that amount. No maximum-normal-output bound has been demonstrated, so **a guaranteed separation between normal output and trip is OPEN**. No delay filter may be added without recalculating fault peak.

KNOWN SCR grade: **TYN612RG**, not the sensitive-gate TRG. At25°C maximum IGT=15 mA, VGT=1.3 V, IL=60 mA, IH=30 mA. Manufacturer temperature curves are typical, without a guaranteed full −40…85°C IGT/VGT table or detector-to-clamp delay maximum. **Full-temperature maxima are OPEN**, not30 mA/1.3 V by fiat. [ST DocID7475 Rev11](https://www.st.com/resource/en/datasheet/tyn612.pdf).

CALCULATED gate-current screening at minimum trip, ASSUMED0.2 V PNP saturation, known25°C VGT1.3 V and1% gate-resistor corners:

```text
IG ≈ (5.18387−0.2−1.3)/101 −1.3/990 =35.16 mA
IB ≈ (5.18387−0.9−2.5)/505 −0.9/9900 =3.44 mA
```

CALCULATED forced gain about11 can supply this in the nominal screen. But ASSUMED0.7 V saturation and1.5 V cold VGT reduce IG to **28.03 mA**, below an ASSUMED30 mA cold trigger screen. Nexperia saturation limits at their stated current/base-drive conditions do not automatically guarantee0.2 V at this operating point. PNP/TL431 conduction buildup and gate rise must be measured; no direct TL431 gate-source current is assumed. Once the SCR pulls the rail down, gate drive collapses, so anode current must exceed the actual latching current before the gate pulse vanishes. Hiccup retrigger is a separate risk. [Nexperia BC807](https://assets.nexperia.com/documents/data-sheet/BC807_SER.pdf).

CALCULATED fault model in the script uses the exact lossless single-node LC solution, retaining current accumulated **before** the trip:

```text
w = 1/sqrt(L C); Z=sqrt(L/C)
V(t)=Vin+(V0−Vin)cos(wt)+I0 Z sin(wt)
I(t)=−(V0−Vin)/Z sin(wt)+I0 cos(wt)
find ttrip at V(ttrip)=Vtrip_high; evaluate V(ttrip+total_delay)
```

ASSUMED event: HS switch short at simultaneous5 A load release. Initial V0=**5.14613 V** (ratio/reference high, half ripple and typical FB-current effect), I0=**6.32156 A** (maximum stressed normal peak), L=4.352 µH and C=110 µF. The conservative use of peak current with high voltage is a screening combination, not an exact switching phase. Source held at24 V for the early fault; upstream current limiting does not remove stored input energy. Total delay includes TL431, PNP, SCR establishment and current commutation, not merely a catalog turn-on number.

| CALCULATED at24 V | Current at detection | Total delay, ASSUMED | Capacitor peak | Screen |
| --- | ---: | ---: | ---: | --- |
| Trip reached at2.648 µs | 17.720 A | 0.2 µs | 5.46886 V | PASS model only |
| same | same | 0.5 µs | **5.52126 V** | **FAIL** |
| same | same | 2 µs | **5.83510 V** | **FAIL** |
| same | same | 5 µs | **6.71695 V** | **FAIL** |

CALCULATED maximum total post-threshold delay before5.5 V in that model is only **0.38067 µs**, with zero allowance for probe uncertainty, ESR/ESL, saturation or harness ringing. No cited part combination guarantees this. At detection the inductor current is already close to its18 A catalog Isat; it rises further during delay. Script sensitivity additionally covers24/26 V, L=4.352/2 µH, and C=40/110/150 µF. The40 µF case is a reduced-capacitance sensitivity, not a claim the raw bank disappears; the150 µF case assumes ideal coupling of both banks. Actual two-node fuse/harness impedance remains OPEN. **The reported capacitor peak is not a guaranteed Pi-pin peak. The requirement at the Pi connector is therefore unproven and the0.5 µs screen fails even before parasitics.**

KNOWN surge ratings: TYN612RG TO-220 ITSM=140 A/10 ms or145 A/8.3 ms and I²t=98 A²s at initial25°C. dI/dt rating50 A/µs assumes IG=2×IGT and gate rise≤100 ns. These are waveform-specific/nonrepetitive ratings, not a constant140 A current ceiling for arbitrary pulses. CALCULATED main-inductor initial rise is only about `(24−5.146)/4.352≈4.33 A/µs`, but local output capacitors discharge directly into SCR without L201. An ASSUMED10 nH local loop gives `(5.5−1.3)/10nH≈420 A/µs`, exceeding50 A/µs. Local40 µF stores0.605 mJ and total150 µF stores2.269 mJ at5.5 V; small energy does not establish acceptable peak/dI/dt. Extract loop R/L, measure SCR current and qualify the gate waveform.

KNOWN F301 is7 A very-fast fuse, nominal cold9 mΩ and melting I²t10.32 A²s. CALCULATED `1.65 (F101) <10.32 (F301) <98 (SCR)` and ratio10.32/98≈0.1053. At ASSUMED50 A the nominal adiabatic melt examples are0.660 ms /4.128 ms. **OPEN coordination:** total clearing including arc, hot SCR surge capacity, capacitor discharge bypassing one or both fuses, repeated pulses and exact source impedance are unknown. Nominal melting I²t is not maximum total-clearing I²t and cannot be extrapolated to slow overloads. F301's documented400 A at32 VDC interrupt entry is suitable only if the input cutoff prevents a64 V HS-short exposure; verify prospective fault current and maximum protected-source voltage. The separate50 A at125 VAC/VDC entry does not confer400 A interruption at64 V.

OPEN UENPO source limit: exact-name searches produced no authoritative S4-T482410 manual giving current limit, foldback or hiccup. The model name is not evidence of10 A output or a specified overload limit. **No finite output-fuse clearing time can be assigned.** Manufacturer fuse table guarantees ≤5 s at200% rating, hence **14 A sustained at F301** under those conditions. At2.2/3/5/6 A it is below nameplate and not guaranteed to open; at7 A100% opening is at least4 hours. At10 A it is143%, with no guaranteed maximum from the200% table. F101 sees the same source current after a physical HS short, not a buck-converted current, and may clear first; below3 A or under hiccup it may not clear either. The earlier generic24 V/2 A example is not a specification for this UENPO.

CALCULATED/OPEN functioning-buck crowbar: a false OV trigger or externally induced OV with an intact regulator can put U201 in its current-limit/hiccup state; the7 A fuse may never clear. Buck cycle limits are **not** indefinite thermal guarantees. Analyze full current/voltage waveforms, average duty and every retry, in addition to SCR continuous loss in §5. For a physical HS short, U201's electronic current limit cannot be credited at all. Source-current-limited faults and failed-HS faults require distinct tests.

**FAIL — raw-capacitor containment:** if F301 opens before F101 during a HS short, SCR and its detector are disconnected from VOUT_5V1. The six16 V raw MLCCs then charge toward24–29 V; input OV cutoff does not respond to a24 V input. Even if Pi isolation succeeds, board fault survival is not established. PROPOSED remedies for review are adequate raw-cap voltage rating, a raw-side clamp, or an independent coordinated input shutdown; none is silently inserted in the selected Option1 or its cost. The selected baseline remains blocked until this is resolved.

## 5. Preliminary thermal — OPEN; unsinked sustained SCR fault FAIL

ASSUMED thermal study point: ambient50°C, desired semiconductor junction≤110°C. These are screening values; enclosure, cooling, required ambient and peak-load duration are OPEN. X5R body temperature must separately remain≤85°C. All losses below are model estimates, not measured efficiency.

CALCULATED buck conduction uses `Irms²×[D×82mΩ+(1−D)×45mΩ]`, the TI high-side/low-side maximum resistance values. Switching overlap uses `0.5 Vin I (tr+tf) f`, with ASSUMED total edge time10–30 ns; another ASSUMED0.1–0.3 W covers LDO/gate/dead-time/Coss losses. These placeholders are not guaranteed upper bounds. BIAS=GND increases internal supply loss. Inductor copper loss uses11.5 mΩ at25°C, copper coefficient0.00393/°C and ASSUMED100°C winding; add ASSUMED0.05–0.30 W core/AC loss.

| CALCULATED at5 A | 18 V | 24 V | 26 V |
| --- | ---: | ---: | ---: |
| Buck conduction | 1.413 W | 1.351 W | 1.337 W |
| Buck total loss screen | 1.693–2.253 W | 1.691–2.371 W | 1.697–2.417 W |
| Inductor copper+AC/core screen | 0.429–0.679 W | 0.431–0.681 W | 0.431–0.681 W |
| Input controller+gate network input power | 0.236 W | 0.564 W | 0.713 W |
| Input current at combined high-loss corner | 1.682 A | 1.255 A | 1.161 A |
| Two input FET losses, ASSUMED2×hot117 mΩ each | 1.324 W | 0.737 W | 0.631 W |
| F101 cold-resistance loss | 0.064 W | 0.036 W | 0.031 W |
| F301 cold loss /drop | 0.225 W /45 mV | same | same |
| Combined efficiency high-loss sensitivity | 84.2% | 84.7% | 84.4% |

CALCULATED input-current solve includes input-FET and fuse I²R losses rather than reusing the earlier1.574 A buck-only estimate: `Vin I=Pscreen+I²(2×0.117×2+0.0227)`. It uses25.5 W load-class power plus fuse/conversion losses conservatively, and approximates duty from the external input; actual post-FET duty and temperature iteration are OPEN. Do not add an assumed90–94% whole-board efficiency on top of these component estimates or claim that range is measured. Gate drive below−10 V invalidates use of the117 mΩ max; the full input network must be characterized at18 V.

CALCULATED buck effective thermal resistance required at the50/110°C study point is approximately **26.6 /25.3 /24.8°C/W** across18/24/26 V at the high loss screen. TI's EVM example is a four-layer board; a small two-layer Lite board does not inherit that result. Measure case/board temperatures, estimate junction with an appropriate thermal model and verify exposed-pad/ground copper/vias. Two input FETs may each dissipate about0.662 W at18 V; sink/tab spacing and insulation must be checked. No thermal accessory is silently assumed unnecessary.

CALCULATED corrected SCR hot conduction model is `P=0.85 I+0.030 I²`. **Correction to Phase B prose:**5 A gives5.00 W, not5.85 W;6 A gives6.18 W, not7.05 W. Phase B JSON already used the correct formula. Historical files are unchanged.

| ASSUMED sustained SCR current | CALCULATED loss | Free-air rise at60°C/W | Required total θ at50/110°C | Sink θ after1.3°C/W junction-case and ASSUMED1°C/W interface |
| ---: | ---: | ---: | ---: | ---: |
| 2.2 A | 2.015 W | 120.9°C | ≤29.77°C/W | ≤27.47°C/W |
| 3 A | 2.820 W | 169.2°C | ≤21.28°C/W | ≤18.98°C/W |
| 5 A | 5.000 W | 300.0°C | ≤12.00°C/W | ≤9.70°C/W |
| 6 A | 6.180 W | 370.8°C | ≤9.71°C/W | ≤7.41°C/W |
| 10 A, sensitivity only | 11.500 W | 690°C | ≤5.22°C/W | ≤2.92°C/W |
| 14 A, clearing pulse only | 17.780 W | not a valid sustained operating point | transient analysis needed | no continuous-use approval |

**FAIL** leaving the SCR without a thermal path for indefinite2.2–6 A current-limited faults. Above-current extrapolations do not override ST current/case-temperature ratings. A five-second14 A clearing case needs the transient thermal curve and actual fault waveform, not the10 ms ITSM rating. The previous40,000 VND sink allowance is retained as ASSUMED procurement accounting, not proof of the required≤7.41°C/W for6 A. Exact sink MPN/insulator, enclosure airflow and source limit are OPEN.

OPEN functioning-buck short thermal: current-limit/hiccup duty may reduce average dissipation but produces repeated SCR trigger and U201 stress. Integrate measured buck switch conduction/switching losses and SCR power over the retry cycle; verify stable shutdown and every Pi-pin peak. For a failed-HS transistor, heat is in its short resistance, L201, both input FETs, fuses, SCR and source. At6 A with ASSUMED0.468 Ω combined hot input-FET resistance, FET loss alone is16.85 W until clearing; a sink sized for normal operation does not cover it. At3 A where F101 may not clear, it is4.21 W. Fault thermal qualification must include those FETs and inductor, not only the SCR.

KNOWN/CALCULATED fuse use:5 A is71.4% of F301's7 A nameplate, near the manufacturer's75% continuous-use convention before extra ambient derating. Hot fuse resistance/drop and pad heating remain OPEN. Input fuse normal current≈56% of3 A in the high-loss18 V screen. Derate connectors, wire and copper for enclosure temperature; measure both outgoing and return drops. No PCB copper/current capacity is validated during calculations-only Phase C.

## 6. Final Phase C analysis BOM and costs — budget FAIL / procurement OPEN

SELECTED exact analysis BOM: [PHASE_C_BOM.csv](PHASE_C_BOM.csv), generated by the script, with ref, MPN, quantity, unit, unit/extended VND, source/date, local realism, safety-critical flag and substitution restriction. [Purchase model](PHASE_C_PURCHASE_MODEL.csv) aggregates identical MPNs before spares/MOQ rounding. This is the final **Phase C candidate BOM**, not an order-ready or electrically approved BOM. Failed parts/functions stay visible rather than being silently substituted to make the totals look complete.

DECISION: D101 candidate identity is **Bourns SMCJ64CA**, whose exact manufacturer table and ordering convention were readable. The earlier Littelfuse search is comparison provenance only. KNOWN Bourns clamp is103 V at14.6 A10/1000 µs, and133.9 V at73 A8/20 µs: neither guarantees100 V FET protection. ASSUMED price **USD0.50 /13,250 VND** is a transparent allowance, not a quote borrowed from another manufacturer. Exact price, stock and a compliant surge solution remain OPEN.

SELECTED for the local-sourcing worker: **all electronic and current-carrying lines are safety-critical=yes, substitute_allowed=no** for this analysis revision. Their identities affect trip accuracy, response, fault rating, impedance or thermal behavior. “No substitution” means the sourced part must be the exact listed manufacturer/MPN; the engineering owner can approve a revised BOM after recalculation. A generic “IRF9540”, “TL431”, “7A fuse”, “6.8µH” or “47µF” is insufficient. Thermal kit MPNs remain OPEN and cannot be purchased from an invented identity. Etched test pads/copper are not separate purchased components.

KNOWN local-evidence convention: `vietnam_local_realistic=no` means **no verified exact Vietnam-local offer exists in this evidence**, not proof that the part is unobtainable in Vietnam. Every row carries that explanation. Imports from LCSC/DigiKey are not relabeled as local. This worker does not duplicate the separate local-sourcing plan. Source prices are original2026-10-03–05 snapshots; zero stock for TVS3300DRVR/MMBTA42-TP and EOL input MLCC risk remain explicit.

ASSUMED accounting retains **26,500 VND/USD**, one assembled prototype, spares `n+max(1,ceil(25%×n))` per exact core MPN, then saved MOQ as provisional cut-tape order increment. Actual applicable purchase tiers are used, not the installed ten-piece price multiplied by an arbitrary factor. New TVS quantity/price are assumed pending quote. Connector purchase remains five headers, three housings and100 contacts because that is the saved minimum-lot evidence. A sourcing worker may reduce those costs only with an exact verified offer.

| CALCULATED total | Scope | VND |
| --- | --- | ---: |
| A dated-price subtotal | Installed core parts with saved offer; excludes new TVS allowance | 274,182.25 |
| A planning total | Above +13,250 assumed TVS | **287,432.25** |
| B planning total | A +23,685.70 installed connector/mate/contact cost +10,600 allocated bare PCB | **321,717.95** |
| Core minimum-lot purchase | One build +spares/MOQ overbuy, includes26,500 assumed for two TVSs | 820,744.75 |
| C planning total | Core purchase +263,502.75 connector lots +408,000 overhead | **1,492,247.50** |
| C above strict1,000,000 ceiling | Before unresolved thermal/safety-redesign costs | **492,247.50** |

ASSUMED C overhead: five bare boards53,000; wire/Pi fanout35,000; shipping/tax180,000; assembly/consumables50,000; rework50,000; SCR sink/insulation40,000 VND. Board allocation remains Phase B's80×60 mm/two-layer/1 oz/1.6 mm planning estimate; enclosure, routing and thermal analysis have not justified it. Lab equipment, upstream converter and Pi are assumed already owned/borrowed. Input-FET fault thermal hardware is explicitly **OPEN/unpriced**, not zero. Safety redesign costs are also excluded and OPEN; therefore no complete qualified cost can yet be stated. The current estimate already fails the budget.

CALCULATED changes from Phase B Option1: add the upstream TVS allowance, retune input divider, split control ballast and gate pullup for power sharing. No option2/3 electronics are included. Whole-build cost is not A or B; a low installed BOM does not demonstrate C below the ceiling. No purchases have been made.

## 7. Removed-function ledger and bench qualification — plan delivered / tests OPEN

SELECTED removals implement the owner's Option1/no-telemetry decision. “Acceptable” is conditional engineering disposition, not a waived protection requirement. No removal has yet been made in CAD.

| REMOVED FUNCTION | WHY PRESENT | WHY ACCEPTABLE | REPLACEMENT TEST |
| --- | --- | --- | --- |
| TPS26630 input current limit/overload timer | Bound fault current and protect wiring | Conditional only; input fuse is retained but not equivalent | Source-current/clearing envelope; FET/resistor/SCR indefinite fault heating and short tests |
| Input controlled slew/inrush | Limit capacitor hot-plug current | Not yet established acceptable | Worst source impedance, long/short leads, hot/cold plug, input FET SOA and TVS energy |
| eFuse UVLO/PGOOD gating | Qualify power before buck startup | New independent EN divider is simpler; no18 V UVLO claim | Slow rise/fall, brownout, reconnect, no-load/full-load startup |
| Old eFuse OV/reverse block | Input fault isolation | Replaced with two100 V P-FETs and TL431 detector; still OPEN dynamically | ±64 V, continuous54.6/64 V, cold-start into fault, reversals with stored charge |
| INPUT_SHDN feedback from output fault | Halt source after downstream fault | **Not presently electrically established** for source-limited crowbar/raw-cap fault | Prove fuse clearing or continuous containment; resolve raw-cap hazard |
| Opposed series output MOSFETs/LTC7001 | Fast isolation and reverse-current blocking | SCR/fuse is selected lower-cost alternative; no equivalent reverse blocking claim | Backfeed/hot-plug, current commutation, output-fuse-first and stuck-fuse faults |
| Precision reference/fast comparator chain | Narrow and fast OV protection | **Not presently established** by TL431 timing | Full-temperature threshold, normal ripple/PFM/load-release margin and Pi-pin HS-short peak |
| MOSFET ballast/disposal branches | Controlled dissipation on raw and protected rails | SCR supplies one clamp path, raw path coverage unresolved | SCR gate current/rise, local-cap pulse/dI/dt, raw capacitor exposure after F301 opens |
| Large470 µF raw/protected reservoirs | Hold-up, load transients and fault-time margin | Conditional on new effective-C and transient tests | Biased C, ripple/loop margin, load steps and fault impulse; no old100 A L assumption |
| Auxiliary buck-boost/HV LDO/hold rails | Keep protection powered through collapse | TL431 paths derive power from their observed rails; no hold-up claim | Cold startup, power collapse, reference validity and SCR latch establishment |
| ARM/RESET/manual latch/debounce | Explicit enable and fault memory | Owner selected simpler power chain; SCR only holds above IH | Hiccup/retry/reversal and restart into persistent fault; no manual-lockout claim |
| Guarded analog switches/supervisors/PG logic | Prevent undefined sequencing/backpower | Conditional removal | Rail-sequence, partially powered detector and open-ground tests |
| SW_HIGH/VIN_GOOD_FAST/manual source fixture | Research observation/injection access | External controlled injector replaces fixture; old manual source contact was not automatic protection | Retain SW/input/gate/raw/load/GND access; separate fault injection from measurement |
| INA228 current/voltage/power/energy and ALERT | Telemetry/diagnostics | Explicitly removed by owner | External calibrated DMM/load/current probe; telemetry N/A |
| R4012 mΩ Kelvin shunt and RC sensing | Accurate current measurement in series path | Explicitly removed; copper removes nominal10 mV/50 mW at5 A | Low-resistance continuous output connection and loaded voltage-drop test; no calibrated onboard sensing |
| TPS70933 local telemetry rail | Power monitor/level translator | No telemetry electronics remain | Rail/load inventory; ensure protection does not depend on removed supply |
| TCA9517/I2C pullups/J503 | Host bus endpoint/translation | No I2C function remains | No remaining SDA/SCL/3V3_HOST endpoints or unexpected host backfeed |
| Custom removable force links | Isolate research blocks | Continuous copper reduces assembly and resistance | Continuity, injection fixture isolation and separate force/sense test access |
| Large research inductor/high-voltage output capacitors | Support stiff fault and raw voltage exposure | Smaller L acceptable only with ratings; **16 V raw fault coverage FAIL** | Saturated-L and fault containment; revise rating/protection before release |
| Legacy connector/board/thermal qualification | Validity for old physical design | New board requires its own evidence | Exact mates/crimps/harness, hot resistance, copper/vias, thermal and spacing review |

PROPOSED future qualification sequence, strictly after engineering review and permitted test-fixture fabrication. Current Phase C does not authorize manufacture or physical testing of an unresolved high-energy design. Use a dummy load throughout all preceding gates; no Pi for initial power or OV experiments.

1. **Visual inspection:** match exact manufacturer/MPN, package pins/tab potential, fuse ratings, TVS/zener/SCR polarity, input/output marking, heatsink isolation, creepage/clearance and soldering against reviewed capture. Inspect both board faces and harness. Record photos and revision.
2. **Unpowered continuity/short checks:** ground path, fuse paths, no SW-to-ground short, Q101/Q102 diode directions, detector divider values, no raw bypass to Pi, and continuous replacement for R401. Discharge and verify capacitors before reconfiguration.
3. **Current-limited bench source:** start at low stored energy and documented current limit; scope VIN_PROTECTED/CTRL12/gates. Use rated differential probes and a separately fused energy-bounded injector. Choose limit from measured startup requirements rather than assuming a3 A fuse sets it.
4. **No-load startup:** 18/24/26 V, slow/fast ramps, hot plug, repeated startup and brownout. First characterize low-energy input cutoff and cold-start-into-OV on an isolated protection coupon; halt on unexpected enhancement, overstress or oscillation.
5. **Verify rails:** raw setpoint and Pi-connector voltage, U201 VCC/EN/BOOT differential, detector REF/cathode/CTRL12. Measure input trip/release versus temperature and ramp rate. Confirm no dependency on deleted auxiliary/telemetry supplies.
6. **Low dummy load:** establish polarity, regulation, stable SCR-off state and measured path drop. Instrument actual current and rail voltage independently.
7. **Increasing load:** step through low loads to5 A at18/24/26 V; log source current, raw/load voltage and connector/return drops. Peak current/duration above5 A stays OPEN until requirements exist. Never infer allowable overload from buck6 A capability.
8. **Thermal:** soak to equilibrium at required ambient/enclosure once specified. Measure U201/L201/FETs/fuses/connectors/resistors/SCR sink and capacitor body temperatures. Fail on temperature ratings or loss of voltage window; verify hot resistor and fuse derating.
9. **Ripple:** measure raw and Pi connector with short probe loops at switching and light-load/PFM modes, state bandwidth and probe uncertainty; distinguish ripple from setup-induced ringing. Confirm actual effective-capacitance and sharing assumptions.
10. **Transient/loop:** startup/inrush, load application/release, line steps and Bode measurements across source/load/temperature; compare to ≥4.75 V and no nuisance trigger. Proposed loop targets45°/10 dB require review. Do not add blanking to hide overshoot.
11. **Protection/fault:** with dummy load and reviewed energy-limited fixture, characterize detector-to-gate-to-clamp delay; then increment source energy up to the documented interface envelope. Inject LM61460 HS short at24 V (also26 V and input-cutoff boundary), with load present and simultaneous release; record Pi-pin peak, raw rail, SCR gate/anode current, fuse I²t and both FET stresses. Require **Pi peak plus measurement uncertainty <5.5 V**, VIN_PROTECTED≤36 V with42 V absolute never crossed, and no raw-cap overstress. Exercise continuous54.6/64 V input, direct cold connection, reverse/reversal with stored charge, cable ringing, source current-limit/foldback/hiccup, output-fuse-first, opened/shorted detector/TVS/FET/SCR/fuse paths and repeated retries. Duration of the continuous-fault test must represent thermal steady state/required service time; no arbitrary short test is labeled continuous survival. Stop if source envelope or fixture ratings are unknown.
12. **Telemetry:** explicitly **N/A, removed**. Validate external measurements/calibration and archive traces, thermal data and uncertainty instead.
13. **SBC integration:** only after every preceding gate passes and reviewed evidence resolves all FAIL/OPEN protection items. Use the qualified harness/interface and real Pi load last; no USB3/D435i data routed through this board.

OPEN evidence for every physical test above: NOT RUN. Source characterization is a prerequisite to high-energy fault tests, not an invitation to connect an unbounded battery. Fault containment, not continued operation of a deliberately failed buck, is the acceptance objective.

## 8. Exact Phase D change list — documented; implementation BLOCKED

PROPOSED plan only. Resolve the TVS/FET clamp mismatch, raw-capacitor containment and protection timing before treating this as a capture-ready design. The refdes below freeze the **analyzed baseline**, including its explicitly failed items; a remedy must receive its own calculation/BOM revision. No later gate is skipped because a netlist can be generated.

| File / sheet | Exact future action |
| --- | --- |
| `hardware/kicad/V1A.kicad_sch` root | Remove Sheet04 hierarchy instance and telemetry pins/wires. Retain01/02/03/05 as four child sheets. Remove BUCK_INPUT_PGOOD, BUCK_PGOOD, INPUT_SHDN and L201_IN cross-sheet connections. Connect01 VIN_PROTECTED→02 input and05 test point;02 VOUT_5V1→03 input;03 LOAD_5V1→05 output. GND common. VIN_RAW comes from05 J501. VIN_FUSED becomes private to01. |
| `01_INPUT_PROTECTION.kicad_sch` | Redraw the entire old TPS26630 block from §2, removing its old controller/FET/TVS/Schottky/force-link contents rather than leaving obsolete nets. Reuse refdes only with new identities. Ports VIN_RAW(input), VIN_PROTECTED(output), GND(passive). No INPUT_SHDN or BUCK_INPUT_PGOOD. Exact refs in table below. |
| `02_BUCK_5V.kicad_sch` | Retain U201 and its pin topology; replace L201, specified capacitors/resistors with Phase C BOM identities/quantities. Remove JP201/JP202 and use direct copper SW→L201→VOUT_5V1. C205 return remains native SW. Add C215/C216 input MLCCs. Replace BUCK_INPUT_PGOOD midpoint with private BUCK_EN, no eFuse gating. PGOOD U201.5 explicit NC. Remove BUCK_PGOOD/L201_IN hierarchy ports. Ports VIN_PROTECTED(input), VOUT_5V1(output), GND(passive). |
| `03_OUTPUT_PROTECTION.kicad_sch` | Redraw completely: delete all old280 physical refs, including U3xx/U6xx, Q/D3xx, auxiliary chain, ballast banks, latches, headers, custom links and legacy TP assignments; then instantiate exactly F301/SCR301/U301/Q301/R301–R308/C301/C302 and new etched sense pads. Ports VOUT_5V1(input), LOAD_5V1(passive), GND(passive). Do not retain VIN_FUSED/VIN_PROTECTED/BUCK_PGOOD/INPUT_SHDN/L201_IN ports. |
| `04_POWER_MONITOR.kicad_sch` | Remove from active hierarchy; preserve original through Git history/historical evidence. Remove its23 physical refs including R401/U401/U402/U403 and all telemetry nets. **Merge VOUT_PROTECTED into canonical LOAD_5V1 through continuous rated copper**; there is no new0 Ω resistor, shunt, or disconnected power path. |
| `05_IO_TEST.kicad_sch` | Set J501/J502 to exact JST header/mates in BOM. J501.1 VIN_RAW, J502.1 LOAD_5V1, both pin2 GND. Delete J503 and3V3_HOST/SDA_HOST/SCL_HOST hierarchy. Delete JP501/custom force-fixture branch; retain sensible etched test pads and direct external dummy-load access at J502. No research fixture header inherited accidentally. |

SELECTED/PROPOSED input reference plan (CSV is the purchase-identity authority):

| Refdes | Function / connection |
| --- | --- |
| F101; D101 | Input3 A fuse; Bourns bidirectional64 V TVS VIN_FUSED↔GND (failed clamp screen retained for review) |
| Q101/Q102 | Reverse /OV common-source100 V P-FET pair; source S_COMMON, drains VIN_FUSED/VIN_PROTECTED |
| Q103; U101 | HV NPN gate sink; TL431 input detector |
| D102/D103 | Q101/Q102 source-gate12 V clamps, cathodes at S_COMMON |
| D104/D105/D106 | CTRL12-to-GND12 V zener;3.3 V level shift with cathode at IN_OV_K; protected33 V TVS at VIN_PROTECTED |
| C101/C102 |100 µF50 V damping at VIN_PROTECTED;1 µF16 V at CTRL12 |
| R101/R102 | Series10 kΩ+10 kΩ Q101 gate to GND |
| R110–R125 | Two parallel8×1 kΩ strings, S_COMMON to CTRL12 |
| R130–R135 | Six100 Ω series Q102 gate to Q103 collector |
| R140–R143 | Two parallel2×1 kΩ strings, Q102 source-to-gate |
| R144/R145/R146 |1 kΩ CTRL12→IN_OV_K;10 kΩ level shift→NPN base;100 kΩ base→GND |
| R150/R151/R152/R153 |100 kΩ+1 kΩ+1 kΩ S_COMMON→IN_OV_REF;10 kΩ REF→GND |
| R147–R149 | Unused/reserved; no phantom BOM rows |

PROPOSED named local nets: Sheet01 `VIN_FUSED`, `S_COMMON`, `REV_GATE`, `OV_GATE`, `CTRL12`, `IN_OV_REF`, `IN_OV_K`, `IN_SHIFT`, `IN_NPN_BASE`, `IN_NPN_COLLECTOR`; Sheet02 `BUCK_SW`, `BUCK_BOOT`, `BUCK_RBOOT`, `BUCK_VCC`, `BUCK_EN`, `BUCK_FB`, `BUCK_FF`; Sheet03 `OUT_OV_REF`, `OUT_OV_K`, `CB_BASE`, `CB_COLLECTOR`, `SCR_GATE`. High-current global/hierarchy nets are `VIN_RAW`, `VIN_PROTECTED`, `VOUT_5V1`, `LOAD_5V1`, `GND`. Intermediate resistor-chain nodes may use native local generated names. Do not retain both LOAD_5V1 and VOUT_PROTECTED as different force nets without a defined connection.

PROPOSED buck ref mapping: keep R201 RT, R202 FB upper, R203 FB lower, R204 BOOT link, R205 FF series, R206 EN upper and R207 EN lower. Keep C201/C202 input10 µF and add C215/C216; C203/C204 paired100 nF; C205 BOOT100 nF; C206 VCC1 µF; C207 FF22 pF; C209–C214 raw47 µF. C208 unused. U201 pin contract:1 BIAS→GND,2 VCC,3 AGND,4 FB,5 PGOOD NC,6 RT,7 EN,8/12 VIN,9/11 PGND,10 SW,13 RBOOT,14 CBOOT. Follow the actual RJR package pad drawing; do not invent an exposed-pad number.

KNOWN pin-sensitive change: **TL431BIDBZR DBZ has cathode1, REF2, anode3**; TL432's DBZ mapping differs. IRF9540NPBF has gate1/drain2/source3 and drain tab. PROPOSED Phase D must independently verify SCR TYN612RG TO-220 pin/tab mapping, BC807-40 and MCC MMBTA42 SOT-23 numbering, TVS3300 DRV pad allocation, zener cathode and connector footprint mating against exact drawings before ERC. Do not reuse old Q101/U101 footprints merely because refdes were retained.

PROPOSED etched test-pad plan: Sheet01 TP101 VIN_FUSED, TP102 S_COMMON, TP103 VIN_PROTECTED, TP104 REV_GATE, TP105 OV_GATE, TP106 CTRL12, TP107 IN_OV_REF, TP108 IN_OV_K, TP109 local GND. Sheet02 TP201 BUCK_SW, TP202 BUCK_BOOT (differential-to-SW measurement), TP203 VOUT_5V1, TP204 BUCK_FB, TP205 BUCK_EN, TP206 BUCK_VCC, TP207 quiet GND. Sheet03 TP301 VOUT_5V1, TP302 LOAD_5V1, TP303 OUT_OV_REF, TP304 OUT_OV_K, TP305 SCR_GATE, TP306 local SCR-return GND. Sheet05 TP501 VIN_RAW, TP502 VIN_PROTECTED, TP503 LOAD_5V1, TP504 GND; remove old TP505 LOAD_FIXTURE. These are sense pads, not unqualified force connectors. Keep high-current fault injection external and reviewed.

PROPOSED Phase D evidence: reconcile every placed ref to Phase C's then-approved BOM; export native netlist; check full force continuity and no removed control dependency; run ERC after every sheet change and final hierarchy; visually inspect all schematic pages and pin/footprint mappings. Do not modify legacy snapshots or weaken old tests to manufacture a Lite PASS; add a scoped Lite contract. No PCB import/layout/DRC until R2 review; when PCB changes later, run DRC and visual review. Current Phase C has no CAD changes, so new ERC/DRC is N/A and old PASS reports do not validate Lite.

## Final check ledger and handback

KNOWN: test scopes are explicit; PASS here does not release hardware.

| Check | Result |
| --- | --- |
| 01 input 64V FET DC voltage only | **PASS** |
| 02 upstream TVS to 100V FET | **FAIL** |
| 03 input trip static screen | **PASS** |
| 04 input VIN never above 36V | **OPEN** |
| 05 input bias timing startup release SOA | **OPEN** |
| 06 reverse and powered reversal | **OPEN** |
| 07 buck L and catalog Isat screens | **PASS** |
| 08 capacitance ripple current loop margin | **OPEN** |
| 09 Pi normal window 5A harness | **OPEN** |
| 10 crowbar HS short 24V 0p5us screen | **FAIL** |
| 11 crowbar max IGT VGT delay over temp | **OPEN** |
| 12 fuse SCR UENPO clearing | **OPEN** |
| 13 raw 16V caps after output fuse opens | **FAIL** |
| 14 unsinked SCR indefinite fault | **FAIL** |
| 15 whole board thermal | **OPEN** |
| 16 cost C under 1000000 | **FAIL** |
| 17 exact local sourcing and full cost | **OPEN** |
| 18 removed function and bench plan documented | **PASS** |
| 19 Phase D change list documented | **PASS** |
| 20 hardware qualification | **OPEN** |

EVIDENCE: [verification record](PHASE_C_VERIFICATION.json) covers deterministic regeneration, independent numerical integration, BOM arithmetic/reference reconciliation and unchanged hardware scope. Script assertions verify the analytic LC energy identity; they do not validate a circuit.

KNOWN Git result: all eight section checkpoint attempts failed at staging with `Unable to create .../.git/worktrees/wt-lite/index.lock: Operation not permitted`. [Exact log](PHASE_C_GIT_LOG.txt). Per the brief, all Phase C work remains uncommitted; HEAD remains `6cfe313`. Nothing was pushed or bought. The final checkpoint is also recorded.

DECISION: R1 electrical release / Phase D implementation **BLOCKED**. Analysis is delivered with explicit failures; no claim of electrical safety or completed physical validation.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

LITEC-HANDBACK
