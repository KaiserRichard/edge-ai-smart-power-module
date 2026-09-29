# Task 3 — vendor-model run plan

2026-09-29. **Every vendor simulation: NOT RUN.** PSpice for TI is unavailable
on this Mac, installation is prohibited, and vendor-model downloads are outside
the continuation's permitted network scope. This is a run plan, not a simulated
result or a selected architecture. **Sheet 03 OPEN; R2/R3 BLOCKED; NOT FOR FABRICATION.**

Electrical values below are ASSUMED test inputs from the brief unless labelled
KNOWN or CALCULATED. Counts, case identifiers and procedure steps are metadata.

## Inputs and artifacts needed from the user / conductor

Provide access to an already authorized PSpice for TI environment, or execute this
plan there and return the artifacts. Provide original TI transient-model packages
for the exact LM61460 variant, TPS26630 and LM74800-Q1 (not silently another family
member), plus an exact Nexperia Q302/Q301 MOSFET model or a separately reviewed
substitute. Actual model names, versions, release dates, simulator build and
supported corner features are **UNKNOWN** until supplied. Do not invent release
identifiers from datasheet revisions. Keep downloaded originals under
`third_party/`, record URLs, exact bytes/hashes, licenses, relevant model/testbench
files, use and modifications. Project testbenches may reference those immutable
originals without editing upstream models. Keep restricted models local if their
license prohibits redistribution; retain hashes and reconstruction instructions.

Also needed: the blocked Coilcraft/TDK/Nexperia sources in the source register;
exact bulk candidate SKU, minimum/maximum effective capacitance, ESR versus
frequency/temperature, ripple rating and geometry; complete detector/latch/gate
circuit with verified limits; actual adapter/source capacitance, current and OVP
behavior; cable and Pi input-network bounds. Task 4 candidate links are unverified
leads, not supplied models or specifications. Until these exist, mark each assumed
parameter and each unsupported model behavior explicitly. A generic instant trip
cannot stand in for a real detector timing guarantee.

## Common procedure and metadata

1. Archive each model's supplied example unmodified. Run it first to establish the
   simulator can use that exact package; a functional example is not V1A validation.
2. Build an analysis-only project from the captured buck/input netlist values and
   proposed path blocks. Do not edit `hardware/`. Confirm pin mapping, control mode,
   frequency, feedback/feedforward branch, bootstrap, BIAS and PGOOD connection.
   KNOWN captured BIAS is grounded; U201.PGOOD is unconnected. The proposed signal
   must use U201.PGOOD, not the captured upstream `BUCK_INPUT_PGOOD`.
3. For every run record: unique ID; UTC date; operator; OS/simulator name/build;
   model names/version/date/SHA-256; testbench and parameter hashes; temperature;
   every corner parameter and its evidence label/source; initialization; event
   times; solver settings; warnings/convergence changes; exit status. Retain the
   exact project, exported netlist, raw waveforms and simulator logs.
4. Resolve supported temperature and tolerance coverage from the model manuals.
   Typical-only macromodels must be called typical-only. A `.TEMP` sweep does not
   prove modeled temperature dependence. Unsupported corners remain NOT RUN /
   UNKNOWN, and acceptance requiring all corners cannot pass.
5. Establish a settled initial operating point before faults/steps. Include
   switching phase sensitivity for the hard short and load step, not only the
   historical lumped initial condition. Extend each trace until settling or a
   bounded persistent-fault state is established. Duration remains UNKNOWN until
   the slow timer/thermal/reset behaviors supported by each model are understood.
6. Refine maximum timestep until peaks, trip/isolation endpoints and event order
   are stable relative to the margin being assessed. ASSUMED 2 ns is an initial
   fast-fault comparison setting, not a universal convergence guarantee. Save
   full-resolution data around events; decimated plots alone cannot prove peaks.

## V1 — LM61460 release and rising-load steps

Base matrix: input 9 / 12 / 24 V; load 5→0 A and 0.5→4.5 A; slew 1 / 10 A/µs;
MLCC only and MLCC plus 470 µF **effective** bulk. This defines 24 base cases.
Use the candidate bank's actual ESR bounds when provided; 20 mΩ remains only the
open-model assumption. Record all source/passive/load/temperature corners, raw
static high/low, and switching phase. Include 24.72 V as a separately labelled
ASSUMED source-maximum sensitivity, not a substitute for the requested 24 V cases.

Save V(raw), V(load), I(L201), switch node, input current, PGOOD, and relevant
control-loop states if exposed. Report raw/load peak and minimum voltage, ringing
frequency/amplitude/cycle count, final DC value and settling time. Define the
settling band explicitly in each result; its approved electrical value is OPEN.
Compute nuisance margin as `Vtrip_static_low − max(raw release peak)` and its
excess above the brief's 50 mV allocation. Use **static worst-low**, with no credit
for overdrive delay. Any added capacitance/threshold from the margin study needs
its own rerun; the requested 470 µF run does not qualify 1000 µF.

## V2 — bulk stability

Reuse V1 waveforms but assess sustained or growing oscillation and count decaying
cycles separately for each load/input/passive corner. Record mode changes, pulse
skipping and model-validity limitations. If the vendor model supports loop-gain
injection, document the injection point/bias arrangement and save gain/phase plots,
crossovers and margins. If unsupported, mark loop gain NOT RUN; do not create an
artificial loop around an opaque behavioral output. Decaying typical waveforms
are supporting evidence only and do not establish all-corner stability.

## V3 — persistent high-side short, options A and I

Start from steady regulation. Add an analysis-only 10 mΩ switch between U201.VIN
and SW to represent a forced high-side short, including its source and event time
in the run metadata. The switch is ASSUMED fault injection, not a real failed-die
model. Establish whether the vendor low-side model continues switching into that
fault and whether it models shoot-through/current limits; an ideal macromodel may
not support internal damage behavior.

First evaluate A and I at the 32 historical parameter corners in `INPUTS.md`
(64 base cases) at source 24.72 V, then add verified component, source, temperature,
static regulation, fault-resistance and switching-phase corners as evidence allows.
The high-side fault resistance differs from the historical 0 / 41 mΩ lumped
comparison; identify that difference. Evaluate I at both its optimistic historical
0.4 µs and proposed 2 µs delay when only behavioral controls are available, labelled
ASSUMED. A real detector/gate circuit is needed for acceptance. Margin-study variants
remain experiments requiring separate approval and verified circuit implementation.

Record peak load voltage, margin to the **KNOWN 5.5 V user ceiling**, time above
5.5 V and historical 6.0 V, raw peak and eventual raw hold, Q302 VDS/VGS/current,
HGATE−OUT minimum, input/eFuse current, OVP/FLT/SHDN/MODE state, detector supply,
latch state, and isolation time. Define isolation by a reviewed residual-current
criterion (value OPEN), not just HGATE falling. Include FB through the actual
C207/R205 feedforward path. Monitor other exposed pins against their own ratings.

Test persistence while input stays connected: raw returns to regulation, buck
hiccup, PGOOD toggles, eFuse fast-trip off/restart, UVLO/SHDN changes and detector
brownout. Latch reset at raw-fed supply UVLO does not by itself satisfy no re-enable
while input is present. Run long enough to expose supported overload/thermal
sequences; KNOWN TPS26630 overload timer maximum is 202 ms, not nominal 162 ms.
If runtime/model coverage prevents that check, report NOT RUN, not a passed latch.

## V4 — startup and delayed-load connection

Input 9 V; load 5 A; MLCC plus 470 µF effective bulk. Compare immediate path enable
with U201.PGOOD-controlled enable AND detector/reference valid AND no fault latch.
Use both assumed load-capacitance corners 2 / 220 µF as sensitivities and later the
actual Pi/harness network. Include both bulk maximum (inrush) and minimum (fault)
capacitance and candidate ESR bounds; a single nominal value is insufficient.

Save input/eFuse current, all rail ramps, detector/reference validity, PGOOD,
HGATE/VGS, latch/reset, load inrush and any current-limit/thermal fault. Re-test
prebiased-load and interrupted-ramp states if the model supports them. Compare
instantaneous peak and any sustained startup plateau with both:

- CALCULATED historical conservative criterion: 0.90 × 4.17 A = 3.753 A.
- CALCULATED source-reviewed conditional value: 0.90 × (4.185/1.001 A) = 3.762737 A.

Report both bases; satisfying the more lenient calculation alone does not revise
the approved requirement. PGOOD separates bulk charging from load application but
can create a new load-capacitor surge. No safe startup result is inferred from it.

## V5 — input hot-plug and TVS coordination

Use the brief's ASSUMED 2 m cable model, 1.5 µH and 50 mΩ, and compare SMBJ26CA
with SMBJ30CA in separate testbenches. Start with source 24.72 V (ASSUMED source
maximum) and repeat actual source/adapter OVP/source-capacitance corners when
supplied. Include input-side capacitor tolerance, cable variation, initial charge,
TVS temperature/derating, connector bounce and upstream supply impedance. Missing
source energy is UNKNOWN, not an ideal unlimited supply qualification.

Record peaks at U101.IN and U201.VIN, TVS current/energy, eFuse OVP/FLT and actual
pass-current interruption, Cin current/charge and restart. Criteria are U101.IN
<60 V and U201.VIN <36 V (ASSUMED original brief acceptance values). KNOWN Vishay
clamp rows apply to specified pulse currents/waveform/temperature; its VBR
coefficient cannot be promoted to a guaranteed VC temperature coefficient.
KNOWN TPS2663 OVP delay is to FLT, not proven isolation. Do not use the historical
72 µC let-through / approximately 33 V estimate as the reference bound.

## Returned result record and acceptance

For every case provide model identity/version/date and measurements above, linked
to raw waveform and log. Use **SIMULATED** only for executed, completed runs;
missing/unsupported/failed cases remain NOT RUN/ERROR with the reason. Summarize
worst corners with reproducible extraction rules; explain differences from the
open model using waveforms rather than fitting unknown parameters to force agreement.
No vendor result currently exists for any of V1–V5. Vendor simulation is supporting
evidence; electrical qualification still requires reviewed hardware and staged
bench work with dummy loads before connecting an SBC.
