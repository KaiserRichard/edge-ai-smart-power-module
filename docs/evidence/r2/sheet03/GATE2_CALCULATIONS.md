# Gate 2c — independent bounds override

**BLOCKED — PRELIMINARY — NOT FOR FABRICATION.**

This section supersedes positive-margin interpretations of the historical Gate2 screen below.
Run `python3 -B scripts/calculate_sheet03_gate2c.py --write`. Only exported XML is read.
Historical JSON members are retained; actual worst-case margins are `null` / **OPEN**.
Sources, tolerance conditions, timelines and proposed changes: [review closure](GATE2C_REVIEW_CLOSURE.md).

Finite entries below are **CALCULATED conditional screens**. Divider/resistor corners are extrema within explicitly **ASSUMED** tolerance stacks; fault curves are sensitivities, not optimized extrema.
They do not establish the application worst case. Efficiency/loss screens are **CALCULATED (typical only)**.

| Margin | Historical claimed CALCULATED screen | Independent conditional calculation | Application worst case |
|---|---:|---:|---|
| Fault | 18.388 mV | 18.645 mV, historical source/L/timing box | OPEN |
| Harness | 11.431 mV | 11.433 mV, reduced path | OPEN |
| False trip | 21.954 mV | 21.954 mV, assumed response | OPEN |

**BLOCKING conditional counterexamples:** retained harness -89.501 mV; assumed longer load release -2.979 mV. Also, the inherited ASSUMED resistor-terminal temperature exceeds the DATASHEET maximum by CALCULATED 30 K. These are premise conflicts, not measured device behavior.

| Conditional shorted-high-side sensitivity — ASSUMED inputs | CALCULATED Pi peak | CALCULATED margin | CALCULATED L peak |
|---|---:|---:|---:|
| 30 V, 0.3 µs action, 0.5 µH floor | 5.481355 V | 18.645 mV | 204.409 A |
| 30 V, 0.4 µs action, 0.5 µH floor | 5.502486 V | -2.486 mV | 204.311 A |
| 24 V, 0.3 µs action, 0.5 µH floor | 5.468711 V | 31.289 mV | 174.731 A |
| 24 V, 0.4 µs action, 0.5 µH floor | 5.485506 V | 14.494 mV | 174.633 A |
| 24 V, 0.3 µs action, 0.1 µH floor | 6.268052 V | -768.052 mV | 502.943 A |
| 24 V, 0.4 µs action, 0.1 µH floor | 6.271942 V | -771.942 mV | 502.457 A |

Negative cases are **BLOCKING** evidence against claiming the assumed floor/timing as a guaranteed bound.

| CALCULATED input/supply screen | Result |
|---|---|
| Input OVP, resistor initial tolerance only | 27.630380 V nominal; 26.973873–28.289211 V |
| Falling UVLO | 7.907137 V nominal; 7.618701–8.168235 V |
| eFuse ILIM | 4.477612 A formula nominal; 4.180819–4.819820 A |
| DET_5V regulated | 4.880625–5.117398 V |
| DRV_7V5 regulated / PG floor screen | 7.440269–7.807424 V / 6.175423 V |
| Supervisor release, nominal external capacitor | 1.257643 s typical equation; maximum application delay OPEN |

| CALCULATED energy/pulse screen, ASSUMED ceiling and isolation | Result |
|---|---:|
| Initial nominal inductor energy | 122.400 µJ |
| Input capacitors at nominal rail, conditional upper C | 17.567 mJ |
| Raw bulk energy at assumed ceiling | 81.893 mJ |
| Downstream tail I²t ceiling | 0.102369 A²s |
| Raw-bulk-only I²t ceiling, if still connected | 2.519391 A²s |
| Each ballast rectangle | 23.265651 mJ |

**24 V rail:** nominal operation is plausible; exact converter tolerance/trim/OVP/isolation and fault containment remain OPEN pending its model. No fallback-module shortlist is justified yet.

<!-- GATE2C GENERATED END -->

## Historical Gate 2 screen — preserved, superseded
# Gate 2 — captured-value calculation

**CALCULATED — PRELIMINARY — R2 BLOCKED — NOT FOR FABRICATION.**

Run `python3 -B scripts/calculate_sheet03_gate1b.py --gate 2 --write`.
The calculator reads the [KiCad XML export](V1A_gate2.net.xml), records its hash
and the values actually used, and appends `gate_2` to
[CALCULATIONS.json](CALCULATIONS.json). Historical gate members are retained.

| Captured values | CALCULATED result | Evidence / remaining assumption |
| --- | --- | --- |
| R301=11.3kΩ, R302=10.0kΩ | Trip nominal5.325V; min5.293568V, max5.356563V | REF5025/TLV3201 DATASHEET limits plus the existing ASSUMED resistor drift, aging/noise and hysteresis allocations; 32 corners |
| R202=100kΩ, R203=24.4kΩ | Raw buck5.098361V nominal;5.038269–5.158632V screen | Existing1% reference,0.1% divider and10nA feedback-current screen retained;10nA is typical, not a guaranteed maximum |
| R103=348kΩ, R104=15.8kΩ | Input OVP27.630380V nominal;26.973873–28.289211V | TPS2663±2%, divider±0.1%,±150nA screen; OVP is not a source clamp |
| C330–C337,8×470µF | 3.76mF nominal;2.4064mF minimum screen | Sequential initial/endurance factors0.8×0.8; temperature, bias, inrush and control-loop stability remain OPEN |
| R308–R311,4×33mΩ in two series branches in parallel | 33mΩ nominal equivalent | DATASHEET1% and50ppm/K, ASSUMED100K excursion; Gate1d full-pulse part selection retained |
| R312=31.9kΩ, R313=10kΩ | DET_5V4.998670V nominal;4.880625–5.117398V screen | TPS7A16 overall±2%, IFB±0.1µA; ASSUMED divider±0.2% including drift |
| R314=53.9kΩ, R315=10kΩ | DRV_7V5 **7.623270V nominal;7.440269–7.807424V** | Same regulated-supply screen; +90.269mV above the assumed7.35V minimum. The net name is retained. Dropout, heating and falling-rail validity remain OPEN |

The raw-bulk load-release screen leaves **21.954mV** false-trip margin after
the existing10mV allocation. The selected fault screen yields
**5.481612V at the Pi,18.388mV below5.5V**. The reduced-resistance harness
screen yields **4.761431V at 5 A,11.431mV above4.75V**; it still misses the
separate 100 mV dynamic reserve by88.569mV. Both narrow margins remain **OPEN**.

The fault margin fell from 39.328 mV because Gate1d changed the assumed crowbar
action time from 0.20 µs to 0.30 µs to accommodate the larger selected MOSFET's
gate-charge screen. That extra 0.10 µs raises the calculated peak by 20.940 mV.
The threshold divider did not change. No measured action time or peak is claimed.

The reused partial detector/latch/driver/charge estimate is207.361ns using
the captured driver's regulated minimum. It is **not** a bound for the full
captured chain: the extra logic gates, sense filtering, nonlinear gate charge,
supply collapse and current commutation must still be qualified. The0.30µs
crowbar and2µs series-off times remain ASSUMED inputs. The selected parts
do not make those times guaranteed. Source/L/C, downstream stores, thermal
interfaces, pulse repetition, startup/reset and series-FET SOA remain OPEN.

Pin and package sources are in the [review](GATE2_PIN_REVIEW.md) and
[source register](../../../../third_party/sheet03_source_register.json).
