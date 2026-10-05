# V1A-Lite layout progress — 2026-10-05

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Authority: full owner `v1a-lab/briefs/V1A_LITE_PCB.md`; sole editor, no sub-agents. Baseline `6feb4a8c7c416018deae8919e7bc5203963ab8a0`. Later explicit layout authorization supersedes historical no-layout scope; it does not close electrical R2 blockers or release fabrication. No push, merge, order or upstream changes.

## Step 0 — complete

Fresh schematic import replaces the historical research PCB (retained on tag `v1a-research-layout-wip`, commit `f1d7b6e`). Imported 116 footprints, 244 numbered pads and 60 nets. Independent XML identity/pad/net check: zero issues. Native KiCad schematic parity: zero issues (`layout/STEP0_DRC.json`). Initial unplaced board has 184 unconnected items, expected before routing; not a final DRC pass. Fresh ERC is retained in `layout/ERC.rpt`.

Scripts use KiCad 9.0.6 bundled Python; no software installed. `layout_v1a_lite.py import` is an explicit destructive board regeneration command, authorized only for this Lite task. Existing schematic builders were not run. Source library hashes in `layout/FOOTPRINT_SOURCES.json`.

Next: board mechanics and placement, authored power routing, signals/DRC, then review exports. Commit attempt recorded below.

Git step 0: staging and commit both failed (exit 128), unable to create `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-lite/index.lock`: Operation not permitted. Per brief, continue uncommitted; no permissions or locks changed.

## Step 1 — mechanics complete; conditional stackup decision

80 × 60 mm, 1.6 mm FR4, 2 layers, 35 µm (1 oz) outer copper; four 3.2 mm M3 NPTH at 4 mm offsets. J501/J502 on opposite edges. Cost-first review candidate, **not thermally qualified**. A 20 mm × 5 mm × 35 µm copper path gives 1.97 mΩ at 20°C; the same at 85°C gives 2.47 mΩ (12.4 mV at 5 A). This is a sizing calculation, not extraction from final copper. Detailed geometry and return-path resistance follow routing. Buck loss up to 2.417 W would need ≤24.8 K/W at historical assumed 50°C ambient/110°C junction; neither the proposed ambient nor actual thermal resistance is qualified. Retain two layers for the authorized review study, with upgrade contingent on thermal validation. Do not claim 1 oz establishes safe 5 A performance.

JLC rules: https://jlcpcb.com/capabilities/pcb-capabilities accessed 2026-10-05. Selected 0.15 mm minimum tracks/clearance, 0.20 mm power clearance, 0.6/0.3 mm vias, 0.25 mm hole clearance/spacing and 0.5 mm copper-edge clearance. Published 1 oz 2-layer track/space capability is 0.10/0.10 mm. No DRC exclusion is introduced. Schematic ERC settings retained.

## Step 2 — in progress

Placement iterated against actual component bounding boxes and native courtyard DRC. Converter bypasses, inductor, bulk bank, SCR, fuse and connectors get priority. Keep historical reports; final checks will supersede exploratory findings.

Step 1 commit attempt: same `index.lock` permission failure; uncommitted.

## Step 2 — placement complete

116 schematic footprints placed without component/courtyard overlaps or shorts in the pre-route native DRC. Four M3 holes remain board-only. C203/C204 sit beside paired VIN/PGND pins; L201 lies directly right of U201; FB/VCC parts lie on the quiet left side. Raw bulk and SCR are directly above the output path. Input detector moved beside the FET/gate area after initial placement review. Test pads are accessible; sense routing is pending. `layout/PLACEMENT.json` records coordinates. Preliminary placement render inspected. Remaining silk label warnings will be corrected before final exports.

Step 3: power pours and thermal vias authored; initial power DRC caught ground via/pad clearances and a fuse-pad conflict. These are being corrected before signals. No final DRC pass claimed.

## Resume audit and Step 3 — complete, 2026-10-05

The resume brief's step-3 stop description and preceding progress entry were stale. Commit `1d99ea9` actually contains completed routing, silk cleanup, final DRC and copper extraction. Current board SHA256 `597b30be4ef73be637cd79bbda192d3280ca3ef2999b7fca378f60f1cf37c908` exactly matches PARITY, COPPER_GEOMETRY and both resistance reports. No finished placement or routing was regenerated. Fresh `layout/RESUME_DRC.json` confirms zero violations, zero unconnected and zero parity findings; `RESUME_ERC.rpt` confirms 0 errors / 0 warnings. Earlier POWER_DRC errors are historical, resolved in the saved board.

EVIDENCE: 2,854 track/via objects, 18 zones/rule areas; inspected front/back copper and assembly plots. Lower layer is a connected GND pour with local signal clearances, isolated FET drain spreaders and VIN strap, not an unbroken all-ground sheet. Buck footprint has no exposed ground pad; vias connect actual ground/VIN pins. FET drain vias must never be connected to GND.

CALCULATION: inherited geometry mesh at 0.1 mm gives capacitor-to-J502 copper round trips of 3.232 mΩ (C209) and 5.843 mΩ (C214) at 20°C, or 4.058 / 7.335 mΩ at illustrative 85°C. This includes positive copper on both sides of F301 and GND return; excludes fuse body, solder and harness. At 5 A the larger hot estimate is 36.7 mV / 0.183 W. The 0.2 mm mesh gives 5.595 mΩ cold for C214, 4.23% lower; raster convergence is approximate, not a guaranteed upper bound. With 40 mΩ hot harness and 9 mΩ cold fuse, nominal Pi voltage is 5.06504 − 5×(0.040+0.009+0.007335) = 4.7834 V; only 33.4 mV remains for regulator tolerance/ripple/transients and hot-fuse increase. This is NOT a 4.75 V compliance claim.

DECISION: retain the already-routed 80×60 mm / 2-layer / 1 oz review candidate. Voltage-drop estimate does not force thicker copper; buck/FET temperatures and EMI still require qualification. TI's four-layer recommendation is not met by this cost study. Source/gate and SCR sense lead geometry, assembly process for vias in solder lands, and manufacturer layout deviations remain explicit engineering-review items. No electrical blocker is closed. Next: tighten/document JLC rule coverage and fresh final checks (step 4), then review-only exports (step 5).

Step 3 Git: authorized staging failed exit 128 (worktree index.lock: Operation not permitted). Continue uncommitted as directed; no lock/permission changes.

## Step 4 — complete: native checks 0/0

Retained existing 0.15 mm track/clearance minimum, 0.20 mm power clearance, 0.60/0.30 mm vias, 0.25 mm general hole clearance/spacing, 0.50 mm copper-edge clearance and 0.10 mm mask web. Added `hardware/kicad/V1A.kicad_dru`: drilled pad spacing 0.45 mm, plated component pad annulus 0.20 mm, plated component hole-to-copper 0.28 mm. These close distinct JLC published limits; via/NPTH constraints remain more conservative than the respective 0.20 mm limits. The initial exploratory global 0.28 mm check also applied to NPTH fills; it is retained in JLC_DRC.json. The final rule correctly distinguishes PTH from NPTH and does not suppress any findings. No DRC exclusions or severity downgrades.

Final `layout/JLC_FINAL_DRC.json`: **0 errors / 0 warnings / 0 unconnected / 0 schematic parity issues**, with all-track-errors and severity-all enabled. Fresh ERC: **0 errors / 0 warnings**. Schematic and board geometry unchanged. JLC source and TI layout comparison recorded under `third_party/v1a_lite_layout/`. DRC is manufacturing geometry/netlist evidence only. Step 5 will package this exact board, keeping all electrical/thermal/assembly release blockers OPEN.

Step 4 Git: authorized staging again failed exit 128 (index.lock: Operation not permitted). Changes remain uncommitted under the explicit fallback.

## Step 5 — complete: review-only package and explanation

Generated `fab/` with two-layer Protel/JLC Gerbers, separate PTH/NPTH Excellon drills and maps, review-only ZIP, 100-row JLC BOM and matching 100-row CPL, native positions, exclusions and rotation review, 11 per-layer PDFs and PNGs, native bare-board 3D render, commands/logs and hash manifest. D101 alone has a blank LCSC field and retains exact Bourns/Mouser identity; it needs the external sourcing route. Nothing was uploaded or ordered.

Visually inspected all 11 layer views, both drill maps and the 3D board. The 3D renderer cannot create its macOS model cache under the restricted filesystem; even a temporary-config/explicit-model-path retry omits component bodies. The bare-board image is retained and documented, not called a populated assembly model. F.Fab is a dense reference drawing; footprint orientation and JLC centroid/zero-angle remain OPEN. `LAYOUT_EXPLAINED.md` provides the student explanation, pictures, copper budget and complete OPEN list.

`layout/PACKAGE_VERIFICATION.json` records 13 passing integrity/check assertions: artifact/input/exporter hashes, ZIP CRC/warning, matching 100-reference BOM/CPL, D101-only LCSC exception, no source differences, DRC/parity/connectivity 0, ERC 0/0, all layer files, and unchanged CAD during resume. Historical capture checker result is preserved separately: 565 pass, one expected pre-layout PCB-preservation failure. No electrical-validation or full-suite pass is claimed.

**FINAL:** DRC 0 errors / 0 warnings / 0 unconnected / 0 parity issues; ERC 0 errors / 0 warnings. Board 80×60 mm / 2 layers / 1 oz / 1.6 mm. Sampled copper loop up to 5.843 mΩ at 20°C / 7.335 mΩ at illustrative 85°C; 36.7 mV at 5 A. Nominal Pi budget has only 33.4 mV remaining with hot-harness/cold-fuse assumptions; compliance and thermal performance remain OPEN. Electrical findings 1–4, source/ambient, sense/layout/assembly/harness/cost qualification and fabrication release remain BLOCKED/OPEN.

Next: independent engineering review of the delivered package and closure of listed blockers before any fabrication/physical bring-up. Do not rerun import/placement/power builders on the finished board without an intentional new layout revision. All earlier exploratory evidence retained. Final commit result follows.

**Final step-5 Git result:** staging failed exit 128: unable to create `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-lite/index.lock` (Operation not permitted). Steps 3, 4 and 5 each had an authorized commit attempt; no commit could be created. Work is retained uncommitted at HEAD `1d99ea96947f07569d571237691ffa255050c973`, as instructed. No push, permission/lock modification, merge or order. `git diff --check` passes. Full deliverable paths: `layout/DELIVERABLE_FILES.txt`. All requested review deliverables are present; fabrication remains blocked.

## FIX1 — resume audit, 2026-10-05

Authority: `V1A_LITE_PCB_FIX1_RESUME.md` and full `V1A_LITE_PCB_FIX1.md`. Sole editor; work on `feat/v1a-lite-cost-reduction`; no push, merge or order. Baseline `44eee9c`. Read all independent R1 findings before editing. Fresh pcbnew audit reproduces board SHA256 `7c6157f95bd1f44c2ec752e5eaddd74a85ff80e7888d5e0bf94667860e026083`; earlier work is retained, not regenerated.

| Finding | Audit at resume | Remaining work |
| --- | --- | --- |
| 1 polarity | DONE: J501/J502 numbered positive/GND labels and J503 polarity match actual pad nets; J502.1 (84,44), .2 (84,47.96). | Final mask-subtracted silk review. |
| 2 BOOT | DONE: R204 (42.55,40.8), C205 (42.5,39.2); RBOOT 2.60 mm F.Cu, zero vias; CBOOT 5.35 mm total tree, zero vias, no old bottom route. | Retain; distinguish total tree from pin-to-cap length; startup/ringing remains untested. |
| 3 crowbar | LAYOUT CHANGED: K/A/G (69,33.4)/(66.46,33.4)/(63.92,33.4), C217 GND (69,26), C218 reversed with GND (76,26); L2 GND and L3 force copper, no old TP302 slot, no intervening fuse. | Document pulse/lead/ESL/cutoff sensitivity and unresolved electrical limits; shorten R308 sense where practical. |
| 4 bridge/budget | LAYOUT DONE: R308 moved to (61,30.7), fuse to (74.5,43), 4 mm authored corridor; extracted L201→F301 1.057 mΩ cold versus 1.834 mΩ old. Harness already ≤25 mΩ. | Missing voltage budget JSON/report; final extraction after remaining edits, include -1% reference and resistor tolerances. |
| 5 thermal | LAYOUT DONE: 4 layers, 35/15.2/15.2/35 µm, expanded drain copper F/B/L3; L2 GND. | Existing assumed thermal screen FAILS; report numbers honestly, add cost/source/qualification record. |
| 6 probes | PARTIAL: SCR pair 3.1 mm apart, no long slot. Q102 pair still 12.50 mm apart. | Move source/gate pickups closer and add local raw-ripple GND access; populated access remains OPEN. |
| 7 VCC/FB | PARTIAL: local top-only VCC 2.357 mm, FB 10.542 mm tree, C206/R203 moved. | Inspect local AGND and detector Kelvin return; avoid claiming net GND is an isolated sense path. |
| 8 spacing | DOCUMENTED OPEN: manufacturing clearance only, B4 environment not established. | Explicit conservative audit and voltage-pair basis; cannot invent environmental requirements. |
| 9 silk/assembly | PARTIAL: 1.0/0.15 mm board labels/rules, warning/revision and native marks present. | Essential TP identification and readable assembly annotation. |
| 10 via process | PARTIAL: FET vias moved; 10 via centers still in SMD lands including C203/C209. | Finish off-land escapes where practical; inspect hole/mask margin, not centers alone. |
| 11 rotations | PARTIAL: 94 SMT candidates / 6 manual operations; exact external D101 retained. | Per-package supplier checklist and explicit unaccepted offsets; no guessed rotations. |

Baseline evidence is retained in commit `44eee9c` and existing intermediate reports. Engineering/fabrication status remains BLOCKED; completion of this correction task is not electrical validation.

### FIX1 — remaining layout corrections completed

- **3:** R308 moved again to (73,34.5), right of SCR's actual body/courtyard. Its ground land now has a 4.019 mm top trace to K; the obsolete ≈14.7 mm bottom return was removed. Gate connects by a local off-land via to the existing driver branch. CB_COLLECTOR was detoured around this placement. This is a separately authored branch, not proof of an isolated Kelvin return in the shared GND plane.
- **6:** TP113/TP114 moved to B.Cu (35.8,22)/(35.8,18.8), 3.2 mm apart, using nearby source/gate vias. Old TP114 leaf stub pruned, common-source control junction preserved. Raw TP504/TP506 now (60,60.5)/(63.25,60.5), 3.25 mm apart; existing GND access reused. SCR pair retained at 3.1 mm spacing; no L2 signal routing or new return-plane slot.
- **9:** Added locally placed 1.0 mm/0.15 mm silk references for test pads and Q101/Q102/U201/SCR301 where geometry allowed; moved key Fab fields to their own body/pad centers. `SILK_IDENTIFICATION.json` records placement and any omissions. Retained numbered connector labels, revision and warning.
- **10:** Relocated ten inherited via centers out of lands, then checked BOTH faces and actual hole radii. Moved Q106 GND via, removed a redundant C203 ground via and vias under moved test pads. R201 ground-via escape required rerouting the existing bottom EN segment; L2 stays GND. Final audit: **zero centers in SMD lands; zero hole-to-land gaps <0.1 mm; minimum 0.142377 mm**. Standard tented through vias with off-land holes selected, no fill/cap premium assumed. Inspection of solder fillets/voids is still required.

`RESUME_SILK_DRC.json`: **0 violations / 0 unconnected / 0 parity**. Exploratory DRC reports retained; earlier failed candidates were corrected before export. No schematic or setpoint changes. Remaining voltage, pulse, thermal, spacing, supplier-orientation and final package evidence follows.

Git finding-group commit: audit staging/commit both failed with `index.lock: Operation not permitted`; further group attempt recorded separately. Changes stay uncommitted per brief; no permissions/lock changes.

### FIX1 — final resume audit and closure, 2026-10-05

Re-read both full briefs and R1 findings 1–11. Baseline is now **51d138b**, which already contains the previous worker's remaining layout changes and draft reports. Fresh pcbnew audit confirms board SHA256 **f4d096e2e63b12c7f2d493a306d8c2a74383398720bba7072b95768c5b67501e**. No CAD or schematic changes are needed for this handback; completed work is retained. Historical progress above is not a statement that those changes remain uncommitted today.

| Finding | Final disposition | Verified geometry / handback work |
| --- | --- | --- |
| 1 | Layout addressed | Numbered J501/J502 polarity and J503 labels agree with pad nets; visually reviewed. Actual keyed-harness continuity still required. |
| 2 | Layout addressed | R204 (42.55,40.8), C205 (42.5,39.2), RBOOT 2.600 mm / CBOOT 5.350 mm F.Cu, zero vias. L2 GND only. |
| 3 | Layout addressed; electrical BLOCKED | SCR K/A/G (69,33.4)/(66.46,33.4)/(63.92,33.4); R308 (73,34.5); local cathode branch and cap orientation retained. Package/lead/ESL, gate waveform, cutoff, energy and recovery remain unqualified. |
| 4 | Conditional allocation PASS | Bridge 1.073683 mΩ cold, 6.740 mV at 5 A/assumed 85°C. Harness ≤25 mΩ; reference/divider screen 4.809622 V, +59.622 mV. Full operating worst case OPEN. |
| 5 | Thermal FAIL; mitigation documented | Four-layer live drain copper retained. At 50°C ambient/h=10, rises Q101/Q102/U201 = 131.0/131.6/156.8 K. Added calculated, conditional 2 A initial bench proposal; no schematic substitution or validated rating. |
| 6 | Geometry addressed; access OPEN | Q102 pair 3.2 mm, SCR pair 3.1 mm, raw ripple pair 3.25 mm. Added complete coordinate/net PROBE_MAP.csv for physical review. |
| 7 | PARTIAL, explicitly deferred | C206 (41.05,43.6), R203 (40.9,46.3), local top routing retained. Detector-return isolation remains a reviewed redesign item; an extra same-net trace would not make it Kelvin. |
| 8 | OPEN requirements | 64 V source and 103 V pulse cases distinguished; coating/environment/altitude basis unavailable. Manufacturing DRC is not insulation approval. |
| 9 | Process sizes addressed; coverage PARTIAL | ≥1.0/0.15 mm board text; warning/revision/polarity checked visually. Missing local silk refs documented and supplemented with probe map. Added missing VISUAL_REVIEW.md. |
| 10 | Layout/process addressed | Fresh both-face audit: zero via/land overlaps, minimum hole-to-open-land 0.142377 mm. Standard off-land tented vias retained. |
| 11 | Disposition complete; offsets OPEN | Found/corrected prose error: **93 SMT / seven manual**, including THT C101. Export was already correct. No guessed supplier offsets. |

Added reproducible `scripts/handback_lite_fix1.py`: saved-board inventory, thermal mitigation calculation, probe map and package hash/ZIP/refset checks. Fresh all-severity native **DRC 0/0/0; ERC 0 errors/0 warnings**. Public JLC entry price rechecked 2026-10-05: from $2/five for 1–4 layers, advertised delta $0; exact configured 80×60 mm quote remains OPEN. Final package regeneration and final Git outcome follow below. No push, merge, order, electrical validation or gate release.

**Final package:** regenerated using the existing exporter in an empty temporary directory, verified and copied into `fab/`. Previous manifest retained as `fix1/PRE_HANDBACK_FAB_MANIFEST.json`, previous complete package retained in commit `51d138b`. All input hashes, raster views/render and assembly files are identical; `HANDBACK_EXPORT_IDENTITY.json` binds the visual review to this fresh export. Gerber/drill/PDF metadata and logs were refreshed. **100 package/identity checks PASS**, including ZIP-to-loose-file bytes, DRC, ERC, source hashes, calculation board hashes and corrected manual/SMT sets. Fresh check and export logs are under `fix1/`; no CAD bytes changed.

**Final Git result:** both authorized current staging attempts (finding/evidence group and final package/manager group) failed exit 128: `Unable to create .../.git/worktrees/wt-lite/index.lock: Operation not permitted`. No commit could be made. All current handback changes remain **uncommitted at 51d138b**, as the brief directs; previous workers' committed work remains intact. No permission/lock changes, push, merge, upload or order. `git diff --check` passes. Requested correction/evidence handback is complete with the explicit partial/OPEN dispositions above; fabrication and electrical validation remain BLOCKED.

## FIX2 — final polish documentation handback, 2026-10-05

This section records the saved-board evidence under `docs/evidence/v1a_lite/fix2/`. No KiCad file was edited in this documentation pass. The FIX2 evidence binds to board SHA256 `01e7046e4072d0dfcc3dd750141c8a14cbf554cbbac3dc0db5ca3a1d246d1066`; `EXPORT.log` reports a regenerated `fab/` review package. These are geometry, file-integrity and calculation results, not electrical validation or fabrication release.

| Item | What the FIX2 evidence shows changed | Status |
| --- | --- | --- |
| 2 — bootstrap/control loop | `GEOMETRY_REVIEW.json` reports top-layer pin-to-component path reductions: RBOOT **1.660 mm** (from 2.600 mm), CBOOT **4.616 mm** (from 5.350 mm), C205_SW **5.945 mm** (from 7.195 mm), VCC **2.248 mm** (from 2.357 mm), and FB **2.842 mm** (from 2.951 mm). L2 remains one GND shield and the main SW zone is unchanged. `BOOT_DRC2.json` is 0 violations / 0 unconnected / 0 parity. | Layout refinement addressed for this pass; startup, ringing and converter behavior remain BENCH/OPEN. |
| 4 — 5 A output path / Pi allocation | The 0.1 mm four-layer mesh reports the C214 round trip as **4.378396 mΩ at 20°C / 5.496858 mΩ at assumed 85°C**; the hot value is **27.484 mV at 5 A**. With the PI harness allocation, the low-setpoint screen is `5.006350 − 5 × (25 + 9 + 5.496858) mΩ = 4.808866 V`. | Conditional allocation only; hot fuse, harness, joints, copper/plating, ripple, transients and uncertainty remain BENCH/OPEN. This is not a 5 A rating. |
| 6 — probe access | `BOARD_AUDIT.json` records final Q102 TP113/TP114 separation **3.20 mm**, SCR TP301/TP302 **3.10 mm**, and raw-ripple TP504/TP506 **3.45 mm**. `PROBE_DRC.json` is 0 violations / 0 unconnected / 0 parity. | Pad geometry addressed; populated probe access, pickup transfer function and shared-plane/Kelvin measurement accuracy remain BENCH/OPEN. |
| 7 — VCC/FB and detector return | The VCC/FB geometry was tightened as recorded above; L2 remains a single GND shield and the main SW zone is unchanged. The temporary `kelvin_cut_test` removed two candidate tracks and produced two intentional unconnected islands; its own evidence says it was a temporary-copy test, not final-board DRC. | VCC/FB geometry improved, but no isolated detector Kelvin return is established; detector behavior and transient verification remain OPEN. |
| 9 — silk identification | `SILK_IDENTIFICATION.json` records the FIX2 marks and intentional omissions/displaced local marks; `SILK_DRC.json` is 0 violations / 0 unconnected / 0 parity. | Silk process/DRC check addressed; local identification coverage remains PARTIAL/OPEN where the evidence records back legends or omitted local marks. |
| 14 — mechanical closure | No qualified screw/washer, connector/probe, strain-relief, or SCR live-tab insulation/cooling envelope is shown by the FIX2 evidence. `EXPORT.log` retains the incomplete 3D-model warning and says populated fit requires review. | OPEN/BENCH; no mechanical release evidence. |
| Final checks/package | `FINAL_DRC.json` reports **0 violations / 0 unconnected / 0 schematic parity issues**; `ERC.rpt` reports **0 errors / 0 warnings**. `EXPORT.log` reports completion of the regenerated review package and retains its OPEN warnings. | Clean file/geometry evidence only; fabrication and electrical validation remain BLOCKED. |

Remaining BENCH items are carried into `LAYOUT_EXPLAINED.md`: crowbar pulse/gate/recovery and remote overshoot; buck/FET loss, temperature and hot turn-off SOA; hot fuse/harness/joint drop and full operating voltage/ripple/transient behavior; source/environment/coating/altitude and spacing qualification; populated probe, solder, connector, mechanical and assembly checks; and supplier/contact/material limits needed before testing. No unverified behavior is closed by the FIX2 checks.
