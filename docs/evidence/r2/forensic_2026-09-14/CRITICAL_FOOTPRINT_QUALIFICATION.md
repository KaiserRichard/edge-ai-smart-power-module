# Critical footprint qualification - 2026-09-14 continuation

**R2 BLOCKED; R3 BLOCKED. NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED.**

Scope: pad geometry and symbol-to-pad assignment, not thermal/fault validation or an approved PCB. Sources and hashes: [qualification source register](qualification_source_register.json). Earlier evidence is retained. Only U201, Q101 and R401 Footprint properties changed; see [assignment log](footprint_assignments.json) and [verification](QUALIFICATION_VERIFICATION.md).

## Disposition

| Part | Exact package and primary drawings | Existing KiCad compatibility | Decision |
| --- | --- | --- | --- |
| U201 LM61460AANRJRR | TI RJR0014A, VQFN-HR 14, 4.0 x 3.5 mm nominal, height 1 mm max; SNVSBD5D pp55-57, drawing 4223976/H 06/2026 | No exact RJR footprint found in installed library; generic QFN is incompatible | Assigned project `TI_RJR0014A_LM61460` |
| Q101 CSD19537Q3 | TI Q3 SON 3.3 x 3.3 mm nominal, 1.1 mm max height; SLPS549B Nov2022 pp1,8-9 | No exact footprint found; SO-8 topology/mechanics incompatible | Assigned project `TI_Q3_CSD19537Q3` |
| R401 WSL27262L000FEA | Vishay WSL2726 four-terminal, document 30131 rev29-Jun-2026 pp1-2; 2 mOhm height 2.9 +/-0.2 mm | No exact WSL2726 found; two-terminal and other Kelvin package mappings incompatible | Assigned project `Vishay_WSL2726_Kelvin_1Fplus_2Splus_3Sminus_4Fminus` |
| L201 XAL8080-682MED | Coilcraft XAL8080, document 839 rev05/01/26; primary physical drawing linked below remains unreadable locally | Installed `L_Coilcraft_XAL8080-XXX` remains an unverified candidate | OPEN; blank assignment retained |
| Nine C5750X7R1H226M250KB | TDK C5750/EIA2220, exact body and land ranges established below | Generic 2220 does not match documented recommendation | OPEN; all nine remain blank |

## U201: pin map, copper and paste

Primary [TI datasheet](https://www.ti.com/lit/ds/symlink/lm61460.pdf), local `third_party/documents/r2/TI_LM61460_SNVSBD5D.pdf`. RJR0014A is the applicable package for the exact catalog order code. It has **no separate EP15**. The board-land drawing is a top board view; do not mirror the bottom package outline.

| Pad | Function | Land bounding box x / y (mm, package center origin; top view, +y down) |
| --- | --- | --- |
| 1 | BIAS, grounded in V1A | -2.2..-1.5 / -1.95..-0.95, shaped |
| 2 | VCC | -2.2..-1.5 / -0.65..-0.40 |
| 3 | AGND | -2.2..-1.5 / -0.15..0.15 |
| 4 | FB | -2.2..-1.5 / 0.40..0.65 |
| 5 | PGOOD, NC | -2.2..-1.5 / 0.95..1.95, shaped |
| 6 | RT | -1.25..-1.00 / 1.25..1.95 |
| 7 | EN/SYNC | -0.75..-0.50 / 1.25..1.95 |
| 8 | VIN | 0.25..0.65 / 0.95..1.95 |
| 9 | PGND | 1.40..2.20 / 0.95..1.95, shaped |
| 10 | SW | -0.20..2.20 / -0.20..0.20 |
| 11 | PGND | 1.40..2.20 / -1.95..-0.95, shaped |
| 12 | VIN | 0.25..0.65 / -1.95..-0.95 |
| 13 | RBOOT | -0.75..-0.50 / -1.95..-1.25 |
| 14 | CBOOT | -1.25..-1.00 / -1.95..-1.25 |

**EVIDENCE:** copper comes from the dimensioned blue vectors on p56; paste from red vectors on p57. Scale 25:1 is checked against labelled dimensions. Cubic fillets are polygonized with 17 samples per segment; exported coordinates retain five decimal places. This is CAD transcription of land geometry, not copied circuit design. Pin 1 is upper left. TI's stencil example is 0.1 mm thick, with reduced shaped corner apertures and two 1.1 x 0.4 mm SW apertures separated by 0.2 mm. There are 14 copper pad numbers and 15 paste-only apertures. Numberless paste apertures have no copper and create no new electrical pad.

**EVIDENCE:** [SNVU621D EVM](https://www.ti.com/lit/pdf/snvu621), local `third_party/documents/ti_converters/lm61460_evm.pdf`, p18 BOM identifies RJR0014A. Layout drawings pp10-11 show short split VIN/PGND decoupling paths, wide power copper, quiet signal routing and thermal spreading. The EVM uses Q1 variants and an older board; it establishes placement/return intent, not an exact current-revision land/stencil overlay. The newer explicit package drawing controls geometry.

**DECISION:** 0.05 mm local non-solder-mask-defined expansion, within TI's 0.07 mm maximum example. Courtyard +/-2.50 x +/-2.25 mm is project allowance, not a TI specification. Thermal power lands must be soldered and tied to their named nets. No invented common ground thermal pad, and no vias are embedded in the footprint. R3 must implement thermal spreading without increasing the noisy SW area indiscriminately. Assembly process, stencil approval and actual thermal performance remain OPEN.

## Q101: every terminal and common drain

Primary [TI CSD19537Q3](https://www.ti.com/lit/ds/symlink/csd19537q3.pdf), local `third_party/documents/r2/TI_CSD19537Q3_SLPS549B.pdf`. Figure 3-1 and p8 top/bottom views: **1/2/3 source, 4 gate, 5/6/7/8 drain**. The exposed underside metal is drain, not ground and not an independent EP9.

The footprint follows p9's board pattern orientation: source/gate row below, pin1 lower left, gate4 lower right, drain8 upper left and drain5 upper right. This is a rotation of p8's top view, not a mirror. Four lower copper pads are 0.500 x 0.630 mm on 0.650 mm pitch at y=1.435, x=-0.975/-0.325/+0.325/+0.975 mm. Drain copper combines a 2.450 x 1.900 mm base (y=-1.340..+0.560) with four fingers extending to y=-1.750. Finger gaps are 0.150 mm and 0.410 mm deep. Overall top-to-bottom span is 3.500 mm; base-to-lower-row clearance is 0.560 mm.

The common base uses pad5; fingers carry 8/7/6/5 and physically overlap the base. These are intentionally one drain conductor, and all four symbol drain pins already share `VIN_EFUSE_IN`. Lower source pads remain geometrically separate and connect to their common schematic net in later layout. Paste follows p9: eight 0.340 x 0.450 apertures plus two 1.020 x 1.445 main-drain apertures. No paste is inferred from the full copper shape.

**DECISION:** project NSMD expansion 0.05 mm; courtyard +/-1.95 x +/-2.00 mm, covering maximum 3.4 mm body and copper with assembly allowance. These are assembly choices, not TI guarantees. Follow TI SLPA005 current-spreading/ringing guidance in R3; solder the drain area, spread source/drain current, keep gate routing separate. No automatic thermal-via array or 50 A current qualification is implied. Hot RDS(on), surge/SOA and assembly validation remain OPEN.

## R401: explicit Kelvin mapping

Primary [Vishay 30131](https://www.vishay.com/docs/30131/wsl2726.pdf), local `third_party/documents/Vishay_WSL2726_30131_2026-06-29.pdf`, p2. Body L=6.9 +/-0.2, W=6.6 +0.3/-0.2 mm. The solder-land sketch defines a=5.71 (force length), b=2.69 (bank width), c=0.89 (force/sense gap), d=0.89 (sense length), w=7.62 mm (outside width across banks). These are not pad-center coordinates.

**CALCULATED transcription:** bank centers x=+/-2.465 mm; force pads 2.69 x 5.71 mm at y=+0.890; sense pads 2.69 x 0.89 mm at y=-3.300. Total land length a+c+d=7.49 mm. Project numbering, absent from the manufacturer drawing:

| Pad | Top-view physical position | Function / schematic net |
| --- | --- | --- |
| 1 | Left wide pad | FORCE+ / VOUT_PROTECTED |
| 2 | Left narrow pad | SENSE+ / SHUNT_KPLUS |
| 3 | Right narrow pad | SENSE- / SHUNT_KMINUS |
| 4 | Right wide pad | FORCE- / LOAD_5V1 |

The device has no inherent electrical polarity; this mapping establishes positive module current. Assembly must align the narrow terminal/notch side with the footprint's sense side (negative Y); a 180-degree turn is not accepted merely because it is a resistor. The sense-side silk dot is a project orientation aid, not a claimed manufacturer pin1 mark. Preserve four separate copper pads; do not connect sense pads to force copper remotely or bypass the resistive element with a pour. The common metal within each terminal is part of the manufactured Kelvin geometry.

**DECISION:** use Vishay's land sizes with project 0.05 mm mask expansion and full-size paste as an initial assembly default. Vishay supplies no exact stencil-volume requirement here; stencil/voiding approval remains OPEN. Courtyard +/-4.10 x +/-4.05 mm encloses maximum body and recommended lands. Large power copper/thermal paths must follow the force terminals; no ground EP exists. At 5 A, nominal shunt loss is only 50 mW, but that does not validate board thermal capacity or accuracy.

## L201 and TDK: unresolved primary geometry

Coilcraft [exact part](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal8080/xal8080-682/) and [mechanical image](https://www.coilcraft.com/getattachment/78738e29-ddc3-4cbc-9810-2db76ca42dd3/xal8080d.gif?lang=en-US). The direct image/PDF retrieval still returns 403; web extraction confirms the image link but cannot display its GIF. The electrical PDF's text is readable but does not establish mechanical dimensions. **OPEN:** body/terminal dimensions, recommended copper, manufacturer orientation and tolerances. Installed footprint pads 1.78 x 7.00 at x=+/-2.58 mm remain **OBSERVATION of KiCad**, not manufacturer evidence. Courtyard and terminal numbering must be checked when the primary image is readable. No substitute third-party CAD was promoted to evidence.

TDK [exact product record](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C5750X7R1H226M250KB), live record checked 2026-09-14: body 5.70+/-0.40 x 5.00+/-0.40 x 2.50+/-0.30 mm, terminal B>=0.20 mm; PA=4.10..4.80, PB=1.20..1.40, PC=4.00..5.00 mm. The PA/PB/PC diagram itself remains unavailable. Generic 2220 has 3.3 mm inner gap, 1.8 mm pad length and 5.4 mm pad width, inconsistent with the documented recommendation under the earlier interpretation. **DECISION:** preserve rejection; do not author a supposedly exact land pattern until dimension orientation is verified. Nonpolar two-terminal part; project 1/2 assignment may follow existing capacitor symbols after geometry closure. No EP/thermal pad. A project footprint is likely required; exact mask/paste/courtyard remain OPEN.

## Reproduction and change control

[Generator](../../../../scripts/build_qualified_footprints.py) takes `--output-dir`; run with existing `.venv/bin/python` (PyMuPDF). It checks the source PDF hash before vector extraction. New source revisions require a fresh drawing review. [Tests](../../../../tests/test_qualified_footprints.py) independently check labelled extents, pin sets, paste count and four-terminal separation. See [verification procedure](QUALIFICATION_VERIFICATION.md) for CLI exports and current ERC.

The historical capture checker does not enforce blank footprints, so no enforcement migration or relaxation is needed. Its protection/Kelvin/domain/no-PCB checks remain intact. The historical schematic generator consumes the old block JSON and can overwrite recovered manual edits; **do not rerun it to rebuild this working schematic**. Its original capture contracts remain historical evidence. A future approved capture-generator migration must preserve these qualified assignments and the then-approved electrical contracts.
