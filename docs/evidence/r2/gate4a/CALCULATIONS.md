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

T04L requires actual-TS pump margin after R305 plus all external leakage and probe load. The non-bleed 5 µA qualification allocation needs ≥10.012531 µA pump capability at 10 V, in the actual circuit; the TS=20 V table point is not substituted.
