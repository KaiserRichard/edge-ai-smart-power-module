# Project II V1A requirements

Date: 2026-09-11. Baseline: `a9fe716`, branch `docs/r0-r1-engineering-audit`, plus uncommitted documentary evidence.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Scope and requirement authority

**CONFIRMED — user scope correction:** the primary product is the standalone **Smart DC Power Module for Edge AI Devices — Project II V1**, called **V1A** when distinguishing it from the teammate's **V1B supercapacitor subsystem**. Future V2 integrates validated V1A and validated V1B, with additional supervision/protection only after review. V1B is not part of the current schematic.

The V1A functional chain is DC input → input/reverse-polarity protection → DC/DC conversion → regulated high-current approximately 5-V output → shunt/current monitor → reusable load output, with I2C telemetry. Requirements come from the user and subsequent manager approval, not from predecessor component ratings.

CAN/CAN-FD, MCP2518FD, robot battery voltage, WBR interfaces, supervisor/watchdog MCUs, robot fault ownership, D435i data routing, HAT/HAT+ geometry and WBR sequencing are **not V1A requirements**. Preserve the [WBR study](WBR_EDGE_SUPERVISOR_HAT_FEASIBILITY.md) as future reference only. USB3 routing remains excluded.

CONFIRMED means explicitly required. PROPOSED means an engineering candidate submitted for review. TBD / OPEN means no acceptance value or implementation is approved. A numerical example in an earlier report is not a requirement.

## Requirement register

| ID | Status | Requirement or candidate | Evidence/rationale and closure needed |
| --- | --- | --- | --- |
| C01 | CONFIRMED | Standalone academic V1A module; independently testable without Pi/WBR | User correction; no host required to regulate or interrupt electrical faults |
| C02 | CONFIRMED | DC input, input protection and reverse-polarity protection | Exact normal/fault envelope and allowed leakage/damage criteria remain OPEN |
| C03 | CONFIRMED | DC/DC conversion to regulated high-current approximately 5 V | Exact setpoint, tolerance, current and load model not confirmed |
| C04 | CONFIRMED | Shunt plus INA228 or justified alternative; voltage/current/power/energy monitoring and I2C | INA228 preferred by documentary evidence; final monitor and calibration still reviewed |
| C05 | CONFIRMED | Reusable Edge-AI/SBC load output and testability | No Pi header, USB connector or vendor-specific load interface is mandatory |
| C06 | CONFIRMED | Sequential R0–R5 gates; R2 blocked for this mission | No schematic, PCB, purchases or hardware integration authorized |
| P01 | PROPOSED | Study 9–24 V DC at the module input connector | Supports nominal 12/19/24-V adapters and a 28-V-class buck, subject to source tolerance and protection margins. A nominal 24-V source is not a 24-V maximum |
| O01 | TBD / OPEN | Freeze actual input minimum/maximum, source type, tolerance, cable, fault current, surge/hot-plug envelope | Earlier 9–28 V is retained as an alternative question, not adopted. If 28 V is normal maximum, prefer a higher-voltage converter; never operate a 28-V part at its ceiling without margin |
| P02 | PROPOSED | Compare 5.00 V and 5.10 V fixed setpoints; characterize 4.75–5.25 V as a candidate load-terminal window | Pi power guidance motivates review, not a universal SBC absolute rating. Freeze the actual load's normal and fault-voltage limits first |
| P03 | PROPOSED | 5 A continuous target; 3 A reduced-scope alternative | 25 W class is useful for demanding SBC loads; Pi's recommended supply capability is not measured consumption. Includes all output branches that V1A supplies |
| O02 | TBD / OPEN | Peak load and duration, slew rate, repetition, downstream capacitance | 6 A is a screening point only. No approved peak-current rating exists |
| P04 | PROPOSED | At least 90% whole-module efficiency at nominal 12/24 V, 5 V, 3–5 A, 25°C | EVM results make this worth evaluating; protection and wiring losses reduce converter-only efficiency. Characterize the full approved input/load/temperature range; no measured efficiency yet |
| P05 | PROPOSED | ≤50 mV peak-to-peak steady ripple at module output under defined CCM conditions | Manufacturer examples report 30–40 mV at different loads. Proposed test: AC coupling, 20-MHz bandwidth limit, ground spring. Light-load skip-mode ripple and load transients need separate limits |
| P06 | PROPOSED | Initial 25°C bench campaign; evaluate 0–50°C ambient operating envelope, natural convection | Enclosure, airflow, board area and duty cycle OPEN. Candidate engineering ceiling Tj ≤125°C and ≥20°C below each part's rated maximum, whichever is stricter; not a frozen thermal specification |
| O03 | TBD / OPEN | Accessible-surface, connector and shunt temperature/rise limits | Use selected component ratings and agreed touch-temperature/test conditions; shutdown temperature is not a design operating target |
| P07 | PROPOSED | Coordinated fuse, input reverse block, UV/OV cutoff and controlled inrush | Candidate TPS26630/31 plus required external reverse-protection devices; simpler fuse/MOSFET alternative if the source envelope permits |
| O04 | TBD / OPEN | Reverse-input duration/voltage, overcurrent trip accuracy/delay, short-circuit retry or latch policy | Protect wiring, connector, MOSFET SOA and converter. Fault interruption cannot depend on host telemetry |
| P08 | PROPOSED | Independent output overvoltage disconnect and defined reverse-feed behavior | A buck high-side short can expose a load to input voltage. Exact circuit/let-through limits are unresolved; internal converter OVP is insufficient for that failure mode |
| O05 | TBD / OPEN | Connector family, mating parts, wire gauge/length, contact derating and allowable total path resistance | Must support continuous, peak, startup and fault currents at temperature; generic terminal/header pitch is not a current rating |
| P09 | PROPOSED | Compare 1, 2 and 5 mΩ four-terminal shunts; load-side high-side sensing | [Calculations](04_POWER_CALCULATIONS.md) compare drop, heat, range and errors. 2 mΩ is a leading candidate, not final selection |
| O06 | TBD / OPEN | Current/voltage/power/energy accuracy bands, temperature range and calibration method | Candidate calibrated current target ±(1% of reading + 1 mA) over an approved range starting at 0.1 A. A 1% shunt alone cannot guarantee this |
| P10 | PROPOSED | 3.3-V-compatible I2C, initial 100 kHz, address candidate 0x40; optional ALERT/test pad | Confirm host, pull-ups, capacitance, connector and powered-off behavior. No MCU required; bus configuration is not frozen |
| P11 | PROPOSED | Four-layer PCB; start thermal/layout assessment from 2/1/1/2 oz manufacturer example | TPS56837 datasheet §7.4; final board size, stackup/copper and assembly process OPEN. Two layers require a separate thermal/layout justification |
| C07 | CONFIRMED | Test access and staged bench bring-up before SBC load | Test points for input/protected input, raw/protected output, both shunt sense nodes, ground, EN/PG/fault and I2C |
| O07 | TBD / OPEN | Board dimensions, fabrication rules, BOM budget and component supply chain | Exact parts/stock and assembly capability must be reviewed before R2 freeze; no availability or procurement guarantee |

## Future V1A–V1B interface register

These are questions for both teams, not a connector definition or permission to design V1B. None of the V1A candidate numbers above fills these entries automatically.

| Interface parameter | Status | Agreement needed before V2 |
| --- | --- | --- |
| Rail voltage | TBD | Which side of conversion/protection hosts the interface? |
| Allowed voltage range | TBD | Normal, startup, backup, transient and fault limits in both directions |
| Maximum load current | TBD | Continuous/peak/time envelope at the selected rail |
| Charge-current allowance | TBD | Load priority, available headroom and recharge time |
| Reverse-current behavior | TBD | Blocking/OR-ing ownership and allowed leakage in every supply state |
| Common ground | TBD | Reference connection, return-current paths and sequencing |
| Connector | TBD | Pinout, mating pair, current rating, keying and wire |
| Power-fail signal | TBD | Source, threshold, lead time, polarity, domain and validity when unpowered |
| Telemetry | TBD | Bus/address ownership, measured boundary, energy accounting and reset gaps |
| Startup/shutdown behavior | TBD | Empty/charged V1B, prebias, hot-plug, source return and restart ownership |
| Backup/hold-up requirements | TBD | Load profile, duration, minimum rail, aging/temperature reserve and graceful-shutdown need |

## Acceptance plan and R2 entry

Before R2, the manager must close O01–O07 to the extent they determine schematic topology, component ratings and interfaces, approve the architecture and authorize schematic work. V1B interface values can remain TBD while V1A stays independent; R2 must nevertheless analyze an externally energized output and avoid an uncontrolled backfeed/discharge path.

Future qualification follows AGENTS: visual inspection → continuity → current-limited supply → no-load/output verification → low dummy load → load steps → thermal → ripple → transients → faults → telemetry → SBC. Record equipment, source/cable, input/output readings, ambient/airflow and exact configurations. Expected acceptance is compliance with the approved register, not simply operation at one bench point. Oscillation, excessive droop/heat, repeated hiccup, reverse feed or unexplained telemetry gaps fail the relevant test.

Sources and provenance: [reference audit](01_REFERENCE_AUDIT.md); recommendation: [architecture](02_ARCHITECTURE.md); gate decision: [manager report](FINAL_MANAGER_REPORT.md).
