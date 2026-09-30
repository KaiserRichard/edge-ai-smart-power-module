---
title: "PCB concepts"
lesson: 6
tags: [v1a, lesson]
---

# 06 — Printed circuit board (PCB) concepts

## Why this matters

The printed circuit board (PCB) carries current, heat and measurement signals.  
Its copper paths can add voltage drop, switching noise and measurement error.  
Understanding these paths helps you review a future layout before hardware testing.

**OBSERVATION:** This lesson is conceptual: no V1A PCB is routed. R2 schematic release and R3 PCB release remain blocked. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## 1. The hot loop and its return

The buck's **hot loop** surrounds the local input capacitor, both switches and the power-ground return. “Hot” means rapidly changing current. A large loop adds unwanted inductance and makes switching noise harder to control.

![[d4-buck-input-switching-loop.png|700]]

The dashed outlines compare compact and long-return loops. They mark loop area, **not simultaneous conduction** of both switches. The switches alternate; see [[02 Buck converter LM61460]].

Current must return to its source. A ground symbol does not remove the return copper's impedance. Keep input capacitors close to both LM61460 input-voltage (VIN) and power-ground (PGND) pairs, following manufacturer guidance.

Keep feedback and shunt-sense paths away from switching nodes and switching-current voltage drops. The final return geometry is **(still open)**.

## 2. Power copper and Kelvin sensing have different jobs

Short, low-resistance power paths limit voltage loss and heating. The shunt's wide **force terminals** carry load current; separate **Kelvin sense terminals** let the INA228 measure the resistor's voltage.

Route sense traces together from those dedicated terminals to the monitor's filter. Remote power-copper connections would include unwanted copper drop. Never bypass the shunt with a copper pour.

**CALCULATION — small signal, real power:** For the nominal 2 milliohm (mΩ) shunt at 5 A:

\[
V=IR=5\times0.002=0.010\ \text{V}=10\ \text{mV}
\]
\[
P=I^2R=5^2\times0.002=0.050\ \text{W}
\]

Only 10 mV represents 5 A, so unwanted sense-path voltage matters. The 50 mW result does not establish temperature or accuracy.

## 3. Heat needs a path too

Power parts transfer heat into copper through package connections. Copper and suitable thermal vias spread heat, following the actual package and electrical nets. The LM61460 has no extra generic ground thermal pad. Do not enlarge noisy switching-node copper indiscriminately for cooling.

Board layers, copper thickness, dimensions, ambient temperature and airflow are **(still open)**. No trace width or via count is approved here. Calculations guide the layout; later dummy-load measurements check temperatures.

> [!warning] Common misconceptions
> - “Short outgoing trace means small loop.” The return matters too.
> - “Any shunt connection is Kelvin sensing.” Use dedicated sense terminals.
> - “More copper is always better.” Respect noisy nodes and the shunt boundary.
> - “Passing design rule checks proves performance.” Electrical and thermal validation remain necessary.

## Check yourself

1. What makes the buck input loop “hot”?
2. Why must you inspect the return path as well as the outgoing path?
3. Where should the INA228 sense traces begin?
4. Does the 50 mW calculation prove the shunt temperature is acceptable?

> [!question]- Answers
> 1. Its current changes rapidly during switching.
> 2. Both paths form the loop; a long return adds unwanted impedance and loop area.
> 3. At the shunt's separate Kelvin sense terminals, not remote force copper.
> 4. No. Temperature depends on the component, board and operating conditions and needs validation.

## Sources

- [Engineering state and blocked layout gate](../docs/context/03_ENGINEERING_STATE.md).
- [Buck review: local decoupling and later layout gates](../docs/evidence/r2/BUCK_DESIGN.md#pinpackage-and-later-layout-gates); its older component selections are not final selections for this lesson.
- [Footprint review: LM61460 thermal lands and R401 Kelvin mapping](../docs/evidence/r2/forensic_2026-09-14/CRITICAL_FOOTPRINT_QUALIFICATION.md).
- [Illustration audit: no routed board](../../wt-illustrations/docs/illustrations/IMAGE_AUDIT.md) and [D4 conceptual-loop prompt](../../wt-illustrations/docs/illustrations/BATCH_D.md#d4--buck-input-switching-loop-regenerate).

Previous: [[05 Powering the Pi 5 through GPIO]] · Next: [[07 Bench bring-up and fault-injection testing]]
