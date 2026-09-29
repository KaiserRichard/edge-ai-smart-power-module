# Gates

Status of the R0–R5 release gates and what closes each. Gate definitions: [workflow and gates](../docs/context/05_WORKFLOW_AND_GATES.md). Seeded 2026-09-29 from the [manager report](../docs/FINAL_MANAGER_REPORT.md), the [blocker review](../docs/evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md), draft [PR #1](https://github.com/KaiserRichard/edge-ai-smart-power-module/pull/1) and the 2026-09-29 schematic check on the Mac.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Only the user closes a gate. ERC and DRC are rule checks, never electrical qualification.

## Summary

| Gate | Scope | Status | Blocked on |
| --- | --- | --- | --- |
| R0 | Environment, predecessor and source audit | CONDITIONAL PASS (2026-09-11) | Nothing that blocks R2 |
| R1 | Requirements and architecture | CONDITIONAL PASS, documentary only (2026-09-11) | Requirement freeze; see [REQUIREMENTS.md](REQUIREMENTS.md) |
| R2 | Schematic release | **BLOCKED** | User facts, Sheet 03 architecture approval, capture, component selections |
| R3 | PCB layout release | **BLOCKED** | R2 release, then separate authorization |
| R4 | Fabrication-readiness review | NOT STARTED | R3 |
| R5 | Physical bring-up and electrical validation | NOT STARTED | R4 and a fabricated board |

## R0: environment and sources

**Status:** CONDITIONAL PASS. Three pinned predecessor designs and official sources are consolidated.
**Limits kept visible:** remote-only sources, unresolved reuse rights on some historical assets, component-level qualification not done.
**Nothing further is needed for R2.**

## R1: requirements and architecture

**Status:** CONDITIONAL PASS as a documentary review package. This is not a freeze of the requirements or the architecture.
**Closes when:**
- The user approves the requirement table in [REQUIREMENTS.md](REQUIREMENTS.md), with every row that shapes topology or ratings CONFIRMED or explicitly accepted as ASSUMED.
- Remaining interface bounds and decisions in REQUIREMENTS.md are resolved or explicitly accepted as assumptions. D-30 closes GPIO entry, normal input range, and intended load scope; no final wall adapter is required.

## R2: schematic release

**Status:** BLOCKED. Current evidence (2026-09-29, KiCad 9.0.6 on the Mac, commit `de1d35c`):
- Sheet 03 is empty apart from TP301 and TP302. `VOUT_5V1` and `VOUT_PROTECTED` are separate by design.
- ERC: 1 error, U402 pin 1 undriven. It is legitimate while Sheet 03 is open and must not be silenced.
- Capture checker and 10 tests pass. That alone does not release R2.
- 26 of 71 parts have no footprint. J501, J502 and J503 read "MPN OPEN".

**Closes when all of these hold:**
1. **Interface definition:** D-30 confirms normal 9–24 V input, GPIO power, and Pi 5 + D435i load scope. Source fault/energy limits, load-dynamics test bounds, and connector/harness qualification remain OPEN (REQUIREMENTS.md). A wall adapter is not required; an unselected converter must eventually demonstrate compliance with the approved interface bounds.
2. **Sheet 03 architecture approved by the user.** Option I is PROPOSED ([DECISIONS.md](DECISIONS.md) D-20). The high-side-short finding stays blocking until these close: LM61460 load-step overshoot (PSpice, then bench), let-through with vendor models, LM61460 stability with the chosen bulk, detector and gate-stage timing across tolerance, and the Pi fault envelope. Since D-27 the load must stay ≤ 5.5 V with margin; option I at 5.49 V (model) does not yet meet that.
3. **Codex brief 02 evidence** meets its 8 explicit engineering acceptance criteria (PR #1). ERC-clean plus tests passing is not acceptance (D-11).
4. **Sheet 03 captured** by one Codex agent to the approved architecture. ERC then has no U402 error because the rail is really driven, not bypassed.
5. **Input coordination:** D101 selected so it never conducts at the source's worst OVP and the hot clamp plus overshoot stays below 67 V at U101 IN; F101 selected and coordinated.
6. **Connectors J501–J503** selected with mates.
7. **Review and explicit release** by the user, recorded in DECISIONS.md.

## R3: PCB layout release

**Status:** BLOCKED. No PCB, routing or Gerbers are authorized.
**Closes when:**
1. R2 is released and the user separately authorizes R3.
2. Every part has a verified footprint, including L201 (manufacturer drawing still unread), the nine TDK 22 µF capacitors, F101, J501–J503 and the test points.
3. Layout follows the TI reference layouts for the LM61460 and the protection stage; hot loop, Kelvin sense routing and thermal paths are reviewed.
4. DRC passes, and outputs (renders, STEP) are visually reviewed.
5. Board size, stack-up and thermal assumptions (REQUIREMENTS E2–E5) are confirmed or accepted.

## R4: fabrication readiness

**Status:** NOT STARTED.
**Closes when:** the BOM, Gerbers, drill, placement and STEP files are reviewed against the released R3 layout and the user gives explicit fabrication authorization. Agents never place orders or buy parts.

## R5: bring-up and validation

**Status:** NOT STARTED.
**Closes when** the bring-up progression passes and each result is recorded with method: visual inspection, continuity and shorts, current-limited supply, no-load start-up, output rail, dummy load, load steps, thermal, ripple, transients, protection and fault tests, telemetry, and only then the Pi. Reverse feed (P7) and recovery (P5) are verified here.
