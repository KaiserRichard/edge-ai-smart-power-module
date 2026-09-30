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

**Current status:** architecture D is a **PRELIMINARY TEST BOARD** proposal. No printed circuit board (PCB) is routed; no tests have run. Application margins are **(still open)**. Schematic, layout and fabrication-readiness gates precede bench work. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## What the bench equipment tells us

| Equipment | Purpose |
|---|---|
| Current-limited bench supply | Controlled input; normal V1A input is 9–26 V. Its limit alone cannot bound fast faults. |
| Dummy resistor or electronic load | Replaces the Raspberry Pi. Resistor current follows voltage; an electronic load can request current steps. Review power and fault ratings. |
| Oscilloscope and rated differential probes | Capture startup, ripple and overshoot at raw output, protected output and far-end dummy header against its loaded return. |
| Calibrated current probe | Captures L201 current through cutoff and decay; additional measurements establish incoming charge and energy-disposal currents. |
| Multimeter and temperature instruments | Check continuity, steady rails and component temperatures. |

Use the reviewed harness with a dummy header; the actual Pi input model is **(still open)**. Probe bandwidth, range and timing alignment must suit the event. Instrument grounds must not bypass the harness return.

## Bring up in this order

1. Inspect assembly and polarity → check continuity and shorts → connect a current-limited supply.
2. Start with no load → verify output and control rails → apply a low-current dummy load → increase load in steps.
3. Measure temperature → measure ripple → test load changes → perform reviewed protection/fault tests.
4. Validate telemetry → connect a single-board computer (SBC) **only after all gates pass**, including Pi interface checks.

Change connections only with supplies off and all capacitors discharged. Review traces and temperatures before increasing fault energy.

## What fault injection must establish

![[a4-fault-event-sequence.png|700]]

**Planned** detection, disconnection and energy disposal; the scope trace is illustrative, not measured.

A buck high-side switch failed short connects input through L201 to output. The reviewed injector must preserve this path; an external supply straight into the output tests a different fault. Never improvise a short across a running converter.

Source containment combines timed TPS26630 isolation, controlled local capacitance and a qualified inductor; applicable limits are **(still open)**. Source cutoff leaves energy in capacitors and L201. The disconnect and crowbar must handle it within component limits.

**Worked example — calculation:** an assumed 2.2 millifarad (mF) dummy capacitor at 5.5 V stores

$$E=\tfrac12 CV^2=\tfrac12(0.0022)(5.5)^2=0.033275\ \mathrm{J}\approx33.3\ \mathrm{mJ}.$$

Include that energy even after source cutoff. This assumption does not establish the Pi's capacitance.

Save raw traces, settings and temperatures. At the dummy header, fault peak **plus uncertainty must be below 5.5 V**; normal minimum **minus uncertainty must be at least 4.75 V at 5 A**. Check current decay, component stress and restart too. Fixture emergency cutoff rescuing a run does not prove autonomous protection.

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

Sources: [current basis](../../wt-gate4a/docs/evidence/r2/gate4a/BASIS.md), [bench plan](../../wt-gate4a/docs/evidence/r2/gate4a/TEST_PLAN.md), [fault fixture](../../wt-gate4a/docs/evidence/r2/gate4a/TEST_HOOKS.md).

Previous: [[06 PCB concepts]] · Next: [[08 V1A inside the robot]]
