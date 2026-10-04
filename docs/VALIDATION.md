# Current validation — Gate2, 2026-09-29

**PRELIMINARY — R2 BLOCKED — NOT FOR FABRICATION.** Current commands:

```sh
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/sheet03/V1A_gate2.net.xml
python3 -B scripts/calculate_sheet03_gate1b.py --gate 2
```

Expected: repository PASS,15 tests PASS, capture integrity PASS followed by R2
release BLOCKED. For every Sheet03 copper pad, add
`--footprints /Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints`
to the capture checker on this workstation. The checker now understands the
real opposed-FET/crowbar circuit; the earlier empty-output assertions and
historical test netlist have been superseded.

The repository checker uses the reviewed
[Gate2 preservation record](evidence/r2/sheet03/GATE2_SCOPE.json), retaining
unchanged historical hashes and separately documenting scoped changes. Do not
update hashes to hide unreviewed edits. Current fresh ERC is 0 violations;
source declarations represent the fitted paths and are independently checked.
See [Gate2 validation](evidence/r2/sheet03/GATE2_VALIDATION.md).

Use the fresh KiCad command forms below with outputs in ignored scratch space.
For the current capture, ERC's expected exit is0; a historical undriven-U402
error is no longer expected. Do not compare current contracts against an old
pre-capture netlist. The full marked PDF can be reproduced using a Python
environment with PyMuPDF:

```sh
python scripts/export_sheet03_review.py --kicad-cli /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli --review-dir /Users/quockaiser/Desktop/Research/V1A_review_2026-09-29
```

The strict R0/R1 cache checker remains unchanged and still fails on the archived
source/predecessor snapshot. Its130 issues were recorded, not reported as PASS.
No bench or electrical safety conclusion follows from these software checks.

---

The following instructions describe the **historical2026-09-26 cleanup state**.
Their old netlist,10-test count and expected ERC error are preserved context;
the current Gate2 instructions above take precedence.

# Repository validation and reproduction

Run from repository root. Python 3.11 and KiCad 9.0.6 were used in the existing evidence. No runtime software build is currently applicable. These are non-destructive checks; R2 and R3 remain BLOCKED.

## Checks without vendor caches

```sh
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/forensic_2026-09-14/V1A_qualified.net.xml
python3 -B scripts/calculate_r2.py
python3 -B scripts/calculate_pi_interface.py
python3 -B scripts/calculate_r2_qualification.py
```

Expected: repository links/JSON/current-source preservation check succeeds; 10 regression tests pass; capture checker reports integrity PASS followed by **R2 RELEASE BLOCKED**; calculators print conditional JSON results. The tests include deliberate Kelvin reversal, wrong reverse-protection connection, host pull-up supply error, and output-boundary bypass attempts. They use retained netlist evidence; fresh export below checks current source capture.

The repository checker records archived-document references separately and verifies hardware bytes against the cleanup baseline. A deliberate future hardware edit requires reviewed new preservation evidence; do not silently update hashes just to pass. Missing files, changed hardware bytes, broken links, malformed JSON, new PCB, or capture invariant violations are failures to investigate.

`python3 -m pytest -q` is optional if pytest is installed. It was unavailable in the system interpreter during cleanup; the same tests passed with `unittest`, without installing system packages. For optional tools use a local virtual environment, not system configuration changes.

## Fresh read-only KiCad validation

Set `KICAD_CLI` to the executable on your workstation; on the audited macOS installation it is `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.

```sh
KICAD_CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
mkdir -p tmp/validation
"$KICAD_CLI" sch export netlist --format kicadxml --output tmp/validation/V1A.net.xml hardware/kicad/V1A.kicad_sch
python3 -B scripts/check_r2_schematic.py --netlist tmp/validation/V1A.net.xml
"$KICAD_CLI" sch erc --format json --exit-code-violations --output tmp/validation/ERC.json hardware/kicad/V1A.kicad_sch
```

Expected: netlist exports; capture invariants pass; ERC returns **exit 5 with one `power_pin_not_driven` error at U402 pin 1**, zero warnings/exclusions. That result documents the open `VOUT_PROTECTED` supply path, not ERC PASS. Additional violations or disappearance of the expected error require review. Never fix this by adding a flag or bypass.

Manual source review: open the current project without saving/re-serializing it, inspect the five-sheet hierarchy and separate Sheet 03 nets, verify project library resolution and the three footprint assignments, and confirm no project PCB exists. Compare any exported netlist with the capture checker; exports must go to ignored scratch space or an explicitly dated evidence folder.

## Historical audit and generators

`python3 -B scripts/check_r0_r1_docs.py` is a strict historical cache audit. It passed before cleanup (122 hashed records, three repository pins). On a fresh clone it is expected to fail for archived downloads/checkouts; it also evaluates recorded historical hashes rather than granting present release. It has deliberately not been weakened to label missing evidence PASS. Restore the original snapshot and run the archived checker there for exact historical reproduction; see [third-party restoration](../third_party/README.md). Use `check_repository.py` for portable current-tree hygiene.

`build_qualified_footprints.py` requires PyMuPDF and the exact hashed TI LM61460 PDF at its original ignored cache path. It writes footprint files: it is a regeneration tool, not a check. Restore the source and reproduce in an isolated copy, then inspect the diff. `build_r2_schematic.py` writes schematics from historical contracts and must not be run as routine validation of the current design. `export_r2_bom.py` writes review-only output; it does not authorize procurement.

No PCB, fabrication exports, design regeneration, or bench test is part of repository hygiene. See [cleanup evidence](REPOSITORY_CLEANUP.md) for the actual session results.
