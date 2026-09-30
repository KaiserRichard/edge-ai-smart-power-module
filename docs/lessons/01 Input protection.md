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

The picture shows functional boundaries. Its “regulated 5 V” label means the approximately 5.1 V local target; it does not establish delivered Pi voltage or a validated board rating.

## Four jobs at the input

**OBSERVATION — captured circuit:** input → F101 → fused node → Q101 → TPS26630 → buck input bank. D101 connects from the fused node to ground; Q102 controls Q101's gate.

| Device | Job and limit |
| --- | --- |
| **F101, fuse** | Opens the series path after enough fault current flows for enough time. Provides backup protection. |
| **D101, transient voltage suppressor (TVS)** | Diverts a short voltage surge toward ground. Must survive the pulse and work with the fuse and electronic cutoff. |
| **Q101/Q102** | Q101 carries power; Q102 helps turn it off by discharging its gate relative to its source. They provide the external reverse-protection arrangement. |
| **U101, TPS26630 electronic fuse (eFuse)** | Checks voltage, limits input current, controls startup and can interrupt incoming power. |

Q101 and Q102 are metal-oxide-semiconductor field-effect transistors (**MOSFETs**). An off MOSFET still has a body diode. Reversing the input wires and feeding power backward from the output are different faults; both paths need checking.

**DECISION — selected for proposed capture:** Gate 4a adopts **Littelfuse SMCJ36CA for D101** and **Schurter 3403.0285.23 for F101**, following the TVS/fuse reselection report. D101 has 36 V standoff; its specified pulse clamp is 58.1 V at 25.9 A for the stated 25°C, 10/1000 µs test. F101 is a 12.5 A time-lag fuse, rated 125 VDC with 1000 A DC interruption under its specified conditions. These are component specifications, not V1A ratings. Installed clearing, hot surge behavior and coordination are **(still open)**.

## Read the eFuse settings correctly

These are **CALCULATED baseline nominal settings**, not measured guarantees or a newly approved operating range:

| Function | Baseline value | Meaning |
| --- | --- | --- |
| Undervoltage lockout (**UVLO**) | About **8.46 V**, rising | Holds the power path off when input voltage is too low. |
| Overvoltage protection (**OVP**) | About **27.6 V** | Commands cutoff above its threshold; it does not clamp the rail to 27.6 V. |
| Input current limit | About **4.5 A** | Controls current entering the converter, not its 5 V output current. |

The inherited rising OVP screen is about **26.97–28.29 V**, only 0.97 V above the normal ceiling at its low end. Thus **27 V is a fault-test point, not a guaranteed trip voltage**. The falling/reset screen is about **25.00–26.58 V**, so returning to 26 V after a trip does not guarantee recovery. Hot drift, restart and nuisance-trip behavior are **(still open)**; these screens are not complete hot limits.

The development plan also uses **timed TPS26630 input isolation** with **10–30 microfarads (µF) of effective local input capacitance**. Source isolation cuts further supply; charged capacitors can still feed a fault. The independent fault trigger and full isolation time are **(still open)**. See [[03 Output protection]].

## Why this design and not another

The owner's **9–26 V** normal range leaves a nominal 24 V module room for tolerance and ripple. That makes 26 V a design requirement, not proven operation: the complete healthy waveform must stay in range, and the remaining OVP margin needs testing. It also does not approve sustained 33.6 V input.

The upstream module must be isolated: a non-isolated buck's shorted high-side switch can create a direct path from the robot bus toward V1A. The owner rejected the UENPO non-isolated module. Isolation removes that direct power-transfer path while its barrier is intact; output-fault limits and connected ports still need review. See [[08 V1A inside the robot]].

The 36 V bidirectional TVS gives more standoff margin for the studied upstream faults than the older 26 V part. The larger SMC package improves the pulse-power screen, but its higher clamp requires separate checks of the buck and auxiliary-supply paths. The 12.5 A fuse improves the assumed hot hold-current margin; it clears moderate faults more slowly. The approximately 4.5 A eFuse limit cannot be relied on to blow it, and the upstream TVS current bypasses that limit. This is why timed source shutdown and coordination remain necessary.

**Gate 4a freeze is BLOCKED** until these and the other open circuit contracts are resolved.

## Small example: input current is different

**ASSUMPTION:** 5.1 V, 5 A at the buck output, 90% buck efficiency and 9 V at its input.<br>
**CALCULATION:** $P_{OUT}=5.1\times5=25.5\,\mathrm{W}$; $I_{IN}\approx25.5/(9\times0.90)=3.15\,\mathrm{A}$.

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
> [Pinned sources and fact-check record](FACTCHECK_LOG.md#sources): IN for the path/settings; TVS for the selected parts and their tradeoffs; BASIS and G4 for 9–26 V and the blocked freeze; SRC for timed isolation. Older 24 V ceilings and unselected-fuse statements are historical.

Previous: [[00 System overview]] · Next: [[02 Buck converter LM61460]] · Terms: [[99-Glossary]]
