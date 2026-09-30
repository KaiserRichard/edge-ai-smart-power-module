---
title: "Monitoring"
lesson: 4
tags: [v1a, lesson, visual]
---

# 04 — Monitoring

> [!abstract] In one sentence
> A small known resistance turns load current into a measurable voltage, but the wiring and measurement boundary decide what the resulting numbers mean.

## 1. An everyday picture: a water meter sees one pipe

![[f4-02-measurement-boundary.png|850]]
*BATCH_F F4.2. Think of a meter in one branch pipe. The teal bubble highlights the shunt and load-side voltage tap; it does not mean the monitor measures the connector's loss.*

A house water meter records water passing through that house's pipe. It cannot tell you how much water the entire town uses, or the pressure lost in every pipe after it. V1A's monitor has the same boundary problem: it measures current through **its shunt** and voltage at **its own voltage tap**.

A shunt is a deliberately small resistance. Current makes a small voltage across it. The INA228 measures that voltage and uses the configured resistance to calculate current. It also reads the load-side module voltage, allowing power and energy calculations.

**Learning goals:** follow force and sense connections; calculate signal and heating; distinguish range from accuracy; explain the I2C supply boundary and an energy-log reset gap.

> [!warning] Status
> Architecture D remains a preliminary test board. **Gate 4a-FIX freeze BLOCKED — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Application margins remain **(still open)**. No measured monitoring accuracy is claimed.

## 2. Picture walkthrough: two power terminals and two sense terminals

![[f4-01-kelvin-sense-3d.png|900]]
*BATCH_F F4.1. The package and chip geometry are generic. Use the reviewed footprint mapping below, not the drawing, for actual pad identity.*

Read the picture in three passes:

1. **Thick blue path:** load current enters a force terminal, crosses the resistive element and leaves through the other force terminal.
2. **Thin teal pair:** the sense terminals read the voltage across the intended element. They do not carry the load current. Small input bias currents still exist; “sense” does not mean a physically impossible zero-current wire.
3. **Monitor:** the INA228 receives both sense connections. A separate bus-voltage connection reads `LOAD_5V1` relative to module ground; it is not drawn as a third shunt terminal.

The selected R401 is **WSL27262L000FEA**, nominal **2 mΩ**, with four-terminal **Kelvin sensing**.

| Reviewed pad | Connection | Role |
|---|---|---|
| 1 | `VOUT_PROTECTED` | FORCE+ |
| 2 | `SHUNT_KPLUS` | SENSE+ |
| 3 | `SHUNT_KMINUS` | SENSE− |
| 4 | `LOAD_5V1` | FORCE− |

Separate sense taps exclude the intended high-current connection drops. They must begin at the dedicated sense terminals, run together and avoid switching noise. A copper pour around the resistor must not create a second load-current path that bypasses it.

## 3. Worked example: 5 A becomes only 10 mV

![[v2-04-shunt-signal-loss.png|900]]

Use the nominal resistor value, not an assumed perfect installed calibration:

$$
V_{shunt}=IR=5\times0.002=0.010\ \mathrm{V}=10\ \mathrm{mV}
$$

$$
P_{shunt}=I^2R=5^2\times0.002=0.050\ \mathrm{W}=50\ \mathrm{mW}
$$

Read the two plots separately. Signal grows linearly with current, while heating grows with current squared. The 50 mW arithmetic does not establish the resistor's temperature; its board and thermal path matter.

Now suppose the sense taps accidentally include an **ASSUMED extra 1 mΩ** of power copper. At 5 A the sensed voltage becomes $5\times0.003=15\ \mathrm{mV}$. Firmware still dividing by 2 mΩ reports

$$
I_{reported}=\frac{0.015}{0.002}=7.5\ \mathrm{A}
$$

That is **50% high**, even if the converter inside the INA228 measured voltage perfectly. Better digital resolution cannot correct the wrong physical boundary.

## 4. Range and accuracy answer different questions

| Question | Number or evidence | Meaning |
|---|---|---|
| How large is the nominal 5 A signal? | 10 mV | A useful reference for noise/error review |
| What shunt tolerance was reviewed? | ±1% initial | Actual resistance can differ from its label |
| How temperature-sensitive is it? | ±25 ppm/°C temperature coefficient | Resistance drift must enter the accuracy budget |
| What is the selected small shunt-input range? | ±40.96 mV with `ADCRANGE=1` | Analog measurement range, not board-current capability |
| What accuracy is required and achieved? | **(still open)** | Needs a requirement, calibration and bench evidence |

Using nominal resistance, the range corresponds to

$$
I_{range}=\frac{40.96\ \mathrm{mV}}{2\ \mathrm{m\Omega}}=20.48\ \mathrm{A}
$$

This does **not** authorize ±20.48 A through the board. Firmware scaling must match the chosen range and shunt. The range and accumulator behavior are documented in the [TI INA228 datasheet, SLYS021A](https://www.ti.com/lit/ds/symlink/ina228.pdf).

For perspective, an **assumed 40°C shunt rise** with a 25 ppm/°C coefficient magnitude corresponds to $40\times25=1000$ ppm, or **0.1% resistance change**. That is a temperature sensitivity, not a measured temperature or total accuracy. Initial tolerance, amplifier offset/gain, noise and calibration remain separate terms.

## 5. Data crosses a bridge; power does not come from the host

![[f4-03-i2c-two-islands.png|850]]
*BATCH_F F4.3. Separate islands mean separately powered bus segments. The drawn shared ground is deliberate: this is not galvanic isolation.*

**Inter-Integrated Circuit (I2C)** uses serial data (**SDA**) and clock (**SCL**). The captured TPS70933 creates the monitor's local 3.3 V supply from `VOUT_PROTECTED`. The TCA9517 buffer joins the local and host bus segments. Each has pull-ups to its own supply, with common ground.

The buffer does not power the host. Existing host pull-ups must be counted in the bus design; adding another set blindly changes the loading. Powered-off behavior and signal timing remain **(still open)**. Supply order matters: the host can remain powered when V1A's monitor rail disappears.

```mermaid
flowchart LR
    S["Sense shunt + local load-side voltage"] --> C["Configured INA228 conversion"]
    C --> I["I2C transfer through TCA9517"]
    I --> H["Host stores value, time and validity"]
```

This flow is telemetry. Independent hardware protection in Lesson 03 cannot wait for the host to poll, interpret and react to a microsecond fault.

## 6. What goes wrong: a convincing number with missing context

![[v2-04-energy-reset-gap.png|850]]

The graph assumes **10 W for 60 s**, with the monitor unavailable from **25 to 35 s**. This special teaching case assumes the load remains powered externally during the monitor outage. It is not a prediction of V1A's shutdown sequence.

The true hypothetical energy is $10\times60=600\ \mathrm{J}$. The device accumulator resets with monitor power loss; it does not remember the first interval. Even software joining the two observed intervals has only $250+250=500\ \mathrm{J}$ of observed energy and a **100 J unobserved interval** in this example. It cannot fill a real missing interval with zero without evidence.

The energy register is also not automatically signed net energy under reverse current. Record direction, register/reset behavior, sample time, configuration and gaps before drawing a battery-energy conclusion.

There is another easy mistake: $V_{LOAD\_5V1}I_{shunt}$ gives power at the module's load-side plane. It includes power later lost in the harness; it does not give actual Pi power. Local monitor power branches **before** the shunt and upstream conversion losses are outside this measurement. Whole-module efficiency needs additional input and output measurements.

## 7. Why this design and not another

The 2 mΩ shunt gives a small delivery-path drop and a measurable current signal. Increasing it would enlarge the signal but spend more voltage and heat; reducing it would make offset and routing errors more significant. The four-terminal package directly addresses the small-signal routing problem. INA228 provides the selected digital telemetry function, while the separately powered bus segments preserve explicit supply ownership. None of these choices replaces calibration or independent fault containment.

> [!warning] Common misconceptions
> More displayed digits do not prove accuracy. An ADC range is not a board rating. A buffer is not an isolator. A module-side voltage does not establish the far-end voltage. A reset energy accumulator is not a continuous energy history.

## 8. Check yourself

1. Why do two sense terminals improve the measurement?
2. What does the nominal shunt dissipate at 5 A?
3. If the wrong taps read 15 mV, what does 2 mΩ scaling report?
4. Can the log silently replace a missing interval with zero energy?

> [!question]- Answers
> 1. They avoid including the intended load-connection voltage drops in the sensed resistor voltage.
> 2. 50 mW; temperature still requires its thermal context.
> 3. 7.5 A, despite the example's actual 5 A.
> 4. No. Record a gap/reset and any justified estimate separately from observed energy.

## 9. One-page visual summary

![[f4-01-kelvin-sense-3d.png|650]]

| Read the measurement as… | Do not read it as… |
|---|---|
| Current through **this 2 mΩ shunt** | Current in every robot branch |
| **10 mV / 50 mW** at nominal 5 A | A temperature or accuracy result |
| Voltage at **LOAD_5V1 against module ground** | Voltage across the distant Pi header |
| Energy over **valid, powered measurement intervals** | Unbroken battery-energy history |
| I2C data through a **shared-ground buffer** | Isolation or hardware protection |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): MON, INA, FP and G4; Gate 4a-FIX `2b99ac7` for status. The old empty-Sheet-03 statement in MON is historical. [BATCH_F](../illustrations/BATCH_F.md) F4.1–F4.3 owns the illustrations. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 04`.

Previous: [[03b Output protection margins and proof]] · Next: [[05 Powering the Pi 5 through GPIO]] · Terms: [[99-Glossary]]
