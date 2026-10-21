# V1A Lessons link-check report

**Audit date:** 2026-10-01  
**Vault:** `/Users/quockaiser/Desktop/Research/V1A-Lessons`  
**Scope:** read-only audit of `lessons/*.md`, `images/`, `BATCH_F.md`, and `code/`.

## 1. Image embeds

There are 113 image embeds. 103 resolve to files in `images/`; these 10 do not:

| Lesson | Missing image | BATCH_F prompt / producer |
| --- | --- | --- |
| 00 System overview.md | `f0-04-circuit-boundary.png` | BATCH_F **F0.4** |
| 01 Input protection.md | `f1-04-input-sense-circuit.png` | BATCH_F **F1.4** |
| 02 Buck converter LM61460.md | `f2-04-feedback-circuit.png` | BATCH_F **F2.4** |
| 03 Output protection.md | `f3-05-schematic-walk-circuit.png` | BATCH_F **F3.5** |
| 03 Output protection.md | `p03-12-simplified-circuit.png` | `code/draw_sheet03_simplified.py`; BATCH_F has no matching prompt entry |
| 04 Monitoring.md | `f4-04-kelvin-filter-circuit.png` | BATCH_F **F4.4** |
| 05 Powering the Pi 5 through GPIO.md | `f5-04-output-connectors-circuit.png` | BATCH_F **F5.4** |
| 06 PCB concepts.md | `f6-04-bypass-pins-circuit.png` | BATCH_F **F6.4** |
| 07 Bench bring-up and fault-injection testing.md | `f7-04-test-nets-circuit.png` | BATCH_F **F7.4** |
| 08 V1A inside the robot.md | `f8-03-input-boundary-circuit.png` | BATCH_F **F8.3** |

No missing embed is without an identified prompt or producer.

## 2. Note links

**Broken note links: none found.** All 48 Obsidian note links resolve to a lesson/support note in the vault.

## 3. Images not used by any lesson

The following 51 image files are present in `images/` but are not referenced by any lesson:

- `00-v1a-kicad-sheet-map.png`
- `00-v1a-system-anatomy.png`
- `01-input-fault-timescale-map.png`
- `01-input-protection-pcb-placement.png`
- `01-reverse-mosfet-operating-states.png`
- `01-tps26630-functional-anatomy.png`
- `01-v1a-to-wbr-system-architecture.png`
- `02-buck-high-side-on.png`
- `02-buck-low-side-on.png`
- `02-inductor-selection.png`
- `02-input-hot-loop.png`
- `02-lm61460-feedback-loop.png`
- `02-lm61460-ideal-placement.png`
- `02-output-capacitor-real-behavior.png`
- `02-v1a-circuit-anatomy.png`
- `03-buck-power-flow-and-waveforms.png`
- `04-protection-and-operating-states.png`
- `05-pcb-layout-kelvin-and-thermal.png`
- `06-power-board-bringup-and-characterization.png`
- `07-wbr-power-distribution-board.png`
- `a1-p0-fault-injection-bench-setup.png`
- `a2-sheet-03-architecture-d.png`
- `a3-present-source-boundary.png`
- `a4-fault-event-sequence.png`
- `b1-input-fault-timescale-map.png`
- `b3-reverse-polarity-and-backfeed-teaching-diagram.png`
- `b4-tps26630-functional-role-and-timing-concept.png`
- `b5-standalone-v1a-and-future-integration-boundary.png`
- `c3-buck-cycle-waveforms.png`
- `c4-10-h-alloy-inductor-selection.png`
- `c5-buck-power-flow-and-both-states.png`
- `d1-kicad-sheet-map.png`
- `d2-v1a-system-anatomy.png`
- `d3-v1a-circuit-anatomy-without-fake-hardware.png`
- `e2-lm61460-placement-principles.png`
- `e3-protection-states-and-fault-response.png`
- `e4-pcb-layout-principles-without-implying-a-routed-board.png`
- `e5-safe-bring-up-and-characterization.png`
- `f2-01-buck-two-states-3d.png`
- `v2-p03-03-energy-stores.png`
- `v2-p03-06-fault-timeline.png`

Unused does not imply disposable; the audit only reports references.

## 4. Filename checks

- Double dots: none found.
- Spaces: present in lesson/support Markdown names, including `00 System overview.md`, `01 Input protection.md`, `02 Buck converter LM61460.md`, `03 Output protection.md`, `03b Output protection margins and proof.md`, `04 Monitoring.md`, `05 Powering the Pi 5 through GPIO.md`, `06 PCB concepts.md`, `07 Bench bring-up and fault-injection testing.md`, and `08 V1A inside the robot.md`.
- Capital letters: present in the lesson/support Markdown names and `00-INDEX.md`, `99-Glossary.md`, `FACTCHECK_LOG.md`, `SCHEMATIC_READING_GUIDE.md`, and `VISUAL_REBUILD_LOG.md`.
- Image filenames use lowercase kebab-case.
- Duplicate names differing only by case: none found.

No renames were made.

## 5. Front matter and navigation

The core lesson notes—00 through 08, including 03b, plus 99 Glossary—have YAML front matter with `title` and `tags`, and have previous/next navigation links.

Structural exceptions:

- `00-INDEX.md`: has `title` and `tags), but intentionally has no previous/next lesson links.
- `FACTCHECK_LOG.md`, `SCHEMATIC_READING_GUIDE.md`, and `VISUAL_REBUILD_LOG.md`: support/audit notes; they have no YAML front matter and are not lesson-navigation notes. They are not lesson-text changes.
- `99-Glossary.md`: has the required front matter and previous/next navigation.

## 6. Vault versus worktree copy

No filename differences found between `V1A-Lessons/lessons/` and `docs/lessons/`. Therefore there is no `03 Output protection.md` owner-notes-only exception to record.

## Disposition

**REPORT ONLY.** No lesson text, vault image, prompt, script, or source file was changed.


