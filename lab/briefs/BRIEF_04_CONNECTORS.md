You are a Codex worker in the V1A lab. Claude is the conductor and reviews your work before anything reaches GitHub.

Context: V1A is a 9-24 V input, 5.1 V / 5 A power module for a Raspberry Pi 5 (read CLAUDE.md, AGENTS.md, docs/context/03_ENGINEERING_STATE.md and docs/evidence/r2/forensic_2026-09-14/CONNECTOR_HARNESS_QUALIFICATION.md first). Connectors J501 (DC input: 1=VIN_RAW, 2=GND), J502 (5.1 V / 5 A output: 1=LOAD_5V1, 2=GND) and J503 (I2C: 1 GND, 2 3V3_HOST, 3 SDA_HOST, 4 SCL_HOST) have no part chosen. The user's brother will review connectors and may add ports, so the goal is a clear shortlist for that review, not a selection.

Objective: a connector shortlist for J501, J502 and J503.

Do, for each connector, 2-3 candidates (build on the existing JST VH / Phoenix / JST XH / PH shortlists; add better ones if justified):
- exact MPN of header and mating housing / crimp contacts, manufacturer datasheet link
- current rating per contact at temperature, voltage rating, contact resistance, wire gauge range
- pitch, footprint size, polarisation / keying, retention (latch), mating cycles
- mis-mating risk between J501 and J502 (they must not be interchangeable), and hot-plug suitability
- for J502: the full 5 A path including a 6 A / 100 ms peak, and the voltage drop contribution
- whether a KiCad standard footprint and 3D model exist (library name) or must be made
Finish with a comparison table and a recommended default per connector, clearly marked RECOMMENDATION FOR REVIEW, with the reason.

Write: docs/evidence/r2/connectors_2026-09-29/CONNECTOR_SHORTLIST.md and source_register.json.

Constraints: work only in this worktree on its local branch. Commit in small commits; do NOT push, open or merge PRs, or run git reset/rebase/clean/stash/force. Do not change anything under hardware/ or any existing file. Do not install software or change system configuration. Download only from manufacturer or distributor sites; if blocked (HTTP 403), record it and move on. No purchasing. Never invent a rating.

Validation before each commit: python3 -B scripts/check_repository.py and python3 -B -m unittest discover -s tests -v (both must pass).

When finished, write a hand-back: commit list, the recommended default per connector in one line each, open questions for the brother's review, sources you could not get. End with the exact line BRIEF-04-HANDBACK.
