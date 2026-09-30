# Gate 3b — source bound and D/E re-score

**STATUS: analysis in progress. Electrical qualification BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Single owner: this branch starts at `65a8698`, `origin/feat/sheet03-gate3-options`. All new authored files stay in this directory. No `.kicad_sch`, `.kicad_pcb` or `.kicad_sym` file is opened or saved. Source research is read-only; architecture ownership, calculations and commits remain with the root owner.

## Requirements and recovered state

REQUIREMENT: GPIO Pi power (D-30); normal input 9–24 V; Pi peak strictly below 5.5 V including let-through; Pi at least 4.75 V at 5 A; normal maximum plus the approved margin below minimum trip; maximum trip plus let-through below 5.5 V. The upstream 48→24 V converter remains OPEN. No threshold, setpoint, interface or architecture is changed by this report.

Read first: [Gate3 options](../GATE3_ARCHITECTURE_OPTIONS.md), [Gate2c closure](../GATE2C_REVIEW_CLOSURE.md), [historical calculations](../CALCULATIONS.json) and [decision log](../../../../context/06_DECISION_LOG.md). [Baseline and scope](BASELINE_AND_SCOPE.json) preserves relevant inputs without altering their evidence state.

Numeric discipline: ASSUMED identifies proposed allocations or graph-reading/application transfers. CALCULATED identifies arithmetic with named inputs, tolerances and source conditions. OPEN identifies a missing applicable bound. Manufacturer specifications are cited with their conditions; they do not make an application bound confirmed. Typical/reference curves are not a guaranteed minimum differential inductance. Negative margins and domain violations remain BLOCKING.

CALCULATED in the inherited ASSUMED resistor/leakage box: the requested 27.63 V is nominal input OVP; the upper corner is 28.289211 V. Both are assessed in addition to normal 24 V; the true transient/input ceiling is OPEN. CALCULATED from Gate3's ASSUMED 20 µF local C, 150 µC continued source charge, 6.1 A initial current, 8.16 µH upper/5.44 µH lower L: the energy-based current screen is 59.135 A at 24 V but exceeds 60 A at the OVP corners. A curve/floor ending at 60 A cannot qualify a result that exits its domain.

## Progress and checkpoint policy

- Setup and inherited-input recovery: complete; source/inductor research ongoing.
- Task 1a manufacturer curves and normal/fault arithmetic: pending.
- Task 1b limiter/local-input discharge and source recommendation: pending.
- Task 2 common fixes/timing/supply: pending.
- Task 3 D/E re-score and resistance/current/independent-threshold contract: pending.
- Final owner explanation, questions, validation and draft PR: pending.

Each finished sub-step is committed and pushed before continuing. Interim verdict is BLOCKED; no electrical qualification is implied by a checkpoint.
