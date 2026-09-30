---
title: "PCB concepts"
lesson: 6
tags: [v1a, lesson, visual]
---

# 06 — Printed circuit board concepts

> [!abstract] In one sentence
> A printed circuit board carries three things at once—current, measurement information and heat—and each needs a deliberate path.

## 1. An everyday picture: a delivery route includes the return trip

![[f6-01-loop-area-compare.png|850]]
*BATCH_F F6.1. Imagine a delivery vehicle returning to its depot. The whole trip matters, not just the outward road. The board geometry is conceptual.*

A short road to a destination does not make a short round trip if the return road goes far around the city. Current also needs an outgoing and returning path. Their geometry forms a **loop**. In switching circuits, a loop carrying rapidly changing current can create unwanted voltage and magnetic coupling.

A ground symbol means a named electrical reference, not zero impedance. Real return copper has resistance and inductance just like outgoing copper.

**Learning goals:** find the buck's changing-current loop, keep measurement taps out of power drops, follow heat into the board, and explain what layout review must establish later.

> [!warning] Status
> This lesson is conceptual: **no V1A PCB is routed**. **Gate 4a-FIX capture freeze BLOCKED; R2/R3 release BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** No trace width, layer stack or via count is selected here.

## 2. Picture walkthrough: identify the hot loop

![[d4-buck-input-switching-loop.png|850]]
*Existing D4. Dashed loops represent switching-current transfer between states, not simultaneous conduction through both switches. Both switches on together would be a fault.*

Read the geometry in this order:

1. Find the **local input capacitor**. It supplies the fast current pulses close to the buck.
2. Find the **high-side and low-side switches** inside LM61460. Compare the two paths from Lesson 02.
3. Identify the path whose current changes most abruptly when conduction transfers between switches. This is the input **hot loop**; “hot” here refers to rapid change, not just temperature.
4. Follow the power-ground (**PGND**) connection back to the capacitor. A long return can undo a short outgoing connection.
5. Locate feedback (**FB**) and the shunt sense pair. Keep these away from SW and switching-current voltage drops.

The manufacturer layout guidance calls for local bypassing at **both VIN/PGND pairs**. Physical package connections decide where the capacitor must connect; a nearby-looking capacitor with a long return is not equivalent.

## 3. Worked example: nanohenries can create volts

![[v2-06-stray-inductance.png|850]]

**ASSUMED teaching case:** current changes by 5 A in 10 ns through 10 nH of stray inductance. These are examples, not extracted V1A geometry or measured switching speed.

$$
\frac{di}{dt}=\frac{5\ \mathrm{A}}{10\ \mathrm{ns}}=0.5\ \mathrm{A/ns}
$$

$$
|V_L|=L\left|\frac{di}{dt}\right|
=10\ \mathrm{nH}\times0.5\ \mathrm{A/ns}=5\ \mathrm{V}
$$

If the same assumed slew passed through 2 nH, the inductive term would be **1 V**. This is why apparently small parasitic inductance matters. It is not a prediction of the total SW peak: polarity, the rest of the circuit, capacitance and damping also matter. The final return geometry is **(still open)**.

## 4. Sense routes: give the monitor a clean observation point

![[f6-03-kelvin-routing-rule.png|900]]
*BATCH_F F6.3. Compare where the teal traces begin, not just whether they look thin.*

In the left panel, both sense routes start at the shunt's dedicated sense terminals. They run together to the monitor/filter. In the right panel, remote taps include some power-copper drop; separated routes can also pick up different noise.

Wide **force** copper carries load current. Narrow **sense** routes report voltage. The reviewed mapping is pad 1 FORCE+, 2 SENSE+, 3 SENSE−, 4 FORCE−; the exact package drawing governs the implementation.

At nominal 5 A the 2 mΩ shunt develops only **10 mV** and dissipates **50 mW**. An extra 5 mV in the sensed path would represent an enormous error. Lesson 04 shows the 1 mΩ routing-error example. Never pour copper around the resistor in a way that bypasses the intended shunt path.

## 5. Power copper: voltage loss and heating are linked

![[v2-06-copper-loss.png|850]]

Read the left plot for voltage loss and the right for heating. Both use fixed resistance assumptions:

$$
V_{drop}=IR,\qquad P_{loss}=I^2R
$$

At 5 A, the nominal 2 mΩ shunt costs **10 mV / 50 mW**. The preliminary **13.6 mΩ hot series-pair allocation** costs **68 mV / 0.34 W**. That pair's number is an assumed hot screen, not a proven board resistance.

Short, appropriately wide copper can reduce resistance, but there is no universal “5 A trace width.” Layer, thickness, length, thermal environment, vias, allowed temperature rise and voltage allowance all affect the answer. Connector lands and neck-downs can dominate an otherwise wide path.

## 6. Heat: follow a second path out of each component

![[f6-02-heat-flow-cutaway.png|850]]
*BATCH_F F6.2. Generic thermal path only. It is **not** a cross-section of LM61460 or permission to add a generic ground thermal pad.*

Heat travels from the component through its actual package connections and solder into copper, then through/spread across the board and into the environment. Thermal vias can help connect appropriate copper areas when the package and nets permit them.

**LM61460 has no extra generic exposed ground pad to invent.** Follow the reviewed RJR package lands and manufacturer layout. The hot switch node is electrically noisy; enlarging its copper indiscriminately to spread heat can create a different problem. The correct thermal and electrical paths must be considered together.

Board layers, copper thickness, dimensions, ambient temperature and airflow are **(still open)**. A calculated dissipation does not establish junction temperature. Later dummy-load measurements need the actual board, mounting and airflow.

## 7. What goes wrong: a beautiful top view hides bad paths

![[f2-03-hot-loop-3d.png|850]]
*BATCH_F F2.3. Left/right comparison of conceptual loop areas. There is no routed V1A board hidden in either image.*

A layout can look tidy yet put the input capacitor's return far away. The result may be excessive switching spikes, ringing and disturbed feedback. A second quiet-looking error is the right-hand sense arrangement in section 4: the monitor reports copper voltage as if it were shunt voltage.

```mermaid
flowchart LR
    P["Review current path and return"] --> S["Review sense taps and quiet reference"]
    S --> H["Review package heat paths"]
    H --> R["Run DRC and inspect outputs"]
    R --> T["Later: measure voltage, noise and temperature"]
```

Design rule check (**DRC**) finds configured geometric/rule violations. It cannot establish the hot loop's actual inductance, a thermal limit, or the correctness of an unmodelled current path. Visual inspection of generated outputs complements automated checks.

## 8. Why this design and not another

Use manufacturer reference layouts for switching-sensitive placement because the package and fast-current paths are already known. Adapt the functional block to V1A's qualified parts and interfaces; do not copy an entire unrelated PCB without understanding its assumptions.

A continuous, deliberately connected return is preferable to adding arbitrary ground cuts to “separate noise”: a cut can force a sensitive current to take a longer route. Kelvin taps preserve the measurement boundary without making the power path narrow. Thermal copper follows the actual electrical nets. Detailed geometry remains R3 work, after R2 closes.

> [!warning] Common misconceptions
> A short outgoing trace does not imply a small loop. Thin traces are not automatically Kelvin connections. More copper is not automatically better on a noisy node. A library named “Qualified” does not establish an assembled thermal result. DRC PASS is rule evidence, not electrical validation.

## 9. Check yourself

1. Which return must be traced when reviewing the input bypass?
2. What does 10 nH contribute at 0.5 A/ns in the example?
3. Where do the two shunt sense traces begin?
4. Can a thermal cutaway select a via count for V1A?

> [!question]- Answers
> 1. The actual PGND path back to that capacitor, at both VIN/PGND pairs.
> 2. A 5 V inductive term; it does not establish total waveform peak.
> 3. The dedicated sense terminals, not arbitrary nearby power copper.
> 4. No. Actual package, nets, stack-up, losses and cooling conditions must be reviewed.

## 10. One-page visual summary

![[f6-01-loop-area-compare.png|650]]

| Follow three paths | Ask this question |
|---|---|
| **Current out and back** | Where does the rapidly changing loop close? |
| **Sense information** | Are the taps at the intended resistor and quiet reference? |
| **Heat to the environment** | Which actual lands/copper/vias carry the losses away? |
| Fast-change example | **10 nH × 0.5 A/ns = 5 V**, assumed |
| Review order | Manufacturer guidance → geometry/return review → DRC/visual → later bench evidence |
| Present state | **No PCB routed; R2 and R3 blocked** |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): BUCK, LM, FP, MON and G4. The LM61460 package/layout source is [TI SNVSBD5D](https://www.ti.com/lit/ds/symlink/lm61460.pdf); new parasitic examples are explicitly assumed sensitivities. [BATCH_F](../illustrations/BATCH_F.md) F6.1–F6.3. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 06`.

Previous: [[05 Powering the Pi 5 through GPIO]] · Next: [[07 Bench bring-up and fault-injection testing]] · Terms: [[99-Glossary]]
