# Gate 4a basis and checkpoint

Owner decision, 2026-09-30: build an R2 **FAULT-TEST BOARD** using architecture D, a module-side series disconnect with an output absorber/crowbar. Pursue the Gate 3b source contract using timed TPS26630 isolation, total effective local input C of 10–30 µF, and a qualified 10 µH L201 candidate. This freezes a development direction, not a verified source envelope.

The strict Pi-end ceiling `<5.5 V`, normal floor `>=4.75 V at5 A`, GPIO D-30 and normal input9–24 V remain fixed. The real harness is part of the fault test. Negative paper examples stay OPEN for measurement and remain historical blocking evidence for electrical release. A Raspberry Pi is never the initial load and cannot be connected until the applicable dummy-load fault and normal-operation tests pass. No KiCad file is opened or saved by this task.

[Input provenance](INPUT_PROVENANCE.json) pins the Gate3b, path-budget and withstand studies by Git commit and content hash. Cross-branch studies are read with `git show`; no merge is made. Read first: Gate3b report and detailed files, Gate3 architecture study, Gate2c closure, the path-budget report and JSON, input-withstand study and decision log.

Path-budget reconciliation: use D's combined lower-loss FET/harness/contact/copper fix set, retain local regulation and the2 mΩ Kelvin telemetry shunt. Its hot35.072941 mΩ /20 mV-trough Pi4.830779 V numbers are conditional targets, not actual fitted limits. Do not duplicate E's added stage or treat new low-loss FETs as already qualified. Two5 V pins2/4 and all eight grounds6/9/14/20/25/30/34/39 need a connector that reaches the complete40-pin header.

Input-withstand reconciliation: D101 and F101 are **PENDING** the TVS study.27 V is a fault-test condition, outside9–24 V normal operation; it may or may not trigger the inherited input OVP. Its full conditional rising range is26.973873–28.289211 V, not a physical clamp. A bench-source terminal ceiling, current/energy limit and fixture protection must be declared before testing. Neither33.6 V continuous nor67.2 V/1 s is included in Gate4a authorization. An unresolved TVS/fuse pair blocks fabrication and high-energy energization, while footprint/analysis capture can remain reviewable.

Worktree: `wt-gate4a`; branch `feat/r2-testboard-freeze`; draft PR destination `feat/sheet03-output-protection`. No merge. Checkpoint after every finished sub-step. New artifacts remain here; the existing manager report will be updated at closure.

STATUS: Basis reconciled; component capture manifest and test plan in progress.
