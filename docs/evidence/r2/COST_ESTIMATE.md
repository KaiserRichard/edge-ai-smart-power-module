# V1A R2 Cost Estimate

STATUS: CONDITIONAL PASS for arithmetic and sourcing evidence only. NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED.

Access date: 2026-10-04. Currency presentation: USD and VND.

This is a planning estimate for the V1A test boards. Nothing was purchased, reserved, quoted through a logged-in cart, or released for fabrication. Distributor prices and stock are snapshots, not reservations. The estimate does not claim electrical safety or fabrication readiness.

## Executive totals

The totals below are CALCULATED known/estimated priced subtotals. They include the numeric 0.5 kg shipping proxies, the current-outline PCB placeholder, and one MEAN WELL DDR-60L-12. They exclude OPEN component, custom copper, hardware, route-specific shipping, customs/tax, and JLC live-quote adders.

| Scenario | Known USD total | VND at 25,980 VND/USD | Included board assumption |
| --- | ---: | ---: | --- |
| Current plan: 3 boards plus BOM spares | USD 2527.67 | 65,668,931 VND | 230 x 195 mm placeholder, 5-board JLC MOQ |
| Student minimum: 2 boards, MOQ-only extras | USD 2114.27 | 54,928,792 VND | 230 x 195 mm placeholder, 5-board JLC MOQ |

Labels: CALCULATED means arithmetic from a recorded or web snapshot; ASSUMED means a planning assumption; OPEN means no numeric amount was included.

Evidence vocabulary: OBSERVATION is a recorded BOM/layout or distributor fact; REQUIREMENT is imposed by the brief or project rules; ASSUMPTION is an unverified planning input; CALCULATION is derived arithmetic; HYPOTHESIS is a provisional comparison to be checked; EVIDENCE is a source snapshot or file; DECISION is an estimate choice; OPEN RISK is unresolved and excluded or clearly marked.

## Inputs and evidence

- [BOM_ORDER.csv](BOM_ORDER.csv), [BOM_ORDER.md](BOM_ORDER.md), [BOM_ORDER_LCSC.csv](BOM_ORDER_LCSC.csv).
- [BOM_ACCESSORIES.csv](bom_order/BOM_ACCESSORIES.csv), [FORCE_LINK_CALCULATIONS.json](bom_order/FORCE_LINK_CALCULATIONS.json), and the other bom_order JSON evidence snapshots.
- Read-only layout status: /Users/quockaiser/Desktop/Research/wt-pcblayout/docs/evidence/r3/layout/PROGRESS.md. The outline is not final: current tested envelope is 230 x 195 mm; 4 layers and 1.6 mm are retained; 70/35/35/70 um copper is ASSUMED, with 70 um outer copper treated as 2 oz. Layout routing and final DRC remain open.
- The BOM has 96 catalog-board rows, harness/mechanical/accessory rows, and OPEN procurement lines. Etched copper features B029, B078, and B079 are not purchased. O01/O02 parent rows are not charged; their concrete subparts are charged once. H07/H08 spool sharing is retained.

### Exchange-rate snapshots

- USD/VND: 1 USD = 25,980 VND, Wise page, access date 2026-10-04: https://wise.com/us/currency-converter/usd-to-vnd-rate
- EUR/USD: 1 EUR = 1.12525 USD, Wise history snapshot, used for B014 and H08: https://wise.com/gb/currency-converter/currencies/eur-euro/history
- AUD/USD: 1 AUD = 0.69565 USD, Wise history snapshot, used for B053: https://wise.com/au/currency-converter/aud-to-usd-rate/history
- CZK/USD: 1 CZK = 0.0463202 USD, Wise current/history snapshot, used for H05 web fill: https://wise.com/us/currency-converter/czk-to-usd-rate/history

### Web fills and official references

| Input | Snapshot and use | URL |
| --- | --- | --- |
| MEAN WELL DDR-60L-12 | Mouser: 314 in stock, USD 34.20 at quantity 1; added as a separate upstream-supply line | https://www.mouser.com/en/ProductDetail/MEAN-WELL/DDR-60L-12?qs=r5DSvlrkXmK4vGRVfx5SeQ%3D%3D |
| H05 3-87456-6 | Mouser Czech page: 65 in stock, 128.04 CZK each; web-only provisional fill, converted to USD 5.9308; original BOM snapshot remains unchanged | https://cz.mouser.com/ProductDetail/TE-Connectivity/3-87456-6?qs=E8qmh8kYf7K5RUvFCDM5vA%3D%3D |
| JLC batch-rate placeholder | Official JLC dynamic quote result used a visible 4-layer batch planning rate of USD 91/m2; this is not a live board quote | https://jlcpcb.com/api/components?search= |
| JLC PCB quote | Quote page supports the required dimension, layer, thickness, and copper selections; no live Gerber quote was available | https://cart.jlcpcb.com/quote |
| JLC capabilities | 4-layer FR-4 capability and 1.6 mm / outer copper options reference | https://jlcpcb.com/capabilities/pcb-capabilities/ |
| JLC shipping | Shipping is calculated from weight, destination, and method; no numeric Vietnam checkout quote was available | https://jlcpcb.com/help/article/how-much-does-shipping-cost |
| JLC assembly | Setup USD 8.00, stencil USD 1.50, SMT USD 0.0017/joint, USD 3/extended component type | https://jlcpcb.com/help/article/pcb-assembly-faqs |
| Distributor shipping | LCSC, Mouser, and DigiKey pages provide policy/rate-estimate mechanisms, not a logged-in Vietnam checkout price | https://fat.lcsc.com/help-center/shipping-delivering/shipping-cost-calculation ; https://www.mouser.com/en/saleterms/ ; https://www.digikey.com/en/help-support/delivery-information/international-shipping-rates |
| DHL proxy | 2026 Vietnam rate guide used only for a 0.5 kg planning proxy: China Zone 2 = 1,862,800 VND; US Zone 7 = 2,309,100 VND | https://mydhlplus.dhl.com/content/dam/downloads/vn/en/rate-guide/service_and_rate_guide_vn_en_2026.pdf.coredownload.pdf |

## A. Current plan

The current plan uses qty_to_order from the BOM: three boards plus its recorded spare rules. For each line, the numeric source is the cheapest complete in-stock offer in the BOM snapshots after converting the recorded EUR/AUD offers. H05 is the only line filled from a current web page because its BOM snapshot was OPEN.

| Cost block | USD | Classification |
| --- | ---: | --- |
| BOM catalog, harness, and priced accessory subparts | 2218.50 | CALCULATED from snapshots/web H05 |
| MEAN WELL DDR-60L-12, one unit | 34.20 | WEB SNAPSHOT; separate upstream supply |
| JLC 230 x 195 mm bare PCB placeholder, 5 boards | 25.51 | CALCULATED PLACEHOLDER / ASSUMED 2 oz multiplier |
| LCSC shipping proxy | 71.70 | ASSUMED |
| Mouser shipping proxy | 88.88 | ASSUMED |
| DigiKey shipping proxy | 88.88 | ASSUMED |
| Current known/estimated total | **2527.67** | CALCULATED |

Current BOM material source grouping (regional additional offers grouped by distributor family):

| Distributor family | Priced USD |
| --- | ---: |
| DigiKey | 861.21 |
| LCSC | 116.05 |
| Mouser | 1088.91 |
| Newark | 13.75 |
| RS | 138.58 |

OPEN current material lines: B009, B015, B038, B068, B080, B093, B026, M01, M02, M03, O01.5. The OPEN set includes the custom copper force links and hardware: B026 is 24 straps; M01 is 48 Wurth 00944 12 bolts; M02 is 96 RS 527381 washers; M03 is 48 RS 6655609 nuts. O01.5 is 100 SVH-41T-P1.1 contacts on an OPEN exact-stock line. Those amounts are not silently assigned a guessed price.

### PCB price sensitivity

The layout is still in progress, so the three board sizes requested by the brief are shown. All are planning placeholders, not quotes.

| Board size | Area (m2) | Placeholder USD/board | 5-board purchase | Use |
| --- | ---: | ---: | ---: | --- |
| 100 x 100 mm | 0.01000 | 1.1375 | 5.69 | Sensitivity only |
| 150 x 100 mm | 0.01500 | 1.7063 | 8.53 | Sensitivity only |
| 230 x 195 mm | 0.04485 | 5.1017 | 25.51 | Current-outline placeholder used in totals |

Method: CALCULATED area x 91 USD/m2 x 1.25. The 91 USD/m2 four-layer batch rate is a visible JLC planning snapshot; the 1.25 2 oz outer-copper multiplier is ASSUMED because a live quote could not be completed. The JLC quote interface shows a 5-board minimum for this planning path, so both 3-board and 2-board scenarios carry a 5-board placeholder. Final dimensions, stackup, copper weight, fabrication price, and shipping remain OPEN.

## B. Student minimum

The student plan uses two boards. A search of the provided BOM evidence found no explicit fragile, ESD, or 0402 spare marks. Therefore no discretionary spares were added. Extra pieces arise only from recorded MOQ, order-multiple, package, or captured price-tier constraints. This is a procurement minimum, not an electrical relaxation.

| Cost block | USD | Classification |
| --- | ---: | --- |
| LCSC-first 2-board BOM and accessory material | 1794.41 | CALCULATED from snapshots |
| MEAN WELL DDR-60L-12, one unit | 34.20 | WEB SNAPSHOT; separate upstream supply |
| JLC 230 x 195 mm bare PCB placeholder, 5 boards | 25.51 | CALCULATED PLACEHOLDER / ASSUMED 2 oz multiplier |
| LCSC shipping proxy | 71.70 | ASSUMED |
| Mouser shipping proxy | 88.88 | ASSUMED |
| DigiKey shipping proxy | 88.88 | ASSUMED |
| JLC SMT for selected standard-passive candidate set | 10.6968 | ASSUMED assembly comparison |
| Student known/estimated total | **2114.27** | CALCULATED |

Student material source grouping:

| Distributor family | Priced USD |
| --- | ---: |
| DigiKey | 620.36 |
| LCSC | 182.17 |
| Mouser | 839.55 |
| Newark | 13.75 |
| RS | 138.58 |

Student custom/hardware planning quantities are 14 straps, 28 bolts, 56 washers, and 28 nuts; exact cost/stock remains OPEN. The two-kit accessory calculation retains one black and one white 100 ft spool, and applies the recorded 100-piece MOQ to the JST contact lines; O01.5 remains OPEN.

### JLC SMT decision

The JLC candidate set is B001-B005, B007-B008, B010-B013, B036-B052, B054-B069, B071-B077: 51 standard passive BOM rows, 176 components per board, 352 components for two boards, and 704 estimated joints at two joints per passive. This joint count is an ASSUMPTION from component class, not a placement-file quote.

| Comparison | Calculation | USD |
| --- | --- | ---: |
| JLC SMT candidate set | USD 8.00 setup + USD 1.50 stencil + USD 0.0017 x 704 joints + USD 0 x 0 extended types | 10.6968 |
| Hand-solder comparison | USD 1.50 stencil + USD 0.08/joint assumed student labor x 704 | 57.82 |

The JLC line is included in the student total only for the candidate set and only under the ASSUMED zero-extended-component classification. If the exact parts are classified as extended, each adds USD 3; a quote must be obtained and that part should move to hand assembly whenever the extended fee makes it more expensive. Student labor is not charged in either total; the hand-solder rate is only a decision model. JLC assembly does not validate the schematic, layout, thermal design, or electrical safety.

Hand-solderable/manual-populate list:

- THT and off-board: B014, B016, B022-B025, H01, H05, H06, H07-H10, B026, M01-M03, and all O01/O02 subparts.
- Large or special SMD/manual candidates excluded from the JLC candidate set: B006, B009, B015, B017-B021, B027-B035, B053, B057, B070, and B080-B100.
- The standard passive candidate set above is also hand-solderable as a fallback. B080/B092 and other exposed-pad/fine-pitch devices are not beginner iron-solder parts; use hot-air/reflow or an assembly service after footprint and library review.

## C. Upstream supply line

MEAN WELL DDR-60L-12 is intentionally separate from the board BOM and appears in both totals as one unit at USD 34.20 from the Mouser web snapshot. It is an upstream bench/system supply assumption for this cost exercise; it does not assume the final WBR battery voltage or robot architecture.

## D. Cost drivers and swaps

Top ten current-plan priced material/accessory lines, excluding shipping and PCB placeholders:

| Rank | BOM line | MPN | Extended USD |
| ---: | --- | --- | ---: |
| 1 | H08 | 8521 010100 | 302.52 |
| 2 | H07 | 8521 002100 | 267.84 |
| 3 | H10 | 8502 010100 | 178.69 |
| 4 | H09 | 8502 002100 | 171.81 |
| 5 | O01.6 | 8125SHZBE | 159.50 |
| 6 | B053 | WFMB2512R0330FEA | 138.58 |
| 7 | B027 | 74437636351002 | 123.40 |
| 8 | B006 | C5750X7R1H226M250KB | 81.60 |
| 9 | B088 | LTC3115IFE-1#PBF | 78.60 |
| 10 | O01.7 | 3050 BK005 | 74.85 |

O01.8 3050 WH005 is tied with O01.7 at USD 74.85 and is the next line at the rank-10 cutoff.

Potential same-footprint cost reduction:

| Status | Current | Candidate | Evidence and constraint | Potential saving |
| --- | --- | --- | --- | ---: |
| ASSUMED - review required | B085 TPS7A1601DGNR, Mouser snapshot USD 4.21 x 7 | TPS7A1601DGNT, LCSC web snapshot USD 3.138 x 7 | TI lists both as the same TPS7A1601 device in HVSSOP (DGN), 8 pins, with LARGE T&R vs SMALL T&R carrier quantities. Confirm DGN thermal-pad footprint, exact packaging, date/stock, and assembly acceptance before changing the BOM. | USD 7.50 current; USD 4.29 student |

This candidate is not included in either total. Sources: TI ordering/package data https://www.ti.com/lit/gpn/TPS7A16 and LCSC price/stock page https://www.lcsc.com/es/product-detail/Linear-Voltage-Regulators-LDO_Texas-Instruments-TPS7A1601DGNT_C2865275.html. It is marked ASSUMED until reviewed.

Screened out: B006 C5750X7R1H226M250KB to TDK CGA9P3X7R1H226M250KB has the same nominal 22 uF/50 V/X7R/2220 description, but the web result showed LCSC out of stock and DigiKey USD 10.65 each versus the recorded Mouser USD 3.40 each. It is not a cheaper swap. Carrier suffix candidates for B084, B089, and B095 were not cheaper or lacked a complete cheaper in-stock price. No other safe cheaper swap is authorized.

## Open risks and handback

- The 230 x 195 mm outline is a placeholder. Layout routing, DRC, stackup, copper weight, fabrication price, and shipping are not final.
- B009, B015, B038, B068, B080, and B093 remain exact-part supply/price OPEN. B026, M01, M02, M03, and O01.5 remain OPEN. H05 is a web-only provisional fill and must be reconfirmed.
- Custom copper strap price, bolt/washer/nut prices, additional-supplier shipping, JLC PCB/PCBA shipping, customs, VAT, tariffs, and payment fees are excluded unless numeric above.
- Distributor stock is not reserved. EUR/AUD/CZK conversions and the DHL figures are snapshots/proxies.
- No manufacturing order, component purchase, cart, login, quote request, or hardware-file change was made.
- This estimate does not replace the R0-R5 engineering gates. It is not evidence of electrical correctness, thermal adequacy, mechanical contact performance, or safety.

The detailed line-level arithmetic, source URLs, access dates, open lines, sensitivity rows, and scenario inclusion flags are in [COST_ESTIMATE.csv](COST_ESTIMATE.csv).
