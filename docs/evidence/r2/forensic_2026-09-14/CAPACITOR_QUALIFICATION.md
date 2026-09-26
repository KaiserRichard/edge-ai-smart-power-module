# C5750X7R1H226M250KB electrical qualification

2026-09-14. **OPEN - no guaranteed effective-capacitance release.**

**KNOWN:** [TDK exact product record](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C5750X7R1H226M250KB), accessed 2026-09-14, specifies 22 uF +/-20%, 50 VDC, X7R (+/-15% temperature class), -55..125 C, dissipation factor <=5%, reflow, commercial grade. Dimensions and footprint disposition are in [critical footprints](CRITICAL_FOOTPRINT_QUALIFICATION.md). Product page has no fixed revision; source identity/retrieval limitations are in [register](qualification_source_register.json).

| Location | Applied voltage | Nominal bank | Electrical disposition |
| --- | --- | --- | --- |
| C201/C202, buck input | Approximately protected input, normal 9..24 V; not exactly connector voltage | 2 x 22 = 44 uF | Effective C at 9/12/24 V OPEN; highest normal bias needs explicit evaluation |
| C209-C214, raw buck output | Approximately 5.1 V normal; potentially upstream voltage during buck failure | 6 x 22 = 132 uF | Effective C at 5.1 V OPEN; high-voltage fault C(V) also OPEN for let-through model |
| C404, TPS709 3V3_LOCAL output | Approximately 3.3 V while enabled | 22 uF plus separately specified bypasses | Effective C at 3.3 V OPEN; this is not a 5.1 V capacitor location |

**EVIDENCE limitation:** the official [characterization PDF](https://product.tdk.com/info/en/documents/chara_sheet/C5750X7R1H226M250KB.pdf) and current TDK charasheet path failed direct retrieval again (403); web access did not yield readable plotted data. The older local `third_party/documents/r2/TDK_C5750X7R1H226M250KB_mirror.pdf`, dated 19-Mar-2019, remains historical reference with incomplete original-mirror provenance. It suggests material loss at 24 V and smaller loss at 5.1 V, but cannot establish a guaranteed minimum. TDK expressly describes public characteristic graphs as reference data, not guaranteed product characteristics. No new numeric bias factor is assigned.

**CALCULATION, tolerance alone:** one part spans 17.6..26.4 uF at its specified initial test conditions; two nominal parts total 35.2..52.8 uF and six 105.6..158.4 uF. These are not DC-biased/aged/temperature-combined bounds. X7R's +/-15% classification is not proof that bias and temperature multipliers are separable. No numeric aging rate was found for this exact part.

**DECISION on existing buck evidence:** preserve `r2_calculations.json` and `BUCK_DESIGN.md` as dated calculations. Their factors 0.65 input bias and 0.95 output bias remain **ASSUMED screening inputs**; calling them conservative does not establish a lower bound. Consequently 19.448 uF input, 85.272 uF output, 13.83 mV ripple and protection calculations using that C must not be promoted to qualified results. This paragraph supersedes any stronger interpretation of those values. No schematic capacitance or MPN changed.

**CALCULATED ripple-current demand:** ideal-buck input-bank RMS `Iout*sqrt(D*(1-D))` is 2.478/2.472/2.045 A at 9/12/24 V and peaks at 2.5 A near half duty. Equal sharing would be about 1.25 A per input MLCC, but actual sharing depends on the two switching loops and impedance. Output-bank RMS `deltaI/sqrt(12)` reaches about 0.658 A using the existing assumed 2.278 A worst ripple. This is current demand, not the capacitor's allowable current. The 5% dissipation-factor specification cannot be treated as ESR at 400 kHz; no exact ripple-current or allowed self-heating curve was obtained. Compute heat with frequency-dependent ESR and harmonics after those data are available.

**OPEN to close:** official exact-part DC-bias CSV/model or readable curve at 3.3, 5.1, 9, 12 and 24 V; measurement frequency/amplitude and temperature; production spread or defensible design margin; combined bias/temperature behavior; aging/time since de-aging; ESR/impedance versus frequency and self-heating limits. Typical data can support a labelled design estimate, but a minimum needs a tolerance basis or manufacturer guidance. No need to invent numeric values while these inputs are missing.

**Acceptance procedure:** check effective input C against TI's local decoupling requirements and effective output C against stability/transient design across the approved operating envelope. Check TPS709's effective 1.5..47 uF output range and ESR requirement including all local bypasses. Later R5 tests use dummy loads, cold/hot operation and measured ripple/step response; failure symptoms are oscillation, excessive droop/ringing or MLCC heating. No capacitor is electrically validated by this review.
