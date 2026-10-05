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
