# V1A-Lite — independent PCB re-review R2

2026-10-05 · **STATUS: CONDITIONAL PASS for layout review; electrical qualification and fabrication release remain OPEN.**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**BLOCKING count: 0. BLOCKING list: none.** This count covers demonstrated, layout-fixable blockers only, as required by the review brief. It does not close the pulse, thermal, operating-voltage, environment or schematic-review gates. Remaining practical layout improvements are identified as SHOULD below.

Reviewed detached commit `4a26b17` and actual `hardware/kicad/V1A.kicad_pcb`, SHA256 `f4d096e2e63b12c7f2d493a306d8c2a74383398720bba7072b95768c5b67501e`. Coordinates are **mm, native top view, X right/Y down**, including bottom-side features; CPL Y has the opposite sign. Outline: (10,10)–(90,70). This task writes only this report; no board, schematic, library, manager-report or historical-evidence changes, no sub-agents, no commit and nothing ordered.

**EVIDENCE:** read R1 in full, FIX1 handback and progress table, relevant qualification/harness/assembly notes; inspected native saved copper polygons, tracks, lands, net names and silk, all four copper plots, front mask/paste/assembly, both silks and the incomplete populated render. Detailed coordinate plots and checks are in temporary `/private/tmp/litepcbrev-r2/`. Fresh KiCad **9.0.6 DRC**, all severities/all track errors with schematic parity, on a temporary copy: **0 violations / 0 unconnected / 0 parity issues**. No schematic changes were made; ERC was not rerun. Checks establish geometry/file consistency, not electrical validation.

Findings 1–11 correspond directly to R1. CLOSED applies to the stated PCB issue, not to subsequent physical qualification. BENCH includes external operating/environment requirements that must be supplied before tests; the test operator must not invent them.

## 1. NOTE — R1 polarity finding CLOSED

**OBSERVATION:** J502.1 **(84,44)** is VOUT_PI; .2 **(84,47.96)** is GND. The old misplaced plus at the ground end is gone. `1 +5V` **(85,39)** and `2 GND` **(85,52)** agree with the lands and pin-1 marker. J501.1/.2 **(16,32)/(16,35.96)** have corresponding `J501 1 VIN+` and `2 GND` text. J503.1/.2 **(68,61.5)/(78,61.5)** agree with `J503 +` **(68,65)** and `GND` **(78,57.5)**.

The rotated C218 positive is **(81,26)**, negative **(76,26)**; its positive silk remains at the positive end. C217 positive/negative are **(64,26)/(69,26)**. SCR301 silk states K/A/G right-to-left, matching its new orientation. No polarity regression found.

**Action:** retain these marks. Actual keyed-harness mating-face and unpowered continuity checks remain required by [PI_HARNESS.md](PI_HARNESS.md); no further polarity layout fix identified.

## 2. SHOULD — R1 bootstrap finding STILL OPEN in part; capacitor-path length REGRESSED

**OBSERVATION:** R204 **(42.55,40.8)** now connects U201.13 **(44.375,42.4)** entirely on F.Cu with **2.600 mm of 0.25 mm track and zero vias**. The old 6.857 mm/two-via bottom detour is removed: that principal R1 blocker is closed. CBOOT routing is now a simple, top-only tree, without redundant branches.

However, U201.14 **(43.875,42.4)** to C205.1 **(41.725,39.2)** is **5.350 mm**, versus approximately **3.48 mm** for the shortest old path. This is a real local regression, not merely a changed total-tree statistic. C205.2 **(43.275,39.2)** to SW **(46,44)** is **7.195 mm**, all 0.25 mm wide, entering under U201 at x44.9 through the VIN2/RBOOT gap. The old SW branch was approximately 6.495 mm/0.20 mm. Width improved, but the capacitor moved farther away.

**Why / exact fix:** further compact C205/R204 around pins 13/14, shorten both capacitor legs and widen unconstrained portions while preserving the under-package SW approach, pin clearances and L2 shield. Compare actual pin-to-cap paths after refill, not aggregate net length. TI's [LM61460 Rev D, §11, pp47–49](https://www.ti.com/lit/ds/symlink/lm61460.pdf) favors close bootstrap placement and short, wide connections. It gives no numerical maximum trace length establishing that this improved top-only implementation necessarily fails; the residual optimization is SHOULD, not a newly invented hard blocker. Startup and ringing remain BENCH evidence.

## 3. BENCH — R1 crowbar finding STILL OPEN electrically; force-return layout correction CLOSED

**OBSERVATION:** SCR301 K/A/G are **(69,33.4)/(66.46,33.4)/(63.92,33.4)**. Cathode to nearest bulk negative C217.2 **(69,26)** now has a direct **7.4 mm center separation** through broad front ground, with local ground stitching around **(70.5,33.5)/(70.5,35)** and continuous L2. The former tiny isolated front cathode island is gone. Raw-positive copper connects the anode, ceramic bank and both bulk capacitors; C218 uses the L3 raw region. There is no fuse between this bank and the SCR. F301 **(74.5,43)** remains downstream toward VOUT_PI.

R308.2 **(73,33.675)** has the reported **4.019 mm authored front cathode branch**; the obsolete long bottom ground stub/TP302 slot is absent. That branch merges with GND fill, so it is not an isolated Kelvin conductor. R308's gate connection still uses the bottom gate route; shortening the force loop has not established its dynamic drive.

**Why / exact closure:** characterize the actual gate waveform and anode pulse, both capacitor banks' ESR/ESL, package/leads, source energy until Q102 cutoff, recovery and remote overshoot. Check against waveform-appropriate [ST TYN612 DocID7475 Rev11](https://www.st.com/resource/en/datasheet/tyn612.pdf), including the gate conditions attached to the 50 A/µs rating. FIX1's 10–100 nH sweep is an assumption, not extracted or measured compliance. Follow [CROWBAR_REVIEW.md](fix1/CROWBAR_REVIEW.md) and the reviewed qualification plan; do not add arbitrary trace inductance or a fuse in the raw-bank/SCR loop. No additional force-return blocker was demonstrated by the saved geometry. Pulse qualification cannot be closed by a PCB image or DRC.

## 4. BENCH — R1 5 A allocation finding STILL OPEN operationally; old copper obstruction CLOSED

**OBSERVATION:** R308 and its via have moved away from the old **(69.5,39.65)** bottleneck. The saved raw corridor toward F301.1 **(72.045,43)** is broader, with L3 support and nearby return planes. Fresh extraction of the complete saved copper is **identical to `fix1/COPPER_GEOMETRY.json`**, tying the existing numerical results to this board.

**CALCULATION:** FIX1's L201.2→F301.1 mesh result is **1.073683 mΩ at 20°C**, versus R1's 1.834256 mΩ; at assumed 85°C/5 A its drop is **6.740 mV**. These are inherited mesh results, not a newly solved or measured current-capacity qualification. The C214→J502 round-trip model is **5.345504 mΩ at assumed 85°C**, excluding the fuse body. Independently recomputed:

`Vraw,min = 0.99 × (1 + 100×0.999/(24.6×1.001)) = 5.006350 V`

`Vpi = 5.006350 − 5×(0.025 + 0.009 + 0.005345504) = 4.809622 V`

The **59.622 mV** conditional margin is correct under the updated ≤25 mΩ hot/aged harness allocation. The earlier 40 mΩ allocation is superseded, not silently proved compliant. Cold 9 mΩ fuse resistance, copper/plating minima, joints, ripple and transients remain unbounded. FIX1's stated sensitivity case still gives **4.745440 V**, below the requirement; it is not a measured failure.

**Exact closure:** obtain finished-copper/plating bounds and qualify hot fuse/joint/harness drop, remote minimum voltage and load transients with a dummy load. Include uncertainty; revise the allocation or hardware if those bounds fail. Do not raise setpoint without revisiting crowbar thresholds. No remaining specific copper neck was shown to require a blocking layout edit now. This is neither a 5 A rating nor permission to connect a Pi.

## 5. BENCH — R1 thermal finding STILL OPEN; four-layer copper change verified

**OBSERVATION:** Q101 **(30,24)** drain spreading occupies approximately **x22–33.3, y16–29** on F/B/L3; Q102 **(44,20)** has its separate VIN_PROTECTED spreader around **x41.2–52, y14–27**, continuing along L3 toward U201 **(45,44)**. These are different live nets, not interchangeable GND heatsinks. L2 is GND. Saved copper thickness is **35/15.2/15.2/35 µm**, nominal board thickness 1.6 mm.

**EVIDENCE / limit:** FIX1's coupled thermal screen still fails its assumed 50°C ambient/110°C junction criterion. Its central illustrative cooling case yields Q101/Q102/U201 **181.0/181.6/206.8°C**. These high, uncalibrated results indicate failure to demonstrate the assumed envelope, not valid operating-temperature predictions. This review checked the board geometry and the report's disposition; it did not independently solve or validate the thermal model. Four layers do not close this issue.

**Exact closure:** define ambient/enclosure/airflow and approved junction/derating limits, then measure efficiency, loss, steady-state temperatures and hot turn-off SOA under staged dummy loading. The proposed ≤2 A initial characterization is conditional and unapproved, not a replacement product rating. Results may require lower-loss parts, cooling or revised current limits. Missing thermal qualification alone is BENCH, not a layout blocker with an invented heatsink/copper requirement.

## 6. SHOULD — R1 probing finding STILL OPEN in part

**OBSERVATION:** pair separations independently reproduce: TP113/TP114 on B.Cu **(35.8,22)/(35.8,18.8): 3.2 mm**; TP301/TP302 **(66.5,38.35)/(69.6,38.35): 3.1 mm**; TP504/TP506 **(60,60.5)/(63.25,60.5): 3.25 mm**. The old 12.5 mm Q102 separation and long cathode sense slot are removed. Pads are exposed on their intended faces.

Nevertheless, close probe-pad centers do not make the complete pickup paths paired. TP301's gate branch runs from SCR301.3 **(63.92,33.4)** around the anode-side copper; TP302 merges into power GND. TP504 reaches C214.1 **(66.025,56)** via a narrow branch extending down toward y59, while TP506 uses shared GND. Bottom Q102 pickups share existing gate/source escapes. The pair geometry is improved, not an isolated Kelvin or calibrated high-frequency measurement path.

**Why / exact fix:** for waveform qualification, add or designate adjacent component-terminal spring/differential contacts at C214 and SCR301; shorten and pair dedicated pickup branches where practical, without slotting L2. Document which pads support slower measurements and which terminal contacts support fast edges. Check the intended probe bodies against the populated assembly, including bottom access. Probe clearance and transfer-function validation remain BENCH; the pickup/label geometry can be improved now. Use rated differential probing for Q102.

## 7. SHOULD — R1 VCC/FB/quiet-return finding STILL OPEN in part

**OBSERVATION:** C206 **(41.05,43.6)** VCC routing is **2.357 mm**, top only. R203 **(40.9,46.3)** and the **10.542 mm total FB tree** are closer/cleaner; this total is not the R203-to-FB path length. U201 AGND **(43.15,44)**, C206.2 **(41.05,44.55)** and R203.2 **(40.075,46.3)** share local front ground over continuous L2. FB stays on the control side; no new crossing of the SW island or split reference was found.

The detector remains materially unchanged: U301.3 **(60.9375,55)** and R304.2 **(56.5,54.175)** return through shared GND, not a paired pickup from C214.2 **(68.975,56)**. R301.1 **(59.175,52)** senses the distributed raw net. Therefore the reported detector Kelvin omission remains real. Its dynamic error cannot be inferred solely from netlist connectivity.

**Exact fix:** move/route the detector divider and local reference return as a reviewed sense pair from selected raw-capacitor terminals, separating it from crowbar force current. Use a controlled local connection or reviewed Kelvin/net-tie arrangement if isolation is required; simply drawing another GND trace over GND fill does not achieve it. Preserve the shielding plane. Keep VCC and the local divider return short/wide as placement permits. This remains a SHOULD improvement plus subsequent transient verification; no measured false-trip or missed-trip failure is asserted.

## 8. BENCH — R1 electrical-spacing basis STILL OPEN; no insulation approval

**OBSERVATION:** input parts F101/D101/Q101/Q102 around **x20–52, y14–43** still use manufacturing clearance rules: nominal **0.15 mm default / 0.20 mm power**. D101's high land **(25,35.6)** and expanded live drain regions remain adjacent to masked ground. The new inner copper does not make external mask a qualified permanent coating.

**Why / exact closure:** supply environment, contamination/condensation, altitude, material/coating qualification and actual net-pair voltage envelopes; then encode the applicable external/internal/assembly spacing rules and inspect exposed leads and solder. Distinguish the 64 V source fault from the TVS pulse-clamp envelope. [SPACING_AND_ASSEMBLY.md](fix1/SPACING_AND_ASSEMBLY.md) records the inherited IPC classifications, not approval of their applicability. This review does not independently certify the standard or an environment that is unspecified.

The missing environment/qualification basis is **BENCH/external requirement**, not a determinate layout defect that can be solved by guessing a universal clearance. Once the basis is approved, any demonstrated spacing shortfall becomes layout-fixable and must be corrected before release. Current DRC is only manufacturing-spacing evidence.

## 9. SHOULD — R1 silk finding STILL OPEN for identification; process-size defect CLOSED

**OBSERVATION:** all **23 board silk text objects** are **1.0 mm high / 0.15 mm stroke**. Revision **(71,13)**, warning **(48,66)/(48,68)** and connector polarity survive the saved views. These meet the text dimensions published on [JLCPCB's capability page](https://jlcpcb.com/capabilities/pcb-capabilities), checked 2026-10-05. Fresh DRC finds no silk-over-pad violation; fresh mask-subtracted silk Gerbers match the package. No new silk/pad or reversed-polarity defect identified.

However, local printed IDs remain absent for Q101/Q102/U201 and TP110 **(54,12.25)**, TP112 **(44.25,13)**, TP301/TP302 **(66.5/69.6,38.35)** and TP505 **(86,59)**, as the omission register admits. TP111's text **(65,16.25)** is displaced from its pad **(59,12.25)**. A separate probe map helps but does not provide local field identification.

**Exact fix:** add unambiguous short IDs/net names and leader marks, or a numbered on-board probe legend where local placement is crowded; prioritize gate/cathode and output probes. Check the populated view and mask-subtracted silk after edits, and keep the process-size rules and fabrication warning. Retain clear pin-1/polarity graphics and the assembly drawing for dense devices.

## 10. NOTE — R1 via-in-pad/process finding CLOSED for layout

**EVIDENCE:** repeated the saved-board, both-face hole-to-open-land polygon audit with temporary output: **zero via centers in SMD lands; zero gaps below 0.1 mm; minimum hole-edge-to-land gap 0.142377 mm**. This includes the Q101/Q102 drain regions and C203/C204 around **(45.95,47.2)/(46.65,40.8)**. Front mask/paste inspection agrees with off-land holes and split DPAK paste windows.

**Action:** retain the documented standard off-land tented-through-via process. Tenting is not filled/capped via-in-pad. Actual mask registration, solder fillets/voids and thermal performance remain assembly/BENCH checks; no remaining via relocation blocker found.

## 11. SHOULD — R1 assembly/rotation finding STILL OPEN at supplier acceptance; disposition CLOSED

**OBSERVATION:** full BOM/CPL contain the same **100 unique purchased references**. SMT review BOM/CPL each contain **93**, disjoint from the **seven manual references: C101, C217, C218, D101, J501, J502, SCR301**. Their union is exactly the full inventory. All full-CPL XY/side/rotation values match the native board modulo 360°. No blanket rotation offset was introduced.

Q101 **(30,24), 180°**, Q102 **(44,20), 0°**, U201 **(45,44), 0°**, and D106 **(48.25,35), 0°** retain native mapping; SCR301 **(69,33.4), 180°** matches the rotated K/A/G sequence. C218's placement anchor **(81,26)** is its positive lead, not its body center. Manual assembly avoids mistaking this anchor for an accepted SMT centroid.

**Exact fix:** finish per-package supplier pin-1/centroid/zero-angle acceptance in `fab/assembly/ROTATION_REVIEW.csv`, especially asymmetric U201, DPAK, SOT-23 and D106 DFN. Regenerate CPL only if an evidenced offset is needed. D101 remains exact externally sourced Bourns SMCJ64CA and is excluded from the SMT subset. This supplier-data task is closable on paper; it is SHOULD, not BENCH-only and not a proven PCB rotation fault.

## 12. NOTE — four-layer and switching-node regression search

**OBSERVATION:** L2/In1.Cu has one connected GND filled outline, ordinary drilled-land antipads and **no signal tracks or live-net zones**. Inspected the U201 control/hot-loop area **x37–53, y37–50** and SCR/capacitor area **x60–83, y23–45**: no new dividing slot beneath them. L3/In2.Cu intentionally has separate VIN_FUSED, VIN_PROTECTED and raw-output regions plus fragmented GND fill. Those fragments are not an uninterrupted reference plane; L2 is the continuous shield. The remaining bottom gate-route interruption around **x64–77, y32–36** does not split L2.

The main SW filled polygon is **11.135377 mm²**, bounds **x45.9–52.05, y42.85–45.15**, **identical to the actual R1 commit's polygon**. No new SW zone on an inner/bottom layer or SW via was found. This number excludes pad/track area; the longer C205 SW branch is explicitly recorded in finding 2. No new FB routing over/along that main SW region was found. Accordingly, neither a four-layer ground-plane split nor a main-SW-island enlargement is a new blocker. EMI/ringing and return-current distribution remain unmeasured.

## 13. NOTE — fabrication package matches the reviewed board

**EVIDENCE:** independently checked all **9 manifest input hashes and 77 artifact hashes**, mapping the original `wt-lite` prefix to this checkout; all match. The fresh native export on the temporary board matches all **11 Gerbers**, job data and both Excellon files after removing generation timestamps only. Copper files are exactly **F.Cu, In1.Cu, In2.Cu, B.Cu**; job metadata declares **4 layers / 1.6 mm**. PTH and NPTH drill files declare layer span **1–4**. ZIP contains the 11 Gerbers, job file, two drills and review-only notice; all manufacturing member bytes match the loose files.

The board has **120 footprints**. The 20 nonpurchased exclusions reconcile exactly to **15 test pads, J503 and four mounting holes**. All 100 purchased refs occur on the board; full CPL coordinates/angles/sides and both 93-ref SMT subsets reconcile as in finding 11. **99/100 LCSC entries are populated and agree with `V1A_LITE_BOM.csv`; D101 is the sole blank**, intentionally manual/external. All 93 SMT candidates have LCSC numbers. This checks identity/completeness against the project's procurement source; it does not requalify live catalog stock, substitutions or supplier assembly offsets.

**Action:** no stale-export, copper-layer-count, drill, refdes-set or LCSC-transfer correction identified. Keep the files marked review-only. The board/title-derived job revision still reads `rev?`; the board silk says FIX1 and hashes bind this package, but explicit release-revision metadata should be set when a future release is authorized.

## 14. SHOULD — retain a mechanical closure item alongside the electrical bench plan

**OBSERVATION:** mounting holes at **(14,14)/(86,14)/(14,66)/(86,66)** have no qualified screw/washer envelope in this review. SCR301's live-anode tab near **(66.46,33.4)** has no accepted heatsink/insulation envelope. The populated render omits connector bodies and some custom models, so it cannot establish mating clearance, strain relief or probe-body access.

**Exact fix:** specify insulated mounting hardware or apply keepouts using the selected screw/washer dimensions, and check the selected connector/probe envelopes in the assembly drawing. Reserve an insulated SCR cooling envelope if the bounded pulse/repetition case requires one. Hardware selection and CAD envelope checks are paper/mechanical work; populated fit remains BENCH. Do not invent hardware dimensions or infer a collision merely from an incomplete render.

## Disposition and evidence boundaries

**Layout-fixable now, SHOULD:** compact C205's remaining loop; improve terminal-level probe pickups and quiet detector sensing; complete local silk identification; finish supplier orientation data and selected mechanical envelopes. None is promoted to BLOCKING solely because its electrical effect has not been measured.

**BENCH/external closure:** SCR pulse/gate/recovery and remote overshoot; buck/FET loss, temperature and hot SOA; hot fuse/harness/joint drop and full operating voltage/transients; source/environment/coating requirements and associated qualification; populated probe/solder/mechanical checks. Supplier/material bounds and acceptance limits must be supplied before testing. Failed results can require a subsequent layout or schematic revision. [SCH_REVIEW_R1.md](SCH_REVIEW_R1.md) and the staged [BENCH_TESTS.md](BENCH_TESTS.md) remain applicable; this re-review does not close their protection findings or advance a fabrication gate.

**Provenance:** manufacturer documents were referenced only; no third-party circuit/artwork was copied or adapted in this task, no source modified and no new third-party material redistributed. TI **SNVSBD5D, July 2022 Rev D**, local `wt-datasheets/third_party/datasheets/LM61460AANRJRR.pdf` and `/private/tmp/liteb/LM61460AANRJRR.txt`, §11; ST **DocID7475 Rev11**, official `tyn612.pdf`, electrical/pin/package tables; and JLCPCB's unrevisioned live capability page were checked against the linked official sources. Copyright remains with TI/ST/JLCPCB; no redistribution license asserted. Existing part/layout provenance, licenses and attribution are retained in [FIX1 sources](../../../third_party/v1a_lite_pcb_fix1/SOURCES.md), [layout sources](../../../third_party/v1a_lite_layout/SOURCES.md) and the [C3 document manifest](../../../third_party/v1a_lite_phase_c3/DOCUMENT_MANIFEST.json). IPC values are inherited from the identified R1/FIX1 notes, not represented as a fresh licensed-standard audit.

**Final PCB-review BLOCKING count: 0 — none.**
