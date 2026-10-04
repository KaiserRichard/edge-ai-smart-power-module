# Raspberry Pi 5 direct 5V/GND power interface

2026-09-12. **CONDITIONAL use case; R2 BLOCKED. NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED.**

## Supported architecture and source authority

**REQUIREMENT:** retain the generic V1A power path:

```text
VIN_RAW -> input protection -> VIN_PROTECTED -> LM61460 -> VOUT_5V1
 -> independent output disconnect -> VOUT_PROTECTED -> Kelvin shunt
 -> LOAD_5V1 / J502 -> short rated harness / adapter -> Pi 5 header 5V + GND
```

SOURCE: Raspberry Pi's [USB Power Delivery on Raspberry Pi 5](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf), Release 1, build 2026-03-17 `1026f0c6e305`, printed p.8; current [bootloader documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#PSU_MAX_CURRENT) and [power properties](https://www.raspberrypi.com/documentation/computers/configuration.html). Official pages were checked live. The documentation repository's current `master` is still `5e2c40fe1125bb8ff7374de2c11c94761084eb1f`, matching the existing cached sources. Exact identities, sections, rights and acquisition evidence are in [pi_direct_sources.json](takeover_2026-09-12/pi_direct_sources.json).

FUNCTION: supply the Pi's power rail through an external adapter. MODIFICATION: no USB-C connector/PD controller or Pi mounting/header is added to V1A. RATIONALE: the same protected load connector serves a dummy load or other SBC; the adapter owns Pi pin mapping, mechanical retention and contact qualification. No HAT EEPROM, HAT geometry, MCU, USB data or V1B circuit is required. The power adapter does not connect to 3.3 V or signal GPIO pins; optional telemetry remains a separate reviewed 3.3 V interface.

**EVIDENCE:** the official white paper explicitly describes GPIO powering. With no PD, firmware assumes a 5 V / 3 A supply. For a genuinely qualified 5 A source and complete delivery path, EEPROM `PSU_MAX_CURRENT=5000` bypasses negotiation and automatically enables the higher USB allowance. `usb_max_current_enable=1` in `config.txt` only overrides that USB policy. Neither setting creates supply capacity or electrical protection. The white paper also describes restrictions on USB boot without the higher-current capability; boot behavior must be checked on the actual EEPROM version. These are firmware assumptions for later integration, not changes made to the separate Pi environment.

The current [hardware power documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply) specifies aggregate USB allowances of 600 mA or 1.6 A, with the fan sharing that budget. This is not 1.6 A per port, a 3 A hardware clamp on header input, or a claim that the Pi continuously consumes 5 A. Include peripherals/fan in the 5 A module budget. Peripheral data cables remain external to V1A.

## Voltage limits: what is and is not established

**EVIDENCE:** the official [HAT+ electrical guidance](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf), chapter 6, recommends 5 A at 5.1 V for a header-powered source. This supports the nominal-voltage direction without making V1A a HAT. The reviewed official Pi 5 documents do **not** provide a complete header-input normal tolerance, absolute maximum versus time, or permitted fault energy.

**ASSUMPTION:** use 4.75-5.25 V only as a provisional engineering screening window. It is not a sourced Pi 5 damage limit or an accepted universal SBC specification. The documentation's generic low-voltage detector figure, 4.63 V +/-5%, is a warning threshold, not a guaranteed operating floor. Its upper extreme is about 4.862 V; a 4.80 V screening result alone cannot guarantee warning-free operation. Load-specific limits remain OPEN, including any connected USB peripherals.

**DECISION:** retain the frozen 5.1 V nominal buck setting. It is appropriate in principle for a short, sufficiently low-resistance delivery path. Full-load adequacy is conditional on actual internal and external losses, regulator tolerances and dynamics. Do not raise the setpoint to disguise cable loss without reopening the no-load upper-voltage and output-OVP budgets.

## Connector, wiring and Pi contacts

**OBSERVATION:** J502 currently has only a two-pin functional symbol (`1=LOAD_5V1`, `2=GND`); its exact part and footprint are OPEN. The existing drawing therefore has no established physical 5 A connector rating.

**REFERENCE CANDIDATE:** Phoenix Contact **1757242** (`MSTBA 2,5/2-G-5,08`) with mating plug **1757019** (`MSTB 2,5/2-ST-5,08`). Manufacturer pages explicitly pair them and specify 12 A nominal and 320 V ratings under their stated conditions. Header contact resistance is listed as 1.4 mOhm; plug durability data give 1.3/1.4 mOhm. These are not a guaranteed complete hot harness resistance. The plug accepts 0.2-2.5 mm2 flexible conductors / AWG 24-12, with 7 mm strip length and 0.5-0.6 Nm screw torque. Sources: [header](https://www.phoenixcontact.com/en-us/products/pcb-header-mstba-25-2-g-508-1757242), [plug](https://www.phoenixcontact.com/en-ae/products/pcb-plug-mstb-25-2-st-508-1757019).

**DECISION:** this is a defensible connector candidate for qualification, not a fitted selection. Verify the exact mate's derating curve at the approved ambient, wire termination/ferrule, polarity, solder lands and retention. It has no locking mechanism. Provide harness strain relief; choose incompatible input/output mating systems or positive coding so a 24 V input lead cannot be inserted into the Pi adapter. Current margin alone does not close those items.

**REFERENCE WIRE:** [Belden 37118](https://www.belden.com/products/cable/electronic-wire-cable/lead-wire-hook-up-wire/37118), revision 0.482 / 2026-02-20, is 18 AWG stranded tinned copper with nominal DCR 7.06 Ohm/1000 ft. Its manufacturer lists 27.2 A per conductor at 30 C, 600 V insulation and 125 C flex / 150 C non-flex construction. That rating is conditional on the manufacturer's installation/thermal assumptions; it is not the rating of this adapter. Its 3.58 mm outside diameter and 35.8 mm minimum bend radius also require mechanical space. This is a source-backed resistance/rating example, not a procurement selection. A short 18 AWG copper pair is a reasonable starting point; the exact wire and assembled harness must sustain 5 A continuously at temperature and withstand the coordinated fault interruption. Do not substitute thin jumper leads, ribbon cable or copper-clad aluminium on an AWG label alone.

**PROPOSED ADAPTER CONNECTION:** use both physical 5 V pins **2 and 4**, and at least two ground contacts, for example physical **6 and 9**, with comparable branch lengths. Verify orientation against the official [GPIO pinout](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header). At equal sharing, two contacts per polarity carry 2.5 A each at 5 A total. This is arithmetic, **not a Raspberry Pi per-pin current rating**. No official Pi 5 fitted-header contact rating was located. Select and verify the mating socket, installed Pi header compatibility, contact resistance/temperature, and current imbalance before claiming 5 A support. A missing/poor contact can transfer nearly the full current to the remaining contact; two pins do not make a single-contact fault safe.

## Reproducible resistance and voltage-drop calculation

Inputs: [pi_interface_assumptions.json](pi_interface_assumptions.json). Results: [pi_interface_calculations.json](takeover_2026-09-12/pi_interface_calculations.json). All numbers here are **CALCULATION**, not measurements.

```text
Rwire = 2 * one_way_length * nominal_wire_DCR
Rcontacts = parallel(5V contacts) + parallel(GND contacts)
Vpi = Vconnector - I * Rexternal
Vpi = Vbuck - I * (Rinternal + Rexternal)   # actual feedback boundary
Ppath = I^2 * Rpath
```

| External loop contribution | Screening value | Classification |
| --- | ---: | --- |
| 0.20 m outgoing + 0.20 m return, 18 AWG example | 9.265 mOhm | Manufacturer nominal DCR; 20 C reference temperature assumed |
| Module connector, both polarities and terminations | 5 mOhm | ASSUMPTION; includes mate/termination allowance; not sum of guaranteed vendor maxima |
| Two 10 mOhm Pi contacts in parallel on each polarity | 10 mOhm total | ASSUMPTION; contacts not yet selected or measured |
| Adapter joints/short branches, complete loop | 5 mOhm | ASSUMPTION; must include every joint and any added socket/connector |
| Total external loop | **29.265 mOhm** | Nominal screening case |
| Total with wire at 60 C | **30.722 mOhm** | Copper coefficient 0.00393/C; contact aging/temperature still unbounded |

The first voltage column below assumes an ideal **5.100 V at the module connector**. The captured buck instead regulates at VOUT_5V1, ahead of output protection and shunt. To show that difference, the second voltage column uses its actual divider result, 5.09836 V, and **allocated**, unqualified internal resistance of 10 mOhm for a future disconnect + 2 mOhm shunt + 5 mOhm board/return copper. No 10 mOhm output switch is selected.

| Load | External drop | Pi voltage from ideal 5.100 V connector | Pi voltage from nominal buck including 17 mOhm internal allocation |
| --- | ---: | ---: | ---: |
| 1 A | 29.3 mV | 5.0707 V | 5.0521 V |
| 3 A | 87.8 mV | 5.0122 V | 4.9596 V |
| 5 A | 146.3 mV | 4.9537 V | 4.8670 V |

At 5 A, external-loop heat is 0.732 W; internal allocated loss is 0.425 W. The external cable loss is outside a connector-to-connector module-efficiency measurement. It still reduces power delivered to the Pi: a nominal 25.5 W buck output is not automatically 25.5 W at the Pi header.

The prior buck's static low-voltage screen is 5.03827 V (itself not a guaranteed complete corner). With the hot-wire loop and internal allocation, the Pi gets **4.7997 V at 5 A**, leaving only **49.7 mV** to the provisional 4.75 V floor. An additional **100 mV illustrative transient droop** gives **4.6997 V**, failing that screen. External loop budgets are 40.65 mOhm for this static screen or **20.65 mOhm** when reserving 100 mV. The 29.27 mOhm example does not meet the latter. Shorter/thicker wire, lower measured contact resistance and lower internal switch/copper loss must close the actual budget. The ripple target also consumes margin; do not assume all peak-to-peak ripple is symmetrically distributed without measurement.

A 60/100 mOhm external harness gives 4.80/4.60 V at 5 A even from an ideal 5.10 V connector. Including the low buck and internal allocation gives 4.653/4.453 V. Cable/contact quality cannot be replaced by a supply-current configuration setting. At no load, cable compensation disappears; the prior 5.1586 V static high screen leaves about 91 mV to the provisional 5.25 V ceiling before ripple/startup overshoot. That ceiling is not a proven Pi fault threshold.

## Startup, transients and protection

**OBSERVATION:** the existing input ramp is screened at 37.3-63.3 ms at 24 V; the buck has 3.5-7 ms soft-start to 90%. The output stage is absent, so these do not specify a Pi rail ramp. Output switch slew, load activation, prebias and brownout restart remain OPEN.

**CALCULATION:** an assumed 1000 uF load charged to 5.1 V in 5 ms adds 1.02 A of capacitor current before active Pi demand. This is not a measured Pi capacitance. An illustrative 2 A load step unsupported for 10 us causes 0.235 V capacitor-only droop in the prior 85.272 uF effective raw bank; ESR, cable inductance and switch impedance add response terms. This is not a prediction of the Pi waveform. Increasing capacitance without analysis raises inrush and can change buck dynamics. Require a defined load-step amplitude, edge, duration, repetition and load-capacitance/ESR envelope; verify startup and transients at the Pi end with dummy loads first.

**R2 BLOCKER:** there is currently no independent output detector, disconnect device, threshold, guaranteed response, recovery policy, conduction-loss rating or reverse-current specification. The open sheet is not a working protection circuit. Upstream input OVP does not detect a buck high-side failure at a normal 24 V input. The [existing LM74800 review](OUTPUT_PROTECTION.md) remains applicable: its comparator spread and delay do not justify a narrow 5 V protection window; a proposed normal-voltage screen cannot substitute for a load fault voltage/time limit. No bypass may be used for Pi operation.

The [required output review](OUTPUT_PROTECTION.md) must close trip tolerance, delay plus FET turn-off, let-through including inductor energy, high-voltage survival, hot SOA, local telemetry survival and persistent/intermittent fault recovery. A wide-voltage monitor or 50 V raw capacitors do not protect the Pi. An independent precision detector with a rated reverse-blocking disconnect may be necessary; no such circuit is invented here.

## Multiple sources, backfeed and measurement boundary

**DECISION for the conditional laboratory use case:** operate with one intentional source. Disconnect USB-C power, PoE power and other 5 V sources before using the V1A adapter. Check powered USB peripherals/hubs for upstream backfeed. Do not assume an undocumented Pi internal power-path detail prevents supplies fighting. The [HAT+ chapter 4 source-only requirement](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf) is useful electrical guidance for accidental coexistence, even though V1A is generic.

| Supply state | Required final behavior | Present draft / consequence |
| --- | --- | --- |
| V1A is the only source | Protected forward supply, all Pi current crosses shunt | Sheet 03 open: VIN cannot power Pi |
| USB-C/PoE/another source also drives Pi | Tolerate accidental coexistence; no harmful sinking, circulation or overshoot | Not qualified; intentional simultaneous power excluded |
| VIN absent, external LOAD_5V1 live | Block reverse power into buck/input; quantify telemetry demand and leakage | Open sheet isolates upstream; external LOAD powers local telemetry through shunt in reverse |
| VIN returns to externally powered load | Defined prebias/handover without discharge or excessive current | Not implemented; requires output-stage review |
| Output disconnect opens but another source remains | Do not promise Pi power-off | External source can keep the Pi powered; V1A cannot remove that source |

The 2 mOhm four-terminal shunt remains in the correct place after the intended disconnect. Force source/load orientation and true Kelvin sense are preserved; INA228 VBUS stays on LOAD_5V1. At 5 A the shunt drops 10 mV and dissipates 50 mW. With V1A as the only Pi source, this measures the current delivered to the entire Pi branch, including peripherals powered by the Pi. With another source tied downstream, it measures **V1A branch contribution**, not total Pi current. Its voltage measurement is at the module, relative to module GND, so it does not include the remote positive/return cable drop. Use a separate Pi-end voltage probe; do not move feedback across a disconnect to imitate remote sensing.

The local monitor supply branches before the shunt. TCA9517 separates host/local 3.3 V domains; local ALERT stays at a test point. If the Pi is the I2C host, review its fixed GPIO2/3 pull-ups before fitting R406/R407, retain common ground, and verify off-state voltages/leakage. Pi 5 V may remain present when Pi 3.3 V is off. Do not tie 3V3_LOCAL to the Pi 3.3 V rail. Future V1B must preserve the same reverse-feed analysis and define its own measurement boundary; this review adds no backup hardware.

## Verification plan and release conditions

Reproduce arithmetic from repository root:

```sh
python3 scripts/calculate_pi_interface.py
```

Expected: 29.265 mOhm external loop, 146.325 mV drop at 5 A from an ideal connector, and 4.7997 V for the stated static low-source/hot-wire screen. These are assumed-case results, not a PASS for hardware. Changing either return path, contact sharing, wire temperature or internal loss must change the relevant result.

After R2-R4 review, use staged R5 bring-up: inspection/pin mapping -> continuity/shorts -> current-limited bench supply -> no-load rail -> low dummy load -> 1/3/5 A load steps -> thermal -> ripple -> transients -> fault tests -> telemetry -> Pi last. Measure simultaneous VOUT_5V1, J502 and dummy-load/Pi-end voltages, four-wire loop/contact resistance, individual parallel-contact current, connector/wire temperatures and fault let-through. Log instruments, uncertainty, source impedance, wire/adapter details, ambient, firmware/configuration, commit and raw results. An open contact, hot termination, repeated restart, low-voltage warning, bus back-powering, current-sign mismatch or excess OV exposure fails its test. Numeric thermal/fault acceptance limits remain OPEN.

Later Pi integration checks (instructions only; not executed here): record `vcgencmd bootloader_version`, inspect `vcgencmd bootloader_config`, and, after a genuinely qualified 5 A path exists, have the Pi environment owner set EEPROM `PSU_MAX_CURRENT=5000` using `sudo rpi-eeprom-config -e` and reboot. Check `vcgencmd get_config usb_max_current_enable`, power properties and `vcgencmd get_throttled`, along with physical rail measurements under the real workload. Software diagnostics supplement the oscilloscope and current/thermal measurements.
