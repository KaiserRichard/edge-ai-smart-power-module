# Lifecycle capacitor closure — 2026-10-04

**Historical review:** [BOM_LOCK_ALL review](LOCK_REVIEW.md) supersedes this document's selection holds for five exact Murata parts and adds the disclosed C351 family proxy. Original calculations and rejected alternatives below are preserved.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**CONFIRMED:** six previously flagged MPNs reviewed; a seventh (GRM32ER71H106KA12L) is also EOL in the [Mouser snapshot](https://www.mouser.fr/fr/ProductDetail/Murata-Electronics/GRM32ER71H106KA12L?qs=6pxx44s1bjkjdm74o%2FrKhg%3D%3D), accessed 2026-10-04. Five candidates pass the Task 1 capacitance screen. Two are selected in the order BOM; three groups remain OPEN for timing/compensation review under Task 2. Two further candidates lack bias evidence. No hardware file changed.

[Manufacturer facts](../../../../third_party/bom_order/CLOSE_CAPACITOR_FACTS.json) preserve adjacent curve samples, exact public request URLs, catalog dimensions/status and access date. [Decisions](../../../../third_party/bom_order/CLOSE_ALTERNATE_REVIEW.json) record every reference, both connected nets, voltage basis and calculated Ceff. Packaging suffixes use verified catalog identities; no constructed MPN is selected.

**CALCULATED:** interpolate Murata SimSurfing C-DC-bias numerical data at 25°C / 1 Vrms. These are typical absolute capacitances, not nominal capacitance multiplied by an invented derating factor. Compare `Ceff_alt/Ceff_original >= 0.90`. **ASSUMED:** steady rail/diode-drop screens are explicitly identified per reference. Startup ramps include their documented upper endpoint; bootstrap capacitors use pin-to-pin differential, not switch-node common mode. Fault screens are additional evaluations, not claims of normal operation. Full bias/temperature/tolerance/age qualification remains at the existing electrical gates.

| Original | Chosen alternate / candidate | Same package, C, dielectric; voltage | Lowest ratio at evaluated net voltages | Disposition |
|---|---|---|---|---|
| GRM32ER72A105KA01L | C3225X7R2A105K200AA | 1210, 1 µF X7R 100 V; existing Capacitor_SMD:C_1210_3225Metric | OPEN | OPEN |
| GRM188R71H104KA93D | GRM188R72A104KA35D | X7R, 100 V; existing Capacitor_SMD:C_0603_1608Metric | 95.64% | CONFIRMED |
| GRM32ER71H106KA12L | C3225X7R1H106K250AC | 1210, 10 µF X7R 50 V; existing Capacitor_SMD:C_1210_3225Metric | OPEN | OPEN |
| GRM21BR71E105KA99L | GCM21BR71E105KA56L | X7R, 25 V; existing Capacitor_SMD:C_0805_2012Metric | 97.62% | CONFIRMED |
| GRM21BR71E475KA73L | GRM21BZ71E475KE15L | X7R, 25 V; existing Capacitor_SMD:C_0805_2012Metric | 98.45% | CONFIRMED |
| GRM21BR71H105KA12L | GCM21BR71H105KA03L | X7R, 50 V; existing Capacitor_SMD:C_0805_2012Metric | 98.86% | CONFIRMED |
| GRM1885C1H330JA01D | GRM1885C2E330JW07D | C0G, 250 V; existing Capacitor_SMD:C_0603_1608Metric | 100.00% | CONFIRMED |

**CONFIRMED:** in-production status B for the five Murata alternates comes from the manufacturer’s SimSurfing catalog, not residual distributor stock. Body dimensions are recorded in JSON. Standard nonpolar 0603/0805 lands remain assigned; alternate maximum height is 0.90/1.40/1.45 mm as recorded. The TDK candidates are explicitly Production on their exact [1 µF](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R2A105K200AA) / [10 µF](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1H106K250AC) pages, accessed 2026-10-04, but are unaccepted because Ceff comparisons are missing.

## Effective capacitance at each net voltage

All values below **CALCULATED**, µF (33 pF = 0.000033 µF). Voltage assumptions/sources and exact per-reference nets are in the decision JSON. Repeated rail populations are grouped only for readability.

| References | DC V across capacitor | Original Ceff µF | Alternate Ceff µF | Ratio |
|---|---:|---:|---:|---:|
| C101, C102, C378 | 9 | OPEN | OPEN | OPEN |
| C101, C102, C378 | 26 | OPEN | OPEN | OPEN |
| C101, C102, C378 | 58.1 | OPEN | OPEN | OPEN |
| C103 | 4.17 | 0.1009437 | 0.1011608 | 1.0022 |
| C103 | 4.75 | 0.1008023 | 0.1008924 | 1.0009 |
| C203, C204 | 9 | 0.09912322 | 0.09846682 | 0.9934 |
| C203, C204, C380 | 26 | 0.0827794 | 0.07932327 | 0.9582 |
| C203, C204 | 30 | 0.07713456 | 0.07377111 | 0.9564 |
| C205, C369, C370, C402, C405, C406 | 3.3 | 0.1010878 | 0.1015385 | 1.0045 |
| C303, C304, C364, C604, C609, C640, C642, C644, C647, C651, C710, C711, C712, C714, C715, C716, C717, C723, C728, C730, C731, C732, C733, C754, C756, C761, C762 | 5.05832 | 0.1007144 | 0.1007452 | 1.0003 |
| C308, C368, C376 | 12 | 0.09741839 | 0.09612957 | 0.9868 |
| C308, C368, C376 | 12.311325 | 0.09721368 | 0.09585257 | 0.9860 |
| C308, C368, C376 | 12.593099 | 0.0970238 | 0.09559895 | 0.9853 |
| C354, C355 | 4.45 | 0.1008793 | 0.1010335 | 1.0015 |
| C354, C355 | 4.58 | 0.1008466 | 0.1009729 | 1.0013 |
| C380 | 30.788889 | 0.07599051 | 0.07268204 | 0.9565 |
| C380 | 35 | 0.06982579 | 0.06697738 | 0.9592 |
| C401 | 0.01 | 0.1008059 | 0.1023998 | 1.0158 |
| C401 | 0.16384 | 0.1007949 | 0.1023974 | 1.0159 |
| C201, C202 | 9 | OPEN | OPEN | OPEN |
| C201, C202 | 26 | OPEN | OPEN | OPEN |
| C201, C202 | 30 | OPEN | OPEN | OPEN |
| C305, C601 | 5.05832 | OPEN | OPEN | OPEN |
| C306, C352, C377, C602, C660 | 12 | OPEN | OPEN | OPEN |
| C306, C352, C377, C602, C660 | 12.311325 | OPEN | OPEN | OPEN |
| C306, C352, C377, C602, C660 | 12.593099 | OPEN | OPEN | OPEN |
| C601 | 5.183488 | OPEN | OPEN | OPEN |
| C206 | 3.3 | 1.036539 | 1.011822 | 0.9762 |
| C301, C309, C365, C367, C374, C375, C600 | 12 | 0.8521483 | 0.8369003 | 0.9821 |
| C301 | 14 | 0.7887712 | 0.7804736 | 0.9895 |
| C309, C365, C367, C375, C600 | 12.311325 | 0.8424428 | 0.8282879 | 0.9832 |
| C309, C365, C367, C375, C600 | 12.593099 | 0.8335925 | 0.820428 | 0.9842 |
| C374 | 17.312 | 0.6838798 | 0.6854656 | 1.0023 |
| C302 | 2.5 | 4.881468 | 4.806014 | 0.9845 |
| C353, C379 | 4.45 | 3.948476 | 4.24045 | 1.0739 |
| C353, C379 | 4.58 | 3.882319 | 4.197475 | 1.0812 |
| C366 | 3.3 | 4.527505 | 4.598502 | 1.0157 |
| C307 | 26 | 0.6000702 | 0.6004332 | 1.0006 |
| C307 | 30.788889 | 0.5085125 | 0.5058762 | 0.9948 |
| C307 | 35 | 0.4403582 | 0.4353402 | 0.9886 |
| C403 | 5.1 | 1.022066 | 1.021522 | 0.9995 |
| C403 | 5.5 | 1.018222 | 1.017868 | 0.9997 |
| C357 | 11 | 3.3e-05 | 3.299999e-05 | 1.0000 |
| C357 | 11.334325 | 3.3e-05 | 3.299999e-05 | 1.0000 |
| C357 | 11.616099 | 3.3e-05 | 3.299999e-05 | 1.0000 |

## Needs owner decision

- **B001 — GRM32ER72A105KA01L:** original model absent; local Murata reference sheet GRM32ER72A105KA01-01A (2026-06-26) gives nominal ratings, not a part-specific bias curve. C3225X7R2A105K200AA is a 1210/1 µF/100 V/X7R candidate; both Ceff values remain OPEN. TDK public model download was unavailable. Obtain manufacturer curves before acceptance. The previous GRM32CR72A105KA35L suggestion is [Last Time Buy](https://www.digikey.com/en/products/detail/murata-electronics/GRM32CR72A105KA35L/2548428), accessed 2026-10-04, and is rejected.
- **B003 — GRM32ER71H106KA12L:** newly found EOL; original absent from SimSurfing. Candidate C3225X7R1H106K250AC requires original/alternate curves, current-bank energy/stability review, and land check. Remains OPEN despite residual stock.
- **Rejected B004 candidate:** GRM219R71E105KA88D gives 0.702170 µF versus 0.852148 µF at 12 V (82.40%); it fails the 90% rule. GCM21BR71E105KA56L replaces that proposal; C374 timing remains an untested electrical qualification item, including the existing >=0.5 µF through 17.312 V requirement.

## Provenance and limits

Manufacturer source files were referenced, not modified; no third-party circuit was copied. SimSurfing dynamic page/data revision is undated; access 2026-10-04. Copyright Murata/TDK; no open redistribution license established; only factual dimensions and selected model points are retained with attribution. Local datasheets in `wt-datasheets/third_party/datasheets` were read-only. ADI LTC3115-1 Rev E p4, TI LM61460 SNVSBD5D (2022-07) LDO table and TPS2663 SLVSE94G (2024-06) electrical table establish internal/bias rail screens (exact local revisions are retained in the source PDF). Project voltage sources are pinned in each JSON record to the freeze commit and captured netlist, accessed 2026-10-04. No third-party PCB reuse.

## Timing-sensitive owner holds

The bias-screen CONFIRMED status above is distinct from order acceptance. Only B007 and B008 are selected. The complete grouped rows B002, B004 and B013 retain their captured MPNs; no timing-sensitive reference is silently substituted.

- **GRM188R71H104KA93D → GRM188R72A104KA35D: OPEN.** C103 sets input DVDT/startup; C401 sets telemetry filter timing. Different bias behavior needs owner timing review before a grouped-row substitution.
- **GRM21BR71E105KA99L → GCM21BR71E105KA56L: OPEN.** C374 sets HOLD_SLEW_C timing and >=0.5 uF requirement; changing its bias curve needs owner timing review.
- **GRM1885C1H330JA01D → GRM1885C2E330JW07D: OPEN.** C357 is LTC3115 feedforward compensation; loop/timing qualification is not established by nominal C0G and bias matching.

## Resume check — 2026-10-04

**CONFIRMED:** all seven flagged capacitor MPNs have a disposition. Five candidates pass the typical-bias screen; only B007/B008 are accepted for order selection. Missing original curves at B001/B003 and timing holds at B002/B004/B013 remain **OPEN**. The manufacturer data already collected are reused.

**CALCULATED / ASSUMED correction:** C352 is on AUX_12V (use the same 12/12.311325/12.593099 V screens as C377), C601 is on SAFE5 (5.05832 V nominal / 5.183488 V static upper), and C602 is on SAFE_IN (auxiliary-rail upper screens with diode/resistor drops omitted). The previous draft applied AUX_LIMITED, driver, and SAFE5 voltages respectively to those three references. Their Ceff remains **OPEN**. Prior values are retained in `voltage_correction_history` in the decision JSON.

**EVIDENCE:** [captured netlist](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/4af7818511076cbbd336880607d262fc311d01bc/docs/evidence/r3/layout_prep/resume/fresh.xml), [FREEZE_TABLE S03-13](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FREEZE_TABLE.md), and [FIX3_INTERLOCK regulator/reservoir and updated numerical screens](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FIX3_INTERLOCK.md), read locally from pinned Git objects on 2026-10-04. No new electrical requirement is inferred.
