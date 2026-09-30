---
title: "Output protection"
lesson: 3
tags: [v1a, lesson]
---

# 03 — Output protection

## Why this matters

A failed buck switch can connect the input supply to the 5 V output.<br>
Protection must stop incoming power and deal with energy already stored.<br>
We prove that behavior with a dummy load before connecting a Raspberry Pi.

**PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)**<br>
**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## The fault that regulation cannot fix

Normally, the buck's high-side switch turns on and off. If it fails short, it permanently connects the input to L201 and the output path. The controller cannot turn off a physical short. The inductor slows the current rise, but it does not stop continuing energy from the source. Its inductance can also fall at high current.

## Architecture D: detect, remember, disconnect

**DECISION:** the owner selected architecture D for the fault-test board. Its series disconnect sits at the **V1A 5 V output**, between `VOUT_5V1` and `VOUT_PROTECTED`.

| Part | Plain-English job |
| --- | --- |
| REF5025 | Provides the independent voltage reference. |
| TLV3201 | Compares a divided copy of the raw output voltage with that reference. |
| 74LVC1G74 | Remembers the fault so protection does not immediately reconnect. |
| LTC7001 | Drives two BSC034N06 metal-oxide-semiconductor field-effect transistors (MOSFETs), arranged back-to-back as the series disconnect. |
| CSD18540Q5B + UCC27511 | Forms the driven crowbar branch on the protected rail, with preliminary ballast resistors to restrict discharge current. |

The crowbar gives protected-side energy a path toward ground. Opening the series pair interrupts the power path. These actions must be coordinated with input shutdown and reliable control supplies. Exact timing, trip thresholds, hot component limits and upstream energy disposal are **(still open)**. A protected-side crowbar cannot absorb upstream inductor energy after the disconnect opens.

## Bound the source, including its capacitors

A **bound** is a justified maximum. We need bounds for both fault current and energy. The development route combines timed input isolation through TPS26630, a controlled **10–30 microfarad (µF) effective input bank**, and qualification of a **10 microhenry (µH) alloy L201 candidate**. These development allocations are **(still open)**, not demonstrated protection.

An input current limiter cannot stop a capacitor downstream of it from discharging. The raw output bank is another store: its discharge toward the load bypasses L201. Therefore, a bound on L201 current alone is not a bound on all current arriving at the protected output.

**CALCULATION — illustrative:** assume 30 µF charged to 24 V:

$$
E=\tfrac12 CV^2=\tfrac12(30\times10^{-6})(24)^2=8.64\text{ mJ}
$$

These **8.64 millijoules (mJ)** remain available after the upstream supply turns off. The example excludes the inductor, output capacitors and energy supplied before shutdown; it is not the full fault budget.

## P0: turn the protection claim into evidence

![[a4-fault-event-sequence.png|700]]

The image shows a **planned** dummy-load sequence. Its frames do not establish the actual order or delay of the protection actions.

P0 uses a current-limited bench source, dummy load, oscilloscope and current probe after inspection, continuity checks and normal startup checks. Measurements must establish the voltage at the protected/load boundary, actual current interruption, source charge and component temperatures under the defined test conditions. A shutdown command alone does not prove that current stopped.

**OPEN RISK:** application margins remain **(still open)**, including negative paper margins. For example, Gate 3b's conditional harness model reached about **5.542 V**, above the strict **5.5 V** Pi limit; this was a calculation, not a measurement. Dummy-load evidence and applicable worst-case limits must close the gaps. **The Pi remains disconnected until all required gates pass.**

> [!warning] Common misconceptions
> A fast comparator alone does not bound fault energy. A current-limited supply does not remove stored capacitor energy. Selecting architecture D does not mean it has passed electrical validation.

## Check yourself

1. Why can normal buck control not stop a high-side short?
2. What does the latch add to a comparator?
3. Why is timed input isolation insufficient by itself?
4. What must be proved before connecting the Pi?

> [!question]- Answers
> 1. The failed switch remains physically conducting regardless of its control command.
> 2. It keeps the fault remembered until deliberate reset/re-arm under valid conditions.
> 3. Stored input/output energy remains, and inductor current needs a discharge path; current and energy bounds must include them.
> 4. The required dummy-load and other validation gates must pass, including voltage, current, timing, thermal and protection limits.

> [!info]- Engineering evidence
> Current owner basis: [Gate4a BASIS](../../wt-gate4a/docs/evidence/r2/gate4a/BASIS.md). Source-energy reasoning and the conditional 5.542 V case: [Gate 3b source bound](../../wt-gate3b/docs/evidence/r2/sheet03/gate3b/GATE3B_SOURCE_BOUND.md). Image context: [Batch A](../../wt-illustrations/docs/illustrations/BATCH_A.md).

Previous: [[02 Buck converter LM61460]] · Next: [[04 Monitoring]] · Terms: [[99-Glossary]]
