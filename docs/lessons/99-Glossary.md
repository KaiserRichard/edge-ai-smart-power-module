---
title: "V1A glossary"
lesson: 99
tags: [v1a, lesson]
---

# 99 — Glossary

> [!abstract] In one sentence
> This glossary is a map: each word points to a physical job, a measurement boundary or a kind of evidence.

## 1. An everyday picture: a map legend

![[f9-01-course-map.png|850]]
*BATCH_F F9.1. A map legend helps you understand the symbols before choosing a route; these words help you read the engineering without guessing.*

Read a term in three steps: **name the object**, **find its boundary**, then **ask what evidence supports the claim**. For example, “protected output” names a node after a protection stage. It does not establish that every fault has been contained. The lessons below provide the pictures and examples behind the terms.

**Learning goals:** distinguish similar protection words, translate the units, and avoid turning an assumption into a measured claim.

**Read a real example:** PDF **page 5, KELVIN SHUNT / MEASUREMENT, R401 force pins 1/4, sense pins 2/3 and U401 IN+ pin 10 / IN− pin 9**. `R401` is a **reference designator** (one component's identity); `10` is a **pin number**; `IN+` is the **pin's function**; `SHUNT_KPLUS` is a **net name**. The [schematic reading guide](SCHEMATIC_READING_GUIDE.md) explains how to follow these labels.

![[v2-04-circuit-sense-filter.png|850]]
*A circuit picture to attach the words to: the thin sense connections are different from the force path. Companion image prompt **F4.4**, `f4-04-kelvin-filter-circuit.png`, and runnable `figures/src/circuit_04.py` are shared with Lesson 04; no new circuit is invented for the glossary.*

## 2. System and measurement

| Term | Plain meaning in these lessons |
| --- | --- |
| DC — direct current | Power with a fixed polarity in normal operation; ripple can still be present. |
| 13S — 13 cells in series | The proposed battery arrangement in the integration context, not a frozen robot architecture or V1A input rating. |
| PDB — power distribution board | Splits source power into system branches. |
| WBR — Wheel-Biped Robot | The future robot integration context; V1A remains a standalone project. |
| GPIO — general-purpose input/output | The Pi header includes dedicated 5 V and ground power pins as well as signal pins. Power does not go through a signal pin. |
| GND — ground | A circuit's voltage reference and return network; current still needs a physical return path. |
| I2C — Inter-Integrated Circuit | The serial bus carrying monitoring data. |
| Galvanic isolation | Power or signals cross a barrier without a direct conductive path across that barrier. V1A requires an isolated upstream converter; its local TCA9517 I2C buffer is not an isolator. External connections and faults still need review. |
| Telemetry | Measurements reported to another device. INA228 is the monitoring chip's part number, not an abbreviation to expand. |
| Shunt / Kelvin sensing | A small resistor produces a current-dependent voltage. Separate sense connections read that voltage without including the power-trace drops. |
| PCB — printed circuit board | The physical interconnect and component support. V1A layout pictures are conceptual; no board is routed. |

## 3. Conversion and protection

| Term | Plain meaning in these lessons |
| --- | --- |
| Buck / duty cycle | A switching step-down converter / the fraction of a switching cycle spent in the high-side on state. |
| MOSFET — metal-oxide-semiconductor field-effect transistor | An electrically controlled switch. “High-side” means toward the positive supply; “low-side” means toward the return. |
| Inductor / saturation | A magnetic energy store / loss of inductance at high current, allowing current to rise faster. |
| Differential inductance | The inductance governing a small current change at the actual operating current; a nominal value alone does not bound fault behavior. |
| Ripple / transient | Repeated variation during operation / a change caused by an event such as startup or a load step. |
| Feedback | The controller senses output voltage and adjusts energy delivery to maintain its setpoint. |
| Hot loop | The compact path where switching rapidly changes current; “hot” here does not mean only high temperature. |
| Effective capacitance | Capacitance actually available under voltage, temperature, and tolerance conditions. |
| ESR — equivalent series resistance | A capacitor's resistive contribution to voltage steps, ripple, and heating. |
| Fuse / eFuse — electronic fuse | A melting element that interrupts sufficient overcurrent / a controlled semiconductor protection stage. Their response mechanisms differ. |
| TVS — transient voltage suppressor | Diverts surge current to limit voltage under specified conditions; not an exact voltage regulator. |
| UVLO — undervoltage lockout | Prevents operation below a supply threshold; turn-on and turn-off thresholds can differ. |
| OVP — overvoltage protection | Responds to excessive voltage. A trip threshold does not by itself specify the peak reached during the response. |
| Inrush / backfeed | A brief surge of startup current, often charging capacitors / power flowing backward into a source or unpowered block. |
| Latch / series disconnect | Stores a fault state while its supply is valid / opens the normal power path. Brownout, reset, current interruption and stored-energy disposal must also be checked. |
| Crowbar / ballast | A switched path that draws fault current away from the protected rail / resistance that limits and shares its pulse stress. |
| Source bound | A justified limit on fault voltage, current, charge, energy, and duration, including local stored energy. |
| SOA — safe operating area | Allowed combinations of transistor voltage, current, time, and temperature under stated conditions. |

## 4. Units and evidence

**mΩ** means milliohm: $1\,\mathrm{m\Omega}=0.001\,\Omega$. **µH** means microhenry; **µF** means microfarad. **µs** means microsecond; **µC** means microcoulomb, a unit of electric charge. The prefix **µ** means one millionth.

**CALCULATION:** a nominal 2 mΩ shunt carrying 5 A drops $V=IR=5\times0.002=0.010\,\mathrm{V}$, or **10 millivolts (mV)**. This excludes connector and wire drops.

**OBSERVATION/EVIDENCE** records what was found, with its source. **REQUIREMENT** states what must be achieved. **ASSUMPTION** supplies a provisional input; a **HYPOTHESIS** proposes behavior to test. **CALCULATION** derives a result from inputs. **DECISION** records a choice. **MEASURED** needs a physical test record. **OPEN RISK**, written **(still open)** here, needs more evidence or a decision.

**BLOCKED** means a gate cannot advance: Gate 4a has unresolved circuit contracts. **FAIL** names a specific unmet criterion: the Harwin contact selection does not satisfy the documented resistance target. That documentary FAIL is not a measured hardware failure. **Selected for qualification** means chosen for further engineering work, not already qualified.

> [!warning] Common misconceptions
> “Selected” does not mean “qualified.” “Calculated” does not mean “measured.”<br>
> Electrical rules check (ERC) and design rules check (DRC) test design rules; passing them does not establish electrical safety.<br>
> A component's headline current rating is not the assembled board's rating.

## 5. Worked example: connect the units to a picture

![[v2-04-shunt-signal-loss.png|850]]

At nominal 5 A through 2 mΩ:

Find that resistance at **page 5 R401**, with power current through **force pins 1→4** and voltage observed across **sense pins 2/3**. The filter delivers the differential signal to **U401 pins 10/9**; VBUS pin 8 is a separate voltage measurement.

$$
V=IR=5\times0.002=0.010\ \mathrm{V}=10\ \mathrm{mV}
$$

$$
P=I^2R=25\times0.002=0.050\ \mathrm{W}=50\ \mathrm{mW}
$$

Read the straight line for voltage and the curved line for heating. A factor of two in current makes twice the voltage drop but four times the dissipation. The formulas are **CALCULATIONS**; the nominal resistance is an input; the actual hot temperature and accuracy require **MEASURED** evidence.

## 6. What goes wrong: treating a boundary as a guarantee

![[v2-p03-09-voltage-ladder.png|850]]

The preliminary trip threshold, a conditional modeled peak and the project limit are different marks on this ruler. An **OVP threshold** says when a detector responds. **Let-through** is what happens during the remaining delay and energy transfer. A **requirement** states what must be met; it is not proof that the circuit meets it. The historical 5.542 V counterexample stays visible because evidence cannot be erased by a later architecture decision.

## 7. Why this design and not another

The course separates power conversion, fault containment and monitoring so each claim has a clear boundary. It uses **ASSUMED**, **CALCULATED**, **MEASURED**, **OPEN** and **BLOCKED** instead of treating every precise-looking number alike. This vocabulary lets a reviewer say exactly what remains to be proved without confusing a component choice with qualification.

## 8. Check yourself

1. What does a 2 mΩ shunt drop at 5 A?
2. Why is an OVP threshold different from a guaranteed voltage peak?
3. Why does the word “nominal” matter for an inductor?

> [!question]- Answers
> 1. 10 mV, using the stated resistance.
> 2. Voltage can continue rising during detection and turn-off; stored energy and wiring also matter.
> 3. Its inductance can change with current and temperature, especially during faults.

## 9. One-page visual summary

| Word family | Picture / example | Ask yourself |
|---|---|---|
| Voltage / current / power / energy | Pressure / flow / delivery rate / accumulated delivery | Which units and which time interval? |
| Input / raw / protected / load | Different locations in the power path | Exactly where is the voltage measured? |
| Fuse / TVS / eFuse | Clear overcurrent / divert surge / controlled admission | Which fault, duration and source limit? |
| Comparator / latch / disconnect / dump | Detect / remember / cut / dispose | Does the control power survive the event? |
| Kelvin / force / sense | Load path versus observation taps | Did unwanted copper enter the measurement? |
| ASSUMED / CALCULATED / MEASURED | Input / arithmetic / physical evidence | What supports the claim? |
| BLOCKED / FAIL / selected | Gate status / unmet criterion / development choice | Has the exact criterion actually closed? |

**Current boundary:** 9–26 V input; architecture D test board; Gate 4a-FIX BLOCKED; no Pi before required gates pass. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

> [!info]- Evidence and reading
> [Pinned source register](FACTCHECK_LOG.md#sources): CTX for scope/evidence vocabulary; BUCK and MON for conversion/measurement; AUX for isolation; G2C and G4 for latch and blocked-freeze limits; VERIFY for the contact FAIL. Older captured selections do not supersede current owner decisions.<br>
> This visual reference reuses lesson charts; those charts remain conditional teaching examples, not new evidence. See [visual rebuild record](VISUAL_REBUILD_LOG.md).

Previous: [[08 V1A inside the robot]] · Next: [[00 System overview]]
