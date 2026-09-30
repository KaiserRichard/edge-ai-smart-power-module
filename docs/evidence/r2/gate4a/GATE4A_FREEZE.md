# Gate4a freeze review — 2026-09-30

**VERDICT: BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** TASKS1–5 analysis deliverables are complete. The proposed change register is reviewable, but essential circuit connections/trigger/rail/receiving-bank contracts are not ready to freeze. This is an R2 fault-test-board review; it does not advance the repository to R3/R4/R5.

## OWNER EXPLANATION — one page

The owner selected **D**: a module-side opposed series pair and protected crowbar, paired with a bounded main input source. Normal operation remains **9–26 V**, locally regulated about5.10 V, with at least4.75 V at the far end at5 A. The selected BSC034 pair and improved short harness give a conditional42.673 mΩ loop: about4.793 V with the inherited minimum regulator screen and an assumed20 mV trough. Hot resistance and true source accuracy are still OPEN.

1. A failed buck high-side can connect the protected input through L201 to the raw output. Current rise depends on differential inductance: `dI/dt=VL/Ldiff`. The proposed10 µH part needs a qualified5…12 µH envelope through100 A; a typical curve is not that guarantee.
2. The main eFuse must stop fresh source work within10 µs of the **fault onset**, with positive replenishment charge≤100 µC. A separate fault trigger is needed: charging the bulk bank before raw OV trips can already consume about19…36 µs in illustrative screens. Source-off timing is therefore OPEN, not the sum of a fast comparator headline and an eFuse headline.
3. Even with the source isolated, local input capacitance and L201 still contain energy. `Enew≤½Cin Vin²+Vin Qsource+½Lmax I0²` gives15.217 mJ under the proposed highest source screen. The output pair opens to stop delivery to the protected node, and its crowbar discharges the protected bank/load-side energy. Raw bulk can bypass L201 into that node before opening, so protected current needs its own bound.
4. The eight bulk capacitors are **upstream** of the open pair. Their energy and L201's tail do not reach the protected crowbar afterward. They charge VOUT_5V1 or flow through a separate raw dump. `Vraw≤sqrt(Vraw0²+2Enew/Craw,min)` gives6.550 V under assumptions, or a6.882 V ESR/ringing sensitivity. Those voltage screens fit35 V bulk; actual peak and powered-off sense stress remain OPEN. A separately rated raw dump is proposed for up to99.865 mJ conditional raw/source energy.
5. Control power comes from a separate surge-limited12 V buck-boost upstream of the main eFuse, with supervised usable rails, hold energy, passive off gates and a fault latch independent of PGOOD. Its tentative inrush/timer/supervisor values still need correction and qualification.
6. The harness and dummy input capacitance can ring after cutoff. Only simultaneous measurements of **both output nodes, L201 current and the far-end real-harness voltage**, with calibrated uncertainty and component-stress review, establish this board's fault result. Require `measured_peak+uncertainty<5.5 V`, and normal `measured_min−uncertainty≥4.75 V`. Test27 V as an OVP-window fault point. No Pi is used until every applicable gate passes.

## Completed task evidence

|Original task|Delivered evidence|Engineering result|
|---|---|---|
|1 FREEZE LIST|[Full register](FREEZE_TABLE.md), [CSV](FREEZE_BOM.csv), [manifest](FREEZE_MANIFEST.json), [timing/logic](TIMING_AND_LOGIC.md)|35 proposed change rows; retained identities and real candidates recorded; missing autonomous trigger explicitly OPEN|
|2 AUX BRANCH FIX|[Supply analysis](AUX_BRANCH_FIX.md)|Independent stopper plus buck-boost retained; main-eFuse-off independence established by topology, actual operation untested|
|3 TEST HOOKS|[Hooks/fixture](TEST_HOOKS.md)|Actual L201-path injection, paired Kelvin/force points and removable dummy harness; fixture/live-switch modes require qualification|
|4 BENCH FAULT TEST PLAN|[TEST_PLAN.md](TEST_PLAN.md)|9/24/26/27 V ×0/2.5/5 A ×cold/hot, dummy C/ESR variants, normal steps and uncertainty-aware far-end acceptance|
|5 CALCULATIONS|[Calculation report](CALCULATIONS.md), [JSON](CALCULATIONS.json), [raw-node energy](RAW_NODE_ENERGY.md), [script](calculate_gate4a.py)|Selected pair re-budgeted; raw/protected energies separated; source/timing/actual peaks remain OPEN|

[Recovery/task accounting](TASK_PROGRESS.md) records STEP0 and each original task. [Source provenance](SOURCES.md)/[machine register](SOURCES.json) record revisions/hashes, function, license, proposed adaptation and attribution. [Validation](VALIDATION.json): six numerical/artifact checks pass; ideal-model curve visually reviewed. No native CAD access/change, new ERC/DRC or bench test occurred.

## Why the capture freeze is blocked

- Autonomous source-fault trigger and full fault-onset→current-off min/max are absent. OV-only triggering does not establish the10 µs/100 µC source contract. Independent current/voltage/energy/C/L bounds remain qualification targets.
- Auxiliary architecture is retained, but10 nF stopper TMR with440 µF nominal hold bank can trip during inrush. Usable-rail supervisor tolerance corners can reject healthy supplies; actual loaded gate/bootstrap and comparator delay condition remain OPEN.
- The proposed powered-off clamp/default-SHDN/latch circuits need pin-level positive/negative/partial-supply/race proof. The1 MΩ sense pull-down increases nominal OV trip28.25 mV, so old trip/timing margins cannot be retained unchanged.
- Proposed protected bank4×470 µF is1.88 mF nominal with published3.5 mΩ initial parallel ESR at20°C/100kHz. It does not meet the inherited≤1.5 mF/≤0.5 mΩ contract. The old conditional module formula gives5.713245 V with that bank; actual arriving current and the full harness trajectory are OPEN. The historical5.542140 V far-end counterexample is not excluded.
- A raw dump has real candidate parts and a concrete topology, but negative/stray-current returns, hot SOA/pulse/repetition and hold duration to safe decay are unqualified. Ballast pre-pulse≤85°C and total terminal<95°C remain mandatory technical limits.
- The selected BSC034 hot pair resistance, complete timing, actual hot contacts/regulation/C/ESR, loop/thermal/startup behavior, source58.1 V main-path let-through and new-MPN pin/land/rating checks remain OPEN. The100 mV negative-excursion path sensitivity fails4.75 V by37.221 mV. No actual failure or PASS is claimed from these calculations alone.

## DECISIONS FOR THE OWNER

These are recommended engineering directions, not requests for manufacturing or merge approval. Existing owner decisions D, source-development route,9–26 V, SMCJ36CA,3403.0285.23, PR15 retained MPNs and BSC034 pair remain in force.

|Decision|Recommended option|Alternative / consequence|
|---|---|---|
|Raw energy destination|Keep raw bank; add/qualify the separate Q330 raw dump and its negative/stray return|Credit capacitive absorption only after its full C/source/spike/pin/discharge limits are proved; moving all bulk downstream increases protected delivery/discharge energy and needs a new model|
|Source deadline|Implement an independently bounded high-side-fault discriminator with physical source-off/charge proof|Use fixture-timed cutoff only for a clearly conditional development experiment; it cannot close autonomous containment or claim a source-bound freeze|
|Aux power|Retain upstream adjustable surge stopper+12 V buck-boost+held output; solve inrush/timer/SOA as one block|Main-eFuse downstream-only power requires qualified hold energy for every source-off/re-arm state and loses sustained independence|
|Usable rails/timing|Set direct-supervisor thresholds from verified minimum loaded rails and response maxima; requalify actual comparator/bootstrap/gates|Typical supervisor delay or gross PG cannot substitute for complete min/max timing; no automatic permission below valid rail conditions|
|Powered-off sense and latch/default SHDN|Complete the proposed ground-return shunt/isolation, explicit fault-priority/disarmed truth table and passive SHDN topology; re-stack trip/leakage/delay|Retaining the old reference-sink clamp or coupling OV to PGOOD leaves partial-power/fault race behavior unresolved|
|Protected receiving bank/harness|Select a credible C/ESR implementation and recompute actual raw-bank arriving current and full harness transient; qualify the bank jointly with timing|Four PCH capacitors cannot inherit the0.5 mΩ margin; adding nominal C alone does not fix ESR/harness/current or startup|
|Path loss|Keep BSC034; qualify10 V loaded VGS/hot resistance and the improved contacts/wire/fanout set|Do not silently restore the previous6 mΩ pair or raise setpoint;100 mV excursion reserve requires further reduction/proven transient bounds|
|M05|Keep selected ballast only with measured pre-pulse terminals≤85°C and hot waveform/repetition acceptance|If that cannot be met, select/review a pulse-rated construction and recalculate geometry/current/thermal behavior; a cold curve is not hot qualification|
|Bench/SBC gate|Use the real harness/dummy endpoint matrix and calibrated strict5.5 V criterion; preserve all failures|A board-local voltage PASS, synthetic PG or fixture-rescued cutoff is insufficient; actual Pi range and repository gates must close before integration|

## Freeze table

The current complete register is [FREEZE_TABLE.md](FREEZE_TABLE.md), synchronized with [FREEZE_BOM.csv](FREEZE_BOM.csv) and [FREEZE_MANIFEST.json](FREEZE_MANIFEST.json). Current fixes and remaining blockers are in [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md).
