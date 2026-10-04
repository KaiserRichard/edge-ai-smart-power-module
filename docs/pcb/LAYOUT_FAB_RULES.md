# Layout-owned fabrication rules

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**EVIDENCE:** `hardware/kicad/V1A.kicad_dru` implements the supplied fabprep
constraints with the same predicates and order, under layout-owned names.
`scripts/check_layout_fab_contract.py` compares the two files read-only.
The supplied reference is
`/Users/quockaiser/Desktop/Research/wt-fabprep/hardware/kicad/V1A.kicad_dru`;
its rationale is that worktree's `docs/pcb/FAB_RULES.md`.

**DECISION:** retain 0.20 mm track/clearance floors, ordinary 0.60/0.30 mm
vias with 0.15 mm radial rings, 0.254 mm component PTH radial rings,
0.45 mm pad/mixed and 0.20 mm via/via drill separation, 0.50 mm edge
clearance, 0.15 mm legend clearance, and 0.20/0.35 mm ordinary/PTH
hole-to-copper clearance. The later 0.25 mm normal-input and 0.64 mm
surge/boosted-domain screens remain active on all layers. Both A/B net
orderings are covered. No package waiver or severity suppression is present.
These rules are **at least as strict as the supplied limits**; this is a
rule-contract statement, not a board compliance statement.

**ASSUMED:** four layers, 70/35/35/70 µm copper, 1.6 mm board, uncoated
surfaces at no more than 3050 m altitude. Finished copper, stack,
plating, assembly and electrical exposure still need review.

**OPEN / BLOCKING M1-5:** the qualified packages contain pad gaps smaller
than these screens. Native DRC reports such conflicts even without any
tracks or pours. Rotation or translation cannot change an internal land
gap. The owner's M1 review prohibits shrinking lands or suppressing rules.
Closure therefore needs an approved net-pair voltage/spacing disposition or
approved package/protection change from engineering and the fab-rule owner.
Until then, retain the errors and do not claim DRC PASS.

Source attribution and the read-only helper revisions are recorded in
`third_party/pcb_layout/SOURCES.md`; the manufacturer's rule basis is the
supplied fabprep document. No upstream source or helper is modified.
