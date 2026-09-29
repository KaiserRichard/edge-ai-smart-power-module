# J501 / J502 / J503 connector shortlist

2026-09-29 — Brief 04 continuation 1, updated for user requirement freeze **D-30**. **RECOMMENDATION FOR REVIEW. No connector selected.**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED. R2 and R3 remain BLOCKED.** This is a review packet for the user's brother and acting Codex conductor. It adds no ports, footprints, circuitry or procurement decision and does not close an engineering gate.

## Scope and evidence basis

**OBSERVATION:** the [current engineering state](../../../context/03_ENGINEERING_STATE.md) and [previous connector review](../forensic_2026-09-14/CONNECTOR_HARNESS_QUALIFICATION.md) leave all three parts and their harnesses OPEN. This shortlist freshly checks the two existing power systems and both signal systems; each power system is an alternative for either power connector, subject to the pairing restriction below. There are **two candidates for each reference**, not permission to fit the same power family twice.

| Interface | REQUIREMENT: existing circuit numbers | Analysis envelope; status |
| --- | --- | --- |
| J501 input | 1 `VIN_RAW`, 2 `GND` | **KNOWN requirement:** normal 9–24 V input from the future auxiliary converter; capability unvalidated. Historical 24.72 V case remains **ASSUMED** only. |
| J502 output | 1 `LOAD_5V1`, 2 `GND` | About 5.1 V, **KNOWN designed 5 A target**, capability unvalidated. Historical 6 A for ≤100 ms remains **ASSUMED screening**, not a user-confirmed mode. |
| J503 Inter-Integrated Circuit (I2C) | 1 `GND`, 2 `3V3_HOST`, 3 `SDA_HOST`, 4 `SCL_HOST` | Host-referenced 3.3 V interface; pin 2 is a reference/supply **input**, not `3V3_LOCAL` output |

**CONTEXT — D-30 controls:** the updated durable `lab/REQUIREMENTS.md` confirms Pi power through the **GPIO 5 V power pins and multiple GND pins**. GPIO means general-purpose input/output. Required runtime scope is Pi 5 idle, sustained CPU-heavy operation, and **Pi 5 with D435i operating**, with representative steps up to the designed 5 A envelope. That envelope includes all intended loads drawing through V1A; it is not an extra camera/peripheral allowance. Arbitrary peripheral hot-plug is not guaranteed. D435i mode, power route, inrush and load-step slew remain to be characterized; its data does not route through this PCB.

The upstream source is a future auxiliary converter; **no final wall adapter is required**. Normal 9–24 V is a known requirement, not a demonstrated rating or fault limit. Converter identity, abnormal voltage/time bounds, current-limit response, capacitance and wiring impedance remain OPEN. Historical Mean Well-derived 24.72 V and hot-plug cases do not specify that converter. Ambient 0–40 °C, natural convection and open-bench use remain assumptions. The confirmed **5.5 V maximum at the Pi rail, with margin** remains in force, with the full fault envelope OPEN. **J502/harness remains OPEN pending resistance, current, retention and mechanical qualification.** The updated external context's SHA-256, exact path and earlier read identity are retained in [source_register.json](source_register.json). No USB-C redesign, connector selection or KiCad edit follows from D-30.

**EVIDENCE:** source IDs S1–S8 and installed-library IDs K1–K4 in that register identify URLs, revisions where printed, hashes where recovered, sections, limitations, reuse and attribution. Manufacturer documents are referenced, not copied into this report. Original downloads remain in the ignored `third_party/documents/connectors_2026-09-29/` cache. Unversioned product pages are dated evidence, not immutable specifications. No measurements were made.

## Power candidate systems shared by J501 and J502

### P-VH — JST shrouded VH, two circuits

**EVIDENCE [S1]:** [manufacturer VH catalog](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), PDF pp1–4. Exact header **`B2P-VH-FB-B`**, housing **`VHR-2N`**, and **two `SVH-21T-P1.1`** crimp contacts. Header catalog labeling includes `(LF)(SN)`; retain the exact base part and finish when ordering. `VHRR-2N` is explicitly incompatible with this two-position shrouded header.

| Requested property | Published value or explicit gap |
| --- | --- |
| Current per circuit/contact | **7 A AC/DC with AWG18 and the shrouded header**. The standard-header 10 A/AWG16 figure is inapplicable to this candidate. |
| Temperature/current condition | −40 to +105 °C **including current-induced temperature rise**. Rating-test ambient and an exact current-versus-ambient curve are **OPEN**; 7 A at 40 °C ambient is not established. |
| Voltage | 250 V AC/DC catalog rating |
| Contact resistance | Mated contact: ≤10 mΩ initial; ≤20 mΩ after test. Test conditions and hot maximum need the controlled specification. |
| Exact contact wire range | AWG22–18, 0.33–0.83 mm²; insulation outer diameter 1.7–3.0 mm |
| Pitch / geometry | 3.96 mm; header body 9.8 × 9.7 mm, 11 mm high above board; catalog mated height about 16.5 mm, depth 10.5 mm. K1 courtyard 10.82 × 10.70 mm. |
| Polarization / retention | Shroud and asymmetric housing orientation; positive housing lock. No secondary retainer on this exact pair. |
| Mating cycles | **OPEN:** no numerical cycle specification found in the public catalog. Do not assign the common unsourced “30/50 cycles” figure. |

**OPEN RISK:** full 5 A and 6 A flow through **each** polarity contact; two positions do not share the current. Current margin does not resolve voltage loss, hot contact temperature, crimp quality, vibration or fault withstand. JST's [handling precautions, PDF p4](https://www.jst-mfg.com/precaution/eP-Handling.pdf) [S7] prohibit live disconnection. Live insertion and controlled contact sequencing are not established. Treat this candidate as **power-off mating/unmating only** for the proposed review configuration.

### P-PC — Phoenix Contact COMBICON, two circuits

**EVIDENCE [S4/S5]:** header **`1757242` / `MSTBA 2,5/ 2-G-5,08`**, mating screw plug **`1757019` / `MSTB 2,5/ 2-ST-5,08`**. Contacts are integral: **no separate crimp contact or empty housing**. Manufacturer technical datasheets are the [header product record](https://www.phoenixcontact.com/en-us/products/pcb-header-mstba-25-2-g-508-1757242) and [plug product record](https://www.phoenixcontact.com/en-de/products/pcb-connector-mstb-25-2-st-508-1757019); the latter explicitly lists `1757242` as a mate. A downloadable PDF was not recovered.

| Requested property | Published value or explicit gap |
| --- | --- |
| Current per circuit/contact | 12 A nominal for each part; not a 24 A two-position path |
| Temperature/current condition | Operation −40 to +100 °C **dependent on derating**. Exact two-position pair/AWG18 curve at 40 °C **OPEN**, as is nominal-rating test ambient; 12 A over the entire temperature range is not claimed. |
| Voltage | 320 V rated at overvoltage category III / pollution degree 2; complete-pair III/3 limit is 250 V from the plug. These are not DC switching ratings. |
| Contact resistance | Header 1.4 mΩ; plug 1.3 mΩ. Durability test header R1/R2 = 1.4/1.4 mΩ; plug R1/R2 = 1.3/1.4 mΩ. Exact reference planes **OPEN**. |
| Wire termination | Plug: AWG24–12; flexible or rigid 0.2–2.5 mm²; 7 mm strip; 0.5–0.6 N·m screw torque. Ferrule-compatible ranges 0.25–2.5 mm²; any ferrule/tool pairing remains to be specified. |
| Pitch / size | 5.08 mm. K2 board body outline 12.16 × 12.00 mm; courtyard 13.17 × 13.00 mm. Manufacturer plug dimensions 10.16 mm width × 18.3 mm length × 15 mm height; do not add overlapping plug/header lengths to invent a mated envelope. |
| Polarization / retention | Polarized mating profile; no distinct voltage coding between two identical pairs. **No positive locking mechanism** on these exact parts. Screw clamp holds the wire, not the plug in the header. |
| Mating cycles | Manufacturer durability/insertion-withdrawal evidence: **25 cycles**. This is the documented test exposure, not unlimited field life or an energized-cycle rating. |

**OPEN RISK:** one contact per polarity carries full current. The catalog resistance terms may include overlapping measurement paths; their sum is not a guaranteed mated-pair maximum. The plug record prohibits insertion/removal while energized or loaded [S5]. Harness strain relief and retention must be reviewed; the catalog vibration test does not qualify the module's unspecified installation.

## J501: two input alternatives

| Candidate | Complete termination | J501-specific assessment |
| --- | --- | --- |
| **J501-A: P-VH** | `B2P-VH-FB-B` + `VHR-2N` + 2 × `SVH-21T-P1.1` | Latching input candidate; use with P-PC output to distinguish voltage domains. AWG18 example fits the exact contact. Input voltage loss needs evaluation at the actual source minimum. |
| **J501-B: P-PC** | `1757242` + `1757019`; integral screw/socket contacts | Easier bench wire termination and lower catalog resistance; no plug latch. Requires a different output family, here P-VH, whose output voltage-drop screen is weaker. |

**CALCULATION, not input qualification:** ignoring connector loss initially, `Iin = Vout × Iout / (Vin × efficiency)`. At the 5 A design target, assumed 5.1 V setpoint, known 9 V normal-input corner and **assumed 85% efficiency**, Iin ≈3.33 A; the historical 6 A load screen gives ≈4.00 A. The retained **historical assumed 24.72 V** case gives ≈1.21 A and 1.46 A; it is not the normal-input maximum or the future converter's tolerance. Efficiency, source sag and losses ahead of the buck remain OPEN. J501 carries converter input current, not automatically the full output-current figure.

At the 3.33 A input example, P-VH's 40 mΩ after-test room loop gives about 133 mV / 0.444 W; at 4 A, 160 mV / 0.640 W. P-PC's **assumed additive** 5.6 mΩ loop gives 18.7 mV / 0.062 W and 22.4 mV / 0.090 W. These exclude wire, crimp/solder terms and heat effects; they are lower-order screens, not a self-consistent constant-power/source-sag solution. Both also need inrush, bounded upstream fault current, F101 coordination and contact-temperature review.

**OPEN operating procedure:** D-30 leaves source startup/transients and wiring impedance unbounded; it does not freeze the historical adapter hot-plug assumption as a requirement. Neither shortlisted board interface is qualified for energized mating/unmating. Review de-energized servicing with capacitors discharged; if live plugging becomes required, reopen interface qualification. Input eFuse behavior cannot by itself grant a connector a switching rating.

## J502: two output alternatives and the complete current path

| Candidate | Complete termination | J502-specific assessment |
| --- | --- | --- |
| **J502-A: P-PC** | `1757242` + `1757019`; integral screw/socket contacts | First candidate to qualify for voltage-drop reasons; conditional on retention, resistance reference planes and hot derating. Pair with P-VH input. |
| **J502-B: P-VH** | `B2P-VH-FB-B` + `VHR-2N` + 2 × `SVH-21T-P1.1` | Positive latch, but published resistance maxima consume much of the 5 V budget. Pair only with different-family input. Does not clear the full-path screens below. |

**REQUIREMENT:** evaluate the entire positive and return path:

```text
LM61460 regulation point -> output disconnect (OPEN) -> PCB copper/vias
 -> R401 -> J502 header + mate + terminations -> positive harness wire
 -> load-end adapter/contacts -> load rail
 -> load ground/contacts -> return wire -> J502 ground pole -> PCB return
```

The current schematic's open output-protection boundary means this is a **future path model**, not a functioning assembled system. **GPIO power entry with multiple grounds is confirmed by D-30**; the exact socket, branch wiring and mechanical implementation remain OPEN. The two-contact-per-polarity example below is a historical resistance allocation, not a frozen ground-pin count or demonstrated current sharing.

**EVIDENCE [S6]:** [Belden 8522 datasheet](https://catalog.belden.com/techdata/EN/8522_techdata.pdf), rev 0.482, 2026-02-20, pp1–2. Example wire stocks are red `8522 002100` and black `8522 010100`: AWG18, 16×30 tinned copper, nominal 2.0 mm insulation diameter, nominal 6.5 Ω/1000 ft direct-current resistance, −40 to +80 °C. They fit the candidate VH contact's stated gauge/diameter and Phoenix conductor range. Belden's 16 A figure is for **one conductor in free air at 30 °C**, not a bundled installed harness.

**ASSUMPTIONS:** retain the [historical full-path allocations](../forensic_2026-09-14/PI_POWER_DELIVERY_REFINED.md) to make the candidate comparison traceable. These are neither final component choices nor maximum resistance guarantees.

| Full-loop term | Screen (mΩ) | Basis and omitted qualification |
| --- | ---: | --- |
| Future output disconnect | 10.000 | ASSUMPTION; architecture and hot resistance OPEN |
| PCB positive and return copper/vias | 5.000 | ASSUMPTION; layout/thermal verification OPEN |
| R401 shunt | 2.000 | Nominal captured value; tolerance/TCR omitted here |
| Terminations and adapter joints not demonstrably included elsewhere | 5.000 | ASSUMPTION; define reference planes so crimps, solder and clamp joints are neither omitted nor counted twice |
| Pi GPIO contacts and unresolved harness/interface resistance | 10.000 | ASSUMPTION; historical example uses two 10 mΩ contacts in parallel per polarity (5+5 mΩ), equal sharing unverified. GPIO 5 V/multiple-GND entry is fixed; exact contacts, ground count and branch resistance remain OPEN. |
| AWG18 positive + return wire, 0.2 m one-way | 8.530 cold / 9.871 hot | CALCULATION from nominal DCR, assumed 20 °C reference and 60 °C hot wire, copper coefficient 0.00393/°C |
| J502 pair, both polarities | See next table | Catalog values or explicitly assumed sensitivity |

The fixed subtotal excluding wire/connector is **32 mΩ**. Durable requirement P8 describes a newer conditional 6.5 mΩ disconnect allocation; achieving it instead of 10 mΩ reduces total drop by 17.5 mV at 5 A or 21 mV at 6 A. This shortlist does not adopt that architecture or replace the historical allocation. The shunt's documented upper screen 2.02379 mΩ at an assumed 100 °C would add only about 0.119 mV at 5 A, but still belongs in a released budget. All downstream interface uncertainty remains.

### Connector-only contribution

`Vdrop = I × Rloop`, `Ploss = I² × Rloop`, and pulse energy `E = I² × Rloop × 0.100 s`.

| J502 case | Both-pole loop (mΩ) | Drop at 5 A (mV) | Heat at 5 A (W) | Drop at 6 A (mV) | Heat at 6 A (W) | Energy during 6 A / 100 ms (J) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| VH initial room resistance maximum | 20.00 | 100.0 | 0.500 | 120.0 | 0.720 | 0.0720 |
| VH after-test room resistance maximum | 40.00 | 200.0 | 1.000 | 240.0 | 1.440 | 0.1440 |
| VH after-test × assumed 1.3 hot factor | 52.00 | 260.0 | 1.300 | 312.0 | 1.872 | 0.1872 |
| Phoenix additive after-test screen | 5.60 | 28.0 | 0.140 | 33.6 | 0.202 | 0.0202 |
| Phoenix additive × assumed 1.3 hot factor | 7.28 | 36.4 | 0.182 | 43.7 | 0.262 | 0.0262 |

**CALCULATION limits:** VH uses `2 × 10` or `2 × 20 mΩ`, once per mated pole, not once for each half. Phoenix uses `2 × (1.4 + 1.4) mΩ` as an **additive hypothesis**: manufacturer R1/R2 entries are not independent extra series resistors. The exact mated measurement path may overlap between the header and plug figures. **The 1.3 multiplier is an assumed sensitivity, not a manufacturer temperature law.** Room-resistance cases must not be read as hot-resistance bounds.

### Full path at 5 A and 6 A

**CALCULATION:** all rows below use the **hot wire** 9.871 mΩ and fixed 32 mΩ subtotal. The retained low static source screen is 5.03827 V (approximately the lab's 5.04 V); it is calculated historical context, not a guaranteed regulator corner. Exact arithmetic, inputs and formulas are in the source register.

| J502 case | Total loop (mΩ) | Total drop at 5 A (mV) | Load V at 5 A | Total drop at 6 A (mV) | Load V at 6 A | Load V at 6 A with assumed extra 100 mV droop |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| VH initial room R + hot wire | 61.871 | 309.4 | 4.7289 | 371.2 | 4.6670 | 4.5670 |
| VH after-test room R + hot wire | 81.871 | 409.4 | 4.6289 | 491.2 | 4.5470 | 4.4470 |
| VH after-test hot sensitivity | 93.871 | 469.4 | 4.5689 | 563.2 | 4.4750 | 4.3750 |
| Phoenix additive after-test + hot wire | 47.471 | 237.4 | 4.8009 | 284.8 | 4.7534 | 4.6534 |
| Phoenix additive hot sensitivity | 49.151 | 245.8 | 4.7925 | 294.9 | 4.7434 | 4.6434 |

The first VH row differs from the historical table, which paired initial contact resistance with **cold** wire. The thermal assumptions are stated separately here to avoid mixing that result with a hot-wire comparison. Total dissipation in the hot-sensitivity rows is 2.347/3.379 W (VH) and 1.229/1.769 W (Phoenix) at 5/6 A; these losses are distributed across the modeled chain, not all in the connector.

**DECISION SCREEN:** using 4.75 V only as the retained operating-floor screen, total permissible resistance is `(5.03827 − 4.75)/5 = 57.654 mΩ` at 5 A or 48.045 mΩ at 6 A. Reserving an **assumed** 100 mV droop reduces those budgets to 37.654/31.378 mΩ. Phoenix's hot sensitivity clears the 5 A static screen but misses the 6 A static and both droop-reserved screens; VH misses them. The 6.5 mΩ disconnect proposal alone does not close either dynamic screen. No whole-path candidate is qualified for 5 A delivery or the peak.

**OPEN RISK — historical peak screen:** 6 A/100 ms is retained for analysis and is **not a user-confirmed performance guarantee**. It is below the nominal 7 A/12 A catalog figures, but no exact installed 40 °C current qualification or pulse evidence was recovered. Resistive drop occurs immediately during the pulse. Energy alone cannot predict contact temperature without thermal impedance, and a peak starting from a hot 5 A equilibrium is not a cold pulse. If repeated with duty fraction D, the simple resistive root-mean-square current screen is `sqrt(25 + 11D) A` for a 5 A baseline; repetition, capacitance, source dynamics, protection response and permissible rail droop remain OPEN. A downstream capacitor's contribution requires a separate transient model, not an assumed exemption for connector current.

## J503: two signal alternatives

**EVIDENCE:** [XH catalog](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf) [S2], pp1–5, and [PH catalog](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) [S3], pp1–3. Preserve circuit numbers from the **connector mounting-side view**; a cable mating-face view is mirrored.

| Property | J503-A: JST XH | J503-B: JST PH |
| --- | --- | --- |
| Exact header | `B4B-XH-A`, catalog label `(LF)(SN)` | `B4B-PH-K-S`, catalog label `(LF)(SN)` |
| Exact mate / contacts | `XHP-4` + 4 × `SXH-001T-P0.6` | `PHR-4` + 4 × `SPH-002T-P0.5S` |
| Rated current per circuit | 3 A AC/DC **with AWG22** | 2 A AC/DC **with AWG24** |
| Temperature | −25 to +85 °C, including rise | −40 to +105 °C, including rise |
| At 40 °C ambient | Exact derated current **OPEN**; 45 °C remaining to catalog total-temperature ceiling is not an ampacity rating | Exact derated current **OPEN**; 65 °C remaining is not an ampacity rating |
| Voltage | 250 V AC/DC | 100 V AC/DC |
| Contact resistance | ≤10 mΩ initial / ≤20 mΩ after environmental tests | ≤10 mΩ initial / ≤20 mΩ after test |
| Exact contact wire range | AWG28–22; 0.08–0.33 mm²; insulation OD 0.9–1.9 mm | AWG30–24; 0.05–0.22 mm²; insulation OD 0.8–1.5 mm |
| Pitch | **2.50 mm**, not 2.54 mm | 2.00 mm |
| Header body / mated height | 12.4 × 5.75 mm; about 9.8 mm mated height | 9.9 × 4.5 mm; about 8.0 mm mated height |
| Installed KiCad courtyard | 13.40 × 6.75 mm (K3) | 10.90 × 5.50 mm (K4) |
| Polarization / retention | Shrouded asymmetric profile, friction/detent retention; no separate actuated positive latch | Shrouded asymmetric profile, friction/detent retention; no separate actuated positive latch |
| Mating cycles | **OPEN**, no numeric value identified in public catalog | **OPEN**, no numeric value identified in public catalog |

**ASSESSMENT:** XH is the easier manual-harness candidate because of its larger pitch and wider exact-contact wire range. PH reduces courtyard area by about one third, calculated from the installed library rectangles, and suits a constrained board. Both need cable restraint if repeated motion is expected; contact lances retain terminals inside a housing and must not be confused with a connector-to-connector latch. Normal-force contacts are retained in both proposals.

**Hot-plug / mis-mating:** neither four-position signal family is a normal mate for either two-position power system (geometry-based inference; verify with unpowered samples). That does not make arbitrary harnesses safe: identical four-pin family cables with different pinouts remain interchangeable. Neither candidate establishes ground-first/last-break contact sequencing. JST's live-disconnection restriction [S7] applies; recommend connecting J503 with **both host and module unpowered**. Powered-off isolation/back-feed, signal pull-ups, cable capacitance/length, buffer margins and actual host-reference current remain OPEN. Contact current ratings do not qualify I2C signal integrity.

## Input/output mis-mating constraint

**REQUIREMENT:** a supply cable for J501 must not fit J502. Reversing a keyed connector is different from fitting a correctly oriented connector to the wrong voltage port. Color, labels, different entry orientation and the existing common pinout are insufficient physical coding.

| Proposed J501 family | Proposed J502 family | Review disposition |
| --- | --- | --- |
| P-VH | P-PC | Recommended family pairing; different pitch/profile, no intended cross-mate |
| P-PC | P-VH | Different pitch/profile, but worse output-drop evidence |
| P-VH | P-VH | **REJECT:** same `VHR-2N` cable fits both |
| P-PC | P-PC | **REJECT:** same `1757019` cable fits both; these exact parts add no distinct voltage code |

**INFERENCE / OPEN:** incompatible-family geometry is a strong screening measure, not a performed abuse/mis-mating test. Before release, check both cable-to-wrong-port directions unpowered, identify circuit 1 beside the key, and verify continuity/polarity from a drawing that states cable view. Any later extra port needs its own voltage-domain and coding review. The exposed source-side header contacts and any accessible energized adapter contacts also need installation review.

## KiCad availability and footprint review scope

**OBSERVATION [K1–K4]:** KiCad **9.0.6** is installed locally. The table reports actual footprint text, courtyard bounds, drill sizes and model-file existence. It is not an assigned footprint or a completed land-pattern/3D review. Library commit IDs are unavailable in the installed bundle; individual file SHA-256 values are recorded. The official [KiCad library license](https://www.kicad.org/libraries/license/) [S8] is CC-BY-SA 4.0 with an electronic-design exception; library-collection redistribution retains attribution/share-alike requirements. No library assets are redistributed here; preserve applicable per-file notices on later reuse.

| System | Standard library footprint | Board pattern and model status |
| --- | --- | --- |
| P-VH | `Connector_JST:JST_VH_B2P-VH-FB-B_1x02_P3.96mm_Vertical` | 2 × Ø1.70 mm plated holes, 3.96 mm pitch; Ø1.45 mm unplated boss hole at (−1.50, −3.40) mm from pad 1. Footprint exists. Referenced `Connector_JST.3dshapes/JST_VH_B2P-VH-FB-B_1x02_P3.96mm_Vertical.step` **is missing locally**, with no matching WRL. |
| P-PC | `Connector_Phoenix_MSTB:PhoenixContact_MSTBA_2,5_2-G-5,08_1x02_P5.08mm_Horizontal` | 2 × Ø1.40 mm plated holes, 5.08 mm pitch. Matching STEP and WRL exist in `Connector_Phoenix_MSTB.3dshapes/`. Footprint description explicitly lists `1757242`; its additional high-current part reference does not change this candidate's rating. |
| XH | `Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical` | 4 × Ø0.95 mm plated holes, 2.50 mm pitch, no boss. Matching STEP/WRL exist in `Connector_JST.3dshapes/`. |
| PH | `Connector_JST:JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical` | 4 × Ø0.75 mm plated holes, 2.00 mm pitch. Matching STEP/WRL exist in `Connector_JST.3dshapes/`; name omits `-S`. Catalog geometry matches this starting outline, but exact ordered variant must be checked. |

All matching models use the footprint basename; references use `${KICAD9_3DMODEL_DIR}`. No model has been validated against a physical sample or used in a board render. For VH, obtain a permitted exact model or make a reviewed envelope model in a later authorized CAD task; do not substitute the unshrouded header model. No new footprint appears necessary solely from this availability check, but package, pad numbering, mounting-side view, finished-hole tolerances and board thickness still require approval. JST catalog drill recommendations are reference ranges, not fabrication instructions. Allow additional room for cable bend, insertion/removal, lock access and Phoenix screwdriver access; the board courtyard alone is not the mated harness envelope.

## Review questions and closure evidence

1. **Brother: interface choice and additional ports.** Accept VH input/Phoenix output as the default pair, or require positive output latching, tool-free wiring, different orientation or more ports? A latch requirement reopens the output shortlist; do not silently substitute a same-pitch part.
2. **Operating procedure.** Is de-energized connection acceptable for power and telemetry? If live plugging is required, both power defaults need a different qualification basis/interface. Define expected lifetime mating count, cable pulls, vibration and strain relief.
3. **Electrical envelope.** Define acceptable upstream source/fault bounds, ambient/enclosure, GPIO-terminal voltage-drop budget and intended Pi 5/D435i load dynamics. The future converter model can remain OPEN while its acceptance limits are developed. Normal 9–24 V and GPIO entry are settled; do not request a wall adapter or reopen the power-interface choice. Treat any proposed 6 A testing as separate screening, not an expanded runtime guarantee.
4. **Harness.** Confirm maximum one-way length, wire gauge/insulation, exact GPIO socket, multiple-ground implementation, mechanical retention and current sharing; choose appropriate crimp tooling or ferrule/torque process. AWG18 is only the analyzed candidate. Its 80 °C wire limit can govern before the connector housing limit.
5. **Evidence needed.** Obtain exact-contact current derating and resistance test planes, JST cycle/assembly specifications, Phoenix controlled drawings/PDF/derating and the missing VH model. Measure the entire manufactured path, not just a loose connector.

**R5 closure plan after the earlier gates:** visual inspection and circuit-number/continuity/short checks → current-limited bench supply → no-load startup/output verification → low-current dummy load → 1/3/5 A steps to thermal equilibrium → connector/wire/crimp temperatures and simultaneous regulation/J502/load voltage measurements → ripple and representative load steps up to the designed 5 A envelope → protection/fault tests → telemetry validation → SBC last. After those gates, qualify Pi 5 idle, sustained CPU-heavy operation and Pi 5 with D435i operating. This does not promise arbitrary peripheral hot-plug. Any additional 6 A/100 ms hot-start test needs an approved screening procedure and cannot establish a user-requested operating mode by itself. Record four-wire resistance including solder, crimps/clamps, both wires and every GPIO power/ground contact, individual branch currents, uncertainty and ambient. Test retention and power-state behavior separately. None of these tests occurred here; neither repository checks nor connector catalog ratings replace them.

## Repository validation

`python3 -B scripts/check_repository.py`: **PASS**, 13 hardware files verified unchanged, no errors. `python3 -B -m unittest discover -s tests -v`: **PASS**, 10 tests. Both are required again before each focused local commit. This evidence covers repository integrity and existing regressions; it does not qualify a connector or release R2/R3. Only this new report and its new source register are intended for the commits.

## Sources not fully recovered

- Phoenix exact header/plug raw downloads returned **HTTP 403**; retrieval stopped. Manufacturer technical tables had been readable through the web tool, but no pinned PDF or exact pair/AWG18 derating curve was obtained. Additive resistance remains a hypothesis.
- JST's VH assembly-manual link led to an email-delivery form and restrictive document terms; no personal information was entered or message sent. The exact VH 2D drawing request timed out. Public VH/XH/PH catalogs were recovered and hashed, but contained no identified numerical mating-cycle or ambient-current curves.
- The installed shrouded-VH STEP reference is unresolved. No downloaded replacement was obtained. Other listed models exist locally; their existence does not verify their geometry.

The initial Python downloader had a certificate-store error; ordinary curl with verification enabled recovered JST/Belden files without any system change. Detailed access outcomes are in the register. These limitations remain visible to the conductor rather than being replaced with distributor headline ratings or invented values.

## Comparison for the brother's review

| Reference / candidate | Published current basis | Retention / servicing | Voltage-drop or interface tradeoff | KiCad footprint / model | Review rank |
| --- | --- | --- | --- | --- | --- |
| J501-A: shrouded VH | 7 A, AWG18; hot curve OPEN | Positive latch; crimp tooling | Higher R is more tolerable on input, still needs low-V input budget; distinct from proposed output | Exists / model missing | Default for review |
| J501-B: Phoenix | 12 A nominal; AWG18 hot curve OPEN | Screw wire clamp, no plug latch | Lower R; forces different-family output | Exists / STEP + WRL present | Alternative |
| J502-A: Phoenix | 12 A nominal; AWG18 hot curve OPEN | Screw termination; external restraint needed | 28 mV at 5 A additive connector screen; 36.4 mV assumed hot. Full dynamic budget OPEN | Exists / STEP + WRL present | Default for review |
| J502-B: shrouded VH | 7 A, AWG18; hot curve OPEN | Positive latch; crimp tooling | 100/200 mV at 5 A initial/after-test connector-only; 260 mV hot sensitivity. Full-path screens miss | Exists / model missing | Conditional fallback; weak drop margin |
| J503-A: XH | 3 A, AWG22; exact host current OPEN | Friction/detent; larger manual interface | Wider exact-contact wire range, larger courtyard | Exists / STEP + WRL present | Default for review |
| J503-B: PH | 2 A, AWG24; exact host current OPEN | Friction/detent; smaller crimp/wire | Smaller footprint; more constrained wire OD | Exists / STEP + WRL present; suffix review | Space-driven alternative |

**RECOMMENDATION FOR REVIEW — J501:** `B2P-VH-FB-B` + `VHR-2N` + 2 × `SVH-21T-P1.1`, with the analyzed AWG18 harness: positive input latch and a different mating family from the proposed output for the known 9–24 V normal-input requirement. Future auxiliary-source fault/inrush and temperature qualification remain OPEN.

**RECOMMENDATION FOR REVIEW — J502:** Phoenix `1757242` + `1757019`: prioritize the lower resistance evidence on the GPIO 5 V/multiple-GND harness for Pi 5 plus D435i within the designed 5 A envelope. **J502/harness stays OPEN** pending resistance, current, retention and mechanical qualification, with de-energized servicing. No 5 A capability or historical 6 A/100 ms mode is claimed as validated.

**RECOMMENDATION FOR REVIEW — J503:** `B4B-XH-A` + `XHP-4` + 4 × `SXH-001T-P0.6`: larger pitch and wider wire range suit manual bench assembly; preserve the host-input pinout and connect with both sides unpowered. Final choice belongs to the brother's review.
