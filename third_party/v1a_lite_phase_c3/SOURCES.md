# Phase C3 source and provenance register

Access date: **2026-10-05**. All sources are **referenced**, not copied circuit/PCB implementations. No third-party PCB was inspected or reused. Manufacturer-authored datasheets are authoritative; supplier catalog electrical fields do not override them. Original downloaded PDFs are unmodified here; SHA-256 and exact URLs are in [DOCUMENT_MANIFEST.json](DOCUMENT_MANIFEST.json).

License for each datasheet below: manufacturer copyright / all rights reserved; no open-source license or redistribution grant asserted. Preserve the original copyright, notices, URLs and revision attribution. Attribution in our calculations is manufacturer, document revision and page. Engineering adaptations are our proposed parameter/topology changes described in the C3 report; no modifications to these upstream files.

| Local source file | Exact revision | Function studied / reference pages |
| --- | --- | --- |
| [tps2663.pdf](tps2663.pdf) | TI SLVSE94G, June2024 | pp3–9,17–23,29–40; eFuse, OVP, current limit, reverse blocker and layout |
| [tps25983.pdf](tps25983.pdf) | TI SLVSHH5C, May2026 | pp4,7–10,21–26; rejected low-resistance alternative; downloaded revC supersedes indexed revB |
| [irfr6215.pdf](irfr6215.pdf) | Infineon/IR, 2016-05-31 | pp1–5;150V input PFET replacement, Rds/Qg/SOA; manufacturer-authored LCSC mirror |
| [csd18540q5b.pdf](csd18540q5b.pdf) | TI SLPS488B, April2017 | pp1,3–6;60V reverse-blocking NFET, package and gate charge |
| [rt_resistor.pdf](rt_resistor.pdf) | Yageo RT series V.16, 2025-05-06 | pp2,5–6;34.8k0.1%25ppm ordering, voltage/power/TCR |
| [ap22615.pdf](ap22615.pdf) | Diodes DS41022 Rev7-2, August2026 | pp1,4–5;rejected3A switch,6V input absolute maximum |
| [nis6150.pdf](nis6150.pdf) | onsemi NIS6150/D Rev5, April2026 | pp3–4;rejected10V/1A input path and excessive OVP clamp |
| [sgm2546.pdf](sgm2546.pdf) | SG Micro December2025 | pp1–7;rejected28V absolute maximum,7A family |
| [tps2596.pdf](tps2596.pdf) | TI SLVSET8A, August2019 | pp1,3,5–7;rejected21V/2A family |
| [2n7002_jscj.pdf](2n7002_jscj.pdf) | Jiangsu Changjing J, September2016 | pp1–2;60V ±20V signal NFET, Ciss50pF max; gate pulldown |

Additional references (not downloaded/copied):

- TI TPS25947 **SLVSFC9C, May2026**, [official sheet](https://www.ti.com/lit/ds/symlink/tps25947.pdf), pp7–11:28V absolute maximum and5.5A class; rejected at29V. Historical read-only text at `/private/tmp/liteb/TPS259470LRPWR.txt` and Phase B source register. No modifications, TI copyright, reference only.
- Richtek RT1720 **DS1720-01, November2015**, [indexed official PDF](https://www.richtek.com/assets/product_file/RT1720/DS1720-01.pdf), p5 indexed FB1.20–1.30V; direct PDF fetch404. [Current official product page](https://www.richtek.com/Products/Supervisor/hot-swap-controllers/RT1720.aspx) reports EOL and5V minimum operation. OPEN: full archived sheet unavailable; not selected, no precise timing/voltage guarantee inferred. Reference only, Richtek copyright, no copied circuit.
- Silergy **SQ24802K2 Rev1.0,2025**, [official PDF](https://www.silergy.com/download/downloadFile?ftype=note&id=6315&type=product), pp1,3–4 viewed through browser; direct PDF download unavailable.18V maximum/14V clamp rejects it. Public document bears manufacturer confidential/customer-use notice; link and minimal factual comparison only, no file redistribution or circuit reuse.
- Infineon [IRFR6215 product page](https://www.infineon.com/part/IRFR6215), undated page observed2026-10-05, exact TRPBF orderable listed active. Reference only; supplier stock0 is a separate fact. Product-page580mΩ entry is the datasheet150°C value, not25°C resistance.

Inherited sources remain unmodified in `../v1a_lite_phase_b/`, `../v1a_lite_phase_c/`, and `../v1a_lite_phase_c2/` with their existing registers: TI LM61460 and TL431; ST TYN612 Rev11; Bourns SMCJ; Diodes BZT52; Panasonic FR-A; Murata output MLCC; Littelfuse451/453; prior exact-MPN and local sourcing snapshots. Reuse means the same cited functional blocks/calculation assumptions, not validation. C3 changes the PFET rating, adds the series eFuse and reverse blocker, retunes the backup crowbar, and adds protected-node capacitance. No historical source or evidence was overwritten.

[LCSC_OBSERVATIONS.json](LCSC_OBSERVATIONS.json): read-only public-page factual extraction (supplier copyright), URLs, MPN/manufacturer, stock, MOQ and all price breaks; snapshot2026-10-05, not a reservation or quote. Indexed stale prices were not selected. Exact revisions do not apply to live catalog pages; timestamp and file hash identify this snapshot. Stock0 prices are explicitly reference allowances. ISP14EP15LM was only catalog/product-family screened and rejected for excessive resistance/current capacity; no circuit reused.

Sibling sourcing plan was read only: `/Users/quockaiser/Desktop/Research/wt-litesrc/docs/evidence/v1a_lite/SOURCING_PLAN.md`, date2026-10-05. Its archived hash/line model remains `../v1a_lite_phase_c2/LOCAL_SOURCING_BASIS.json`. C3 preserves its reserve and spare policy, charges the full remaining generic100nF lot, and sources the shared timing-capacitor MPN exactly rather than treating it as generic decoupling.

Reproducer source is original project code, not vendor code. Original lookup helper was adapted from this repository's prior price-extraction workflow; no external implementation licensed or copied. No purchase, contact, cart, order, upstream modification or push occurred.

Additional preliminary catalog screens, reference only/no circuit adaptation: [TI TPS25982](https://www.ti.com/product/TPS25982),30V family with unsuitable fixed OVLO options; [TPS25981](https://www.ti.com/product/TPS25981),20V maximum; [onsemi protected-switch selector](https://www.onsemi.com/design/tools-software/product-recommendation-tools-plus/protected-power-switch/products),NIS3071 minimum8V; [Infineon IRF6215](https://www.infineon.com/part/IRF6215),obsolete through-hole variant; [Vishay IRF9640](https://www.vishay.com/docs/91086/irf9640.pdf),200V alternative; [Infineon ISP14EP15LM](https://www.infineon.com/part/ISP14EP15LM),high resistance. Undated live pages observed2026-10-05; exact archived PDF revisions were not established for these unselected preliminary screens (OPEN). Copyright belongs to each vendor; links/names only, no copied files/circuits.
