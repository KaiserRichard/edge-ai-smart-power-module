# Exact-stock and alternate review — 2026-10-04

**Historical review:** current defaults, updated offers and the sole owner decision are in [LOCK_REVIEW.md](LOCK_REVIEW.md) and [CLOSE_SUMMARY.md](CLOSE_SUMMARY.md). The earlier findings below remain evidence; a supply gap no longer means the owner must choose another component.

**CONFIRMED:** exact MPNs were searched first; the resume addendum below supersedes the earlier B033 and H01 findings; public indexed snapshots only, no account/cart/login/contact. Stock and prices can change. **OPEN** does not assert a part is nonexistent. Historical facts remain unchanged. New facts Q271–Q280 are in [CLOSE_CATALOG_FACTS.json](../../../../third_party/bom_order/CLOSE_CATALOG_FACTS.json).

**CONFIRMED closure:** B085 TPS7A1601DGNR, Mouser 595-TPS7A1601DGNR, 63 observed / 7 required, USD4.21 each at qty7, minimum/multiple1, factory16 weeks; exact original MPN. [Source](https://www.mouser.com/es/ProductDetail/Texas-Instruments/TPS7A1601DGNR?qs=KC2rBGieF4oE7JWkZS%2FgAQ%3D%3D), accessed2026-10-04, crawl4weeks. Incoming dates are excluded.

## Needs owner decision

| Row / original | Exact-source result; candidate if established | One-line hold |
|---|---|---|
| B009 PCH1V471MCL1GS | Manufacturer exact code confirmed; no stocked distributor offer established. Retain exact part for quote. | Different bank capacitor would change ESR/ESL, stored energy and fault containment; no proven same-land alternate. |
| B011 C3216X7R1H475K160AB | No current exact offer. Candidate [C3216X7R1H475K160AC](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X7R1H475K160AC): TDK exact production page, same1206/4.7uF/50V/X7R. | AB is not proven an ordering alias; original/alternate bias and auxiliary-converter behavior need review. Manufacturer table shows RS330 at2026-09-07, not a verified USD offer. |
| B014 EEU-FR1E221 | Retain exact bulk straight-lead part. Older US snapshot56 and French snapshot5 conflict with newer Q270 zero. | No closure from stale positive counts; lead-formed alternatives need mechanical and hold-up/ESR review. No fit-qualified substitute established. |
| B015 Littelfuse SMCJ36CA | Mouser0; existing DigiKey0. Candidate [Diodes Incorporated SMCJ36CA](https://www.diodes.com/part/view/SMCJ36CA), SMC bidirectional36V, clamp58.1V. | Same generic MPN is a different manufacturer/device: hot clamp, pulse and fuse/protection coordination require owner review. |
| B033 CSD18540Q5B | Exact0; candidate CSD18540Q5BT in alternative-packing listing atUSD4.53/min1; numeric stock/pack terms incomplete. | TI SLPS488B p1 lists sameSON5x6 device, reels250vs2500; obtain a coherent quantity/price offer before selection. Any different die/Rds(on) needs SOA/path review. |
| B038 TNPW0805348KBEEA | Exact stock not established. Candidate ERA-6AEB3483V, existing catalog evidence. | 0805/348kohm/0.1%/25ppm nominal match; different power/voltage/thermal behavior can shift input threshold. |
| B045 TNPW060324K4BEEA | Exact code unverified; no qualified24.4kohm/0.1%0603 substitute established. | Do not silently round to24.3k or24.9k: LM61460 output setpoint and Sheet03 path budget change. |
| B053 WFMB2512R0330FEA | 53required; three existing channels0, refreshed DigiKey0. Candidate WSL2512R0330FEB appears in distributor2512/33mohm/1% table. | 1W WSL differs from3W WFM copper-spreader construction; pulse/thermal/current-sharing and custom WFM lands unqualified. Do not substitute. |
| B068 TNPW0805365KBEEA | Exact0 in DigiKey substitute table; ERA-6AEB3653V candidate also0. | Input supervisor thresholds require power/voltage/TCR review. IBS listing calls this5.36k/thick-film while code is365k: rejected as identity-inconsistent. |
| B080 TPS26630RGER | Exact Mouser/DigiKey0. RGET candidate recentDigiKey0. | Preserve latch-off variant and RGE package; no stock closure; other TPS2663 variants change protection behavior. |
| B093 INA228AIDGSR | Exact recentMouser/DigiKey0. AIDGST candidate now Mouser Obsolete/restricted. | Reject old positive stock and obsolete packing suggestion; another monitor can change pins, range and telemetry behavior. |

Additional source register (all accessed2026-10-04):

- [EEU-FR1E221 US](https://www.mouser.com/en/ProductDetail/Panasonic-Industry/EEU-FR1E221?qs=tfZGHB2PWd1Rv9iToDM7xw%3D%3D): older crawl4weeks positive56; existing2026-10-03 Q270 crawl4days zero retained.
- [CSD18540Q5B TI datasheet](https://www.ti.com/lit/ds/symlink/csd18540q5b.pdf), SLPS488B April2017 p1 ordering table; [Q5BT Mouser India](https://www.mouser.in/en/ProductDetail/Texas-Instruments/CSD18540Q5BT?qs=NRIcxvoDUteGYlfdfF0DmQ%3D%3D), crawl3weeks stock90/min1/multiple1 but INR; do not combine with a different USD snapshot.
- [348k exact candidate row](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/RNCF0805BTE348K/6240068), crawl4months: exact Vishay0; [365k candidate table](https://www.digikey.com/en/products/detail/panasonic-industry/ERA-6AEB3653V/2025893), crawl5months: exactVishay0 and Panasonic0.
- [IBS inconsistent365k listing](https://www.ibselectronics.com/part/bc-components/tnpw0805365kbeea/2560549/), crawl3months: not accepted.
- [WSL2512R0330FEB candidate](https://www.mouser.in/c/passive-components/resistors/smd-resistors-chip-resistors/?case+code+-+in=2512&pg=2&resistance=33+mOhms), crawl3months stock1361; [Vishay WFM construction](https://www.vishay.com/docs/48828/_ss17197859-sell%20sheet_wfm.pdf), document48828/SS17197859, contrasts WFM with WSL; no pulse equivalence inferred.
- [TPS26630RGER](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS26630RGER?qs=vLWxofP3U2ztcw332RlqMw%3D%3D), crawl3weeks zero; [RGET](https://www.digikey.com/en/products/detail/texas-instruments/TPS26630RGET/10434724), crawl2weeks zero.
- [INA228 exact](https://www.digikey.com/en/products/detail/texas-instruments/INA228AIDGSR/13691042), crawl3days zero; [Mouser exact](https://www.mouser.fr/fr/ProductDetail/Texas-Instruments/INA228AIDGSR?qs=pUKx8fyJudB2qGvt%252BmXPAg%3D%3D), crawl1week zero; [AIDGST obsolete](https://hu.mouser.com/en/ProductDetail/Texas-Instruments/INA228AIDGST?qs=pUKx8fyJudB1B0ZroBoURA%3D%3D), crawl2months.

## Existing exact routes for partial-channel shortages

These rows already have sufficient exact stock in another channel in the pinned2026-10-03 register. Retain that MPN and use one route. Quantities and dates remain the recorded snapshots; no new live-stock claim.

| Row | MPN | Required | Sufficient exact channels / evidence |
|---|---|---:|---|
| B003 | GRM32ER71H106KA12L | 30 | lcsc: Q104 / stock41315 |
| B006 | C5750X7R1H226M250KB | 24 | mouser: Q058 / stock45172 |
| B010 | C1608C0G1H103J080AA | 8 | digikey: Q052 / stock26138 |
| B012 | C1608C0G1H102J080AA | 5 | digikey: Q050 / stock149480 |
| B017 | BAS116,215 | 30 | lcsc: Q039 / stock65200 |
| B018 | BAT46W-E3-08 | 4 | lcsc: Q042 / stock4435 |
| B021 | 3403.0285.23 | 5 | digikey: Q011 / stock1099 |
| B024 | 1776508 | 4 | mouser: Q003 / stock1177; digikey: Q001 / stock1384 |
| B027 | 74437636351002 | 5 | digikey: Q013 / stock13 |
| B028 | 7447789004 | 5 | digikey: Q015 / stock1170 |
| B030 | CSD19537Q3 | 4 | lcsc: Q077 / stock3779; digikey: Q076 / stock66702 |
| B034 | 2N7002,215 | 4 | lcsc: Q008 / stock275600 |
| B036 | TNPW0603332KBEEA | 5 | mouser: Q188 / stock2709 |
| B037 | TNPW060354K9BEEA | 5 | mouser: Q208 / stock3128; digikey: Q206 / stock98 |
| B040 | TNPW06034K02BEEA | 5 | mouser: Q201 / stock5350; digikey: Q199 / stock10881 |
| B060 | TNPW060388K7BEEA | 5 | digikey: Q217 / stock4608 |
| B063 | TNPW0805383KBEEA | 5 | digikey: Q226 / stock3853 |
| B067 | TNPW06036K49BEEA | 5 | digikey: Q215 / stock7189 |
| B069 | TNPW060348K7BEEA | 5 | mouser: Q195 / stock6337 |
| B077 | TNPW0603143KBEEA | 5 | digikey: Q166 / stock4900 |
| B082 | LTC7001IMSE#PBF | 4 | lcsc: Q125 / stock45; mouser: Q126 / stock199 |
| B084 | TLV3201AIDBVR | 14 | lcsc: Q153 / stock37123 |
| B088 | LTC3115IFE-1#PBF | 4 | mouser: Q123 / stock1054; digikey: Q121 / stock896 |
| B089 | TPS70933DBVR | 7 | lcsc: Q246 / stock21460 |
| B090 | ADG4612BRUZ | 10 | mouser: Q029 / stock445; digikey: Q027 / stock694 |
| B095 | TPS3808G50DBVR | 4 | lcsc: Q243 / stock576 |
| B096 | SN74LVC1G74DCTR | 10 | lcsc: Q144 / stock1568; mouser: Q145 / stock17460 |
| B098 | SN74LVC1G32DBVR | 4 | lcsc: Q141 / stock111770 |
| H01 | 1777989 | 4 | mouser: Q006 / stock10 |
| H08 | 8521 010100 | 1 | mouser: Q024 / stock2 |

H01/H08 stock-only routes still lack a complete USD/pack offer; H05 housing procurement remains OPEN. M01–M03 hardware purchase codes/quotes and O01/O02 harness/thermal definitions remain OPEN. Their stock rows are not engineering qualification. See generated CLOSE_SUMMARY.md for the complete deduplicated count.

**Provenance:** distributor pages are undated dynamic snapshots, copyright their respective owners, no open redistribution license established. Only factual observations retained; referenced, not copied/adapted circuitry. Manufacturer sources above and capacitor model data were read only. No third-party design or PCB reused.

## Resume addendum — 2026-10-04

**CONFIRMED B033 closure:** original CSD18540Q5B exact offers remain zero. The [TI SLPS488B ordering table](https://www.ti.com/lit/ds/symlink/csd18540q5b.pdf), April 2017 p1, lists CSD18540Q5B and CSD18540Q5BT as one SON 5×6 mm device with 2500/250-piece reel options. Shared electrical specifications are on p3, Q5B lands/pins on pp8–9. This is a carrier-only substitution, with no new electrical model or CAD change. **CONFIRMED:** [Mouser's US/Spanish page](https://www.mouser.com/es/ProductDetail/Texas-Instruments/CSD18540Q5BT?qs=NRIcxvoDUteGYlfdfF0DmQ%3D%3D) gives SKU 595-CSD18540Q5BT, stock592, minimum/multiple1, USD4.53 at seven units, factory9weeks (crawl last month). Accept seven cut-tape units for Q303/Q330. [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/CSD18540Q5BT/4915639) remains zero (crawl last week); its later expected inventory is excluded. These snapshots are independent offers, not combined stock/price fields.

**OPEN H01 correction:** the [newer exact Phoenix 1777989 Mouser page](https://eu.mouser.com/en/ProductDetail/Phoenix-Contact/1777989?qs=TrDcmYSSX9WKfp2I32hSmA%3D%3D), crawl2weeks, shows zero stock. It supersedes the older Q006 stock10 route above. Its EUR price is excluded from USD totals. H08 still lacks a coherent exact-SKU USD offer; indexed category results do not resolve the missing offer and are not substituted for the recorded page.

**EVIDENCE:** all links accessed 2026-10-04; Q281–Q283 in [CLOSE_RESUME_CATALOG_FACTS.json](../../../../third_party/bom_order/CLOSE_RESUME_CATALOG_FACTS.json), technical decision in [CLOSE_STOCK_DECISIONS.json](../../../../third_party/bom_order/CLOSE_STOCK_DECISIONS.json). Undated dynamic pages; copyright Mouser/DigiKey and TI, factual metadata only, no open redistribution license established. TI document referenced, no circuit copied or adapted. Other previously sourced searches/owner holds are retained, including the rejected INA228AIDGST packing proposal. No accounts, carts or purchases.
