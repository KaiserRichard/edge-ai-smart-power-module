---
title: "Powering the Pi 5 through GPIO"
lesson: 5
tags: [v1a, lesson, visual]
---

# 05 — Powering the Pi 5 through GPIO

> [!abstract] In one sentence
> The computer receives the voltage left after the complete positive-and-return path loses some; parallel contacts help only when the actual assembled connections are qualified.

## 1. An everyday picture: walking down a staircase

![[f5-01-voltage-staircase.png|850]]
*BATCH_F F5.1. Each step is a voltage cost. The return path is included even though it is usually called “ground.” Step heights are illustrative; use the chart for numbers.*

You begin at the top with a small height allowance. Every step brings you closer to the minimum acceptable level. A thicker wire can reduce one step, but it does nothing to a poor connector or resistive protection switch elsewhere.

At a nominal 5.10 V starting point and a 4.75 V minimum, the entire allowance is only **350 mV**. Regulator tolerance, load transients and every series resistance compete for that allowance.

**Learning goals:** identify the intended power pins; calculate the complete loop drop; explain unequal sharing; distinguish a proposed connector from a qualified hot assembly.

> [!warning] Status and boundaries
> **REQUIREMENT:** at the loaded Pi header, at least **4.75 V at 5 A**, and peak **strictly below 5.5 V**, including overshoot. Compliance and any Pi damage-versus-time curve are **(still open)**; no higher brief pulse is allowed. **Gate 4a-FIX BLOCKED — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** No Pi before required fault and other qualification gates pass.

## 2. Picture walkthrough: power pins are not signal pins

![[f5-02-gpio-pin-map-power.png|650]]
*BATCH_F F5.2. Physical numbering, viewed in the illustrated orientation: pin 1 at top left. The picture is a learning map, not a released mating-face assembly drawing.*

**General-purpose input/output (GPIO)** names the whole header, but V1A uses its dedicated **5 V and ground power pins**. Never apply the supply through a signal or 3.3 V pin. This path bypasses the Pi's **Universal Serial Bus Type-C (USB-C) input overvoltage protection**, which is why V1A requires independent protection.

| Function | Physical pins | Equal-share current at 5 A |
|---|---|---:|
| Positive supply | **2, 4** | 2.5 A each |
| Ground return | **6, 9, 14, 20, 25, 30, 34, 39** | 0.625 A each |

These currents are calculations, not contact ratings. A wire-entry view can mirror the mating-face view; verify indexing, orientation and continuity with power removed. Both positive connections and all eight grounds are the intended arrangement.

## 3. Trace both halves of the loop

![[a5-pi-power-harness-boundary.png|850]]
*Existing A5 shows functional grouping. Its generic connector is not the selected two-pole J502 geometry; its “not final” wording must not hide the known Harwin resistance failure.*

Follow positive current from local buck output through the series disconnect, shunt, PCB copper, J502, harness and Pi positive contacts. Then follow the same total current back through Pi ground contacts, return wires, connector and module ground.

$$
V_{Pi}=V_{buck}-I(R_{send}+R_{return})-V_{dynamic\ trough}
$$

The Pi cares about its own positive pin **relative to its own loaded ground**. Measuring only at J502 misses both the outgoing cable drop and the rise of the distant ground potential.

The INA228 bus-voltage tap is before this external harness. Its reading cannot substitute for the far-end differential measurement. Lesson 07 shows where to put the probes on a dummy-header fixture.

## 4. Worked example: build the drop budget

![[v2-05-full-drop-budget.png|900]]

Read the waterfall left to right. It begins at **5.100 V nominal**, reserves the conditional regulator corner down to **5.026143 V**, subtracts the full loop's resistive loss, then an assumed transient trough.

The inherited **retained-BSC034-pair** screen uses **42.673 mΩ** total loop resistance. At 5 A:

$$
V_{resistive}=5\times0.042673=0.213365\ \mathrm{V}
$$

$$
V_{Pi}=5.026143-0.213365-0.020\approx4.793\ \mathrm{V}
$$

That leaves only **43 mV** above 4.75 V. The path also dissipates about $5^2\times0.042673=1.067\ \mathrm{W}$, spread among the parts.

![[v2-p03-10-drop-budget.png|900]]
*The pilot-derived detailed allocation. The large steps are the preliminary **13.6 mΩ hot series pair** and the assumed Pi contact/termination block. J502's complete hot resistance remains pending qualification.*

These are conditional arithmetic results. Actual hot resistance and dynamic margins are **(still open)**. If the total trough were **100 mV instead of 20 mV**, the same path gives **4.713 V**, below the minimum. Do not subtract both troughs: they are alternative cases.

For comparison, a simple **ASSUMED 50 mΩ loop** at exactly 5.10 V gives $5.10-5\times0.050=4.85\ \mathrm{V}$ and $25\times0.050=1.25\ \mathrm{W}$ loss before any extra transient allowance. Starting from the nominal voltage hides the lower regulation corner.

## 5. Contacts: resistance decides how current shares

![[f5-03-current-sharing-lanes.png|850]]
*BATCH_F F5.3. The inset shows a positive contact opening. “Doubles” assumes the two original branches shared equally.*

![[v2-05-contact-sharing.png|900]]

For two parallel positive branches, the lower-resistance branch carries more current:

$$
I_1=I_{total}\frac{R_2}{R_1+R_2}
$$

With **ASSUMED 20 and 30 mΩ complete branches**, 5 A divides as **3 A and 2 A**, not 2.5 A each. With one positive branch open, the survivor carries the full 5 A. That exceeds the cited **3 A female-contact test rating**; the actual hot Pi mating-pair rating remains unqualified. Eight good grounds cannot fix an overloaded positive pin.

For equal contact resistances alone, two positives and eight grounds give

$$
R_{contacts}=\frac{R_{one}}{2}+\frac{R_{one}}{8}
$$

At **20 mΩ each**, this is 12.5 mΩ, or **62.5 mV at 5 A**. At **30 mΩ each**, it becomes **93.75 mV**—an extra **31.25 mV**. These examples exclude separate wire/crimp differences and are not measured hot resistance.

## 6. Selection status: keep the old failure and new proposals distinct

**EVIDENCE — documentary FAIL:** Harwin **M20-1180042** permits **30 mΩ after conditioning**, exceeding the specified **≤20 mΩ hot/conditioned mating-contact target**. That is a failure of the documented criterion, not proof that a measured specimen failed. The proposed two housings spanning **1–20 and 25–40** were needed because one 2×10 housing cannot reach all eight grounds.

The inherited path uses **American Wire Gauge (AWG)16 trunks with AWG22 fan-outs** and retains **Phoenix 1776508 header + 1777989 plug** as the J502 proposal. The **≤3.12 mΩ per complete hot pole** allocation remains **(still open)**; footprint geometry and a catalogue current rating cannot establish it.

The separately requested connector report, pinned at **`4ff92f3`**, proposes a new external assembly. It is useful new evidence, not an automatically accepted change to the inherited budget:

| Version | Pi end / fan-outs | Module side | Meaning of its numbers |
|---|---|---|---|
| Inherited Gate 4a screen used above | Harwin criterion unresolved; AWG22 | Phoenix proposal; retained BSC034 pair | **42.673 mΩ / 4.793 V**, conditional |
| Connector proposal A | **TE 3-87456-6** full 2×20 housing, ten **87309-9** sockets; **AWG20** fan-outs | Retain Phoenix | With retained 13.6 mΩ pair and D: **41.856 mΩ / 4.797 V**, conditional |
| Connector proposal B | Same proposed TE Pi assembly | **Molex 42819-2213 + 42816-0212 + 42815-0042** | Larger interface; new footprint/assembly review needed; unqualified |

Proposal A's small improvement also relies on a **redefined combined contact-plus-female-crimp acceptance block**. It is not a measured gain and cannot be mixed term-by-term with the older mating-only allocation. TE's published system data does not guarantee the actual Pi male header's hot mate. Mixed mating, loaded adjacent pins, indexing, cooler clearance, wire fit, crimps and retention remain open.

The new full housing also occupies the header. Telemetry contacts would need an integrated reviewed map; an added stacking adapter would add contacts and losses. Keep these as proposals until the connector handoff is reconciled. The old Harwin FAIL remains historical evidence.

## 7. What goes wrong: the module looks good while the endpoint fails

![[v2-p03-07-with-vs-without.png|850]]
*Pilot fault-model chart: ideal far end, **no harness model**. It explains why stopping source energy alone is insufficient; it cannot predict the actual Pi-header peak.*

A harness has inductance as well as resistance. A fast module-side clamp can leave current flowing into far-end capacitance, causing a different voltage there. The retained Gate 3b conditional counterexample reached **5.542 V at the far end**. Architecture D's favorable module screen therefore cannot establish the strict Pi peak requirement.

The same harness must pass both ends of the voltage problem: normal loaded minimum and fault peak. Lower resistance improves the DC budget but does not by itself prove acceptable ringing.

## 8. Why this design and not another

GPIO is the owner's chosen interface. Keep local feedback and the 2 mΩ shunt: changing the setpoint or remote-sensing point would reopen regulation and protection analysis. Raising the setpoint spends the narrow upper nuisance-trip margin explained in Lesson 03.

D keeps protection on V1A and avoids E's additional Pi-end stage. E observes the final endpoint more directly but adds resistance, hardware and auxiliary wiring. The owner chose **D for the test board**, with far-end fault and contact qualification still owed. The older **35.073 mΩ** budget assumed a lower-loss module pair and cannot be claimed for the retained pair.

> [!warning] Common misconceptions
> More grounds do not repair an overloaded positive contact. Thicker trunks do not qualify crimps or contacts. Equal sharing is an assumption. A firmware current setting creates no copper capacity. A favorable calculated voltage is not permission to connect the Pi.

## 9. Check yourself

1. Why must return resistance be included?
2. How much voltage does each extra 1 mΩ cost at 5 A?
3. What happens when one positive contact opens?
4. Did the new TE proposal erase the Harwin FAIL or qualify the Pi interface?

> [!question]- Answers
> 1. The load sees its positive voltage minus its own ground; return current creates a ground rise.
> 2. 5 mV, so apparently small resistances consume useful margin.
> 3. The surviving path can carry all 5 A; its rating and fault response cannot be assumed adequate.
> 4. No. It is a proposed replacement with its own unresolved hot mixed-mate and assembly evidence.

## 10. One-page visual summary

![[v2-05-full-drop-budget.png|700]]

| Boundary | Remember |
|---|---|
| Physical power pins | **2 and 4**, plus **all eight named grounds** |
| Normal / fault voltage | **≥4.75 V at 5 A / strictly <5.5 V peak** at the actual endpoint |
| Inherited selected-pair screen | **42.673 mΩ → 4.793 V** with assumed 20 mV trough |
| Harwin finding | **30 mΩ allowed >20 mΩ target: documentary FAIL** |
| New connector work | TE/AWG20 proposals require reconciliation and qualification |
| Test load | Representative **dummy header first; Pi disconnected** |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): PATH, PI, VERIFY, BASIS and G4. Later proposals: [J502 selection, `4ff92f3`](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/4ff92f3ef68822007642a0e2cbb09b351d043222/docs/evidence/r2/J502_SELECTION.md); inherited owner choice remains D with BSC034. [BATCH_F](../illustrations/BATCH_F.md) F5.1–F5.3. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 05`; detailed allocation reused from the pilot generator.

Previous: [[04 Monitoring]] · Next: [[06 PCB concepts]] · Terms: [[99-Glossary]]
