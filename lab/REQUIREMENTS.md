# Requirements (Step 0 table)

Current working requirement table for V1A. **Not frozen.** It merges the confirmed scope in [docs/00_REQUIREMENTS.md](../docs/00_REQUIREMENTS.md) with the proposed revision 2 envelope in draft [PR #1](https://github.com/KaiserRichard/edge-ai-smart-power-module/pull/1) (`REQUIREMENT_ENVELOPE_PROPOSED.md`), which answers the user's 2026-09-26 review of revision 1. Seeded 2026-09-29.

**Labels**
- **CONFIRMED**: the user explicitly required it, or it is a directly established source or repository fact.
- **ASSUMED**: a provisional input used for analysis. It may change.
- **CALCULATED**: derived from stated inputs by a reproducible calculation. Only as good as its inputs.
- **OPEN**: unresolved. The row says what closes it.

A row moves to CONFIRMED only with the user's word or a cited source. Changing a label is a decision: log it in [DECISIONS.md](DECISIONS.md).

## A. Scope

| ID | Requirement | Value | Label | Source / what closes it |
| --- | --- | --- | --- | --- |
| C01 | Standalone V1A module, testable without a Pi or the robot | – | CONFIRMED | User; 00_REQUIREMENTS |
| C02 | DC input with input and reverse-polarity protection | – | CONFIRMED | User; fault envelope is rows S1a–S1f |
| C03 | Regulated high-current output of about 5 V | – | CONFIRMED | User; setpoint and window are L1, L3 |
| C04 | Shunt + INA228 (or justified alternative) with I²C telemetry | – | CONFIRMED | User; captured U401/R401 |
| C05 | Reusable Edge-AI / SBC load output and testability | – | CONFIRMED | User |
| C06 | Sequential R0–R5 gates | – | CONFIRMED | User; see [GATES.md](GATES.md) |
| C07 | Test access and staged bench bring-up before any SBC load | – | CONFIRMED | User; 00_REQUIREMENTS |

## B. Source envelope (S1, revised on user review)

The analysis source is the Mean Well GST60A24-P1J. **It is ASSUMED, not the confirmed adapter** (DECISIONS D-14).

| ID | Parameter | Value | Label | Depends on the final adapter? |
| --- | --- | --- | --- | --- |
| S1 | Actual adapter | not chosen | OPEN | Closed by the user naming the adapter or its datasheet |
| S1a | Steady maximum at J501 | 24.72 V (24 V + 3 %) | ASSUMED | Yes: TVS standoff and high-side-short source voltage |
| S1b | Steady minimum | 9.0 V | ASSUMED (P01 proposal) | Yes, if a 12 V or 19 V adapter is chosen |
| S1c | Source OVP range | 25.2–32.4 V | ASSUMED | Yes: sets the TVS breakdown floor |
| S1d | Overload behaviour / available current | hiccup at 105–150 % of 2.5 A | ASSUMED | Yes: F101 coordination |
| S1e | Output capacitance and cable | 2 m cable, hot-plug only; adapter capacitance unknown | ASSUMED / OPEN | Yes: hot-plug ringing |
| S1f | Surge class | none (bench module) | ASSUMED | No |

## C. Load envelope

| ID | Parameter | Value | Label | Source / what closes it |
| --- | --- | --- | --- | --- |
| L1 | Buck output setpoint | 5.098 V | CALCULATED | Feedback divider, rechecked 2026-09-29 on the Mac |
| L2 | Load current | 5 A continuous; 6 A for ≤ 100 ms | ASSUMED | P03 proposal; peak is a screening point only |
| L3 | Raw static regulation | 5.04–5.16 V | CALCULATED | PR #1 envelope |
| L4 | Pi connection (GPIO 5 V pins or USB-C) | – | OPEN | User answer |
| L5 | Largest realistic load step and slew | analysis uses 5 A → 0 A | OPEN | User answer (which USB devices hot-plug) |
| L6 | Load capacitance | 2–220 µF analysed; Pi 5 value unknown | ASSUMED | Raspberry Pi data or measurement |
| L7 | Pi voltage at 5 A, static hot-wire case | 4.7997 V (4.6997 V with 100 mV assumed droop) | CALCULATED | 2026-09-14 blocker review; no qualified harness |

## D. Protection

| ID | Requirement | Value | Label | Source / what closes it |
| --- | --- | --- | --- | --- |
| P1 | Independent output OV disconnect with defined reverse-feed behaviour (Sheet 03) | architecture not chosen; option I PROPOSED | OPEN | User approval of an architecture (D-20), then Codex brief 02 evidence |
| P2 | OV trip window | LM74800-only 5.45–5.79 V is a candidate window; option I 5.40 V ±1.1 % | CALCULATED window; nuisance immunity OPEN | Load-release overshoot is an ideal-controller estimate (5.63 V without bulk), not a bound. Needs LM61460 PSpice, then bench |
| P3 | Trip to load isolation | ≤ 2 µs with bulk | CALCULATED | Delay sensitivity in PR #1 §3; vendor-model and bench confirmation needed |
| P4 | Load fault voltage versus time | 6.0 V peak as a screening criterion only; 5.5 V at the board rail proposed as an interim ceiling (INFERRED, PR #4) | ASSUMED; the real envelope is OPEN | Not a Pi damage rating (D-13). PR #4 (2026-09-29): no official Pi 5 survival rating exists; Raspberry Pi engineer guidance is 4.75–5.5 V with transients ≤ 5.5 V; GPIO feeding bypasses the Pi's USB-C OVP; lowest component absolute maximum found is 6.0 V (AP22652, not a board rating). Closed by a Raspberry Pi statement or a component-level analysis |
| P5 | Recovery policy (latch, retry, chatter, start-up) | candidate: latch off until input is cycled, no automatic retry | OPEN | Conditional on thresholds and the real rail trajectory (D-12). Needs the approved architecture and a bench check |
| P5b | Detector latch and hysteresis | latching, hysteresis ≥ 50 mV, valid before the path enables | OPEN (proposal) | Approved architecture |
| P6 | Telemetry during a trip | INA228 domain may lose power | ASSUMED (inferred) | Approved architecture |
| P7 | Reverse feed with input off | ≤ 100 µA into `VOUT_5V1`, load held ≤ 5.25 V | OPEN (proposal) | Verify at R5 |
| P8 | Protection-path drop at 5 A | ≤ 35 mV (32.5 mV calculated) | CALCULATED, conditional | Holds only for PSMN1R8-40YLC at max RDS(on), VGS ≥ 10 V, copper excluded (PR #1 §8) |
| P9 | Start-up | path enabled from BUCK_PGOOD; input current ≤ 90 % of the eFuse minimum limit at 9 V | OPEN (proposal) | Approved architecture |
| P10 | Input UVLO | 8.457 V | CALCULATED | Divider, rechecked 2026-09-29 |
| P11 | Input eFuse OVP | 27.63 V | CALCULATED | Divider, rechecked 2026-09-29 |
| P12 | Input TVS D101 | SMBJ26CA captured; NOT QUALIFIED | OPEN | Must never conduct at the source's worst OVP; hot clamp + overshoot < 67 V at U101 IN (D-15, D-16) |
| P13 | Fuse F101 | 5 A class, no exact part | OPEN | Source short-current, DC interrupt rating, I²t and coordination with TVS and eFuse |

## E. Interconnect, environment and board

| ID | Requirement | Value | Label | Source / what closes it |
| --- | --- | --- | --- | --- |
| E1 | J501 input, J502 5.1 V / 5 A output, J503 I²C connectors | pinouts captured; parts, mates and footprints not chosen | OPEN | User's brother's connector review, then selection |
| E2 | Ambient | 0–40 °C, natural convection, open bench | ASSUMED | User |
| E3 | Junction temperature | ≤ 125 °C and ≥ 20 °C below each part's rating | ASSUMED | Engineering proposal |
| E4 | Stack-up | 4 layers, 2/1/1/2 oz | ASSUMED | R3 |
| E5 | Board size | ≤ 65 × 55 mm; option I adds area | ASSUMED | R3 floorplan |

## Facts only the user can supply

In priority order, because they change the architecture decision:
1. The real adapter, or at least its maximum steady voltage and OVP range (S1, S1a, S1c).
2. How the Pi is powered, GPIO pins or USB-C, and any Raspberry Pi statement on input fault tolerance (L4, P4).
3. The largest realistic load step (L5).
4. The brother's connector review (E1).
