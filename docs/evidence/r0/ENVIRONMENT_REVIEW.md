# R0 environment review

Date: 2026-09-11. Owner: Richard. Execution scope: R0 and R1 only.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Baseline and scope

- OBSERVATION: Initial branch `main`, initial commit `a9fe716` (`chore: initialize edge AI smart power module project`). Only README and AGENTS were tracked. No authored schematic, PCB, firmware or monitor software existed.
- OBSERVATION: `AGENTS.md` was already modified by the user: populated from an empty tracked file. It is preserved unchanged by this mission.
- DECISION: Work on `docs/r0-r1-engineering-audit`. No commit or push authorized or performed.
- DECISION: Add documentation, isolated reference checkouts and small reproducible calculation tooling. No hardware interface is implemented or frozen. Rollback can remove mission additions and restore only the README; never reset the user's AGENTS change.

## Observed tools

Full command output and return codes: [environment.json](environment.json).

| Item | Observed result | Consequence |
| --- | --- | --- |
| OS | macOS 15.7.9, build 24G830 | Local workstation audit only |
| KiCad | 9.0.6 | Standard KiCad 9 project files proposed for R2 |
| CLI | `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` | Use explicit path; no PATH/system configuration changes |
| Git | 2.52.0 | Detached upstream checkouts, separately pinned |
| Default Python | 3.11.0rc2 | Prerelease interpreter observed; calculation checks must record it; use a stable interpreter for future runtime development |
| ERC | `sch erc`, report/JSON, severity and nonzero violation exit flags | Available, not run against a V1 schematic because none exists |
| DRC/parity | `pcb drc --schematic-parity` | Available, not run against a V1 PCB because none exists |
| Schematic exports | BOM, netlist, PDF, SVG and other formats | Help verified; V1 export not tested |
| PCB exports | Gerbers, drill, placement, PDF/SVG, STEP and other formats; `pcb render` | Help verified; V1 fabrication export not tested |
| PDF tools | No Poppler binaries or PDF Python packages on initial PATH/interpreter | Read-only PDF rendering uses ignored local tooling; no global install |

Local root `.venv` contains PyMuPDF 1.28.2 for PDF extraction/rendering. The predecessor reviewer also used an isolated ignored review environment; details are in the reference audit. These are review aids, not a KiCad automation framework. Python urllib failed TLS certificate verification using the default interpreter; downloads used `curl` with normal certificate verification. Raspberry Pi HTML download returned HTTP 403, so official web reads and pinned source files were used. Neither failure was bypassed by disabling TLS.

## Reproduce capability checks

```sh
KICAD_CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
"$KICAD_CLI" version
"$KICAD_CLI" sch erc --help
"$KICAD_CLI" pcb drc --help
"$KICAD_CLI" sch export --help
"$KICAD_CLI" pcb export --help
```

Expected: version `9.0.6`, help exits zero, DRC help includes `--schematic-parity`. Failure symptoms: missing executable, loader errors, or absent flags. These checks demonstrate CLI availability, not that a future project will pass checks.

## Gate limitations

No electrical tests, hardware measurements, V1 ERC/DRC, footprint validation, or fabrication outputs exist. KiCad GUI interaction and 3D export dependencies remain untested. R2 must verify actual symbol/footprint availability and successful project loading. An ERC/DRC pass will be rule-check evidence only.
