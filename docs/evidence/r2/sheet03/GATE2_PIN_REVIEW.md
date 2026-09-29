# Gate 2 capture and pin review — 2026-09-29

**PRELIMINARY — R2 BLOCKED — NOT FOR FABRICATION**

**DECISION:** retain the capture and two-latch startup/fault circuit committed at `13e4c2d`. The overlapping 78-component alternative is not the captured design. Reconciliation corrects pin/package errors and incorporates the auxiliary reverse-input diode and driver-divider correction. The raw rail passes through Q301/Q302 to the protected rail; no bypass is fitted.

## Manufacturer pin review

Pin numbers below are physical package numbers, viewed as specified by each manufacturer. All populated IC/discrete pins, exposed pads and intentional NCs were compared with the indicated manufacturer pin tables. The [captured contract](../output_block.json) records every pin's actual net; [exported netlist](V1A_gate2.net.xml) is the independent KiCad connectivity evidence. Sources, exact revisions, hashes where locally available, rights and reuse are in the [source register](../../../../third_party/sheet03_source_register.json).

| References / package | DATASHEET pin contract and source |
| --- | --- |
| U301 LTC7001IMSE, MSOP-10 + EP | 1 VCC, 2 VCCUV, 3 GND, 4 INP, 5 OVLO, 6 TGDN, 7 TGUP, 8 TS, 9 BST, 10 NC, 11 GND EP. ADI Rev G, Nov 2021, pp2,7,16. TS connects to both series sources at `PROT_MID`, not the output drain. |
| U302 REF5025IDGKR, DGK | 1 DNC, 2 VIN, 3 TEMP, 4 GND, 5 TRIM/NR, 6 VOUT, 7 NC, 8 DNC. TI SBOS410O, Oct2025, p4. DNCs/TEMP/TRIM/NC remain unconnected. This is the high-grade I version, not AI or EI. |
| U303 TLV3201AIDBVR | 1 OUT, 2 GND, 3 IN+, 4 IN−, 5 VCC. TI SBOS561C, May2024, p3. Reference on IN+, divided raw voltage on IN−; good output is high. |
| U304/U309 SN74LVC1G74DCTR | 1 CLK, 2 D, 3 inverted Q, 4 GND, 5 Q, 6 active-low CLR, 7 active-low PRE, 8 VCC. TI SCES794G, Sep2021, p4; DCT0008A drawing 4220784/D Oct2025, appended pp19–21. U309 inverted Q is NC; PRE held high. |
| U305/U310/U311 SN74LVC1G11DBVR | 1 A, 2 GND, 3 B, 4 Y, 5 VCC, 6 C. TI SCES487I, Nov2024, p3. |
| U306/U307 TPS7A1601DGNR | 1 OUT, 2 FB, 3 open-collector PG, 4 GND, 5 EN, 6 NC, 7 DELAY, 8 IN, 9 GND thermal pad. TI SBVS171F, Oct2015, p4; DGN0008C drawing4218838/A, Nov2017, appended pp34–36. |
| U308 TPS3808G25DBVR | 1 open-drain RESET, 2 GND, 3 active-low MR, 4 CT, 5 SENSE, 6 VDD. TI SBVS050N, Aug2026, pp3–4. G25 monitors the 2.5V reference with nominal 2.33V threshold; it is a startup supervisor, not the precision OVP detector. |
| U312 SN74LVC1G08DBVR | 1 A, 2 B, 3 GND, 4 Y, 5 VCC. TI SCES217AA, Aug2026, p3. |
| U313 SN74LVC1G14DBVR | 1 NC, 2 A, 3 GND, 4 Y, 5 VCC. TI SCES212, revision/date pinned in register, p3. Schmitt inverter for the active-low ARM button. |
| U314 SN74LVC1G17DBVR | 1 NC, 2 A, 3 GND, 4 Y, 5 VCC. TI SCES351Y, Oct2025, p3. Schmitt buffer for the delayed history clock. |
| U315 UCC27511DBVR | **1 VDD, 2 OUTH, 3 OUTL, 4 GND, 5 IN−, 6 IN+.** TI SLUSAW9F, Nov2014, p6. Corrected the wrong mapping in `13e4c2d`. Pin2 feeds R306=1Ω; pin3 goes directly to Q303 gate; pin5 is GND; pin6 receives CROWBAR_ON. |
| Q301/Q302 BSC034N06NSATMA1 | 1–3 source, 4 gate, 5–8 drain. Infineon final Rev2.3, 06-May-2020, p1; pp10–11 package drawings. Both sources share PROT_MID; Q301 drain is raw, Q302 drain is protected. Opposed body diodes block through-conduction when off. |
| Q303 CSD18540Q5B | 1–3 source, 4 gate, 5–8 drain and drain thermal land. TI SLPS488B, Apr2017, p1 diagram and pp8–9. Source is GND; four ballast resistors are upstream of drain. |
| Q304 2N7002,215 | 1 gate, 2 source, 3 drain. Nexperia Rev7, 08-Sep-2011 (served copyright2017), p1 Table2; p5 4.5V RDS test. Replaces the unsuffixed BSS138 with a source-verified SHDN pull-down; same topology. |
| D301/D302 BAS116,215 | 1 anode, 2 NC, 3 cathode. Nexperia 05-Aug-2020, p1 Table2. D301 clamps OV_DIV to the sinking 2.5V reference; D302 precharges BST from the auxiliary driver rail. |
| D303 BAT46W-E3-08 | **1 anode, 2 cathode**. Vishay86406 Rev1.1, 20-Nov-2025, p1; p4 SOD123 drawing. Custom footprint retains this numbering, opposite the generic KiCad cathode=1 convention. VIN_FUSED → anode → cathode → VIN_AUX. |
| R301–R323 | Two-terminal, nonpolar. R308–R311 are exact WFMB2512R0330FEA parts; Vishay30387,04-Aug-2022, pp1–3. Other MPNs remain OPEN procurement specifications; their nominal values, tolerance/rating assumptions and assigned package are captured. No unspecified manufacturer's pinout is claimed verified. |
| C301–C325 | Two-terminal nonpolar MLCC specifications; exact MPN, biased capacitance and thermal qualification remain OPEN. LDO output capacitors must retain at least 2.2µF effective C. Bootstrap C301 must retain more than 82nF for two 41nC gate-charge screens. |
| C330–C337 PCH1V471MCL1GS | 1 positive to raw rail, 2 negative to GND; visible positive marker on the schematic. Nichicon PCH May2024 catalog pp1–2: **470µF/35V, 10×16mm**, 10.3mm platform, 4.6mm terminal spacing. |
| J301/J302 and TP301–TP305 | Project-defined low-energy button/probe interfaces. Header pin1 is ARM_N or RESET_N; pin2 GND. Exact button/header MPNs remain OPEN. Test pads have one physical pad1. They are never load-current connectors. |

## Footprints and changes

- Series FETs use `V1A_Qualified:Infineon_BSC034N06NS_8pin`. The isolated KiCad source combines drain copper under pad5; the adapted footprint numbers the four drain fingers **8,7,6,5** from top to bottom and retains the common drain land. Thus all eight schematic pin numbers have copper pads. Pad6–8 copper overlaps the same-net drain land, intentionally; the checker requires all four drains on the same net.
- U304/U309 use project-authored `TI_DCT0008A_SN74LVC1G74`: 0.65mm pitch, 1.1×0.4mm pads, ±1.9mm row centers. The prior generic SOT-23-8 row spacing did not match DCT0008A. TI's appended land drawing was visually reviewed.
- C330–C337 use `Nichicon_PCH_10x16`. The retained 10mm-family land is adapted from the isolated KiCad source; the incorrect-height model is removed. Catalog dimensions/polarity were visually reviewed. Land/assembly acceptance is still OPEN; no 3D height/model qualification is claimed.
- U301 MSOP exposed pad is 11; U306/U307 exposed pad is 9. The selected stock packages' pitch/body/pad numbers were compared with the manufacturer package drawings. No thermal-performance qualification follows.
- Q303 and ballast retain the project-owned patterns from `13e4c2d`, with all numbered pins present. Their manufacturer drawings remain the geometry basis. Assembly/paste/thermal realization remains OPEN.
- All new physical symbols have a footprint assignment. Generic passive/header assignments are dimensional review choices with MPNs OPEN. The pin-to-pad checker rejects missing, extra or misnumbered copper terminals.

## Capture corrections and state sequence

**DECISION:** add D303 and R323 on Sheet03 only. The independent LDOs previously took VIN_FUSED directly, ahead of the input reverse-protection MOSFET. D303 isolates their positive supply on reverse connection; R323 bleeds VIN_AUX. This is not a claim that the full negative-input/transient envelope is validated. Its hot leakage, rail decay, dropout at 9V and LDO dissipation remain OPEN.

**CALCULATION:** change R314 to 53.9kΩ with R315=10kΩ, giving 7.62327V nominal, while retaining the `DRV_7V5` net name for continuity. A literal 52.8kΩ divider gives 7.49204V nominal and falls below the earlier assumed 7.35V minimum after tolerance. The captured value restores positive regulated-rail headroom. Supply collapse/PG thresholds and nonlinear gate charge remain OPEN timing risks.

Retain R305=2.2MΩ, replacing the earlier concept's unsustainable 22kΩ gate bleed. LTC7001's charge pump is only tens of µA; 22kΩ would consume roughly 0.5mA at 11V. The captured 2.2MΩ draws about 5µA. Confirm steady VGS, startup charge and leakage under actual temperature before crediting the 10V RDS rating.

Reset clears history and holds output off. After supply/reference settling and buck PGOOD, a deliberate ARM edge sets the run latch. A delayed clock stores successful arming in U309; only then can U305 enable the series driver. A subsequent OV or PGOOD fault clears U304, while U309 retains history: U311 asserts the crowbar and Q304 pulls input SHDN low. RESET clears history and permits a fresh deliberate ARM. No successful fault recovery or startup timing has been measured.

**ERC modeling:** two nonphysical source declarations now accompany real fitted paths: VIN_AUX is fed through D303, and VOUT_PROTECTED through Q301/Q302 when enabled. The flags add no wire or bypass. This supersedes the old prohibition on hiding an *empty* Sheet03 with a flag; the physical paths and driver/control pins must pass independent connectivity checks. ERC cannot represent MOSFET on/off states or establish that either rail is safe.

**OPEN:** preserve the Gate1d 18.39mV fault margin, 11.43mV harness margin, unmet100mV dynamic reserve, timing/source/L/C/thermal assumptions, reference-valid and reset behavior, series SOA, inrush, input protection and final connectors. Pin verification is capture evidence only.
