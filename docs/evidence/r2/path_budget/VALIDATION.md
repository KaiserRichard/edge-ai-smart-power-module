# V1A path-budget validation and owner status

2026-09-30. Analysis branch `feat/v1a-5a-path-budget`, base `65a86982fc4a48502d3a6da1cd710e796b3d8734`; target `feat/sheet03-gate3-options`. No merge or hardware release.

## Checks and their limits

- **Arithmetic — PASS:** `python3 docs/evidence/r2/path_budget/calculate_path_budget.py --check` reconciles the historical original75.554538 mΩ/reduced55.367741 mΩ cases and checks deterministic saved JSON against recomputation. Raw-hot screen5.026143255 V; recommended D35.072940994 mΩ/E45.072940994 mΩ. At an ASSUMED20 mV trough, CALCULATED Pi4.830778550/4.780778550 V. Actual worst-case minima remain OPEN/null.
- **Independent read-only arithmetic review — PASS:** a separate gpt-6-astra reviewer checked the source reconciliation, temperature/tolerance stack, retained D path plus E stage and numerical results. Root corrected presentation/cost/leg-accounting issues and increased ground fan-outs to35 mm to allow the full-header span; positive fan-outs remain15 mm. The reviewer did not edit files or open CAD.
- **Input identities — PASS:** all eight pinned project documents reproduce the SHA-256 values in INPUT_PROVENANCE.json via their exact git commits. Only `.md`/`.json` inputs were read.
- **Documentation — PASS:** relative Markdown links resolve; resistance table columns are consistent; the OWNER EXPLANATION is427 words (one-page-length briefing); required current-pin list, alternatives, decisions and explicit verdict are present. No hardware measurement or PDF layout is claimed.
- **Scope — PASS:** diff against base contains only new files under `docs/evidence/r2/path_budget/`; no pre-existing design/source document is modified. Native `.kicad_sch`/`.kicad_pcb`/`.kicad_sym` files were never opened, read or saved by root or the read-only reviewers. Git metadata/name inspection is not a CAD-content check.
- **Whitespace — PASS:** `git diff --check 65a86982fc4a48502d3a6da1cd710e796b3d8734` checks the complete branch diff, including the new report. Two trailing spaces caught by the staged check were corrected before PR creation. No external source assets or secrets are committed; primary-document provenance and redistribution boundaries are in SOURCES.md.

These checks validate an analysis artifact, not the hardware. ERC/DRC, circuit simulation, full repository electrical tests and bench tests were not run: this task forbids native CAD access and makes no electrical changes. Ordinary CAD/export tests are outside this analysis scope. No SBC, dummy load or supply was energized. No component purchase, fabrication or deployment was performed.

## Manager-status fields within the permitted scope

**STATUS: BLOCKED for electrical release; requested documentary analysis complete.**

**WHAT WAS DONE:** itemised cold/hot send/return resistance study; original/reduced reconciliation; component and connector primary-source audit; D/E calculations; wire/contact/FET/shunt/sense/setpoint tradeoffs; individual header pin current checks; plain-language owner briefing and decisions.

**EVIDENCE:** PATH_BUDGET.md, PATH_CALCULATIONS.json, calculate_path_budget.py, SOURCES.md, SOURCE_AUDIT.md, INPUT_PROVENANCE.json. Read-only independent review and scope/link/identity/arithmetic checks above.

**DECISIONS:** recommend qualified low-loss Pi mate, both5 V/eight GND pins,75 mm AWG16 trunks with15 mm positive/35 mm ground AWG22 branches,≤6 mΩ hot module FET pair, retained2 mΩ shunt/local setpoint, copper/J502/joint acceptance targets and E added stage≤10 mΩ. Recommendations are not selected/implemented electrical changes.

**OPEN RISKS:** actual Pi male/mated hot current/resistance rating, current sharing/plane spreading, source full-operating bounds/feedback TCR, loaded gate drive/hot FET resistance, real copper/harness/termination losses, added-stage/auxiliary consumption, ripple/transient envelope and all existing fault-containment qualification. D has only0.779 mV under the assumed100 mV excursion; E fails that screen by49.221 mV.

**NEXT GATE:** owner/component/interface decisions and continued R2 electrical qualification. Do not advance to PCB/fabrication merely because the conditional DC arithmetic is positive. Follow current-limited/dummy-load staged bring-up before Pi integration.

The user restricts new files to this directory; therefore these fields are recorded here instead of editing docs/FINAL_MANAGER_REPORT.md. Commits are focused and pushed after completed sub-steps; the final PR is draft into the requested architecture-options branch, with no merge.
