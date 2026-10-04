# BOM order resume review — 2026-10-03

**STATUS: CONDITIONAL PASS for procurement documentation; BLOCKED for a complete order.**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**REQUIREMENT:** continue the committed partial work under `BOM_ORDER_RESUME.md` and `BOM_ORDER_READY.md`. The resume brief confirms U316 `LT4363HMS-1#PBF` and supersedes the earlier pending marker. KiCad is read-only; no cart, purchase, quote request or push is authorized or performed.

**EVIDENCE:** the worktree fetch failed with `FETCH_HEAD: Operation not permitted`. The existing independent `/tmp/v1a-bom-order.aC9fug` clone was fetched and detached at `56e9837e522c01bd680aca602f9f471d38d6039f`, the retrieved `origin/feat/r2-testboard-capture` tip. A fresh KiCad 9.0.6 `sch export bom` matches the saved export exactly: SHA-256 `b2e57ccf9cfd4251d297d6e2bb6b422f2bfc0aead7b5d0fec14f03fad456acae`. All six schematic hashes match the previous source; the tracked temporary checkout remains clean. The source advance contains PCB preparation and documentation, which do not change this BOM. See [provenance](PROVENANCE.json) and [export log](resume-export.log).

**OBSERVATION:** 366 references are represented once: 298 catalog components in 96 exact MPN groups, seven custom links and 61 etched PCB features. Sheet03 has 280 references, Sheet04 23 and Sheet05 11. Historical draft BOM, reconciliation and original catalog facts are retained. The full register has 112 rows including external harness/mechanical/accessory entries. Three-board quantities, spare rules and supplier rounding are in [BOM_ORDER.md](../BOM_ORDER.md).

**DECISIONS:**

- U316 is confirmed, one per board and four to order. The source C1–C3 review verifies the selected -1 12-pin MSOP. It now appears in the 37-line LCSC candidate subset as `C580193`, quantity 4. A sourcing change to -2 is not approved.
- JP201/JP501 resolve to the existing authored `CUSTOM-FX-CU-01 RevA` drawing. Seven board positions require 24 links for three boards plus spares, with at least 48 bolts, 96 washers and 48 nuts. This closes drawing identity, not a catalog MPN or fabricator quote. Fabrication/contact/parasitic qualification remains OPEN.
- New Q264–Q270 observations add the J501 DigiKey alias, L301 Mouser cut-tape pricing, R106 Mouser stock/pricing, the TE housing DigiKey bulk offer, verified Mouser 0-ohm stock, LCSC 100-kohm pricing and a refreshed Panasonic bulk-capacitor offer. No foreign-currency price or marketplace stock is silently incorporated.
- An alternate supplier of the same captured MPN is identified separately from a different component. Backorder/OPEN-stock backup routes do not establish immediate supply. TI-confirmed carrier alternatives replace generic similar-device suggestions for TLV3201 and TPS70933. Different-MPN candidates remain outside selected quantities/totals and require engineering acceptance.

**CALCULATION:** known catalog-board USD subtotals are LCSC **595.13** (54/96 lines), Mouser **720.57** (47/96), and DigiKey **937.85** (82/96). These are alternative distributor scenarios, not additive purchases. Harness subtotals are separate. Four selected catalog MPNs remain unpriced across all three channels; 12 have no confirmed stock in the evidence. Complete-board/kit totals remain OPEN; incomplete subtotals include some backorders and do not authorize a purchase.

| Unpriced selected MPN | References | Planning quantity | Required closure |
|---|---|---:|---|
| PCH1V471MCL1GS | C330–337, C340–343 | 40 | Exact manufacturer code verified; distributor SKU/stock/price and replacement qualification OPEN |
| C3216X7R1H475K160AB | C351 | 5 | Resolve exact AB ordering code; AC is a different, unapproved candidate |
| TNPW060324K4BEEA | R203 | 5 | Verify exact 24.4 kohm order code or approve recalculated feedback-network change |
| TNPW0805365KBEEA | R376, R378 | 8 | Verify selected-part supply or qualify the named 365 kohm candidate's power/voltage margins |

**OPEN RISKS:** backorders/long lead times, channel EOL/NRND labels, limited observed supplier coverage, unqualified alternates, custom-link fabrication and assembly, other mating harnesses, live-tab cooling/insulation and tooling costs. Indexed snapshots include old crawls and are not live inventory reservations. Required electrical/physical validation remains open; sourcing evidence cannot release R2 or fabrication.

**VALIDATION:** [VALIDATION.json](VALIDATION.json) records reference coverage/uniqueness, native MPN/footprint preservation, source hash, spare and spool arithmetic, every selected supplier evidence field, USD-only price tiers, costs and stock-sufficient subtotals, exact Markdown/CSV commercial values, local links and complete LCSC subset membership. No ERC/DRC was rerun because this work changes no KiCad files. The detached source refresh and BOM export are independent evidence of synchronization, not circuit validation.

**NEXT GATE:** resolve the explicit procurement/electrical review items before releasing the complete order or advancing the design gates. This handoff completes the requested read-only procurement register with OPEN fields where evidence is missing. Local commit is attempted under the resume brief's permission-denial fallback; no push is performed.

**GIT HANDBACK:** the requested local commit was attempted after validation. `git add` failed before staging with `Unable to create '/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-bom/index.lock': Operation not permitted`. Per the resume brief, the changes remain uncommitted. No lock deletion, permission change or alternate Git-directory workaround was attempted. `git diff --check` passes; generated order CSVs use LF line endings, while the original KiCad source export remains byte-preserved.
