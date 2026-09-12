# V1A power calculations and measurement plan

Date: 2026-09-11. Baseline: `a9fe716` plus the uncommitted R0/R1 package. All results below are **CALCULATION**, not hardware measurements. Inputs are **PROPOSED/ASSUMPTION**, not approved requirements.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Screening inputs and source trail

Use 5.00 V/5 A for the main example, 6 A only for a peak-load question, and 9/12/19/24 V for input screening. Historical 5.10 V and 28 V examples remain alternatives. Equations follow basic circuit relations and TPS56837 datasheet §7.2.2; sensor scaling follows INA228 §8.1.2. Exact revisions and local caches are in the [audit](01_REFERENCE_AUDIT.md). These calculations were recomputed in Python during this mission; the reproduction check below requires only the standard library.

## Power, efficiency and input current

`Pout = Vout × Iout`; `Iin = Pout / (Vin × η)`; `Ploss = Pout × (1/η − 1)`.

5.00 V/5 A gives 25 W; 5.10 V/5 A gives 25.5 W. At 5.00 V/6 A the output is 30 W, but the allowed duration is OPEN. Assuming **90% whole-module efficiency**:

| Vin | Input current at 25 W | Input current at 30 W |
| --- | ---: | ---: |
| 9 V | 3.086 A | 3.704 A |
| 12 V | 2.315 A | 2.778 A |
| 19 V | 1.462 A | 1.754 A |
| 24 V | 1.157 A | 1.389 A |

This whole-module assumption includes auxiliary losses; if using converter-only efficiency, add auxiliary/input-protection demand separately. Input current limit cannot be selected equal to the desired output current without this conversion. With ±7% limit tolerance, require `Ilimit_nom × 0.93 > Iin_required_max` while `Ilimit_nom × 1.07` remains within protected ratings and fault policy. Startup and source foldback can impose a stricter condition.

At 25 W output, 85/90/95% whole-module efficiency means 4.412/2.778/1.316 W loss respectively. These are thermal-budget scenarios, not predicted efficiency.

## Buck ripple and component stress

For an ideal CCM buck, `D ≈ Vout/Vin`, `ΔIL = Vout(1−D)/(L fsw)`, `IL_peak = Iout + ΔIL/2`, `IL_rms = sqrt(Iout² + ΔIL²/12)`.

Using the **reference** 3.3 µH and 500 kHz at 5 V:

| Vin | Duty | ΔIL peak-to-peak | IL peak at 5-A load | IL peak at 6-A load |
| --- | ---: | ---: | ---: | ---: |
| 9 V | 0.556 | 1.347 A | 5.673 A | 6.673 A |
| 12 V | 0.417 | 1.768 A | 5.884 A | 6.884 A |
| 19 V | 0.263 | 2.233 A | 6.116 A | 7.116 A |
| 24 V | 0.208 | 2.399 A | 6.199 A | 7.199 A |

At 24 V/5 A, IL_rms ≈5.048 A. With −20% inductance and −10% frequency **illustrative tolerances**, ripple rises to 3.332 A and peak current to 6.666 A; a 6-A load reaches 7.666 A. Final calculations must use selected component/controller limits and saturation under fault current, not just this nominal table.

Input-capacitor RMS screening: `Icin_rms ≈ Iout sqrt(D(1−D))`, reaching approximately 2.5 A near 50% duty for a 5-A load. Check MLCC bias/temperature capacitance and ripple/temperature ratings. Output ripple first-order estimate: `ΔV ≈ ΔIL/(8 fsw Ceff) + ΔIL × ESR`. For Ceff=35 µF and ESR=2 mΩ at the 24-V point, the estimate is approximately **21.9 mV**. It excludes switching spikes, control-mode transitions and layout parasitics and cannot establish the proposed 50-mV acceptance limit.

TPS56837's EVM reports 94.96% at 24 V/5 V/5 A and 40-mV ripple at 8 A. Its datasheet/EVM use particular layout, LC and measurement conditions. Do not compare those observations with another device's different load point as measured improvement.

## Loss and thermal screening

Conduction-only estimate for an integrated synchronous stage: `PFET ≈ Iout²[RHS D + RLS(1−D)]`, ignoring ripple, temperature and switching losses. Using the datasheet typical resistances at 24 V → 5 V/5 A gives approximately 0.294 W for TPS56837 and 0.373 W for TPS56637. This explains a candidate advantage but is **not** a total-loss or measured-efficiency comparison.

For an asynchronous stage, `Pdiode ≈ VF × Iout × (1−D)`. Assuming VF=0.5 V at 24 V → 5 V/5 A gives **1.98 W** in the catch diode alone. Actual VF, leakage, thermal resistance and switching losses require its datasheet; this is a reason not to adopt Sailor Hat's RT6365 block blindly.

Use `Tj ≈ Ta + Pdevice × θeffective` only with an appropriate board/airflow thermal model. Datasheet θJA is tied to a reference test board and is not a universal constant. At Ta=50°C, a candidate 125°C junction ceiling allows 75°C rise; an assumed 1.5-W device loss would require θeffective ≤50°C/W. Whole-board loss must not all be assigned to one IC. Verify component temperatures with documented emissivity/thermocouple method, thermal equilibrium and actual copper/airflow.

## Distribution, protection and startup

`Vload = Vregulated − I × Rpath`, where Rpath includes both supply and return copper, connectors, wiring, shunt and output switches. For an **assumed** 4.75-V load floor and exact 5.00-V source, the total nominal budget at 5 A is 50 mΩ; at exact 5.10 V it is 70 mΩ. Regulation tolerance/transients consume this margin before allocating copper or connectors. A 2-mΩ shunt uses 10 mV/50 mW at 5 A.

Copper resistance screening: `R = ρ l/(w t)` with ρ≈1.72×10⁻⁸ Ω·m at 20°C. An illustrative 50-mm × 5-mm × 35-µm trace is approximately 4.91 mΩ. Equal outgoing/return traces total 9.83 mΩ, dropping 49 mV and dissipating 0.246 W at 5 A. This estimates resistance only; **it is not a current-capacity rating**. Neckdowns, vias, finish/plating, temperature and heat spreading require actual geometry and thermal/current verification.

Startup demand: `Icap = Cload × dV/dt`. An illustrative 1000 µF charged to 5 V in 2 ms requires 2.5 A in addition to any active load. Stored energy is 12.5 mJ. Load capacitance is OPEN; source current limiting and buck/eFuse retries may interact. Review switch `∫VDS I dt` and pulsed/DC SOA, not just energy in the load capacitor.

Output OVP must satisfy `Vnormal_max < Vtrip_min` and `Vtrip_max + transient_letthrough < Vload_fault_allowable`, with any time-dependent load damage limits included. LM74800's approximately ±2.93% OV comparator threshold tolerance alone is about ±0.15 V around 5.1 V before divider and delay errors; a narrow 5.10–5.25-V assumption cannot be accepted without closing that budget. No OVP threshold is selected here.

## Shunt range and loss

`Vshunt = I Rshunt`; `Pshunt = I² Rshunt`; `Ianalog_FS = Vshunt_FS/Rshunt`.

| Candidate | At 0.1 A: drop / loss | At 5 A: drop / loss | At 6 A: drop / loss | Analog range at ±40.96 mV |
| --- | --- | --- | --- | --- |
| 1 mΩ | 0.1 mV / 0.01 mW | 5 mV / 25 mW | 6 mV / 36 mW | ±40.96 A |
| 2 mΩ | 0.2 mV / 0.02 mW | 10 mV / 50 mW | 12 mV / 72 mW | ±20.48 A |
| 5 mΩ | 0.5 mV / 0.05 mW | 25 mV / 125 mW | 30 mV / 180 mW | ±8.192 A |

The wider ±163.84-mV setting multiplies nominal analog range by four. This does not permit those currents through the board or guarantee the programmed CURRENT register can represent them. At 5 mΩ, 10 A produces 50 mV and clips the lower analog range; peak and fault-reporting requirements matter.

WSL2726 candidate family: ±1% tolerance; 3-W P70 rating depends on pad temperature and substrate; component TCR ±75 ppm/°C at 1 mΩ, ±25 ppm/°C at 2–5 mΩ. For +50°C, the corresponding resistance drift bounds are 0.375% or 0.125%. Do not substitute the lower alloy-only TCR. Kelvin terminals remove load-pad resistance from the measurement only if routed correctly.

At the INA228's specified conditions, ±1-µV input offset corresponds to ±1/0.5/0.2 mA for 1/2/5 mΩ. With 2 mΩ, a first-order uncalibrated budget is approximately `1.05% of reading + 0.5 mA` (1% shunt +0.05% gain +offset), before noise, thermal EMF and temperature. At 5 A this is about 1.06%; at 0.1 A about 1.55%. Four-wire shunt calibration and instrument uncertainty are needed for a tighter system claim.

VBUS senses the load-side shunt node; the reported power excludes shunt/converter losses and upstream local loads. If V1B later supplies the load through another branch, this monitor alone may not measure total load energy. Freeze the measurement boundary at joint interface review.

## INA228 scaling example

For the **candidate** 2-mΩ shunt, ADCRANGE=1 and a chosen digital full scale of 10 A:

```text
CURRENT_LSB = 10 / 2^19 = 19.073486328125 µA
SHUNT_CAL = 4 × 13107.2e6 × CURRENT_LSB × 0.002 = 2000
POWER_LSB = 3.2 × CURRENT_LSB = 61.03515625 µW
ENERGY_LSB = 16 × POWER_LSB = 0.0009765625 J
CHARGE_LSB = CURRENT_LSB C
```

Digital positive current full scale is just below 10 A, despite ±20.48-A analog headroom. ENERGY is unsigned 40-bit; CHARGE is signed 40-bit. Continuous conversion is required for valid energy accumulation. Read diagnostic flags in the correct order, handle rollover and configuration reset, and report missing energy intervals. These values are not firmware, an approved logger format or a bidirectional net-energy guarantee.

## Future hold-up equation only

For future V1B/V2 review, `Eusable = ½ Ceff(Vhigh²−Vlow²)` and `Eusable × η ≥ ∫Pload(t)dt`, with ESR drop, aging, imbalance and temperature reserves. `tcharge ≈ C ΔV/Icharge` is only a constant-current idealization. **All V1A–V1B interface values and hold-up duration remain TBD.** No capacitor bank, charger or balancing circuit is designed here.

## Reproduction and later measurements

Run from the repository root; expected output is the nominal 24-V screening point and PASS:

```sh
python3 - <<'PY'
from math import isclose, sqrt
vout, vin, load, inductance, frequency = 5.0, 24.0, 5.0, 3.3e-6, 500e3
ripple = vout * (1 - vout / vin) / (inductance * frequency)
peak = load + ripple / 2
assert isclose(ripple, 2.398989898989899)
assert isclose(peak, 6.19949494949495)
for resistance in (0.001, 0.002, 0.005):
    print(resistance, load * resistance, load**2 * resistance, 0.04096 / resistance)
lsb = 10 / 2**19
assert isclose(4 * 13107.2e6 * lsb * 0.002, 2000)
print(f'ripple={ripple:.3f} A, peak={peak:.3f} A, rms={sqrt(load**2+ripple**2/12):.3f} A; PASS')
PY
```

Failure symptoms: unit-conversion or expected-value mismatch. Passing this arithmetic check establishes neither model completeness nor board performance.

Later bench experiments must record goal/hypothesis, hardware, software/firmware versions if used, input/load/cable, config and commands, raw voltage/current/power/ripple/temperature/transient/fault data, interpretation, limitations, reproduction steps and project commit plus dirty-tree patch where applicable. Measure input and output simultaneously at explicit connector boundaries. No performance result in this document is a V1A measurement, and no new experiment format is imposed.
