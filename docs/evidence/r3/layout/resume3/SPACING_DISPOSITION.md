# Native package spacing disposition required

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**OBSERVATION:** KiCad 9.0.6 reproduces all 53 baseline error pairs after every track, via and zone is removed from a temporary board. No project board, footprint or rule is changed by this diagnostic. Translation and rotation preserve these within-package gaps.

**REQUIREMENT:** the resume brief demands rules at least as strict as the supplied fab contract, 0 DRC errors, unchanged qualified lands, and closure of M1-5. With the present package assignments those requirements cannot all be met by layout.

**OPEN / DECISION REQUIRED:** an engineering-approved pairwise voltage/fabrication exception that explicitly revises the brief’s strict contract, or an approved schematic/package/protection change. No such decision was supplied. No exception is proposed as already safe; solder mask is not credited as insulation.

| Package | Native violating pad pairs |
|---|---:|
| U101 | 13 |
| U201 | 2 |
| U317 | 5 |
| U316 | 4 |
| Q101 | 5 |
| U302 | 6 |
| U403 | 6 |
| U600 | 6 |
| U306 | 6 |

| Package / first pad | Second pad | Required / actual gap, mm |
|---|---|---|
| Pad 1 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of U101 | Pad 24 [unconnected-(U101-NC-Pad24)] of U101 | 0.6400 / 0.2993 |
| Pad 1 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of U101 | Pad 25 [/GND] of U101 | 0.6400 / 0.2000 |
| Pad 2 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of U101 | Pad 3 [/01_INPUT_PROTECTION/INPUT_BGATE] of U101 | 0.6400 / 0.2500 |
| Pad 2 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of U101 | Pad 25 [/GND] of U101 | 0.6400 / 0.2000 |
| Pad 3 [/01_INPUT_PROTECTION/INPUT_BGATE] of U101 | Pad 4 [/01_INPUT_PROTECTION/INPUT_DRV] of U101 | 0.6400 / 0.2500 |
| Pad 3 [/01_INPUT_PROTECTION/INPUT_BGATE] of U101 | Pad 25 [/GND] of U101 | 0.6400 / 0.2000 |
| Pad 4 [/01_INPUT_PROTECTION/INPUT_DRV] of U101 | Pad 5 [/VIN_FUSED] of U101 | 0.6400 / 0.2500 |
| Pad 4 [/01_INPUT_PROTECTION/INPUT_DRV] of U101 | Pad 25 [/GND] of U101 | 0.6400 / 0.2000 |
| Pad 5 [/VIN_FUSED] of U101 | Pad 6 [/01_INPUT_PROTECTION/INPUT_UVLO] of U101 | 0.6400 / 0.2500 |
| Pad 5 [/VIN_FUSED] of U101 | Pad 25 [/GND] of U101 | 0.6400 / 0.2000 |
| Pad 14 [/01_INPUT_PROTECTION/INPUT_FLT] of U101 | Pad 25 [/GND] of U101 | 0.2500 / 0.2000 |
| Pad 17 [/01_INPUT_PROTECTION/EFUSE_OUT] of U101 | Pad 25 [/GND] of U101 | 0.2500 / 0.2000 |
| Pad 18 [/01_INPUT_PROTECTION/EFUSE_OUT] of U101 | Pad 25 [/GND] of U101 | 0.2500 / 0.2000 |
| Pad 1 [/GND] of U201 | Pad 14 [/02_BUCK_5V/BUCK_CBOOT] of U201 | 0.6400 / 0.2500 |
| Pad 13 [/02_BUCK_5V/BUCK_RBOOT] of U201 | Pad 14 [/02_BUCK_5V/BUCK_CBOOT] of U201 | 0.6400 / 0.2500 |
| Pad 12 [/03_OUTPUT_PROTECTION/AUX_VCC] of U317 | Pad 13 [/03_OUTPUT_PROTECTION/AUX_LIMITED] of U317 | 0.2500 / 0.2000 |
| Pad 13 [/03_OUTPUT_PROTECTION/AUX_LIMITED] of U317 | Pad 14 [/03_OUTPUT_PROTECTION/AUX_VCC] of U317 | 0.2500 / 0.2000 |
| Pad 15 [/03_OUTPUT_PROTECTION/AUX_BST2] of U317 | Pad 16 [/03_OUTPUT_PROTECTION/AUX_BST1] of U317 | 0.6400 / 0.2000 |
| Pad 16 [/03_OUTPUT_PROTECTION/AUX_BST1] of U317 | Pad 17 [/03_OUTPUT_PROTECTION/AUX_LIMITED] of U317 | 0.6400 / 0.2000 |
| Pad 17 [/03_OUTPUT_PROTECTION/AUX_LIMITED] of U317 | Pad 18 [/03_OUTPUT_PROTECTION/AUX_SW1] of U317 | 0.2500 / 0.2000 |
| Pad 3 [/03_OUTPUT_PROTECTION/AUX_SNS] of U316 | Pad 4 [/03_OUTPUT_PROTECTION/AUX_GATE_DRIVE] of U316 | 0.6400 / 0.2500 |
| Pad 4 [/03_OUTPUT_PROTECTION/AUX_GATE_DRIVE] of U316 | Pad 5 [/03_OUTPUT_PROTECTION/AUX_RAW] of U316 | 0.6400 / 0.2500 |
| Pad 7 [/GND] of U316 | Pad 8 [/03_OUTPUT_PROTECTION/AUX_RAW] of U316 | 0.6400 / 0.2500 |
| Pad 8 [/03_OUTPUT_PROTECTION/AUX_RAW] of U316 | Pad 9 [/GND] of U316 | 0.6400 / 0.2500 |
| Pad 1 [/VIN_FUSED] of Q101 | Pad 5 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of Q101 | 0.6400 / 0.5600 |
| Pad 2 [/VIN_FUSED] of Q101 | Pad 5 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of Q101 | 0.6400 / 0.5600 |
| Pad 3 [/VIN_FUSED] of Q101 | Pad 4 [/01_INPUT_PROTECTION/INPUT_BGATE] of Q101 | 0.6400 / 0.1500 |
| Pad 3 [/VIN_FUSED] of Q101 | Pad 5 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of Q101 | 0.6400 / 0.5600 |
| Pad 4 [/01_INPUT_PROTECTION/INPUT_BGATE] of Q101 | Pad 5 [/01_INPUT_PROTECTION/VIN_EFUSE_IN] of Q101 | 0.6400 / 0.5600 |
| Pad 1 [unconnected-(U302-DNC-Pad1)] of U302 | Pad 2 [/03_OUTPUT_PROTECTION/DET5] of U302 | 0.2000 / 0.1500 |
| Pad 2 [/03_OUTPUT_PROTECTION/DET5] of U302 | Pad 3 [unconnected-(U302-TEMP-Pad3)] of U302 | 0.2000 / 0.1500 |
| Pad 3 [unconnected-(U302-TEMP-Pad3)] of U302 | Pad 4 [/GND] of U302 | 0.2000 / 0.1500 |
| Pad 5 [unconnected-(U302-TRIM_NR-Pad5)] of U302 | Pad 6 [/03_OUTPUT_PROTECTION/REF_2V5] of U302 | 0.2000 / 0.1500 |
| Pad 6 [/03_OUTPUT_PROTECTION/REF_2V5] of U302 | Pad 7 [unconnected-(U302-NC-Pad7)] of U302 | 0.2000 / 0.1500 |
| Pad 7 [unconnected-(U302-NC-Pad7)] of U302 | Pad 8 [unconnected-(U302-DNC-Pad8)] of U302 | 0.2000 / 0.1500 |
| Pad 1 [/3V3_HOST] of U403 | Pad 2 [/SCL_HOST] of U403 | 0.2000 / 0.1500 |
| Pad 2 [/SCL_HOST] of U403 | Pad 3 [/SDA_HOST] of U403 | 0.2000 / 0.1500 |
| Pad 3 [/SDA_HOST] of U403 | Pad 4 [/GND] of U403 | 0.2000 / 0.1500 |
| Pad 5 [/04_POWER_MONITOR/3V3_LOCAL] of U403 | Pad 6 [/04_POWER_MONITOR/SDA_LOCAL] of U403 | 0.2000 / 0.1500 |
| Pad 6 [/04_POWER_MONITOR/SDA_LOCAL] of U403 | Pad 7 [/04_POWER_MONITOR/SCL_LOCAL] of U403 | 0.2000 / 0.1500 |
| Pad 7 [/04_POWER_MONITOR/SCL_LOCAL] of U403 | Pad 8 [/04_POWER_MONITOR/3V3_LOCAL] of U403 | 0.2000 / 0.1500 |
| Pad 1 [/03_OUTPUT_PROTECTION/SAFE5] of U600 | Pad 2 [/03_OUTPUT_PROTECTION/SAFE_FB] of U600 | 0.2000 / 0.1500 |
| Pad 2 [/03_OUTPUT_PROTECTION/SAFE_FB] of U600 | Pad 3 [unconnected-(U600-PG-Pad3)] of U600 | 0.2000 / 0.1500 |
| Pad 3 [unconnected-(U600-PG-Pad3)] of U600 | Pad 4 [/GND] of U600 | 0.2000 / 0.1500 |
| Pad 5 [/03_OUTPUT_PROTECTION/SAFE_IN] of U600 | Pad 6 [unconnected-(U600-NC-Pad6)] of U600 | 0.2000 / 0.1500 |
| Pad 6 [unconnected-(U600-NC-Pad6)] of U600 | Pad 7 [unconnected-(U600-DELAY-Pad7)] of U600 | 0.2000 / 0.1500 |
| Pad 7 [unconnected-(U600-DELAY-Pad7)] of U600 | Pad 8 [/03_OUTPUT_PROTECTION/SAFE_IN] of U600 | 0.2000 / 0.1500 |
| Pad 1 [/03_OUTPUT_PROTECTION/DET5] of U306 | Pad 2 [/03_OUTPUT_PROTECTION/DET_FB] of U306 | 0.2000 / 0.1500 |
| Pad 2 [/03_OUTPUT_PROTECTION/DET_FB] of U306 | Pad 3 [/03_OUTPUT_PROTECTION/DET_PG] of U306 | 0.2000 / 0.1500 |
| Pad 3 [/03_OUTPUT_PROTECTION/DET_PG] of U306 | Pad 4 [/GND] of U306 | 0.2000 / 0.1500 |
| Pad 5 [/03_OUTPUT_PROTECTION/DRV_HOLD] of U306 | Pad 6 [unconnected-(U306-NC-Pad6)] of U306 | 0.2000 / 0.1500 |
| Pad 6 [unconnected-(U306-NC-Pad6)] of U306 | Pad 7 [unconnected-(U306-DELAY-Pad7)] of U306 | 0.2000 / 0.1500 |
| Pad 7 [unconnected-(U306-DELAY-Pad7)] of U306 | Pad 8 [/03_OUTPUT_PROTECTION/DRV_HOLD] of U306 | 0.2000 / 0.1500 |

**EVIDENCE:** [pad-only native DRC](PAD_ONLY_DRC.json), [current baseline DRC with parity](BASELINE_DRC.json), [machine-readable pairs](NATIVE_SPACING.json), [unchanged rule contract](RULE_CONTRACT.json). The temporary diagnostic retained package placement, pads and project/rule settings, removed authored copper only, and ran without schematic parity because no temporary schematic was copied. Baseline parity is zero.

**DECISION:** preserve the errors. Do not weaken a rule, shrink a land, substitute a package, change a net, or mark M1-5 closed without the required engineering disposition.
