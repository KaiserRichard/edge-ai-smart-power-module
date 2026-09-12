# R2 recovery and design-basis reconciliation

Date: 2026-09-12. OBSERVATION: HEAD is `a9fe716`; the only committed files are
AGENTS.md and README.md. Original branch: `docs/r0-r1-engineering-audit`.
Work continues on `feat/r2-schematic-recovery`, without commits or pushes.

## Previous state

- Modified tracked files: AGENTS.md and README.md. Untracked: .gitignore,
  docs/, scripts/, selected third_party/ sources and pcb-r0-r1-review.zip.
- hardware/kicad/ and tests/ contain no authored files. No authored schematic,
  project, PCB, ERC, PDF export, R2 review or manager packet exists.
- scripts/build_r2_schematic.py is an unfinished generator requiring five JSON
  blocks; only buck_block.json exists. It has not produced a local project.
- buck_block.json contains 25 components, LM61460AANRJRR, 6.8 uH and capacitor
  selections. Its referenced BUCK_DESIGN.md is missing. Its status is an
  unsupported block-level claim, not completed R2 evidence.
- third_party/review/r2/ contains manufacturer text and selected page renders;
  third_party/documents/r2/ contains additional PDFs and failed download bodies.
  Third-party KiCad files, PCB files and PDFs are references, not V1A work.
- tmp/ contains older R0 review artifacts. No hidden R2 implementation was found.

[recovery_manifest.json](recovery_manifest.json) records pre-edit hashes and
sizes. [recovery_originals.json](recovery_originals.json) preserves the exact
unfinished generator and buck specification. Other pre-existing documents are
retained with dated addenda; upstream originals and historical evidence remain.

## Conflicts recorded before circuit changes

| Previous local claim | Current authority / action |
| --- | --- |
| R0/R1 conditional; R2 unauthorized | User explicitly sets R0=PASS, R1=PASS, R2 authorized; R3 blocked |
| TPS56837 leads; 9-24 V and 5.10 V only proposed | Frozen normal input 9-24 V; 36 V-class LM61460 leads; 5.1 V nominal, 5 A, 25.5 W; no 6 A peak rating |
| Monitor and shunt alternatives remain open | INA228 and four-terminal 2 mOhm shunt frozen |
| VIN_BUCK / VOUT_RAW / VOUT_LOAD generator names | Reconcile to VIN_PROTECTED / VOUT_5V1 / LOAD_5V1; retain VOUT_PROTECTED between disconnect and shunt |
| Buck BIAS connected through 10 Ohm to raw output | BIAS absolute maximum is 16 V. A 24 V high-side fault defeats that path; ground BIAS and remove its unused RC branch. Assess additional internal-LDO loss |
| VCC supplies a PGOOD pull-up | TI reserves VCC for internal circuits. Leave buck PGOOD unconnected; input PGOOD still controls buck EN |
| Capacitance budgets expressed as guaranteed minima | Typical manufacturer curves plus tolerances are screening, not guaranteed production bounds; preserve assumptions and flag qualification |

## Scope, risks and rollback

Authorized architecture: fuse/transient/reverse-input/UV-OV/inrush protection →
LM61460 → independent output disconnect → Kelvin shunt → load; INA228 senses
load-side VBUS with a reviewed host power boundary. No architectural expansion.

Affects only R2 capture, R2 evidence/tooling and dated navigation/status addenda.
The principal risk is an unjustified output-protection window and fault
let-through. Capture that boundary **open, with no bypass** if it cannot close.
Unassigned package/part choices must remain conspicuous release blockers.

Rollback is scoped to this session's additions and addenda; restore the two
unfinished R2 files from recovery_originals.json only after checking for later
edits. Never reset or clean the working tree. No rollback was executed.

## Verification plan

Check manufacturer pin diagrams (not PDF extraction order), calculations and
ratings; generate to an empty destination; run KiCad ERC and export a netlist and
PDF. Review every ERC item, compare exported pin-to-net connectivity against
independent invariants, and inspect every schematic page. Confirm no authored
PCB or fabrication artifact appears. ERC success cannot release an electrically
incomplete circuit. R3 remains BLOCKED.
