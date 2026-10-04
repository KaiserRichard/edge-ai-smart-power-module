# Readability correction review — 2026-09-30

REQUIREMENT: Apply the independent VERIFY_GATE2B.md findings against reviewed presentation commit `2cd138f`, retaining the electrical baseline `c47409f`. PRELIMINARY — Sheet 03 BLOCKED — NOT FOR FABRICATION.

The independent report and original crops remain in the external review folder; historical review evidence is preserved in Git. This correction record supersedes the earlier visual PASS for the replaced PDF.

## Sheet checkpoints

- Sheet 01: moved INPUT_PGTH/ILIM/DVDT label anchors beyond the vertical FLT route; centered C103's value below its body between the vertical routes. Actual vector-PDF render reviewed: text unobscured and contained. Fresh canonical netlist diff 0 bytes; all-severity ERC zero; all 20 tests, fresh-netlist contract checker and repository integrity checker PASS.
- Sheet 02: moved C212 and the similarly affected C213 voltage-value fields beyond their vertical pickup routes. Rendered output-bank/feedback detail reviewed; all six capacitors remain visible. Fresh identity/zero ERC/20 tests/contract/repository checks PASS.
- Sheet 03: reorganized the actual control circuit as reference/detector → qualification/latches → run/fault action → series driver from left to right. Crowbar driver sits below the crowbar, with named CB_GATE continuation; series driver caption identifies PROT_GATE/PROT_MID to the power row. Auxiliary rails/reset/ARM occupy the lower support row. Technical references, values, pin names/numbers and net labels increased to 1.524 mm (matching the other pages, about 6.017 PDF pt). All eight bulk values are aligned below their bank; field groups and signal corridors were spaced inside their panels; header/footer moved wholly inside the drawing frame. Actual vector-PDF overview and all affected detail regions reviewed, including final enlarged U310 ARM_CLOCK/BUCK_PGOOD/QUALIFIED crops. Fresh identity/zero ERC/20 tests/contract/repository checks PASS. Retained detail crops: [power](readability/fix/s03_power.png), [control](readability/fix/s03_control.png), [support](readability/fix/s03_aux_reset_arm.png), [header](readability/fix/s03_header.png), [footer](readability/fix/s03_footer.png).
- Sheet 04: extended the SCL_LOCAL/SDA_LOCAL conductor stubs to a clear label column right of both ALERT and supply-decoupling routes. Reviewed the actual [sense-circuit PDF crop](readability/fix/s04_sense.png); the I2C names are unobscured. Fresh identity/zero ERC/20 tests/contract/repository checks PASS.
- Sheet 05: moved the 3V3_HOST/PWR_FLAG return to x=314.96 mm, left of the complete SDA_HOST/SCL_HOST label extents. Reviewed the actual [host-connector PDF crop](readability/fix/s05_host.png); all host names and pin numbers are unobscured. Fresh identity/zero ERC/20 tests/contract/repository checks PASS.

The final independent PDF review also found four crossed signal labels at U403 on Sheet 04. All four repeated SCL/SDA names were moved beyond the crossing routes, using conductor continuations without new junctions. The [separator detail](readability/fix/s04_i2c_separator.png) is clear; fresh identity/zero ERC/20 tests/contract/repository checks PASS again.

## Input provenance and scope

- Independent readability findings: exact retained [input report](readability/fix/VERIFY_GATE2B_INPUT.txt), originally `~/Desktop/Research/V1A_review_2026-09-29/VERIFY_GATE2B.md`, reviewing `2cd138f77190be0871c4b7bc9863db48079f5b74`.
- Cover-note engineering basis: [retained review closure](readability/fix/GATE2C_REVIEW_CLOSURE_INPUT.txt), obtained with `git show origin/feat/sheet03-gate2c:docs/evidence/r2/sheet03/GATE2C_REVIEW_CLOSURE.md`; pinned source commit `0677fea0a32fc87b740949d589abe1588e55934c`. No electrical changes from that branch were imported.
- Electrical baseline: `c47409fb2637c94ccaa685c3ac4cbbd10681d5a2`. Final hardware checkpoint: `46495d2`. Focused sheet commits were pushed after completion: `8b08b5b` (01), `533a47a` (02), `5a57d35` (03), `6ff61dc` (04), `862de4c` (05), then `46495d2` (04 final separator clearance).
- Only presentation geometry/text and its review tooling/evidence changed. Part identities, values, footprints, pins, full net names, memberships, hierarchy and project settings remain identical. No PCB, fabrication release, component order or hardware test was performed.

## Sheet 03: closure of every numbered finding

| Verifier item | Final rendered-PDF observation / disposition |
|---|---|
| 1 — header/footer | Title and complete evidence note lie inside the frame; footer uses two columns. |
| 2 — bulk values | All eight C330–C337 remain visible; aligned reference/value rows clear their leads and plates. |
| 3 — series-FET panel | TP302 VOUT_PROTECTED field is inside the panel; common-source arrangement remains traceable. |
| 4 — ballast/crowbar | Pin numbers are separated from resistor bodies; incoming label has panel clearance; two parallel series strings retained. |
| 5 — auxiliary rails | SUPPLY_OK and DRV_DELAY occupy separate clear segments; C306 and right-side fields are contained; VIN_FUSED lies inside the frame. |
| 6 — series driver | C301 value is contained; driver follows run/fault action and names PROT_GATE/PROT_MID continuation to the FETs above. |
| 7 — detector | C304 and U303 part number have clear, contained field positions. Divider, clamp and reference remain visible. |
| 8 — crowbar driver | CROWBAR_ON is inside the panel with pin clearance; CB_GATE continuation identifies Q303 above. |
| 9 — supply/reset | SUPPLY_OK, RESET_N, GND and DET_5V are independently readable; C322 value remains within the panel. |
| 10 — ARM/history | ARM_N clears pin numbers; ARM_DELAYED clears wires/edge; C324 value is contained. |
| 11 — qualification/latches | OV_OK, U310 part number and C320 fields clear pins/routes/edges; U304/U309 fields are spaced. Final ARM_CLOCK, BUCK_PGOOD and QUALIFIED labels are also separated. |
| 12 — run/fault action | C325 is inside panel/frame; R322 fields clear Q304; input and lower labels occupy clear corridors. |
| 13 — reading order/text | Actual detector → qualification/latches → run/fault action → series driver circuit reads left to right. Power devices above their named driver continuations; support circuitry below. Technical text raised to 1.524 mm; no block placeholders replace circuit detail. |

## Final actual-PDF review

The supplied vector PDF was freshly rendered, with full-page overviews and enlarged affected regions. The verifier's criterion was applied: any confirmed wire/symbol/frame overprint on technical text fails locally, even if the intended string could be inferred. Functional flow, block names and useful sparse net naming were checked separately. Primary owner inspected all six final pages; a separate read-only reviewer inspected the delivered PDF and each original failed criterion, including the additional U403 correction.

| PDF page / sheet | Text | Left-to-right flow | Functional blocks | Useful net labels |
|---|---|---|---|---|
| 1 / top hierarchy | PASS | PASS | PASS | PASS |
| 2 / input protection | PASS | PASS | PASS | PASS |
| 3 / buck | PASS | PASS | PASS | PASS |
| 4 / output protection | PASS | PASS | PASS | PASS |
| 5 / power monitor | PASS | PASS | PASS | PASS |
| 6 / IO/test | PASS | PASS | PASS | PASS |

All six pages are native landscape A3, approximately 419.989 × 297.002 mm, without export scaling. Essential Sheet 03 technical text now matches the other sheets at approximately 6.017 PDF pt. This remains small A3 text; a physical A3 print has not been produced, so physical print comfort is not validated. Export/warning/page dimensions are recorded in [PDF validation](readability/PDF_VALIDATION.json); retained page images and detail crops support the visual findings.

## Electrical proof and delivery

Fresh baseline and final KiCad XML exports compare equal: **154 components, 94 nets, 450 pin memberships; canonical netlist diff 0 bytes**. Complete component/library XML and source inventories also match: **161 symbols / 457 pins including seven power flags**. The comprehensive canonical SHA-256 is `2257bd9f080e02365bf209175b83235a7975dce2e30cef671fc9d480279f09fc`; the independent verifier's narrower ref/value/footprint/lib-ID/net-membership comparator yields `d05d276d194f8cb69ad2c79aea422a650e8037c4adcff2d8d348e041d564da0b` for both exports. These digests cover different canonical representations, each equal before/after.

Fresh KiCad 9.0.6 ERC with `--severity-all --exit-code-violations`: **0 violations**. `V1A.kicad_pro` is byte-identical to baseline, SHA-256 `2f3f1d74c5c1c75bbfb7daa1cc8822c177a31f2dea212aa09cc127ca813c62c5`; exclusions and severities are unchanged. **All 20 tests pass**, together with the fresh-netlist contract checker and repository integrity checker. Existing electrical assertions were preserved; the readability checker now requires 1.524 mm reference/value text on every sheet. The independent fresh-export audit is retained separately from the implementation's recorded XML check.

[Reviewer cover note](REVIEWER_COVER_NOTE.md) and its [one-page PDF](REVIEWER_COVER_NOTE.pdf) retain all four blocking topics, the three OPEN margins with negative counterexamples, and five specific laboratory questions. Its numbers come from the pinned engineering closure and are explicitly conditional calculations, not hardware measurements.

The replacement [review PDF](V1A_REVIEW_READABLE.pdf) and cover PDF were copied to `~/Desktop/Research/V1A_review_2026-09-29/`. Repo/external byte equality, hashes, input provenance and independent evidence are recorded in [final delivery evidence](readability/fix/DELIVERY.json). The review PDF SHA-256 is `61d50d69de3942a87d5ff7381e25f01bbd1eee937a1e1de698e8f4c0a0db0e70`.

Recheck commands from repository root (PyMuPDF required for PDF renderers):

```sh
python3 -B scripts/check_schematic_readability.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/sheet03/readability/readable.net.xml --footprints /Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints
python3 -B scripts/check_repository.py
```

Fresh XML/ERC regeneration uses `kicad-cli sch export netlist --format kicadxml` and `kicad-cli sch erc --format json --severity-all --exit-code-violations` on `hardware/kicad/V1A.kicad_sch`; the baseline is exported from an isolated archive of `c47409f`. `fix_schematic_readability.py --sheet 01` through `05` reproduce corrections from the pinned reviewed presentation; running only the earlier `make_schematic_readable.py` recreates the superseded drawing.

DECISION: READABLE + NETLIST IDENTICAL, presentation review only. PRELIMINARY — Sheet 03 BLOCKED — NOT FOR FABRICATION. Electrical fault energy, timing, temperature, and the three application margins remain OPEN; R3 and hardware qualification remain blocked. Draft PR #8 is updated by branch pushes; no merge.
