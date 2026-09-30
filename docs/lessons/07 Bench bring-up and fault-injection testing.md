---
title: Bench bring-up and fault-injection testing
lesson: 7
tags: [v1a, lesson]
---

# 07 — Bench bring-up and fault-injection testing

## Why this matters

A correct-looking schematic cannot show the real fault voltage or temperature.  
A dummy load lets us investigate failures before connecting an expensive computer.  
Measurements must prove both normal operation and fault containment.

**Current status:** architecture D is a **PRELIMINARY TEST BOARD** proposal. **Gate 4a capture freeze is BLOCKED** by open circuit contracts. No printed circuit board (PCB) is routed; the cited bench plan reports no physical tests. Application margins are **(still open)**. Schematic, layout and fabrication-readiness gates precede bench work. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## What the bench equipment tells us

| Equipment | Purpose |
|---|---|
| Current-limited bench supply | Controlled input; normal V1A input is 9–26 V. Its limit alone cannot bound fast faults. |
| Dummy resistor or electronic load | Replaces the Raspberry Pi. Resistor current follows voltage; an electronic load can request current steps. Review power and fault ratings. |
| Oscilloscope and rated differential probes | Capture startup, ripple and overshoot at raw output, protected output and far-end dummy header against its loaded return. |
| Calibrated current probe | Captures L201 current through cutoff and decay; additional measurements establish incoming charge and energy-disposal currents. |
| Multimeter and temperature instruments | Check continuity, steady rails and component temperatures. |

Use the proposed harness with a dummy header only after reviewing its suitability for each planned test. **The Harwin Pi-contact selection fails the documented resistance criterion** in [[05 Powering the Pi 5 through GPIO]]; a review is not electrical qualification. The actual Pi input model is **(still open)**. Probe bandwidth, range and timing alignment must suit the event. Instrument grounds must not bypass the harness return; keep equipment protective earth intact.

## Bring up in this order

1. Inspect assembly and polarity → check continuity and shorts → connect a current-limited supply.
2. Start with no load → verify output and control rails → apply a low-current dummy load → increase load in steps.
3. Measure temperature → measure ripple → test load changes → perform reviewed protection/fault tests.
4. Validate telemetry → connect a single-board computer (SBC) **only after all gates pass**, including Pi interface checks.

Change connections only with supplies off and all capacitors discharged. Review traces and temperatures before increasing fault energy.

The plan includes normal tests at **9, 24 and 26 V**, with **0, 2.5 and 5 A** load cases and controlled temperature states. **27 V is an additional fault/OVP-window point**, outside normal operation. It may or may not trip the fitted eFuse. If the source is already isolated, that run cannot demonstrate fault interruption from an energized source; do not defeat OVP to disguise that difference.

## What fault injection must establish

![[a4-fault-event-sequence.png|700]]

**Planned** detection, disconnection and energy disposal; the scope trace is illustrative, not measured. Set up recording before injection and capture the entire event. Frame 5 means reviewing recorded data, not starting the oscilloscope after cutoff. The diagram omits source isolation and the separate raw-side energy path.

A buck high-side switch failed short connects input through L201 to output. The reviewed injector must preserve this path; an external supply straight into the output tests a different fault. Never improvise a short across a running converter.

The proposed source containment combines timed TPS26630 isolation, controlled local capacitance and an inductor whose fault limits still need qualification. Source cutoff leaves energy in capacitors and L201. The protected crowbar handles its side of the disconnect; upstream energy needs the separately reviewed raw-side path after the pair opens. All paths must stay within component limits.

**Worked example — calculation:** an assumed 2.2 millifarad (mF) dummy capacitor at 5.5 V stores

$$E=\tfrac12 CV^2=\tfrac12(0.0022)(5.5)^2=0.033275\ \mathrm{J}\approx33.3\ \mathrm{mJ}.$$

Include that energy even after source cutoff. This assumption does not establish the Pi's capacitance.

Save synchronized raw traces, settings and temperatures, starting before injection and continuing through current decay. At the dummy header, fault peak **plus uncertainty must be below 5.5 V**; normal minimum **minus uncertainty must be at least 4.75 V at 5 A**. Capture both module output nodes, L201 current and source/dump currents; check component stress, usable control rails and restart too.

For retained WFMB2512 ballast, the plan requires pre-pulse terminal temperature plus uncertainty **≤85°C**, with terminal temperature including pulse rise kept **below 95°C**. A temperature label for the room cannot establish those limits.

Fixture-timed shutdown tests only a conditional source bound; it cannot prove the missing autonomous trigger. Fixture emergency cutoff rescuing a run does not prove autonomous protection either.

> [!warning] Common misconceptions
> A supply current limit does not stop a charged capacitor's fast discharge. One acceptable output peak does not prove component survival. A dummy-load pass covers its tested conditions; it does not authorize immediate Pi connection.

## Check yourself

1. Why use a dummy load first?
2. Why does turning off the source leave fault energy?
3. Why measure voltage at the far end of the harness?
4. Does one passing fault trace permit Pi connection?

> [!question]- Answers
> 1. It allows controlled testing without risking the Pi.
> 2. Capacitors and the inductor still store energy.
> 3. Harness impedance changes the voltage seen by the load, including transients.
> 4. No. Normal, fault, thermal, telemetry and interface gates all need closure.

Sources: [pinned source register](FACTCHECK_LOG.md#sources), G4 and BASIS for status/input limits; TEST and HOOKS for the planned matrix, recording, temperature and fixture distinctions; VERIFY for the contact finding. This lesson describes planned work, not performed tests.

Previous: [[06 PCB concepts]] · Next: [[08 V1A inside the robot]]
