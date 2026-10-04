# Edge AI Smart Power Module V1A

A standalone Project II compute-power module for Raspberry Pi 5 / Edge Artificial Intelligence (AI): **9–24 V-class input → input protection → LM61460 synchronous buck → approximately 5.1 V / 5 A target → independent output protection → 2 mΩ Kelvin shunt + INA228 monitoring → load**.

**R2 schematic release BLOCKED. R3 printed circuit board (PCB) release BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

The five-sheet schematic exists. Sheet 03 output protection remains OPEN: `VOUT_5V1` and `VOUT_PROTECTED` are electrically separate. The U402 undriven-power Electrical Rules Check (ERC) error is expected. No PCB is authorized; no hardware performance is validated by repository checks.

V1A is not the complete Wheel-Biped Robot (WBR) power distribution board. A future approximately 48 V battery system requires main protection and auxiliary conversion upstream of V1A; it is not V1A's direct input specification.

## Start here

- [Current engineering state and blockers](docs/context/03_ENGINEERING_STATE.md)
- [Project overview](docs/context/01_PROJECT_OVERVIEW.md) and [current architecture](docs/context/02_V1A_ARCHITECTURE.md)
- [Workflow/gates](docs/context/05_WORKFLOW_AND_GATES.md), [decision index](docs/context/06_DECISION_LOG.md), and [learning sequence](docs/context/04_LEARNING_CURRICULUM.md)
- [Manager report](docs/FINAL_MANAGER_REPORT.md) and [detailed blocker evidence](docs/evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md)
- [AI instructions](CLAUDE.md), [repository rules](AGENTS.md), and [Claude Project file selection](docs/CLAUDE_PROJECT_SETUP.md)

## Repository layout

| Path | Contents |
| --- | --- |
| `hardware/kicad/` | Current project, root/five functional schematics, custom symbols, three project footprints, library tables |
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
python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/forensic_2026-09-14/V1A_qualified.net.xml
python3 -B scripts/calculate_r2.py
```

These commands check repository/capture integrity and reproduce calculations, not electrical release. No software build is currently required. [Validation instructions](docs/VALIDATION.md) include fresh KiCad export/ERC commands, expected failure symptoms, and optional tools. Do not run the schematic builder as a check: it writes design files.

Vendor downloads, full predecessor repositories, backups, environments, and scratch renders were preserved in a sibling local archive. They are not restored by cloning GitHub. [Third-party policy/restoration](third_party/README.md) and the [cleanup record](docs/REPOSITORY_CLEANUP.md) explain dependencies and recovery. Historical engineering evidence remains in Git.
