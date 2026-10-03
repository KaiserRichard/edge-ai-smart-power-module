# BOM order source provenance

**Reference only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

`CATALOG_FACTS.json` contains factual catalog observations used by the order register, not copies of third-party circuit designs. Each entry identifies the exact queried MPN, distributor, URL, observed date, displayed crawl age, available SKU, price tiers, stock, lead time, lifecycle label and retrieval limitations. These are indexed website snapshots; access on 2026-10-03 does not establish live stock. `SEARCH_LOG.json` records the main exact-MPN sourcing searches, including unmatched codes. Missing values are OPEN.

For the distributor entries, the document revision is **OPEN: undated dynamic catalog page**; the reproducible evidence is the recorded URL, access date, crawl age and factual fields. Copyright remains with LCSC, Mouser, DigiKey and the named manufacturers; no redistribution license for full pages was established. Only factual catalog data is retained. Attribution is the named channel/manufacturer and linked product page in the BOM. No page, upstream reference source, circuit or PCB was modified, copied or adapted. Raw page text used during research remains outside the repository in the temporary work area.

## Additional authoritative documents referenced

| Owner / URL | Revision / relevant location | Function studied / use | License and attribution | Modifications |
|---|---|---|---|---|
| [Nichicon PCH catalog](https://www.nichicon.co.jp/_assets/images/products/catalog/corporate/digital/sh_pch.pdf) | 2026 catalog; dimensions table, PCH1V471MCL1GS row | Exact part identity, 470 uF / 35 V, 10×16 mm; referenced, no circuit reuse | Copyright Nichicon; no open redistribution license established; attribute linked table | None |
| [Panasonic EEUFR1E221](https://na.industrial.panasonic.com/products/capacitors/aluminum-electrolytic-capacitors/series/83367/model/83695) | Undated model page, accessed 2026-10-03; specifications | Manufacturer spelling and bulk straight-lead package geometry; referenced | Copyright Panasonic; factual metadata only, linked attribution | None |
| [Panasonic precision resistor table](https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models?order=atr-ind-pRDM0000J5_46_A&page=60&series=AOA0026&sort=desc) | Undated table, accessed 2026-10-03; ERA6AEB3653V row | Nominal alternate identity: 365 kohm, 0.1%, 25 ppm/K, 0805, 0.125 W. Candidate only; voltage/power qualification OPEN | Copyright Panasonic; factual metadata only, linked attribution | None |

The project source itself is pinned to `6d25cf28c4d246417c0a89ec89574c702850e069` of [edge-ai-smart-power-module](https://github.com/KaiserRichard/edge-ai-smart-power-module). Relevant files are `hardware/kicad/V1A.kicad_sch`, Sheets 01–05, `docs/evidence/r2/gate4b/CAPTURED_BOM.csv`, `PIN_REVIEW.md`, `SHEET05_REVIEW.md`, and `CHECK_C1C3.md`. The earlier source `838a8a45d8939f9b57af4715724bc71afc0134fc` has identical CAD/BOM content. This is the user's project, referenced read-only; no external PCB reuse occurred.

The custom-link dimensions are referenced from project commit `898759e45578f3767721d19eb313312b7d7733a9`, `docs/evidence/r2/gate4a/FIX3_FIXTURE.md`, [permanent source link](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/898759e45578f3767721d19eb313312b7d7733a9/docs/evidence/r2/gate4a/FIX3_FIXTURE.md). Drawing identity: `CUSTOM-FX-CU-01 RevA`. No custom mechanical drawing or manufacturer part number was invented. The procurement report does not grant fabrication or energized-fixture approval.

The external J502 harness selection is the captured solution A originating at `41cb9e889418d50d2f5f24467e66ac7f15a90476`, `docs/evidence/r2/J502_SELECTION.md`. It is referenced through the pinned Sheet05 review; neither the harness nor its hot-contact behaviour is newly qualified by this sourcing task.

Distributor-suggested alternatives in the factual register are **unapproved candidates**, not copied reference designs. A nominal-match listing cannot establish pinout, effective capacitance, pulse energy, hot SOA, thermal behaviour or control timing. Prices for unapproved alternatives are excluded from the selected-part totals.

## Resume evidence — 2026-10-03

The source was fetched again in the existing detached `/tmp` checkout and now pins `56e9837e522c01bd680aca602f9f471d38d6039f`. Its six source schematics and fresh KiCad BOM are byte-identical to the previous source. Historical catalog observations above are retained unchanged.

`RESUME_CATALOG_FACTS.json` adds Q264–Q270 and supersedes earlier observations only for matching MPN/distributor pairs. Every new stock/price pair is one retrieved snapshot; explicit SKU/alias identity links are recorded separately where needed. In particular, DigiKey explicitly lists the complete JST suffix as an alias; the selected schematic MPN is preserved. The TE housing entry uses direct DigiKey stock (zero), excluding WEC marketplace stock. Mouser's European 0-ohm entry supplies stock and pack details only; EUR pricing is not treated as USD. All dynamic-page revisions are OPEN, access date 2026-10-03; individual crawl ages remain attached to each fact. The original catalog-data license/attribution restrictions apply.

`ALTERNATE_REVIEW.json` records focused alternate dispositions. [TI TPS70933DBVT](https://www.ti.com/product/TPS709/part-details/TPS70933DBVT) (linked datasheet Rev. H) and [TI TLV3201AIDBVT](https://www.ti.com/product/TLV3201/part-details/TLV3201AIDBVT) (linked datasheet Rev. C) explicitly identify their R/T suffix options as the same device in different carrier quantities. Relevant sections: exact-part title, status, package/pins, carrier alternatives. The undated part pages were read 2026-10-03; TI copyright, factual metadata only, no document/CAD adaptation. The YAGEO nominal resistor candidate is distributor evidence only and expressly requires manufacturer qualification.

Additional documents inspected during sourcing, without selecting or adapting a circuit: [Vishay D/CRCW e3](https://www.vishay.com/docs/20035/dcrcwe3.pdf), document 20035, revision 14-Apr-2026, pp. 1–2 (0603/jumper ratings); [Panasonic ERA3AEB104V](https://industrial.panasonic.com/ww/products/pt/high-precision-chip-resistors/models/ERA3AEB104V), undated model page (identity only). Copyright remains with the named manufacturers; no open license established, no modifications, linked attribution. Failed TCA9517/YAGEO page retrievals establish no technical facts and do not authorize alternate selection.

Repeated exact-code searches did not establish orderable C3216X7R1H475K160AB, TNPW060324K4BEEA or distributor supply of PCH1V471MCL1GS. Searches for potential ballast/resistor replacements did not qualify a replacement. No search failure is interpreted as manufacturer EOL or proof that a part does not exist. See [resume review](../../docs/evidence/r2/bom_order/RESUME_REVIEW.md).
