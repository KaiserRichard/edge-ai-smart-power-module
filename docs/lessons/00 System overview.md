---
title: "System overview"
lesson: 0
tags: [v1a, lesson]
---

# 00 — System overview

## Why this matters

V1A is designed to turn a higher direct-current (DC) supply into a monitored 5 V supply.<br>
Each block has a different job: distribute, convert, protect, or measure.<br>
Understanding these boundaries helps you find where a fault must be stopped.

## Follow the power

The proposed Wheel-Biped Robot (WBR) integration context uses a **13-series-cell (13S) battery** and a **power distribution board (PDB)**; the complete robot electrical architecture is still open. The intended Raspberry Pi 5 connection uses the power pins on its **general-purpose input/output (GPIO)** header.

**Battery → PDB → bought isolated 48 V → 24 V module → V1A → Pi 5 GPIO power pins.**

![[a3-present-source-boundary.png|650]]

The picture ends at V1A and highlights the unselected upstream module. “48 V → 24 V” describes the module class, not guaranteed operating or fault limits. Its exact model and fault behavior are **(still open)**. Isolation separates the converter's power-transfer sides; it does not guarantee that every output fault is contained.

**REQUIREMENT:** V1A's normal input range is **9–26 V**. The robot battery must never connect directly to it. V1A remains a standalone Project II design; it can first be studied using a suitable current-limited bench source.

## Inside V1A

![[d3-v1a-circuit-anatomy-without-fake-hardware.png|650]]

The upper row shows power moving toward the load. The lower row shows measurement and test access; it is a functional drawing, not a wiring diagram.

| Block | Job |
| --- | --- |
| Input protection | Handle input faults and control admission of power. See [[01 Input protection]]. |
| LM61460 buck converter | Reduce the input to about **5.1 V locally**, targeting **5 A** operation. See [[02 Buck converter LM61460]]. |
| Output protection | Independently interrupt a failed converter's output path. Architecture D is a **preliminary test-board design**. See [[03 Output protection]]. |
| Shunt and INA228 | Measure current through a **2 milliohm (mΩ)** resistor and the load-side voltage; report telemetry over **Inter-Integrated Circuit (I2C)**. See [[04 Monitoring]]. |
| Output interface | Carry power through the connector and harness to the load. Their voltage drops matter. |

The buck's local 5.1 V is not a guarantee of 5.1 V at the Pi. Switches, the shunt, contacts, and both supply and return wires lose some voltage. Monitoring reports measurements; it does not replace fast hardware protection.

## Small example: the power target

**CALCULATION:** at the local regulator target, power is

$$
P=VI=5.1\,\mathrm{V}\times5\,\mathrm{A}=25.5\,\mathrm{W}.
$$

The input must supply more than 25.5 W because conversion and wiring produce heat. Actual efficiency and continuous thermal capability are **(still open)**; the calculation is not a measured board rating.

## Where the project stands

**PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD). Gate 4a freeze: BLOCKED.** Required circuit connections and limits are still open: the independent fault trigger, control supplies, fault logic and protected capacitor bank. Gate 4a is part of R2 schematic work, not the R4 fabrication gate. No printed circuit board (PCB) is routed. Schematic, layout and fabrication reviews must precede hardware tests. Later tests use dummy loads; **no Pi is connected before fault tests and all other required gates pass**.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

> [!warning] Common misconceptions
> A nominal 24 V module is not automatically a qualified source.<br>
> V1A is not the robot's whole power distribution board.<br>
> A clean schematic or rule-check report does not prove electrical performance.

## Check yourself

1. Which block sits between the PDB and V1A?
2. Why can the Pi receive less voltage than the buck produces?
3. Does 5.1 V × 5 A establish the input power requirement exactly?
4. What replaces the Pi during initial testing?

> [!question]- Answers
> 1. A bought isolated 48 V → 24 V module; its model is still open.
> 2. Current causes voltage drops in the complete output and return path.
> 3. No. It gives 25.5 W at the local output; input power also covers losses.
> 4. A dummy or electronic load, with controlled power and measurements.

> [!info]- Evidence and reading
> [Pinned sources and fact-check record](FACTCHECK_LOG.md#sources): CTX and MON explain the blocks; G4 and OWNER control the current 9–26 V requirement, architecture D decision and blocked freeze. IMG records the illustration context; its older part-selection statements are superseded. Neither drawing is a completed circuit or hardware result.

Previous: [[00-INDEX|Lesson index]] · Next: [[01 Input protection]] · Terms: [[99-Glossary]]
