# Brief 02 conductor review follow-up — 2026-09-29

Continue your existing task; this is not a new worker assignment. Preserve the 5.5 V amendment and all hardware/architecture restrictions.

Conductor reviewed the two initial commits in the separate clean v1a-wt-review-brief02 worktree at 7e78c2a. The unit tests and capture check pass, but check_repository.py FAILS there on three RAW_SIDE_RATING_SCREEN.md links to ignored PDF caches. Replace those Markdown link targets with the matching authoritative manufacturer URLs already pinned in source_register.json; preserve cache paths/hashes as text. Do not weaken the repository checker or commit vendor PDFs to hide the portability issue. Rerun checks from a state without vendor caches (a separate temporary checkout if needed) before final hand-back.

Task 4 openly states its required verified candidate specifications and footprint comparison are incomplete because the earlier override restricted downloads to Task 1. This conductor follow-up expands that research permission ONLY to official manufacturer datasheets/drawings for the candidates already listed in OPTION_I_CANDIDATES.md and exact orderable variants of those candidates. Archive under third_party and record full provenance. This is research permission, not part selection, architecture approval, or permission for software installation. Finish the source-backed comparison where access permits; document blocked sources individually. Do not invent guarantees absent in the datasheets or design/capture a replacement architecture. Keep provisional timing and reset-policy gaps explicit.

The historical 5.49 V result used 0.4 us isolation, whereas the brief requested up to 2 us. Your Task2 note identifies this. Make this discrepancy prominent in the final eight-criterion report, along with both recalculated peaks and margins. Retain the historical evidence unchanged.

The user wants a complete schematic package before handing it to their brother. Your deliverable remains analysis only; do not respond by filling Sheet 03 or asserting readiness. Finish and hand back the evidence and explicit remaining blockers.
