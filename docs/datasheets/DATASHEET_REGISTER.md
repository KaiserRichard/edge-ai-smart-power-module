# V1A datasheet register

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Date: 2026-10-03. **CONDITIONAL: register complete; the OPEN items below remain unresolved.**

**EVIDENCE:** Exported 345 component entries from `hardware/kicad/V1A.kicad_sch` at `634dfa319139a4bfe98202cd0a888fb71319074f` on `docs/datasheet-pack`, using KiCad CLI 9.0.6. All 107 distinct MPN-field values and every exported reference are accounted for: 93 commercial MPNs, 2 custom identifiers and 12 etched-test-feature identifiers. No blank MPNs or DNP entries were exported.

**EVIDENCE:** 77 commercial MPNs have local PDFs (41 distinct documents); 16 commercial MPN downloads remain OPEN. One downloaded reference, SMCJ36CA, also has an OPEN manufacturer selection. Both custom identifiers need project specifications.

**DECISION:** This is a documentation side task. KiCad files were read only and their SHA-256 values remained unchanged. No gate was advanced or electrical behavior validated. ERC/DRC were not rerun because there were no schematic/PCB changes. Only this register and its JSON counterpart are intended for commit; all vendor PDFs remain local under `third_party/datasheets/`.

**OBSERVATION:** The schematic has no populated Manufacturer or Datasheet export fields. Manufacturers were resolved from exact product/family documents and existing project provenance. onsemi is the prior documented BSS138 reference; SMCJ36CA remains ambiguous across manufacturers.

## Export and interpretation

BOM command (run at repository root):

```sh
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch export bom --output /tmp/v1a-datasheet-pack/V1A_BOM.csv --fields 'Reference,Value,MPN,Manufacturer,Datasheet,Footprint,${DNP},Rating' --labels 'Reference,Value,MPN,Manufacturer,Datasheet,Footprint,DNP,Rating' --include-excluded-from-bom hardware/kicad/V1A.kicad_sch
```

BOM SHA-256: `321280b0a2664ff33b412f50f568c893d6da39218b41c6407375189b92f216c9`. Export CSV and temporary extraction tools are under `/tmp/v1a-datasheet-pack/`, outside the commit. The JSON embeds the complete reference-to-MPN mapping and source-file hashes.

- Pages below are **one-based PDF pages**, including covers and package appendices. Package pages select the captured order-code variant.
- DOWNLOADED proves retrieval of parseable source bytes only. Remote page/revision evidence is labeled and has no local hash.
- For passives, ratings and derating replace an IC-style absolute maximum table. Nonpolar devices have no electrical polarity assignment.
- An empty page list is explained as OPEN or not supplied; it is never an invented page number.
- One family PDF is saved under each applicable exact MPN. Its revision does not prove exact-MPN availability or circuit qualification.
- Vendor originals are unchanged, copyrighted manufacturer references; no open redistribution license is inferred. Preserve manufacturer, URL, revision and all notices. No circuit was copied/adapted during this task.

## OPEN downloads and owner actions

Open the official link in a browser, save the actual PDF to the listed filename, verify the exact part/package and revision, compute SHA-256, and confirm these page references. If a URL is retired, use the manufacturer product page. HTML error/challenge pages were rejected. HTTP 403 entries remain OPEN as requested.

| MPN | Retrieval result | Official source | Expected local file |
| --- | --- | --- | --- |
| 1776508 | HTTP 403; curl: (22) The requested URL returned error: 403 | [PDF](https://www.phoenixcontact.com/us/products/1776508/pdf) | `third_party/datasheets/1776508.pdf` |
| 2N7002,215 | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf) | `third_party/datasheets/2N7002,215.pdf` |
| ADG4612BRUZ | HTTP 000; curl: (56) Recv failure: Operation timed out | [PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG4612_4613.pdf) | `third_party/datasheets/ADG4612BRUZ.pdf` |
| BAS116,215 | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://assets.nexperia.com/documents/data-sheet/BAS116.pdf) | `third_party/datasheets/BAS116,215.pdf` |
| BSC034N06NSATMA1 | HTTP 202; HTTP response is not a PDF | [PDF](https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsc034n06ns-datasheet-en.pdf) | `third_party/datasheets/BSC034N06NSATMA1.pdf` |
| C1608C0G1H102J080AA | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://product.tdk.com/info/en/documents/chara_sheet/C1608C0G1H102J080AA.pdf); [product](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608C0G1H102J080AA) | `third_party/datasheets/C1608C0G1H102J080AA.pdf` |
| C1608C0G1H103J080AA | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://product.tdk.com/info/en/documents/chara_sheet/C1608C0G1H103J080AA.pdf); [product](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608C0G1H103J080AA) | `third_party/datasheets/C1608C0G1H103J080AA.pdf` |
| C3216X7R1H475K160AB | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://product.tdk.com/info/en/documents/chara_sheet/C3216X7R1H475K160AB.pdf); [product](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X7R1H475K160AB) | `third_party/datasheets/C3216X7R1H475K160AB.pdf` |
| C5750X7R1H226M250KB | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://product.tdk.com/info/en/documents/chara_sheet/C5750X7R1H226M250KB.pdf); [product](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C5750X7R1H226M250KB) | `third_party/datasheets/C5750X7R1H226M250KB.pdf` |
| CGA3E2C0G1H220J080AA | HTTP 403; curl: (56) The requested URL returned error: 403 | [PDF](https://product.tdk.com/info/en/documents/chara_sheet/CGA3E2C0G1H220J080AA.pdf); [product](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CGA3E2C0G1H220J080AA) | `third_party/datasheets/CGA3E2C0G1H220J080AA.pdf` |
| GRM188R71H104KA93D | HTTP 000; Official reference URL returned HTTP 404; distributor mirror also failed: curl: (92) HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR (err 2) | [PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H104KA93-01.pdf); [product](https://www.murata.com/en-us/products/productdetail?partno=GRM188R71H104KA93D); [mirror attempt](https://www.mouser.com/datasheet/2/281/1/GRM188R71H104KA93_01-3155748.pdf) | `third_party/datasheets/GRM188R71H104KA93D.pdf` |
| GRM32ER71H106KA12L | HTTP 404; curl: (56) The requested URL returned error: 404 | [PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER71H106KA12-04A.pdf); [product](https://www.murata.com/en-us/products/productdetail?partno=GRM32ER71H106KA12L) | `third_party/datasheets/GRM32ER71H106KA12L.pdf` |
| LT4363HMS-1#PBF | HTTP 000; curl: (92) HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR (err 2) | [PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf) | `third_party/datasheets/LT4363HMS-1#PBF.pdf` |
| LTC3115IFE-1#PBF | HTTP 000; curl: (92) HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR (err 2) | [PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf) | `third_party/datasheets/LTC3115IFE-1#PBF.pdf` |
| LTC7001IMSE#PBF | HTTP 000; curl: (28) Operation timed out after 35004 milliseconds with 0 bytes received | [PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf) | `third_party/datasheets/LTC7001IMSE#PBF.pdf` |
| STPS60H100CT | HTTP 000; curl: (28) Operation timed out after 35005 milliseconds with 0 bytes received | [PDF](https://www.st.com/resource/en/datasheet/stps60h100c.pdf) | `third_party/datasheets/STPS60H100CT.pdf` |

**OPEN RISK — manufacturer:** `SMCJ36CA` has a Vishay PDF cached for reference, but the schematic does not identify a manufacturer. Confirm the intended manufacturer and full ordering code before treating that PDF as binding.

**OPEN RISK — custom items:** `CUSTOM-FX-CU-01 RevA` and `CUSTOM-FX-PAD-M4 RevA` have no manufacturer datasheets. The owner must supply controlled mechanical/material/rating/assembly specifications. No PDFs were invented.

## Complete MPN and reference coverage

Document IDs link to the revision, URL, SHA-256 and page index below. The JSON also repeats those fields per commercial MPN for machine use.

| MPN / schematic field | Manufacturer / kind | References | Qty | Status | Document |
| --- | --- | --- | ---: | --- | --- |
| 1776508 | Phoenix Contact | J502 | 1 | OPEN | [phoenix1776508](#doc-phoenix1776508) |
| 2N7002,215 | Nexperia | Q304 | 1 | OPEN | [2n7002](#doc-2n7002) |
| 3403.0285.23 | SCHURTER | F101 | 1 | DOWNLOADED | [umt_h](#doc-umt_h) |
| 3V3_LOCAL | N/A: etched PCB test feature | TP404 | 1 | NOT_APPLICABLE | N/A |
| 74437636351002 | Würth Elektronik | L201 | 1 | DOWNLOADED | [74437636351002](#doc-74437636351002) |
| 7447789004 | Würth Elektronik | L301 | 1 | DOWNLOADED | [7447789004](#doc-7447789004) |
| ADG4612BRUZ | Analog Devices | U321, U651 | 2 | OPEN | [adg4612](#doc-adg4612) |
| ALERT_LOCAL | N/A: etched PCB test feature | TP401 | 1 | NOT_APPLICABLE | N/A |
| B260-13-F | Diodes Incorporated | D304, D600, D660 | 3 | DOWNLOADED | [b260](#doc-b260) |
| B2B-XH-A(LF)(SN) | JST | J301, J302, J603, J604, J605, J606, JP600, JP660 | 8 | DOWNLOADED | [jst_xh](#doc-jst_xh) |
| B2P-VH-FB-B(LF)(SN) | JST | J501 | 1 | DOWNLOADED | [jst_vh](#doc-jst_vh) |
| B4B-XH-A(LF)(SN) | JST | J503 | 1 | DOWNLOADED | [jst_xh](#doc-jst_xh) |
| BAS116,215 | Nexperia | D301, D302, D322, D618, D619 | 5 | OPEN | [bas116](#doc-bas116) |
| BAT46W-E3-08 | Vishay | D303 | 1 | DOWNLOADED | [bat46w](#doc-bat46w) |
| BSC034N06NSATMA1 | Infineon | Q301, Q302 | 2 | OPEN | [bsc034](#doc-bsc034) |
| BSS138 | onsemi | Q102 | 1 | DOWNLOADED | [bss138](#doc-bss138) |
| C1608C0G1H102J080AA | TDK | C356 | 1 | OPEN | [C1608C0G1H102J080AA](#doc-c1608c0g1h102j080aa) |
| C1608C0G1H103J080AA | TDK | C350, C603 | 2 | OPEN | [C1608C0G1H103J080AA](#doc-c1608c0g1h103j080aa) |
| C3216X7R1H475K160AB | TDK | C351 | 1 | OPEN | [C3216X7R1H475K160AB](#doc-c3216x7r1h475k160ab) |
| C5750X7R1H226M250KB | TDK | C209, C210, C211, C212, C213, C214, C404 | 7 | OPEN | [C5750X7R1H226M250KB](#doc-c5750x7r1h226m250kb) |
| CGA3E2C0G1H220J080AA | TDK | C207 | 1 | OPEN | [CGA3E2C0G1H220J080AA](#doc-cga3e2c0g1h220j080aa) |
| CRCW06030000Z0EA | Vishay | R204 | 1 | DOWNLOADED | [crcw](#doc-crcw) |
| CRCW0603100RFKEA | Vishay | R374 | 1 | DOWNLOADED | [crcw](#doc-crcw) |
| CRCW060310R0FKEA | Vishay | R333 | 1 | DOWNLOADED | [crcw](#doc-crcw) |
| CRCW06031R00FKEA | Vishay | R306, R384 | 2 | DOWNLOADED | [crcw](#doc-crcw) |
| CRCW120610K0FKEA | Vishay | R323 | 1 | DOWNLOADED | [crcw](#doc-crcw) |
| CSD18540Q5B | Texas Instruments | Q303, Q330 | 2 | DOWNLOADED | [csd18540q5b](#doc-csd18540q5b) |
| CSD19537Q3 | Texas Instruments | Q101 | 1 | DOWNLOADED | [csd19537q3](#doc-csd19537q3) |
| CUSTOM-FX-CU-01 RevA | Project-authored custom item; fabricator OPEN | JP101, JP201, JP202, JP301, JP330, JP331, JP501 | 7 | OPEN | N/A |
| CUSTOM-FX-PAD-M4 RevA | Project-authored custom item; fabricator OPEN | PF1, PF2, PF3, PF4, PF5 | 5 | OPEN | N/A |
| EEUFR1E221 | Panasonic | C358, C359 | 2 | DOWNLOADED | [eeufr](#doc-eeufr) |
| FDB33N25TM | onsemi | Q316 | 1 | DOWNLOADED | [fdb33n25tm](#doc-fdb33n25tm) |
| GND | N/A: etched PCB test feature | TP504 | 1 | NOT_APPLICABLE | N/A |
| GRM1885C1H330JA01D | Murata | C357 | 1 | DOWNLOADED | [GRM1885C1H330JA01D](#doc-grm1885c1h330ja01d) |
| GRM188R71H104KA93D | Murata | C103, C203, C204, C205, C303, C304, C308, C354, C355, C364, C368, C369, C370, C376, C380, C401, C402, C405, C406, C604, C609, C644, C651, C710, C711, C712, C714, C715, C716, C717, C723, C728, C730, C731, C732, C733, C754, C756, C761, C762 | 40 | OPEN | [GRM188R71H104KA93D](#doc-grm188r71h104ka93d) |
| GRM21BR71E105KA99L | Murata | C206, C301, C309, C365, C367, C374, C375, C600 | 8 | DOWNLOADED | [GRM21BR71E105KA99L](#doc-grm21br71e105ka99l) |
| GRM21BR71E475KA73L | Murata | C302, C353, C366, C379 | 4 | DOWNLOADED | [GRM21BR71E475KA73L](#doc-grm21br71e475ka73l) |
| GRM21BR71H105KA12L | Murata | C307, C403 | 2 | DOWNLOADED | [GRM21BR71H105KA12L](#doc-grm21br71h105ka12l) |
| GRM32ER71H106KA12L | Murata | C201, C202, C305, C306, C352, C377, C601, C602, C660 | 9 | OPEN | [GRM32ER71H106KA12L](#doc-grm32er71h106ka12l) |
| GRM32ER72A105KA01L | Murata | C101, C102, C378 | 3 | DOWNLOADED | [GRM32ER72A105KA01L](#doc-grm32er72a105ka01l) |
| INA228AIDGSR | Texas Instruments | U401 | 1 | DOWNLOADED | [ina228](#doc-ina228) |
| INPUT_FLT | N/A: etched PCB test feature | TP102 | 1 | NOT_APPLICABLE | N/A |
| INPUT_SHDN | N/A: etched PCB test feature | TP101 | 1 | NOT_APPLICABLE | N/A |
| LM4040A25IDBZR | Texas Instruments | D321, D601 | 2 | DOWNLOADED | [lm4040](#doc-lm4040) |
| LM61460AANRJRR | Texas Instruments | U201 | 1 | DOWNLOADED | [lm61460](#doc-lm61460) |
| LOAD_5V1 | N/A: etched PCB test feature | TP503 | 1 | NOT_APPLICABLE | N/A |
| LT4363HMS-1#PBF | Analog Devices | U316 | 1 | OPEN | [lt4363](#doc-lt4363) |
| LTC3115IFE-1#PBF | Analog Devices | U317 | 1 | OPEN | [ltc3115](#doc-ltc3115) |
| LTC7001IMSE#PBF | Analog Devices | U301 | 1 | OPEN | [ltc7001](#doc-ltc7001) |
| N/A etched paired pads | N/A: etched PCB test feature | TP103, TP201, TP202, TP203, TP204, TP306, TP307, TP308, TP309, TP310, TP311, TP312, TP313, TP314, TP315, TP316, TP317, TP318, TP319, TP320, TP321, TP322, TP323, TP324, TP327, TP328, TP329, TP330, TP331, TP332, TP333, TP334, TP335, TP336, TP405, TP406, TP505 | 37 | NOT_APPLICABLE | N/A |
| PCH1V471MCL1GS | Nichicon | C330, C331, C332, C333, C334, C335, C336, C337, C340, C341, C342, C343 | 12 | DOWNLOADED | [pch](#doc-pch) |
| REF5025IDGKR | Texas Instruments | U302 | 1 | DOWNLOADED | [ref50](#doc-ref50) |
| SHUNT_KMINUS | N/A: etched PCB test feature | TP403 | 1 | NOT_APPLICABLE | N/A |
| SHUNT_KPLUS | N/A: etched PCB test feature | TP402 | 1 | NOT_APPLICABLE | N/A |
| SMCJ36CA | Vishay | D101 | 1 | OPEN | [smcj](#doc-smcj) |
| SN74LVC1G08DBVR | Texas Instruments | U617, U623, U628, U630, U631, U632, U633 | 7 | DOWNLOADED | [sn74lvc1g08](#doc-sn74lvc1g08) |
| SN74LVC1G14DBVR | Texas Instruments | U614, U616, U644, U654, U656, U661 | 6 | DOWNLOADED | [sn74lvc1g14](#doc-sn74lvc1g14) |
| SN74LVC1G17DBVR | Texas Instruments | U662 | 1 | DOWNLOADED | [sn74lvc1g17](#doc-sn74lvc1g17) |
| SN74LVC1G32DBVR | Texas Instruments | U615 | 1 | DOWNLOADED | [sn74lvc1g32](#doc-sn74lvc1g32) |
| SN74LVC1G74DCTR | Texas Instruments | U610, U611, U612 | 3 | DOWNLOADED | [sn74lvc1g74](#doc-sn74lvc1g74) |
| STPS60H100CT | STMicroelectronics | D102, D330, D331 | 3 | OPEN | [stps60](#doc-stps60) |
| TCA9517DGKR | Texas Instruments | U403 | 1 | DOWNLOADED | [tca9517](#doc-tca9517) |
| TLV3201AIDBVR | Texas Instruments | U303, U607 | 2 | DOWNLOADED | [tlv3201](#doc-tlv3201) |
| TNPW0603100KBEEA | Vishay | R108, R202, R206, R321, R322, R330, R346, R364, R367, R605, R606, R609, R623, R650, R718 | 15 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0603100RBEEA | Vishay | R304 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060310K0BEEA | Vishay | R107, R302, R307, R313, R316, R317, R363, R365, R370, R371, R372, R385, R404, R405, R408, R601, R603, R604, R648, R707, R708, R710, R713, R723, R727, R728, R729 | 27 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060310R0BEEA | Vishay | R402, R403 | 2 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0603143KBEEA | Vishay | R711 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060315K0BEEA | Vishay | R343, R344 | 2 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060315K8BEEA | Vishay | R104 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW06031K00BEEA | Vishay | R205, R303, R373, R622, R647, R649, R709, R712, R717, R730, R731 | 11 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060323K7BEEA | Vishay | R342 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0603249KBEEA | Vishay | R362 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060324K4BEEA | Vishay | R203 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060324K9BEEA | Vishay | R207 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060332K4BEEA | Vishay | R312, R600 | 2 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0603332KBEEA | Vishay | R101 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060333K2BEEA | Vishay | R201, R379 | 2 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060347R0BEEA | Vishay | R602 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060348K7BEEA | Vishay | R377 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW06034K02BEEA | Vishay | R105 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW06034K32BEEA | Vishay | R331 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW06034K70BEEA | Vishay | R406, R407 | 2 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060354K9BEEA | Vishay | R102 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060356K2BEEA | Vishay | R106 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060368K1BEEA | Vishay | R361 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW06036K49BEEA | Vishay | R375 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW060388K7BEEA | Vishay | R341 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW06039K88BEEA | Vishay | R301 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW08051M00BEEA | Vishay | R340 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0805348KBEEA | Vishay | R103 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0805365KBEEA | Vishay | R376, R378 | 2 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW0805383KBEEA | Vishay | R345 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TNPW12062M00BEEA | Vishay | R305 | 1 | DOWNLOADED | [tnpw](#doc-tnpw) |
| TPS259470LRPWR | Texas Instruments | U327 | 1 | DOWNLOADED | [tps25947](#doc-tps25947) |
| TPS26630RGER | Texas Instruments | U101 | 1 | DOWNLOADED | [tps2663](#doc-tps2663) |
| TPS3808G01DBVR | Texas Instruments | U322, U323 | 2 | DOWNLOADED | [tps3808](#doc-tps3808) |
| TPS3808G50DBVR | Texas Instruments | U602 | 1 | DOWNLOADED | [tps3808](#doc-tps3808) |
| TPS70933DBVR | Texas Instruments | U318, U402 | 2 | DOWNLOADED | [tps709](#doc-tps709) |
| TPS7A1601DGNR | Texas Instruments | U306, U600 | 2 | DOWNLOADED | [tps7a16](#doc-tps7a16) |
| TestPoint | N/A: etched PCB test feature | TP301, TP302, TP303, TP304, TP305 | 5 | NOT_APPLICABLE | N/A |
| UCC27511DBVR | Texas Instruments | U315, U330 | 2 | DOWNLOADED | [ucc27511](#doc-ucc27511) |
| VIN_PROTECTED | N/A: etched PCB test feature | TP502 | 1 | NOT_APPLICABLE | N/A |
| VIN_RAW | N/A: etched PCB test feature | TP501 | 1 | NOT_APPLICABLE | N/A |
| WFMB2512R0330FEA | Vishay | R308, R309, R310, R311, R380, R381, R382, R383, R386, R387, R388, R389, R390, R391, R392, R393 | 16 | DOWNLOADED | [wfm](#doc-wfm) |
| WSL2512R3300FEA | Vishay | R332 | 1 | DOWNLOADED | [wsl](#doc-wsl) |
| WSL27262L000FEA | Vishay | R401 | 1 | DOWNLOADED | [wsl2726](#doc-wsl2726) |

## Source documents and relevant pages

Each downloaded document is stored as `third_party/datasheets/<MPN>.pdf` for every MPN mapped to that document. Shared hashes intentionally identify identical family datasheets. Source files, retrieval attempts, PDF metadata and package drawing identifiers are recorded in the JSON.

<a id="doc-2n7002"></a>
### 2n7002 — Nexperia

**Revision/date:** Rev. 7; 8 September 2011 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Limiting values |
| Pinout / polarity | p1: SOT23 pin mapping |
| Package | p8: SOT23 outline |
| Layout / land pattern | p9: Reflow and wave soldering footprints |

<a id="doc-74437636351002"></a>
### 74437636351002 — Würth Elektronik

**Revision/date:** 001.000; 2025-02-07. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.we-online.com/components/products/datasheet/74437636351002.pdf).

**SHA-256:** `b32dd62136d8b614b362d43296187b6c8557cf4dab98fbf7ed20a70e655e02d8`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [74437636351002.pdf](../../third_party/datasheets/74437636351002.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,7: Electrical limits, current/temperature curves and cautions |
| Pinout / polarity | p1: Terminal 1/2 drawing |
| Package | p1: WE-HCFT dimensions |
| Layout / land pattern | p1: Recommended plated-hole pattern and current-test copper conditions |

<a id="doc-7447789004"></a>
### 7447789004 — Würth Elektronik

**Revision/date:** 007.000; 2023-05-30. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.we-online.com/components/products/datasheet/7447789004.pdf).

**SHA-256:** `def0ae180c1b4298cb9ac319b87723ee916c65344acb67c94b1fb24ec63b0d63`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [7447789004.pdf](../../third_party/datasheets/7447789004.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,5: Electrical limits, current/temperature curves and cautions |
| Pinout / polarity | p1: Winding-start marking and terminal geometry |
| Package | p1: WE-PD 7332 dimensions |
| Layout / land pattern | p1: Recommended land pattern |

<a id="doc-adg4612"></a>
### adg4612 — Analog Devices

**Revision/date:** Rev. 0; October 2010 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG4612_4613.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p9: Absolute maximum ratings |
| Pinout / polarity | p10: ADG4612 TSSOP pin configuration |
| Package | p21: RU-16 TSSOP outline |
| Layout / land pattern | —: OPEN: no dedicated layout section located in remote text; inspect application guidance and mechanical drawing after download |

<a id="doc-b260"></a>
### b260 — Diodes Incorporated

**Revision/date:** DS13004 Rev. 22-2; July 2015. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.diodes.com/assets/Datasheets/ds13004.pdf).

**SHA-256:** `19ab27e98e717e7012275062b715964897882f3ce95eab846f71d5f2b485ab5b`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [B260-13-F.pdf](../../third_party/datasheets/B260-13-F.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Maximum and electrical ratings; B260 column |
| Pinout / polarity | p1: Cathode mark/polarity |
| Package | p4: SMB outline |
| Layout / land pattern | p4: Suggested pad layout |

<a id="doc-bas116"></a>
### bas116 — Nexperia

**Revision/date:** 5 August 2020 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://assets.nexperia.com/documents/data-sheet/BAS116.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Limiting values |
| Pinout / polarity | p1: Anode, NC and cathode pins |
| Package | p6: SOT23 outline |
| Layout / land pattern | p7: Reflow and wave soldering footprints |

<a id="doc-bat46w"></a>
### bat46w — Vishay

**Revision/date:** 86406 Rev. 1.1; 20-Nov-2025. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/86406/bat46w.pdf).

**SHA-256:** `4913578755adb8c128c72614222a1dc19a4a39c296962234bfe44d4e7f2ffd84`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [BAT46W-E3-08.pdf](../../third_party/datasheets/BAT46W-E3-08.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2: Absolute maximum and electrical ratings |
| Pinout / polarity | p1,4: Diode orientation and cathode bar |
| Package | p4: SOD-123 outline |
| Layout / land pattern | p4: Footprint recommendation |

<a id="doc-bsc034"></a>
### bsc034 — Infineon

**Revision/date:** Final Rev. 2.3; 2020-05-06 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsc034n06ns-datasheet-en.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p3: Maximum ratings |
| Pinout / polarity | p1: PG-TDSON-8 pin mapping |
| Package | p10,11: Package outline and mounting drawing |
| Layout / land pattern | p10,11: Package/mounting drawings; owner must inspect graphics after download |

<a id="doc-bss138"></a>
### bss138 — onsemi

**Revision/date:** BSS138/D Rev. 7; April 2024; package CASE 318 issue AU, 14-Aug-2024. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.onsemi.com/pdf/datasheet/bss138-d.pdf).

**SHA-256:** `d1bff01c42324bc87d9fef988b6ec27425a2d8e91a9ff422b709fd1f8d1d59a5`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [BSS138.pdf](../../third_party/datasheets/BSS138.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2,3: Absolute maximum and diode ratings |
| Pinout / polarity | p1: Device pinout; use device-specific mapping |
| Package | p6,7: SOT-23 outline and generic style options |
| Layout / land pattern | p6: Recommended mounting footprint; visually checked |

onsemi manufacturer reference established in docs/evidence/r2/source_register.json; schematic omits manufacturer field.

<a id="doc-c1608c0g1h102j080aa"></a>
### C1608C0G1H102J080AA — TDK

**Revision/date:** Characterization sheet; May 21, 2019 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://product.tdk.com/info/en/documents/chara_sheet/C1608C0G1H102J080AA.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Rated voltage, temperature characteristic and typical curves; not an IC abs-max table |
| Pinout / polarity | p1: Nonpolar two-terminal device |
| Package | p1: Body dimensions |
| Layout / land pattern | —: OPEN: land pattern is on the exact-product web page, not this characterization sheet |

<a id="doc-c1608c0g1h103j080aa"></a>
### C1608C0G1H103J080AA — TDK

**Revision/date:** OPEN: revision/date unavailable; HTTP 403. **Download:** OPEN.

Official source: [manufacturer PDF](https://product.tdk.com/info/en/documents/chara_sheet/C1608C0G1H103J080AA.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | —: OPEN: download and inspect ratings |
| Pinout / polarity | —: Nonpolar MLCC; exact terminal drawing OPEN |
| Package | —: OPEN: download and inspect dimensions |
| Layout / land pattern | —: OPEN: use exact-product page for land pattern, then record source |

<a id="doc-c3216x7r1h475k160ab"></a>
### C3216X7R1H475K160AB — TDK

**Revision/date:** OPEN: revision/date unavailable; HTTP 403. **Download:** OPEN.

Official source: [manufacturer PDF](https://product.tdk.com/info/en/documents/chara_sheet/C3216X7R1H475K160AB.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | —: OPEN: download and inspect ratings |
| Pinout / polarity | —: Nonpolar MLCC; exact terminal drawing OPEN |
| Package | —: OPEN: download and inspect dimensions |
| Layout / land pattern | —: OPEN: use exact-product page for land pattern, then record source |

<a id="doc-c5750x7r1h226m250kb"></a>
### C5750X7R1H226M250KB — TDK

**Revision/date:** Characterization sheet; March 19, 2019 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://product.tdk.com/info/en/documents/chara_sheet/C5750X7R1H226M250KB.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Rated voltage, temperature characteristic and typical curves; not an IC abs-max table |
| Pinout / polarity | p1: Nonpolar two-terminal device |
| Package | p1: Body dimensions |
| Layout / land pattern | —: OPEN: land pattern is on the exact-product web page, not this characterization sheet |

<a id="doc-cga3e2c0g1h220j080aa"></a>
### CGA3E2C0G1H220J080AA — TDK

**Revision/date:** OPEN: revision/date unavailable; HTTP 403. **Download:** OPEN.

Official source: [manufacturer PDF](https://product.tdk.com/info/en/documents/chara_sheet/CGA3E2C0G1H220J080AA.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | —: OPEN: download and inspect ratings |
| Pinout / polarity | —: Nonpolar MLCC; exact terminal drawing OPEN |
| Package | —: OPEN: download and inspect dimensions |
| Layout / land pattern | —: OPEN: use exact-product page for land pattern, then record source |

<a id="doc-crcw"></a>
### crcw — Vishay

**Revision/date:** 20035; revision 14-Apr-2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/20035/dcrcwe3.pdf).

**SHA-256:** `cddb122cd628e47beffa463ec023e01a1cfe8ebfece01124df0aa9c12f315ff6`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [CRCW06030000Z0EA.pdf](../../third_party/datasheets/CRCW06030000Z0EA.pdf), [CRCW0603100RFKEA.pdf](../../third_party/datasheets/CRCW0603100RFKEA.pdf), [CRCW060310R0FKEA.pdf](../../third_party/datasheets/CRCW060310R0FKEA.pdf), [CRCW06031R00FKEA.pdf](../../third_party/datasheets/CRCW06031R00FKEA.pdf), [CRCW120610K0FKEA.pdf](../../third_party/datasheets/CRCW120610K0FKEA.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,5,6: Ratings, jumper-current limits, derating and pulse curves |
| Pinout / polarity | p11: Two nonpolar terminals; no numbered electrical pinout |
| Package | p11: 0603/1206 body dimensions |
| Layout / land pattern | p11: Reflow/wave solder-pad dimensions |

Standard D/CRCW e3 family, not CRCW...C commodity variant; ordering code on p3.

<a id="doc-csd18540q5b"></a>
### csd18540q5b — Texas Instruments

**Revision/date:** SLPS488B; revised April 2017. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/csd18540q5b.pdf).

**SHA-256:** `2e43c4a2ac82af8a089be0a9e413282326f8d7857254ac07390b458deca854e0`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [CSD18540Q5B.pdf](../../third_party/datasheets/CSD18540Q5B.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Absolute maximum ratings |
| Pinout / polarity | p1: Top view and terminal mapping |
| Package | p8: Q5B SON outline |
| Layout / land pattern | p9: PCB and stencil patterns |

<a id="doc-csd19537q3"></a>
### csd19537q3 — Texas Instruments

**Revision/date:** SLPS549B; revised November 2022. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/csd19537q3.pdf).

**SHA-256:** `d74d65b7815d46d642a11c89834ee71245ae6d3541595df2b4fcfa21dfbd4903`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [CSD19537Q3.pdf](../../third_party/datasheets/CSD19537Q3.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Absolute maximum ratings |
| Pinout / polarity | p1: Top view and terminal mapping |
| Package | p8: Q3 SON outline |
| Layout / land pattern | p9: PCB and stencil patterns |

<a id="doc-eeufr"></a>
### eeufr — Panasonic

**Revision/date:** FR-A series / ABA0000C1259; 01-Sep-2025. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1259.pdf).

**SHA-256:** `47cf18461482e03270f72e475f855080e11e2154e3f343f735e5cb0e61e27df7`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [EEUFR1E221.pdf](../../third_party/datasheets/EEUFR1E221.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,5,8,10: Series ratings, exact EEUFR1E221 row, application/lifetime conditions |
| Pinout / polarity | p1,11: Polarity drawing and assembly polarity cautions |
| Package | p1,5: Radial case and exact-row lead spacing |
| Layout / land pattern | p1,5,11: Lead geometry and mounting cautions; finished PCB drill diameter is not specified |

<a id="doc-fdb33n25tm"></a>
### fdb33n25tm — onsemi

**Revision/date:** FDB33N25/D Rev. 3; January 2022; CASE 418AJ issue F, 11-Mar-2021. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.onsemi.com/download/data-sheet/pdf/fdb33n25-d.pdf).

**SHA-256:** `08982131cc18dcbfb47dfbe8f968732b6e66c7508cf0179e00e38c4f0c99dead`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [FDB33N25TM.pdf](../../third_party/datasheets/FDB33N25TM.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2,3: Maximum and diode ratings |
| Pinout / polarity | p1: G/D/S mapping |
| Package | p8: D2PAK-3 outline |
| Layout / land pattern | p8: Recommended mounting footprint; visually checked |

<a id="doc-grm1885c1h330ja01d"></a>
### GRM1885C1H330JA01D — Murata

**Revision/date:** GRM1885C1H330JA01-01A; specifications as of Jun.19,2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM1885C1H330JA01-01A.pdf).

**SHA-256:** `e119014a9ad26bd47ad64ab49bc5c37f93c9039c1c5cc3c15a7e78def1fa66bc`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [GRM1885C1H330JA01D.pdf](../../third_party/datasheets/GRM1885C1H330JA01D.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2,3,4,9,10: Rated values, tests and operating cautions |
| Pinout / polarity | p2: Two nonpolar terminals |
| Package | p2: Exact part dimensions and packaging code |
| Layout / land pattern | p26,27: PCB design and land dimensions |

<a id="doc-grm188r71h104ka93d"></a>
### GRM188R71H104KA93D — Murata

**Revision/date:** GRM188R71H104KA93-01; Feb.28,2016 (manufacturer reference sheet indexed at Mouser; local retrieval failed). **Download:** OPEN.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R71H104KA93-01.pdf).
Distributor mirror attempt: [manufacturer document at distributor](https://www.mouser.com/datasheet/2/281/1/GRM188R71H104KA93_01-3155748.pdf).
Revision evidence: [source record](https://www.mouser.com/datasheet/2/281/1/GRM188R71H104KA93_01-3155748.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Rated values |
| Pinout / polarity | p1: Two nonpolar terminals |
| Package | p1: Exact part dimensions and package code |
| Layout / land pattern | —: OPEN: inspect full reference sheet after browser download |

<a id="doc-grm21br71e105ka99l"></a>
### GRM21BR71E105KA99L — Murata

**Revision/date:** GRM21BR71E105KA99-01; specifications as of Mar.3,2016. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM21BR71E105KA99-01.pdf).

**SHA-256:** `4ae17d407c021cd0a24240147bb043038f30275f648a162660e656f37bd6fee2`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [GRM21BR71E105KA99L.pdf](../../third_party/datasheets/GRM21BR71E105KA99L.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3,11,12: Rated values, tests and voltage/temperature cautions |
| Pinout / polarity | p1: Two nonpolar terminals |
| Package | p1: Exact part dimensions and packaging code |
| Layout / land pattern | p25,26: PCB design and land dimensions |

<a id="doc-grm21br71e475ka73l"></a>
### GRM21BR71E475KA73L — Murata

**Revision/date:** GRM21BR71E475KA73-01; specifications as of Mar.5,2016. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM21BR71E475KA73-01.pdf).

**SHA-256:** `020fa2705366af3b3fa93f05d46a44c40a87dc121ea2543cf52eedc10cb22c15`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [GRM21BR71E475KA73L.pdf](../../third_party/datasheets/GRM21BR71E475KA73L.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3,11,12: Rated values, tests and voltage/temperature cautions |
| Pinout / polarity | p1: Two nonpolar terminals |
| Package | p1: Exact part dimensions and packaging code |
| Layout / land pattern | p25,26: PCB design and land dimensions |

<a id="doc-grm21br71h105ka12l"></a>
### GRM21BR71H105KA12L — Murata

**Revision/date:** GRM21BR71H105KA12-01; specifications as of Mar.7,2016. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM21BR71H105KA12-01.pdf).

**SHA-256:** `9921ee74a9703bfed89f091cba34075e54707b2487c428a984253470da53c52e`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [GRM21BR71H105KA12L.pdf](../../third_party/datasheets/GRM21BR71H105KA12L.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3,11,12: Rated values, tests and voltage/temperature cautions |
| Pinout / polarity | p1: Two nonpolar terminals |
| Package | p1: Exact part dimensions and packaging code |
| Layout / land pattern | p25,26: PCB design and land dimensions |

<a id="doc-grm32er71h106ka12l"></a>
### GRM32ER71H106KA12L — Murata

**Revision/date:** GRM32ER71H106KA12-04A; Nov.22,2017 (manufacturer web index; URL returns HTTP 404 locally). **Download:** OPEN.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER71H106KA12-04A.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Rated values |
| Pinout / polarity | p1: Two nonpolar terminals |
| Package | p1: Exact part dimensions and package code |
| Layout / land pattern | —: OPEN: current downloadable reference sheet and land-pattern pages must be recovered |

<a id="doc-grm32er72a105ka01l"></a>
### GRM32ER72A105KA01L — Murata

**Revision/date:** GRM32ER72A105KA01-01A; specifications as of Jun.26,2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER72A105KA01-01A.pdf).

**SHA-256:** `cec81b201f2646123970829c05cae803e3f25f59403617d12e68809cb6ad9176`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [GRM32ER72A105KA01L.pdf](../../third_party/datasheets/GRM32ER72A105KA01L.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2,3,4,9,10: Rated values, tests and operating cautions |
| Pinout / polarity | p2: Two nonpolar terminals |
| Package | p2: Exact part dimensions and packaging code |
| Layout / land pattern | p26,27: PCB design and land dimensions |

<a id="doc-ina228"></a>
### ina228 — Texas Instruments

**Revision/date:** SLYS021A; revised May 2022. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/ina228.pdf).

**SHA-256:** `a138d39eeee04f8388426fed204c2f4012e75d36e95b60b0751ef003cd277447`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [INA228AIDGSR.pdf](../../third_party/datasheets/INA228AIDGSR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p3,4: Absolute maximum and recommended conditions |
| Pinout / polarity | p3: DGS pin configuration and functions |
| Package | p45: DGS0010A outline |
| Layout / land pattern | p39,46: Application layout and DGS board pattern |

<a id="doc-jst_vh"></a>
### jst_vh — JST

**Revision/date:** No printed controlled revision; PDF creation/modification date 2026-01-09. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf).

**SHA-256:** `d51e669c597988b20c0963daf5bef7356cbd2104c1f867e9107c6fa6cd2b899c`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [B2P-VH-FB-B(LF)(SN).pdf](../../third_party/datasheets/B2P-VH-FB-B%28LF%29%28SN%29.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Connector ratings and operating conditions |
| Pinout / polarity | p4: Shrouded header No. 1 circuit position |
| Package | p4: B2P-VH-FB-B drawing |
| Layout / land pattern | p4: Shrouded header PCB hole pattern |

Series sheet omits LF/SN suffix in dimensional table; retain schematic suffix. Document metadata date is not a claimed controlled revision.

<a id="doc-jst_xh"></a>
### jst_xh — JST

**Revision/date:** No printed controlled revision; PDF creation/modification date 2025-07-30. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf).

**SHA-256:** `9426b136902f11900825077535e5c65032b7fbc31ffb59c5e9e1f463bb20fb90`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [B2B-XH-A(LF)(SN).pdf](../../third_party/datasheets/B2B-XH-A%28LF%29%28SN%29.pdf), [B4B-XH-A(LF)(SN).pdf](../../third_party/datasheets/B4B-XH-A%28LF%29%28SN%29.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Connector ratings and operating conditions |
| Pinout / polarity | p5: Top-entry B2B-XH-A / B4B-XH-A No. 1 circuit |
| Package | p5: Top-entry header dimensions |
| Layout / land pattern | p2: Through-hole top-entry PCB pattern |

Use top-entry headers without boss for the captured MPNs. LF/SN suffix is retained from the schematic; metadata date is not a controlled revision.

<a id="doc-lm4040"></a>
### lm4040 — Texas Instruments

**Revision/date:** SLOS456Q; revised April 2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/lm4040.pdf).

**SHA-256:** `f43b6b6d3ecd51c8c90b70a7c4630c7e3140822b0073953ed2459df81b251c1c`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [LM4040A25IDBZR.pdf](../../third_party/datasheets/LM4040A25IDBZR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5: Absolute maximum and recommended conditions |
| Pinout / polarity | p4: DBZ pin configuration |
| Package | p53: DBZ0003A SOT-23 outline |
| Layout / land pattern | p28,29,54: Application layout and DBZ board pattern |

<a id="doc-lm61460"></a>
### lm61460 — Texas Instruments

**Revision/date:** SNVSBD5D; revised July 2022. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/lm61460.pdf).

**SHA-256:** `2c8a0bf340c70aa3ac29e586146804d7651822e14bee0897f6415ee9e56be84d`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [LM61460AANRJRR.pdf](../../third_party/datasheets/LM61460AANRJRR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p4: Absolute maximum and recommended conditions |
| Pinout / polarity | p3: RJR pin configuration and functions |
| Package | p55: RJR0014A outline |
| Layout / land pattern | p47,48,49,56: Switching-loop/layout guidance, examples and RJR land pattern |

<a id="doc-lt4363"></a>
### lt4363 — Analog Devices

**Revision/date:** Rev. C; manufacturer product page dated 2024-01-18 (remote PDF/product record). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf).
Revision evidence: [source record](https://www.analog.com/en/products/lt4363.html).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Absolute maximum ratings |
| Pinout / polarity | p2: LT4363-1 MS pin configuration |
| Package | p22: MS 12-lead package |
| Layout / land pattern | p16,22: Layout considerations and MS solder-pad layout |

<a id="doc-ltc3115"></a>
### ltc3115 — Analog Devices

**Revision/date:** Rev. E; manufacturer product page dated 2023-04-07 (remote PDF/product record). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf).
Revision evidence: [source record](https://www.analog.com/en/products/ltc3115-1.html).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Absolute maximum ratings |
| Pinout / polarity | p2: FE pin configuration and exposed pad |
| Package | p40: FE 20-lead TSSOP outline |
| Layout / land pattern | p30,32,40: PCB guidance, FE layout example and FE solder-pad layout |

<a id="doc-ltc7001"></a>
### ltc7001 — Analog Devices

**Revision/date:** Rev. G; November 2021 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Absolute maximum ratings |
| Pinout / polarity | p2: MSE pin configuration and exposed pad |
| Package | p16: MSE package |
| Layout / land pattern | p14,16: PC board layout considerations and package pad layout |

<a id="doc-pch"></a>
### pch — Nichicon

**Revision/date:** PCH catalog; May 2024 (no separate revision identifier). **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.nichicon.co.jp/english/_assets/images/products/catalog/corporate/digital/PCH_e.pdf).

**SHA-256:** `418b2838c3d9044b26e9b396a8f94fa24dddfd728cc3ef076c640205f5612bf4`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [PCH1V471MCL1GS.pdf](../../third_party/datasheets/PCH1V471MCL1GS.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2: Series ratings and exact PCH1V471MCL1GS row |
| Pinout / polarity | p1: Positive/negative marks and terminal drawing |
| Package | p1,2: Standard 10 x 16 mm case; exact row on p2 |
| Layout / land pattern | —: OPEN: dedicated recommended PCB land pattern not supplied in this two-page sheet; terminal geometry is on p1 |

<a id="doc-phoenix1776508"></a>
### phoenix1776508 — Phoenix Contact

**Revision/date:** Catalog-generated PDF dated Oct 3, 2025, 12:01 PM (manufacturer web index; local HTTP 403). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.phoenixcontact.com/us/products/1776508/pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1: Headline ratings; full electrical conditions require browser copy |
| Pinout / polarity | —: OPEN: locate pin numbering in browser-downloaded PDF |
| Package | —: OPEN: locate current dimensional drawing |
| Layout / land pattern | —: OPEN: locate current PCB drilling pattern |

Manufacturer PDF indexed as 15 pages; generated date is not a controlled hardware revision.

<a id="doc-ref50"></a>
### ref50 — Texas Instruments

**Revision/date:** SBOS410O; revised October 2025. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/ref50.pdf).

**SHA-256:** `d2da9488194dba11732c85c498b563c12e0bb6b3e2d21631022dde9bff51a13d`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [REF5025IDGKR.pdf](../../third_party/datasheets/REF5025IDGKR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5: Absolute maximum and recommended conditions |
| Pinout / polarity | p4: DGK pin configuration |
| Package | p49: DGK0008A VSSOP outline |
| Layout / land pattern | p29,30,31,50: Application layout and DGK board pattern |

<a id="doc-smcj"></a>
### smcj — Vishay

**Revision/date:** 88394; revision 09-Jan-2024. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/88394/smcj.pdf).

**SHA-256:** `d9b1dafa25c0fa45eeb22fc4258fbdee3cafffb0bd14741e3cd9e35ea98f8e4c`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [SMCJ36CA.pdf](../../third_party/datasheets/SMCJ36CA.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2: Maximum ratings and SMCJ36CA row |
| Pinout / polarity | p1: CA is bidirectional; unidirectional cathode instructions do not apply |
| Package | p5: DO-214AB (SMC) outline |
| Layout / land pattern | p5: Mounting-pad layout |

OPEN manufacturer selection: SMCJ36CA is a multi-manufacturer base designation and the schematic has no Manufacturer field. This is a Vishay reference document only; it does not select Vishay or qualify a substitute.

<a id="doc-sn74lvc1g08"></a>
### sn74lvc1g08 — Texas Instruments

**Revision/date:** SCES217AA; revised August 2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf).

**SHA-256:** `30b963cc44233cf3ca35c891ff987c8323a2244ecc765e23296ec96ca4b42666`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [SN74LVC1G08DBVR.pdf](../../third_party/datasheets/SN74LVC1G08DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p4,5: Absolute maximum and recommended conditions |
| Pinout / polarity | p3: DBV pin configuration |
| Package | p27: DBV0005A SOT-23 outline |
| Layout / land pattern | p14,15,28: Application layout and DBV board pattern |

<a id="doc-sn74lvc1g14"></a>
### sn74lvc1g14 — Texas Instruments

**Revision/date:** SCES218AA; revised October 2025. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf).

**SHA-256:** `d64e41f0a267e8c5f73873058561642c57e093a2b7ecb4715d7ab62f0ef31a4f`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [SN74LVC1G14DBVR.pdf](../../third_party/datasheets/SN74LVC1G14DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5,6: Absolute maximum and recommended conditions |
| Pinout / polarity | p3,4: DBV pin configuration and functions |
| Package | p39: DBV0005A SOT-23 outline |
| Layout / land pattern | p13,14,40: Application layout and DBV board pattern |

<a id="doc-sn74lvc1g17"></a>
### sn74lvc1g17 — Texas Instruments

**Revision/date:** SCES351Y; revised October 2025. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf).

**SHA-256:** `c76fa723fac4502423967a1aa087dd669106b52b8de620c024b26e56f5d59309`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [SN74LVC1G17DBVR.pdf](../../third_party/datasheets/SN74LVC1G17DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p4,5: Absolute maximum and recommended conditions |
| Pinout / polarity | p3: DBV pin configuration |
| Package | p23: DBV0005A SOT-23 outline |
| Layout / land pattern | p12,24: Application layout and DBV board pattern |

<a id="doc-sn74lvc1g32"></a>
### sn74lvc1g32 — Texas Instruments

**Revision/date:** SCES219W; revised August 2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/sn74lvc1g32.pdf).

**SHA-256:** `b64786a568abe6a715c6f15dbc8ab1ffde3ad1017a1128a98931200e12c4c416`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [SN74LVC1G32DBVR.pdf](../../third_party/datasheets/SN74LVC1G32DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5,6: Absolute maximum and recommended conditions |
| Pinout / polarity | p3,4: DBV pin configuration and functions |
| Package | p41: DBV0005A SOT-23 outline |
| Layout / land pattern | p15,16,42: Application layout and DBV board pattern |

<a id="doc-sn74lvc1g74"></a>
### sn74lvc1g74 — Texas Instruments

**Revision/date:** SCES794G; revised September 2021. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf).

**SHA-256:** `e46a5a867fec742290000dca5ed3b291535f3c4418ef2ae267acc4ab51b26d8a`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [SN74LVC1G74DCTR.pdf](../../third_party/datasheets/SN74LVC1G74DCTR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5,6: Absolute maximum and recommended conditions |
| Pinout / polarity | p4: DCT pin configuration |
| Package | p19: DCT0008A SSOP outline |
| Layout / land pattern | p13,20: Application layout and DCT board pattern |

<a id="doc-stps60"></a>
### stps60 — STMicroelectronics

**Revision/date:** DS3978 Rev. 3; August 2018 (remote PDF). **Download:** OPEN.

Official source: [manufacturer PDF](https://www.st.com/resource/en/datasheet/stps60h100c.pdf).

**SHA-256: OPEN — no local PDF bytes.**

Evidence: Remote metadata/page references where stated; local bytes unavailable and SHA-256 OPEN.

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p2: Absolute ratings |
| Pinout / polarity | p1: Common-cathode A1/K/A2 mapping |
| Package | p5,6: TO-220AB outline and mechanical data |
| Layout / land pattern | —: OPEN: dedicated PCB land/hole pattern not found in remote datasheet text |

<a id="doc-tca9517"></a>
### tca9517 — Texas Instruments

**Revision/date:** SCPS242D; revised July 2017. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tca9517.pdf).

**SHA-256:** `fde93fd601168d6f457bbf38377f8ee5eb14ab2589ed52974fdf9c847163f22c`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TCA9517DGKR.pdf](../../third_party/datasheets/TCA9517DGKR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p4,5: Absolute maximum and recommended conditions |
| Pinout / polarity | p4: DGK pin configuration |
| Package | p25: DGK0008A VSSOP outline |
| Layout / land pattern | p16,26: Application layout and DGK board pattern |

<a id="doc-tlv3201"></a>
### tlv3201 — Texas Instruments

**Revision/date:** SBOS561C; revised May 2024. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tlv3201.pdf).

**SHA-256:** `1777bba814c74772bb54c6f1f56702985039043ce2fb2affaf996a83eaf1076e`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TLV3201AIDBVR.pdf](../../third_party/datasheets/TLV3201AIDBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p4: Absolute maximum and recommended conditions |
| Pinout / polarity | p3: TLV3201 DBV pin configuration |
| Package | p34: DBV0005A SOT-23 outline |
| Layout / land pattern | p18,19,35: Application layout and DBV board pattern |

<a id="doc-tnpw"></a>
### tnpw — Vishay

**Revision/date:** 28758; revision 10-Apr-2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/28758/tnpw_e3.pdf).

**SHA-256:** `6f0508c568cb355aaf2accdd33fe3a780d3ea5ef207c4c9a71839a8acadc33a5`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TNPW0603100KBEEA.pdf](../../third_party/datasheets/TNPW0603100KBEEA.pdf), [TNPW0603100RBEEA.pdf](../../third_party/datasheets/TNPW0603100RBEEA.pdf), [TNPW060310K0BEEA.pdf](../../third_party/datasheets/TNPW060310K0BEEA.pdf), [TNPW060310R0BEEA.pdf](../../third_party/datasheets/TNPW060310R0BEEA.pdf), [TNPW0603143KBEEA.pdf](../../third_party/datasheets/TNPW0603143KBEEA.pdf), [TNPW060315K0BEEA.pdf](../../third_party/datasheets/TNPW060315K0BEEA.pdf), [TNPW060315K8BEEA.pdf](../../third_party/datasheets/TNPW060315K8BEEA.pdf), [TNPW06031K00BEEA.pdf](../../third_party/datasheets/TNPW06031K00BEEA.pdf), [TNPW060323K7BEEA.pdf](../../third_party/datasheets/TNPW060323K7BEEA.pdf), [TNPW0603249KBEEA.pdf](../../third_party/datasheets/TNPW0603249KBEEA.pdf), [TNPW060324K4BEEA.pdf](../../third_party/datasheets/TNPW060324K4BEEA.pdf), [TNPW060324K9BEEA.pdf](../../third_party/datasheets/TNPW060324K9BEEA.pdf), [TNPW060332K4BEEA.pdf](../../third_party/datasheets/TNPW060332K4BEEA.pdf), [TNPW0603332KBEEA.pdf](../../third_party/datasheets/TNPW0603332KBEEA.pdf), [TNPW060333K2BEEA.pdf](../../third_party/datasheets/TNPW060333K2BEEA.pdf), [TNPW060347R0BEEA.pdf](../../third_party/datasheets/TNPW060347R0BEEA.pdf), [TNPW060348K7BEEA.pdf](../../third_party/datasheets/TNPW060348K7BEEA.pdf), [TNPW06034K02BEEA.pdf](../../third_party/datasheets/TNPW06034K02BEEA.pdf), [TNPW06034K32BEEA.pdf](../../third_party/datasheets/TNPW06034K32BEEA.pdf), [TNPW06034K70BEEA.pdf](../../third_party/datasheets/TNPW06034K70BEEA.pdf), [TNPW060354K9BEEA.pdf](../../third_party/datasheets/TNPW060354K9BEEA.pdf), [TNPW060356K2BEEA.pdf](../../third_party/datasheets/TNPW060356K2BEEA.pdf), [TNPW060368K1BEEA.pdf](../../third_party/datasheets/TNPW060368K1BEEA.pdf), [TNPW06036K49BEEA.pdf](../../third_party/datasheets/TNPW06036K49BEEA.pdf), [TNPW060388K7BEEA.pdf](../../third_party/datasheets/TNPW060388K7BEEA.pdf), [TNPW06039K88BEEA.pdf](../../third_party/datasheets/TNPW06039K88BEEA.pdf), [TNPW08051M00BEEA.pdf](../../third_party/datasheets/TNPW08051M00BEEA.pdf), [TNPW0805348KBEEA.pdf](../../third_party/datasheets/TNPW0805348KBEEA.pdf), [TNPW0805365KBEEA.pdf](../../third_party/datasheets/TNPW0805365KBEEA.pdf), [TNPW0805383KBEEA.pdf](../../third_party/datasheets/TNPW0805383KBEEA.pdf), [TNPW12062M00BEEA.pdf](../../third_party/datasheets/TNPW12062M00BEEA.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3,6,7,8: Ratings, limiting voltage, TCR, derating and pulse curves |
| Pinout / polarity | p15: Two nonpolar terminals; no numbered electrical pinout |
| Package | p15: 0603, 0805 and 1206 body dimensions |
| Layout / land pattern | p15: Reflow/wave solder-pad dimensions |

Family datasheet covers all listed TNPW values; ordering-code fields are on p4. It does not establish exact-MPN availability or circuit suitability.

<a id="doc-tps25947"></a>
### tps25947 — Texas Instruments

**Revision/date:** SLVSFC9C; revised May 2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tps25947.pdf).

**SHA-256:** `8f96de389903091650d4f462dcfad3210071c3ae7093623a7978f34baf8a65b4`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TPS259470LRPWR.pdf](../../third_party/datasheets/TPS259470LRPWR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p7,8: Absolute maximum and recommended conditions |
| Pinout / polarity | p5,6: RPW pin configuration and functions |
| Package | p72: RPW0010A WQFN outline |
| Layout / land pattern | p62,63,64,73: Power-path/layout guidance and RPW land pattern |

<a id="doc-tps2663"></a>
### tps2663 — Texas Instruments

**Revision/date:** SLVSE94G; revised June 2024. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tps2663.pdf).

**SHA-256:** `bb61314ace65ed37684bd07f541fc676081d7cf81cb24020e7c5c2065bfe16b2`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TPS26630RGER.pdf](../../third_party/datasheets/TPS26630RGER.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5: Absolute maximum and recommended conditions |
| Pinout / polarity | p3,4: RGE pin configuration and functions; distinguish PW alternative |
| Package | p52: RGE0024H VQFN outline |
| Layout / land pattern | p38,39,40,53: Application layouts and RGE land pattern |

<a id="doc-tps3808"></a>
### tps3808 — Texas Instruments

**Revision/date:** SBVS050N; revised August 2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tps3808.pdf).

**SHA-256:** `74d889c0f68af88032f1633c26381817cc03e10d9fd3b4c177a044ad3ed86eed`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TPS3808G01DBVR.pdf](../../third_party/datasheets/TPS3808G01DBVR.pdf), [TPS3808G50DBVR.pdf](../../third_party/datasheets/TPS3808G50DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5: Absolute maximum and recommended conditions |
| Pinout / polarity | p4: DBV pin configuration |
| Package | p36: DBV0006A SOT-23 outline |
| Layout / land pattern | p15,16,37: Application layout and DBV board pattern |

<a id="doc-tps709"></a>
### tps709 — Texas Instruments

**Revision/date:** SBVS186H; revised July 2021. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tps709.pdf).

**SHA-256:** `8c14e3efae738a27b857b789aa87369de9037a8ef3616a9f71a423587cdc6949`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TPS70933DBVR.pdf](../../third_party/datasheets/TPS70933DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p4: Absolute maximum and recommended conditions |
| Pinout / polarity | p3: DBV pin configuration |
| Package | p33: DBV0005A SOT-23 outline |
| Layout / land pattern | p16,34: Application layout and DBV board pattern |

<a id="doc-tps7a16"></a>
### tps7a16 — Texas Instruments

**Revision/date:** SBVS171F; revised October 2015. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/tps7a16.pdf).

**SHA-256:** `4e05cfdef8f64684f9f24b7d1f86e83badb7784c09c96f2ddbcbdbc0a3b48f80`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [TPS7A1601DGNR.pdf](../../third_party/datasheets/TPS7A1601DGNR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p5: Absolute maximum and recommended conditions |
| Pinout / polarity | p4: DGN pin configuration and thermal pad |
| Package | p34: DGN0008C HVSSOP outline |
| Layout / land pattern | p19,20,21,35: Application layouts and DGN land pattern |

<a id="doc-ucc27511"></a>
### ucc27511 — Texas Instruments

**Revision/date:** SLUSAW9F; revised November 2014. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.ti.com/lit/ds/symlink/ucc27511.pdf).

**SHA-256:** `781cc451dbb371a4137337a4bdecbe11a9f1ff8979a11e238e97d8a80a287b31`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [UCC27511DBVR.pdf](../../third_party/datasheets/UCC27511DBVR.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p7: Absolute maximum and recommended conditions |
| Pinout / polarity | p5,6: UCC27511 DBV pin configuration/functions |
| Package | p37: DBV0006A SOT-23 outline |
| Layout / land pattern | p27,28,38: Gate-loop/layout guidance and DBV board pattern |

<a id="doc-umt_h"></a>
### umt_h — SCHURTER

**Revision/date:** UMT-H datasheet; 21.07.2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.schurter.com/en/datasheet/typ_UMT-H.pdf).

**SHA-256:** `bac65726cd086e794288aa169ef2349664e674520019839b234b3a90f7c06ec7`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [3403.0285.23.pdf](../../third_party/datasheets/3403.0285.23.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,3,4,5: Ratings, time-current/derating, exact 3403.0285.23 row and copper test conditions |
| Pinout / polarity | p2: Two nonpolar terminals |
| Package | p2: Body dimensions |
| Layout / land pattern | p2,5: Soldering pads and copper test conditions; p2 visually checked |

<a id="doc-wfm"></a>
### wfm — Vishay

**Revision/date:** 30387; revision 04-Aug-2022. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/30387/wfm.pdf).

**SHA-256:** `a045b66d5ba1ba6f0c254e4c2fe60460fb25c4af01910416b38b30858ca5cc99`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [WFMB2512R0330FEA.pdf](../../third_party/datasheets/WFMB2512R0330FEA.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3: Rating, TCR and thermal derating |
| Pinout / polarity | p2: Two nonpolar terminals; no numbered electrical pinout |
| Package | p2: WFM2512 dimensions |
| Layout / land pattern | p2: Solder-pad dimensions |

<a id="doc-wsl"></a>
### wsl — Vishay

**Revision/date:** 30100; revision 23-Nov-2023. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/30100/wsl.pdf).

**SHA-256:** `96c2dc89ae1e3039815ed6c41f566a6e9f6b53035f8e45ea2ada1697935a44dc`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [WSL2512R3300FEA.pdf](../../third_party/datasheets/WSL2512R3300FEA.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3: WSL2512 rating, TCR and derating |
| Pinout / polarity | p2: Two nonpolar terminals; no numbered electrical pinout |
| Package | p2: WSL2512 outline |
| Layout / land pattern | p2: Solder-pad dimensions |

<a id="doc-wsl2726"></a>
### wsl2726 — Vishay

**Revision/date:** 30131; revision 29-Jun-2026. **Download:** DOWNLOADED.

Official source: [manufacturer PDF](https://www.vishay.com/docs/30131/wsl2726.pdf).

**SHA-256:** `583946079d110ac74dc7987e1f1d2c5a170253b03f123b993c414761c6b89373`.

Evidence: Local original PDF; text extraction and selected visual page checks.

Local PDFs: [WSL27262L000FEA.pdf](../../third_party/datasheets/WSL27262L000FEA.pdf).

| Review topic | PDF pages and scope |
| --- | --- |
| Abs max / ratings | p1,2,3: Rating, tolerance, TCR and thermal derating |
| Pinout / polarity | p2: Four-terminal Kelvin geometry; no project pin numbering implied |
| Package | p2: WSL2726 outline |
| Layout / land pattern | p2: Solder pads and Kelvin terminal geometry |

## Source-file preservation evidence

| Read-only source file | SHA-256 before and after |
| --- | --- |
| `hardware/kicad/01_INPUT_PROTECTION.kicad_sch` | `e1bce9b948dda904ccd756ea3e619704c9e2a30de4de2e6801271357e2b21d47` |
| `hardware/kicad/02_BUCK_5V.kicad_sch` | `4617898c69df9d1ecbb9700c6e031b76e19fe19d30220497b9bf993fb0603fce` |
| `hardware/kicad/03_OUTPUT_PROTECTION.kicad_sch` | `6ec05531a51d3a3306936b2e18ea369e2e51d9e570a25f32d155e28c09a6a695` |
| `hardware/kicad/04_POWER_MONITOR.kicad_sch` | `89202066a5d70f3c9d69d4dae605329748693e761144eba7f9725248bd456dab` |
| `hardware/kicad/05_IO_TEST.kicad_sch` | `e45adc24cb598a8455f0448ac6e811e51fe5d98bf34193dd537971808b8c9483` |
| `hardware/kicad/V1A.kicad_pro` | `2f3f1d74c5c1c75bbfb7daa1cc8822c177a31f2dea212aa09cc127ca813c62c5` |
| `hardware/kicad/V1A.kicad_sch` | `3580b27084d7dee4d0a27a59d6ace32510fd7cc0d3af0863aaffb0fca253721f` |
| `hardware/kicad/V1A.kicad_sym` | `37a2e8c7ee5df5cc168ff8a2283842757b5afd9af5d514cb1b3bf67002478c93` |

## Validation

**EVIDENCE:** Register generation checks every exported reference exactly once, MPN counts, each downloaded file’s PDF signature/parser success/SHA-256, one-based page bounds, and unchanged KiCad source hashes. Git staging is restricted to the two register paths. PDFs, temporary tools and BOM exports are excluded from the commit.
