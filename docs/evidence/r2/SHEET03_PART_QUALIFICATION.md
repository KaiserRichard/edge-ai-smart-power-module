# Sheet 03 part qualification register

**Date:** 2026-10-01 (Asia/Ho_Chi_Minh)  
**Status:** EVIDENCE ONLY — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED

This register records manufacturer-document data found for Sheet 03 candidates in docs/evidence/r2/BOM_DRAFT.csv. It is a source/rating screen for Gate 4a-FIX, not release approval. A datasheet rating is not automatically a rating for the assembled circuit. OPEN means the current evidence does not establish the requested value or condition. No value is interpolated from a distributor listing or a different package/suffix.

## Critical pulse and power-path evidence

| MPN / refs | Manufacturer source and page | Datasheet data found | Disposition |
| --- | --- | --- | --- |
| CSD18540Q5B / Q303, Q330 | [TI SLPS488B](https://www.ti.com/lit/ds/symlink/csd18540q5b.pdf), pp. 1, 3, 4 Fig. 1, 6 Fig. 10, 8–9 | 60 V N-MOSFET; 400 A pulse headline under stated short-pulse/test-duty conditions; max RDS(on) 3.3 mOhm at 4.5 V/28 A; max Qg 26 nC under its test condition; RthetaJC 0.8 °C/W; SOA/transient curves at cited figures. | Preliminary screen only. Gate 1d uses the published SOA figure and conditional 0.30 us / 5.5 V envelope. Hot SOA, negative waveform, thermal layout, repeat faults and actual downstream C remain OPEN. |
| WFMB2512R0330FEA / R308–R311, R380–R383, R386–R393 | [Vishay WFM 30387](https://www.vishay.com/docs/30387/wfm.pdf), pp. 1–3 | 2512 WFMB range 33–500 mOhm; component TCR ±50 ppm/°C; operating −65 to +170 °C; 2512 max terminal temperature 95 °C; single-pulse chart explicitly valid for 33 mOhm; other values require separate testing. | Selected pulse candidate, not qualified. Existing Gate 1d screen uses 1000 W / 0.100 J per element at 100 us plus an explicit derating assumption. Sharing, repetition and negative current remain OPEN. |
| BSC034N06NSATMA1 / Q301, Q302 | [Infineon BSC034N06NS](https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsc034n06ns-datasheet-en.pdf), Rev. 2.3, p. 1, pp. 10–11 | 60 V N-channel identity and package/pin data. | Exact suffix hot RDS(on), Qg, single-pulse SOA, sharing and layout qualification OPEN. |
| STPS60H100CT / D102, D330, D331 | [ST product page](https://www.st.com/en/diodes-and-rectifiers/stps60h100ct.html) | 100 V dual common-cathode Schottky family; proposed TO-220AB, pins 1/3 anodes and pin 2/tab cathode. | Negative crowbar pulse, thermal mounting, die sharing and exact land OPEN. |
| FDB33N25TM / Q316 | [onsemi product page](https://www.onsemi.com/products/discrete-power-modules/mosfets/FDB33N25TM) | 250 V N-MOSFET identity for AUX pass device. | Exact SOA, linear-mode/pulse, Qg, thermal and package qualification OPEN. |

## Discrete protection and control

| MPN / refs | Source and pages | Data found | Remaining gap |
| --- | --- | --- | --- |
| 2N7002,215 / Q304–Q306 | [Nexperia 2N7002](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf), Rev. 7, p. 1 Table 2, p. 5 | 60 V small-signal N-MOSFET identity; 4.5 V test condition documented. | Gate-clamp, fault-sink pulse energy, polarity and exact suffix/package OPEN. |
| BAS116,215 / D301, D302, D322 | [Nexperia BAS116](https://assets.nexperia.com/documents/data-sheet/BAS116.pdf), p. 1 Table 2 | Low-leakage switching-diode family and absolute-rating table. | Clamp transient, reverse recovery, temperature and exact suffix OPEN. |
| BAT46W-E3-08 / D303 | [Vishay BAT46W](https://www.vishay.com/docs/86406/bat46w.pdf), Rev. 1.1, p. 1, p. 4 | Small-signal Schottky family, pins and package. | AUX surge-stopper pulse/reverse transient and exact order-code land OPEN. |
| B260-13-F / D304 | [Diodes Inc. product page](https://www.diodes.com/part/view/B260-13-F) | 60 V / 2 A Schottky candidate identity. | Exact surge/SOA/pulse and thermal mounting OPEN. |
| BZT52H-C10,115 / D305 | [Nexperia BZT52H-C10](https://www.nexperia.com/product/BZT52H-C10) | 10 V Zener candidate for gate clamp. | Dynamic impedance, pulse energy, exact suffix and gate behavior OPEN. |
| LM4040A25IDBZR / D321 | [TI LM4040](https://www.ti.com/product/LM4040) | 2.5 V shunt-reference candidate. | Clamp-current transient, sink range, partial-power and DBZR qualification OPEN. |

## ICs, logic and regulators

These parts do not have MOSFET-style SOA ratings. The relevant evidence is the manufacturer absolute-maximum/electrical-limit table, timing, supply range and package data; no SOA or pulse rating is claimed where none is specified.

| MPN / refs | Manufacturer source and pages | Data located | Application OPEN items |
| --- | --- | --- | --- |
| LTC7001IMSE#PBF / U301 | [ADI LTC7001](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf), Rev. G, pp. 2–4, 9–12 | High-side driver supply/driver limits, timing and inrush material. | Held rail, gate-loop inductance, pair timing and fault pulse. |
| UCC27511DBVR / U315, U330 | [TI UCC27511](https://www.ti.com/lit/ds/symlink/ucc27511.pdf), p. 6, pp. 9–10 | Pinout and driver electrical/timing conditions. | 7.5 V rail, peak-current loop, Miller turn-on, negative current and repetition. |
| ADG4612BRUZ / U321 | [ADI ADG4612](https://www.analog.com/en/products/adg4612.html) | Quad SPST candidate identity. | Powered-off isolation, injected current, Ron versus DET5 and recovery. |
| LT4363HMS-1#PBF / U316 | [ADI LT4363](https://www.analog.com/en/products/lt4363.html) | Surge-stopper controller identity. | Exact suffix limits, timer, pass-FET SOA, gate clamp and 35 V ceiling. |
| LTC3115IFE-1#PBF / U317 | [ADI LTC3115-1](https://www.analog.com/en/products/ltc3115-1.html) | 40 V, 2 A buck-boost family identity. | Exact suffix, inductor/thermal limits, startup below 8 V, compensation and layout. |
| REF5025IDGKR / U302 | [TI REF50](https://www.ti.com/lit/gpn/REF50), Rev. O, pp. 7–8, 50 | 2.5 V reference family and package data. | Load transient, output-capacitance window and fault-current injection. |
| TLV3201AIDBVR / U303 | [TI TLV3201](https://www.ti.com/lit/ds/symlink/tlv3201.pdf), Rev. C, pp. 4–6 | Input limits, offset, bias, hysteresis and propagation conditions. | DET5 clamp, negative input current, recovery and trip accuracy. |
| SN74LVC1G08DBVR, SN74LVC1G11DBVR, SN74LVC1G14DBVR, SN74LVC1G17DBVR / U305, U310–U314, U320, U325, U326 | [1G08](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf), [1G11](https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf), [1G14](https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf), [1G17](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf) | Logic-family and DBV package sources identified. | Partial-power/Ioff, thresholds at selected VCC, latch race and truth-table closure. |
| SN74LVC1G74DCTR / U304, U309, U320 | [TI SN74LVC1G74](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf), pp. 4, 7–8, 20 | Pinout, PRE/CLR function and propagation/function tables. | Fault-latch race, async set/reset overlap and powered-off behavior. |
| SN74AHCT1G125DBVR / U319, U324 | [TI product page](https://www.ti.com/product/SN74AHCT1G125) | AHCT buffer and DBV identity. | 5 V VIH/VIL, partial supply, output loading and sequencing. |
| TPS3808G01DBVR / U322, U323 | [TI TPS3808](https://www.ti.com/lit/ds/symlink/tps3808.pdf), pp. 3–4 | DBV pin data and supervisor family. | Delay/threshold tolerance, CT mode, hysteresis and loaded rails. |
| TPS70933DBVR / U318, U402 | [TI TPS709](https://www.ti.com/lit/ds/symlink/tps709.pdf) | 3.3 V LDO family and DBV candidate. | Hold-bank capacitance, dropout, reverse current and enable behavior. |
| TPS7A1601DGNR / U306 (U307 DNP) | [TI TPS7A16](https://www.ti.com/lit/ds/symlink/tps7a16.pdf), Rev. F, pp. 5–6, 23, 35 | 60 V / 100 mA adjustable LDO family and package data. | EN≤IN, dropout/thermal dissipation, startup and DGN copper. |

## Passives and capacitors

The BOM nominal values/order codes are source selections, not pulse qualification. Exact-order-code datasheet review, DC-bias/temperature derating, package/land confirmation and circuit-specific pulse calculations remain OPEN for TDK/Murata ceramics, Panasonic EEU-FR1E221, Nichicon PCH1V471MCL1GS, Vishay TNPW/CRCW parts and WSL2512R3300FEA. Do not apply the WFM pulse chart to those different families.

The [Nichicon PCH catalogue](https://www.nichicon.co.jp/english/_assets/images/products/catalog/corporate/digital/PCH_e.pdf), pp. 1–2, identifies the PCH family and the 470 uF / 35 V candidate row; effective capacitance, ESR, ripple, lifetime and fault-pulse suitability remain OPEN.

## Gate 4a-FIX conclusions

- **EVIDENCE:** CSD18540Q5B and WFMB2512R0330FEA have the most directly relevant reviewed SOA/pulse evidence; their cited curves are the basis of the conditional Gate 1d screen.
- **EVIDENCE:** the pinned source inventory provides manufacturer documents and page locations for the remaining selected Sheet 03 semiconductors, logic and regulators.
- **OPEN RISK:** no entry closes hot crowbar pulse, diode reverse pulse, hold-bank ride-through, startup, partial-power, layout, sharing or repeated-fault questions.
- **DECISION:** retain the BOM identities as source-selected candidates. This evidence does not change MPNs, prices, stock, quantities or footprints.

**Provenance:** source inventory is third_party/sheet03_source_register.json plus docs/evidence/r2/sheet03/GATE1D_PULSE_REVIEW.md. Sources are manufacturer documents/product pages, referenced only; no manufacturer circuit or CAD was copied or modified. Distributor pages are not electrical qualification evidence.

