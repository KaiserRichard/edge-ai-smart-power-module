# PCB layout source record

All manufacturer documents are REFERENCED for independently authored placement/routing. No third-party PCB is copied. No upstream files were modified. Manufacturer copyright applies; no redistribution license is inferred. Retain the linked manufacturer, revision and section attribution below. Downloaded PDFs/page images are isolated under ignored `third_party/documents/pcb_layout/`.

| Source | Exact revision / sections | Relevant local material / use |
|---|---|---|
| https://www.ti.com/lit/ds/symlink/lm61460.pdf | SNVSBD5D, July 2022, §11, pp47–49, Figure 11-2; visually reviewed p49 on 2026-10-04 | `scripts/layout_v1a.py`, `scripts/v1a_copper.py`: paired local input loops, bootstrap, quiet-side feedback, underlying GND, separate buried VIN strap. Test links and large inductor are project deviations, not TI-qualified geometry. |
| https://www.analog.com/media/en/technical-documentation/data-sheets/ltc3115-1.pdf | Rev E, pp30–32, FE Figure 17 | Auxiliary converter FE pin/loop placement. Web document read; local download initially failed. |
| https://www.ti.com/lit/ds/symlink/tps2663.pdf | SLVSE94G, June 2024, §9.6, QFN Figure 9-18 | Input power/ground and EP25 thermal-via arrangement. |
| Existing project guide | `ad04d28`, `docs/pcb/LAYOUT_GUIDE.md`; copied read-only guide at step 0 | Per-sheet critical cluster requirements; source P1–P12 citations retained verbatim in the guide. |
| Current schematic/footprint contracts | `5f371fd`, `hardware/kicad/*.kicad_sch`, `V1A_Qualified.pretty`, `third_party/gate4b/SOURCES.json`, `third_party/layout_prep/SOURCES.md` | Unchanged native package lands and pin mapping; source licenses and upstream versions are recorded in those ledgers. |
| Frozen path calculation | `23624ee`, `docs/evidence/r2/R203_OPTION_A.md` and `r203_option_a/CALCULATIONS.json` | 24.6k setpoint and 41.855546 mΩ send+return allocation; not changed by layout. |

KiCad stock footprint/library provenance remains in `third_party/layout_prep/SOURCES.md` and `KICAD_LIBRARY_CHECK.json` (9.0.6 upstream pins and license attribution). Project scripts are original work; no Freerouting or external router was installed or used.
