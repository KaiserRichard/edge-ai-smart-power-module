# Qualification verification and reproduction

2026-09-14. Branch `feat/r2-schematic-recovery`, baseline HEAD `bc2379025a6320dff9186724a03f6e1ab0db7019`. All continuation work is uncommitted. **R2 BLOCKED, R3 BLOCKED. NOT FOR FABRICATION.**

## Observed results

| Check | Result / scope |
| --- | --- |
| KiCad9.0.6 netlist export | Exit0; [qualified netlist](V1A_qualified.net.xml),71 physical entries,47 named nets |
| KiCad ERC, all severities | Exit5; exactly one error, U402 pin1 `power_pin_not_driven`; [report](ERC_qualified.json). No added exclusions, PWR_FLAG or severity changes |
| Current netlist checker | PASS pin contracts, hierarchy, Kelvin polarity, local/host domains and open output boundary; release still BLOCKED |
| Tests |10 passed:5 existing capture regressions and5 new independent footprint dimensional/paste/pin checks |
| Existing R2 and Pi calculations | Rerun to new files; unchanged values/bytes as applicable; all sensitivity assumptions preserved |
| New qualification calculation | Fuse current sweep and candidate loop loss at1/3/5A; config hash recorded; no measured values |
| Footprint parser/export | KiCad exported all3 project footprints successfully; copper/paste/body/courtyard visual review completed |
| Restore-point comparison | All47 net groups and component identities/fields unchanged. Reversing only the3 Footprint strings restores all pre-existing hardware hashes and all10 corresponding restore-ZIP members |
| Scope | No authored `.kicad_pcb`; no routing, Gerbers, board DRC, fabrication, commit or push |

[Change manifest](qualification_change_manifest.json) lists this continuation's files separately from pre-existing dirty changes. All three regenerated footprints are byte-identical to the project library. Documentation/source integrity audit: `qualification_documentation_complete.json` (122 stored hash records). An initial check caught a link to its not-yet-written output; that ordering issue was corrected without weakening the checker.

[Machine-readable preservation comparison](qualification_preservation.json), [assignment log](footprint_assignments.json), [review BOM](BOM_QUALIFIED_REVIEW.md), [new assumptions](qualification_assumptions.json) and [calculated results](qualification_calculations.json). Fresh R2/Pi outputs have `_qualified` filenames solely to keep old evidence untouched; the filename does not mean electrical qualification.

## Footprint visuals and manual verification

[U201 copper/paste](footprints/TI_RJR0014A_LM61460.svg), [Q101 copper/paste](footprints/TI_Q3_CSD19537Q3.svg), [R401 Kelvin lands](footprints/Vishay_WSL2726_Kelvin_1Fplus_2Splus_3Sminus_4Fminus.svg). The SVGs are intentional review exports, not manufacturing files. Source diagrams were visually inspected alongside exported views; geometry/pin extents were independently checked in tests. Temporary raster views stay under ignored `tmp/r2-qualification/`.

Manual checklist for later independent review: U201 upper-left pin1/noEP15, both VIN/PGND sides and split SW paste; Q101 lower1/2/3 source and4 gate, upper8/7/6/5/common drain and reduced paste; R401 narrow2/3 sense pads on the same designated side, wide1/4 force pads. Check every labelled dimension against the pinned PDF, not only nominal package size. In later layout, verify thermal/current return and Kelvin routing separately. DRC/assembly/thermal validation cannot be performed on a nonexistent board and are not implied here.

**Known limitation:** the source manufacturers provide recommended/example lands; project courtyard/mask choices and the shunt paste default need assembly review. L201 and all nine TDK footprints remain OPEN. The historical checker does not demand blank footprints, so it was not weakened or migrated. Historical build_r2_schematic.py is not a safe regeneration command for the manually recovered working capture.

## Reproduce into an empty scratch directory

From repository root, using installed KiCad9.0.6 and Python3; footprint generator additionally requires PyMuPDF (available in `.venv`). Create a new directory if the example outputs already exist. No global environment changes are needed.

```sh
mkdir -p tmp/r2-qualification-recheck
.venv/bin/python scripts/build_qualified_footprints.py --output-dir tmp/r2-qualification-recheck/V1A_Qualified.pretty
python3 -m unittest discover -s tests -v
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli fp export svg --output tmp/r2-qualification-recheck/svg --layers F.Cu,F.Paste,F.SilkS,F.Fab,F.CrtYd tmp/r2-qualification-recheck/V1A_Qualified.pretty
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch export netlist --format kicadxml -o tmp/r2-qualification-recheck/V1A.net.xml hardware/kicad/V1A.kicad_sch
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch erc --format json --severity-all --exit-code-violations -o tmp/r2-qualification-recheck/ERC.json hardware/kicad/V1A.kicad_sch
python3 scripts/check_r2_schematic.py --netlist tmp/r2-qualification-recheck/V1A.net.xml
python3 scripts/calculate_r2.py --output tmp/r2-qualification-recheck/r2.json
python3 scripts/calculate_pi_interface.py --output tmp/r2-qualification-recheck/pi.json
python3 scripts/calculate_r2_qualification.py --output tmp/r2-qualification-recheck/qualification.json
python3 scripts/export_r2_bom.py --netlist tmp/r2-qualification-recheck/V1A.net.xml --output tmp/r2-qualification-recheck/BOM.md
```

Run commands independently: ERC's expected exit5 must not prevent subsequent checks. Expected outputs are exactly the results table above. Compare regenerated footprint bytes with project files and normalized pin-to-net mappings with the prior export. A changed manufacturer hash, pad dimension/number, joined output nets, newly driven U402 without approved protection, extra ERC violation, changed component value/net or unexpected board file is a failure requiring review. Fontconfig warnings appeared during KiCad exports; exports completed and no system configuration was changed.

**Rollback:** use [continuation baseline](continuation_baseline.json) and [assignment log](footprint_assignments.json); after checking for later edits, clear only the3 added Footprint strings, remove only this continuation's new library/table/scripts/tests/evidence, and remove only its additive manager/blocker updates. Never reset the dirty working tree or restore an entire old schematic over the user's recovery. The earlier `reduction_baseline.json`, restore ZIPs, forensic netlist/ERC and previous reports remain historical evidence.
