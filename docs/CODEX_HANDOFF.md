> Context note (2026-09-26): this dated document preserves earlier requirements/review history. Read [current engineering state](context/03_ENGINEERING_STATE.md) and [current architecture](context/02_V1A_ARCHITECTURE.md) before interpreting selections or release claims. Local cache/scratch paths mentioned below are archived external evidence; see [reference restoration](../third_party/README.md).

# Codex handoff — 2026-09-11

## Current mission addendum — scope correction and R0/R1 consolidation

The user explicitly corrected the primary objective to **standalone Project II V1A Smart DC Power Module**. V1B is the teammate's separate supercapacitor subsystem; future V2 integrates both after validation. WBR/HAT/CAN/supervisor work is future reference only. The historical recovery below remains intact; its instruction to finish WBR CAN/Linux reviews is superseded for the current mission.

Current deliverables are the seven R0/R1 documents linked from [README](../README.md), the source manifest and validation evidence. R0 is CONDITIONAL PASS for supporting R1; R1 is CONDITIONAL PASS as a documentary review package; R2 remains BLOCKED. No hardware was implemented, no component/requirement was frozen, and no commit/push occurred.

Next action: send [FINAL_MANAGER_REPORT.md](FINAL_MANAGER_REPORT.md) and [CODEX_HARDWARE_SOURCE_PACK.md](CODEX_HARDWARE_SOURCE_PACK.md) for the user's technical review. Then resolve source/input limits, output/current/thermal acceptance and complete component/protection/interface choices before asking for R2 authorization. Do not resume the old WBR implementation path or design the teammate's supercapacitor circuit.

Created: `00_REQUIREMENTS.md`, `01_REFERENCE_AUDIT.md`, `02_ARCHITECTURE.md`, `03_COMPONENT_SELECTION.md`, `04_POWER_CALCULATIONS.md`, `CODEX_HARDWARE_SOURCE_PACK.md`, `FINAL_MANAGER_REPORT.md`, R0 source/validation records and `scripts/check_r0_r1_docs.py`. Updated navigation/scope in README, this handoff, the WBR feasibility report and its Pi power/watchdog review. Existing R0 reports/manifests, AGENTS user changes and upstream caches were preserved. Exact validation commands/results and limitations are in [R0_R1_VALIDATION.md](evidence/r0/R0_R1_VALIDATION.md).

## Historical handoff retained below

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Objective and stopping point

Preserve the existing R0/R1 engineering investigation and finish its missing documentation before any schematic implementation. The latest recoverable task is a documentary feasibility study for a WBR Edge Supervisor HAT using Raspberry Pi 5, direct-USB3 D435i, CAN-FD, power monitoring and independent shutdown/recovery supervision.

This session reconstructed local state and created only this handoff. The user explicitly requested no implementation after writing it. No commit, push, architecture approval, hardware configuration or gate advancement occurred.

## Original task and current gate

The exact earlier conversation is unavailable; this reconstruction is based on files and Git, not a verbatim recovery of the original prompt.

- Original repository objective: standalone Project II Smart DC Power Module, with DC input protection, regulated high-current 5 V, voltage/current/power/energy monitoring and I2C telemetry.
- Earlier mission: R0 environment/predecessor audit and R1 requirements/architecture recommendations. `docs/evidence/r0/ENVIRONMENT_REVIEW.md` explicitly limits execution to R0/R1.
- Latest task: WBR HAT feasibility and a hardware source pack, inferred from `docs/WBR_EDGE_SUPERVISOR_HAT_FEASIBILITY.md`. The source pack is absent despite the report claiming both deliverables exist.
- **Current gate: R0/R1 documentation and proposal review, with incomplete R0 consolidation.** The feasibility report says CONDITIONAL PASS for the proposal and R2 BLOCKED. No manager gate record or approval exists locally. Do not interpret its conclusion as completion of all R0/R1 deliverables.

## Architecture recovered

No project-authored schematic, PCB, firmware, runtime software, tests or measurement results were found. Hardware/fabrication directory scaffolding is not implemented hardware. Third-party CAD and exports are reference material only.

The standalone module concept is input protection → high-current converter → independently justified output protection → Kelvin shunt/load output, with INA228 and a protected local telemetry supply. Earlier 9–28 V input, 5.1 V/5 A output and 6 A peak examples remain proposals, not frozen requirements.

The separate WBR proposal is external regulated nominal 5 V/5 A → protected reverse-blocking switched Pi branch → shunt → Pi header. An upstream supervisor remains powered while the Pi branch is off; CAN-FD uses SPI and the camera connects directly to Pi USB3. This does not replace the standalone project. Package/interface/state ownership changes require architectural approval before implementation.

## Completed work and existing files

Read all existing authored Markdown reports and inspected the JSON evidence structure in this session. Existing work comprises:

| Path | Recovered content/status |
| --- | --- |
| `AGENTS.md` | User-populated engineering rules; tracked file modified from an empty baseline. Preserve. |
| `README.md` | Tracked, unchanged; standalone V1 scope and early-research status. |
| `.gitignore` | Untracked; ignores reference repositories/documents/review caches, local environments, transient files and secrets. |
| `docs/evidence/r0/ENVIRONMENT_REVIEW.md` | Environment, CLI capabilities, scope and limitations. |
| `docs/evidence/r0/environment.json` | Recorded command outputs and exit codes. |
| `docs/evidence/r0/RASPBERRY_PI_SOURCE_REVIEW.md` | Official Pi power/HAT reference findings. |
| `docs/evidence/r0/raspberry_pi_sources.json` | Five source records; URLs/cache identity and retrieval evidence. |
| `docs/evidence/r0/MONITOR_PROTECTION_SOURCE_REVIEW.md` | INA228/INA226, shunt calculations, calibration, protection and unresolved design constraints. |
| `docs/WBR_EDGE_SUPERVISOR_HAT_FEASIBILITY.md` | Broad feasibility proposal, GPIO budget, power/CAN/supervisor concepts, test plan and R2 entry conditions; incomplete supporting links. |
| `docs/evidence/wbr_hat/PI_POWER_WATCHDOG_REVIEW.md` | Pinned Pi sources, power domains, GPIO shutdown and watchdog analysis. |
| `docs/evidence/wbr_hat/power_source_manifest.json` | Seven source records. |
| `third_party/wbr_hat/raspberry_pi/` | Untracked pinned documentation/kernel source files and license notices, including `rpi-6.18.y/`. |
| `docs/CODEX_HANDOFF.md` | The only file created by this recovery session. |

All existing `docs/` files above were untracked at recovery. No other existing files were edited.

Ignored local material is also valuable evidence: `third_party/repos/`, `third_party/documents/`, `third_party/review/`, `.venv/`, and `tmp/pdfs/`. Review caches include predecessor PDF/SVG/PNG/text exports and WBR CAN/Linux reference artifacts. Preserve them; their presence alone does not prove complete review or validation. They will not accompany a normal Git checkout.

## Git snapshot

- Branch: `docs/r0-r1-engineering-audit`.
- HEAD and sole commit: `a9fe716` — `chore: initialize edge AI smart power module project`.
- Only `AGENTS.md` and `README.md` are tracked at baseline.
- Existing tracked diff: `AGENTS.md`, 183 added lines. No staged changes.
- Untracked groups before this handoff: `.gitignore`, the eight existing files under `docs/`, and `third_party/wbr_hat/raspberry_pi/` source files.
- No commit/push authorized. Do not reset, clean, overwrite or automatically stage this working tree.

Read-only checkout inspection found clean predecessor worktrees:

| Repository | Exact local HEAD |
| --- | --- |
| `https://github.com/wilsondr9999/1026-RPi-Power-Hat.git` | `7af0c4d3cd5b66c6948879393b34898937d37348` |
| `https://github.com/hatlabs/SH-RPi-hardware.git` | `e82e3c9823bbcf94091b22927dd2e0da9cdfac8c` |
| `https://github.com/sbcshop/UPS-Hat-RPi.git` | `14926b39f14ee541c9e5aa879d2b654a4e4605ad` |

These pins identify cached sources, not approval to reuse circuits or proof that the missing predecessor audit is complete.

## Commands and checks already run

Historical evidence in `environment.json` records successful `sw_vers`, `git --version`, KiCad `version`, top-level `--help`, `sch --help`, `sch erc --help`, `sch export --help`, `pcb --help`, `pcb drc --help`, and `pcb export --help`.

- Recorded environment: macOS 15.7.9, Git 2.52.0, Python 3.11.0rc2, KiCad 9.0.6.
- CLI path: `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`; not found on the initial PATH.
- Existing review notes report PyMuPDF 1.28.2 in local `.venv`, PDF extraction and selected visual inspections. These were not rerun during recovery.
- Predecessor `pdf-export.log` files end in successful plotting for 1026 and Sailor Hat, with Fontconfig warnings. Exact original invocation/exit status is not established by those logs alone.
- Prior Python HTTPS certificate errors and HTTP 403 responses are documented. Prior downloads used normal verified-TLS curl; do not disable TLS checks or repeat failed URLs without examining existing evidence.
- No project ERC/DRC, build, electrical test, Pi configuration, CAN test or workload benchmark has been executed according to the available record. Report code blocks are proposed procedures, not execution logs.

Recovery checks: `git status --short` (including full untracked listing), `git branch --show-current`, `git log --oneline -8`, `git diff`, `git diff --stat`, `git diff --cached --stat`, `git ls-files`, file inventories with `rg`/`find`, all existing report reads, JSON parse checks, local Markdown-link existence checks, and predecessor `rev-parse HEAD`, `remote get-url origin`, `status --short`.

JSON files parsed successfully. Link checks found three distinct missing WBR report targets listed below. No external source verification or numerical recalculation was performed in recovery; engineering statements below summarize the existing reports.

## Important decisions and proposal boundaries

Established repository constraints: keep standalone V1 separate; never assume WBR battery voltage; do not route USB3/D435i data on this PCB; use sequential gates and manufacturer evidence; no fabrication or expensive SBC first-load testing.

Recorded WBR proposals, **not approved design selections**:

- External 5 V/5 A input; no onboard battery conversion or energy store. Budget total Pi/camera/cooling/HAT consumption against the source.
- No guaranteed graceful shutdown on abrupt source loss without verified hold-up. USB-C coexistence bypasses the HAT's cutoff authority; detect remaining rail voltage and enter EXTERNAL_POWER.
- Independent upstream supervisor owns switch/recovery; Linux owns orderly shutdown and final ACK. Robot motion safety stays independent.
- INA228 with four-terminal 2 mΩ `WSL27262L000FEA` candidate; load-side VBUS measures delivered branch, not total system efficiency or total Pi consumption under alternate supply.
- INA226 is a fallback; monitor/kernel compatibility and single software ownership must be resolved. Calibration, reset/rollover and data gaps require validation.
- MCP2518FD, proposed 40 MHz clock and initial 10 MHz SPI; MCP2562FD leading transceiver, TCAN3413 alternative. CAN topology/isolation are not frozen.
- Standard HAT+ EEPROM class at 0x50 proposed; power-only classes cannot cover the GPIO functions. Call it a HAT-form-factor engineering board until conformance is established.
- Local 3.3 V must not be tied to Pi 3.3 V. All off-state signal crossings require explicit analysis.
- Native standby and external GPIO-controlled cutoff are separate modes. Configuration examples were not applied.
- Integrated eFuse versus lower-resistance external-FET power path is unresolved. No exact protection thresholds, connector system, final GPIO interface, timeout policy or BOM is approved.

## Unfinished work, inconsistencies and blockers

Requested baseline files are **absent**, not merely unread:

- `docs/FINAL_MANAGER_REPORT.md`
- `docs/00_REQUIREMENTS.md`
- `docs/01_REFERENCE_AUDIT.md`

The feasibility report links to absent deliverables:

- `docs/CODEX_HARDWARE_SOURCE_PACK.md`
- `docs/evidence/wbr_hat/CAN_HARDWARE_REVIEW.md`
- `docs/evidence/wbr_hat/LINUX_CAN_HAT_REVIEW.md`

Its statement that both requested documents/supporting evidence are delivered is not supported by the local inventory. The monitor report also mentions a root source manifest without an identifiable root manifest present. Do not invent its filename or assume complete provenance. The environment report mentions planned calculation tooling; no authored calculation scripts or tests were found. README was not modified despite the historical rollback text referring to restoring it.

Engineering blockers include source tolerance/fault/surge envelope; total voltage-drop and thermal budget; continuous/peak load and acceptance limits; independent OVP threshold/let-through coordination; off-state/backfeed behavior; USB-C cutoff limitations; CAN harness/ground/isolation; target OS/kernel/overlay and INA228 support; supervisor/ACK/retry ownership and timing; connector current ratings and cooler fit; calibration/accuracy targets. No measured performance or safety evidence exists.

Portability risk: Git alone currently preserves almost none of the investigation. Switching accounts on this same workspace retains local files; a fresh clone does not retain untracked reports or ignored source caches. Preserve the working directory through an explicitly authorized transfer if changing machines. Do not solve this by silently committing, uploading large caches or redistributing manufacturer PDFs.

## Exact next steps for the next authorized session

1. Read this handoff and AGENTS; inspect Git status/branch/log and changes since this snapshot. Preserve concurrent user work. Do not rerun the completed environment audit unless the environment changed.
2. Resume the missing documentary consolidation first. Search existing local caches for the missing CAN/Linux/predecessor/source-pack material and recover source pins, licenses, actual inspected files and export evidence. Reuse preserved sources/renders; only repeat inspections needed to substantiate missing claims. Do not fabricate prior execution history.
3. Complete the missing supporting reviews/source pack and reconcile the feasibility report's broken links and completion statement with actual evidence. Record referenced/adapted/copied status and attribution per source. Keep historical R0 assumptions explicitly separate from WBR requirements.
4. Create the missing requirements/reference-audit/manager records from verified evidence. Mark unspecified electrical requirements OPEN. Record gate status, work, evidence, decisions, risks and next gate honestly; do not award an unsupported PASS. Update README navigation/status as appropriate. This is documentation consolidation, not approval of a replacement architecture.
5. Prepare a concrete R1 review package covering the unresolved requirements and component/power-domain/state-ownership choices. Obtain architectural approval before implementing any interface, schematic or firmware. If standalone versus WBR implementation priority is still unclear, resolve it at that review.
6. Only after R1 approval and R2 entry conditions close, begin schematic work with verified symbols/footprints/ratings and an ERC/test plan. Continue R3–R5 sequentially, with dummy-load bring-up before SBC integration.

For documentation verification, parse manifests, check relative links and confirm every completion claim against actual files/logs. Expected result: no unexplained missing evidence targets and no claim that proposals are validated. Broken links, missing pins/licenses, or unsupported PASS statements are failures to resolve. Electrical checks belong to later authorized gates; none is needed to validate this handoff.

## Preservation and rollback

Do not repeat completed source downloads, environment checks or reference exports by default. Do not overwrite original reports/manifests, upstream checkouts, cached originals or historical renders to conceal gaps; add traceable corrections. Do not reinterpret candidate numbers as requirements or illustrative shell commands as completed tests.

This session's change is one additive Markdown handoff; rollback is limited to removing this newly created file if explicitly desired. No existing project evidence needs restoration. Stop here for the requested session/account switch.
