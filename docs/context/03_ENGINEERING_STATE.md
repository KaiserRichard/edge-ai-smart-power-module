# Current engineering state

Consolidated 2026-09-26 from the 2026-09-14 continuation in [FINAL_MANAGER_REPORT.md](../FINAL_MANAGER_REPORT.md), the [blocker review](../evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md), current source files, and explicit user preservation constraints. Repository cleanup is not engineering qualification.

**R2 schematic release: BLOCKED. R3 PCB release: BLOCKED. No printed circuit board (PCB) creation or routing authorized. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Open protection boundary

Sheet 03 — OUTPUT PROTECTION is OPEN. `VOUT_5V1` and `VOUT_PROTECTED` must remain separate. Never short them, create a temporary bypass, add a fake `PWR_FLAG`, or capture placeholder protection to obtain a clean Electrical Rules Check (ERC).

U402/TPS70933 pin 1 is legitimately undriven because `VOUT_PROTECTED` has no supply through Sheet 03. The [dated ERC report](../evidence/r2/forensic_2026-09-14/ERC_qualified.json) records that one error. It is not ERC PASS. Passing capture tests does not release R2.

## Accepted current footprint assignments

| Reference | Assignment |
| --- | --- |
| Q101 | `V1A_Qualified:TI_Q3_CSD19537Q3` |
| U201 | `V1A_Qualified:TI_RJR0014A_LM61460` |
| R401 | `V1A_Qualified:Vishay_WSL2726_Kelvin_1Fplus_2Splus_3Sminus_4Fminus` |

Preserve `hardware/kicad/V1A_Qualified.pretty/`, `fp-lib-table`, and `sym-lib-table`. “Qualified” in the historical library name describes reviewed assignment/geometry scope; thermal, assembly, and PCB layout qualification are not complete. See [footprint evidence](../evidence/r2/forensic_2026-09-14/CRITICAL_FOOTPRINT_QUALIFICATION.md).

| R401 pad | Kelvin intent |
| --- | --- |
| 1 | `VOUT_PROTECTED` FORCE+ |
| 2 | `SHUNT_KPLUS` SENSE+ |
| 3 | `SHUNT_KMINUS` SENSE− |
| 4 | `LOAD_5V1` FORCE− |

## Remaining engineering blockers and validation work

- Output-protection architecture and Raspberry Pi/load voltage-time envelope.
- SMBJ26CA coordination and final source fault envelope.
- Final F101 selection.
- J501/J502/J503 final selection and harness qualification.
- Raspberry Pi compute-rail voltage budget.
- L201 exact physical qualification.
- Capacitor land and effective-capacitance qualification.
- Later thermal and bench validation; no physical measurement is established by repository checks.

**2026-09-26 protection analysis (PROPOSAL, not approved):** [output-protection architecture analysis](../evidence/r2/protection_analysis_2026-09-26/PROTECTION_ANALYSIS.md) finds that an LM74800-only Sheet 03 lets 6.1–8.4 V reach the load in a modelled buck high-side short (blocking finding) and recommends bulk capacitance plus a fast precision detector for user approval. See the [proposed requirement envelope](../evidence/r2/protection_analysis_2026-09-26/REQUIREMENT_ENVELOPE_PROPOSED.md). Sheet 03 remains electrically open.

The detailed blocker review owns closure criteria. This list preserves state; it does not resolve or rank new electrical choices. Earlier R0/R1 proposals and earlier blank-footprint statements remain dated history. Current captured choices and later dated evidence take precedence; report any unresolved contradiction instead of guessing.
