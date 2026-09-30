---
title: "V1A inside the robot"
lesson: 8
tags: [v1a, lesson, visual]
---

# 08 — V1A inside the robot

> [!abstract] In one sentence
> V1A powers and measures one compute branch; integrating it into a robot requires explicit upstream, harness, grounding and data boundaries.

## 1. An everyday picture: one apartment in a large building

![[f8-01-robot-cutaway-power.png|850]]
*BATCH_F F8.1. Think of V1A as one apartment's supply and meter. The other branches belong to the larger building, not to that apartment.*

A building's distribution board supplies many apartments. One apartment's meter cannot describe all building consumption, and a fault in another branch can still disturb the shared source. Similarly, a robot has separate compute and motor branches. V1A does not become the entire robot power system just because it sits inside the robot.

**Learning goals:** trace the intended supply hierarchy, explain what isolation changes, budget upstream power and identify what compute telemetry can actually establish.

> [!warning] Status
> V1A remains a standalone Project II module. The final robot electrical architecture is not frozen. **Gate 4a-FIX freeze BLOCKED — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** These lessons do not authorize procurement, fabrication or Pi integration.

## 2. Picture walkthrough: five boundaries on the journey

![[f0-01-power-journey-robot.png|900]]
*BATCH_F F0.1. “48 V → 24 V” denotes the required converter class, not an approved exact product or fault envelope.*

1. **13S battery context:** thirteen cells in series is the supplied future integration concept. It is not a V1A input rating or a complete battery specification.
2. **Power distribution board (PDB):** feeds separate branches and upstream protection. V1A does not carry the motor branches.
3. **Bought isolated 48 V → 24 V module:** transforms the compute branch supply. Its model, limits and fault behavior are **(still open)**.
4. **V1A:** requires **9–26 V normal input**, then targets approximately 5.1 V locally with regulation, protection and monitoring.
5. **Pi GPIO harness:** dedicated 5 V and ground pins carry power. Actual delivered voltage includes all path losses; see Lesson 05.

An upstream module must meet the full healthy voltage envelope: initial tolerance, line/load variation, ripple and startup. A nominal 24 V label alone answers none of the transient or fault questions.

## 3. Isolation: a boundary with a specific job

![[f8-02-isolated-vs-nonisolated.png|900]]
*BATCH_F F8.2. The green mark means the required isolation architecture, not a passed fault test. The 48 V battery label is nominal context, not a frozen battery limit.*

In the left panel, a non-isolated buck's shorted high-side switch can leave a direct path from battery toward V1A. The inductor does not remove that sustained electrical connection. **The owner rejected the UENPO non-isolated module for V1A's supply.**

The right panel transfers power across an isolation barrier. With that barrier intact, the same direct switch-short path across the power-transfer stage is absent. This is why an **isolated module is required**.

Isolation does not guarantee a safe output voltage under every control or component fault. The upstream protection must still prevent battery pass-through and provide reviewed output-fault limits. Grounding, shields, USB connections, test instruments and other ports can also create external conductive paths. Review the full connected system; the symbol alone is not the system boundary proof.

Source current, local stored energy and shutdown behavior are **(still open)** inputs to V1A's protection study. A rated isolation test does not establish the output waveform that V1A will actually receive.

## 4. Worked example: size the upstream power budget

![[v2-08-input-power-budget.png|850]]

**ASSUMED:** local buck output 5.1 V at 5 A; efficiency from V1A input to that local node 90%. The efficiency sweep is a sensitivity study, not a measured curve.

$$
P_{out}=5.1\times5=25.5\ \mathrm{W}
$$

$$
P_{V1A,in}=\frac{25.5}{0.90}=28.33\ \mathrm{W},\qquad
I_{24V}=\frac{28.33}{24}=1.18\ \mathrm{A}
$$

The isolated upstream converter must deliver the required input power plus any auxiliary loads omitted from this simplified efficiency boundary. Its own losses make battery-side power larger again. Do not claim 28.33 W as the complete robot demand or use 1.18 A to approve startup/fault capability.

At an assumed 80% efficiency the same 25.5 W target would need **31.875 W**. That sensitivity shows why efficiency and thermal evidence affect upstream sizing; it does not select a converter.

## 5. A 24 V label needs a complete voltage envelope

![[v2-08-source-voltage-envelope.png|850]]

This is an **ASSUMED example only**: 24 V nominal, +2% DC allowance, +0.20 V positive ripple and +0.15 V startup allowance.

$$
V_{healthy,peak}=24(1.02)+0.20+0.15=24.83\ \mathrm{V}
$$

That example is below 26 V. It is not a supplier guarantee. The exact module may specify different limits, typical rather than maximum values, and overlapping definitions. If a tolerance already includes load regulation, do not add load regulation a second time. If ripple is specified peak-to-peak, do not silently treat half of it as a guaranteed positive allowance without knowing its reference.

A complete normal envelope must satisfy the **9–26 V requirement**. A separate fault envelope must bound voltage, current, time, charge and energy, including output capacitors. These are different engineering contracts.

## 6. What goes wrong: one branch meter becomes “whole-robot energy”

![[f4-02-measurement-boundary.png|850]]
*BATCH_F F4.2. The current is the compute-branch contribution through R401; the voltage tap is at the module. The bubble does not extend the measurement to the battery or distant Pi.*

The INA228 reports current, voltage, power and energy over **Inter-Integrated Circuit (I2C)**. It excludes upstream conversion losses, local monitor supply branched before the shunt, and unrelated robot branches. Its module voltage cannot directly tell the Pi's voltage after the cable.

A research log could associate branch readings with time, workload and reset events. That may help compare two compute workloads under controlled conditions. It cannot establish whole-robot efficiency from a single branch sensor.

![[v2-04-energy-reset-gap.png|850]]
*Reuse of Lesson 04's assumed example: the missing interval is unknown data. It is not evidence of zero power.*

If the monitor loses power, accumulated energy resets. Record the reset and gap; do not silently join new zero-based readings to an old total. Logging, fault reporting and robot recovery policies remain **(still open)**. Independent hardware protection acts locally; host software must not be credited with a response faster than its actual measurement and communication path.

## 7. Why this design and not another

Keeping V1A standalone makes its requirements and tests understandable before robot integration. A bought isolated upstream module provides the owner-required power-transfer boundary without expanding V1A into a high-voltage robot PDB. The exact product remains subject to source-envelope qualification.

V1A does not promise backup energy, orderly shutdown or automatic recovery. Historical supercapacitor work belongs to another subsystem and requires a separately reviewed interface. **USB 3.x and D435i camera data do not route through this board.** Adding those functions would create new requirements rather than complete the current power module.

```mermaid
flowchart LR
    S["Qualify standalone V1A"] --> U["Qualify exact isolated source"]
    U --> H["Qualify harness and connected grounds"]
    H --> T["Close dummy-load normal and fault gates"]
    T --> I["Review Pi and robot integration"]
```

This is a dependency summary, not permission to skip the repository's R0–R5 sequence.

> [!warning] Common misconceptions
> “Isolated” is not a guarantee of every output-fault peak. Branch energy is not whole-robot energy. A 24 V label is not a source envelope. Telemetry is not fast independent protection. An abrupt safe-voltage shutdown does not prove safe robot behavior.

## 8. Check yourself

1. Which block separates the battery-class supply from V1A's normal input?
2. What direct fault path does isolation remove while its barrier is intact?
3. Why is the worked example not the whole robot's power requirement?
4. When may the Pi replace the dummy load?

> [!question]- Answers
> 1. The required bought isolated 48 V-to-24 V module plus reviewed upstream protection; its exact identity remains open.
> 2. The non-isolated high-side-short conductive path across the converter's power-transfer stage.
> 3. It excludes the upstream converter's own loss and other branches/omitted auxiliary loads.
> 4. After all required engineering, dummy-load, fault, thermal, telemetry and interface gates pass.

## 9. One-page visual summary

![[f8-01-robot-cutaway-power.png|650]]

| Boundary | Remember |
|---|---|
| Battery/PDB → converter | Future robot context; separate other branches |
| Converter → V1A | **Isolated required; UENPO non-isolated rejected; 9–26 V normal** |
| V1A local target | **5.1 V × 5 A =25.5 W**, not validated |
| Illustrative input need | **28.33 W / 1.18 A at 24 V**, assuming 90% to the local output |
| Measurement | One branch at a module-side plane; log resets and gaps |
| Integration | Source, harness, grounding and all gates must close before Pi use |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): CTX, MON, AUX, OWNER, BASIS and G4. The old AUX 24 V ceiling/trim proposals do not override the current 9–26 V requirement. Gate 4a-FIX `2b99ac7` retains the unidentified source envelope as open. [BATCH_F](../illustrations/BATCH_F.md) F8.1–F8.2. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 08`.

Previous: [[07 Bench bring-up and fault-injection testing]] · Next reference: [[99-Glossary]] · [[00-INDEX|Lesson index]]
