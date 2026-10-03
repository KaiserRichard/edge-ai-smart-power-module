# Sheet 05 — connectors and test access

2026-10-03. **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

**STATUS: CONDITIONAL PASS for capture; electrical release BLOCKED.** Eleven physical parts and three inherited external-source declarations. No new protection/control circuit is placed on this sheet. [Whole-project ERC after Sheet 05](sheet05_review_erc.json): zero violations.

| Interface | Verified captured map / source |
|---|---|
| J501 | Retained PR15 JST B2P-VH-FB-B(LF)(SN), qualified 3.96 mm land: 1 VIN_RAW, 2 GND. Input requirement corrected to 9–26 V in its metadata. |
| J502 | Phoenix **1776508**, qualified PR15 land; cable mate **1777989**. Contact 1 LOAD_5V1, contact 2 GND, after series protection and shunt. Owner solution A retained from `41cb9e889418d50d2f5f24467e66ac7f15a90476`, `docs/evidence/r2/J502_SELECTION.md`. |
| J503 | Retained JST B4B-XH-A(LF)(SN), qualified 2.50 mm land: 1 GND, 2 host 3.3 V reference, 3 SDA, 4 SCL. Disconnect during first fault tests. No local supply output to the host. |
| JP501 | Removable authored M4 link: 1 LOAD_5V1, 2 LOAD_FIXTURE. Dummy load force takeoff is pad2 with PF5 return. Opening JP501 does not isolate a separately attached J502 load: unplug J502 too. |
| PF1 / PF5 | Authored M4 input/return pads VIN_RAW/GND, completing PF2 VIN_PROTECTED, PF3 BUCK_SW and PF4 L201_IN on Sheet 02. |
| TP501…505 | Sense access only. TP505 is paired LOAD_FIXTURE/GND; its small pads are not the dummy-load force terminals. |

**DECISION:** preserve the power-only Pi harness notes: TE 3-87456-6 housing, ten 87309-9 contacts; Belden 8521 AWG16 trunks, 75 mm maximum; 8502 AWG20 positive 2×15 mm and return 8×35 mm pigtails. Pi physical positive 2/4 and GND 6/9/14/20/25/30/34/39. Those coordinates require a verified mating-face drawing; they do not establish TE cavity numbering. All other power-harness cavities remain empty. Telemetry integration into this occupied housing stays OPEN.

**DATASHEET:** J502 family nominal 12 A is not a hot assembly guarantee. **ASSUMED acceptance:** ≤3.12 mΩ per complete hot pole, plus the selected harness budgets, must be measured. The 5 A mixed-mate/contact-sharing claim remains unqualified.

**OPEN RISKS:** input contact/fuse/wire coordination; bolt torque, plating, copper, contact resistance and fixture parasitics; conditioned hot J502 and Pi current sharing; single-positive-contact loss; indexed housing/tooling/welded fanouts and bend geometry; final telemetry harness; actual Pi input behavior. No Pi before dummy-load/fault/telemetry gates pass. All force connections are changed only with sources isolated and every store verified discharged.

Next: project net classes, complete marked PDF/netlist, freeze coverage and manager handback. No PCB layout or fabrication release.

## Final resume checkpoint — 2026-10-03

**EVIDENCE:** continued `f2e80c2` without additional native Sheet05 edits. J502's exact Phoenix selection, J503's host-reference map, M4 dummy-load path and separate sense pads were rechecked against the connector handoff and export. Fresh [all-severity ERC](sheet05_final_erc.json): zero violations. Native PDF page6 visually reviewed; A2, complete warnings and connector/harness notes present. The 47-test suite includes independent connector-before-protection and native/injection force-pad regressions.

**DECISION:** capture checkpoint conditionally complete. Git's earlier `index.lock` denial invokes the brief's uncommitted fallback. Proceed to the complete freeze/inventory/preservation handback; no PCB, fabrication or Pi authorization follows.

## Second resume checkpoint

**WHAT WAS DONE:** changed the hook annotation to quote the required phrase as **FUTURE ACCEPTANCE REQUIRED**, followed by **UNTESTED CANDIDATE; evidence NOT RUN**. Retained all 11 physical references, Phoenix1776508/1777989 selection, host-reference connector and dummy-load isolation instructions. No connector, pin or power-path change.

**EVIDENCE:** [fresh whole-project ERC](sheet05_resume2_erc.json): zero violations at all severities. Existing package review remains applicable; the final six-page PDF and netlist are regenerated after this checkpoint.

**DECISION:** CONDITIONAL PASS for capture; electrical release BLOCKED. No Pi before prior dummy-load/fault/telemetry gates pass. Current/contact/fixture/harness qualification remains NOT RUN. Next: final reconciliation and manager handback. Git index.lock denial leaves this checkpoint uncommitted under the brief fallback.
