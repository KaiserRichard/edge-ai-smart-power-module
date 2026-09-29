# Active decision index

Consolidated 2026-09-26; this is an index into existing decisions, not a replacement engineering history or newly granted architecture approval. The date is the context consolidation date, not an invented original decision date.

| Active decision / constraint | Basis and evidence | State / limit |
| --- | --- | --- |
| V1A is a standalone compute module, not the WBR power distribution board | User scope; [overview](01_PROJECT_OVERVIEW.md); [requirements](../00_REQUIREMENTS.md) | KNOWN scope; future robot interface not frozen |
| LM61460 buck architecture selected | Captured U201; [buck review](../evidence/r2/BUCK_DESIGN.md) | KNOWN captured choice; electrical release BLOCKED |
| TPS26630 input electronic-fuse architecture selected | Captured U101; [input review](../evidence/r2/INPUT_PROTECTION.md) | KNOWN captured choice; source/fuse/transient qualification OPEN |
| INA228 + 2 mΩ Kelvin shunt selected | Captured U401/R401; [monitor review](../evidence/r2/MONITOR_POWER_DOMAINS.md) | KNOWN captured choice; measurement accuracy not bench validated |
| Sheet 03 must not be bypassed | [Output review](../evidence/r2/OUTPUT_PROTECTION.md); explicit user constraint | Captured opposed-FET path; preserve separate raw/protected nets and independent no-bypass checks |
| R2 must close before PCB work | [Manager report](../FINAL_MANAGER_REPORT.md); [gate workflow](05_WORKFLOW_AND_GATES.md) | R2/R3 BLOCKED; R3 requires separate authorization |
| Never fabricate qualification state | [AGENTS.md](../../AGENTS.md); [engineering state](03_ENGINEERING_STATE.md) | Permanent evidence discipline |

## 2026-09-30 — Gate2 preliminary capture completed

Retain and reconcile `13e4c2d`; do not replace its two-latch startup/fault implementation with the overlapping alternative. Manufacturer pin review corrects UCC27511 to 1 VDD / 2 OUTH / 3 OUTL / 4 GND / 5 IN− / 6 IN+; the series-FET footprint retains pads 1–8. The auxiliary diode, driver divider 53.9 kΩ/10kΩ and reviewed package/polarity corrections are captured. Unrelated sheets are preserved with the explicitly listed hierarchy exceptions. See [Gate2 validation](../evidence/r2/sheet03/GATE2_VALIDATION.md).

Gate2 is CONDITIONAL PASS for preliminary review: ERC 0 violations,15 tests and current repository checks pass, captured thresholds are recalculated, and the marked six-page PDF exists in both requested locations. The 18.388 mV fault and 11.431 mV harness margins remain OPEN; the former uses0.30µs rather than Gate1c's0.20µs assumed crowbar action time. R2/R3 release stays BLOCKED. This dated result supersedes the old empty-Sheet03/expected-ERC-error state, without changing historical evidence.

## 2026-09-29 — Gate1d preliminary pulse selection

User acceptance of Candidate C + crowbar supersedes earlier architecture/no-capture decisions for preliminary Sheet03 capture. Gate1d CONDITIONAL PASS selects CSD18540Q5B, four WFMB2512R0330FEA drain-ballast elements (33mΩ equivalent), UCC27511 at7.5V. Moving the ballast off the source fixes the demonstrated VGS contradiction. Revised fault margin18.388mV and static harness margin11.431mV remain OPEN. See the [pulse review](../evidence/r2/sheet03/GATE1D_PULSE_REVIEW.md) for temperature/duration/SOA evidence. Gate2 authorized; R2/R3 release BLOCKED. Earlier entries below are historical, not competing current verdicts.

## 2026-09-29 — requirements consolidation and Sheet 03 no-go

Authoritative record: [SHEET03_ARCHITECTURE_DECISION.md](../evidence/r2/sheet03/SHEET03_ARCHITECTURE_DECISION.md). Today's conductor D-27/D-30 and protection/Pi/connector branch identities are recorded there; they were inspected, not merged or rewritten.

| Decision / requirement | Rationale and evidence state | Result |
| --- | --- | --- |
| Freeze GPIO 5 V + multiple GND power, normal 9–24 V input, 5 A total envelope and specified Pi/D435i qualification loads | User instruction; D-30 consolidation | REQUIREMENT, not measured capability; supersedes older interface/adapter questions |
| Allocate direct 54.6 V converter pass-through containment upstream | Current user instruction: 13S → PDB → future auxiliary converter → V1A | Responsibility resolved; residual source voltage/current/time/energy bounds and converter MPN remain OPEN |
| Require `V_Pi_peak < 5.5 V` including transients | Current user instruction, tightening the earlier ≤5.5 V wording | Supersedes 6 V screening; detector threshold must leave tolerance and let-through margin |
| Do not select/capture Sheet 03 yet | Native LM74800 window fails the retained 50 mV margin screen; LTC4368 dynamic evidence is inadequate; precision direction lacks a complete bounded circuit/state proof | Architecture gate BLOCKED; conditional capture/commit/push continuation not entered; R2/R3 remain BLOCKED |

## 2026-09-29 — Candidate C Gate 1c

Gate 1c retains Candidate C and adds a low-side crowbar: CSD17308Q3, UCC27511DBVR, and a 33 mΩ ballast screen driven by the same detector/latch. The crowbar is the selected preliminary development direction because its conditional 5.46067 V Pi peak leaves +39.33 mV at 119.96 A and 0.02483 A²s modeled I²t, whereas series-only is 5.86600 V and −366.00 mV. The eFuse remains the upstream current-limit/latch path; SHDN and the fault latch prevent automatic retry. The remaining single design blocker is `B1C_UNCOORDINATED_FAULT_ENERGY_PATH`: pulse-rated ballast, MOSFET SOA, and complete source-to-commutation bounds are not closed. Harness co-design selects reduced cut-path resistance with raw-node detection; remote sense and setpoint increase fail one of the required windows. No KiCad capture is authorized.

## 2026-09-29 — Candidate C Gate 1b

Candidate C is retained as the only review concept: REF5025 + TLV3201 threshold detector, SN74LVC1G74 latch, LTC7001 independent high-side driver, and common-source BSC034N06NS pair. With explicit assumptions and a reproducible script, `V_trip` is 5.325 V nominal / 5.294–5.357 V corner and the normal-release screen leaves +22 mV. The 30 V, 0.5 µH, 2 µs fault screen reaches 5.868 V, failing the Pi limit by 368 mV. The single remaining blocker is `B1_FAULT_INTERRUPTION_ENVELOPE`: authoritative source/inductance bounds and an effective isolation time below 0.385 µs are not evidenced. No KiCad capture is authorized.

Future entries should link to the authoritative dated decision record, include rationale and evidence state, and identify superseded decisions explicitly. Do not copy whole reviews here.
