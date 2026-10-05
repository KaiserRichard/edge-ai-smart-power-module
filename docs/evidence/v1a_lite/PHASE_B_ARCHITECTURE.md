# V1A-Lite Phase B — costed architecture comparison

**2026-10-05 — resumed and completed; PROPOSED, analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**Completion finding:** all options now include Addendum 2’s continuous 54.6–64 V input cutoff. Installed core BOMs are 274–307k VND, but first-build minimum-lot estimates are 1.42–1.52 million VND. Budget and electrical qualification remain BLOCKED; no option is ready for fabrication. [Verification record](PHASE_B_VERIFICATION.md).

## Scope, evidence and interpretation

KNOWN: follows the complete Phase B brief and its lead-architect addendum, including the revised report name and option definitions. Worktree `wt-litephb`, branch `docs/v1a-lite-phase-b`, starting commit `cd18b2bdbdd13b77ca3200b49ba517d92b84ecd1`. [Phase A](PHASE_A_AUDIT.md) and its complete CSV were read. No schematic, PCB, library, upstream reference source or historical evidence is changed. No purchases or push. Work is performed directly without sub-agents.

KNOWN owner requirements: 18–28 V assumed normal auxiliary bus, upstream 13S-to-24 V converter outside this design; retain LM61460; 5.1 V-class, 5 A Pi 5 supply; independent hardware output OV protection; fuse/TVS/reverse input protection; remove Sheet 04 with a copper replacement for R401. Preferred installed core cost 300–500k VND, whole first prototype strictly below 1 million VND. Priorities are affordability, Pi survival, output capability, education, then PCB simplicity.

KNOWN: use the project's frozen **Pi-pin peak <5.5 V and minimum 4.75 V**, not a newly inferred Raspberry Pi damage specification. [Decision log](../../context/06_DECISION_LOG.md) records the strict inequality and no permissible overvoltage duration. No transient above 5.5 V is excused because it is short. The continuous 54.6–64 V input fault in Addendum 2 below is now mandatory for every option. Exact source current limit, hiccup timing, reservoir capacitance, wiring impedance, ambient range, surge waveform and Pi harness/interface remain OPEN.

Labels: KNOWN = dated observation or cited specification; CALCULATED = arithmetic/model; ASSUMED = explicit screening/accounting input, not a newly invented requirement; PROPOSED = recommendation awaiting Claude/owner selection; OPEN = missing bound or qualification. No option is bench validated. This is R1 comparison work, not advancement through schematic/layout/fabrication gates.

## Step 1 — common LM61460 cost-down

PROPOSED: retain the audited **5.06504065 V nominal** divider (100 kΩ/24.6 kΩ) for this comparison, as directed by the addendum. Treat “5.1 V” as the supply class; this does not deliver precisely 5.100 V at the Pi under load. A later exact-5.1-V setpoint decision requires repeating both undervoltage and nuisance-trip budgets. All totals include the new inductor and lower-voltage output bank, not the research design's expensive parts.

KNOWN source: [TI LM61460 datasheet SNVSBD5D, July 2022](https://www.ti.com/lit/ds/symlink/lm61460.pdf), local read-only `LM61460AANRJRR.pdf`, §§7.4, 9.2.2 and table 9-5. The reference 400 kHz/5 V application uses 4.7 µH and four 22 µF capacitors; table 9-3 also gives two/three 47 µF starting points. Lite changes the input envelope, inductance, capacitor technology/effective value and downstream load. Reference values are a starting point, not proof of loop margin.

### Inductor comparison

| PROPOSED candidate | L / tolerance | Isat at 20% L drop, 25°C | Irms at 40°C rise | DCR typ / max | Body envelope | LCSC USD @10 / VND |
| --- | --- | --- | --- | --- | --- | --- |
| **Bourns SRP1265A-6R8M**, costed | 6.8 µH ±20% | 18 A | 11.5 A | 9.5 / 11.5 mΩ | 13.5 × 12.5 × 6.5 mm nominal | 0.9375 / 24,844 |
| Bourns SRP1265A-100M, alternate | 10 µH ±20% | 15.5 A | 10 A | 13.2 / 16.5 mΩ | same family | 1.0292 / 27,274; direct stock zero |

KNOWN: [Bourns SRP1265A Rev. 06/24](https://www.bourns.com/docs/product-datasheets/srp1265a.pdf). Carbonyl-powder shielded parts; curves and current figures are not minimum hot differential-inductance guarantees. The 6.8 µH part was stocked in the direct LCSC observation; the 10 µH part's old indexed stock must not supersede the direct zero-stock result. Coilcraft XAL7070-103's Phase-A 7.5 A Isat fails the new ≥8 A requirement and is excluded.

CALCULATED, `ΔIL = Vo(1−Vo/Vin)/(L f)`, using 5.1 V for conservative ripple screening:

| L | 18 V ripple / peak at 5 A | 24 V ripple / peak | 28 V ripple / peak | 28 V stressed ripple / peak |
| --- | --- | --- | --- | --- |
| 6.8 µH | 1.344 / 5.672 A | 1.477 / 5.738 A | 1.533 / 5.767 A | 2.689 / 6.345 A |
| 10 µH | 0.914 / 5.457 A | 1.004 / 5.502 A | 1.043 / 5.521 A | 1.829 / 5.914 A |

ASSUMED stressed column combines −20% initial L, an additional 20% magnetic drop and 356.4 kHz (`360 kHz` datasheet minimum with an extra 1% frequency-resistor allowance). These multipliers are sensitivity inputs, not certified simultaneous corners. At 6.8 µH, Irms = sqrt(25 + 2.689²/12) = 5.060 A. Copper loss at maximum 25°C DCR is 0.294 W; applying copper's approximate 0.393%/°C rise to 100°C gives 0.381 W, before AC/core loss. A square-law scaling of the catalog temperature rise gives ~7.7°C at 5.06 A (10 µH: ~10°C); this is only a thermal estimate. Measure actual temperature at 5 A in the enclosure.

KNOWN/CALCULATED: TI's high-side peak limit is 8.9/10.3/11.5 A at low duty, with duty-dependent slope compensation; low-side valley limit is 6.1/7.1/8.1 A. Normal calculated peaks have headroom, but an 8 A saturation rating alone does not satisfy TI's recommendation to exceed the high-side limit. Both Bourns candidates exceed 11.5 A at their catalog test condition. A shorted high-side transistor **bypasses these electronic current limits entirely**. Do not extend either inductor's normal-operation L to 100 A as in the research model.

### Capacitors and small passives

PROPOSED input bank: four Murata **GRM32ER71H106KA12L**, 10 µF/50 V/1210, split symmetrically across both VIN/PGND pairs; two GRM188R71H104KA93D 100 nF/50 V directly at the pin pairs. The 10 µF MPN has residual stock but is EOL in the prior procurement audit. Its current manufacturer bias model is unavailable. **OPEN** minimum effective input C; 40 µF nominal is not 40 µF at 28 V. An ASSUMED 40% bias retention ×0.9 initial ×0.85 temperature gives 12.24 µF, above TI's 10 µF target; replace or increase the bank if verified C falls below that. Input RMS switching current is 2.25 A at 18 V, 2.05 A at 24 V, 1.93 A at 28 V; verify sharing, MLCC heating and layout. A 50 V electrolytic damping reservoir is included in Step 2.

| Output-bank candidate | Manufacturer typical effective C at 5.1 V, 25°C | Cost and disposition |
| --- | --- | --- |
| **GRM32ER61C476KE15L**, 47 µF/16 V/X5R/1210/±10% | **29.728753 µF each**; at 5.5 V: 28.008429 µF | Costed: six raw-side parts, plus two local protected-side parts in all options; USD 0.3135 each at ten pieces |
| GRM31CR61A476ME15L, 47 µF/10 V/X5R/1206/±20% | **18.322512 µF each**; at 5.5 V: 16.814102 µF | More units needed for equal effective C; price OPEN, not used in totals |
| TDK C3225X7R1C226M250AC, 22 µF/16 V/1210 | Manufacturer characterization exists; no numeric curve reading used here | Exact LCSC offer OPEN; not confused with C338051, which is a different 47 µF part |

KNOWN evidence: Murata SimSurfing responses, 25°C, **0.5 Vrms** excitation for these high-C models, are retained in [manufacturer observations](../../../third_party/v1a_lite_phase_b/MURATA_05V_OBSERVATIONS.json). Linear interpolation of surrounding data points produces the values above. The attempted 1 Vrms query was rejected, and is retained separately rather than represented as valid evidence. Typical model curves are not production minima. X5R limits the body-temperature class to 85°C; a hotter board requires a new capacitor choice.

ASSUMED/CALCULATED: six raw capacitors total 178.373 µF typical at 5.1 V. For fault/ripple screens use **120 µF**, rounded down from `6 ×29.728753 ×0.9 ×0.85 ×0.9 =122.809 µF` (initial tolerance, temperature and additional aging/model allowance). This is a proposed acceptance target, not a manufacturer guarantee; at 5.5 V the same convention gives 115.70 µF. Use **110 µF** in fault analysis to cover that voltage range. Two protected-side parts give ~40 µF using the same convention. Do not count the Pi's unknown internal capacitance, or capacitors isolated behind a series switch, as raw-side fault storage.

PROPOSED small parts: 100 nF/16 V X7R CBOOT from CBOOT to native SW; 0 Ω RBOOT; 1 µF/16 V X7R VCC to AGND; 22 pF/16 V C0G CFF with 1 kΩ RFF; RT =33.2 kΩ; 100 kΩ/24.6 kΩ 0.1% FB divider. The power bank uses 1206/1210 as required; the tiny feedforward capacitor is 0402 and bypass/feedback parts are 0603/0805. No 50 V part is costed on a 5 V bank or low-voltage timing node. BIAS stays at GND: tying it to a raw output that can fault toward 28 V violates its 16 V limit unless another protection bound is established. VCC is never a supply for independent OV protection.

PROPOSED EN: discard the TPS26630 PGOOD dependency, retain an independent 100 kΩ/24.6 kΩ divider from protected input. This is an enable connection, **not** a claimed 18 V UVLO. Its nominal ratio gives ~3.55–5.53 V on EN over 18–28 V; verify TI thresholds and pin rating at surge. Buck PGOOD may be left unused; do not leave an old Sheet-03 pullup dependency in a future capture.

### Ripple, regulation, transient and stability screens

CALCULATED: with 120 µF and ASSUMED 3 mΩ effective bank ESR, stressed switching ripple is `2.689/(8×356400×120e−6) +2.689×0.003 =15.93 mV p-p`, excluding spikes/ESL. FB ±1% and two ±0.1% resistors give **5.00635–5.12391 V** at the bank, before resistor drift, FB current and dynamics. Therefore the brief's **5.12 V maximum including ripple and overshoot is not established even statically**. A +25 mV load-release allowance and half the above ripple imply ~5.157 V; +100 mV gives ~5.232 V. These are sensitivity cases, not allowed overshoot requirements. A true 5.100 V nominal divider would widen the high corner further.

CALCULATED: 100 kΩ with 22 pF puts the ideal feedforward zero near 72.3 kHz and divider pole near 366 kHz; 1 kΩ adds its high-frequency rolloff. At 120 µF/3 mΩ the capacitor ESR zero is ~442 kHz, above TI's 200 kHz “omit CFF” boundary. The LC resonance spans ~4.1–7.3 kHz over representative 6.8–10 µH / 110–178 µF values. TI's below-50%-duty minimum-L rule gives `0.2×5.1/356400=2.86 µH`; stressed 6.8 µH gives 4.352 µH. Minimum ripple at 18 V, 440 kHz, 12 µH is ~0.692 A, above 10% of 6 A. These checks satisfy useful datasheet design screens, **not measured phase margin**.

OPEN: internal compensation plus the revised L/C bank, output-fuse ESR in Options 1/3B, series-switch impedance and actual Pi capacitance must be modeled/measured. No numerical phase margin can honestly be inferred from the BOM table. PROPOSED acceptance: ≥45° phase margin and ≥10 dB gain margin over source/load/temperature corners, verify 18/24/28 V and 0–5 A steps. A simple 5 A load step lasting 10 µs requires ~0.417 V from 120 µF before ESR; the feedback response and local capacitance must be measured. These inexpensive parts do not by themselves guarantee the narrow Pi window.

ASSUMED efficiency at 25.5 W is 90–94%, implying 1.63–2.83 W total conversion loss and worst input current 1.574 A at 18 V/90%. Budget input connectors/fuse for that continuous current plus startup/fault. Do not claim a measured efficiency. Follow TI's dual hot-loop layout, compact SW copper, uninterrupted power return, separate quiet FB/AGND path, and thermal copper/vias; verify pin numbering and each replacement footprint before R2/R3. Required peak-load duration and enclosure ambient remain OPEN.

Step 1 component costing is in [PHASE_B_BOM.csv](PHASE_B_BOM.csv); complete option totals follow in Step 5. Source provenance and stock/price snapshots are kept under `third_party/v1a_lite_phase_b/`.

## Step 2 — original simple input comparison (superseded by Addendum 2)

PROPOSED common topology:

```text
JIN + -> F101 3 A fast -> Q101 reverse P-FET -> VIN_BUCK -> LM61460
                         D=input, S=output       |-- TVS3300 -> power GND
                         gate -> 10k -> GND      |-- 100uF/50V + input MLCCs
                         12V zener S-to-G
JIN - --------------------------------------------- power GND
```

KNOWN/PROPOSED fuse: **Littelfuse 0451003.MRL**, very fast 3 A, 125 V, nominal cold 22.7 mΩ, nominal melting I²t **1.650 A²s**. Relevant DC interrupt capability is 300 A at 32 V (the distinct 75 V high-interrupt entry must not be mixed with a different series). [Manufacturer 451/453 sheet](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1), revision as printed `GD. 12/01/25`. At 1.574 A input the fuse is at 52.5% nameplate; allow ambient derating and inrush. It is not a 3 A electronic limiter. At 100% rating the opening time is at least four hours; 200% has a five-second maximum, which is far too slow to protect the Pi directly. Source-limited/hiccup behavior is treated in Step 3.

PROPOSED reverse FET: **Diodes DMP6023LE-13**, 60 V P-channel SOT-223; use it reversed relative to a conventional high-side switch so its body diode initially conducts from input drain to protected source. [DS37199 Rev. 3-2, January 2015](https://www.diodes.com/assets/Datasheets/DMP6023LE.pdf): 23 mΩ maximum at −10 V gate drive, 35 mΩ at −4.5 V. Normal loss at 1.574 A is 57 mW at 23 mΩ; a 2× hot-resistance screen gives 114 mW. It is not a true ideal diode: when powered it can pass reverse current. A powered output plus reversed input can impose ~56 V across a 60 V part; that combination and surge/reversal sequencing are OPEN tests.

PROPOSED gate clamp: **BZT52C12-7-F**, cathode to Q101 source, anode to gate; 10 kΩ/0805 gate-to-ground resistor. At 28 V, approximately 1.6 mA and 19 mW in the zener, 26 mW in the resistor. At a 40 V protected node, ~2.8 mA, 34 mW/78 mW. Verify zener behavior at this low current, ±20 V FET VGS limit, and source/gate dv/dt. Zener-short failure turns the FET off; zener-open can overstress its gate. FET short loses reverse protection; FET open interrupts service.

### TVS feasibility: ordinary 30 V TVS versus flat clamp

KNOWN: **SMCJ30CA** has 30 V standoff, 33.3–36.8 V breakdown and **48.4 V clamp at 31 A**, so it cannot be represented as a <42 V clamp at its rated surge current. Its 30 V standoff exceeds 28 V plus an ASSUMED extra 5% uncertainty (29.4 V), but standoff alone says nothing about safe clamping. For illustration only, interpolating the catalog endpoints suggests ~37.17 V at 1 A at 25°C; this is **not a guaranteed low-current or hot clamp bound**. USD 0.3993 at ten pieces is cheap, but this candidate is rejected for an unspecified bus surge.

PROPOSED engineered alternative: **TI TVS3300DRVR**, standoff 33 V, manufacturer maximum 40 V at 15 A and 35 A **8/20 µs**, initial VIN=0 and 27°C test condition ([SLVSDO2C, February 2018](https://www.ti.com/lit/ds/symlink/tvs3300.pdf), §7.6). Place it after reverse protection because it is unidirectional. The **DRV** package is limited to **3.5 A 10/1000 µs**, not the WCSP's 4 A figure. Costed LCSC price is USD 0.4442, but direct stock is zero: procurement remains OPEN, and that reference price is not an in-stock offer.

ASSUMED initial surge qualification envelope: positive pulse **≤15 A, 8/20 µs**, and a separate **≤3 A, 10/1000 µs** test; no continuous bus OV, no direct 13S connection. Use ≤50 V source excursion at the input P-FET for its 60 V VDS screen, explicitly accounting for source/cable impedance when producing those currents. These are proposed test envelopes, not measured characteristics of the owner's converter. At the cited 8/20 condition, 40 V leaves 2 V to the buck's 42 V absolute limit. Reserve ≤1 V for layout inductance/ringing and require measured peak **<41 V** at both VIN pins. The hot/prebiased/10–1000 clamp bound and raw-source slew remain OPEN; the 27°C table must not be promoted to an all-condition guarantee. 36 V is the normal operating ceiling, so a <42 V surge result still does not authorize continuous operation at 40 V.

PROPOSED damping reservoir **Panasonic EEUFR1H101**, 100 µF/50 V, 8×11.5 mm, polarity verified in later capture. This helps cable/MLCC resonance but does not limit inrush. With 140 µF nominal total input capacitance, stored energy at 28 V is 54.9 mJ. For an ASSUMED 0.5 Ω charge path, `∫i²dt = C V²/(2R) =0.110 A²s`, below 1.650 A²s nominal melting; at 0.05 Ω this rises to 1.10 A²s and initial current to 560 A. That latter idealized spike invalidates a casual fuse/P-FET rating check. Hot-plug waveform, FET SOA, fuse pulse derating and TVS slew must be measured; copper resistance is not an intentional inrush limiter.

| Input implementation | Incremental parts and installed USD | Result |
| --- | --- | --- |
| Costed P-FET | F101 0.2556; TVS3300 0.4442; Q101 0.4734; gate zener 0.0771; 10 kΩ 0.0034; 100 µF reservoir 0.3259 = **1.5796 / 41,859 VND** | Lowest cost; TVS stock and surge/hot-plug qualification OPEN |
| N-FET ideal diode alternative | Replace Q101/zener/resistor block with LM74700QDBVRQ1 1.5974 + CSD19537Q3 0.7498 + 100 nF/16 V charge-pump cap 0.0170 + gate-zener allowance 0.0771 =2.4413; total input **3.4670 / 91,876 VND** | Better reverse-current blocking; more cost. External zener choice must not fight the controller's regulated drive; this is a costed screening alternative, not a wiring release |

KNOWN source topology: [TI reverse battery note SLVA139, September 2003](https://www.ti.com/lit/an/slva139/slva139.pdf), P-FET technique, and [LM74700-Q1 SNOSD64G](https://www.ti.com/lit/ds/symlink/lm74700-q1.pdf). Referenced only; no upstream circuitry copied into CAD. All three output-option totals use the P-FET input stage. No electronic input cutoff, ramp, PGOOD or input latch survives this simplification. Continuous overvoltage beyond TVS energy ratings remains a limitation, not a fault cleared by assumption.

KNOWN resume provenance: the previous worker reported a Step 1 index-lock failure; its partial Steps 1–2 and source observations were subsequently preserved in `db2a88c`. This continuation starts from that clean commit and reuses all saved price searches. Historical prices remain dated 2026-10-04, not freshly verified offers.

### Resume review of Step 1

OPEN — mandatory low-voltage capacitor tradeoff: the six raw-side 16 V MLCCs can see the auxiliary bus after a buck high-side short. A downstream disconnect alone cannot protect them. A downstream crowbar stops protecting them if its output fuse clears first. None of the costed low-voltage banks is qualified for this fault until source removal or a raw-side clamp is proved. Do not infer a fault voltage rating from normal 5.1 V operation. The same caution applies to bootstrap/VCC damage after an internal buck failure; containment, not continued buck operation, is the objective.

### Resume review of Step 2

KNOWN: the 451-family table actually includes a separate 10,000 A/75 VDC entry for 2–5 A ratings; the conservative 300 A/32 VDC figure used here remains applicable. Neither interrupt rating establishes selective clearing or a safe source waveform. At 5 A load, the 7 A output fuse introduced below operates at 71.4% nameplate, only slightly below the manufacturer's 75% continuous-use convention before extra ambient derating.

OPEN: direct saved stock is zero for TVS3300DRVR. Saved alternatives TVS3301DRBR (USD 0.5736, stock 2,563) and TVS3300YZFR (USD 0.2979, stock 55) exist, but their package/layout and pulse limits are not interchangeable. No repeat price search was made. Procurement and package qualification are still required; no silent substitute enters the totals.

## Addendum 2 — continuous 54.6–64 V input fault, common to EVERY option

**KNOWN — governing owner requirement, received 2026-10-05:** upstream is the non-isolated UENPO S4-T482410; the owner states 60 V maximum input and no output OVP. Its failed high-side switch can expose this board continuously to 54.6 V battery / approximately 64 V regeneration bus. These are owner-supplied interface facts, not independent validation of a UENPO datasheet. The earlier exclusion of direct battery pass-through is superseded. Also, 64 V exceeds the owner's stated upstream 60 V rating: upstream regeneration coordination remains OPEN even if Lite disconnects successfully.

**OPEN requirement conflict:** original normal range is 18–28 V; Addendum 2 also calls 26 V “max normal” while requesting standoff above 28 V. Preserve 28 V for no-trip screening pending an owner interface resolution. PROPOSED nominal cutoff ~30 V rather than exactly 28 V, leaving tolerance above 28 V and below buck's 36 V operating ceiling. No requirement is silently narrowed to make a circuit pass.

### Costed discrete cutoff/reverse stage replacing original Step 2

```text
JIN -> F101 -> Q101 reverse PFET -> S_COMMON -> Q102 OV PFET -> VIN_BUCK
              drain=input         sources common        drain=output
              gate:12V clamp      Q102 gate:12V clamp       | TVS3300
              +20k to GND         +1k to S_COMMON            | 100uF/50V
                                                           | input MLCCs
S_COMMON -> 4k power-resistor chain -> CTRL12 (12V shunt zener, 1uF/16V)
S_COMMON -> 110k/10k divider -> TL431 REF; TL431 A=GND
CTRL12 -> 1k -> TL431 K -> 3.3V zener -> 10k -> Q103 base
Q103: 300V NPN, emitter=GND; base->100k->GND
Q102 gate -> 600R power-resistor chain -> Q103 collector
Normal: TL431 off, Q103 on, Q102 gate pulled down.
Input OV: TL431 K low, 3.3V level shift removes Q103 drive,
          1k pulls Q102 gate to source; Q102 blocks continuous input.
```

PROPOSED Q101/Q102 **Infineon IRF9540NPBF**, 100 V P-channel TO-220; each has its own gate and 12 V source-gate zener. Q101's body diode initially charges S_COMMON positively; Q102's opposing body diode blocks forward feed when off. The controller is powered from S_COMMON before Q102, so cutoff does not remove its own fault observation. Reversed input leaves Q101 off and avoids directly applying negative input to TL431/control supply. This is a review concept, not a pin-verified schematic or validated fail-safe circuit. Cold-start into 64 V and control-rail sequencing are explicitly unresolved.

KNOWN/CALCULATED: FETs are 100 V VDS, ±20 V VGS, 117 mΩ maximum at −10 V/25°C; at 1.574 A their combined cold loss is ~0.580 W and a 2× hot screen ~1.16 W. At 64 V off, Q102 nominal VDS margin is 36 V, before inductive ringing. The gate zener needs maximum voltage/dynamic behavior verified at actual current; its label “12 V” is not a maximum bound. Q101's gate uses **2×10 kΩ** series to share continuous 64 V resistor voltage/power: ~0.135 W total at 52 V across the chain. Reverse −64 V with a separately powered 28 V output can approach 92 V across a 100 V FET: this combined fault has little margin and remains OPEN. [Infineon IRF9540N datasheet, v01_01, 01/04](https://www.infineon.com/dgdl/Infineon-IRF9540N-DataSheet-v01_01-EN.pdf?fileId=5546d462533600a401535611cfa21dc8).

PROPOSED detector protection: 4 kΩ is eight 500 Ω/0603 resistors; at 64 V and 12 V clamp, total 0.676 W (~84.5 mW each at 25°C). Hot derating may require larger packages: OPEN, no 0603 is assumed adequate at unspecified ambient. Available current is ~13 mA at 64 V; clamp worst-case no-load dissipation ~156 mW. At 18 V only 1.5 mA is available, so zener knee, Q103 drive and startup must be checked. TL431 K and REF remain on low-voltage nodes instead of exposing its 36 V cathode limit to 64 V. Q103 **MCC MMBTA42-TP**, 300 V VCEO, takes the high collector voltage; exact saved LCSC offer has **zero stock**, retained as an OPEN procurement issue after the one new lookup. No alternate vendor's electrical ratings are assigned to this part.

CALCULATED threshold: upper 100 kΩ +10 kΩ, lower 10 kΩ, all 0.1%. Ideal trip **29.94 V**, typical reference-input current adds ~0.22 V. With B-grade 2.449–2.541 V expanded reference range, up to 26 mV additional cathode-voltage effect, ±0.1% ratios and reference current up to 6.5 µA, an intentionally broad static screen is approximately **29.0–31.3 V**. This leaves >1 V over 28 V and ≥4.7 V to 36 V, before dynamic let-through. Cathode current changes throughout the transition; divider TCR and zener/base logic make this a screening interval, not a guaranteed threshold. A divider tuned exactly to 28 V would conflict with the unchanged 28 V normal bound.

CALCULATED turnoff/charge screen: one FET's typical Miller charge is ~34 nC. A 1 kΩ gate-source pullup at a 2–4 V plateau gives 2–4 mA, hence **~8.5–17 µs** typical Miller time, plus TL431, transistor-storage and gate-tail delays. Assume **25 µs total** only for sensitivity, not a specification. Protected input C has ASSUMED minimum `80 µF electrolytic +12.24 µF ceramics ≈92 µF`. From worst static trip 31.3 V, holding VIN_BUCK below 36 V requires integrated incoming excess charge `<92µF×4.7V≈432µC`; at 15 A this permits **28.8 µs**, at 100 A only **4.3 µs**. A 15 A/25 µs screen reaches **~35.38 V** before parasitics; a stiff-source 100 A case exceeds the window. Do not claim the gate-charge typical numbers prove 64 V cutoff safety.

OPEN SOA: a rough `64 V ×15 A ×25 µs=24 mJ` overlap screen is not a MOSFET SOA qualification. Check the actual 64 V/hot single-pulse SOA and transient thermal impedance for each instantaneous VDS/current, and startup capacitor charging as well as turnoff. The datasheet's 25°C single-pulse SOA cannot justify hot repetitive linear operation. There is no active current limit in this input stage. Actual battery/UENPO short impedance, source reservoir, gate storage, dV/dt coupling and wire inductance remain unbounded; fast source application can defeat the assumed timing. An active source-referenced turnoff driver or qualified HV OVP controller may be needed, with a fresh cost review.

PROPOSED TVS placement: retain 33 V TVS3300 **after Q102**, with the protected input capacitors. It must not sit directly across the continuous 64 V source. When cutoff succeeds it sees only the short let-through/inductive transient, then no sustained 64 V current. Earlier ≤15 A 8/20 µs and ≤3 A 10/1000 µs transient screens do not establish a 25 µs rectangular 64 V fault pulse. Derive and test actual pulse energy; at 40 V×15 A×25 µs, the illustrative clamp energy is 15 mJ. Require buck-pin peak <42 V always and preferably <36 V during controlled cutoff. TVS short must be cleared or sustained safely; TVS open leaves only cutoff timing. Q102 short or detector failure can make the TVS conduct continuously and destroy it; fuse/source coordination is still required. This design is not single-fault tolerant at its own input protection layer.

KNOWN/CALCULATED F101 remains 0451003.MRL, nominal melting 1.65 A²s. Its 2–5 A family includes a 10 kA/75 VDC interrupt entry, unlike the earlier 32 V-only screening assumption; **64 V use must verify the exact agency/rating and source prospective current**, not reuse a 32 V interrupt rating. During successful sustained cutoff, source current is just controller bias/leakage, so **the fuse need not and normally will not blow**. Q102 stays off as long as the input detector sees OV. This avoids the need to force a current-limited source to clear a fuse. No specified hysteresis means threshold chatter/retry remains OPEN; do not use linear gate cycling as continuous surge regulation.

### Input SCR crowbar alternative

PROPOSED comparison: retain F101 and one 100 V reverse Q101, replace series Q102/Q103/gate-drive network with a **TYN612RG SCR across the protected input**, triggered by the same ~30 V detector through a BC807 PNP. The PNP must be fed from the clamped CTRL12 reservoir, never directly from 64 V; the input divider and detector-supply protection stay. This is an input crowbar, independent of the output crowbar/detector. The 1 µF/12 V reservoir stores only 72 µJ; sustaining ~100 mA gate current for 100 µs needs ~10 µC and causes ~10 V droop. Gate latch establishment therefore needs a larger local reservoir or a verified shorter trigger pulse. No implementation is silently approved.

CALCULATED nominal fuse/SCR inequality remains **1.65 A²s <98 A²s** with 140 A/10 ms SCR surge rating, but battery fault current may exceed both the SCR peak/dI/dt limit and fuse interrupt rating. At a hypothetical 100 A sustained pulse, nominal melt time is 165 µs; at 300 A it is ~18 µs, yet 300 A exceeds the quoted 140 A SCR pulse rating and needs a waveform-specific check. Maximum clearing I²t/hot derating are still missing. If the upstream high-side is physically shorted, its electronic regulation may no longer limit fault current at all. If some upstream limiting remains, a 2.2–3 A limit may never clear F101. SCR then dissipates the same **2.02–2.82 W** as the output-crowbar current screen; current is not multiplied by 64 V, but supply/wire fault energy is much larger. Without a qualified sink and hiccup retrigger envelope this is not safe indefinite containment.

CALCULATED nominal component-only comparison, using saved prices and omitting no common supply/divider/fuse/TVS/reverse parts: remove Q102 (0.3593), Q103 (0.0583), level-shift zener (0.0528), Q102 gate zener (0.0771), six 100Ω (0.0192), gate 1k (0.0026), base 10k (0.0034), base bleed 100k (0.0031): **0.5758 USD**. Add SCR (0.5700), PNP (0.0200), 500Ω base (0.0020), 10k base-emitter (0.0034), 100Ω gate (0.0032), 1k gate-cathode (0.0026): **0.6012 USD**. Difference **+0.0254 USD /673 VND**, before a larger trigger reservoir/sink. Thus, for these exact offers, the discrete series cutoff is marginally cheaper in components and materially cheaper when indefinite crowbar cooling is included; it is also the safer **direction** for a continuous uncertain/current-limited source because it can disconnect without fuse clearing. Neither is electrically qualified.

Every Option 1/2/3A/3B below includes the new **COMMON_INPUT 66,324 VND** stage in the totals. The old 41,859 VND input number is superseded. All retain independent output protection against LM61460 HS short; input OV cutoff cannot detect that internal fault while its own input remains 24 V. Qualification must separately exercise continuous 54.6/64 V at the input, cold connection into fault, slow ramps, source-current extremes, open/short detector/FET/TVS, hot SOA, reverse polarity and repetitive crossings. **R1 architecture release remains BLOCKED.**

## Step 3 — three independent output-OV candidates

All references below are **PROPOSED functional BOM identifiers**, not edits to the old CAD reference numbering. Exact MPNs, quantities, unit/extended LCSC prices, dated URLs, local availability and substitution restrictions are in [PHASE_B_BOM.csv](PHASE_B_BOM.csv). `COMMON_*` applies once to every option; Option 1 adds `OPT1 + CROWBAR`, Option 2 adds `OPT2`, Option 3A adds `OPT3`, and Option 3B adds `OPT3 + CROWBAR`. The crowbar in 3B is placed on the raw output, so it has no separate output fuse. All detectors operate independently of LM61460 FB/PGOOD/VCC/control.

### Common high-side-short calculation and nuisance margin

ASSUMED screening event: buck high-side device shorts at the simultaneous release of a 5 A load, with initial bank voltage 5.124 V and inductor current 6.345 A. Use 24 V and 28 V source cases, stressed L =4.352 µH, raw C =110 µF; ignore protected C to avoid relying on fuse/wiring/switch sharing. The source can initially supply a reservoir pulse even if its long-term current limit is only 2–3 A. A final source impedance/current/time contract remains OPEN.

CALCULATED short-time constant-acceleration screen, with `a=(Vin−V0)/(L C)`:

```text
V(t) = V0 + I0 t/C + a t²/2
at detector threshold VT:
  tT = [−I0/C + sqrt((I0/C)² + 2 a (VT−V0))]/a
  IT = I0 + (Vin−V0)tT/L
after threshold, action delay d:
  Vpeak ≈ VT + IT d/C + (Vin−VT)d²/(2 L C)
```

This retains current accumulated BEFORE detection. The approximation overstates acceleration for constant L as voltage rises, but is NOT a worst-case bound: saturation can reduce L further, capacitance can fall, and ESR/ESL/cable resonance can increase Pi-pin peak. At these trip points IT is already ~18–20 A, near or above the candidate's catalog Isat. Electronic buck current limiting no longer operates. A current-limited-source example must not erase its stored output/input-capacitor energy.

| Case / screening high trip | Vin | IT at trip | Delay after threshold | Calculated capacitor peak, without ESR/ESL |
| --- | --- | --- | --- | --- |
| Option 1, 5.430 V | 24 / 28 V | 18.23 / 19.85 A | 0.5 µs | 5.518 / 5.526 V |
| Option 1, same | 24 / 28 V | same | 2 µs | 5.839 / 5.885 V |
| Option 2, 5.450 V | 24 / 28 V | 18.74 / 20.43 A | 5 µs | 6.786 / 6.967 V |
| Option 3, rounded 5.418 V | 24 / 28 V | approximately 17.9 / 19.5 A | 1.2 µs typical IC response | approximately 5.641 / 5.665 V |

CALCULATED: Option 1's 70 mV static fault headroom at 28 V allows only about **0.38 µs** total detector/drive/SCR establishment time, before all parasitic allowance. Option 3's ~82 mV allows roughly **0.45 µs** under the same current-rise screen. Neither quoted typical response nor an assumed SCR turn-on establishes this. Pi pins may see these peaks plus local ringing; **no candidate demonstrates <5.5 V**. These failed screens are useful rejections of a claimed guarantee, not predictions of a particular prototype's measured waveform.

CALCULATED nuisance screen: nominal is 5.065 V; static tolerance high 5.124 V; illustrative ripple +25 mV load release gives 5.157 V; +100 mV release gives 5.232 V. A detector whose minimum trip is ~5.19–5.22 V has only ~33–63 mV above the first case and can trip in the second. No exact allowed load-step overshoot or ambient range has been established. Do not use the brief's 5.12 V as a proven maximum or add a delay filter to cure nuisance trips without repeating the fault peak calculation.

### Option 1 — output fuse, TL431 detector and SCR crowbar

```text
24 V -> common input fuse/TVS/reverse block -> LM61460 -> L201 -> RAW5
                                                               | 6 x 47uF/16V
RAW5 -> F301 7A -> PROTECTED5 -> copper replacing R401 -> Pi harness
                      |-- 2 x 47uF/16V -> GND
                      |-- SCR301 anode; cathode -> power GND
                      |-- divider -> TL431 REF; TL431 anode -> GND
                      |-- QCB PNP emitter
TL431 cathode <- 500R <- QCB base (10k base-emitter)
QCB collector -> 100R -> SCR gate (1k gate-cathode)
```

PROPOSED threshold: TL431BIDBZR, upper divider **1.13 kΩ** =1 kΩ/0.1% +100 Ω/0.1% +30 Ω/1%, lower 1 kΩ/0.1%. Lower resistance limits the TL431 reference-input-current error. Nominal ideal trip `2.495 ×2.13=5.31435 V`; typical 2 µA reference current adds ~2.26 mV. The saved exact resistor offers are reused, avoiding an invented price for a single 1.13 kΩ part. These extra segments can be consolidated after one exact qualified offer is available.

KNOWN/CALCULATED: TL431 industrial B-grade has 2.483–2.507 V at 25°C, up to 34 mV full-range deviation, up to 4 µA reference current plus 2.5 µA deviation, and cathode-voltage dependence. Conservatively expand reference to 2.449–2.541 V; reserve another 8 mV reference reduction for cathode movement before PNP conduction. Upper-divider tolerance is ±1.4 Ω and lower ±1 Ω. Static range is about **5.193–5.426 V**, including up to 6.5 µA ×Rtop at the high end; round high to **5.430 V** for screening. Resistor TCR, actual cathode current during the analog transition, noise, gate-drive buildup and temperature range qualification remain OPEN. The TL431 reference table is characterized at 10 mA; this circuit's several-mA base drive requires checking actual threshold and dynamics. [TI TL431 §6.12](https://www.ti.com/lit/ds/symlink/tl431.pdf).

PROPOSED gate drive: TL431 sinks PNP base current; it cannot source an SCR gate directly. At 5.19 V with ASSUMED 0.2 V PNP saturation and 1.3 V gate voltage, 100 Ω supplies 36.9 mA, less 1.3 mA in the gate-cathode resistor =**35.6 mA**. A 500 Ω base resistor supplies approximately `(5.19−0.9−2.5)/500=3.58 mA`, a forced gain below 11 for ~37 mA. This is a feasible screening drive budget, not a guaranteed saturated-transistor or full-temperature trigger specification.

KNOWN: **TYN612RG is the 15 mA IGT grade**, not the 5 mA TYN612TRG. ST's 25°C maximum is 15 mA, gate maximum 1.3 V, holding maximum 30 mA and latching maximum 60 mA. Its temperature graph indicates increased cold trigger current, but supplies no tabulated guaranteed −40°C IGT maximum; using **30 mA** as a 2× cold screen leaves only ~5.6 mA drive margin and remains ASSUMED. Full-temperature gate-trigger current and total turn-on delay must be qualified or a guaranteed sensitive-gate replacement selected. The 35.6 mA drive exceeds 2×25°C IGT, but does not establish the specified fast gate rise or cold dI/dt condition. [ST TYN612 tables 1–3](https://www.st.com/resource/en/datasheet/tyn612.pdf).

CALCULATED fuse/SCR screen: F301 **0451007.MRL**, 7 A very fast, nominal cold 9 mΩ, melting I²t **10.32 A²s**; input F101 is **1.650 A²s**. TYN612RG TO-220 is **140 A/10 ms**, **145 A/8.3 ms**, **98 A²s**, at initial 25°C. Thus `1.65 <10.32 <98` is a useful nominal comparison. It does **not** prove coordination: maximum total clearing I²t (including arc), hot SCR derating, arbitrary waveform peak, dI/dt and repeated pulses are missing. At ASSUMED 50 A, nominal adiabatic melt times are 0.66 ms and 4.13 ms; source reservoir discharge through F301 bypasses F101. Never extrapolate melting I²t to long, low-overload operation. Output-capacitor discharge can exceed 140 A locally even with an upstream current-limited supply. [Littelfuse 451/453 tables](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1).

CALCULATED long-fault screen: after HS short, the source current flows through F101, Q101, the failed switch, L201, F301 and SCR; it is **not** multiplied by the old buck conversion ratio. An illustrative 24 V/2 A supply at 110% current limit gives 2.2 A: neither fuse is guaranteed to clear. At 3 A limit the input fuse is only at 100%; even 6 A permits up to five seconds for F101 by the series specification. Hiccup can repeatedly cool the fuse without opening it. No actual MEAN WELL part or its limit/hiccup waveform has been selected.

CALCULATED SCR sustained loss, using ST's hot on-state model `P≈0.85 I +0.030 I²`: **2.02 W at 2.2 A, 2.82 W at 3 A, 5.85 W at 5 A, 7.05 W at 6 A**. TO-220's nominal 60°C/W free-air figure gives ~169°C rise at 3 A; it cannot be left indefinitely without a thermal path. At an ASSUMED 50°C ambient and target junction ≤110°C, total thermal resistance must be ≤21.3°C/W at 3 A or ≤10.3°C/W at 5 A. Allow 1.3°C/W junction-case plus interface; a verified isolated sink around ≤15°C/W serves the 3 A screen only. Copper alone on a small board is not demonstrated to do so. Sink, tab potential, insulation, clearances and mounting remain OPEN; a 40,000 VND allowance enters first-build costing.

OPEN hold behavior: while SCR remains above holding current, Pi rail is near the SCR on-state voltage, below 5.5 V. Once the source hiccups off, SCR unlatches; the next pulse must be detected again and repeats the overshoot risk. At near-holding current, the detector-powered gate can also collapse. A fuse that never clears therefore requires both continuous thermal survival AND safe repetitive retriggering, neither established here. If F301 opens first, Pi is disconnected but raw 16 V capacitors can rise toward 24–28 V until F101 opens; that may never happen. Raw-bank containment is unresolved.

Advantages: cheapest output protection, low normal drop (~45 mV cold fuse, 0.225 W at 5 A), simple visible educational mechanism, no auxiliary rail. Lost functions: source shutdown, controlled inrush, reverse-current isolation, explicit manual fault memory and independent series isolation. Complexity/PCB: moderate discrete count, TO-220 and possible sink enlarge the board; very short SCR/capacitor ground loop with a Kelvin detector ground, separated from buck FB. SCR short holds rail low and stresses source/fuse; SCR/gate/PNP open or TL431/reference failure can remove protection. A false detector trip shorts the supply. TL431 REF-to-ground short can inhibit trip. A shorted output fuse removes intended isolation. No single-fault-tolerant safety claim.

Qualification: trip thresholds and nuisance response at temperature; cold gate-drive margin and dI/dt; 24/28 V HS-short injection into dummy load; probe actual Pi connector peak and SCR current; maximum clearing energy with stiff source; sustained 2.2/3/5 A and source hiccup tests with sink; output-fuse-first clearing and raw-cap containment; open/short detector/SCR faults. **BLOCKED as protection meeting the frozen ceiling.**

### Option 2 — one comparator/reference and one P-FET

```text
RAW5 -> QOV P-FET (source RAW5, drain PROTECTED5) -> R401 copper -> Pi
  |-- six raw capacitors                        |-- two local capacitors
  |-- TLV1701 supply, 100nF bypass
  |-- 1k bias chain -> TL431 fixed 2.495V reference -> GND
  |-- 1.13k/1k divider -> comparator IN+
reference -> comparator IN-
comparator open collector -> QOV gate; gate -> 10k -> source
12V zener cathode=source, anode=gate
```

PROPOSED: TLV1701AIDBVR, TL431BIDBZR and DMP4015SPS-13. Normal divider below reference makes comparator sink gate; OV releases it and the 10 kΩ source-gate resistor turns the FET off. The P-FET body diode is directed protected drain → raw source, so it blocks forward fault feed when off but permits reverse backfeed. No LTC7001, flip-flop or auxiliary rail is used. A back-to-back N-FET pair would need a charge pump/high-side drive not provided by this comparator alone and is not silently added.

CALCULATED reference feed: ten 100 Ω resistors in series give 1 kΩ, ~2.57 mA at 5.065 V and ~25.5 mA at 28 V, total dissipation ~0.65 W shared across ten parts. This exceeds TL431's 0.7 mA minimum; resistor hot-rating and reference thermal limits still need review. Comparator works over 2.2–36 V, with ±5.5 mV full-temperature offset. Fixed-reference divider gives an approximate **5.198–5.432 V** static screen including ±34 mV reference deviation, divider errors and comparator offset; use **5.450 V high** as an explicit engineering reserve, not a vendor guarantee. Reference current/load dependence, TCR and startup settling remain OPEN. [TLV1701 §§7.6–7.7](https://www.ti.com/lit/ds/symlink/tlv1701.pdf).

KNOWN/CALCULATED: P-FET is 40 V, RDS(on) max 15 mΩ at −4.5 V/25°C, gate charge typ 47.5 nC and Miller charge typ 13.5 nC under the cited test. Ideal cold drop at 5 A is 75 mV and loss 0.375 W; at ASSUMED 2× hot resistance these become 150 mV/0.75 W. However comparator output-low guarantee and gate drive near the low rail may not reach −4.5 V, so those losses are **conditional**, not qualified maxima. The FET requires SOA analysis during interruption/startup. [Diodes DMP4015SPS, saved DS35518 Rev 13-2](https://www.diodes.com/assets/Datasheets/DMP4015SPS.pdf).

CALCULATED timing defect: a 10 kΩ pullup at a ~2 V Miller plateau supplies only ~0.2 mA. `13.5 nC/0.2 mA≈67.5 µs` is a typical-charge order-of-magnitude screen. Comparator's ~0.56 µs typical release delay at **100 mV input overdrive** is neither maximum nor total gate isolation time. Reducing pullup to 1 kΩ still gives ~6.75 µs Miller time and raises normal sink-current/VOL problems. The common table's optimistic 5 µs already fails. Significant drain-source current persists while the gate slews; simple pullup turnoff is not acceptable for this fault window.

OPEN failure/behavior: startup may conduct before reference validity; no UV-valid latch, hysteresis or manual reset is present. Near threshold it can chatter or operate linearly. Supply collapse changes comparator output state. Comparator stuck-low, reference drift/high, lower-divider open or P-FET short defeats protection; P-FET open turns load off. A 12 V zener short forces off; open risks gate damage at fault. The 16 V comparator bypass and six raw MLCCs remain exposed to a 24–28 V HS short after isolation. Even without Pi damage, the board is not fault-surviving. A cheap SCR backup on RAW5 would add the `CROWBAR` 22,069 VND plus sink needs; it inherits Option 1 response/hold limitations and does not repair the slow series turnoff. It is not included in Option 2's three main totals.

Advantages: low component price and fewer controls than research V1A; no crowbar current in ordinary OV shutdown. Lost functions: reverse blocking, defined latch/reset, prequalified rails, fast gate driver and source shutdown. Complexity/PCB: compact SO-8/SMT with thermal copper; less board area than a sinked SCR, but analog gate timing/SOA is difficult. Test hot normal drop at 5 A, startup with slowly rising/falling source, reference/ground faults, reverse backfeed, turnoff under HS short, ringing and repeated threshold crossings. **PROPOSED disposition: reject this minimal implementation for the strict ceiling.** Adding an active fast turnoff stage would be another architecture/cost review, not evidence that this one passes.

### Option 3A — adjustable-OVLO eFuse alone

```text
RAW5 -> TPS259470LRPWR -> PROTECTED5 -> copper replacing R401 -> Pi
  | six raw caps          | two local caps
  |-- 34.2k/10k divider -> OVLO
  |-- 1k power-resistor chain -> EN/UVLO -> 3.3V zener -> GND
ILM -> 550R -> GND; AUXOFF low; FLT unused; ITIMER and dVdt open per configuration
```

PROPOSED exact part is **TPS259470L**, adjustable OVLO with current limiting; do not substitute TPS259472's fixed clamp. Its nominal ~5.74 V clamp can reach 6.2 V, incompatible with the ceiling. Low-voltage TPS2595x-class parts must not be assumed 28 V fault-tolerant. TPS259470 is stocked in the saved LCSC data at USD 1.2039, with integrated opposed FETs and controlled startup/reverse blocking. [TI TPS25947](https://www.ti.com/lit/ds/symlink/tps25947.pdf).

CALCULATED divider: top 33.2 kΩ +1 kΩ (0.1% each), bottom 10 kΩ/0.1%; 1.2 V nominal OVLO gives **5.304 V**. TI's 1.183–1.223 V threshold and ±0.1 µA leakage plus divider corners give **5.21735–5.41746 V**. At 28 V the OVLO pin sees ~6.335 V, below 6.5 V absolute but outside the normal recommended OVLO range. PROPOSED EN supply: ten 100 Ω resistors in series from RAW5 to EN, with **BZT52C3V3-7-F** cathode at EN/anode GND. At 5.065 V it supplies ~1.77 mA; at 28 V, ~24.7 mA with ~0.61 W resistor-chain and ~82 mW zener loss. The catalog 3.1–3.5 V specification at its test current is comfortably below 6.5 V pin absolute maximum, but the low-current knee and high-current dynamic clamp must be verified; no ordinary unclamped EN divider is fault-safe over the full range. This pin clamp is included in the BOM, with hot resistor derating OPEN. The eFuse dVdt/ITIMER configuration and startup behavior remain qualification items.

KNOWN/CALCULATED limitations: recommended VIN ends at **23 V**, absolute max is **28 V**. At 24 V fault there is absolute-rating room but operation is outside the recommended range; at 28 V fault there is zero positive tolerance/ringing margin. Required VIN−VOUT bound is 21 V below −10°C (22 V at warmer temperatures); after the load discharges, even a 24 V input exceeds this differential. Thus “abs max ≥28 V” satisfies only the brief's initial screening criterion, **not sustained HS-short survival**. The 1.2 µs OVLO response is typical, and the common fault model fails even at that typical time. Fast short-circuit response is a different condition and cannot be substituted for OVLO timing.

CALCULATED losses: typical ~28.2 mΩ gives 141 mV/0.705 W at 5 A; specified 45 mΩ maximum gives **225 mV/1.125 W**. At buck low static 5.006 V, only **31 mV** remains for harness, copper, connectors, ripple and transient before 4.75 V. This makes 5 A delivery especially difficult. A 550 Ω ILM chain (500+30+20 Ω/1%) approximates the 549 Ω table point, whose thresholds are 5.4–6.6 A; resistor tolerance shifts the range roughly to 5.34–6.65 A. That supports nominal 5 A but does not authorize sustained 6.65 A operation of the 5.5 A-rated device. ITIMER open means no intentional extended overload blanking; dVdt open uses its default ramp and requires inrush testing. No 50 V timing capacitor is hidden in the 5 V BOM.

OPEN failure modes: IC/series-FET short passes raw OV; detector failure has no independent backup. Open failure interrupts service. OVLO can release when voltage returns below its falling threshold; the `L` suffix must not be interpreted as manual-latching every OV event. Low-voltage raw capacitors are unprotected even after a successful isolation. Simple 24 V bus protection does not guarantee the eFuse's narrower differential or absolute limits.

Advantages: few parts, tiny package, current limiting and reverse blocking; easiest routing logically. Lost functions: independently powered fast precision detector, manual fault memory, raw-energy disposal and coordinated source shutoff. PCB difficulty: low part count but exposed-pad assembly and ~1 W dissipation require thermal vias/copper. Qualification requires max hot drop, pin clamps, startup, repeated OV, 24/28 V/differential survival, turnoff delay and shorted-pass-FET fault. **Rejected as sole Pi protection under the frozen fault criterion.**

### Option 3B — eFuse plus independent raw-side crowbar

```text
common input F101 -> buck failed HS -> L201 -> RAW5 -> eFuse -> Pi
                                              |        | local caps
                                        raw caps + SCR
                                              |
                                             GND
TL431/PNP detector senses RAW5; same CROWBAR parts as Option 1
No F301 between RAW5 and SCR: F101/upstream source must clear or remain safe.
```

PROPOSED: add the fully independent TL431/PNP/SCR assembly at **RAW5**, not only after the eFuse. This placement can clamp raw capacitors and eFuse VIN and provides a parallel response path if the eFuse pass FET fails short. It avoids an output fuse disconnecting the raw bank from its clamp. It adds 22,069 VND installed and the sink allowance; EN-pin-clamp qualification above still applies.

OPEN coordination: crowbar high trip ~5.43 V is above nominal eFuse trip, but threshold ranges overlap; either may act first. No guaranteed selective order is claimed. The raw crowbar can limit eFuse exposure if fast enough, but its calculated peaks and cold triggering still fail to demonstrate <5.5 V when the eFuse is shorted. If eFuse opens first, the Pi may be isolated, while source-side current continues into SCR. F101's nominal 1.65 A²s is below SCR's 98 A²s, with the same clearing/hot/repetitive caveats; there is no F301 to interrupt a sustained source-limited crowbar. The 2.2–6 A thermal and hiccup calculations from Option 1 apply in full.

Failure matrix: eFuse short + functioning crowbar gives only the unqualified crowbar envelope; SCR open + functioning eFuse leaves its voltage/differential/delay defects; SCR short forces source fault; detector failure can leave the raw bank exposed. Shared ground/copper failures can disable both. Startup must not put eFuse and crowbar into repeated retry. This offers better functional coverage for modest extra cost, but **redundancy does not prove either path meets the frozen ceiling**.

PCB/qualification: highest Lite area/assembly cost because it combines eFuse thermal land with SCR surge loop and sink. Run both single-path tests and deliberately short the eFuse pass path, open SCR gate drive, exercise source hiccup and verify raw-cap/eFuse differential voltage. **PROPOSED disposition: retain as comparison fallback only; not a qualified improvement.**

## Step 4 — removed-function ledger

**PROPOSED removal, not a CAD edit.** “Acceptable” below is conditional on the replacement test/limit; safety functions are not waived by affordability. All old reports and paused-layout evidence remain tied to their historical revision.

| REMOVED FUNCTION | WHY IT WAS PRESENT | WHY ACCEPTABLE IN V1A-LITE | WHAT LIMITATION OR TEST REPLACES IT |
| --- | --- | --- | --- |
| TPS26630 input current limit / timed overload | Electronic fault-current control | Only conditionally; fuse/source contract may replace wiring protection | Fuse clearing, input FET SOA, continuous current-limited fault; no electronic input current limit remains |
| TPS26630 controlled input ramp | Bound hot-plug/inrush | Conditional cost reduction | Cold/hot plug with actual input C/source impedance; no guaranteed inrush limiting |
| TPS26630 input UVLO and PGOOD gating | Qualified source before buck enable | Source is now nominal 24 V, but envelope still OPEN | New EN-divider threshold and brownout/restart tests; no claimed 18 V UVLO |
| Old input OVP and 60 V reverse-FET scheme | Isolate abnormal input/reversal | Original simplification is NOT acceptable after Addendum 2 | Replace with costed 100 V reverse + OV cutoff; 64 V continuous fault is mandatory |
| INPUT_SHDN / fault-driven input shutdown loop | Halt power after downstream fault | Conditional only; input OV cutoff senses input, not buck HS short | Output SCR sustained/hiccup/clearing tests; 24 V input fault feed is not automatically cut off |
| LTC7001 and original opposed output N-FET pair | Fast forward isolation / reverse blocking | Replaced differently in Options 1–3 | Option 1 has no series isolation before fuse clearing; Option 2 lacks reverse blocking; 3 has loss/differential-limit issues |
| Precision REF5025 / fast dedicated OV chain | Narrow trip window and rapid action | Lower-cost detector is educational, but not yet electrically acceptable | New full-temperature threshold + delay budget and measured Pi-pin peak <5.5 V |
| UCC27511-driven MOSFET disposal branches and ballast banks | Controlled raw/load energy disposal | Replace only with a qualified SCR path | SCR gate, pulse, copper, fuse and continuous cooling tests; Option 2/3A raw disposal absent |
| Large 8×470µF raw +4×470µF protected bank | Hold-up and fault/transient energy buffer | Smaller bank saves size/cost, conditional on performance | Effective-C qualification, load release, startup, loop margin and HS-short rerun; old 100 A L/C model invalid |
| LT4363/FDB33N25/LTC3115/L350 auxiliary chain, hold rail, DET5/SAFE5/3V3_AUX | Keep protection alive through fault/rail decay | New output detectors use their observed rail; input uses a small HV-fed clamp supply | Rail-startup/brownout and detector supply-collapse tests; no stored auxiliary hold-up guarantee |
| Main/series ARM, RESET, fault latches, debounce and manual-valid logic | Explicit sequencing and persistent fault memory | Simpler operation desired | SCR only latches while holding current exists; other options may retry; no equivalent manual lockout claim |
| Guarded analog switches, rail supervisors and PG qualification | Avoid undefined comparisons/back-powering | Conditional simplification | Startup/reference-valid tests; a comparator alone does not establish fail-safe sequencing |
| SW_HIGH / VIN_GOOD_FAST and source-contact fixture | Observe source conditions / inject manual fault | Reduced educational fixture count | Keep accessible input/SW/raw/protected/gate/GND pads; separate external fault injector. Old manual contact was not autonomous detection |
| INA228 V/I/P/energy and ALERT | Telemetry and diagnostics | Explicit owner removal | External DMM/electronic-load/current-probe measurements; no firmware telemetry or energy claim |
| R401 2mΩ Kelvin shunt + input RC network | Accurate series current sensing | Explicit owner removal; avoids 10mV/50mW at 5A | **Continuous rated copper from VOUT_PROTECTED to LOAD_5V1**; no floating output path, no calibrated on-board current measurement |
| Sheet04 local TPS70933 rail / decoupling | Power telemetry independently of host logic | No telemetry remains | Remove its load from power budget; do not reuse this removed rail for OVP |
| TCA9517, I2C pullups and J503 endpoint | Host isolation/level translation | No on-board I2C function remains | Remove J503 or mark unused in future capture; host must supply its own pullups elsewhere |
| Custom removable force links and research fixture headers | Isolate and inject faults by block | Continuous copper is simpler and lower loss | Retain etched sense/test pads and external fused injection fixture; no unpriced custom straps in core BOM |
| Oversized 90A-class inductor / 50V output MLCCs | Very stiff old fault envelope / raw voltage exposure | Cost-down requested, but fault containment NOT established | New Isat, saturated L, raw-cap fault and thermal tests; cannot claim these rating reductions are qualified |
| Research board connectors/harness implementation | Defined high-current force/host interfaces | New small board requires fresh interface selection | Costed connector planning below; no automatic carryover of legacy mating/hot-resistance PASS |

PROPOSED retained educational/test access: VIN_RAW, S_COMMON, VIN_BUCK, SW, RAW5, PROTECTED5, both input FET gates, detector/reference nodes, SCR gate and local grounds. Etched pads cost no separate purchased component, but PCB area is included. Keep raw and protected labels distinct. No USB 3.x/D435i data goes through this board.

PROPOSED copper/ground screen: a 50 mm, 5 mm wide, 35 µm copper trace is ~4.93 mΩ at 20°C, dropping ~24.6 mV and dissipating ~123 mW at 5 A per conductor. A similarly long return doubles that. This resistance example is not a temperature-rise/current-capacity certification; use short wide pours on both layers, avoid necks/fuse-pad constrictions, qualify vias and connector returns. Route SCR surge ground directly to its capacitor/power return, sense the load rail and quiet ground separately, and keep buck dual hot loops per TI. New high-voltage input copper, TO-220 tabs and optional sinks need spacing and insulation review.

CALCULATED low-rail budget, before dynamics: buck static low 5.006 V minus Pi minimum 4.75 V allows total path resistance **51.3 mΩ at 5 A**. Option 1's 9 mΩ nominal cold fuse leaves ~42.3 mΩ for hot fuse increment, copper, contacts and cable; Option 2's conditional 30 mΩ hot FET screen leaves ~21.3 mΩ; Option 3's 45 mΩ max leaves ~6.3 mΩ. Two connector contacts and a realistic cable can exhaust these budgets. Exact harness length/gauge/contact temperature must be specified; remote-sense compensation must not be added without repeating the OV budget.

## Step 5 — three totals per option, including Addendum 2

**CALCULATED planning currency: 1 USD =26,500 VND**, retained from Phase A; this is an accounting assumption, not a market exchange quote. A/B use installed extensions from the saved **LCSC** core-part prices, not Mouser substitutions. Where MOQ exceeds 10, the strict quantity-10 column says OPEN and the installed estimate uses the actual lowest published MOQ tier, explicitly identified. Zero stock is never described as available stock. Core scope includes the full reworked buck, mandatory 64 V cutoff/reverse/TVS stage, eight output MLCCs and chosen output protection.

**A** = installed core electronic components. **B** = A + one allocated bare board + installed input/output connectors and mates. **C** = actual minimum-lot purchasing model for one assembled prototype with reasonable spares, plus first-order overhead. C is not A×a convenient percentage. Model [source/parts](PHASE_B_PARTS.json), [purchase lines](PHASE_B_PURCHASE_MODEL.csv), [exact totals](PHASE_B_TOTALS.json) and [reproducer](calculate_phase_b.py) are delivered beside the BOM.

ASSUMED board: **80×60 mm, two layers, 1 oz copper, 1.6 mm FR-4**, five bare boards in one order, 53,000 VND total /10,600 VND allocated per board. This fits the cited JLCPCB ≤100×100 mm entry offer; it is not a configured fabrication quote. No routing/thermal proof says two layers suffice. A four-layer/2 oz/special-process change, extra heat sink or paid rework must be recosted. [JLCPCB public offer](https://jlcpcb.com/ads/pcb-prototype).

PROPOSED connector price baseline: two JST B2P-VH-FB-B headers, two VHR-2N housings and four SVH-41T-P1.1 contacts, **23,686 VND installed**. Use distinct clear input/output marking and error-proof the harness; identical mates could be interchanged. Family current ratings depend on wire/header combination, not merely “VH”; exact mating and hot contact resistance remain OPEN. Required Pi fanout uses both 5 V pins and the project ground interface, with cable length/gauge and crimp workmanship to be qualified. No USB-C PD negotiation or USB data routing is included.

KNOWN/CALCULATED purchasing penalty: saved exact contact offer has **100-piece minimum**, stock OPEN, so C charges all 100 contacts rather than four. Headers are bought in a five-piece lot; buy three housings for two installed plus one spare. This costs **263,503 VND** for connector procurement, using the archived LCSC/DigiKey offers. Price freshness, alternate small-lot availability and delivery are OPEN. A local verified small-lot harness could reduce C materially, but no invented local offer replaces this evidence.

ASSUMED spares: for each exact core MPN, buy installed quantity plus `max(1, ceil(25%×installed))`, then round up to saved MOQ. Use the actual price break at that purchase quantity. MOQ is provisionally used as the order increment; the supplier's reel/package count is **not** mistaken for a required order multiple. Verify cut-tape increments before purchase. This provides a spare buck, inductor and protection semiconductors; high-MOQ passive surplus is fully charged to this first build. No purchase was placed.

| C overhead beyond core purchasing | VND / first build | Basis / scope |
| --- | --- | --- |
| Connector minimum lots | 263,503 | Archived exact offers above; stock OPEN |
| Five-board bare-PCB minimum | 53,000 | ASSUMED public entry-price estimate |
| Wire, Pi fanout termination and strain relief | 35,000 | ASSUMED allowance; exact harness quote OPEN |
| Shipping, import/tax/handling reserve | 180,000 | ASSUMED planning allowance across parts/PCB; no landed quote |
| Assembly/consumables | 50,000 | ASSUMED manual assembly using existing lab reflow/tools; service quote OPEN |
| Miscellaneous/rework contingency | 50,000 | ASSUMED reserve, cannot substitute for missing safety components |
| SCR sink/insulation/mounting | 40,000 for 1/3B | ASSUMED 3A sustained-fault thermal screen; exact sink and 5A case OPEN |

Upstream converter, battery, Pi, bench supply, load, scope and probes are assumed already owned/borrowed. Purchasing them would increase C and is not concealed in component cost. Thermal hardware for the new input FETs is not proven unnecessary; if testing requires it, add its actual cost. Normal input loss may raise input current beyond the old 1.574 A buck-only estimate: use at least **1.65 A as a preliminary total-stage screen** and recompute efficiency/temperature after measuring losses.

| Option (all include 64 V input cutoff) | A core PCB BOM | B core + PCB + required connectors | C first build with spares/minimum lots | Hard <1,000,000 VND result |
| --- | ---: | ---: | ---: | --- |
| 1 — output fuse + SCR | **273,602** | **307,888** | **1,465,748** | FAIL; exceeds by 465,748 |
| 2 — minimal comparator/P-FET | **294,667** | **328,952** | **1,444,517** | FAIL; exceeds by 444,517 |
| 3A — eFuse alone | **284,724** | **319,010** | **1,421,330** | FAIL; exceeds by 421,330 |
| 3B — eFuse + raw crowbar | **306,793** | **341,079** | **1,520,102** | FAIL; exceeds by 520,102 |

**OPEN / budget requirement unmet:** all installed core estimates are below the preferred 500k upper target, but none of these evidenced first-build procurement models satisfies Addendum 2's hard whole-prototype ceiling. It would be misleading to report A or B as the whole first prototype. A minimum-lot supply plan is also not a complete available quote because TVS3300DRVR, MMBTA42-TP and connector contacts lack confirmed stock.

CALCULATED procurement-only sensitivity: eliminating all connector lot overbuy would save ~239,817 VND; Option 1 C would still be ~1,225,930 VND. Eliminating the spare inductor saves another ~30,292 VND but still does not meet the ceiling. Shared laboratory stock/group purchasing, a cheaper fully specified harness and an actual consolidated landed quote are meaningful next cost levers. Their savings are **not booked** without evidence, and cheaper procurement cannot repair the electrical blockers. The brief's “stay under” requirement is therefore reported as BLOCKED rather than asserted through unsupported allowances.

## Step 6 — proposed pick, risks and gate handback

**PROPOSED pick for the next engineering iteration: Option 1 (output fuse/SCR) with the mandatory discrete 100 V input cutoff/reverse stage. Claude and the owner decide; this is not approval to build or connect a Pi.** It has the lowest installed cost and smallest normal output loss, retains the educational LM61460 block, and makes fault-current and fuse coordination observable. The input series cutoff is preferable to forcing the uncertain upstream source/battery to clear an input SCR fuse. Option 2's passive gate turnoff is too slow; Option 3A adds a narrow voltage/differential envelope and substantial 5 A drop without a backup. Option 3B improves raw-bank coverage, but adds both loss and cost while retaining unqualified timing.

**DECISION / OPEN: no option currently meets all requirements.** Do not choose a build-ready winner merely because its installed BOM is cheap. The mandatory <1 million VND first-build budget is unmet by the recorded minimum-lot model, and no candidate establishes Pi-pin peak <5.5 V or validated continuous 64 V input disconnection. R1 comparison is delivered; R1 selection/release, R2, R3 and fabrication remain BLOCKED.

| Priority / OPEN RISK | Consequence / required evidence before selection |
| --- | --- |
| 64 V input turnoff and hot SOA | Obtain battery/UENPO fault impedance, capacitance and current envelope; prove VIN_BUCK peak and sustained off-state at 54.6/64 V, including cold startup and gate-driver faults. A 100 V marking alone is insufficient. Resolve 26/28 V normal conflict. |
| Strict Pi <5.5 V | Common HS-short screens fail even optimistic timings. Need guaranteed/characterized detector-to-current-extinction envelope, a faster protection path and/or larger qualified C; repeat false-trip budget simultaneously. |
| Raw-side 16 V capacitors | Option 1 must prevent output-fuse-first clearing from leaving the bank at 24–28 V; Options 2/3A need a raw-side containment path. Option 3B's raw clamp is a direction, not proof. Lower-rated parts cannot be waved through because normal output is 5 V. |
| SCR non-clearing fault | Cold IGT maximum, gate establishment, clearing I²t, hot ITSM and dI/dt missing. A 2.2–3 A current-limited/hiccup source may never open a fuse; qualify continuous cooling and every restart pulse. |
| 5 A undervoltage/thermal | Validate true effective C, closed-loop response/margins, connector/harness resistance and hot losses. At 1.65 A input the two-input-FET 2× hot-resistance screen is ~1.27 W, additional to buck loss. |
| Procurement and whole-build cost | TVS and HV NPN stock OPEN; exact contact offer requires 100 pieces and stock OPEN. Obtain smaller-lot/shared-stock evidence and landed quote; all savings must be counted honestly. |

PROPOSED qualification order after architecture review: visual/pin/package/polarity inspection; continuity/short checks; current-limited bench supply; no-load startup; verify all rails and input cutoff; low-current dummy load; rising 0–5 A load; thermal and ripple measurements; load-step/loop checks; protection/fault tests using an energy-bounded external injector; repeat continuous input fault and source hiccup tests; record telemetry as **removed / not applicable**; Pi integration only after preceding gates pass. Start with a dummy load, never the expensive SBC. Fault tests must include source energy and measurement bandwidth, differential Pi-pin and buck-input probing, hot/cold corners and repeated events, not only a slow DC trip sweep.

KNOWN delivery: documentation and calculation artifacts only. No schematic, PCB, library, upstream manufacturer file, manufacturing order or purchase changed; no push. New ERC/DRC is not applicable because CAD is unchanged. Existing historical ERC/DRC reports do not validate Lite. [Source register](../../../third_party/v1a_lite_phase_b/SOURCES.md) records URLs, revisions, access dates, relevant files, reference-only reuse, copyright/attribution and retrieval gaps.

KNOWN Git limitation: section commit attempts for resumed buck review, input review, output/Addendum 2 comparison, removal ledger and totals all failed with `Unable to create .../.git/worktrees/wt-litephb/index.lock: Operation not permitted`. As instructed, files remain uncommitted; no permission workaround or push. HEAD remains `db2a88c`. Completion-section commit is also attempted in the final verification record.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
