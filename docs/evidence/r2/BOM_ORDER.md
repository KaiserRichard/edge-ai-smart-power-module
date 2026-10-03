# V1A R2 order BOM — three boards plus spares

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**STATUS: BLOCKED for a complete order.** The procurement register is synchronized and every unavailable or unverified commercial field is marked **OPEN**. It is not a claim that all parts can be purchased today or that the R2 design is electrically released. No purchase, cart, quote request, CAD edit, merge or push was made.

**EVIDENCE — 2026-10-03:** KiCad 9.0.6 BOM export from a detached `/tmp` copy of [`origin/feat/r2-testboard-capture` at `56e9837`](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/56e9837e522c01bd680aca602f9f471d38d6039f/hardware/kicad/V1A.kicad_sch). The resumed fetch advances the recorded source from `6d25cf2` to the current branch tip (PCB preparation and documentation only). All six schematic hashes are unchanged and the fresh export has identical SHA-256 `b2e57ccf9cfd4251d297d6e2bb6b422f2bfc0aead7b5d0fec14f03fad456acae`. The source contains **366 references: 298 catalog components across 96 MPNs, seven custom links, and 61 etched PCB features**. Power flags are excluded by KiCad; the exported physical references have no DNP marks. Manufacturer fields are blank in the export; names come from the existing selection register and exact catalog identities, never invented schematic fields.

[BOM_ORDER.csv](BOM_ORDER.csv) contains every reference, footprint, quantity, supplier SKU, supplier-specific order quantity, USD unit/extended price, stock, lead time, lifecycle, source URL, observation date, crawl age and alternate disposition. [SOURCE_BOM.csv](bom_order/SOURCE_BOM.csv), [PROVENANCE.json](bom_order/PROVENANCE.json), [RECONCILIATION.json](bom_order/RECONCILIATION.json) and [TOTALS.json](bom_order/TOTALS.json) make the arithmetic and synchronization reviewable. Historical BOM_DRAFT files are preserved.

## Quantities and commercial interpretation

**DECISION:** aggregate identical exact MPNs over all five sheets before calculating spares. For each resistor, capacitor, inductor or fuse: `base = 3 × quantity per board`, `spares = max(2, ceil(base × 10%))`. Other catalog parts and custom links use `max(1, ceil(base × 10%))`. Etched pads have an instance count but **zero purchased pieces**. A link kit is supplied for all seven positions; fitting depends on the isolated-test configuration.

**CALCULATION:** each distributor quantity rounds that planning quantity up to its retrieved minimum/multiple. Unit price uses the largest displayed applicable tier, for cut tape or bulk/tube where identified. Cut-tape and Digi-Reel prices are kept distinct; no reeling fee is silently included. A minimum inferred from the first displayed tier and an assumed single-piece multiple are labeled in CSV notes. An unknown multiple remains OPEN and requires pack confirmation. Wire columns distinguish metres consumed from whole **100-foot (30.48 m) spools** ordered; one spool of each selected colour/gauge covers the three harnesses and `max(10%, 1 m)` cutting allowance.

**EVIDENCE LIMIT:** website/index snapshots, not live reservations or firm quotes. Each stock/price offer is one coherent retrieved snapshot; an independently linked SKU/alias identity source is identified when needed; stock and price are not stitched from unrelated pages. Prefer complete exact-SKU evidence, then the more recent crawl. Pages with another manufacturer's same-number component, unmatched suffixes or unverified marketplace supply do not become selected offers. OPEN does not mean zero stock or EOL. Lifecycle is labeled by channel; channel withdrawal is not manufacturer EOL. Shipping, tax, duty, tariffs, reeling, assembly, PCB, custom fabrication and external test equipment are excluded from numeric subtotals. Reconfirm published prices, quantities and stock before ordering.

## JP201 / JP501 and U316 dispositions

**DECISION — identities closed:** JP201 and JP501 both resolve to **CUSTOM-FX-CU-01 RevA**, as do JP101, JP202, JP301, JP330 and JP331. This is an authored removable force-link drawing, **not a distributor MPN**. Catalog MPN is N/A; qualified fabricator, purchased stock/subpart MPNs and price remain OPEN. [Captured pin review](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/56e9837e522c01bd680aca602f9f471d38d6039f/docs/evidence/r2/gate4b/PIN_REVIEW.md) and [Sheet05 review](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/56e9837e522c01bd680aca602f9f471d38d6039f/docs/evidence/r2/gate4b/SHEET05_REVIEW.md) establish the exact interfaces. No 2.54 mm shunt is substituted.

The pinned [fixture drawing description](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FIX3_FIXTURE.md) specifies C110 copper 2 mm × 15 mm, span ≤30 mm, 4.5 mm holes on 20 mm pitch; M4×12 A2-70 bolts, two 4.3/9/0.8 mm washers and an all-metal M4 nut per joint. Seven links imply 14 joints per board. Accessory rows enumerate those subparts without inventing supplier codes; finishing, actual stackup, insulation, torque, contact resistance and parasitic qualification remain OPEN. These subparts make up the custom links and are not extra schematic instances.

JP201 joins native BUCK_SW to L201_IN and is removed for isolated tests. JP501 joins LOAD_5V1 to LOAD_FIXTURE; opening it does not isolate an attached J502 load. The separate force return is PF5.

**U316: CONFIRMED — LT4363HMS-1#PBF.** The resume brief explicitly closes the original pending check. The [C1–C3 pin review](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/56e9837e522c01bd680aca602f9f471d38d6039f/docs/evidence/r2/gate4b/CHECK_C1C3.md) records ADI LT4363 Rev. C, pp. 2, 3 and 8: the captured -1 variant uses the 12-pin MSOP mapping. Order planning is **4 pieces** (three boards plus one spare); the obsolete U316-specific hold is removed from the CSV and LCSC subset. No -2 substitution or circuit change is made. Electrical release remains a separate gate.

## Sheets 03–05 synchronization

**OBSERVATION:** all 366 native references are represented once in the board register, including Sheet03's 280, Sheet04's 23 and Sheet05's 11. Compared with the earlier draft, 153 references are added and 49 retired. The detailed reconciliation also records identity/feature-label changes. Obsolete AHCT/control proposals and draft DNP rows do not drive quantities. The manual source-fault hook and actual observation front end replace the old unquantified on-board FAULT_TRIGGER placeholder; the separately documented external injection fixture is outside this board BOM.

R312 is now 32.4 kohm (shared with R600); R341 is 88.7 kohm. All added R6xx/R7xx/U6xx/C6xx/C7xx parts and revised bypass counts come directly from the export. C350 remains captured as 10 nF. The Panasonic export spelling EEUFR1E221 is normalized only for distributor matching to EEU-FR1E221; [Panasonic's model page](https://na.industrial.panasonic.com/products/capacitors/aluminum-electrolytic-capacitors/series/83367/model/83695) confirms the 220 uF / 25 V bulk straight-lead part, 8 mm diameter and 3.5 mm pitch.

## Remaining procurement blockers

- **C351:** exact captured C3216X7R1H475K160AB ordering code not verified. The independently listed AC suffix is an unapproved candidate, not a spelling correction.
- **R203:** exact TNPW060324K4BEEA listing/orderability is OPEN. Preserve 24.4 kohm; do not substitute a neighbouring value without recalculating and approving the feedback network.
- **R376/R378:** captured TNPW0805365KBEEA still has no verified selected-part price or stock; the Panasonic 365 kohm candidate remains unapproved because its power/voltage qualification differs.
- **PCH1V471MCL1GS:** [Nichicon's 2026 catalog](https://www.nichicon.co.jp/_assets/images/products/catalog/corporate/digital/sh_pch.pdf) confirms the exact 470 uF / 35 V, 10×16 mm code. Supplier SKU, price, stock and lead time remain OPEN. A different bank capacitor requires ESR/ESL, fault-energy and thermal review.
- **Supply / lifecycle:** EOL/NRND capacitors, unstocked semiconductors and ballast resistors, and single-observed-source rows are flagged below. Alternates are identified where verified; **OPEN alternate** is an unresolved action, never approval to buy a constructed MPN. Different carrier suffixes are distinguished from different packages; where TI explicitly confirms the same device/package, the alternate register records that evidence. Remaining alternatives require manufacturer review. Distributor “Direct” or “Similar” labels do not establish electrical equivalence.
- **Custom / harness / thermal:** link fabrication and accessory codes, mating input/control/I2C harnesses, live-tab insulation/heatsinking, tools/splices and assembly costs remain OPEN. The chosen J502/Pi harness is listed separately and has unvalidated hot-contact/current-sharing behaviour. No SBC as the first load.

## Distributor totals

Each channel column is an alternative whole-build scenario. **Do not add the three distributor totals together.** Known-price subtotals include priced backorders and confirmed U316; stock-sufficient subtotals are still not an engineering release or complete order. All custom/accessory and complete-kit totals remain **OPEN**.

| Distributor | Complete catalog-board total | Known-price subtotal USD | Coverage | Stock-sufficient priced subtotal USD | Harness subtotal USD / coverage |
|---|---|---:|---|---:|---|
| lcsc | OPEN | 595.13 | 54/96 | 254.28 (42 lines) | 0.00 / 0/7; complete OPEN |
| mouser | OPEN | 720.57 | 47/96 | 444.25 (33 lines) | 350.50 / 2/7; complete OPEN |
| digikey | OPEN | 937.85 | 82/96 | 619.14 (63 lines) | 581.46 / 5/7; complete OPEN |

## Parts and quantities

| ID | Refdes / purpose | Per board | 3-board base | Spares | Planning order | MPN | Manufacturer | Flags |
|---|---|---:|---:|---:|---|---|---|---|
| B001 | C101, C102, C378 | 3 piece | 9 | 2 | 11 piece | GRM32ER72A105KA01L | Murata Electronics | NRND/EOL(mouser); NRND/EOL(digikey) |
| B002 | C103, C203, C204, C205, C303, C304, C308, C354, C355, C364, C368, C369, C370, C376, C380, C401, C402, C405, C406, C604, C609, C640, C642, C644, C647, C651, C710, C711, C712, C714, C715, C716, C717, C723, C728, C730, C731, C732, C733, C754, C756, C761, C762 | 43 piece | 129 | 13 | 142 piece | GRM188R71H104KA93D | Murata Electronics | NRND/EOL(mouser); NRND/EOL(digikey); SINGLE-OBSERVED(lcsc) |
| B003 | C201, C202, C305, C306, C352, C377, C601, C602, C660 | 9 piece | 27 | 3 | 30 piece | GRM32ER71H106KA12L | Murata Electronics | OOS(digikey); CHANNEL-RESTRICTION(digikey); SINGLE-OBSERVED(lcsc) |
| B004 | C206, C301, C309, C365, C367, C374, C375, C600 | 8 piece | 24 | 3 | 27 piece | GRM21BR71E105KA99L | Murata Electronics | NRND/EOL(mouser); NRND/EOL(digikey); SINGLE-OBSERVED(lcsc) |
| B005 | C207 | 1 piece | 3 | 2 | 5 piece | CGA3E2C0G1H220J080AA | TDK | No supply flag in retrieved evidence |
| B006 | C209, C210, C211, C212, C213, C214, C404 | 7 piece | 21 | 3 | 24 piece | C5750X7R1H226M250KB | TDK | OOS(lcsc); OOS(digikey); SINGLE-OBSERVED(mouser) |
| B007 | C302, C353, C366, C379 | 4 piece | 12 | 2 | 14 piece | GRM21BR71E475KA73L | Murata Electronics | NRND/EOL(mouser); NRND/EOL(digikey); SINGLE-OBSERVED(lcsc) |
| B008 | C307, C403 | 2 piece | 6 | 2 | 8 piece | GRM21BR71H105KA12L | Murata Electronics | NRND/EOL(mouser); NRND/EOL(digikey); SINGLE-OBSERVED(lcsc) |
| B009 | C330, C331, C332, C333, C334, C335, C336, C337, C340, C341, C342, C343 | 12 piece | 36 | 4 | 40 piece | PCH1V471MCL1GS | Nichicon | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| B010 | C350, C603 | 2 piece | 6 | 2 | 8 piece | C1608C0G1H103J080AA | TDK | OOS(mouser); SINGLE-OBSERVED(digikey) |
| B011 | C351 | 1 piece | 3 | 2 | 5 piece | C3216X7R1H475K160AB | TDK | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE; EXACT-ORDER-CODE-UNCONFIRMED |
| B012 | C356 | 1 piece | 3 | 2 | 5 piece | C1608C0G1H102J080AA | TDK | OOS(mouser); SINGLE-OBSERVED(digikey) |
| B013 | C357 | 1 piece | 3 | 2 | 5 piece | GRM1885C1H330JA01D | Murata Electronics | NRND/EOL(mouser); NRND/EOL(digikey) |
| B014 | C358, C359 | 2 piece | 6 | 2 | 8 piece | EEU-FR1E221 | Panasonic | OOS(mouser); OOS(digikey); NO-CONFIRMED-STOCK |
| B015 | D101 | 1 piece | 3 | 1 | 4 piece | SMCJ36CA | Littelfuse | OOS(digikey); NO-CONFIRMED-STOCK |
| B016 | D102, D330, D331 | 3 piece | 9 | 1 | 10 piece | STPS60H100CT | STMicroelectronics | No supply flag in retrieved evidence |
| B017 | D301, D302, D322, D618, D619, D640, D641, D642, D643 | 9 piece | 27 | 3 | 30 piece | BAS116,215 | Nexperia | OOS(mouser); OOS(digikey); SINGLE-OBSERVED(lcsc) |
| B018 | D303 | 1 piece | 3 | 1 | 4 piece | BAT46W-E3-08 | Vishay | OOS(mouser); SHORTFALL(digikey) |
| B019 | D304, D600, D660 | 3 piece | 9 | 1 | 10 piece | B260-13-F | Diodes Incorporated | No supply flag in retrieved evidence |
| B020 | D321, D601 | 2 piece | 6 | 1 | 7 piece | LM4040A25IDBZR | Texas Instruments | No supply flag in retrieved evidence |
| B021 | F101 | 1 piece | 3 | 2 | 5 piece | 3403.0285.23 | SCHURTER | SHORTFALL(mouser) |
| B022 | J301, J302, J603, J604, J605, J606, JP600, JP660 | 8 piece | 24 | 3 | 27 piece | B2B-XH-A(LF)(SN) | JST | No supply flag in retrieved evidence |
| B023 | J501 | 1 piece | 3 | 1 | 4 piece | B2P-VH-FB-B(LF)(SN) | JST | No supply flag in retrieved evidence |
| B024 | J502 | 1 piece | 3 | 1 | 4 piece | 1776508 | Phoenix Contact | OOS(lcsc) |
| B025 | J503 | 1 piece | 3 | 1 | 4 piece | B4B-XH-A(LF)(SN) | JST | No supply flag in retrieved evidence |
| B026 | JP101, JP201, JP202, JP301, JP330, JP331, JP501 | 7 piece | 21 | 3 | 24 piece | CUSTOM-FX-CU-01 RevA | Project-defined | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| B027 | L201 | 1 piece | 3 | 2 | 5 piece | 74437636351002 | Würth Elektronik | OOS(mouser); SINGLE-OBSERVED(digikey) |
| B028 | L301 | 1 piece | 3 | 2 | 5 piece | 7447789004 | Würth Elektronik | OOS(mouser); SINGLE-OBSERVED(digikey) |
| B029 | PF1, PF2, PF3, PF4, PF5 | 5 PCB feature | 15 | 0 | 0 piece | CUSTOM-FX-PAD-M4 RevA | Project-defined | NOT PURCHASED |
| B030 | Q101 | 1 piece | 3 | 1 | 4 piece | CSD19537Q3 | Texas Instruments | SHORTFALL(mouser) |
| B031 | Q102 | 1 piece | 3 | 1 | 4 piece | BSS138 | onsemi | No supply flag in retrieved evidence |
| B032 | Q301, Q302 | 2 piece | 6 | 1 | 7 piece | BSC034N06NSATMA1 | Infineon Technologies | No supply flag in retrieved evidence |
| B033 | Q303, Q330 | 2 piece | 6 | 1 | 7 piece | CSD18540Q5B | Texas Instruments | OOS(lcsc); OOS(mouser); OOS(digikey); NO-CONFIRMED-STOCK |
| B034 | Q304 | 1 piece | 3 | 1 | 4 piece | 2N7002,215 | Nexperia | OOS(mouser); OOS(digikey); SINGLE-OBSERVED(lcsc) |
| B035 | Q316 | 1 piece | 3 | 1 | 4 piece | FDB33N25TM | onsemi | No supply flag in retrieved evidence |
| B036 | R101 | 1 piece | 3 | 2 | 5 piece | TNPW0603332KBEEA | Vishay | OOS(digikey); SINGLE-OBSERVED(mouser) |
| B037 | R102 | 1 piece | 3 | 2 | 5 piece | TNPW060354K9BEEA | Vishay | OOS(lcsc) |
| B038 | R103 | 1 piece | 3 | 2 | 5 piece | TNPW0805348KBEEA | Vishay | OOS(lcsc); NO-CONFIRMED-STOCK |
| B039 | R104 | 1 piece | 3 | 2 | 5 piece | TNPW060315K8BEEA | Vishay | No supply flag in retrieved evidence |
| B040 | R105 | 1 piece | 3 | 2 | 5 piece | TNPW06034K02BEEA | Vishay | SHORTFALL(lcsc) |
| B041 | R106 | 1 piece | 3 | 2 | 5 piece | TNPW060356K2BEEA | Vishay | No supply flag in retrieved evidence |
| B042 | R107, R302, R307, R313, R316, R317, R363, R365, R370, R371, R372, R385, R404, R405, R408, R601, R603, R604, R645, R648, R707, R708, R710, R713, R723, R727, R728, R729 | 28 piece | 84 | 9 | 93 piece | TNPW060310K0BEEA | Vishay | No supply flag in retrieved evidence |
| B043 | R108, R202, R206, R321, R322, R330, R346, R364, R367, R605, R606, R609, R623, R650, R651, R652, R718 | 17 piece | 51 | 6 | 57 piece | TNPW0603100KBEEA | Vishay | No supply flag in retrieved evidence |
| B044 | R201, R379 | 2 piece | 6 | 2 | 8 piece | TNPW060333K2BEEA | Vishay | No supply flag in retrieved evidence |
| B045 | R203 | 1 piece | 3 | 2 | 5 piece | TNPW060324K4BEEA | Vishay | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE; EXACT-ORDER-CODE-UNCONFIRMED |
| B046 | R204 | 1 piece | 3 | 2 | 5 piece | CRCW06030000Z0EA | Vishay | No supply flag in retrieved evidence |
| B047 | R205, R303, R373, R622, R647, R649, R709, R712, R717, R730, R731 | 11 piece | 33 | 4 | 37 piece | TNPW06031K00BEEA | Vishay | No supply flag in retrieved evidence |
| B048 | R207 | 1 piece | 3 | 2 | 5 piece | TNPW060324K9BEEA | Vishay | No supply flag in retrieved evidence |
| B049 | R301 | 1 piece | 3 | 2 | 5 piece | TNPW06039K88BEEA | Vishay | SINGLE-OBSERVED(digikey) |
| B050 | R304 | 1 piece | 3 | 2 | 5 piece | TNPW0603100RBEEA | Vishay | No supply flag in retrieved evidence |
| B051 | R305 | 1 piece | 3 | 2 | 5 piece | TNPW12062M00BEEA | Vishay | No supply flag in retrieved evidence |
| B052 | R306, R384 | 2 piece | 6 | 2 | 8 piece | CRCW06031R00FKEA | Vishay | No supply flag in retrieved evidence |
| B053 | R308, R309, R310, R311, R380, R381, R382, R383, R386, R387, R388, R389, R390, R391, R392, R393 | 16 piece | 48 | 5 | 53 piece | WFMB2512R0330FEA | Vishay | OOS(lcsc); OOS(mouser); OOS(digikey); NO-CONFIRMED-STOCK |
| B054 | R312, R600 | 2 piece | 6 | 2 | 8 piece | TNPW060332K4BEEA | Vishay | SINGLE-OBSERVED(digikey) |
| B055 | R323 | 1 piece | 3 | 2 | 5 piece | CRCW120610K0FKEA | Vishay | No supply flag in retrieved evidence |
| B056 | R331 | 1 piece | 3 | 2 | 5 piece | TNPW06034K32BEEA | Vishay | No supply flag in retrieved evidence |
| B057 | R332 | 1 piece | 3 | 2 | 5 piece | WSL2512R3300FEA | Vishay | No supply flag in retrieved evidence |
| B058 | R333 | 1 piece | 3 | 2 | 5 piece | CRCW060310R0FKEA | Vishay | No supply flag in retrieved evidence |
| B059 | R340 | 1 piece | 3 | 2 | 5 piece | TNPW08051M00BEEA | Vishay | No supply flag in retrieved evidence |
| B060 | R341 | 1 piece | 3 | 2 | 5 piece | TNPW060388K7BEEA | Vishay | OOS(lcsc); SINGLE-OBSERVED(digikey) |
| B061 | R342 | 1 piece | 3 | 2 | 5 piece | TNPW060323K7BEEA | Vishay | No supply flag in retrieved evidence |
| B062 | R343, R344 | 2 piece | 6 | 2 | 8 piece | TNPW060315K0BEEA | Vishay | No supply flag in retrieved evidence |
| B063 | R345 | 1 piece | 3 | 2 | 5 piece | TNPW0805383KBEEA | Vishay | SHORTFALL(mouser) |
| B064 | R361 | 1 piece | 3 | 2 | 5 piece | TNPW060368K1BEEA | Vishay | No supply flag in retrieved evidence |
| B065 | R362 | 1 piece | 3 | 2 | 5 piece | TNPW0603249KBEEA | Vishay | No supply flag in retrieved evidence |
| B066 | R374 | 1 piece | 3 | 2 | 5 piece | CRCW0603100RFKEA | Vishay | No supply flag in retrieved evidence |
| B067 | R375 | 1 piece | 3 | 2 | 5 piece | TNPW06036K49BEEA | Vishay | OOS(mouser); SINGLE-OBSERVED(digikey) |
| B068 | R376, R378 | 2 piece | 6 | 2 | 8 piece | TNPW0805365KBEEA | Vishay | OOS(mouser); NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| B069 | R377 | 1 piece | 3 | 2 | 5 piece | TNPW060348K7BEEA | Vishay | SHORTFALL(digikey) |
| B070 | R401 | 1 piece | 3 | 2 | 5 piece | WSL27262L000FEA | Vishay | No supply flag in retrieved evidence |
| B071 | R402, R403 | 2 piece | 6 | 2 | 8 piece | TNPW060310R0BEEA | Vishay | No supply flag in retrieved evidence |
| B072 | R406, R407 | 2 piece | 6 | 2 | 8 piece | TNPW06034K70BEEA | Vishay | No supply flag in retrieved evidence |
| B073 | R602 | 1 piece | 3 | 2 | 5 piece | TNPW060347R0BEEA | Vishay | No supply flag in retrieved evidence |
| B074 | R640, R642 | 2 piece | 6 | 2 | 8 piece | TNPW060320K0BEEA | Vishay | No supply flag in retrieved evidence |
| B075 | R641 | 1 piece | 3 | 2 | 5 piece | TNPW06036K19BEEA | Vishay | No supply flag in retrieved evidence |
| B076 | R644 | 1 piece | 3 | 2 | 5 piece | TNPW060349K9BEEA | Vishay | No supply flag in retrieved evidence |
| B077 | R711 | 1 piece | 3 | 2 | 5 piece | TNPW0603143KBEEA | Vishay | SHORTFALL(mouser) |
| B078 | TP101, TP102, TP301, TP302, TP303, TP304, TP305, TP401, TP402, TP403, TP404, TP501, TP502, TP503, TP504 | 15 PCB feature | 45 | 0 | 0 piece | N/A etched copper | Project-defined | NOT PURCHASED |
| B079 | TP103, TP201, TP202, TP203, TP204, TP306, TP307, TP308, TP309, TP310, TP311, TP312, TP313, TP314, TP315, TP316, TP317, TP318, TP319, TP320, TP321, TP322, TP323, TP324, TP327, TP328, TP329, TP330, TP331, TP332, TP333, TP334, TP335, TP336, TP337, TP338, TP339, TP340, TP405, TP406, TP505 | 41 PCB feature | 123 | 0 | 0 piece | N/A etched copper | Project-defined | NOT PURCHASED |
| B080 | U101 | 1 piece | 3 | 1 | 4 piece | TPS26630RGER | Texas Instruments | OOS(lcsc); OOS(digikey); NO-CONFIRMED-STOCK |
| B081 | U201 | 1 piece | 3 | 1 | 4 piece | LM61460AANRJRR | Texas Instruments | No supply flag in retrieved evidence |
| B082 | U301 | 1 piece | 3 | 1 | 4 piece | LTC7001IMSE#PBF | Analog Devices | OOS(digikey) |
| B083 | U302 | 1 piece | 3 | 1 | 4 piece | REF5025IDGKR | Texas Instruments | No supply flag in retrieved evidence |
| B084 | U303, U607, U640, U642 | 4 piece | 12 | 2 | 14 piece | TLV3201AIDBVR | Texas Instruments | OOS(mouser); OOS(digikey); SINGLE-OBSERVED(lcsc) |
| B085 | U306, U600 | 2 piece | 6 | 1 | 7 piece | TPS7A1601DGNR | Texas Instruments | OOS(lcsc); OOS(digikey); NO-CONFIRMED-STOCK |
| B086 | U315, U330 | 2 piece | 6 | 1 | 7 piece | UCC27511DBVR | Texas Instruments | No supply flag in retrieved evidence |
| B087 | U316 | 1 piece | 3 | 1 | 4 piece | LT4363HMS-1#PBF | Analog Devices | No supply flag in retrieved evidence |
| B088 | U317 | 1 piece | 3 | 1 | 4 piece | LTC3115IFE-1#PBF | Analog Devices | SHORTFALL(lcsc) |
| B089 | U318, U402 | 2 piece | 6 | 1 | 7 piece | TPS70933DBVR | Texas Instruments | OOS(digikey); SINGLE-OBSERVED(lcsc) |
| B090 | U321, U647, U651 | 3 piece | 9 | 1 | 10 piece | ADG4612BRUZ | Analog Devices | OOS(lcsc); CHANNEL-RESTRICTION(mouser) |
| B091 | U322, U323 | 2 piece | 6 | 1 | 7 piece | TPS3808G01DBVR | Texas Instruments | No supply flag in retrieved evidence |
| B092 | U327 | 1 piece | 3 | 1 | 4 piece | TPS259470LRPWR | Texas Instruments | No supply flag in retrieved evidence |
| B093 | U401 | 1 piece | 3 | 1 | 4 piece | INA228AIDGSR | Texas Instruments | OOS(lcsc); OOS(digikey); NO-CONFIRMED-STOCK |
| B094 | U403 | 1 piece | 3 | 1 | 4 piece | TCA9517DGKR | Texas Instruments | No supply flag in retrieved evidence |
| B095 | U602 | 1 piece | 3 | 1 | 4 piece | TPS3808G50DBVR | Texas Instruments | OOS(mouser); OOS(digikey); SINGLE-OBSERVED(lcsc) |
| B096 | U610, U611, U612 | 3 piece | 9 | 1 | 10 piece | SN74LVC1G74DCTR | Texas Instruments | OOS(digikey) |
| B097 | U614, U616, U644, U654, U656, U661 | 6 piece | 18 | 2 | 20 piece | SN74LVC1G14DBVR | Texas Instruments | No supply flag in retrieved evidence |
| B098 | U615 | 1 piece | 3 | 1 | 4 piece | SN74LVC1G32DBVR | Texas Instruments | OOS(digikey); SINGLE-OBSERVED(lcsc) |
| B099 | U617, U623, U628, U630, U631, U632, U633 | 7 piece | 21 | 3 | 24 piece | SN74LVC1G08DBVR | Texas Instruments | No supply flag in retrieved evidence |
| B100 | U662 | 1 piece | 3 | 1 | 4 piece | SN74LVC1G17DBVR | Texas Instruments | No supply flag in retrieved evidence |
| H01 | J502 mating plug | 1 piece | 3 | 1 | 4 piece | 1777989 | Phoenix Contact | OOS(digikey); SINGLE-OBSERVED(mouser) |
| H05 | HARNESS full Pi 2x20 socket housing | 1 piece | 3 | 1 | 4 piece | 3-87456-6 | TE Connectivity | OOS(digikey); NO-CONFIRMED-STOCK |
| H06 | HARNESS ten populated power/ground contacts | 10 piece | 30 | 3 | 33 piece | 87309-9 | TE Connectivity | No supply flag in retrieved evidence |
| H07 | HARNESS positive AWG16 trunk | 0.075 metre | 0.225 | 1 | 1 100 ft spool (30.48 m) | 8521 002100 | Belden | No supply flag in retrieved evidence |
| H08 | HARNESS return AWG16 trunk | 0.075 metre | 0.225 | 1 | 1 100 ft spool (30.48 m) | 8521 010100 | Belden | OOS(digikey); SINGLE-OBSERVED(mouser) |
| H09 | HARNESS positive AWG20 branches | 0.030 metre | 0.090 | 1 | 1 100 ft spool (30.48 m) | 8502 002100 | Belden | SINGLE-OBSERVED(mouser) |
| H10 | HARNESS return AWG20 branches | 0.280 metre | 0.840 | 1 | 1 100 ft spool (30.48 m) | 8502 010100 | Belden | No supply flag in retrieved evidence |
| M01 | M4 bolts for seven links | 14 piece | 42 | 6 | 48 piece | OPEN | OPEN | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| M02 | M4 washers for seven links | 28 piece | 84 | 12 | 96 piece | OPEN | OPEN | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| M03 | M4 nuts for seven links | 14 piece | 42 | 6 | 48 piece | OPEN | OPEN | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| O01 | Input / control / I2C mating harnesses | OPEN piece | OPEN | OPEN | OPEN piece | OPEN | OPEN | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |
| O02 | Thermal / assembly accessories | OPEN piece | OPEN | OPEN | OPEN piece | OPEN | OPEN | NO-CONFIRMED-STOCK; NO-VERIFIED-PRICE |

## lcsc commercial register

All prices below are USD per stated order unit. Lead time is the published manufacturer/factory lead time if retrieved, not an arrival promise. Dates/crawl ages, currency limitations and MOQ assumptions are in the CSV.

| ID | Distributor SKU / evidence | Order qty | Unit USD | Extended USD | Stock | Lead time | Lifecycle |
|---|---|---:|---:|---:|---|---|---|
| B001 | OPEN | 11 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B002 | [C77055](https://www.lcsc.com/product-detail/C77055.html) | 150 | 0.0171 | 2.5650 | 1177900 | OPEN | OPEN |
| B003 | [C77102](https://www.lcsc.com/product-detail/C77102.html) | 30 | 0.3322 | 9.9660 | 41315 | OPEN | OPEN |
| B004 | [C77080](https://www.lcsc.com/product-detail/C77080.html?is_substitute=1&lcsc_vid=RFAKAVdeTlMPX1IAR1ReXwBeQ1ZcXgcAFVYPXgYCElgxVlNeQFJbUVxWR1RYXztW&original_product_code=C2168801&original_unit_price=0.0957) | 30 | 0.0586 | 1.7580 | 17770 | OPEN | OPEN |
| B005 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B006 | [C3901066](https://www.lcsc.com/product-detail/C3901066.html) | 24 | 4.123 | 98.952 | 0 | OPEN | OPEN |
| B007 | [C162427](https://www.lcsc.com/product-detail/C162427.html) | 15 | 0.1365 | 2.0475 | 10385 | OPEN | OPEN |
| B008 | [C77083](https://www.lcsc.com/product-detail/C77083.html) | 10 | 0.0425 | 0.4250 | 119480 | OPEN | OPEN |
| B009 | OPEN | 40 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B010 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B011 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B012 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B013 | [C77035](https://www.lcsc.com/product-detail/C77035.html) | 50 | 0.0165 | 0.8250 | 77750 | OPEN | OPEN |
| B014 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B015 | [OPEN](https://www.lcsc.com/product-detail/C7495268.html) | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B016 | [C2688542](https://www.lcsc.com/product-detail/Schottky-Diodes_STMicroelectronics-STPS60H100CT_C2688542.html) | 10 | 2.028 | 20.280 | 10 | OPEN | OPEN |
| B017 | [C48502](https://www.lcsc.com/product-detail/C48502.html) | 40 | 0.0219 | 0.8760 | 65200 | OPEN | OPEN |
| B018 | [C14099](https://www.lcsc.com/product-detail/C14099.html) | 5 | 0.1671 | 0.8355 | 4435 | OPEN | OPEN |
| B019 | [C72265](https://www.lcsc.com/product-detail/C72265.html) | 10 | 0.1286 | 1.2860 | 84335 | OPEN | OPEN |
| B020 | [C9421](https://www.lcsc.com/product-detail/Voltage-References_Texas-Instruments_C9421.html) | 7 | 1.9928 | 13.9496 | 4737 | OPEN | OPEN |
| B021 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B022 | [C158012](https://www.lcsc.com/product-detail/C158012.html) | 40 | 0.0409 | 1.6360 | 288240 | OPEN | OPEN |
| B023 | [C158006](https://www.lcsc.com/product-detail/VH-Connectors_JST_B2P-VH-FB-B-LF-SN_VHsocket-1-2P-pitch3-96mm_C158006.html) | 5 | 0.1607 | 0.8035 | 35200 | OPEN | OPEN |
| B024 | [C480526](https://www.lcsc.com/es/product-detail/Pluggable-System-Terminal-Block_Phoenix-Contact-1776508_C480526.html) | 4 | 0.7316 | 2.9264 | 0 | OPEN | OPEN |
| B025 | [C144395](https://www.lcsc.com/product-detail/C144395.html) | 10 | 0.0622 | 0.6220 | 82000 | OPEN | OPEN |
| B026 | OPEN | 24 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B027 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B028 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B029 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B030 | [C478469](https://www.lcsc.com/product-detail/C478469.html) | 4 | 0.8449 | 3.3796 | 3779 | OPEN | OPEN |
| B031 | [C52895](https://www.lcsc.com/es/product-detail/MOSFET_FAIRCHILD_BSS138_BSS138_C52895.html) | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B032 | [C55106953](https://www.lcsc.com/product-detail/C55106953.html) | 7 | 1.0754 | 7.5278 | 998 | OPEN | OPEN |
| B033 | [C86513](https://www.lcsc.com/product-detail/C86513.html) | 7 | 2.3114 | 16.1798 | 0 | OPEN | OPEN |
| B034 | [C65189](https://www.lcsc.com/product-detail/C65189.html) | 20 | 0.0183 | 0.3660 | 275600 | OPEN | OPEN |
| B035 | [C241752](https://www.lcsc.com/product-detail/C241752.html) | 4 | 1.6089 | 6.4356 | 1365 | OPEN | OPEN |
| B036 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B037 | [C2079049](https://www.lcsc.com/product-detail/C2079049.html) | 5 | 0.0986 | 0.4930 | 0 | OPEN | OPEN |
| B038 | [C1709278](https://www.lcsc.com/ko/product-detail/C1709278.html) | 5 | 0.1555 | 0.7775 | 0 | OPEN | OPEN |
| B039 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B040 | [C844459](https://www.lcsc.com/product-detail/C844459.html?is_substitute=1&original_product_code=C4084206&original_unit_price=0.2583) | 5 | 0.5228 | 2.6140 | 4 | OPEN | OPEN |
| B041 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B042 | [C844890](https://www.lcsc.com/es/product-detail/chip-resistor-surface-mount_vishay-intertech-tnpw060310k0beea_C844890.html) | 100 | 0.0562 | 5.6200 | 59580 | OPEN | OPEN |
| B043 | [C844888](https://www.lcsc.com/product-detail/C844888.html) | 60 | 0.0632 | 3.7920 | 41105 | OPEN | OPEN |
| B044 | [C2075328](https://www.lcsc.com/product-detail/C2075328.html) | 10 | 0.1001 | 1.0010 | 4700 | OPEN | OPEN |
| B045 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B046 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B047 | [C844891](https://www.lcsc.com/fr/product-detail/C844891.html?is_substitute=1&lcsc_vid=FQAKVwECEQQKXlUHQgVXVFdXR1IIBABUFgMKBgIDElkxVlNeQVVdUVNfQVlXVjtW&original_product_code=C2093795&original_unit_price=0.2710) | 40 | OPEN | OPEN | 14380 | OPEN | OPEN |
| B048 | [C3009044](https://www.lcsc.com/product-detail/C3009044.html?is_substitute=1&lcsc_vid=FQAKVwECEQQKXlUHQgVXVFdXR1IIBABUFgMKBgIDElkxVlNeQVRZV1FWRlZYXjtW&original_product_code=C4261892&original_unit_price=0.4429) | 5 | 0.0833 | 0.4165 | 2935 | OPEN | OPEN |
| B049 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B050 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B051 | [C1854583](https://www.lcsc.com/es/product-detail/C1854583.html) | 5 | 0.1661 | 0.8305 | 28335 | OPEN | OPEN |
| B052 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B053 | [C2090631](https://www.lcsc.com/product-detail/C2090631.html) | 53 | 0.6325 | 33.5225 | 0 | OPEN | OPEN |
| B054 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B055 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B056 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B057 | [C2073866](https://www.lcsc.com/product-detail/C2073866.html) | 5 | 0.328 | 1.640 | 1165 | OPEN | OPEN |
| B058 | [C844919](https://www.lcsc.com/product-detail/C844919.html) | 10 | 0.0046 | 0.0460 | 313700 | OPEN | OPEN |
| B059 | [C844679](https://www.lcsc.com/es/product-detail/chip-resistor-surface-mount_vishay-tnpw08051m00beea_C844679.html) | 5 | 0.252 | 1.260 | 14730 | OPEN | OPEN |
| B060 | [C2088700](https://www.lcsc.com/product-detail/C2088700.html) | 5 | OPEN | OPEN | 0 | OPEN | OPEN |
| B061 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B062 | [C844454](https://www.lcsc.com/de/product-detail/C844454.html?is_substitute=1&original_product_code=C1693814&original_unit_price=0.0964) | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B063 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B064 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B065 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B066 | [C844917](https://www.lcsc.com/product-detail/C844917.html) | 100 | 0.0044 | 0.4400 | 253600 | OPEN | OPEN |
| B067 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B068 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B069 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B070 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B071 | [OPEN](https://www.lcsc.com/es/product-detail/C844675.html?is_substitute=1&lcsc_vid=EVlZVV1eFgdfAlECTwINXgJWRFZbVgdXQFlaU1FUFgQxVlNeT1FbVFFXQVFZUTtW&original_product_code=C2076354&original_unit_price=0.2727) | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B072 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B073 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B074 | [C844676](https://www.lcsc.com/it/product-detail/C844676.html) | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B075 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B076 | [C844267](https://www.lcsc.com/de/product-detail/C844267.html?is_substitute=1&original_product_code=C705780&original_unit_price=0.0384) | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B077 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B078 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B079 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B080 | [C1850276](https://www.lcsc.com/product-detail/Surge-Suppressors_Texas-Instruments-TPS26630RGER_C1850276.html) | 4 | 9.0636 | 36.2544 | 0 | OPEN | OPEN |
| B081 | [C2864505](https://www.lcsc.com/product-detail/C2864505.html?is_substitute=1&original_product_code=C2876600&original_unit_price=2.3091) | 4 | 1.8929 | 7.5716 | 1289 | OPEN | OPEN |
| B082 | [C581062](https://www.lcsc.com/product-detail/C581062.html) | 4 | 9.7168 | 38.8672 | 45 | OPEN | OPEN |
| B083 | OPEN | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B084 | [C105188](https://www.lcsc.com/product-detail/C105188.html) | 14 | 0.8638 | 12.0932 | 37123 | OPEN | OPEN |
| B085 | [C55770](https://www.lcsc.com/product-detail/C55770.html) | 7 | 0.8102 | 5.6714 | 0 | OPEN | OPEN |
| B086 | [C191027](https://www.lcsc.com/product-detail/C191027.html?lcsc_vid=RlIKUgVfEwcPUVNQQFYIBVdVQFJaAlwCFFQMBlVeR1cxVlNRT1hZUVRWR1daVjtW) | 7 | 0.611 | 4.277 | 6891 | OPEN | OPEN |
| B087 | [C580193](https://www.lcsc.com/product-detail/C580193.html) | 4 | 17.0545 | 68.2180 | 8 | OPEN | OPEN |
| B088 | [C580691](https://www.lcsc.com/product-detail/dc-dc-converters_adi-ltc3115ife-1-pbf_C580691.html) | 4 | 12.2387 | 48.9548 | 3 | OPEN | OPEN |
| B089 | [C89347](https://www.lcsc.com/product-detail/C89347.html) | 10 | 0.3379 | 3.3790 | 21460 | OPEN | OPEN |
| B090 | [C657391](https://www.lcsc.com/product-detail/C657391.html) | 10 | 6.8968 | 68.9680 | 0 | OPEN | OPEN |
| B091 | [C19653](https://www.lcsc.com/product-detail/C19653.html?s_z=n_tps709) | 10 | 0.4142 | 4.1420 | 1885 | OPEN | OPEN |
| B092 | [C3662793](https://www.lcsc.com/product-detail/C3662793.html) | 4 | 1.4568 | 5.8272 | 2681 | OPEN | OPEN |
| B093 | [C2887910](https://www.lcsc.com/product-detail/Current-Sensing-Amplifiers_Texas-Instruments-INA228AIDGSR_C2887910.html) | 4 | 6.3843 | 25.5372 | 0 | OPEN | OPEN |
| B094 | [C544515](https://www.lcsc.com/product-detail/C544515.html) | 4 | 0.9568 | 3.8272 | 877 | OPEN | OPEN |
| B095 | [C134123](https://www.lcsc.com/product-detail/C134123.html) | 4 | 1.1127 | 4.4508 | 576 | OPEN | OPEN |
| B096 | [C840104](https://www.lcsc.com/product-detail/C840104.html) | 10 | 0.6717 | 6.7170 | 1568 | OPEN | OPEN |
| B097 | [C7835](https://www.lcsc.com/product-detail/C7835.html) | 20 | 0.0655 | 1.3100 | 311540 | OPEN | OPEN |
| B098 | [C10096](https://www.lcsc.com/product-detail/C10096.html) | 10 | 0.0714 | 0.7140 | 111770 | OPEN | OPEN |
| B099 | [C7666](https://www.lcsc.com/product-detail/C7666.html) | 30 | 0.047 | 1.410 | 124900 | OPEN | OPEN |
| B100 | [C7836](https://lcsc.com/product-detail/Buffers-Drivers_Texas-Instruments_C7836.html) | 5 | 0.1696 | 0.8480 | 40370 | OPEN | OPEN |
| H01 | [C480522](https://www.lcsc.com/es/product-detail/C480522.html) | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H05 | OPEN | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H06 | OPEN | 33 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H07 | OPEN | 1 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H08 | OPEN | 1 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H09 | OPEN | 1 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H10 | OPEN | 1 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M01 | OPEN | 48 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M02 | OPEN | 96 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M03 | OPEN | 48 | OPEN | OPEN | OPEN | OPEN | OPEN |
| O01 | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| O02 | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |

## mouser commercial register

All prices below are USD per stated order unit. Lead time is the published manufacturer/factory lead time if retrieved, not an arrival promise. Dates/crawl ages, currency limitations and MOQ assumptions are in the CSV.

| ID | Distributor SKU / evidence | Order qty | Unit USD | Extended USD | Stock | Lead time | Lifecycle |
|---|---|---:|---:|---:|---|---|---|
| B001 | [81-GRM32ER72A105KA01](https://www.mouser.com/en/ProductDetail/Murata-Electronics/GRM32ER72A105KA01L?qs=IjyrXs0Hof%252B1DBjYdhBu6w%3D%3D) | 11 | 0.602 | 6.622 | 4755 | 12 Weeks | End of Life: |
| B002 | [81-GRM39X104K50D](https://gr.mouser.com/en/ProductDetail/Murata-Electronics/GRM188R71H104KA93D?qs=f7ZljCwbPOm85Y6l%2FNGt7A%3D%3D) | 142 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B003 | [OPEN](https://gr.mouser.com/ProductDetail/Murata-Electronics/GRM32ER71H106KA12L?qs=6pxx44s1bjkjdm74o%2FrKhg%3D%3D) | 30 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B004 | [81-GRM21BR71E105KA99](https://www.mouser.com/en/ProductDetail/Murata-Electronics/GRM21BR71E105KA99L?qs=pAhIg4h%2FqUTk69tB5q7hhg%3D%3D) | 27 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B005 | [810-CGA3E2C0G1H220J](https://www.mouser.com/en/ProductDetail/TDK/CGA3E2C0G1H220J080AA?qs=FxQuwy19cyDYFYuuIEBNFA%3D%3D) | 5 | 0.15 | 0.75 | 49442 | 24 Weeks | OPEN |
| B006 | [810-C5750X7R1H226M25](https://www.mouser.com/ProductDetail/TDK/C5750X7R1H226M250KB?qs=P1JMDcb91o59nz9c5XhFzA%3D%3D) | 24 | 3.40 | 81.60 | 45172 | 12 Weeks | OPEN |
| B007 | [81-GRM21BR71E475KA3L](https://www.mouser.com/ProductDetail/Murata-Electronics/GRM21BR71E475KA73L?qs=Od3eZLdO5mERWmTe7n2nHA%3D%3D) | 14 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B008 | [81-GRM21BR71H105KA2L](https://my.mouser.com/en/ProductDetail/Murata-Electronics/GRM21BR71H105KA12L?qs=Er06SXQpt%252B60EIT%2FJ7%2F41Q%3D%3D) | 8 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B009 | OPEN | 40 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B010 | [810-C1608C0G1H103J](https://www.mouser.com/en/ProductDetail/TDK/C1608C0G1H103J080AA?qs=NRhsANhppD%2FAN3pEk1wMuQ%3D%3D) | 8 | 0.24 | 1.92 | 0 | 24 Weeks | OPEN |
| B011 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B012 | [810-C1608C0G1H102J](https://www.mouser.com/en/ProductDetail/TDK/C1608C0G1H102J080AA?qs=NRhsANhppD8t9qBk5zN%252Bsw%3D%3D) | 5 | 0.15 | 0.75 | 0 | 24 Weeks | OPEN |
| B013 | [81-GRM39C330J50](https://www.mouser.com/ProductDetail/Murata-Electronics/GRM1885C1H330JA01D?qs=E%252B5dfF6xfG3shwmI3hm0tg%3D%3D) | 5 | OPEN | OPEN | OPEN | 10 Weeks | NRND: |
| B014 | [667-EEU-FR1E221](https://www.mouser.com/en/ProductDetail/Panasonic-Industry/EEU-FR1E221?qs=tfZGHB2PWd1Rv9iToDM7xw%3D%3D) | 8 | 0.71 | 5.68 | 0 | 37 Weeks | OPEN |
| B015 | [576-SMCJ36CA](https://www.mouser.com/en/ProductDetail/Littelfuse/SMCJ36CA?qs=zHiv0nsVGmqDVrcTX3XJRw%3D%3D) | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B016 | [511-STPS60H100CT](https://www.mouser.com/en/ProductDetail/STMicroelectronics/STPS60H100CT?qs=kndcJBrKlnQCElnVE4U9wA%3D%3D) | 10 | 1.79 | 17.90 | 474 | 15 Weeks | OPEN |
| B017 | [771-BAS116-T/R](https://www.mouser.com/ProductDetail/Nexperia/BAS116215?qs=me8TqzrmIYUhk4ykXYPaNg%3D%3D) | 30 | 0.151 | 4.530 | 0 | 53 Weeks | OPEN |
| B018 | [78-BAT46W-E3-08](https://www.mouser.com/en/ProductDetail/Vishay-Semiconductors/BAT46W-E3-08?qs=KP8Io%2FXyE5QAjvoG5XlHWA%3D%3D) | 4 | OPEN | OPEN | 0 | 29 Weeks | OPEN |
| B019 | [621-B260-F](https://www.mouser.com/en/ProductDetail/Diodes-Incorporated/B260-13-F?qs=eVtA5waOtifTWH0TOzQQ1A%3D%3D) | 10 | 0.244 | 2.440 | OPEN | OPEN | OPEN |
| B020 | OPEN | 7 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B021 | [693-3403.0285.23](https://uy.mouser.com/es/ProductDetail/Schurter/3403.0285.23?qs=sGAEpiMZZMsZt0HrY5I79gvvspmojkSvBgiu4pDZC1A%3D) | 5 | OPEN | OPEN | 3 | OPEN | OPEN |
| B022 | [306-B2BXHALFSNP](https://www.mouser.com/en/ProductDetail/JST-Commercial/B2B-XH-ALFSN?qs=cdbOS8ANM9DdcSn9qRmfCw%3D%3D) | 27 | 0.087 | 2.349 | 4010 | 26 Weeks | OPEN |
| B023 | OPEN | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B024 | [651-1776508](https://my.mouser.com/ProductDetail/Phoenix-Contact/1776508?qs=8M15sSGRUn%252B2z3E1%2FgeKhw%3D%3D) | 4 | OPEN | OPEN | 1177 | OPEN | OPEN |
| B025 | [306-B4BXHALFSN](https://www.mouser.com/ProductDetail/JST-Commercial/B4B-XH-ALFSN?qs=cdbOS8ANM9CfC08d%252BywhFw%3D%3D) | 4 | 0.17 | 0.68 | 85057 | 16 Weeks | OPEN |
| B026 | OPEN | 24 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B027 | [710-74437636351002](https://www.mouser.com/ProductDetail/Wurth-Elektronik/74437636351002?qs=2FehpBK1j97R94Iy%2Fo9K7Q%3D%3D) | 5 | 25.98 | 129.90 | 0 | OPEN | New Product: |
| B028 | [710-7447789004](https://www.mouser.com/ProductDetail/Wurth-Elektronik/7447789004?qs=E%2F%2FhvbtCqpM%252BzhhZNuF4OQ%3D%3D) | 5 | 2.51 | 12.55 | 0 | OPEN | OPEN |
| B029 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B030 | [595-CSD19537Q3](https://www.mouser.com/en/ProductDetail/Texas-Instruments/CSD19537Q3?qs=kFLL9AfgRSA2baK1OoK3Jg%3D%3D) | 4 | OPEN | OPEN | 1 | 16 Weeks | OPEN |
| B031 | [512-BSS138](https://www.mouser.com/en/ProductDetail/onsemi/BSS138?qs=HK%252BeIG1iaahCeqBvjB4arg%3D%3D) | 4 | OPEN | OPEN | 578 | 26 Weeks | OPEN |
| B032 | [OPEN](https://www.mouser.com/en/ProductDetail/Infineon-Technologies/BSC034N06NSATMA1?qs=WkdRfq4wf1Mx6O2FQ7xjpw%3D%3D) | 7 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B033 | [595-CSD18540Q5B](https://www.mouser.com/en/ProductDetail/Texas-Instruments/CSD18540Q5B?qs=NRIcxvoDUteMaKTIEMaARQ%3D%3D) | 7 | OPEN | OPEN | 0 | 12 Weeks | OPEN |
| B034 | [771-2N7002-T/R](https://www.mouser.com/ProductDetail/Nexperia/2N7002215?qs=P62ublwmbi9rRKKuNdhqMA%3D%3D) | 4 | 0.23 | 0.92 | 0 | 53 Weeks | OPEN |
| B035 | [512-FDB33N25TM](https://www.mouser.com/en/ProductDetail/onsemi/FDB33N25TM?qs=efMQ9B2bthcq0RaZmjVB%2Fg%3D%3D) | 4 | 3.44 | 13.76 | 21605 | 13 Weeks | OPEN |
| B036 | [71-TNPW0603332KBEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW0603332KBEEA?qs=CxPiq9xx9FKSJfW2xVEvxQ%3D%3D) | 5 | 0.32 | 1.60 | 2709 | 22 Weeks | OPEN |
| B037 | [71-TNPW060354K9BEEA](https://au.mouser.com/en/ProductDetail/Vishay/TNPW060354K9BEEA?qs=sGAEpiMZZMvdGkrng054t%252BPZDYtCzF2JyxpTKQkiwqI%3D) | 5 | OPEN | OPEN | 3128 | 22 Weeks | OPEN |
| B038 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B039 | [71-TNPW060315K8BEEA](https://eu.mouser.com/ProductDetail/Vishay/TNPW060315K8BEEA?qs=UyvxJcuXVAb2EBXqPsn9og%3D%3D) | 5 | OPEN | OPEN | 9 | 12 Weeks | OPEN |
| B040 | [71-TNPW06034K02BEEA](https://www.mouser.com/ProductDetail/Vishay/TNPW06034K02BEEA?qs=hEUCbmUtbxE90GbFNhSfXA%3D%3D) | 5 | 0.26 | 1.30 | 5350 | OPEN | OPEN |
| B041 | [71-TNPW060356K2BEEA](https://www.mouser.com/en/c/passive-components/resistors/film-resistors/?case+code+-+mm=1608&resistance=56.2+kOhms) | 5 | 0.26 | 1.30 | 12191 | OPEN | OPEN |
| B042 | [71-TNPW060310K0BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060310K0BEEA?qs=80vFmtL7BC940KIiWqacAA%3D%3D) | 93 | 0.267 | 24.831 | 141178 | 11 Weeks | OPEN |
| B043 | [71-TNPW0603100KBEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW0603100KBEEA?qs=80vFmtL7BC9RsqlOJE1GSA%3D%3D) | 57 | 0.26 | 14.82 | OPEN | OPEN | OPEN |
| B044 | [71-TNPW060333K2BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060333K2BEEA?qs=kHCK1FE53PmrSCtdbuezTg%3D%3D) | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B045 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B046 | [71-CRCW0603-0-E3](https://eu.mouser.com/en/ProductDetail/Vishay/CRCW06030000Z0EA?qs=uFJqmf%2F3rbbVtxvMdbYUaQ%3D%3D) | 5 | OPEN | OPEN | 2865345 | 18 Weeks | OPEN |
| B047 | [71-TNPW06031K00BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW06031K00BEEA?qs=U8jWr0D8IJhJummGFaCE2g%3D%3D) | 37 | 0.26 | 9.62 | 86488 | 22 Weeks | OPEN |
| B048 | [71-TNPW060324K9BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060324K9BEEA?qs=rhzOH%252BTaZWtEsP8aUWokGA%3D%3D) | 5 | 0.26 | 1.30 | 6951 | 22 Weeks | OPEN |
| B049 | [71-TNPW06039K88BEEA](https://gr.mouser.com/en/ProductDetail/Vishay/TNPW06039K88BEEA?qs=sGAEpiMZZMvdGkrng054twbPyJJnNTBKxZF4yk9Nt%2FU%3D) | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B050 | [71-TNPW0603100RBEEA](https://eu.mouser.com/ProductDetail/Vishay-Dale/TNPW0603100RBEEA?qs=80vFmtL7BC8%252BAhJgjFj4tw%3D%3D) | 5 | OPEN | OPEN | 23 | OPEN | OPEN |
| B051 | [71-TNPW12062M00BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW12062M00BEEA?qs=WEabXX7UcOBK%252BrR3BfpUfg%3D%3D) | 5 | 0.93 | 4.65 | OPEN | OPEN | OPEN |
| B052 | [71-CRCW06031R00FKEA](https://www.mouser.com/en/ProductDetail/Vishay/CRCW06031R00FKEA?qs=80Q0wBSdnoFsJFjT92phpw%3D%3D) | 8 | 0.10 | 0.80 | 538326 | 12 Weeks | OPEN |
| B053 | [71-WFMB2512R0330FEA](https://www.mouser.com/ProductDetail/Vishay-Dale/WFMB2512R0330FEA?qs=2WXlatMagcH7xrOdLzbSxA%3D%3D) | 53 | 1.10 | 58.30 | 0 | 87 Weeks | OPEN |
| B054 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B055 | [71-CRCW1206-10K-E3](https://www.mouser.com/ProductDetail/Vishay/CRCW120610K0FKEA?qs=ODaLBy2SlZHPHItpfGW8KQ%3D%3D) | 5 | 0.10 | 0.50 | 580301 | 12 Weeks | OPEN |
| B056 | [71-TNPW06034K32BEEA](https://au.mouser.com/en/ProductDetail/Vishay/TNPW06034K32BEEA?qs=sGAEpiMZZMtG0KNrPCHnjUkh%2F9eucPbm%2FECs8LQBFnU%3D) | 5 | OPEN | OPEN | 10536 | 22 Weeks | OPEN |
| B057 | [71-WSL2512R3300FEA](https://www.mouser.com/ProductDetail/Vishay-Dale/WSL2512R3300FEA?qs=z7wylDbq%2FU7JmRwkAzOwJQ%3D%3D) | 5 | 0.66 | 3.30 | 82217 | OPEN | OPEN |
| B058 | [71-CRCW0603-10-E3](https://www.mouser.com/ProductDetail/Vishay/CRCW060310R0FKEA?qs=wiO5jjUX9wsETsRLGnHNyA%3D%3D) | 5 | 0.10 | 0.50 | 417104 | 12 Weeks | OPEN |
| B059 | [71-TNPW08051M00BEEA](https://www.mouser.com/ProductDetail/Vishay/TNPW08051M00BEEA?qs=1C6%2FyOstnVs6mca%252BeEgWbA%3D%3D) | 5 | OPEN | OPEN | 14550 | OPEN | OPEN |
| B060 | [71-TNPW060388K7BEEA](https://eu.mouser.com/en/ProductDetail/Vishay/TNPW060388K7BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6AbwmdvebLgE%3D) | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B061 | [71-TNPW060323K7BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060323K7BEEA?qs=rhzOH%252BTaZWt4L%252B7rCpkOzw%3D%3D) | 5 | 0.27 | 1.35 | 7022 | 22 Weeks | OPEN |
| B062 | [71-TNPW060315K0BEEA](https://my.mouser.com/en/ProductDetail/Vishay/TNPW060315K0BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6%2FHqGwBTfsDk%3D) | 8 | OPEN | OPEN | 17026 | OPEN | OPEN |
| B063 | [71-TNPW0805383KBEEA](https://lv.mouser.com/en/ProductDetail/Vishay/TNPW0805383KBEEA?qs=sGAEpiMZZMvdGkrng054tzV2vEziUmcBmW%252BZbNQ0D3g%3D) | 5 | OPEN | OPEN | 3 | 17 Weeks | OPEN |
| B064 | [71-TNPW060368K1BEEA](https://nz.mouser.com/en/ProductDetail/Vishay/TNPW060368K1BEEA?qs=sGAEpiMZZMtlubZbdhIBINLZLyWy7QeNDpwhuu44zSU%3D) | 5 | OPEN | OPEN | 5726 | 22 Weeks | OPEN |
| B065 | [71-TNPW0603249KBEEA](https://lv.mouser.com/en/ProductDetail/Vishay/TNPW0603249KBEEA?qs=sGAEpiMZZMvdGkrng054t4IX%2F4ppktZymWPavdpogMU%3D) | 5 | 0.261 | 1.305 | 11427 | 22 Weeks | OPEN |
| B066 | [71-CRCW0603-100-E3](https://www.mouser.com/en/ProductDetail/Vishay/CRCW0603100RFKEA?qs=90AHS1y%2FsidGWjjxZAupKg%3D%3D) | 5 | 0.10 | 0.50 | 199607 | 18 Weeks | OPEN |
| B067 | [71-TNPW06036K49BEEA](https://hu.mouser.com/en/ProductDetail/Vishay/TNPW06036K49BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6Ajf5Nzy89Tc%3D) | 5 | OPEN | OPEN | 0 | 22 Weeks | OPEN |
| B068 | [71-TNPW0805365KBEEA](https://au.mouser.com/ProductDetail/Vishay/TNPW0805365KBEEA?qs=l%252BcklhsjygfNLOYszerPyg%3D%3D) | 8 | OPEN | OPEN | 0 | 8 Weeks | OPEN |
| B069 | [71-TNPW060348K7BEEA](https://www.mouser.com/ProductDetail/Vishay/TNPW060348K7BEEA?qs=hEUCbmUtbxHsTKFAH4FGJg%3D%3D) | 5 | 0.26 | 1.30 | 6337 | OPEN | OPEN |
| B070 | [71-WSL27262L000FEA](https://www.mouser.com/ProductDetail/Vishay-Dale/WSL27262L000FEA?qs=eFWhpKjIuGiQvQmTqzV1gQ%3D%3D) | 5 | 2.62 | 13.10 | 2048 | 24 Weeks | OPEN |
| B071 | [71-TNPW060310R0BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060310R0BEEA?qs=ncxkyCpAYDDV%2F27OnQWKbw%3D%3D) | 8 | 0.35 | 2.80 | 61727 | 22 Weeks | OPEN |
| B072 | [71-TNPW06034K70BEEA](https://eu.mouser.com/ProductDetail/Vishay/TNPW06034K70BEEA?qs=hEUCbmUtbxH2b2BZ4ek4qQ%3D%3D) | 8 | OPEN | OPEN | 14 | OPEN | OPEN |
| B073 | [71-TNPW060347R0BEEA](https://www.mouser.com/ProductDetail/Vishay/TNPW060347R0BEEA?qs=p6uSqCSYdoMOPn%252Bml2n48A%3D%3D) | 5 | 0.78 | 3.90 | 2199 | OPEN | OPEN |
| B074 | [71-TNPW060320K0BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060320K0BEEA?qs=U8jWr0D8IJi%2Ff30ZsPE6lA%3D%3D) | 8 | 0.26 | 2.08 | 64336 | 22 Weeks | OPEN |
| B075 | [71-TNPW06036K19BEEA](https://eu.mouser.com/en/ProductDetail/Vishay/TNPW06036K19BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6kwsQ2%252BXgEuU%3D) | 5 | OPEN | OPEN | 6 | 22 Weeks | OPEN |
| B076 | [71-TNPW060349K9BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW060349K9BEEA?qs=hEUCbmUtbxG1Kn0Yx0petw%3D%3D) | 5 | 0.26 | 1.30 | 44343 | 22 Weeks | OPEN |
| B077 | [71-TNPW0603143KBEEA](https://uy.mouser.com/en/ProductDetail/Vishay/TNPW0603143KBEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f64Y6MLIrBo3s%3D) | 5 | OPEN | OPEN | 4 | 22 Weeks | OPEN |
| B078 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B079 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B080 | [595-TPS26630RGER](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS26630RGER?qs=vLWxofP3U2ztcw332RlqMw%3D%3D) | 4 | 4.52 | 18.08 | OPEN | OPEN | OPEN |
| B081 | [595-LM61460AANRJRR](https://au.mouser.com/en/ProductDetail/Texas-Instruments/LM61460AANRJRR?qs=sGAEpiMZZMvAX9OfPh%252B2NZ7JgNTOi02AV26FnUWhnvp%252BGBZD%252BgTDyA%3D%3D) | 4 | OPEN | OPEN | 1259 | OPEN | OPEN |
| B082 | [584-LTC7001IMSEPBF](https://www.mouser.com/ProductDetail/Analog-Devices/LTC7001IMSEPBF?qs=BZBei1rCqCCuiLQ%252BeMjtcQ%3D%3D) | 4 | 8.59 | 34.36 | 199 | OPEN | OPEN |
| B083 | [595-REF5025IDGKR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/REF5025IDGKR?qs=AFkNxQkJKAJ8W8NohOGecw%3D%3D) | 4 | 7.56 | 30.24 | 2263 | 20 Weeks | OPEN |
| B084 | [595-TLV3201AIDBVR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TLV3201AIDBVR?qs=5771e39Rz9GGuYwPEKy7fA%3D%3D) | 14 | 1.03 | 14.42 | 0 | OPEN | OPEN |
| B085 | [OPEN](https://www.mouser.com/es/ProductDetail/Texas-Instruments/TPS7A1601DGNR?qs=KC2rBGieF4oE7JWkZS%2FgAQ%3D%3D) | 7 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B086 | OPEN | 7 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B087 | [584-LT4363HMS-1#PBF](https://www.mouser.com/ProductDetail/Analog-Devices/LT4363HMS-1PBF?qs=hVkxg5c3xu8ArsH0sbL%2FnA%3D%3D) | 4 | 11.79 | 47.16 | 1056 | OPEN | OPEN |
| B088 | [584-LTC3115IFE-1#PBF](https://www.mouser.com/en/ProductDetail/Analog-Devices/LTC3115IFE-1PBF?qs=hVkxg5c3xu9vMUkzUIxpDQ%3D%3D) | 4 | 19.65 | 78.60 | 1054 | OPEN | OPEN |
| B089 | [OPEN](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS70933DBVR?qs=Z9twEOuL%252B%2FJOaGO60BtvLA%3D%3D) | 7 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B090 | [584-ADG4612BRUZ](https://www.mouser.com/ProductDetail/Analog-Devices/ADG4612BRUZ?qs=BpaRKvA4VqEHMnQJf6gOMQ%3D%3D) | 10 | 5.01 | 50.10 | 445 | OPEN | Restricted Availability: |
| B091 | [595-TPS3808G01DBVR](https://eu.mouser.com/ProductDetail/Texas-Instruments/TPS3808G01DBVR?qs=zwk82MlA57ZFbh4v6Meb8A%3D%3D) | 7 | OPEN | OPEN | 47 | 12 Weeks | OPEN |
| B092 | [595-TPS259470LRPWR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS259470LRPWR?qs=iLbezkQI%252BsibLmP55loGPQ%3D%3D) | 4 | OPEN | OPEN | 167 | 12 Weeks | OPEN |
| B093 | OPEN | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B094 | [595-TCA9517DGKR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TCA9517DGKR?qs=teNCaa%2FZ3av3Q4R5skhdZQ%3D%3D) | 4 | OPEN | OPEN | 222 | 16 Weeks | OPEN |
| B095 | [595-TPS3808G50DBVR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/TPS3808G50DBVR?qs=zwk82MlA57bbRDSNjc0z1g%3D%3D) | 4 | 1.84 | 7.36 | 0 | 20 Weeks | OPEN |
| B096 | [595-SN74LVC1G74DCTR](https://www.mouser.com/ProductDetail/Texas-Instruments/SN74LVC1G74DCTR?qs=DS7Z8uEdLNwRYlUtd5z9Zw%3D%3D) | 10 | 0.556 | 5.560 | 17460 | 16 Weeks | OPEN |
| B097 | [595-SN74LVC1G14DBVR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/SN74LVC1G14DBVR?qs=dT9u2OTAaVWRIgCrQFnxuQ%3D%3D) | 20 | 0.094 | 1.880 | 26244 | 20 Weeks | OPEN |
| B098 | [OPEN](https://www.mouser.com/en/ProductDetail/Texas-Instruments/SN74LVC1G32DBVR?qs=3pnr37ZAbK%2F6ArGi%2FPb2Ng%3D%3D) | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B099 | OPEN | 24 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B100 | [595-SN74LVC1G17DBVR](https://www.mouser.com/en/ProductDetail/Texas-Instruments/SN74LVC1G17DBVR?qs=fvkeCqCHl3BQIcdbAa1fbQ%3D%3D) | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H01 | [651-1777989](https://eu.mouser.com/ProductDetail/Phoenix-Contact/1777989?qs=TrDcmYSSX9WKfp2I32hSmA%3D%3D) | 4 | OPEN | OPEN | 10 | 7 Weeks | OPEN |
| H05 | [571-3-87456-6](https://ar.mouser.com/es/ProductDetail/TE-Connectivity/3-87456-6?qs=sGAEpiMZZMvlX3nhDDO4AGTYleWEkGmaDuMluOXipMk%3D) | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H06 | [571-873099](https://www.mouser.com/es/ProductDetail/TE-Connectivity/87309-9?qs=ZDXmSm13592Ol9UKkiRmzQ%3D%3D) | 33 | OPEN | OPEN | 112500 | OPEN | OPEN |
| H07 | [566-8521-100-02](https://eu.mouser.com/ProductDetail/Belden-Wire-Cable/8521-002100?qs=sGAEpiMZZMuGxYVy11yKKgHFk5vWcMIQhsWIt9snOas%3D) | 1 | OPEN | OPEN | 2 | OPEN | OPEN |
| H08 | [566-8521-100-10](https://my.mouser.com/en/ProductDetail/Belden-Wire-Cable/8521-010100?qs=sGAEpiMZZMuGxYVy11yKKvWndU1ab51ugk%2FTwCk%252B8%2Fk%3D) | 1 | OPEN | OPEN | 2 | 5 Weeks | OPEN |
| H09 | [566-8502-100-02](https://www.mouser.com/en/ProductDetail/Belden-Wire-Cable/8502-002100?qs=PcTXDFmDvaRnB3Fx%2FUgJ%252BA%3D%3D) | 1 | 171.81 | 171.81 | 7 | 5 Weeks | OPEN |
| H10 | [566-8502-100-10](https://www.mouser.com/ProductDetail/Belden-Wire-Cable/8502-010100?qs=8D2JqG3k8CjFj9wNKOzTuw%3D%3D) | 1 | 178.69 | 178.69 | 8 | 5 Weeks | OPEN |
| M01 | OPEN | 48 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M02 | OPEN | 96 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M03 | OPEN | 48 | OPEN | OPEN | OPEN | OPEN | OPEN |
| O01 | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| O02 | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |

## digikey commercial register

All prices below are USD per stated order unit. Lead time is the published manufacturer/factory lead time if retrieved, not an arrival promise. Dates/crawl ages, currency limitations and MOQ assumptions are in the CSV.

| ID | Distributor SKU / evidence | Order qty | Unit USD | Extended USD | Stock | Lead time | Lifecycle |
|---|---|---:|---:|---:|---|---|---|
| B001 | [490-1857-1-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM32ER72A105KA01L/587295) | 11 | 0.78400 | 8.62400 | 250534 | OPEN | Not For New Designs |
| B002 | [490-1519-2-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM188R71H104KA93D/587854) | 142 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B003 | [490-6544-1-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM32ER71H106KA12L/2548481) | 30 | OPEN | OPEN | 0 | OPEN | Discontinued at DigiKey |
| B004 | [490-6484-2-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71E105KA99L/2472647) | 27 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B005 | [445-5632-1-ND](https://www.digikey.com/en/products/detail/tdk/CGA3E2C0G1H220J080AA/2443110) | 5 | 0.15000 | 0.75000 | 27243 | 24 Weeks | Active |
| B006 | [445-C5750X7R1H226M250KBCT-ND](https://www.digikey.com/en/products/detail/tdk-corporation/C5750X7R1H226M250KB/13672015) | 24 | 3.46000 | 83.04000 | 0 | 24 Weeks | Active |
| B007 | [490-9962-2-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71E475KA73L/4905545) | 14 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B008 | [490-4736-2-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71H105KA12L/1244326) | 8 | OPEN | OPEN | OPEN | OPEN | Obsolete |
| B009 | OPEN | 40 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B010 | [445-7404-1-ND](https://www.digikey.com/en/products/detail/tdk-corporation/C1608C0G1H103J080AA/2732839) | 8 | 0.24000 | 1.92000 | 26138 | 24 Weeks | Active |
| B011 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B012 | [445-1293-1-ND](https://www.digikey.com/en/products/detail/tdk-corporation/C1608C0G1H102J080AA/513735) | 5 | 0.16000 | 0.80000 | 149480 | 24 Weeks | Active |
| B013 | [490-1415-1-ND](https://www.digikey.com/en/products/detail/murata-electronics/GRM1885C1H330JA01D/586908) | 5 | 0.13000 | 0.65000 | 1109312 | OPEN | Not For New Designs |
| B014 | [P124223-ND](https://www.digikey.com/en/products/detail/panasonic-electronic-components/EEU-FR1E221/9921023) | 8 | 0.71000 | 5.68000 | 0 | 37 Weeks | Active |
| B015 | [SMCJ36CALFCT-ND](https://www.digikey.com/en/products/detail/littelfuse-inc/SMCJ36CA/762405) | 4 | 0.97000 | 3.88000 | 0 | 34 Weeks | Active |
| B016 | [497-3812-5-ND](https://www.digikey.com/en/products/detail/stmicroelectronics/STPS60H100CT/691910) | 10 | 1.69800 | 16.98000 | 524 | 15 Weeks | Active |
| B017 | [1727-4795-1-ND](https://www.digikey.com/en/products/detail/nexperia-usa-inc/BAS116-215/1232056) | 30 | 0.12800 | 3.84000 | 0 | 30 Weeks | Active |
| B018 | [BAT46W-E3-08CT-ND](https://www.digikey.com/en/products/detail/vishay-general-semiconductor-diodes-division/BAT46W-E3-08/3104177) | 4 | 0.49000 | 1.96000 | 3 | 56 Weeks | Active |
| B019 | [B260-FDICT-ND](https://www.digikey.com/en/products/detail/diodes-incorporated/B260-13-F/814954) | 10 | 0.33700 | 3.37000 | 132304 | 44 Weeks | Active |
| B020 | [296-20859-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/LM4040A25IDBZR/1216465) | 7 | 4.23000 | 29.61000 | 5514 | 20 Weeks | Active |
| B021 | [486-3569-1-ND](https://www.digikey.com/en/products/detail/schurter-inc/3403-0285-23/6569073) | 5 | 3.26000 | 16.30000 | 1099 | 18 Weeks | Active |
| B022 | OPEN | 27 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B023 | [455-B2P-VH-FB-B-ND](https://www.digikey.com/en/products/detail/jst-sales-america-inc/B2P-VH-FB-B/2178726) | 4 | 0.23000 | 0.92000 | 70887 | 16 Weeks | Active |
| B024 | [277-5741-ND](https://www.digikey.com/en/products/detail/phoenix-contact/1776508/349000) | 4 | 1.72000 | 6.88000 | 1384 | 6 Weeks | Active |
| B025 | OPEN | 4 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B026 | OPEN | 24 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B027 | [732-74437636351002-ND](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/74437636351002/26681923) | 5 | 24.68000 | 123.40000 | 13 | 25 Weeks | Active |
| B028 | [732-1175-1-ND](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/7447789004/1638580) | 5 | 2.51000 | 12.55000 | 1170 | 20 Weeks | Active |
| B029 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B030 | [296-44351-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/CSD19537Q3/5438037) | 4 | 1.99000 | 7.96000 | 66702 | 20 Weeks | Active |
| B031 | [BSS138CT-ND](https://www.digikey.com/en/products/detail/onsemi/BSS138/244294) | 4 | 0.32000 | 1.28000 | 712990 | 26 Weeks | Active |
| B032 | [BSC034N06NSATMA1CT-ND](https://www.digikey.com/en/products/detail/infineon-technologies/BSC034N06NSATMA1/5959900) | 7 | 1.69000 | 11.83000 | 14650 | 52 Weeks | Active |
| B033 | [296-41076-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/CSD18540Q5B/5181315?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKAVgE4KAWAJguQF9Gg) | 7 | 3.26000 | 22.82000 | 0 | 9 Weeks | Active |
| B034 | [1727-2N7002,215CT-ND](https://www.digikey.com/en/products/detail/nexperia-usa-inc/2N7002-215/762973) | 4 | 0.18000 | 0.72000 | 0 | 30 Weeks | Active |
| B035 | [FDB33N25TMCT-ND](https://www.digikey.com/en/products/detail/onsemi/FDB33N25TM/1922973) | 4 | 3.57000 | 14.28000 | 6828 | 13 Weeks | Active |
| B036 | [541-3654-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603332KBEEA/1607053) | 5 | 0.26000 | 1.30000 | 0 | 25 Weeks | Active |
| B037 | [541-3691-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060354K9BEEA/7355051) | 5 | 0.26000 | 1.30000 | 98 | 25 Weeks | Active |
| B038 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B039 | [541-3592-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060315K8BEEA/1606901) | 5 | 0.26000 | 1.30000 | 2449 | 25 Weeks | Active |
| B040 | [TNP4.02KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06034K02BEEA/1606835) | 5 | 0.26000 | 1.30000 | 10881 | 25 Weeks | Active |
| B041 | [541-3694-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060356K2BEEA/7355054) | 5 | 0.26000 | 1.30000 | 8661 | 25 Weeks | Active |
| B042 | [TNP10.0KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060310K0BEEA/1857057) | 93 | 0.20320 | 18.89760 | 67287 | 14 Weeks | Active |
| B043 | [TNP100KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603100KBEEA/1857055) | 57 | 0.19180 | 10.93260 | 30867 | 14 Weeks | Active |
| B044 | [541-2018-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060333K2BEEA/4869152) | 8 | 0.26000 | 2.08000 | 16317 | 25 Weeks | Active |
| B045 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B046 | [541-0.0GCT-ND](https://www.digikey.com/en/products/detail/vishay-dale/CRCW06030000Z0EA/1174156?s=N4IgTCBcDaIKwBYCMBaADAOjQcQMIBUUA5AERAF0BfIA) | 5 | 0.10000 | 0.50000 | 3358163 | 21 Weeks | Active |
| B047 | [TNP1.00KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06031K00BEEA/1606767) | 37 | 0.21900 | 8.10300 | 74229 | 25 Weeks | Active |
| B048 | [TNP24.9KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060324K9BEEA/1606924) | 5 | 0.28000 | 1.40000 | 10795 | 25 Weeks | Active |
| B049 | [541-4557-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06039K88BEEA/4972508) | 5 | 0.26000 | 1.30000 | 8597 | 25 Weeks | Active |
| B050 | [TNP100AACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603100RBEEA/1857056) | 5 | 0.26000 | 1.30000 | 33193 | 25 Weeks | Active |
| B051 | [541-TNPW12062M00BEEACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW12062M00BEEA/11500936) | 5 | 0.59000 | 2.95000 | 80469 | 11 Weeks | Active |
| B052 | [541-1.00HHCT-ND](https://www.digikey.com/en/products/detail/vishay-dale/CRCW06031R00FKEA/1961997) | 8 | 0.10000 | 0.80000 | 215256 | 15 Weeks | Active |
| B053 | [541-10281-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/WFMB2512R0330FEA/9972305) | 53 | 0.99320 | 52.63960 | 0 | 83 Weeks | Active |
| B054 | [TNP32.4KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060332K4BEEA/1857080) | 8 | 0.26000 | 2.08000 | 4140 | 25 Weeks | Active |
| B055 | [541-10.0KFCT-ND](https://www.digikey.com/en/products/detail/vishay-dale/CRCW120610K0FKEA/1176758) | 5 | 0.11000 | 0.55000 | 671025 | 21 Weeks | Active |
| B056 | [541-TNPW06034K32BEEACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06034K32BEEA/1606839) | 5 | 0.26000 | 1.30000 | 12837 | 25 Weeks | Active |
| B057 | [WSLG-.33CT-ND](https://www.digikey.com/en/products/detail/vishay-dale/WSL2512R3300FEA/712579) | 5 | 0.67000 | 3.35000 | 21062 | 38 Weeks | Active |
| B058 | [541-10.0HCT-ND](https://www.digikey.com/en/products/detail/vishay-dale/CRCW060310R0FKEA/1174440) | 5 | 0.10000 | 0.50000 | 877308 | 21 Weeks | Active |
| B059 | OPEN | 5 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B060 | [541-2050-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060388K7BEEA/4869184) | 5 | 0.26000 | 1.30000 | 4608 | 25 Weeks | Active |
| B061 | [541-TNPW060323K7BEEACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060323K7BEEA/1606921) | 5 | 0.26000 | 1.30000 | 4792 | 25 Weeks | Active |
| B062 | [TNP15.0KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060315K0BEEA/1606899) | 8 | 0.26000 | 2.08000 | 12305 | 14 Weeks | Active |
| B063 | [541-TNPW0805383KBEEACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0805383KBEEA/1607575) | 5 | 0.41000 | 2.05000 | 3853 | 20 Weeks | Active |
| B064 | [541-3702-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060368K1BEEA/7355062) | 5 | 0.26000 | 1.30000 | 8148 | 25 Weeks | Active |
| B065 | [TNP249KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603249KBEEA/1857071) | 5 | 0.26000 | 1.30000 | 8936 | 25 Weeks | Active |
| B066 | [541-100HCT-ND](https://www.digikey.com/en/products/detail/vishay-dale/CRCW0603100RFKEA/1179695) | 5 | 0.10000 | 0.50000 | 2672582 | 21 Weeks | Active |
| B067 | [541-3705-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06036K49BEEA/7355065) | 5 | 0.28000 | 1.40000 | 7189 | 25 Weeks | Active |
| B068 | OPEN | 8 | OPEN | OPEN | OPEN | OPEN | OPEN |
| B069 | [541-3679-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060348K7BEEA/1606959) | 5 | 0.26000 | 1.30000 | 2 | 25 Weeks | Active |
| B070 | [541-10339-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/WSL27262L000FEA/5215856) | 5 | 2.14000 | 10.70000 | 3877 | 27 Weeks | Active |
| B071 | [TNP10.0AACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060310R0BEEA/1857058) | 8 | OPEN | OPEN | 30051 | 25 Weeks | Active |
| B072 | [TNP4.70KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06034K70BEEA/1857085) | 8 | 0.26000 | 2.08000 | 18798 | 25 Weeks | Active |
| B073 | [541-TNPW060347R0BEEACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060347R0BEEA/1606615) | 5 | 0.35000 | 1.75000 | 8472 | 25 Weeks | Active |
| B074 | [TNP20.0KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060320K0BEEA/1857070) | 8 | 0.26000 | 2.08000 | 3511 | 14 Weeks | Active |
| B075 | [541-2041-1-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06036K19BEEA/1606857) | 5 | 0.26000 | 1.30000 | 10702 | 25 Weeks | Active |
| B076 | [TNP49.9KAACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060349K9BEEA/1606960) | 5 | 0.26000 | 1.30000 | 33837 | 25 Weeks | Active |
| B077 | [541-TNPW0603143KBEEACT-ND](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603143KBEEA/11500920) | 5 | 0.26000 | 1.30000 | 4900 | 25 Weeks | Active |
| B078 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B079 | N/A | 0 | N/A | N/A | N/A | N/A | N/A |
| B080 | [296-TPS26630RGERCT-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS26630RGER/10820326) | 4 | 4.52000 | 18.08000 | 0 | 20 Weeks | Active |
| B081 | [296-LM61460AANRJRRCT-ND](https://www.digikey.com/en/products/detail/texas-instruments/LM61460AANRJRR/12165587) | 4 | 4.48000 | 17.92000 | 24 | 20 Weeks | Active |
| B082 | [505-LTC7001IMSE#PBF-ND](https://www.digikey.com/en/products/detail/analog-devices-inc/LTC7001IMSE-PBF/7363804) | 4 | 9.38000 | 37.52000 | 0 | 24 Weeks | Active |
| B083 | [296-REF5025IDGKRCT-ND](https://www.digikey.com/en/products/detail/texas-instruments/REF5025IDGKR/2232441) | 4 | 7.56000 | 30.24000 | 3647 | 20 Weeks | Active |
| B084 | [296-36750-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TLV3201AIDBVR/3188691) | 14 | 1.02900 | 14.40600 | 0 | 20 Weeks | Active |
| B085 | [296-30203-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A1601DGNR/2811171) | 7 | 4.12000 | 28.84000 | 0 | 16 Weeks | Active |
| B086 | [296-30285-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/UCC27511DBVR/3053304) | 7 | 0.99000 | 6.93000 | 9129 | 20 Weeks | Active |
| B087 | [505-LT4363HMS-1#PBF-ND](https://www.digikey.com/en/products/detail/analog-devices-inc/LT4363HMS-1-PBF/4245464) | 4 | 12.88000 | 51.52000 | 2929 | 19 Weeks | Active |
| B088 | [505-LTC3115IFE-1#PBF-ND](https://www.digikey.com/en/products/detail/analog-devices-inc/LTC3115IFE-1-PBF/3074270) | 4 | 20.12000 | 80.48000 | 896 | 13 Weeks | Active |
| B089 | [296-35483-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS70933DBVR/3767568) | 7 | 1.51000 | 10.57000 | 0 | 20 Weeks | Active |
| B090 | [505-ADG4612BRUZ-ND](https://www.digikey.com/en/products/detail/analog-devices-inc/ADG4612BRUZ/2507324) | 10 | 5.13100 | 51.31000 | 694 | 10 Weeks | Active |
| B091 | [296-17188-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS3808G01DBVR/666712?msockid=2002127634786b56294b04d135d96a9f) | 7 | 1.96000 | 13.72000 | 80521 | 16 Weeks | Active |
| B092 | [296-TPS259470LRPWRCT-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS259470LRPWR/14124014) | 4 | 1.53000 | 6.12000 | 312 | 12 Weeks | Active |
| B093 | [296-INA228AIDGSRCT-ND](https://www.digikey.com/en/products/detail/texas-instruments/INA228AIDGSR/13691042) | 4 | 4.68000 | 18.72000 | 0 | 20 Weeks | Active |
| B094 | [296-35972-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TCA9517DGKR/3926681) | 4 | 1.37000 | 5.48000 | 13344 | 20 Weeks | Active |
| B095 | [296-17196-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/TPS3808G50DBVR/666729) | 4 | 1.84000 | 7.36000 | 0 | 20 Weeks | Active |
| B096 | [296-25553-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G74DCTR/2195375) | 10 | 0.55600 | 5.56000 | 0 | 20 Weeks | Active |
| B097 | [296-11607-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G14DBVR/385724?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKAJgDYwLkBOAVgoF8mg) | 20 | 0.09400 | 1.88000 | 2497 | 16 Weeks | Active |
| B098 | [296-9847-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G32DBVR/381323) | 4 | 0.12000 | 0.48000 | 0 | 20 Weeks | Active |
| B099 | [296-11601-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G08DBVR/385718?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLJATgDZEAWAJkQF8Gg) | 24 | 0.07700 | 1.84800 | 236414 | 16 Weeks | Active |
| B100 | [296-11933-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G17DBVR/389051?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKAFjGQAZkyBOAXwaA) | 4 | 0.15000 | 0.60000 | 34117 | 16 Weeks | Active |
| H01 | [277-5710-ND](https://www.digikey.com/en/products/detail/phoenix-contact/1777989/349029?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKNAFmTQAYAmAX3qA) | 4 | 2.32000 | 9.28000 | 0 | 6 Weeks | Active |
| H05 | [A3044-ND](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/3-87456-6/30003) | 4 | 5.70000 | 22.80000 | 0 | 29 Weeks | Active |
| H06 | [A100842CT-ND](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/87309-9/290791) | 33 | 0.41520 | 13.70160 | 110052 | 4 Weeks | Active |
| H07 | [BEL1663-100-ND](https://www.digikey.com/en/products/detail/belden-inc/8521-002100/7389045) | 1 | 267.84000 | 267.84000 | 10 | 7 Weeks | Active |
| H08 | [BEL1664-100-ND](https://www.digikey.com/en/products/detail/belden-inc/8521-010100/7389046) | 1 | 267.84000 | 267.84000 | 0 | 7 Weeks | Active |
| H09 | [OPEN](https://www.digikey.com/es/products/detail/belden-inc/8502-002100/7389017) | 1 | OPEN | OPEN | OPEN | OPEN | OPEN |
| H10 | [OPEN](https://www.digikey.com/en/products/detail/belden-inc/8502-010100/7389023) | 1 | OPEN | OPEN | 14 | OPEN | Active |
| M01 | OPEN | 48 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M02 | OPEN | 96 | OPEN | OPEN | OPEN | OPEN | OPEN |
| M03 | OPEN | 48 | OPEN | OPEN | OPEN | OPEN | OPEN |
| O01 | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| O02 | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |

## Alternate disposition register

Different-MPN candidates are excluded from order quantities and totals and need engineering approval. SAME-MPN entries are alternate supplier routes for the existing quantities; do not order twice. Backorder/OPEN-stock routes do not solve an immediate stock shortage. SINGLE-OBSERVED means only one channel in the retrieved evidence showed stock, not proof of an exclusive manufacturer or distributor. OPEN replacements remain unresolved procurement actions.

| ID | Selected MPN | Alternate / manufacturer | Evidence | Disposition |
|---|---|---|---|---|
| B001 | GRM32ER72A105KA01L | GRM32CR72A105KA35L / Murata Electronics | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM32ER72A105KA01L/587295) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B002 | GRM188R71H104KA93D | 0603BB104K500YT / Knowles Novacap | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM188R71H104KA93D/587854) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B003 | GRM32ER71H106KA12L | UMK325AB7106KM-T / Taiyo Yuden | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM32ER71H106KA12L/2548481) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B004 | GRM21BR71E105KA99L | GRM219R71E105KA88D / Murata Electronics | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71E105KA99L/2472647) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B005 | CGA3E2C0G1H220J080AA | CGA3E2C0G1H220J080AA / TDK | [source](https://www.digikey.com/en/products/detail/tdk/CGA3E2C0G1H220J080AA/2443110) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B006 | C5750X7R1H226M250KB | CGA9P3X7R1H226M250KB / TDK | [source](https://www.digikey.com/en/products/detail/tdk-corporation/C5750X7R1H226M250KB/13672015) | UNAPPROVED catalog candidate (Parametric Equivalent); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B007 | GRM21BR71E475KA73L | 08053C475KAT2A / KYOCERA AVX | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71E475KA73L/4905545) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B008 | GRM21BR71H105KA12L | GJ821BR71H105KA12L / Murata Electronics | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71H105KA12L/1244326) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B009 | PCH1V471MCL1GS | PCH1V471MCL1GS / Nichicon | [source](https://www.nichicon.co.jp/_assets/images/products/catalog/corporate/digital/sh_pch.pdf) | Alternate sourcing route: manufacturer/distributor quote for exact part. Different electrical MPN OPEN; pulse/ESR/ESL/thermal requalification required. |
| B010 | C1608C0G1H103J080AA | C1608NP01H103J080AA / TDK | [source](https://www.digikey.com/en/products/detail/tdk-corporation/C1608C0G1H103J080AA/2732839) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B011 | C3216X7R1H475K160AB | C3216X7R1H475K160AC / TDK | [source](https://www.digikey.com/en/products/detail/tdk/C3216X7R1H475K160AC/2792268) | UNAPPROVED: Suffix AC is a catalog candidate, not an alias for AB; verify DC-bias capacitance, package and compensation. Stock remains a separate issue. |
| B012 | C1608C0G1H102J080AA | C0603C102J5GAC7411 / KEMET | [source](https://www.digikey.com/en/products/detail/tdk-corporation/C1608C0G1H102J080AA/513735) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B013 | GRM1885C1H330JA01D | GRM1885C1H330GA01D / Murata Electronics | [source](https://www.digikey.com/en/products/detail/murata-electronics/GRM1885C1H330JA01D/586908) | UNAPPROVED catalog candidate (Upgrade); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B014 | EEU-FR1E221 | UHE1E221MPD / Nichicon | [source](https://www.digikey.com/en/products/detail/panasonic-electronic-components/EEU-FR1E221/9921023) | UNAPPROVED catalog candidate (Similar); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B015 | SMCJ36CA | SMCJ36CA-TP / MCC (Micro Commercial Components) | [source](https://www.digikey.com/en/products/detail/littelfuse-inc/SMCJ36CA/762405) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B016 | STPS60H100CT | STPS60H100CT / STMicroelectronics | [source](https://www.digikey.com/en/products/detail/stmicroelectronics/STPS60H100CT/691910) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B017 | BAS116,215 | BAS116-7-F / Diodes Incorporated | [source](https://www.digikey.com/en/products/detail/nexperia-usa-inc/BAS116-215/1232056) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B018 | BAT46W-E3-08 | BAT46W-TP / MCC (Micro Commercial Components) | [source](https://www.digikey.com/en/products/detail/vishay-general-semiconductor-diodes-division/BAT46W-E3-08/3104177) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B019 | B260-13-F | B260-13-F / Diodes Incorporated | [source](https://www.digikey.com/en/products/detail/diodes-incorporated/B260-13-F/814954) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B020 | LM4040A25IDBZR | LM4040A25IDBZR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/LM4040A25IDBZR/1216465) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B021 | 3403.0285.23 | 3403.0285.11 / SCHURTER Inc. | [source](https://www.digikey.com/en/products/detail/schurter-inc/3403-0285-23/6569073) | UNAPPROVED catalog candidate (Parametric Equivalent); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B022 | B2B-XH-A(LF)(SN) | B2B-XH-A(LF)(SN) / JST | [source](https://www.mouser.com/en/ProductDetail/JST-Commercial/B2B-XH-ALFSN?qs=cdbOS8ANM9DdcSn9qRmfCw%3D%3D) | SAME-MPN alternate sourcing: lcsc, mouser each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B023 | B2P-VH-FB-B(LF)(SN) | B2P-VH-FB-B(LF)(SN) / JST | [source](https://www.digikey.com/en/products/detail/jst-sales-america-inc/B2P-VH-FB-B/2178726) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B024 | 1776508 | 1776508 / Phoenix Contact | [source](https://www.digikey.com/en/products/detail/phoenix-contact/1776508/349000) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B025 | B4B-XH-A(LF)(SN) | B4B-XH-A(LF)(SN) / JST | [source](https://www.mouser.com/ProductDetail/JST-Commercial/B4B-XH-ALFSN?qs=cdbOS8ANM9CfC08d%252BywhFw%3D%3D) | SAME-MPN alternate sourcing: lcsc, mouser each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B026 | CUSTOM-FX-CU-01 RevA | CUSTOM-FX-CU-01 RevA / Qualified fabricator OPEN | [source](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/56e9837e522c01bd680aca602f9f471d38d6039f/docs/evidence/r2/gate4b/PIN_REVIEW.md) | Build-to-drawing sourcing only; no compatible catalog jumper verified. Identity closed; procurement and qualification OPEN. |
| B027 | 74437636351002 | 74437636351002 / Würth Elektronik | [source](https://www.mouser.com/ProductDetail/Wurth-Elektronik/74437636351002?qs=2FehpBK1j97R94Iy%2Fo9K7Q%3D%3D) | SAME-MPN backup sourcing: mouser 710-74437636351002; observed stock 0. Backorder/stock confirmation required; no stocked replacement established. Different component MPN remains OPEN. |
| B028 | 7447789004 | 7447789004 / Würth Elektronik | [source](https://www.mouser.com/ProductDetail/Wurth-Elektronik/7447789004?qs=E%2F%2FhvbtCqpM%252BzhhZNuF4OQ%3D%3D) | SAME-MPN backup sourcing: mouser 710-7447789004; observed stock 0. Backorder/stock confirmation required; no stocked replacement established. Different component MPN remains OPEN. |
| B030 | CSD19537Q3 | CSD19537Q3 / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/CSD19537Q3/5438037) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B031 | BSS138 | BSS138 / onsemi | [source](https://www.digikey.com/en/products/detail/onsemi/BSS138/244294) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B032 | BSC034N06NSATMA1 | BSC034N06NSATMA1 / Infineon Technologies | [source](https://www.digikey.com/en/products/detail/infineon-technologies/BSC034N06NSATMA1/5959900) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B033 | CSD18540Q5B | FDMS86500DC / onsemi | [source](https://www.digikey.com/en/products/detail/texas-instruments/CSD18540Q5B/5181315?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKAVgE4KAWAJguQF9Gg) | UNAPPROVED catalog candidate (Similar); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B034 | 2N7002,215 | 2N7002ET1G / onsemi | [source](https://www.digikey.com/en/products/detail/nexperia-usa-inc/2N7002-215/762973) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B035 | FDB33N25TM | FDB33N25TM / onsemi | [source](https://www.digikey.com/en/products/detail/onsemi/FDB33N25TM/1922973) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B036 | TNPW0603332KBEEA | RG1608P-3323-B-T5 / Susumu | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603332KBEEA/1607053) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B037 | TNPW060354K9BEEA | TNPW060354K9BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060354K9BEEA/7355051) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B038 | TNPW0805348KBEEA | ERA-6AEB3483V / Panasonic Industry | [source](https://www.digikey.com/en/products/detail/panasonic-industry/ERA-6AEB3483V/2025891) | UNAPPROVED: 348 kohm, 0.1%, 25 ppm/K, 0805 candidate; 0.125 W rating differs. Verify voltage and power margins. |
| B039 | TNPW060315K8BEEA | TNPW060315K8BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060315K8BEEA/1606901) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B040 | TNPW06034K02BEEA | TNPW06034K02BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06034K02BEEA/1606835) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B041 | TNPW060356K2BEEA | TNPW060356K2BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060356K2BEEA/7355054) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B042 | TNPW060310K0BEEA | TNPW060310K0BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060310K0BEEA/1857057) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B043 | TNPW0603100KBEEA | TNPW0603100KBEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603100KBEEA/1857055) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B044 | TNPW060333K2BEEA | TNPW060333K2BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060333K2BEEA/4869152) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B045 | TNPW060324K4BEEA | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |
| B046 | CRCW06030000Z0EA | CRCW06030000Z0EA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/CRCW06030000Z0EA/1174156?s=N4IgTCBcDaIKwBYCMBaADAOjQcQMIBUUA5AERAF0BfIA) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B047 | TNPW06031K00BEEA | TNPW06031K00BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06031K00BEEA/1606767) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B048 | TNPW060324K9BEEA | TNPW060324K9BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060324K9BEEA/1606924) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B049 | TNPW06039K88BEEA | TNPW06039K88BEEA / Vishay | [source](https://gr.mouser.com/en/ProductDetail/Vishay/TNPW06039K88BEEA?qs=sGAEpiMZZMvdGkrng054twbPyJJnNTBKxZF4yk9Nt%2FU%3D) | SAME-MPN backup sourcing: mouser 71-TNPW06039K88BEEA; observed stock OPEN. Backorder/stock confirmation required; no stocked replacement established. Different component MPN remains OPEN. |
| B050 | TNPW0603100RBEEA | TNPW0603100RBEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603100RBEEA/1857056) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B051 | TNPW12062M00BEEA | TNPW12062M00BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW12062M00BEEA/11500936) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B052 | CRCW06031R00FKEA | CRCW06031R00FKEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/CRCW06031R00FKEA/1961997) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B053 | WFMB2512R0330FEA | WFMB2512R0330FEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/WFMB2512R0330FEA/9972305) | SAME-MPN backup sourcing: digikey 541-10281-1-ND; observed stock 0. Backorder/stock confirmation required; no stocked replacement established. Different component MPN remains OPEN. |
| B054 | TNPW060332K4BEEA | ERA-3AEB3242V / Panasonic Industry | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060332K4BEEA/1857080) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B055 | CRCW120610K0FKEA | CRCW120610K0FKEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/CRCW120610K0FKEA/1176758) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B056 | TNPW06034K32BEEA | TNPW06034K32BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06034K32BEEA/1606839) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B057 | WSL2512R3300FEA | WSL2512R3300FEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/WSL2512R3300FEA/712579) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B058 | CRCW060310R0FKEA | CRCW060310R0FKEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/CRCW060310R0FKEA/1174440) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B059 | TNPW08051M00BEEA | TNPW08051M00BEEA / Vishay | [source](https://www.mouser.com/ProductDetail/Vishay/TNPW08051M00BEEA?qs=1C6%2FyOstnVs6mca%252BeEgWbA%3D%3D) | SAME-MPN alternate sourcing: lcsc, mouser each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B060 | TNPW060388K7BEEA | ERA-3AEB8872V / Panasonic Industry | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060388K7BEEA/4869184) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B061 | TNPW060323K7BEEA | TNPW060323K7BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060323K7BEEA/1606921) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B062 | TNPW060315K0BEEA | TNPW060315K0BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060315K0BEEA/1606899) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B063 | TNPW0805383KBEEA | ERA-6AEB3833V / Panasonic Industry | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0805383KBEEA/1607575) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B064 | TNPW060368K1BEEA | TNPW060368K1BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060368K1BEEA/7355062) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B065 | TNPW0603249KBEEA | TNPW0603249KBEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603249KBEEA/1857071) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B066 | CRCW0603100RFKEA | CRCW0603100RFKEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/CRCW0603100RFKEA/1179695) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B067 | TNPW06036K49BEEA | RT0603BRD076K49L / YAGEO | [source](https://www.digikey.com/en/products/detail/yageo/RT0603BRD076K49L/5139169) | UNAPPROVED catalog candidate: 6.49 kohm, 0.1%, 25 ppm/K, 0603, 0.1 W; listed Active with 47061 pieces in the indexed snapshot. Lower nominal power than TNPW requires manufacturer datasheet, voltage, thermal and drift review. No substitution authorized; excluded from totals. |
| B068 | TNPW0805365KBEEA | ERA-6AEB3653V / Panasonic Industry | [source](https://www.digikey.com/en/products/detail/panasonic-electronic-components/ERA-6AEB3653V/2025893) | UNAPPROVED: 365 kohm, 0.1%, 25 ppm/K, 0805 candidate; 0.125 W rating differs. Verify voltage and power margins. |
| B069 | TNPW060348K7BEEA | ERA-3AEB4872V / Panasonic Industry | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060348K7BEEA/1606959) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B070 | WSL27262L000FEA | WSL27262L000FEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/WSL27262L000FEA/5215856) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B071 | TNPW060310R0BEEA | TNPW060310R0BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060310R0BEEA/1857058) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B072 | TNPW06034K70BEEA | TNPW06034K70BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06034K70BEEA/1857085) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B073 | TNPW060347R0BEEA | TNPW060347R0BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060347R0BEEA/1606615) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B074 | TNPW060320K0BEEA | TNPW060320K0BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060320K0BEEA/1857070) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B075 | TNPW06036K19BEEA | TNPW06036K19BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW06036K19BEEA/1606857) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B076 | TNPW060349K9BEEA | TNPW060349K9BEEA / Vishay | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW060349K9BEEA/1606960) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B077 | TNPW0603143KBEEA | RT0603BRD07143KL / YAGEO | [source](https://www.digikey.com/en/products/detail/vishay-dale/TNPW0603143KBEEA/11500920) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B080 | TPS26630RGER | TPS26630RGET / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/TPS26630RGET/10434724) | UNAPPROVED: Different packing suffix candidate; preserve latch-off device variant and RGE package. No confirmed availability guarantee. |
| B081 | LM61460AANRJRR | LM61460AANRJRR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/LM61460AANRJRR/12165587) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B082 | LTC7001IMSE#PBF | LTC7001IMSE#PBF / Analog Devices | [source](https://www.mouser.com/ProductDetail/Analog-Devices/LTC7001IMSEPBF?qs=BZBei1rCqCCuiLQ%252BeMjtcQ%3D%3D) | SAME-MPN alternate sourcing: lcsc, mouser each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B083 | REF5025IDGKR | REF5025IDGKR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/REF5025IDGKR/2232441) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B084 | TLV3201AIDBVR | TLV3201AIDBVT / Texas Instruments | [source](https://www.ti.com/product/TLV3201/part-details/TLV3201AIDBVT) | UNAPPROVED procurement alternate: TI explicitly identifies DBVT and DBVR as the same device in different carrier quantities (250 / 3000), same DBV 5-pin SOT-23. Confirm distributor stock and packing; preserve exact comparator function and timing. Replaces a generic similar-comparator suggestion; not included in order totals. |
| B085 | TPS7A1601DGNR | TPS7A1601DGNT / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A1601DGNT/3046187) | UNAPPROVED: Different packing suffix candidate; verify ordering table and DGN thermal pad. No confirmed availability guarantee. |
| B086 | UCC27511DBVR | UCC27511DBVR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/UCC27511DBVR/3053304) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B087 | LT4363HMS-1#PBF | LT4363HMS-1#PBF / Analog Devices | [source](https://www.digikey.com/en/products/detail/analog-devices-inc/LT4363HMS-1-PBF/4245464) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B088 | LTC3115IFE-1#PBF | LTC3115IFE-1#PBF / Analog Devices | [source](https://www.digikey.com/en/products/detail/analog-devices-inc/LTC3115IFE-1-PBF/3074270) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B089 | TPS70933DBVR | TPS70933DBVT / Texas Instruments | [source](https://www.ti.com/product/TPS709/part-details/TPS70933DBVT) | UNAPPROVED procurement alternate: TI explicitly identifies DBVT and DBVR as the same device in different carrier quantities (250 / 3000), same DBV 5-pin SOT-23 and 30 V family. Confirm distributor stock and packing. Replaces an unqualified different-regulator suggestion; not included in order totals. |
| B090 | ADG4612BRUZ | ADG4612BRUZ / Analog Devices | [source](https://www.digikey.com/en/products/detail/analog-devices-inc/ADG4612BRUZ/2507324) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B091 | TPS3808G01DBVR | TPS3808G01DBVR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/TPS3808G01DBVR/666712?msockid=2002127634786b56294b04d135d96a9f) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B092 | TPS259470LRPWR | TPS259470LRPWR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/TPS259470LRPWR/14124014) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B093 | INA228AIDGSR | INA228AIDGST / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/INA228AIDGST/13691047) | UNAPPROVED: Same device/package family with different packing suffix; verify exact ordering table and availability. |
| B094 | TCA9517DGKR | TCA9517DGKR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/TCA9517DGKR/3926681) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B095 | TPS3808G50DBVR | TPS3808G50DBVT / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/TPS3808G50DBVR/666729) | UNAPPROVED catalog candidate (Parametric Equivalent); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B096 | SN74LVC1G74DCTR | SN74LVC1G74DCTR / Texas Instruments | [source](https://www.mouser.com/ProductDetail/Texas-Instruments/SN74LVC1G74DCTR?qs=DS7Z8uEdLNwRYlUtd5z9Zw%3D%3D) | SAME-MPN alternate sourcing: lcsc, mouser each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B097 | SN74LVC1G14DBVR | SN74LVC1G14DBVR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G14DBVR/385724?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKAJgDYwLkBOAVgoF8mg) | SAME-MPN alternate sourcing: lcsc, mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B098 | SN74LVC1G32DBVR | 74LVC1G32W5-7 / Diodes Incorporated | [source](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G32DBVR/381323) | UNAPPROVED catalog candidate (Direct); recheck package/pins, ratings, timing and application. Not in order quantities. |
| B099 | SN74LVC1G08DBVR | SN74LVC1G08DBVR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G08DBVR/385718?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLJATgDZEAWAJkQF8Gg) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| B100 | SN74LVC1G17DBVR | SN74LVC1G17DBVR / Texas Instruments | [source](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G17DBVR/389051?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKAFjGQAZkyBOAXwaA) | SAME-MPN alternate sourcing: lcsc, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| H01 | 1777989 | 0395245002 / Molex | [source](https://www.digikey.com/en/products/detail/phoenix-contact/1777989/349029?s=N4Ig7CBcoIYE5QIwA5EGYA0IYBcmZAAcBLKNAFmTQAYAmAX3qA) | UNAPPROVED catalog candidate (Similar); recheck package/pins, ratings, timing and application. Not in order quantities. |
| H05 | 3-87456-6 | 3-87456-6 / TE Connectivity | [source](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/3-87456-6/30003) | SAME-MPN backup sourcing: digikey A3044-ND; observed stock 0. Backorder/stock confirmation required; no stocked replacement established. Different component MPN remains OPEN. |
| H06 | 87309-9 | 87309-9 / TE Connectivity | [source](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/87309-9/290791) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| H07 | 8521 002100 | 8521 002100 / Belden | [source](https://www.digikey.com/en/products/detail/belden-inc/8521-002100/7389045) | SAME-MPN alternate sourcing: mouser, digikey each show sufficient stock. Use one channel; do not duplicate order quantities. No component substitution. |
| H08 | 8521 010100 | 8521 010100 / Belden | [source](https://www.digikey.com/en/products/detail/belden-inc/8521-010100/7389046) | SAME-MPN backup sourcing: digikey BEL1664-100-ND; observed stock 0. Backorder/stock confirmation required; no stocked replacement established. Different component MPN remains OPEN. |
| H09 | 8502 002100 | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |
| H10 | 8502 010100 | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. Same-MPN alternate distributor route: mouser, digikey. |
| M01 | OPEN | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |
| M02 | OPEN | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |
| M03 | OPEN | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |
| O01 | OPEN | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |
| O02 | OPEN | OPEN / OPEN | OPEN | OPEN: no qualified alternate; seek exact-part stock or engineering selection. No substitution authorized. |

## LCSC upload and validation

[BOM_ORDER_LCSC.csv](BOM_ORDER_LCSC.csv) is a **local LCSC-upload-style candidate subset**, with LCSC part number, quantity, manufacturer part number and designators. It includes only catalog-board lines with a verified SKU, published order-quantity price, known multiple, enough observed stock, no reported NRND/EOL and no unresolved exact-order code. Confirmed U316 is included when those commercial criteria pass. The other lines remain in the main CSV. Upload compatibility has not been tested against an account; no upload, cart or purchase was performed. This file is not a complete board BOM or an order authorization.

[VALIDATION.json](bom_order/VALIDATION.json) checks source coverage, uniqueness, source hash, three-board/spare arithmetic, supplier rounding, exact selected MPNs, confirmed U316 identity and inclusion, CSV/Markdown prices and exact upload membership. No ERC or DRC rerun is claimed: native KiCad files were read-only. This procurement subtask does not close R2 or advance to R3/R4/R5. Rebuild with `python3 docs/evidence/r2/bom_order/generate.py`.

Catalog facts and third-party provenance are isolated in [third_party/bom_order](../../../third_party/bom_order/README.md). The [resume review](bom_order/RESUME_REVIEW.md) records the refreshed source, supplier additions, remaining actions and evidence limits. Referenced designs/documents were not modified or copied into CAD. Validate the regenerated files with `python3 -B docs/evidence/r2/bom_order/validate.py`.
