# Layout preparation — source provenance

Read 2026-10-03. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Project baseline

- Repository: https://github.com/KaiserRichard/edge-ai-smart-power-module
- Capture commit: `6d25cf28c4d246417c0a89ec89574c702850e069`, branch `feat/r2-testboard-capture`.
- Relevant files: `hardware/kicad/V1A.kicad_pro`, all six `*.kicad_sch`, `V1A_Qualified.pretty`, `docs/evidence/r2/gate4b/{captured.xml,PIN_REVIEW.md,CHECK_C1C3.md,*_block.json}`, and `third_party/gate4b/SOURCES.json`.
- Guide base: `8f9ebe5576a8aa177948b5e772ae4e815ec85446`, branch `docs/pcb-layout-guide`, `docs/pcb/LAYOUT_GUIDE.md`.
- Use: current project connectivity/part identity referenced; assigned footprints transferred unchanged in geometry to the new board. No circuit redesign or placement.

## Manufacturer layout documentation

All entries below were **REFERENCED** for placement guidance. No circuit or third-party PCB was copied. Upstream modifications: none. TI and ADI retain manufacturer copyright; no open redistribution license is asserted. Required attribution: preserve manufacturer, title, URL, revision and section in the placement guide. Original text is paraphrased into project-specific instructions. No manufacturer PDFs are committed.

The official documents were opened through the web tool. Existing local TI LM61460/TPS2663/INA228 copies under the guide worktree's ignored `third_party/documents/layout_guide/` were also read; local TPS25947/TPS709 copies are already registered by Gate4B. No new local PDF retrieval or hash is claimed. The layout sections do not specify numeric component-to-component distances; close/short/same-side/Kelvin constraints were retained without inventing millimetre limits.

| ID | Manufacturer document / exact revision | Relevant source section |
| --- | --- | --- |
| P1 | [TI TPS2663x](https://www.ti.com/lit/ds/symlink/tps2663.pdf), SLVSE94G, June 2024 | §9.6, pp38–40; QFN Figure 9-18 |
| P2 | [TI LM61460](https://www.ti.com/lit/ds/symlink/lm61460.pdf), SNVSBD5D, July 2022 | §11, pp47–49; Figure 11-2 |
| P3 | [ADI LTC7001](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf), Rev. G | p14, PC Board Layout Considerations |
| P4 | [TI UCC27511](https://www.ti.com/lit/ds/symlink/ucc27511.pdf), SLUSAW9F, November 2014 | §11–12, pp27–28 |
| P5 | [ADI LT4363](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf), Rev. C | pp16–17, Layout Considerations; C1–C3 pin check retains -1 MSOP |
| P6 | [ADI LTC3115-1](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc3115-1.pdf), Rev. E | pp30–32, PCB Layout Considerations, Figures 15/17 |
| P7 | [TI TPS25947](https://www.ti.com/lit/ds/symlink/tps25947.pdf), SLVSFC9C, May 2026 | §8.4, pp62–64 |
| P8 | [TI TPS7A16](https://www.ti.com/lit/ds/symlink/tps7a16.pdf), SBVS171F, October 2015 | §10, pp19–21 |
| P9 | [TI TPS709](https://www.ti.com/lit/ds/symlink/tps709.pdf), SBVS186H, July 2021 | §10.1, p16 |
| P10 | [TI TLV3201](https://www.ti.com/lit/ds/symlink/tlv3201.pdf), SBOS561C, May 2024 | §8.4, p18 |
| P11 | [TI INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf), SLYS021A, May 2022 | §9–10, p39 |
| P12 | [TI TCA9517](https://www.ti.com/lit/ds/symlink/tca9517.pdf), SCPS242D, July 2017 | §11–12, pp15–16 |

## KiCad standard footprint library

- Repository: https://gitlab.com/kicad/libraries/kicad-footprints
- Exact Git commit: `f64dbd713b8e5c0f6d8638d6794cda5938b3c7e7` (tag `9.0.6`; annotated tag object `0836ca140b415055e373de97c466961088d8972a`). Confirmed with `git ls-remote`.
- Relevant source files: all 24 paths in [KICAD_LIBRARY_CHECK.json](KICAD_LIBRARY_CHECK.json), including each installed and upstream SHA-256. **All 24 match.** Raw upstream files are isolated under ignored `third_party/documents/layout_prep/kicad-footprints/`.
- License: [CC-BY-SA 4.0 with KiCad design exception](https://www.kicad.org/libraries/license/), read 2026-10-03. The exception waives article 3 for electronic designs and generated files using library material. It does not apply to redistribution as a library collection.
- Function: standard passive, IC, diode, transistor, capacitor and test-pad land geometry already assigned in the schematic.
- Use: **COPIED as footprint instances into the authored board**, with geometry unchanged. Refdes, values, schematic UUID links, fields, assembly attributes, and pad nets are supplied by the V1A schematic. No stock library file was modified; no whole PCB reused.
- Attribution: KiCad library contributors and this license/source record retained voluntarily for design provenance. This commit does not distribute a separate stock-library collection.

## KiCad tools and documentation

- Installed CLI/SWIG API: KiCad `9.0.6`; script uses the installed `pcbnew.py` function signatures. No KiCad source code copied or modified.
- [PCB Editor manual](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html), manual 9.0, documentation revision `152cd19e`, based on 9.0.9: shared net-class settings and forward annotation.
- [Library license page](https://www.kicad.org/libraries/license/), accessed 2026-10-03; no page revision published.
- Documentation license: KiCad Documentation Contributors, GPL-3.0-or-later or CC-BY-3.0-or-later. Referenced, not copied. Retain links and contributor attribution; upstream changes: none.

## Resume review, 2026-10-03

Reopened the official P3 LTC7001 Rev. G p14, P4 UCC27511 SLUSAW9F §§11–12 pp27–28 and P6 LTC3115-1 Rev. E pp30–32 sources above. Rechecked compact driver/bypass paths and FE-package grounding against the current netlist. Clarified the guide's U317 PGND pins/thermal path and continuous local shield, and flagged the UCC27511 shield/star-return arrangement for reconciliation with the system ground plan before routing. These sections give qualitative proximity constraints, not numeric part-to-part distances. Use remains REFERENCED; no upstream modifications, new PDF redistribution or circuit changes. The manufacturer, revision, URL, licensing and attribution records above continue to apply.
