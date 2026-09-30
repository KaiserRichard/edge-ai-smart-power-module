# V1A input TVS and fuse re-selection

2026-09-30 · Analysis only · **PRELIMINARY — BLOCKED — NOT FOR FABRICATION**

**Proposed parts: D101 = Littelfuse SMCJ36CA; F101 = Schurter 3403.0285.23. Proven V1A continuous withstand = OPEN; recommended standalone converter = NONE.** These are selections for a design/qualification review, not installed or validated replacements. No KiCad file was opened, read or saved; no electrical change was made.

## OWNER EXPLANATION — one-page handout

V1A takes 9–24 V DC, protects the input and converts it to 5.1 V for a 5 A Raspberry Pi 5 load through the GPIO power pins. Its input TVS is a brief-surge absorber. Its eFuse disconnects the buck during overvoltage. The small auxiliary supplies connect before that disconnect, so they still see an input fault.

A TVS has three different voltages. **Standoff** is the voltage it can sit across without intentional avalanche. **Breakdown** is where avalanche begins at a small test current. **Clamp** is the much higher voltage reached while carrying a large surge. Our proposed 36 V part has 40.0–44.2 V breakdown and a specified 58.1 V pulse clamp at room temperature. It does not regulate the input to 36 V. [Littelfuse SMCJ datasheet](https://www.littelfuse.com/assetdocs/littelfuse_tvs_diode_smcj_datasheet?assetguid=37388813-0d6d-4329-969b-1aa8b7614ac1)

The existing 26 V standoff is too low for the converters' 31.2–33.6 V OVP figures. A sustained fault could keep that TVS conducting. Even a small avalanche current creates continuous heat, while being too small to blow the fuse. A TVS must not be used as a continuous avalanche regulator. The replacement avoids this particular conflict, but trades it for a higher surge voltage elsewhere.

That higher voltage exposes real limits. The auxiliary LDO enable inputs are specified for operation only up to 40 V, and their input capacitor is currently specified as 50 V. The LDO inputs have a 62 V absolute limit. These paths need a separate voltage bound or component/circuit changes; the buck's input disconnect does not protect them. Hot TVS clamp voltage and wiring overshoot still need a guaranteed limit. [TI TPS7A16 datasheet](https://www.ti.com/lit/ds/symlink/tps7a16.pdf)

The proposed larger TVS has more pulse-power headroom. The proposed fuse can hold 5 A in our assumed hot calculation, but its higher rating also makes it slower to clear moderate faults. Fuse melting energy is not proof that it will save the TVS or wiring. The source must shut down sustained faults independently.

Finally, nominal 24 V can exceed our frozen 24 V normal-input ceiling after tolerance, ripple and startup. Downward adjustment is still needed, but “23 V” is not sufficient without a complete peak guarantee. Of the four converters, TEP 200-7215UIR is the best next technical enquiry. None is approved yet; increasing the TVS rating does not prove the board or the Pi safe.

## Scope, labels and frozen requirements

**REQUIREMENT:** normal V1A input 9–24 V; Pi 5 A through GPIO; Pi fault peak strictly below 5.5 V. The input OVP setting is unchanged. The inherited initial-tolerance minimum is **CALCULATED 26.973873 V**; this report uses the requested conservative **26.97 V** comparison. Full-temperature threshold drift is **OPEN**. Documentary topology and identities are pinned in [TVS_INPUT_AUDIT.md](TVS_INPUT_AUDIT.md) and [TVS_INPUT_PROVENANCE.json](TVS_INPUT_PROVENANCE.json).

Table labels: **ASSUMED** includes explicitly stated application conditions and transfer of manufacturer test-condition data to this design; **CALCULATED** means arithmetic under those assumptions; **OPEN** means no applicable guaranteed limit or qualification evidence. Manufacturer source limits retain their specified conditions and are not measurements of V1A. Source identities/revisions and functions studied are in [TVS_SOURCES.md](TVS_SOURCES.md); reproducible arithmetic is in [TVS_CALCULATIONS.json](TVS_CALCULATIONS.json).

For the requested comparison, **ASSUMED complete output peaks** are 32.4 V for both RSD units, 31.2 V for TEP 200 and 33.6 V for TEP 150, inclusive of overshoot **only if guaranteed as such**. Manufacturer documents give maximum OVP **trigger** values, not complete peak guarantees. Additional excursion after the trigger is therefore **OPEN**. The tables show its remaining allowance; do not add overshoot twice if a supplier proves the supplied figure already includes it.

## 1. D101 selection and the assumed surge

**ASSUMED selection reserves:** at least 1.0 V from the supplied complete peak to TVS standoff; ordinary 67 V TPS26630 absolute maximum is the clamp comparison, not its conditional 75 V headline. Bidirectional CA parts are retained because D101 is ahead of Q101. A unidirectional replacement would forward-conduct a reverse input into F101; Q101 would not prevent that upstream current. Reverse-source current/energy coordination is **OPEN**, so a unidirectional part is not justified.

All rows below are Littelfuse manufacturer limits at 25 °C, breakdown test 1 mA, clamp at the listed 10/1000 µs peak current. **ASSUMED:** these are the room-temperature comparison conditions; hot application maxima are **OPEN**. Specified leakage at standoff is 1 µA maximum at the stated test condition. [SMBJ](https://www.littelfuse.com/assetdocs/tvs-diodes-smbj-series-datasheet?assetguid=ba555e99-a12d-4f72-a0b6-86b06c67171e), [SMCJ](https://www.littelfuse.com/assetdocs/littelfuse_tvs_diode_smcj_datasheet?assetguid=37388813-0d6d-4329-969b-1aa8b7614ac1)

| D101 candidate | Standoff V | Breakdown min–max V | Clamp max V / rated peak A | Peak power headline | CALCULATED headroom to 67 V | CALCULATED standoff headroom to 33.6 V | Decision under assumed 1 V reserve |
|---|---:|---:|---:|---:|---:|---:|---|
| SMBJ30CA | 30 | 33.3–36.8 | 48.4 / 12.4 | 600 W | 18.6 V | −3.6 V | FAIL standoff |
| SMBJ33CA | 33 | 36.7–40.6 | 53.3 / 11.3 | 600 W | 13.7 V | −0.6 V | FAIL TEP 150; RSD has only 0.6 V |
| SMBJ36CA | 36 | 40.0–44.2 | 58.1 / 10.4 | 600 W | 8.9 V | 2.4 V | Voltage screen fits; little hot pulse-power reserve |
| SMCJ30CA | 30 | 33.3–36.8 | 48.4 / 31.0 | 1500 W | 18.6 V | −3.6 V | FAIL standoff |
| SMCJ33CA | 33 | 36.7–40.6 | 53.3 / 28.2 | 1500 W | 13.7 V | −0.6 V | FAIL TEP 150; RSD reserve insufficient |
| **SMCJ36CA** | **36** | **40.0–44.2** | **58.1 / 25.9** | **1500 W** | **8.9 V** | **2.4 V** | **Recommended for qualification** |

Vishay provides the same voltage rows; its rated SMBJ36CA current is 10.3 A, and SMCJ33CA/36CA currents are 28.1/25.8 A. These are distinct manufacturer specifications, not Littelfuse ratings. [Vishay SMBJ](https://www.vishay.com/docs/88392/smbj.pdf), [Vishay SMCJ](https://www.vishay.com/docs/88394/smcj.pdf)

**CALCULATED:** 58.1 V leaves 8.9 V, or 13.3%, below the eFuse's ordinary absolute ceiling. **ASSUMED application acceptance ceiling: 60.0 V at every exposed raw/input node**, including temperature and parasitic overshoot; this leaves 7.0 V below 67 V but zero operating reserve to the eFuse's 60 V operating ceiling. The actual maximum is **OPEN**. SMCJ uses **DO-214AB / SMC**, larger than the existing **DO-214AA / SMB**; it requires a future footprint/layout review and is not a drop-in footprint change.

Manufacturer pulse-rating mounting uses **8×8 mm copper at each SMCJ terminal** versus **5×5 mm for SMBJ**; installed geometry must be qualified. SMCJ's 6.5 W continuous headline assumes an infinite heatsink at lead temperature 50 °C, and its 75 °C/W junction-to-ambient value is typical; SMBJ equivalents are 5 W and 100 °C/W. None is an installed continuous-avalanche allowance. [Littelfuse SMCJ](https://www.littelfuse.com/assetdocs/littelfuse_tvs_diode_smcj_datasheet?assetguid=37388813-0d6d-4329-969b-1aa8b7614ac1), [Littelfuse SMBJ](https://www.littelfuse.com/assetdocs/tvs-diodes-smbj-series-datasheet?assetguid=ba555e99-a12d-4f72-a0b6-86b06c67171e)

| Surge quantity | Label and value | Meaning / qualification consequence |
|---|---|---|
| TVS-current waveform | **ASSUMED:** 5 A peak; 10 µs linear rise; exponential tail reaching half-current 1000 µs after start | One isolated positive pulse; no maintained DC tail; source then returns below standoff. This is not a measured source or IEC compliance claim. |
| Charge; pulse I²t | **CALCULATED:** 7.16634 mC; 0.0179367 A²s | Integral of that waveform, not the selected fuse's melting rating. |
| Absorbed energy | **CALCULATED:** 0.41636 J at constant 58.1 V; ≤0.42998 J if node stays ≤60 V | **ASSUMED energy envelope 0.45 J.** Actual source energy, repetition and TVS hot energy capability **OPEN**. |
| Initial TVS junction | **ASSUMED:** 85 °C | Hot initial temperature must include prior loading and local heating. |
| Hot power comparison | **CALCULATED within ASSUMED linear derating:** factor (150−85)/(150−25) = 0.52; SMCJ 780 W, SMBJ 312 W | Pulse peak ≤300 W at 5 A/60 V. SMCJ has 480 W screen reserve; SMBJ only 12 W. A graph/power comparison does not guarantee pulse energy or hot clamp. |
| Hot clamp + layout | **OPEN:** no applicable guaranteed maximum for the assembled hot circuit | **ASSUMED sensitivity only:** 58.1×(1+0.001×60)+2 = **63.586 V**. The breakdown coefficient is deliberately used as a sensitivity, not misrepresented as a clamp guarantee. This exceeds the LDO's 62 V absolute limit and the 60 V node criterion. |
| Sustained fault | **OPEN:** current, duration, shutoff and energy | A 67.2 V / 1 s direct exposure is not qualified by a millisecond pulse rating. Illustratively **ASSUMED** 0.1 A avalanche at 50 V makes **CALCULATED** 5 W and 5 J in one second, with no reason for a 12.5 A fuse to open. |

TVS overload can result in short, open or degraded behavior; coordination must cover those outcomes, rather than relying on a guaranteed short failure. [Vishay failure note](https://www.vishay.com/doc?88440)

## 2. What the higher clamp changes

Documented path: **J501 → F101 → VIN_FUSED → Q101 → U101 IN → VIN_PROTECTED → buck**. D101/C101, IN_SYS/dividers and the D303 auxiliary branch connect to VIN_FUSED; C102 connects to U101 IN. U101 opening does not remove these source-side exposures. Q101's forward body diode is not an independent positive-overvoltage cutoff. BAT46W D303 likewise conducts into the auxiliary branch; no protective forward-drop credit is taken.

The following are **CALCULATED voltage-only screens under ASSUMED 58.1/60 V node conditions**, not tested survival. C101/C102/C307 and several resistor specifications remain placeholders without qualified exact parts.

| Exposed element / established source limit | At 58.1 V | At 60 V acceptance ceiling | Required consequence / OPEN evidence |
|---|---:|---:|---|
| TPS26630 IN / IN_SYS, ordinary +67 V absolute; IN operation ≤60 V | Absolute reserve 8.9 V; operating reserve 1.9 V | Absolute reserve 7 V; operating reserve 0 V | Retain cutoff variant and trip setting. Guarantee actual hot spike and all differential pin limits; no credit for 75 V except its specified 10 ms/25 °C condition. |
| C101/C102, documented 1 µF / 100 V X7R | Rating reserve 41.9 V | 40 V | Nominal voltage specification need not increase. Exact MPN, bias-dependent capacitance, temperature, pulse current and layout remain OPEN. |
| Q101 CSD19537Q3, 100 V VDS / ±20 V VGS | Full-node differential screen reserve 41.9 V | 40 V | Check actual drain/source/gate waveforms. The full raw voltage is a conservative possible VDS, not the normal common-mode difference. It does not isolate positive faults. |
| U306/U307 TPS7A1601, IN operation ≤60 V / absolute 62 V | Operating reserve 1.9 V; absolute 3.9 V | Operating reserve 0 V; absolute 2 V | Hot clamp sensitivity above demonstrates inadequate guaranteed reserve. Need a bounded branch voltage or a higher-voltage supply redesign. |
| Same LDOs, EN tied to raw auxiliary node; EN operation ≤40 V | **18.1 V above operating maximum** | **20 V above** | Add a reviewed, limited enable drive or clamp the whole branch. EN absolute 62 V is not permission to operate EN above 40 V. Even the old 42.1 V TVS clamp exceeded this operating specification. |
| C307, documented 1 µF / 50 V X7R | **8.1 V above rating** | **10 V above** | Qualify a 100 V replacement, or independently bound this branch below the capacitor's derated working voltage. |
| R323, 10 kΩ ±1%, 0.25 W / 75 V placeholder | Worst-resistance P = **0.34097 W** | **0.36364 W** | Its continuous 0.25 W specification is insufficient if this voltage persists; transient survival requires pulse evidence. Select hot usable power ≥0.37 W and voltage margin, or lower branch voltage. A nominal 0.5 W / 100 V specification still needs hot derating and an exact MPN. |
| Auxiliary LDO dissipation, **ASSUMED 10 mA each** | Detector 0.532 W; driver 0.507 W | Detector 0.551 W; driver 0.526 W | Uses inherited minimum outputs 4.8806/7.4403 V; excludes quiescent current and dynamic drive. Actual loads, thermal mounting and transient junction rise OPEN. |

Limits above come from [TPS2663](https://www.ti.com/lit/ds/symlink/tps2663.pdf), [Q101](https://www.ti.com/lit/ds/symlink/csd19537q3.pdf), [TPS7A16](https://www.ti.com/lit/ds/symlink/tps7a16.pdf) and the pinned documentary component specifications.

Additional **CALCULATED/OPEN** checks:

- At the proposed **ASSUMED 35 V continuous fault target**, R323 dissipates 0.12374 W; the two assumed 10 mA LDO loads dissipate 0.3012/0.2756 W. These are thermal inputs, not proof of hot operation. DGN datasheet thermal resistance is a test-board value, not the installed board's guaranteed cooling.
- At 60 V, initial ±0.1% resistors and ±150 nA divider leakage give UVLO pin ≤8.536 V, OVP pin ≤2.614 V and maximum top-resistor voltage 57.402 V/power 9.477 mW. The documented 75 V resistor voltage specification clears this screen; exact parts, hot drift and pulse qualification remain OPEN.
- Under documented gate-drive limits, BGATE at raw 60 V plus 14 V is 74 V, below its 81 V absolute ceiling; DRV at raw 60 V plus 5.2 V is 65.2 V, below its 72 V absolute ceiling. Q101 VGS must still stay within ±20 V and BGATE−IN_SYS within its own 14 V absolute maximum. Q102's source-referenced drive is not the full raw voltage across its 50 V VDS. Fault/dynamic differential waveforms remain OPEN.
- A bidirectional 58.1 V reverse clamp has only 1.9 V magnitude reserve to IN_SYS's −60 V absolute minimum. Q101 must keep U101 IN above −0.3 V. Reverse hot clamp and wiring overshoot are OPEN; the positive 67 V comparison alone does not qualify reverse exposure.
- The buck is on VIN_PROTECTED: its 36 V operating / 42 V absolute input limits cannot tolerate a 58.1 V let-through. Require measured/bounded protected-node peak **≤35 V, ASSUMED with 1 V operating reserve**, including eFuse cutoff delay and stored energy. That requirement and the independent Pi <5.5 V fault containment remain OPEN; the raw TVS cannot establish either. [TI LM61460, SNVSBD5D §§7.1–7.2](https://www.ti.com/lit/ds/symlink/lm61460.pdf)

**Recommended auxiliary direction:** review an independent raw-branch limiter/pre-regulator rated for the entire source fault and transient envelope, targeting **≤35 V ASSUMED** at the existing auxiliary branch. This preserves margin for EN and C307 while reducing LDO heat. Its exact circuit/MPNs, safe default, cold startup, hold-up, absorber energy and common-fault independence are OPEN. If instead retaining raw-fed LDOs, EN limiting, C307 replacement and R323 qualification are mandatory, and the actual hot input must still be proved ≤60 V. This report authorizes neither circuit as already validated.

## 3. F101 selection: DC interruption, hot hold and energy

**Proposed F101: Schurter UMT-H 3403.0285.23**, 12.5 A time-lag, **125 VDC / 1000 A DC interruption**, typical melting I²t **340 A²s at 10× rated current**. The family headline 1500 A does not apply to this 12.5 A row. **ASSUMED voltage envelope for this selection is 67.2 V**; 125 V clears it by **CALCULATED 57.8 V**. It also exceeds 100 V numerically, but does not establish V1A survival at that voltage. Prospective fault current must be ≤1000 A and compatible with the qualified DC circuit conditions; actual source/capacitor current and L/R are **OPEN**. [Schurter UMT-H datasheet](https://www.schurter.com/en/datasheet/typ_UMT-H.pdf)

**ASSUMED hot hold model:** 70% continuous utilization, with conservative graph factors 0.80 at 60 °C or 0.70 at **85 °C local ambient around F101**, excluding its own self-heating already implicit in the fuse characteristic. The installed worst local temperature is **OPEN**; 85 °C is the study envelope, not a newly invented environmental requirement. Manufacturer general selection guidance supplies the continuous factor; temperature factors are rounded-down application assumptions, not guaranteed tabular limits. [Schurter selection guidance](https://www.schurter.com/en/knowledge/fuse-link)

| Exact UMT-H order number | Manufacturer current / DC rating | Typical melting I²t at 10× In | CALCULATED hold screen, 60 °C | CALCULATED hold screen, 85 °C | 5 A at assumed 85 °C |
|---|---|---:|---:|---:|---|
| 3403.0281.23 | 5 A / 125 V / 1500 A | 100 A²s | 2.80 A | 2.45 A | FAIL |
| 3403.0283.23 | 8 A / 125 V / 1500 A | 95 A²s | 4.48 A | 3.92 A | FAIL |
| 3403.0284.23 | 10 A / 125 V / 1500 A | 180 A²s | 5.60 A | 4.90 A | FAIL; viable only with cooler qualified mounting |
| **3403.0285.23** | **12.5 A / 125 V / 1000 A** | **340 A²s** | **7.00 A** | **6.125 A** | **Conditional hold margin 1.125 A (22.5%)** |

Manufacturer test copper for 10/12.5 A parts is **7.5 mm wide / 140 µm thick**. Installed footprint/copper/thermal qualification is necessary; existing thinner copper cannot inherit the hold result. The package is approximately 15.4×5.35 mm and needs a future mechanical/layout review. Typical rated-current drop is 63 mV at 12.5 A, equivalent to **CALCULATED 5.04 mΩ at that test point**; cold resistance, 5 A drop and maximum hot resistance are OPEN. [Schurter UMT-H](https://www.schurter.com/en/datasheet/typ_UMT-H.pdf)

The 12.5 A part's pre-arcing bands allow up to 120 s at 25 A and 10–100 ms at 125 A. **Typical melting I²t is not maximum DC total-clearing I²t**; arcing energy is additional and OPEN. The actual source must be checked against both the fuse's clearing curve and TVS/wiring energy. The latest inherited eFuse current-limit screen is 4.180819–4.819820 A: it cannot force a 12.5 A fuse to clear, and it does not limit the upstream parallel TVS current. Independent bounded source shutdown is required for maintained faults. A larger hold-capable fuse trades away moderate-fault clearing speed.

Alternative fast Littelfuse 0451008.MRL/0451010.MRL parts have 125 VDC but only 50 A DC interruption; the family's 10,000 A / 75 VDC entry is for 2–5 A parts. They cannot be selected on that headline. Their lower typical melting I²t may be useful if source current and hot hold are separately proved; they are not the current recommendation. [Littelfuse 451/453](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1)

## 4. Normal-operation voltage and the 23 V trim requirement

**Drop 23.0 V as a universal requirement derived from OVP. Retain downward trim as a conditional way to meet the frozen 24.0 V normal ceiling.** Use the actual complete normal peak contract, including startup and hot conditions, to set it.

**ASSUMED normal nuisance reserve:** 1.0 V below 26.97 V; this is separate from fault-standoff reserves. **ASSUMED healthy startup/load-step allowance:** +0.150 V. Use the full p-p ripple as a conservative positive allowance until waveform centering is guaranteed; TEP 200's 200 mV p-p is typical only. Unfiltered spike, aging and trim error bounds are OPEN. MEAN WELL ±2% already includes initial, line and load tolerance; do not add those terms twice.

| Module at nominal 24 V | ASSUMED application screen using manufacturer error terms | CALCULATED DC allowance | Ripple allowance | Startup/step allowance | CALCULATED peak | CALCULATED reserve to 26.97 V after 1 V nuisance margin | Frozen 24 V normal ceiling |
|---|---|---:|---:|---:|---:|---:|---|
| RSD-100C-24 | ±2% inclusive; ±0.03%/°C, **0–50 °C only**, ΔT=25 °C | 0.660 V | 0.150 V max | 0.150 V ASSUMED | **24.960 V** | **1.010 V** | FAIL screen |
| RSD-200C-24 | Same | 0.660 V | 0.150 V max | 0.150 V ASSUMED | **24.960 V** | **1.010 V** | FAIL screen |
| TEP 150-4815WI | 1% initial +0.2% line +0.4% load +0.02%/K×45 K; **−20…60 °C ASSUMED** | 0.600 V | 0.200 V max | 0.150 V ASSUMED | **24.950 V** | **1.020 V** | FAIL screen |
| TEP 200-7215UIR | 1% +0.2% +0.1% +0.02%/K×45 K; **−20…60 °C ASSUMED** | 0.528 V | **0.200 V typical**, assumed envelope only | 0.150 V ASSUMED | **24.878 V** | **1.092 V** | FAIL screen |

Source conditions: [RSD-100](https://www.meanwell.com/Upload/PDF/RSD-100/RSD-100-spec.pdf), [RSD-200](https://www.meanwell.com/Upload/PDF/RSD-200/RSD-200-spec.pdf), [TEP 150](https://www.tracopower.com/products/tep150wi.pdf), [TEP 200](https://datasheet.lcsc.com/datasheet/pdf/1aacbb4d3e936de490f194024e78306c.pdf?productCode=C6717418). These screens do not prove maximum normal peaks: RSD temperature coefficient outside 0–50 °C, TEP 200 maximum ripple, and all complete startup/load-step peaks are OPEN. OVP drift is also OPEN. The positive nuisance reserves show why 23 V is not compelled by the initial 26.97 V trip; they do not validate nominal 24 V operation against the separately frozen 24 V ceiling.

| Setting / assumptions | CALCULATED complete-peak screen | Consequence |
|---|---:|---|
| 23 V, complete +3% DC, guaranteed +0.100 V ripple, +0.150 V startup/step | 23.940 V | Leaves 60 mV to frozen ceiling; complete bounds OPEN. |
| Same but +0.200 V positive ripple allocation | **24.040 V** | FAIL. Typical 200 mV p-p is not a guaranteed +100 mV ripple. |
| Complete +3%, +0.200 V ripple, +0.150 V startup/step | Required setting **≤22.9612 V** | A calculation, not a guaranteed supplier trim setting. Leaves no extra reserve at equality. |
| TEP 200 at 23 V using +2.2% of nominal 24 V, +0.200 V ripple, +0.150 V startup/step | **23.878 V** | Leaves 122 mV, but ripple/startup/aging/trim and changed-setting transfer remain OPEN. Usable power is 23×8.4 = **193.2 W before derating**. |

**Recommendation:** ask for a supplier-guaranteed maximum peak ≤24.0 V at the connector, with an explicit reserve and minimum-load/temperature envelope. Retain 23 V as the first TEP 200 enquiry setting; require a lower set point or tighter guaranteed errors if its complete budget demands it. Check all shared loads at that lower voltage. Do not change the eFuse threshold or the normal-input requirement to make a module pass.

## 5. Re-score the four modules

**ASSUMED proposed whole-board continuous fault target: 35 V**, 1 V below the TVS's 36 V catalogue standoff. This is a target for a later complete qualification, not “V1A withstands 35 V.” Actual continuous withstand stays **OPEN** because hot leakage/thermal behavior, auxiliary limits, passives/connectors, source/fuse coordination and protected-node/Pi fault containment are not closed.

The next table applies an additional **ASSUMED 1 V source-to-board reserve** when comparing a module peak with that proposed 35 V board target. This reserve is distinct from the 1 V between the board target and TVS standoff. If the figures are only OVP triggers, listed allowances must absorb all further overshoot; if guaranteed complete peaks, they are residual reserve.

| Module | Supplied OVP figure / manufacturer trigger max | CALCULATED remaining allowance to 36 V standoff after 1 V | CALCULATED allowance to proposed 35 V board target after 1 V | Other established mismatch / OPEN constraint | Revised result |
|---|---:|---:|---:|---|---|
| **RSD-100C-24** | 32.4 V | 2.6 V | 1.6 V | 33.6–62.4 V input / 67.2 V 1 s fails proposed 100 V 1 s primary screen absent qualified PDB suppression. Standard output has no downward trim. Hypothetical 23 V capacity 96.6 W falls below 97.92 W for +50 W scenario, before hot derating. | TVS voltage screen improved; normal/fault/thermal interface **not met**. |
| **RSD-200C-24** | 32.4 V | 2.6 V | 1.6 V | Same primary-surge and fixed-output problems. Hypothetical 23 V gives 193.2 W, enough arithmetically for 160.42 W scenario before hot derating. Factory trim/PDB/cooling are OPEN. | **Not met** as standard standalone unit. |
| **TEP 150-4815WI** | 33.6 V | 1.4 V | 0.4 V | 18–75 V input / 100 V 1 s; trim **24–28.8 V upward only**, so frozen normal ceiling not met. Nominal 151.2 W is below 160.42 W +100 W scenario before hot derating. Isolation/fault peaks remain OPEN. | **Not met**; lowest remaining proposed-board reserve. |
| **TEP 200-7215UIR** | 31.2 V | 3.8 V | 2.8 V | 14–160 V input / 185 V 1 s; trim **19.2–26.4 V**. Best input/trim fit. Requires carrier/cooling and specified primary 150 µF / 200 V capacitor; ripple maximum, fault independence/peak and hot usable power remain OPEN. | **Best next enquiry, not approved.** |

Module source links and revisions are in the normal-budget table and [source register](TVS_SOURCES.md). Power targets are **CALCULATED 35.42 / 97.92 / 160.42 W** for V1A plus **ASSUMED 0 / 50 / 100 W** shared loads, with **ASSUMED** 90% V1A efficiency and 25% reserve. Shared loads are not through V1A. Hypothetical 23 V capacity for a fixed/upward-only module is not an available catalogue setting. Hot capacity and actual loads are OPEN.

Insulation test ratings do not prove single-fault output containment. A module's primary surge rating does not establish its secondary peak at V1A. Raising D101 standoff removes one incompatibility; it cannot turn the revised output-fault requirement into PASS while actual V1A withstand is OPEN. Unbranded nonisolated bucks remain unsuitable for the frozen battery pass-through fault requirement.

## DECISIONS FOR THE OWNER

| Decision | 2–3 options and consequences | Recommended option and reason |
|---|---|---|
| **D101 family** | **A:** SMCJ36CA: clears supplied OVP figures with proposed margin and has more assumed hot pulse-power reserve, but needs larger pads. **B:** SMBJ36CA: smaller existing package class, little reserve for the assumed hot pulse. **C:** retain 26/30/33 V standoff: lower clamp but cannot cover all supplied sustained fault figures with margin. | **A**, for subsequent qualification. It solves the standoff comparison without relying on continuous avalanche. Hot clamp and energy remain acceptance conditions. |
| **Raw auxiliary branch** | **A:** independently limit/pre-regulate to proposed ≤35 V: more components, loss and qualification work; better voltage/thermal reserve. **B:** retain raw-fed TPS7A16 with limited EN, 100 V C307 and qualified R323: fewer architecture changes, requires tight ≤60 V hot raw-node proof. **C:** keep existing branch: 50 V capacitor and EN operating bound conflict with the new clamp. | **A**, because the 62 V LDO limit leaves little room for hot clamp and wiring overshoot. Exact design and common-fault independence are OPEN. |
| **F101 hot hold** | **A:** 12.5 A UMT-H 3403.0285.23, assumed 85 °C hold screen passes; slower moderate-fault clearing and 1000 A interrupt limit. **B:** 10 A 3403.0284.23 with proved local ≤60 °C mounting: lower I²t and 1500 A interrupt rating, cooling contract required. **C:** lower-rated fast fuse: lower melting energy, but hot hold and prospective DC current may fail. | **A provisionally for the assumed 85 °C envelope**, with installed hold, conductor protection and independent source shutdown required. Choose B only if the cooler installed condition is guaranteed. |
| **Maintained input fault** | **A:** qualify an independent cutoff/energy path ahead of D101 with bounded residual peak/energy. **B:** redesign and qualify V1A for the complete source waveform, including auxiliary supply and reverse exposure. **C:** rely on F101 blowing before TVS damage: unproved at low fault current. | **A**, because a hold-capable fuse cannot clear every sustained avalanche fault. The proposed 0.45 J pulse is not a one-second fault contract. |
| **Output setting** | **A:** downward trim near 23 V with a guaranteed complete ≤24 V normal peak. **B:** lower toward 22.96 V if the assumed +3%/+200 mV/+150 mV budget applies: more headroom, less shared-load voltage and usable power. **C:** leave nominal 24 V: calculated peaks exceed the frozen ceiling. | **A**, with the final setting determined by the complete guarantee; use B if that budget cannot be tightened. Drop an unconditional “exactly 23 V” requirement. |
| **Converter choice** | **A:** TEP 200-7215UIR enquiry with qualified input/output protection, carrier and cooling. **B:** supplier-configured isolated module proving the same complete interface. **C:** factory-trimmed RSD plus qualified primary surge suppression: more integration evidence required. | **A as the next enquiry**, while **RECOMMENDED MODULE remains NONE**. It has the strongest input/trim fit; no inspected standalone unit proves the complete normal/fault/thermal contract. |

## Acceptance evidence still required

**OPEN:** define the complete source voltage/current/energy/repetition and worst local temperatures; obtain applicable hot TVS clamp/leakage guarantees; prove ≤60 V exposed raw-node peak and reverse pin limits or redesign for a larger envelope; implement/qualify the auxiliary voltage bound; identify capacitors/resistors; prove installed 5 A fuse hold and applicable DC clearing/current/L/R coordination; bound eFuse protected-node peak and Pi <5.5 V fault behavior; close normal peak, shared-load voltage and hot converter capacity. Tests must use current-limited sources and dummy loads before a Pi.

Documentary calculations and source checks are recorded in [TVS_VALIDATION.md](TVS_VALIDATION.md). They do not replace ERC, hardware thermal/pulse/fault tests or an engineering fabrication review.

**VERDICT: NEW D101 SMCJ36CA, F101 3403.0285.23, V1A WITHSTANDS OPEN V continuous, RECOMMENDED MODULE NONE.**
