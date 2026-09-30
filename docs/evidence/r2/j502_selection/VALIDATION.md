# J502 selection completion evidence

2026-09-30. **PASS for the documentary checks below; qualified hot 5 A delivery remains BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Continued both partial commits, ending at `89590ab9283f494448189ba2fdecd96a199b03d3`; did not restart connector selection. The full selection and resume briefs were read. Their current identities and the preserved earlier resume-file identity are in [INPUT_PROVENANCE.json](INPUT_PROVENANCE.json).

## Completed checks

| Check | Evidence / result |
|---|---|
| Inherited arithmetic | `python3 docs/evidence/r2/j502_selection/calculate.py --check` reproduces the checked-in [CALCULATIONS.json](CALCULATIONS.json). No arithmetic change was needed. |
| Separate numerical reconstruction | [validate.py](validate.py) does not import or execute `calculate.py`. Decimal arithmetic reconstructs the hot divider minimum from 0.99 V, the 100 kΩ/24.4 kΩ divider, ±0.25% and the inherited −10 nA bias screen. It builds individual Pi branches, combines their conductances, and adds both trunks and every other series allocation. All four D/E results and the report's rounded values agree. This verifies arithmetic, not the assumed inputs. |
| Negative cases | Both E proposals fail the 100 mV excursion and the unchanged 13.6 mΩ module-FET screen. Qualified application minima remain `null` in the calculations. |
| Physical pin coverage | Report table and JSON agree: positive 2/4, grounds 6/9/14/20/25/30/34/39, each exactly once. Odd/even row and station coordinates and equal-share currents also checked. This does not verify TE moulded cavity numbers or a built harness. |
| Input provenance | Current hashes and byte counts agree for both task briefs, the independent footprint review and three pinned PATH_BUDGET files. The earlier resume hash was stale; it is preserved separately rather than discarded. |
| Remote input pins | Final read-only `git ls-remote origin refs/heads/feat/v1a-5a-path-budget refs/heads/feat/v1a-footprints-complete` returned `ebe51b9e141588d118d74daf37e65a3bd2307c1f` and `51d1c2ff1f7eca4f20eef137c1595e4b9e052a75`. Existing objects were reused. The earlier fetch failure is retained in provenance; no merge or setup restart was needed. |
| Sources | All source records retain identity/revision or an explicit unversioned limitation, URL, reviewed sections, use, licence and attribution. The two successfully cached, hash-recorded PDFs (T3 and X5) match their SHA-256 values. Other records retain their web-only/download limitations; no missing hash or released specification was invented. |
| Links | All relative file links in the selection report, this record, the source README and the J502 manager-report section resolve. Historical unrelated manager sections were not re-audited. |
| Scope / whitespace | All changed tracked files and non-ignored new files versus `51d1c2f` are limited to the J502 report/evidence/source register and manager report. `git diff --check` passes. No KiCad, library, footprint, PCB, project-setting or upstream-reference file changed. |
| Owner PDF | One A4 page, exported using PyMuPDF 1.28.2 and [export_owner.py](export_owner.py). Key voltages, fabrication warning, qualification limits and final recommendation survive text extraction. The actual rendered page was visually reviewed for clipping, legibility, table flow and completeness. |

## Manufacturer evidence rechecked at completion

The [source register](../../../../third_party/j502_selection/SOURCES.json) remains the authoritative URL/revision map. Final review re-opened T1/T2 product records, T3's preliminary attachment, T4 application specification, M1's current specification, M2/M4 identities, P1/P2 and W1/W2. Earlier alternative screening was preserved, not represented as newly repeated research.

- **T3:** visually inspected PDF pages 10/11 (specification pages 7/8): Figure 3 includes the female termination and wire span, so a separate full crimp allowance must not be added again to that same span. Figure 4 gives loading-dependent current; its fully loaded screen does not support 2.5 A/contact. The high-pressure 30 µin gold durability category is 50 cycles, not the standard-pressure 200-cycle category. Applicability to the actual Pi mate and required life remain OPEN.
- **T1/T4:** the selected housing remains 40 positions / two rows / 2.54 mm, and the wire-diameter versus housing-depth restriction remains relevant. The current S5 drawing and standalone Rev B specification again failed web retrieval. No new drawing or released-specification acceptance is claimed; the prior S2 extracted-text limitation is retained.
- **M1:** confirmed the two-circuit AWG16 current-table entry, matching-plating requirement, initial/rated-current contact resistance, separate crimp resistance and conditioning **change** criterion. The report does not substitute a 50 A headline or a Δ-resistance criterion for a hot application maximum.
- **P1/P2 and W1/W2:** confirmed the retained connector and wire families against live manufacturer records. Catalogue/test readings and nominal wire DCR still do not establish the complete hot assembly bounds.

No vendor material was modified or newly committed. Review renders remain temporary; manufacturer PDFs remain in the ignored `third_party/documents/j502_selection/` cache. A clean clone must retrieve the pinned external inputs and those review PDFs before reproducing the complete provenance audit. The arithmetic-only check does not need that cache.

## Reproduction and handoff

From the repository root:

```sh
python3 docs/evidence/r2/j502_selection/calculate.py --check
python3 docs/evidence/r2/j502_selection/validate.py
```

The PDF exporter requires PyMuPDF. The existing isolated dependency directory was reused with `PYTHONPATH=/private/tmp/j502-python python3 docs/evidence/r2/j502_selection/export_owner.py`; no system configuration was changed. It also renders `/private/tmp/j502-owner-review.png` for manual review. PDF byte identity across exports is not required; page content and layout are the checked outputs.

**DECISION:** retain A as the first qualification candidate and B as the board-connector fallback. Both share the unresolved Pi contact/current limit, so B cannot cure a failed Pi-end rating. Analysis deliverables are complete; the brief's ≥4.75 V hot worst-case requirement remains unqualified. Complete supplier/mechanical/electrical review and later dummy-load validation before any SBC integration.

**Publication:** local commit only, as authorized by the brief; the conductor owns push and draft PR creation. No ERC/DRC rerun applies to this documentation-only change, no physical tests were performed, and no execution gate advanced.
