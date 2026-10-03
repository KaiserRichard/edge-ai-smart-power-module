# Gate 4B pin and land review

**PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

Pin/land review is capture evidence, not application qualification. Existing parts retain the PR15 pin and land reviews unless a row below changes them. New project geometry is authored from manufacturer dimensions. Nominal values are DATASHEET; thresholds and timing screens are CALCULATED; missing application bounds remain ASSUMED or OPEN.

## Sheet 01

- F101: Schurter **3403.0285.23**, UMT-H, manufacturer sheet dated **21.07.2026**, pp2/4/5. Two nonpolar terminals; no exposed pad. Lands 3.75 × 5.6 mm, 10 mm inside gap, centers ±6.875 mm. Body 15.4 × 5.35 mm. Do not use the smaller UMT250 family. Custom project footprint follows this drawing; installed clearing and copper thermal design remain OPEN. Source: https://www.schurter.com/en/datasheet/typ_UMT-H.pdf .
- D101: **SMCJ36CA**, bidirectional DO-214AB/SMC; two interchangeable terminals, no exposed pad. Assigned standard KiCad `Diode_SMD:D_SMC`; frozen 36 V stand-off and 58.1 V test clamp are distinct quantities. Hot/source coordination remains OPEN.
- D102: ST **STPS60H100CT**, **DS3978 Rev3, August2018**, pp1/5/6. Pin1 A1 and pin3 A2 join GND; pin2 K and metal tab join VIN_PROTECTED. Standard TO-220-3 vertical footprint has 2.54 mm pitch. Electrically isolated mounting is required if the heatsink is grounded. Source: https://www.st.com/resource/en/datasheet/stps60h100c.pdf .
- C101/C102: Murata GRM32ER72A105KA01L, 1210 nonpolar two-terminal MLCC, 1µF/100V. R103 becomes0805; other divider/current resistors retain0603. Exact MPNs follow freeze S01-05/06 and passive completion. Bias capacitance and hot thresholds remain OPEN.
- U101 remains TPS26630RGER, pins1/2 IN,5 IN_SYS,8/25 ground/EP,11 MODE intentionally unconnected,12 SHDN. Existing latch-off selection retained; no automatic retry or fabricated permission added.

## Power-source declarations

The inherited ERC power flags on VIN_RAW/GND/3V3_HOST describe external J501/J503 sources; VIN_FUSED and VIN_EFUSE_IN describe those same sources through fitted F101 and Q101. They do not represent missing power-path parts, and they do not assert a control permission or successful protection behavior. Every added declaration must list its physical source path here and pass the independent connectivity checks.

## Sheet 02

- L201: Wurth **74437636351002**, drawing **001.000, 2025-02-07**, p1. Two winding terminals; pad1 at(-5.75,-12.1) and pad2 at(+5.75,+12.1), plated slots9.5×3.5mm, center offsets11.5/24.2mm. Authored11.5×5.5mm copper surrounds each slot; annular ring and high-current plating require R3/R4 review. The36×35.7mm body and34.2mm maximum height are recorded; no PCB placement is performed. Source: https://www.we-online.com/components/products/datasheet/74437636351002.pdf .
- C201/C202 become Murata10µF/50V1210; C203/C204/C205 are100nF/50V0603. R202/R203 retain100k/24.4k. Main feedback and bootstrap pins retain the existing TI review.
- JP201: authored **CUSTOM-FX-CU-01 RevA** M4 force interface, two numbered isolated pads20mm apart,4.5mm holes; removable external C110 strap from FIX3_FIXTURE. No PCB copper joins these pads. Pin1 native BUCK_SW, pin2 L201_IN. Default test setup removes the strap. Strap/parasitic/current qualification remains OPEN; it is not a2.54mm signal shunt.
- TP201/202/203: authored paired1.5mm etched pads,2.54mm pitch, pin1 signal/pin2 local power return. Sense connections carry no force current.

## Resumed Sheet 01/02 fixture access

JP101 now separates U101 OUT17/18 (`EFUSE_OUT`) from every main local input capacitor (`VIN_PROTECTED`). TP103 measures the source side. `#FLG103` declares only the physical U101→JP101 source path. JP202 separates L201.2 (`L201_OUT`) from the raw bank, for IL201 measurement. PF2/3/4 expose VIN_PROTECTED/native BUCK_SW/L201_IN with single 10 mm copper lands and 4.5 mm holes. PF1/5 on Sheet 05 complete DUT input/power return access. These authored fixture interfaces follow FIX3 C110/M4 geometry; current, plating, bolt torque, insulation, contact resistance and parasitics remain R3/T12 OPEN. All force links are absent during isolated logic/rail work. No signal shunt substitutes for them.

## Sheet 03 — package-specific independent pin review

[PIN_CONTRACTS.json](PIN_CONTRACTS.json) records every active new semiconductor pin independently from the generated connection specification. Existing PR15 semiconductor identities and lands retain their source ledger; the following additions were checked against manufacturer pin tables. Package EP statements are part of the review, not inferred from a generic symbol.

| New device / refs | DATASHEET pin/package finding | Assigned land / disposition |
|---|---|---|
| LT4363HMS-1#PBF / U316 | ADI Rev C pp2/22: MS12, 1FB 2OUT 3SNS 4GATE 5VCC 6SHDN 7GND 8UV 9GND 10FLT 11ENOUT 12TMR; **no EP**. Pin7 is GND in the -1 variant. | Stock MSOP12 3×4.039 mm /0.65 mm. |
| FDB33N25TM / Q316 | onsemi FDB33N25/D Rev3 Jan2022 pp1/8: gate1, drain2/tab, source3. | Stock TO-263-3_TabPin2; tab is electrically live AUX_RAW. |
| LTC3115IFE-1#PBF / U317 | ADI Rev E pp2/40: FE20, **EP21=PGND**. VIN13/PVIN17, SW1=18/SW2=3, BST1=16/BST2=15, VCC12/PVCC14, PVOUT4. Full ledger checks all21 pins. | New ADI_FE20_EP2.74x4.95 follows drawing05-08-1663 RevL CA: 0.65 mm pitch, 1.05×0.45 mm leads, EP2.74×4.95 mm. Project six-window stencil proposal requires R3 process review. |
| 7447789004 / L301 | Wurth007.000,2023-05-30,p1: two winding terminals, no EP; 7.3 mm body. | New 1.7×2.0 mm lands with4.0 mm inner gap (centers±3 mm). No sensitive traces under body. |
| TPS259470LRPWR / U327 | TI SLVSFC9C May2026 pp5–6/72–74: RPW10, **no extra EP**. Broad copper IN5/OUT6; AUXOFF3/FLT4 (not PG/PGTH of other variants). | New TI_RPW0010A_TPS25947: drawing4225183/A08-2019 copper and stencil contours, 0.1 mm stencil example. Ground is pin8. |
| TPS70933DBVR / U318 | TI SBVS186H p3: IN1 GND2 EN3 NC4 OUT5, no EP. EN intentionally open per manufacturer; not tied to held12 V. | Stock SOT-23-5, same reviewed family as U402. |
| TPS3808G01/G50DBVR / U322,U323,U602 | TI SBVS050N Aug2026 pp3–4: RESET1 GND2 MR3 CT4 SENSE5 VDD6; DBV has no EP. CT open is fixed-delay mode; G01 adjustable versus G50 4.65 V threshold. | Stock SOT-23-6. U322/U323 are observation only. |
| ADG4612BRUZ / U321,U651 | ADI Rev0 p10 TSSOP column: 1IN1 2D1 3S1 4VSS 5GND 6S4 7D4 8IN4 9IN3 10D3 11S3 12NC 13VDD 14S2 15D2 16IN2; no EP. | Stock TSSOP16 4.4×5 mm/0.65 mm; unused channels grounded; pin12 NC. |
| LM4040A25IDBZR / D321,D601 | TI SLOS456Q Apr2026 p4: K1 A2; pin3 floats or joins anode, here GND. No EP. | Stock SOT-23; independent shunt references never short into REF5025 output. |
| SN74LVC1G32DBVR / U615 | TI SCES219W Aug2026 p3 DBV5: A1 B2 GND3 Y4 VCC5; no EP. | Stock SOT-23-5. |
| LVC1G74/08/14/17, TLV3201, TPS7A16, UCC27511, CSD18540, BAS116 reused at new refs | PR15 independent ledger retained. DCT flip-flop **CLK1 /CLR6 /PRE7**, DGN LDO **EP9=GND**, UCC27511 **OUTH2 OUTL3 IN−5 IN+6**. | Existing project DCT/Q5B or reviewed stock lands. No use of alternate package pin maps. |
| STPS60H100CT / D330,D331 | Same DS3978 Rev3 pin/tab review as D102. | TO-220-3 vertical; individual tabs tied to their respective output rails. |
| B260-13-F / D304,D600,D660 | Diodes SMB cathode band corresponds to project pad1 K; pad2 A. No EP. | D_SMB; anodes face the upstream supply, cathodes face the held/isolated reservoir. |
| EEUFR1E221 / C358,C359 | Panasonic exact part record, checked 2026-10-03: 8.0 mm diameter, 11.5 mm length, 3.5 mm pitch. Polar radial capacitor: pad1+, pad2−; negative stripe faces GND. | **Corrected** to CP_Radial_D8.0mm_P3.50mm; draft 6.3 mm/2.5 mm land was wrong. Height/clearance/ripple/lifetime remain assembly review. |
| C340…343 | Same PCH1V471MCL1GS polarity and10×16 mm project land as PR15 C330…337. | Positive protected rail, negative GND; 1.88 mF nominal only. |
| New resistors / ceramics | Exact freeze MPNs; nonpolar pins1/2, no EP. R3052M uses1206; R3401M and R345383k use0805; R3320.33Ω uses2512. | Metric lands selected by manufacturer case; pulse/DC-bias/thermal qualification stays OPEN. All exported pad numbers checked. |
| J603…606, JP600, JP660 and sense/force interfaces | JST B2B-XH-A uses PR15 qualified2.50 mm THT footprint. Pin1 is labelled signal/feed; pin2 return or switched supply as specified. Etched pairs and force links have project-defined numbering. | Signal/low-current access only except explicitly M4 force links. Dry-contact controls must not inject external logic power. |

**EVIDENCE:** manufacturer references and retrieval limitations are in `third_party/gate4b/SOURCES.json`; stock footprint files are referenced unchanged. `build_gate4b_footprints.py` creates only the three new Sheet03 packages. No upstream CAD or entire PCB was copied. The TI land artwork is adapted into project footprints with manufacturer attribution; fabrication-process checks remain OPEN.

**Power declarations on Sheet03:** AUX_RAW from F101/D303; AUX_LIMITED from Q316/R332; AUX_PREHOLD from U317/D304; SER_DRV from U327/D660/JP660; SAFE_IN from U327/D600/R602; VOUT_PROTECTED from U201/JP201/L201/JP202/Q301/Q302/JP301. These declare physical power paths, never valid PG, source-trip coverage, MANUAL_RAILS_VALID, RUN or fault permission. Flags are excluded from physical BOM/board. Missing links invalidate their test configuration; ERC cannot prove a fitted strap or healthy semiconductor.

## Sheet 04

R401/INA228 retain the PR15 four-terminal Kelvin contract and qualified WSL2726 lands. Force1→VOUT_PROTECTED and force4→LOAD_5V1 remain distinct; sense2/3 feed the symmetric10Ω/100nF filter. TPS70933/TCA9517 pin maps and host/local domains are unchanged. The exact freeze MPNs complete R402…408/C401 and remaining bypasses; C404 retains the PR15 TDK2220 land. TP405/406 use the same reviewed paired etched1.5mm/2.54mm pads as other sense hooks, pin1 force-node observation/pin2 GND. These are not load connectors. Calculated10mV/50mW at5A and nominal ADC ranges are annotated; accuracy, pulse stress and thermal behavior remain OPEN.

## Second resume — source sensing observation circuit

**EVIDENCE:** U640/U642 use TLV3201AIDBVR, [TI SBOS561C, revised May 2024, p3](https://www.ti.com/lit/ds/symlink/tlv3201.pdf): OUT1, GND2, IN+3, IN−4, VCC5; DBV5 has no exposed pad. U647 uses the **TSSOP** ADG4612BRUZ column of [ADI Rev0, p10](https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf): the existing independent 16-pin ledger applies; no LFCSP exposed pad is invented. D640…643 use [Nexperia BAS116, Rev5, 5 August 2020, p1](https://assets.nexperia.com/documents/data-sheet/BAS116.pdf), A1/NC2/K3, no EP. Sources were reopened during this resume; footprints use the already reviewed SOT-23-5, TSSOP16 and SOT-23 libraries. All pins/lands are checked against the independent ledger and fresh XML.

R640/641/642/644/645/651/652 and C640/642/647 retain the exact FIX3_SOURCE_TRIGGER selections and 0603 nonpolar lands. TP337…340 use the reviewed paired sense pads, signal1/GND2, with no force-current role. The front end is connected to the real hierarchical L201_IN and VIN_PROTECTED, not duplicated local labels. R640 is after JP201; C205 remains before JP201. No power declaration was added.

**DECISION:** the frozen analog sensing circuit is captured for observation. U641/643/645/646 and their autonomous qualifier/memory function remain absent under owner option A; U644 retains its documented manual-source role. Observed SW_HIGH/VIN_GOOD_FAST never drive SRC_TRIP or permission. Shared reference loading/injection, threshold/hysteresis, probe capacitance, SAFE5 current/hold and partial-power recovery remain OPEN.
