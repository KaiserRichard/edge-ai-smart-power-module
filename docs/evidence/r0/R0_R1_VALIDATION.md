# R0/R1 documentary validation — V1A

Date: 2026-09-11. Scope: authored documentation, recorded source identity and arithmetic. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Checks and evidence

The current review uses baseline commit `a9fe716` plus uncommitted R0/R1 files on `docs/r0-r1-engineering-audit`. No hardware build is applicable. Existing KiCad capability outputs in [environment.json](environment.json) were reused; no project schematic/PCB exists on which to run ERC/DRC.

| Check | Command / method | Evidence and acceptance |
| --- | --- | --- |
| Initial Git state | `git status --short`, `git branch --show-current`, `git log --oneline -5`, `git diff`, `git diff --cached` | Existing AGENTS modification and untracked documentation/caches identified before editing; no staged changes |
| Source identity | Local `git rev-parse HEAD`, `git cat-file`, `git remote get-url origin`, `git status --porcelain`; SHA-256 of selected files/licenses | Three exact predecessor pins in [source manifest](source_manifest.json); upstream worktrees must remain clean |
| Historical preservation | SHA-256 baseline of 687 existing documentation/reference files, excluding Git/venv/cache internals | Only the announced README/handoff/WBR scope annotations may differ. Existing R0 reports/manifests, AGENTS, upstream sources and historical renders must be unchanged |
| PDF/reference review | Reused predecessor text/renders; PyMuPDF extracted converter/reference pages; selected images inspected | New review renders under ignored `tmp/pdfs/v1a-r0-review/`; original PDFs untouched. Review is selected-page inspection, not complete PCB validation |
| Manufacturer verification | Official TI/Richtek/ADI/Eaton sources accessed; cached datasheets/EVMs reused | Revisions/pages and remote-only limitations recorded; no exact stock or unmeasured efficiency claim |
| Authored links / JSON / hashes / pins | `python3 scripts/check_r0_r1_docs.py` | Exit zero and PASS required; missing files, headings, digests or pin mismatches fail |
| Calculation reproduction | Execute the Python block under [power calculations](../../04_POWER_CALCULATIONS.md#reproduction-and-later-measurements) | Expected 24-V result: ripple 2.399 A, peak 6.199 A, RMS 5.048 A; shunt scaling check PASS |
| Final change review | `git diff --check`, `git diff --stat`, `git status --short --untracked-files=all`; manual new-document review | No whitespace errors, unauthorized hardware edits, deletion, staged change, commit or push |

The final checker snapshot is saved as `docs/evidence/r0/documentation_validation.json`. It records its actual counts/results; it does not overwrite earlier experiment or source records. To obtain a fresh report, choose a new filename or omit `--report` to print results. The checker refuses to overwrite an existing report.

## Executed results

The documentary checker and calculation reproduction both exited **0 / PASS**. At the pre-report snapshot, 16 authored Markdown files, 66 relative links, five JSON inputs, 58 hashed source records and three predecessor pins passed. The generated validation JSON is an additional JSON file, so later runs can report a higher JSON count without any source change.

The 687-file preservation comparison found **zero missing files**. Exactly four existing files changed: `README.md`, `docs/CODEX_HANDOFF.md`, `docs/WBR_EDGE_SUPERVISOR_HAT_FEASIBILITY.md`, and `docs/evidence/wbr_hat/PI_POWER_WATCHDOG_REVIEW.md`. These are the announced scope/navigation annotations; original R0 evidence and upstream files were unchanged. Native predecessor component fields and four-copper-layer declarations were also checked read-only. `git diff --check` and an authored-file trailing-whitespace scan passed.

One supplementary one-off component-inventory command initially had a Python syntax typo; the corrected read-only command exited zero. It made no file changes and did not affect the passing documentation checker or arithmetic reproduction.

## Manual completion review

- All seven requested review documents contain substantive requirements, sources, tradeoffs, calculations or manager decisions.
- README and current handoff identify standalone V1A as primary. The original handoff remains below a dated addendum. WBR feasibility and Pi watchdog evidence carry the requested future-reference label.
- Unavailable historical CAN/Linux review links are now explicit unavailable filenames, with a correction explaining the original completion claims. No placeholder CAN reports were created.
- Confirmed/proposed/open status is separated; the eleven V1A–V1B interface categories remain TBD; no supervisor/CAN/HAT requirement is introduced into V1A.
- R0 supports documentary R1, R1 is a proposal package, and R2 stays BLOCKED. The manager report identifies actual deliverables and the remaining electrical decisions.

## Limits and failure handling

The checker covers authored root/docs Markdown links, including local heading anchors, not links inside third-party repositories or online URL availability. It parses all authored JSON and the preserved converter download manifest. Duplicate records across manifests are independently hashed; failed historical downloads remain failure records, not missing local files presented as successful downloads.

Three predecessor Git objects and clean worktrees are checked locally. Pi documentation/legacy pins are exact raw-URL identities with cached file hashes; full local Pi repository objects are not available. Remote-only manufacturer sources have revision/section records but no local digest. Manufacturer rights notices are recorded, not legally certified for future reuse.

Local caching attempts for LTC3350/Eaton returned curl code 92 (HTTP/2); official PDFs were instead read remotely. Earlier converter size-limit and Python TLS errors remain documented. No TLS bypass or global system/tooling changes were used.

PASS means documentary integrity within this scope. It does not prove an equation's complete physical model, correct circuit behavior, component availability, thermal capacity or electrical safety. If caches are missing on another account/machine, preserve remaining files and restore only the recorded source identities; do not change the manifest merely to make the check pass.
