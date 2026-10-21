---
title: "Buck converter LM61460"
lesson: 2
tags: [v1a, lesson, visual]
---

# 02 — Buck converter LM61460

> [!abstract] In one sentence
> The buck alternates two current paths so an inductor and capacitors can turn a pulsed switch-node voltage into a nearly steady local 5.1 V rail.

## 1. An everyday picture: push a flywheel, then let it coast

![[f2-02-inductor-flywheel.png|800]]
*BATCH_F F2.2. Speed represents current; a push represents applied voltage. This picture explains continuity, not the magnetic saturation law.*

A heavy flywheel does not instantly reach full speed when pushed, and does not stop the moment the push ends. You can maintain its average speed with repeated short pushes. An inductor behaves similarly with **current**: applied voltage changes the current gradually.

The important difference is that the buck gives current a closed path while the high-side switch is off. Opening a path without providing another one would produce a voltage transient rather than a gentle coast.

**After this lesson:** explain both switch states, read the three aligned waveforms, calculate one ripple cycle, and connect the inductor/capacitor choices to the fault problem.

> [!warning] Status
> The normal V1A input requirement is **9–26 V**; the buck receives that supply after input-stage losses. The **10 µH candidate is selected for qualification**, not validated. **Gate 4a-FIX BLOCKED — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## 2. First state: the input pushes current upward

Open **PDF page 3, “02 BUCK 5V”** in [V1A_GATE4B_WIP_2026-10-03.pdf](/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_GATE4B_WIP_2026-10-03.pdf#page=3). Its two blocks are BUCK / NATIVE SWITCH NODE and FAULT INJECTION / LOCAL REGULATION. Page 1 is the hierarchy; Sheet 02 is PDF page 3. The schematic walks below use this WIP PDF: Sheets 01–02 are redrawn to the frozen design; Sheets 03–05 retain their earlier drawings. The [schematic reading guide](SCHEMATIC_READING_GUIDE.md) and embedded page image still describe the older review PDF. The two switching MOSFETs are **inside U201**, so the external schematic gives them no separate Q-refdes or gate pins.

![[v2-review-p03.png|1000]]
*Historical review-PDF page 3, retained for context; its **6.8 µH** label is superseded. The linked WIP page captures L201 as **10 µH**, Würth **74437636351002**, with JP201/JP202 and separate `BUCK_SW`, `L201_IN`, `L201_OUT` and `VOUT_5V1` nets. Selection for qualification is not validation.*

**Read the first path:** in BUCK / NATIVE SWITCH NODE, **C201–C204 pin 1** join `VIN_PROTECTED`, which reaches **U201 VIN1 pin 8 and VIN2 pin 12**. The internal high-side switch connects input toward **SW pin 10** when on. Follow `BUCK_SW` into FAULT INJECTION / LOCAL REGULATION: **JP201 FORCE_A pin 1 → FORCE_B pin 2** → `L201_IN` → **L201 pin 1→2** → `L201_OUT` → **JP202 FORCE_A pin 1 → FORCE_B pin 2** → `VOUT_5V1`. This path assumes both removable force links are fitted; JP202 is before all raw output capacitance. The matching net labels are continuous electrical connections across the separate blocks.

![[c1-buck-high-side-mosfet-on.png|850]]
*Existing C1 teaching image. High-side metal-oxide-semiconductor field-effect transistor (MOSFET) on, low-side MOSFET off. Geometry is functional, not a pin-level circuit.*

Follow the power loop: input capacitor/source → high-side switch → switch node (**SW**) → L201 → output/load → ground return. The output capacitor carries the difference between inductor current and load current; not every ampere through L201 necessarily enters the load.

Choose positive inductor current from SW toward the output. Define inductor voltage left minus right:

$$
V_L=V_{SW}-V_{out},\qquad \frac{di_L}{dt}=\frac{V_L}{L}
$$

At an **assumed 24 V input and 5.1 V output**, the on-state inductor voltage is approximately **+18.9 V**. The current rises. Some energy goes to the load and some increases the inductor's magnetic store.

## 3. Second state: current keeps moving toward the load

**Return to page 3, BUCK / NATIVE SWITCH NODE, U201 PGND1 pin 9 / PGND2 pin 11 and SW pin 10.** During the low-side interval, the internal low-side switch gives positive inductor current a path from ground toward SW. Follow **fitted JP201 pins 1→2**, then **L201 pin 1→2** and **fitted JP202 pins 1→2** in the same direction as before; the current direction has not reversed merely because the voltage across L201 changes sign.

![[c2-buck-low-side-freewheel-state.png|850]]
*Existing C2. The +/− marks define the left-to-right voltage reference. In this state the left end is actually at lower potential. Falling current still flows toward the load.*

Now the high side is off and the low side conducts. Follow the loop: ground → low-side switch → SW → L201 → output/load → ground. The SW node is near ground, so $V_L\approx-5.1\ \mathrm{V}$. The current slopes downward, but remains positive in the continuous-conduction example.

The switches must not conduct together: that would short the input to ground. Real control includes brief dead time and other switching details; the ideal waveform below omits them. Light-load operation can differ from this continuous-current example.

| State | Approximate SW voltage | Inductor voltage at 24 V input | Current slope |
|---|---:|---:|---|
| High side on | 24 V | +18.9 V | Positive |
| Low side on | 0 V | −5.1 V | Negative, while current can remain positive |

## 4. Read the waveforms from top to bottom

**Match traces to page 3:** native SW voltage belongs at **U201 pin 10 / TP201 SIGNAL pin 1 (`BUCK_SW`)**. **TP202 SIGNAL pin 1 (`L201_IN`)** is after JP201, at **L201 pin 1**; inductor current runs through **L201 pins 1/2**. **TP204 SIGNAL pin 1 (`L201_OUT`)** is at L201 pin 2, before JP202; **TP203 SIGNAL pin 1 (`VOUT_5V1`)** is after JP202 at the raw output bank. Each of **TP201–TP204 RETURN pin 2** joins GND; these are sense connections, not force-current paths. Output-bank current divides among **C209–C214 pins 1/2** and the same-net raw bank **C330–C337 pins 1/2 on page 4**. The plotted capacitor current is the **total** in the ideal model, not a prediction for any individual capacitor; a schematic pin label alone cannot provide that waveform.

![[v2-02-buck-waveforms.png|900]]

1. **Purple:** SW jumps between approximately input and ground. It is not a 5.1 V rail.
2. **Orange:** L201 current forms a triangle. Its average supplies the assumed 5 A load.
3. **Blue:** capacitor current is $i_C=i_L-I_{load}$. Positive current charges the output capacitor; negative current lets it supply the difference.

A steady average output requires no accumulating change in inductor current over a cycle. In the ideal model:

$$
(V_{in}-V_{out})DT+(-V_{out})(1-D)T=0
\quad\Rightarrow\quad D=\frac{V_{out}}{V_{in}}
$$

Here $D$ is duty cycle, the high-side on fraction; $T$ is the full switching period. The basic operating explanation follows the [TI LM61460 datasheet, SNVSBD5D](https://www.ti.com/lit/ds/symlink/lm61460.pdf). This ideal relation does not include losses or controller timing limits.

## 5. Worked example: rebuild one triangle

**Schematic settings:** page 3 BUCK / NATIVE SWITCH NODE **U201 RT pin 6 → R201 pin 1 (33.2 kΩ), R201 pin 2 → GND** sets the nominal 400 kHz. Use **L201 pins 1/2 (`L201_IN` / `L201_OUT`)** for the voltage reference, with JP201/JP202 fitted. The calculation uses the 10 µH candidate now labelled in the WIP PDF; constant inductance remains an assumption.

**ASSUMED:** 24 V in, 5.1 V out, 400 kHz, constant 10 µH, 5 A average current, no losses.

$$
T=\frac{1}{400\,000}=2.5\ \mathrm{\mu s},\qquad
D=\frac{5.1}{24}=0.2125
$$

$$
t_{on}=DT=0.53125\ \mathrm{\mu s},\qquad
t_{off}=1.96875\ \mathrm{\mu s}
$$

The rise during the short on interval is

$$
\Delta I_{on}=\frac{18.9\times0.53125\ \mathrm{\mu s}}{10\ \mathrm{\mu H}}
=1.004\ \mathrm{A}
$$

The fall during the longer off interval is

$$
\Delta I_{off}=\frac{-5.1\times1.96875\ \mathrm{\mu s}}{10\ \mathrm{\mu H}}
=-1.004\ \mathrm{A}
$$

They cancel over the period. Current ranges from approximately **4.498 to 5.502 A**. This is normal-operation ripple under fixed inductance, not the fault peak or an established current rating.

## 6. Why L201 is changing

**Look at page 3, FAULT INJECTION / LOCAL REGULATION, L201 pin 1 (`L201_IN`) / pin 2 (`L201_OUT`).** The two-terminal symbol says where the inductor connects, not how its inductance changes with current or temperature. The 10 µH replacement, Würth **74437636351002**, is now captured in this WIP schematic; capture does not establish qualification or a passed freeze gate. JP201 separates native `BUCK_SW` from `L201_IN`; JP202 separates `L201_OUT` from the raw output bank. The page also identifies **PF2 pin 1 = `VIN_PROTECTED`, PF3 pin 1 = `BUCK_SW`, PF4 pin 1 = `L201_IN`** as M4 force pads.

![[v2-02-inductor-ripple.png|850]]

The inherited inductor is **6.8 µH XAL8080-682MED**. The owner-selected qualification candidate is **10 µH alloy Würth 74437636351002**. At the same applied voltage, a larger constant inductance slows the current change; the lower curve shows that simple effect.

During a fault, **differential inductance** means the inductance at the actual current. Magnetic saturation can reduce it, allowing current to rise faster. The candidate's published current-dependent curve helps the investigation, but hot behavior and production bounds remain **(still open)**. A typical graph is not a guaranteed minimum.

The candidate also changes size, mounting, direct-current winding resistance (**DCR**), ripple and load-step behavior. Heating, physical fit and stable regulation, especially low ripple at 9 V, remain **(still open)**. No illustrative component drawing is a footprint approval.

## 7. Capacitors and feedback: local helpers with costs

**Page 3, BUCK / NATIVE SWITCH NODE:** C201/C202 are the larger input bank, now labelled **10 µF / 50 V each**, and **C203/C204 pins 1/2** are the **100 nF / 50 V** local bypasses. Follow their common **pin-1 net `VIN_PROTECTED`** to **U201 VIN1 8 / VIN2 12** and **pin-2 return GND** to **PGND1 9 / PGND2 11**. The drawing joins the nets logically; only a later layout can make each physical bypass loop short.

![[e1-capacitor-behavior-and-effective-capacitance.png|850]]
*Existing E1: conceptual capacitor behavior. A nominal capacitance label is not the effective value under voltage, temperature and tolerance.*

The **input capacitors** provide switching-current pulses close to the chip. The source study asks for at least **10 µF effective main input ceramic capacitance**, plus nominal **100 nF local bypassing at each VIN/PGND pair**. Every local reservoir and bypass must fit the proposed **30 µF total effective maximum**. More input capacitance can help normal switching while storing more fault energy.

The **output bank** supplies the load while inductor current catches up. Capacitance controls gradual voltage change; equivalent series resistance (**ESR**) adds an immediate voltage component when capacitor current changes. Effective capacitance, ESR and startup stress must be qualified together.

**Page 3, FAULT INJECTION / LOCAL REGULATION, C209–C214:** each **pin 1** connects to raw `VOUT_5V1` after **JP202 pin 2**, each **pin 2** to GND. Also find the larger raw bank at **page 4, C330–C337 pins 1/2**. Those capacitors are on the same raw net even though a different sheet draws them; the sheet boundary does not remove their stored energy.

![[d5-lm61460-feedback-principle.png|800]]
*Existing D5: feedback is local to the raw output, before the series disconnect. Arrows describe control information, not a power path.*

The captured **100 kΩ / 24.4 kΩ** feedback divider sets about **5.098 V** locally. Feedback adjusts energy delivery when this voltage changes. It does not measure Pi-header ground rise or harness loss. Keeping the sense route quiet matters because a false reading prompts a real control action.

![[v2-02-circuit-feedback.png|900]]
*Exact DC feedback branch from page 3. R202 pin 1 samples raw output; **R202 pin 2 / R203 pin 1** form `BUCK_FB` and reach **U201 FB pin 4**. R203 pin 2 returns to GND, shared with **U201 AGND pin 3**. The feedforward branch C207/R205 is omitted from this small excerpt, not removed from the design.*

![[f2-04-feedback-circuit.png|850]]
*Circuit companion F2.4 in [BATCH_F](../illustrations/BATCH_F.md). Reproduce the exact excerpt with `python3 -B docs/lessons/figures/src/circuit_02.py`.*

Two other pin pairs explain useful boundaries. **Page 3 U201 VCC pin 2 → C206 pin 1, C206 pin 2 → GND** is the chip's internal-supply bypass, not an external accessory supply. **C205 pin 1** connects to **CBOOT pin 14 (`BUCK_CBOOT`)**; **C205 pin 2** returns to **SW pin 10 (`BUCK_SW`)**, on the native switch-node side of JP201, not `L201_IN`. The bootstrap capacitor therefore sees their differential voltage, not simply the input voltage to ground. **EN/SYNC pin 7** follows `BUCK_INPUT_PGOOD` from page 2 **U101 PGOOD pin 16**; an enable permission is separate from the raw-output feedback measurement.

## 8. What goes wrong: the controller loses its switch

**Find page 3 U201 VIN pins 8/12 and SW pin 10; follow `BUCK_SW` through fitted JP201 pins 1→2, L201 pins 1→2 and fitted JP202 pins 1→2 to `VOUT_5V1`.** The failure joins the internal high-side path permanently. Changing **FB pin 4** or **EN/SYNC pin 7** cannot open shorted silicon. The revised architecture D series/crowbar/control arrangement and raw dump are **frozen on paper, not yet in the schematic** in the [older review snapshot](SCHEMATIC_READING_GUIDE.md#snapshot-versus-current-decisions); that snapshot's page 4 shows an earlier preliminary implementation.

![[p03-02-buck-normal-vs-shorted.png|850]]

With a permanent high-side short, SW stays near input. Using the **same assumed 10 µH** at the beginning of a 24 V fault:

$$
\frac{di}{dt}=\frac{24-5.1}{10\ \mathrm{\mu H}}=1.89\ \mathrm{A/\mu s}
$$

Ten microseconds would add roughly **18.9 A** if that initial voltage and inductance remained constant. The inductor cannot contain a source that stays connected indefinitely. Saturation can make the rise faster. See [[03 Output protection]] for the reused pilot fault model and its explicit limitations.

![[f2-03-hot-loop-3d.png|800]]
*BATCH_F F2.3. The outlined hot loop is the switching-current **difference/commutation loop**, not simultaneous conduction through both switches.*

A second failure comes from physical layout: a large loop adds unwanted inductance, making rapid current changes generate extra voltage. Keep local input bypasses close to both VIN/PGND pairs and feedback away from SW. This is a future layout principle; **no PCB is routed**.

## 9. Why this design and not another

LM61460 is the captured synchronous buck choice. The bigger inductor is a qualification direction because the small inherited part lacks a justified fault-current inductance bound across the studied range. The cost is size and changed normal behavior. Gate 3b therefore couples the candidate with timed source isolation and controlled capacitance. Replacing L201 alone cannot solve an indefinitely energized fault.

> [!warning] Common misconceptions
> Negative inductor voltage does not instantly reverse current. SW is not the regulated output. A 10 µH label does not establish hot fault behavior. Extra capacitance can increase fault energy. Feedback cannot command a physical short off.

## 10. Check yourself

1. Why does current still flow toward the load with SW near ground?
2. Why are the up and down slopes different but their current changes equal?
3. When does the output capacitor supply current to the load?
4. Why does the new inductor still require qualification?

> [!question]- Answers
> 1. The inductor's stored energy sustains positive current while negative voltage reduces it.
> 2. The on/off durations differ; equal and opposite changes give a steady repeating cycle.
> 3. When load current exceeds inductor current; $i_C=i_L-I_{load}$ is then negative.
> 4. Its current/temperature-dependent inductance, thermal behavior, mounting and regulation are unproved.

## 11. One-page visual summary

![[v2-02-buck-waveforms.png|700]]
*Page 3: find native SW pin 10 / TP201 pin 1 before JP201, L201 pin 1 / TP202 pin 1 at `L201_IN`, L201 pin 2 / TP204 pin 1 at `L201_OUT`, raw output after JP202 at TP203 pin 1 (`VOUT_5V1`), then FB pin 4 at the divider midpoint. These are distinct named nodes; JP201/JP202 join the force path only when fitted.*

| Picture to remember | Equation / boundary |
|---|---|
| High-side push | $V_L\approx V_{in}-V_{out}$; current rises |
| Low-side coast | $V_L\approx-V_{out}$; current falls but can stay positive |
| Capacitor shares the load | $i_C=i_L-I_{load}$ |
| Example at 24 V | **21.25% duty**, **1.004 A** peak-to-peak, ideal 10 µH |
| Candidate decision | **74437636351002**, selected for qualification only |
| Failed switch | Independent Sheet 03 and a bounded source are required |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): BUCK, LM, L, SRC, BASIS and G4. Gate 4a-FIX `2b99ac7` retains magnetic, capacitor and source qualifications as open. [BATCH_F](../illustrations/BATCH_F.md) contains the flywheel and hot-loop prompts. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 02`.

Previous: [[01 Input protection]] · Next: [[03 Output protection]] · Terms: [[99-Glossary]]
