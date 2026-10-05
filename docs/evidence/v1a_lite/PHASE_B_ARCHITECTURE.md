# V1A-Lite Phase B — costed architecture comparison

**2026-10-04 — PROPOSED, analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Scope, evidence and interpretation

KNOWN: follows the complete Phase B brief and its lead-architect addendum, including the revised report name and option definitions. Worktree `wt-litephb`, branch `docs/v1a-lite-phase-b`, starting commit `cd18b2bdbdd13b77ca3200b49ba517d92b84ecd1`. [Phase A](PHASE_A_AUDIT.md) and its complete CSV were read. No schematic, PCB, library, upstream reference source or historical evidence is changed. No purchases or push. Work is performed directly without sub-agents.

KNOWN owner requirements: 18–28 V assumed normal auxiliary bus, upstream 13S-to-24 V converter outside this design; retain LM61460; 5.1 V-class, 5 A Pi 5 supply; independent hardware output OV protection; fuse/TVS/reverse input protection; remove Sheet 04 with a copper replacement for R401. Preferred installed core cost 300–500k VND, whole first prototype strictly below 1 million VND. Priorities are affordability, Pi survival, output capability, education, then PCB simplicity.

KNOWN: use the project's frozen **Pi-pin peak <5.5 V and minimum 4.75 V**, not a newly inferred Raspberry Pi damage specification. [Decision log](../../context/06_DECISION_LOG.md) records the strict inequality and no permissible overvoltage duration. No transient above 5.5 V is excused because it is short. Exact source current limit, hiccup timing, reservoir capacitance, wiring impedance, ambient range, surge waveform and Pi harness/interface remain OPEN.

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

## Step 2 — simple input protection

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

KNOWN delivery: Step 1 commit attempt failed creating the worktree `index.lock` with “Operation not permitted.” Files remain uncommitted as instructed. Step 2 and subsequent steps will be attempted independently; no permission workaround or push.
