# C1–C3 pinout check

**Date:** 2026-10-03  
**Reviewed baseline:** `838a8a4`, branch `feat/r2-testboard-capture` (PR #21).  
**STATUS: PASS for these pinout items.**  
**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Results

| Item | Result | Evidence and action |
| --- | --- | --- |
| C1 — U101 TPS26630 MODE | PASS, prior verification accepted | The task brief records Claude's verification: MODE open selects latch-off, matching the freeze; TI TPS26630 datasheet **p. 8**. Existing netlist has U101 pin 11 MODE explicitly unconnected. No change; no new TI retrieval or independent datasheet review in this check. |
| C2 — U316 LT4363HMS-1#PBF | **PASS, independently checked** | ADI LT4363 **Rev. C, p. 2**, upper MS-package diagram for **LT4363-1**, matches all 12 captured pins. Ordering information **p. 3** identifies the selected MPN as 12-lead MSOP. Pin functions **p. 8** confirm OV applies only to LT4363-2 and permit unused UV to connect to VCC. No change. |
| C3 — U318 TPS70933 EN | PASS, prior verification accepted | The task brief records Claude's verification: EN may float to enable; TI TPS709 datasheet **p. 3**. Existing netlist has U318 pin 3 EN explicitly unconnected. No change; no new TI retrieval or independent datasheet review in this check. |

## C2 evidence

**EVIDENCE:** [ADI LT4363 datasheet, Rev. C](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf), printed pp. 2, 3 and 8. The manufacturer's 24-page PDF was read through the web tool. Direct local-download attempts failed; no local PDF download or hash is claimed. [Source provenance](../../../../third_party/check_c1c3/SOURCE.md) records that limitation.

| MSOP pin | Datasheet LT4363-1 name | Captured connection |
| --- | --- | --- |
| 1 | FB | AUX_FB |
| 2 | OUT | AUX_LIMITED |
| 3 | SNS | AUX_SNS |
| 4 | GATE | AUX_GATE_DRIVE |
| 5 | VCC | AUX_RAW |
| 6 | SHDN | AUX_RAW |
| 7 | GND | GND |
| 8 | UV | AUX_RAW, same net as VCC |
| 9 | GND | GND |
| 10 | FLT | Explicit no-connect |
| 11 | ENOUT | AUX_RUN |
| 12 | TMR | AUX_TMR |

**OBSERVATION:** this mapping agrees in `hardware/kicad/V1A.kicad_sym`, the embedded symbol in `03_OUTPUT_PROTECTION.kicad_sch`, `output_block.json`, and `captured.xml`.

**DECISION:** retain the capture. The recollection of 7 = UV / 8 = OV is refuted: the selected **-1** variant has 7 = GND / 8 = UV / 9 = GND; the **-2** MSOP has 7 = OV / 8 = UV / 9 = GND (p. 2). No OV divider is applicable to U316. UV remains connected to VCC as allowed on p. 8; FLT remains as designed.

The Gate 4a auxiliary notes were inspected at local remote-tracking commit `898759e45578f3767721d19eb313312b7d7733a9` (`origin/feat/r2-testboard-freeze`), including `AUX_BRANCH_FIX.md` and the related freeze/fix references. This check introduces no threshold or component changes.

## Validation and changes

**EVIDENCE:** `python3 -B -m unittest discover -s tests -v` — **50 tests passed**, 13.858 s. `python3 -B scripts/check_r2_schematic.py --netlist docs/evidence/r2/gate4b/captured.xml` — **PASS**.

`python3 -B scripts/check_repository.py` — **PASS**, 32 hardware files verified, no errors. `git diff --check` — **PASS**.

**OBSERVATION:** no changes to hardware, `captured.xml`, or `V1A_GATE4B_REVIEW.pdf` relative to `838a8a4`. The brief requires ERC and re-export if C2 needs a correction; that condition was not met. ERC was not rerun and exports were not regenerated. Existing ERC evidence remains historical.

Changes are limited to this report, the source provenance record and a manager-report addendum. **OPEN RISK:** this pinout PASS does not validate electrical performance; R2 electrical release remains BLOCKED.

**Git handback:** the local commit attempt stopped at `git add`: Git could not create `/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-gate4b/index.lock` (`Operation not permitted`). Per the brief, changes remain uncommitted. No lock or permission changes were attempted; nothing was pushed.

C2: PASS
C1C3-HANDBACK
