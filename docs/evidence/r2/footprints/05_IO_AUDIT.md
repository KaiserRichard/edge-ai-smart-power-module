# Sheet 05 — preliminary footprint audit, 2026-09-29

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

OBSERVATION: all seven physical symbols initially had blank footprint fields. J501–J503 have no decided MPN and already display `MPN OPEN` in their values. They remain blank and **OPEN**; no connector, mate, wire, current rating, mounting style, or pinout has been selected here.

DECISION: TP501–TP504 are fabricated bare copper probe pads, not purchased test-point components. Assign standard `TestPoint:TestPoint_Pad_D1.5mm`: one circular 1.5 mm copper pad, pad number 1, front copper and mask only, no paste. This is a preliminary physical test-access choice within footprint assignment scope. MPN/package datasheet is not applicable to fabricated copper. Pad-to-symbol mapping is 1 → 1. Placement/access, probe clearance, and voltage spacing need R3 review. Existing schematic BOM flags are preserved; a later assembly BOM must distinguish these copper features from purchased parts.

| Ref | MPN | Package | Footprint | Pin-map checked yes/no | Source |
| --- | --- | --- | --- | --- | --- |
| J501 | OPEN | OPEN | OPEN — blank | no — MPN and mating pinout undecided | Existing `DC INPUT - MPN OPEN` schematic value |
| J502 | OPEN | OPEN | OPEN — blank | no — MPN and mating pinout undecided | Existing `LOAD OUTPUT - MPN OPEN` schematic value |
| J503 | OPEN | OPEN | OPEN — blank | no — MPN and mating pinout undecided | Existing `HOST I2C - MPN OPEN` schematic value |
| TP501 | N/A — copper feature | 1.5 mm round copper test pad | TestPoint:TestPoint_Pad_D1.5mm | yes — symbol 1 to pad 1 | [KiCad pinned pad](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/f64dbd713b8e5c0f6d8638d6794cda5938b3c7e7/TestPoint.pretty/TestPoint_Pad_D1.5mm.kicad_mod) |
| TP502 | N/A — copper feature | 1.5 mm round copper test pad | TestPoint:TestPoint_Pad_D1.5mm | yes — symbol 1 to pad 1 | Same pinned KiCad pad |
| TP503 | N/A — copper feature | 1.5 mm round copper test pad | TestPoint:TestPoint_Pad_D1.5mm | yes — symbol 1 to pad 1 | Same pinned KiCad pad |
| TP504 | N/A — copper feature | 1.5 mm round copper test pad | TestPoint:TestPoint_Pad_D1.5mm | yes — symbol 1 to pad 1 | Same pinned KiCad pad |

EVIDENCE: installed footprint exactly matches upstream KiCad library tag 9.0.6, commit `f64dbd713b8e5c0f6d8638d6794cda5938b3c7e7`, SHA-256 `b863253216b04db5519fae21af9390e330c8fc62dee105cab1cf015166eeb2fd`. Source file `TestPoint.pretty/TestPoint_Pad_D1.5mm.kicad_mod`; referenced unmodified by library identifier. No custom footprint for this sheet. Source download is isolated under ignored `third_party/documents/footprint_library_refs/`; [library source register](kicad_library_sources.json) records reproducible identity.

PROVENANCE: KiCad Library Team, [CC BY-SA 4.0 with KiCad design exception](https://www.kicad.org/libraries/license/). Use in a board design has the published attribution/share-alike exception; redistribution as a library collection must retain attribution and license. No library collection is added to this project.

RESULT: 4 new assignments, 3 blank OPEN connector footprints, no identified mismatch among existing assignments (there were none). Power flags `#FLG501–503` are schematic annotations and require no physical footprint.
