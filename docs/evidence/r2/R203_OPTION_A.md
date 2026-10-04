# R203 option A — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**DECISION:** owner chose A: R203 = **24.6k / TNPW060324K6BEEA**, Vishay 0603, 0.1%, 25 ppm/K; B045 **LOCKED**, selection OPEN **0**. R202 remains 100k. Only R203 Value/MPN/Source properties changed in Sheet02; footprint `Resistor_SMD:R_0603_1608Metric`, nets and PCB are unchanged. The Source property supersedes the old sheet-wide setpoint note, which the narrow edit scope leaves intact.

**EVIDENCE:** [BUCK_DESIGN](BUCK_DESIGN.md) and [original buck block](buck_block.json) are historical. The later [Gate4A freeze, 898759e](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FREEZE_TABLE.md), S02-04/S03-02/S04-05, establishes the current path and loaded OV detector. [Source register](../../../third_party/bom_order/R203A_SOURCES.json) records TI SNVSBD5D, Vishay 28758 and dated supplier snapshots. [Reproducible calculations](r203_option_a/CALCULATIONS.json): `python3 docs/evidence/r2/r203_option_a/calculate.py`.

**CALCULATED setpoint:** `1 × (1 + 100/24.6) = 5.065040650 V`, down **33.320 mV** from 5.098360656 V. With VFB ±1% and independent 0.1% resistors, `Vmin=.99(1+100×.999/(24.6×1.001))`, with opposite signs for Vmax: **5.006350–5.123911 V**. Including the inherited **ASSUMED ±10 nA** FB-current screen gives **5.005351–5.124912 V**. At the path study's **ASSUMED 85°C** divider temperature, independent ±(0.1% + 25 ppm/K × 60 K) gives **4.993321–5.137273 V** including FB current. TI's ±1% is FPWM-conditioned; 10 nA is typical, not a guaranteed maximum. Full auto-mode regulation remains **OPEN**.

**CALCULATED 5 A path:** use frozen **D / BSC034 pair 13.6 mΩ / J502 solution A**, not the earlier E or 6 mΩ-pair proposals. Total SEND+RETURN **41.855546 mΩ**, drop **209.278 mV**, loss **1.046389 W**; itemized frozen allocations are retained in the JSON. `VPi=4.993320972−5×.041855546243−Vnegative`; floor **4.75 V**.

| CALCULATED hot case | Pi minimum V | Margin mV | Result |
|---|---:|---:|---|
| Static | 4.784043 | +34.043 | PASS within assumptions |
| Documented 20 mV trough | **4.764043** | **+14.043** | **PASS within assumptions** |
| 100 mV total excursion sensitivity | 4.684043 | −65.957 | FAIL |
| 6 V gate sensitivity, 20 mV trough | 4.730043 | −19.957 | FAIL |

The former 20 mV-case margin was +46.866 mV; loss of margin is **32.822 mV**. Total negative-excursion allowance is now **34.043 mV**, including ripple. The 100 mV sensitivity already failed before; it is not a newly imposed requirement. Contact, hot FET and copper maxima remain qualification targets.

**CALCULATED OV:** unchanged current loaded detector nominal **5.266700 V**, conditional trip **5.219922–5.314622 V**. Minimum trip exceeds the new maximum by **95.010 mV** at initial tolerance, **82.648 mV** hot, or **62.648 mV** with +20 mV ripple: **PASS static separation**. The strict **5.5 V** fault ceiling leaves **185.378 mV** above maximum trip, **143.126 mV** after conditional comparator overdrive (5.356874 V), or **123.126 mV** after a further assumed 20 mV local allowance. Margin to the frozen 5.38 V overdrive allocation is **23.126 mV**. These exclude commutation delay/energy/ESL. No fault-containment PASS follows: the historical receiving-bank 5.713245 V sensitivity fails by **213.245 mV**; reusing the earlier 107.620 mV release increment plus 10 mV nuisance reserve also fails by **34.972 mV**.

**OBSERVATION / OPEN RISK:** ERC **0 errors/0 warnings → 0/0**; contract checks pass, with the pre-existing CLI PCB-scope rejection separately recorded. [Execution/checks](r203_option_a/EXECUTION.md) list tests, changes and Git failure. DigiKey indexed stock **1,920**, Mouser **5,101**, versus five needed; prices/stock require reconfirmation. Nothing bought. Git cannot create `index.lock`; all edits remain uncommitted. **R2 electrical release BLOCKED**; no gate advanced or hardware validated.
