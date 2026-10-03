# Sheet 03 — architecture D test-board capture review

2026-10-03. **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

## Disposition

**CONDITIONAL PASS for capture integrity; electrical release BLOCKED.** Continued the draft in `634dfa3`. The owner’s 2026-10-01 option A permits manual source-trigger/reset and rail-loss hooks in place of the two unresolved autonomous circuits. It does not approve their behavior. All physical tests are **NOT RUN**.

**EVIDENCE:** 259 physical components plus six source declarations; [pin review](PIN_REVIEW.md), independent [pin identities](PIN_CONTRACTS.json), [netlist](captured.xml), and fresh [whole-project ERC after Sheet 03 review](sheet03_review_erc.json). ERC has zero violations, no exclusions or severity reductions. Each declaration follows a real fitted power path recorded in PIN_REVIEW; none asserts a control input.

## Captured blocks

- Upstream LT4363-1 surge stopper, FDB33N25 pass FET and 0.33 Ω sense element; LTC3115-1 auxiliary buck-boost with both compensation branches returning to FB.
- D304 reverse blocking, TPS259470L slow hold charging, two 220 µF held capacitors, separate SAFE5/DET5/3V3_AUX and isolated SER_DRV reservoir.
- Common-source BSC034 pair and LTC7001, 2 MΩ gate bleed, distinct BST–TS and reference capacitors. Force path: `VOUT_5V1 → Q301 → PROT_MID → Q302 → JP301 → VOUT_PROTECTED`; no passive bypass.
- Protected crowbar with two 66 mΩ strings in parallel; independent raw dump with two 198 mΩ strings in parallel. Four protected PCH capacitors, eight retained raw PCH capacitors, separate negative-return diodes.
- Isolated OV comparator/reference/clamp, real buck-PG receiver, observation-only TPS3808 monitors, fault-priority latch and manual MAIN/SERIES ARM memory.

**Correction:** C358/C359 were assigned a wrong 6.3 mm/2.5 mm radial footprint in the partial draft. Panasonic’s [exact EEUFR1E221 record](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1E221) specifies an 8 mm body, 11.5 mm length and 3.5 mm pitch. Both now use `CP_Radial_D8.0mm_P3.50mm`, plus-to-DRV_HOLD/minus-to-GND. An independent regression rejects the old footprint. D303’s cathode graphic now agrees with its preserved A1/K2 electrical pin map; no pin/net reversal was made.

## Manual hooks and intended stable-supply logic

The sheet contains the required text **“TEST HOOK — design proven on bench”**, immediately qualified with **“ALL hardware evidence is NOT RUN”**. The quoted label names the required bench closure; it is not a validation statement.

| Hook | Captured function / limit |
|---|---|
| J603 | Dry contact SOURCE_CONTACT-to-GND; U644 generates SRC_TRIP. No autonomous SW watchdog or input-collapse discriminator is fitted. Manual timing cannot qualify the fault-onset 10 µs/100 µC requirement. |
| J302 | Dry contact manual reset clocks NOFAULT high only while its asynchronous fault clear is released. No persistent-short diagnostic: isolate/discharge sources and verify repair before reset. |
| JP600 | Manual rail-valid link SAFE5-to-MANUAL_RAILS_VALID; R729 pulls invalid when absent. Remove by default. Bench rail checks precede fitting; this link cannot detect a subsequent brownout. |
| J301 / J604 | Separate dry-contact MAIN ARM and SERIES ARM. Genuine PG and main permission must exist for series clear to release. In ideal stable-supply logic, PG loss clears SERIES_ARMED; PG recovery supplies no clock edge. Bounce/held-contact/race/partial-power behavior is OPEN. |
| JP660 / TP313 | Remove the low-current SER_DRV supply connection for controlled driver-supply-loss characterization. Local capacitors remain charged; measure before handling. |
| JP301 / JP330 / JP331 | Removable M4 series, protected-dump and raw-dump force links. Opening a dump link disables that disposal path. Reconfigure only discharged. |
| J605 / J606 | Guarded observations of genuine PG_GOOD and MAIN_PERMISSION through 1 kΩ. No synthetic PG input. |
| TP306…336 | Paired detector, supply, SHDN, PG, fault, gate and force-link observations. TP314/334 return to PROT_MID, never instrument earth; TP335/336 are differential link observations. |

With valid supplies, SRC_TRIP or enabled OV asynchronously clears NOFAULT; FAULT inhibits the source and both arm memories and commands both dumps after POR. Ordinary PG loss only clears series permission. These connections are checked independently from the editable JSON. Propagation delay, recovery width and real VGS/current behavior remain unmeasured.

## Intentional retirement of PR15 circuitry

The following 31 original Sheet 03 references are removed from the active assembly, with the original evidence preserved at PR15 `51d1c2f`:

- U307, R314/R315: old cascaded driver LDO/divider, replaced by the 12 V buck-boost and held charging path.
- U304/U305/U308/U309/U310/U311/U312/U313/U314, R318/R319/R320: old qualification/delay/reset logic, replaced by the owner-authorized manual latch/ARM/rail hooks.
- C310…C325: bypass/delay capacitors belonging to those retired blocks. Active replacement devices have their own named bypasses.

Gate4a’s reserved autonomous U640…647 and full fast interlock/diagnostic circuitry are not an active assembly under option A. U644 and selected U6xx references are reused for the explicit manual circuit; their current maps are in output_block.json/PIN_CONTRACTS, not the older FIX3 reservation. The final freeze coverage report records these exceptions. No PR15 project footprint was removed or modified.

## OPEN risks / next sheet

Autonomous source coverage, interlock brownout/PG recovery, direct SER_DRV loss, persistent-short lockout, held/bouncing contacts, bootstrap leakage, auxiliary startup/compensation/thermal/hold, detector partial power, hot dump/diode/FET ratings, negative return, protected/far-end peak, source envelope, fixture ratings and calibration remain OPEN. Review of current pins/lands does not close these tests.

Next: Sheet 04 Kelvin monitoring, then Sheet 05 connectors/hooks, net classes and final exports. R3 is not authorized by this capture review.
