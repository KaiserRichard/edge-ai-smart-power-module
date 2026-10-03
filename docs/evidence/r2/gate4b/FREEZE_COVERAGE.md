# Gate 4b freeze coverage and BOM handoff

2026-10-03. **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

**DECISION:** Gate4a `898759e45578f3767721d19eb313312b7d7733a9` governs circuit selections; the owner's 2026-10-01 option A supersedes its two unresolved autonomous circuit reservations with manual hooks. J502 follows `41cb9e889418d50d2f5f24467e66ac7f15a90476`. No architecture E stage or lower-resistance replacement series pair is imported.

**EVIDENCE:** [machine reconciliation](FREEZE_RECONCILIATION.json) enumerates present and absent reserved references for all 40 freeze rows. [Captured assembly inventory](CAPTURED_BOM.csv) lists all 345 physical references, including etched features and project-defined force interfaces; it is not a procurement BOM. [PR15 delta](CAPTURE_DELTA.json) records every added/retired reference and changed value, MPN, footprint or pin/net assignment. Independent pin/net checks supplement this inventory; presence alone does not prove a circuit correct.

| Freeze row | Capture disposition / evidence |
|---|---|
| S01-01 | D101 SMCJ36CA, SMC footprint; owner selection retained. |
| S01-02 | F101 Schurter 3403.0285.23, authored UMT-H land, 12.5 A time lag / 125 VDC. |
| S01-03 | TPS26630 MODE11 NC for latch-off; SHDN12 from Sheet03. JP101 exposes the source-current boundary before local main capacitance. |
| S01-04 | Q101/Q102 retained; D102 STPS60H100CT A1/A3 to GND, K2/tab to VIN_PROTECTED. |
| S01-05 | C101/C102 exact Murata 1 µF/100 V/1210 selections. |
| S01-06 | Exact five precision resistor codes; R103 348 kΩ uses 0805. |
| S01-07 | **OWNER OPTION A:** J603/U644 manual source trigger; R647–650/Q304 source command/default retained. Autonomous SW/VIN discriminator is absent. Reused U644/C644 refs now denote manual-hook parts, not FIX3 timer logic. |
| S02-01 | L201 Wurth 74437636351002, 10 µH, project THT slot land. Magnetic qualification OPEN. |
| S02-02 | C201/C202 Murata 10 µF/50 V/1210. |
| S02-03 | C203/C204 100 nF/50 V/0603. |
| S02-04 | LM61460 and local 100 kΩ/24.4 kΩ feedback retained. |
| S02-05 | Six TDK ceramics and eight raw PCH capacitors retained on VOUT_5V1. |
| S02-06 | JP201 separates native SW from L201_IN; JP202 measures winding current; paired sense points plus PF2–PF4 force pads. |
| S03-01 | Common-source BSC034 pair, LTC7001, isolated SER_DRV, R711 143 kΩ. JP301 is downstream of both FETs. |
| S03-02 | REF5025/TLV3201, 9.88 kΩ/10 kΩ divider, 1 kΩ sense and reference guards. |
| S03-03 | ADG4612 isolation, independent LM4040 clamp, two BAS116 clamps, sense/rail bleeds. Enable is the manual rail-valid hook under option A. |
| S03-04 | **OWNER OPTION A:** obsolete U304/U309 and qualification gates absent. U610 fault memory and U612/U611 MAIN/SERIES ARM memory use manual controls. No full FIX3 interlock claim. |
| S03-05 | R316/R317 pull PG to 3V3_AUX; old AHCT chain absent as required by FIX3. U607/U651 receive genuine buck PG with R623 pulldown. |
| S03-06 | Q304 retained; obsolete Q305/Q306/Zener bias absent as required by FIX3. R647–650 provide the selected SHDN network. |
| S03-07 | R305 2 MΩ/1206 gate–TS bleed; protected gate and command pulldowns retained. |
| S03-08 | Protected CSD18540/UCC27511 dump; four 33 mΩ elements make two 66 mΩ strings in parallel. JP330 enables branch-current access. |
| S03-09 | Independent raw CSD18540/UCC27511 dump; twelve 33 mΩ elements make two 198 mΩ strings in parallel. JP331 plus raw/protected STPS returns. |
| S03-10 | C340–343: four PCH1V471MCL1GS on protected rail, 1.88 mF nominal candidate. |
| S03-11 | D303, LT4363-1, FDB33N25, 0.33 Ω sense, 10 nF timer and input bypass before the main eFuse. |
| S03-12 | C307/R323 on AUX_LIMITED; U306 IN/EN on DRV_HOLD. U307/R314/R315 retired. |
| S03-13 | LTC3115-1, 4.7 µH L301, exact compensation branches to FB; R341 88.7 kΩ, R345 383 kΩ; internal/local bypasses captured. |
| S03-14 | D304 reverse blocking, two EEUFR1E221 hold capacitors, TPS70933 3V3_AUX supply. C358/C359 use corrected 8 mm / 3.5 mm-pitch lands. |
| S03-15 | TPS3808 adjustable rail monitors with frozen dividers/pull-ups, observation only. |
| S03-16 | Paired TP306–312 plus additional rail/gate/current-link observations. TP308 observes latched FAULT; TP307 observes comparator output. |
| S03-17 | Distinct C301 BST–TS and C302 REF–GND; R312 32.4 kΩ; D302 anode on SER_DRV. |
| S03-18 | TPS259470L controlled hold charging; exact DVDT/ILM/EN/OVLO network, no fast bypass. AUXOFF/FLT have sense points. |
| S04-01 | 2 mΩ four-terminal WSL2726 and INA228 retained with fault-stress annotation. |
| S04-02 | Separate Kelvin senses, symmetric 10 Ω / differential 100 nF filter; TP405/406 force-rail observations. |
| S04-03 | Local TPS70933/TCA9517 and separate host/local pull-ups retained. |
| S04-04 | Sheet05 J502 Phoenix 1776508 / mate 1777989, J503 host map; JP501 M4 dummy-load force takeoff. |
| S04-05 | **EXTERNAL HARNESS:** TE 3-87456-6 + ten 87309-9, Belden 8521 trunks/8502 pigtails documented on Sheet05. No PCB symbol invented for the cable assembly. |
| SXX-01 | All retained passive-completion MPNs match the pinned CSV. Sixteen old logic capacitors and R318–320 retired with their circuits. |
| SFX-01 | **EXTERNAL FIXTURE:** independent bleed adapters are not board components; separately reviewed assembly and discharge acceptance remain required. |
| S06-01 | **OWNER OPTION A, on Sheet03:** SAFE5, POR, real PG receiver and selected held reservoirs retained. Manual reset/ARM/JP600/JP660 replace unresolved fast interlock/diagnostic behavior. No Sheet06 added. |
| SFX-02 | **EXTERNAL FIXTURE:** only DUT-side PF1–PF5/force/sense hooks captured. Injector/limiter/abort/discharge hardware stays in the pinned external fixture BOM. |

## Precedence over the separate BOM draft

**OBSERVATION:** BOM branch `6e5017c9bf61b59a65a6a45a9f8cec0686fcb3f6` only synchronizes Sheets01/02 and still draws later-sheet proposals from older freeze `47c7c07`. Its U319/U324 AHCT population, Q305/Q306/D305, old logic/bypasses, R312=31.9 kΩ, R341=90.9 kΩ and JP501 OPEN do not describe this completed capture. Here R312=32.4 kΩ, R341=88.7 kΩ, C350=10 nF with the selected slow charger, and JP501 is the project M4 interface. Later FIX3 circuitry and owner option A control these changes.

**DECISION:** hand the exported per-reference inventory to the BOM owner for quantity/pricing reconciliation. Do not merge or edit that separate branch, transfer its old quantities to this board, or claim stocked availability. The 31 PR15 retirements are fully enumerated in the delta and Sheet03 review; remaining absent freeze reservations are explicitly listed by row. Custom straps, bolts, insulation, cable mates, switches and fixture procurement remain separate OPEN assembly work.
