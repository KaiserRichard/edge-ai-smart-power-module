# V1A-Lite layout sources — 2026-10-05

All manufacturer material is REFERENCED, with copyrights retained and no open redistribution license asserted. No external PCB was copied or upstream file modified. Attribution is retained here and in the layout report. Original downloaded vendor content is not distributed in this packet.

| Source and exact revision | Relevant material | Use / modification / attribution |
| --- | --- | --- |
| Texas Instruments LM61460, SNVSBD5D, July 2022, https://www.ti.com/lit/ds/symlink/lm61460.pdf | §11 pp47–49, Figure 11-2; package pins | REFERENCED. Adapted functional layout guidance: paired input bypasses, short SW, separate feedback side, thermal vias. Two-layer 1 oz cost study differs from recommended four-layer 2/1/1/2 oz stack. No TI PCB copied. Credit Texas Instruments. |
| JLCPCB PCB capabilities, live page accessed 2026-10-05, no published revision, https://jlcpcb.com/capabilities/pcb-capabilities | Drilling, traces, solder mask; 1 oz two-layer process | REFERENCED for rule limits and 18 µm average barrel-plating sensitivity. Project constraints are generally more conservative; capability is not an electrical rating or production guarantee. No content copied. Credit JLCPCB. |
| KiCad 9.0.6 installed footprints | Exact files/hashes in ../../docs/evidence/v1a_lite/layout/FOOTPRINT_SOURCES.json | Existing footprints retained. KiCad library contributors, CC-BY-SA 4.0 with electronic-design exception; https://www.kicad.org/libraries/license/. No stock library modified. |

Manufacturer footprint/pin/MPN provenance remains in ../v1a_lite_phase_d/SOURCES.md and ../v1a_lite_fix1/SOURCES.md; these are referenced without rewriting history.

Project-owned helper provenance (not a third-party PCB): wt-fabprep/scripts/export_fab_package.py was read and adapted into scripts/export_lite_fab.py for Lite BOM fields, two layers, strict DRC acceptance and review warnings. The matching PDF rasterizer was already committed in the Lite worktree. wt-pathcheck/scripts/check_5a_path.py was read for comparison only; its research nets/budgets were not applied. No sibling worktree was modified. Exact sibling source hashes/commits are in LOCAL_HELPERS.json.
