# V1A-Lite Option 1 sourcing plan

**Access date:** 2026-10-05  
**Scope:** one Option 1 first prototype, using the saved Phase B common core + `OPT1` output fuse + `CROWBAR`.  
**Currency:** 1 USD = 26,500 VND, retained from the Phase B accounting model; this is an accounting assumption, not a live exchange quote.  
**Status:** **BLOCKED** against the hard 1,000,000 VND whole-prototype ceiling.  
**Safety:** **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Result

The cheapest realistic plan found is **1,155,930 VND** rounded, or **155,930 VND over** the ceiling. It assumes a successful current-price LCSC order, one five-board JLCPCB order, local purchases, and non-zero shipping/delivery reserves. It does not include any purchase, cart, login, or commitment.

The lower sensitivity with local pickup instead of the 20,000 VND local-delivery reserve is **1,135,930 VND**, still **135,930 VND over**. Removing a spare or replacing an exact safety part is not an acceptable budget remedy.

**CALCULATION**

```text
LCSC exact-MPN order                       700,010.75 VND
Local generic passive purchase              18,200.00 VND
Core electronic subtotal                   718,210.75 VND
Local connector sets                         4,719.00 VND
Five-board bare PCB                         53,000.00 VND
Wire, heat-shrink and strain relief         20,000.00 VND
LCSC shipping/import reserve                80,000.00 VND  ASSUMED
JLCPCB shipping/tax/handling reserve       120,000.00 VND  ASSUMED
Local delivery reserve                      20,000.00 VND  ASSUMED
Manual assembly/consumables                 50,000.00 VND  ASSUMED
Miscellaneous/rework contingency             50,000.00 VND  ASSUMED
SCR sink/insulation/mounting                 40,000.00 VND  ASSUMED
                                             ----------------
New Option 1 C total                    1,155,929.75 VND
Rounded total                           1,155,930.00 VND
Ceiling gap                              +155,929.75 VND
```

The Phase B Option 1 C baseline was 1,465,748 VND. This plan therefore reduces the recorded first-build estimate by **309,818 VND**, but the result remains a budget failure. The two LCSC prices for `TVS3300DRVR` and `MMBTA42-TP` are saved reference prices while current stock is open; an authorized-distributor fallback would increase the result and is not hidden in the total.

## Purchasing decisions

1. For every Phase B Option 1 MPN, the target is `installed quantity + 1 spare`.
2. Buy the smallest quantity that meets that target and the saved MOQ/price-break increment. The MOQ is charged even when it creates more than one spare.
3. Keep the exact MPN for the input P-FET, TL431s, TVS, SCR, fuses, LM61460, inductor, output capacitors, feedback/threshold resistors, high-voltage zeners, and other non-local lines below. No substitute is authorized by this plan.
4. Use local stock only for generic 0603/0805 resistors and non-safety-critical decoupling capacitors where the value, case size, voltage rating, dielectric/temperature behavior, tolerance, and power rating still pass engineering review.
5. Keep one LCSC order, one JLCPCB five-board order, and one combined local order. The local connector is a cost candidate only; its mating geometry and PCB footprint must be checked before any order.

## Option 1 line-by-line plan

All LCSC line prices below are the archived Phase B price multiplied by 26,500 VND/USD. `Target` is installed plus one. Local rows are generic candidates, not claims that the local item is the exact Murata/Yageo/Vishay MPN.

| # | Required MPN | Installed | Target | Buy | Route and price basis | Line cost (VND) | Source / decision |
| ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1 | `RT0603BRD071KL` | 2 | 3 | 20 | LCSC, $0.0298 × 20 | 15,794.00 | [C110776](https://www.lcsc.com/product-detail/C110776.html); exact 0.1% divider resistor |
| 2 | `BZT52C12-7-F` | 3 | 4 | 10 | LCSC, $0.0771 × 10 | 20,431.50 | [C124196](https://www.lcsc.com/product-detail/C124196.html); exact HV gate/supply zener |
| 3 | `0451003.MRL` | 1 | 2 | 5 | LCSC, $0.2556 × 5 | 33,867.00 | [C13982](https://www.lcsc.com/product-detail/C13982.html); exact 3 A input fuse |
| 4 | `BZT52C3V3-7-F` | 1 | 2 | 10 | LCSC, $0.0528 × 10 | 13,992.00 | [C151564](https://www.lcsc.com/product-detail/C151564.html); exact level-shift zener |
| 5 | `0805W8F1002T5E` | 4 | 5 | 50 | Local, 50 × 56 VND | 2,800.00 | [Thegioiic 10 kΩ 0805](https://www.thegioiic.com/dien-tro-10-kohm-0805-1-); generic 1%, 0.1 W candidate; verify gate/fault power |
| 6 | `EEUFR1H101` | 1 | 2 | 5 | LCSC, $0.3259 × 5 | 43,181.75 | [C178702](https://www.lcsc.com/product-detail/C178702.html); exact input electrolytic |
| 7 | `SRP1265A-6R8M` | 1 | 2 | 2 | LCSC, $1.1431 × 2 | 60,584.30 | [C2041326](https://www.lcsc.com/product-detail/C2041326.html); exact 6.8 µH inductor |
| 8 | `TNPW060333K2BEEA` | 1 | 2 | 5 | LCSC, $0.0909 × 5 | 12,044.25 | [C2075328](https://www.lcsc.com/product-detail/C2075328.html); exact 33.2 kΩ precision resistor |
| 9 | `0603WAF1001T5E` | 4 | 5 | 50 | Local, 50 × 38 VND | 1,900.00 | [Thegioiic 1 kΩ 0603](https://www.thegioiic.com/dien-tro-1-kohm-0603-1-); generic 1%, 0.1 W candidate |
| 10 | `C0402C220J4GACTU` | 1 | 2 | 50 | LCSC, $0.0171 × 50 | 22,657.50 | [C2168192](https://www.lcsc.com/product-detail/C2168192.html); exact 0402 C0G/NP0 feed-forward capacitor |
| 11 | `0603WAF1000T5E` | 7 | 8 | 50 | Local, 50 × 76 VND | 3,800.00 | [Thegioiic 100 Ω 0603](https://www.thegioiic.com/dien-tro-100-ohm-0603-1-); generic 1%, 0.1 W candidate |
| 12 | `0603WAF1300T5E` | 1 | 2 | 100 | LCSC, $0.0014 × 100 | 3,710.00 | [C22796](https://www.lcsc.com/product-detail/C22796.html); exact 30 Ω line, no local 30 Ω evidence used |
| 13 | `0603WAF1501T5E` | 9 | 10 | 100 | LCSC, $0.0020 × 100 | 5,300.00 | [C22843](https://www.lcsc.com/product-detail/C22843.html); exact 500 Ω ballast, no 510 Ω substitution |
| 14 | `0603WAF100JT5E` | 1 | 2 | 20 | LCSC, $0.0032 × 20 | 1,696.00 | [C22859](https://www.lcsc.com/product-detail/C22859.html); exact 0 Ω link |
| 15 | `IRF9540NPBF` | 2 | 3 | 5 | LCSC, $0.3593 × 5 | 47,607.25 | [C2575](https://www.lcsc.com/product-detail/C2575.html); exact 100 V input/reverse P-FET |
| 16 | `0603WAF1003T5E` | 2 | 3 | 50 | Local, 50 × 76 VND | 3,800.00 | [Thegioiic 100 kΩ 0603](https://www.thegioiic.com/dien-tro-100-kohm-0603-1-); generic 1%, 0.1 W candidate |
| 17 | `TYN612RG` | 1 | 2 | 2 | LCSC, $0.6784 × 2 | 35,955.20 | [C262993](https://www.lcsc.com/product-detail/C262993.html); exact crowbar SCR |
| 18 | `TVS3300DRVR` | 1 | 2 | 2 | LCSC reference, $0.5261 × 2 | 27,883.30 | [C2863624](https://www.lcsc.com/product-detail/C2863624.html); exact TVS, current stock OPEN |
| 19 | `LM61460AANRJRR` | 1 | 2 | 2 | LCSC, $1.8929 × 2 | 100,323.70 | [C2864505](https://www.lcsc.com/product-detail/C2864505.html); exact buck controller |
| 20 | `TL431BIDBZR` | 2 | 3 | 5 | LCSC, $0.0784 × 5 | 10,388.00 | [C41283](https://www.lcsc.com/product-detail/C41283.html); exact TL431B devices |
| 21 | `GRM188R71C104KA01D` | 1 | 2 | 2 allocated / 10 shared | Local, 10 × 190 VND shared lot | 760.00 | [Thegioiic 100 nF 0603 50 V](https://www.thegioiic.com/tu-gom-0603-100nf-0-1uf-50v); generic decoupling candidate; verify 0603 fit |
| 22 | `BC807-40,215` | 1 | 2 | 20 | LCSC, $0.0200 × 20 | 10,600.00 | [C57316](https://www.lcsc.com/product-detail/C57316.html); exact crowbar PNP |
| 23 | `GRM188R71H104KA93D` | 2 | 3 | 3 allocated / 10 shared | Local, same shared 100 nF lot | 1,140.00 | [Thegioiic 100 nF 0603 50 V](https://www.thegioiic.com/tu-gom-0603-100nf-0-1uf-50v); generic input decoupling candidate |
| 24 | `GRM21BR71C105KA01L` | 2 | 3 | 10 | Local, 10 × 400 VND | 4,000.00 | [Thegioiic Samsung 0805 1 µF 25 V catalog](https://www.thegioiic.com/suppliers/samsung/tu-gom-dan-smd/146); 0805 candidate, verify dielectric and DC-bias |
| 25 | `GRM32ER61C476KE15L` | 8 | 9 | 10 | LCSC, $0.3135 × 10 | 83,077.50 | [C77101](https://www.lcsc.com/product-detail/C77101.html); exact 1210 output capacitors, MOQ/pack increment 5 |
| 26 | `GRM32ER71H106KA12L` | 4 | 5 | 5 | LCSC, $0.3322 × 5 | 44,016.50 | [C77102](https://www.lcsc.com/product-detail/C77102.html); exact 1210 50 V input capacitors |
| 27 | `MMBTA42-TP` | 1 | 2 | 10 | LCSC reference, $0.0583 × 10 | 15,449.50 | [C78715](https://www.lcsc.com/product-detail/C78715.html); exact 300 V NPN, current stock OPEN |
| 28 | `TNPW0603100KBEEA` | 2 | 3 | 5 | LCSC, $0.0797 × 5 | 10,560.25 | [C844888](https://www.lcsc.com/product-detail/C844888.html); exact 100 kΩ 0.1% feedback resistor |
| 29 | `TNPW0603100RBEEA` | 1 | 2 | 5 | LCSC, $0.0922 × 5 | 12,216.50 | [C844889](https://www.lcsc.com/product-detail/C844889.html); exact 100 Ω precision divider resistor |
| 30 | `TNPW060310K0BEEA` | 2 | 3 | 10 | LCSC, $0.0711 × 10 | 18,841.50 | [C844890](https://www.lcsc.com/product-detail/C844890.html); exact 10 kΩ 0.1% divider resistor |
| 31 | `RT0603BRD0724K6L` | 2 | 3 | 20 | LCSC, $0.0354 × 20 | 18,762.00 | [C861250](https://www.lcsc.com/product-detail/C861250.html); exact 24.6 kΩ precision resistor |
| 32 | `0451007.MRL` | 1 | 2 | 5 | LCSC, $0.2345 × 5 | 31,071.25 | [C99548](https://www.lcsc.com/product-detail/C99548.html); exact 7 A output fuse |
|  | **Totals** | **—** | **—** | **—** | **LCSC 700,010.75 + local 18,200.00** | **718,210.75** | Local 100 nF rows share one ten-piece lot; it is charged once. |

### Exact-part boundary

The local rows are deliberately limited to generic resistors and decoupling capacitors. The following remain exact LCSC/authorized-distributor MPNs: `IRF9540NPBF`, `TL431BIDBZR`, `TVS3300DRVR`, `TYN612RG`, `0451003.MRL`, `0451007.MRL`, `LM61460AANRJRR`, `SRP1265A-6R8M`, `GRM32ER61C476KE15L`, all precision feedback/threshold resistors, both input high-voltage zeners, `MMBTA42-TP`, `BC807-40,215`, and the exact `C0402C220J4GACTU` C0G capacitor. The local candidates must not be used if their package, voltage, dielectric, tolerance, power, or temperature behavior fails review.

## Local and fabrication purchases outside the 32 lines

| Item | Quantity / basis | Cost (VND) | Status and evidence |
| --- | --- | ---: | --- |
| Generic VH3.96 2-pin connector kit with male/female and crimp contacts | 3 kits; 2 installed ports + 1 spare | 4,719 | [Thegioiic listing](https://www.thegioiic.com/bo-dau-noi-vh3-96mm-2-chan-thang-kem-kim-bam-day), 1,573 VND/kit, stock and price observed 2026-10-05. **ASSUMED/OPEN:** verify mating, footprint, contact resistance, creepage, and crimp range before use. If it cannot mate with the released board, revert to the exact connector procurement and add its lot cost. |
| Red and black 18 AWG / 0.75 mm² wire | 1 m red + 1 m black; cut as four 0.5 m leads for input/output and one spare pair | 15,048 | [Red wire](https://www.thegioiic.com/day-dien-don-nhieu-loi-dong-rv-0-75-0-75mm2-mau-do) and [black wire](https://www.thegioiic.com/day-dien-don-nhieu-loi-dong-rv-0-75-0-75mm2-mau-den), 7,524 VND/m each, observed 2026-10-05. Verify current, insulation, crimp barrel, and final harness length. |
| Heat-shrink, labels, strain relief | Small local allowance | 4,952 | **ASSUMED**, rounded with wire to the 20,000 VND harness line. |
| Five bare PCBs | 80 × 60 mm, 2-layer, 1 oz, 1.6 mm FR-4; one order of five | 53,000 | [JLCPCB public prototype offer](https://jlcpcb.com/ads/pcb-prototype), **ASSUMED** entry-price basis from Phase B, not a configured quote. |
| LCSC shipping/import reserve | One component order | 80,000 | **ASSUMED** small-parcel planning reserve. [LCSC says shipping varies with weight, method, and destination](https://www.lcsc.com/help-center/shipping-delivering/shipping-cost-calculation); checkout is OPEN. |
| JLCPCB shipping/tax/handling reserve | One five-board order | 120,000 | **ASSUMED** planning reserve. [JLCPCB states that shipping is selected/estimated during checkout and duties/taxes are extra](https://jlcpcb.com/help/article/shipping-methods-and-delivery-time); no quote was placed. |
| Local delivery | One combined local order | 20,000 | **ASSUMED** Vietnam courier/pickup-to-lab reserve; zero only if the lab can collect in person. |
| Manual assembly and consumables | Existing lab tools/reflow path | 50,000 | **ASSUMED**, retained from Phase B. |
| Miscellaneous/rework contingency | First-build reserve | 50,000 | **ASSUMED**, retained from Phase B; does not cover unresolved safety parts. |
| SCR sink, insulation, mounting hardware | Option 1 crowbar | 40,000 | **ASSUMED**, retained from Phase B; sustained SCR fault thermal behavior is not proven. |

## Price and total reconciliation

**CALCULATION:**

```text
Exact LCSC rows                     700,010.75 VND
Local generic rows                   18,200.00 VND
Core electronics                   718,210.75 VND

Connectors                            4,719.00 VND
PCB                                  53,000.00 VND
Wire/heat-shrink/strain relief       20,000.00 VND
LCSC shipping reserve                80,000.00 VND
JLCPCB shipping reserve             120,000.00 VND
Local delivery                       20,000.00 VND
Assembly/consumables                 50,000.00 VND
Misc/rework                          50,000.00 VND
SCR thermal hardware                 40,000.00 VND
Non-core overhead                   437,719.00 VND

Option 1 C total                  1,155,929.75 VND
```

The result is not an available landed quote. LCSC and JLCPCB shipping are both **ASSUMED** until a checkout/quote exists; the local listings are price snapshots, not purchase reservations. Current LCSC availability must be rechecked immediately before any release.

### Exact authorized fallback risk

The saved LCSC page for `TVS3300DRVR` currently reports stock OPEN. The saved Phase B input also marks `MMBTA42-TP` stock OPEN. Exact fallbacks were found at authorized distributors: [DigiKey TVS3300DRVR](https://www.digikey.com/en/products/detail/texas-instruments/TVS3300DRVR/7044059) and [DigiKey MMBTA42-TP](https://www.digikey.com/en/products/detail/mcc-micro-commercial-components/MMBTA42-TP/717401). Their observed unit prices were higher than the LCSC references; substituting the two required units of each would add approximately **41,467 VND before any separate authorized-order shipping, tax, or handling**. Do not silently substitute, split orders, or claim the base total is buyable until this stock/open item is resolved.

## Five biggest savings versus the Phase B Option 1 C baseline

1. Replace the archived exact connector minimum lots with three local generic connector kits: **258,784 VND** saved (`263,503 - 4,719`). This is conditional on mechanical and electrical interface verification.
2. Share one local 0603 100 nF ten-piece lot between the two generic decoupling lines: **43,282.50 VND** saved against the two old LCSC minimum lots (`45,182.50 - 1,900`).
3. Reduce the wire/strain-relief allowance from the Phase B 35,000 VND assumption to a short 18 AWG harness plus heat-shrink: **15,000 VND** saved. The harness length remains OPEN.
4. Buy a local 0805 1 µF 25 V generic lot for the 0805 `GRM21...` lines: **12,456.50 VND** saved against the old LCSC minimum (`16,456.50 - 4,000`). Package/dielectric/DC-bias verification is required.
5. Buy a local 0805 10 kΩ generic lot: **6,210 VND** saved (`9,010 - 2,800`). Verify the gate/fault power screen before accepting it.

The next component savings are local 0603 1 kΩ (**4,990 VND**) and local 0603 100 Ω (**4,680 VND**). The new 20,000 VND local-delivery reserve and 20,000 VND increase in combined shipping reserves are included in the total, so they are not hidden as savings.

## Open risks and release gates

- **OPEN / budget:** the evidenced plan is 155,930 VND over the ceiling. A shared-stock donation, verified free shipping, or other real quote would have to close that gap; none is booked here.
- **OPEN / exact stock:** resolve `TVS3300DRVR` and `MMBTA42-TP` stock before ordering. Authorized fallbacks remain exact-MPN options only.
- **OPEN / local connector:** confirm that the generic VH3.96 kit mates with the intended harness and that the released PCB footprint is compatible. This sourcing task does not authorize a hardware edit.
- **OPEN / local passives:** confirm package, tolerance, rated voltage, dielectric, DC-bias capacitance, temperature coefficient, and power dissipation against the Phase B calculations. Any failure returns that line to exact LCSC/authorized sourcing.
- **OPEN / landed freight:** obtain one LCSC checkout and one JLCPCB quote to replace the 80,000/120,000 VND assumptions. Import tax and carrier handling can move the result upward.
- **OPEN / electrical safety:** this plan does not validate 64 V input cutoff, reverse-polarity behavior, SCR thermal survival, fuse coordination, Pi-rail overshoot, ripple, inrush, or any other electrical requirement. ERC/DRC, if later run, would not close these risks.
- **DECISION:** keep Option 1 as the sourcing comparison, but do not authorize fabrication or first power-on from this document. Follow the project bring-up sequence only after the architecture, schematic, PCB, and fabrication-readiness gates are passed.

No carts, logins, orders, purchases, or manufacturing actions were performed. No files outside this document were edited.

SOURCING-HANDBACK
