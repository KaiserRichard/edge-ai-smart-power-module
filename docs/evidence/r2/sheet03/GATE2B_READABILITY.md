# Gate 2b — V1A schematic readability

REQUIREMENT: presentation only against c47409fb2637c94ccaa685c3ac4cbbd10681d5a2. No electrical changes. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.

## Recovery

OBSERVATION (2026-09-30): branch feat/sheet03-readable was at c47409f with uncommitted redraws of all five sheets, hierarchy, symbol graphics, scripts and proof artifacts. No KiCad editor process, schematic backup or autosave was present. Existing review folder PDFs were V1A_SCHEMATIC_2026-09-29.pdf and V1A_GATE2_PRELIMINARY.pdf. The worktree contained a new V1A_REVIEW_READABLE.pdf.

EVIDENCE: fresh recovered-source export matched the baseline canonical netlist (154 components, 94 nets); all 161 source symbols including power flags were preserved. Fresh ERC with all severities reported zero violations. DECISION: preserve useful work as 22fa287 (`wip: gate2b recovered`), push it, and finish the presentation. The recovered Sheet 03 was A2 and required an A3 correction.

## Changes and sheet checkpoints

- Sheet 01: input fuse/TVS/reverse stage at left, eFuse at right, UV/OV dividers below. Real wire connects reverse stage to eFuse; ground returns are below circuitry. References and values are 1.524 mm. Visual review completed; ERC zero. Checkpoint 9f32136 pushed.
- Sheet 02: input bypass/enable at left, LM61460 in center, inductor/output bank and feedback at right. VIN and switching path use real wires; feedback remains on the existing local raw rail. Notes wrapped clear of title block. ERC zero. Checkpoint saved with this entry.

- Sheet 03: raw capacitor bank, opposed series FETs and ballast/crowbar form the top power path. Auxiliary supplies, reference/OV detector and gate drivers occupy the middle row; reset/ARM, qualification/latches and fault action occupy the bottom row. An on-sheet numbered guide explains detector → latch → series switch + crowbar. A3 fit uses 1.27-mm minimum text and keeps every connection on the original 50-mil grid; project/ERC settings are unchanged. Fresh netlist identical and ERC zero.

- Sheet 04: four-terminal shunt force path reads left to right, sense pins connect to the existing differential filter/INA228 block, telemetry LDO stays above right, and I2C domains occupy a separate lower block. Ground is at each block bottom. Notes wrapped to keep the title clear. Visual review completed; ERC zero.

- Sheet 05: J501 DC input, J502 protected/measured load output, and J503 host I2C appear in left-to-right blocks with bench access below. Existing power flags stay connected; host supply reference remains host-owned. Corrected stale presentation note saying Sheet03 output path was open; the circuit itself is unchanged. Visual review completed; ERC zero.

- Top hierarchy: main power blocks 01 → 02 → 03 → 04 connect with real wires. Sheet 05 shows connector access below; control/host links use existing named nets. Extra label spacing separates IO port names from their wire labels. All six pages retain a title block and fabrication warning.

## Netlist-identical proof

EVIDENCE: the baseline was freshly materialized from Git c47409f into a temporary directory and exported with KiCad 9.0.6. The final redraw was independently exported with the same CLI. Both raw XML exports are retained under [readability](readability/NETLIST_IDENTITY.json).

| Check | Result |
| --- | --- |
| Components, including values/footprints/properties | 154; identical |
| Named nets and every pin membership | 94; identical |
| Source inventory, including nonphysical flags | 161 symbols; identical |
| Canonical JSON diff | 0 bytes; identical |
| Canonical SHA-256 | 2257bd9f080e02365bf209175b83235a7975dce2e30cef671fc9d480279f09fc |
| ERC, all severities including exclusions | 0 violations |
| Pin contracts and proof regression suite | 20 tests PASS |
| Project, ERC settings, footprints and PCB files | Unchanged; no PCB generated |

The comparison retains complete component/libpart XML, full net names, and every node attribute. It normalizes element order and numeric net codes and excludes export date/source/tool/title metadata and library filesystem URIs. Source inventories separately verify symbol UUIDs, library IDs, properties, flags, hierarchy identity, and pin names/numbers/electrical types. Drawing coordinates have no electrical meaning and are excluded. Mutation tests confirm that changed values, footprints, pin membership or removed power flags fail the proof.

Evidence: [raw before](readability/baseline.net.xml), [raw after](readability/readable.net.xml), [canonical before](readability/baseline.canonical.json), [canonical after](readability/readable.canonical.json), [empty diff](readability/netlist.diff), [ERC](readability/ERC.json), [source preservation](readability/GATE2B_SCOPE.json).

## PDF and visual review

EVIDENCE: [V1A_REVIEW_READABLE.pdf](V1A_REVIEW_READABLE.pdf) contains six native vector A3 landscape pages (419.989 × 297.002 mm): top hierarchy plus all five circuit sheets. An identical copy is delivered to `/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf`.

All six pages were visually inspected from 96-dpi renders representing physical-size/100% display scaling; final Sheet 03 and adjusted Sheet 04 were reviewed again after export. References, values, pin identifiers, local labels, block headings, notes and title blocks are readable. Sheet 03 uses 1.27-mm minimum text; other sheets use 1.524-mm references/values. The export stays A3 without fit-to-A4 reduction. Display DPI/viewer scaling affects perceived size. No text block falls outside its page. Long notes were wrapped and Sheet 04 notes raised to stay clear of the lower frame. Native vector lines/text remain zoomable.

[PDF validation and page-image hashes](readability/PDF_VALIDATION.json) record exact dimensions, six fabrication warnings and the PDF SHA-256. Page images are intentional review evidence, not build caches. CLI emitted local Fontconfig configuration warnings; exports succeeded, visible text was checked, and no system configuration was modified.

## How to read this schematic

1. Start with the top hierarchy. Trace `VIN_RAW → VIN_PROTECTED → VOUT_5V1 → VOUT_PROTECTED → LOAD_5V1`. The fuse-derived `VIN_FUSED` branch supplies independent protection auxiliaries.
2. Sheet 01 establishes the input protection and upstream PGOOD/SHDN boundary. Sheet 02 converts the protected input to the existing nominal 5.1-V raw rail; feedback stays before the output disconnect.
3. Sheet 03 top row is the energy path: upstream raw bulk → opposed Q301/Q302 → protected rail and ballast/Q303 crowbar branch. Q301/Q302 share source node `PROT_MID`; the crowbar is a shunt path to ground.
4. Sheet 03 reference/divider/comparator produce `OV_OK`. Supply/reset qualification and BUCK_PGOOD feed the latch logic. ARM sets U304; U309 retains history until RESET. U305 `RUN_GATE` drives U301 and the series FETs. Fault removes run permission and drives U311 `CROWBAR_ON`, U315/Q303 and Q304 input shutdown. RESET then ARM is required; no automatic retry. Follow identically named labels between blocks; short local paths use wires. A crossing without a junction dot is not connected.
5. Sheet 04 measures the force current through R401 with separate Kelvin sense paths. The local monitor supply branches before the shunt. Host/local I2C pull-up domains remain separate.
6. Sheet 05 identifies J501 input, J502 load, J503 host reference/I2C and test points. Begin hardware bring-up with a current-limited bench supply and dummy load under the documented gate procedure.

## Decisions, open risks and checkpoint history

DECISION: Gate 2b presentation PASS. No electrical redesign, component substitution, new requirement, PCB work, manufacturing release or physical validation is implied.

OPEN RISK: existing Gate 2 electrical blockers remain, including fault timing/energy/SOA and transient/stability qualification. Review original Gate 2 evidence and manager packet before progressing. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.

Recovery and each finished sheet were committed and pushed: 22fa287 recovery; 9f32136 Sheet 01; d32cbf9 Sheet 02; 17fc35b Sheet 03; f795504 Sheet 04; 2528c4d Sheet 05. Final hierarchy/PDF/validation evidence follows in the delivery commit.

## Reproduce the checks

From the repository root with KiCad 9 and PyMuPDF available:

```sh
KICAD_CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
baseline_dir=$(mktemp -d /private/tmp/gate2b-baseline.XXXXXX)
git archive c47409f hardware/kicad | tar -x -C "$baseline_dir"
"$KICAD_CLI" sch export netlist --format kicadxml --output docs/evidence/r2/sheet03/readability/baseline.net.xml "$baseline_dir/hardware/kicad/V1A.kicad_sch"
"$KICAD_CLI" sch export netlist --format kicadxml --output docs/evidence/r2/sheet03/readability/readable.net.xml hardware/kicad/V1A.kicad_sch
python3 scripts/check_schematic_readability.py --record
"$KICAD_CLI" sch erc --format json --severity-all --exit-code-violations --output docs/evidence/r2/sheet03/readability/ERC.json hardware/kicad/V1A.kicad_sch
python3 scripts/export_readable_review.py --kicad-cli "$KICAD_CLI"
python3 scripts/check_r2_schematic.py --netlist docs/evidence/r2/sheet03/readability/readable.net.xml
python3 -B -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

`make_schematic_readable.py` reproduces the drawings from the pinned baseline; `--sheet 01` through `05` or `root` supports separate checkpoints. Re-export and verify after any redraw; visual review must follow regenerated PDFs.

VERDICT: READABLE + NETLIST IDENTICAL
