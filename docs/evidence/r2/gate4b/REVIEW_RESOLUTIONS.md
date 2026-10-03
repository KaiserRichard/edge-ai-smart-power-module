# Gate4b review finding resolutions

2026-10-03. **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

**STATUS: CONDITIONAL PASS for authorized capture; electrical release BLOCKED.** This is the editor's correction record, not a new independent-review verdict. The original external REVIEW_4B_S0102.md is unchanged. Its reviewed hardware was 634dfa3; this resume continued 74b9dc8. Input paths/hashes and actual connected net identities are in [REVIEW_RESOLUTIONS.json](REVIEW_RESOLUTIONS.json).

| Original finding | Correction and evidence | Disposition |
|---|---|---|
| Missing L201_IN/R640 and VIN_PROTECTED/R644 detector interface | Sheet02 now exports L201_IN through its hierarchical port and root pin. Sheet03 receives that net and VIN_PROTECTED. The fresh XML puts **L201.1, JP201.2, PF4.1, TP202.1 and R640.1 on the same full net**; R644.1 shares U201.8/.12 and C201.1. The frozen R640–642/R644–645/R651–652, U640/U642/U647, clamps and bypasses provide the actual sensing endpoint. | **PASS for interface capture.** Autonomous qualification/trip memory remains absent under owner option A. |
| Unsupported “design proven on bench” assertion | Sheets02/03/05 quote the exact brief phrase only after **FUTURE ACCEPTANCE REQUIRED**, immediately followed by **UNTESTED CANDIDATE; evidence NOT RUN**. Current PDF contains these qualifications. | **PASS for annotation correction.** No bench validation claimed. |

**DECISION:** preserve the owner-authorized manual source trigger/reset. U640's SW_HIGH and U642's VIN_GOOD_FAST end at observation pads (plus the frozen SW hysteresis feedback); they never drive SRC_TRIP or permission. U641/643/645/646, their timer/memory passives and autonomous fault coverage remain OPEN. U644 retains its explicitly documented manual-trigger assignment. No 10 µs or 100 µC system result follows from these additions.

**EVIDENCE:** 21 added physical references; no existing physical reference removed, and no existing MPN/value/footprint or pin-to-leaf-net assignment changed relative to 74b9dc8. The L201_IN full name intentionally becomes hierarchical rather than child-local. The native BUCK_SW/C205 bootstrap boundary stays before JP201. No additional power flags, ERC exclusions or severity reductions. [Final ERC](ERC_FINAL.json): zero violations at all severities. All 50 regression tests pass; three new mutations reject native-SW sensing, same-named disconnected local nets and an observation output driving the manual fault input.

**Pin evidence:** [PIN_REVIEW.md](PIN_REVIEW.md) records manufacturer pin tables, package variants, NC pins and the absence of exposed pads for the three added ICs/four diodes. Existing footprints are reused unchanged; all physical pad-number sets match. Exact source records and attribution remain under third_party/gate4b.

**Visual evidence:** the full six-page [PDF](V1A_GATE4B_REVIEW.pdf) was inspected, with detail inspection of the new source front end and root hierarchy. Warnings and future-acceptance notes are present; no clipping was found. Sheet03 is A0 portrait and needs native-size or zoomed review.

**OPEN RISKS:** analog threshold/hysteresis/settling and shared-clamp injection, SAFE5/hold loading, partial-power recovery, probe capacitance, autonomous discrimination/timing, brownout/PG/series-driver loss, persistent-short diagnosis and every existing power/thermal/fault/fixture/harness qualification. Physical tests remain NOT RUN; no R3/R4/R5 release.
