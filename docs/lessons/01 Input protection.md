---
title: "Input protection"
lesson: 1
tags: [v1a, lesson, visual]
---

# 01 — Input protection

> [!abstract] In one sentence
> Four different input guards manage sustained overcurrent, brief surges, reversed connections and unsuitable supply conditions; none alone guarantees a safe 5 V output.

## 1. An everyday picture: guards at an entrance

![[f1-01-input-guards-analogy.png|850]]
*BATCH_F F1.1. Four responsibilities, not four identical switches. “Backwards power” groups two different cases: reversed input polarity and output backfeed; each needs its own path analysis.*

A building entrance has a guard who checks visitors, a barrier that closes, an emergency overflow channel and a last-resort breakaway link. Giving every guard the same job would leave gaps. V1A similarly combines a fuse, a transient voltage suppressor (**TVS**), a reverse-protection arrangement and an electronic fuse (**eFuse**).

**Learning goals:** trace the real input path; distinguish standoff, breakdown and clamp; read the voltage window; explain why 5 A out can need much less than 5 A in.

> [!warning] Status
> Normal input is **9–26 V**. **Gate 4a-FIX freeze BLOCKED. PRELIMINARY TEST BOARD — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Component selections below are not installed protection ratings.

## 2. Picture walkthrough: where current actually travels

Open **PDF page 2, “01 INPUT PROTECTION”** in [V1A_GATE4B_WIP_2026-10-03.pdf](/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_GATE4B_WIP_2026-10-03.pdf#page=2). Page 1 is the hierarchy, so “Sheet 01” is **not** PDF page 1. The schematic walks below use this WIP PDF: Sheets 01–02 are redrawn to the frozen design; Sheets 03–05 retain their earlier drawings. Page 2 now labels F101 `12.5A T / 125VDC`, D101 `SMCJ36CA 36V bidirectional` and the input requirement 9–26 V. The [schematic reading guide](SCHEMATIC_READING_GUIDE.md) and embedded page image still describe the older review PDF.

![[v2-review-p02.png|1000]]
*Historical review-PDF page 2, retained for context. For the current walk, open the WIP PDF linked above: INPUT / REVERSE POLARITY is upper left, EFUSE / SOURCE DISCONNECT is to its right, and MAIN CURRENT / COUPON ISOLATION is below the input block.*

![[b2-conceptual-input-protection-placement.png|850]]
*Existing B2 image: conceptual placement only. Current owner selections are D101 **SMCJ36CA** and F101 **Schurter 3403.0285.23**, regardless of older labels. No PCB is routed.*

Read the paths in this order:

1. **Enter — page 6, DC INPUT / FIXTURE POWER RETURN, J501 pins 1 (+), 2 (RETURN); page 2, INPUT / REVERSE POLARITY, F101 pins 1→2.** `VIN_RAW` joins those pages. Follow F101 to `VIN_FUSED`: the fuse is in series with the positive supply, not across it.
2. **Divert — page 2, same block, D101 pins 1/2.** Pin 1 joins `VIN_FUSED` and pin 2 joins GND. This branch leaves before Q101 and U101, so surge current through D101 passes through F101 but **does not pass through the downstream eFuse**. The bidirectional device has no ordinary single-anode direction to infer from “pin 1.”
3. **Block reverse paths — page 2, Q101 S pins 1/2/3, D pins 5/6/7/8 and G pin 4.** Read the grouped pins as terminals of one power transistor. Q102 S pin 2 is tied to `VIN_FUSED`, **not GND**; D pin 3 joins Q101's gate, and G pin 1 follows U101 DRV pin 4. Q102 helps discharge that gate relative to the source. The power body-diode direction is source-to-drain, from `VIN_FUSED` toward `VIN_EFUSE_IN`; the WIP pin rectangle does not draw that diode. Do not equate an OFF transistor with two-way blocking in every power state.
4. **Admit — page 2, EFUSE / SOURCE DISCONNECT, U101 IN pins 1/2 → OUT pins 17/18.** Its internal switch is inside the IC rectangle. Follow OUT to `EFUSE_OUT`, then **MAIN CURRENT / COUPON ISOLATION, JP101 FORCE_A pin 1 → FORCE_B pin 2**, to reach `VIN_PROTECTED` when the removable force link is fitted. JP101 is before all main local input capacitors; **TP103 SIGNAL pin 1** observes `EFUSE_OUT`, with **RETURN pin 2** at GND. Continue to page 3 U201 VIN pins 8/12. This is the protected **buck input**, not the protected 5 V output.
5. **Locate D102 — page 2, EFUSE / SOURCE DISCONNECT, STPS60H100CT.** Its **A1 pin 1 / A2 pin 3** join GND; **K_TAB pin 2 and the tab** join `VIN_PROTECTED`. This is a separate branch from D101 at `VIN_FUSED`.
6. **Return — page 2, U101 GND pin 8 / EP pin 25, and page 6 J501 RETURN pin 2.** The ground symbols express common connectivity. They do not specify zero-resistance copper, a short physical return or the eventual probe connection.

| Guard | Selected device / arrangement | What must be established |
|---|---|---|
| Fuse | F101 Schurter 3403.0285.23 | Hot hold current, total clearing, DC interruption and source/wire coordination |
| TVS | D101 Littelfuse SMCJ36CA | Pulse clamp at actual current, temperature and repetition |
| Reverse path | Q101 CSD19537Q3 with Q102 BSS138 control | Gate voltage, body-diode paths, reversed input and backfeed cases |
| Electronic admission | TPS26630 | Threshold corners, current limit, startup and physical cutoff |

The fuse is a **12.5 A time-lag** part, with **125 VDC / 1000 A DC interruption** at its specified conditions. Its number is not V1A's output-current rating. Installed clearing, hot surge behavior and coordination remain **(still open)**.

## 3. TVS: three voltage labels, three meanings

**Look at page 2, INPUT / REVERSE POLARITY, D101 pins 1/2 and F101 pin 2.** The curve is voltage **across D101** versus current **through its branch**. It is not the voltage at U101 OUT or the Pi. The owner-selected SMCJ36CA is now labelled on this WIP page; the embedded historical page image retains the old label.

![[v2-01-tvs-iv.png|850]]

Follow the positive-polarity curve from left to right. The bidirectional CA part also has an avalanche behavior under reversed polarity; this plot only shows the positive magnitude.

1. At **36 V standoff**, the device is specified to have only small leakage under its stated test conditions. “36 V TVS” does not mean a surge stays at 36 V.
2. **40.0–44.2 V breakdown** is specified at **1 mA**. It describes the beginning of appreciable avalanche conduction.
3. At the specified **25.9 A pulse**, the maximum clamp is **58.1 V**, for the datasheet's **25°C, 10/1000 µs** test conditions.

The drawn curve between the anchors is **ASSUMED**, not a measured characteristic or a hot guarantee. Read the anchors as different tests, not as an accurate interpolated component model. These values come from the [Littelfuse SMCJ datasheet, 2025-02-27 v.2](https://www.littelfuse.com/assetdocs/littelfuse_tvs_diode_smcj_datasheet?assetguid=37388813-0d6d-4329-969b-1aa8b7614ac1).

The higher standoff avoids the old 26 V device conducting during some studied upstream faults. The cost is a higher clamp: the **58.1 V figure cannot be allowed directly onto the LM61460 input**. The main eFuse's dynamic let-through and the separately supplied auxiliary branch need their own review.

## 4. eFuse: read the window, then read its uncertainty

**Read page 2, EFUSE / SOURCE DISCONNECT, the divider resistors below U101:** R101 pin 2 / R102 pin 1 form `INPUT_UVLO`, which reaches **U101 UVLO pin 6**; R103 pin 2 / R104 pin 1 form `INPUT_OVP`, which reaches **U101 OVP pin 7**. R101/R103 pin 1 watch `VIN_FUSED`; R102/R104 pin 2 return to GND. Equal net labels join the divider to the IC without a long wire crossing the page.

![[v2-01-circuit-dividers.png|950]]
*Exact sensing subset. Follow each divider midpoint to its named U101 pin. The two midpoint wires are separate nets.*

![[f1-04-input-sense-circuit.png|850]]
*Circuit companion F1.4 in [BATCH_F](../illustrations/BATCH_F.md). Runnable exact excerpt: `python3 -B docs/lessons/figures/src/circuit_01.py`.*

![[f1-03-efuse-three-jobs.png|800]]
*BATCH_F F1.3. Admission, cutoff and current limiting are different actions. A commanded cutoff has a response delay.*

![[v2-01-efuse-window.png|900]]

Read the top ruler first. **Undervoltage lockout (UVLO)** holds the path off below its threshold; **overvoltage protection (OVP)** commands cutoff above its threshold. Baseline nominal rising thresholds are **8.46 V** and **27.63 V**. The normal-input requirement remains **9–26 V**, inside that wider nominal window.

Now read the enlarged lower ruler:

- The inherited rising OVP screen spans **26.97–28.29 V**. A 27 V test can trip one corner and leave another on. **27 V is a fault-test point, not guaranteed normal operation or a guaranteed trip.**
- The falling/reset screen spans **25.00–26.58 V**. After a trip, returning to 26 V does not guarantee recovery.
- The initial minimum rising screen is only **0.97 V above 26 V**. Hot drift, restart and nuisance-trip behavior are **(still open)**; the plotted bands are not complete hot limits.

Startup control reduces the rate at which the downstream voltage rises. It is not a promise of a particular inrush current: capacitor current also depends on effective capacitance through $I=C\,dV/dt$.

Find **U101 dVdT pin 9 → C103 pin 1; C103 pin 2 → GND** in the page-2 EFUSE / SOURCE DISCONNECT block. This capacitor programs a voltage-ramp behavior. Separately, **ILIM pin 10 → R105 pin 1; R105 pin 2 → GND** programs the input current-limit screen. They are two different control pins, not two names for one limit.

## 5. Worked example: why the input limit can be below 5 A

![[v2-01-input-current.png|800]]

**Calculation boundary — page 2 U101 OUT pins 17/18 (`EFUSE_OUT`) → fitted JP101 pins 1→2 (`VIN_PROTECTED`) → page 3 U201 VIN pins 8/12; raw output at JP202 pin 2 (`VOUT_5V1`), after L201 pin 2 (`L201_OUT`) and fitted JP202 pins 1→2.** The example compares power on opposite sides of the buck. It does not compare the input current with a current through the same series wire.

**ASSUMED:** local output 5.1 V at 5 A, buck efficiency 90%, and **9 V at the buck input**. Ignore input-path and auxiliary losses for this example.

$$
P_{out}=5.1\times5=25.5\ \mathrm{W}
$$

$$
I_{in}=\frac{P_{out}}{\eta V_{in}}
=\frac{25.5}{0.90\times9}=3.15\ \mathrm{A}
$$

At 24 V the same estimate is **1.18 A**. The eFuse's roughly **4.48 A nominal input limit** therefore does not contradict a 5 A output target. At low input voltage, current and losses increase; the graph does not prove startup or hot full-load capability.

## 6. What goes wrong: assigning each guard a fixed timescale

![[f1-02-tvs-vs-fuse-timescale.png|850]]
*F1.2 requires regeneration with the corrected BATCH_F prompt. The existing “eFuse acts in between” / millisecond placement is **not a valid timing bound**. eFuse response depends on the fault and action; fuse clearing depends on current. Use this picture only to distinguish mechanisms.*

A TVS diverts current when voltage rises. A fuse must heat enough to open. An eFuse detects a condition and changes semiconductor conduction. These responses overlap in time; they are not exclusive microsecond/millisecond/second lanes.

A particularly important failure is a **sustained excessive voltage**. The TVS could keep dissipating heat while the current is too small to clear F101. The downstream 4.48 A limit cannot guarantee blowing a 12.5 A fuse, and it does not limit the upstream TVS branch at all.

**Trace that failure on page 2:** F101 pin 2 branches straight to D101 pin 1, while **U101 ILIM pin 10** controls only the eFuse path. For a shutdown request, find **U101 SHDN pin 12 and TP101 pin 1 (`INPUT_SHDN`)**. A falling command there is not proof of current extinction at OUT pins 17/18. The later autonomous source trigger is **frozen on paper, not yet in the schematic** as a completed circuit; the page-4 historical shutdown sink cannot establish the later 10 µs contract.

```mermaid
flowchart LR
    F["Sustained upstream fault"] --> T["TVS may keep conducting"]
    T --> H["Heat accumulates"]
    H --> X["Pulse rating alone cannot prove survival"]
    F --> C["Need bounded source shutdown and fuse coordination"]
```

A different failure starts **inside the buck** at an otherwise normal input. Source isolation is necessary but leaves charged capacitors downstream. The development route calls for **10–30 µF effective local input capacitance** and a **physical cutoff within 10 µs** of fault onset. The independent fault trigger and full isolation time are **(still open)**; see [[03 Output protection]].

## 7. Why this design and not another

The owner chose 9–26 V to give the nominal 24 V source normal tolerance room; it is a requirement to prove, not permission for sustained 33.6 V operation. The required isolated upstream module is **(still open)** in model and qualification. The UENPO non-isolated module was rejected because its failed high-side switch can create a direct battery pass-through path.

The larger SMCJ36CA improves the studied pulse-power/standoff screen but raises clamp exposure. A bidirectional TVS ahead of Q101 avoids the straightforward forward-conduction path a unidirectional diode would create under reversed input. The selected larger time-lag fuse improves an assumed hot hold-current screen but clears moderate faults more slowly. Each choice trades one margin for another; source shutdown and component coordination remain necessary.

> [!warning] Common misconceptions
> A fuse is not a universal fast-spike stopper. Standoff is not clamp voltage. An OVP threshold is not a maximum transient peak. TPS26630 does not replace the captured external reverse-input arrangement. Input protection cannot by itself contain a shorted buck switch.

## 8. Check yourself

1. Why does TVS current bypass the eFuse's current limit?
2. What does the 58.1 V label actually mean?
3. Why might a 27 V OVP test leave the input on?
4. Why does 5 A at the output need only about 1.18 A at 24 V in the example?

> [!question]- Answers
> 1. D101 branches from the fused node before the eFuse; topology determines the current path.
> 2. A specified clamp maximum at a particular pulse current and test condition, not a continuous rail or hot installed limit.
> 3. The inherited rising threshold screen extends above 27 V, to about 28.29 V.
> 4. The converter lowers voltage while approximately conserving power; 90% efficiency supplies the assumed loss.

## 9. One-page visual summary

![[v2-01-efuse-window.png|700]]
*Page 2: divider midpoint → U101 UVLO 6 / OVP 7. Return to the upper power path to distinguish sensing from interruption.*

| Remember | Current fact | Still owed |
|---|---|---|
| Normal input | **9–26 V** | Complete source waveform within range |
| D101 | **SMCJ36CA**, 36 V standoff | Hot/repeated pulse and downstream clamp exposure |
| F101 | **3403.0285.23**, 12.5 A time-lag | Installed hold/clearing and DC source coordination |
| eFuse | **8.46 / 27.63 V** nominal admission thresholds | Tolerance, hot behavior and restart |
| Source isolation | **≤10 µs**, **≤100 µC** proposed contract | Autonomous trigger and whole-event measurements |
| Release | **BLOCKED** | No Pi before required qualification gates |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): IN, TVS, SRC, BASIS, G4, OWNER. Threshold corners also read from `0677fea:GATE2C_REVIEW_CLOSURE.md` under `docs/evidence/r2/sheet03/`; Gate 4a-FIX `2b99ac7` retains source/auxiliary gaps. [BATCH_F](../illustrations/BATCH_F.md) records the F1.2 correction. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 01`.

Previous: [[00 System overview]] · Next: [[02 Buck converter LM61460]] · Terms: [[99-Glossary]]
