---
title: "V1A lesson index"
tags: [v1a, lesson]
---

# V1A lesson map

Read in order. These notes explain the design and planned tests; they do not establish tested performance or release any engineering gate.

**Current status:** normal input 9–26 V; architecture D fault-test board; **Gate 4a freeze BLOCKED** by open circuit contracts. No Pi before fault tests and all other applicable gates pass. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

- [[00 System overview]] — Follow power from the battery and upstream module through V1A to the Pi.
- [[01 Input protection]] — Understand the fuse, transient suppression, reverse-polarity path and electronic fuse.
- [[02 Buck converter LM61460]] — Follow switching states, inductor current, capacitors and voltage feedback.
- [[03 Output protection]] — Understand preliminary architecture D, the source fault bound and dummy-load proof.
- [[04 Monitoring]] — Read the 2 milliohm shunt, INA228 measurements and their system boundary.
- [[05 Powering the Pi 5 through GPIO]] — Budget voltage drop through the protection, connectors and complete harness.
- [[06 PCB concepts]] — Learn switching loops, return paths, Kelvin routing and heat flow before layout.
- [[07 Bench bring-up and fault-injection testing]] — Plan staged measurements and protection tests before connecting a Pi.
- [[08 V1A inside the robot]] — Connect the standalone module to the future robot interface and telemetry plan.
- [[99-Glossary]] — Look up the abbreviations and engineering terms used throughout the lessons.

[[FACTCHECK_LOG|Fact-check log and pinned sources]] records corrections, current owner decisions, image-caption limitations and verified teaching calculations. The Harwin Pi-contact qualification FAIL is explained in lesson 05; the required isolated supply and UENPO rejection are explained in lessons 01 and 08.
