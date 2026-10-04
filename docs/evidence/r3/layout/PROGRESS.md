# V1A layout progress

NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED

Owner brief: `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/PCB_LAYOUT.md`, read in full on 2026-10-04. Authorized placement/routing despite R2 BLOCKED, directly without sub-agents, only this worktree, step commits, no push/merge/orders.

## Step 0 — complete

Synchronized R203 Value = 24.6k, MPN = TNPW060324K6BEEA and Source with the schematic. No schematic or library changed. KiCad 9.0.6 native schematic parity: **0 issues** (`STEP0_DRC.json`). Fresh ERC: **0 errors / 0 warnings** (`ERC.json`). Initial physical DRC is expected to fail with all 366 footprints at origin: 2,191 violations, 213 unconnected reports. Those are not final layout results.

Copied the owner's layout guide verbatim into `docs/pcb/LAYOUT_GUIDE.md`. Its historical 5.098 V note is superseded by `docs/evidence/r2/R203_OPTION_A.md`: 5.065040650 V nominal, frozen send+return allocation 41.855546 mΩ, 14.043 mV conditional margin. Existing board has **two** copper layers; step 1 will select **four** as explicitly required by the guide, with ASSUMED 70/35/35/70 µm copper.

Tool inventory: KiCad CLI and bundled pcbnew available. Freerouting not found in PATH or installed application/package trees; no installation attempted. Routing will use project scripts. Next: step 1 mechanical envelope and connector arrangement, then placement.

## Step 1 — mechanical study complete

ASSUMED board envelope: 280 × 215 mm, four board-only Ø3.2 mm NPTH mounting holes for a preliminary M3 fixture. Connector positions face the perimeter; final mating/tool/washer envelopes remain OPEN. Selected four copper layers per guide, 70/35/35/70 µm; 1.6 mm dielectric+copper stack is ASSUMED, not fabricator approved. Preserved all five net classes. Native DRC evidence: `STEP1_DRC.json` (unplaced components still overlap; no physical pass claimed).

Git step 0 attempt failed: `Unable to create .../.git/worktrees/wt-pcblayout/index.lock: Operation not permitted`. No permission/lock workaround attempted. Changes remain uncommitted. Next: functional placement with two compact U201 bypass loops and separate power/quiet regions.

## Resume — step 2 complete, 2026-10-04

Read both `PCB_LAYOUT_RESUME.md` and `PCB_LAYOUT.md` in full. Working alone in this worktree. The preceding step-0/1 edits are already committed as `ad04d28`; the earlier Git failure note is historical.

Placed all 366 electrical footprints by functional block. Replaced the oversized provisional envelope with a tested 230 × 195 mm placement envelope (25.50% area reduction); the smaller 220 × 170 mm trial crowded large force-link/connector courtyards. Four layers retained, 70/35/35/70 µm ASSUMED. See `PLACEMENT_REVIEW.md`, `PLACEMENT.json`, and `STEP2_DRC.json`. Native 0.15 mm within-package pad gaps use a narrowly scoped pad-pair custom rule; all other clearances remain 0.20 mm. No schematic, value, net, upstream footprint or severity changed. Visual placement reviewed using native PDF output. Silkscreen cleanup is deferred to step 5. R2/R3 release remains BLOCKED.

Next: authored power geometry, thermal vias/continuous GND, resistance calculation, then remaining signal routing and fresh final DRC/ERC/export review.

Step-2 commit attempt: Git again cannot create the worktree `index.lock` (`Operation not permitted`). Changes remain uncommitted as the brief permits. No lock or permission workaround, push, merge or owner-checkout edit was attempted.

## Resume2 / independent M1 review — active, 2026-10-04

Read `PCB_LAYOUT_RESUME2.md`, its parent brief and `LAYOUT_REVIEW_M1.md` in
full. Baseline HEAD is `1c4c44d`; the historical commit-failure statements
above are superseded by the commits supplied at this resume. Work is solo.

**OBSERVATION:** the actual baseline already has 27 vias, 39 zones and zero
trace segments. These are preliminary step-3 geometry, not a completed route.
Fresh strict baseline DRC: **135 errors, 213 warnings, 499 unconnected,
0 schematic-parity issues**. The rule contract added by the previous worker
matches the supplied fabprep rules; the step-2 same-package waiver is gone.
Existing `RESUME2_*` evidence is historical and will not be overwritten.

- **M1-1 — geometric fix applied:** J502 rotated from −90° to +90°, pin 1
  retained at (230,70.39). Its recorded mate/tool rectangle now occupies
  x=240–250, y=57.69–78.01, outside the right edge and clear of R401.
  Pin 2 is now at (230,65.31), still GND. Existing zones are refilled;
  qualified lands and schematic connectivity are unchanged. See
  `M1_CONNECTOR_FIX.json`. Actual plug/tool/fixture validation remains OPEN.
- **M1-2 — OPEN:** re-evaluate force and return copper after the connector
  change. The read-only checker must not be reported PASS from disconnected
  geometry, omitted neckdowns or an altered frozen setpoint.
- **M1-3 — OPEN:** switching links, force-probe branches and remote output
  ceramics require a folded placement/routing review.
- **M1-4 — OPEN:** compact and pair both dump paths; a DC path calculation
  cannot close their pulse-loop inductance assessment.
- **M1-5 — BLOCKED on engineering disposition:** native 0.15–0.25 mm
  package gaps violate the required 0.20/0.64 mm screens. Asked the owner
  for the fab-rule owner's approved net-pair exceptions or approved
  package/protection change. No waiver, pad shrink, schematic edit or
  severity suppression has been made. Independent layout work continues.

**NEXT:** verify the connector correction, then address the remaining
geometry and path calculation within the unchanged electrical constraints.
Steps 3–6 and R3 release remain incomplete; R4 is not authorized.
