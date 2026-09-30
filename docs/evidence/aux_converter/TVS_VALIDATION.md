# TVS re-selection — validation and owner status

2026-09-30 · branch `feat/v1a-input-tvs` · base `50c94e05a4896b6d95ec13019e4c722a6ae2c1bf` (`origin/feat/v1a-input-withstand` at setup).

## Scoped manager record

- **STATUS: BLOCKED for electrical qualification; analysis deliverable complete.** PRELIMINARY — NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.
- **WHAT WAS DONE:** reconcile frozen input/Pi requirements and raw-node topology; compare six TVS options; select provisional SMCJ36CA and 3403.0285.23; calculate a labelled pulse/temperature envelope, auxiliary stress, hot fuse hold, normal peak/trim and four-module scores; prepare the owner handout and decisions.
- **EVIDENCE:** [report](TVS_RESELECTION.md), [input audit](TVS_INPUT_AUDIT.md), [pinned internal hashes](TVS_INPUT_PROVENANCE.json), [primary source register](TVS_SOURCES.md), [deterministic results](TVS_CALCULATIONS.json), [calculator](calculate_tvs_reselection.py). Input audit committed/pushed as `5c86254`; calculation/source sub-step committed/pushed as `84630ac`; final report/validation follows in a separate focused commit.
- **DECISIONS:** larger bidirectional 36 V-standoff TVS for qualification; 12.5 A time-lag fuse for the assumed 85 °C local hold envelope; independent bounded auxiliary/input fault paths recommended; retain downward-trim enquiry, drop unconditional 23 V rule; TEP 200-7215UIR is an enquiry candidate, recommended module NONE.
- **OPEN RISKS:** guaranteed hot clamp/leakage/energy, raw auxiliary voltage limit, actual fuse mounting/hold/clearing coordination and prospective source current/L/R, exact passive parts, normal/startup/module-fault peaks, hot usable power, reverse exposure and protected buck/Pi fault containment. No proven whole-board continuous withstand value is available.
- **NEXT GATE:** owner engineering review and closure of those source/thermal/fault contracts before a separately authorized circuit implementation and dummy-load validation. No gate is advanced by this paper selection.

The existing manager report is unchanged because this task permits only new files under `docs/evidence/aux_converter/`. These fields provide the manager record within that authorized scope.

## Checks performed

| Check | Result and limits |
|---|---|
| Exact baseline inputs | **PASS:** eight documentary files match their pinned Git bytes and SHA-256 identities in TVS_INPUT_PROVENANCE.json. Only `.md` / `.json` input contents were read; no native CAD or netlist content was opened. |
| Deterministic arithmetic | **PASS:** `python3 -B docs/evidence/aux_converter/calculate_tvs_reselection.py --check` reproduces the saved JSON without writing. Assertions check inherited OVP identity, pulse-envelope arithmetic, selected fuse voltage and assumed hold screen. |
| Independent pulse integral | **PASS:** numerical midpoint integration at 0.1 µs, through 25 exponential time constants, independently gives 0.007166340 C and 0.017936682 A²s; agreement with analytical charge/I²t within 1e-7 / 1e-6 relative respectively. Units distinguish joules from fuse A²s. |
| Independent module audit | **PASS:** read-only reviewer confirmed error/trim/power arithmetic and OPEN/NONE verdict; review prompted explicit trigger-versus-peak field names, startup/step labels and retention of known module mismatches. |
| Independent TVS audit | **PASS:** read-only reviewer checked exact selected TVS row, assumed hot derating, pulse arithmetic, auxiliary/reverse/let-through consequences and OPEN verdict; mounting/thermal conditions and buck provenance added. |
| Owner explanation | **PASS:** 401 words excluding its heading; one-page text handout. Its layout has not been claimed as a typeset PDF. |
| Links and document consistency | **PASS:** local file links and existing heading anchors resolve; final report and JSON have the same MPNs and OPEN/NONE verdict. Manufacturer links are direct sources; unavailable guaranteed values remain OPEN. |
| Change scope and formatting | **PASS:** staged/delivered changes checked for whitespace and new-file-only scope relative to the pinned base; every added path is under `docs/evidence/aux_converter/`. Baseline documents/code/CAD unchanged. |

## What was not validated

No schematic/PCB/symbol file was opened, read or saved during this TVS task. No circuit, component value, footprint, ERC setting or net was changed. ERC/DRC and circuit-dependent test suites were not run for this documentation-only study; they would provide no hardware withstand evidence and may read prohibited CAD inputs. No hot/cold, surge, fuse interruption, thermal, startup or single-fault hardware test was performed. No purchase, fabrication, merge or supplier communication occurred.

The 35 V continuous fault target, ≤60 V raw-node pulse ceiling, 0.45 J surge envelope, 85 °C fuse ambient, temperature factors and voltage reserves remain labelled assumptions. Catalogue standoff and initial-tolerance computations are not a proven V1A continuous rating. Test first with current-limited sources and dummy loads; use a Pi only after electrical review and prior validation stages pass.

**VERDICT: NEW D101 SMCJ36CA, F101 3403.0285.23, V1A WITHSTANDS OPEN V continuous, RECOMMENDED MODULE NONE.**
