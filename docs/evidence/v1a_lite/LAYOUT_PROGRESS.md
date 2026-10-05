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
