---
title: "V1A inside the robot"
lesson: 8
tags: [v1a, lesson]
---

# 08 — V1A inside the robot

## Why this matters

V1A is intended to power one compute branch of the Wheel-Biped Robot (WBR).  
The upstream supply and the power harness affect that branch's behavior.  
Telemetry can explain its energy use, provided you know what is being measured.

## Follow the system boundary

The current integration concept is **13 series-connected battery cells (13S) → power distribution board (PDB) → bought isolated 48 V-to-24 V module → V1A → Raspberry Pi 5**. The Pi receives power through its general-purpose input/output (GPIO) header, as explained in [[05 Powering the Pi 5 through GPIO]]. This is the project context, not a complete specification of the robot's electrical system.

![[b5-standalone-v1a-and-future-integration-boundary.png|700]]

The picture separates V1A's five functions from the future robot interfaces. The isolated module's model, limits and fault behavior are **(still open)**. V1A remains a standalone Project II design; the dashed boundary does not add robot control or other power branches to it.

**REQUIREMENT:** upstream protection must prevent the battery voltage from passing through a failed converter into V1A. Isolation removes a direct conductive power path while its barrier is intact, but does not prove safe output voltage during every fault. Module fault testing, grounding and connected ports still need review. Source current, stored energy and shutdown behavior are **(still open)** inputs to V1A's protection review.

## What telemetry can tell the robot

The INA228 reports voltage, current, power and energy over **Inter-Integrated Circuit (I2C)**. Its 2 milliohm (mΩ) shunt measures V1A's contribution to the compute branch. Voltage is sensed at the board's load-side node relative to board ground, not across the distant Pi power pins.

A useful future log would pair readings with time, workload and monitor-reset events. It could compare energy used by two compute workloads. It would not measure the whole robot's battery consumption: upstream conversion losses and other branches are outside this measurement boundary. A power interruption also resets the monitor's accumulated energy; a missing interval cannot be counted as zero consumption. Logging and robot response policies are **(still open)**.

## Worked example — budget upstream power

**ASSUMPTION:** use the study's 5.1 V, 5 A output target and 90% V1A efficiency for an example.

**CALCULATION:** output power = 5.1 × 5 = **25.5 W**; input power = 25.5 / 0.90 = **28.3 W**. At a nominal 24 V input, that is about **1.18 A**.

The different input and output currents follow from power conversion. This is a sizing estimate, not measured efficiency or a module selection; other auxiliary loads require their own budget.

> [!warning] Common misconceptions
> “Isolated” does not mean all fault peaks are contained. I2C readings do not replace independent hardware protection or oscilloscope fault measurements. V1A also does not promise backup power or automatic robot recovery. Universal Serial Bus (USB) 3.x and D435i camera data do not pass through this board.

## Check yourself

1. Which block converts the robot's battery supply to the V1A input supply?
2. Why is INA228 energy not total robot energy?
3. Does a nominal 24 V module label establish its fault behavior?
4. What must happen before the Pi becomes a test load?

> [!question]- Answers
> 1. The bought isolated 48 V-to-24 V module; its exact model is still open.
> 2. It measures one branch and excludes upstream losses and other branches.
> 3. No. Actual voltage, current, stored energy and shutdown limits need evidence.
> 4. Complete the required engineering reviews and dummy-load bring-up, thermal, ripple, transient, protection and telemetry gates in lesson 07.

Sources: [project scope](../docs/context/01_PROJECT_OVERVIEW.md), [monitor boundary](../docs/evidence/r2/MONITOR_POWER_DOMAINS.md), [upstream interface study](../../wt-aux24/docs/evidence/aux_converter/AUX24_INTERFACE.md), and [current scope illustration brief](../../wt-illustrations/docs/illustrations/BATCH_B.md#b5--standalone-v1a-and-future-integration-boundary-replace).

Previous: [[07 Bench bring-up and fault-injection testing]] · Next reference: [[99-Glossary]] · [[00-INDEX|Lesson index]]
