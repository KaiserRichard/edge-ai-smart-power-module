# V1A fabrication export script

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Run from this checkout with an absent or empty output directory:

```sh
scripts/export_fab_package.sh hardware/kicad/V1A.kicad_pcb /tmp/v1a-fab-review
```

The wrapper uses the installed KiCad 9 CLI at
`/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`, KiCad's bundled Python
3.9 (`pcbnew` plus standard library), and the installed `/usr/bin/swift` with
macOS CoreGraphics/ImageIO. It installs nothing and makes no network calls.
Swift's temporary module cache is kept outside the repository and removed.
Spaces in input/output paths are supported. Nonempty output directories are
rejected; incomplete runs retain `STATUS.txt` and command logs for diagnosis.

**DECISION:** successful exit means the requested export operations completed;
it is **not** a DRC pass, correct assembly orientation, or a fabrication release.
The script deliberately permits DRC violation return code 5 so the requested
unplaced-board smoke test can run, and writes those failures into the manifest,
README and zip notice. Other required-command failures stop the export.
Rendering is attempted when the CLI offers it; unavailability/failure is recorded
explicitly. No upload, account login, order, purchase, or push occurs.

## Files and exact conventions

| Output | Convention / source |
|---|---|
| `gerbers/` | Native enabled copper layers, F/B mask, silk, paste, Edge.Cuts; Protel extensions, mm 4.6 precision, X2/net attributes retained, mask subtracted from silk |
| `drill/` | Metric decimal Excellon, separate PTH/NPTH, alternate oval-hole mode, PDF drill maps |
| `assembly/CPL_JLC.csv` | Exactly `Designator,Mid X,Mid Y,Layer,Rotation`; X/Y have `mm` suffix; Top/Bottom; native KiCad positive CCW angle normalized to [0,360) |
| `assembly/BOM_JLC.csv` | Exactly `Comment,Designator,Footprint,LCSC Part #`; one populated reference per row; no procurement quantity/spares column |
| `assembly/POSITIONS_KICAD.csv` | Unmodified native CLI position CSV, retained for audit |
| `assembly/EXCLUDED.csv` | Every footprint excluded by DNP, exclude-from-BOM or exclude-from-position flags, with reason |
| `assembly/ROTATION_REVIEW.csv` | Every exported part's footprint, LCSC code, native angle, applied offset = 0 and OPEN review status |
| `pdf/`, `png/` | One native PDF and 150 dpi white-background PNG per plotted layer, plus F.Fab/B.Fab; bottom views unmirrored |
| `render/PCB_3D.png` | CLI-rendered oblique view when supported; actual saved board, no added outline or placement |
| `*_GERBERS_DRILL_REVIEW_ONLY.zip` | Gerbers, Gerber job metadata, PTH/NPTH drill data and `NOT_FOR_FABRICATION.txt`; maps/assembly/review imagery kept outside |
| `review/`, `logs/` | All-severity DRC with schematic parity when available; fresh schematic XML; exact commands, return codes and logs |
| `MANIFEST.json`, `README.md`, `STATUS.txt` | Input/artifact hashes, actual layer inventory, source differences, counts, export status and OPEN issues |

**DECISION:** use the **absolute origin** consistently for Gerbers, drills and
CPL. No `--use-drill-file-origin` or `--bottom-negate-x`. Native position Y is
preserved; do not invert it again. A regression checks a nonzero auxiliary
origin and a bottom-side part. This follows JLCPCB's
[KiCad 9 Gerber/drill guide](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-9)
(updated 2026-09-24, accessed 2026-10-04) and
[CPL specification](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly)
(updated 2026-09-09, accessed 2026-10-04). Format choices are not a CAM acceptance
claim. Actual layers are exported; a two-layer source never receives fabricated
inner-layer files merely to look like the intended four-layer stack.

The script reads saved zone fills without modifying the source PCB. **OPEN:**
the layout owner must refill/save zones, reconcile schematic parity and review
DRC before final exports. Project/rule/schematic/BOM hashes are checked again
after export; any change during the run fails the package as inconsistent.

## Assembly identity and population

**REQUIREMENT:** LCSC codes come only from
[the frozen procurement CSV](../evidence/r2/BOM_ORDER_LCSC.csv). Each grouped
Designator field is expanded and checked for duplicates; `Quantity` is not used
because it includes three-board procurement and spares. No code is invented
for an unmapped part. Blank codes mean **OPEN sourcing / assembly route**, not
permission for JLC to choose a replacement. No stock or JLC assembly-library
availability is inferred from having an LCSC code.

**DECISION:** Comment uses the freshly exported schematic value when available,
plus the mapped MPN; board value is the fallback without a matching schematic
reference. Footprint and position always come from the actual PCB. Differences
are recorded rather than silently modifying hardware. The current board's
R203 remains **24.4k**, whereas the schematic and authorized selection are
**24.6k**; the BOM Comment therefore uses **24.6k**, with the PCB discrepancy
still visible in `source_comparison` and native schematic-parity DRC.

BOM and CPL contain the same reference set. Both SMT and THT parts are retained
for assembly review. DNP and explicitly excluded footprints appear only in
`EXCLUDED.csv`. Mechanical force links, test interfaces and THT/manual work
must be checked against the intended assembly service; this script does not
silently choose a service or convert them into SMT placements. The format
follows JLCPCB's [BOM specification](https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly)
(updated 2026-09-09, accessed 2026-10-04).

## JLC rotation and centroid issues — OPEN

No family-wide correction is presumed. `Rotation` is the native KiCad angle
modulo 360, with **zero verified JLC offsets**. A zero offset in the review table
means no transformation was applied, not that zero has been qualified.

- **OPEN:** each LCSC/JLC library part's zero-angle convention, reel orientation
  and pin-1 definition versus the exact KiCad footprint.
- **OPEN:** diodes/TVS cathode or bidirectional marking; polarized electrolytic/
  polymer capacitors; MOSFET gate/source/drain; QFN/MSOP and all asymmetric ICs.
- **OPEN:** custom `V1A_Qualified` footprints, shunt Kelvin pin numbering,
  connector pin 1 and through-hole insertion orientation.
- **OPEN:** footprint origin versus physical package centroid, especially custom
  footprints, asymmetric connectors, force links and manual assembly parts.
- **OPEN:** bottom-side library mirroring/rotation interpretation; native CSV
  conversion is tested, but JLC's per-part library match is not.

Resolve against manufacturer package drawings and the exact assembly-library
record during a separately authorized assembly review. Do not assign blanket
90/180/270° offsets without per-part evidence. No upload or login was performed
for this task, so JLC's placement preview has not been checked.

## Verification and present limitations

[EXPORT_CHECK.json](../evidence/r4/fabprep/EXPORT_CHECK.json) records the full
current-board smoke test and a separate synthetic four-layer regression.
[HANDOFF.md](../evidence/r4/fabprep/HANDOFF.md) lists commands, outcomes and files.
Native rule-boundary checks are documented in [FAB_RULES.md](FAB_RULES.md).

**OBSERVATION:** current V1A is an origin pile, so full-page layer plots clip
unplaced footprints at the page edge and the 3D image shows overlapping parts.
KiCad may synthesize a display substrate when the board has no outline; that
rectangle is not an Edge.Cuts design. The generated visuals prove rendering
only and cannot support placement, assembly, mechanical or fabrication review.
An independent CAM/Gerber visual review of a completed layout remains **OPEN**.
