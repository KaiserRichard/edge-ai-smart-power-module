# Gate4a-FIX independent auxiliary branch

**BENCH REQUIRED; package BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** This supersedes tentativeauxvalues in[historicalreviewedproposal](history/931e369/AUX_BRANCH_FIX.md). The58.1Vconditionisoneboundedauxpulsedevelopmentcase inT14; sustained58.1V isnotanapprovednormalinputrequirement.

DECISION: VIN_FUSED→D303BAT46W→Q316FDB33N25TM→R3320.33Ω→AUX_LIMITED→LTC3115-1nominal12V→D304B260→DRV_HOLD. HeldrailfeedsLTC7001/twoUCC27511, DET5TPS7A16 and3V3_AUXTPS709. MainU101OFF leaves thisbranch supplied. WholeinputlossorLT4363-1latchedoff leaves onlyqualifiedholdenergy. NoPG/output/hostpowerdependency. Theisolated48→24Vmoduleupstream isownerfixed; exactmodule/envelope remainsOPEN.

Theexactrefdes/MPN/value/net contractisS03-11…15/17; calculationstoR4A-07 arein[resolutiontable](REVIEW_RESOLUTIONS.md) and[CALCULATIONS](CALCULATIONS.md). C3501µF50V replacedunsupported10nFcode. Supervisordividers249k/10k driverand105k/10k detectorreplace261k/113k choiceswhich couldrejecthealthysupplies. U317RUNtiesAUX_LIMITEDpermanufacturerhighvoltageRUN guidance, not10VdemoUVLO; switchingstagePVCC/VCC staytheinternal4.45Vrail andmustnotconnectto12V. U306IN/ENbothDRV_HOLD; U307DNP.

CALCULATION: limiter29.940620–31.643683V staticscreen; qualificationceiling35V, not40Voperatinglimit. Converter11.621343–12.311325V staticscreen. Driverfall10.224179–10.757090V, detector4.540933–4.775024V; floor10V/4.5V, loadedseriesVGS≥10Vseparately. WithCeff300µF,start11V,40mAcontrol,and2.036µCgatecharge, usableholdscreen7.4491ms. Eachpremise isT07/T04qualificationtarget, notmeasured.

Startupcannotuse9msassumption:440µF stores31.68mJ at12V; chargingaloneaverages488.889mA inputover9ms at9V/80%, before40mAcontrols. Nominalstopperlimit151.515mA impliesatleast51.857mschargewiththedeclaredload. C350effectivefloor0.75µF gives3.229839ms highstresstimerscreen and77.019ms lowstress13µA screen. Actualtimercurrent,VDS,tolerance, softstartinteractionandSOA determinewhetherstartupworks; T07 ismandatorybeforeARM. Noarbitrarytimerextensionrelease.

T07 measures main-eFuse-off, aux-stopper-off andtotalinputloss separately. T14 usesanindependentlyboundedaux-onlyfixtureat58.1V; mainbuckmustneverbeexposedaspartofthatbranchtest. T04/T05verify loadedbootstrapandbias. R4A-15completepin/statecontractandT15brownout-raceproof precede anyclaimofcapturefreeze. TPS3808's20µs responseistypical; useactualmaximumplusuncertainty, notapaperdeadline.

EVIDENCE: ADILT4363RevC, LTC3115-1RevEp38,andTITPS3808SBVS050N; sourceprovenanceinSOURCES.md. NoKiCad/benchwork.
