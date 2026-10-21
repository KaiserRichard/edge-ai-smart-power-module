---
title: "System overview"
lesson: 0
tags: [v1a, lesson, visual]
---

# 00 — System overview

> [!abstract] In one sentence
> V1A is a small power station: it admits a suitable input, converts voltage, contains output faults, measures one branch, and delivers power through a real harness.

## 1. An everyday picture: supplying a house with water

![[f0-03-five-jobs-analogy.png|850]]
*BATCH_F F0.3. This is a job analogy. The existing picture puts the meter before the emergency gate; in V1A, the shunt is **after output protection**, as the exact sequence below shows.*

Imagine supplying a house from a reservoir on a hill. The high pressure is useful for moving water, but it is too high for the house. A reducing station lowers it. An entrance guard rejects unsuitable supply conditions. A separate emergency valve protects the house if the reducing station breaks. A meter records consumption, and the pipe carries water to the house.

In this analogy, voltage resembles pressure and current resembles flow. Power is the rate of energy delivery. The analogy stops at switching and magnetic storage; a buck converter does more than squeeze a pipe.

**After this lesson you should be able to:** trace the five jobs, distinguish three output measurement points, and explain why a diagram is not evidence that the board works.

> [!warning] Project status
> **PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD). Gate 4a-FIX freeze: BLOCKED. R2 schematic release and R3 PCB release remain BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** The lessons explain intended behavior; they do not release hardware. No Pi before fault tests and all other applicable gates pass.

## 2. Picture walkthrough: from the robot to V1A

![[f0-01-power-journey-robot.png|900]]
*BATCH_F F0.1. “48 V → 24 V” is an upstream module class. “5.1 V target” is the local buck target, not a guaranteed voltage at the computer.*

**Schematic anchor:** PDF **page 6, “DC INPUT / J501,” pin 1 (+) and pin 2 (RETURN)**. The robot and upstream converter are outside the drawing; J501 is the boundary where their reviewed output would enter. Read the two wires as a complete supply pair.

Read the journey left to right:

1. **Battery:** the future Wheel-Biped Robot (WBR) context uses 13 series cells, abbreviated **13S**. Its final electrical architecture is not frozen here.
2. **Power distribution board (PDB):** distributes battery power to separate branches. V1A is not the PDB.
3. **Bought isolated converter:** supplies the lower-voltage compute branch. Its exact model and fault behavior are **(still open)**. The owner rejected the UENPO non-isolated module.
4. **V1A:** accepts a **9–26 V normal input**, including the source's healthy tolerance, ripple and startup behavior. The battery must never connect directly to V1A.
5. **Computer:** the intended Raspberry Pi 5 receives power through dedicated 5 V and ground pins on its general-purpose input/output (**GPIO**) header. A dummy load occupies this position during qualification.

V1A remains a standalone Project II design. A suitable current-limited bench source can represent the upstream boundary before robot integration.

## 3. Open the module: five jobs, five sheets

![[f0-02-v1a-board-exploded.png|850]]
*BATCH_F F0.2. The floating layers are functional groups, not physical PCB layers or a routed design.*

```mermaid
flowchart LR
    I["01 Input protection"] --> B["02 Buck converter"]
    B --> O["03 Independent output protection"]
    O --> M["04 Shunt and monitor"]
    M --> H["05 Connector and harness"]
    H --> L["Dummy load during qualification"]
```

| Follow the picture | Job | What it cannot establish alone |
|---|---|---|
| Purple entrance | Fuse, transient voltage suppressor and electronic fuse manage input faults | Safe output after a failed buck switch |
| Orange converter | LM61460 switching stage regulates locally near 5.1 V | The voltage after every downstream loss |
| Orange-to-blue boundary | Architecture D disconnects the output and disposes of stored energy | A qualified result until timing, parts and the harness are tested |
| Teal monitor | INA228 reads a 2 mΩ shunt and load-side module voltage | Whole-robot energy or a fast fault peak |
| Blue exit | Connector and harness carry send **and return** current | Equal pin sharing or negligible resistance |

The input fuse **F101 is Schurter 3403.0285.23**; the selected TVS **D101 is Littelfuse SMCJ36CA**. Those owner choices are distinct from installed qualification.

### Read the real schematic: one stop at a time

Open [the six-page review PDF](/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf). **PDF page 1 is the hierarchy; Sheet 01 begins on PDF page 2.** The [schematic reading guide](SCHEMATIC_READING_GUIDE.md) records the snapshot and older labels.

![[v2-review-p01.png|1000]]
*Unchanged render of PDF page 1. Its old “9–24 V” text is historical; the current requirement is **9–26 V**. The rectangles are sheet ports, not IC pinouts.*

1. **Enter — page 6, DC INPUT / J501: pins 1 (+), 2 (RETURN).** Follow `VIN_RAW` to **page 2, INPUT / REVERSE PROTECTION, F101 pins 1→2**. A matching net name joins pages even when there is no long drawn wire.
2. **Admit — page 2, EFUSE / SUPERVISION: U101 IN pins 1/2 → OUT pins 17/18.** The output label is `VIN_PROTECTED`. Here “protected” means after the input stage; this is still the high-voltage input to the buck, not a protected 5 V load rail.
3. **Convert — page 3, BUCK CONVERTER: U201 VIN1 pin 8 / VIN2 pin 12, SW pin 10; OUTPUT / FEEDBACK: L201 pins 1→2.** SW is the pulsed node before L201. `VOUT_5V1` is the raw regulated node after it, sensed by U201 FB pin 4 through R202/R203.
4. **Contain — page 4, OPPOSED SERIES FETS: Q301 outer drains 5–8 → common sources 1–3 → Q302 outer drains 5–8.** Gates are pin 4 on each device; the shared source is `PROT_MID`. This is an earlier preliminary implementation: the **revised architecture D series/crowbar/control arrangement is frozen on paper, not yet in the schematic**. A raw dump is absent from this PDF and has no PDF refdes/pin to follow.
5. **Measure — page 5, KELVIN SHUNT / MEASUREMENT: R401 force pin 1 → pin 4; U401 VBUS pin 8.** R401 changes the net name from `VOUT_PROTECTED` to `LOAD_5V1`. The separate VBUS wire observes the latter; it does not carry the load current.
6. **Deliver — page 6, LOAD OUTPUT / J502: pin 1 (+), pin 2 (RETURN).** Follow both conductors into the future harness. The Pi header is outside this PDF, so J502 pin 1 must not be confused with Pi physical pin 1.

“Frozen on paper” describes the recorded proposal, **not a passed freeze gate**. Page 4 already draws an earlier pair and crowbar; the later raw dump, auxiliary and logic changes remain incomplete. No shortcut wire may join raw and protected output.


## 4. Three places that are all called “5 V”

![[f4-02-measurement-boundary.png|850]]
*BATCH_F F4.2. Look at the protection switch, shunt, and cable as separate boundaries.*

| Name on the schematic | Where it is | Why the distinction matters |
|---|---|---|
| `VOUT_5V1` | Raw buck output | The feedback divider regulates here |
| `VOUT_PROTECTED` → `LOAD_5V1` | Before → after the 2 mΩ shunt | INA228 bus voltage is on the load side of the shunt |
| Pi header voltage | Far end, measured against its own ground | Includes positive and return-path losses and cable transients |

![[v2-00-circuit-boundary.png|950]]
*Exact simple excerpt: **page 5, R401 force pins 1/4 and U402 IN pin 1; page 6, J502 pins 1/2**. The local supply branches before the shunt. Sense pins and the rest of the monitor are omitted here, then expanded in Lesson 04.*

![[f0-04-circuit-boundary.png|900]]
*Circuit-picture prompt **F0.4** in [BATCH_F](../illustrations/BATCH_F.md); the owner generates this companion. Reproduce the exact excerpt with `python3 -B docs/lessons/figures/src/circuit_00.py`.*

For a simple resistive loop, $V_{Pi}=V_{buck}-IR_{loop}$. The loop includes switches, shunt, board copper, contacts, positive wire **and ground wire**. A module-side 5 V reading cannot prove the Pi-end voltage.

## 5. Worked example: where does the power go?

![[v2-00-power-accounting.png|800]]

**Schematic anchor for the calculation:** **page 3, OUTPUT / FEEDBACK, L201 pin 2 (`VOUT_5V1`)**, measured against U201 PGND pins 9/11. The example stops at this local plane; it does not reach J502 or the Pi.

**ASSUMED teaching case:** 5.1 V and 5 A at the local buck output, with 90% efficiency from the V1A input to that node. Actual efficiency and continuous thermal capability are **(still open)**.

$$
P_{out}=VI=5.1\times5=25.5\ \mathrm{W}
$$

$$
P_{in}=\frac{25.5}{0.90}=28.33\ \mathrm{W},\qquad
P_{loss}=28.33-25.5=2.83\ \mathrm{W}
$$

At 24 V, the estimated input current is $28.33/24=1.18\ \mathrm{A}$. The output can carry 5 A because it is at a lower voltage. There is no free energy: input power pays for output power and losses. Downstream harness loss further reduces the power reaching the computer; this example is not a measured board rating.

## 6. What goes wrong: one job cannot replace another

![[p03-02-buck-normal-vs-shorted.png|850]]
*The pilot's concept picture compares a healthy switching action with a permanent high-side short. Read it as a functional explanation, not a buildable schematic.*

**Find the failure on page 3, BUCK CONVERTER: U201 VIN pins 8/12 and SW pin 10.** The high-side switch is inside the IC rectangle, so it has no separate Q-refdes. Follow the failed internal connection through **L201 pins 1→2** toward the raw rail.

A shorted high-side switch can apply the input to the inductor continuously. A normal 24 V input gives the **input** overvoltage detector no reason to trip. Meanwhile the **output** rises. Feedback cannot switch off a physical short; telemetry does not replace the independent protection circuit.

```mermaid
flowchart LR
    F["Buck high-side short"] --> R["Raw output rises"]
    R --> D["Independent protection must act"]
    D --> T["Prove source cutoff, energy disposal and far-end voltage"]
```

The unresolved independent source trigger, control supplies, fault/re-arm logic and protected capacitor bank keep the freeze blocked. Lesson 03 explains the favorable teaching waveform **and** the failed conditional screens.

## 7. Why this design and not another

A bought 5 V regulator would perform conversion, but conversion alone does not answer V1A's protection, measurement and testability requirements. Separating the jobs makes each claim reviewable. Architecture D keeps output protection on V1A; the owner chose it for a fault-test board, with far-end proof still owed. The isolated upstream module addresses the robot's supply boundary while preserving V1A as a standalone project.

> [!warning] Common misconceptions
> A nominal 24 V label is not a qualified source envelope. A 5.1 V setpoint is not the Pi voltage. Monitoring is not fault containment. Electrical/design rule checks do not demonstrate performance or safety.

## 8. Check yourself

1. Why is protection needed on both sides of the buck?
2. Which side of the shunt supplies the INA228 bus-voltage reading?
3. Does 25.5 W at the buck establish 25.5 W at the Pi?
4. What replaces the Pi in qualification?

> [!question]- Answers
> 1. Input faults and a buck's own output fault are different events at different nodes.
> 2. `LOAD_5V1`, relative to module ground; the distant header remains outside that voltage measurement.
> 3. No. The downstream path dissipates power and drops voltage.
> 4. A reviewed dummy/electronic load and representative harness, after the preceding engineering gates.

## 9. One-page visual summary

![[v2-00-circuit-boundary.png|800]]
*Find the same boundary on PDF pages 5–6; return to page 1 for the five-sheet route.*

| Keep this boundary in mind | Remember |
|---|---|
| Source → V1A | Isolated module required; normal input **9–26 V** |
| Buck → protection | Local target **about 5.1 V / 5 A**; not validated |
| Protection → load | Owner chose **D test board**; fault behavior remains open |
| Shunt → host | **2 mΩ + INA228**, one branch's telemetry |
| Harness → Pi | Loaded minimum **4.75 V**; peak **strictly below 5.5 V** |
| Paper → hardware | **Gate 4a-FIX BLOCKED; no Pi before all required gates pass** |

> [!info]- Sources and reproducibility
> [Fact-check source register](FACTCHECK_LOG.md#sources): CTX, MON, BASIS, G4 and OWNER. Later Gate 4a-FIX at `2b99ac7` retains the blocked verdict. Artwork targets are in [BATCH_F](../illustrations/BATCH_F.md). Chart: `python3 -B docs/lessons/figures/src/lesson_charts.py 00`. A teaching edit closes no engineering gate.

Previous: [[00-INDEX|Lesson index]] · Next: [[01 Input protection]] · Terms: [[99-Glossary]]
