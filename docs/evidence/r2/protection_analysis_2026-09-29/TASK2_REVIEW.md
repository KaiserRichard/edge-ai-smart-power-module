# Task 2 continuation review

2026-09-29. **Permitted preparation complete; simulator cross-check BLOCKED / NOT RUN.
Sheet 03 OPEN; R2/R3 BLOCKED. NOT FOR FABRICATION.**

The takeover inspected the unfinished Python model, its tests, open-SPICE generator,
behavioral core, README and result JSON files. Their prior existence was not treated
as evidence of completed simulation. The continuation regenerated both Python
profiles, checked historical reproduction, added unrounded peaks for the comparison
and margin, and tied the SPICE load rolloff and stop time to the Python ledger.
The collector now rejects nonfinite peaks and parser/analysis error logs. These
are code-review improvements; ngspice syntax/convergence is still untested.

## Evidence retained

- [Input ledger](INPUTS.md), including source corrections and unreplaced assumptions.
- [Baseline calculation](baseline_model_results.json) and
  [reviewed calculation](protection_model_results.json): intentionally retained
  generated engineering evidence, with no overwrite of the historical evidence.
- [Numerical review](task2_numerical_review.json): all historical fault rows checked
  against regenerated baseline rows, and reviewed worst-corner peak sensitivity
  at ASSUMED integration steps 2 ns, 1 ns and 0.5 ns for A, B2, I and H.
- [Environment observation](task2_environment.json): ngspice executable absent;
  PSpice for TI unavailable per continuation. Existing LTspice was not substituted
  for either requested simulator. No software installation or new network access.
- [SPICE README](../../../../simulation/hs_short/README.md), authored core,
  parameter wrappers and NOT RUN manifest: A/B2/I/H × the historical corner matrix,
  both baseline and reviewed profiles. The ledger and hashes pin the exact inputs.

**KNOWN numerical reproduction:** every historical output field in all 320
fault rows agrees exactly at its archived precision. Additional margin and
unrounded-peak fields do not change those archived values. Counts are evidence
metadata, not added electrical requirements. Numerical step sensitivity is limited
to each requested option's worst sampled corner; it does not validate the circuit.

**UNKNOWN / NOT RUN:** no Python-versus-ngspice comparison result exists. The
manifest contains null simulator peaks and errors; no inferred agreement is
substituted for the requested ±3% comparison. Event-control discontinuities,
reverse-timer reset and implicit-versus-sequential integration are explicit
potential discrepancies to inspect when the simulator is available.

## Takeover findings

The source correction changes some peaks by a few millivolts; it does not repair
the large model omissions. CALCULATED option I retains only 5.772 mV margin to the
KNOWN user limit 5.5 V at its ASSUMED 0.4 µs isolation delay. At ASSUMED 2 µs its
CALCULATED peak is 5.660 V. Those are screening calculations, not device limits.
The original ±3% cross-model allowance is CALCULATED approximately 165 mV near
5.5 V, much greater than the existing margin; even a future numerical-comparison
PASS would not close amended electrical acceptance criterion 2.

Required external action: run the documented matrix on an authorized existing
ngspice installation; retain version, logs, state traces and comparisons. A syntax
or convergence correction must be recorded with fresh hashes and reruns. Missing
Coilcraft/TDK/Nexperia sources must be supplied before replacing their assumed
values. Then repeat the calculation and SPICE matrix with separately identified
new evidence. Do not modify historical records in place.
