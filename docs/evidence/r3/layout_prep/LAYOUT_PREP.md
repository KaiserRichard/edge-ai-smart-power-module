# V1A layout preparation

2026-10-03. Baseline: `6d25cf28c4d246417c0a89ec89574c702850e069`, after the U316 check.

**STATUS: CONDITIONAL PASS for the unplaced PCB import. Guide installation is BLOCKED by filesystem permissions. R2 electrical release / R3 layout release remain BLOCKED.**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## What was done

- Read `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/LAYOUT_PREP.md` in full. Worked directly without sub-agents.
- Created [V1A.kicad_pcb](../../../../hardware/kicad/V1A.kicad_pcb) beside its existing project. KiCad CLI 9.0.6 has no schematic-to-board import subcommand; [prepare_layout_board.py](../../../../scripts/prepare_layout_board.py) performs the initial transfer using a fresh native XML export and KiCad's board API.
- Transferred all 366 physical references, footprint assignments, fields, schematic UUID paths, assembly attributes and 1,027 numbered-pad net connections. Nonphysical power flags are absent from the board.
- Left every footprint anchor at `(0,0)`, orientation 0°, unplaced. **Zero tracks, vias, zones, board drawings or outline.** The default empty-board layer configuration is not a selected fabrication stackup.
- Verified all five net classes through KiCad's loaded board/project and every named net's effective class. The existing project required **no change**. Schematics, symbols, footprint libraries and library tables also remain unchanged.
- Prepared [Critical placement per sheet](CRITICAL_PLACEMENT_SECTION.md), including current refdes, fast-current loops, local returns, manufacturer guidance and open decoupling questions. No numeric placement distance was invented where the reviewed layout section provides none.

## Net-class evidence

**EVIDENCE:** [IMPORT_CHECK.json](IMPORT_CHECK.json), including file hashes and the complete resolved-net map. KiCad stores shared net-class rules in `V1A.kicad_pro`; they are not duplicated as legacy `net_class` sections in the board file. Open the board through this project to retain those settings.

| Class | Named nets | Track width, mm | Clearance, mm | Via diameter / drill, mm | Microvia diameter / drill, mm |
| --- | ---: | ---: | ---: | --- | --- |
| Default | 0 | 0.20 | 0.20 | 0.60 / 0.30 | 0.30 / 0.10 |
| HighCurrent | 29 | 2.00 | 0.20 | 0.60 / 0.30 | 0.30 / 0.10 |
| Switching | 4 | 1.00 | 0.20 | 0.60 / 0.30 | 0.30 / 0.10 |
| Kelvin | 4 | 0.20 | 0.20 | 0.60 / 0.30 | 0.30 / 0.10 |
| Signal | 121 | 0.20 | 0.20 | 0.60 / 0.30 | 0.30 / 0.10 |

There are 158 named nets and 49 explicit no-connect nets, 207 total. No-connect nets retain Default. The XML's known local-net class discrepancy is not used for PCB class assignment; the original project rules resolve correctly in KiCad. These values are editor presets, not qualified copper geometry or permission to use microvias.

## Validation

| Check | Result / practical limit |
| --- | --- |
| Fresh board import/reload | **PASS:** all 366 references, values, assigned footprint IDs, full hierarchical UUID links, assembly attributes, numbered-pad sets and nets match. All 158 named nets resolve to the expected class dimensions. |
| Capture/pin/footprint contracts | **PASS:** [CAPTURE_CHECK.json](CAPTURE_CHECK.json), using existing independent validators on the fresh XML and installed footprint library. |
| Existing regression suite | **PASS:** 50 tests, [tests.log](tests.log). |
| KiCad schematic parity | **PASS:** zero parity issues in [DRC.json](DRC.json). The initial DRC found 56 test-pad BOM exclusions omitted by KiCad's XML export. Those attributes were read directly from the native schematics and synchronized. [Initial report](DRC_initial.json) retained. |
| Physical DRC | **FAIL / expected at this stage:** exit 5; 2,191 reported violations and 213 unconnected items. Includes overlap/short/clearance/holes/silk errors from the origin pile, one missing outline, and nine text-height warnings requiring later review. Counts are KiCad's reported counts, subject to its reporting caps. No exclusions or severity relaxations were added. |
| Visual review | [UNPLACED.png](UNPLACED.png), rendered from the CLI [SVG](UNPLACED.svg), inspected: stacked footprint geometry at the origin, no routing/outline. This only confirms the import state; the pile cannot support assembly/thermal/clearance review. |
| Standard library provenance | **PASS:** all 24 used stock footprint files match upstream KiCad library tag 9.0.6 at the exact commit in [source provenance](../../../../third_party/layout_prep/SOURCES.md). |
| Guide patch | `git apply --check` passes against guide branch `8f9ebe5576a8aa177948b5e772ae4e815ec85446`; all 250 explicitly spelled refdes in the new section exist in the fresh capture. |
| Legacy repository/CLI scope checks | **FAIL on the older blanket no-PCB guard only.** [Repository log](repository_check.log) still verifies all 32 existing hardware files. The current brief explicitly authorizes this import. Those older guards were left intact; the functional capture validators were run separately, as recorded above. |

ERC was not rerun because no schematic changed. DRC/parity and tests establish capture/import consistency only; electrical behavior and all physical tests remain unvalidated.

### Reproduce the import check

From the capture worktree:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9 \
  scripts/prepare_layout_board.py \
  --kicad-cli /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli \
  --footprints /Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints

/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc \
  --format json --severity-all --schematic-parity --exit-code-violations \
  -o docs/evidence/r3/layout_prep/DRC.json hardware/kicad/V1A.kicad_pcb
```

The script creates a board only if none exists; otherwise it verifies without editing it and rejects placement/routing. KiCad's Python runtime emits a wx diagnostic in this headless session; the saved board reloads and the native CLI parity check completes. `SaveBoard(..., True)` intentionally leaves project settings untouched.

## Guide-worktree handoff

**BLOCKED:** opening `/Users/quockaiser/Desktop/Research/wt-layoutguide/docs/pcb/LAYOUT_GUIDE.md` for writing returned `Operation not permitted`. That worktree is outside the session's writable roots, and escalation is unavailable. No target file was changed and no commit was made there. This is a filesystem restriction, not a request for additional engineering approval.

Review the [prepared full document](LAYOUT_GUIDE.md.prepared) and [patch](layout-guide.patch). [GUIDE_HANDOFF.json](GUIDE_HANDOFF.json) records the target branch/commit and before/after hashes. From a session with write access, use:

```sh
cd /Users/quockaiser/Desktop/Research/wt-layoutguide
git branch --show-current
git apply --check /Users/quockaiser/Desktop/Research/wt-gate4b/docs/evidence/r3/layout_prep/layout-guide.patch
git apply /Users/quockaiser/Desktop/Research/wt-gate4b/docs/evidence/r3/layout_prep/layout-guide.patch
git diff --check
git diff -- docs/pcb/LAYOUT_GUIDE.md
git add docs/pcb/LAYOUT_GUIDE.md
git commit -m "docs(pcb): add critical placement guidance for all V1A sheets"
```

The expected branch is `docs/pcb-layout-guide`. If the guide has changed, review/reconcile the patch before applying. If Git refuses `index.lock`, leave changes uncommitted as the brief requires.

## Decisions, open risks and next gate

**DECISION:** board import and placement preparation only. No placement, routing, electrical redesign, gate release, push or fabrication action.

**OPEN RISKS:** unresolved electrical/thermal/fault/fixture/harness work from R2; force-link switching geometry; stackup and final current/clearance rules; U315 local driver bypass, U306 input bypass allocation and U327 local output-ceramic discrepancy noted in the new guide section. No component or wiring change is authorized by a placement recommendation.

**NEXT GATE:** install/review the guide addition, resolve R2 engineering items, and authorize the owner's placement before R3 layout work. At that stage, open `V1A.kicad_pro`, inspect Board Setup → Design Rules → Net Classes, and use Tools → Update PCB from Schematic (F8) to confirm the native transfer remains synchronized. Avoid committing any footprint moves during this preparation handoff. R4 fabrication remains unreleased.

## Local Git handback

The authorized local commit stopped at `git add`: Git could not create the capture worktree's `index.lock` (`Operation not permitted`). Per the brief, all capture changes remain uncommitted. The guide-worktree commit is also blocked because its target file cannot be written. See [Git attempt log](git_commit.log). No lock/permission changes were attempted; nothing was pushed.
