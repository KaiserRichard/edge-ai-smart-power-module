---
title: "Buck converter LM61460"
lesson: 2
tags: [v1a, lesson]
---

# 02 — Buck converter LM61460

## Why this matters

V1A targets a 9–26 V input; the LM61460 receives that supply after input-stage losses and regulates a local rail near 5.1 V.<br>
Its switches, inductor and capacitors work together to deliver fairly steady power.<br>
Understanding that energy path also explains why a failed switch needs separate protection.

## Two states, one current direction

A **buck converter** lowers voltage by switching. The LM61460's **metal-oxide-semiconductor field-effect transistors (MOSFETs)** alternately connect the switch node (**SW**) to input or ground (**GND**). Turning both on together would short the input.

Take inductor current as positive from SW toward the output. Define its voltage as **left end minus right end**: $V_L=V_{SW}-V_{OUT}$.

| State | Inductor voltage | What current does |
| --- | --- | --- |
| High side on; low side off | $V_L\approx V_{IN}-V_{OUT}>0$ | Rises; input supplies the output and adds magnetic energy. |
| High side off; low side on | $V_L\approx -V_{OUT}<0$ | Falls; stored magnetic energy continues supplying the output. |

![[c2-buck-low-side-freewheel-state.png|500]]

Follow the blue loop: ground → low-side switch → inductor → load → ground. **Falling current still flows toward the load.** Here it stays above zero: continuous-conduction operation. The picture's +/− marks define the voltage reference; they do not mean the left end is actually more positive in this state. The output capacitor also carries the difference between inductor and load current. Light-load behavior can differ; brief switching transitions are simplified.

## Why L201 is changing

For constant inductance and voltage, $\Delta I=V_L\Delta t/L$: more inductance slows current change. At large current, magnetic saturation can reduce inductance, speeding up the rise.

**DECISION — selected qualification candidate:** move from the inherited **6.8 microhenry (µH)** XAL8080 to the **10 µH alloy Würth 74437636351002** for further qualification. Gate 4a lists this proposed change; it is **not a qualified or fitted replacement**. Its published current-dependent curve helps the fault study, but guaranteed behavior across temperature and production batches is **(still open)**.

**Ldiff** means differential inductance at the present current; **DCR** means direct-current winding resistance.

**Image status correction:** the older picture below says “not selected.” Gate 4a now selects this part **for qualification**, with its limits still open. The component shape and shaded curve are generic illustrations, not a manufacturer drawing or a guaranteed inductance envelope.

![[c4-10-h-alloy-inductor-selection.png|600]]

Heating, footprint and stable regulation need checking, especially low ripple at 9 V **(still open)**. A larger inductor cannot stop a connected source supplying energy indefinitely.

## Why this design and not another

The old small inductor lacks a justified inductance bound across the studied fault currents. The larger 10 µH alloy candidate has a published curve extending through the study's current range, making it a useful qualification starting point. The cost is a much larger through-hole package, different mounting and changed ripple/load-step behavior. A typical curve alone does not close those checks.

Gate 3b therefore combines the candidate with **timed source isolation and controlled input capacitance**. More inductance alone cannot bound the energy from a source that remains connected. **Gate 4a freeze remains BLOCKED** while these circuit and component limits are open.

**Calculated example — illustrative only:** assume constant inductance, 24 V input, 5.1 V output and a 0.5 microsecond high-side-on interval; ignore losses:

$$
\Delta I_{10\,\mu H}=\frac{(24-5.1)\times0.5\,\mu s}{10\,\mu H}=0.945\,A
$$

With 6.8 µH, the increase is **1.39 A**. These are not predicted fault peaks.

## Capacitors, feedback and the hot loop

**Input capacitors** supply switching-current pulses. **Output capacitors** carry the difference between inductor and load current, charging or discharging to smooth voltage. Ceramic capacitance can fall under applied direct-current (**DC**) voltage. The source study calls for at least **10 microfarads (µF) effective main input ceramic capacitance**, plus a nominal **100 nanofarad (nF) bypass at each VIN/PGND pair**. All local reservoirs and bypasses must fit the proposed **30 µF total effective maximum**. These are qualification targets; nominal part labels do not prove them.

**Feedback (FB)** senses local output through a resistor divider: falling voltage increases energy delivery; rising voltage reduces it. Sensing is before the output disconnect, so cable voltage drop remains.

The **hot loop** links input capacitors, both switches and power-ground return. Rapid current changes demand a small loop area; keep FB away from SW. This describes switching-current transfer, not simultaneous switch conduction. Layout is **conceptual; no printed circuit board (PCB) is routed**.

> [!warning] Common misconceptions
> Negative inductor voltage does not immediately reverse current. A 10 µH label does not guarantee fault behavior. More capacitance stores more fault energy. Feedback cannot turn off a shorted high-side switch.

## Check yourself

1. Which state makes inductor current rise?
2. How does current return during the low-side state?
3. Why is the 10 µH candidate not a completed fix?
4. Why keep input capacitors close and feedback away from SW?

> [!question]- Answers
> 1. High side on: the inductor sees positive left-to-right voltage.
> 2. Through ground and the conducting low-side switch, then back into the inductor.
> 3. Its hot/current-dependent inductance, normal regulation and physical fit need qualification; source isolation must also bound fault energy.
> 4. A compact switching loop reduces unwanted voltage spikes and noise; quiet feedback helps the controller sense the actual output.

> [!info]- Evidence and current status
> [Pinned sources and fact-check record](FACTCHECK_LOG.md#sources): BUCK and LM for converter principles; L and SRC for the inductor/capacitor tradeoffs; BASIS and G4 for current selections and the blocked freeze. IMG is historical illustration context. No bench validation is claimed.

Previous: [[01 Input protection]] · Next: [[03 Output protection]] · Terms: [[99-Glossary]]
