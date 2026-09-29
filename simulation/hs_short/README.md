# Open high-side-short model — Task 2

**All SPICE results: NOT RUN.** ngspice is unavailable on this Mac and the
continuation forbids installation. These are authored behavioral netlists, not
vendor models or a syntax-verified simulator deliverable. No software was installed.
Sheet 03 remains OPEN; R2/R3 BLOCKED; NOT FOR FABRICATION.

## Reproduction and required external environment

Needed: an existing ngspice installation supporting behavioral sources, ternary
expressions, transient `.meas`, and `UIC`; Python 3 with the standard library;
this entire worktree snapshot including both dated Python result JSON files.
No PSpice models, proprietary libraries or Python packages are needed for this
open-model cross-check. ngspice's actual version/platform must be recorded before
making a result claim. Parser acceptance and convergence remain UNKNOWN until run.

From the repository root, regenerate the Python evidence, then the cases:

```sh
python3 -B scripts/analyze_output_protection.py --profile baseline --write
python3 -B scripts/analyze_output_protection.py --profile reviewed --write
python3 -B simulation/hs_short/prepare.py
```

The matrix is A, B2, I and H at each of the historical 32 corners, for both
`baseline` and `reviewed`: 256 independent `.cir` files. Manifest peaks are
CALCULATED Python values, and every SPICE peak/error is null with status NOT RUN.
Numerical counts are run identifiers, not additional electrical requirements.
`prepare.py` never invokes ngspice unless explicitly given `--run`.

On an authorized machine that already has ngspice, use a **new** output directory:

```sh
python3 -B simulation/hs_short/prepare.py --run --output /tmp/v1a-ngspice-run01
```

This checks netlist/core hashes, records simulator version, commands, exit codes,
logs, state checks and comparisons. A missing executable does not create fabricated
results. Failed/missing measurements remain ERROR/NOT RUN. Preserve the logs and
`comparison_results.json` under a new dated evidence directory for review; do not
replace these NOT RUN records without recording the actual execution provenance.
The runner's PASS means numerical agreement only, never electrical acceptance.

For event debugging, run an individual case from this directory in ngspice's
interactive mode, `run`, then `write /tmp/case.raw` and preserve the waveform.
Inspect raw/load, input, inductor/crowbar currents, action/connection states and
both clocks. Repeat on a separate generated matrix with an ASSUMED 1 ns or
0.5 ns maximum step (`--directory /tmp/v1a-hs-fine --maxstep 1e-9`), and rerun
Python at matching smaller `dt`. Do not infer a physical margin from solver
agreement; both models share large electrical omissions.

## Equations, topology and numerical differences

All electrical parameters inherit their evidence labels/source strings from
`get_inputs(profile)` and are stored once per profile in `manifest.json`; wrappers identify that ledger. Parameter arithmetic
is CALCULATED. Every behavioral switch, timer, ideal capacitor and instantaneous
eFuse response is ASSUMED. The model follows the Python chain:

`source → clipped eFuse current → Cin → failed HS + L/DCR → raw → path → load`.
Raw has its MLCC bank and optional series-ESR bulk; H also has the latched crowbar.

With `i` represented by `V(il_state)`, the authored state equation is
`di/dt = (Vcin − Vraw − i × (Rhs + DCR)) / L(i)`. A conventional flux-table
inductor would not necessarily reproduce Python's abrupt differential-inductance
rule. The state capacitor and controlled current source reproduce that rule
explicitly; they do not establish Coilcraft saturation behavior. The same method
implements crowbar inductance. Conventional capacitors solve all physical node
voltages, and behavioral branch currents apply the same Ohm's-law/load equations.

Initial conditions reproduce Python exactly: Cin at the source voltage; raw,
bulk and load at the calculated nominal raw voltage; inductor current equals the
selected load current; crowbar current and timer states zero. Use `UIC`, not a
DC operating-point solve. These conditions intentionally have initial zero path
current and eFuse source current; they are comparison conditions rather than a
settled physical pre-fault circuit. “Lossless” removes only HS resistance and DCR.
It retains eFuse resistance, path/shunt resistance and bulk ESR.

First raw threshold crossing starts a retained clock. Falling raw voltage cannot
cancel the pending action. Disconnect options open permanently; H holds its
crowbar on. A separate reverse timer resets when forward/zero path current
returns. Reaching its delay sets a persistent cutoff latch; the current becoming
zero after opening cannot reconnect the path. This latching is programmed
ASSUMED behavior, not proof of a physical latch or no reset while input is present.

Numerical auxiliary settings are ASSUMED: clocks use 1 nF and 1 mA (CALCULATED
1 V/µs), retained-clock seed 1 µV (CALCULATED 1 ps), reverse reset RC 1 ps,
Gear order at most 2, maximum step 2 ns, window 120 µs. Those auxiliary capacitors
are not proposed hardware. The discontinuities and fast reset are untested
convergence risks. A decoupled auxiliary bulk-state capacitor avoids a zero
capacitance element when no bulk branch exists. It draws exactly zero raw current.

SPICE solves the continuous equations implicitly/adaptively. Python updates
inductor current, input voltage, bulk, crowbar, raw and load in sequence using
Euler steps, then checks threshold/action. Thus Python action timing has step
quantization and update-order error. The generated core uses continuous threshold
events, with negligible intended auxiliary latch/reset lag that still requires
numerical verification. Expected possible differences: integration, threshold
sampling, reverse reset, floating-point roundoff and event convergence.
None is an observed difference: **comparison NOT RUN**.

## Acceptance and coverage

Criterion 8 requires every corner to satisfy
`abs(Vpeak_SPICE − Vpeak_Python) / abs(Vpeak_Python) ≤ 0.03`, or a documented
waveform-based explanation. The comparison uses the CALCULATED unrounded Python peak. The human-readable
summary also provides a peak rounded to 1 mV; the limit margin is calculated
from the unrounded value. Review discrepancies with waveforms and a finer timestep.
Initial/final action and connected states are checked as additional diagnostics;
endpoint checks alone cannot prove absence of intermediate reconnection.

The amendment's KNOWN user-required Pi-rail limit is 5.5 V with explicit margin;
the historical 6.0 V duration is retained only for reproducibility. Criterion 8's
3% comparison allowance is roughly 165 mV near that rail, so it cannot certify
the few-millivolt margin of the original option I even if agreement later passes.

Both models omit converter control/low-side conduction, eFuse response dynamics,
MOSFET switching/SOA/Miller effects, capacitor voltage/temperature/aging/ESL,
layout/cable ringing, detector overdrive/supply/reset behavior, actual Pi rail
network and indefinite fault hold. `.cir` file creation and offline unit tests
prove none of the eight electrical acceptance criteria. Source-reviewed input
changes and unavailable values are recorded in the dated `INPUTS.md`.


## Retained artifacts

The complete 256 `.cir` parameter wrappers, shared authored `model.inc`, generator,
and NOT RUN manifest are intentionally versioned run inputs. They are required
review evidence, not simulator build/cache output. Labels and sources are stored
once per profile in the manifest to avoid repeating the input ledger in every
wrapper. Dated Python result JSON files are intentionally retained calculation
evidence. Runtime waveforms and solver scratch files are ignored locally; export
selected executed evidence deliberately under `docs/` after review. No upstream
SPICE or manufacturer circuit has been copied. No new third-party license applies
to these project-authored behavioral equations; cited datasheet rights remain in
the Task 1 source register.
