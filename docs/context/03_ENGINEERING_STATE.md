# Current engineering state

Consolidated 2026-09-26 from the 2026-09-14 continuation in [FINAL_MANAGER_REPORT.md](../FINAL_MANAGER_REPORT.md), the [blocker review](../evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md), current source files, and explicit user preservation constraints. Repository cleanup is not engineering qualification.

**R2 schematic release: BLOCKED. R3 PCB release: BLOCKED. No printed circuit board (PCB) creation or routing authorized. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Sheet 03 — Gates1d + 2, completed 2026-09-30

**PRELIMINARY — READY FOR SCHEMATIC REVIEW; Gate1d/Gate2 CONDITIONAL PASS.** Candidate C + crowbar is captured using the two-latch circuit from `13e4c2d`, CSD18540Q5B, four WFMB2512R0330FEA drain-ballast elements (33mΩ equivalent), UCC27511 and a common-source BSC034N06NS pair driven by LTC7001. The independent driver rail is 7.62327 V nominal, with the existing `DRV_7V5` net name retained.

**EVIDENCE:** [pin review](../evidence/r2/sheet03/GATE2_PIN_REVIEW.md), [captured-value calculation](../evidence/r2/sheet03/GATE2_CALCULATIONS.md), [scope/check report](../evidence/r2/sheet03/GATE2_VALIDATION.md) and [full marked PDF](../evidence/r2/sheet03/V1A_GATE2_PRELIMINARY.pdf). ERC has 0 violations; 15 capture/footprint tests and the current repository checker pass. The strict historical cache audit still fails for archived sources/predecessor checkouts; it is not reported as PASS.

**OPEN margins:** the assumed 0.30 µs crowbar timing gives 5.481612 V / +18.388mV. Gate1c's0.20µs screen gave +39.328mV; the larger selected FET's charge screen required the longer preliminary delay. Reduced harness assumptions give 4.761431 V / +11.431mV at 5 A. The 100 mV dynamic reserve remains unmet. No measured timing or peak is claimed. Source/L/C, temperature, pulse tail, startup/reset, auxiliary supplies, series SOA and remaining component qualifications remain OPEN.

## Captured protection boundary

`VOUT_5V1` reaches `VOUT_PROTECTED` only through the fitted opposed MOSFETs; no bypass is present. Sheet03's source declarations describe the real diode-fed auxiliary rail and transistor-switched protected rail for ERC. They do not validate those paths or permit an unfitted source. The independent checker verifies the physical pin/net and package paths.

The historical U402.1 undriven error belonged to the empty Sheet03 stub. Its disappearance is now supported by the captured power path and documented declarations, not by shorting the two rails. The earlier ERC report remains dated evidence.

**Next gate:** remaining R2 engineering review of the actual capture and OPEN limits. R2 release and R3 remain BLOCKED; no PCB work is authorized.

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

- Qualify the captured output-protection circuit, startup/reset, normal/fault transient bounds, and proof of the frozen Pi peak limit; no Pi damage-versus-time allowance is credited.
- SMBJ26CA coordination and final source fault envelope.
- Final F101 selection.
- J501/J502/J503 final selection and harness qualification.
- Raspberry Pi compute-rail voltage budget.
- L201 exact physical qualification.
- Capacitor land and effective-capacitance qualification.
- Later thermal and bench validation; no physical measurement is established by repository checks.

The detailed blocker review owns closure criteria. This list preserves state; it does not resolve or rank new electrical choices. Earlier R0/R1 proposals and earlier blank-footprint statements remain dated history. Current captured choices and later dated evidence take precedence; report any unresolved contradiction instead of guessing.
