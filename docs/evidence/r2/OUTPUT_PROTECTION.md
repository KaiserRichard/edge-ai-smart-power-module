# Independent output protection — R2 blocker

Date: 2026-09-12. **BLOCKED. No disconnect or bypass is fitted.**

SOURCE: [TI LM7480-Q1 SNOSD95C](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf),
electrical characteristics and common-drain application. FUNCTION REQUIRED:
independent OV detection and load isolation after a buck power-stage failure,
plus controlled reverse-feed behavior. MODIFICATION: isolate the functional
boundary rather than copy an unjustified reference circuit. RATIONALE: the
load's fault-voltage/time limit and capacitance range were not supplied; continued
work was authorized, but those missing electrical requirements were not resolved.

## Candidate topology and concrete limitation

Review candidate **LM74800QDRRRQ1** with two common-drain N-channel MOSFETs:
first MOSFET source at VOUT_5V1, drain at the common midpoint; second drain at
the midpoint, source at VOUT_PROTECTED. Opposed body diodes prevent an off-state
direct path. DGATE owns ideal-diode/reverse-current control; HGATE owns forward
disconnect. The OV divider would sense upstream raw voltage so that detection
does not disappear when the output is disconnected. Neither FET nor divider is
selected or placed in the schematic.

The integrated OV comparator rises at **1.195-1.267 V** (1.231 V nominal).
Ignoring divider error and delay, any setting that avoids a false trip at 5.162 V
can trip as high as **5.473 V** at the other comparator extreme. A hypothetical
5.25 V fault ceiling therefore cannot be met by this detector. **5.25 V is not
adopted as a user requirement**; this counterexample explains why the missing
fault ceiling matters. Light-load auto-mode excursions and divider error further
consume the window. A precision detector driving a qualified disconnect may be
necessary, but is not invented or selected here.

TI specifies up to **5.4 us OV deglitch** for LM74800, followed by gate discharge
and the power path's dynamic response. An illustrative 24 V high-side short,
6.8 uH and 100 uF with no initial excess current gives di/dt≈2.78 A/us:
over 5.4 us, current could increase 15 A and capacitor voltage about **0.405 V**
using deltaV≈(Vi-Vo)t²/(2LC). This simplified estimate ignores saturation,
source limits, ESR, initial inductor current and FET switching. It is evidence
that delay cannot be ignored, not a safe upper bound. Upstream input OVP will
not detect a buck failure while input remains a valid 24 V.

## Required behavior versus captured behavior

| State | Required final behavior / candidate assessment | Current schematic |
| --- | --- | --- |
| Normal input/output | Conduct 5 A with known loss/drop | Open at sheet 03; VIN cannot power load |
| Buck output rises toward input | Independent detector opens forward switch before permitted load exposure is exceeded | No detector/FET fitted; no claim of protection |
| Fault persists | Stay disconnected without repeated damaging attempts | No recovery circuit fitted |
| Input removed, LOAD externally alive | Block LOAD → buck/input; permit only quantified leakage/local demand | Open stub blocks the upstream path; external LOAD feeds shunt/local telemetry |
| Input returns while LOAD is externally powered | Qualified prebias/OR-ing handover with bounded circulating current and no forced discharge | Upstream remains disconnected |

Candidate trip/recovery: LM74800 pulls HGATE down on OV and automatically
recovers when its falling OV threshold is met; it is not a latched precision
OVP. With a persistent high raw rail it remains off. For a marginal/intermittent
fault, retry behavior and hysteresis must be assessed; a required latch would
change the implementation. No output recovery policy is silently frozen.

Conduction screening only: two CSD19537Q3 devices at 16.6 mOhm each (their 6 V
gate-drive resistance bound at 25 C) would lose **0.83 W / 0.166 V at 5 A**, plus
0.05 W/0.010 V in the shunt. Hot resistance is higher. This demonstrates a cost
to the 2.833 W whole-module loss budget; these FETs are **not selected for output**.
Final MOSFET VDS/VGS, gate drive, SOA during interruption/startup, leakage and
body-diode transient stress need a chosen detector and fault envelope.

Reverse behavior is not just a body-diode drawing: verify controller supply from
the common node, sensing connections, off-state leakage, gate thresholds during
collapse, and source-return transient current. The final block must prevent the
buck's body diode/discharge behavior or BIAS/feedback wiring from draining V1B.
V1A does not define V1B voltage, charging or hold-up time. No direct V1B connector
or storage circuit was added.

## Decisions required to complete R2

1. Load terminal normal min/max, fault maximum versus duration, permissible
   let-through energy and downstream capacitance/ESR range.
2. Buck-failure/source impedance and fault-current envelope for detector delay,
   disconnect SOA and energy calculations.
3. Output trip/recovery policy and allowed externally supplied output range,
   leakage/local demand and prebiased source-return behavior.
4. Select and independently review the simplest detector + disconnect that meets
   those limits, including exact parts/footprints and fault tests.

After capture, rerun ERC, netlist/visual checks and manager review. The current
netlist intentionally retains the undriven U402 input diagnostic rather than
using a PWR_FLAG to conceal the missing output power source. **R3 remains BLOCKED.**
