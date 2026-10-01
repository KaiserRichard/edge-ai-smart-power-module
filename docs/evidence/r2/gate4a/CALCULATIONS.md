# TASK 5 — Gate4a calculations

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Values are CALCULATED within explicitly ASSUMED/test-conditioned inputs. Unknown actual maxima are JSON `null` (OPEN), never zero. [Script](calculate_gate4a.py) reproduces [CALCULATIONS.json](CALCULATIONS.json); [raw-node analysis](RAW_NODE_ENERGY.md) explains topology, stress and the proposed fix. No frozen electrical value is silently replaced.

Reproduce: `python3 -B docs/evidence/r2/gate4a/calculate_gate4a.py --write`; optional `--plot` adds a standalone ideal-model SVG using matplotlib. `python3 -B -m unittest discover -s docs/evidence/r2/gate4a -p test_gate4a_calculations.py` checks energy conservation/derivatives, topology and artifact consistency.

|Selected-BOM path sensitivity|Loop mΩ|Far-end V at5 A|Margin to4.75 mV|
|---|---:|---:|---:|
|ASSUMED negative excursion 0 mV|41.855546|4.816866|66.866|
|ASSUMED negative excursion 20 mV|41.855546|4.796866|46.866|
|ASSUMED negative excursion 100 mV|41.855546|4.716866|-33.134|

`Vfar=Vraw_min−I·(Rsend+Rreturn)−Vnegative`. Keep BSC034 x2:25°C pair3.4mΩ/device maximum at10 V gate; hot2x resistance is ASSUMED. The imported lower-R pair6mΩ target is replaced by13.6mΩ. All other itemised wire/contact/shunt/copper allocations are retained in JSON. True source min/hot loop remain OPEN. Nominal5 A pair loss0.340 W; total path1.046389 W. At6 V gate using ASSUMED2x hot RDS, loop48.655546mΩ and far-end4.762866V after20mV: not a guaranteed lower-drive pass. Actual current sharing/contact ratings remain OPEN.

`Enew<=0.5 Cin_max Vin_max²+Vin_max Qsource+0.5 Ldiff_max I0²`; `I_L<=sqrt(2Enew/Ldiff_min)`; `Vraw_cap<=sqrt(Vraw0²+2Enew/Craw_min)`. Do not add the peak-current magnetic energy again: it is already inside Enew. The source ceiling is an ASSUMED boundary, not an OVP clamp.

|Input screen V|New energy mJ|L201 current bound A|Raw-cap bound V|
|---|---:|---:|---:|
|9.000000|2.499000|31.616451|5.685680|
|24.000000|11.424000|67.598817|6.304338|
|26.000000|13.124000|72.454123|6.415417|
|27.000000|14.019000|74.883910|6.473131|
|28.289211|15.217113|78.018236|6.549596|

Raw Cmin=2.4064mF (eight470µF ×0.8 initial ×0.8 additional assumed retention); ceramic minimum not credited. Cmax=5.59656mF, all raw initial energy upper=84.647970mJ. At highest source screen, raw terminal sensitivity with4mΩ/20mV is 6.881668V; extra local parasitic spike is OPEN. Maximum raw dump pool=99.865083mJ; the historical0.2J capacity target is withdrawn as a current claim; no hot part rating is established. Actual raw peak OPEN.

Proposed protected bank4×470µF: nominal1.88mF, assumed minimum1.2032mF/maximum2.7072mF. Published14mΩ20°C/100kHz per capacitor means3.5mΩ for four, versus the inherited0.5mΩ target; low-temperature/endurance row28mΩ gives7mΩ. These frequency-conditioned values do not bound edge ESR/ESL. Substitution into the legacy80 A/0.5µs/5.38V/20mV screen gives 5.713245V, not a PASS/prediction. Capacitor/harness topology must be recomputed. Initial protected energy upper=40.946400mJ. Including assumed2.2mF dummy gives an all-store subtotal174.086483mJ, before cable/other stores. Protected-arriving peak and Pi Cmax remain OPEN.

Historical5.325V OV latency counterexamples use an ideal maintained voltage,10µH/2.4064mF,8 A initial andzero ESR, not a qualified TPS26630 trajectory. They demonstrate why output OV propagation cannot be assumed to start at fault onset.

|Input V|Raw V after10µs|Time to nominal5.325V µs|
|---|---:|---:|
|9|5.139686|36.379761|
|24|5.170842|20.181617|
|26|5.174997|19.353955|
|27|5.177074|18.978433|

Aux static limited output=29.940620…31.643683V; buck-boost=11.621343…12.311325V. Hold screen=5.199100ms at300µF/11.2→10.5V/40mA/2.036µC; lower buck-boost minus0.5V diode gives4.609176ms. Nominal hold store31.68mJ, capacitor-only9ms average input0.488889A at9V/80% efficiency. Historical261k/113k supervisor screens=10.697782…11.255596V / 4.856669…5.107361V. Actual dynamic clamp/usable supply/hold remain OPEN.

Current sense: retain2mΩ ±1%,25ppm/K inherited shunt inputs. At5 A,10mV/50mW nominal; independent100°C/initial corners give maximum2.0237875mΩ,10.1189375mV/50.5946875mW. At80 A the nominal shunt screen is160mV/12.8W while it actually carries that current; pulse energy requires the measured integral and actual protected current can exceed L201 due to raw-bank bypass. INA228 full-scale ±163.84mV normal range (alternate ±40.96mV range) and input common-mode/absolute/pin limits must be checked at the fault and correct ADCRANGE. Normal full scale with2mΩ is81.92A or20.48A nominal, not a fault-survival guarantee. Kelvin force/sense, shunt tolerance/TCR/self-heating, monitor gain/offset/timebase/error and energy accuracy remain qualification items. Filter10Ω+10Ω/100nF gives79.577kHz; it is not the high-bandwidth fault current probe.

Normal input-current screens use25.491803W buck output/ASSUMED90% buck efficiency plus0.480W controls/ASSUMED80% aux efficiency; main input3.147136/1.180176/1.089393A at9/24/26V, before input dropout/unmodeled loads. Efficiency is not qualified. Inrush current is `C*dV/dt`; large raw/protected/dummy banks and series-FET charging require measured startup/current/SOA. Nominal10µH/400kHz ripple at9V is0.552555App, below the manufacturer nominal0.6A guidance; control-loop/stability/load-release/thermal/core-loss checks remain OPEN. Retain manufacturer reference-loop layout, low-current reference/Kelvin returns separate from disposal currents, dual VIN bypass, raw/protected/local stored-C accounting, connector/contact conditioning and copper/thermal targets from pinned PATH. Input current, efficiency, ripple/startup/inrush/transient/stability/protection/thermal limits are conditional calculations or OPEN. kicad ERC/DRC not rerun: no native schematic or PCB changes.

## Gate4a-FIX current screens

The sections above preserve the original energy/path screens, with the detector arithmetic corrected. Current circuit deltas, assumptions and remaining blockers are in [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md). Round-2 J502 solution A supersedes the historical harness; see the current selected-path table and round-2 section. This section is generated by [calculate_gate4a_fix.py](calculate_gate4a_fix.py). A numeric target is not a measurement.

|Item|Calculated value / status|
|---|---|
|R103 conservative58.1V power,0805|0.009724339584593669|
|R3052M bleed at10V maximum,A|5.012531328320802e-06|
|C3010.5µF/82nC event droop,V|0.164|
|Old loaded1M trip corrected,V|5.358574999999999|
|Old20mV raw increment,V|0.04286859999999999|
|Current OV-only latency at9/24/26/27V,s|[2.956487356739687e-05, 1.6912575964072873e-05, 1.6240793974457944e-05, 1.5935291252588232e-05]|
|New ideal trip,V|5.266699999999999|
|New conditional trip min/max,V|[5.219921610220708, 5.314621546439162]|
|New conditional20mV-overdrive upper,V|5.356873880264201|
|New supervisor held rail min/max,V|[10.224178614557356, 10.757090412124061]|
|New supervisorDET5 falling min/max,V|[4.343598238778056, 4.567313016917294]|
|New supervisorDET5 rising upper,V|4.704332407424813|
|Hold charging end-of-ramp input sensitivity,A|1.24|
|Raw99mΩ conditional peak current,A|70.46305404996032|
|Raw worst resistor energy,J|0.008606572034546716|
|Raw ideal discharge to0.3V,s|0.001759209196449833|
|Conditional protected current allowance3.5/7mΩ,A|[25.539140770928853, 13.48516094324397]|
|Measurement target Upeak/Umin,V|0.015|
|Source-off measured current ceiling with1%+2mA error,A|0.007920792079207921|
|Charge example uncertainty,C|1.6500000000000003e-06|
|Whole2ms charge example uncertainty,C|2.1550000000000002e-05|
|Energy partial error WITHOUT relative skew,J|0.0034948223999999996|
|Complete energy uncertainty (OPEN without measured skew),J|null|
|Aux-only pulse source energy screen,J|0.013540205000000003|

Detector equation: `Ip=Vs/R367+Ileak; Vdiv=Vs+(R303+Ron)Ip; Vraw=Vdiv(1+R301/R302)+R301Ip`. Corners enumerate four independently±0.25% resistors, Ron0…17Ω, inherited reference error0.12125%, comparator offset±4mV, **assumed** hysteresis±2mV, transferred PSRR/CMRR, additional R373 input-bias error±5.0125µV, and **assumed**1µA diode/PCB leakage plus125nA switch/comparator allowance. This conditional bound is not a guaranteed5.38V overdrive PASS; the missing hysteresis/dynamic/leakage transfer is T06.

Raw decay is ideal RC with maximum conditional bank and independent initial/tolerance plus TCR resistor corners; FET resistance, continued source current, harness coupling and hot resistance change the measured time. Timing minima/maxima, actual source bound, loadedVGS, clamp/negative peaks and calibration remain JSONnull. No computed conditional number fills them.

## Round 2 — completed connector handoff

Solution A is imported unchanged from connector commit `41cb9e8`. The owner-selected BSC034 pair retains its **assumed** 13.6 mΩ hot allocation; the connector report's alternative 6 mΩ pair and architecture E are not adopted. Previous path rows are retained under `historical_round1_selected_path` in JSON. J502 selection is complete; contact derating, splices and actual mixed mate remain T11/T16.

Current loop screen: 41.855546243 mΩ. At 5 A with a 20 mV trough: 4.796865523 V; with 100 mV: 4.716865523 V (FAIL screen). No hot assembly or Pi qualification is asserted.

## Round 2 — controlled hold charging

U327 TPS259470LRPWR follows D304 and drives DRV_HOLD. C374 1 µF / R374 100 Ω set a nominal 2 V/s ramp. T07D must demonstrate ≤10 V/s over all starts/restarts, ≤600 µF charged capacitance, ≤40 mA controls, and valid component temperatures. These are qualification allocations, not guaranteed startup specifications.

Aux input screen: 107.014375 mA at 7.5 V after branch loss and 75% efficiency, including 5 mA overhead; the transferred stopper floor is 135.014 mA at its datasheet test condition. The actual 9 V transfer and the converter's own local-capacitor startup remain T07A/C. U327 worst flat power sensitivity is 0.566321 W; with 85°C ambient and 74.5°C/W it gives 127.191°C, above the 125°C operating ceiling. Therefore the added charger requires local ambient ≤70°C for the initial coupon (112.191°C sensitivity), plus measured junction/board correlation; no hot PASS is inferred.

LT4363 TMR starts around 0.5 V in regulated operation: `tOC=C*(Voff−Vstart)/ITMR`. At 10 nF, 1.375 V and 310 µA, this is 28.226 µs, not the historical 43.065 µs zero-start screen. Initial timer voltage and stress-dependent charging are measured in T07; the old calculation remains explicitly historical.

## Round 2 — U317 RUN and compensation completion

F2-05 assigns the VC–FB and output–FB compensation branches. R345 changes from 464 kΩ to 383 kΩ because the old divider fails the declared 7.5 V low-line allocation with 3 µA adverse leakage.

Old/new conditional RUN rising ranges: [5.120075112219451, 8.531185263157894] / [4.428768896508728, 7.26186197368421] V. The 3 µA leakage ceiling must be qualified in T07E. Selected passive-network zeros are 10.610330 / 4.751603 kHz and the feedforward pole is 321.525138 kHz. These are network frequencies, not loop crossover or stability margins. Actual margins remain OPEN.

## Round 2 — coupled-bank energy and bootstrap measurements

F2-06 screens either dump against all initially connected output banks plus Enew. For effective dummy C≤2.2 mF, the conditional pool is 174.086483 mJ; one raw resistor receives at most 15.003120 mJ and one protected resistor 44.404903 mJ inside the fixed topology/tolerance model. These are separate worst allocations; do not add them as simultaneous dissipated energies. Missing fixture/cable stores and actual partition/SOA remain OPEN. A nominal 2.2 mF dummy at +20% raises the pool to 180.741483 mJ.

F2-10 adds 10 kOhm pulldowns at both AHCT inputs. The fully-off DC screen is 0.120300 V; the extra load is 0.681704 mA. This does not bound intermediate-rail behavior or input transition time. Both AHCT parts also require the existing TTL-high delta-ICC load in the 40 mA ledger.

T04L requires actual-TS pump margin after R305 plus all external leakage and probe load. The non-bleed 5 µA qualification allocation needs ≥10.012531 µA pump capability at 10 V, in the actual circuit; the TS=20 V table point is not substituted.

## Round 2 — passive fixture discharge adapters

F2-11/SFX-01 selects independent bleeders; resistor local ambient is limited to 70 C and review power to 0.125 W per 1206 part. These are external fixture limits. Rows assume separated capacitances and zero replenishment. Connected decay remains OPEN.

|Ref / node|R (ohm)|V screen|C ceiling (uF)|P upper (mW)|Isolated time to 0.3 V (s)|
|---|---:|---:|---:|---:|---:|
|RFD01 / VIN_PROTECTED|10000|28.289211|30.000|80.228517|1.367346|
|RFD02 / VOUT_5V1|1000|6.900000|5596.560|47.729323|17.591851|
|RFD03 / VOUT_PROTECTED|1000|6.900000|2707.200|47.729323|8.509631|
|RFD04 / FAR_5V|1000|6.900000|2640.000|47.729323|8.298399|
|RFD05 / DRV_HOLD|10000|12.311325|600.000|15.194859|22.342672|
|RFD06 / AUX_12V|10000|12.311325|26.000|15.194859|0.968182|
|RFD07 / AUX_PREHOLD|10000|12.311325|1.200|15.194859|0.044685|
|RFD08 / AUX_LIMITED|47000|35.000000|10.000|26.129153|2.242473|
|RFD09 / VIN_AUX|47000|58.100000|2.400|72.001493|0.595505|
|RFD10 / DET5|10000|5.250000|10.000|2.763158|0.286936|
|RFD11 / 3V3_AUX|10000|3.400000|10.000|1.158897|0.243382|
|RFD12 / REF_2V5|10000|2.525000|10.000|0.639160|0.213554|

Added held-domain current (DRV_HOLD and downstream LDO/reference bleeds): 2.354519 mA. Include it in the total control allocation; do not extend the old hold result unchanged. Converter-input/prehold bleeds are additional upstream loads. A far-end bleed returns only to FAR_GND and creates no local-ground bypass.

If all prior loads already use 40 mA, the PG and held-domain bleeds raise it to 43.036223 mA; the illustrative hold time falls to 4.283994 ms. This fails the existing total-current allocation; it must not be treated as an increased allowance. For normal-load bookkeeping, conservatively applying the two additional output bleeds at 5.5 V through the entire selected loop gives an extra 0.461565 mV drop and 4.796403959 V far-end sensitivity after the 20 mV trough. The far bleed is already included in the 5 A terminal load. Actual regulation/thermal margins remain OPEN.

## Round 2 — manufacturer-conditioned power-device screens

F2-12 reconfirms the BSC034 pair: 6.8 mOhm at 10 V gate, 10.2 mOhm at 6 V gate at the 25 C table points; 82 nC pair gate charge at the specified test point gives 0.164 V on a 0.5 uF effective bootstrap. No hot or actual gate-charge transfer is guaranteed by these values.

Q316 at separately qualified VDS<=58.1 V and ID<=0.20 A gives 11.62 W, 11.8524 mJ for 1.02 ms, and 91.1586 C bulk-junction sensitivity using fixed case85 C and 0.53 C/W. This is not a hot linear-SOA approval. Local input reservoirs can violate the branch-current target despite a 0.20 A source setting.

## Round 3 — source, interlock and external fixture screens

FIX3_SOURCE_TRIGGER.md and FIX3_INTERLOCK.md specify the circuits. These calculations allocate test limits; every physical result remains OPEN. The source interval applies only to a qualifying continuous high / input-collapse signature.

|Quantity|Conditional result|
|---|---|
|Source: SW_rise_V|[6.355354335821618, 6.900875120196956]|
|Source: SW_fall_V|[1.4351193277178904, 2.4942152560696638]|
|Source: qualifier_s|[3.7421509999999996e-06, 4.259151e-06]|
|Source: complete_conditional_interval_s|[0.0, 7.534151e-06]|
|Source: reserve_to_10us_s|2.465849000000001e-06|
|Source: useful_dump_allocation_s|6.1e-06|
|Source: node_C_allocation_F|1e-10|
|Source: actual_complete_interval_s|[null, null]|
|Source: actual_positive_charge_C|null|
|Source: internal_bridge_fault_coverage|null|
|Source: counterexample|{"SW_high_s": 3e-06, "SW_low_s": 1e-06, "VIN_V": 9.0, "qualification_trips": false, "classification": "Logic counterexample only; not a measured damaged buck"}|
|Interlock: threshold_intervals_V|{"SER_DRV": [10.667678103727713, 11.030524260180998], "DET5": [4.762118889789303, 4.916713547415094], "3V3_AUX": [3.086399570502431, 3.1819022696508554], "SAFE5": [4.599952504051864, 4.748828585050814], "DIAG_VIN": [3.6945235170178274, 3.81147087851691], "ZERO": [0.26691995571832067, 0.2782232138724906], "VIN_PROTECTED": [7.978418873581846, 8.246431967640005], "DRV_HOLD": [10.667678103727713, 11.030524260180998]}|
|Interlock: LDO_min_max_V|[4.934070090486847, 5.183488170923049]|
|Interlock: converter_min_max_V|[11.883849347858467, 12.593098582794244]|
|Interlock: SER_DRV_start_V|11.183849347858468|
|Interlock: aux_input_screen_A|0.12054307873031304|
|Interlock: charger_flat_power_W|0.6422480277225064|
|Interlock: charger_Tj_screen_C|117.84747806532673|
|Interlock: held_cap_screen_s|0.0045137512079453405|
|Interlock: driver_local_droop_V|0.043|
|Interlock: READY_s|[0.0970066649088, 0.10354928762880002]|
|Interlock: button_s|[0.0193379299328, 0.020642178252800004]|
|Interlock: release_recovery_s|[0.00099067264, 0.00105748864]|
|Interlock: diagnostic_feed|{"Rfeed_ohm": 470, "equivalent_load_min_ohm": 5285.513286954965, "healthy_VIN_min_V": 3.8588390461256465, "short_current_max_A": 0.011199611746792777, "feed_power_max_W": 0.058797961670662084}|
|Interlock: historical_4700ohm_feed|{"Rfeed_ohm": 4700, "equivalent_load_min_ohm": 5285.513286954965, "healthy_VIN_min_V": 1.9977012708303339, "short_current_max_A": 0.0011199611746792776, "feed_power_max_W": 0.005879796167066208}|
|Interlock: diagnostic_current_max_A|0.011199611746792777|
|Interlock: rejected_DC_path_below_ohm|305.03738704367674|
|Interlock: SHDN_off_screen_V|0.20052500000000004|
|Interlock: SHDN_on_screen_V|3.4528931455056884|
|Interlock: POR_0p8V_sink_screen_A|1.302105527008397e-05|
|Interlock: POR_4p75V_high_screen_V|4.21860875|
|Interlock: SAFE_input_start_V|9.623013|
|Interlock: SAFE_cap_hold_s|0.0022643831250000004|
|Interlock: fast_source_loss_allocation_s|3.2250000000000005e-06|
|Interlock: actual_loss_interval_s|[null, null]|
|Interlock: actual_hold_s|null|
|Interlock: actual_persistent_short_rejection|null|
|External fixture: classification|"External fixture design envelope; application qualification NOT RUN"|
|External fixture: limit_Rmin_ohm|2.22665625|
|External fixture: resistor_current_max_A|13.922220818772542|
|External fixture: resistor_power_each_W|107.89721134548721|
|External fixture: resistor_allowable_screen_W|200.0|
|External fixture: load_power_max_at_9V_source_W|9.09435392194013|
|External fixture: source_voltage_for_26V_5A_ideal_V|28.2786640625|
|External fixture: dead_timer_s|[1.8710754999999998e-06, 2.1295755e-06]|
|External fixture: abort_timer_s|[1.5255847999999998e-05, 1.6747848e-05]|
|External fixture: abort_complete_max_s|1.8772848000000002e-05|
|External fixture: abort_earliest_after_fault_s|1.26262725e-05|
|External fixture: hardware_abort_acceptance_s|2e-05|
|External fixture: added_energy_J|0.024031999999999998|
|External fixture: coupled_energy_J|0.18955637|
|External fixture: inductor_current_screen_A|98.04488767906258|
|External fixture: coupled_reverse_inductor_screen_A|275.3589439259237|
|External fixture: classification_100A|"First positive source-driven interval only; reverse/coupled current not capped by this allocation"|
|External fixture: raw_no_dump_peak_screen_V|7.5068472719058335|
|External fixture: force_FET_on_energy_each_J|0.00136|
|External fixture: source_FET_on_energy_each_J|2.6656e-05|
|External fixture: FET_overlap_energy_each_J|0.005|
|External fixture: contact_energy_each_J|4e-05|
|External fixture: actual_current_bound_A|null|
|External fixture: actual_abort_s|null|
|External fixture: actual_hot_SOA_margin|null|
|External fixture: actual_all_stores_discharged|null|
