# Edge AI Smart Power Module — V1A-Lite

This branch (`feat/v1a-lite-cost-reduction`) captures **V1A-Lite option 1R**: 18–26 V normal auxiliary input (24 V nominal) → reverse protection and latched input cutoff → LM61460 → raw-node SCR crowbar → 7 A wiring fuse → Pi power output. The 100k/24.6k feedback divider sets 5.065 V nominal; 5 A operation remains a qualification target. Telemetry and the series shunt are removed.

**Phase D capture: ERC 0 errors / 0 warnings. Electrical release remains BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** No Pi until dummy-load and OV/crowbar qualification gates pass.

Read the [Phase D capture and open items](docs/evidence/v1a_lite/PHASE_D_CAPTURE.md), [five-page schematic PDF](docs/schematic/V1A_Lite_schematic.pdf), [BOM](docs/evidence/v1a_lite/V1A_LITE_BOM.csv), and [progress/handoff](docs/evidence/v1a_lite/PHASE_D_PROGRESS.md). The schematic has root plus Sheets 01, 02, 03 and 05.

The old research design is preserved on **`v1a-research-schematic`** and **`v1a-research-layout-wip`**. The existing `V1A.kicad_pcb` is unchanged historical research layout, **not a V1A-Lite board**. Older context and architecture documents below describe research V1A unless explicitly identified as Lite; its 9–24 V/I2C architecture does not govern this branch. No final WBR battery or robot architecture is assumed.

## Start here

- [Current engineering state and blockers](docs/context/03_ENGINEERING_STATE.md)
- [Project overview](docs/context/01_PROJECT_OVERVIEW.md) and [current architecture](docs/context/02_V1A_ARCHITECTURE.md)
- [Workflow/gates](docs/context/05_WORKFLOW_AND_GATES.md), [decision index](docs/context/06_DECISION_LOG.md), and [learning sequence](docs/context/04_LEARNING_CURRICULUM.md)
- [Manager report](docs/FINAL_MANAGER_REPORT.md) and [detailed blocker evidence](docs/evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md)
- [AI instructions](CLAUDE.md), [repository rules](AGENTS.md), and [Claude Project file selection](docs/CLAUDE_PROJECT_SETUP.md)

## Repository layout

| Path | Contents |
| --- | --- |
| `hardware/kicad/` | Lite root/four functional schematics and libraries; unchanged historical research PCB |
| `docs/context/` | Compact current project context; read before dated proposals |
| `docs/00_…05_*.md` | Requirements and design/review history; dated notices identify older state |
| `docs/evidence/` | Engineering provenance, calculations, contracts, source registers, dated netlists/ERC/review exports |
| `scripts/`, `tests/` | Calculation, capture, footprint, and repository checks |
| `software/power_monitor/` | Documented future telemetry work; no runtime implementation yet |
| `measurements/`, `fabrication/` | Documented future gated evidence/release areas |
| `third_party/` | Source registry, retained download manifest, small licensed historical reference extracts |

## Safe validation

From the repository root, with Python 3.11 or compatible Python 3:

```sh
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_v1a_lite.py
```

These commands check Lite capture integrity and retained historical regressions, not electrical release. The repository runner selects the Lite profile; incompatible research architecture suites are explicitly skipped. No software build is currently required. [Validation instructions](docs/VALIDATION.md) include fresh KiCad export/ERC commands, expected failure symptoms, and optional tools. Do not run the schematic builder as a check: it writes design files.

Vendor downloads, full predecessor repositories, backups, environments, and scratch renders were preserved in a sibling local archive. They are not restored by cloning GitHub. [Third-party policy/restoration](third_party/README.md) and the [cleanup record](docs/REPOSITORY_CLEANUP.md) explain dependencies and recovery. Historical engineering evidence remains in Git.
