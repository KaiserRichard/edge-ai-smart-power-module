---
title: Powering the Pi 5 through GPIO
lesson: 5
tags: [v1a, lesson]
---

# 05 — Powering the Pi 5 through general-purpose input/output (GPIO)

## Why this matters

The Pi receives the voltage left after every connection and wire loses some.  
Header power depends on V1A's own output protection.  
The complete delivery path must pass dummy-load tests before the Pi is connected.

## The two voltage boundaries

**General-purpose input/output (GPIO) header power** uses the header's **5 volt (V) and ground (GND) pins**, never its signal pins. It bypasses the Pi's **Universal Serial Bus Type-C (USB-C)** input overvoltage protection.

**REQUIREMENT:** at least **4.75 V at the loaded Pi header**, relative to its ground, and a **peak strictly below 5.5 V**, including overshoot. These are project acceptance boundaries. A Pi damage-versus-time curve and demonstrated compliance are **(still open)**; no brief higher pulse is allowed.

## Count the complete voltage-drop chain

The buck regulates locally at about 5.1 V, before the output disconnect and shunt:

```text
Buck → disconnect → shunt → copper → J502 connector
     → harness → Pi 5 V contacts → load
     → Pi ground contacts → return harness → module ground
```

Every resistance in that loop consumes voltage. Measuring at J502 misses harness losses and the rise of Pi ground relative to module ground. Check the intended header endpoint with a representative dummy-load fixture first.

**CALCULATION — teaching example:** assume 5.10 V at the buck and 50 milliohms (mΩ) for the complete loop at 5 amperes (A).

```text
Drop = I × R = 5 × 0.050 = 0.25 V
Pi-end voltage = 5.10 − 0.25 = 4.85 V
Path heating = I² × R = 25 × 0.050 = 1.25 W
```

Only 0.10 V remains above the minimum. Lower regulator voltage, hotter contacts or a load transient can consume it. This is not a qualified result; actual hot resistance and dynamic margins are **(still open)**. Raising the setpoint spends light-load and protection margin; it is not an approved fix.

## Share current through the intended contacts

![[a5-pi-power-harness-boundary.png|700]]

The image shows grouping, not an assembly pinout. **DECISION:** both 5 V pins and all eight grounds, with a short **American Wire Gauge 16 (AWG16)** harness trunk. J502 is not final. Fan-out, mating contacts, retention and hot ratings remain **(still open)**.

**Physical pins:** 2 and 4 are 5 V; 6, 9, 14, 20, 25, 30, 34 and 39 are ground. Verify orientation against a checked assembly drawing. At 5 A with equal sharing, each positive contact carries 2.5 A; each ground carries 0.625 A. These are calculations, not ratings. Contact resistance differences change sharing.

> [!warning] Common misconceptions
>
> - More ground pins cannot cure an overloaded positive contact.
> - Thicker wire does not remove connector or protection-switch losses.
> - A firmware supply-current setting creates neither current capacity nor protection.
> - Never attach the Pi for fault injection; architecture D is still a preliminary test board.

## Check yourself

1. Why count ground-wire resistance?
2. Where must the 4.75 V minimum be checked?
3. Is 2.5 A per positive pin a guaranteed current rating?
4. Does “strictly below 5.5 V” permit a short 5.6 V spike?

> [!question]- Answers
>
> 1. Return current also loses voltage; the load sees the difference between its own supply and ground.
> 2. At the loaded Pi header endpoint, relative to its loaded ground contacts.
> 3. No. It assumes equal sharing; the complete hot mating interface still needs qualification.
> 4. No. Peak voltage includes brief excursions.

Sources: [path budget](../../wt-pathbudget/docs/evidence/r2/path_budget/PATH_BUDGET.md) (`ebe51b9`); [Pi fault envelope](../../v1a-wt-pi5-envelope/docs/evidence/r2/pi5_input_envelope_2026-09-29/PI5_INPUT_FAULT_ENVELOPE.md); [owner decision](../../wt-illustrations/docs/illustrations/IMAGE_AUDIT.md), which supersedes older harness choices and the report's architecture-E recommendation.

Previous: [[04 Monitoring]] · Next: [[06 PCB concepts]]
