# Claude Project knowledge selection

In Claude, open the Project → add content / Add from GitHub, authorize access to `KaiserRichard/edge-ai-smart-power-module`, and select **`feat/r2-schematic-recovery`**. The repository remains private and `main` still represents older work. Select this branch explicitly. The connector imports selected files/folders on a specific branch; refresh the GitHub sync after later updates. See [Claude's official integration guide](https://support.claude.com/en/articles/10167454-use-the-github-integration), checked 2026-09-26.

## Compact starting selection

Select these exact paths first:

```text
CLAUDE.md
AGENTS.md
README.md
docs/context/
docs/FINAL_MANAGER_REPORT.md
docs/VALIDATION.md
docs/evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md
```

Read the context files before the historical manager entries. Paste this short instruction into the Project instructions: “Read CLAUDE.md and docs/context/03_ENGINEERING_STATE.md first. Communicate in English. R2/R3 remain BLOCKED; Sheet 03 is OPEN. Preserve evidence states. Address one gate per session and obtain approval before architecture changes.” Do not assume that a file imported as knowledge is automatically treated as a system instruction.

## Current engineering files for design-review sessions

Select these source files if the connector accepts their KiCad extensions:

```text
hardware/kicad/V1A.kicad_pro
hardware/kicad/V1A.kicad_sch
hardware/kicad/01_INPUT_PROTECTION.kicad_sch
hardware/kicad/02_BUCK_5V.kicad_sch
hardware/kicad/03_OUTPUT_PROTECTION.kicad_sch
hardware/kicad/04_POWER_MONITOR.kicad_sch
hardware/kicad/05_IO_TEST.kicad_sch
hardware/kicad/V1A.kicad_sym
hardware/kicad/fp-lib-table
hardware/kicad/sym-lib-table
hardware/kicad/V1A_Qualified.pretty/
```

If a source extension is unsupported, retain the source in Git and select the text evidence below for that session; do not rename or rewrite authoritative KiCad files for ingestion. A connector import does not establish that Claude can parse or visually inspect a schematic.

```text
docs/05_SCHEMATIC_REVIEW.md
docs/evidence/r2/INPUT_PROTECTION.md
docs/evidence/r2/BUCK_DESIGN.md
docs/evidence/r2/OUTPUT_PROTECTION.md
docs/evidence/r2/MONITOR_POWER_DOMAINS.md
docs/evidence/r2/forensic_2026-09-14/CRITICAL_FOOTPRINT_QUALIFICATION.md
docs/evidence/r2/forensic_2026-09-14/BOM_QUALIFIED_REVIEW.md
docs/evidence/r2/forensic_2026-09-14/V1A_qualified.net.xml
docs/evidence/r2/forensic_2026-09-14/qualification_source_register.json
third_party/README.md
```

Add `scripts/`, `tests/`, calculation JSON/configurations, and specific numbered core documents only when the session needs them. The core documents preserve earlier proposals; current context explains superseding selections.

Do not initially select all `docs/evidence/`, dated schematic PDFs, SVG review images, logs, old netlists, or `third_party/wbr_hat/`. Those remain available for focused provenance work. Archived caches/backups and full third-party repositories are intentionally absent from GitHub. After syncing, ask Claude to identify the branch, the two blocked releases, the separate output nets, and the legitimate U402 condition before assigning engineering work.
