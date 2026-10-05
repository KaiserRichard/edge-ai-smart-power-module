# Requirements (Step 0 table)

Current working requirement table for V1A. **Partially frozen:** the user fixed the normal input range, GPIO power interface, and intended load scope on 2026-09-29 (D-30); fault bounds and component choices remain OPEN. It merges the confirmed scope in [docs/00_REQUIREMENTS.md](../docs/00_REQUIREMENTS.md) with the proposed revision 2 envelope in draft [PR #1](https://github.com/KaiserRichard/edge-ai-smart-power-module/pull/1) (`REQUIREMENT_ENVELOPE_PROPOSED.md`), which answers the user's 2026-09-26 review of revision 1. Seeded 2026-09-29.

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

## B. Source envelope (updated by user D-30)

**CONFIRMED / KNOWN requirement:** intended final robot chain is a 13S Li-ion battery (approximately 48 V nominal, 54.6 V maximum) → Main Protection / power distribution board → future HV-to-approximately-12-V auxiliary converter → V1A. These are user-specified system intentions, not validated equipment ratings. V1A remains a standalone module; direct battery connection is not authorized. There is no required wall adapter in the final architecture. A programmable DC supply may emulate the auxiliary rail during bench work.

The earlier Mean Well GST60A24-P1J source and its numerical envelope remain **historical ASSUMED analysis cases only**. They do not specify the future converter. Preserve the old analysis; do not silently relabel its outputs as qualified for the robot source.

| ID | Parameter | Value | Label | Closure / consequence |
| --- | --- | --- | --- | --- |
| S0 | V1A normal input operating requirement | 9–24 V at V1A input | CONFIRMED (KNOWN requirement) | User D-30; not a demonstrated operating rating or a fault-withstand limit |
| S1 | Final upstream HV-to-approximately-12-V converter model / MPN | not selected | OPEN | Future selection must satisfy an agreed input-interface envelope; wall adapter selection is not required |
| S1a | Source voltage tolerance and maximum abnormal voltage / duration at J501 | not bounded | OPEN | Historical 24.72 V case remains ASSUMED; derive and approve allowable limits before source compatibility is claimed |
| S1b | Minimum normal input | 9.0 V | CONFIRMED (KNOWN requirement) | User D-30; verify startup and full-load performance at this corner |
| S1c | Upstream overvoltage protection and HV pass-through containment | not specified | OPEN | Define fault responsibility and voltage-versus-time bound; normal 9–24 V does not establish battery-fault protection |
| S1d | Prospective short current, current-limit response, foldback / restart | unknown | OPEN | Bound for input protection and persistent buck-short analysis; no Mean Well hiccup behavior is assumed for the new source |
| S1e | Output capacitance, wiring impedance, startup and transient behavior | unknown | OPEN | Bound stored energy and transient impedance; a generic bench supply is not automatically equivalent |
| S1f | Robot/bench surge environment | not defined for final robot | OPEN | Historical no-surge bench assumption remains limited to that analysis |

## C. Load envelope

| ID | Parameter | Value | Label | Source / what closes it |
| --- | --- | --- | --- | --- |
| L1 | Buck output setpoint | 5.098 V | CALCULATED | Feedback divider, rechecked 2026-09-29 on the Mac |
| L2 | Output load envelope | designed 5 A envelope | CONFIRMED target; capability unvalidated | User D-30; includes intended loads drawing through V1A, not an extra peripheral allowance |
| L2a | Historical overload screening point | 6 A for ≤ 100 ms | ASSUMED | P03 proposal retained; not promoted to a guaranteed mode by D-30 |
| L3 | Raw static regulation | 5.04–5.16 V | CALCULATED | PR #1 envelope |
| L4 | Pi power interface | Direct 5 V through GPIO header power pins with multiple grounds; no USB-C PD redesign | CONFIRMED | User D-30. Raw rail → Sheet 03 → protected rail → 2 mΩ Kelvin shunt / INA228 → LOAD_5V1 → J502/harness → Pi. Harness implementation remains OPEN |
| L5 | Required load / qualification scope | Pi 5 idle; sustained CPU-heavy load; Pi 5 + D435i operating; representative steps up to designed 5 A envelope | CONFIRMED | User D-30; D435i may remain connected and operating during runtime. Arbitrary USB peripheral hot-plug is not guaranteed in R2; additional peripherals excluded unless characterized |
| L5a | Load-step amplitudes/slew, inrush, camera mode and power route | exact test bounds not yet established | OPEN | Bound analytically and with electronic loads, then characterize intended system. Historical 5 A → 0 A remains a conservative analysis case, not a measured runtime waveform |
| L6 | Load capacitance | 2–220 µF analysed; Pi 5 value unknown | ASSUMED | Raspberry Pi data or measurement |
| L7 | Pi voltage at 5 A, static hot-wire case | 4.7997 V (4.6997 V with 100 mV assumed droop) | CALCULATED | 2026-09-14 blocker review; no qualified harness |

## D. Protection

| ID | Requirement | Value | Label | Source / what closes it |
| --- | --- | --- | --- | --- |
| P1 | Independent output OV disconnect with defined reverse-feed behaviour (Sheet 03) | architecture not chosen; option I PROPOSED | OPEN | User approval of an architecture (D-20), then Codex brief 02 evidence |
| P2 | OV trip window | LM74800-only 5.45–5.79 V is a candidate window; option I 5.40 V ±1.1 % | CALCULATED window; nuisance immunity OPEN | Load-release overshoot is an ideal-controller estimate (5.63 V without bulk), not a bound. Needs LM61460 PSpice, then bench |
| P3 | Trip to load isolation | ≤ 2 µs with bulk | CALCULATED | Delay sensitivity in PR #1 §3; vendor-model and bench confirmation needed |
| P4 | Load fault voltage versus time | **≤ 5.5 V at the Pi 5 board rail, with margin** (user decision D-27, 2026-09-29). The full voltage-versus-time envelope is still unknown | CONFIRMED limit; envelope OPEN | PR #4: no official Pi 5 survival rating exists; Raspberry Pi engineer guidance is 4.75–5.5 V with transients ≤ 5.5 V; GPIO feeding bypasses the Pi's USB-C OVP; lowest component absolute maximum found is 6.0 V (AP22652, not a board rating). 6.0 V is withdrawn as a screen |
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
| E1 | J501 input, J502 5.1 V / 5 A output, J503 I²C connectors | pinouts captured; parts, mates and footprints not chosen | OPEN | D-30: J502/harness remains OPEN pending resistance, current, retention and mechanical qualification. Candidate review and approval before capture; complete schematic set before brother handoff (D-29) |
| E2 | Ambient | 0–40 °C, natural convection, open bench | ASSUMED | User |
| E3 | Junction temperature | ≤ 125 °C and ≥ 20 °C below each part's rating | ASSUMED | Engineering proposal |
| E4 | Stack-up | 4 layers, 2/1/1/2 oz | ASSUMED | R3 |
| E5 | Board size | ≤ 65 × 55 mm; option I adds area | ASSUMED | R3 floorplan |

## Remaining decisions and evidence

GPIO entry and intended load scope are resolved (D-30). Do not request a final wall adapter or re-open USB-C versus GPIO.

- Propose and approve a bounded upstream source/fault interface, including responsibility for an auxiliary-converter HV pass-through fault. Final converter identity can remain OPEN while its acceptance limits are developed.
- Bound load dynamics, acceptable Pi-terminal voltage drop, effective capacitance, and startup behavior through calculations, models and staged experiments. D435i operating configuration and its intended power route still require characterization.
- Approve Sheet 03 architecture, recovery/reset behavior, and external backfeed/dual-source policy. The existing 5.5 V board-rail limit with margin remains in force; no allowed overvoltage pulse has been established.
- Select and qualify connectors and harness; select/coordinate F101 and D101 against the approved source envelope.
- No KiCad change is authorized by D-30. R2 and R3 stay BLOCKED.
