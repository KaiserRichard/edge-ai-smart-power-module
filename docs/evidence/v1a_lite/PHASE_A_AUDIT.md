# V1A-Lite Phase A — architecture and cost audit

**KNOWN — 2026-10-04. Audit only; no design selection or implementation. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

KNOWN: this report follows `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/V1A_LITE_PHASE_A.md`. The owner has an upstream 13S (48 V nominal, 54.6 V full) → 24 V converter, outside this redesign. Lite's intended boundary is approximately 24 V auxiliary bus → fuse/TVS/reverse-polarity FET → retained LM61460 → independent output OV protection (fuse + SCR crowbar is a candidate) → Pi 5 after dummy-load tests. The target is ≤500,000 VND and hard ceiling <1,000,000 VND. Sheet 04 removal is optional. These are owner inputs, not new decisions by this audit.

Labels: **KNOWN** = observed capture, repository or dated supplier fact; **CALCULATED** = arithmetic from stated inputs; **ASSUMED** = an explicit accounting/screening convention, not an invented electrical requirement; **OPEN** = missing price/requirement or unvalidated behavior. No behavior is described as bench validated.

## a. Repository state and preservation

KNOWN: the starting worktree `/Users/quockaiser/Desktop/Research/wt-liteaudit` was clean on `docs/v1a-lite-audit`. Starting HEAD, local `feat/sheet03-output-protection` and `origin/feat/sheet03-output-protection` all equal **5f371fd7c59e90a5037004b9309bff63b0d95e71**, “Merge PR #23: order-ready BOM for 3 test boards, R203 = 24.6 kΩ”. Local `feat/v1a-pcb-layout` and its origin tracking ref equal **99292b4ff363535963fa8328c55b8c8ae8cb6c05**, “wip(r3): layout paused by owner for V1A-Lite redesign (codex-h)”. Preceding layout commits include 0276ab0, 9c8bbac and 1c4c44d. These are locally recorded refs; remote-server freshness and other worktrees' dirty status were not established.

KNOWN: the paused layout was inspected through `git log` and `git show` only. No checkout, fetch, source edit, history rewrite, purchase, login, cart or push occurred. The specific brief authorizes a commit of new evidence. Commit outcome is reported in the final handback.

KNOWN — delivery outcome: `git add -- docs/evidence/v1a_lite/PHASE_A_AUDIT.md docs/evidence/v1a_lite/PHASE_A_BOM.csv` failed before staging with `Unable to create '/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-liteaudit/index.lock': Operation not permitted`. Per the brief, both new files are left uncommitted. No commit was created and nothing was pushed; starting HEAD remains unchanged.

KNOWN: the existing `docs/FINAL_MANAGER_REPORT.md` contains dated historical gate reports. It remains unchanged because the Phase A brief forbids modifying existing documents. This audit does not close a design/validation gate or advance the paused layout. No schematic/PCB changes occurred, so new ERC/DRC runs are not applicable to this documentation-only audit.

## b. KiCad hierarchy and sheet pins

KNOWN: root `hardware/kicad/V1A.kicad_sch` contains five direct child sheets: six schematic pages total. The root contains wiring/declarations, no purchased physical references. Directions below are captured sheet-pin types, not proof of actual current or signal direction.

| Sheet | File under hardware/kicad | All sheet pins | Physical refs |
| --- | --- | --- | --- |
| 01_INPUT_PROTECTION | 01_INPUT_PROTECTION.kicad_sch | VIN_RAW (input); VIN_PROTECTED (output); BUCK_INPUT_PGOOD (output); GND (passive); VIN_FUSED (output); INPUT_SHDN (input) | 21 |
| 02_BUCK_5V | 02_BUCK_5V.kicad_sch | VIN_PROTECTED (input); BUCK_INPUT_PGOOD (input); VOUT_5V1 (output); GND (passive); BUCK_PGOOD (output); L201_IN (passive) | 31 |
| 03_OUTPUT_PROTECTION | 03_OUTPUT_PROTECTION.kicad_sch | VOUT_5V1 (input); VOUT_PROTECTED (passive); VIN_FUSED (input); GND (passive); BUCK_PGOOD (input); INPUT_SHDN (output); L201_IN (passive); VIN_PROTECTED (input) | 280 |
| 04_POWER_MONITOR | 04_POWER_MONITOR.kicad_sch | VOUT_PROTECTED (input); LOAD_5V1 (bidirectional); 3V3_HOST (input); SDA_HOST (bidirectional); SCL_HOST (bidirectional); GND (passive) | 23 |
| 05_IO_TEST | 05_IO_TEST.kicad_sch | VIN_RAW (output); VIN_PROTECTED (input); LOAD_5V1 (bidirectional); 3V3_HOST (output); SDA_HOST (bidirectional); SCL_HOST (bidirectional); GND (passive) | 11 |


KNOWN: hierarchy pins were read from the root S-expressions. All connectivity inventories below come from a fresh flattened XML netlist, including common GND, rather than assuming a sheet's port list proves its physical connections.

## c–d. BOM and cost baseline

KNOWN: [PHASE_A_BOM.csv](PHASE_A_BOM.csv) covers every captured physical reference once: **366 references = 298 catalog components + seven custom force links + 61 etched PCB features**. Rows group identical captured MPN/value within each sheet. Refdes prefixes do not imply sheet ownership: U6xx/R6xx/C7xx controls are on Sheet 03. PWR_FLAG declarations are not purchased parts.

ASSUMED accounting: **1 USD = 26,500 VND**, a planning conversion, not a retrieved market quote. “Quantity 10” means ten pieces of an MPN, not ten boards. The largest published break ≤10 supplies its unit price, multiplied by installed per-board quantity. No interpolation, spares, MOQ overbuy or three-board purchasing quantities enter the extension. Use exact-part LCSC offers where stock is positive, otherwise Mouser. If stocked LCSC has no valid ten-piece offer (e.g. MOQ 20/50/100), strict quantity-10 price remains OPEN; notes preserve the minimum-lot quote. A higher-quantity price is not extrapolated downward.

KNOWN: existing prices originate in `docs/evidence/r2/BOM_ORDER*.csv`, `bom_order/*.json` and their supporting tier ledgers `third_party/bom_order/*CATALOG_FACTS.json`. CSV rows retain the source file/evidence ID, URL, original observation date, crawl age, supplier, exact MPN, stock, MOQ/multiple and applied break. Saved 2026-10-03/04 observations are not described as freshly rechecked. Missing prices were searched on LCSC/Mouser on 2026-10-04; usable new USD observations appear in the source section. Mouser backorder prices are included when available, with stock limitations explicitly separate from price.

OPEN: every subtotal is a **known-price component subtotal**, not a complete BOM quote. Unknown prices are never zero. Etched features have zero purchased-component cost only. Custom link manufacture/fasteners, harness/mating parts, heat sinks/insulators, PCB fabrication, assembly, shipping, taxes, fixtures and the upstream converter are outside these sums. Original accessory rows H01/H05–H10/M01–M03/O01/O02 and `BOM_ACCESSORIES.csv` are not on-sheet parts; they are not double counted. A complete Lite budget must account for its actual scope of such costs.

| Sheet | Known USD/board | Known VND/board | Priced catalog groups / total | Unpriced custom links |
| --- | --- | --- | --- | --- |
| 01_INPUT_PROTECTION | 9.1337 | 242,043 | 11/16 | 1 |
| 02_BUCK_5V | 45.1633 | 1,196,827 | 10/13 | 2 |
| 03_OUTPUT_PROTECTION | 122.5651 | 3,247,975 | 52/78 | 3 |
| 04_POWER_MONITOR | 7.5659 | 200,496 | 8/10 | 0 |
| 05_IO_TEST | 0.2229 | 5,907 | 2/3 | 1 |
| TOTAL | 184.6509 | 4,893,249 | 83/120 | 7 |


CALCULATED: the target is $18.8679 and the hard ceiling is strictly below $37.7358 at the stated rate. These are old-V1A baseline costs, not a predicted Lite cost or a savings promise.

### Fifteen most expensive priced lines per board

CALCULATED: MPNs are grouped across all sheets and ranked by installed extension. Unknown lines, especially 12 × PCH1V471MCL1GS, cannot be ranked; this is the top 15 among priced lines only.

| Rank | MPN | Refs | Sheets | Qty | Supplier | USD/unit @10 | USD/board | VND/board |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C5750X7R1H226M250KB | C209, C210, C211, C212, C213, C214, C404 | 02,04 | 7 | MOUSER | 3.40 | 23.8000 | 630,700 |
| 2 | 74437636351002 | L201 | 02 | 1 | MOUSER | 21.84 | 21.8400 | 578,760 |
| 3 | WFMB2512R0330FEA | R308, R309, R310, R311, R380, R381, R382, R383, R386, R387, R388, R389, R390, R391, R392, R393 | 03 | 16 | MOUSER | 1.28 | 20.4800 | 542,720 |
| 4 | LT4363HMS-1#PBF | U316 | 03 | 1 | LCSC | 16.2348 | 16.2348 | 430,222 |
| 5 | ADG4612BRUZ | U321, U647, U651 | 03 | 3 | MOUSER | 5.01 | 15.0300 | 398,295 |
| 6 | LTC3115IFE-1#PBF | U317 | 03 | 1 | LCSC | 11.6716 | 11.6716 | 309,297 |
| 7 | LTC7001IMSE#PBF | U301 | 03 | 1 | LCSC | 8.3881 | 8.3881 | 222,285 |
| 8 | TPS7A1601DGNR | U306, U600 | 03 | 2 | MOUSER | 3.18 | 6.3600 | 168,540 |
| 9 | STPS60H100CT | D102, D330, D331 | 01,03 | 3 | LCSC | 2.028 | 6.0840 | 161,226 |
| 10 | REF5025IDGKR | U302 | 03 | 1 | MOUSER | 5.84 | 5.8400 | 154,760 |
| 11 | CSD18540Q5B | Q303, Q330 | 03 | 2 | MOUSER | 1.89 | 3.7800 | 100,170 |
| 12 | TLV3201AIDBVR | U303, U607, U640, U642 | 03 | 4 | LCSC | 0.8638 | 3.4552 | 91,563 |
| 13 | TPS26630RGER | U101 | 01 | 1 | MOUSER | 3.44 | 3.4400 | 91,160 |
| 14 | LM4040A25IDBZR | D321, D601 | 03 | 2 | LCSC | 1.7093 | 3.4186 | 90,593 |
| 15 | GRM32ER71H106KA12L | C201, C202, C305, C306, C352, C377, C601, C602, C660 | 02,03 | 9 | LCSC | 0.3322 | 2.9898 | 79,230 |


### Captured versus purchasing identities

KNOWN: several order-BOM substitutions are not captured in CAD. This audit preserves and prices the captured identity, rather than silently using an alternate's price. The Panasonic hyphen is the existing documented ordering alias, not a value/package substitution.

| Ref | Captured MPN | Existing BOM_ORDER selected MPN |
| --- | --- | --- |
| C302 | GRM21BR71E475KA73L | GRM21BZ71E475KE15L |
| C307 | GRM21BR71H105KA12L | GCM21BR71H105KA03L |
| C351 | C3216X7R1H475K160AB | C3216X7R1H475K160AC |
| C353 | GRM21BR71E475KA73L | GRM21BZ71E475KE15L |
| C358 | EEUFR1E221 | EEU-FR1E221 |
| C359 | EEUFR1E221 | EEU-FR1E221 |
| C366 | GRM21BR71E475KA73L | GRM21BZ71E475KE15L |
| C379 | GRM21BR71E475KA73L | GRM21BZ71E475KE15L |
| C403 | GRM21BR71H105KA12L | GCM21BR71H105KA03L |
| Q303 | CSD18540Q5B | CSD18540Q5BT |
| Q330 | CSD18540Q5B | CSD18540Q5BT |


### Full BOM by sheet

KNOWN/CALCULATED: all references, MPNs, quantities, suppliers, USD unit prices at quantity 10 and extensions follow. Source URLs/dates, stock and OPEN reasons are in the CSV. VND extensions use the one stated rate.

#### 01_INPUT_PROTECTION

| Refs | Captured MPN / feature | Qty | Supplier | USD unit @10 | USD extension |
| --- | --- | --- | --- | --- | --- |
| F101 | 3403.0285.23 | 1 | MOUSER | OPEN | OPEN |
| Q102 | BSS138 | 1 | MOUSER | OPEN | OPEN |
| Q101 | CSD19537Q3 | 1 | LCSC | 0.7498 | 0.7498 |
| C103 | GRM188R71H104KA93D | 1 | LCSC | OPEN | OPEN |
| C101; C102 | GRM32ER72A105KA01L | 2 | MOUSER | 0.602 | 1.204 |
| D101 | SMCJ36CA | 1 | MOUSER | 0.446 | 0.446 |
| D102 | STPS60H100CT | 1 | LCSC | 2.028 | 2.028 |
| R108 | TNPW0603100KBEEA | 1 | LCSC | 0.0797 | 0.0797 |
| R107 | TNPW060310K0BEEA | 1 | LCSC | 0.0711 | 0.0711 |
| R104 | TNPW060315K8BEEA | 1 | MOUSER | OPEN | OPEN |
| R101 | TNPW0603332KBEEA | 1 | MOUSER | 0.30 | 0.30 |
| R105 | TNPW06034K02BEEA | 1 | LCSC | 0.4061 | 0.4061 |
| R102 | TNPW060354K9BEEA | 1 | MOUSER | 0.149 | 0.149 |
| R106 | TNPW060356K2BEEA | 1 | MOUSER | 0.26 | 0.26 |
| R103 | TNPW0805348KBEEA | 1 | MOUSER / OPEN | OPEN | OPEN |
| U101 | TPS26630RGER | 1 | MOUSER | 3.44 | 3.44 |
| JP101 | CUSTOM-FX-CU-01 RevA | 1 | N/A | OPEN | OPEN |
| TP101; TP102 | N/A etched copper | 2 | N/A | 0 | 0 |
| TP103 | N/A etched copper | 1 | N/A | 0 | 0 |

#### 02_BUCK_5V

| Refs | Captured MPN / feature | Qty | Supplier | USD unit @10 | USD extension |
| --- | --- | --- | --- | --- | --- |
| L201 | 74437636351002 | 1 | MOUSER | 21.84 | 21.84 |
| C209; C210; C211; C212; C213; C214 | C5750X7R1H226M250KB | 6 | MOUSER | 3.40 | 20.40 |
| C207 | CGA3E2C0G1H220J080AA | 1 | MOUSER | 0.058 | 0.058 |
| R204 | CRCW06030000Z0EA | 1 | MOUSER | OPEN | OPEN |
| C203; C204; C205 | GRM188R71H104KA93D | 3 | LCSC | OPEN | OPEN |
| C206 | GRM21BR71E105KA99L | 1 | LCSC | 0.0586 | 0.0586 |
| C201; C202 | GRM32ER71H106KA12L | 2 | LCSC | 0.3322 | 0.6644 |
| U201 | LM61460AANRJRR | 1 | LCSC | 1.5995 | 1.5995 |
| R202; R206 | TNPW0603100KBEEA | 2 | LCSC | 0.0797 | 0.1594 |
| R205 | TNPW06031K00BEEA | 1 | LCSC | OPEN | OPEN |
| R203 | TNPW060324K6BEEA | 1 | MOUSER | 0.20 | 0.20 |
| R207 | TNPW060324K9BEEA | 1 | LCSC | 0.0833 | 0.0833 |
| R201 | TNPW060333K2BEEA | 1 | LCSC | 0.1001 | 0.1001 |
| JP201; JP202 | CUSTOM-FX-CU-01 RevA | 2 | N/A | OPEN | OPEN |
| PF2; PF3; PF4 | CUSTOM-FX-PAD-M4 RevA | 3 | N/A | 0 | 0 |
| TP201; TP202; TP203; TP204 | N/A etched copper | 4 | N/A | 0 | 0 |

#### 03_OUTPUT_PROTECTION

| Refs | Captured MPN / feature | Qty | Supplier | USD unit @10 | USD extension |
| --- | --- | --- | --- | --- | --- |
| Q304 | 2N7002,215 | 1 | LCSC | OPEN | OPEN |
| L301 | 7447789004 | 1 | MOUSER | 1.70 | 1.70 |
| U321; U647; U651 | ADG4612BRUZ | 3 | MOUSER | 5.01 | 15.03 |
| D304; D600; D660 | B260-13-F | 3 | LCSC | 0.1286 | 0.3858 |
| J301 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| J606 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| JP600 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| J302 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| J605 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| J604 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| JP660 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| J603 | B2B-XH-A(LF)(SN) | 1 | LCSC | OPEN | OPEN |
| D301; D302; D322; D618; D619; D640; D641; D642; D643 | BAS116,215 | 9 | LCSC | OPEN | OPEN |
| D303 | BAT46W-E3-08 | 1 | LCSC | 0.1671 | 0.1671 |
| Q301; Q302 | BSC034N06NSATMA1 | 2 | LCSC | 0.8783 | 1.7566 |
| C356 | C1608C0G1H102J080AA | 1 | MOUSER | 0.058 | 0.058 |
| C350; C603 | C1608C0G1H103J080AA | 2 | MOUSER | 0.099 | 0.198 |
| C351 | C3216X7R1H475K160AB | 1 | MOUSER / OPEN | OPEN | OPEN |
| R374 | CRCW0603100RFKEA | 1 | LCSC | OPEN | OPEN |
| R333 | CRCW060310R0FKEA | 1 | LCSC | 0.0046 | 0.0046 |
| R306; R384 | CRCW06031R00FKEA | 2 | MOUSER | 0.025 | 0.050 |
| R323 | CRCW120610K0FKEA | 1 | MOUSER | 0.034 | 0.034 |
| Q303; Q330 | CSD18540Q5B | 2 | MOUSER | 1.89 | 3.78 |
| C358; C359 | EEUFR1E221 | 2 | MOUSER | 0.451 | 0.902 |
| Q316 | FDB33N25TM | 1 | LCSC | 1.3643 | 1.3643 |
| C357 | GRM1885C1H330JA01D | 1 | LCSC | OPEN | OPEN |
| C303; C304; C308; C354; C355; C364; C368; C369; C370; C376; C380; C604; C609; C640; C642; C644; C647; C651; C710; C711; C712; C714; C715; C716; C717; C723; C728; C730; C731; C732; C733; C754; C756; C761; C762 | GRM188R71H104KA93D | 35 | LCSC | OPEN | OPEN |
| C301; C309; C365; C367; C374; C375; C600 | GRM21BR71E105KA99L | 7 | LCSC | 0.0586 | 0.4102 |
| C302; C353; C366; C379 | GRM21BR71E475KA73L | 4 | LCSC | 0.1365 | 0.5460 |
| C307 | GRM21BR71H105KA12L | 1 | LCSC | 0.0425 | 0.0425 |
| C305; C306; C352; C377; C601; C602; C660 | GRM32ER71H106KA12L | 7 | LCSC | 0.3322 | 2.3254 |
| C378 | GRM32ER72A105KA01L | 1 | MOUSER | 0.602 | 0.602 |
| D321; D601 | LM4040A25IDBZR | 2 | LCSC | 1.7093 | 3.4186 |
| U316 | LT4363HMS-1#PBF | 1 | LCSC | 16.2348 | 16.2348 |
| U317 | LTC3115IFE-1#PBF | 1 | LCSC | 11.6716 | 11.6716 |
| U301 | LTC7001IMSE#PBF | 1 | LCSC | 8.3881 | 8.3881 |
| C330; C331; C332; C333; C334; C335; C336; C337; C340; C341; C342; C343 | PCH1V471MCL1GS | 12 | MOUSER / OPEN | OPEN | OPEN |
| U302 | REF5025IDGKR | 1 | MOUSER | 5.84 | 5.84 |
| U617; U623; U628; U630; U631; U632; U633 | SN74LVC1G08DBVR | 7 | LCSC | 0.047 | 0.329 |
| U614; U616; U644; U654; U656; U661 | SN74LVC1G14DBVR | 6 | LCSC | 0.0655 | 0.3930 |
| U662 | SN74LVC1G17DBVR | 1 | LCSC | 0.1696 | 0.1696 |
| U615 | SN74LVC1G32DBVR | 1 | LCSC | 0.0714 | 0.0714 |
| U610; U611; U612 | SN74LVC1G74DCTR | 3 | LCSC | 0.6717 | 2.0151 |
| D330; D331 | STPS60H100CT | 2 | LCSC | 2.028 | 4.056 |
| U303; U607; U640; U642 | TLV3201AIDBVR | 4 | LCSC | 0.8638 | 3.4552 |
| R321; R322; R330; R346; R364; R367; R605; R606; R609; R623; R650; R651; R652; R718 | TNPW0603100KBEEA | 14 | LCSC | 0.0797 | 1.1158 |
| R304 | TNPW0603100RBEEA | 1 | MOUSER | 0.174 | 0.174 |
| R302; R307; R313; R316; R317; R363; R365; R370; R371; R372; R385; R601; R603; R604; R645; R648; R707; R708; R710; R713; R723; R727; R728; R729 | TNPW060310K0BEEA | 24 | LCSC | 0.0711 | 1.7064 |
| R711 | TNPW0603143KBEEA | 1 | MOUSER | OPEN | OPEN |
| R343; R344 | TNPW060315K0BEEA | 2 | MOUSER | OPEN | OPEN |
| R303; R373; R622; R647; R649; R709; R712; R717; R730; R731 | TNPW06031K00BEEA | 10 | LCSC | OPEN | OPEN |
| R640; R642 | TNPW060320K0BEEA | 2 | MOUSER | 0.26 | 0.52 |
| R342 | TNPW060323K7BEEA | 1 | MOUSER | 0.25 | 0.25 |
| R362 | TNPW0603249KBEEA | 1 | MOUSER | 0.261 | 0.261 |
| R312; R600 | TNPW060332K4BEEA | 2 | MOUSER / OPEN | OPEN | OPEN |
| R379 | TNPW060333K2BEEA | 1 | LCSC | 0.1001 | 0.1001 |
| R602 | TNPW060347R0BEEA | 1 | MOUSER | 0.554 | 0.554 |
| R377 | TNPW060348K7BEEA | 1 | MOUSER | 0.192 | 0.192 |
| R644 | TNPW060349K9BEEA | 1 | MOUSER | 0.26 | 0.26 |
| R331 | TNPW06034K32BEEA | 1 | MOUSER | OPEN | OPEN |
| R361 | TNPW060368K1BEEA | 1 | MOUSER | OPEN | OPEN |
| R641 | TNPW06036K19BEEA | 1 | MOUSER | OPEN | OPEN |
| R375 | TNPW06036K49BEEA | 1 | MOUSER | OPEN | OPEN |
| R341 | TNPW060388K7BEEA | 1 | MOUSER | 0.192 | 0.192 |
| R301 | TNPW06039K88BEEA | 1 | MOUSER | OPEN | OPEN |
| R340 | TNPW08051M00BEEA | 1 | LCSC | 0.252 | 0.252 |
| R376; R378 | TNPW0805365KBEEA | 2 | MOUSER | OPEN | OPEN |
| R345 | TNPW0805383KBEEA | 1 | MOUSER | OPEN | OPEN |
| R305 | TNPW12062M00BEEA | 1 | LCSC | 0.1661 | 0.1661 |
| U327 | TPS259470LRPWR | 1 | LCSC | 1.2039 | 1.2039 |
| U322; U323 | TPS3808G01DBVR | 2 | LCSC | 0.4142 | 0.8284 |
| U602 | TPS3808G50DBVR | 1 | LCSC | 0.9024 | 0.9024 |
| U318 | TPS70933DBVR | 1 | LCSC | 0.3379 | 0.3379 |
| U306; U600 | TPS7A1601DGNR | 2 | MOUSER | 3.18 | 6.36 |
| U315; U330 | UCC27511DBVR | 2 | LCSC | 0.4911 | 0.9822 |
| R308; R309; R310; R311 | WFMB2512R0330FEA | 4 | MOUSER | 1.28 | 5.12 |
| R380; R381; R382; R383; R386; R387; R388; R389; R390; R391; R392; R393 | WFMB2512R0330FEA | 12 | MOUSER | 1.28 | 15.36 |
| R332 | WSL2512R3300FEA | 1 | LCSC | 0.328 | 0.328 |
| JP301; JP330; JP331 | CUSTOM-FX-CU-01 RevA | 3 | N/A | OPEN | OPEN |
| TP301; TP302; TP303; TP304; TP305 | N/A etched copper | 5 | N/A | 0 | 0 |
| TP306; TP307; TP308; TP309; TP310; TP311; TP312; TP313; TP314; TP315; TP316; TP317; TP318; TP319; TP320; TP321; TP322; TP323; TP324; TP327; TP328; TP329; TP330; TP331; TP332; TP333; TP334; TP335; TP336; TP337; TP338; TP339; TP340 | N/A etched copper | 33 | N/A | 0 | 0 |

#### 04_POWER_MONITOR

| Refs | Captured MPN / feature | Qty | Supplier | USD unit @10 | USD extension |
| --- | --- | --- | --- | --- | --- |
| C404 | C5750X7R1H226M250KB | 1 | MOUSER | 3.40 | 3.40 |
| C401; C402; C405; C406 | GRM188R71H104KA93D | 4 | LCSC | OPEN | OPEN |
| C403 | GRM21BR71H105KA12L | 1 | LCSC | 0.0425 | 0.0425 |
| U401 | INA228AIDGSR | 1 | MOUSER / OPEN | OPEN | OPEN |
| U403 | TCA9517DGKR | 1 | LCSC | 0.7842 | 0.7842 |
| R404; R405; R408 | TNPW060310K0BEEA | 3 | LCSC | 0.0711 | 0.2133 |
| R402; R403 | TNPW060310R0BEEA | 2 | MOUSER | 0.259 | 0.518 |
| R406; R407 | TNPW06034K70BEEA | 2 | MOUSER | 0.26 | 0.52 |
| U402 | TPS70933DBVR | 1 | LCSC | 0.3379 | 0.3379 |
| R401 | WSL27262L000FEA | 1 | MOUSER | 1.75 | 1.75 |
| TP401; TP402; TP403; TP404 | N/A etched copper | 4 | N/A | 0 | 0 |
| TP405; TP406 | N/A etched copper | 2 | N/A | 0 | 0 |

#### 05_IO_TEST

| Refs | Captured MPN / feature | Qty | Supplier | USD unit @10 | USD extension |
| --- | --- | --- | --- | --- | --- |
| J502 | 1776508 | 1 | MOUSER | OPEN | OPEN |
| J501 | B2P-VH-FB-B(LF)(SN) | 1 | LCSC | 0.1607 | 0.1607 |
| J503 | B4B-XH-A(LF)(SN) | 1 | LCSC | 0.0622 | 0.0622 |
| JP501 | CUSTOM-FX-CU-01 RevA | 1 | N/A | OPEN | OPEN |
| PF1; PF5 | CUSTOM-FX-PAD-M4 RevA | 2 | N/A | 0 | 0 |
| TP501; TP502; TP503; TP504 | N/A etched copper | 4 | N/A | 0 | 0 |
| TP505 | N/A etched copper | 1 | N/A | 0 | 0 |


## e. Sheet 04 complete external net/pin boundary

KNOWN: exactly six nets connect Sheet 04 to other sheets: **VOUT_PROTECTED, LOAD_5V1, 3V3_HOST, SDA_HOST, SCL_HOST and GND**. The following lists every connected physical pin by sheet, including common ground. Hierarchical pins appear in section b.

### /3V3_HOST

| Sheet | Every physical pin on this net |
| --- | --- |
| 04_POWER_MONITOR | C405.1 (1), R406.1 (1), R407.1 (1), U403.1 (VCCA) |
| 05_IO_TEST | J503.2 (VREF) |

### /GND

| Sheet | Every physical pin on this net |
| --- | --- |
| 01_INPUT_PROTECTION | C101.2 (2), C102.2 (2), C103.2 (2), D101.2 (2), D102.1 (A1), D102.3 (A2), R102.2 (2), R104.2 (2), R105.2 (2), R107.2 (2), TP103.2 (RETURN), U101.8 (GND), U101.25 (EP) |
| 02_BUCK_5V | C201.2 (2), C202.2 (2), C203.2 (2), C204.2 (2), C206.2 (2), C209.2 (2), C210.2 (2), C211.2 (2), C212.2 (2), C213.2 (2), C214.2 (2), R201.2 (2), R203.2 (2), R207.2 (2), TP201.2 (RETURN), TP202.2 (RETURN), TP203.2 (RETURN), TP204.2 (RETURN), U201.1 (BIAS), U201.3 (AGND), U201.9 (PGND1), U201.11 (PGND2) |
| 03_OUTPUT_PROTECTION | C302.2 (-_/_2), C303.2 (-_/_2), C304.2 (-_/_2), C305.2 (-_/_2), C306.2 (-_/_2), C307.2 (-_/_2), C308.2 (-_/_2), C309.2 (-_/_2), C330.2 (-), C331.2 (-), C332.2 (-), C333.2 (-), C334.2 (-), C335.2 (-), C336.2 (-), C337.2 (-), C340.2 (-), C341.2 (-), C342.2 (-), C343.2 (-), C350.2 (2), C351.2 (2), C352.2 (2), C353.2 (2), C358.2 (-), C359.2 (-), C364.2 (2), C365.2 (2), C366.2 (2), C367.2 (2), C368.2 (2), C369.2 (2), C370.2 (2), C374.2 (2), C375.2 (2), C376.2 (2), C377.2 (2), C378.2 (2), C379.2 (2), C380.2 (2), C600.2 (2), C601.2 (2), C602.2 (2), C603.2 (2), C604.2 (2), C609.2 (2), C640.2 (2), C642.2 (2), C644.2 (2), C647.2 (2), C651.2 (2), C660.2 (2), C710.2 (2), C711.2 (2), C712.2 (2), C714.2 (2), C715.2 (2), C716.2 (2), C717.2 (2), C723.2 (2), C728.2 (2), C730.2 (2), C731.2 (2), C732.2 (2), C733.2 (2), C754.2 (2), C756.2 (2), C761.2 (2), C762.2 (2), D321.2 (A), D321.3 (NC_GND), D322.1 (A), D330.1 (A1), D330.3 (A2), D331.1 (A1), D331.3 (A2), D601.2 (A), D601.3 (NC_GND), D619.1 (A), D641.1 (A), D643.1 (A), J301.2 (RETURN), J302.2 (RETURN), J603.2 (RETURN), J604.2 (RETURN), J605.2 (RETURN), J606.2 (RETURN), Q303.1 (S), Q303.2 (S), Q303.3 (S), Q304.2 (S), Q330.1 (S), Q330.2 (S), Q330.3 (S), R302.2 (2), R307.2 (2), R313.2 (2), R321.2 (2), R322.2 (2), R323.2 (2), R331.2 (2), R341.2 (2), R342.2 (2), R346.2 (2), R363.2 (2), R365.2 (2), R367.2 (2), R370.2 (2), R375.2 (2), R377.2 (2), R379.2 (2), R385.2 (2), R601.2 (2), R603.2 (2), R606.2 (2), R623.2 (2), R641.2 (2), R645.2 (2), R648.2 (2), R650.2 (2), R651.2 (2), R652.2 (2), R710.2 (2), R711.2 (2), R713.2 (2), R718.2 (2), R723.2 (2), R729.2 (2), TP306.2 (RETURN), TP307.2 (RETURN), TP308.2 (RETURN), TP309.2 (RETURN), TP310.2 (RETURN), TP311.2 (RETURN), TP312.2 (RETURN), TP313.2 (RETURN), TP315.2 (RETURN), TP316.2 (RETURN), TP317.2 (RETURN), TP318.2 (RETURN), TP319.2 (RETURN), TP320.2 (RETURN), TP321.2 (RETURN), TP322.2 (RETURN), TP323.2 (RETURN), TP324.2 (RETURN), TP327.2 (RETURN), TP328.2 (RETURN), TP329.2 (RETURN), TP330.2 (RETURN), TP331.2 (RETURN), TP332.2 (RETURN), TP333.2 (RETURN), TP337.2 (RETURN), TP338.2 (RETURN), TP339.2 (RETURN), TP340.2 (RETURN), U301.3 (GND), U301.5 (OVLO), U301.11 (EP), U302.4 (GND), U303.2 (GND), U306.4 (GND), U306.9 (EP), U315.4 (GND), U315.5 (IN-), U316.7 (GND), U316.9 (GND), U317.1 (PGND), U317.5 (GND), U317.6 (GND), U317.10 (PGND), U317.11 (PGND), U317.19 (PWM_SYNC), U317.20 (PGND), U317.21 (EP_PGND), U318.2 (GND), U321.4 (VSS), U321.5 (GND), U321.6 (S4), U321.7 (D4), U321.8 (IN4), U321.9 (IN3), U321.10 (D3), U321.11 (S3), U321.14 (S2), U321.15 (D2), U321.16 (IN2), U322.2 (GND), U323.2 (GND), U327.8 (GND), U330.4 (GND), U330.5 (IN-), U600.4 (GND), U600.9 (EP), U602.2 (GND), U607.2 (GND), U610.4 (GND), U611.4 (GND), U612.4 (GND), U614.3 (GND), U615.3 (GND), U616.3 (GND), U617.3 (GND), U623.3 (GND), U628.3 (GND), U630.3 (GND), U631.3 (GND), U632.3 (GND), U633.3 (GND), U640.2 (GND), U642.2 (GND), U644.3 (GND), U647.4 (VSS), U647.5 (GND), U647.6 (S4), U647.7 (D4), U647.8 (IN4), U647.9 (IN3), U647.10 (D3), U647.11 (S3), U651.4 (VSS), U651.5 (GND), U651.6 (S4), U651.7 (D4), U651.8 (IN4), U651.9 (IN3), U651.10 (D3), U651.11 (S3), U651.14 (S2), U651.15 (D2), U651.16 (IN2), U654.3 (GND), U656.3 (GND), U661.3 (GND), U662.3 (GND) |
| 04_POWER_MONITOR | C402.2 (2), C403.2 (2), C404.2 (2), C405.2 (2), C406.2 (2), TP405.2 (RETURN), TP406.2 (RETURN), U401.1 (A1), U401.2 (A0), U401.7 (GND), U402.2 (GND), U403.4 (GND) |
| 05_IO_TEST | J501.2 (RETURN), J502.2 (RETURN), J503.1 (GND), PF5.1 (FORCE), TP504.1 (TP), TP505.2 (RETURN) |

### /LOAD_5V1

| Sheet | Every physical pin on this net |
| --- | --- |
| 04_POWER_MONITOR | R401.4 (I-), TP406.1 (SIGNAL), U401.8 (VBUS) |
| 05_IO_TEST | J502.1 (+), JP501.1 (FORCE_A), TP503.1 (TP) |

### /SCL_HOST

| Sheet | Every physical pin on this net |
| --- | --- |
| 04_POWER_MONITOR | R407.2 (2), U403.2 (SCLA) |
| 05_IO_TEST | J503.4 (SCL) |

### /SDA_HOST

| Sheet | Every physical pin on this net |
| --- | --- |
| 04_POWER_MONITOR | R406.2 (2), U403.3 (SDAA) |
| 05_IO_TEST | J503.3 (SDA) |

### /VOUT_PROTECTED

| Sheet | Every physical pin on this net |
| --- | --- |
| 03_OUTPUT_PROTECTION | C340.1 (+), C341.1 (+), C342.1 (+), C343.1 (+), D331.2 (K_TAB), JP301.2 (FORCE_B), R308.1 (1), R310.1 (1), TP302.1 (TP) |
| 04_POWER_MONITOR | C403.1 (1), R401.1 (I+), TP405.1 (SIGNAL), U402.1 (IN) |


KNOWN: R401 force terminals 1 (VOUT_PROTECTED) and 4 (LOAD_5V1) form the series load-current path. Kelvin terminals 2/3 feed R402/R403 then U401.10/.9. U401.8 senses the load side; U402.1 powers the local regulator from the pre-shunt side. Deleting Sheet 04 alone leaves **J502.1, JP501.1 and TP503.1 without the captured power connection**. A replacement power-path definition is OPEN in Phase B, not implemented here.

KNOWN: J503.2 supplies 3V3_HOST. Sheet 04 R406/R407 provide host SDA/SCL pullups; U403 bridges host and local I2C. Removing Sheet 04 removes those pullups and the bridge, not only INA228. J503.1 stays on GND; its other three nets then have no on-board endpoint outside Sheet 05. U403.5 EN is local 3V3, not an off-sheet control. ALERT_LOCAL connects only U401.3/R408/TP401 on Sheet 04: no hidden external alert exists.

KNOWN: all private Sheet 04 nets, including intentional NCs, follow. They have no physical endpoint on another sheet.

| Private net | Pins |
| --- | --- |
| /04_POWER_MONITOR/3V3_LOCAL | C402.1 (1), C404.1 (1), C406.1 (1), R404.1 (1), R405.1 (1), R408.1 (1), TP404.1 (TP), U401.6 (VS), U402.5 (OUT), U403.5 (EN), U403.8 (VCCB) |
| /04_POWER_MONITOR/ALERT_LOCAL | R408.2 (2), TP401.1 (TP), U401.3 (ALERT) |
| /04_POWER_MONITOR/INA_IN_MINUS | C401.2 (2), R403.2 (2), U401.9 (IN-) |
| /04_POWER_MONITOR/INA_IN_PLUS | C401.1 (1), R402.2 (2), U401.10 (IN+) |
| /04_POWER_MONITOR/SCL_LOCAL | R405.2 (2), U401.5 (SCL), U403.7 (SCLB) |
| /04_POWER_MONITOR/SDA_LOCAL | R404.2 (2), U401.4 (SDA), U403.6 (SDAB) |
| /04_POWER_MONITOR/SHUNT_KMINUS | R401.3 (S-), R403.1 (1), TP403.1 (TP) |
| /04_POWER_MONITOR/SHUNT_KPLUS | R401.2 (S+), R402.1 (1), TP402.1 (TP) |
| unconnected-(U402-EN-Pad3) | U402.3 (EN) |
| unconnected-(U402-NC-Pad4) | U402.4 (NC) |


CALCULATED: the captured 2 mΩ shunt contributes nominal 10 mV drop and 0.05 W dissipation at 5 A. Removing it changes the old path-budget arithmetic; these figures are not measurement-accuracy or thermal-validation evidence.

## f. Sheet 03 control and cross-sheet dependencies

KNOWN: all eight cross-sheet nets appear below. There is **no direct Sheet 05 control input** to Sheet 03: ARM, RESET, SOURCE FAULT, SERIES ARM, the manual-valid link and guarded outputs physically reside on Sheet 03. Sheet 05 shares power/GND; VIN_RAW reaches Sheet 03 through Sheet 01 F101/VIN_FUSED.

### /BUCK_PGOOD

| Sheet | Every physical pin on this net |
| --- | --- |
| 02_BUCK_5V | U201.5 (PGOOD) |
| 03_OUTPUT_PROTECTION | R317.2 (2), R622.1 (1), TP317.1 (SIGNAL) |

KNOWN: `/GND` connects all five sheets; its full pin list is in section e.

### /INPUT_SHDN

| Sheet | Every physical pin on this net |
| --- | --- |
| 01_INPUT_PROTECTION | TP101.1 (TP), U101.12 (SHDN) |
| 03_OUTPUT_PROTECTION | Q304.3 (D), R647.2 (2), R648.1 (1), TP312.1 (SIGNAL) |

### /L201_IN

| Sheet | Every physical pin on this net |
| --- | --- |
| 02_BUCK_5V | JP201.2 (FORCE_B), L201.1 (1), PF4.1 (FORCE), TP202.1 (SIGNAL) |
| 03_OUTPUT_PROTECTION | R640.1 (1) |

### /VIN_FUSED

| Sheet | Every physical pin on this net |
| --- | --- |
| 01_INPUT_PROTECTION | C101.1 (1), D101.1 (1), F101.2 (2), Q101.1 (S), Q101.2 (S), Q101.3 (S), Q102.2 (S), R101.1 (1), R103.1 (1), U101.5 (IN_SYS) |
| 03_OUTPUT_PROTECTION | D303.1 (A) |

### /VIN_PROTECTED

| Sheet | Every physical pin on this net |
| --- | --- |
| 01_INPUT_PROTECTION | D102.2 (K_TAB), JP101.2 (FORCE_B), R106.1 (1), R108.1 (1) |
| 02_BUCK_5V | C201.1 (1), C202.1 (1), C203.1 (1), C204.1 (1), PF2.1 (FORCE), R206.1 (1), U201.8 (VIN1), U201.12 (VIN2) |
| 03_OUTPUT_PROTECTION | R644.1 (1) |
| 05_IO_TEST | TP502.1 (TP) |

### /VOUT_5V1

| Sheet | Every physical pin on this net |
| --- | --- |
| 02_BUCK_5V | C207.1 (1), C209.1 (1), C210.1 (1), C211.1 (1), C212.1 (1), C213.1 (1), C214.1 (1), JP202.2 (FORCE_B), R202.1 (1), TP203.1 (SIGNAL) |
| 03_OUTPUT_PROTECTION | C330.1 (+), C331.1 (+), C332.1 (+), C333.1 (+), C334.1 (+), C335.1 (+), C336.1 (+), C337.1 (+), D330.2 (K_TAB), Q301.5 (D), Q301.6 (D), Q301.7 (D), Q301.8 (D), R301.1 (1), R380.1 (1), R388.1 (1), TP301.1 (TP) |

### /VOUT_PROTECTED

| Sheet | Every physical pin on this net |
| --- | --- |
| 03_OUTPUT_PROTECTION | C340.1 (+), C341.1 (+), C342.1 (+), C343.1 (+), D331.2 (K_TAB), JP301.2 (FORCE_B), R308.1 (1), R310.1 (1), TP302.1 (TP) |
| 04_POWER_MONITOR | C403.1 (1), R401.1 (I+), TP405.1 (SIGNAL), U402.1 (IN) |


KNOWN: VIN_FUSED → D303 → AUX_RAW supplies the auxiliary chain: U316/Q316 surge stage → U317/L350 buck-boost → U327 hold rail → DRV_HOLD. U306 DET5, U318 3V3_AUX and U600 SAFE5 support sensing, drivers and logic. This branches before TPS26630 but shares F101 and its upstream source. It does not depend on Sheet 04's local 3V3. VOUT_5V1 feeds the series protection and OV divider; VOUT_PROTECTED exits toward Sheet 04.

KNOWN: the captured output block uses Q301/Q302 opposed series MOSFETs with U301 LTC7001, plus Q303 and Q330 MOSFET disposal branches driven by U315/U330 UCC27511 and ballast banks. It is not the owner's candidate fuse/SCR circuit. The existing source shutdown, stored-energy discharge and auxiliary-supply functions therefore cannot be assumed present in a simplified SCR implementation.

KNOWN: BUCK_PGOOD comes from U201.5. Its pullup R317 to 3V3_AUX is on Sheet 03. R622 → U651 guarded analog switch → PG_SENSE/R623/C651 → U607 comparator produces PG_GOOD. U631 combines MAIN_PERMISSION and PG_GOOD into SERIES_CLEAR_N; U611/U632 produce the series-run logic. Removing Sheet 03 also removes the buck PGOOD pullup.

KNOWN: VIN_PROTECTED → R644/R645 → VIN_MON → U647 channel 2 → VIN_SENSE/R652/C642 → U642 produces VIN_GOOD_FAST. L201_IN → R640/R641/R642 → SW_HYS → U647 channel 1 → SW_SENSE/R651/C640 → U640 produces SW_HIGH. In this capture these are observation/test outputs, not autonomous source-fault triggers: SRC_TRIP comes from J603 SOURCE_CONTACT through U644. The manual fixture must not be described as automatic fault protection.

KNOWN: J301/U654 MAIN ARM and JP600 MANUAL_RAILS_VALID participate in U612/U623/U630 MAIN_PERMISSION. R647 drives INPUT_SHDN, R648 pulls it down, and Q304 pulls it down on FAULT_DRIVE via R649/R650. J302/U656 and U610 reset/hold the fault state. J604/U661 separately arms U611 series logic. J605 PG_FIXTURE and J606 MAIN_FIXTURE are resistor-isolated observation outputs.

## g. TPS26630 dependencies in Sheets 02/03/05

KNOWN: the complete U101 pin table follows, including NCs. BUCK_INPUT_PGOOD (input eFuse) and BUCK_PGOOD (buck output) are distinct nets. INPUT_FLT and the Sheet 03 FAULT/HOLD_FLT signals are also distinct.

| U101 pin | Function | Captured net |
| --- | --- | --- |
| 1 | IN | /01_INPUT_PROTECTION/VIN_EFUSE_IN |
| 2 | IN | /01_INPUT_PROTECTION/VIN_EFUSE_IN |
| 3 | B_GATE | /01_INPUT_PROTECTION/INPUT_BGATE |
| 4 | DRV | /01_INPUT_PROTECTION/INPUT_DRV |
| 5 | IN_SYS | /VIN_FUSED |
| 6 | UVLO | /01_INPUT_PROTECTION/INPUT_UVLO |
| 7 | OVP | /01_INPUT_PROTECTION/INPUT_OVP |
| 8 | GND | /GND |
| 9 | dVdT | /01_INPUT_PROTECTION/INPUT_DVDT |
| 10 | ILIM | /01_INPUT_PROTECTION/INPUT_ILIM |
| 11 | MODE | unconnected-(U101-MODE-Pad11) |
| 12 | SHDN | /INPUT_SHDN |
| 13 | IMON | unconnected-(U101-IMON-Pad13) |
| 14 | FLT | /01_INPUT_PROTECTION/INPUT_FLT |
| 15 | PGTH | /01_INPUT_PROTECTION/INPUT_PGTH |
| 16 | PGOOD | /BUCK_INPUT_PGOOD |
| 17 | OUT | /01_INPUT_PROTECTION/EFUSE_OUT |
| 18 | OUT | /01_INPUT_PROTECTION/EFUSE_OUT |
| 19 | NC | unconnected-(U101-NC-Pad19) |
| 20 | NC | unconnected-(U101-NC-Pad20) |
| 21 | NC | unconnected-(U101-NC-Pad21) |
| 22 | NC | unconnected-(U101-NC-Pad22) |
| 23 | NC | unconnected-(U101-NC-Pad23) |
| 24 | NC | unconnected-(U101-NC-Pad24) |
| 25 | EP | /GND |


| Dependency | KNOWN capture | OPEN consequence of removing TPS26630 |
| --- | --- | --- |
| Direct buck enable | U101.16 → BUCK_INPUT_PGOOD → U201.7 EN/SYNC, R206.2, R207.1. R206.1 connects VIN_PROTECTED; R207.2 GND. | U101's gating action disappears. R206/R207 alone would form a VIN-dependent EN divider; replacement enable/UVLO behavior is not established. |
| Main supply | U101.17/.18 EFUSE_OUT → JP101 → VIN_PROTECTED → U201.8/.12, C201–C204, R206; Sheet 03 R644; Sheet 05 TP502. | Controlled ramp, cutoff, current limiting and latch-off assumptions disappear; downstream startup/fault models need a new source contract. |
| Shutdown loop | U630 MAIN_PERMISSION → R647 → INPUT_SHDN/U101.12; R648 pull-down; Q304 FAULT pull-down; TP312 and Sheet 01 TP101. | The loop no longer disconnects the main source; fuse/SCR coordination is unestablished. |
| Input PGOOD threshold | Sheet 01 R106/R107 → INPUT_PGTH/U101.15 observes VIN_PROTECTED. | That hardware qualification no longer gates the buck. |
| UVLO / OVP | R101/R102 INPUT_UVLO/U101.6 and R103/R104 INPUT_OVP/U101.7 stay local to Sheet 01. | No direct UVLO/OVP control net exists on Sheets 02/03/05. Effects propagate through supply and BUCK_INPUT_PGOOD. |
| Input limit / ramp | R105 INPUT_ILIM/U101.10; C103 INPUT_DVDT/U101.9, local to Sheet 01. | No exported current-limit command exists. Old pulse, inrush and crowbar current models cannot be inherited. |
| Input fault | U101.14 INPUT_FLT connects R108 (pullup from VIN_PROTECTED) and TP102 only, on Sheet 01. | No INPUT_FLT endpoint exists on Sheets 02/03/05. |
| Reverse-FET control | U101.3 INPUT_BGATE and .4 INPUT_DRV support Sheet 01 Q101/Q102. | Q101/Q102 do not remain a complete stand-alone reverse-polarity block without their controller. |
| IMON / mode | U101.13 IMON and .11 MODE are intentional NC. | No input-current telemetry signal leaves U101; old MODE-dependent latch/retry behavior needs reconsideration. |
| Series permission | eFuse power/enable → U201 BUCK_PGOOD → R317/R622/U651/U607/U631/U611/U632. | Revised source/startup behavior changes PG timing and downstream series sequencing. |
| Rail/switch observations | R644 VIN_PROTECTED and R640 L201_IN feed U642/U640 through the networks in section f. | New transient scale/source behavior changes fixture interpretation. |
| Sheet 05 | TP502 observes VIN_PROTECTED; J501/TP501/PF1 are upstream; J502/TP503/JP501 are downstream. | No direct PGOOD, UVLO, ILIM, SHDN or FLT pin exists on Sheet 05; supply/fault-isolation and load-test procedures still change. |

KNOWN: the pin-level downstream dependency ledger follows for traceability; it does not model temporal behavior.

| Ref | Value | All physical pins → net |
| --- | --- | --- |
| R206 | 100k | 1 1 → /VIN_PROTECTED; 2 2 → /BUCK_INPUT_PGOOD |
| R207 | 24.9k | 1 1 → /BUCK_INPUT_PGOOD; 2 2 → /GND |
| R317 | 10k | 1 1 → /03_OUTPUT_PROTECTION/3V3_AUX; 2 2 → /BUCK_PGOOD |
| R622 | 1k | 1 1 → /BUCK_PGOOD; 2 2 → /03_OUTPUT_PROTECTION/PG_DIV |
| R623 | 100k | 1 1 → /03_OUTPUT_PROTECTION/PG_SENSE; 2 2 → /GND |
| U651 | ADG4612BRUZ | 1 IN1 → /03_OUTPUT_PROTECTION/SAFE5; 2 D1 → /03_OUTPUT_PROTECTION/PG_DIV; 3 S1 → /03_OUTPUT_PROTECTION/PG_SENSE; 4 VSS → /GND; 5 GND → /GND; 6 S4 → /GND; 7 D4 → /GND; 8 IN4 → /GND; 9 IN3 → /GND; 10 D3 → /GND; 11 S3 → /GND; 12 NC → unconnected-(U651-NC-Pad12); 13 VDD → /03_OUTPUT_PROTECTION/SAFE5; 14 S2 → /GND; 15 D2 → /GND; 16 IN2 → /GND |
| U607 | TLV3201AIDBVR | 1 OUT → /03_OUTPUT_PROTECTION/PG_GOOD; 2 GND → /GND; 3 IN+ → /03_OUTPUT_PROTECTION/PG_SENSE; 4 IN- → /03_OUTPUT_PROTECTION/REF1V25; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U630 | SN74LVC1G08DBVR | 1 A → /03_OUTPUT_PROTECTION/ARMED; 2 B → /03_OUTPUT_PROTECTION/MANUAL_VALID_NOFAULT; 3 GND → /GND; 4 Y → /03_OUTPUT_PROTECTION/MAIN_PERMISSION; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| R647 | 1k | 1 1 → /03_OUTPUT_PROTECTION/MAIN_PERMISSION; 2 2 → /INPUT_SHDN |
| R648 | 10k | 1 1 → /INPUT_SHDN; 2 2 → /GND |
| R649 | 1k | 1 1 → /03_OUTPUT_PROTECTION/FAULT; 2 2 → /03_OUTPUT_PROTECTION/FAULT_DRIVE |
| R650 | 100k | 1 1 → /03_OUTPUT_PROTECTION/FAULT_DRIVE; 2 2 → /GND |
| Q304 | 2N7002,215 | 1 G → /03_OUTPUT_PROTECTION/FAULT_DRIVE; 2 S → /GND; 3 D → /INPUT_SHDN |
| U631 | SN74LVC1G08DBVR | 1 A → /03_OUTPUT_PROTECTION/MAIN_PERMISSION; 2 B → /03_OUTPUT_PROTECTION/PG_GOOD; 3 GND → /GND; 4 Y → /03_OUTPUT_PROTECTION/SERIES_CLEAR_N; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U611 | SN74LVC1G74DCTR | 1 CLK → /03_OUTPUT_PROTECTION/SERIES_DOWN; 2 D → /03_OUTPUT_PROTECTION/SAFE5; 3 nQ → unconnected-(U611-nQ-Pad3); 4 GND → /GND; 5 Q → /03_OUTPUT_PROTECTION/SERIES_ARMED; 6 nCLR → /03_OUTPUT_PROTECTION/SERIES_CLEAR_N; 7 nPRE → /03_OUTPUT_PROTECTION/SAFE5; 8 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U632 | SN74LVC1G08DBVR | 1 A → /03_OUTPUT_PROTECTION/SERIES_ARMED; 2 B → /03_OUTPUT_PROTECTION/SERIES_CLEAR_N; 3 GND → /GND; 4 Y → /03_OUTPUT_PROTECTION/RUN_GATE_LOGIC; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| R640 | 20.0k | 1 1 → /L201_IN; 2 2 → /03_OUTPUT_PROTECTION/SW_HYS |
| R641 | 6.19k | 1 1 → /03_OUTPUT_PROTECTION/SW_HYS; 2 2 → /GND |
| R642 | 20.0k | 1 1 → /03_OUTPUT_PROTECTION/SW_HIGH; 2 2 → /03_OUTPUT_PROTECTION/SW_HYS |
| R644 | 49.9k | 1 1 → /VIN_PROTECTED; 2 2 → /03_OUTPUT_PROTECTION/VIN_MON |
| R645 | 10k | 1 1 → /03_OUTPUT_PROTECTION/VIN_MON; 2 2 → /GND |
| R651 | 100k | 1 1 → /03_OUTPUT_PROTECTION/SW_SENSE; 2 2 → /GND |
| R652 | 100k | 1 1 → /03_OUTPUT_PROTECTION/VIN_SENSE; 2 2 → /GND |
| U647 | ADG4612BRUZ | 1 IN1 → /03_OUTPUT_PROTECTION/SAFE5; 2 D1 → /03_OUTPUT_PROTECTION/SW_HYS; 3 S1 → /03_OUTPUT_PROTECTION/SW_SENSE; 4 VSS → /GND; 5 GND → /GND; 6 S4 → /GND; 7 D4 → /GND; 8 IN4 → /GND; 9 IN3 → /GND; 10 D3 → /GND; 11 S3 → /GND; 12 NC → unconnected-(U647-NC-Pad12); 13 VDD → /03_OUTPUT_PROTECTION/SAFE5; 14 S2 → /03_OUTPUT_PROTECTION/VIN_SENSE; 15 D2 → /03_OUTPUT_PROTECTION/VIN_MON; 16 IN2 → /03_OUTPUT_PROTECTION/SAFE5 |
| U640 | TLV3201AIDBVR | 1 OUT → /03_OUTPUT_PROTECTION/SW_HIGH; 2 GND → /GND; 3 IN+ → /03_OUTPUT_PROTECTION/SW_SENSE; 4 IN- → /03_OUTPUT_PROTECTION/REF1V25; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U642 | TLV3201AIDBVR | 1 OUT → /03_OUTPUT_PROTECTION/VIN_GOOD_FAST; 2 GND → /GND; 3 IN+ → /03_OUTPUT_PROTECTION/VIN_SENSE; 4 IN- → /03_OUTPUT_PROTECTION/REF1V25; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U644 | SN74LVC1G14DBVR | 1 NC → unconnected-(U644-NC-Pad1); 2 A → /03_OUTPUT_PROTECTION/SOURCE_CONTACT; 3 GND → /GND; 4 Y → /03_OUTPUT_PROTECTION/SRC_TRIP; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U610 | SN74LVC1G74DCTR | 1 CLK → /03_OUTPUT_PROTECTION/RESET_DOWN; 2 D → /03_OUTPUT_PROTECTION/SAFE5; 3 nQ → /03_OUTPUT_PROTECTION/FAULT; 4 GND → /GND; 5 Q → /03_OUTPUT_PROTECTION/NOFAULT; 6 nCLR → /03_OUTPUT_PROTECTION/FAULT_CLEAR_N; 7 nPRE → /03_OUTPUT_PROTECTION/SAFE5; 8 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U623 | SN74LVC1G08DBVR | 1 A → /03_OUTPUT_PROTECTION/NOFAULT; 2 B → /03_OUTPUT_PROTECTION/MANUAL_RAILS_VALID; 3 GND → /GND; 4 Y → /03_OUTPUT_PROTECTION/MANUAL_VALID_NOFAULT; 5 VCC → /03_OUTPUT_PROTECTION/SAFE5 |
| U612 | SN74LVC1G74DCTR | 1 CLK → /03_OUTPUT_PROTECTION/ARM_DOWN; 2 D → /03_OUTPUT_PROTECTION/SAFE5; 3 nQ → unconnected-(U612-nQ-Pad3); 4 GND → /GND; 5 Q → /03_OUTPUT_PROTECTION/ARMED; 6 nCLR → /03_OUTPUT_PROTECTION/MANUAL_VALID_NOFAULT; 7 nPRE → /03_OUTPUT_PROTECTION/SAFE5; 8 VCC → /03_OUTPUT_PROTECTION/SAFE5 |


## h. LM61460 block and cheaper candidates for Phase B evaluation

KNOWN: U201 is **LM61460AANRJRR**, L201 is **10 µH** (not the older narrative's 6.8 µH), and R202/R203 are **100 kΩ / 24.6 kΩ** (not 24.4 kΩ). CALCULATED with nominal 1 V FB reference: `1 × (1 + 100/24.6) = 5.065041 V`. The owner's 5.1 V target is not the exact captured nominal setpoint. No divider adjustment is selected here.

| Ref | Captured value / MPN | All pins → net | USD unit @10 |
| --- | --- | --- | --- |
| C201 | 10uF 50V / GRM32ER71H106KA12L | 1 1 → /VIN_PROTECTED; 2 2 → /GND | 0.3322 |
| C202 | 10uF 50V / GRM32ER71H106KA12L | 1 1 → /VIN_PROTECTED; 2 2 → /GND | 0.3322 |
| C203 | 100nF 50V / GRM188R71H104KA93D | 1 1 → /VIN_PROTECTED; 2 2 → /GND | OPEN |
| C204 | 100nF 50V / GRM188R71H104KA93D | 1 1 → /VIN_PROTECTED; 2 2 → /GND | OPEN |
| C205 | 100nF 50V / GRM188R71H104KA93D | 1 1 → /02_BUCK_5V/BUCK_CBOOT; 2 2 → /02_BUCK_5V/BUCK_SW | OPEN |
| C206 | 1uF 25V / GRM21BR71E105KA99L | 1 1 → /02_BUCK_5V/BUCK_VCC; 2 2 → /GND | 0.0586 |
| C207 | 22pF 50V / CGA3E2C0G1H220J080AA | 1 1 → /VOUT_5V1; 2 2 → /02_BUCK_5V/BUCK_FF | 0.058 |
| C209 | 22uF 50V / C5750X7R1H226M250KB | 1 1 → /VOUT_5V1; 2 2 → /GND | 3.40 |
| C210 | 22uF 50V / C5750X7R1H226M250KB | 1 1 → /VOUT_5V1; 2 2 → /GND | 3.40 |
| C211 | 22uF 50V / C5750X7R1H226M250KB | 1 1 → /VOUT_5V1; 2 2 → /GND | 3.40 |
| C212 | 22uF 50V / C5750X7R1H226M250KB | 1 1 → /VOUT_5V1; 2 2 → /GND | 3.40 |
| C213 | 22uF 50V / C5750X7R1H226M250KB | 1 1 → /VOUT_5V1; 2 2 → /GND | 3.40 |
| C214 | 22uF 50V / C5750X7R1H226M250KB | 1 1 → /VOUT_5V1; 2 2 → /GND | 3.40 |
| L201 | 10uH DATASHEET / 74437636351002 | 1 1 → /L201_IN; 2 2 → /02_BUCK_5V/L201_OUT | 21.84 |
| R201 | 33.2k / TNPW060333K2BEEA | 1 1 → /02_BUCK_5V/BUCK_RT; 2 2 → /GND | 0.1001 |
| R202 | 100k / TNPW0603100KBEEA | 1 1 → /VOUT_5V1; 2 2 → /02_BUCK_5V/BUCK_FB | 0.0797 |
| R203 | 24.6k / TNPW060324K6BEEA | 1 1 → /02_BUCK_5V/BUCK_FB; 2 2 → /GND | 0.20 |
| R204 | 0 / CRCW06030000Z0EA | 1 1 → /02_BUCK_5V/BUCK_CBOOT; 2 2 → /02_BUCK_5V/BUCK_RBOOT | OPEN |
| R205 | 1k / TNPW06031K00BEEA | 1 1 → /02_BUCK_5V/BUCK_FF; 2 2 → /02_BUCK_5V/BUCK_FB | OPEN |
| R206 | 100k / TNPW0603100KBEEA | 1 1 → /VIN_PROTECTED; 2 2 → /BUCK_INPUT_PGOOD | 0.0797 |
| R207 | 24.9k / TNPW060324K9BEEA | 1 1 → /BUCK_INPUT_PGOOD; 2 2 → /GND | 0.0833 |
| U201 | LM61460AANRJRR / LM61460AANRJRR | 1 BIAS → /GND; 2 VCC → /02_BUCK_5V/BUCK_VCC; 3 AGND → /GND; 4 FB → /02_BUCK_5V/BUCK_FB; 5 PGOOD → /BUCK_PGOOD; 6 RT → /02_BUCK_5V/BUCK_RT; 7 EN/SYNC → /BUCK_INPUT_PGOOD; 8 VIN1 → /VIN_PROTECTED; 9 PGND1 → /GND; 10 SW → /02_BUCK_5V/BUCK_SW; 11 PGND2 → /GND; 12 VIN2 → /VIN_PROTECTED; 13 RBOOT → /02_BUCK_5V/BUCK_RBOOT; 14 CBOOT → /02_BUCK_5V/BUCK_CBOOT | 1.5995 |


KNOWN: C201/C202 provide nominal 20 µF/50 V on VIN_PROTECTED. C203/C204 are 100 nF local input bypass; C205 is bootstrap capacitance returned to native BUCK_SW; R204 is the 0 Ω RBOOT link; C206 is 1 µF/25 V on internal VCC. R201 33.2 kΩ sets RT. R202/R203 meet directly at BUCK_FB/U201.4; C207 and R205 form a series feed-forward branch: VOUT_5V1 → C207 22 pF → BUCK_FF → R205 1 kΩ → BUCK_FB. U201.1 BIAS is grounded. R206/R207 serve EN/PGOOD, not output feedback. Six C209–C214 provide nominal 132 µF/50 V before output protection. Nominal sums are not effective capacitance under bias.

KNOWN: Sheet 03 adds eight 470 µF/35 V C330–C337 at VOUT_5V1 (3,760 µF nominal) and four C340–C343 at VOUT_PROTECTED (1,880 µF nominal). Changing Sheet 03 therefore changes buck startup/transient behavior even if Sheet 02 stays intact. Sheet 04 C404 is another 22 µF/50 V part, but it is on **3V3_LOCAL**, not the 5 V output.

| KNOWN observation | Phase B evaluation relevance | Unselected candidate / OPEN checks |
| --- | --- | --- |
| L201 74437636351002 costs $21.84 at the applicable six-piece tier: 578,760 VND. Manufacturer lists 10 µH, 63.8 A typical at 40 K rise, 90.7 A at 30% inductance drop, 0.62 mΩ ±10%, and a 36 × 35.7 × 34.2 mm envelope. | Large current capability and size relative to ordinary 5 A operation, but the old fault model assumed Ldiff 5–12 µH through 100 A. | Coilcraft XAL7070-103MEC: maker table $3.58 at 1–149, 10 µH, 7.5 A Isat, 20.2 mΩ max DCR. Bourns SRP1265A-100M: 10 µH, 15.5 A Isat, 16.5 mΩ max DCR, 10 A Irms; lower-cost direction, USD @10 not established here. Neither inherits the old 100 A magnetic assumption. |
| C209–C214: six 22 µF/50 V C5750X7R1H226M250KB, $3.40 each, $20.40/board. | Potential excess normal-operation voltage rating/size, but old 50 V rating also addressed buck high-side-short exposure. Nominal 24 V input does not make the pre-crowbar output rail inherently ≤16 V. | TDK C3225X7R1C226M250AC 22 µF/16 V/X7R/1210 is a reputable lower-voltage candidate. Lower cost needs a quote; effective C, ESR, loop stability, inrush, transient and fault exposure require analysis before changing ratings or quantity. |
| C201/C202: 50 V/10 µF on approximately 24 V input. | Not demonstrated over-specified: DC bias and upstream transients remain relevant. | Current Murata/TDK 50 V alternatives may be evaluated; do not infer that 25 V input parts are acceptable. |
| R201/R205/R206/R207: premium thin-film parts; low-voltage bypass/bootstrap parts often rated 50 V. | Nonprecision roles may offer savings; voltage rating alone does not imply worthwhile savings for small C0G/bypass capacitors. | Reputable Vishay/Yageo/Panasonic 1% parts for nonprecision roles only after frequency, enable/UVLO and voltage-margin review. FB R202/R203 need a separate tolerance budget. |
| C206 1 µF/25 V on VCC; low-voltage 50 V decouplers. | Possible lower-voltage MLCC cost reduction. | Murata/TDK X7R or suitable X5R at 10/16 V are evaluation families only; biased C and fault exposure remain OPEN. |

CALCULATED screening example: with ASSUMED 24 V input, 5.1 V output, 400 kHz and ideal 10 µH, `ΔIL = VOUT × (1 − VOUT/VIN)/(L × f) = 1.004 A p-p`; 5 A load gives approximately 5.502 A peak before tolerance, hot saturation, transients or faults. The 400 kHz value is legacy nominal intent, not a measurement. This screen cannot qualify an alternate inductor.

OPEN: bus extrema/surge/source current, efficiency, ripple, continuous/peak thermal limits, input inrush, fuse/TVS/reverse-FET behavior and SCR latch/hold/I²t coordination must be reviewed in Phase B. No candidate, component rating, circuit or protection threshold is selected by Phase A.

## i. Test points, jumpers, force links and fixture nets

KNOWN: the complete J/JP/PF/TP inventory follows, including possibly retained parts. Sheet 04 TP401–TP406 would disappear with telemetry; Sheet 05 J503 loses its on-board I2C destination. Every Sheet 03 fixture needs remapping if that block is replaced. Sheet 02 switch/current-injection links are features of the old fault fixture, not intrinsic LM61460 requirements.

### 01_INPUT_PROTECTION

| Ref | Captured purpose | Every terminal → net | Impact |
| --- | --- | --- | --- |
| JP101 | REMOVABLE FORCE LINK | 1 FORCE_A → /01_INPUT_PROTECTION/EFUSE_OUT; 2 FORCE_B → /VIN_PROTECTED | Input protection / source rail change |
| TP101 | INPUT_SHDN | 1 TP → /INPUT_SHDN | Input protection / source rail change |
| TP102 | INPUT_FLT | 1 TP → /01_INPUT_PROTECTION/INPUT_FLT | Input protection / source rail change |
| TP103 | EFUSE_OUT | 1 SIGNAL → /01_INPUT_PROTECTION/EFUSE_OUT; 2 RETURN → /GND | Input protection / source rail change |

### 02_BUCK_5V

| Ref | Captured purpose | Every terminal → net | Impact |
| --- | --- | --- | --- |
| JP201 | REMOVABLE FORCE LINK | 1 FORCE_A → /02_BUCK_5V/BUCK_SW; 2 FORCE_B → /L201_IN | Buck injection / current-force review |
| JP202 | REMOVABLE FORCE LINK | 1 FORCE_A → /02_BUCK_5V/L201_OUT; 2 FORCE_B → /VOUT_5V1 | Buck injection / current-force review |
| PF2 | VIN_PROTECTED | 1 FORCE → /VIN_PROTECTED | Buck injection / current-force review |
| PF3 | BUCK_SW | 1 FORCE → /02_BUCK_5V/BUCK_SW | Buck injection / current-force review |
| PF4 | L201_IN | 1 FORCE → /L201_IN | Buck injection / current-force review |
| TP201 | BUCK_SW | 1 SIGNAL → /02_BUCK_5V/BUCK_SW; 2 RETURN → /GND | Buck injection / current-force review |
| TP202 | L201_IN | 1 SIGNAL → /L201_IN; 2 RETURN → /GND | Buck injection / current-force review |
| TP203 | VOUT_5V1 | 1 SIGNAL → /VOUT_5V1; 2 RETURN → /GND | Buck injection / current-force review |
| TP204 | L201_OUT | 1 SIGNAL → /02_BUCK_5V/L201_OUT; 2 RETURN → /GND | Buck injection / current-force review |

### 03_OUTPUT_PROTECTION

| Ref | Captured purpose | Every terminal → net | Impact |
| --- | --- | --- | --- |
| J301 | MAIN ARM / dry contact | 1 CONTACT → /03_OUTPUT_PROTECTION/ARM_CONTACT; 2 RETURN → /GND | Output protection / fixture remap |
| J302 | MANUAL RESET / dry contact | 1 CONTACT → /03_OUTPUT_PROTECTION/RESET_CONTACT; 2 RETURN → /GND | Output protection / fixture remap |
| J603 | SOURCE FAULT / dry contact | 1 CONTACT → /03_OUTPUT_PROTECTION/SOURCE_CONTACT; 2 RETURN → /GND | Output protection / fixture remap |
| J604 | SERIES ARM / dry contact | 1 CONTACT → /03_OUTPUT_PROTECTION/SERIES_CONTACT; 2 RETURN → /GND | Output protection / fixture remap |
| J605 | REAL PG / guarded output | 1 CONTACT → /03_OUTPUT_PROTECTION/PG_FIXTURE; 2 RETURN → /GND | Output protection / fixture remap |
| J606 | MAIN PERMISSION / guarded output | 1 CONTACT → /03_OUTPUT_PROTECTION/MAIN_FIXTURE; 2 RETURN → /GND | Output protection / fixture remap |
| JP301 | REMOVABLE FORCE LINK | 1 FORCE_A → /03_OUTPUT_PROTECTION/SERIES_OUT; 2 FORCE_B → /VOUT_PROTECTED | Output protection / fixture remap |
| JP330 | REMOVABLE FORCE LINK | 1 FORCE_A → /03_OUTPUT_PROTECTION/CB_BALLAST_OUT; 2 FORCE_B → /03_OUTPUT_PROTECTION/CB_DRAIN | Output protection / fixture remap |
| JP331 | REMOVABLE FORCE LINK | 1 FORCE_A → /03_OUTPUT_PROTECTION/RAW_BALLAST_OUT; 2 FORCE_B → /03_OUTPUT_PROTECTION/RAW_DUMP_DRAIN | Output protection / fixture remap |
| JP600 | MANUAL RAIL VALID LINK | 1 CONTACT → /03_OUTPUT_PROTECTION/SAFE5; 2 RETURN → /03_OUTPUT_PROTECTION/MANUAL_RAILS_VALID | Output protection / fixture remap |
| JP660 | SER_DRV SUPPLY LINK | 1 CONTACT → /03_OUTPUT_PROTECTION/SER_FEED; 2 RETURN → /03_OUTPUT_PROTECTION/SER_DRV | Output protection / fixture remap |
| TP301 | VOUT_5V1 | 1 TP → /VOUT_5V1 | Output protection / fixture remap |
| TP302 | VOUT_PROTECTED | 1 TP → /VOUT_PROTECTED | Output protection / fixture remap |
| TP303 | REF_2V5 | 1 TP → /03_OUTPUT_PROTECTION/REF_2V5 | Output protection / fixture remap |
| TP304 | PROT_MID | 1 TP → /03_OUTPUT_PROTECTION/PROT_MID | Output protection / fixture remap |
| TP305 | PROT_GATE | 1 TP → /03_OUTPUT_PROTECTION/PROT_GATE | Output protection / fixture remap |
| TP306 | OV_DIV | 1 SIGNAL → /03_OUTPUT_PROTECTION/OV_DIV; 2 RETURN → /GND | Output protection / fixture remap |
| TP307 | OV_COMPARATOR | 1 SIGNAL → /03_OUTPUT_PROTECTION/OV_COMPARATOR; 2 RETURN → /GND | Output protection / fixture remap |
| TP308 | FAULT | 1 SIGNAL → /03_OUTPUT_PROTECTION/FAULT; 2 RETURN → /GND | Output protection / fixture remap |
| TP309 | CB_GATE | 1 SIGNAL → /03_OUTPUT_PROTECTION/CB_GATE; 2 RETURN → /GND | Output protection / fixture remap |
| TP310 | DRV_HOLD | 1 SIGNAL → /03_OUTPUT_PROTECTION/DRV_HOLD; 2 RETURN → /GND | Output protection / fixture remap |
| TP311 | DET5 | 1 SIGNAL → /03_OUTPUT_PROTECTION/DET5; 2 RETURN → /GND | Output protection / fixture remap |
| TP312 | INPUT_SHDN | 1 SIGNAL → /INPUT_SHDN; 2 RETURN → /GND | Output protection / fixture remap |
| TP313 | SER_DRV | 1 SIGNAL → /03_OUTPUT_PROTECTION/SER_DRV; 2 RETURN → /GND | Output protection / fixture remap |
| TP314 | PROT_GATE | 1 SIGNAL → /03_OUTPUT_PROTECTION/PROT_GATE; 2 RETURN → /03_OUTPUT_PROTECTION/PROT_MID | Output protection / fixture remap |
| TP315 | RAW_DUMP_GATE | 1 SIGNAL → /03_OUTPUT_PROTECTION/RAW_DUMP_GATE; 2 RETURN → /GND | Output protection / fixture remap |
| TP316 | SAFE5 | 1 SIGNAL → /03_OUTPUT_PROTECTION/SAFE5; 2 RETURN → /GND | Output protection / fixture remap |
| TP317 | BUCK_PGOOD | 1 SIGNAL → /BUCK_PGOOD; 2 RETURN → /GND | Output protection / fixture remap |
| TP318 | MANUAL_RAILS_VALID | 1 SIGNAL → /03_OUTPUT_PROTECTION/MANUAL_RAILS_VALID; 2 RETURN → /GND | Output protection / fixture remap |
| TP319 | RUN_GATE | 1 SIGNAL → /03_OUTPUT_PROTECTION/RUN_GATE; 2 RETURN → /GND | Output protection / fixture remap |
| TP320 | SRC_TRIP | 1 SIGNAL → /03_OUTPUT_PROTECTION/SRC_TRIP; 2 RETURN → /GND | Output protection / fixture remap |
| TP321 | CORE_POR_N | 1 SIGNAL → /03_OUTPUT_PROTECTION/CORE_POR_N; 2 RETURN → /GND | Output protection / fixture remap |
| TP322 | DRV_OBS_N | 1 SIGNAL → /03_OUTPUT_PROTECTION/DRV_OBS_N; 2 RETURN → /GND | Output protection / fixture remap |
| TP323 | DET_OBS_N | 1 SIGNAL → /03_OUTPUT_PROTECTION/DET_OBS_N; 2 RETURN → /GND | Output protection / fixture remap |
| TP324 | DET_PG | 1 SIGNAL → /03_OUTPUT_PROTECTION/DET_PG; 2 RETURN → /GND | Output protection / fixture remap |
| TP327 | HOLD_AUXOFF | 1 SIGNAL → /03_OUTPUT_PROTECTION/HOLD_AUXOFF; 2 RETURN → /GND | Output protection / fixture remap |
| TP328 | HOLD_FLT | 1 SIGNAL → /03_OUTPUT_PROTECTION/HOLD_FLT; 2 RETURN → /GND | Output protection / fixture remap |
| TP329 | AUX_RAW | 1 SIGNAL → /03_OUTPUT_PROTECTION/AUX_RAW; 2 RETURN → /GND | Output protection / fixture remap |
| TP330 | AUX_LIMITED | 1 SIGNAL → /03_OUTPUT_PROTECTION/AUX_LIMITED; 2 RETURN → /GND | Output protection / fixture remap |
| TP331 | AUX_12V | 1 SIGNAL → /03_OUTPUT_PROTECTION/AUX_12V; 2 RETURN → /GND | Output protection / fixture remap |
| TP332 | AUX_PREHOLD | 1 SIGNAL → /03_OUTPUT_PROTECTION/AUX_PREHOLD; 2 RETURN → /GND | Output protection / fixture remap |
| TP333 | 3V3_AUX | 1 SIGNAL → /03_OUTPUT_PROTECTION/3V3_AUX; 2 RETURN → /GND | Output protection / fixture remap |
| TP334 | PROT_BST | 1 SIGNAL → /03_OUTPUT_PROTECTION/PROT_BST; 2 RETURN → /03_OUTPUT_PROTECTION/PROT_MID | Output protection / fixture remap |
| TP335 | CB_BALLAST_OUT | 1 SIGNAL → /03_OUTPUT_PROTECTION/CB_BALLAST_OUT; 2 RETURN → /03_OUTPUT_PROTECTION/CB_DRAIN | Output protection / fixture remap |
| TP336 | RAW_BALLAST_OUT | 1 SIGNAL → /03_OUTPUT_PROTECTION/RAW_BALLAST_OUT; 2 RETURN → /03_OUTPUT_PROTECTION/RAW_DUMP_DRAIN | Output protection / fixture remap |
| TP337 | SW_HIGH | 1 SIGNAL → /03_OUTPUT_PROTECTION/SW_HIGH; 2 RETURN → /GND | Output protection / fixture remap |
| TP338 | VIN_GOOD_FAST | 1 SIGNAL → /03_OUTPUT_PROTECTION/VIN_GOOD_FAST; 2 RETURN → /GND | Output protection / fixture remap |
| TP339 | SW_SENSE | 1 SIGNAL → /03_OUTPUT_PROTECTION/SW_SENSE; 2 RETURN → /GND | Output protection / fixture remap |
| TP340 | VIN_SENSE | 1 SIGNAL → /03_OUTPUT_PROTECTION/VIN_SENSE; 2 RETURN → /GND | Output protection / fixture remap |

### 04_POWER_MONITOR

| Ref | Captured purpose | Every terminal → net | Impact |
| --- | --- | --- | --- |
| TP401 | ALERT_LOCAL | 1 TP → /04_POWER_MONITOR/ALERT_LOCAL | Removed with Sheet04 |
| TP402 | SHUNT_KPLUS | 1 TP → /04_POWER_MONITOR/SHUNT_KPLUS | Removed with Sheet04 |
| TP403 | SHUNT_KMINUS | 1 TP → /04_POWER_MONITOR/SHUNT_KMINUS | Removed with Sheet04 |
| TP404 | 3V3_LOCAL | 1 TP → /04_POWER_MONITOR/3V3_LOCAL | Removed with Sheet04 |
| TP405 | VOUT_PROTECTED | 1 SIGNAL → /VOUT_PROTECTED; 2 RETURN → /GND | Removed with Sheet04 |
| TP406 | LOAD_5V1 | 1 SIGNAL → /LOAD_5V1; 2 RETURN → /GND | Removed with Sheet04 |

### 05_IO_TEST

| Ref | Captured purpose | Every terminal → net | Impact |
| --- | --- | --- | --- |
| J501 | DC INPUT | 1 + → /VIN_RAW; 2 RETURN → /GND | Power/load/fixture mapping review |
| J502 | LOAD OUTPUT / mate1777989 | 1 + → /LOAD_5V1; 2 RETURN → /GND | Power/load/fixture mapping review |
| J503 | HOST I2C | 1 GND → /GND; 2 VREF → /3V3_HOST; 3 SDA → /SDA_HOST; 4 SCL → /SCL_HOST | I2C destination removed |
| JP501 | REMOVABLE FORCE LINK | 1 FORCE_A → /LOAD_5V1; 2 FORCE_B → /05_IO_TEST/LOAD_FIXTURE | Power/load/fixture mapping review |
| PF1 | VIN_RAW | 1 FORCE → /VIN_RAW | Power/load/fixture mapping review |
| PF5 | GND | 1 FORCE → /GND | Power/load/fixture mapping review |
| TP501 | VIN_RAW | 1 TP → /VIN_RAW | Power/load/fixture mapping review |
| TP502 | VIN_PROTECTED | 1 TP → /VIN_PROTECTED | Power/load/fixture mapping review |
| TP503 | LOAD_5V1 | 1 TP → /LOAD_5V1 | Power/load/fixture mapping review |
| TP504 | GND | 1 TP → /GND | Power/load/fixture mapping review |
| TP505 | LOAD_FIXTURE | 1 SIGNAL → /05_IO_TEST/LOAD_FIXTURE; 2 RETURN → /GND | Power/load/fixture mapping review |


KNOWN: the force path is J501 → F101/reverse/eFuse → JP101 → VIN_PROTECTED/U201 → BUCK_SW → JP201 → L201_IN/L201 → L201_OUT → JP202 → VOUT_5V1 → series FETs → SERIES_OUT → JP301 → VOUT_PROTECTED → R401 → LOAD_5V1 → J502. JP501 branches to LOAD_FIXTURE. JP330/JP331 isolate the two ballast/disposal branches. JP600 and JP660 are contact headers, not high-current copper straps. The custom-link drawing concerns seven force links only.

KNOWN: TP314 and TP334 return to PROT_MID, TP335 to CB_DRAIN, and TP336 to RAW_DUMP_DRAIN; their second terminals are not GND. Paired test points are sense features, not force connectors. Old procedures distinguish dummy-load takeoff JP501.2/PF5 from J502 and require unpowered link changes. Those mappings cannot be carried forward unchanged after simplification.

## j. Documentation, evidence, scripts and tests affected

KNOWN: this is an impact inventory, not permission to overwrite historical evidence. Old reports, exported schematics/netlists, ERC/DRC and identity proofs remain revision-bound. Future Lite work needs separate specifications/results and updated current-document pointers; no old PASS transfers to Lite.

| Concrete paths / family | Future revision or replacement needed |
| --- | --- |
| docs/00_REQUIREMENTS.md; 02_ARCHITECTURE.md; 03_COMPONENT_SELECTION.md; 04_POWER_CALCULATIONS.md; 05_SCHEMATIC_REVIEW.md; VALIDATION.md; FINAL_MANAGER_REPORT.md; R2_MANAGER_PACKET.md | New approximately 24 V contract, optional telemetry, budget scope, input/output protection and gate state; preserve dated historical entries. |
| README.md; docs/CODEX_HANDOFF.md; docs/context/01_PROJECT_OVERVIEW.md; 02_V1A_ARCHITECTURE.md; 03_ENGINEERING_STATE.md; 04_LEARNING_CURRICULUM.md; 06_DECISION_LOG.md | Existing eFuse/shunt/INA228 architecture and old gates; distinguish new owner context from historical decisions. |
| docs/evidence/r2/INPUT_PROTECTION.md; BUCK_DESIGN.md; OUTPUT_PROTECTION.md; MONITOR_POWER_DOMAINS.md; RASPBERRY_PI_DIRECT_POWER.md; SHEET03_PART_QUALIFICATION.md; R203_OPTION_A.md | New fuse/TVS/cutoff and fault envelope, FB setpoint, current path, I2C and Pi assumptions alongside old reviews. |
| docs/evidence/r2/BOM_DRAFT*; BOM_ORDER*; bom_order/*; bom_completion/* | Old 366-reference identities/stock, force links, harness and thermal accessories; create a separate Lite BOM and reconciliation. |
| docs/evidence/r2/{input,buck,output,monitor,io}_block.json and gate4b equivalents; gate4b/PIN_CONTRACTS.json; NET_CLASSES.json; GATE4B_SCOPE.json; CAPTURED_BOM.csv | Five-block schema, fixed refs/pins/nets, declarations and fixtures. Create Lite contracts while preserving old snapshots. |
| docs/evidence/r2/sheet03/*; footprints_complete/*; forensic_2026-09-14/*; takeover_2026-09-12/*; r203_option_a/* | Old threshold/timing/auxiliary, 100 A magnetic, fault-pulse/hold-up, shunt/harness, footprint and identity evidence does not validate Lite. |
| docs/evidence/r3/layout_prep/* and resume/*; paused layout branch | Placement/import/routing/DRC/export evidence belongs to the old architecture. |
| scripts/build_r2_schematic.py; build_sheet03_preliminary.py; build_gate4b.py; make_schematic_readable.py; fix_schematic_readability.py | Hard-coded hierarchy/blocks, manual fixtures and labels; running unchanged could restore removed circuitry. |
| scripts/build_qualified_footprints.py; build_sheet03_footprints.py; build_gate4b_footprints.py; build_completion_footprints.py; prepare_layout_board.py | Exact old MPN/ref/footprint assumptions, seven force links, Kelvin shunt and import placement. |
| scripts/check_r2_schematic.py; check_gate4b_contracts.py; check_gate4b_netclasses.py; check_footprint_completion.py; check_schematic_readability.py; check_repository.py; audit_gate4b_capture.py | U101/R401/U401/U402/U403 invariants; five-sheet/ref counts, netclasses, NC/power declarations and capture identity. |
| scripts/calculate_r2.py; calculate_r2_qualification.py; calculate_sheet03_gate1b.py; calculate_pi_interface.py | UV/OV/limit/timing, L/C/pulse models, 2 mΩ path budget, losses and calibration require a new source/protection contract. |
| scripts/export_r2_bom.py; export_sheet03_review.py; export_readable_review.py; export_reviewer_cover.py; check_r0_r1_docs.py | BOM and six-page/five-child hierarchy expectations, documentation references and gate text. |
| tests/test_r2_capture.py; test_gate4b_capture.py; test_qualified_footprints.py; test_footprint_completion.py; test_readability_identity.py; test_bom_order.py | Fixed reference sets/contracts, fixture continuity, footprints, source identity and order baseline. Preserve legacy regression coverage; later add scoped Lite expectations. |
| docs/evidence/r2/bom_order/validate.py; docs/evidence/r2/bom_completion/validate.py | Order/capture reconciliation, source hashes and fixed identities/quantities. |
| software/power_monitor/README.md; measurements/README.md; fabrication/README.md | Telemetry software is a placeholder, not an implementation. Lite bring-up/fabrication pointers require revision; dummy load precedes Pi integration. |

KNOWN: a per-file architecture-term match index follows. It identifies dependencies for later review; a match does not mean an archived file should be edited. Binary/generated evidence families are addressed above.

| Tracked path | First matching lines / terms | Matching lines |
| --- | --- | --- |
| README.md | 3:INA228, 7:VOUT_PROTECTED | 2 |
| docs/00_REQUIREMENTS.md | 26:INA228, 38:TPS2663 | 2 |
| docs/01_REFERENCE_AUDIT.md | 51:INA228, 74:INA228, 75:INA228, 79:TPS2663 | 6 |
| docs/02_ARCHITECTURE.md | 26:INA228, 41:TPS2663 | 2 |
| docs/03_COMPONENT_SELECTION.md | 40:INA228, 52:TPS2663 | 2 |
| docs/04_POWER_CALCULATIONS.md | 11:INA228, 81:INA228, 85:INA228 | 3 |
| docs/05_SCHEMATIC_REVIEW.md | 16:INA228, 28:TPS2663, 33:VOUT_PROTECTED, 35:LOAD_5V1 | 7 |
| docs/CLAUDE_PROJECT_SETUP.md | 31:04_POWER_MONITOR | 1 |
| docs/CODEX_HANDOFF.md | 38:INA228, 55:INA228, 109:INA228, 133:INA228 | 4 |
| docs/CODEX_HARDWARE_SOURCE_PACK.md | 13:TPS2663, 35:INA228, 37:ina228, 75:TPS2663 | 5 |
| docs/FINAL_MANAGER_REPORT.md | 101:INA228, 153:INA228, 162:INA228, 164:TPS2663 | 7 |
| docs/R2_MANAGER_PACKET.md | 12:TPS2663, 14:VOUT_PROTECTED, 15:VOUT_PROTECTED, 16:LOAD_5V1 | 6 |
| docs/VALIDATION.md | 79:VOUT_PROTECTED | 1 |
| docs/WBR_EDGE_SUPERVISOR_HAT_FEASIBILITY.md | 59:INA228, 93:INA228, 105:INA228, 127:INA228 | 9 |
| docs/context/01_PROJECT_OVERVIEW.md | 5:INA228, 14:04_POWER_MONITOR | 2 |
| docs/context/02_V1A_ARCHITECTURE.md | 7:TPS2663, 30:VOUT_PROTECTED, 34:INA228 | 3 |
| docs/context/03_ENGINEERING_STATE.md | 17:VOUT_PROTECTED, 35:VOUT_PROTECTED, 38:LOAD_5V1 | 3 |
| docs/context/04_LEARNING_CURRICULUM.md | 11:INA228 | 1 |
| docs/context/06_DECISION_LOG.md | 9:TPS2663, 10:INA228 | 2 |
| docs/evidence/r0/MONITOR_PROTECTION_SOURCE_REVIEW.md | 15:INA228, 16:INA228, 20:TPS2663, 31:INA228 | 10 |
| docs/evidence/r2/BOM_DRAFT.md | 5:JP501, 13:gate4b, 27:JP101, 36:JP101 | 20 |
| docs/evidence/r2/BOM_ORDER.md | 7:bom_order, 9:bom_order, 13:bom_order, 19:bom_order | 44 |
| docs/evidence/r2/INPUT_PROTECTION.md | 5:TPS2663, 8:TPS2663, 9:TPS2663 | 3 |
| docs/evidence/r2/MONITOR_POWER_DOMAINS.md | 1:INA228, 5:INA228, 14:INA228, 15:LOAD_5V1 | 10 |
| docs/evidence/r2/OUTPUT_PROTECTION.md | 17:VOUT_PROTECTED | 1 |
| docs/evidence/r2/PIN_AND_FOOTPRINT_REVIEW.md | 8:TPS2663, 25:INPUT_SHDN, 29:BUCK_INPUT_PGOOD, 83:BUCK_INPUT_PGOOD | 9 |
| docs/evidence/r2/R203_OPTION_A.md | 7:bom_order | 1 |
| docs/evidence/r2/RASPBERRY_PI_DIRECT_POWER.md | 11:VOUT_PROTECTED, 12:LOAD_5V1, 33:LOAD_5V1, 96:LOAD_5V1 | 5 |
| docs/evidence/r2/RECOVERY.md | 34:INA228, 35:LOAD_5V1, 43:INA228 | 3 |
| docs/evidence/r2/bom_completion/validate.py | 70:JP501 | 1 |
| docs/evidence/r2/bom_order/ACCESSORY_REVIEW.md | 5:bom_order, 9:gate4b, 16:MANUAL_RAILS_VALID | 3 |
| docs/evidence/r2/bom_order/CAPACITOR_REVIEW.md | 9:bom_order, 85:TPS2663 | 2 |
| docs/evidence/r2/bom_order/CLOSE_EXECUTION.md | 14:bom_order | 1 |
| docs/evidence/r2/bom_order/CLOSE_SUMMARY.md | 27:TPS2663, 28:INA228, 51:TPS2663, 52:INA228 | 5 |
| docs/evidence/r2/bom_order/FORCE_LINK_DRAWING.md | 23:JP101, 25:VOUT_PROTECTED, 28:JP501, 48:bom_order | 4 |
| docs/evidence/r2/bom_order/LOCK_REVIEW.md | 9:bom_order, 19:bom_order, 29:bom_order, 43:TPS2663 | 6 |
| docs/evidence/r2/bom_order/RESUME_REVIEW.md | 7:BOM_ORDER, 11:BOM_ORDER, 16:JP501 | 3 |
| docs/evidence/r2/bom_order/STOCK_REVIEW.md | 5:bom_order, 22:TPS2663, 23:INA228, 32:TPS2663 | 6 |
| docs/evidence/r2/bom_order/closeout.py | 9:bom_order, 75:Gate4B, 109:bom_order, 113:bom_order | 6 |
| docs/evidence/r2/bom_order/generate.py | 16:bom_order, 17:bom_order, 129:INA228, 130:TPS2663 | 25 |
| docs/evidence/r2/bom_order/validate.py | 18:BOM_ORDER, 19:BOM_ORDER, 21:bom_order, 22:bom_order | 21 |
| docs/evidence/r2/footprints_complete/SHEET04.md | 5:INA228 | 1 |
| docs/evidence/r2/footprints_complete/SHEET05.md | 10:LOAD_5V1, 25:LOAD_5V1, 26:LOAD_5V1 | 3 |
| docs/evidence/r2/forensic_2026-09-14/BOM_QUALIFIED_REVIEW.md | 28:INA228, 65:INPUT_SHDN, 68:VOUT_PROTECTED, 75:LOAD_5V1 | 6 |
| docs/evidence/r2/forensic_2026-09-14/CONNECTOR_HARNESS_QUALIFICATION.md | 7:LOAD_5V1, 42:INA228 | 2 |
| docs/evidence/r2/forensic_2026-09-14/CRITICAL_FOOTPRINT_QUALIFICATION.md | 62:VOUT_PROTECTED, 65:LOAD_5V1 | 2 |
| docs/evidence/r2/forensic_2026-09-14/FUSE_REQUIREMENTS_AND_CANDIDATES.md | 13:TPS2663 | 1 |
| docs/evidence/r2/forensic_2026-09-14/INPUT_TRANSIENT_COORDINATION.md | 17:TPS2663, 20:TPS2663 | 2 |
| docs/evidence/r2/forensic_2026-09-14/OUTPUT_PROTECTION_REQUIREMENTS_MATRIX.md | 13:INA228, 14:VOUT_PROTECTED, 55:LOAD_5V1 | 3 |
| docs/evidence/r2/forensic_2026-09-14/R2_R3_BLOCKER_REVIEW.md | 16:TPS2663, 31:VOUT_PROTECTED, 45:INA228, 49:VOUT_PROTECTED | 9 |
| docs/evidence/r2/gate4b/CHECK_C1C3.md | 12:TPS2663, 43:gate4b, 47:GATE4B, 51:gate4b | 4 |
| docs/evidence/r2/gate4b/FREEZE_COVERAGE.md | 13:TPS2663, 42:INA228, 45:JP501, 54:JP501 | 4 |
| docs/evidence/r2/gate4b/GATE4B_CAPTURE.md | 15:TPS2663, 18:INA228, 23:VOUT_PROTECTED, 37:JP101 | 10 |
| docs/evidence/r2/gate4b/PIN_REVIEW.md | 13:TPS2663, 28:JP101, 32:PIN_CONTRACTS, 54:gate4b | 6 |
| docs/evidence/r2/gate4b/REVIEW_RESOLUTIONS.md | 1:Gate4b, 16:gate4b, 18:GATE4B | 3 |
| docs/evidence/r2/gate4b/SHEET01_RESUME2_REVIEW.md | 5:INPUT_SHDN | 1 |
| docs/evidence/r2/gate4b/SHEET03_REVIEW.md | 9:PIN_CONTRACTS, 15:VOUT_PROTECTED, 29:MANUAL_RAILS_VALID, 46:PIN_CONTRACTS | 4 |
| docs/evidence/r2/gate4b/SHEET04_REVIEW.md | 7:VOUT_PROTECTED, 9:INA228 | 2 |
| docs/evidence/r2/gate4b/SHEET05_REVIEW.md | 10:LOAD_5V1, 12:JP501 | 2 |
| docs/evidence/r2/r203_option_a/EXECUTION.md | 7:gate4b, 8:gate4b, 14:bom_order, 16:bom_order | 4 |
| docs/evidence/r2/sheet03/GATE1D_PULSE_REVIEW.md | 11:VOUT_PROTECTED | 1 |
| docs/evidence/r2/sheet03/GATE2B_FIX_REVIEW.md | 30:VOUT_PROTECTED | 1 |
| docs/evidence/r2/sheet03/GATE2B_READABILITY.md | 20:INA228, 55:VOUT_PROTECTED | 2 |
| docs/evidence/r2/sheet03/GATE2_CALCULATIONS.md | 14:TPS2663 | 1 |
| docs/evidence/r2/sheet03/GATE2_PIN_REVIEW.md | 53:VOUT_PROTECTED | 1 |
| docs/evidence/r2/sheet03/GATE2_VALIDATION.md | 35:PIN_CONTRACTS, 63:INPUT_SHDN | 2 |
| docs/evidence/r2/sheet03/SHEET03_ARCHITECTURE_DECISION.md | 35:INPUT_SHDN, 47:TPS2663, 48:TPS2663, 49:TPS2663 | 11 |
| docs/evidence/r2/takeover_2026-09-12/BOM_REVIEW.md | 28:INA228, 65:INPUT_SHDN, 68:VOUT_PROTECTED, 75:LOAD_5V1 | 6 |
| docs/evidence/r2/takeover_2026-09-12/STATE.md | 18:04_POWER_MONITOR, 33:INA228, 54:VOUT_PROTECTED, 57:TPS2663 | 4 |
| docs/evidence/r3/layout_prep/CRITICAL_PLACEMENT_SECTION.md | 5:gate4b, 21:JP101, 54:VOUT_PROTECTED, 59:JP501 | 6 |
| docs/evidence/r3/layout_prep/LAYOUT_PREP.md | 76:gate4b, 77:gate4b | 2 |
| docs/evidence/r3/layout_prep/resume/RESUME.md | 50:gate4b, 51:gate4b, 60:gate4b | 3 |
| docs/evidence/wbr_hat/PI_POWER_WATCHDOG_REVIEW.md | 46:INA228, 55:INA228 | 2 |
| scripts/audit_gate4b_capture.py | 20:gate4b, 80:gate4b, 81:gate4b, 160:GATE4B | 6 |
| scripts/build_gate4b.py | 2:Gate4B, 12:gate4b, 15:04_POWER_MONITOR, 39:Gate4B | 28 |
| scripts/build_gate4b_footprints.py | 58:gate4b | 1 |
| scripts/build_r2_schematic.py | 84:Gate4B, 263:BUCK_INPUT_PGOOD, 264:BUCK_INPUT_PGOOD, 265:VOUT_PROTECTED | 8 |
| scripts/build_sheet03_preliminary.py | 53:INPUT_SHDN, 65:INPUT_SHDN, 67:INPUT_SHDN | 3 |
| scripts/calculate_sheet03_gate1b.py | 341:vout_protected, 427:TPS2663, 432:TPS2663, 433:TPS2663 | 10 |
| scripts/check_gate4b_contracts.py | 1:Gate4B, 38:INPUT_SHDN, 43:MANUAL_RAILS_VALID, 47:MANUAL_RAILS_VALID | 19 |
| scripts/check_gate4b_netclasses.py | 17:gate4b, 26:GATE4B | 2 |
| scripts/check_r2_schematic.py | 56:BUCK_INPUT_PGOOD, 62:VOUT_PROTECTED, 63:LOAD_5V1, 64:LOAD_5V1 | 20 |
| scripts/check_repository.py | 41:04_POWER_MONITOR, 69:gate4b, 89:gate4b, 90:gate4b | 16 |
| scripts/check_schematic_readability.py | 21:04_POWER_MONITOR | 1 |
| scripts/configure_gate4b_netclasses.py | 17:VOUT_PROTECTED, 18:LOAD_5V1 | 2 |
| scripts/export_readable_review.py | 16:04_POWER_MONITOR | 1 |
| scripts/export_sheet03_review.py | 20:04_POWER_MONITOR | 1 |
| scripts/fix_schematic_readability.py | 285:INPUT_SHDN, 314:04_POWER_MONITOR | 2 |
| scripts/make_schematic_readable.py | 383:TPS2663, 390:BUCK_INPUT_PGOOD, 407:BUCK_INPUT_PGOOD, 423:VOUT_PROTECTED | 13 |
| software/power_monitor/README.md | 3:INA228 | 1 |
| tests/test_bom_order.py | 8:bom_order | 1 |
| tests/test_gate4b_capture.py | 19:Gate4B, 24:gate4b, 27:gate4b, 43:gate4b | 10 |
| tests/test_r2_capture.py | 70:VOUT_PROTECTED, 71:VOUT_PROTECTED | 2 |


## Sources, OPEN prices and validation

KNOWN: no third-party PCB or reference circuit was copied or adapted. Existing upstream material remains isolated under `third_party/` and unchanged. External manufacturer documents below were referenced for component facts/evaluation only; no source file was downloaded into this repository. Copyright remains with each manufacturer/distributor; no redistribution license is assumed. Attribution is recorded here and in CSV URLs. Later circuit reuse would require its own exact source/license review.

| Reference | Revision / access | Function studied / reuse |
| --- | --- | --- |
| [TI LM61460 datasheet](https://www.ti.com/lit/ds/symlink/lm61460.pdf) | SNVSBD5D, May 2019 / revised July 2022; accessed 2026-10-04 | FB and L/C context; referenced only. |
| [Würth 74437636351002](https://www.we-online.com/components/products/datasheet/74437636351002.pdf) | 001.000, 2025-02-07, pp1–2; accessed 2026-10-04 | Captured inductor current, DCR, envelope; referenced only. |
| [Coilcraft XAL7070-103](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal7070/xal7070-103/) | Live page, no revision displayed; accessed 2026-10-04 | Unselected cost/size candidate. No circuit copied. |
| [Bourns SRP1265A](https://www.bourns.com/docs/product-datasheets/srp1265a.pdf) | Manufacturer PDF revision identifier OPEN; accessed 2026-10-04 | Unselected 10 µH candidate electrical table; referenced only. |
| [TDK C3225X7R1C226M250AC](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1C226M250AC) | Live production-part page, revision not displayed; accessed 2026-10-04 | Lower-voltage candidate identity; referenced only. |
| [TDK characterization](https://product.tdk.com/info/en/documents/chara_sheet/c3225x7r1c226m250ac.pdf) | January 4, 2016; accessed 2026-10-04 | Bias/ESR/thermal curves to evaluate in Phase B; not qualified here. |
| [TI TPS26630–33EVM](https://www.ti.com/lit/ug/slvubi8a/slvubi8a.pdf) | SLVUBI8A, Rev A; accessed 2026-10-04 | PGOOD/UVLO/SHDN reference context; no circuit copied. Pin tracing uses project XML. |

### New public price observations

| Evidence / MPN | Channel / stock snapshot | USD unit @10 | Source / access / crawl |
| --- | --- | --- | --- |
| LITE-A-W01 / TNPW0603100RBEEA | MOUSER / 23202 | 0.174 | [TNPW0603100RBEEA](https://www.mouser.com/c/?q=71-TNPW0603100RBEEN); 2026-10-04; 4 months ago |
| LITE-A-W03 / TNPW06034K70BEEA | MOUSER / OPEN | 0.26 | [TNPW06034K70BEEA](https://www.mouser.com/en/ProductDetail/Vishay/TNPW06034K70BEEA?qs=hEUCbmUtbxH2b2BZ4ek4qQ%3D%3D); 2026-10-04; yesterday |
| LITE-A-W02 / TNPW060354K9BEEA | MOUSER / 4314 | 0.149 | [TNPW060354K9BEEA](https://www.mouser.com/c/?q=71-TNPW060354K9BEEA); 2026-10-04; 3 months ago |
| LITE-A-W04 / TNPW060388K7BEEA | MOUSER / 15484 | 0.192 | [TNPW060388K7BEEA](https://www.mouser.com/c/passive-components/resistors/film-resistors/thin-film-resistors-smd/?q=388); 2026-10-04; 3 months ago |


KNOWN: indexed TNPW060388K7BEEA tables disagree ($0.192/$0.25/$0.267); this audit uses the explicitly cited $0.192 observation, not a live quote. L201's $21.84 tier was also independently found at [Mouser](https://www.mouser.com/ProductDetail/Wurth-Elektronik/74437636351002?qs=2FehpBK1j97R94Iy%2Fo9K7Q%3D%3D), accessed 2026-10-04, crawl age three months; saved stock was not upgraded on that basis.

### Remaining OPEN price lines

KNOWN: exact-MPN LCSC/Mouser queries on 2026-10-04 did not establish every required USD tier. Some results provide only foreign currency, alternate packaging, nonstocked records or inaccessible pages. Bare Mouser product URLs for 1776508, 3403.0285.23, INA228AIDGSR and TNPW060315K0BEEA returned access errors. MOQ conflicts are known from saved tables. No price for an alternate TDK AC suffix, CSD18540Q5BT, Murata alternate or resistor packaging suffix was silently assigned to the captured identity.

KNOWN: additional lookup provenance below records accessed/indexed URLs for unsuccessful price closure. All accesses were **2026-10-04**; indexed results may be older. Foreign currencies were not treated as USD.

| Queried part | Retrieved/attempted URL | Disposition |
| --- | --- | --- |
| 1776508 | [Mouser exact product](https://www.mouser.com/ProductDetail/Phoenix-Contact/1776508) | Direct access failed; regional search did not establish usable USD @10. |
| 3403.0285.23 | [Mouser Australia](https://au.mouser.com/en/ProductDetail/Schurter/3403.0285.23?qs=sGAEpiMZZMsZt0HrY5I79gvvspmojkSvBgiu4pDZC1A%3D) | AUD @10 found; USD unresolved. |
| INA228AIDGSR | [Mouser exact product](https://www.mouser.com/ProductDetail/Texas-Instruments/INA228AIDGSR) | Direct access failed; regional indexed offers were not USD. |
| BSS138 | [LCSC onsemi C52895](https://www.lcsc.com/product-detail/MOSFET_ON-Semicon_BSS138_ON-Semicon-ON-BSS138_C52895.html) | Identity found, usable quantity-10 price/stock not established. |
| GRM1885C1H330JA01D | [Mouser exact product](https://www.mouser.com/es/ProductDetail/Murata-Electronics/GRM1885C1H330JA01D?qs=E%252B5dfF6xfG3shwmI3hm0tg%3D%3D) | No usable USD @10; stocked LCSC has minimum-lot conflict. |
| GRM188R71H104KA93D | [Mouser Europe](https://eu.mouser.com/pl/ProductDetail/Murata-Electronics/GRM188R71H104KA93D?qs=f7ZljCwbPOm85Y6l%2FNGt7A%3D%3D) | No usable USD @10; stocked LCSC minimum is 50. |
| TNPW060315K0BEEA | [Mouser France](https://www.mouser.fr/fr/ProductDetail/Vishay/TNPW060315K0BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6%2FHqGwBTfsDk%3D) | EUR table found; no USD conversion invented. |
| TNPW060315K8BEEA | [Mouser Ecuador](https://www.mouser.ec/es/ProductDetail/Vishay/TNPW060315K8BEEA?qs=UyvxJcuXVAb2EBXqPsn9og%3D%3D) | No usable exact-part USD @10; BEEN packaging results not substituted. |
| TNPW06031K00BEEA | [LCSC exact product C844891](https://www.lcsc.com/product-detail/C844891.html) | Direct access failed; indexed alternate-product rows show varying prices without a complete exact-part tier table. |
| TNPW06034K32BEEA | [Mouser Australia](https://au.mouser.com/en/ProductDetail/Vishay/TNPW06034K32BEEA?qs=sGAEpiMZZMtG0KNrPCHnjUkh%2F9eucPbm%2FECs8LQBFnU%3D) | No usable USD @10. |
| TNPW06036K19BEEA | [Mouser Europe](https://eu.mouser.com/en/ProductDetail/Vishay/TNPW06036K19BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6kwsQ2%252BXgEuU%3D) | No usable USD @10. |
| TNPW06039K88BEEA | [Mouser Greece](https://gr.mouser.com/en/ProductDetail/Vishay/TNPW06039K88BEEA?qs=sGAEpiMZZMvdGkrng054twbPyJJnNTBKxZF4yk9Nt%2FU%3D) | No usable USD @10. |
| TNPW0805365KBEEA | [Mouser Australia](https://au.mouser.com/ProductDetail/Vishay/TNPW0805365KBEEA?qs=l%252BcklhsjygfNLOYszerPyg%3D%3D) | Nonstocked, no usable numeric USD tier. |
| TNPW0805383KBEEA | [Mouser Latvia](https://lv.mouser.com/en/ProductDetail/Vishay/TNPW0805383KBEEA?qs=sGAEpiMZZMvdGkrng054tzV2vEziUmcBmW%252BZbNQ0D3g%3D) | EUR table found; no USD conversion invented. |

KNOWN: exact-part searches for C3216X7R1H475K160AB, PCH1V471MCL1GS, CRCW06030000Z0EA, TNPW0603143KBEEA, TNPW060332K4BEEA, TNPW060368K1BEEA, TNPW06036K49BEEA and TNPW0805348KBEEA did not yield a usable LCSC/Mouser USD @10 offer. Datasheet-only and alternate-suffix results were excluded. Their prior source records, if present, are retained in the CSV and table below.

| MPN | Affected refs | OPEN reason | Existing supplier source / original date |
| --- | --- | --- | --- |
| 1776508 | J502 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://my.mouser.com/ProductDetail/Phoenix-Contact/1776508?qs=8M15sSGRUn%252B2z3E1%2FgeKhw%3D%3D) |
| 2N7002,215 | Q304 | LCSC stocked; smallest quoted lot 20 at USD 0.0183/piece. Quantity-10 OPEN; no downward extrapolation. | [2026-10-03](https://www.lcsc.com/product-detail/C65189.html) |
| 3403.0285.23 | F101 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://uy.mouser.com/es/ProductDetail/Schurter/3403.0285.23?qs=sGAEpiMZZMsZt0HrY5I79gvvspmojkSvBgiu4pDZC1A%3D) |
| B2B-XH-A(LF)(SN) | J301, J302, J603, J604, J605, J606, JP600, JP660 | LCSC stocked; smallest quoted lot 20 at USD 0.0409/piece. Quantity-10 OPEN; no downward extrapolation. | [2026-10-03](https://www.lcsc.com/product-detail/C158012.html) |
| BAS116,215 | D301, D302, D322, D618, D619, D640, D641, D642, D643 | LCSC stocked; smallest quoted lot 20 at USD 0.0219/piece. Quantity-10 OPEN; no downward extrapolation. | [2026-10-03](https://www.lcsc.com/product-detail/C48502.html) |
| BSS138 | Q102 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://www.mouser.com/en/ProductDetail/onsemi/BSS138?qs=HK%252BeIG1iaahCeqBvjB4arg%3D%3D) |
| C3216X7R1H475K160AB | C351 | No exact-part USD quantity-10 offer verified. Existing BOM_ORDER identity differs: C3216X7R1H475K160AC. Captured identity retained. | No verified exact offer |
| CRCW06030000Z0EA | R204 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://eu.mouser.com/en/ProductDetail/Vishay/CRCW06030000Z0EA?qs=uFJqmf%2F3rbbVtxvMdbYUaQ%3D%3D) |
| CRCW0603100RFKEA | R374 | LCSC stocked; smallest quoted lot 100 at USD 0.0044/piece. Quantity-10 OPEN; no downward extrapolation. | [2026-10-03](https://www.lcsc.com/product-detail/C844917.html) |
| CUSTOM-FX-CU-01 RevA | JP101, JP201, JP202, JP301, JP330, JP331, JP501 | Custom force-link manufacture/hardware cost OPEN. | No verified exact offer |
| GRM1885C1H330JA01D | C357 | LCSC stocked; smallest quoted lot 50 at USD .0165/piece. Quantity-10 OPEN; no downward extrapolation. | [2026-10-04](https://www.lcsc.com/product-detail/C77035.html) |
| GRM188R71H104KA93D | C103, C203, C204, C205, C303, C304, C308, C354, C355, C364, C368, C369, C370, C376, C380, C401, C402, C405, C406, C604, C609, C640, C642, C644, C647, C651, C710, C711, C712, C714, C715, C716, C717, C723, C728, C730, C731, C732, C733, C754, C756, C761, C762 | LCSC stocked; smallest quoted lot 50 at USD .0171/piece. Quantity-10 OPEN; no downward extrapolation. | [2026-10-04](https://www.lcsc.com/product-detail/C77055.html) |
| INA228AIDGSR | U401 | No exact-part USD quantity-10 offer verified. | No verified exact offer |
| PCH1V471MCL1GS | C330, C331, C332, C333, C334, C335, C336, C337, C340, C341, C342, C343 | No exact-part USD quantity-10 offer verified. | No verified exact offer |
| TNPW0603143KBEEA | R711 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://uy.mouser.com/en/ProductDetail/Vishay/TNPW0603143KBEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f64Y6MLIrBo3s%3D) |
| TNPW060315K0BEEA | R343, R344 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://my.mouser.com/en/ProductDetail/Vishay/TNPW060315K0BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6%2FHqGwBTfsDk%3D) |
| TNPW060315K8BEEA | R104 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://eu.mouser.com/ProductDetail/Vishay/TNPW060315K8BEEA?qs=UyvxJcuXVAb2EBXqPsn9og%3D%3D) |
| TNPW06031K00BEEA | R205, R303, R373, R622, R647, R649, R709, R712, R717, R730, R731 | LCSC stocked in recorded evidence but quantity-10 USD price unavailable; no silent Mouser substitution. | [2026-10-03](https://www.lcsc.com/fr/product-detail/C844891.html?is_substitute=1&lcsc_vid=FQAKVwECEQQKXlUHQgVXVFdXR1IIBABUFgMKBgIDElkxVlNeQVVdUVNfQVlXVjtW&original_product_code=C2093795&original_unit_price=0.2710) |
| TNPW060332K4BEEA | R312, R600 | No exact-part USD quantity-10 offer verified. | No verified exact offer |
| TNPW06034K32BEEA | R331 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://au.mouser.com/en/ProductDetail/Vishay/TNPW06034K32BEEA?qs=sGAEpiMZZMtG0KNrPCHnjUkh%2F9eucPbm%2FECs8LQBFnU%3D) |
| TNPW060368K1BEEA | R361 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://nz.mouser.com/en/ProductDetail/Vishay/TNPW060368K1BEEA?qs=sGAEpiMZZMtlubZbdhIBINLZLyWy7QeNDpwhuu44zSU%3D) |
| TNPW06036K19BEEA | R641 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://eu.mouser.com/en/ProductDetail/Vishay/TNPW06036K19BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6kwsQ2%252BXgEuU%3D) |
| TNPW06036K49BEEA | R375 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://hu.mouser.com/en/ProductDetail/Vishay/TNPW06036K49BEEA?qs=sGAEpiMZZMvdGkrng054t1txRVFnX3f6Ajf5Nzy89Tc%3D) |
| TNPW06039K88BEEA | R301 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://gr.mouser.com/en/ProductDetail/Vishay/TNPW06039K88BEEA?qs=sGAEpiMZZMvdGkrng054twbPyJJnNTBKxZF4yk9Nt%2FU%3D) |
| TNPW0805348KBEEA | R103 | No exact-part USD quantity-10 offer verified. | No verified exact offer |
| TNPW0805365KBEEA | R376, R378 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://au.mouser.com/ProductDetail/Vishay/TNPW0805365KBEEA?qs=l%252BcklhsjygfNLOYszerPyg%3D%3D) |
| TNPW0805383KBEEA | R345 | No exact-part USD quantity-10 offer verified. | [2026-10-03](https://lv.mouser.com/en/ProductDetail/Vishay/TNPW0805383KBEEA?qs=sGAEpiMZZMvdGkrng054tzV2vEziUmcBmW%252BZbNQ0D3g%3D) |


### Audit reproduction and checks

KNOWN: KiCad CLI version **9.0.6**. `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch export netlist --format kicadxml -o /private/tmp/v1a-lite-phase-a.xml hardware/kicad/V1A.kicad_sch` exited 0. Fontconfig warnings appeared; XML parsed successfully. The export is temporary and uncommitted. No legacy builder or generator was executed.

KNOWN: source SHA-256 hashes:

| Input | SHA-256 |
| --- | --- |
| hardware/kicad/01_INPUT_PROTECTION.kicad_sch | e1bce9b948dda904ccd756ea3e619704c9e2a30de4de2e6801271357e2b21d47 |
| hardware/kicad/02_BUCK_5V.kicad_sch | 0a68c0ed3dc2b7503c574f6ef49383c5f6fed5e9a1ab210254396ab51a8a5c6b |
| hardware/kicad/03_OUTPUT_PROTECTION.kicad_sch | b1ef585adf37946493721f510a197a1c0b5f0ec562446685ec78f0bbc8955075 |
| hardware/kicad/04_POWER_MONITOR.kicad_sch | a2c653cfe327d0370318c210d5690425b2a0f7c900124d378cdd3d7e6f96ffb6 |
| hardware/kicad/05_IO_TEST.kicad_sch | 3dc65ef9267c9599e26226a4bfb1a1dbd13584a860c689447166ada62ca536e9 |
| hardware/kicad/V1A.kicad_sch | 926bb81d876645902594c34808b2905ef1fb6463873d87a19fd2f07abe5324a1 |
| docs/evidence/r2/BOM_ORDER.csv | 16183d9484627e260950ccaf86435ddf3110e16a897b79755597eda91fbe76be |
| docs/evidence/r2/BOM_ORDER_LCSC.csv | b6da18d126a9670f0e4d3e6a61d348885766468e594a32f331f61a38fb5b5ea0 |
| docs/evidence/r2/bom_order/PROVENANCE.json | 352886f443459e1855886c2ad2c7bbdc173f7c18c56b610133951f48489aee0c |


CALCULATED reconciliation: **366 unique XML refs; 135 per-sheet CSV rows; quantities sum to 366; no missing/duplicate ref; 79 J/JP/PF/TP references enumerated**. Root sheet-pin sets exactly match child hierarchical-label sets for all five sheets. Six Sheet04 and eight Sheet03 cross-sheet nets were counted from physical pin membership. Decimal CSV extensions and per-sheet totals reconcile at 26,500 VND/USD; unknown prices stay OPEN. Hardware/software validation was not performed.


OPEN: this audit records the old design and pricing gaps. It does not choose the SCR, fuse, reverse FET, TVS, cheaper passives or setpoint, establish the auxiliary-bus fault envelope, authorize fabrication, or demonstrate a Lite budget. Phase B can use the complete pin/ref inventory and explicitly incomplete cost baseline.
