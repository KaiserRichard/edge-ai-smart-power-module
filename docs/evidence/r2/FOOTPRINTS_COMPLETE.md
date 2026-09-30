# V1A footprint completion — 2026-09-30

**VERDICT: FOOTPRINTS COMPLETE EXCEPT L201, D101, F101. J502 hot contact resistance remains OPEN.**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED. R2 electrical release and R3 remain BLOCKED.** This verdict covers the missing/placeholder package assignments identified at redraw `1f4c2f821793506871b9abe6227b1deba419d27e`; it is not blanket qualification of the inherited BOM, electrical ratings or assembly process.

## OWNER EXPLANATION — one-page briefing

A schematic symbol says which electrical pins connect. A footprint says where the real component solders to the board. Both must describe the **same exact manufacturer part and package variant**. A familiar package name or matching pin count is insufficient. A wrong footprint can leave pins unsoldered, connect power to the wrong terminal, short an exposed pad or make a connector impossible to install. Those errors can require a new PCB fabrication run (a board respin), even when ERC reports no violations.

Start with the manufacturer's package and recommended PCB land drawings. Record their revision, page and units. Check whether the drawing is a top view, bottom view or connector mounting-surface view; rotate it as needed, but never silently mirror it. Compare pad centers, pitch, length, width and drill size numerically. Body dimensions describe the component, not the solder lands. Here, the TDK 2220 capacitor's recommended lands differ from the generic KiCad 2220 footprint; the manufacturer's A/B/C diagram resolves that difference.

Next trace **pin 1** from the symbol to the physical pad and the part's identifying mark. Check every pin, including repeated source/drain pins, the positive side of polarized capacitors and connector cavity numbering. A nonpolar ceramic capacitor has no electrical pin 1; its project pads 1/2 are interchangeable. For connectors, specify the mating housing, contact and wire range. The cable-entry view can reverse the apparent order. Continuity-test the completed cable rather than relying on wire colours.

For an **exposed pad**, determine its actual electrical function and number from the datasheet. It may be ground, drain, another terminal or absent. Do not invent an extra pin. Copper, solder-mask openings and solder-paste apertures serve different purposes. A large copper pad may need several smaller paste windows to control solder volume and voids. The existing LM61460 footprint has fourteen terminals, not an invented EP15; this work preserves its reviewed copper and stencil geometry.

Check the **courtyard**, which reserves placement space around maximum body and pad extents. Connectors also need mating, fastener and tool access beyond the solder pads. Record project-selected annuli, mask expansion, paste and courtyard allowances separately from manufacturer dimensions; an assembler must qualify the process.

Finally compare symbol pins to footprint copper numbers, inspect a native render, and prove that assignment did not change the circuit or drawing layout. ERC and these tests establish capture consistency. They do not establish current capacity, thermal performance, fault protection or safe SBC operation. J502 illustrates the distinction: its pads are checked, while the complete hot Pi mating contact still lacks the required resistance guarantee.

## Baseline and reuse

**OBSERVATION:** the actual baseline contains154 physical components and24 empty footprints: F101; TP101/102; C201/202/209/210/211/212/213/214; L201; C404; TP401/402/403/404; J501/502/503; TP501/502/503/504. No nonempty footprint ID contains OPEN/TBD/placeholder. J301/J302 additionally had generic `PinHeader_1x02` MPN placeholders. D101 was already assigned and is an explicit selection hold. Nonphysical power flags have no board footprint and are not XML physical components.

**EVIDENCE:** [baseline inventory](footprints_complete/BASELINE_INVENTORY.json), [raw baseline export](footprints_complete/baseline_1f4c2f8.xml), [PR7 port record](footprints_complete/PR7_PORT.md). PR[#7](https://github.com/KaiserRichard/edge-ai-smart-power-module/pull/7), commit8535cffe2151794ae352d25e19f9262a549dbc1b, supplied the ten test-pad assignments. They were ported by field into the redraw. Its old sheet geometry/ERC evidence was not imported. The earlier audit's “fourteen” is the count after those ten test pads, not this redraw's initial blank count. There are **nine TDK capacitors total**, eight on Sheet02 and C404 on Sheet04.

The existing `V1A_Qualified.pretty`, [decision index](../../context/06_DECISION_LOG.md), [critical footprint review](forensic_2026-09-14/CRITICAL_FOOTPRINT_QUALIFICATION.md) and path-budget branch were read before selection. Exact path-budget/harness source commits and document hashes are in [INPUT_PROVENANCE.json](footprints_complete/INPUT_PROVENANCE.json). Only this worktree's KiCad files were edited; no other KiCad GUI instance was running.

## Assignment and pad-check table

All new footprint names below use library `V1A_Qualified`. **PASS** means checked land geometry and symbol/pad mapping. **OPEN** identifies a held selection or missing qualification. Bare test pads are etched copper; a purchased MPN and manufacturer datasheet are **not applicable**.

| Refdes | MPN | Footprint | Datasheet revision used | Pad check |
|---|---|---|---|---|
| F101 | OPEN, unchanged | empty | TVS/fuse study owns selection | OPEN — excluded |
| D101 | SMBJ26CA, inherited; no new selection | Diode_SMD:D_SMB, unchanged | TVS study owns reselection | OPEN — excluded |
| TP101 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | KiCad9.0.6 f64dbd7 / PR7 | PASS — Ø1.5, pad1, no paste |
| TP102 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |
| C201 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | TDK B11 Apr2011 printedp72/PDF70 + exact product record2026-09-30 | PASS |
| C202 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| C209 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| C210 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| C211 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| C212 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| C213 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| C214 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | same | PASS |
| L201 | XAL8080-682MED, inherited; no new selection | empty | Gate3b owns selection | OPEN — excluded |
| J301 | B2B-XH-A(LF)(SN) | JST_B2B_XH_A_P2.50_THT | JST eXH, unnumbered; PDF metadata2025-07-30, pp2–5 | PASS |
| J302 | B2B-XH-A(LF)(SN) | JST_B2B_XH_A_P2.50_THT | same | PASS |
| C404 | C5750X7R1H226M250KB | TDK_C5750_2220_A4.45_B1.30_C4.50 | TDK B11 + exact product record above | PASS |
| TP401 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | KiCad9.0.6 f64dbd7 / PR7 | PASS |
| TP402 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |
| TP403 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |
| TP404 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |
| J501 | B2P-VH-FB-B(LF)(SN) | JST_B2P_VH_FB_B_P3.96_THT | JST eVH, unnumbered; PDF metadata2026-01-09, pp1–4; KiCad f64dbd7 | PASS |
| J502 | Phoenix1776508 | Phoenix_1776508_MSTB_2_GF_5.08 | Phoenix generated2013-11-12 p6 + current product record2026-09-30 | PASS geometry / OPEN hot contact |
| J503 | B4B-XH-A(LF)(SN) | JST_B4B_XH_A_P2.50_THT | JST eXH, unnumbered; PDF metadata2025-07-30, pp2–5 | PASS |
| TP501 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | KiCad9.0.6 f64dbd7 / PR7 | PASS |
| TP502 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |
| TP503 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |
| TP504 | N/A — etched copper | TestPoint:TestPoint_Pad_D1.5mm | same | PASS |

Detailed pad dimensions, pin1 orientation, holes, annuli, paste and courtyard rationale are in [Sheet02](footprints_complete/SHEET02.md), [Sheet03](footprints_complete/SHEET03.md), [Sheet04](footprints_complete/SHEET04.md) and [Sheet05](footprints_complete/SHEET05.md). New capacitor/connectors have no exposed pad; connector paste is absent and mounting holes have no electrical pad number. Existing IC exposed-pad/thermal-pad numbering and stencil shapes remain unchanged. New source notes identify the manufacturer revision in each footprint description. [Full physical inventory](footprints_complete/FULL_INVENTORY.csv) also lists inherited assignments; generic resistor/capacitor MPN procurement qualification remains outside this completion verdict.

## Mates and the J502 requirement

J501 mates with **VHR-2N + SVH-21T-P1.1** contacts; J502 with **Phoenix1777989**, whose screw contacts are integral; J503 with **XHP-4 + SXH-001T-P0.6**; J301/J302 each with **XHP-2 + SXH-001T-P0.6**. Input and output mating families differ to reduce accidental9–24V-to-output connection.

**REQUIREMENT:** use Pi physical5V pins2/4 and all eight GND pins6/9/14/20/25/30/34/39. The [complete harness map](footprints_complete/SHEET05.md#j502--pi-all-ten-required-physical-contacts) preserves J502's two original electrical pins and fans out externally. Candidate Pi sockets are Harwin **M20-1071000 over1–20** and **M20-1070800 over25–40**, with ten **M20-1180042** gold crimps and an indexed hold-down. The gap over21–24 avoids housing interference while using every required ground. No physical harness was built.

**OPEN RISK:** no inspected datasheet proves≤20mΩ for the complete hot, conditioned contact mated to the actual Pi male header. Harwin's20mΩ initial/30mΩ conditioned specification does not satisfy that proof. J502's Phoenix catalogue resistance also does not prove its stricter PATH_BUDGET target≤3.12mΩ per complete hot pole/clamp. These candidates are assigned for engineering review under the user's explicit OPEN fallback; no hot multiplier or nominal resistance is represented as a manufacturer maximum. Current sharing, header identity, mating length, crimp/torque quality, splices, retention and thermal rise require qualification. Retain the path-budget wire targets and measure every active contact before any SBC integration.

## Exclusions

- **L201:** untouched MPN/value and empty footprint; Gate3b may replace it. Consequence: inductor package/placement cannot be frozen.
- **D101:** untouched inherited SMBJ26CA/D_SMB assignment, explicitly OPEN; TVS reselection owns its final voltage/package. An existing footprint is not approval.
- **F101:** untouched empty footprint and unresolved MPN; coordinated TVS/fuse study owns selection. Consequence: fuse size, interrupt capability and energy coordination cannot be frozen.

J502 is **not** an empty-footprint exemption: it has checked geometry, and the checker rejects a missing J502 assignment. Its hot mating/contact qualification remains an explicitly documented OPEN electrical item.

## Verification and limits

**EVIDENCE:** [canonical field-change report](footprints_complete/NETLIST_FIELD_DIFF.json) and [full canonical diff](footprints_complete/canonical_netlist.diff) show **32 changes:24 Footprint,5 MPN,3 Value**. All154 components, libraries, complete net names, pin attributes, hierarchy and connections are otherwise identical. Canonicalization ignores only the pre-existing export date/source/tool metadata, filesystem library paths, order and numeric net codes; it does not discard net names, UUIDs, pin functions or library definitions. Duplicate KiCad fields are checked for consistency. Source comparison additionally proves exact non-field schematic bytes, including power flags omitted by XML, and unchanged project/ERC/library settings.

**EVIDENCE:** full-project ERC reports **0 violations** after every finished sheet with unchanged settings. The [final capture check](footprints_complete/capture.log) checks all assigned footprints' numbered copper pads against exported symbol pins, including inherited IC exposed pads. The checker now rejects every empty/placeholder footprint except exactlyF101/D101/L201; it does not exempt whole component classes. [31 regression tests](footprints_complete/tests.log) pass, including adversarial empty/placeholder cases, nonallowed net/property changes and independent manufacturer dimensions. [Repository preservation](footprints_complete/repository_check.json) chains the historical evidence without replacing or weakening it. No PCB was authored or changed, so DRC is not applicable to this schematic/library task.

**EVIDENCE:** six-page native landscapeA3 [review PDF](footprints_complete/V1A_REVIEW_READABLE.pdf) re-exported and delivered to `~/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf`. [PDF comparison](footprints_complete/PDF_COMPARISON.json): pages1–5 are pixel-identical at96dpi; page6 changes only the three shortened connector Value strings. All symbol/wire/text positions and sizes are byte-preserved. Sheet03 and Sheet05 were visually inspected; no redraw layout disturbance observed. Five new native footprint renders were inspected against the cited drawings. The previous external review PDF is retained under a timestamped backup before replacement.

**DECISION:** preserve historical Source/Rating strings and schematic narrative notes because the user permits only Footprint/MPN/Value changes. Some still say connector/TDK package OPEN; this dated report supersedes those specific assignment uncertainties. No electrical validation claim is implied. Full BOM selection for already-assigned generic passives, source/fault studies, capacitor bias/stability, copper/return/thermal layout and physical bring-up remain separate R2–R5 gates.

## DECISIONS FOR THE OWNER

| Decision | Options / consequence | Recommended option |
|---|---|---|
| TDK land pattern | Generic2220 conflicts with published ranges; reviewed custom lands follow those ranges. | Use the qualified custom footprint; obtain assembler paste-volume/strain feedback before R4. |
| J502/contact acceptance | Assume initial catalogue figures; or qualify the exact complete hot mate and resistance reference planes. | Keep the concrete Phoenix/Harwin candidate OPEN and qualify≤3.12mΩ per module pole and≤20mΩ per Pi contact, including ageing/hot measurements and per-pin current. Re-select if it misses. |
| Harness population | Earlier four-ground harness; or both5V/all eight GND with indexed two-socket carrier. | Use all ten specified contacts and the updated map. Review exact Pi board/retention/clearance and continuity before power. |
| Held components | Freeze inherited L201/D101/F101 now; or wait for the owning electrical studies. | Retain all three holds. Import final parts only through a separately reviewed follow-up. |
| Existing generic-passive BOM | Treat assigned land size as a selected MPN; or complete value/tolerance/TCR/rating procurement qualification separately. | Separate BOM qualification before release; do not infer a vendor part from0603/0805/1210. |
| PCB/fabrication progression | Start from clean ERC; or close R2 electrical and assembly risks first. | Close R2, then obtain the required R3 authorization. No merge, procurement or fabrication is authorized by this footprint task. |

Reproduce checks using `kicad-cli sch export netlist --format kicadxml`, `kicad-cli sch erc --format json --exit-code-violations`, `python3 scripts/check_footprint_completion.py --netlist <fresh.xml>`, `python3 scripts/check_r2_schematic.py --netlist <fresh.xml> --footprints <installed-footprint-root>`, `python3 -m unittest discover -s tests -v` and `python3 scripts/check_repository.py`. Regenerate each new land with `scripts/build_completion_footprints.py --part <tdk|xh2|xh4|vh|phoenix> --output-dir <scratch-library>`; do not run the historical whole-schematic generator.

**VERDICT: FOOTPRINTS COMPLETE EXCEPT L201, D101, F101. J502 hot contact resistance OPEN. Electrical release BLOCKED.**
