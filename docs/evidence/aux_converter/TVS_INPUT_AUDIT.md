# V1A TVS re-selection — input audit

2026-09-30. Worktree `wt-tvs`, branch `feat/v1a-input-tvs`; base `50c94e05a4896b6d95ec13019e4c722a6ae2c1bf`. New analysis files only under `docs/evidence/aux_converter/`. No KiCad file was opened, read or saved. Existing reports, source registers and circuits remain unchanged. Documentary input hashes are pinned in [TVS_INPUT_PROVENANCE.json](TVS_INPUT_PROVENANCE.json).

## Requirements and reference planes

REQUIREMENT from this task: choose a real bidirectional D101 replacement and F101 part; TVS standoff must clear the specified module OVP-output figures with margin; clamp at its rated pulse current must be below TPS26630's ordinary67 V absolute maximum with margin; explicitly state assumed surge energy and waveform. F101 must have applicable DC interruption voltage and prospective-current capacity, I²t evidence and hot5 A hold capability. No pulse, fuse or component headline is a whole-board withstand proof.

REQUIREMENT preserved from D-30: normal V1A input9–24 V, total Pi5 A through GPIO, strict Pi fault peak below5.5 V. Existing input OVP minimum26.973873 V is a CALCULATED initial-tolerance screen; full resistor drift/application minimum OPEN. A larger TVS does not change the normal-input requirement, the trip setting or the downstream fault obligations.

OBSERVATION from the existing documentary topology: J501→F101→VIN_FUSED→Q101→U101 input; D101/C101, U101 IN_SYS/dividers and the D303 raw auxiliary feed attach before U101's internal cutoff. C102 is at U101 input. Q101's body diode conducts forward toward U101, so it is not a positive-overvoltage isolation device. The raw TVS and auxiliary load remain energized when U101 turns off.

The required read-only baseline document includes instructions describing its own earlier native-CAD inspection. Those historical actions are evidence about that earlier study, not permission to inspect CAD in this task; current topology/values are taken from the documents only.

## Key corrections carried into the new study

- ASSUMED comparison inputs, specified by the user: RSD-100C-24/RSD-200C-24 output figure32.4 V; TEP20031.2 V; TEP15033.6 V. The manufacturer documents publish these as OVP threshold maxima. Their complete post-threshold overshoot is OPEN. Show both the requested comparison treating the figures as complete peaks and the additional overshoot allowance if they are only threshold bounds; do not double-count an already included overshoot or invent a supplier guarantee.
- DATASHEET source evidence: Littelfuse/Vishay30/33/36CA standoff30/33/36 V; rated pulse clamps48.4/53.3/58.1 V. With an ASSUMED1 V standoff margin, only36CA clears all three specified figures. A36 V standoff is not a36 V clamp or a demonstrated board rating.
- The new58.1 V room-temperature clamp fits U101's67 V absolute input ceiling numerically, but is close to its60 V operating ceiling and the auxiliary LDO's62 V absolute input ceiling. Its directly tied EN has only40 V recommended maximum; C307 is a50 V specification placeholder. Those are separate constraints and must be addressed.
- C101/C102 are100 V placeholders, Q101 is documented CSD19537Q3 with100 V VDS/±20 V VGS. Actual capacitor MPNs, hot dynamics, source/fuse energy and built layout remain OPEN.
- The latest inherited eFuse current-limit screen is4.180819–4.819820 A, superseding the old4.160–4.796 A worksheet. The task's5 A fuse-hold condition is evaluated explicitly even though the normal5 A Pi load draws about3.333 A at9 V/85% assumed efficiency.
- The23.0 V trim proposal protects the separately frozen24 V normal ceiling. It is not compelled by26.97 V nuisance OVP. Complete normal tolerance, ripple and load-step peak guarantees remain OPEN; typical200 mV p-p cannot be treated as guaranteed+100 mV ripple.
- Fuse melting I²t is not maximum DC total-clearing I²t. A pre-TVS fuse can remain intact during a low-current maintained avalanche. A short-pulse TVS rating does not establish survival for a67.2 V/1 s source fault.

STATUS: input reconciliation complete; component selection/calculations follow. Proven V1A continuous withstand and recommended standalone module remain OPEN/NONE until the complete applicable limits and qualification close.
