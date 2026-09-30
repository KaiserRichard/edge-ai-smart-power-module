---
title: "V1A glossary"
lesson: 99
tags: [v1a, lesson]
---

# 99 — Glossary

## Why this matters

Short names help you read diagrams once you know what they mean.<br>
Similar words can describe very different protection functions.<br>
Use this page when a term interrupts your understanding of the system.

## System and measurement

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

## Conversion and protection

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

## Units and evidence

**mΩ** means milliohm: $1\,\mathrm{m\Omega}=0.001\,\Omega$. **µH** means microhenry; **µF** means microfarad. **µs** means microsecond; **µC** means microcoulomb, a unit of electric charge. The prefix **µ** means one millionth.

**CALCULATION:** a nominal 2 mΩ shunt carrying 5 A drops $V=IR=5\times0.002=0.010\,\mathrm{V}$, or **10 millivolts (mV)**. This excludes connector and wire drops.

**OBSERVATION/EVIDENCE** records what was found, with its source. **REQUIREMENT** states what must be achieved. **ASSUMPTION** supplies a provisional input; a **HYPOTHESIS** proposes behavior to test. **CALCULATION** derives a result from inputs. **DECISION** records a choice. **MEASURED** needs a physical test record. **OPEN RISK**, written **(still open)** here, needs more evidence or a decision.

**BLOCKED** means a gate cannot advance: Gate 4a has unresolved circuit contracts. **FAIL** names a specific unmet criterion: the Harwin contact selection does not satisfy the documented resistance target. That documentary FAIL is not a measured hardware failure. **Selected for qualification** means chosen for further engineering work, not already qualified.

> [!warning] Common misconceptions
> “Selected” does not mean “qualified.” “Calculated” does not mean “measured.”<br>
> Electrical rules check (ERC) and design rules check (DRC) test design rules; passing them does not establish electrical safety.<br>
> A component's headline current rating is not the assembled board's rating.

## Check yourself

1. What does a 2 mΩ shunt drop at 5 A?
2. Why is an OVP threshold different from a guaranteed voltage peak?
3. Why does the word “nominal” matter for an inductor?

> [!question]- Answers
> 1. 10 mV, using the stated resistance.
> 2. Voltage can continue rising during detection and turn-off; stored energy and wiring also matter.
> 3. Its inductance can change with current and temperature, especially during faults.

> [!info]- Evidence and reading
> [Pinned source register](FACTCHECK_LOG.md#sources): CTX for scope/evidence vocabulary; BUCK and MON for conversion/measurement; AUX for isolation; G2C and G4 for latch and blocked-freeze limits; VERIFY for the contact FAIL. Older captured selections do not supersede current owner decisions.<br>
> This reference page needs no illustration; examples and terms link the other lessons together.

Previous: [[08 V1A inside the robot]] · Next: [[00 System overview]]
