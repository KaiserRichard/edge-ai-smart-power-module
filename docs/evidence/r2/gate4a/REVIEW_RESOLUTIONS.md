# Gate4a-FIX review disposition

**VERDICT: BLOCKED. Analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Review has 12 BLOCKING, 4 MAJOR and 1 MINOR numbered findings (17 total); the request describes 14 blockers. All 17 are tracked. CORRECTED means an identified paper defect was fixed; BENCH REQUIRED is unmeasured physical behavior; DESIGN BLOCKED means construction/evidence is missing. None is a hardware PASS.

|Review item|Resolution|Evidence / named measurement|Status|
|---|---|---|---|
|R4A-01|Pending reconciliation|Independent review|PENDING|
|R4A-02|R103 = TNPW0805348KBEEA (348 kΩ) VIN_FUSED→U101 OVP with R104 15.8 kΩ to GND; R340 = TNPW08051M00BEEA (1 MΩ) AUX_12V→U317 FB; R367 initially same 0805 1 MΩ SENSE→GND, revised under R4A-06. 0.1%, 25 ppm/K; replace 0603 lands at capture.|[Vishay TNPW document28758,10-Apr-2026](https://www.vishay.com/docs/28758/tnpw_e3.pdf), resistance, ordering and derating tables; [historical package](history/931e369/README.md).; T07 OVP/hot divider; T06 detector settling; T07 converter loop before power qualification. These test actual board parasitics, not resistor existence.|CORRECTED|
|R4A-03|Pending reconciliation|Independent review|PENDING|
|R4A-04|Pending reconciliation|Independent review|PENDING|
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
