# V1A fabrication rules — 2026-10-04

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**STATUS: CONDITIONAL PASS for rule preparation only.** This is supporting work
for R3/R4, not closure of R2 electrical review, R3 layout or R4 release.
The brief authorizes rules/exports while a separate worker owns layout.
`hardware/kicad/V1A.kicad_pcb` must remain unchanged here.

## Stack and source basis

**REQUIREMENT (brief):** default fabricator JLCPCB; four layers; 1.6 mm finished
thickness. **ASSUMED (layout worker):** F.Cu/In1.Cu/In2.Cu/B.Cu =
70/35/35/70 µm (2/1/1/2 oz). Routed outline, ordinary plated through vias,
no HDI/blind/buried vias, uncoated electrical-spacing basis at altitude ≤3050 m.
Solder mask is not credited as conformal insulation. Exact laminate, dielectric
thicknesses, finish, mask color and production stack identifier remain **OPEN**.
Inner 1 oz must be specified explicitly; JLC's published default is 0.5 oz.

**OBSERVATION:** baseline `5f371fd` has a two-layer, 1.6 mm unplaced import with
366 footprints and no outline, routing or zones. The rules do not change its
stack or turn it into a four-layer board. The layout owner must select the
intended stack and resolve DRC before a release review.

Sources accessed **2026-10-04**, with provenance in
[third_party/fabprep/SOURCES.md](../../third_party/fabprep/SOURCES.md):

- **J1:** [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities),
  live unversioned page, sections Drilling, Traces, Legend and Outline.
- **I1:** [TI SLUP421, clearance/creepage presentation](https://www.ti.com/lit/ml/slup421/slup421.pdf),
  slide 24, identifies IPC-2221B coated/uncoated values.
- **I2:** [Würth Elektronik, Creepage and Clearance of Connector](https://www.we-online.com/files/pdf1/creepage-and-clearance-of-connector.pdf),
  slide 31, reproduces the IPC2221 B1/B2/B3/B4/A5/A6/A7 table.
- **I3:** [IPC-2221B publisher revision record / contents](https://www.ipc.org/TOC/IPC-2221B.pdf),
  December 2012. The complete licensed standard was not obtained; numerical
  evidence is the two manufacturer publications above. This is not an IPC
  certification or a product-safety insulation assessment.
- **K1:** [KiCad 9 PCB Editor custom rules](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#custom-design-rules),
  also checked against the installed 9.0.6 help and native DRC.

## Implemented dimensions

All distances are mm; rings and separations are **edge-to-edge**, not diameters
or center distances. `V1A.kicad_dru` uses KiCad custom-rule syntax version 1.

| Check | J1 published capability | Implemented decision |
|---|---|---|
| Track / different-net copper space | Multilayer 2 oz: 0.15/0.15; 1 oz: 0.09/0.09 | **ASSUMED** 0.20/0.20 on every copper layer; conservative manufacturing floor |
| Via hole / pad | Minimum 0.15/0.25; preferred hole ≥0.20; preferred pad-minus-hole ≥0.15 | **ASSUMED** hole ≥0.30, pad ≥0.60, radial annulus ≥0.15; all three checked |
| Component PTH ring | 2 oz ≥0.254; multilayer 1 oz ≥0.20 recommended, 0.15 absolute | **REQUIREMENT** radial annulus ≥0.254, conservatively all layers; separate from via ring |
| Hole-to-hole | Via/via 0.20; pad/pad 0.45 | **REQUIREMENT** 0.20 via/via; **ASSUMED** 0.45 for pad and mixed pairs |
| Copper-to-edge | Routed 0.20; V-cut 0.40 | **ASSUMED** 0.50; does not authorize panel V-scoring |
| Silk-to-pad | 0.15 | **REQUIREMENT** `silk_clearance` ≥0.15; KiCad checks exposed copper/mask and other silk objects |
| Hole-to-other-net copper | Via 0.20; inner PTH 0.30; outer PTH-to-track 0.28 minimum / 0.35 recommended | **ASSUMED** 0.20 default, 0.35 if either object is a PTH pad |

**CALCULATED:** a 0.60/0.30 via has `(0.60−0.30)/2 = 0.15` radial ring;
a 0.30 hole in a component PTH pad needs at least `0.30+2×0.254 = 0.808`
copper diameter. Increasing the via drill also requires increasing its pad.
A diametral allowance must not be mistaken for a radial annulus.

**DECISION:** preserve the existing project class presets. Every existing class
has 0.20 clearance. HighCurrent's 2.0 mm and Switching's 1.0 mm track settings
are routing presets; this file adds only a manufacturing width floor. It does
not calculate continuous/pulse ampacity, voltage drop, temperature rise,
via current sharing or switching-loop inductance.

**OPEN / checks outside this rule file:** mask dams/openings, same-net gaps,
slotted-hole spacing, hole/slot tool limits, tenting, via filling, paste apertures,
legend stroke/height, thermals and detailed DFM still need review. KiCad's
`hole_to_hole` constraint excludes milled slots and microvias. The ordinary-via
assumption must be checked in the board inventory. A generic copper clearance
rule cannot prove any of these conditions.

## Electrical spacing and actual net names

**CALCULATED:** 26 V belongs to IPC-2221B 16–30 V; 58.1 V belongs to 51–100 V.
For those bands, respectively: internal B1 = 0.05 / 0.10; external uncoated
B2 (≤3050 m) = 0.10 / 0.64; uncoated component leads A6 = 0.25 / 0.50.
The above-altitude B3 requirement becomes 1.50 for 51–100 V.
**ASSUMED:** apply the more conservative external dimensions to inner copper too.
These are conductor potential-difference bands, not net-name ratings.

| Rule group | Calculation / assumption | Minimum |
|---|---|---:|
| Normal input/protected domain | `max(0.20 fab, 0.10 B2, 0.25 A6)` | 0.25 |
| 58 V-class surge domain | `max(0.20 fab, 0.64 B2, 0.50 A6)` | 0.64 |
| Boosted switching nodes | **ASSUMED** >30 and ≤100 V including driver offset/ringing; 31–50 and 51–100 B2 both 0.64 | 0.64 |

**EVIDENCE:** targets were read from a fresh full-project schematic XML export,
not inferred from an old input-protection report. Exact connections and values
are retained in [NET_RULE_TARGETS.json](../evidence/r4/fabprep/NET_RULE_TARGETS.json).
The frozen capture uses **9–26 V and SMCJ36CA**, whose documented 58.1 V clamp
is a specified test point, not a guaranteed installed surge ceiling.
See [current input review](../evidence/r2/gate4b/SHEET01_RESUME2_REVIEW.md) and
[capture risks](../evidence/r2/gate4b/GATE4B_CAPTURE.md).

- **Normal 26 V:** `/VIN_PROTECTED`, `/01_INPUT_PROTECTION/EFUSE_OUT`,
  `/01_INPUT_PROTECTION/INPUT_FLT`, `/02_BUCK_5V/BUCK_SW`, `/L201_IN`,
  `/03_OUTPUT_PROTECTION/AUX_LIMITED`, `/03_OUTPUT_PROTECTION/AUX_SNS`.
- **58 V class:** `/VIN_RAW`, `/VIN_FUSED`,
  `/01_INPUT_PROTECTION/VIN_EFUSE_IN`, `/01_INPUT_PROTECTION/INPUT_BGATE`,
  `/01_INPUT_PROTECTION/INPUT_DRV`, `/03_OUTPUT_PROTECTION/AUX_RAW`,
  `/03_OUTPUT_PROTECTION/AUX_GATE`, `/03_OUTPUT_PROTECTION/AUX_GATE_DRIVE`.
- **Boosted nodes:** `/02_BUCK_5V/BUCK_CBOOT`, `/02_BUCK_5V/BUCK_RBOOT`,
  `/03_OUTPUT_PROTECTION/AUX_BST1`.

**ASSUMED / rationale:** before-fuse VIN_RAW is conservatively screened as
surge-exposed but is not guaranteed clamped by the downstream TVS. D303 connects
VIN_FUSED to AUX_RAW; U316/Q316 gate drive rides on that input, so those nodes
must not be omitted. INPUT_BGATE/DRV also ride above their input. Screening
them in the ≤100 V band accommodates an offset; it does not establish the
actual peak. The buck bootstrap and input-side auxiliary bootstrap can exceed
30 V at a 26 V input even in ordinary operation.

**OPEN RISK:** normal-domain targets assume input/auxiliary protection operates;
let-through, ringing, reverse input, fault combinations and overshoot are not
bounded by this file. A full pairwise worst-case voltage review may promote
other nets (including normally 5 V output paths under a high-side short) into
higher bands. No 58.1 V exposure of the LM61460 is authorized. Low-voltage
sense/divider outputs are not automatically treated as high-voltage inputs.
A >100 V differential, altitude >3050 m, contamination or insulation requirement
invalidates this screen and requires revised rules.

**DECISION:** each rule tests **both A and B** so either object ordering is
covered, and applies to different-net copper including pads/tracks/zones.
The later voltage groups override the 0.20 fab floor; do not reorder them
behind a weaker rule. No footprint or same-package clearance waivers are added.
Fine-pitch U101/U201/U316 pads can violate these conservative clearances;
that is an explicit engineering-review issue, not a reason to suppress DRC.

## If outer copper changes to 1 oz

**DECISION:** this file remains conservative if outer copper becomes 35 µm.
The published multilayer track/space floor becomes 0.09/0.09 instead of
0.15/0.15, and the component PTH ring recommendation becomes 0.20 instead of
0.254. Keep the implemented 0.20 copper floor and existing larger rings unless
a reviewed revision needs the smaller geometry. Electrical 0.25/0.64 screens,
drill/edge/silk limits do not decrease merely because copper is thinner.

**CALCULATED (equal width/length/temperature, neglecting plating differences):**
halving copper thickness approximately doubles DC resistance and I²R loss at
unchanged current. Recalculate power/return widths, pulse capability, via
sharing and thermal performance before accepting 1 oz. Copper weight is not
proof of current capacity. Mask processing/DFM also changes with copper weight.

## Verification

Run the native boundary probes using KiCad's bundled Python:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9 \
  docs/evidence/r4/fabprep/check_rules.py
```

The probes use isolated four-layer fixture boards and check below/above limits,
both net object orders, all copper layers, ordinary and auxiliary surge nets,
boosted nodes, vias/PTHs, drill separation, board edge and silk clearance.
Results and current-board DRC are summarized in
[RULE_CHECK.json](../evidence/r4/fabprep/RULE_CHECK.json).
DRC execution and rule recognition establish software behavior only.
