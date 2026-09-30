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

Start with **PDF page 6, LOAD OUTPUT / J502 pins 1 (+) and 2 (RETURN)**. The V1A drawing ends at this two-terminal module connector; it does **not** contain a Raspberry Pi 40-pin header or a released external harness pinout. Use the [schematic reading guide](SCHEMATIC_READING_GUIDE.md) to keep PDF pages, connector pin numbers and Pi physical pin numbers separate.

![[v2-review-p06.png|1000]]
*Unchanged PDF page 6. J501 is the input, J502 the load-power output, and J503 the host-reference/I2C interface.*

![[v2-05-circuit-connectors.png|950]]
*Exact connector subset. J502 pin 1 is load power; **J503 pin 1 is GND**. Reusing a pin number on different connectors does not join those pins or give them the same function.*

![[f5-04-output-connectors-circuit.png|900]]
*Circuit companion F5.4 in [BATCH_F](../illustrations/BATCH_F.md). Run `python3 -B docs/lessons/figures/src/circuit_05.py` for the exact excerpt.*

![[f5-02-gpio-pin-map-power.png|650]]
*BATCH_F F5.2. Physical numbering, viewed in the illustrated orientation: pin 1 at top left. The picture is a learning map, not a released mating-face assembly drawing.*

**General-purpose input/output (GPIO)** names the whole header, but V1A uses its dedicated **5 V and ground power pins**. Never apply the supply through a signal or 3.3 V pin. This path bypasses the Pi's **Universal Serial Bus Type-C (USB-C) input overvoltage protection**, which is why V1A requires independent protection.

| Function | Physical pins | Equal-share current at 5 A |
|---|---|---:|
| Positive supply | **2, 4** | 2.5 A each |
| Ground return | **6, 9, 14, 20, 25, 30, 34, 39** | 0.625 A each |

These currents are calculations, not contact ratings. A wire-entry view can mirror the mating-face view; verify indexing, orientation and continuity with power removed. Both positive connections and all eight grounds are the intended arrangement.

Read the intended external mapping as **J502 pin 1 → Pi physical pins 2 and 4**, and **J502 pin 2 → the eight physical GND pins above**. That mapping is a reviewed requirement/proposal outside the PDF, not a newly drawn connector in it. **Pi physical pin 1 is a 3.3 V pin, not J502's positive pin.** The early fixture uses a representative dummy header in place of the Pi.

## 3. Trace both halves of the loop

![[a5-pi-power-harness-boundary.png|850]]
*Existing A5 shows functional grouping. Its generic connector is not the selected two-pole J502 geometry; its “not final” wording must not hide the known Harwin resistance failure.*

Follow positive current from local buck output through the series disconnect, shunt, PCB copper, J502, harness and Pi positive contacts. Then follow the same total current back through Pi ground contacts, return wires, connector and module ground.

Use these stops in the PDF while tracing that sentence:

| Stop | Page, block and pins | How to read it |
|---|---|---|
| Local regulation | Page 3, OUTPUT / FEEDBACK: **L201 pin 2; R202 pin 1** | Both join raw `VOUT_5V1`. The buck senses this node, before downstream drops. |
| Series pair | Page 4, OPPOSED SERIES FETS: **Q301 drains 5–8 → sources 1–3 → Q302 sources 1–3 → drains 5–8** | Shared sources are `PROT_MID`; the outer output is `VOUT_PROTECTED`. No bypass wire joins the outer rails. |
| Current shunt | Page 5, KELVIN SHUNT: **R401 force pin 1→4** | This is a further series drop; output becomes `LOAD_5V1`. Sense pins 2/3 carry no load current. |
| Module exit | Page 6, LOAD OUTPUT: **J502 pin 1→external harness** | The harness and Pi contacts are outside the captured sheet. A net label cannot specify their resistance. |
| Return | Page 6, **J502 pin 2 GND**, back to page 3 **U201 PGND pins 9/11** | The common net still needs actual copper, connector and wire resistance in the loop budget. |

Page 4 shows the earlier preliminary pair/crowbar. The **revised architecture D series/crowbar/control arrangement is frozen on paper, not yet in the schematic**; its later resistor/driver assumptions cannot be inferred from the old drawing. The raw dump is also absent from this snapshot.

$$
V_{Pi}=V_{buck}-I(R_{send}+R_{return})-V_{dynamic\ trough}
$$

The Pi cares about its own positive pin **relative to its own loaded ground**. Measuring only at J502 misses both the outgoing cable drop and the rise of the distant ground potential.

The INA228 bus-voltage tap is before this external harness. Its reading cannot substitute for the far-end differential measurement. Lesson 07 shows where to put the probes on a dummy-header fixture.

## 4. Worked example: build the drop budget

**Endpoints for this calculation:** begin at **page 3 L201 pin 2** against local GND; pass **page 6 J502 pins 1/2**; end across the **external dummy/Pi power and return contacts**. The far-end voltage is not a node drawn in this PDF. Every resistance allocation below refers to that complete trip, including the return.

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

**Page 6 J502 pin 1 is one electrical net before the external positive fan-out; pin 2 is the collected return.** The two positive branches and eight ground branches appear only in the proposed harness map. The PDF's single wire does not prove equal branch resistance or sharing.

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

**Snapshot check — page 6 J502 pins 1/2:** the generic symbol specifies the two nets, not the eventual mating geometry. In the later Gate 4a-FIX record at `2b99ac7`, **J502 is PENDING** its separate handoff. “Retained Phoenix” above names the inherited budget/proposal; it is not a completed current connector freeze.

The separately requested connector report, pinned at **`4ff92f3`**, proposes a new external assembly. It is useful new evidence, not an automatically accepted change to the inherited budget:

| Version | Pi end / fan-outs | Module side | Meaning of its numbers |
|---|---|---|---|
| Inherited Gate 4a screen used above | Harwin criterion unresolved; AWG22 | Phoenix proposal; retained BSC034 pair | **42.673 mΩ / 4.793 V**, conditional |
| Connector proposal A | **TE 3-87456-6** full 2×20 housing, ten **87309-9** sockets; **AWG20** fan-outs | Retain Phoenix | With retained 13.6 mΩ pair and D: **41.856 mΩ / 4.797 V**, conditional |
| Connector proposal B | Same proposed TE Pi assembly | **Molex 42819-2213 + 42816-0212 + 42815-0042** | Larger interface; new footprint/assembly review needed; unqualified |

Proposal A's small improvement also relies on a **redefined combined contact-plus-female-crimp acceptance block**. It is not a measured gain and cannot be mixed term-by-term with the older mating-only allocation. TE's published system data does not guarantee the actual Pi male header's hot mate. Mixed mating, loaded adjacent pins, indexing, cooler clearance, wire fit, crimps and retention remain open.

The new full housing also occupies the header. Telemetry contacts would need an integrated reviewed map; an added stacking adapter would add contacts and losses. Keep these as proposals until the connector handoff is reconciled. The old Harwin FAIL remains historical evidence.

For telemetry, find **page 6 HOST I2C / J503 pins 1 GND, 2 VREF, 3 SDA and 4 SCL**. These are separate from J502's power terminals. Page 5 **U403 VCCA pin 1** expects the host reference from J503 pin 2; the lesson does not invent how extra contacts would fit into the proposed full Pi housing.

## 7. What goes wrong: the module looks good while the endpoint fails

**Compare measurement planes:** page 5 **U401 VBUS pin 8** observes `LOAD_5V1`, which reaches **page 6 TP503 pin 1 / J502 pin 1**. The real far-end measurement crosses the external positive contact **and its own return contact**. Referencing it to **TP504 pin 1 (module GND)** would omit the return-wire voltage difference.

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
