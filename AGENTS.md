# AGENTS.md — Edge AI Smart Power Module

## Project

This repository contains the design and validation of a Smart DC Power Module for Edge AI / Edge Computing devices.

V1 focuses on:
- DC input
- input and reverse-polarity protection
- high-current regulated 5 V output
- voltage/current/power/energy monitoring
- I2C telemetry
- testability and fabrication readiness

The project may later provide validated design blocks for a WBR-specific V2, but V1 must remain a standalone Project II design.

## Engineering Rules

- Prefer proven reference circuits and manufacturer reference designs over inventing circuits from scratch.
- Manufacturer datasheets, application notes, and official documentation are authoritative over GitHub implementations.
- Never blindly copy an entire third-party PCB.
- Reuse or adapt functional blocks only after understanding their assumptions, ratings, and interfaces.
- Record the source and engineering rationale for important design decisions.
- Never invent missing electrical requirements. Mark them `OPEN` and document the consequence.
- Do not route USB 3.x or D435i data through this PCB.
- Do not assume the final WBR battery voltage or robot electrical architecture.

## Third-Party Provenance

For every third-party design inspected or reused, record:
- repository/document URL
- exact Git commit or document revision
- relevant source files
- license
- circuit/function studied
- whether it was referenced, adapted, or copied
- modifications made
- required attribution

Keep third-party material isolated under `third_party/`.

Do not modify upstream reference sources unless explicitly required.

## KiCad

- Use standard KiCad project files.
- Prefer `kicad-cli` for automated checks and fabrication exports.
- Run ERC after schematic changes.
- Run DRC after PCB changes.
- Treat ERC/DRC PASS only as rule-check evidence, never as proof of electrical correctness or safety.
- Verify footprints, package variants, polarity, pin numbering, and component ratings against authoritative documentation.
- Follow manufacturer reference layouts for switching regulators and other layout-sensitive circuits.
- Visually review generated PCB outputs in addition to automated checks.

## Power Design

Explicitly analyze and document:
- input voltage range
- output voltage
- continuous and peak current
- efficiency
- ripple
- thermal limits
- inrush/startup behavior
- protection behavior
- component derating
- connector ratings
- copper/current capacity
- switching-loop geometry
- return-current paths
- grounding
- decoupling
- thermal paths

For current sensing, explicitly verify:
- shunt resistance
- shunt voltage range
- I^2R dissipation
- tolerance
- temperature coefficient
- Kelvin connections
- sense routing
- measurement range and accuracy

## Fabrication Safety

Until explicitly approved after engineering review, all PCB revisions are:

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Codex may generate:
- schematics
- PCB layouts
- ERC/DRC reports
- BOMs
- Gerbers
- drill files
- placement files
- PDFs/renders
- STEP models
- engineering reports

Codex must not:
- place manufacturing orders
- purchase components
- claim the design is electrically safe solely because ERC/DRC passes
- use an expensive SBC as the first hardware load
- modify unrelated repositories or system configuration unnecessarily

## Bring-Up

Plan first power-on using this progression:

1. visual inspection
2. continuity and short-circuit checks
3. current-limited bench supply
4. no-load startup
5. verify output rail
6. low-current dummy/electronic load
7. increasing load steps
8. thermal measurements
9. ripple measurements
10. transient/load testing
11. protection/fault testing
12. telemetry validation
13. SBC integration only after the previous gates pass

## Documentation

Keep engineering evidence under `docs/`.

Important documents should include:
- requirements
- predecessor/reference audit
- architecture
- component-selection rationale
- calculations
- schematic review
- PCB-layout review
- bring-up procedure
- manager report

Clearly distinguish:
- OBSERVATION
- REQUIREMENT
- ASSUMPTION
- CALCULATION
- HYPOTHESIS
- EVIDENCE
- DECISION
- OPEN RISK

Do not describe untested behavior as validated.

## Execution Gates

Work sequentially:

- R0 — environment and predecessor audit
- R1 — requirements and architecture
- R2 — schematic
- R3 — PCB layout
- R4 — fabrication-readiness review
- R5 — physical bring-up and electrical validation

Do not skip gates merely because later work can be generated automatically.

At the end of each gate, update `docs/FINAL_MANAGER_REPORT.md` with:

- STATUS: PASS / CONDITIONAL PASS / BLOCKED
- WHAT WAS DONE
- EVIDENCE
- DECISIONS
- OPEN RISKS
- NEXT GATE

## Git Discipline

- Keep commits focused and reviewable.
- Do not commit generated build/cache files unless intentionally required.
- Do not commit secrets or credentials.
- Do not rewrite or delete historical experimental evidence.
- Do not commit or push unless explicitly instructed.
