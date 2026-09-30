---
title: "V1A lesson index"
tags: [v1a, lesson, visual]
---

# V1A lesson map

![[f9-01-course-map.png|900]]
*BATCH_F F9.1. Start at the left. Lesson 03 connects the normal power path to the fault problem.*

Nine lesson topics build one system picture in ten lesson notes (03 has A/B parts). Each begins with an analogy, walks through images, works a numerical example, shows a failure, and ends with a visual summary. Expand the check-yourself answers after trying the questions. The glossary is a companion reference, not a tenth design stage.

**Current controlling state:** normal input **9–26 V**; D101 **SMCJ36CA**; F101 **Schurter 3403.0285.23**; architecture **D fault-test board**; required **isolated 48→24 V module**, exact model open. **Gate 4a-FIX freeze BLOCKED. No Pi before fault tests and all other applicable gates pass. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

| Lesson | Follow this picture | By the end, explain… |
|---|---|---|
| [[00 System overview]] | Water service and five functional zones | Where conversion, protection, measurement and delivery begin/end |
| [[01 Input protection]] | Four guards, TVS curve and eFuse window | Why standoff, clamp and cutoff are different |
| [[02 Buck converter LM61460]] | Flywheel, current paths and aligned waveforms | How current rises and falls while still supplying the load |
| [[03 Output protection|03a Output protection: fault and energy]] | Stuck tap, two drains and pilot fault plots | Why source cutoff alone is insufficient |
| [[03b Output protection margins and proof|03b Output protection: margins and proof]] | Voltage ladder, delay plot and reset sequence | What D still owes despite the ideal waveform |
| [[04 Monitoring]] | Kelvin close-up and bus islands | What the shunt measures and what energy logs miss |
| [[05 Powering the Pi 5 through GPIO]] | Voltage staircase, pin map and sharing chart | How a few milliohms spend the Pi's voltage margin |
| [[06 PCB concepts]] | Return loops, sense routes and heat cutaway | Why physical geometry is part of the circuit |
| [[07 Bench bring-up and fault-injection testing]] | Bench station, probes and uncertainty plots | What a valid dummy-load protection test must establish |
| [[08 V1A inside the robot]] | Robot cutaway and isolation boundary | What standalone V1A can and cannot claim about the robot |
| [[99-Glossary]] | Course legend and voltage ladder | How units, boundaries and evidence labels prevent mistakes |

The green/blue/orange curves are teaching calculations, not recorded oscilloscope traces. Read the **ASSUMED / preliminary** text on each chart. The unchanged pilot fault model intentionally omits important hardware effects; Lesson 03 states them before the trajectories. Known failed screens remain visible alongside favorable examples.

The Harwin contact criterion failure and newer unqualified TE harness proposal are separated in Lesson 05. The UENPO rejection and isolation rationale are in Lessons 01 and 08. Gate 4a is a review within R2, **not** the repository's R4 fabrication-readiness gate.

- [[FACTCHECK_LOG|Original fact-check log and pinned sources]] — preserved historical audit.
- [[VISUAL_REBUILD_LOG|Visual rewrite, source pins, checks and handoff]] — current editorial evidence and asset handling.
- [BATCH_F prompts](../illustrations/BATCH_F.md) — existing concept-image prompts plus the specific pilot-image additions.
- [Figure source README](figures/src/README.md) — reproduce the charts from Python.

Read illustrations as teaching views, never as build instructions or component/package approval. Owner images are referenced by filename; newly generated charts use unique `v2-` filenames under `figures/` to avoid confusing them with older vault charts.
