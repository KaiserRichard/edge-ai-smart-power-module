# Codex brief 02: R2 protection analysis with reproducible models (no schematic change)

Paste this whole file into Codex. It supersedes brief 01, which was withdrawn and must not be executed.

- **Repo:** https://github.com/KaiserRichard/edge-ai-smart-power-module
- **Branch:** `feat/r2-sheet03-output-protection`. It already contains Claude's analysis. Pull it and work on top of it; do not branch from `main`.
- **Do not change:** anything under `hardware/`, `scripts/check_r2_schematic.py`, `tests/test_r2_capture.py`,
  `docs/evidence/repository_cleanup_2026-09-26/`. Sheet 03 stays electrically open. R2/R3 stay BLOCKED.
- **Read first:** `CLAUDE.md`, `AGENTS.md`, `docs/evidence/r2/protection_analysis_2026-09-26/PROTECTION_ANALYSIS.md`,
  `REQUIREMENT_ENVELOPE_PROPOSED.md`, `scripts/analyze_output_protection.py`.
- **Goal:** produce the evidence the user needs to approve (or reject) the recommended output-protection architecture
  "option I": ≥ 470 µF bulk on `VOUT_5V1` + precision latching OV detector with ≤ 2 µs gate pull-down of Q302 + LM74800 /
  Q301 / Q302 common-drain path + path enable from BUCK_PGOOD. Your job is evidence, not selection. Label every number
  KNOWN / CALCULATED / SIMULATED / INFERRED / ASSUMED / UNKNOWN.

Put all outputs in a new folder `docs/evidence/r2/protection_analysis_<YYYY-MM-DD>/` (the date you do the work), plus
`simulation/` for netlists.

## Task 1: primary sources

Download and archive under `third_party/documents/r2_protection/`. Record URL, revision and SHA-256 in `source_register.json`,
following the provenance rules in `AGENTS.md`. Read these visually, not only as text:

| Source | What to extract |
| --- | --- |
| TI LM7480-Q1 SNOSD95C | §7.6 `tOVP_OFF(deg)_HGATE`: say which column 3.98 µs and 5.4 µs sit in. The text extraction was AMBIGUOUS. Also tEN_OFF, tDGATE_OFF, HGATE/DGATE sink, and HGATE−OUT vs VS below 5 V |
| TI TPS2663 SLVSE94G | fast-trip threshold/delay, current-limit response, PLIM/timer, OVP delay definition, SHDN behaviour, output-short SOA |
| TI LM61460 SNVSBD5D | output-capacitance guidance, any mention of electrolytic/polymer bulk, soft-start, HS/LS behaviour in faults |
| Coilcraft XAL8080-682 | L tolerance, DCR max, Isat at 10/20/30 %. This replaces the ASSUMED 14 A knee |
| TDK C5750X7R1H226M250KB | DC-bias curve at 5.1 V and 24 V. This replaces the ASSUMED C_in 15–40 µF and C_raw 60–130 µF |
| Vishay SMBJ (88392) | VBR/VC/IR for 26CA and 30CA, derating curves |
| Nexperia PSMN1R8-40YLC | RDS(on) vs VGS and Tj, Qg curve, SOA |

If a download is blocked (Coilcraft and TDK returned HTTP 403 before), say so and ask the user to download it in a browser.
Do not guess the values.

## Task 2: cross-check the Python model with an open SPICE model

Write `simulation/hs_short/*.cir` for ngspice, with the same topology and inputs as `scripts/analyze_output_protection.py`.
Run options A, B2, I and H at the 32 corners. Acceptance: the peak load voltage agrees with the Python model within
±3 % at every corner, or you explain the difference. Then re-run both with the Task 1 values that replace the ASSUMED
inputs, update the `INPUTS` table (keeping labels and sources) and regenerate `protection_model_results.json`.

## Task 3: vendor-model simulations (only if the user has PSpice for TI installed; otherwise list what you need from the user)

1. **LM61460 load step** (TI transient model):
   - input 9 / 12 / 24 V
   - steps 5 → 0 A and 0.5 → 4.5 A at 1 A/µs and 10 A/µs
   - output MLCC only, then + 470 µF with the Task 4 candidate ESR

   Record the raw peak, undershoot, ringing and settling. This closes (or not) the nuisance-trip margin in analysis §4.
2. **LM61460 stability with bulk.** Load-step ringing (count the cycles) and, if the model supports it, loop gain.
3. **High-side short with vendor models.** TPS2663 + LM61460 power stage (force the HS switch shorted, e.g. a 10 mΩ switch
   in parallel) + LM74800. Options A and I. Record the load peak, time above 5.5 and 6.0 V, the raw peak, Q302 VDS, and the eFuse
   current and state.
4. **Start-up** at 9 V, 5 A load, 470 µF bulk: path enabled immediately vs from BUCK_PGOOD. Record the input current against the
   eFuse limit (4.17 A minimum).
5. **Input hot-plug.** 2 m cable (ASSUMED 1.5 µH, 50 mΩ), SMBJ26CA and SMBJ30CA. Record the peaks at U101 IN and U201 VIN and
   the eFuse OV response.

Record the model name, version and date for every run. A vendor simulation is supporting evidence, not qualification.

## Task 4: candidate parts for option I (candidates, not selections)

For each block give 2–3 candidates, each with its datasheet link, the key numbers, an error or timing budget, and footprint size:
- **Bulk capacitor:** ≥ 35 V, ≥ 470 µF effective at 5.1 V (hybrid polymer or polymer), ESR, ripple current, height.
- **Reference:** ≤ 0.5 % initial accuracy, with its tempco.
- **Comparator:** ≤ 100 ns propagation at 10 mV overdrive, 3.3 V supply, push-pull.
- **Detector supply:** LDO rated ≥ 30 V input, valid before the path enables. The existing TPS70933 part is acceptable if its ratings fit.
- **Latch:** a flip-flop, or a comparator with positive feedback. Reset only by the detector supply falling through its UVLO.
- **Gate pull-down stage:** discrete PNP/NPN or equivalent that pulls Q302 gate to OUT in ≤ 1.6 µs including Q302's 96 nC Qg.
  It must never pull HGATE below OUT − 0.3 V (LM74800 absolute limit), must hold against the 55 µA HGATE source current,
  and must not load HGATE by more than 1 µA when idle.

Deliver a window error budget (reference, divider, comparator offset, hysteresis, temperature) showing 5.40 V ± ≤ 1.1 %,
and a timing budget showing trip-to-isolation ≤ 2 µs at worst case.

## Task 5: report

Write `SIMULATION_REPORT.md` in the new folder with:
- each result and its label
- a model-coverage list (what each model omits)
- an explicit pass/fail against the engineering acceptance criteria below
- a one-page block diagram of option I (SVG or PDF, not a KiCad sheet)

Add `tests/test_output_protection_model.py` cases for any model change.

### Engineering acceptance criteria for the approval decision

1. The load-release raw peak (vendor model, all corners) is ≥ 50 mV below the detector's worst-low trip.
2. The hard high-side short (vendor model, all corners) keeps the load ≤ 6.0 V (ASSUMED screening criterion, analysis §3), with no re-enable while input is present.
3. The detector window is ≤ ± 1.1 % and trip-to-isolation is ≤ 2 µs worst case, both by budget.
4. The LM61460 stays stable with the bulk: step response settles without sustained ringing.
5. Start-up input current is ≤ 90 % of the eFuse minimum limit at 9 V / 5 A.
6. Every raw-side part is rated for the source voltage it holds after a fault (≥ 24.72 V steady, 28.3 V eFuse OV limit).
7. Hot-plug keeps U101 IN < 60 V and U201 VIN < 36 V.
8. Python and SPICE agree within ±3 %, or the difference is explained.

Passing ERC or unit tests is not evidence for any of these.

## Validation to run before each push

```sh
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/forensic_2026-09-14/V1A_qualified.net.xml
python3 -B scripts/analyze_output_protection.py
```

All must pass. The capture checker must still report the output boundary as open and "R2 RELEASE BLOCKED".

## Hand-back

Commit in small commits on `feat/r2-sheet03-output-protection`, push, and report:
- the commit list
- the pass/fail table for the 8 criteria
- every source you could not download
- anything that contradicts `PROTECTION_ANALYSIS.md`
