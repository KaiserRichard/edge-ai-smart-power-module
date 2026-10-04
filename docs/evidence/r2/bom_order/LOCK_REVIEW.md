# BOM lock review — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Authority: BOM_LOCK_ALL.md; three boards plus spares; hardware read-only. Historical CLOSE evidence is preserved. This review distinguishes selected MPN, stocked offer, and electrical validation.

## Group 1 — exact capacitors

**DECISION:** B001, B002, B003, B004 and B013 retain their exact captured Murata MPNs. The brief prioritizes exact stock and does not prohibit finite-build purchases of NRND/EOL parts. Supplier lifecycle labels remain visible. This is an explicit finite-build lifecycle disposition, not a claim of renewed production.

**EVIDENCE:** [L001–L005](../../../../third_party/bom_order/LOCK_CATALOG_FACTS.json), all accessed 2026-10-04. B001 DigiKey 248,909 / 11 required; B002 LCSC 1,176,650 / 150 after pack rounding; B003 LCSC 36,990 / 30; B004 LCSC 17,770 / 30; B013 LCSC 77,750 / 50. Each stock/price/pack observation comes from one page. DigiKey cut-tape single-piece multiple is an explicit ordering assumption from the qty1 tier, to reconfirm at order time.

**CALCULATION:** replacement/original Ceff ratio is exactly 1 by identity, at every voltage in CLOSE_ALTERNATE_REVIEW.json; this does not invent an absolute Ceff for the two missing original curves. No capacitor substitution is made and no nearest-family estimate is needed for a relative comparison. Absolute Ceff(V,T,age) qualification remains at the original electrical gate.

**REQUIREMENT / EVIDENCE:** frozen S01-05/06, S02-04, S03-13/18 and S04-02 in [FREEZE_TABLE, 898759e](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FREEZE_TABLE.md), accessed 2026-10-04. Retaining C103 preserves the 100 nF ramp, C401 preserves the 20 ohm / 100 nF differential filter (79.577 kHz nominal), C374 preserves the >=0.5 uF/17.312 V and <=10 V/s qualification allocation, and C357 preserves the 33 pF feedforward compensation. No tolerance or threshold is widened.

**OPEN RISK:** residual lots must meet original specifications; stock snapshots expire. Earlier alternate candidates remain historical, unselected proposals. Bench qualification is not established by this choice.

## Land, package and electrical comparison

**EVIDENCE:** every source below is identified with URL, revision, relevant pages, access date, use and attribution in [LOCK_SOURCES.json](../../../../third_party/bom_order/LOCK_SOURCES.json). Read-only PDF hashes are retained. Original catalogue facts and CLOSE review JSON remain unchanged. All cited web pages were accessed2026-10-04; their crawl ages are separate from access dates.

| Rows | Maker drawing versus assigned footprint | Result for the selected default |
|---|---|---|
| B001/B003 | Murata GRM32:3.2×2.5 mm case; KiCad C1210 pads at±1.475,1.15×2.70 mm | Same original two nonpolar terminals; package/terminal overlap preserved |
| B002/B013 | Murata GRM18:1.6×0.8 mm; C0603 pads at±0.775,0.90×0.95 mm | Exact originals; no pin/value/dielectric/rating change |
| B004 | Murata GRM21:2.0×1.25 mm; C0805 pads at±0.95,1.00×1.45 mm | Exact original, including C374; no change to slew-control capacitance |
| B009 | Nichicon PCH standard10×16 mm; platform10.3 mm, terminal spread11 mm; custom pads at±4.2,4.4×2.5 mm | Retain exact polar470µF/35V polymer;1 positive/2 negative; no vibration-version substitution |
| B011 | TDK AC case3.2±0.2×1.6±0.2×1.6±0.2 mm, terminal≥0.2 mm; C1206 pads at±1.475,1.15×1.8 mm | Same1206 two nonpolar terminals, full terminal overlap; no footprint edit |
| B014 | Panasonic FR bulk8 mm diameter,3.5 mm leadpitch; CP_Radial_D8.0mm_P3.50mm | Exact straight-lead part;1 positive/2 negative, no lead-formed suffix |
| B015 | Littelfuse DO-214AB/SMC two-terminal drawing; standard D_SMC pads at±3.4 mm | Original bidirectional device retained; no polarity swap or same-name maker substitution |
| B038/B068 | TNPW0805 body2.0×1.25 mm; R0805 pads at±0.9125,1.025×1.4 mm | Exact348k/365k originals; preserve0.1% and25ppm/K |
| B045 | TNPW0603 body1.6×0.8 mm; R0603 pads at±0.825,0.8×0.95 mm | Physical package fits; nominal24.4k ordering identity is the hard stop |
| B053 | Vishay WFM2512 maker lands1.55×3.60 mm,4.40 mm innergap; custom centers±2.975 mm | Exact match; retain33mΩ/1%/50ppm/K WFM construction |
| B080 | TI RGE0024H4×4 mm,0.5 mm pitch,2.7×2.7 mm EP | Exact TPS26630RGER; existing numbered-land/pin review retained |
| B093 | TI DGS10,VSSOP3×3 mm,0.5 mm pitch,noEP | Exact INA228AIDGSR; existing numbered-land/pin review retained |

**DECISION:** standard IPC library pads are not represented as exact manufacturer-recommended solder-process lands. For example, TDK C351 preferred reflow gap2.0–2.4 mm/width1.1–1.6 mm differs from the existing gap1.8/width1.8 mm. The AC terminals still fit: at minimum0.2 mm termination and3.0–3.4 mm body length, the end-termination interval lies within the pad's0.9–2.05 mm radial span. The selected device needs no mechanical footprint change. Retain the original footprint and review paste/wetting/placement tolerances at R3. Original Murata library pads likewise retain their IPC land choices. This check establishes physical fit, not process qualification.

## Group 2 — remaining board parts

**DECISION B011:** select **C3216X7R1H475K160AC**. TDK's current product record confirms production4.7µF,50V,X7R,±10%,1206/1.6 mm height. The captured AB code is not asserted to be an alias. Neither a current AB-specific offer nor an AB-specific DC-bias curve was established. Under the brief's express nearest-characterized-family allowance, use the **same maker's C3216X7R1H475K160AC characterization sheet,20-Jan-2020**, as the original AB estimate. It matches nominal value, voltage, dielectric, tolerance and dimensions. C351 is auxiliary **input** bypass, not C357 feedforward or a protection-timing capacitor; no converter output/compensation values change.

**ASSUMPTION / CALCULATION:** at C351's actual AUX_LIMITED-to-GND voltages26V,30.788889V and35V, `Ceff_AB_est(V)=Ceff_AC_characterized(V)`, so the estimated replacement/original ratio is1.000 at all three points (within0.90–1.10). This is a disclosed family-proxy comparison, **not measured AB equivalence or a guarantee of ±10% across lots/temperature/aging**. No fabricated numeric absolute capacitance is supplied. The published curve is typical, and the original unknown AB response remains the evidence limit. These assumptions are machine-readable in LOCK_DECISIONS.json. Newark E001 provides the exact selected AC code and a coherent cut-tape offer. Check input ripple/temperature at bring-up.

**DECISION B009/B014:** exact originals avoid uncertainty about polymer-bank ESR/fault energy or electrolytic hold-up. Their Ceff ratio is1 by identity at any applied voltage. PCH initialESR14mΩ and ripple3.1Arms at135°C/100kHz are manufacturer's conditions, not installed current approval. PCH order selection is fixed to the catalogue code even though an authorized supplier quote remains needed. Panasonic has a separate EUR bulk offer; no US price/European stock splice is made.

**DECISION B015:** retain **Littelfuse** SMCJ36CA:36V stand-off,40–44.2V breakdown at1mA,58.1V clamp at25.9A under the specified pulse test. The local read-only file named SMCJ36CA.pdf actually describes **Vishay** and was rejected as manufacturer evidence for this selection. Littelfuse's own JC.02/27/25 v.2 sheet is authoritative. Hot clamp/source/fuse coordination is still unvalidated; a distributor's “direct” equivalent does not replace it.

**DECISION B038/B068:** keep Vishay TNPW0805 exact348k/365k identities on backorder/quote. The2026 TNPW table gives up to0.260W for0805 and0.210W for0603 in its advanced rating mode, with lower general/power-mode ratings;150V/100V limiting element voltages respectively. No larger dissipation allowance is granted to the actual PCB. Proposed Panasonic ERA0805 parts are0.125W and are rejected under the brief's no-rating-reduction rule. Exact identity preserves the frozen resistor tolerance/TCR, input OVP minimum26.973872559V and supervisor thresholds; no new threshold margin is claimed.

**DECISION B053:** keep WFMB2512R0330FEA. Maker30387 specifies4W at70°C terminal or3W at95°C terminal; the catalogue's3W shorthand is not the ambient-board rating. Preserve componentTCR±50ppm/K,1% tolerance and the manufacturer WFM lands. RS Australia E003 supplies55 pieces in five-piece tapes for53 required. The1W WSL proposal is rejected; pulse-energy/thermal/current-sharing tests remain. The telemetry2mΩ shunt and its Kelvin routing are untouched.

**DECISION B080/B093:** retain TI identities via exact backorders. TPS26630RGER preserves IN1/2,IN_SYS5,GND8/EP25,MODE11 NC selecting latch-off,SHDN12 andOUT17/18. Neither TPS26631 nor a same-number third-party clone is selected. INA228AIDGSR retains DGS10 pinout,85V monitor family,shunt ranges,calibration and I2C behavior; the obsolete/restricted AIDGST channel proposal stays rejected. Frozen current-limit resistor18/Rk and timing targets remain unchanged; no tested protection claim follows from order selection.

## Sole value-change decision — B045

**OBSERVATION:** Vishay's TNPW series publishes E24/E192 preferred values;24.4k is not one of those entries. Searches did not establish an orderable exact24.4k/0603/0.1%/25ppm/K equivalent with equal ratings. This does not prove custom production impossible. Do not purchase an MPN assembled from the ordering-code grammar alone.

**CALCULATION:** frozen R202100k/R20324.4k and1V reference give `1+100/24.4=5.098360656V`. A24.3k part gives5.115226337V and violates the frozen **no setpoint increase** rule. A24.6k part gives5.065040650V,33.320mV lower (−0.654%). The concrete [TNPW060324K6BEEA catalogue listing](https://www.digikey.co.uk/en/products/detail/vishay-dale/TNPW060324K6BEEA/4972391), accessed2026-10-04, establishes the proposed A code. It still changes the schematic nominal value and requires recalculating the complete load/path budget before adoption. It is **not selected into the BOM**. Option B retains24.4k and seeks an actual manufacturer-confirmed custom identity. [OWNER_DECISIONS.md](OWNER_DECISIONS.md) contains the only A/B question.

## Group 3 — external and mechanical identities

**DECISION H01/H05/H08:** exact Phoenix1777989 mating1776508, TE3-87456-6 with87309-9 contacts, and Belden8521 010100 blackAWG16 spool remain fixed. Preserve the frozen Pi40-position power-only allocation:5V pins2/4 and grounds6/9/14/20/25/30/34/39; other cavities empty. J502 hot-pole resistance/current-sharing tests and the published connector current ratings remain separate. Newark E004 and Mouser Europe E005 provide coherent offers for H01/H08. H05 remains an exact backorder, not an owner component-choice request.

**DECISION B026/M01/M02/M03:** drawing and finishing/tolerances are adopted as reasoned defaults in the [force-link addendum](FORCE_LINK_DRAWING.md), with Würth00944 12 bolts,RS PRO527381 washers and6655609 all-metal nuts. The4.3 mm washer bore clearsM4 and9 mm OD stays within the10 mm force pad; no insulation washer is placed in the electrical contact path. The30×15 mm strap and20 mm pitch are unchanged. Two washers and one nut per joint require48/96/48 items for24 straps. Bag/pack rounding is explicit; the ambiguous RS nut stock unit is not used to claim stock.

**CALCULATION / ASSUMPTION:** existing board thickness1.6 mm plus2 mm strap and2×0.8 mm washers leaves6.8 mm of an M4×12 shank for nut engagement/protrusion. Nut locking engagement, actual stack tolerances, flatness, torque, creep, resistance and temperature are **bench check, does not block layout**; no unverified assembly torque is invented. The hardware supplies the existing joint envelope without a PCB change. Obtain the fabricator's exact commercial quote before any eventual authorized order.

**DECISION O01/O02:** [ACCESSORY_REVIEW.md](ACCESSORY_REVIEW.md) defines every selected MPN, quantity, connector cavity, loose manual-link default and thermal envelope. These remove undefined accessory placeholders without asserting thermal validation or a host-specific end connector.
