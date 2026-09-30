# V1A upstream 24 V converter interface study

Date: 2026-09-30. Owner: auxiliary converter interface study. Baseline: `0677fea0a32fc87b740949d589abe1588e55934c` (`origin/feat/sheet03-gate2c`).

**STUDY ONLY — ENGINEERING REVIEW REQUIRED. NOT FOR FABRICATION.** No purchase, circuit change, or hardware validation is authorized by this document.

**VERDICT: PENDING MARKET EVIDENCE.** This checkpoint completes the proposed interface specification; candidate evidence and final selection follow in subsequent commits.

## Authority and evidence labels

**REQUIREMENT** means the user's frozen interface constraint. **ASSUMED** means a proposed procurement allocation, not an approved robot specification. **CALCULATED** means arithmetic using the stated inputs. **EVIDENCE / DATASHEET** means a documented manufacturer claim within its stated conditions. **OPEN** means an applicable guarantee, environmental requirement, or owner decision is missing. A typical specification is not a guaranteed maximum.

Frozen architecture: 13S Li-ion → PDB → purchased isolated auxiliary converter → V1A → Raspberry Pi 5. **REQUIREMENT:** 54.6 V or regeneration peaks must never reach V1A after converter failure. **ASSUMED:** discharged battery about 39 V (13 × 3.0 V), V1A efficiency 90%. **CALCULATED:** 5.1 V × 5 A / 0.90 = 28.33 W, rounded upward from the user's approximately 28 W for sizing. Other auxiliary loads and their transients remain **OPEN**.

The [frozen decision log](../../context/06_DECISION_LOG.md) and [Gate 2c closure](../r2/sheet03/GATE2C_REVIEW_CLOSURE.md#can-v1a-use-the-robots-proposed-24-v-rail) are the local authority. This user instruction now authorizes the upstream shortlist that the earlier conditional Gate 2c request did not authorize. It does not alter the frozen circuit or release R2/R3.

Gate 2c finds 24 V operation nominally plausible, with higher auxiliary LDO heating and unresolved board thermals. Its eFuse OVP calculation is 26.973873–28.289211 V with initial resistor tolerance; resistor drift/MPNs remain **OPEN**. Those are cutoff thresholds, not clamp voltages. [Input review](../r2/INPUT_PROTECTION.md) gives rising UVLO 8.224–8.691 V, falling 7.619–8.168 V, and an approximately 37.3–63.3 ms eFuse-controlled ramp at 24 V. The latest Gate 2c current-limit screen is 4.181–4.820 A; it supersedes the older approximate current-limit calculation.

## Buyer handoff — proposed one-page interface specification

All allocations marked **ASSUMED** require engineering acceptance. Request guaranteed bounds, test conditions, and single-fault evidence from the supplier; an unchecked box prevents purchase approval.

| ID / item | Requirement to place on the enquiry / purchase specification | Classification / consequence |
|---|---|---|
| S1 — Input | Guaranteed continuous operation over at least 36–60 VDC, covering approximately 39–54.6 V plus allocation. Prefer an 18–75 V or wider industrial input range. | 39 V empty **ASSUMED**; 54.6 V full **REQUIREMENT**; 36–60 V allocation **ASSUMED**. Actual PDB dropout/minimum **OPEN**. |
| S2 — Input transients | Prefer ≥100 V guaranteed survival at the module terminals, including polarity, pulse duration, source impedance, energy, and repetition. Provisionally enquire for 100 V / 1 s; an input range including 100 V continuously is stronger evidence. A 75 V maximum is acceptable only behind independently qualified PDB clamping below that rating. | **ASSUMED** screening target; actual regen/hot-plug envelope **OPEN**. 100 V gives 45.4 V headroom over full charge; this is margin, not a measured bus bound. Sustained regeneration needs an energy sink, not merely a TVS. |
| S3 — Output / trim | Buy a **24 V class** output adjustable down to 23.5 V, then lock the adjustment. Proposed complete DC error ≤±1% of 23.5 V over line/load/temperature/aging/trim. Normal peaks at the V1A connector must remain ≤24.0 V; other 24 V loads must accept the lower setting. | 9–24 V normal **REQUIREMENT**. 23.5 V/±1% **ASSUMED**; DC bounds 23.265–23.735 V **CALCULATED**. A fixed 24 V output with positive tolerance does not prove the frozen limit. Acceptance by other loads **OPEN**. |
| S4 — Output OVP / let-through | Independent shutdown or disconnection: proposed threshold 25.0 V ±2% **including all threshold errors**, hence 24.5–25.5 V. Latch off until deliberate reset. Guarantee the **complete fault peak ≤26.0 V** at V1A, including delay, ripple, stored energy, wiring overshoot and all credible switch/control faults. | Threshold/peak allocations **ASSUMED**. Margin to initial-only V1A minimum: 26.97−26.0 = 0.97 V **CALCULATED**. Full eFuse drift margin **OPEN**. A trip value alone fails this item; specify an independent energy-rated barrier if internal OVP is insufficient. |
| S5 — Isolation / failed switch | Transformer-isolated input/output required; proposed ≥1.5 kVDC dielectric test, with manufacturer-declared insulation type and working voltage covering the qualified primary bus. No primary-to-secondary DC bypass in a primary switch short; require single-fault output peak/energy and input-fuse coordination evidence. | Isolation **REQUIREMENT for proposed purchase architecture**; 1.5 kVDC screening **ASSUMED**, not proof of fault containment. Barrier failure, transient coupling, external ports/grounds and insulation maintenance **OPEN**. |
| S6 — Continuous power | Use the scenario table below; guarantee the selected power at minimum input and actual mounting/ambient, preferably with ≥25% headroom. At reduced trim check output **current**, not just nameplate watts. Give guaranteed OCP range, peak duration, output capacitance and fault energy. | 90% V1A efficiency and 25% reserve **ASSUMED**; other loads, peak power and source/fault impedance **OPEN**. Do not route other loads through V1A's eFuse. |
| S7 — Startup / restart | Monotonic startup, no overshoot beyond S3 in healthy startup, no repeated UVLO crossings after enable; proposed module rise 10–100 ms and settled output within 1 s. Start into the complete V1A plus shared-load network without current-limit/hiccup cycling. Persistent OVP/short must enter maintained shutdown at the **system interface**. | Timing targets **ASSUMED**. Respect eFuse rising UVLO maximum 8.691 V and 9 V normal floor. Full input/output capacitance, startup current, fault reset and hold-up **OPEN**. A converter with automatic short-circuit recovery needs a separately qualified inhibit policy. |
| S8 — Ripple / healthy transients | Proposed ripple/noise ≤200 mV p-p, with positive deviation from the DC value ≤100 mV, measured at V1A with a short probe loop and 20 MHz bandwidth. Allocate an additional ≤150 mV positive healthy startup/load-step deviation. Require the complete peak ≤24.0 V; record unfiltered switching spikes separately. No healthy operation below 9 V after startup. | Limits **ASSUMED**. High screen 23.5×1.01+0.100+0.150 = 23.985 V **CALCULATED**. A p-p number alone does not guarantee a symmetric waveform. Shared-load step spectrum and harness drop **OPEN**. |
| S9 — Temperature | Proposed procurement environment −20…+60°C local ambient; rated scenario power after manufacturer derating, in the actual enclosure. Require thermal path, baseplate/case limit, airflow assumptions and overtemperature shutdown behavior. | Environment **ASSUMED**; actual robot ambient/enclosure, hot-spot limits and thermal validation **OPEN**. Nominal efficiency is insufficient. |
| S10 — Mounting / integration | Prefer enclosed chassis mount with protected screw terminals, positive mechanical retention, strain relief and a qualified baseplate thermal path. Separate primary and auxiliary wiring; identify PE/chassis/return bonding and isolated control interfaces. Input fuse must have qualified DC voltage/interrupt rating; branch fusing and connectors must suit scenario current and fault energy. | Form-factor preference **ASSUMED**; dimensions, vibration, cooling, grounding, fuse/connector MPNs and cross-domain ports **OPEN**. A bare brick additionally needs a carrier, heatsink and terminal enclosure. |

### Power scenarios

Use 28.33 W for V1A rather than rounding downward. Reserve is a procurement allocation, not a prediction of unknown loads. Primary budget uses a separate **ASSUMED** upstream efficiency of 90%, not a candidate's typical headline.

| Other 24 V loads | Total continuous demand, CALCULATED | Current at 24 V / 23.5 V, CALCULATED | Minimum usable capacity with 25% reserve, CALCULATED | Candidate size / primary current at 39 V, ASSUMED / CALCULATED |
|---|---:|---:|---:|---|
| 0 W, scenario | 28.33 W | 1.181 / 1.206 A | 35.42 W; 1.507 A at 23.5 V | ≥40 W usable; 0.807 A primary |
| 50 W, OPEN scenario | 78.33 W | 3.264 / 3.333 A | 97.92 W; 4.167 A at 23.5 V | ≥100 W **usable at temperature/trim**; 2.232 A primary |
| 100 W, OPEN scenario | 128.33 W | 5.347 / 5.461 A | 160.42 W; 6.826 A at 23.5 V | ≥180–200 W class; 3.656 A primary |

For example, a 24 V/4.2 A module provides only 98.7 W at 23.5 V before thermal derating; a 24 V/6.3 A module provides 148.05 W. Neither can be judged by the rounded “100 W” or “150 W” label alone. Larger modules also increase available short-circuit current and stored energy; the V1A branch needs its own source/fault budget.

## Study checkpoint

**STATUS: CONDITIONAL PASS — proposed interface specification complete; procurement BLOCKED pending market evidence and owner decisions.** Evidence: frozen baseline, Gate 2c and input-protection reviews. Decision: keep the 24 V normal ceiling and require independent upstream fault containment. Open risks: actual bus transients, full eFuse threshold drift, shared loads, environment and fault dynamics. Next sub-step: failure analysis and plain-language owner explanation, then candidate screening. This is a scoped study checkpoint, not closure of an R0–R5 project gate; the manager report is not edited because this task permits new files only in this directory.
