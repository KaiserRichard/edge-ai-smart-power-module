# Raw-side ratings and candidate detector interfaces

Date: 2026-09-29. Task 4 candidate-interface evidence; no circuit selection or schematic change. Sheet 03 remains electrically OPEN; R2 and R3 remain BLOCKED. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Evidence and scope

**KNOWN — captured connectivity:** This review reads the archived [qualified netlist](../forensic_2026-09-14/V1A_qualified.net.xml), exact repository path `docs/evidence/r2/forensic_2026-09-14/V1A_qualified.net.xml`. It distinguishes a component's recorded rating from a rating independently verified in an available primary source. A netlist rating annotation is not itself manufacturer qualification. Reference designators, net numbers, page numbers, dates, document identifiers and source line locations are identifiers rather than electrical quantities.

**KNOWN — primary sources:** Texas Instruments [LM61460, SNVSBD5D, May 2019, revised July 2022](../../../../third_party/documents/r2_protection/lm61460.pdf), especially printed pages 4, 7–8 and 15–16; [LM7480-Q1, SNOSD95C, April 2020, revised December 2020](../../../../third_party/documents/r2_protection/lm7480.pdf), especially printed pages 3–7; and [TPS2663, SLVSE94G, September 2018, revised June 2024](../../../../third_party/documents/r2_protection/tps2663.pdf), especially printed pages 24–25 and 28. URLs, hashes, revisions and use/attribution records are in the [source register](source_register.json). These sources are referenced only; upstream files and circuits are unchanged. TI copyright applies. Related reviews: [buck/TVS](BUCK_TVS_SOURCE_REVIEW.md), [TPS2663](TPS2663_SOURCE_REVIEW.md), and [LM7480 primary-source extraction](PRIMARY_SOURCE_REVIEW.md).

**ASSUMED — screening envelope:** raw-side steady source voltage after a persistent buck high-side short is screened at **24.72 V** and the historical eFuse overvoltage screening point of **28.3 V**. The latter is a **CALCULATED historical threshold estimate**, not a guaranteed ceiling on the raw node. TPS2663 overvoltage timing ends at its fault flag; input ringing, let-through and internal buck failure behavior remain **UNKNOWN**. Passing a static rating comparison at these values does not close the transient requirement.

## Captured raw-side connections

**KNOWN — connectivity:** `/VOUT_5V1`, net 35 at netlist line 2731, connects only C207, C209–C214, L201 pin 2, R202 pin 1 and TP301. It has no connection through Sheet 03 to `/VOUT_PROTECTED`. The latter is net 36 at line 2743 and includes U402 pin 1, C403, R401 force input and TP302.

| Item | Evidence label and electrical screen | Consequence |
| --- | --- | --- |
| C209–C214 | **KNOWN — captured annotation:** each is C5750X7R1H226M250KB, nominal **22 µF**, **±20%**, **50 V**. **UNKNOWN — independent Task 1 confirmation:** the requested TDK characterization source was blocked. | Their annotated voltage class exceeds the screening voltages. Effective capacitance versus voltage/temperature/aging and physical qualification remain OPEN. Do not promote the annotations to a new primary-source verification. |
| C207 | **KNOWN — captured annotation:** CGA3E2C0G1H220J080AA, **22 pF**, **±5%**, **50 V**; in series with R205. | Nominal static voltage-class screen is compatible. Its feedforward path exposes FB to fast edges; see the separate calculation below. Exact component confirmation remains OPEN in this brief. |
| L201 | **KNOWN — captured annotation:** XAL8080-682MED, **6.8 µH**, with **60 V** in its rating field. **UNKNOWN — primary verification:** Coilcraft download was blocked. | Do not claim a manufacturer-verified winding/terminal voltage or fault-current capability from the annotation. Saturation, current and thermal qualifications remain OPEN. |
| R202/R203 | **KNOWN — captured values:** **100 kΩ / 24.4 kΩ**, each **0.1%**, **0.1 W**, **50 V**, with exact MPNs OPEN. **CALCULATED:** at raw **28.3 V**, R202 dissipates **5.175 mW**, R203 **1.263 mW**. | Static voltage/power screen is below the annotations; exact part ratings, temperature derating and transient behavior still require confirmation. |
| R205 | **KNOWN — captured value:** **1 kΩ**, **1%**, **0.1 W**, **50 V**, exact MPN OPEN. | Part of the feedforward path; its transient current and pulse stress depend on the raw waveform. |
| U201 FB | **KNOWN — primary source:** FB-to-ground absolute maximum **16 V** (SNVSBD5D p. 4). **CALCULATED — nominal divider only:** FB is **4.8486 V** at raw **24.72 V**, and **5.5508 V** at raw **28.3 V**. | Static divider screen is below the absolute maximum. This is not a guarantee of converter behavior or FB transient survival after internal failure. |
| U201 BIAS | **KNOWN — primary source:** BIAS-to-ground absolute maximum **16 V**. **KNOWN — connectivity:** U201 pin 1 is on `/GND`, netlist line 2685. | The captured circuit avoids exposing BIAS directly to the faulted raw rail. Do not infer the typical application's BIAS-to-output connection. |
| U201 PGOOD | **KNOWN — primary source:** PGOOD-to-ground absolute maximum **20 V** (p. 4). **KNOWN — connectivity:** U201 pin 5 is NC, netlist line 2773. | A future pullup directly to raw is incompatible with the held-fault screening voltages. Use a reviewed bounded supply/domain. This is a proposed-interface hazard, not an existing netlist error. |
| U201 VIN / SW / bootstrap | **KNOWN — primary source:** VIN absolute maximum **42 V**, recommended maximum **36 V**; SW maximum **VIN + 0.3 V**; CBOOT−SW and RBOOT−SW maximum **5.5 V** (p. 4). | The failed high-side connects the input/SW/inductor system. These pin-specific limits, ringing and low-side shoot-through require separate transient review; a VIN rating is not a blanket rating for every pin. |
| C205 / C206 | **KNOWN — captured annotations:** both rated **16 V**; C205 is **100 nF** between bootstrap and SW, C206 is **1 µF** on VCC. | Their stress is differential/local, not raw-to-ground. Primary source gives VCC maximum **5.5 V** and bootstrap differential maximum **5.5 V**. Exact capacitor MPNs and behavior during internal buck failure remain OPEN. |
| TP301 | **KNOWN — connectivity:** exposed access to raw. **UNKNOWN:** final physical test-point rating and enclosure/probe arrangement. | Must be treated as a source-voltage node after a fault. |

**CALCULATED — divider formulas:** with `Rt = R202`, `Rb = R203`, and raw voltage `Vr`, `Vfb = Vr × Rb/(Rt + Rb)`, `P_R202 = (Vr − Vfb)²/Rt`, and `P_R203 = Vfb²/Rb`. Values above use nominal resistances, ignore FB loading and presume intact divider components. They are static component-stress calculations, not a guarantee that an internally failed converter preserves its original input-pin behavior.

## Feedforward transient sensitivity

**KNOWN — connectivity and nominal values:** netlist lines 2562–2571 show C207 between raw and `BUCK_FF`, R205 between `BUCK_FF` and `BUCK_FB`, R202 between raw and FB, and R203 between FB and ground. **KNOWN — captured values:** `Cff = 22 pF`, `Rf = 1 kΩ`, `Rt = 100 kΩ`, `Rb = 24.4 kΩ`.

**CALCULATED — ideal linear network:** ignoring FB input capacitance/current/clamps, the transfer from raw to FB is

```text
H(s) = [Rb/(Rt + Rb)] × [1 + s Cff (Rt + Rf)]
                         / [1 + s Cff (Rf + (Rt || Rb))]

H(0)   = Rb/(Rt + Rb)
H(∞)   = Rb/[Rb + (Rt || Rf)]
tau    = Cff × [Rf + (Rt || Rb)]
Vfb(0+) = Vfb(0−) + H(∞) × [Vr(0+) − Vr(0−)]
```

**CALCULATED:** the nominal high-frequency gain is approximately **0.9610** and `tau` approximately **0.454 µs**. For an **ASSUMED instantaneous** raw step from the **CALCULATED nominal 5.09836 V** operating point to **ASSUMED 28.3 V**, with initial **CALCULATED FB = 1 V**, the ideal initial FB response is approximately **23.30 V**. This exceeds the **KNOWN 16 V** FB absolute maximum in that deliberately idealized fast-edge case.

**UNKNOWN — actual exposure:** This is not a prediction that the high-side-short event produces that step. The input/output capacitance and inductor constrain the fault waveform; parasitic capacitance, finite edge speed, pin loading and clamps also change the response. Conversely, local ringing and internal failure can invalidate a simple ramp approximation. The example shows why DC division alone cannot establish FB pin survival. Check the actual FB waveform using the captured feedforward branch and a supported pin model, then physical fault testing. Do not add or select a clamp based solely on this illustrative calculation.

## Independent detector supply and startup interlock

**KNOWN — captured supply:** U402 is TPS70933DBVR, SOT-23-5, with repository annotation **30 V** input and **3.3 V** nominal output. Its cited source is TI SBVS186H, but that document is not in the available primary-source archive. **UNKNOWN:** independently confirmed startup, UVLO, transient, thermal and output-validity limits for a new detector-supply implementation.

**KNOWN — connectivity:** U402.IN is on `/VOUT_PROTECTED`, not raw, and its output supplies `/04_POWER_MONITOR/3V3_LOCAL`. **INFERRED:** using that existing rail for the independent detector creates a startup dependency on the power path it must first authorize and can remove detector/latch power after isolation. Task 4 therefore needs a separate, reviewed detector supply; reuse of the part number does not mean reuse of this downstream instance or domain.

**KNOWN — connectivity:** `/BUCK_INPUT_PGOOD` is U101.PGOOD to U201.EN/SYNC at netlist lines 2644–2648. It is not the currently unconnected U201 output-regulation PGOOD. A future `BUCK_PGOOD` signal must be identified explicitly.

**KNOWN — LM61460 timing:** SNVSBD5D pp. 7–8 specifies a PGOOD rising delay of **1.5 / 2 / 2.5 ms MIN/TYP/MAX** and a falling glitch-filter time of **120 µs typical**, with no maximum in that row. Pages 15–16 explain that brief excursions do not force PGOOD low and that PGOOD can be invalid at sufficiently low input. **INFERRED:** PGOOD cannot substitute for the independent fast detector, establish reference settlement, or guarantee behavior of a converter whose power stage has failed.

**PROPOSED logic requirement — not a selected circuit:** path enable requires `buck_good AND detector_supply_valid AND reference_valid AND NOT fault_latched`. An invalid/unpowered detector must leave the path off. Verify startup order, brownout, prebiased external load, logic backpower and fault-input/reset priority. Merely adding an AND gate without defined power-off behavior does not close this requirement.

## Proposed comparator, latch and gate-stage interfaces

**CALCULATED — comparator input exposure:** a divider that produces an **ASSUMED 1.25 V** threshold input at the **ASSUMED 5.40 V** raw trip produces **6.551 V** at raw **28.3 V**. An **ASSUMED 2.5 V** threshold produces **13.102 V**. **UNKNOWN:** whether any specific **ASSUMED 3.3 V-supplied** comparator tolerates these inputs; do not assume beyond-rail operation. A proposed clamp/attenuation network must include worst-case leakage in the trip-window budget, current injection and backpower during unpowered states, overdrive recovery, and fault-voltage survival. Adding a clamp can change both accuracy and timing.

**INFERRED — reset-policy gap:** a latch reset only when its raw-powered detector supply crosses UVLO does not prove no re-enable while input is physically connected. Buck hiccup, eFuse interruption, UVLO or source droop can collapse raw and reset the latch while the upstream source remains connected. TPS26630's fast-trip off/restart sequence and SHDN/UVLO reset paths are documented in [its source review](TPS2663_SOURCE_REVIEW.md). Literal no-re-enable requires reviewed state retention/source-presence supervision or an explicitly approved narrower recovery policy. No alternative power architecture is selected here.

Two **PROPOSED conceptual approaches**, neither supported by a completed worst-case timing budget:

| Approach | Latch concept | Gate-discharge concept | Unresolved interfaces |
| --- | --- | --- | --- |
| A | Asynchronous set flip-flop or SR latch; independent comparator sets fault; supervisor controls reset/startup sequencing | Local NPN collector at HGATE, emitter at OUT, driven by a reviewed source-referenced base driver | Default-off state, set/reset priority, base-drive energy/headroom, hot leakage and static hold current |
| B | Separate comparator latch with regenerative feedback; supervised detector-supply reset | Local NMOS drain at HGATE, source at OUT, driven by a reviewed source-referenced gate driver | Feedback latch retention, initial state, floating drive availability, gate-rating control and leakage |

**INFERRED:** a ground-referenced detector output cannot directly provide the required drive above OUT for either local device while OUT is near the regulated output. The source-referenced driver is a necessary unresolved circuit, not a presumed capability. An ordinary HGATE-to-ground pull-down risks violating the LM74800 **KNOWN −0.3 V HGATE−OUT absolute minimum**. A simple PNP discharge substitution requires separate review of residual Q302 gate voltage and unintended junction-current paths; it does not automatically establish isolation.

**KNOWN — LM74800 limits:** SNOSD95C specifies HGATE−OUT and DGATE−A absolute maxima **15 V**, HGATE−OUT absolute minimum **−0.3 V**, and HGATE source current maximum **75 µA**. The reviewed HGATE drive upper bound is **14.5 V** under its stated supply conditions. Its high-voltage supply/pin ratings do not establish ratings for new logic, clamps or driver transistors.

**CALCULATED — conditional discharge screen:** using the brief's **ASSUMED/unverified Q302 gate charge 96 nC** and **ASSUMED gate-discharge allocation 1.6 µs**, average charge-removal current is `96 nC / 1.6 µs = 60 mA`; allowing for the **KNOWN 75 µA** maximum HGATE source current gives **60.075 mA**. This is not a guaranteed gate-to-isolation time: maximum charge, Miller effects, changing sink capability, propagation, parasitics and isolation endpoint remain **UNKNOWN**. To limit the load of a permanent gate-source resistor to **ASSUMED 1 µA** at **KNOWN 14.5 V** drive would require **CALCULATED at least 14.5 MΩ**. Such a resistor cannot be assumed to hold the gate off against the controller's source current; hold-off needs an active reviewed state.

**OPEN — new raw-side parts:** bulk capacitor, detector supply and bypass, raw divider and clamps, level shifter, gate driver and common-drain path all require individual voltage/current/pulse/thermal checks. Check elevated gate and CAP nodes as well as raw voltage, and distinguish voltage-to-ground from voltage-to-source. Keep the separate isolation and reverse-feed requirements, including externally powered load states.

## Acceptance interpretation

**RESULT: acceptance criterion 6 is not demonstrated.** Some captured voltage classes and the nominal static FB divider support further study, but exact component/source verification, new detector parts, held-fault interfaces and transient pin stresses remain OPEN. The reset policy and detector-valid interlock also prevent treating acceptance criterion 2 as established by a conceptual latch. No SPICE or vendor-model result is claimed: **NOT RUN**. This document does not change hardware, approve an architecture, release R2/R3, or qualify electrical safety.
