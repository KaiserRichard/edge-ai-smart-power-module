# CUSTOM-FX-CU-01 RevA — make-or-quote drawing / 1 of 1

**Current selection:** the BOM_LOCK_ALL addendum at the end supersedes the earlier owner-selection hold; historical calculations below are retained.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED** · 2026-10-04 · dimensions mm · seven positions / board; order plan **24 straps** for three boards plus spares.

```text
TOP (flat, no bend)                       SIDE
             30 overall                  ┌──────────────────────────┐
  ┌──────────────────────────────┐       └──────────────────────────┘ 2 thick
  │    ○                    ○    │ 15
  └──────────────────────────────┘        Hole axes on width centreline
       |<------ 20 pitch ---->|           2 × Ø4.5 through, no countersink
  |<-5->|                    |<-5->|      Bend angle 0°; bend radius N/A
```

**CONFIRMED interface:** existing [ForceLink_M4_P20](../../../../hardware/kicad/V1A_Qualified.pretty/ForceLink_M4_P20.kicad_mod) pads at (−10,0)/(+10,0), Ø10 copper, Ø4.5 drills; F.Fab 30×15, courtyard31×16. Existing [fixture specification][fixture] selects C110 copper, 2×15 section, span≤30, 20 pitch, M4×12 A2-70 bolts, two4.3/9/0.8 washers and one all-metal M4 nut **per joint**. Full section30mm²; hole-neck section21mm². CAD read-only.

**ASSUMED manufacturing details for quotation:** C11000/Cu-ETP flat copper; tin plate1–5µm on all surfaces after drilling/deburring; no paint at contacts. Finished length/width30.0/15.0±0.1; thickness2.0±0.05; holeØ4.5+0.1/−0; pitch20.00±0.10; transverse centring±0.10; mating-face flatness≤0.10. Break sharp edges≤0.2. Flatness, plating process/temper, stack height, torque, bolt clearance and mating finish need owner/fabricator review; these are proposed tolerances, not historical RevA requirements. No solder-only structural joint; do not bridge separate nets with washers. Set quantities:48bolts/96washers/48nuts for24links. Assembly/removal only discharged; fit per test configuration.

| Position / actual path | Current to review (not a validated rating) |
|---|---|
| JP101 EFUSE_OUT→VIN_PROTECTED | Normal input3.147A at9V,5A output, **ASSUMED**90% efficiency [calculation][calc]; startup/fault peak OPEN. |
| JP201 BUCK_SW→L201_IN; JP202 L201_OUT→VOUT_5V1 | Inductor5A average plus ripple; healthy8A initial-current allocation. JP201 removed for external injection; JP202 may see conditional first-forward100A/≤20µs; reverse/coupled bound OPEN. |
| JP301 SERIES_OUT→VOUT_PROTECTED | Normal5A; series/bank-coupled fault waveform OPEN. Fixture's100A first-forward allocation is not a bound on all link currents. |
| JP330 CB_BALLAST_OUT→CB_DRAIN | Protected dump: **CALCULATED**169A screen =5.5V/[33mΩ×(1−1%−50ppm/K×70K)], ignoring positive other resistance; assumes node≤5.5V. Duration/reversal OPEN. |
| JP331 RAW_BALLAST_OUT→RAW_DUMP_DRAIN | Raw dump: **CALCULATED**76.9A screen =7.50685V/[99mΩ×(1−1%−50ppm/K×70K)], conditional fixture no-dump voltage; duration/reversal OPEN. |
| JP501 LOAD_5V1→LOAD_FIXTURE | Normal dummy load up to5A; capacitive/transient current OPEN. Opening JP501 does not disconnect J502: unplug J502 as required; PF5 is paired force return. |

**CALCULATED continuous screen: 8 A, 20 K rise at40°C ambient**, conditional lumped heat balance. [KME C11000][kme] typical conductivity58MS/m givesρ20=1.724×10⁻⁸Ωm; α=.0037/K. Conservatively use30mm length/21mm² neck throughout: R60=28.28µΩ. **ASSUMED:** each measured joint≤0.2mΩ, h=5W/m²K, exposed top area323mm², uniform assembly temperature; ignore radiation/end cooling. `I=sqrt(h·A·20/(R60+0.4mΩ))=8.68A`, rounded down8A. At5A:10.71mW,2.14mV,6.63K model rise. This omits local contact hot spots; installed rating remains **OPEN**.

**CALCULATED pulse screen:**100A×20µs gives5.66µJ bulk and40µJ/joint; bulk mass7.46g, cp394J/kg/K gives≈1.93µK bulk rise. It does **not** qualify169A dump duration or repetition. Fixture feeder14A is separate from local100A; coupled-reverse275.36A is an invalid-domain warning, not an approved envelope [fixture]. Verify full waveform, hot joints, four-wire resistance≤0.2mΩ/joint and injection-loopL≤40nH allocations before use. PCB copper/return paths, torque/creep, thermal rise and clearances remain engineering gates.

**OPEN catalog equivalent:** none verified to match both20mm/M4 geometry and fault envelope. Quote this authored strap; no generic PCB jumper current rating is transferred. [Reproducible calculations](FORCE_LINK_CALCULATIONS.json) / [calculator](calculate_force_link.py). Material source referenced only, copyright KME, no open redistribution license established; physical-property facts retained, no circuit/design copied. Access2026-10-04; KME revisionC11000_Cu-ETP_10_2020 p1. Project sources pinned below; no upstream changes.

[fixture]: https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FIX3_FIXTURE.md
[calc]: https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/CALCULATIONS.json
[kme]: https://www.kme.com/fileadmin/DOWNLOADCENTER/COPPER%20DIVISON/4%20Industrial%20Rolled/3_Datasheets/Datasheets_NEW_2021/Cu-ETP_01_2021_e.pdf

## Needs owner decision

**OPEN:** approve the proposed finishing/tolerances and joint stack/torque, obtain the fabricator quote and exact fastener codes, and establish each installed current waveform/contact-temperature limit. No catalog equivalent is accepted. This drawing supplies the make-or-quote definition; it does not close B026/M01–M03 or authorize fabrication.

**CONFIRMED resume check, 2026-10-04:** all seven captured links use the inspected M4/20 mm footprint and the net pairs above in the [pinned netlist](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/4af7818511076cbbd336880607d262fc311d01bc/docs/evidence/r3/layout_prep/resume/fresh.xml). Re-running the calculator reproduces the committed JSON exactly. All 33 baseline hardware file hashes match. Existing sourced material data and current allocations are retained.

## BOM_LOCK_ALL selection addendum — 2026-10-04

**DECISION:** B026 is closed as an ordering specification to this authored RevA drawing,24 straps. Adopt the stated C11000, tin1–5µm, dimensions/tolerances, deburring and flatness as the quotation default. No footprint, net or nominal geometry changes. M01:Würth00944 12,M4×12A2-70,48 pieces; M02:RS PRO527381,4.3/9/0.8 mm A2 plain washer,96 minimum (one bag250); M03:RS PRO6655609,M4A4all-metal Aerotight,48 minimum (two packs25). [Sources and revisions](../../../../third_party/bom_order/LOCK_SOURCES.json), accessed2026-10-04; [selection rationale](LOCK_REVIEW.md).

**BENCH DISPOSITION:** installed current rating, contact resistance, torque/creep, thread locking, joint temperature, fault-pulse envelope and parasitics are **bench check, does not block layout**. The earlier8 A thermal screen remains conditional and is not a measured rating. The existing1.6 mm board plus2 mm copper plus1.6 mm washer stack leaves6.8 mm of the12 mm shank for the nut and protrusion; verify locking engagement with the actual hardware. Preserve the stated four-wire joint and pulse checks. Supply the straps loose; fit only for the specified discharged test configuration.

**SUPPLY ACTION:** obtain an exact fabricator quote and confirm purchased pack quantities before an authorized order. This is a commercial gap, not an owner decision about a different link. No fabricator was contacted and no manufacturing approval is granted. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
