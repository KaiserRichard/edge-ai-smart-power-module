# Completion validation record

2026-09-30. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Baseline: `1f4c2f821793506871b9abe6227b1deba419d27e`. Tool: KiCad9.0.6 at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`. Python3.11 standard-library checkers; project-local `.venv` with PyMuPDF1.28.2 for rendering. No system configuration changes. Manufacturer source caches and virtual environment are not committed.

| Check | Result / evidence |
|---|---|
| Baseline XML and ERC captured before editing | 154 physical components, 24 blank footprints; baseline ERC0; immutable XML retained |
| Sheet01 checkpoint | `cdd5f2e`: PR7 test pads; ERC0; corrected duplicate-field canonical comparison proves only TP101/TP102 footprint strings changed |
| Sheet02 checkpoint | `df5c817`: eight TDK assignments; ERC0;10 cumulative allowed field changes |
| Sheet03 checkpoint | `000e7b4`: two concrete button connector MPN/footprints; ERC0;14 cumulative field changes |
| Sheet04 checkpoint | `9018949`: C404/four test pads; ERC0;19 cumulative field changes |
| Sheet05 checkpoint | `03bc815`: three board connectors/four test pads; ERC0;32 cumulative field changes |
| Canonical comparison | PASS;24 Footprint +5 MPN +3 Value changes only; all154 components/94 nets preserved. Raw XML, canonical JSON and full diff retained |
| Source preservation | PASS; all six schematic files identical outside permitted instance property string values; project, symbol library and library tables byte-identical |
| Physical pad numbering | PASS; every assigned footprint exists and copper numbers match its exported symbol. F101/L201 blank, D101 held unchanged |
| Regression suite | PASS:31 tests, including every nonexcluded physical part made empty/placeholder in adversarial subcases |
| Hardware/source evidence chain and links | PASS;24 hardware files, five new project footprint files; historical evidence retained |
| Footprint reproducibility | PASS; independently rebuilt all five files into `/tmp/v1a_footprint_rebuild`; byte-identical to working library |
| Native footprint export | PASS; all five accepted by KiCad SVG exporter, rendered with pad numbers/Fab/courtyard/hole outlines, visually reviewed |
| PDF | PASS; six landscapeA3 pages; pages1–5 pixel-identical at96dpi; page6 pixel-identical after masking only the three changed connector Value bounds |
| Visual review | Native Sheet03/05 and five enlarged footprint SVG renderings inspected. No unexpected label/wire/symbol movement; capacitor orientation, connector pin1 marks, boss/fixing-hole arrangement and courtyard reviewed |
| External delivery | Refreshed requested `V1A_REVIEW_READABLE.pdf`; hash equals repository deliverable. Original external file preserved under timestamped backup; paths/hashes in PDF_COMPARISON.json |
| Owner briefing | One-page434-word approximate plain-English PDF companion; source text in FOOTPRINTS_COMPLETE.md |

Run from this worktree (use your local KiCad executable path):

```sh
kicad-cli sch export netlist --format kicadxml -o /tmp/v1a-fresh.xml hardware/kicad/V1A.kicad_sch
kicad-cli sch erc --format json --exit-code-violations -o /tmp/v1a-erc.json hardware/kicad/V1A.kicad_sch
python3 scripts/check_footprint_completion.py --netlist /tmp/v1a-fresh.xml
python3 scripts/check_r2_schematic.py --netlist /tmp/v1a-fresh.xml --footprints /Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
git diff --check
```

Footprint build example: `python3 scripts/build_completion_footprints.py --part tdk --output-dir /tmp/rebuilt.pretty`. Other part selectors: `xh2`, `xh4`, `vh`, `phoenix`. Native preview: `kicad-cli fp export svg --footprint <name> --layers F.Cu,F.SilkS,F.Fab,F.CrtYd,Dwgs.User --sketch-pads-on-fab-layers --output /tmp/footprint-preview hardware/kicad/V1A_Qualified.pretty`.

No PCB editing, DRC, manufacturing exports/orders, purchases, electrical bench tests or SBC power-on occurred. Clean ERC/pad tests are consistency evidence; held component decisions, inherited electrical blockers and J502 hot contact qualification remain OPEN.

Historical source notes are not rewritten. The first provisional Sheet01 XML comparison omitted KiCad's duplicate `<fields><field name="Footprint">`; the corrected canonicalizer explicitly handles/checks both representations and passes. The initial documentation check saw its own output file truncated by shell redirection and a not-yet-created capture log; writing checker results outside the repository then copying them after completion resolves this without changing checker rules. Neither transient tooling issue was an electrical mismatch or an ERC waiver.
