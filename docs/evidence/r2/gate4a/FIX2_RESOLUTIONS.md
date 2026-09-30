# Gate4a-FIX round 2 — circuit decisions

**Analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

This document supersedes conflicting round-1 dispositions in FIX_RESOLUTIONS.md, at baseline 47c7c07. Earlier calculations and failed screens remain evidence. No KiCad changes, hardware tests, sub-agents or push. GATE4A_FIX2.md controls the present scope: assembly measurements do not block capture when bounded, isolated test hooks can carry them safely. Missing circuits still require an explicit disposition.

## F2-01 — completed J502 handoff (R4A-11/16)

**DECISION:** use solution A from commit `41cb9e889418d50d2f5f24467e66ac7f15a90476`: Phoenix 1776508 board header + 1777989 plug, TE 3-87456-6 full 2×20 housing and ten 87309-9 sockets, Belden 8521 002100/010100 AWG16 75 mm trunks, and Belden 8502 002100/010100 AWG20 branches (2×15 mm positive; 8×35 mm return). J502.1=LOAD_5V1; .2=GND. Pi physical +2/4 and GND6/9/14/20/25/30/34/39 remain fixed. Supersede Harwin and the interim 8503 selection. Molex solution B is a documented fallback, not fitted in parallel.

**CALCULATION:** retain architecture D and the 13.6 mΩ BSC034 pair screen: `Rloop=34.255546+13.6−6=41.855546 mΩ`. At source screen 5.026143255 V, `Vfar=5.026143255−5×0.041855546−0.020=4.796865525 V`. Reserve above 4.75 V is 46.866 mV, or 31.866 mV after the proposed 15 mV measurement allowance. A 100 mV trough gives 4.716865525 V and fails. These remain conditional allocations, not a guaranteed hot assembly. Each positive branch must be rated above its measured current; matching ratio ≤1.05 gives `5×1.05/2.05=2.560976 A` in the lower-resistance leg. The preliminary fully loaded TE derating screen near 2.01 A does not qualify 5 A operation.

**T11 acceptance:** complete hot J502 pole ≤3.12 mΩ, each Pi mated-contact/female-crimp block ≤20 mΩ, all fan-out splice joints together ≤0.5 mΩ per polarity, full loop/voltage with actual uncertainty, individual contact current below applicable hot male/female rating, and verified indexed carrier/crimp/tooling/strain relief. The full housing is power-only: no host telemetry connection until its separately reviewed mapping is incorporated. An open positive contact leaves 5 A on one pin and is not qualified. Test first with a rated dummy coupon; no Pi is required to capture the board.

**Disposition:** connector selection and wire mismatch are closed for the test-board candidate. Supplier mixed-mate applicability, hot measurements, splice process and actual Pi header remain T11/T16 assembly/integration gates. They no longer appear as a missing J502 selection.

**EVIDENCE:** [pinned imported report](../J502_SELECTION.md), [calculation/provenance](../j502_selection/INPUT_PROVENANCE.json), [third-party sources](../../../../third_party/j502_selection/SOURCES.json), [import hashes](FIX2_INPUTS.json). The report and its supporting files were imported byte-for-byte; its architecture E recommendation and alternative pair were not adopted.
