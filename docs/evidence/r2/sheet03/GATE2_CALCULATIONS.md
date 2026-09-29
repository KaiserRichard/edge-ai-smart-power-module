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
screen yields **4.761431V at5A,11.431mV above4.75V**; it still misses the
separate100mV dynamic reserve by88.569mV. Both narrow margins remain **OPEN**.

The fault margin fell from39.328mV because Gate1d changed the assumed crowbar
action time from0.20µs to0.30µs to accommodate the larger selected MOSFET's
gate-charge screen. That extra0.10µs raises the calculated peak by20.940mV.
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
