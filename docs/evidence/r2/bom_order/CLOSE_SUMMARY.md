# BOM close summary — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**CONFIRMED:** OPEN order rows **27 → 24**. Closed B007, B008, B033, B085; newly OPEN B003 (EOL).

Purchased row without at least one exact/accepted MPN offer with SKU, enough stock, USD price and known multiple, or unresolved lifecycle/exact-code/owner hold. Count once per row; secondary missing channels are not extra blockers.

Literal CSV cells equal to OPEN: 1461 → 1462; rows containing OPEN text: 109 → 109. These secondary metrics include absent supplier channels and unneeded alternates, so they are not a blocker count. The CSV columns are unchanged.

## Selected alternates

| Row | Captured original → selected alternate | Reason / bias evidence | Stock route |
|---|---|---|---|
| B007 | GRM21BR71E475KA73L → GRM21BZ71E475KE15L | Original NRND/EOL; retain nominal capacitance, dielectric and footprint CALCULATED worst ratio 98.45%: 4.88147 → 4.80601 µF at 2.5 V (C302). | mouser |
| B008 | GRM21BR71H105KA12L → GCM21BR71H105KA03L | Original NRND/EOL; retain nominal capacitance, dielectric and footprint CALCULATED worst ratio 98.86%: 0.440358 → 0.43534 µF at 35 V (C307). | digikey |
| B033 | CSD18540Q5B → CSD18540Q5BT | Exact original out of stock; manufacturer confirms same device/package in 250-piece instead of 2500-piece reels. | mouser |

**CONFIRMED exact-part closure:** B085 retains TPS7A1601DGNR; Mouser Q277 stock63 / required7, USD4.21 each. This is not a component substitution.

[Capacitor review](CAPACITOR_REVIEW.md) contains every original/alternate effective capacitance at the evaluated net voltages, manufacturer provenance and timing holds. [Stock review](STOCK_REVIEW.md) records exact-first sourcing and the TI carrier-only decision. Prices/stock are dated indexed snapshots, not live reservations.

## Needs owner decision

| Row | MPN / purpose | Reason |
|---|---|---|
| B001 | GRM32ER72A105KA01L | original absent from Murata SimSurfing; original/alternate effective capacitance comparison unavailable. TDK nominal same-package in-production candidate only; do not substitute. |
| B002 | GRM188R71H104KA93D | C103 sets input DVDT/startup; C401 sets telemetry filter timing. Different bias behavior needs owner timing review before a grouped-row substitution. |
| B003 | GRM32ER71H106KA12L | original absent from Murata SimSurfing; original/alternate effective capacitance comparison unavailable. TDK nominal same-package in-production candidate only; do not substitute. |
| B004 | GRM21BR71E105KA99L | C374 sets HOLD_SLEW_C timing and >=0.5 uF requirement; changing its bias curve needs owner timing review. |
| B009 | PCH1V471MCL1GS | Exact PCH1V471MCL1GS supplier quote required; another bank capacitor changes ESR/ESL, energy and fault behavior. |
| B011 | C3216X7R1H475K160AB | C3216X7R1H475K160AB ordering code unverified; AC candidate needs bias, lands and converter review. |
| B013 | GRM1885C1H330JA01D | C357 is LTC3115 feedforward compensation; loop/timing qualification is not established by nominal C0G and bias matching. |
| B014 | EEU-FR1E221 | Exact straight-lead EEU-FR1E221 stock absent; another part needs lead-fit, ESR and hold-up review. |
| B015 | SMCJ36CA | Exact Littelfuse SMCJ36CA stock absent; Diodes same-number candidate needs hot-clamp/pulse/fuse coordination review. |
| B026 | CUSTOM-FX-CU-01 RevA | Approve force-link finishing/tolerances, joint stack/torque and installed current envelope; fabricator quote required. |
| B038 | TNPW0805348KBEEA | Exact 348 kohm resistor stock absent; ERA-6AEB3483V power/voltage/thermal margins affect protection threshold. |
| B045 | TNPW060324K4BEEA | Exact 24.4 kohm order code unverified; rounding changes output setpoint and Sheet03 path budget. |
| B053 | WFMB2512R0330FEA | 53 exact WFMB2512R0330FEA ballast parts unavailable; 1 W WSL candidate needs WFM-land, pulse, thermal and sharing review. |
| B068 | TNPW0805365KBEEA | Exact 365 kohm resistor stock absent; Panasonic candidate also lacks stock and threshold power/voltage/TCR review. |
| B080 | TPS26630RGER | TPS26630RGER/RGET stock absent; preserve latch-off variant, timing, current limit and RGE pinout. |
| B093 | INA228AIDGSR | INA228AIDGSR stock absent; obsolete/restricted AIDGST proposal rejected. Different monitor needs range/pin/telemetry review. |
| H01 | 1777989 | Exact 1777989 stock absent in newer Mouser/DigiKey snapshots; confirm source for the selected mating plug. |
| H05 | 3-87456-6 | Exact 3-87456-6 housing stock absent; marketplace supply is not accepted; confirm exact housing source. |
| H08 | 8521 010100 | Exact 8521 010100 needs one coherent supplier SKU/stock/USD price/pack offer for a 100 ft spool. |
| M01 | M4 bolts for seven links | Choose and quote exact M4x12 A2-70 bolt code after force-link joint-stack approval (48 required). |
| M02 | M4 washers for seven links | Choose and quote exact 4.3/9/0.8 mm washer code and finish (96 required). |
| M03 | M4 nuts for seven links | Choose and quote exact all-metal M4 nut code/finish after stack/torque review (48 required). |
| O01 | Input / control / I2C mating harnesses | Define input/control/I2C mating harnesses, contacts, wire and manual links before quantities and sourcing. |
| O02 | Thermal / assembly accessories | Define thermal interfaces, live-tab insulation and mounting after thermal/layout review before sourcing. |

**CALCULATED force-link screen:** [30×15×2 mm C110 strap](FORCE_LINK_DRAWING.md), 20 mm M4 pitch, conditional 8 A / 20 K rise at 40°C ambient; contact and pulse qualifications remain OPEN. No verified catalog equivalent.

## Validation and handback

Run `python3 -B docs/evidence/r2/bom_order/validate.py` and `python3 -B -m unittest discover -s tests -p test_bom_order.py -v`. [VALIDATION.json](VALIDATION.json) records document/evidence checks; [CLOSE_EXECUTION.md](CLOSE_EXECUTION.md) records execution and Git limitations. No electrical-release claim follows from these checks. The captured source BOM and all hardware remain unchanged; ERC/DRC were not rerun. R2 remains blocked; no later gate is advanced.
