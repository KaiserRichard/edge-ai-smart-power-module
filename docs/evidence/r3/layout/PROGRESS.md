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
