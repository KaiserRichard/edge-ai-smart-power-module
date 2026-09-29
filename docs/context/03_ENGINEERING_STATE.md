# Current engineering state

Consolidated 2026-09-26 from the 2026-09-14 continuation in [FINAL_MANAGER_REPORT.md](../FINAL_MANAGER_REPORT.md), the [blocker review](../evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md), current source files, and explicit user preservation constraints. Repository cleanup is not engineering qualification.

**R2 schematic release: BLOCKED. R3 PCB release: BLOCKED. No printed circuit board (PCB) creation or routing authorized. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Sheet 03 architecture gate — 2026-09-29

**BLOCKED — Candidate C close attempt did not reach preliminary capture readiness.** The authoritative [Sheet 03 architecture decision](../evidence/r2/sheet03/SHEET03_ARCHITECTURE_DECISION.md) now records a complete review concept and bounded calculation. The sole named blocker is `B1_FAULT_INTERRUPTION_ENVELOPE`: the accepted source/inductance transient and a production-supported or measured effective isolation time below approximately 0.385 µs are missing. The calculated normal false-trip margin is +22 mV; the 30 V/0.5 µH/2 µs fault screen is −368 mV. KiCad remains unchanged.

**Current user requirements:** normal input 9–24 V; final source 13S battery → PDB → future HV-to-approximately-12-V auxiliary converter → V1A. Direct 54.6 V pass-through containment is allocated upstream, not to V1A. Pi 5 receives power through GPIO 5 V pins and multiple GND pins. Total output envelope is 5 A; qualification includes idle, sustained CPU-heavy Pi 5, Pi 5 + D435i, and representative load steps. **Pi rail peak must remain strictly below 5.5 V; 5.5 V is not the detector threshold.** Exact converter dynamics and J502/harness remain OPEN. The fixed peak criterion supersedes older 6 V screens; no undocumented permitted overvoltage pulse is assumed.

**Next gate:** bounded Candidate-C circuit/transient-contract review and architecture selection; only a successful readiness decision permits single-agent Sheet 03 capture with ERC/netlist/diff validation. No PCB authorization follows.

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

- Complete output-protection circuit, normal/fault transient bounds, and proof of the frozen Pi peak limit; no Pi damage-versus-time allowance is required or credited.
- SMBJ26CA coordination and final source fault envelope.
- Final F101 selection.
- J501/J502/J503 final selection and harness qualification.
- Raspberry Pi compute-rail voltage budget.
- L201 exact physical qualification.
- Capacitor land and effective-capacitance qualification.
- Later thermal and bench validation; no physical measurement is established by repository checks.

The detailed blocker review owns closure criteria. This list preserves state; it does not resolve or rank new electrical choices. Earlier R0/R1 proposals and earlier blank-footprint statements remain dated history. Current captured choices and later dated evidence take precedence; report any unresolved contradiction instead of guessing.
