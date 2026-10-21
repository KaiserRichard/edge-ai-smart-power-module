# Visual lesson rebuild — editorial record

Resumed from `d41ce3a` and `9be63e7` on `docs/illustration-audit`, following `LESSONS_V2_RESUME2.md`, `LESSONS_V2_RESUME.md` and the full `LESSONS_V2.md`, including the owner's 23:45 feedback. Lesson 03 and 03b are reserved for Claude and are not edited in this continuation. Work stays in this checkout; the owner's vault and review files are read-only. Local commits are authorized; no push is authorized.

## Source boundary

- Content baseline: `4b33d83`, preserved in [FACTCHECK_LOG](FACTCHECK_LOG.md). The pilot's structure and existing chart model were retained by the preceding workers.
- [Review PDF](/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf): all six pages opened as renders and extracted text. SHA-256 `b5dd287088d00fac765f56d9f76f88c5bcd0de74369abe85117e62915c294247`. Page/pin anchors describe **this snapshot**, not uncaptured proposals.
- Later blocked paper review: `2b99ac7bd60d352a4b418cd75e0fc8f66e345b4d`, `docs/evidence/r2/gate4a/`. The numerical screens remain conditional; source trigger, auxiliary construction, reset/re-arm and rated fixture gaps remain open. Later branch work in progress is not silently treated as a reviewed release.
- Connector proposal: `4ff92f3ef68822007642a0e2cbb09b351d043222`, `docs/evidence/r2/J502_SELECTION.md`. Keep proposal versions separate from the inherited voltage-drop allocation and the historical Harwin documentary FAIL.
- The [schematic reading guide](SCHEMATIC_READING_GUIDE.md) lists obsolete PDF labels and their current replacements. “Frozen on paper, not yet in the schematic” describes the later proposal; it does not claim the blocked freeze passed.

## Asset rules

Existing charts, prose, owner notes and every `(still open)` marker are preserved unless a documented factual correction is needed. Existing analogy and realistic illustrations remain filename embeds into the owner's image folder. New such illustrations are **prompts**, not code drawings. Exact simple circuit excerpts are the exception explicitly requested in the owner's final feedback; their runnable matplotlib scripts live in `figures/src/`, with the rendered excerpts in `figures/`. Each excerpt states its omissions and source page. PDF page images are unchanged exports, not generated circuit artwork or annotated evidence. No native KiCad files are changed.

These excerpts adapt the project's own captured connections for teaching; they do not copy a new third-party circuit, PCB, image or code source. Manufacturer references and existing third-party provenance remain in the source register and `third_party/`; no redistribution permission is inferred and no new third-party files are downloaded into the lesson tree.

## Resume coverage

| Item | Disposition |
|---|---|
| 00 | Existing schematic walkthrough, F0.4 prompt and `circuit_00.py` retained from `9be63e7`; PDF pins checked. |
| 01 | Completed PDF page-2 walkthrough, pin-level sensing excerpt and F1.4 companion prompt. |
| 02 | Completed PDF page-3 walkthrough, exact local-feedback excerpt and F2.4 companion prompt. |
| 04 | Completed PDF page-5 force/sense/filter/supply/I2C walkthrough, exact filter excerpt and F4.4 companion prompt. |
| 05 | Completed page-6 connector boundary and full-loop walkthrough, exact J502/J503 excerpt and F5.4 prompt. Explicitly reconciled inherited Phoenix allocation with later J502 PENDING status. |
| 06 | Completed actual bypass/feedback/Kelvin/power-land anchors, two-pair circuit excerpt and F6.4 prompt; no physical layout invented. |
| 07 | Completed staged-test landmarks and real probe/command/current-boundary anchors, voltage-test-net excerpt and F7.4 prompt; uncaptured fixture hooks explicitly distinguished. |
| 08 | Completed external-versus-captured system boundaries, input circuit excerpt and F8.3 prompt; no upstream converter pins or robot ground bonds invented. |
| 03 / 03b | Intentionally skipped; concurrent Claude task. |

This is documentation work, not completion of an engineering gate. R2/R3 and Gate 4a-FIX remain **BLOCKED**. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Git checkpoint limitation

The lesson-01 checkpoint attempted `git add` followed by `git commit`. Git refused to create `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-illustrations/index.lock` with **Operation not permitted**. Per the resume brief, all continuation changes are left uncommitted for the conductor. No permission workaround, index deletion or push is attempted. The deadline does not override this explicit fallback.
