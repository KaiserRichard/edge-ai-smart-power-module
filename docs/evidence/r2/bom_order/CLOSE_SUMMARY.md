# BOM lock summary — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**Selection OPEN: 24 → 0. Immediate-procurement OPEN: 24 → 12.**

All 24 starting selections are LOCKED. The owner chose B045 option A on 2026-10-04: R203 is 24.6k, TNPW060324K6BEEA. Backorders, unpriced quotes and unconfirmed stock remain visible supply gaps; they are not requests for the owner to choose a component.

The procurement count includes complete offers in their published currencies, without conversion or mixing regional snapshots. NRND/EOL labels remain visible; the five exact Murata selections have an explicit finite-three-board disposition. The previous 27→24 review is preserved in LOCK_BASELINE.json and the original CLOSE evidence.

| Row | Chosen MPN | Selection | Reason | Route |
|---|---|---|---|---|
| B001 | GRM32ER72A105KA01L | LOCKED | Exact original in stock; preserves value, package, dielectric, bias and all frozen timing. EOL/NRND accepted only for this three-board build. | L001 |
| B002 | GRM188R71H104KA93D | LOCKED | Exact original in stock; preserves value, package, dielectric, bias and all frozen timing. EOL/NRND accepted only for this three-board build. | L002 |
| B003 | GRM32ER71H106KA12L | LOCKED | Exact original in stock; preserves value, package, dielectric, bias and all frozen timing. EOL/NRND accepted only for this three-board build. | L003 |
| B004 | GRM21BR71E105KA99L | LOCKED | Exact original in stock; preserves value, package, dielectric, bias and all frozen timing. EOL/NRND accepted only for this three-board build. | L004 |
| B009 | PCH1V471MCL1GS | LOCKED | Keep exact 470 uF/35 V polymer bank, ESR and 10x16 mm case; factory quote default. | Nichicon exact-part RFQ; price/stock/MOQ OPEN; no quote requested. |
| B011 | C3216X7R1H475K160AC | LOCKED | Production 4.7 uF/50 V/X7R/1206; AC characterized family is the disclosed AB bias proxy. | E001: Newark 95Y0089, 5 cut-tape pieces. |
| B013 | GRM1885C1H330JA01D | LOCKED | Exact original in stock; preserves value, package, dielectric, bias and all frozen timing. EOL/NRND accepted only for this three-board build. | L005 |
| B014 | EEU-FR1E221 | LOCKED | Exact straight-lead 220 uF/25 V FR, 8 mm diameter/3.5 mm pitch; no ESR or hold-up change. | E002: DigiKey Ireland P124223-ND, 8 bulk pieces; EUR kept separate. |
| B015 | SMCJ36CA | LOCKED | Preserve exact Littelfuse bidirectional 36 V SMC and frozen clamp; reject other makers same-number TVS. | Mouser 576-SMCJ36CA or DigiKey SMCJ36CALFCT-ND backorder; four pieces. |
| B026 | CUSTOM-FX-CU-01 RevA | LOCKED | Lock C110 30x15x2 mm, M4/20 mm drawing and tin finish; installed current/contact resistance are bench checks. | Make-to-drawing 24 straps; fabricator quotation OPEN, selection closed. |
| B038 | TNPW0805348KBEEA | LOCKED | Keep 348 kohm, 0.1%, 25 ppm/K TNPW0805; lower-power alternatives fail the rating rule. | LCSC C1709278 / Vishay authorized-distributor exact backorder or quote; five pieces. |
| B045 | TNPW060324K6BEEA | LOCKED | Owner chose option A on 2026-10-04: R203 24.6k, 0.1%, 25 ppm/K; nominal 5.065041 V. CALCULATED hot 5 A/20 mV path PASS +14.043 mV; 100 mV sensitivity FAIL -65.957 mV; qualification OPEN. | Mouser 71-TNPW060324K6BEEA: 5101 indexed stock, 5 required, USD 0.26 each; DigiKey UK 1920 stock (GBP). Reconfirm stock before any future order. |
| B053 | WFMB2512R0330FEA | LOCKED | Exact 33 mohm WFM, 1%, 50 ppm/K; custom lands match maker 1.55x3.60 mm pads/4.40 mm gap. | E003: RS Australia 188-0668; 55 pieces in tapes of five. |
| B068 | TNPW0805365KBEEA | LOCKED | Keep exact 365 kohm, 0.1%, 25 ppm/K divider parts; preserve supervisor thresholds and power rating. | Mouser 71-TNPW0805365KBEEA backorder/quote; eight pieces, price/availability OPEN. |
| B080 | TPS26630RGER | LOCKED | Keep TI TPS26630 RGE24 with MODE pin11 NC for latch-off; no clone or variant change. | Mouser 595-TPS26630RGER backorder; four cut-tape pieces. |
| B093 | INA228AIDGSR | LOCKED | Keep INA228 DGS10, range, pinout, calibration and telemetry interface; no monitor substitution. | DigiKey 296-INA228AIDGSRCT-ND backorder; four cut-tape pieces. |
| H01 | 1777989 | LOCKED | Manufacturer-listed screw-flange mate for 1776508; preserve J502 interface. | E004: Newark 69R9824, four pieces. |
| H05 | 3-87456-6 | LOCKED | Keep 40-position housing and 87309-9 contacts; preserve frozen Pi power-only pin allocation. | DigiKey A3044-ND exact housing backorder; four pieces. |
| H08 | 8521 010100 | LOCKED | Keep frozen black AWG16 conductor; one 100-foot spool covers J502 and added bench input leads. | E005: Mouser Europe 566-8521-100-10, one spool; EUR preserved. |
| M01 | 00944 12 | LOCKED | Exact M4x12 ISO4762 A2-70 bolt, 7 mm head, selected to the existing force-link drawing. | Würth article 00944 12; 48 pieces minimum; pack/quote OPEN. |
| M02 | 527381 | LOCKED | Plain A2 stainless washer, 4.3 mm ID/9 mm OD/0.8 mm thick, as specified. | RS 527-381 / Distrelec 30417580; one bag250 covers96; price/stock confirmation OPEN. |
| M03 | 6655609 | LOCKED | M4 A4 stainless all-metal Aerotight nut; no nylon insert; 7 mm wrench size. | RS US 70826017; two packs25 cover48, stock quantity basis requires reconfirmation. |
| O01 | XHP-2; XHP-4; SXH-001T-P0.6; VHR-2N; SVH-41T-P1.1; 8125SHZBE; 3050 BK005; 3050 WH005 | LOCKED | Define four complete input/control/I2C kits with keyed mates, gold dry contacts, labelled flying leads and manual links. | Order BOM_ACCESSORIES.csv O01.*; reuse H07/H08 spools for input leads; no duplicate spool charge. |
| O02 | 507302B00000G; 4880SG | LOCKED | Three individual TO-220 bolt-on sinks and insulating mounting kits per board; reserve envelope in layout. | Order BOM_ACCESSORIES.csv O02.*: 12 sinks and12 kits for four complete sets. |

## Owner decision taken

1. **B045 — DECISION TAKEN: A on 2026-10-04. LOCKED:** R203 24.6k, TNPW060324K6BEEA (0603, 0.1%, 25 ppm/K); R202 100k retained. Selection OPEN = 0. [CALCULATED review](../R203_OPTION_A.md): 5 A/20 mV PASS +14.043 mV; 100 mV sensitivity FAIL -65.957 mV. Electrical release remains BLOCKED.

## Supply gaps

| Row | Selected MPN | Remaining supply action |
|---|---|---|
| B009 | PCH1V471MCL1GS | Selection LOCKED; supply only: Nichicon exact-part RFQ; price/stock/MOQ OPEN; no quote requested. |
| B015 | SMCJ36CA | Selection LOCKED; supply only: Mouser 576-SMCJ36CA or DigiKey SMCJ36CALFCT-ND backorder; four pieces. |
| B026 | CUSTOM-FX-CU-01 RevA | Selection LOCKED; supply only: Make-to-drawing 24 straps; fabricator quotation OPEN, selection closed. |
| B038 | TNPW0805348KBEEA | Selection LOCKED; supply only: LCSC C1709278 / Vishay authorized-distributor exact backorder or quote; five pieces. |
| B068 | TNPW0805365KBEEA | Selection LOCKED; supply only: Mouser 71-TNPW0805365KBEEA backorder/quote; eight pieces, price/availability OPEN. |
| B080 | TPS26630RGER | Selection LOCKED; supply only: Mouser 595-TPS26630RGER backorder; four cut-tape pieces. |
| B093 | INA228AIDGSR | Selection LOCKED; supply only: DigiKey 296-INA228AIDGSRCT-ND backorder; four cut-tape pieces. |
| H05 | 3-87456-6 | Selection LOCKED; supply only: DigiKey A3044-ND exact housing backorder; four pieces. |
| M01 | 00944 12 | Selection LOCKED; supply only: Würth article 00944 12; 48 pieces minimum; pack/quote OPEN. |
| M02 | 527381 | Selection LOCKED; supply only: RS 527-381 / Distrelec 30417580; one bag250 covers96; price/stock confirmation OPEN. |
| M03 | 6655609 | Selection LOCKED; supply only: RS US 70826017; two packs25 cover48, stock quantity basis requires reconfirmation. |
| O01 | XHP-2; XHP-4; SXH-001T-P0.6; VHR-2N; SVH-41T-P1.1; 8125SHZBE; 3050 BK005; 3050 WH005 | Selection LOCKED; supply only: Order BOM_ACCESSORIES.csv O01.*; reuse H07/H08 spools for input leads; no duplicate spool charge. |

[Lock review](LOCK_REVIEW.md) records lands, ratings, frozen functions and the disclosed C351 family proxy. [Accessory definition](ACCESSORY_REVIEW.md) and [sub-BOM](BOM_ACCESSORIES.csv) close the harness/thermal identities. [Force-link drawing](FORCE_LINK_DRAWING.md): installed current, contact resistance, torque and pulse envelope are **bench check, does not block layout**.

Run `python3 docs/evidence/r2/bom_order/validate.py` and `python3 -m unittest tests.test_bom_order`. [VALIDATION.json](VALIDATION.json) and [R203 execution](../r203_option_a/EXECUTION.md) record checks and Git limitations. The historical capture is preserved; only R203 Value/MPN/Source changed in hardware under [owner option A](../R203_OPTION_A.md). PCB unchanged. R2 electrical release remains BLOCKED; no later gate is advanced.
