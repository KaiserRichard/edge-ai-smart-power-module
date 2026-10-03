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
