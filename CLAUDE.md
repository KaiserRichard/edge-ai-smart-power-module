# V1A agent context

- Communicate in English unless the user explicitly requests another language. Expand abbreviations on first use. Explain design-review reasoning; do not delegate understanding away from the user.
- Read [AGENTS.md](AGENTS.md), [context](docs/context/01_PROJECT_OVERVIEW.md), and [current engineering state](docs/context/03_ENGINEERING_STATE.md) before work. Inspect relevant source files, Git status, branch, and recent commits before edits.
- V1A is a standalone 9–24 V-class input, approximately 5.1 V / 5 A compute-power module for Raspberry Pi 5 / Edge AI. It is not the complete Wheel-Biped Robot power distribution board.
- **R2 schematic release BLOCKED; R3 PCB release BLOCKED. Sheet 03 output protection is OPEN. No PCB before reviewed R2 release and separate R3 authorization. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
- Keep `VOUT_5V1` and `VOUT_PROTECTED` separate. No bypass, temporary jumper, fake `PWR_FLAG`, or placeholder protection to silence Electrical Rules Check (ERC). U402 pin 1 undriven power is expected while Sheet 03 is open.
- Do not arbitrarily substitute components, change values/connectivity, or overwrite user work. Major architecture changes require approval. Preserve the three current project footprints and library tables; their names do not establish thermal/assembly qualification.
- Preserve evidence states: KNOWN / MEASURED / CALCULATED / INFERRED / ASSUMED / UNKNOWN / OPEN / BLOCKED. ERC and Design Rules Check (DRC) are not electrical qualification. Never invent measurements or qualification.
- Normally address one gate per session. Keep historical evidence and source identities. Current context summarizes the latest dated review; old proposals are not current selections.
- Inspect the diff and run targeted validation afterward; see [validation](docs/VALIDATION.md). Never regenerate schematics as routine validation. Do not commit or push unrelated changes blindly; use feature branches and explicit authorization.
