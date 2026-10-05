# FIX1 spacing and assembly disposition

2026-10-05 — **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Finding 8: electrical spacing remains OPEN

**OBSERVATION:** native DRC enforces manufacturing spacing, not a qualified insulation/environment design. The 64 V source fault and the TVS's 103 V pulse-clamp envelope are distinct cases. VIN_RAW/VIN_FUSED/S_COMMON and the cutoff gate networks must be assessed against GND and each other at the actual instantaneous differential voltage; assigning every pair a 64 V differential is incorrect. VIN_PROTECTED survival depends on Q102 cutoff and is not established by the layer change.

**EVIDENCE inherited from independent review R1:** IPC-2221B November 2012 Table 6-1 identifies 51–100 V B2 0.64 mm, B4 0.13 mm and A6 0.50 mm; at 103 V the applicable next row includes B4 0.40 mm and A6 0.80 mm. These are clearance classifications, not a complete creepage/safety certification.

**OPEN REQUIREMENTS:** environment, altitude, pollution/condensation, CTI/material and coating permanence are unspecified. Therefore B4 applicability cannot be asserted merely because solder mask exists. Exposed solder/lead surfaces need a separate assembly assessment. A manufacturing DRC pass cannot be described as a 64/103 V electrical-spacing pass. No speculative B4 waiver or DRC exclusion was added. Pending that basis, an uncoated B2 redesign/audit is required; the present dense design is **not released** on its 0.15/0.20 mm manufacturing clearances.

## Findings 6, 9–11: assembly checklist

**DECISION:** ordinary standard through-via manufacture, with drain thermal vias relocated outside FET solder lands. The relocation audit also moved other accessible vias off lands. The resume completed the remaining escapes and separately checked both faces using drill radius and exposed-land polygons. Final `BOARD_AUDIT.json`: zero via centers in lands, zero hole-to-land gaps below 0.1 mm, minimum 0.142377 mm. Standard off-land tented through vias are selected; no filled/capped-via premium is needed by this geometry. Assembly solder/void and mask-web inspection remains required. Ordinary tenting is not described as filling/capping.

**OBSERVATION:** saved connector text identifies J501 input pin 1 / GND pin 2, J502 +5 V pin 1 / GND pin 2, and J503 polarity; compare the pad-net inventory in `BOARD_AUDIT.json` with the mating-face view in `PI_HARNESS.md`. Final mask-subtracted Gerber silk, native silk plot and board/pad locations were inspected. Critical board text is ≥1.0 mm with ≥0.15 mm stroke. The explicit FIX1 revision and fabrication warning remain readable. Native U/Q orientation graphics were retained. Full test-reference coverage remains partial, with omissions in `SILK_IDENTIFICATION.json`. Removed 117 duplicate Fab reference annotations; paired-probe Fab fields are separated. Use native positions and enlarged PDF together for dense control circuitry. No populated probe-body or screw/washer clearance qualification is claimed.

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

The complete 100-reference BOM/CPL remain a review inventory. `BOM_JLC_SMT_REVIEW.csv` and `CPL_JLC_SMT_REVIEW.csv` contain only the 93 nonmanual candidates. `MANUAL_ASSEMBLY.csv` separates C101, D101, SCR301, C217/C218 and J501/J502. No order, upload or supplier acceptance occurred.

**Probe geometry:** TP301/TP302 now have 3.1 mm center spacing beside the SCR, with dedicated branches and no long return-plane slot. Their 2 mm exposed lands do not establish populated probe-body clearance. TP113/TP114 source/gate pickups are now on B.Cu at (35.8,22)/(35.8,18.8), 3.2 mm apart, connected through nearby source/gate escape vias. Always use rated differential probing for the high side. Raw ripple TP504/TP506 are now (60,60.5)/(63.25,60.5), 3.25 mm apart; for fastest edges use capacitor-terminal spring access. Neither shared GND nor the shared high-side escape establishes an isolated Kelvin measurement. Populated access, heatsink insulation/envelope and mounting-hardware insulation remain OPEN.

**Resume update:** R308 moved to (73,34.5), with 4.019 mm authored front K return and off-land gate via at (73,36.3); its long bottom GND branch was removed. Board has 93 SMT candidate references and seven manual operations exactly as above. All supplier offsets remain unaccepted.

**Handback count correction:** C101 is also a radial THT capacitor. Native export already placed it in MANUAL_ASSEMBLY.csv; the earlier 94/six narrative was wrong. All seven manual references are checked explicitly by handback_lite_fix1.py. [PROBE_MAP.csv](PROBE_MAP.csv) supplements omitted silk refs without inventing supplier offsets.

**Finding 7 disposition:** C206 is (41.05,43.6), R203 (40.9,46.3), U201 AGND (43.15,44). U301.3 GND (60.9375,55) and R304.2 GND (56.5,54.175) still join the shared plane rather than an isolated C214.2 (68.975,56) Kelvin branch. A trace drawn across that same filled GND would not isolate its return. Cutting the reference plane to force isolation needs a reviewed detector-return redesign; it is deferred with the pulse/schematic review, not described as fixed. The practical local VCC/FB improvements are retained.
