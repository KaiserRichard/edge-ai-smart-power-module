# Gate4a-FIX review disposition

**VERDICT: BLOCKED. Analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Review has 12 BLOCKING, 4 MAJOR and 1 MINOR numbered findings (17 total); the request describes 14 blockers. All 17 are tracked. CORRECTED means an identified paper defect was fixed; BENCH REQUIRED is unmeasured physical behavior; DESIGN BLOCKED means construction/evidence is missing. None is a hardware PASS.

|Review item|Resolution|Evidence / named measurement|Status|
|---|---|---|---|
|R4A-01|Pending reconciliation|Independent review|PENDING|
|R4A-02|R103 = TNPW0805348KBEEA (348 kΩ) VIN_FUSED→U101 OVP with R104 15.8 kΩ to GND; R340 = TNPW08051M00BEEA (1 MΩ) AUX_12V→U317 FB; R367 initially same 0805 1 MΩ SENSE→GND, revised under R4A-06. 0.1%, 25 ppm/K; replace 0603 lands at capture.|[Vishay TNPW document28758,10-Apr-2026](https://www.vishay.com/docs/28758/tnpw_e3.pdf), resistance, ordering and derating tables; [historical package](history/931e369/README.md).; T07 OVP/hot divider; T06 detector settling; T07 converter loop before power qualification. These test actual board parasitics, not resistor existence.|CORRECTED|
|R4A-03|Replace unsupported U319 dual-DCU proposal with separate U319/U324 SN74AHCT1G125DBVR buffers. Five-pin DBV circuit, pullups, 220 kΩ output pulldowns and100 nF local bypass are explicit in S03-05; existing SUPPLY_OK and BUCK_PGOOD receiver nets must pass through these outputs. No dual footprint reuse.|[TI SCLS378P March2024](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf), pins/DC; [exact DBVR order entry](https://www.ti.com/product/SN74AHCT1G125/part-details/SN74AHCT1G125DBVR); accessed2026-09-30.; T03 BUFFER-SEQUENCING. PASS only with no source/series conduction before valid rails plus freshARM; no DET5 backfeed>0.3 V; every pin remains within ratings. Measures unspecified partial-power behavior under passive shutdown; does not replace the R4A-15 policy implementation.|CORRECTED / BENCH REQUIRED|
|R4A-04|R305 = TNPW12102M20BEEA,2.2 MΩ,0.1%/25ppm/K,1210, common PROT_GATE→PROT_MID source. Remove220 kΩ proposal. Retain LTC7001IMSE#PBF and BAS116,215 D302; C301 assigned under R4A-05. 2.2M requires1210 because1206 ends at2MΩ.|[ADI LTC7001 RevG](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf), electrical/charge-pump/bootstrap; [Vishay TNPW28758 10-Apr-2026](https://www.vishay.com/docs/28758/tnpw_e3.pdf),1210 range/ordering.; T04 BOOTSTRAP-DC-HOLD. PASS measuredVGS−U≥10V under lowestDRV_HOLD andTS4.75…5.5V,0/5A,25°C/hot,10-minute settled hold; no continuing downwardBST/VGS trend. Repeat after input removal through disposal; verify physical series-off in T08. Measurement closes TS5V pump/leakage not guaranteed by theTS20V table.|CORRECTED / BENCH REQUIRED|
|R4A-05|Pending reconciliation|Independent review|PENDING|
|R4A-06|Pending reconciliation|Independent review|PENDING|
|R4A-07|Pending reconciliation|Independent review|PENDING|
|R4A-08|Pending reconciliation|Independent review|PENDING|
|R4A-09|Pending reconciliation|Independent review|PENDING|
|R4A-10|Pending reconciliation|Independent review|PENDING|
|R4A-11|Pending reconciliation|Independent review|PENDING|
|R4A-12|Pending reconciliation|Independent review|PENDING|
|R4A-13|Pending reconciliation|Independent review|PENDING|
|R4A-14|Pending reconciliation|Independent review|PENDING|
|R4A-15|Pending reconciliation|Independent review|PENDING|
|R4A-16|Pending reconciliation|Independent review|PENDING|
|R4A-17|Pending reconciliation|Independent review|PENDING|

## R4A-02 — CORRECTED

**DECISION:** R103 = TNPW0805348KBEEA (348 kΩ) VIN_FUSED→U101 OVP with R104 15.8 kΩ to GND; R340 = TNPW08051M00BEEA (1 MΩ) AUX_12V→U317 FB; R367 initially same 0805 1 MΩ SENSE→GND, revised under R4A-06. 0.1%, 25 ppm/K; replace 0603 lands at capture.

**CALCULATION / consequence:** Rmin=Rnom(1−0.001−25 ppm/K×60 K)=0.9975Rnom. At 58.1 V across R103, P≤9.724 mW. R340 at 12.311325 V: P≤0.151949 mW. R367 at 2.5 V: 6.266 µW. 0805 range ≤1 MΩ, working voltage 150 V, general-operation P70=140 mW; conditional 85°C linear derating toward125°C gives101.818 mW. Values unchanged, initial-only OVP26.973873–28.289211 V / aux11.621343–12.311325 V screens retained; pads/parasitic transfer is not assumed unchanged.

**EVIDENCE:** [Vishay TNPW document28758,10-Apr-2026](https://www.vishay.com/docs/28758/tnpw_e3.pdf), resistance, ordering and derating tables; [historical package](history/931e369/README.md).

**CLOSURE:** T07 OVP/hot divider; T06 detector settling; T07 converter loop before power qualification. These test actual board parasitics, not resistor existence.

## R4A-03 — CORRECTED / BENCH REQUIRED

**DECISION:** Replace unsupported U319 dual-DCU proposal with separate U319/U324 SN74AHCT1G125DBVR buffers. Five-pin DBV circuit, pullups, 220 kΩ output pulldowns and100 nF local bypass are explicit in S03-05; existing SUPPLY_OK and BUCK_PGOOD receiver nets must pass through these outputs. No dual footprint reuse.

**CALCULATION / consequence:** At 3V3_AUX floor3.2 V and measured total PG leakage≤10µA: VHIGH≥3.2−10µA×10.025k=3.09975 V, margin1.09975 V to2.0 V. At AUXmax3.4 V, PG low≤0.4 V requires sink0.300752 mA. At DET5≤5.5 V,220k minimum219.45k consumes25.06µA; total output load must remain≤50µA for the 4.4 V minimum high at4.5 V table condition. LVC threshold≤0.7×5.5=3.85 V gives0.55 V conditional static margin. The 8 mA hot VOH3.8 V table is not the25°C3.94 V value and is not credited to this low-load bound. AHCT has no output Ioff guarantee; partial-power outputs cannot enforce fail-off. Inputs may be high with VCC=0 within their stated leakage/rating test conditions; same-rail receivers and passiveSHDN enforce containment.

**EVIDENCE:** [TI SCLS378P March2024](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf), pins/DC; [exact DBVR order entry](https://www.ti.com/product/SN74AHCT1G125/part-details/SN74AHCT1G125DBVR); accessed2026-09-30.

**CLOSURE:** T03 BUFFER-SEQUENCING. PASS only with no source/series conduction before valid rails plus freshARM; no DET5 backfeed>0.3 V; every pin remains within ratings. Measures unspecified partial-power behavior under passive shutdown; does not replace the R4A-15 policy implementation.

## R4A-04 — CORRECTED / BENCH REQUIRED

**DECISION:** R305 = TNPW12102M20BEEA,2.2 MΩ,0.1%/25ppm/K,1210, common PROT_GATE→PROT_MID source. Remove220 kΩ proposal. Retain LTC7001IMSE#PBF and BAS116,215 D302; C301 assigned under R4A-05. 2.2M requires1210 because1206 ends at2MΩ.

**CALCULATION / consequence:** At10 V,220k requires45.455µA versus15µA minimum pump atTS20V/10V differential table point. 2.2M nominal requires4.545µA; at12V andRmin2.1945M,5.469µA. Residual15−5.469=9.531µA is a test-point leakage budget only. At actualTS≈5V andDRV_HOLD≈11V, D302 cannot replenishBST≈15V; no TS5V pump minimum is provided. C cannot cure steady DC loss. With82nC/10V effective gate capacitance, passiveτ≈18.04ms; activeTGDN must establish fault cutoff. Hot leakage/full gate charge remain OPEN.

**EVIDENCE:** [ADI LTC7001 RevG](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf), electrical/charge-pump/bootstrap; [Vishay TNPW28758 10-Apr-2026](https://www.vishay.com/docs/28758/tnpw_e3.pdf),1210 range/ordering.

**CLOSURE:** T04 BOOTSTRAP-DC-HOLD. PASS measuredVGS−U≥10V under lowestDRV_HOLD andTS4.75…5.5V,0/5A,25°C/hot,10-minute settled hold; no continuing downwardBST/VGS trend. Repeat after input removal through disposal; verify physical series-off in T08. Measurement closes TS5V pump/leakage not guaranteed by theTS20V table.
