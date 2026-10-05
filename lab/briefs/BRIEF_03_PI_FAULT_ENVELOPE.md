You are a Codex worker in the V1A lab. Claude is the conductor and reviews your work before anything reaches GitHub.

Context: V1A is a 9-24 V input, 5.1 V / 5 A power module for a Raspberry Pi 5 (read CLAUDE.md, AGENTS.md and docs/context/03_ENGINEERING_STATE.md first). Requirement P4 is OPEN: we do not know what voltage, for how long, the Pi 5's 5 V input can survive during a fault. 6.0 V is only an ASSUMED screening criterion, not a rating. The output-protection design depends on this.

Objective: find the best available evidence for the Raspberry Pi 5 5 V input fault envelope (voltage versus time), for both entry points: USB-C and the GPIO 5 V header pins.

Do:
1. Search official Raspberry Pi sources first (Pi 5 product brief, power supply documentation, schematics / reduced schematics, forum posts by Raspberry Pi engineers, the PMIC used on the Pi 5). Then the datasheets of the parts that sit directly on the Pi 5's 5 V input: the input protection / load switch, the PMIC (its absolute maximum VIN and transient rating), and any TVS on that rail. Record URL, document revision and date, and SHA-256 for anything you download into third_party/documents/pi5_input/.
2. Build a table: part, its role on the 5 V input, absolute maximum voltage, transient rating (voltage and duration), source and page. Say which part sets the weakest limit.
3. State the resulting envelope as clearly as the evidence allows, labelled KNOWN / INFERRED / ASSUMED / UNKNOWN. Say plainly if no official statement exists.
4. Say whether USB-C and GPIO feeding differ (e.g. whether GPIO bypasses input protection).

Write: docs/evidence/r2/pi5_input_envelope_2026-09-29/PI5_INPUT_FAULT_ENVELOPE.md and source_register.json.

Constraints: work only in this worktree on its local branch. Commit in small commits; do NOT push, open or merge PRs, or run git reset/rebase/clean/stash/force. Do not change anything under hardware/ or any existing file. Do not install software or change system configuration. Download only from official vendor or Raspberry Pi sites; if blocked (HTTP 403), record it and move on. Never invent a rating.

Validation before each commit: python3 -B scripts/check_repository.py and python3 -B -m unittest discover -s tests -v (both must pass).

When finished, write a hand-back: commit list, the envelope in 3-5 lines with labels, the weakest-limit part, sources you could not get. End with the exact line BRIEF-03-HANDBACK.
