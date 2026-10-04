# V1A 5 A path checker

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**STATUS: CONDITIONAL PASS for the calculation tool; the current PCB path is OPEN.**
No electrical gate advances. No hardware file was changed. Work follows the
2026-10-04 `v1a-lab/briefs/PATH_CHECK.md` on `feat/v1a-path-check`, based on
`5f371fd`, without installations or sub-agents.

## Usage

From the repository root, with Python 3.9 or newer and no additional packages:

```sh
python3 scripts/check_5a_path.py hardware/kicad/V1A.kicad_pcb
python3 scripts/check_5a_path.py /path/to/routed/V1A.kicad_pcb --copper-um-outer 70 --copper-um-inner 35 --temp-c 85
python3 scripts/check_5a_path.py hardware/kicad/V1A.kicad_pcb --json
python3 -m unittest discover -s tests -p test_check_5a_path.py -v
```

The PCB is opened read-only; it is never saved, filled, or changed. A board from
the layout worker can be checked by passing its path. The frozen allocation JSON
is located relative to the script, so execution does not depend on the working
directory. `--json` emits endpoint paths, itemized allocations, material settings,
source/board hashes, and individual trace estimates as well as summary results.

| Option | Default | Meaning / classification |
|---|---:|---|
| `--copper-um-outer` | 70 | ASSUMED finished F.Cu/B.Cu copper thickness, µm |
| `--copper-um-inner` | 35 | ASSUMED finished internal copper thickness, µm |
| `--temp-c` | 85 | ASSUMED operating **copper** temperature, °C; not ambient |
| `--via-plating-um` | 25 | ASSUMED barrel wall plating, µm; obtain fabrication minimum |
| `--zone-grid-mm` | 1 | ASSUMED polygon routing search resolution, mm |
| `--zone-width-cap-mm` | 1 | ASSUMED maximum credited zone corridor width, mm |

Thickness arguments explicitly control the calculation; copper values in a board
stackup do not silently override them. Board thickness comes from `(general
(thickness ...))`. Missing board thickness gives OPEN. Non-finite, zero, or
negative dimensions are rejected. The temperature screening range is −50–200°C.

Exit **0** means **CONDITIONAL PASS within the stated model**. Exit **1** means
FAIL (voltage below 4.75 V, or either copper allocation exceeded), OPEN (unrouted,
missing endpoints, unsupported relevant geometry, incomplete input), or a handled
input/file error. Normal argparse usage errors return 2. OPEN quantities are
printed as OPEN and encoded as JSON `null`, never zero resistance or a fabricated
Pi voltage.

## Frozen budget and physical endpoints

**EVIDENCE:** [R203 option A](../evidence/r2/R203_OPTION_A.md) and its
[CALCULATIONS.json](../evidence/r2/r203_option_a/CALCULATIONS.json) remain unchanged.
The script loads the full-precision JSON, verifies its itemized sum, and uses:

- hot-case buck minimum: **4.993320972112401 V**;
- load: **5 A**; Pi minimum: **4.75 V**; negative trough: **20 mV**;
- frozen loop: **41.85554624343832 mΩ**;
- copper rows `unsensed_buck_copper` (0.5 + 0.5 mΩ) and `module_PCB`
  (1.0 + 1.0 mΩ): **1.5 mΩ send + 1.5 mΩ return**;
- retained non-copper allocations: **38.85554624343832 mΩ**.

**DECISION:** replace the two frozen copper rows with computed PCB copper,
including traces, via/plated-hole barrels, pad spreading, and filled zones. Keep
every other row once: FET pair 13.6 mΩ, shunt 2.0237875 mΩ, J502 poles, trunk,
fanout, Pi contacts/attachment, splices, and module solder joints. No double
counting of the original 3 mΩ copper allowance. Check send and return separately,
so unused return allowance cannot conceal excessive send resistance.

The present Gate4B pin contracts include intermediate nets and a removable force
link. The checker uses these actual endpoints:

| Side | Copper net | From | To |
|---|---|---|---|
| Send | `VOUT_5V1` | C209–C214 pin 1 | Q301 pins 5–8, including duplicate physical pad 5 |
| Send | `PROT_MID` | Q301 pins 1–3 | Q302 pins 1–3 |
| Send | `SERIES_OUT` | Q302 pins 5–8 | JP301 pin 1 |
| Send | `VOUT_PROTECTED` | JP301 pin 2 | R401 force pin 1 |
| Send | `LOAD_5V1` | R401 force pin 4 | J502 pin 1 |
| Return | `GND` | J502 pin 2 | C209–C214 pin 2 |

**OBSERVATION:** this J502 is a two-pole connector with one board pin per pole;
the multi-pin Pi fanout lives in the retained off-board allocation. R401 Kelvin
sense pins 2/3 never substitute for its force pins. Missing or wrong-net required
pins give OPEN. Every physical endpoint must reach the opposite endpoint group.
Each net uses the largest of these single-terminal shortest-path resistances;
this avoids granting a low-resistance result from only the nearest capacitor or
one connected MOSFET pad. Independent worst cases are added, conservatively.

**ASSUMPTION / OPEN RISK:** FETs are enabled and JP301 is fitted. The frozen JSON
does not separately allocate JP301 bulk/contact resistance; the checker does not
invent one or borrow the later force-link screening value. Therefore even a
numerical CONDITIONAL PASS requires review of that omitted installed link.
The modeled boundary is the buck output capacitor bank, not L201, JP202, the
switching loop, or an assertion of actual regulator performance.

## Resistance and connectivity model

**CALCULATED:** use `R = ρ(T) L / A`, with all inputs converted to SI units:

```text
ρ(T) = 1.724e-8 × [1 + 0.00393 × (T − 20)] Ω m
A_trace = width_mm × 1e-3 × thickness_um × 1e-6 m²
A_barrel = π × (finished_bore_m + plating_m) × plating_m m²
R_loop_mΩ = R_send_copper + R_return_copper + 38.85554624343832
drop_mV = 5 × R_loop_mΩ
VPi_min = 4.993320972112401 − drop_mV / 1000 − 0.020 V
margin_mV = 1000 × (VPi_min − 4.75)
```

**ASSUMED:** copper material constants are rounded annealed-copper reference
values, not measurements of the fabricated foil. See
[source provenance](../../third_party/path_check/SOURCES.md).
At 85°C, the resistivity multiplier is 1.25545. A 10 mm × 1 mm × 70 µm trace is
2.462857 mΩ at 20°C and 3.091423 mΩ at 85°C. Substituting the original 3 mΩ copper
budget reproduces 4.764043241 V and +14.043241 mV.

The plain Python S-expression reader handles quoted UTF-8 strings, footprint
transforms, standard lands, the V1A shunt's custom polygon lands, straight tracks,
arcs, through vias, and saved filled polygons. Each node belongs to one net and
one copper layer. Same-net centerline intersections and T junctions split tracks
before resistance is summed. Different layers require a real via or plated hole.
Different nets never connect just because their coordinates coincide. Hierarchical
net suffix collisions produce OPEN.

Arc resistance uses true arc length. Chords of at most 5° are used for graph
geometry, with twice the sagitta subtracted from the modeled trace width.
Through-via/plated-hole resistance uses board thickness and the annular barrel
cross-section. Without dielectric layer depths, every adjacent copper-layer hop
is charged the **full** board thickness. This intentionally overestimates
multi-layer hops and gives no parallel-via credit. Blind/buried/microvia depth,
slotted holes, offset drills, and custom/removed-layer padstacks give OPEN.

**ASSUMED pad approximation:** land spreading is a finite-resistance strip from
the terminal center to an interior connection. Standard pad width uses the
smaller dimension; custom pad width uses twice the anchor-to-outline clearance.
Plated pads are limited to half the difference between land width and bore.
This is a lumped approximation, not a solved spreading-resistance field. Circular
corners use an inscribed polygon. Concave-pad cutouts cannot be crossed. A contact
exactly on a pad outline can remain unresolved and needs review.

## Conservative zone shortest-path width approximation

**ASSUMED / CALCULATED:** only saved `filled_polygon` copper is conductive.
An unfilled zone outline has no conductive area and is flagged OPEN. Polygon
holes, slots and disconnected islands are retained; a bounding box is never
treated as a plane. Refill and save in KiCad before checking a routed board:
the checker cannot establish whether a stored fill is stale.

For each polygon, the graph contains an eight-neighbor interior grid, existing
terminals, and direct visible terminal pairs. Each candidate straight edge must
lie inside copper. Its width is:

```text
effective_width = min(zone_width_cap,
                      2 × minimum distance from the entire edge to polygon boundaries)
```

An edge intersecting any boundary or hole is rejected. The resulting finite-width
strip is charged `ρL/(width × thickness)`. Dijkstra selects the shortest path by
**resistance**, and the strips along it are added. Pads may attach to interior grid
points within their actual land, allowing filled thermal spokes to participate.
No equipotential zone, parallel-route, or heat-spreading credit is taken. This
restricted-copper model aims to overestimate copper resistance; discretization,
pad injection and current crowding prevent treating it as a rigorous bound on a
manufactured board.

**OPEN RISK:** a coarse grid may miss a narrow or oblique thermal spoke. A path
can remain OPEN even when KiCad shows continuity; try a smaller `--zone-grid-mm`
and inspect the reported strips. A small width cap can produce a conservative
FAIL for a broad plane. Increasing the cap requires reviewing actual bottlenecks.
The grid is limited to 40,000 candidate nodes per polygon; exceeding this emits
OPEN rather than silently dropping the zone. Copper is never invented to bridge
an island, void, or unrouted gap.

## Temperature rise screen

**CALCULATED / ASSUMED:** report every trace/arc on the six path nets at a
hypothetical full 5 A, including branches which may carry less in service:

```text
A_mil² = width_mm × thickness_um / 1000 / 0.0254²
ΔT_screen = [5 / (0.024 × A_mil²^0.725)]^(1/0.44) °C
```

This is an **IPC-2152-style conservative screening workflow using the legacy
IPC-2221 internal-conductor envelope**, applied to **both outer and inner**
traces. It is not an implementation of the IPC-2152 chart dataset or a claim of
compliance. TI SNVA766 Eq. 3 provides the legacy coefficients; Jouppi's IPC paper
explains the conservative envelope and the dependence on board construction.
No plane or airflow cooling correction is assumed. Sources and exact revisions
are in the [provenance register](../../third_party/path_check/SOURCES.md).

`--temp-c` sets resistance at the assumed copper temperature; the reported rise
is a separate screening result above local board temperature. It is **not** added
again to an already assumed hot copper temperature. If the user means 85°C
ambient, a hotter resistance case is needed. Installed cooling, mutual heating,
current sharing, maximum allowable rise, and thermal equilibrium remain OPEN.
No thermal acceptance threshold was invented, and no via/zone temperature is
claimed from a trace-only correlation. Very large estimates indicate a severe
screening failure, not a physically valid prediction beyond material limits.

## Evidence and limits

**EVIDENCE:** [42 tests pass](../evidence/r3/path_check/VERIFICATION.json), covering
SI-unit resistance, temperature/thickness scaling, via barrels, thermal equation
inversion, frozen allocation accounting, voltage and copper failures, both layer
and net isolation, branch/T-junction handling, arcs, plated lands, footprint
rotation, custom force pads, missing Kelvin/force endpoints, zone bottlenecks,
slots, linked holes, islands, unfilled zones, CLI errors, and the current board.

The installed KiCad 9.0.6 `pcbnew` independently matched **48 pad coordinates**
for Q301/R401/J502 at 0°, 37°, 90° and 180°, including front/back placement, using
only temporary copies. It emitted a nonfatal wxApp diagnostic; comparison and
process exit both passed. This extra check is not a runtime dependency.

**OBSERVATION:** the current board has no routed path. Its
[saved report](../evidence/r3/path_check/UNROUTED.json) shows all six legs OPEN,
total/drop/voltage/margin `null`, and no trace temperature estimate. CLI exit is
**1**, with no stderr or crash. The board's SHA-256 before and after is:

```text
afaf15d9a55527c0457ce71e8437885e8dcbec3c4d640029befbc5c40c94b59a
```

**OPEN RISKS:** this is a screening tool, not a copper-field solver, DRC engine,
short-circuit detector, or electrical validation. Pad/trace edge-only overlaps,
trace contacts solely inside a zone with both endpoints outside, and narrow
off-grid contacts may be unresolved. Unknown/non-modeled copper primitives get
no connectivity credit. Saved fills must respect outline, clearances, thermal
settings, and net assignments through independent KiCad review. Actual minimum
copper/plating thickness, hot contacts, FET gate drive, force-link assembly,
regulation, ripple and transient/fault behavior still require engineering review
and the established current-limited dummy-load bring-up. The expensive SBC is
not the first load.

**DECISION:** no ERC/DRC rerun was required because no schematic or PCB changed.
R2 electrical release and R3 layout release remain BLOCKED. Next, use the tool
on a reviewed, filled and saved layout; inspect its path breakdown and resolve
the inherited electrical risks before any fabrication decision.

**Git handback:** local commit attempts after implementation, tests and
documentation failed at `git add`: Git could not create
`/Users/quockaiser/Desktop/Research/edge-ai-smart-power-module/.git/worktrees/wt-pathcheck/index.lock`
(`Operation not permitted`, exit 128). Per the task's explicit fallback, all work
remains uncommitted. See [attempt log](../evidence/r3/path_check/GIT_ATTEMPTS.log).
Nothing was pushed; no lock or permission changes were attempted.
