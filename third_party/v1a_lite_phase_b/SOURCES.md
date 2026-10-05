# V1A-Lite Phase B source register

Access date for this packet: **2026-10-04**. Manufacturer documents were referenced for engineering facts, never copied as PCB designs. No reference circuit has been implemented. Copyright remains with each owner; no open redistribution license is asserted. Required attribution: retain manufacturer, exact document/revision and URL when citing/adapting later. No upstream source was modified. Downloaded PDFs used for reading were temporary; factual catalog/model responses below are the intentionally retained third-party evidence.

| Owner / document | URL / exact revision | Relevant source / studied function | Reuse and modifications |
| --- | --- | --- | --- |
| TI LM61460 | https://www.ti.com/lit/ds/symlink/lm61460.pdf ; SNVSBD5D, July 2022 | Read-only sibling datasheet `LM61460AANRJRR.pdf`; §§7.4/9.2.2/tables 9-3–9-5; buck design and current limit | Referenced; proposed values differ; no circuit copied |
| Bourns SRP1265A | https://www.bourns.com/docs/product-datasheets/srp1265a.pdf ; Rev. 06/24 | Table p1, dimensions, L/current and thermal curves | Referenced only; no modifications |
| Murata SimSurfing | https://ds.murata.com/simserve/characteristics ; undated dynamic model, exact requests and response hashes in `MURATA*OBSERVATIONS.json` | 47 µF 10/16 V, input and VCC capacitor DC-bias data; both unsuccessful and successful excitation queries retained | Referenced; interpolation is our calculation; responses unchanged |
| TDK 22 µF candidate | https://product.tdk.com/info/en/documents/chara_sheet/c3225x7r1c226m250ac.pdf ; January 4, 2016 | One-page part characterization; no numeric plotted point claimed | Referenced only; not selected |
| KEMET C0402C220J4GACTU | https://search.kemet.com/download/specsheet/C0402C220J4GACTU ; dynamic sheet revision OPEN | 22 pF, 16 V C0G identity; LCSC C2168192 cross-check | Referenced; not a circuit |
| LCSC exact product pages | Every URL in `LCSC_OBSERVATIONS.json`; undated live pages accessed 2026-10-04 | Identity, stock, MOQ/multiple, complete USD tier lists, linked PDF URL | Factual extracts only. No checkout/login/cart; no guarantee of future stock or delivered price |

`LCSC_OBSERVATIONS.json` is direct public-page `__NEXT_DATA__` extraction, selecting **webData for the requested part**, not the similar-parts list. Zero stock and failed requests are preserved. A catalog price is not engineering evidence. Use manufacturer PDFs for limits. Do not substitute another manufacturer's same-looking MPN. No Vietnam stock is asserted without an exact local offer.
