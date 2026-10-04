# Partial-commit preservation audit

PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION

**EVIDENCE:** `git show --stat b640c2c` was checked before continued editing. The 13,615 deleted lines are regenerated Sheet 01/02 content and replaced library entries, largely compact S-expression serialization. [Machine audit](RESUME_AUDIT.json) compares PR15 `51d1c2f` with the partial commit using the native symbol tree and a fresh KiCad XML export.

- No existing physical reference or library reference was removed. All 14 existing project footprint files remain byte-identical. Sheet 03/04/05 and the root project remain unchanged in the partial commit.
- Sheet 01 changes match S01-01…06: fuse/TVS/commutation diode, passive MPNs and the 0805 R103. D102 terminal numbering changes because the two-pin B260 was intentionally replaced by dual-anode STPS60H100CT.
- Sheet 02 changes match S02-01…06: 10 µH L201, 10 µF input ceramics, exact passives, and JP201/TP201…203. L201.1 intentionally moves from BUCK_SW to L201_IN; JP201 is the removable force connection. C209…214 and their PR15 TDK lands are intact.
- Other physical pin/net assignments, all hierarchical ports, and all Sheet 03/04/05 library definitions are preserved. Graphics/placement of Sheet 01/02 were regenerated as functional groups with named connections; prior connected-wire presentation and notes remain recoverable at PR15, not deleted from history. New notes supersede the old requirements and identify OPEN qualifications.

**DECISION:** no lost circuit or footprint requires restoration. Resume the existing capture; do not restart it. Later freeze-directed retirement of Sheet 03 logic must be separately enumerated.
