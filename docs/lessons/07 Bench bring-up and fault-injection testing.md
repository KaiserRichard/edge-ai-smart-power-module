---
title: "Bench bring-up and fault-injection testing"
lesson: 7
tags: [v1a, lesson, visual]
---

# 07 — Bench bring-up and fault-injection testing

> [!abstract] In one sentence
> Bring-up turns a conditional design claim into evidence by increasing stress in controlled steps and measuring the actual load endpoint before connecting a Pi.

## 1. An everyday picture: climb stairs, do not jump to the roof

![[f7-02-bring-up-staircase.png|850]]
*BATCH_F F7.2 compresses the learning sequence into seven pictures. The full required sequence below includes separate rail, ripple, transient, fault and telemetry checks.*

Before driving a repaired car on a motorway, you inspect it, check basic functions and try it under controlled conditions. A power board deserves the same progression. A working indicator light or one good no-load voltage is only one step.

Every step asks a particular question. If the answer fails or is uncertain, stop increasing stress and investigate. A dummy load makes early tests possible without using the expensive computer as a detector of mistakes.

**Learning goals:** explain the sequence, place the measurements, apply uncertainty to a pass line, and distinguish autonomous protection from a fixture rescuing the board.

> [!warning] Current status
> **Architecture D is a PRELIMINARY TEST BOARD proposal. Gate 4a-FIX capture freeze BLOCKED; no PCB routed; no physical tests reported by the cited plan. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Application margins are **(still open)**. The rated injector/abort/discharge fixture is incomplete; this lesson is not a build or live-test authorization.

## 2. Picture walkthrough: each instrument answers a different question

Open **PDF page 6, DC INPUT / J501, LOAD OUTPUT / J502 and BENCH TEST ACCESS**, with the [schematic reading guide](SCHEMATIC_READING_GUIDE.md). **J501 pins 1/2** receive the reviewed supply pair; **J502 pins 1/2** lead to the proposed dummy harness. Those connector symbols show electrical boundaries, not a built or rated bench fixture.

![[v2-07-circuit-test-nets.png|950]]
*Exact captured test-net excerpt. TP501/TP502/TP503/TP504 each have **one pin**. A voltage test point is neither a high-current force terminal nor an installed current sensor.*

![[f7-04-test-nets-circuit.png|900]]
*Circuit companion F7.4 in [BATCH_F](../illustrations/BATCH_F.md). Run `python3 -B docs/lessons/figures/src/circuit_07.py` for the exact excerpt.*

![[f7-01-bench-station-overview.png|900]]
*BATCH_F F7.1. A conceptual station, not an inventory of available or calibrated equipment.*

| Follow the bench | Question answered | Limit to remember |
|---|---|---|
| Current-limited supply | Is input voltage/current controlled? | Its limit may be too slow for a fast fault and does not empty local capacitors |
| Dummy resistor/electronic load | Can the path deliver normal and changing load? | Resistor current varies with voltage; an electronic load has its own control and ratings |
| Oscilloscope + differential probes | What happens during startup, ripple, a load step and a fault? | Probe bandwidth, loading, voltage range and uncertainty matter |
| Current probe(s) | When does source current really stop; where does stored current flow? | Offset, bandwidth and timing alignment affect charge/energy integration |
| Multimeter / temperature instruments | Are connections/steady rails correct; how hot are parts? | Slow voltage readings cannot establish a fast peak; surface and junction temperatures differ |

The dummy header must represent the intended endpoint. The existing Harwin selection fails its resistance criterion; newer connector proposals in Lesson 05 remain unqualified. The actual Pi input model is **(still open)**. A test fixture needs explicit load capacitance and ESR cases rather than a guess that one dummy perfectly represents the Pi.

**Keep the initial fault setup separate from the host interface:** page 6 **J503 pins 1–4** are the host GND/reference/SDA/SCL connection. The cited fixture plan removes the host, USB and Pi during initial faults. A proposed external dummy header has no refdes in this PDF; do not treat the generic J502 symbol as that header.

## 3. Follow the gates in order

| Step | Action after its prerequisites pass | Evidence to keep |
|---:|---|---|
| 1 | Visual inspection | Assembly, polarity, parts and damage record |
| 2 | Continuity and short checks | Intended connections and absence of unintended shorts |
| 3 | Current-limited bench source | Reviewed voltage/current/energy setup |
| 4 | No-load startup | Startup waveform and supply behavior |
| 5 | Verify output and control rails | Correct levels, sequencing and usable driver supply |
| 6 | Low-current dummy/electronic load | First controlled loaded behavior |
| 7 | Increasing load steps | Voltage and current at each step |
| 8 | Thermal measurements | Component-local temperatures under stated conditions |
| 9 | Ripple measurements | Correct probe method, bandwidth and conditions |
| 10 | Transient/load tests | Minima, maxima and recovery |
| 11 | Reviewed protection/fault tests | Whole-event waveforms, component stress, source cutoff and disposal |
| 12 | Telemetry validation | Calibration, domains, timing and reset behavior |
| 13 | SBC integration | **Only after all previous and interface gates pass** |

Use the following schematic landmarks while reading the sequence. They are reading locations, not an instruction to energize unfinished hardware:

| Steps | PDF page, block, refdes and pin | What the drawing can establish |
|---|---|---|
| 1–2: inspect/check connections | Page 6, DC INPUT **J501 1/2**, LOAD OUTPUT **J502 1/2**; page 5 **R401 force 1/4** | Intended polarity and continuity. Actual assembly, shorts and mating orientation need physical inspection. |
| 3–4: limited input/startup | Page 2, EFUSE **U101 OUT 17/18, dVdT 9**; page 3 **U201 EN/SYNC 7** | Which input, ramp and enable nodes to observe; not proof of their startup waveforms. |
| 5: verify rails | Page 4 **TP301 1 raw, TP302 1 protected**; page 5 **U402 OUT 5 / TP404 1** | Three different rails. The later held-up control rails are paper proposals, not the old LDO rails drawn on page 4. |
| 6–7: apply increasing dummy load | Page 6, LOAD OUTPUT **J502 1/2**; page 5 **R401 force 1/4** | Load and shunt boundaries. The fixture's own force connections/rating are outside this drawing. |
| 8: thermal | Page 3 **U201 power pins 8–12, L201 1/2**; page 4 **Q301/Q302 power pins**; page 5 **R401 1/4** | Identifies parts whose local heat matters. A schematic contains no temperature measurement. |
| 9–10: ripple/load transients | Page 3, OUTPUT / FEEDBACK **L201 2 / R202 1**; page 6 **TP503 1 / TP504 1** plus the external endpoint | Compare local raw, module load output and far-end differential voltage; they are not interchangeable. |
| 11: faults | Page 2 **U101 SHDN 12**, page 3 **U201 SW 10 / L201 1**, page 4 **Q301/Q302 G 4 and S 1–3** | Locates commands and physical power paths. Completed injector, source trigger and new dump hooks remain absent. |
| 12: telemetry | Page 5 **U401 IN+ 10 / IN− 9, VBUS 8, VS 6, SDA 4 / SCL 5** | Identifies the analog, power and digital quantities to compare with calibrated instruments. |
| 13: integration | Page 6 **J502 1/2 and J503 1–4** | Identifies the module interfaces only; the Pi/robot integration review remains external and gated. |

The planned normal matrix includes **9, 24 and 26 V**, and **0, 2.5 and 5 A** load cases with controlled temperature states. **27 V is an additional OVP/fault-window test**, outside normal operation. A fitted eFuse may already be off there; that run cannot prove interruption of an energized source. Do not bypass its protection to relabel the run.

Change connections only with supplies off and stored charge discharged. The sequence begins only after schematic, layout and fabrication-readiness review have authorized the actual hardware and fixture.

## 4. Where the probes go

![[f7-03-probe-placement.png|900]]
*BATCH_F F7.3. Measure far-end positive against its own return. The picture omits additional source/dump-current channels required by the full plan.*

Read from left to right:

1. **Raw voltage — page 4, RAW BULK / FAULT-RISE BUFFER, TP301 pin 1 at `VOUT_5V1`, against its local return.** This is before the series pair. It observes the failed buck/raw bank; the later raw dump is not drawn in this snapshot.
2. **Protected voltage — page 4, OPPOSED SERIES FETS, TP302 pin 1 at Q302 drains 5–8.** This is `VOUT_PROTECTED`, before the shunt, not `LOAD_5V1`. Use the protected bank's own local return in the future fixture.
3. **Module output and far end — page 6, LOAD OUTPUT, TP503 pin 1 / J502 pin 1, with J502 pin 2 return.** These are module-side anchors. The far-end probe goes across the external dummy header's own positive and loaded return contacts; no PDF test point reaches that external plane.
4. **Inductor current — page 3, OUTPUT / FEEDBACK, L201 pins 1/2.** The proposed current-probe force link is outside the captured schematic. Record actual inductor current through cutoff and the tail, not merely voltage at a nearby test point.
5. **Source and disposal currents — page 2 U101 OUT pins 17/18 before the counted input bank; page 4 protected ballast R308–R311 and Q303 drains 5–8.** The later source-current link, raw-dump link and final fixture construction are **frozen on paper, not yet in the schematic**. Named reservations in the test plan are not evidence of fitted hardware.

Instrument grounds must not create a parallel return that makes the harness look better than it is. Use the reviewed differential/isolation arrangement while keeping equipment protective earth intact. Start recording **before** the fault with pre-trigger history and retain the entire decay/recovery tail.

The high-side-short injector must preserve the actual **input → failed-switch path → L201 → output** fault mechanism. Driving an external supply directly into the output tests a different event. The reviewed fixture must also prevent an unintended short through the native low-side switch; its construction remains blocked. Never improvise a short across an operating converter.

**Find that fault in page 3 U201 VIN pins 8/12 → internal high-side path → SW pin 10 → L201 pin 1.** The PDF still joins native SW directly to L201. The later fixture's isolation/injection changes are **frozen on paper, not yet in the schematic** and cannot be inferred from the existing wire. Likewise, the revised architecture D pair/crowbar controls and raw dump must not be treated as captured just because an earlier pair and crowbar appear on page 4.

## 5. Worked example: a displayed peak needs an uncertainty margin

**Measurement anchor — page 6 J502 pins 1/2, continued through the proposed harness to the external dummy header.** The acceptance limit applies at that far end against its own return. A trace at **page 4 TP302 pin 1** or **page 6 TP503 pin 1** alone is a different measurement and cannot establish this result.

![[v2-07-measurement-uncertainty.png|900]]

The plotted readings are **ASSUMED examples**, not measured traces. Suppose the justified voltage uncertainty allowance is **15 mV**:

$$
V_{peak,read}+U_V<5.5\ \mathrm{V}
$$

A displayed **5.470 V** gives an upper screen of **5.485 V**, below 5.5 V. A displayed **5.490 V** gives **5.505 V**, which does not establish a pass. Thus, with this uncertainty, the recorded fault peak must be **strictly below 5.485 V**.

The normal minimum uses the opposite direction:

$$
V_{min,read}-U_V\ge4.75\ \mathrm{V}
\quad\Rightarrow\quad V_{min,read}\ge4.765\ \mathrm{V}
$$

A 4.760 V reading is insufficient under that allowance. Actual probe/scope calibration, bandwidth, noise, offset and timing evidence must substantiate the uncertainty budget; the plan's 15 mV number is not an instrument certificate.

## 6. What goes wrong: a test fixture silently does the protection's job

![[f3-04-fault-bench-no-pi.png|850]]
*BATCH_F F3.4. The computer remains disconnected. “After fault tests” is necessary but not sufficient: normal, thermal, telemetry and interface gates also apply.*

There are two different source-cutoff experiments:

| Mode | Who starts the source cutoff? | What a successful run can show |
|---|---|---|
| Autonomous board | Its own real fault detector | Potential evidence for the full source-containment claim, if all endpoints pass |
| Fixture timed | An external timer synchronized to injection | Behavior **conditional on** a supplied cutoff time; cannot prove the missing autonomous trigger |

If the fixture's emergency abort saves a run, record that fact. It is not a board protection PASS. The planned autonomous contract is physical source-current cutoff within **10 µs of fault onset**, plus **whole-event positive replenishment charge ≤100 µC**, both including uncertainty. An SHDN logic edge is not the same as stopped current.

Compare **page 2 U101 SHDN pin 12 / TP101 pin 1** with the actual current leaving **OUT pins 17/18 before C201–C204 on page 3**. The former is a command; the latter is the source-energy boundary. **Page 6 TP502 pin 1** observes that net's voltage, not its current. A current sensor/link still has to be implemented and qualified.

![[v2-07-source-charge-tail.png|850]]

The teaching plot assumes **10 A for 10 µs**, then only **10 mA for the remaining 1990 µs**. The first interval already delivers 100 µC. The small tail adds

$$
Q_{tail}=0.010\ \mathrm{A}\times1990\ \mathrm{\mu s}=19.9\ \mathrm{\mu C}
$$

The total is **119.9 µC before uncertainty**. Integrating only the first 10 µs would miss the violation. Integrate positive replenishment over the whole event; negative current cannot cancel the positive-charge limit. Account for current-probe offset/noise before positive clipping.

## 7. The source is off; stored energy is still present

**Find the stores and drains:** page 3 **C201–C204 pins 1/2** are local input stores; page 4 **C330–C337 pins 1/2** are the raw bank, and **R308–R311 pins 1/2 → Q303 drains 5–8 → sources 1–3 GND** form the earlier protected crowbar path. The protected-module capacitor proposal, raw dump and external dummy capacitor are **frozen on paper, not yet in the schematic** as the later intended assembly. They do not have valid captured PDF pins to invent here.

![[f3-03-two-sides-two-drains.png|800]]
*BATCH_F F3.3. After the series pair opens, the protected crowbar cannot absorb energy isolated on the raw side.*

A dummy capacitor also stores energy. For the plan's **ASSUMED 2.2 mF at 5.5 V**:

$$
E=\tfrac12CV^2=\tfrac12(0.0022)(5.5)^2
=0.033275\ \mathrm{J}=33.275\ \mathrm{mJ}
$$

That is not a measurement of Pi capacitance. Add it to the appropriate protected-side stress accounting, while the raw bank and inductor need their separately rated destination. Record control rails and useful gate drive until the energy is disposed of; a collapsing driver supply can invalidate an otherwise good command sequence.

For retained **WFMB2512 ballast**, the plan requires pre-pulse terminal temperature plus uncertainty **≤85°C**, and terminal temperature including the pulse rise **below 95°C**. Room temperature cannot substitute for resistor-terminal temperature. MOSFET junction, resistor terminal, board and ambient temperatures are different quantities.

## 8. Why this design and not another

A staged dummy-load bench lets us test a failing hypothesis without placing the Pi at the end of an unqualified path. Simultaneous raw/protected/far-end channels distinguish a good local clamp from a bad harness result. Whole-event recording distinguishes a fast-looking command from actual current extinction and successful energy disposal. These choices test the specific open contracts; a generic load test or a single multimeter reading cannot do that.

> [!warning] Common misconceptions
> A supply limit does not bound capacitor discharge. A fixture rescue is not autonomous protection. One acceptable voltage peak does not prove component survival. A dummy-load pass covers tested conditions only. No Pi is connected merely because one trace looks good.

## 9. Check yourself

1. Why start recording before injection?
2. Which ground reference belongs to the far-end probe?
3. Does 5.490 V with 15 mV uncertainty establish the peak requirement?
4. What does the tiny current-tail example teach?

> [!question]- Answers
> 1. To identify physical onset and capture the entire causal sequence and pre-fault state.
> 2. The far-end loaded return; a module-ground reference misses return-path effects.
> 3. No: the upper screen is 5.505 V.
> 4. Small current integrated over a long tail can violate the whole-event charge contract.

## 10. One-page visual summary

![[f7-03-probe-placement.png|700]]

| Before / during / after | Keep this evidence |
|---|---|
| Before | Reviewed board/fixture, staged checks, calibrated instruments, dummy load |
| During | Raw + protected + **far-end** voltages; source, inductor and disposal currents |
| Acceptance | Peak + uncertainty **<5.5 V**; normal 5 A minimum − uncertainty **≥4.75 V** |
| Source contract | Physical cutoff **≤10 µs**; whole-event positive charge + uncertainty **≤100 µC** |
| Stress/recovery | Local temperatures, pulse/SOA limits, control-rail survival and checked re-arm |
| After | Raw traces, settings, hardware revision, verdict and limitations; **Pi only after all gates** |

> [!info]- Sources and reproducibility
> [Fact-check register](FACTCHECK_LOG.md#sources): TEST, HOOKS, VERIFY and BASIS. Latest [Gate 4a-FIX test plan, `2b99ac7`](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/2b99ac7bd60d352a4b418cd75e0fc8f66e345b4d/docs/evidence/r2/gate4a/TEST_PLAN.md), especially T01/T10/T12/T13. [BATCH_F](../illustrations/BATCH_F.md) F7.1–F7.3. Charts: `python3 -B docs/lessons/figures/src/lesson_charts.py 07`. No tests described here have been performed by this lesson rewrite.

Previous: [[06 PCB concepts]] · Next: [[08 V1A inside the robot]] · Terms: [[99-Glossary]]
