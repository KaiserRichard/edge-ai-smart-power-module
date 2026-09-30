# V1A 5 A path budget — source reconciliation

2026-09-30. Analysis only. Worktree `wt-pathbudget`; base `65a86982fc4a48502d3a6da1cd710e796b3d8734`. No native KiCad file was opened or saved. No source branch was merged. Input document identities are pinned in [INPUT_PROVENANCE.json](INPUT_PROVENANCE.json).

## Frozen endpoint and inherited screens

REQUIREMENT (user-frozen): the Pi GPIO supply must be at least 4.75 V at 5 A under worst-case temperature, contact and regulator conditions. D-30 specifies GPIO 5 V pins 2 and 4 and multiple ground pins via J502; USB-C protection is not credited. The inherited strict fault ceiling is below 5.5 V. Analysis temperatures, geometry, resistance allocations and dynamic reserves remain ASSUMED until qualified.

CALCULATED from the historical records: raw buck static screen 5.038271–5.158632 V, nominal 5.098361 V. Static loop allowance `(5.038271−4.75)/5` is 57.654280 mΩ. An optional ASSUMED 100 mV dynamic reserve reduces it to 37.654280 mΩ; this reserve is not a new frozen requirement. Regulator FB-current and full operating bounds remain OPEN.

The two historical harness cases must not be confused:

| Case | CALCULATED hot-loop screen | CALCULATED Pi voltage at 5 A | CALCULATED margin |
|---|---:|---:|---:|
| Original PR #6 path plus 13.6 mΩ series pair | 75.554538 mΩ | 4.660499 V | −89.501 mV |
| Reduced assumed path plus the same series pair | 55.367741 mΩ | 4.761433 V | +11.433 mV |
| Gate 3 E proposed whole-path target | 50.000000 mΩ, ASSUMED acceptance target | 4.788271 V | +38.271 mV |
| Reduced path plus an additional 10 mΩ local stage | 65.367741 mΩ | 4.711433 V | −38.567 mV |

The reduced case already credits eight parallel ground contacts rather than PR #6's four, shorter wires and smaller PCB/J502/joint allocations. Those changes are not implemented or qualified. Adding eight grounds again would double-count that improvement. Pins 2 and 4 are the only ordinary 5 V pins on the 40-pin header; GPIO/signal/3.3 V pins cannot be repurposed as extra power contacts.

## Selected harness evidence from PR #6

The exact history pin is `54d3bc67fd64f4bd947440518d90e76673faf5db`. Its docs were read with `git show`, without checkout/merge. Preliminary J502: Phoenix 1776508 header + 1777989 screw-lock plug; contacts/clamps are integral, separate J502 crimps are not applicable. Pi mate: Harwin M20-1071000 housing + M20-1180042 female contacts, AWG22 fan-outs; AWG18 trunk. Original lengths: 150 mm trunk plus 50 mm branches per polarity. Original grounds: physical pins 6, 9, 14, 20.

The Harwin source lists 3 A/contact and 20 mΩ initial / 30 mΩ conditioned resistance at its test conditions; a hot multiplier of 1.3 was only ASSUMED. The actual fitted Pi male-header part/rating and mating qualification remain OPEN. A catalogue test reading is not automatically a hot maximum for the entire mated termination.

Phoenix durability values (header 1.0 mΩ, plug 1.4 mΩ after 25 cycles) were used only as an additive screen. Their reference planes can overlap; R1/R2 are before/after tests, not separate series resistors. A guaranteed maximum per complete hot contact, including screw clamp, remains OPEN. The original study instead allocated 5 mΩ per polarity at hot; the reduced case allocated 3.12 mΩ. Neither is a vendor maximum.

## D / E interpretation for this study

D puts the last disconnect/absorber at the module. E puts an independent disconnect/absorber at the GPIO entry and includes the retained module path unless removal/relocation is separately approved. A shunt already in the retained path is counted once; any genuinely additional current-limiter shunt, local copper and terminations must be counted separately. Shunt absorbers are not normal-current series resistors, but their supply current and PCB junction/ground geometry still matter. Auxiliary supply and return are separate paths, not free capacity within the 5 A load envelope.

Moving a component within the same current loop does not remove its voltage drop. Remote feedback changes the regulated boundary and fault/stability behavior; it is not resistance reduction. The final report will show conditional feasible allocations separately from the unproven implemented worst case.

STATUS: source reconciliation complete; application worst-case voltage and contact rating remain OPEN. No electrical release or fabrication authorization.
