# V1A-Lite — independent PCB review R1

2026-10-05 · **STATUS: BLOCKED**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Reviewed detached snapshot `5d4ba5eed2cbe6c5a6549f7fcbbfd1d72ca261ef`. PCB SHA256: `597b30be4ef73be637cd79bbda192d3280ca3ef2999b7fca378f60f1cf37c908`. Coordinates below are **mm, native top view, X right/Y down**; outline is (10,10)–(90,70). CPL Y has the opposite sign. This review changes only this report; no CAD/library edits, gate advancement, commit, upload or order.

EVIDENCE: read the specified layout, harness, bench and C2 notes; inspected saved front/back copper, silk and assembly plots, with coordinate-derived detailed views. Fresh KiCad **9.0.6 DRC**, all severities/all track errors with schematic parity: **0 violations, 0 unconnected, 0 parity issues**. Fresh Gerber/drill exports and calculations were confined to `/private/tmp/litepcbrev-r1/`. These are inspection/calculation results, not electrical validation.

### 1. BLOCKING — J502 positive marking is at the ground end

**OBSERVATION:** J502.1 **VOUT_PI=(84,44)**; J502.2 **GND=(84,47.96)**. The separate silk **“+”=(85,52)** is below the ground end of the connector body, opposite its pin-1 triangle. This can misdirect wiring or first-power probing. J503's exposed pads, positive **(68,61.5)** and ground **(78,61.5)**, have no printed polarity labels.

**Why:** conflicts with the actual pin mapping and [PI_HARNESS.md](PI_HARNESS.md), which requires unambiguous J502 pin-1 identification and continuity before power.

**Exact fix:** delete/move the misplaced plus; print `1 +5V` adjacent to J502.1 and `2 GND` adjacent to J502.2, outside the installed body. Add `+`/`GND` beside J503 and equivalent numbered input labels at J501. Verify the final silk against pad nets and the mating-face drawing, not just the connector outline.

### 2. BLOCKING — bootstrap routing defeats the local bypass placement

**OBSERVATION:** U201=(45,44), C205=(42.5,39.9), R204=(39.8,39.5). U201.13→R204.1 uses **6.857 mm of 0.20 mm track plus two through vias**, at **(44.3,43.25)** and **(39.8,41.5)**; including nominal board thickness gives approximately **10.06 mm** of conductor. Its bottom route crosses beneath the IC/control side and cuts the ground reference. The 0 Ω link is therefore not a local connection between pins 13/14. C205's SW connection is also a narrow 0.20 mm branch. The CBOOT net contains redundant branches; its total track length must not be confused with the shorter 3.48 mm pin-14→capacitor path.

**Why:** [TI LM61460 SNVSBD5D, §11.1, p47](https://www.ti.com/lit/ds/symlink/lm61460.pdf) calls for short, wide bootstrap connections, the SW branch through the VIN2/RBOOT gap, and a local RBOOT link. The present detour adds gate-drive impedance and interrupts shielding; DRC cannot assess the resulting switching behavior.

**Exact fix:** re-place R204 and C205 immediately at pins 13/14, make the 0 Ω link and capacitor connections short on F.Cu, retain the prescribed under-package SW approach, and remove the bottom RBOOT route/vias and redundant branches. Refill and inspect the restored ground beneath U201; recheck DRC and startup/SW ringing in the subsequently authorized prototype.

### 3. BLOCKING — crowbar discharge/return geometry has no qualified pulse bound

**OBSERVATION:** SCR301 K/A/G are **(67,35.5)/(69.54,35.5)/(72.08,35.5)**. C217/C218 positives are **(64,26)/(76,26)**, with roughly 9–11 mm straight-line distances to the anode; C209/C214 are at **(67.5,41)/(67.5,56)**. Raw positive rails toward the bulk capacitors are about 3 mm wide, but there is no comparably direct top-side cathode return: its filled GND island is only **x66.053–67.961, y34.505–36.578**. Power returns through the plated/soldered cathode lead connection into B.Cu. That is a valid connection, but not an established low-inductance pulse loop. Nearby bottom gate routing and the long TP302 keepout further divert return current. R308's ground at **(69.575,38)** joins the plane separately from the cathode.

**Why:** [ST TYN612 DocID7475 Rev11, pp2–5](https://www.st.com/resource/en/datasheet/tyn612.pdf) specifies **50 A/µs** with **IG=2×IGT, rise time ≤100 ns**; its 140 A/10 ms and 98 A²s figures have specified waveform/temperature conditions. No extracted loop inductance or qualified gate/pulse waveform establishes compliance. C2's assumed 10 nH case gives **465 A/µs**, not a measurement. Conversely, extra loop inductance can worsen clamping. TO-220 thermal resistance is 60 K/W to ambient; a conditional 5 A, `(0.85 I + 0.030 I²)` screen gives **5 W**, so indefinite conduction cannot be accepted without effective cutoff/thermal provisions.

**Exact fix:** re-place/orient SCR301 and the nearest raw capacitors for a broad, paired force loop; provide a short cathode-to-capacitor-ground connection and adjacent stitching without the sense-route slot. Return R308 and the gate measurement directly to the cathode separately from force current. Extract/bound the revised loop with package/lead parasitics, both capacitor banks and Q102 cutoff; close gate-rise, di/dt, pulse-energy and recovery limits. Reserve an insulated heatsink envelope if the bounded energy/repetition requires it; the tab is live anode. Do not insert a fuse between the raw bank and SCR, or rely on incidental trace inductance as current limiting. This remains tied to schematic review finding 4 and the remote-overshoot check.

### 4. BLOCKING — the 33 mV nominal margin does not close the 5 A voltage requirement

**EVIDENCE / CALCULATION:** inspected the geometry extractor and resistor solver and reran the **0.1 mm mesh** in temporary files; all six resistance results reproduce exactly. The board hash matches the extracted geometry. For C214 **(67.5,56)** through F301 **(74.2,40.5)** and J502 **(84,44)**, including return:

| Quantity | Independently reproduced result |
| --- | ---: |
| C214→F301.1 positive copper, 20°C | 4.289162 mΩ |
| F301.2→J502.1 copper, 20°C | 0.920815 mΩ |
| C214.2↔J502.2 return, 20°C | 0.632527 mΩ |
| Total, 20°C / assumed 85°C | **5.842504 / 7.334971 mΩ** |
| Nominal Pi voltage with 40 mΩ harness + 9 mΩ fuse | **4.783366 V** |

The claimed **33.366 mV** margin and **0.1834 W** modeled copper loss are arithmetically correct. However, applying the regulator's −1% reference allowance and R202/R203's 0.1% opposing tolerances gives `0.99 × (1 + 99.9/24.6246) = 5.006350 V`, hence **4.724675 V** under that same allocation, before ripple, hot-fuse increase or uncertainty. Basis: TI RevD p6 and the **≥4.75 V** requirement in PI_HARNESS.md. This is a failed allocation screen, not a measured voltage or a proof that the capacitor-injection model bounds actual DC operation.

**Current-density observation:** the main positive bridge near **(69.5,39.65)** narrows to approximately **0.53 mm** around R308's ground via/clearance. An additional mesh run injecting 5 A at L201.2 and sinking at F301.1 routes approximately **3.35 A** through this bridge; local grid-edge density is about **188 A/mm²**. These raster values identify crowding, not an allowable temperature rise. The actual inductor→fuse resistance is **1.834256 mΩ cold**; the capacitor-injection paths must not be presented as the sole DC current distribution. No output shunt exists in Lite.

**Exact fix:** reallocate the complete worst-case voltage budget. With the stated copper/fuse assumptions, harness resistance must already be **<34.935 mΩ** before reserving ripple, hot fuse and uncertainty. Widen the bridge by moving R308/via and clearing a direct L201→F301 corridor, then rerun the DC/current-density extraction. Choose a qualified lower harness/fuse drop, revise regulation/sensing, or revise the operating requirement; increasing setpoint requires rechecking the narrow crowbar trip window. Include copper/plating tolerances and hot joints; validate with the remote dummy load before any Pi.

### 5. BLOCKING — the two-layer thermal case is not established for the selected parts

**OBSERVATION:** Q101/Q102 at **(30,24)/(44,20)** each have nine drain vias, but their bottom drain islands are only about **6×5.4 mm**. They are correctly separate live-drain nets, not GND heat spreaders. At the notes' assumed 90% efficiency and 18 V input, input current is approximately **1.563 A**. The actual IRFR6215's maximum 0.295 Ω cold / 0.58 Ω at 150°C gives **0.721/1.417 W per FET** at that current. The [Infineon 2016-05-31 datasheet, pp1–2](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irfr6215-datasheet-en.pdf) conditions its 50 K/W PCB figure on a 1-inch-square board; neither that figure nor the obsolete IRF9540 calculation qualifies these small islands. Hot turn-off SOA remains open.

U201 **(45,44)** additionally has the inherited **2.417 W** loss screen. Its assumed 50°C ambient/110°C junction screen would require **≤24.8 K/W**, for which no model or measurement is supplied. TI RevD §11.1.1 p48 recommends a four-layer 2/1/1/2 oz implementation; this 2×1 oz board is a substantial unqualified departure, not automatically a failure solely because of layer count.

**Exact fix:** establish ambient/airflow, derating and loss envelopes for the selected IRFR6215 and LM61460; calculate the actual coupled board thermal paths and hot SOA. Increase appropriate drain/VIN/GND spreading, stack/copper, or reduce the continuous-current requirement until a credible pre-build case exists. Record an engineering-approved prototype thermal qualification plan and acceptance limits. Nine vias and a low copper resistance alone do not qualify 5 A.

### 6. SHOULD — repair probe geometry and preserve ground continuity

**OBSERVATION:** TP301 **(77.5,34)** / TP302 **(79.75,37.25)** are 3.95 mm apart. Cathode→TP302 is approximately **22.42 mm routed**, including its 1.6 mm layer transition; gate→TP301 is approximately **7.95 mm**, also including the transition. The cathode sense keepout runs below the SCR/F301 area and cuts the otherwise useful return plane. TP113 **(42.5,25.25)** / TP114 **(40,13)** are **12.50 mm apart**. They do not implement the short paired pickups explicitly required in BENCH_TESTS.md.

**Exact fix:** put small paired gate/cathode pads beside SCR301 and paired source/gate pads beside Q102, with short dedicated branches from the relevant component lands. Remove the long TP302 slot. Provide local adjacent ground access for raw-output ripple measurement. Recheck populated probe-body access; 2 mm exposed test-pad diameter alone proves only tip access. Keep high-side probing differential.

### 7. SHOULD — compact VCC/feedback connections and their quiet return

**OBSERVATION:** C206 **(40.8,43.8)** uses about **2.56 mm** pin-to-pad routing with 0.20/0.25 mm sections. R203 **(40.5,46.65)** to U201.4 is about **4.44 mm**; R202/C207/R205 extend left to **x35.25–38**. They are appropriately away from the principal SW island, but the feedback network contains redundant routing branches and its ground joins the general plane. U301/R304 **(60,55)/(56.5,55)** likewise lack an explicit paired raw-capacitor Kelvin return in the saved layout.

**Why/fix:** apply TI RevD p47's local VCC/AGND and divider guidance: move C206 and R203 closer, make the VCC bypass connection wide/direct, prune feedback branches, and take divider ground locally to AGND. Route output detector sense/return as a pair from the selected raw-capacitor terminals outside crowbar force current. Preserve the solid reference beneath these routes when repairing finding 2.

### 8. SHOULD — make the 64 V spacing classification explicit

**OBSERVATION:** F101/D101/Q101/Q102 occupy approximately **x20–49, y17–43**. Rules enforce only **0.15 mm default / 0.20 mm power clearance**; D101's high pad at **(25,35.6)** sits beside masked ground at the pour clearance. An exposed-pad scan of VIN_RAW, VIN_FUSED, S_COMMON and both gate nets found no different-net pad gap below **0.80 mm**. This does not establish all lead, solder or enclosure spacings.

**Rule:** **IPC-2221B, November 2012, Table 6-1 p57/§6.3.4–6 p58** uses **0.64 mm B2**, **0.13 mm B4**, and **0.50 mm A6** for 51–100 V. B4 is conditional on permanent conductor coating and the stated controlled environment; exposed assembly lands/leads still require A6. A generic “0.6 mm everywhere” or “soldermask makes everything compliant” conclusion would be wrong. Source: [IPC edition identity](https://www.ipc.org/TOC/IPC-2221B.pdf) and [reading transcription of the primary standard](https://studylib.net/doc/27758238/ipc-2221b).

**Exact fix:** declare the environmental/coating/altitude basis and net-pair peak voltages, then encode and inspect the applicable spacing classes. If the B4 basis is unavailable, enlarge uncoated conductor gaps to the applicable B2 limit. Include the upstream TVS's higher pulse-clamp envelope: 103 V falls in a different row (B4 **0.40 mm**, A6 **0.80 mm**). Creepage/contamination suitability remains OPEN until the actual environment/material requirements are defined; the current DRC is only a manufacturing-spacing check.

### 9. SHOULD — silk is below published process limits and loses field identification

**OBSERVATION:** zero visible reference fields are on F.SilkS; 116 are on F.Fab. The latter already has collisions around **TP301/TP302/TP508** and **TP504/U301**. Board silk text is **0.8–0.9 mm high, 0.12 mm stroke**, including the fabrication warning at **(49,67)**. [JLCPCB's live capability page](https://jlcpcb.com/capabilities/pcb-capabilities), accessed 2026-10-05, publishes **1.0 mm height / 0.15 mm stroke / 0.15 mm pad clearance**. A warning exists, but reliable printed legibility is not established.

**Exact fix:** enlarge critical text to these limits; print connector/test-pad references, nets, polarity and an explicit revision ID. Restore essential U/Q/SCR orientation marks and a readable assembly drawing. Configure silk width/height rules, review mask-subtracted silk, and retain the fabrication warning. No new silk-on-pad violation was found in the fresh configured DRC; that does not excuse undersized text.

### 10. SHOULD — select an actual solder process for vias inside lands

**OBSERVATION:** Q101 drain via **(28.74,24)** and Q102 drain via **(45.26,20)**, with their eight neighbors each, pierce the solder lands/paste-window region; capacitor-ground vias also intersect lands near C203/C204. Global front/back tenting cannot cover a via inside an open component mask aperture on that side.

**Exact fix:** either move the via holes outside paste/wettable lands with short thermal connections, or specify a reviewed via-fill/cap or assembly process and corresponding stencil/mask treatment. Recheck voiding and thermal assumptions. JLC's published mask-plug conditions require clearance from other mask openings; ordinary tenting must not be treated as guaranteed filled/capped via-in-pad service. Reprice if a premium process is selected.

### 11. SHOULD — finish assembly disposition and supplier rotation checks

**EVIDENCE:** all 100 CPL positions/angles match the board's native coordinates modulo 360°. Pin-side sanity is consistent: Q101 **180°**, gate at **(35.04,26.28)**; Q102 **0°**, gate **(38.96,17.72)**; Q103 **0°** versus Q301 **180°**; U201 **0°**, pin 1 **(42.87,42.75)**; D106 **0°**, GND pins to the left; SCR301 K/A/G progress left-to-right. **No SOT-223 is populated**. This establishes internal consistency, not supplier zero-angle acceptance.

**OPEN / exact fix:** verify exact supplier package orientation/centroid for SOT-23, DPAK, U201's asymmetric QFN and D106's DFN; record accepted offsets in ROTATION_REVIEW.csv. Separate the manual/THT operation or obtain an explicit THT placement convention: C217's CPL anchor **(64,−26)** is its positive lead, while the body center is **(66.5,−26)**. Do not reinterpret all native anchors as body centroids. D101 **(25,39)** remains the sole blank LCSC entry; retain the exact Bourns part and explicitly exclude it from JLC placement if externally sourced/installed, or supply a verified exact identifier. [JLC's CPL definition](https://jlcpcb.com/blog/files-needed-for-pcb-assembly) requires component placement location and orientation. No blanket ±90° correction is justified.

### 12. NOTE — topology, basic fabrication geometry and file consistency passed their limited checks

**OBSERVATION:** J501→F101→VIN_FUSED (D101 shunt)→Q101→common source→Q102→VIN_PROTECTED is correct. D101 is electrically after the fuse and before both FETs; its branch extends approximately 12 mm from Q101's drain center, so actual surge-loop ringing still belongs in the input-fault qualification. The selected FETs are **150 V**; do not repeat C2's obsolete 100 V mismatch as a current finding. Raw capacitors/SCR share copper before F301; no crowbar-series fuse was found.

C203/C204 at **(45.95,47.2)/(45.95,40.8)** serve the paired VIN/PGND pins, with local ground vias and a bottom VIN strap. SW is confined to the local U201–L201 connection/bootstrap branch. **LM61460 RJR has no separate exposed ground pad**: the 14-pin package and thermal vias at real VIN/GND lands are appropriate; adding an “EP15” would be wrong. B.Cu is connected ground with interruptions, not an uninterrupted shield; findings 2/3/6 identify the significant local cuts.

Actual tracks are ≥**0.20 mm**, vias **0.60/0.30 mm** with **0.15 mm annulus**; the smallest component PTH annulus is approximately **0.403 mm** at SCR301. Project rules include 0.45 mm component-hole spacing, 0.28 mm component-hole-to-copper and 0.50 mm copper-to-edge. These satisfy the inspected JLC two-layer/1 oz drill/track capability screen, subject to silk and via-process findings. The 0.10 mm mask-web selection needs a compatible mask color/process.

Four 3.2 mm holes at **(14,14)/(86,14)/(14,66)/(86,66)** leave 2.4 mm laminate to the edge. J501/J502 drawn body envelopes **x10.8–20.5 / x78.8–88.5** remain inside the board; no drawn body overhang was found. **OPEN mechanical action:** define washer/screw-head copper keepouts or insulating hardware, connector mating/strain-relief envelopes and any SCR heatsink clearance. The supplied bare-board 3D render cannot close populated mechanical access.

All **9 manifest input hashes and 66 artifact hashes match**. Fresh **9 Gerbers + job file + 2 drill files** match delivered contents after removing only generation timestamps; ZIP member bytes match loose files. BOM and CPL each have the same **100 unique purchased references**; all exist on the PCB. Exclusions reconcile exactly to **15 test pads, J503 and 4 mounting holes**. **99/100** LCSC entries are populated. Thus no stale-export or refdes-set defect was found; assembly qualification remains finding 11.

Manufacturer materials were **referenced only**, with no copied PCB, modified upstream source or newly redistributed datasheet. Exact revisions/files/licenses/attribution remain in the [layout](../../../third_party/v1a_lite_layout/SOURCES.md), [Phase D](../../../third_party/v1a_lite_phase_d/SOURCES.md) and [C3](../../../third_party/v1a_lite_phase_c3/DOCUMENT_MANIFEST.json) registers. Supplemental IPC reference is the November 2012 B edition, Table 6-1/§6.3; IPC copyright retained, no redistribution license asserted. Live JLC pages have no published revision. Existing [schematic review findings 1–4](SCH_REVIEW_R1.md) remain open, including input cutoff and latch capture/retention; this PCB review does not close them or authorize fabrication.

**PCB-review BLOCKING count: 5 — J502 polarity marking; bootstrap routing; crowbar pulse/return qualification; worst-case 5 A voltage allocation; buck/FET thermal qualification.**
