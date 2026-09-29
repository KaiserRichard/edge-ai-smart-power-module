# Active decision index

Consolidated 2026-09-26; this is an index into existing decisions, not a replacement engineering history or newly granted architecture approval. The date is the context consolidation date, not an invented original decision date.

| Active decision / constraint | Basis and evidence | State / limit |
| --- | --- | --- |
| V1A is a standalone compute module, not the WBR power distribution board | User scope; [overview](01_PROJECT_OVERVIEW.md); [requirements](../00_REQUIREMENTS.md) | KNOWN scope; future robot interface not frozen |
| LM61460 buck architecture selected | Captured U201; [buck review](../evidence/r2/BUCK_DESIGN.md) | KNOWN captured choice; electrical release BLOCKED |
| TPS26630 input electronic-fuse architecture selected | Captured U101; [input review](../evidence/r2/INPUT_PROTECTION.md) | KNOWN captured choice; source/fuse/transient qualification OPEN |
| INA228 + 2 mΩ Kelvin shunt selected | Captured U401/R401; [monitor review](../evidence/r2/MONITOR_POWER_DOMAINS.md) | KNOWN captured choice; measurement accuracy not bench validated |
| Sheet 03 must not be bypassed | [Output review](../evidence/r2/OUTPUT_PROTECTION.md); explicit user constraint | OPEN architectural boundary; preserve legitimate ERC error |
| R2 must close before PCB work | [Manager report](../FINAL_MANAGER_REPORT.md); [gate workflow](05_WORKFLOW_AND_GATES.md) | R2/R3 BLOCKED; R3 requires separate authorization |
| Never fabricate qualification state | [AGENTS.md](../../AGENTS.md); [engineering state](03_ENGINEERING_STATE.md) | Permanent evidence discipline |

## 2026-09-29 — requirements consolidation and Sheet 03 no-go

Authoritative record: [SHEET03_ARCHITECTURE_DECISION.md](../evidence/r2/sheet03/SHEET03_ARCHITECTURE_DECISION.md). Today's conductor D-27/D-30 and protection/Pi/connector branch identities are recorded there; they were inspected, not merged or rewritten.

| Decision / requirement | Rationale and evidence state | Result |
| --- | --- | --- |
| Freeze GPIO 5 V + multiple GND power, normal 9–24 V input, 5 A total envelope and specified Pi/D435i qualification loads | User instruction; D-30 consolidation | REQUIREMENT, not measured capability; supersedes older interface/adapter questions |
| Allocate direct 54.6 V converter pass-through containment upstream | Current user instruction: 13S → PDB → future auxiliary converter → V1A | Responsibility resolved; residual source voltage/current/time/energy bounds and converter MPN remain OPEN |
| Require `V_Pi_peak < 5.5 V` including transients | Current user instruction, tightening the earlier ≤5.5 V wording | Supersedes 6 V screening; detector threshold must leave tolerance and let-through margin |
| Do not select/capture Sheet 03 yet | Native LM74800 window fails the retained 50 mV margin screen; LTC4368 dynamic evidence is inadequate; precision direction lacks a complete bounded circuit/state proof | Architecture gate BLOCKED; conditional capture/commit/push continuation not entered; R2/R3 remain BLOCKED |

## 2026-09-29 — Candidate C Gate 1b

Candidate C is retained as the only review concept: REF5025 + TLV3201 threshold detector, SN74LVC1G74 latch, LTC7001 independent high-side driver, and common-source BSC034N06NS pair. With explicit assumptions and a reproducible script, `V_trip` is 5.325 V nominal / 5.294–5.357 V corner and the normal-release screen leaves +22 mV. The 30 V, 0.5 µH, 2 µs fault screen reaches 5.868 V, failing the Pi limit by 368 mV. The single remaining blocker is `B1_FAULT_INTERRUPTION_ENVELOPE`: authoritative source/inductance bounds and an effective isolation time below 0.385 µs are not evidenced. No KiCad capture is authorized.

Future entries should link to the authoritative dated decision record, include rationale and evidence state, and identify superseded decisions explicitly. Do not copy whole reviews here.
