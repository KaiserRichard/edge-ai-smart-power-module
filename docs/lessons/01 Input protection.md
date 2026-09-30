---
title: "Input protection"
lesson: 1
tags: [v1a, lesson]
---

# 01 — Input protection

## Why this matters

A power cable can deliver a voltage spike, reversed polarity or excessive current.<br>
Different faults need different protection functions.<br>
Understanding the input stage explains its jobs and limits.

## What reaches V1A?

**REQUIREMENT:** normal input is **9–26 V direct current (DC)**. The Wheel-Biped Robot (WBR) context below places a bought isolated **48 V → 24 V module** before V1A; its selection is **(still open)**. Here, 13S means 13 series cells and PDB means power distribution board.

![[b5-standalone-v1a-and-future-integration-boundary.png|700]]

## Four jobs at the input

**OBSERVATION — captured circuit:** input → F101 → fused node → Q101 → TPS26630 → buck input bank. D101 connects from the fused node to ground; Q102 controls Q101's gate.

| Device | Job and limit |
| --- | --- |
| **F101, fuse** | Opens the series path after enough fault current flows for enough time. Provides backup protection. |
| **D101, transient voltage suppressor (TVS)** | Diverts a short voltage surge toward ground. Must survive the pulse and work with the fuse and electronic cutoff. |
| **Q101/Q102** | Q101 carries power; Q102 helps turn it off by discharging its gate relative to its source. They provide the external reverse-protection arrangement. |
| **U101, TPS26630 electronic fuse (eFuse)** | Checks voltage, limits input current, controls startup and can interrupt incoming power. |

Q101 and Q102 are metal-oxide-semiconductor field-effect transistors (**MOSFETs**). An off MOSFET still has a body diode. Reversing the input wires and feeding power backward from the output are different faults; both paths need checking.

**DECISION — proposed update:** Gate4a adopts **SMCJ36CA for D101** and **3403.0285.23 for F101**, superseding the older reselection notes. These are proposed capture choices. Fuse clearing, hot surge behavior and coordination are **(still open)**.

## Read the eFuse settings correctly

These are **CALCULATED baseline nominal settings**, not measured guarantees or a newly approved operating range:

| Function | Baseline value | Meaning |
| --- | --- | --- |
| Undervoltage lockout (**UVLO**) | About **8.46 V**, rising | Holds the power path off when input voltage is too low. |
| Overvoltage protection (**OVP**) | About **27.6 V** | Commands cutoff above its threshold; it does not clamp the rail to 27.6 V. |
| Input current limit | About **4.5 A** | Controls current entering the converter, not its 5 V output current. |

The inherited minimum OVP threshold is about 26.97 V, only 0.97 V above normal input's ceiling. Final settings, hot drift and nuisance-trip behavior are **(still open)**.

The development plan also uses **timed TPS26630 input isolation** with **10–30 microfarads (µF) of effective local input capacitance**. Source isolation cuts further supply; charged capacitors can still feed a fault. The independent fault trigger and full isolation time are **(still open)**. See [[03 Output protection]].

## Small example: input current is different

**ASSUMPTION:** 5.1 V, 5 A at the buck output, 90% buck efficiency and 9 V at its input.<br>
**CALCULATION:** output power = 5.1 × 5 = **25.5 W**; input current ≈ 25.5 ÷ (9 × 0.90) = **3.15 A**.

Thus a 5 A output can coexist with an approximately 4.5 A input limit. Extra path losses and startup are excluded; this is not measured.

> [!warning] Common misconceptions
> A fuse does not stop every fast spike. A TVS voltage label is not its surge clamping voltage. The TPS26630 alone does not provide the captured external reverse-input function. Input protection cannot by itself guarantee a safe 5 V output after a buck fault.

## Check yourself

1. Why do we need both a fuse and a TVS?
2. Does a 27.6 V OVP setting mean V1A may operate normally at 27.6 V?
3. Why can input current be below 5 A while output current is 5 A?
4. Does opening the eFuse remove all stored fault energy?

> [!question]- Answers
> 1. The TVS handles short surges; the fuse interrupts sufficiently severe, lasting current. Their coordination needs testing.
> 2. No. Normal input is 9–26 V; the cutoff has tolerances and delay.
> 3. The buck trades input voltage for output current, with some power lost as heat.
> 4. No. Local capacitors and the inductor can still release stored energy.

> [!info]- Evidence and reading
> [Captured input review](../docs/evidence/r2/INPUT_PROTECTION.md), [current Gate4a basis](../../wt-gate4a/docs/evidence/r2/gate4a/BASIS.md), [source-isolation study](../../wt-gate3b/docs/evidence/r2/sheet03/gate3b/INPUT_LIMITER_AND_ENERGY.md).

Previous: [[00 System overview]] · Next: [[02 Buck converter LM61460]] · Terms: [[99-Glossary]]
