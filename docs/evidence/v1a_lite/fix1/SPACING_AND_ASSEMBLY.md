# FIX1 spacing and assembly disposition

2026-10-05 — **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Finding 8: electrical spacing remains OPEN

**OBSERVATION:** native DRC enforces manufacturing spacing, not a qualified insulation/environment design. The 64 V source fault and the TVS's 103 V pulse-clamp envelope are distinct cases. VIN_RAW/VIN_FUSED/S_COMMON and the cutoff gate networks must be assessed against GND and each other at the actual instantaneous differential voltage; assigning every pair a 64 V differential is incorrect. VIN_PROTECTED survival depends on Q102 cutoff and is not established by the layer change.

**EVIDENCE inherited from independent review R1:** IPC-2221B November 2012 Table 6-1 identifies 51–100 V B2 0.64 mm, B4 0.13 mm and A6 0.50 mm; at 103 V the applicable next row includes B4 0.40 mm and A6 0.80 mm. These are clearance classifications, not a complete creepage/safety certification.

**OPEN REQUIREMENTS:** environment, altitude, pollution/condensation, CTI/material and coating permanence are unspecified. Therefore B4 applicability cannot be asserted merely because solder mask exists. Exposed solder/lead surfaces need a separate assembly assessment. A manufacturing DRC pass cannot be described as a 64/103 V electrical-spacing pass. No speculative B4 waiver or DRC exclusion was added. Pending that basis, an uncoated B2 redesign/audit is required; the present dense design is **not released** on its 0.15/0.20 mm manufacturing clearances.

## Findings 6, 9–11: assembly checklist

**DECISION:** ordinary standard through-via manufacture, with drain thermal vias relocated outside FET solder lands. The relocation audit also moved other accessible vias off lands. Residual center-in-land locations are enumerated in `BOARD_AUDIT.json`; the report is deliberately not a claim of zero hole/mask overlap. Ordinary tenting cannot close these remaining locations. They need another escape-layout revision or a supplier-reviewed fill/cap/stencil process, whose cost is **OPEN**, before fabrication. No premium via process has been silently selected or priced at zero.

**OBSERVATION:** saved connector text identifies J501 input pin 1 / GND pin 2, J502 +5 V pin 1 / GND pin 2, and J503 polarity; compare the pad-net inventory in `BOARD_AUDIT.json` with the mating-face view in `PI_HARNESS.md`. Final mask-subtracted Gerber silk, native silk plot and board/pad locations were inspected. Critical board text is ≥1.0 mm with ≥0.15 mm stroke. The explicit FIX1 revision and fabrication warning remain readable. Native U/Q orientation graphics were retained. Full test-reference coverage and crowded F.Fab annotation remain partial; use the placement CSV and enlarged PDF together. No populated probe-body or screw/washer clearance qualification is claimed.

| Check | Disposition |
| --- | --- |
| Q101/Q102 DPAK tab = drain, gates/sources on correct ends | Saved pad nets unchanged; opposite native orientation retained. Supplier reel zero angle/centroid still OPEN. |
| U201 asymmetric RJR | Fourteen electrical pins; no invented EP15. Native orientation unchanged. Supplier pin-1/body-center check OPEN. |
| Q103/Q301 and other SOT-23 devices | Different native orientations preserved; supplier pin-1/zero-angle match OPEN. |
| D106 DFN | Existing pin-net mapping preserved; supplier centroid and zero-angle match OPEN. |
| SCR301 | Rotated 180°: K (69,33.4), A (66.46,33.4), G (63.92,33.4); tab is live anode. Manual THT operation. |
| C217/C218 | C217 positive (64,26), negative (69,26); C218 positive (81,26), negative (76,26). Manual THT; native positive-lead anchor is not body centroid. |
| J501/J502 | Manual THT; verify latch/key direction and unpowered continuity against manufacturer mating drawing before wiring. |
| D101 | Exact Bourns SMCJ64CA, Mouser 652-SMCJ64CA retained. Excluded from JLC SMT candidate files; external source/manual install. |
| Supplier offset acceptance | `ROTATION_REVIEW.csv` marks all unverified SMT offsets OPEN. No blanket ±90° correction. Zero applied does **not** mean zero accepted. |

The complete 100-reference BOM/CPL remain a review inventory. `BOM_JLC_SMT_REVIEW.csv` and `CPL_JLC_SMT_REVIEW.csv` contain only the 94 nonmanual candidates. `MANUAL_ASSEMBLY.csv` separates D101, SCR301, C217/C218 and J501/J502. No order, upload or supplier acceptance occurred.

**Probe geometry:** TP301/TP302 now have 3.1 mm center spacing beside the SCR, with dedicated branches and no long return-plane slot. Their 2 mm exposed lands do not establish populated probe-body clearance. TP113/TP114 source/gate pair remains 12.50 mm apart and requires a further placement/probe review; always use rated differential probing for the high side. Ripple probing needs a local spring return at the selected raw capacitor, not a long bench ground lead. Populated access, heatsink insulation/envelope and mounting-hardware insulation remain OPEN.
