# Task 2 input ledger

2026-09-29. **CALCULATED screening only. SPICE and vendor models NOT RUN.
Sheet 03 OPEN; R2/R3 BLOCKED; NOT FOR FABRICATION.**

The `baseline` profile retains the historical numerical values; the `reviewed`
profile applies only values supported by the committed Task 1 review. Historical
2026-09-26 evidence is unchanged. The full labelled ledger is also embedded in
both result JSON files and the SPICE manifest. Identifiers/counts are metadata.

## Source-driven changes

- KNOWN LM74800 OV deglitch is 5.4 µs maximum (3.98 µs typical). Its endpoint is
  HGATE falling; adding a charge quotient still does not prove isolation.
- KNOWN TPS26630 direct-table limits at the captured resistor are 4.185/4.5/4.815 A.
  CALCULATED conditional external ±0.1% resistor scaling gives 4.180819–4.819820 A.
  The historical equation-based 4.1664–4.7936 A comparison is retained separately.
- KNOWN eFuse full-temperature resistance maximum is 53 mΩ; the old 34.5 mΩ
  maximum is only at 25 °C. Neither makes instantaneous current limiting valid.
- KNOWN opposing HGATE source maximum is 75 µA. ASSUMED 96 nC charge divided by
  KNOWN 168 mA sink is CALCULATED 0.571429 µs, without a guaranteed gate waveform.
  The source-current maximum informs the candidate budget, not this ideal switch.
- UNKNOWN Coilcraft, TDK and Nexperia replacements remain missing. Retain and label
  the old saturation, effective-capacitance, hot-resistance and charge assumptions.
  Do not substitute the eFuse typical fast-trip comparator level as a current cap.
- KNOWN user requirement is load ≤5.5 V with explicit margin. The historical
  6.0 V duration remains only a comparison output. No new architecture is selected.

## Reviewed INPUTS

Values below use SI units unless the key gives another unit. Each label applies
only as qualified by its source: known device rows do not make their simplified
application a guaranteed model. Bulk values are **effective** bank values, not
purchasable nominal values. Static fault initial voltage is nominal, not a sweep
of regulation tolerance; the 32-corner matrix is the requested historical matrix,
not an exhaustive electrical corner set.

| Input | Value | Label | Source / limitation |
| --- | --- | --- | --- |
| `vin_source_max_V` | `24.72` | ASSUMED | GST60A24 24 V x 1.03 tolerance, Mean Well GST60A spec |
| `efuse_iol_nom_A` | `4.5` | KNOWN | TI TPS2663 SLVSE94G p7 typical at RILIM=4.02 kOhm; direct table basis |
| `efuse_iol_tol` | `0.07` | KNOWN | TI TPS2663 SLVSE94G p7: 4.185/4.5/4.815 A MIN/TYP/MAX; excludes external resistor tolerance |
| `efuse_ron_ohm` | `0.053` | KNOWN | TI TPS2663 SLVSE94G p7 maximum -40 to +125 C at 0.6 to 6 A; 34.5 mOhm is 25 C only |
| `buck_hs_rdson_ohm` | `0.041` | ASSUMED | Intact LM61460 SNVSBD5D p6 typical is 41 mOhm; failed-short resistance UNKNOWN; retained comparison value |
| `L_nom_H` | `6.8e-06` | KNOWN | Inherited XAL8080-682 nominal from captured BOM; no fresh Coilcraft tolerance/saturation verification |
| `L_dcr_max_ohm` | `0.0146` | CALCULATED | back-calculated from calculate_r2.py max-DCR copper loss |
| `L_isat_A` | `14.0` | ASSUMED | saturation knee not verified (Coilcraft drawing download failed) |
| `L_sat_ratio` | `0.7` | ASSUMED | inductance above knee, soft-saturation screen |
| `vraw_static_V` | `(5.038271401729418, 5.098360655737705, 5.158632237795172)` | CALCULATED | calculate_r2.py |
| `cin_eff_F` | `(1.5e-05, 4e-05)` | ASSUMED | 2x22 uF X7R at 24 V; DC-bias minimum OPEN (CAPACITOR_QUALIFICATION.md) |
| `craw_eff_F` | `(6e-05, 0.00013)` | ASSUMED | 6x22 uF X7R at 5.1 V; nominal 132 uF, bias/aging minimum OPEN |
| `fet_rds_hot_ohm` | `0.00325` | ASSUMED | Inherited PSMN1R8-40YLC hot resistance; Nexperia primary download HTTP 403, condition/maxima unverified |
| `shunt_ohm` | `0.002` | KNOWN | WSL27262L000FEA |
| `ideal_diode_off_s` | `8.75e-07` | ASSUMED | Known SNOSD95C p6 tDGATE_OFF max uses 10 nF and +30 to -100 mV step; applying to path current is ASSUMED |
| `lm74800_ov_deglitch_s` | `5.4e-06` | KNOWN | TI SNOSD95C p7 visually confirmed MAX; ends at HGATE falling, not full isolation |
| `lm74800_en_off_max_s` | `6e-06` | KNOWN | TI SNOSD95C p7 MAX HGATE deglitch; ends at HGATE falling, not full isolation |
| `hgate_discharge_s` | `5.714285714285714e-07` | CALCULATED | ASSUMED Qg=96 nC / KNOWN sink minimum 168 mA; charge quotient only, not worst-case isolation |
| `lm74800_trip_worst_high_V` | `5.7936` | CALCULATED | 348k/97.6k 0.1 % divider, VOVR 1.267 V max |
| `precision_trip_worst_high_V` | `5.5` | ASSUMED | target for a +/-1.1 % precision detector; parts OPEN |
| `precision_trip_with_bulk_worst_high_V` | `5.46` | ASSUMED | 5.40 V nominal +/-1.1 %, usable only with bulk |
| `precision_detect_s` | `3e-07` | ASSUMED | fast comparator + driver; parts OPEN |
| `crowbar_ohm` | `0.01` | ASSUMED | crowbar switch + copper |
| `crowbar_loop_H` | `1e-08` | ASSUMED | crowbar loop inductance incl. MLCC ESL; layout OPEN |
| `fast_gate_off_s` | `1e-07` | ASSUMED | discrete gate pull-down of Q302; circuit OPEN |
| `bulk_esr_ohm` | `0.02` | ASSUMED | hybrid-polymer class bank ESR |
| `load_current_corners_A` | `(0.3, 5.0)` | ASSUMED | 2026-09-26 PROTECTION_ANALYSIS.md section 2; actual load envelope OPEN |
| `load_capacitance_corners_F` | `(2e-06, 0.00022)` | ASSUMED | 2026-09-26 REQUIREMENT_ENVELOPE_PROPOSED.md L6; actual Pi network UNKNOWN |
| `bulk_capacitance_corners_F` | `(0.0, 0.00047, 0.001)` | ASSUMED | Historical comparison values; effective bank minima not qualified; OPTION_I_CANDIDATES.md |
| `load_rolloff_voltage_V` | `1.0` | ASSUMED | Numerical constant-current load becomes conductance below this voltage; not a Pi load model |
| `load_screen_levels_V` | `(5.5, 6.0)` | ASSUMED | Historical reporting thresholds retained for comparison; current user limit is separately labelled load_fault_limit_V |
| `load_fault_limit_V` | `5.5` | KNOWN | User REQUIREMENT in BRIEF_02_AMENDMENT_1.md (2026-09-29); replaces 6 V screen and requires explicit margin |
| `integration_step_s` | `2e-09` | ASSUMED | Historical Euler integration step; numerical setting, not device timing |
| `fault_duration_s` | `0.00012` | ASSUMED | Historical fault observation interval; cannot establish indefinite fault hold |
| `release_inductance_scales` | `(0.8, 1.0, 1.2)` | ASSUMED | Inherited +/-20% screen; Coilcraft primary download blocked |
| `release_peak_currents_A` | `(5.0, 6.139)` | ASSUMED | Historical release envelope; 6.139 A inherited ripple estimate, not measured peak |
| `startup_soft_start_s` | `(0.0035, 0.007)` | ASSUMED | Uses LM61460 tSS limits as a linear full-output ramp; actual endpoint is 90% reference |
| `startup_input_V` | `9.0` | ASSUMED | Proposed minimum operating corner; REQUIREMENT_ENVELOPE_PROPOSED.md S1b |
| `startup_load_A` | `5.0` | ASSUMED | Proposed continuous load; REQUIREMENT_ENVELOPE_PROPOSED.md L2 |
| `startup_efficiency` | `0.88` | ASSUMED | Historical efficiency estimate at startup; no converter control/efficiency model |
| `startup_current_limit_fraction` | `0.9` | ASSUMED | Brief criterion 5 proposed input-current margin |
| `q302_gate_charge_C` | `9.6e-08` | ASSUMED | Nexperia primary download HTTP 403; inherited charge, maximum and test conditions UNKNOWN |
| `hgate_sink_min_A` | `0.168` | KNOWN | TI LM7480-Q1 SNOSD95C p6 minimum sink under specified conditions; not a constant waveform |
| `hgate_source_max_A` | `7.5e-05` | KNOWN | TI LM7480-Q1 SNOSD95C p6 maximum; Task 1 visual primary-source review |
| `precision_isolation_sensitivity_s` | `2e-06` | ASSUMED | Brief criterion 3 proposed worst-case allocation, not demonstrated circuit delay |
| `efuse_ilim_resistor_tol` | `0.001` | KNOWN | Captured R105 specified +/-0.1%; TPS2663_SOURCE_REVIEW.md tolerance screen |
| `efuse_iol_max_A` | `4.81981981981982` | CALCULATED | SLVSE94G p7 4.815 A / (1 - 0.001), conditional inverse-resistance scaling; not a new guaranteed row |
| `efuse_iol_min_A` | `4.180819180819181` | CALCULATED | SLVSE94G p7 4.185 A / (1 + 0.001), conditional inverse-resistance scaling; not a new guaranteed row |
