# Workflow and gates

Requirements → architecture → R2 schematic release → R3 printed circuit board (PCB) release → fabrication release → safe bring-up → characterization → Raspberry Pi integration → research instrumentation.

The repository gate names remain R0 environment/predecessor audit; R1 requirements/architecture; R2 schematic; R3 PCB layout; R4 fabrication-readiness review; R5 physical bring-up/electrical validation. Normally one AI execution session addresses one gate. A repository-maintenance session does not close an electrical gate. Current R2 and R3 are BLOCKED.

Before significant changes, inspect relevant files and instructions, Git status/branch/history, current architecture, affected modules, risks, validation, and rollback. Major architecture changes require explicit approval. Never overwrite existing user work. Preserve source identities and dated evidence; distinguish current decisions from historical alternatives.

After edits, inspect the diff and run targeted checks from [validation](../VALIDATION.md). Electrical Rules Check (ERC) and Design Rules Check (DRC) establish rule-check evidence only, never electrical safety or qualification. Keep the legitimate Sheet 03/U402 condition visible. At each gate end update [the manager report](../FINAL_MANAGER_REPORT.md) with STATUS, WHAT WAS DONE, EVIDENCE, DECISIONS, OPEN RISKS, and NEXT GATE.

Evidence vocabulary: KNOWN = directly established context/source fact; MEASURED = recorded physical observation with method; CALCULATED = derived result with inputs; INFERRED = reasoned conclusion; ASSUMED = provisional input; UNKNOWN = missing information; OPEN = unresolved requirement/choice; BLOCKED = gate cannot advance. Do not promote states without evidence.

Bring-up progression: visual inspection → continuity/short checks → current-limited bench supply → no-load startup → verify output rail → low-current dummy/electronic load → increasing load steps → thermal → ripple → transient/load tests → protection/fault tests → telemetry → single-board computer (SBC) integration only after prior gates pass.

Every future experiment should record goal, hypothesis, hardware/software, input/configuration, commands, metrics, raw results, interpretation, limitations, reproduction steps, and commit hash. Do not claim performance improvements without measurements. Do not place orders or fabricate without explicit reviewed authorization.
