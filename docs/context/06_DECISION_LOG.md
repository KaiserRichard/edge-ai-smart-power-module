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

Future entries should link to the authoritative dated decision record, include rationale and evidence state, and identify superseded decisions explicitly. Do not copy whole reviews here.
