# Output-protection requirements and timing preparation

2026-09-14. **NO ARCHITECTURE SELECTED. Sheet03 remains electrically open.**

Requirements must describe what the load must survive separately from what a detector/controller can do. A candidate's threshold or delay is not a load acceptance criterion. The existing [forensic candidate comparison](R2_R3_BLOCKER_REVIEW.md) remains historical context; this worksheet adds explicit owners, sources and timing limits.

## Requirements matrix

| Category | Established basis and source | OPEN requirement / evidence needed |
| --- | --- | --- |
| LOAD SURVIVAL REQUIREMENTS | V1A specifies nominal5.1V/5A load direction; Raspberry Pi primary supply guidance supports that supply class | Exact Pi/load model and direct-power interface; normal minimum/maximum at load; absolute voltage-versus-time envelope; permitted fault charge/energy; negative voltage and local telemetry survival limits. 5.25V is an earlier ASSUMED screen, not a sourced Pi damage rating |
| SOURCE / BUCK FAILURE ENVELOPE | V1A normal9..24V input; LM61460 VIN36V operating/42V abs max, L201 nominal6.8uH and raw bank6x22uF | High-side short is a HYPOTHESIS, not guaranteed buck failure behavior; fault source maximum/slope/current, eFuse response, L saturation, biased C, ESR/ESL, repetition and raw-side clamp requirement |
| DETECTION | REQUIREMENT: independent hardware OV detection, not software/INA228/buck-control dependent | Worst-low threshold above full normal high/ripple; worst-high below accepted load fault envelope; comparator/reference/divider/leakage errors; noise immunity, overdrive-dependent delay and supply availability |
| DISCONNECT | REQUIREMENT: independent forward interruption between VOUT_5V1 and VOUT_PROTECTED | Actual FET/controller, failure voltage rating, maximum gate discharge and commutation time, default-off state and hot conduction budget |
| REVERSE CURRENT | Preserved system can have externally energized LOAD; local telemetry is then powered backward through R401 | External source voltage, permitted reverse charge/current/leakage, input-off/return handover, reverse trip behavior. A breaker is not ideal-diode zero-backfeed protection |
| STARTUP | Existing input/eFuse/buck soft-start sequence known; downstream load C is not | Maximum load C/inrush, slew/current limiting, hot-start frequency, detector-valid-before-enable, interaction with precharged load and local3V3 |
| RECOVERY | Existing input MODE latch does not automatically latch output OV | Auto-retry vs deliberate reset, retry count/cooldown, persistent-fault behavior, local telemetry off/on sequencing. Latched OV is a PROPOSAL only |
| THERMAL / SOA | R401 nominal50mW at5A; example output-switch allocation10mOhm is ASSUMED | Ambient/enclosure/airflow, hot RDS(on), linear startup/interruption SOA, gate clamp and pulse repetition; no Q101 substitution approved for output |
| LET-THROUGH ENERGY | CALCULATION framework: integrate load V(t)I(t), excess charge and energy above initial state; include time to threshold and isolation | Approved voltage/time/charge/energy envelope, actual source/L/C and disconnect trajectories; allocation of inductor energy between load/raw capacitance/clamps; off-switch VDS and avalanche/SOA |

Source boundaries: [Raspberry Pi official documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply) and archived primary source/review establish supply guidance only. [V1A requirements](../../../00_REQUIREMENTS.md), user-authorized scope and current netlist establish preserved architecture and output class. [TI LM61460 SNVSBD5D](https://www.ti.com/lit/ds/symlink/lm61460.pdf) establishes regulator behavior within ratings, not a guaranteed destructive-failure waveform. Unsupported acceptance values remain OPEN.

## Candidate timing ledger

Define `t_total = t_detect + t_propagation + t_turnoff` from the **applicable detection threshold crossing** to effective current isolation. Add `t_to_threshold` from fault onset when computing load exposure. Published parameters sometimes combine internal detection/propagation; do not add the same interval twice. `t_turnoff` must include actual gate discharge/Miller effects and current commutation, not merely a logic output edge.

| Candidate direction | Primary timing evidence | Conditional estimate / bound and missing terms |
| --- | --- | --- |
| A: LM74800QDRRRQ1 + common-drain N-FETs | SNOSD95C §§7.5/7.6: OV to HGATE turnoff deglitch5.4us max under stated conditions; HGATE OV sink168mA min,260mA typ | Internal combined term <=5.4us only for the cited test basis. External term `Qoff_max/Isink_min + gate-network delay + commutation` remains OPEN. ASSUMED Qoff20nC at168mA gives0.119us, hence5.519us **screen before added gate/commutation effects**. This is not a full bound and cannot use typical Qg as Qoff_max |
| B: LTC4368-2 + back-to-back N-FETs and its separate breaker shunt | RevC p4: UV/OV propagation2us max at VIN12V/50mV overdrive; fast gate-off6us max with CGATE2.2nF; Fig6 identifies fault/gate timing | Reference timing budget up to2+6=8us if treated as successive intervals; confirm exact endpoints against Fig6 for a selected implementation rather than asserting a universal8us bound. Real5.1V supply, small detector overdrive, actual FET gate charge/gate RC and commutation remain OPEN. No extra2us should be counted if using a characterized end-to-end fault-to-gate interval |
| C: precision detector/reference + rated reverse-blocking disconnect | Architecture direction only; no exact detector/supply/driver combination is qualified | `tdet_max(overdrive,T) + tprop_max + Qoff_max/Isink_min + tcommutation`. All terms OPEN. A synthetic sub-microsecond target would be an ASSUMPTION; without load acceptance and concrete parts there is no defensible numeric upper bound |
| Integrated TPS259470x/474x screen | TI SLVSFC9C: OV response1.2us typical; internal28.3mOhm nominal; operating input ends23V, absolute28V | Typical response is not a bound. Maximum response/turnoff, hot drop and unbounded buck-fault survival missing; current upstream OV corner28.289V already exceeds28V before overshoot. **Not qualified for present failure envelope** |

Primary documents: [LM7480-Q1 SNOSD95C](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf), [ADI LTC4368 RevC](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4368.pdf), [TPS25947 SLVSFC9C](https://www.ti.com/lit/ds/symlink/tps25947.pdf). See [register](qualification_source_register.json) for available local sources and retrieval limitations. The HGATE example must not borrow DGATE's larger reverse-switch sink rating.

**Threshold feasibility screen:** avoiding false trip below the old static-high5.15863V requires an optimistic worst-high threshold no smaller than `Vnormal_high * detector_max/detector_min`: LM74800(1.195..1.267V) ->5.46945V; LTC4368(0.4925..0.5075V) ->5.31575V; TPS25947(1.183..1.223V) ->5.33306V. Divider/leakage/ripple errors add uncertainty. These fail the old ASSUMED5.25V screen even before delay; they do not establish failure of an unspecified real load requirement. Therefore no final threshold divider is calculated or wired.

## Fault-energy preparation

Preserve [existing screening inputs/results](protection_screening.json): ASSUMED24V source,5.1V initial rail, constant6.8uH,5A initial current,85.272uF raw capacitance and constant load. `di/dt=(24-5.1)/6.8uH=2.779A/us`; at5.4us, current increases15.009A and the early-time estimate `deltaV=(Vin-Vo)*t^2/(2LC)` is0.475V. Initial magnetic energy85uJ grows to approximately1.361mJ in this simplified model. This is an illustrative local approximation, not a safe fault bound: the assumed constant L/C/current/voltage fails as the core saturates, capacitance changes and protection/source react.

Actual exposure includes time to the worst-high trip plus `t_total`. After opening, raw capacitors remain upstream of the switch. Inductor energy does not all flow into the Pi; some charges the raw bank or is absorbed in clamps/losses. Model raw-rail overshoot, disconnect VDS/VGS, gate re-turn-on and remaining load energy separately. Calculate `integral(Vload*Iload dt)`, excess charge, peak Vload and duration above each accepted voltage level. No allowed energy value can be inferred from a power-supply watt rating.

## Required operating-state review and later tests

| State | Required behavior to decide / verify |
| --- | --- |
| Input on, unpowered load | Valid detector before path enable; acceptable inrush and SOA |
| Input on, externally precharged load | No uncontrolled reverse current or source contention |
| Input removed, external load supply on | Defined leakage/reverse trip; local telemetry may be powered through R401 with negative reported branch current |
| Output OV / buck fault | Independent detection and timely disconnect, raw-side survival, no parasitic re-enable |
| After disconnect, no external source | 3V3_LOCAL decays; detector must retain authority without depending on the rail it disconnected |
| Persistent fault/reset/input return | Approved recovery policy, bounded retry energy and no host-rail back-powering |

An upstream disconnect cannot protect telemetry from an arbitrary OV source directly attached to LOAD_5V1. That external envelope must be specified. Host/local rails and shunt placement remain unchanged. Later R5 dummy-load tests must capture raw/protected/load voltage, current, gate voltage and temperature under the approved states/limits; failure includes overvoltage, reverse-current excess, SOA exceedance, chatter, back-power or unavailable fault authority. No output circuit was captured, no bypass/PWR_FLAG added, and manager approval remains necessary before Sheet03 implementation.
