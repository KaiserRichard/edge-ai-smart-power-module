---
title: Monitoring
lesson: 4
tags: [v1a, lesson]
---

# 04 — Monitoring

## Why this matters

Voltage alone does not tell you how much power a load uses.  
A small shunt lets V1A measure current with little voltage loss.  
Knowing the measurement boundary prevents misleading power and energy claims.

## Where the measurement happens

**OBSERVATION:** the captured path is output protection → R401 shunt → load connector. A shunt is a small, known resistance. The INA228 measures its voltage drop to calculate current, and the load-side voltage to calculate power.

![[d3-v1a-circuit-anatomy-without-fake-hardware.png|700]]

The image separates power flow from sensing and test access. Its single “shunt sense” arrow is simplified: current needs two Kelvin sense connections, and bus voltage needs a separate connection to `LOAD_5V1`. No printed circuit board (PCB) is routed. Architecture D remains a preliminary fault-test board; **Gate 4a freeze is BLOCKED** and application margins are **(still open)**.

## Why four-terminal Kelvin sensing matters

R401 is a **2 milliohm (mΩ)** four-terminal shunt. Two **force terminals** carry load current. Two **sense terminals** measure directly across the resistor, excluding extra drop in high-current connections. This is **Kelvin sensing**.

The sense traces must start at those sense terminals, stay together, and avoid the noisy switching area. Arbitrary taps on nearby power copper change the measurement boundary.

**CALCULATION — nominal 5 ampere (A) example:**

$$
V_{SHUNT}=IR=5\times0.002=0.010\,\mathrm{V}=10\,\mathrm{mV}
$$

$$
P_{SHUNT}=I^2R=5^2\times0.002=0.050\,\mathrm{W}=50\,\mathrm{mW}
$$

A small resistance wastes little power but produces a small signal. The reviewed shunt has ±1% initial tolerance and a temperature coefficient of ±25 parts per million per degree Celsius. Amplifier error, routing and calibration also affect accuracy. The accuracy requirement and measured result are **(still open)**.

With the INA228's `ADCRANGE=1` setting, its ±40.96 mV shunt-input range corresponds to $40.96\,\mathrm{mV}/2\,\mathrm{m\Omega}=20.48\,\mathrm{A}$ in each direction using nominal resistance. This is a measurement-range calculation, **not a ±20.48 A board rating**. Firmware scaling/calibration must match the shunt and chosen range.

## What reaches the host

The INA228 sends readings through **Inter-Integrated Circuit (I2C)**: serial data and clock lines. The monitor has a local 3.3 volt (V) supply. A TCA9517 buffer connects separately powered local and host bus segments; each side has pull-ups to its own supply, with shared ground. **It is not galvanic isolation and does not power the host.** Existing host pull-ups must be included in the bus check. Powered-off behavior and signal timing are **(still open)** pending bench checks.

Current means current crossing **this shunt**. Voltage means the load-side node relative to module ground, before the harness. Monitoring power branches before the shunt. These readings exclude upstream conversion losses and do not establish whole-module efficiency or actual Pi voltage.

Energy accumulates power over time. Monitor power loss resets accumulation and leaves a gap that software must record. The energy accumulator is not automatically signed net energy when current reverses.

> [!warning] Common misconceptions
>
> - A precise-looking digital value is not proof of measurement accuracy.
> - Monitoring is not the independent hardware fault protection from Lesson 03.
> - A good module-voltage reading does not prove a good Pi-end voltage.

## Check yourself

1. What voltage does the nominal shunt produce at 5 A?
2. Why use separate force and sense terminals?
3. Does the INA228 measure the external harness voltage drop?
4. Can an energy total continue reliably through a monitor power loss?

> [!question]- Answers
>
> 1. 10 mV; nominal shunt heating is 50 mW.
> 2. To keep load-path connection drops out of the intended shunt measurement.
> 3. No. Its voltage measurement is at the module, relative to module ground.
> 4. No. Accumulation resets and the unpowered interval is a measurement gap.

Sources: [pinned source register](FACTCHECK_LOG.md#sources), MON and INA for measurement/domain behavior; G4 for the blocked freeze. The monitor review's old empty-Sheet-03 statement is historical. The manufacturer range does not establish assembled-board accuracy or fault survival.

Previous: [[03 Output protection]] · Next: [[05 Powering the Pi 5 through GPIO]]
