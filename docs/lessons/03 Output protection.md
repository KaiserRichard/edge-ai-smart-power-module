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

**Gate 4a freeze: BLOCKED.** The owner selected a development direction. The independent source-fault trigger, control supplies, powered-off sensing, fault logic and protected capacitor bank still have unresolved circuit connections or limits.

## The fault that regulation cannot fix

Normally, the buck's high-side switch turns on and off. If it fails short, it permanently connects the input to L201 and the output path. The controller cannot turn off a physical short. The inductor slows the current rise, but it does not stop continuing energy from the source. Its inductance can also fall at high current.

## Architecture D: detect, remember, disconnect

**DECISION:** the owner selected architecture D for the fault-test board. Its series disconnect sits at the **V1A 5 V output**, between `VOUT_5V1` and `VOUT_PROTECTED`.

| Part | Plain-English job |
| --- | --- |
| REF5025 | Provides the independent voltage reference. |
| TLV3201 | Compares a divided copy of the raw output voltage with that reference. |
| SN74LVC1G74 latch logic | Intended to keep a fault latched while its control supply remains valid. Fault priority, brownout and reset/re-arm behavior still need proof. |
| LTC7001 | Drives two BSC034N06NSATMA1 metal-oxide-semiconductor field-effect transistors (MOSFETs), arranged back-to-back with common sources as the series disconnect. |
| CSD18540Q5B + UCC27511 | Forms the driven crowbar branch on the protected rail, with preliminary ballast resistors to restrict discharge current. |

The crowbar gives protected-side energy a path toward ground. Opening the series pair interrupts the power path. These actions must be coordinated with input shutdown and reliable control supplies. Exact timing, trip thresholds, hot component limits and upstream energy disposal are **(still open)**. A protected-side crowbar cannot absorb upstream inductor energy after the disconnect opens. Gate 4a therefore proposes a **separate raw-side dump** and an **independent, held-up control supply**. Neither circuit is qualified; a shutdown command or a latch symbol does not prove safe behavior when power disappears.

## Why this design and not another

**D keeps the final disconnect and crowbar on V1A.** This is simpler to package and avoids E's extra Pi-end stage and its voltage drop. **E places protection at the Pi header**, where it can respond directly to the voltage the Pi sees, but adds wiring, control power and hardware. The older gate comparison recommended E; the owner later chose D for a **fault-test board**, not because D had proved the better fault margin.

With D, cable inductance and capacitance can let the Pi-end voltage ring above the module voltage. That is why D needs both a source-energy bound and measurements at the far end of the real harness. The architecture choice leaves those obligations open.

## Bound the source, including its capacitors

A **bound** is a justified maximum. We need bounds for both fault current and energy. The development route combines timed input isolation through TPS26630, a controlled **10–30 microfarad (µF) effective input bank**, and qualification of a **10 microhenry (µH) alloy L201 candidate**. These development allocations are **(still open)**, not demonstrated protection.

The proposed source targets are **physical source-current cutoff within 10 microseconds (µs) of fault onset** and **no more than 100 microcoulombs (µC) of positive replenishment charge** before cutoff. Neither is established. A raw-output overvoltage detector can trip too late while the output bank is charging, so a separate, bounded fault trigger is still needed. The 100 µC target is incoming source charge; it does not include all charge discharged from local capacitors toward the load.

An input current limiter cannot stop a capacitor downstream of it from discharging. The raw output bank is another store: its discharge toward the load bypasses L201. Therefore, a bound on L201 current alone is not a bound on all current arriving at the protected output.

**CALCULATION — illustrative:** assume 30 µF charged to 24 V:

$$
E=\tfrac12 CV^2=\tfrac12(30\times10^{-6})(24)^2=8.64\text{ mJ}
$$

If the capacitor is still at 24 V when the source turns off, these **8.64 millijoules (mJ)** remain stored. Energy already transferred before cutoff must also be counted. The example excludes the inductor, output capacitors and energy supplied before shutdown; it is not the full fault budget or the 26 V normal-ceiling case.

## P0: turn the protection claim into evidence

![[a4-fault-event-sequence.png|700]]

The image shows a **planned** dummy-load sequence. Its frames do not establish the actual order or delay of protection actions. Recording must start before injection and cover the whole event; it does not wait for frame 5. The picture omits the separate input cutoff and raw-side dump. Its protected crowbar cannot receive all upstream energy after the series pair opens.

P0 uses a current-limited bench source, dummy load, oscilloscope and current probe after inspection, continuity checks and normal startup checks. Measurements must establish the voltage at the protected/load boundary, actual current interruption, source charge and component temperatures under the defined test conditions. A shutdown command alone does not prove that current stopped.

**OPEN RISK:** application margins remain **(still open)**, including negative paper margins. For example, Gate 3b's conditional harness model reached about **5.542 V**, above the strict **5.5 V** Pi limit; this was a calculation, not a measurement. Gate 4a's proposed protected capacitor bank also misses its assumed capacitance/ESR limits; its conditional module-voltage screen is about **5.713 V**. This is a different calculation at a different node, not a measured Pi peak. A working circuit, applicable bounds and dummy-load evidence must close the gaps. **The Pi remains disconnected until all required gates pass.**

> [!warning] Common misconceptions
> A fast comparator alone does not bound fault energy. A current-limited supply does not remove stored capacitor energy. Selecting architecture D does not mean it has passed electrical validation.

## Check yourself

1. Why can normal buck control not stop a high-side short?
2. What does the latch add to a comparator?
3. Why is timed input isolation insufficient by itself?
4. What must be proved before connecting the Pi?

> [!question]- Answers
> 1. The failed switch remains physically conducting regardless of its control command.
> 2. It is intended to prevent immediate reconnection. Fault retention depends on valid power; brownout and deliberate reset/re-arm still need proof.
> 3. Stored input/output energy remains, and inductor current needs a discharge path; current and energy bounds must include them.
> 4. The required dummy-load and other validation gates must pass, including voltage, current, timing, thermal and protection limits.

> [!info]- Engineering evidence
> [Pinned sources and fact-check record](FACTCHECK_LOG.md#sources): G2C and COMMON for latch/supply gaps; G3 and DE for historical D/E comparisons; G3B and SRC for the source contract and 5.542 V case; BASIS and G4 for the current D decision and blocked freeze; TEST and HOOKS for P0. Older recommendations do not override the owner decision.

Previous: [[02 Buck converter LM61460]] · Next: [[04 Monitoring]] · Terms: [[99-Glossary]]
