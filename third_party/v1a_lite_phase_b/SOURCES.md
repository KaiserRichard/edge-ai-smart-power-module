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

## Resume engineering sources — accessed 2026-10-05

The same copyright/no-redistribution-license/reference-only/attribution policy above applies to every entry below. Local filenames identify reading evidence, not an upstream design reused in CAD. No vendor file was modified. Earlier catalog observations remain dated 2026-10-04.

| Owner / document | URL / exact revision | Relevant files and function studied | Use / modification |
| --- | --- | --- | --- |
| TI TL431 | https://www.ti.com/lit/ds/symlink/tl431.pdf ; SLVS543S, May 2024 | `/private/tmp/liteb/tl431.txt`; §6.12 industrial B-grade reference tolerance, current and cathode-voltage dependence | Referenced; proposed divider and PNP interface are our analysis |
| TI TLV1701 | https://www.ti.com/lit/ds/symlink/tlv1701.pdf ; SBOS589D, June 2015 | `/private/tmp/liteb/tlv1701.txt`; §§7.6–7.7, open-collector output, offset and delay | Referenced; minimal disconnect concept only |
| TI TPS25947 | https://www.ti.com/lit/ds/symlink/tps25947.pdf ; SLVSFC9C, May 2026 | `/private/tmp/liteb/TPS259470LRPWR.txt`; §§6–7, limits, OVLO, FET and restart behavior | Referenced; no EVM/PCB copied |
| ST TYN612 | https://www.st.com/resource/en/datasheet/tyn612.pdf ; DocID7475 Rev 11, October 2016 | Tables 1–4 and temperature/trigger curves; TYN612RG specifically (not TRG) | Referenced; proposed crowbar, no PCB copied |
| Littelfuse 451/453 | https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1 ; GD. 12/01/25 | pp1–3; 3 A and 7 A, clearing, melting I²t, derating | Referenced; no modification |
| Diodes DMP4015SPS | https://www.diodes.com/assets/Datasheets/DMP4015SPS.pdf ; DS35518 Rev 13-2, 2026 | `/private/tmp/liteb/dmp4015.txt`; electrical, charge and thermal tables (web reopen failed; saved manufacturer PDF used) | Referenced only |
| Diodes DMP6023LE | https://www.diodes.com/assets/Datasheets/DMP6023LE.pdf ; DS37199 Rev 3-2, January 2015 | `/private/tmp/liteb/dmp6023.txt`; input P-FET | Referenced only |
| TI TVS3300 | https://www.ti.com/lit/ds/symlink/tvs3300.pdf ; SLVSDO2C, February 2018 | `/private/tmp/liteb/tvs3300.txt`; DRV clamp and waveform ratings | Referenced only |
| TI reverse battery application note | https://www.ti.com/lit/an/slva139/slva139.pdf ; SLVA139, September 2003 | P-FET topology used by inherited Step 2 | Referenced, no CAD copied |
| TI LM74700-Q1 | https://www.ti.com/lit/ds/symlink/lm74700-q1.pdf ; SNOSD64G | Alternative ideal-diode block from inherited Step 2 | Referenced, not selected |

## Addendum 2 and completion sources — accessed 2026-10-05

| Owner / exact document | URL / revision | Relevant source / use | License, attribution, modifications |
| --- | --- | --- | --- |
| Infineon IRF9540NPBF | https://www.infineon.com/dgdl/Infineon-IRF9540N-DataSheet-v01_01-EN.pdf?fileId=5546d462533600a401535611cfa21dc8 ; v01_01, printed 01/04 | Ratings, charge, SOA and TO-220; PDF pp1/2/4 inspected, detailed hot SOA remains OPEN | Manufacturer copyright; referenced only, no modifications; retain Infineon/document citation |
| MCC MMBTA42 | https://www.mccsemi.com/pdf/Products/MMBTA42%28SOT-23%29.pdf ; Rev.3-3-12012020 | Manufacturer indexed PDF text: 300V VCEO and SOT-23 limits; direct reopen returned 403. Gate-driver characterization remains OPEN | Manufacturer copyright, factual reference only; retain MCC/revision; no modifications |
| Nexperia BC807 series | https://assets.nexperia.com/documents/data-sheet/BC807_SER.pdf ; Rev.8, 1 July 2022 | PNP ratings, gain grade and saturation test conditions; gate-drive assumptions distinguished from specs | Manufacturer copyright; referenced only; retain citation |
| Diodes BZT52C family | https://www.diodes.com/assets/Datasheets/BZT52C2V4-BZT52C51.pdf ; revision OPEN | Manufacturer retrieval failed. LCSC exact 3.3V identity and price saved; minimum/maximum clamp at actual current remains OPEN. Existing 12V identity from draft retained | No manufacturer curve claimed; no copied design, retain supplier identity |
| JST VH connector | https://www.jst-mfg.com/product/pdf/eng/eVH.pdf ; printed revision OPEN; live manufacturer page https://www.jst-mfg.com/product/index.php?lang=2&series=262 | Family rating is wire/header-dependent: 10A with AWG16 standard header, 7A with AWG18 shrouded header. Exact planned mating/temperature qualification OPEN | JST copyright, reference only; retain manufacturer citation |
| JLCPCB prototype offer | https://jlcpcb.com/ads/pcb-prototype ; undated public page accessed above | Advertised $2/5pcs for selected standard ≤100×100mm orders; estimating basis, not configured delivered quote | Commercial page copyright; factual price/conditions only |
| Existing project Phase A and R2 procurement ledgers | Local `docs/evidence/v1a_lite/PHASE_A_BOM.csv`, `docs/evidence/r2/BOM_ORDER.csv`, `docs/evidence/r2/bom_order/BOM_ACCESSORIES.csv`; baseline db2a88c | Exact JST header, housing and contact unit prices/minimum lots; their URLs and observation dates retained in BOM | Internal engineering evidence reused, originals unchanged |

New price requests only: IRF9540NPBF C2575, MCC MMBTA42-TP C78715, BZT52C3V3-7-F C151564; direct-page observations added to the existing JSON, without refreshing previous quotes. MMBTA42-TP has zero stock. A Nexperia MMBTA42,215 search produced no exact usable offer and is OPEN; no repeated search. UENPO facts are owner requirements from Addendum 2, not manufacturer-derived claims. The brief's upstream module is not a third-party PCB reused or copied here.
