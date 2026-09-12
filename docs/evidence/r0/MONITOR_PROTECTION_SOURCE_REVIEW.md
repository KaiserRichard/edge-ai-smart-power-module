# R0/R1 monitor and protection source review

Date: 2026-09-11. Author: execution engineer. Scope: reference inspection and architecture recommendations only.

**NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED**

No schematic, footprints, PCB, or protection settings are approved by this review. Numerical examples use a **proposed**, not frozen, 9-28 V input and 5.1 V / 5 A output, with 6 A considered only as a load-envelope question. Board thermal and fault performance remain untested.

## Source register and provenance

All manufacturer material below was **referenced**, not copied into a project circuit. Local PDFs remain unmodified under the ignored `third_party/documents/` cache. The root source manifest records retrieval hashes; document revisions below are read from PDF pages, not search-result publication dates. No upstream design source or schematic is incorporated in project-authored hardware files.

| ID | Official source and revision | Relevant material inspected | Local cache file |
|---|---|---|---|
| M1 | [TI INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf), SLYS021A, May 2022 | pp. 3-6 limits/accuracy/interface; 13-18 conversion/accumulation; 22-32 registers/scaling; 34-39 filtering/application/layout | `TI_INA228_SLYS021A.pdf` |
| M2 | [TI INA228/229/237/238/239 EVM guide](https://www.ti.com/lit/ug/sbou241e/sbou241e.pdf), SBOU241E, August 2022 | p. 22 signal path; p. 23 Fig. 6-1 SENS063 schematic; pp. 27-30 layout/BOM | `TI_INA228_EVM_SBOU241E.pdf` |
| M3 | [TI Getting Started with Digital Power Monitors](https://www.ti.com/lit/an/sboa511a/sboa511a.pdf), SBOA511A, September 2021 | pp. 3-7 shunt constraints, noise/resolution, current LSB and calibration | `TI_DIGITAL_POWER_MONITORS_SBOA511A.pdf` |
| M4 | [TI INA226 datasheet](https://www.ti.com/lit/ds/symlink/ina226.pdf), SBOS547C, August 2026 | pp. 4-6 electrical limits; pp. 22-28 register set; p. 31 layout | `TI_INA226_SBOS547C.pdf` |
| M5 | [Vishay WSL2726 datasheet](https://www.vishay.com/docs/30131/wsl2726.pdf), document 30131, 29 June 2026 | pp. 1-2 order code, tolerance, component TCR, Kelvin geometry and dimensions; derating/pulse sections | `Vishay_WSL2726_30131_2026-06-29.pdf` |
| P1 | [TI TPS2663 datasheet](https://www.ti.com/lit/ds/symlink/tps2663.pdf), SLVSE94G, June 2024 | p. 1 family capability; pp. 20-22 cutoff, external reverse protection; pp. 37-39 transient/layout guidance | `TI_TPS2663_SLVSE94G.pdf` |
| P2 | [TI LM74500-Q1 datasheet](https://www.ti.com/lit/ds/symlink/lm74500-q1.pdf), SNOSDB7, December 2020 | p. 1 explicit absence of reverse-current blocking; pp. 4-6 operating limits | URL-only inspected reference |
| P3 | [TI LM7480-Q1 datasheet](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf), SNOSD95C, December 2020 | pp. 3-7 pins, limits and OV thresholds/delay; pp. 15-16 load disconnect and slew control; p. 35 layout | `TI_LM7480-Q1_SNOSD95C.pdf` |
| P4 | [TI TPS25982 datasheet](https://www.ti.com/lit/ds/symlink/tps25982.pdf), SLVSEI3D, May 2026 | p. 1 2.7-24 V operating range; pp. 21-22 fixed OVP variants | URL-only screened reference |

**Rights:** TI and Vishay datasheets/EVM documentation are copyrighted manufacturer resources, not open hardware licenses. TI's included notice authorizes development using the TI products described and restricts other reproduction/display. Preserve notices; retain originals as local research cache, link and cite the originals in public documentation. Do not present copied EVM CAD as permissively licensed project work. Vishay includes document 91000 disclaimer and patent notices; no open redistribution license was found. Any later adaptation must record exact circuit, changes and applicable terms in `docs/01_REFERENCE_AUDIT.md`.

**Visual evidence:** local page renders of M2 p. 23 and P1 p. 21 were reviewed, confirming SENS063 signal connections and the additional external reverse-protection FETs. PDF text extraction was used to check numeric limits, with full-page review where circuit connectivity mattered. Web screenshots were unavailable; the repository's `.venv` PyMuPDF supplied the local rendering fallback. This is reference inspection, not a completed layout review.

## Monitor recommendation

**DECISION PROPOSAL:** retain INA228 as the leading V1 monitor. Its integrated energy accumulation avoids making Linux polling cadence the energy timebase. Place a single shunt in the protected output's high side; connect VBUS to the **load side** of that shunt. The measurement then describes delivered load power, excluding converter/protection losses. Module efficiency still needs simultaneous input and output laboratory measurements. Do not claim that one output sensor measures module efficiency.

**EVIDENCE (M1):** INA228 has 2.7-5.5 V VS, 0-85 V bus sensing, selectable ±40.96/±163.84 mV shunt ranges, 20-bit conversion, ±1 µV maximum offset for conversion time >280 µs, ±0.05% gain error, 10 nV/°C offset drift and 20 ppm/°C gain drift maxima. Bus offset/gain maxima are 2.5 mV/0.05%. The 20-bit data format does not promise 20 noise-free bits. Datasheet conditions and Table 8-2 noise performance apply.

**Alternative (M4):** INA226 supports the 5 V common mode and costs one host integration step for energy: software must integrate timestamped power samples and record gaps. Its 16-bit shunt step is 2.5 µV; offset maximum is 10 µV and gain error maximum 0.1%. With 2 mΩ, those correspond to 1.25 mA quantization and 5 mA offset, before shunt error. It has no ENERGY/CHARGE accumulator registers. It is a credible fallback if sourcing, software support or BOM constraints justify reduced low-current performance; no cost saving was measured or price quoted.

### Shunt candidate and range

**DECISION PROPOSAL:** evaluate `WSL27262L000FEA`: a true four-terminal 2 mΩ, ±1%, 3 W at 70°C device. M5 specifies **component** TCR ±25 ppm/°C for 2-5 mΩ; the separate alloy-only TCR statement is not the component limit. This candidate is intentionally real and source-backed, rather than an invented 0.1% low-ohmic ordering code. Its 2726 geometry and height require an actual footprint check in R2.

**CALCULATION:** use `Vshunt = I R` and `Pshunt = I² R`, with nominal R = 0.002 Ω:

| Current | Drop | Dissipation | Interpretation |
|---:|---:|---:|---|
| 0.1 A | 0.2 mV | 0.02 mW | Low-current accuracy test point |
| 5 A | 10 mV | 50 mW | Proposed continuous load |
| 6 A | 12 mV | 72 mW | Proposed peak question; duration remains OPEN |
| 10 A | 20 mV | 200 mW | Instrumentation headroom only; not permitted output loading |

With ±40.96 mV range, nominal analog full scale is ±20.48 A. At +1% resistance and +50°C, a conservative resistance is `2 mΩ × 1.01 × (1 + 25e-6 × 50) = 2.022525 mΩ`; 10 A produces 20.225 mV. This does not establish survivable short-circuit current or pulse energy. Protection must interrupt faults independently of telemetry.

A 1% shunt is not a 0.1% measurement system. A first-order 25°C current budget, before noise/layout/thermoelectric effects, is approximately `1.05% of reading + 0.5 mA` from tolerance, monitor gain and offset. At 5 A it is about 1.06%; at 0.1 A about 1.55%. Another +50°C adds up to 0.125% from shunt TCR, 0.1% from monitor gain drift and 0.25 mA from monitor offset drift. These arithmetic bounds are screening estimates, not a statistical uncertainty statement.

**RECOMMENDATION:** if the manager adopts a ≤1% current objective, make it explicitly a **calibrated target** with a specified current/temperature band. Record four-wire shunt calibration and instrument uncertainty. A tentative engineering target is ±(1% of reading + 1 mA) after calibration over 0.1-6 A; acceptance conditions remain OPEN. Below 0.1 A use an absolute-error specification rather than percentage claims. Validate power and energy separately; full-scale IC accuracy is not percentage-of-reading board accuracy.

### Calibration example and energy semantics

The following is a calculated initialization example, not firmware or an approved experiment format. M1 pp. 30-32 gives the equations; M3 explains why the register scaling must correspond to the installed shunt.

```text
ADCRANGE = 1
Rshunt_nominal = 0.002 ohm
I_numeric_full_scale = 10 A
CURRENT_LSB = 10 / 2^19 = 19.073486328125 microampere
SHUNT_CAL = 4 * 13107.2e6 * CURRENT_LSB * Rshunt = 2000
Power_LSB = 3.2 * CURRENT_LSB = 61.03515625 microwatt
Energy_LSB = 16 * Power_LSB = 0.0009765625 joule
Charge_LSB = CURRENT_LSB coulomb
```

The ×4 is essential for ADCRANGE=1. The numerical CURRENT field limit is just below +10 A here, even though the analog shunt range is larger. Do not treat the larger analog range as valid calibrated-current headroom. Use measured Rshunt when calibration is performed, then account for integer register rounding.

**EVIDENCE (M1):** energy requires continuous conversion; triggered mode accumulation is invalid. ENERGY is 40-bit unsigned, CHARGE is 40-bit signed. Accumulators roll over; reading the respective accumulator clears its overflow flag. Power-on reset clears registers. Therefore logging must inspect diagnostics before accumulator reads, restore configuration after resets, distinguish resets from rollover, and identify missing intervals. ENERGY must not be described as signed net import/export energy. V1 forward delivery is the proposed use; negative-current behavior needs explicit testing.

**CALCULATION:** the energy modulus with the example scaling is `2^40 / 1024 = 1,073,741,824 J`; at constant 25.5 W the first full wrap takes approximately 487.4 days. Positive signed-charge capacity is just below `2^39 × 10/2^19 = 10,485,760 C`, about 24.27 days at 5 A. Polling regularly does not by itself eliminate the need to extend these counters in software. An interruption of monitor power loses the unlogged tail of energy; there is no nonvolatile totalizer in the proposed V1 hardware.

**Timing proposal:** 1.052 ms per shunt/bus/temperature conversion and averaging=16 gives `3 × 1.052 ms × 16 = 50.496 ms`, about 19.8 measurement updates/s. A 10 Hz logger is plausible, with the internal accumulator retaining its own timebase. This is a telemetry proposal, not adequate instrumentation for converter ripple or fast load-transient peaks; use an oscilloscope for those.

### Routing, filtering and power domains

- **DECISION PROPOSAL:** route separate matched Kelvin sense lines directly from the shunt sense terminals; never include the load-current pad/plane segment in the sensed voltage. Keep both traces together, away from SW and inductors, with a continuous quiet ground reference (M1 layout, M2 circuit).
- **Starting point:** 10 Ω in each input and 100 nF differential capacitor at the monitor, plus 100 nF local VS bypass. The differential RC pole is about `1/(2π × 20 Ω × 100 nF) = 79.6 kHz`. Confirm gain loading and load-step settling before freezing. M1 discourages input resistors above 100 Ω; M2 provides 0 Ω/filter options, not a mandate to copy its complete evaluation-board configuration.
- **DECISION PROPOSAL:** use a local 3.3 V LDO from **OVP-protected 5 V**, branching before the load shunt if monitoring only the external load. Do not connect local 3.3 V power to an SBC 3.3 V power pin. The regulator's power loss is small at telemetry-only load but its selected part still needs reverse and startup assessment.
- **OPEN RISK:** supply-loss sequencing and powered-off leakage at the host connector. M1 allows SDA/SCL absolute maxima independent of VS, but its leakage specification does not establish every unpowered mixed-supply condition. ALERT is limited to VS+0.3 V. Do not infer safe power-off behavior solely from I2C being open drain.
- **INTERFACE REQUIREMENT PROPOSAL:** host-facing I2C must be 3.3 V compatible, with known pull-up ownership and no back-power path in any host/module power combination. Select a bus isolation/buffer arrangement with explicit partial-power-down specifications or prove an equally valid circuit. Pull-ups tied to the host alone are not sufficient evidence. If monitor VS disappears during OVP cutoff, record the reset/data gap after recovery.
- **DECISION PROPOSAL:** disable automatic shunt temperature compensation initially. INA228 measures its die temperature; that is not necessarily shunt temperature. Characterize thermal coupling and actual signed TCR before enabling a positive-TCR correction model.

## Protection recommendation

**DECISION PROPOSAL:** separate input fault protection, converter current limiting, and independent load overvoltage disconnect. A catastrophic buck high-side short can put input voltage on the 5 V node without exceeding the input current limit. INA228 ALERT or a Linux command must not be the sole protective path.

| Option | Supported function | Assessment for this board |
|---|---|---|
| Input fuse + diode/reverse MOSFET + buck's internal limiting | Passive catastrophic-fault interruption; reverse-input protection if correctly implemented | Few parts, but fuse clearing, source fault current, inrush and fault energy need coordination. A fuse is not a precision 5 A output limiter; diode loss is material at low Vin. |
| TPS26630/31 + required external blocking NFET and pulldown transistor | Adjustable input current limit, UVLO/OV cutoff, controlled slew, reverse input/current protection | Leading input candidate for comparison. P1 operates at 4.5-60 V; 31 mΩ typical; current limit ±7%. Use cutoff variants, not a 35/39 V clamp variant simply because the family name matches. All resistor/FET choices remain OPEN. |
| LM74500-Q1 + NFET + separate fuse/current protection | Reverse input polarity | P2 explicitly does not block reverse current. Reject any diagram that labels this device alone as doing both. |
| LM74800-Q1 + back-to-back NFETs | Reverse-current blocking and independent OV load disconnect | Candidate output protection block, not final choice: operates at 3-65 V and can survive the proposed 28 V DC fault envelope with correctly rated FETs. It does not supply an adjustable overcurrent limiter. |
| TPS25982 output eFuse | Low-loss output eFuse with variant-dependent fixed OV behavior | Screened out for a 28 V buck-failure guarantee: its operating range is 2.7-24 V. Normal 5 V operation alone is insufficient selection evidence. |

**EVIDENCE (P1):** Fig. 8-7 needs Q1 and Q2 for reverse input/current protection. Omitting them and connecting IN_SYS to IN as Fig. 8-8 removes those functions. Review Q1 VDS/VGS/SOA and Q2 turn-off requirements; IC family capability is not complete-circuit capability.

**CALCULATION:** at 25.5 W, 9 V and an assumed 90% conversion efficiency, input current is `25.5/(9 × 0.9) = 3.148 A`; at 30.6 W it is 3.778 A. Internal eFuse conduction loss using 31 mΩ typical is approximately 0.307 W and 0.442 W respectively, excluding the external FET, temperature increase, auxiliary loads and startup. This is a sizing assumption, not measured efficiency. Nominal current limit must stay above maximum demand at its negative tolerance and below protected ratings at its positive tolerance. Do not simply set input limit equal to 5 A because output is 5 A.

**Output OVP unresolved:** P3's OV threshold is 1.195/1.231/1.267 V, roughly ±2.93% before divider/leakage errors. The specified OV deglitch can reach 5.4 µs for LM74800, followed by gate discharge and circuit response. It cannot automatically meet a hypothetical 5.10-5.25 V regulation/trip window. P1's adjustable cutoff is ±2%; using a second TPS26630/31 at 5 A would add about 0.775 W typical conduction loss and create further 6 A-limit headroom questions. Keep the output protection function in R1, but choose the actual controller only after load absolute limits, normal tolerance/transients and acceptable fault energy are fixed. Independent precision detection plus a rated disconnect may be required. This is an R2 entry blocker, not permission to omit OVP.

### Coordination and fault checks required before R2/R3

1. **OPEN:** actual source type, maximum fault current, lead length/inductance, allowed hot-plug, and required surge waveform/energy. No automotive or IEC compliance is claimed for this standalone board.
2. **TVS selection:** standoff must exceed maximum normal input including tolerance; maximum clamp at the actual pulse current plus wiring overshoot must remain below the protected-device ratings with margin. A nominal TVS voltage is not its maximum clamp voltage. Place suppression after a suitably coordinated input fuse; choose bidirectional behavior or an arrangement that does not deliberately short a reversed supply through an upstream unidirectional TVS. P1 pp. 37-38 describes interruption-induced input positive/output negative spikes.
3. **Fuse selection:** coordinate DC voltage rating, interrupt rating, cold/inrush behavior, temperature derating and I²t against TVS, connector/wire and downstream faults. Fuse/eFuse combination is defense against different faults, not a claim that either component is infallible.
4. **Capacitors:** pre-disconnect parts, including raw buck-output parts exposed to a high-side short, need a considered fault-voltage/energy rating. Input capacitors must withstand normal input and coordinated clamp; 35 V parts cannot be accepted for 28 V input without a transient/derating argument. After-disconnect components need a proven let-through envelope.
5. **Startup:** calculate `Iinrush = C dV/dt` for both board and attached load capacitance; check eFuse thermal limits/SOA, converter enable timing and retry interaction. Coordinate PGOOD with buck enable where suitable; make dummy-load startup independent of an SBC or host software.
6. **Fault modes:** reversed input; wrong positive adapter; input short/open; output short; load hot-plug; converter failure high; protection MOSFET short; supply collapse while output is externally energized; common-ground loss; unpowered host/module I2C. Single-source use does not establish immunity to accidental backfeed.
7. **Layout:** minimize input-protection current and gate loops; follow P1 Q1/Q2 placement and P3 package guidance. For P3, the exposed pad is specified floating, **not ground**; never infer thermal-pad connectivity from package appearance.
8. **Validation:** bench supply/current limiting, dummy load, scopes and thermal measurements must precede SBC integration. Demonstrate trip/restart limits, peak let-through voltage and energy, reverse leakage, shunt calibration, noise floor, counter rollover/reset handling and all I2C power combinations. No result in this audit replaces those measurements.

## Gate conclusion for integration

**R0 evidence:** monitor/EVM/protection sources and rights inspected; important reference figures checked visually; immutable local source copies available. **R1 recommendation:** INA228 with an output Kelvin shunt and protected local 3.3 V supply; input eFuse/reverse block with a separately justified output OVP path. **OPEN before final schematic:** accepted load voltage/peak profile, protection settings and source envelope, actual output OVP solution, I2C off-state isolation, connector ratings, thermal conditions, accuracy acceptance band and calibration method. All recommendations require manager approval within the R1 architecture review.
