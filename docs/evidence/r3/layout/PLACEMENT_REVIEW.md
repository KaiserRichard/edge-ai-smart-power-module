# V1A placement study — step 2

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**DECISION:** resume `ad04d28`, retaining the completed R203 synchronization and four-layer choice. No schematic, component value or upstream footprint was changed. The owner's 2026-10-04 authorization permits this R3 study while R2 remains BLOCKED.

## Envelope

**ASSUMED:** 230 × 195 mm, four layers, outer 70 µm / inner 35 µm copper, preliminary 1.6 mm board. This is 25.50% less area than the inherited 280 × 215 mm study. A 220 × 170 mm placement trial crowded the 31 × 16 mm force-link courtyards, Phoenix output assembly, bulk capacitors and auxiliary/control clusters. The selected envelope is the smallest completed placement trial with these clusters and accessible perimeter controls; it is not a mathematical global optimum or a frozen mechanical requirement. Further compaction would require another placement/routing review. The 36 × 35.7 mm inductor and large removable links dominate the power region. Its 34.2 mm height and the mate/bolt/tool envelopes still need physical checking.

**DECISION:** keep the principal force chain on the upper half, raw bank and matched dump strings above it, protected bank and dump below its output, auxiliary power below the input, references below the discharge region, and manual logic along the lower edge. J501 faces the left edge; J502 and J503 face the right edge; manual controls face the bottom. Four board-only 3.2 mm mounting holes are preliminary fixture features, excluded from the schematic/BOM.

**EVIDENCE:** `PLACEMENT.json` records every electrical footprint position and rotation. The board retains all 366 electrical references and original pad nets. `STEP2_DRC.json` includes native schematic parity. All high-current links remain separate nets; the shunt's force pads and sense pads remain distinct.

## Critical clusters

- Input: F101/D101, Q101/Q102/U101 and its settings sit together. JP101 and downstream D102 remain separate. The auxiliary branch leaves VIN_FUSED through D303.
- Buck: C203/C204 flank U201's two VIN/PGND pairs, C201/C202 behind them. Bootstrap returns to native BUCK_SW. Feedback is on the quiet side. JP201, L201 and JP202 retain their captured test boundaries.
- Output: Q301/Q302 face their sources toward each other; U301, bootstrap, gate and supply parts are adjacent. Raw and protected discharge strings are separate from the monitor. No claim is made that their pulse loops are qualified.
- Auxiliary: separate U316, U317, U327 and regulator clusters. U317's FE pin map is preserved. Missing/undersized local bypass issues already recorded in the guide remain OPEN.
- Monitor: R401 sits between JP301 and J502 with INA228 and its input filter above it. R401 pads 2/3 are sense only. The host-side I2C interface sits by J503.
- Logic: each captured bypass is assigned to its corresponding IC. Test pads are placed by their observed circuit, not used as force conductors.

## Native pad gaps

**OBSERVATION:** Q101, U302, U306, U600 and U403 contain adjacent native lands with 0.150 mm gaps, smaller than the project's provisional 0.200 mm global clearance. These existed before placement. The library land patterns and their source/pin audits are retained unchanged.

**DECISION:** `V1A.kicad_dru` defines a 0.150 mm exception only between pads within the same one of those five footprints. It does not relax track, via, zone, inter-footprint or other package clearance. No DRC severity is disabled. **OPEN:** the fabricator must confirm this geometry with the assumed heavy outer copper; no creepage, insulation or fabrication qualification is claimed.

## Review limits

**OPEN:** force-link fastener and strap inductance; washer and screwdriver envelopes; probe access with actual instruments; maximum transient voltage and insulation basis; hot copper and contact resistance; thermal coupling and airflow; driver/held-rail local capacitor discrepancies; reference and sensing accuracy; actual return-current distribution; all electrical bring-up gates. R4 remains blocked.
