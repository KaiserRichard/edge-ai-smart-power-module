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
