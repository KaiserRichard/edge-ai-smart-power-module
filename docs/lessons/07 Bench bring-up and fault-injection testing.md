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

The planned normal matrix includes **9, 24 and 26 V**, and **0, 2.5 and 5 A** load cases with controlled temperature states. **27 V is an additional OVP/fault-window test**, outside normal operation. A fitted eFuse may already be off there; that run cannot prove interruption of an energized source. Do not bypass its protection to relabel the run.

Change connections only with supplies off and stored charge discharged. The sequence begins only after schematic, layout and fabrication-readiness review have authorized the actual hardware and fixture.

## 4. Where the probes go

![[f7-03-probe-placement.png|900]]
*BATCH_F F7.3. Measure far-end positive against its own return. The picture omits additional source/dump-current channels required by the full plan.*

Read from left to right:

1. **Raw voltage:** before the output series pair, to observe the failed buck and raw dump.
2. **Protected voltage:** after the pair, to observe the local clamp.
3. **Far-end voltage:** across the dummy header's own positive and return contacts, to include harness effects.
4. **L201 current:** through source cutoff and subsequent decay, not just at the first peak.
5. **Additional boundary currents:** incoming source current establishes replenishment charge; dump/crowbar currents establish energy-disposal stress.

Instrument grounds must not create a parallel return that makes the harness look better than it is. Use the reviewed differential/isolation arrangement while keeping equipment protective earth intact. Start recording **before** the fault with pre-trigger history and retain the entire decay/recovery tail.

The high-side-short injector must preserve the actual **input → failed-switch path → L201 → output** fault mechanism. Driving an external supply directly into the output tests a different event. The reviewed fixture must also prevent an unintended short through the native low-side switch; its construction remains blocked. Never improvise a short across an operating converter.

## 5. Worked example: a displayed peak needs an uncertainty margin

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

![[v2-07-source-charge-tail.png|850]]

The teaching plot assumes **10 A for 10 µs**, then only **10 mA for the remaining 1990 µs**. The first interval already delivers 100 µC. The small tail adds

$$
Q_{tail}=0.010\ \mathrm{A}\times1990\ \mathrm{\mu s}=19.9\ \mathrm{\mu C}
$$

The total is **119.9 µC before uncertainty**. Integrating only the first 10 µs would miss the violation. Integrate positive replenishment over the whole event; negative current cannot cancel the positive-charge limit. Account for current-probe offset/noise before positive clipping.

## 7. The source is off; stored energy is still present

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
