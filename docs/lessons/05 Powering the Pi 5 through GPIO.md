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

$$
V_{DROP}=IR=5\times0.050=0.25\,\mathrm{V}
$$

$$
V_{Pi}=5.10-0.25=4.85\,\mathrm{V}
$$

$$
P_{PATH}=I^2R=25\times0.050=1.25\,\mathrm{W}
$$

Only 0.10 V remains above the minimum. Lower regulator voltage, hotter contacts or a load transient can consume it. This is not a qualified result; actual hot resistance and dynamic margins are **(still open)**. Raising the setpoint spends light-load and protection margin; it is not an approved fix.

The **current selected-parts screen** is different: Gate 4a retains the BSC034 series pair and calculates a **42.673 mΩ** loop with its improved harness assumptions. With a conditional **5.026 V** regulator minimum and assumed **20 mV** trough, that gives about **4.793 V** at 5 A. The older **35.073 mΩ** target assumed a different, lower-loss pair and cannot be claimed for this selection. Hot contacts and regulation are still unqualified; a 100 mV total-excursion sensitivity gives only **4.713 V**, below the minimum.

## Share current through the intended contacts

![[a5-pi-power-harness-boundary.png|700]]

The image shows grouping, not an assembly pinout. Its generic connector drawing is **not the selected J502 geometry**. **DECISION:** use both 5 V pins and all eight grounds, with a short **American Wire Gauge 16 (AWG16)** trunk and **AWG22 fan-out wires** at the Pi crimps. Gate 4a retains the proposed **Phoenix 1776508 header + 1777989 plug** at J502. Its footprint review does not qualify its complete hot resistance; the **≤3.12 mΩ per pole** budget remains **(still open)**.

**EVIDENCE — Pi-contact qualification FAIL:** the proposed Harwin **M20-1180042** contacts permit **30 mΩ after conditioning**, exceeding the path target of **≤20 mΩ per complete hot/conditioned mating contact**. The actual Pi male header and hot mate are also unqualified. This is a **failure to meet the documented acceptance criterion**, not a measured specimen failure. The generic picture's “not final” label must not hide this known finding.

For equal intact contacts, the target Pi interface contributes $R_{Pi}=(20/2+20/8)\,\mathrm{m\Omega}=12.5\,\mathrm{m\Omega}$, or **62.5 mV at 5 A**. Substituting 30 mΩ gives **93.75 mV**, an extra **31.25 mV** before any further hot effect. This calculation explains why the missing guarantee matters; it does not predict actual contact resistance.

**Physical pins:** 2 and 4 are 5 V; 6, 9, 14, 20, 25, 30, 34 and 39 are ground. Verify orientation against a checked assembly drawing. At 5 A with equal sharing, each positive contact carries 2.5 A; each ground carries 0.625 A. These are calculations, not ratings. Contact resistance differences change sharing.

The proposed Harwin housings span physical pins **1–20 and 25–40**; one 2×10 housing cannot reach all eight grounds. Retention, exact mating fit and continuity checks remain open. One open positive contact would put the full 5 A through the survivor, exceeding the cited 3 A female-contact rating; the assembled hot-pair rating still needs evidence.

## Why this design and not another

GPIO is the owner's chosen interface, so V1A must provide independent output protection. Keeping local regulation and the 2 mΩ shunt preserves the detector relationship and useful current signal. The path study favors reducing real switch/contact/wire losses: thicker wire alone cannot fix poor contacts, while a higher setpoint consumes overvoltage margin. Remote sensing would require a new feedback and fault review.

The owner selected **D for the test board**. E's extra Pi-end stage could protect the load endpoint more directly, but adds series loss and auxiliary wiring. D still needs far-end fault testing and qualified contacts. **Gate 4a freeze is BLOCKED; the Pi stays disconnected until fault tests and all other applicable gates pass.**

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

Sources: [pinned source register](FACTCHECK_LOG.md#sources), PATH for loss/current calculations; PI for the USB-C/GPIO distinction; VERIFY for the failed Harwin criterion and proposed harness map; G3 for the D/E comparison; BASIS and G4 for current owner choices and the blocked freeze. Earlier 35.073 mΩ/E recommendations are historical.

Previous: [[04 Monitoring]] · Next: [[06 PCB concepts]]
