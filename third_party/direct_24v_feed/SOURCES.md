# Direct feed source provenance

Access/read date: **2026-10-04**. Project baseline: `5f371fd7c59e90a5037004b9309bff63b0d95e71`, branch `docs/v1a-direct-24v-feed`, [repository](https://github.com/KaiserRichard/edge-ai-smart-power-module). Relevant project sources: native `hardware/kicad/*.kicad_sch`, `docs/context/*`, `docs/evidence/r2/gate4b/`, and `docs/evidence/r2/R203_OPTION_A.md`. A fresh CLI netlist was exported to temporary scratch space and inspected; historical Gate4B exports predate the R203 change.

All manufacturer material below was **REFERENCED**, not adapted or copied into circuitry. Function studied: supply compatibility, protection thresholds, ratings, fuse/TVS coordination and buck dissipation. No upstream modifications; no third-party PCB inspected or copied. License: respective manufacturer copyright; no open redistribution license asserted. Attribution retained here and in the report by manufacturer, title, URL, revision and page. No manufacturer PDFs are committed. [SOURCE_HASHES.json](SOURCE_HASHES.json) pins the exact local PDFs read and the two downloaded module PDFs.

Local filenames below are relative to the read-only `/Users/quockaiser/Desktop/Research/wt-datasheets/third_party/datasheets/`. Page numbers refer to PDF pages, coinciding with printed pages for the cited component tables.

| ID | Manufacturer/document and URL | Exact revision / relevant pages | Relevant local source / function |
| --- | --- | --- | --- |
| S1 | [TI TPS2663x](https://www.ti.com/lit/ds/symlink/tps2663.pdf) | SLVSE94G, June 2024; pp5–9, 19–20, 37–40 | `TPS26630RGER.pdf`; absolute/operating ratings, comparator/timing, cutoff/recovery and transient layout |
| S2 | [Vishay SMCJ5.0A–SMCJ188CA](https://www.vishay.com/docs/88394/smcj.pdf) | 88394, 09-Jan-2024; pp1–4 | `SMCJ36CA.pdf`; bidirectional convention, SMCJ36 row, pulse/DC thermal ratings |
| S3 | [SCHURTER UMT-H](https://www.schurter.com/en/datasheet/typ_UMT-H.pdf) | 21.07.2026, printed on p5 and PDF metadata; pp3–5 | `3403.0285.23.pdf`; exact fuse row, footnote 4, pre-arcing times and test copper |
| S4 | [TI LM61460](https://www.ti.com/lit/ds/symlink/lm61460.pdf) | SNVSBD5D, July 2022; pp4–6, 16, 32, 35, 47–49 | `LM61460AANRJRR.pdf`; ratings, losses, BIAS, efficiency curves, layout |
| S5 | [Würth 74437636351002](https://www.we-online.com/components/products/datasheet/74437636351002.pdf) | 001.000, 2025-02-07; pp1–3 | `74437636351002.pdf`; current captured inductor, DCR and application-dependent heating |
| S6 | [Vishay TNPW e3](https://www.vishay.com/docs/28758/tnpw_e3.pdf) | 28758, 10-Apr-2026; pp1–4, 12 | `TNPW0805348KBEEA.pdf`, `TNPW060315K8BEEA.pdf`; resistance, B/E suffix tolerance/TCR, rating and aging limitations |
| S7 | [TI CSD19537Q3](https://www.ti.com/lit/ds/symlink/csd19537q3.pdf) | SLPS549B, November 2022; pp1, 3 | `CSD19537Q3.pdf`; reverse-path MOSFET voltage ratings |
| S8 | [onsemi BSS138](https://www.onsemi.com/pdf/datasheet/bss138-d.pdf) | BSS138/D Rev7, April 2024; p2 | `BSS138.pdf`; local VDS/VGS, not voltage to ground |
| S9 | [Murata GRM32ER72A105KA01L](https://www.murata.com/en-global/products/productdetail?partno=GRM32ER72A105KA01%23) | GRM32ER72A105KA01-01A, specification as of 2026-06-26; p2 rated values | `GRM32ER72A105KA01L.pdf`; pre-eFuse/auxiliary raw capacitor rating |
| S10 | [Vishay BAT46W](https://www.vishay.com/docs/86406/bat46w.pdf) | 86406, Rev1.1, 20-Nov-2025; p1 | `BAT46W-E3-08.pdf`; auxiliary input diode ratings |
| S11 | [onsemi FDB33N25](https://www.onsemi.com/pdf/datasheet/fdb33n25-d.pdf) | FDB33N25/D Rev3, January 2022; pp1–2 | `FDB33N25TM.pdf`; auxiliary pass FET rating |
| S12 | [ADI LT4363](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf) | Rev C; pp2–4, 8–11 | Web, no new local PDF/hash claimed; independent auxiliary surge stopper, not main feed protection |
| S13 | [ADI LTC3115-1](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc3115-1.pdf) | Rev E; pp1–4 | Web, no new local PDF/hash claimed; downstream auxiliary converter operating/absolute ratings |
| M1 | [MEAN WELL DDR-120](https://www.meanwell.com/Upload/PDF/DDR-120/DDR-120-SPEC.PDF) | DDR-120-SPEC **2026-09-10**, PDF p3 C/D specification, p4 block diagram | Downloaded and table visually inspected; DDR-120C-24 normal regulation/trim/isolation/OVP |
| M2 | [MEAN WELL RSD-200](https://www.meanwell.com/Upload/PDF/RSD-200/RSD-200-SPEC.PDF) | RSD-200-SPEC **2025-07-18**, PDF p1 specification, p2 block diagram | Downloaded and table visually inspected; RSD-200C-24 normal regulation/isolation/OVP |

**UENPO S4-T482410: OPEN primary document.** Exact manufacturer datasheet URL, revision, pages, license and attribution requirements could not be established. Web searches on the access date included exact `"S4-T482410"`, `"S4-T482410" datasheet`, `"T482410" 24V`, and UENPO/S4/48-to-24 converter variants. Results were unrelated products or marketplace listings without an authenticated exact-part specification. No reseller claim was promoted to a manufacturer rating. The supplied brief is the source for the assumed case topology, nominal voltages, input range, absence of output OVP and fault scenario. No fabricated source URL or datasheet page is supplied; normal tolerance/trim/dynamic limits remain OPEN.

The brief is `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/DIRECT_24V_FEED.md`, read in full. Engineering findings and reproducible arithmetic are in [DIRECT_24V_FEED.md](../../docs/evidence/r2/DIRECT_24V_FEED.md).
