# Preliminary harness documentation verification

2026-09-29. Scope: authored documents, arithmetic, source identities and preserved hardware; no electrical or retention measurements.

| Check | Result | Meaning |
| --- | --- | --- |
| `python3 -B scripts/check_repository.py` | PASS; 13 hardware files preserved, no errors | Links/JSON and hardware preservation only |
| `python3 -B -m unittest discover -s tests -v` | PASS; 10 existing tests | Existing capture/footprint regressions unchanged |
| `python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/forensic_2026-09-14/V1A_qualified.net.xml` | Capture integrity PASS; R2 RELEASE BLOCKED | Read-only retained-netlist check, not a fresh ERC |
| Independent arithmetic review | PASS; no material findings | Recomputed both polarities, parallel paths, source low, required setpoints and sharing ratio |
| Source identities | PASS | All report source IDs resolve; five cached original PDF byte counts/SHA-256 values match the register. Remote-only sources retain explicit retrieval/revision limits |
| `git diff --check` and staged-path review | PASS | Authored files under `docs/` only; no downloaded vendor bytes or generated caches staged |

**CALCULATED review checkpoints from [budget.json](budget.json):** loop resistance 61.954538484 mΩ, drop 0.309772692 V, low protected source 4.988269402 V, Pi static 4.678496709 V, Pi with assumed reserve 4.578496709 V. These are conditional engineering calculations; their inputs and sources are labelled in the budget. No bench evidence exists.

Reproduction: use the labelled JSON inputs and equations. Compute each wire resistance, parallel branch/contact equivalent and shunt corner; sum `terms_mOhm`; multiply by load current; subtract from the source low after the separate upstream disconnect allowance. The JSON retains full precision. No new software tests were added for the document change.

No KiCad changes were made, so fresh ERC/DRC is not applicable to this documentation change. The existing R2 blockers remain. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
