# V1A-Lite final whole-build cost estimate

**Date:** 2026-10-05
**Currency:** VND
**Accounting rate:** **KNOWN** `1 USD = 26,500 VND`, retained from the Phase B/C accounting model and dated 2026-10-05. This is an accounting assumption, not a live FX quote.
**Scope:** one populated V1A-Lite prototype, with the required five-board JLCPCB bare-PCB order, minimum realistic purchase lots, the Pi 5 harness, shipping reserves, and first-prototype allowances.
**Status:** **BLOCKED against the 1,000,000 VND ceiling. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Result

The conservative, MOQ-aware estimate is:

| Result | VND | Label |
| --- | ---: | --- |
| Whole-build estimate | **1,562,948.85** | **ESTIMATE** — sum of the costed rows below; not a landed quote |
| Rounded whole-build estimate | **1,562,949** | **ESTIMATE** |
| Ceiling | **1,000,000** | **KNOWN** — project brief |
| Difference from ceiling | **+562,948.85** | **ESTIMATE** — over ceiling |

This total charges the full five-board PCB order and purchase lots needed to populate one board. Four bare boards and MOQ-forced component spares remain after the first prototype. It includes the exact `SVH-41T-P1.1` 100-piece distributor strip because the published authorized-distributor listing does not offer a two-piece purchase at the reviewed price. A local exact-stock source or a smaller authorized pack could reduce the result, but that source is **OPEN** and is not assumed.

## Evidence and counting basis

The released assembly inventory was taken from:

- `docs/evidence/v1a_lite/fab/assembly/BOM_JLC.csv` — 100 populated board components.
- `docs/evidence/v1a_lite/fab/assembly/CPL_JLC.csv` — matching placement inventory.
- `docs/evidence/v1a_lite/fab/assembly/MANUAL_ASSEMBLY.csv` — seven manual parts: `C101`, `C217`, `C218`, `D101`, `J501`, `J502`, `SCR301`.
- `docs/evidence/v1a_lite/V1A_LITE_BOM.csv` — released MPNs, references, and source links.
- `docs/evidence/v1a_lite/PHASE_C_PURCHASE_MODEL.csv` and `PHASE_C2_PURCHASE_MODEL.csv` — dated LCSC price and MOQ/price-break data.
- `docs/evidence/v1a_lite/PI_HARNESS.md` — exact Pi harness interface and parts.
- `/Users/quockaiser/Desktop/Research/wt-litesrc/docs/evidence/v1a_lite/SOURCING_PLAN.md` — read-only local Vietnam sourcing price snapshots.

The final BOM uses `IRFR6215TRPBF`, not the earlier C2 analysis candidate `IRF9540NPBF`. The exact-MPN `IRFR6215TRPBF` reference price from the saved C3 correction is used below; the older `IRF9540NPBF` price is not silently substituted.

Cost labels in this document are deliberately narrow:

- **KNOWN:** a published supplier/listing price or the project brief, with a URL and access date. A published price is not a current checkout quote.
- **ESTIMATE:** a derived VND conversion, configuration estimate, local-equivalence scenario, shipping reserve, or allowance. Electrical/mechanical equivalence and landed cost may still be **OPEN**.

## 1. JLCPCB bare PCB — five boards

Required configuration: **5 boards, 80 × 60 mm, 4 layers, nominal 1.6 mm, 1 oz outer copper / 0.5 oz inner copper, HASL, green**.

JLCPCB’s public prototype page states **1–4 layers, 5 pcs, 100 × 100 mm, from $2.00**, and also states that final pricing varies with board specifications. The public quote page exposes the requested layer, quantity, thickness, green mask, HASL, and copper-weight fields, but no configured price is published without uploading the design/creating a quote. No upload, cart, login, or quote was made.

| PCB line | Basis | VND | Label |
| --- | --- | ---: | --- |
| Public prototype entry floor | $2.00 × 26,500 VND/USD; 1–4 layer / 5-piece / 100 × 100 mm category | 53,000 | **KNOWN** public price floor; exact configuration not priced |
| Applied five-board estimate | Use the public $2.00 entry floor for the requested 80 × 60 mm / 4-layer / 1.6 mm / 1 oz outer / 0.5 oz inner / HASL / green order | **53,000** | **ESTIMATE** — optimistic configured-price basis, not a quote |

**JLC source:** [JLCPCB public prototype price page](https://jlcpcb.com/ads/pcb-prototype), accessed 2026-10-05; [JLCPCB online quote fields](https://cart.jlcpcb.com/quote/), accessed 2026-10-05; [JLCPCB four-layer stackup data](https://jlcpcb.com/impedance), accessed 2026-10-05. The exact HASL subtype (leaded versus lead-free) remains **OPEN**.

## 2. Board parts for one populated board

The exact rows below retain the final-BOM MPN wherever the part is safety-critical, layout-critical, precision, high-voltage, or otherwise not suitable for an unreviewed local substitute. `Buy` includes one spare where practical and the smallest saved LCSC/authorized-distributor MOQ or price-break quantity. `SMCJ64CA` is an authorized-distributor route with an allowance rather than a quote.

### Exact MPN rows

| MPN | Installed | Buy | Route / price basis | Line cost (VND) | Label |
| --- | ---: | ---: | --- | ---: | --- |
| `0451003.MRL` | 1 | 5 | LCSC C13982; $0.2556 each; [source](https://www.lcsc.com/product-detail/C13982.html), accessed 2026-10-04 | 33,867.00 | **KNOWN** dated offer; landed quote OPEN |
| `0451007.MRL` | 1 | 5 | LCSC C99548; $0.2345 each; [source](https://www.lcsc.com/product-detail/C99548.html), accessed 2026-10-04 | 31,071.25 | **KNOWN** dated offer; landed quote OPEN |
| `0603WAF100JT5E` | 1 | 20 | LCSC C22859; $0.0032 each; [source](https://www.lcsc.com/product-detail/C22859.html), accessed 2026-10-04 | 1,696.00 | **KNOWN** dated offer; landed quote OPEN |
| `0603WAF1300T5E` | 1 | 100 | LCSC C22796; $0.0014 each; [source](https://www.lcsc.com/product-detail/C22796.html), accessed 2026-10-04 | 3,710.00 | **KNOWN** dated offer; landed quote OPEN |
| `0603WAF1501T5E` | 1 | 100 | LCSC C22843; $0.0020 each; [source](https://www.lcsc.com/product-detail/C22843.html), accessed 2026-10-04 | 5,300.00 | **KNOWN** dated offer; landed quote OPEN |
| `BC807-40,215` | 2 | 20 | LCSC C57316; $0.0200 each; [source](https://www.lcsc.com/product-detail/C57316.html), accessed 2026-10-04 | 10,600.00 | **KNOWN** dated offer; exact MPN stock/landed quote OPEN |
| `BZT52C12-7-F` | 3 | 10 | LCSC C124196; $0.0771 each; [source](https://www.lcsc.com/product-detail/C124196.html), accessed 2026-10-04 | 20,431.50 | **KNOWN** dated offer; landed quote OPEN |
| `BZT52C3V3-7-F` | 1 | 10 | LCSC C151564; $0.0528 each; [source](https://www.lcsc.com/product-detail/C151564.html), accessed 2026-10-05 | 13,992.00 | **KNOWN** dated offer; landed quote OPEN |
| `C0402C220J4GACTU` | 1 | 50 | LCSC C2168192; $0.0171 each; [source](https://www.lcsc.com/product-detail/C2168192.html), accessed 2026-10-04 | 22,657.50 | **KNOWN** dated offer; landed quote OPEN |
| `EEUFR1A102` | 2 | 5 | LCSC C407868; $0.1751 each; [source](https://www.lcsc.com/product-detail/C407868.html), accessed 2026-10-04 | 23,200.75 | **KNOWN** dated offer; landed quote OPEN |
| `EEUFR1H101` | 1 | 5 | LCSC C178702; $0.3259 each; [source](https://www.lcsc.com/product-detail/C178702.html), accessed 2026-10-04 | 43,181.75 | **KNOWN** dated offer; landed quote OPEN |
| `GRM31CR61E476ME44L` | 6 | 7 | LCSC C403725; $0.6136 each; [source](https://www.lcsc.com/product-detail/C403725.html), accessed 2026-10-05 | 113,822.80 | **KNOWN** dated offer; seven-piece local-plan quantity |
| `GRM32ER61C476KE15L` | 2 | 5 | LCSC C77101; $0.3135 each; [source](https://www.lcsc.com/product-detail/C77101.html), accessed 2026-10-04 | 41,538.75 | **KNOWN** dated offer; landed quote OPEN |
| `GRM32ER71H106KA12L` | 4 | 5 | LCSC C77102; $0.3322 each; [source](https://www.lcsc.com/product-detail/C77102.html), accessed 2026-10-04 | 44,016.50 | **KNOWN** dated offer; landed quote OPEN |
| `IRFR6215TRPBF` | 2 | 3 | LCSC C150936; $0.9375 each; [source](https://www.lcsc.com/product-detail/C150936.html), accessed 2026-10-05; final-BOM exact-MPN correction | 74,531.25 | **KNOWN** reference price; stock is OPEN |
| `LM61460AANRJRR` | 1 | 2 | LCSC C2864505; $1.8929 each; [source](https://www.lcsc.com/product-detail/C2864505.html), accessed 2026-10-04 | 100,323.70 | **KNOWN** dated offer; landed quote OPEN |
| `MMBTA42-TP` | 3 | 10 | LCSC C78715; $0.0583 each; [source](https://www.lcsc.com/product-detail/C78715.html), accessed 2026-10-05 | 15,449.50 | **KNOWN** reference price; stock is OPEN |
| `RT0603BRD071KL` | 4 | 20 | LCSC C110776; $0.0298 each; [source](https://www.lcsc.com/product-detail/C110776.html), accessed 2026-10-04 | 15,794.00 | **KNOWN** dated offer; landed quote OPEN |
| `RT0603BRD0724K6L` | 2 | 20 | LCSC C861250; $0.0354 each; [source](https://www.lcsc.com/product-detail/C861250.html), accessed 2026-10-04 | 18,762.00 | **KNOWN** dated offer; landed quote OPEN |
| `SMCJ64CA` | 1 | 2 | Exact Bourns part via Mouser route; $0.50/unit allowance; [identity source](https://www.mouser.com/en/ProductDetail/Bourns/SMCJ64CA?qs=NMatY7cgvvbtyPM2xB%252BvVA%3D%3D), accessed 2026-10-05 | 26,500.00 | **ESTIMATE** — exact quote OPEN |
| `SRP1265A-6R8M` | 1 | 2 | LCSC C2041326; $1.1431 each; [source](https://www.lcsc.com/product-detail/C2041326.html), accessed 2026-10-04 | 60,584.30 | **KNOWN** dated offer; landed quote OPEN |
| `TL431BIDBZR` | 2 | 5 | LCSC C41283; $0.0784 each; [source](https://www.lcsc.com/product-detail/C41283.html), accessed 2026-10-04 | 10,388.00 | **KNOWN** dated offer; landed quote OPEN |
| `TNPW0603100KBEEA` | 2 | 5 | LCSC C844888; $0.0797 each; [source](https://www.lcsc.com/product-detail/C844888.html), accessed 2026-10-04 | 10,560.25 | **KNOWN** dated offer; landed quote OPEN |
| `TNPW0603100RBEEA` | 1 | 5 | LCSC C844889; $0.0922 each; [source](https://www.lcsc.com/product-detail/C844889.html), accessed 2026-10-04 | 12,216.50 | **KNOWN** dated offer; landed quote OPEN |
| `TNPW060310K0BEEA` | 1 | 10 | LCSC C844890; $0.0711 each; [source](https://www.lcsc.com/product-detail/C844890.html), accessed 2026-10-04 | 18,841.50 | **KNOWN** dated offer; landed quote OPEN |
| `TNPW060333K2BEEA` | 1 | 5 | LCSC C2075328; $0.0909 each; [source](https://www.lcsc.com/product-detail/C2075328.html), accessed 2026-10-04 | 12,044.25 | **KNOWN** dated offer; landed quote OPEN |
| `TVS3300DRVR` | 1 | 2 | LCSC C2863624; $0.5261 each; [source](https://www.lcsc.com/product-detail/C2863624.html), accessed 2026-10-04 | 27,883.30 | **KNOWN** reference price; stock is OPEN |
| `TYN612RG` | 1 | 2 | LCSC C262993; $0.6784 each; [source](https://www.lcsc.com/product-detail/C262993.html), accessed 2026-10-04 | 35,955.20 | **KNOWN** dated offer; landed quote OPEN |
| **Exact MPN subtotal** | **—** | **—** | Final-BOM installed quantities aggregated before MOQ rounding; `IRFR6215TRPBF` replaces the older C2 `IRF9540NPBF` row | **848,919.55** | **ESTIMATE** — purchase-lot subtotal |

The exact-MPN subtotal includes only board parts. `D101` is the manually installed external `SMCJ64CA`; it remains in the cost because it is part of the released BOM.

### Local generic passive lots

These are the cheapest local candidates recorded in the read-only Vietnam sourcing plan. They are not claims that the local listings are the released MPNs. Package, voltage, dielectric, tolerance, power, temperature coefficient, DC-bias behavior, and availability must pass review before use.

| Final-BOM function / candidate | Installed | Local buy lot | Published listing basis | Line cost (VND) | Label |
| --- | ---: | ---: | --- | ---: | --- |
| 10 kΩ 0805, candidate for `0805W8F1002T5E` | 8 | 50 | 50 × 56 VND; [local listing](https://www.thegioiic.com/dien-tro-10-kohm-0805-1-), accessed 2026-10-05 | 2,800.00 | **ESTIMATE** — known listing price, equivalence OPEN |
| 1 kΩ 0603, candidate for `0603WAF1001T5E` | 23 | 50 | 50 × 38 VND; [local listing](https://www.thegioiic.com/dien-tro-1-kohm-0603-1-), accessed 2026-10-05 | 1,900.00 | **ESTIMATE** — known listing price, equivalence OPEN |
| 100 Ω 0603, candidate for `0603WAF1000T5E` | 7 | 50 | 50 × 76 VND; [local listing](https://www.thegioiic.com/dien-tro-100-ohm-0603-1-), accessed 2026-10-05 | 3,800.00 | **ESTIMATE** — known listing price, equivalence OPEN |
| 100 kΩ 0603, candidate for `0603WAF1003T5E` | 5 | 50 | 50 × 76 VND; [local listing](https://www.thegioiic.com/dien-tro-100-kohm-0603-1-), accessed 2026-10-05 | 3,800.00 | **ESTIMATE** — known listing price, equivalence OPEN |
| 100 nF 0603 shared generic lot for `GRM188R71C104KA01D` and `GRM188R71H104KA93D` | 3 | 10 shared | 10 × 190 VND; [local listing](https://www.thegioiic.com/tu-gom-0603-100nf-0-1uf-50v), accessed 2026-10-05 | 1,900.00 | **ESTIMATE** — one shared lot, voltage/derating OPEN |
| 1 µF 0805, candidate for `GRM21BR71C105KA01L` | 2 | 10 | 10 × 400 VND; [local catalog](https://www.thegioiic.com/suppliers/samsung/tu-gom-dan-smd/146), accessed 2026-10-05 | 4,000.00 | **ESTIMATE** — local equivalent, DC-bias/voltage OPEN |
| **Local generic passive subtotal** | **—** | **—** | Six charged lots; spares are the unused lot balance | **18,200.00** | **ESTIMATE** |

**Board-parts subtotal:** **867,119.55 VND — ESTIMATE** (`848,919.55` exact-MPN purchase lots + `18,200.00` local generic lots).

## 3. Board connectors and Pi 5 harness

### Board connectors

The released board has two `B2P-VH-FB-B(LF)(SN)` footprints (`J501`, `J502`). The cheapest recorded split is three local generic VH3.96 2-pin kits: two installed port sets and one spare. This is a cost candidate only. The local kit must be proven to mate with the released board footprint and the selected cable system; otherwise the exact JST connector route returns and the total increases.

| Item | Quantity | Line cost (VND) | Label |
| --- | ---: | ---: | --- |
| Generic VH3.96 2-pin connector kit, male/female/contact set | 3 kits | **4,719.00** | **ESTIMATE** — 3 × 1,573 VND listing; [local listing](https://www.thegioiic.com/bo-dau-noi-vh3-96mm-2-chan-thang-kem-kim-bam-day), accessed 2026-10-05 |

### Pi harness parts

`PI_HARNESS.md` specifies one `VHR-2N` cable housing with two `SVH-41T-P1.1` contacts, a Harwin `M20-1070500` 2×5 housing with four `M20-1160042` contacts, AWG18 trunk conductors, paired AWG22 fanouts, and a keyed insulating carrier. The table charges the exact connector/contact parts. The `SVH-41T-P1.1` line uses the published 100-piece strip minimum; 98 contacts are MOQ-forced spares.

| Exact harness part / construction | Installed | Buy | Price basis | Line cost (VND) | Label |
| --- | ---: | ---: | --- | ---: | --- |
| JST `VHR-2N` housing | 1 | 1 | DigiKey published $0.110 each; [source](https://www.digikey.com/en/products/detail/jst-sales-america-inc/VHR-2N/608624), accessed 2026-10-05 | 2,915.00 | **KNOWN** component price; freight/import OPEN |
| JST `SVH-41T-P1.1` contacts | 2 | 100-strip | DigiKey published $0.08810 each at 100; [source](https://www.digikey.com/en/products/detail/jst-sales-america-inc/SVH-41T-P1-1/26213078), accessed 2026-10-05 | **233,465.00** | **KNOWN** component price and pack basis; freight/import OPEN |
| Harwin `M20-1070500` 2×5 housing | 1 | 1 | DigiKey published $0.420 each; [source](https://www.digikey.com/en/products/detail/harwin-inc/M20-1070500/3727997), accessed 2026-10-05 | 11,130.00 | **KNOWN** component price; freight/import OPEN |
| Harwin `M20-1160042` contacts | 4 | 4 | DigiKey published $0.100 each at cut-tape quantity 1; [source](https://www.digikey.com/en/products/detail/harwin-inc/M20-1160042/3728123), accessed 2026-10-05 | 10,600.00 | **KNOWN** component price; freight/import OPEN |
| AWG18/AWG22 wire, heat-shrink, labels, insulated splices, strain relief | Per `PI_HARNESS.md` lengths | Local allowance | 18 AWG red/black listing plus unpriced AWG22/splice/strain-relief allowance from the read-only sourcing plan | **20,000.00** | **ESTIMATE** |
| **Board connector + exact Pi harness subtotal** | **—** | **—** | Local board connector kits plus exact Pi harness parts and harness consumables | **282,829.30** | **ESTIMATE** |

The connector/harness subtotal is **282,829.30 VND — ESTIMATE** (`4,719.00` board kits + `258,110.00` exact Pi connector/contact parts + `20,000.00` wire/consumables). The keyed carrier dimensions and final mechanical support are **OPEN** and are not priced; a carrier may add cost.

## 4. Shipping and prototype allowances

### JLCPCB + LCSC combined shipment

The intended low-cost method is one combined shipment:

1. Place the JLCPCB PCB order using the LCSC/JLC consolidation warehouse address specified by LCSC, with the same customer ID and currency as the LCSC component order.
2. At LCSC checkout, select the JLCPCB order for combination, or contact LCSC support with both order numbers before either shipment is packed.
3. Let LCSC recalculate the single shipment to Vietnam. Do not split or bind the orders after shipment has started.

LCSC states that the combined order requires the same currency and customer ID, uses the Hong Kong consolidation address, and has shipping recalculated; see the [official LCSC/JLCPCB combination procedure](https://www.lcsc.com/help-center/notice/combine-lcsc-jlcpcb-orders), accessed 2026-10-05. No order, login, cart, support request, or quote was made for this estimate.

| Line | VND | Label |
| --- | ---: | --- |
| One combined JLCPCB + LCSC shipment, import/tax/handling reserve to Vietnam | **200,000.00** | **ESTIMATE** — no checkout quote; replaces separate 80,000 + 120,000 planning reserves |
| Local delivery to the lab | **20,000.00** | **ESTIMATE** — local courier/pickup reserve |
| Manual assembly and consumables | **50,000.00** | **ESTIMATE** — lab/reflow/soldering allowance |
| First-prototype rework contingency | **50,000.00** | **ESTIMATE** — not a safety validation reserve |
| SCR thermal sink, insulation, and mounting contingency | **40,000.00** | **ESTIMATE** — sustained-fault thermal solution remains unqualified |

The combined-shipment reserve does not guarantee the separate authorized-distributor harness parts can be added to the LCSC/JLC shipment. If those parts require a separate imported order, extra freight/import cost is **OPEN** and the total rises.

## 5. Total reconciliation

| Cost line | VND | Label |
| --- | ---: | --- |
| Board parts: exact MPN lots + local generic lots | 867,119.55 | **ESTIMATE** — purchase-lot subtotal |
| Board connector kits + exact Pi harness parts + wire/consumables | 282,829.30 | **ESTIMATE** |
| Five-board JLCPCB bare PCB order | 53,000.00 | **ESTIMATE** — public $2 entry-floor basis; exact configured price OPEN |
| Combined JLCPCB/LCSC freight/import/handling reserve | 200,000.00 | **ESTIMATE** |
| Local delivery | 20,000.00 | **ESTIMATE** |
| Manual assembly/consumables | 50,000.00 | **ESTIMATE** |
| Rework contingency | 50,000.00 | **ESTIMATE** |
| SCR thermal/mounting contingency | 40,000.00 | **ESTIMATE** |
| **Whole-build estimate** | **1,562,948.85** | **ESTIMATE** |
| **Difference from 1,000,000 VND ceiling** | **+562,948.85** | **ESTIMATE — FAIL / over ceiling** |

The displayed total uses `282,829.30 VND` for the connector/harness line. The intermediate exact Pi connector/contact arithmetic is `2,915.00 + 233,465.00 + 11,130.00 + 10,600.00 = 258,110.00 VND`; adding the `4,719.00 VND` board connector kits and `20,000.00 VND` wire/consumables gives `282,829.30 VND`.

## 6. Five biggest cost lines

| Rank | Line | VND | Label |
| ---: | --- | ---: | --- |
| 1 | `SVH-41T-P1.1` 100-piece strip for two installed Pi-harness contacts | 233,465.00 | **KNOWN** published pack price; separate freight OPEN |
| 2 | Combined JLCPCB + LCSC shipment/import/handling reserve | 200,000.00 | **ESTIMATE** |
| 3 | `GRM31CR61E476ME44L`, seven-piece LCSC purchase | 113,822.80 | **KNOWN** dated price; landed quote OPEN |
| 4 | `LM61460AANRJRR`, two-piece LCSC purchase | 100,323.70 | **KNOWN** dated price; landed quote OPEN |
| 5 | `IRFR6215TRPBF`, three-piece exact-MPN purchase | 74,531.25 | **KNOWN** reference price; stock OPEN |

## Open risks and decisions

- **OPEN / JLC price:** the exact 80 × 60 mm, four-layer, 1.6 mm, copper-weight, HASL, green configuration was not published as a static price. The applied 53,000 VND line is an optimistic estimate and can increase at checkout.
- **OPEN / imported stock:** `TVS3300DRVR`, `MMBTA42-TP`, and `IRFR6215TRPBF` have reference prices with stock/landed availability open. The `SMCJ64CA` amount is an allowance, not a quote.
- **OPEN / exact Pi harness:** the `SVH-41T-P1.1` price is based on a 100-piece authorized-distributor strip. A Vietnam exact-stock source, smaller pack, or alternate authorized distributor was not assumed.
- **OPEN / board connector fit:** the local VH3.96 kit must mate with the released JST VH footprint and the exact `VHR-2N` harness. If it does not, revert to exact JST parts and recost; no hardware edit is authorized by this document.
- **OPEN / local passive equivalence:** verify package, voltage, dielectric, DC-bias capacitance, tolerance, temperature coefficient, and resistor power before accepting any local lot.
- **OPEN / landed freight:** the combined JLC/LCSC method recalculates shipping and may add tax/carrier handling. Authorized harness parts may require a separate shipment.
- **OPEN / Pi mechanical key:** `PI_HARNESS.md` requires a captive asymmetric carrier registered to Pi pin 1. Its design and cost are not included because no approved mechanical definition exists.
- **OPEN / electrical qualification:** this estimate does not validate input cutoff, reverse-polarity protection, crowbar energy, fuse coordination, regulator ripple, inrush, transient behavior, harness resistance, connector derating, or Pi voltage limits. ERC/DRC would not close those risks.
- **DECISION:** retain this estimate as a budget gate only. Do not buy, fabricate, or connect an SBC. Follow the documented bring-up sequence only after the engineering gates and fabrication-readiness review pass.

No hardware files were edited. No carts, logins, quotes, purchases, orders, manufacturing uploads, or external messages were performed.

FINALCOST-HANDBACK
