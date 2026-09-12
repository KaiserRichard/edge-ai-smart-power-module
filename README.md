# Smart DC Power Module for Edge AI Devices

Standalone University Project II hardware project: design and validation of a reusable smart DC power module for Edge AI / Edge Computing loads.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Project scope

**V1A (current V1):** DC input → input/reverse-polarity protection → DC/DC conversion → regulated high-current approximately 5-V output → shunt/INA228 or justified alternative → reusable load output, with I2C telemetry and test access.

**V1B:** a separate supercapacitor backup subsystem developed by another team member. It is not part of the current V1A schematic.

**Future V2:** integration of validated V1A and validated V1B, with additional supervision/protection only after review. Interface electrical values remain TBD.

CAN, WBR/robot interfaces, supervisor/watchdog MCUs, HAT/HAT+ form factor and WBR sequencing are not V1A requirements. No USB3/D435i data routing is included. Earlier WBR/HAT research is preserved as future reference.

## Current status and review documents

R0: CONDITIONAL PASS, sufficient for documentary R1. R1: CONDITIONAL PASS for the review package; essential requirements and component selections remain open. **R2 schematic entry: BLOCKED pending manager review and explicit authorization.** No authored schematic, PCB or electrical validation exists.

- [Final manager report](docs/FINAL_MANAGER_REPORT.md)
- [Hardware source pack for ChatGPT/Richard](docs/CODEX_HARDWARE_SOURCE_PACK.md)
- [Requirements: confirmed, proposed and open](docs/00_REQUIREMENTS.md)
- [Reference/provenance audit](docs/01_REFERENCE_AUDIT.md)
- [Architecture recommendation](docs/02_ARCHITECTURE.md)
- [Component-selection review](docs/03_COMPONENT_SELECTION.md)
- [Calculations and future measurement plan](docs/04_POWER_CALCULATIONS.md)
- [Validation evidence](docs/evidence/r0/R0_R1_VALIDATION.md)
- [Session handoff and historical recovery](docs/CODEX_HANDOFF.md)

## Documentary checks

```sh
python3 scripts/check_r0_r1_docs.py
```

Expected: PASS for authored links/JSON, required documents, selected source hashes/licenses and pinned predecessor checkouts. This is documentation integrity evidence, not ERC/DRC or electrical validation. The calculation reproduction command is in the calculations document. No project build is applicable at this gate.

Existing upstream repositories, PDFs and review outputs under `third_party/` remain local research caches; most are ignored by Git. A fresh clone does not restore them. Source URLs, identities, rights and hashes are recorded in the audit/manifest. Missing caches must be reported and restored from the recorded identity when needed; do not replace pins with current upstream HEAD.

## Historical future reference

[WBR Edge Supervisor HAT feasibility](docs/WBR_EDGE_SUPERVISOR_HAT_FEASIBILITY.md) — **FUTURE WBR REFERENCE — NOT PROJECT II V1 REQUIREMENTS**. This preserved study contains incomplete historical evidence references and is not the current product definition.
