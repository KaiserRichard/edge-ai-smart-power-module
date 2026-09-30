# TASK 5 — Gate4a calculations

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Values are CALCULATED within explicitly ASSUMED/test-conditioned inputs. Unknown actual maxima are JSON `null` (OPEN), never zero. [Script](calculate_gate4a.py) reproduces [CALCULATIONS.json](CALCULATIONS.json); [raw-node analysis](RAW_NODE_ENERGY.md) explains topology, stress and the proposed fix. No frozen electrical value is silently replaced.

Reproduce: `python3 -B docs/evidence/r2/gate4a/calculate_gate4a.py --write`; optional `--plot` adds a standalone ideal-model SVG using matplotlib. `python3 -B -m unittest discover -s docs/evidence/r2/gate4a -p test_gate4a_calculations.py` checks energy conservation/derivatives, topology and artifact consistency.

|Selected-BOM path sensitivity|Loop mΩ|Far-end V at5 A|Margin to4.75 mV|
|---|---:|---:|---:|
|ASSUMED negative excursion 0 mV|42.672941|4.812779|62.779|
|ASSUMED negative excursion 20 mV|42.672941|4.792779|42.779|
|ASSUMED negative excursion 100 mV|42.672941|4.712779|-37.221|

`Vfar=Vraw_min−I·(Rsend+Rreturn)−Vnegative`. Keep BSC034 x2:25°C pair3.4mΩ/device maximum at10 V gate; hot2x resistance is ASSUMED. The imported lower-R pair6mΩ target is replaced by13.6mΩ. All other itemised wire/contact/shunt/copper allocations are retained in JSON. True source min/hot loop remain OPEN. Nominal5 A pair loss0.340 W; total path1.066824 W. At6 V gate using ASSUMED2x hot RDS, loop49.472941mΩ and far-end4.758779V after20mV: not a guaranteed lower-drive pass. Actual current sharing/contact ratings remain OPEN.

`Enew<=0.5 Cin_max Vin_max²+Vin_max Qsource+0.5 Ldiff_max I0²`; `I_L<=sqrt(2Enew/Ldiff_min)`; `Vraw_cap<=sqrt(Vraw0²+2Enew/Craw_min)`. Do not add the peak-current magnetic energy again: it is already inside Enew. The source ceiling is an ASSUMED boundary, not an OVP clamp.

|Input screen V|New energy mJ|L201 current bound A|Raw-cap bound V|
|---|---:|---:|---:|
|9.000000|2.499000|31.616451|5.685680|
|24.000000|11.424000|67.598817|6.304338|
|26.000000|13.124000|72.454123|6.415417|
|27.000000|14.019000|74.883910|6.473131|
|28.289211|15.217113|78.018236|6.549596|

Raw Cmin=2.4064mF (eight470µF ×0.8 initial ×0.8 additional assumed retention); ceramic minimum not credited. Cmax=5.59656mF, all raw initial energy upper=84.647970mJ. At highest source screen, raw terminal sensitivity with4mΩ/20mV is 6.881668V; extra local parasitic spike is OPEN. Maximum raw dump pool=99.865083mJ; proposed0.2J hot capacity is a target, not a part rating. Actual raw peak OPEN.

Proposed protected bank4×470µF: nominal1.88mF, assumed minimum1.2032mF/maximum2.7072mF. Published14mΩ20°C/100kHz per capacitor means3.5mΩ for four, versus the inherited0.5mΩ target; low-temperature/endurance row28mΩ gives7mΩ. These frequency-conditioned values do not bound edge ESR/ESL. Substitution into the legacy80 A/0.5µs/5.38V/20mV screen gives 5.713245V, not a PASS/prediction. Capacitor/harness topology must be recomputed. Initial protected energy upper=40.946400mJ. Including assumed2.2mF dummy gives an all-store subtotal174.086483mJ, before cable/other stores. Protected-arriving peak and Pi Cmax remain OPEN.

OV latency counterexamples use an ideal maintained voltage,10µH/2.4064mF,8 A initial andzero ESR, not a qualified TPS26630 trajectory. They demonstrate why output OV propagation cannot be assumed to start at fault onset.

|Input V|Raw V after10µs|Time to nominal5.325V µs|
|---|---:|---:|
|9|5.139686|36.379761|
|24|5.170842|20.181617|
|26|5.174997|19.353955|
|27|5.177074|18.978433|

Aux static limited output=29.940620…31.643683V; buck-boost=11.621343…12.311325V. Hold screen=7.449100ms at300µF/11.0→10.0V/40mA/2.036µC; lower buck-boost minus0.5V diode gives8.359176ms. Nominal hold store31.68mJ, capacitor-only9ms average input0.488889A at9V/80% efficiency. Supervisor screens=10.224179…10.757090V / 4.540933…4.775024V. Actual dynamic clamp/usable supply/hold remain OPEN.

Current sense: retain2mΩ ±1%,25ppm/K inherited shunt inputs. At5 A,10mV/50mW nominal; independent100°C/initial corners give maximum2.0237875mΩ,10.1189375mV/50.5946875mW. At80 A the nominal shunt screen is160mV/12.8W while it actually carries that current; pulse energy requires the measured integral and actual protected current can exceed L201 due to raw-bank bypass. INA228 full-scale ±163.84mV normal range (alternate ±40.96mV range) and input common-mode/absolute/pin limits must be checked at the fault and correct ADCRANGE. Normal full scale with2mΩ is81.92A or20.48A nominal, not a fault-survival guarantee. Kelvin force/sense, shunt tolerance/TCR/self-heating, monitor gain/offset/timebase/error and energy accuracy remain qualification items. Filter10Ω+10Ω/100nF gives79.577kHz; it is not the high-bandwidth fault current probe.

Normal input-current screens use25.491803W buck output/ASSUMED90% buck efficiency plus0.480W controls/ASSUMED80% aux efficiency; main input3.147136/1.180176/1.089393A at9/24/26V, before input dropout/unmodeled loads. Efficiency is not qualified. Inrush current is `C*dV/dt`; large raw/protected/dummy banks and series-FET charging require measured startup/current/SOA. Nominal10µH/400kHz ripple at9V is0.552555App, below the manufacturer nominal0.6A guidance; control-loop/stability/load-release/thermal/core-loss checks remain OPEN. Retain manufacturer reference-loop layout, low-current reference/Kelvin returns separate from disposal currents, dual VIN bypass, raw/protected/local stored-C accounting, connector/contact conditioning and copper/thermal targets from pinned PATH. Input current, efficiency, ripple/startup/inrush/transient/stability/protection/thermal limits are conditional calculations or OPEN. kicad ERC/DRC not rerun: no native schematic or PCB changes.

## Current Gate4a-FIX decisions and worst-case screens

The preceding conditional energy/path models remain evidence, with any superseded component proposals identified below. These are paper calculations or named bench prerequisites; no test was run.

### R4A-01 — DESIGN BLOCKED / BENCH REQUIRED

WithSWdivider40.2k/10k,1kseries and82kpulldown,G=5.5714634146; REF1V25 gives6.964329268V nominalSWthreshold. DeclaredhotR±0.25%, REF±0.068%, derivedrefdivider±0.25%, comparatoroffset±4mV+1.25mVCMRRsensitivity, RON0…17Ω andspecifiedleakage screen6.875509…7.055127V, excludingdynamic/partial-supplyterms. Nominal9V source leaves≈1.945V beforemainpathdropandthresholdmax. At400kHz,normal9V/5.098Videalontime1.4162µs, notanallmodebound. LM61460allows98%duty in frequencyfoldback; nofullhealthymaximumONwidth ispublished. TimerNDIV1,RSET300k:6µs×(1±0.25%)×(1±6.2%)=5.61393…6.38793µs screen. AddingTPS1.5µs leaves2.11207µs foranalogsettling/comparator/OR/SHDN/physicalcommutation. Timerstartupis500×tMASTER≈3ms typical; require measuredreadybeforemainpermission, nottypicaldelayassumption. Qsource=integral(max(IMAIN,0)dt)≤100µC isindependentofdeadline andmustincludeallpositivework; moduleisolationdoesnotboundC/current.

Replace blankFAULT_TRIGGER with a concretecontinuous-SW-high watchdogcandidateU331TLV3201AIDBVR→U332LTC6994IS6-1#TRPBF,6µs rising-edge qualifier, independentofPG/outputOV. S01-07 specifies exactMPNs, values, sharedADGsparechannel, independentclamps andsourcefaultOR/Q304/U320connection. It isnot yeta proven discriminator; T01mustfirst boundhealthymaximumSW-high/startup/foldback andreadinessbeforethemainpathcanarm. KeeparchitectureD andTPS26630RGER; nofixturetimingclaim.

Closure: T01 SOURCE-WATCHDOG. Beforecapturefreeze, measurehealthySW-highmaximumat9/24/26V, allstartup/prebias/load/foldback/brownoutstates, plusobservedwatchdogminimum. PASShealthymax+Utime<watchdogmin−Utime withnofalsefault; readinessbeforemainpermission; everyphysicalfaultphase/sourcecorner gives tOFF+U≤10µs andQpositive+U≤100µC, includingpersistentfault/inputreturn. CannotclaimPASSwithmissinghealthybehaviororfixture. Measuringat0load/9V catches currentthresholdschemes thatotherwiseexceeddeadline; bulkOV19–36µs isretainedcounterevidence.

### R4A-02 — CORRECTED

Rmin=Rnom(1−0.001−25 ppm/K×60 K)=0.9975Rnom. At 58.1 V across R103, P≤9.724 mW. R340 at 12.311325 V: P≤0.151949 mW. R367 at 2.5 V: 6.266 µW. 0805 range ≤1 MΩ, working voltage 150 V, general-operation P70=140 mW; conditional 85°C linear derating toward125°C gives101.818 mW. Values unchanged, initial-only OVP26.973873–28.289211 V / aux11.621343–12.311325 V screens retained; pads/parasitic transfer is not assumed unchanged.

R103 = TNPW0805348KBEEA (348 kΩ) VIN_FUSED→U101 OVP with R104 15.8 kΩ to GND; R340 = TNPW08051M00BEEA (1 MΩ) AUX_12V→U317 FB; R367 initially same 0805 1 MΩ SENSE→GND, revised under R4A-06. 0.1%, 25 ppm/K; replace 0603 lands at capture.

Closure: T07 OVP/hot divider; T06 detector settling; T07 converter loop before power qualification. These test actual board parasitics, not resistor existence.

### R4A-03 — CORRECTED / BENCH REQUIRED

At 3V3_AUX floor3.2 V and measured total PG leakage≤10µA: VHIGH≥3.2−10µA×10.025k=3.09975 V, margin1.09975 V to2.0 V. At AUXmax3.4 V, PG low≤0.4 V requires sink0.300752 mA. At DET5≤5.5 V,220k minimum219.45k consumes25.06µA; total output load must remain≤50µA for the 4.4 V minimum high at4.5 V table condition. LVC threshold≤0.7×5.5=3.85 V gives0.55 V conditional static margin. The 8 mA hot VOH3.8 V table is not the25°C3.94 V value and is not credited to this low-load bound. AHCT has no output Ioff guarantee; partial-power outputs cannot enforce fail-off. Inputs may be high with VCC=0 within their stated leakage/rating test conditions; same-rail receivers and passiveSHDN enforce containment.

Replace unsupported U319 dual-DCU proposal with separate U319/U324 SN74AHCT1G125DBVR buffers. Five-pin DBV circuit, pullups, 220 kΩ output pulldowns and100 nF local bypass are explicit in S03-05; existing SUPPLY_OK and BUCK_PGOOD receiver nets must pass through these outputs. No dual footprint reuse.

Closure: T03 BUFFER-SEQUENCING. PASS only with no source/series conduction before valid rails plus freshARM; no DET5 backfeed>0.3 V; every pin remains within ratings. Measures unspecified partial-power behavior under passive shutdown; does not replace the R4A-15 policy implementation.

### R4A-04 — CORRECTED / BENCH REQUIRED

At10 V,220k requires45.455µA versus15µA minimum pump atTS20V/10V differential table point. 2.2M nominal requires4.545µA; at12V andRmin2.1945M,5.469µA. Residual15−5.469=9.531µA is a test-point leakage budget only. At actualTS≈5V andDRV_HOLD≈11V, D302 cannot replenishBST≈15V; no TS5V pump minimum is provided. C cannot cure steady DC loss. With82nC/10V effective gate capacitance, passiveτ≈18.04ms; activeTGDN must establish fault cutoff. Hot leakage/full gate charge remain OPEN.

R305 = TNPW12102M20BEEA,2.2 MΩ,0.1%/25ppm/K,1210, common PROT_GATE→PROT_MID source. Remove220 kΩ proposal. Retain LTC7001IMSE#PBF and BAS116,215 D302; C301 assigned under R4A-05. 2.2M requires1210 because1206 ends at2MΩ.

Closure: T04 BOOTSTRAP-DC-HOLD. PASS measuredVGS−U≥10V under lowestDRV_HOLD andTS4.75…5.5V,0/5A,25°C/hot,10-minute settled hold; no continuing downwardBST/VGS trend. Repeat after input removal through disposal; verify physical series-off in T08. Measurement closes TS5V pump/leakage not guaranteed by theTS20V table.

### R4A-05 — CORRECTED / BENCH REQUIRED

Qpair published test maximum82nC gives Ceff≥82nC/0.25V=328nF; declared measured floor330nF yields ΔV≤0.248485V at that charge. Additional leakage/driver charge is measured, not hidden in82nC.50V rating exceeds12V bootstrap differential/2.5Vreference, not a dynamic differential proof. MLCC effective-C and REF50 loop stability depend on bias/temperature/ESR; nominal1µF cannot guarantee either.

C301 = GRM21BR71H105KA12L1µF50V0805X7R: PROT_BST(U301.9)→PROT_MID(U301.8). C302 = same1µF50V part REF_2V5(U302.6)→GND. R31231.9k,R31310k retained; D302BAS116,215 anodeDRV_HOLD,cathodePROT_BST,NC pad2. Do not assign reference bypass asbootstrap.

Closure: T05 BOOT-CAP-REFERENCE: C301 effective≥330nF at measuredBST−TS/temperature, actual gate-event droop≤0.25V whileVGS−U≥10V; C302 stable/reference within completeT06threshold budget. T04DCbudget still mandatory. Measurement closes bias and real charge/stability; refdes itself is closed by exportednet connectivity.

### R4A-06 — CORRECTED / BENCH REQUIRED

HistoricalG=1+1k/1M+(11.3k/10k)(1+1k/1M)+11.3k/1M=2.14343: Vtrip5.358575V;20mVraw42.8686mV. RevisedG=2.1327317073: trip5.331829268V,overdrive42.654634mV. Declared25→85°Cscreen±0.25%R,REF±0.068%,Vos±4mV,test-conditionedRon0…17Ω,120nAonleak+5nAinput and80nAclamp-diode leakage gives5.303164…5.361687V, excluding unboundedhysteresis/load/PSRR/dynamicterms. Switchoff3µA×R367max82.205k=0.246615V before bias/capacitiveinjection, versus3.0075V for1M. Partial-powered16Vfaultleak38µA gives3.12379V beforeclamps; staticoffmath is notpartial-powerproof. AtDRV_HOLD10.5V/shunt2.5175V,R361max82.205k provides97.1µA>80µA minimum. Atconditionalraw6.881668V,DIVclamp≤3.5175V with1Vdiode allocation, availableclampcurrent≈0.339mA plusbias. ThediodeVF/negativeinput response still requiremeasuredcorners; operation below−0.2V is not credited.58.1V is aux-only: if itreachesraw,R301power≈0.303W exceeds0603 and mainbuck/caps fail their input envelope.

Correct the historical1k/1M loaded trip to5.358575V andraw20mV overdrive42.8686mV. Replace that network withR3019.88k,R30210k,R3031k,R36782k; R36182k independentshunt bias, D322BAT46W negativeDIVclamp. ExactMPNs/pins inS03-02/03. U321 powered byDET5; enableDET5_VALID; unused pins defined. D301feeds independentLM4040 ground-return shunt, neverREF50.

Closure: T06 DETECTOR-PARTIAL-POWER. PASS revisedloadedtrip is bounded andnohealthyfalsefault; atpoweroffeach comparatorpin≥−0.3V and≤VCC+0.3V designguard, injection within ratings andnoDET5backfeed>0.3V; reference/clampcurrentswithinratings; comparator atmin validrail meetsT08 andfar-endT10. If partial-power clamp transient fails, redesign before capture/release. Measurement closescapacitance, diodeknee/negativecommutation andramps not specified by static tables.

### R4A-07 — BENCH REQUIRED

Clamp29.940620…31.643683V,12Vscreen11.621343…12.311325V retainstated±0.25%R anddatasheetbias. Supervisorcorners10.224179…10.757090V /4.540933…4.775024V leave0.224179V/0.040933V above declaredvalidfloors beforedelay/droop. At40mA/300µF,driverdroop100µs=13.333mV; actualDETload/C andsupervisorresponsemax remainOPEN. Hold=(300µF×1V−2.036µC)/40mA=7.4491ms conditional, notqualified. Buck-boostlow−assumed0.5Vdiode=11.121343V meets11V targetconditionally. Holdcapenergy31.68mJ; 9mschargeinputaverage488.889mA alone violatesnominal151.515mAlimit. With9V/80%/151.515mA and0.480Wload, availablechargepower0.610909W givesnominalminimum51.857ms beforeotherloads/losses. NewC350floor0.75µF×1.335V/310µA=3.229839ms at thehigh-stresstablepoint; lowstress13µA gives77.019ms. These are timer sensitivities, notallstartupguarantees. At58.1/31.644V/177.533mA,Q316instantaneousloss≈4.697W; hottime/SOA mustmatchobservedTMR/inrush. Retrying intoUVLO orlatchtrip isnotPASS.

Keep upstream LT4363HMS-1#PBF/FDB33N25TM0.33Ωsense andLTC3115IFE-1#PBF12V block. C350 becomes verifiedGRM21BR71H105KA12L1µF50V TMR→GND. Retain100k/4.32k clamp and1M0805/90.9k converterFB. Replace supervisor dividers withU322249k/10k andU323105k/10k. D304B260/2×EEU-FR1E221 hold targets arestart≥11V, Ceff≥300µF,totalcontrol≤40mA, DRVfloor10V/DETfloor4.5V; VGS≥10V independently.

Closure: T07 AUX-START-HOLD. PASS9/24/26V cold/hot startupwithouttimertrip/UVLOoscillation, settledrails validwithmainU101OFF, loadedbootstrapT04, usablehold≥1ms ANDlongerthanactualT09disposal+uncertainty; invalidrails removepermissionbeforefloorscross andneverrearmpersistentfault. T14qualifiesauxpulseindependently. Measurement isrightclosurefor coupledsoftstart,currentlimit,timer,hotSOA,diodeloss andcompletecontrolcharge notspecifiedbyblockdatasheets.

### R4A-08 — BENCH REQUIRED

tCB=tanalogthreshold+settling/overdrive+tcmp+tlogic/latch+tUCC+tgate/usefulclamp; tSER=tanalogthreshold+settling/overdrive+tcmp+tRUN+tLTC+tgate/commutation; tSRC=twatchdoganalog+6µsqualifier+tOR+SHDNcross+tTPS+sourcecommutation. Datasheetpartialmax93.3ns/134.2ns usesoldload/supplycondition; newOR/latch/drive mustbeincluded. Revised20mVsenseoverdrive requires42.654634mVraw, notzerotime. WithprotectedCmin1.2032mF,80A,3.5mΩ,staticscreen5.361687V,20mVring, allowableCBdelay C*(5.5−Vbase−I*ESR−ring)/I=−2.431776µs evenbeforeoverdrive; inherited0.5µs/0.75µs allocations arewithdrawn. At5.38Vbase/0.5µs legacycandidatecase remains5.713245V. Completephysicalmin/max remainOPEN/OPEN; no zero minimuminferred.

Freeze B02measurement endpoints: actualfaultonsett0→usefulraw/protectedcrowbarcurrent/clamp, physicalseriescurrentinterruption, physicalmain-sourcecurrentoff. RetainU303TLV3201,U301LTC7001,U315/U330UCC27511 andupdatedwatchdog/rails/pincontract. No93.3ns/134.2ns partialsum iscalledsystemmaximum; minima/maxima remainOPENuntilT08.

Closure: T08 COMPLETE-B02. PASSallapplicablevalidrail/temp/load/PWMphasecornersproduce recordedboundedmin/max tophysicalendpoints; source tOFF+Ut≤10µs/Q++UQ≤100µC; eachcrowbar/seriestrajectory plusuncertainty satisfiesstrictT10far-endpeak andcomponentSOA/T09. Abenchmin/max recordqualifiesonlytestedconditions; missingcoverage/instrumentclipping isINCONCLUSIVE. Measurementisnecessaryforanalogoverdrive, gatecharge/plateau, partialrails andcurrentcommutation, notjustlogicpropagation.

### R4A-09 — BENCH REQUIRED / RATINGS BLOCKED

Enew≤½30µF×28.289211²+28.289211×100µC+½12µH×8²=15.217113mJ. Rawinitial½5.59656mF×5.5²=84.647970mJ; rawdump99.865083mJ. Cmin2.4064mF: Vcap≤6.549596V; ESR4mΩ/ring20mV sensitivity6.881668V, notqualifiedpeak. Original33mΩ wouldgive6.881668/(.033×.99)=210.642A initialscreen; revised66mΩ gives105.321A beforeotherresistance. WorstRC.066×1.01×5.59656mF=373.067µs; idealdecayto0.5V≈978.184µs; residual~80.557A at100µs. Equalsharingenergy12.483135mJperresistor isnotboundwithtolerances/strayreturns; measuredEj=integral(ij²Rjdt). CSD400Apulseheadline applies≤100µs/≤1%duty/25°C; package100AcontinuousandactualhotSOA mustcoverlongtail.0.2J remainsdesignreserve targetonly. D10250A8.3mshalf-sinespec doesnotqualify78A/shortcommutationbyitself. Noavalanchecredited. RawFBscreen6.881668/(1+100/24.4)=1.349845V; actualfeedforward/negativepinspikesOPEN.

UseQ330CSD18540Q5B/U330UCC27511DBVR for independentrawdump. Increase itsballastfrom33mΩ to66mΩ usingeightselectedWFMB2512R0330FEA (twofour-resistorstringsparallel);1ΩgateR384/10kbleedR385. D330B260-13-F anodeGND/cathoderawprovidesdefinedlocalnegative/strayreturn; retainD102B260VIN_PROTECTEDnegativecommutation withactualwaveformqualification. ProtectedQ303/33mΩdisposesdownstreamenergyseparately. Exactraw-pin exposuresremainlisted.

Closure: T09 TWO-NODE-ENERGY-COMMUTATION. PASSactualenergybalance/destinationswithinuncertainty; allMOSFET/diode/resistorwaveformsinsideapplicablehotSOA/pulse/current/thermalratings; ballastbeforepulse≤85°C andtotalterminal<95°C; raw/protected/dummyV≤0.5V andILwithinmeasuredsafezero by≥1msdesignwindow orrecalculatehold. No electrolyticreversevoltagecredited; everyrawVIN/SW/BOOT/FB/sense/pinabsolute/operatinglimitmusthold. Missinghotratingspreventsfull-stressenergization; useboundedlowenergyfirst. Measurebecauseparasiticloops,sharing,commutationandpulseheatcannotbeprovenbytotaljoules.

### R4A-10 — BENCH REQUIRED

Cnom4×470=1880µF; initial±20%withadditionalassumed0.8/1.2 retention givesCmin1203.2µF,Cmax2707.2µF.14mΩcatalogESR/4=3.5mΩat20°C/100kHz;28mΩrow/4=7mΩ.80A/0.5µs/5.38V/20mVlegacy sensitivity=5.713245V; astatic80A×3.5mΩ jumpalone=0.28V. RawbankcanbypassL201beforepaircutoff, so78.018A Lbounddoesnotboundprotectedarrivingcurrent. Initialprotectedenergy40.9464mJ and2.2mFdummy33.275mJ; raw/new subtotal99.865083mJ givesall-store174.086483mJ beforecable/otherstores. Historicalfar-end5.542140Vexceeds5.5by42.140mV andisnotexcluded. Normal42.672941mΩ conditionalpathgives4.792779Vafter20mVtrough; 100mVtroughcase4.712779Vfailsby37.221mV. ActualC/ESR/ESL/R/Vreg/loadresponse remainOPEN.

SelectC340…343PCH1V471MCL1GS470µF35V,positiveprotectednode/negativeGND, solelyasmeasuredtest-boardcandidate. Explicitlywithdrawinherited≤1.5mF/≤0.5mΩclaim and0.5µscontainmentallocation; retainrawbankupstream. KeepDpair/localregulation/shunt. Acceptorrejectcandidateonlywithactualrawbank-arrivingcurrent, series/dumpactionsandrealharness/far-endtrajectoryT10; changingCwithoutESR/currentproof isnotclosure.

Closure: T10 PROTECTED-BANK-HARNESS. PASSeveryT01/T08/T09autonomousfaultcorner maxfullbandfar-end+Upeak<5.5V includingboth5Vcontacts/loadedreturn, allcutoff/ringing/tail/recovery; normal5Amin−Umin≥4.75Vat9/24/26V, withcomponentstressacceptance. MeasureIseries/IPROTindependentlyofILandactualC/ESR/loopR. Failureoroverlaprejectscandidate; collectallcounterexamples. Measurementisthecorrectclosurebecausemulti-nodecap/harness/currentredistribution cannotbeprovedwithL201-onlybound orcatalogESR.

### R4A-11 — CORRECTED / BENCH REQUIRED

8503manufacturerDCR16.2Ω/1000ft=.0531496063Ω/mnominal. Declared20°Creference,60°Cfactor1+.00393×40=1.1572 and±10%screen givesmaxsend0.015×.0531496063×1.1572×1.1/2=0.507438mΩ; return0.035×same/8=0.296005mΩ. ThismatchesimportedAWG22model; nomDCRisnotmanufacturerworstcase. For5Awithtwo positivebranchesRhigh/Rlow≤1.5,Imax=5×1.5/(1+1.5)=3A; openbranchforces5Aonremainingpin andisnotpermitted. Wire8503rating−40…105°C/600Vrms doesnotestablishcontact/housinghot3A/faultpulseorbundledampacity. Belden8521lower80°C/housing85°C/shunt-reference85°C stillgovernlocalfixturetemperatures.

ReplaceincorrectBelden8529AWG22description withBelden8503,22AWG7×30strandedtinnedcopperPVCfanout. RetainBelden8521AWG16trunks, HarwinM20-118004222–30AWGcontacts andtwohousings.75mmtrunks; positivefanouts15mm×2,return35mm×8. AWG16neverentersM20contact; connectviareviewedsplice. J502 remainsPENDINGseparatejob.

Closure: T11 HARNESS-CRIMP-SHARING. PASScorrect22AWGwire/insulationdiameter/approvedcrimptool/pulltest; fullhotloopR andpercontactcurrentinsidequalifiedratings; bothpositives/all8grounds intact,Ipositive≤rated3Acase andimbalance≤1.5 when3Ascreencredited; localtemperaturesbelowwire/housing/contactlimits. T10strictfar-endrails stillgovern. Measurementcloses actualmate/crimp/hotresistance/sharing; wiregaugecompatibilityitselfisclosedbydatasheets.

### R4A-12 — DESIGN BLOCKED / BENCH REQUIRED

5mm×3mm×1mmcopperlinkusingrho20=1.724e−8Ωm gives28.733µΩ; at78.018A,0.1749Wbeforejoint/hotloss,5A0.718mW. ActualstrayL/rating/jointheat measurednotinferredfromcopper. LocalCin≤30µFat28.289V stores12.004192mJ; raw/protected/dummyall-store174.086483mJ conditionalalreadyexceedsbench-supplycurrentlimitprotectionassumption. Isolatedcontrolbootstrap1µFat12V stores72µJ; measure/controltomaincouplingandincludeanydeliveredwork, notsilentlyoutsideenergybudget. Ifsource6A persists50µsat26V,extra7.8mJ; anyabortdeadlinechangesfaultenergyallocation andmustbeinratedfixturebeforetest. FixtureopeningmustnotrescueDUTPASS. ENlow/preisolated/syntheticPG casesremainseparatecharacterization.

Selectfault-portmodewithU201SWphysicallyisolatedfromL201byremovedJP201beforepower; QF1BSC034N06NSATMA1 bridgesVIN_PROTECTED→L201_SW_FORCE, UF1LTC7001isolated12Vdrive/1µFBSTcap/1Ωgate/2.2M1210bleed. Initialraw/protectedbanksareprechargedwithaboundedtemporarysource thenisolated;actualFB andactualBUCK_PG/ARM/RUNmustbeobservedvalidatt0,neverforciblyoverridden. ThisexercisesactualL201/source/DprotectionwhileexcludinginternalLSshoot-through. JP201/202boltedCu-linkconstructionandforce/senseplanes defined. Abort/prechargetransfercontrols, rateddisconnectMPNs andwhole-sourceenergyremainOPEN; thereforefullyexecutablefixtureisnotclaimedfrozen.

Closure: T12 ARMED-FAULT-PORT-ABORT. Beforeanyfullmatrix: capture/source/precharge/injector/abortcircuit&BOM review withhotSOA/energybounds, thenlowenergysequencingmeasurement. PASSactualPG/RUN/pairarmedatt0, prechargecurrentzeroandisolationverified, internalU201SWdisconnectedfromL201/VINfaultpath, allfixtureparasitics/C counted; injectorconduction/norescue/currentdisposalmonitored; forcedDUTfailuretriggersindependentabortwithinitsreviewedhotSOA/energy anddischargesallbanks. Missingaborthardware/ratingsisDESIGNBLOCKED, notsolvedbyatestplan. Measurementclosesobservedinitialstate, parasiticsandabortbehavioronlyafterconstruction exists.
