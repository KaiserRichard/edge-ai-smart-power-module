# Harness and thermal defaults — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**DECISION:** O01 and O02 each mean three board kits plus one complete spare kit. These are project assemblies, not invented manufacturer MPNs. Order the concrete subparts in [BOM_ACCESSORIES.csv](BOM_ACCESSORIES.csv) once; do not also purchase the parent kit. Manufacturer sources, revisions and attribution are in [LOCK_SOURCES.json](../../../../third_party/bom_order/LOCK_SOURCES.json); all accessed 2026-10-04. Supplier snapshots are retained in [LOCK_ACCESSORIES.json](../../../../third_party/bom_order/LOCK_ACCESSORIES.json).

## O01 — actual mating interfaces

**EVIDENCE:** the pinned [fresh netlist](../../r3/layout_prep/resume/fresh.xml) determines these mappings. Numbering is the manufacturer's numbered cavity viewed as specified in its drawing, not an assumed left-to-right view from the cable. Existing JST mounting-side land/pin review is retained in [PIN_REVIEW.md](../gate4b/PIN_REVIEW.md) and the JST source records. XH pitch is **2.50 mm**, not 2.54 mm; VH is 3.96 mm. Off-board sockets require no new PCB lands.

| Board interface | Selected housing/contact | Wiring per kit |
|---|---|---|
| J501 DC input | VHR-2N; two SVH-41T-P1.1 | 1 VIN_RAW, 2 GND; one metre each red/black AWG16 from H07/H08 |
| J301 main arm; J302 reset; J603 source fault; J604 series arm | Four XHP-2; eight SXH-001T-P0.6; four C&K8125SHZBE | Header1 contact signal, header2 GND; switch1 common→GND, switch2 momentary→signal; unused switch3 insulated |
| J605 real PG; J606 main permission | Two XHP-2; four SXH-001T-P0.6 | 1 PG_FIXTURE/MAIN_FIXTURE respectively, 2 GND; labelled observation leads, **no shorting plug or control switch** |
| JP600 manual rail-valid link | XHP-2; two SXH-001T-P0.6 | Removable loop1 SAFE5→2 MANUAL_RAILS_VALID |
| JP660 driver-supply link | XHP-2; two SXH-001T-P0.6 | Removable loop1 SER_FEED→2 SER_DRV |
| J503 host I2C | XHP-4; four SXH-001T-P0.6 | 1 GND, 2 3V3_HOST, 3 SDA_HOST, 4 SCL_HOST; four labelled flying leads |

**DECISION:** 32 XHP-2, four XHP-4 and four VHR-2N housings cover four kits. Eighty XH contacts round to one cut strip100; eight VH contacts round to one strip100. The selected SVH-41T-P1.1 supports AWG20–16 / insulation OD1.7–3.0 mm; SVH-21T-P1.1 is not substituted for AWG16. XH contacts support AWG28–22 / OD0.9–1.9 mm. Alpha3050 **stranded AWG24**, approximately1.42 mm OD, fits that range. Use black3050 BK005 for ground and white3050 WH005 with individual net labels for other leads. Do not use the thicker J502 AWG20 branches in XH crimps.

**ASSUMPTION, bench cut plan:** six two-wire control/observation pigtails300 mm, I2C leads150 mm, each removable loop50 mm. Per kit:1.95 m black and2.35 m white. One100-foot spool of each covers four kits plus ample cutting allowance. These are assembly defaults, not validated I2C cable-length limits. Pull-up/rise-time and injected-noise checks remain at bring-up. No USB data route or WBR battery assumption is introduced.

**CALCULATION:** four input lead sets consume4 m per colour from the already-ordered Belden8521 spools. The frozen J502 trunk consumption stays3×0.075 m; even with its existing1 m minimum cut allowance, total reserved wire5.225 m per colour is below30.48 m. No second H07/H08 spool is charged. J502/Pi lengths, ten87309-9 contacts and its40-position3-87456-6 housing remain unchanged.

**EVIDENCE / DECISION:** C&K8020 sheet,9-Feb-2022:8125SHZBE uses gold contacts and ON–MOM switching; pins1–3 rest,1–2 pressed. Use only1–2, giving a normally-open dry contact. Its0.4 VA /20 V rating covers the low-voltage control interface by nominal voltage; load/wetting and contact-bounce behavior remain checks. Never connect a switch to J605/J606. JP600/JP660 loops are supplied loose, labelled and normally absent until the prescribed test configuration permits them.

**DECISION:** contract the crimp assemblies to a qualified harness shop using the selected maker contacts and approved tooling; no tool purchase is included. Termination fit, pull test, continuity, cavity orientation and isolation of the unused switch lug are assembly acceptance checks. Source-fault injection remains deliberate and controlled. The external injection fixture, host-end device-specific connector and lab instrumentation are outside O01; the defined harness ends in labelled insulated flying leads.

## O02 — three isolated TO-220 assemblies

**DECISION:** select Boyd/Aavid **507302B00000G** sink plus **4880SG** insulating mounting kit for each of D102, D330 and D331:12 sinks and12 kits for four board sets. The kit includes the ThermalsilIII pad, shoulder washer, flat/lock washers, nut and4-40×0.5-inch screw. It mounts through the TO-220 tab hole; it does not require additional PCB holes or soldered sink pins.

**EVIDENCE:** ST DS3978 Rev3,August2018: STPS60H100CT has live cathode pin2/tab; pins1/3 are the two anodes. Each diode gets a separate sink and insulating stack. Anodizing alone is not electrical insulation. Verify tab-to-sink isolation after tightening. Q316 is TO-263/D2PAK with live AUX_RAW tab: the TO-220 kit does not fit it. Its copper/via thermal path remains a PCB-layout task.

**LAYOUT INPUT:** maker507302 drawing gives19.05×19.05×9.65 mm overall sink envelope and screw/nut attachment. Reserve that envelope at each diode, plus fastener/tool clearance, while placing components; orientation follows the tab and device lead clearance. Existing footprints remain unchanged. The unplaced board cannot establish collision clearance yet.

**OPEN RISK:** the published24°C/W sink-air figure is a catalogue condition, not a guaranteed installed thermal resistance. At1 W it implies24°C sink rise before interface/junction resistances; airflow, pulse energy, nearby heat and real dissipation remain to be established. This selection supplies a concrete layout default and does not validate5 A steady-state temperature, fault pulses, grounded-sink insulation or an electrical release. Start with the current-limited supply and dummy-load progression in the project bring-up procedure.
