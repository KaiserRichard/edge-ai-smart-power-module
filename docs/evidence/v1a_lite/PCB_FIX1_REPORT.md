# V1A-Lite PCB FIX1 handback — 2026-10-05

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**STATUS: CONDITIONAL PASS for the requested layout correction/evidence package; BLOCKED for electrical qualification and fabrication release.** Sole editor, no sub-agents. Baseline `44eee9c`; all 11 findings audited before further editing. No push, merge, upload, order, physical test or schematic/setpoint change. Git staging/commit is denied by worktree `index.lock` permissions; work remains uncommitted as directed.

Final board SHA256: `f4d096e2e63b12c7f2d493a306d8c2a74383398720bba7072b95768c5b67501e`. Board **80×60 mm, four layers, nominal 1.6 mm, 35/15.2/15.2/35 µm copper**. L2 GND only; L3 GND plus separate live power/thermal regions. See [progress](LAYOUT_PROGRESS.md) and [source register](../../../third_party/v1a_lite_pcb_fix1/SOURCES.md).

## Per-finding disposition

“Layout addressed” is not electrical validation. Items requiring missing source/environment/supplier data or physical measurements remain explicitly OPEN.

| R1 finding | Final status | Evidence / remaining limitation |
| --- | --- | --- |
| 1 connector polarity | Layout addressed | J501/J502 numbered positive/GND labels; J503 polarity. J502.1 (84,44)=VOUT_PI, .2 (84,47.96)=GND. Match [harness mating-face instructions](PI_HARNESS.md); real keyed harness continuity still required. |
| 2 BOOT | Layout addressed | R204 (42.55,40.8), C205 (42.5,39.2). RBOOT 2.600 mm F.Cu, no vias; CBOOT tree 5.350 mm F.Cu, no old bottom route or redundant branch. Pin14-to-C205 path 5.350 mm, with R204 on the tree. SW approach remains under-package through VIN/RBOOT gap; ringing/startup untested. |
| 3 crowbar force/return | Layout addressed; pulse qualification BLOCKED | SCR rotated, bulk bank reoriented, broad front/inner raw force copper, short nearest-cap return and stitching. R308 (73,34.5) has 4.019 mm authored K return instead of long bottom stub. Shared GND is not an isolated Kelvin net. No fuse between raw bank and SCR. [Pulse review](fix1/CROWBAR_REVIEW.md) identifies missing gate/ESL/source-cutoff bounds. |
| 4 bridge / Pi allocation | Conditional calculation PASS | Removed R308 obstruction from bridge; F301 (74.5,43). 5 A bridge drop **6.740 mV at assumed 85°C**. Pi tolerance screen **4.809622 V**, margin **59.622 mV** with ≤25 mΩ harness. Full operating worst case remains OPEN. |
| 5 thermal / stack | Copper addressed; thermal screen FAIL | Expanded Q101/Q102 drain spreading on F/B/L3, L2 GND retained. Coupled loss/thermal sensitivity below fails all three assumed cooling cases. No continuous 5 A thermal qualification. |
| 6 probes / GND continuity | Geometry improved; access OPEN | Q102 pair B.Cu (35.8,22)/(35.8,18.8), 3.2 mm apart; SCR pair 3.1 mm; raw TP504/TP506 pair (60,60.5)/(63.25,60.5), 3.25 mm. Long TP302 slot removed. Differential probe-body, shared-escape and actual populated access unqualified. |
| 7 VCC / FB / quiet return | PARTIAL | Local top-only VCC 2.357 mm; FB tree 10.542 mm, divider closer and redundant routing removed. Local GND plane serves AGND; detector U301/R304 still lack an isolated paired capacitor Kelvin return. Do not call shared-plane connectivity a Kelvin pass. |
| 8 64/103 V spacing | OPEN requirements | Explicit coating/environment/voltage-pair classification in [spacing note](fix1/SPACING_AND_ASSEMBLY.md). Native DRC checks manufacturing spacing, not an approved B4/B2 insulation design. No spacing waiver. |
| 9 silk / assembly | Process sizes addressed; coverage PARTIAL | Critical labels ≥1.0 mm/0.15 mm; revision, polarity and warning retained. Added available local TP/SCR refs and bottom probe refs; [omissions recorded](fix1/SILK_IDENTIFICATION.json). Removed 117 duplicate Fab annotations and reduced probe Fab text to separate adjacent IDs. Native orientation marks retained. |
| 10 via-in-pad | Layout/process addressed | Zero via centers in exposed lands; both-face hole-to-land audit minimum **0.142377 mm**, zero below 0.1 mm. Standard off-land tented through vias; no filled/capped premium. Solder/void inspection still required. |
| 11 assembly / rotation | Disposition complete; supplier offsets OPEN | 100-part review inventory; 94 SMT candidates; D101/SCR301/C217/C218/J501/J502 manual. Exact Bourns D101 retained. Native angles/pad identities preserved; [rotation checklist](fab/assembly/ROTATION_REVIEW.csv) does not falsely accept supplier zero angles. |

## Copper and voltage evidence

**CALCULATION:** final filled geometry, 0.1 mm resistor mesh, actual four-layer thicknesses, assumed 18 µm barrel plating; equipotential terminal contacts. Copper model excludes fuse body, contact/solder losses and switching behavior. Re-extraction after Fab-only annotation cleanup proved all extracted geometry identical; [identity record](fix1/COPPER_IDENTITY.json) permits reuse of the numerical solve, with original solved-board hashes retained.

| Modeled path | 20°C resistance | Assumed 85°C resistance | Drop at 5 A / 85°C |
| --- | ---: | ---: | ---: |
| L201.2→F301.1 | 1.073683 mΩ | 1.347956 mΩ | 6.740 mV |
| C209→J502 including return, excluding fuse | 2.860784 mΩ | 3.591571 mΩ | 17.958 mV |
| C214→J502 including return, excluding fuse | 4.257839 mΩ | 5.345504 mΩ | 26.728 mV |

L201→F301 cold resistance fell from R1's **1.834256 mΩ** to **1.073683 mΩ**. At x69.5, y41–45, the 5 A injection model carries 2.693 A on F.Cu and 0.300 A on L3; the rest crosses outside this local window. Maximum sheet-edge density in that window is **86.6 A/mm²**, versus R1's ≈188 A/mm² at the old bottleneck. The whole raw-net maximum is 106.3 A/mm² near (68.3,42.85). Raster peaks are not ampacity/temperature limits. The C214 round trip differs **+1.09%** on the 0.2 mm mesh; neither mesh is a guaranteed worst-case bound. Actual DC source is the inductor; capacitor injections sample bank spreading only.

**CALCULATION:** `Vraw,min = 0.99 × (1 + 100k×0.999/(24.6k×1.001)) = 5.006350 V`.

`Vpi = 5.006350 − 5 × (0.025 + 0.009 + 0.005345504) = 4.809622 V`.

**PASS, conditional margin 59.622 mV** against 4.75 V. Nominal setpoint remains **5.065041 V**. Sampled hot copper loss is 0.1336 W. The harness allowance covers hot/aged mates, splices and cable; maximum 150 mm 18 AWG trunk plus parallel 50 mm 22 AWG fanouts does not guarantee its resistance.

**OPEN / FAIL to demonstrate full worst case:** fuse resistance is a **cold** 9 mΩ assumption; copper/plating minima, hot joints, ripple/load transients and uncertainty lack approved bounds. As a sensitivity example only, 20% conductor-area reduction, a 13.5 mΩ hot fuse, 2 mΩ board joints and 25 mV negative ripple give **4.745440 V**, **-4.560 mV** margin (FAIL). These are explicitly assumptions, not invented requirements. Remote dummy-load qualification must close the real terms before a Pi.

## Thermal evidence and cost

**CALCULATED / ASSUMED, not validated:** actual IRFR6215 loss at 1.563 A and 18 V at the buck is **0.721 W cold / 1.417 W at the 150°C RDS(on) value, per FET**. Solving the input-voltage drop self-consistently at 18 V module input and assumed 90% buck efficiency gives 1.764 A and **1.804 W per FET** at the same hot resistance; U201 loss screen is **2.417 W**. Gate drive, hot SOA, actual efficiency and remaining component heat are not qualified.

The coupled 2 mm four-sheet model uses filled copper, via conduction, FR4 0.3 W/mK, copper 400 W/mK, illustrative 50°C ambient, and package proxies 1.4/1.4/19.2 K/W for Q101/Q102/U201. JEDEC/package values are not calibrated resistances for this board. Small-gap homogenization and omitted enclosure/other heat sources limit the model; above 150°C, the fixed hot FET resistance is not a valid upper bound. These high outputs mean the screen fails, not that these are valid operating predictions.

| Assumed convection+radiation W/m²K | Q101 junction °C | Q102 junction °C | U201 junction °C | Against assumed 110°C screen |
| ---: | ---: | ---: | ---: | --- |
| 5 | 245.8 | 245.7 | 270.0 | FAIL / FAIL / FAIL |
| 10 | 181.0 | 181.6 | 206.8 | FAIL / FAIL / FAIL |
| 15 | 158.5 | 159.5 | 185.5 | FAIL / FAIL / FAIL |

Ambient/airflow/derating and a revised loss/cooling or continuous-current case need engineering approval. [Thermal JSON](fix1/THERMAL_SCREEN.json), [proposed qualification plan](fix1/QUALIFICATION_PLAN.md). No unapproved derating was silently changed into a requirement.

**Public cost screen, checked 2026-10-05:** JLC advertises **from US$2/five for 1–4 layers**, with the same US$2/five two-layer baseline. This 80×60 mm board fits the published ≤100×100 mm size tier: **advertised entry-price delta US$0/five**. Exact configuration/nonpromotional price, freight/tax and first-build landed budget remain OPEN. [Price/stack detail](fix1/COST_AND_STACK.md), [public page](https://jlcpcb.com/ads/pcb-prototype). No premium via process selected or order placed.

## Checks, package, and handoff

Native KiCad 9.0.6 **DRC: 0 violations, 0 unconnected, 0 schematic parity** with all severities/all track errors and JLC manufacturing rules. **ERC: 0 errors / 0 warnings.** [Final package DRC](fab/review/DRC.json), [fresh ERC](fix1/RESUME_ERC.rpt). These are geometry/netlist evidence only.

[Four-layer Gerber/drill ZIP](fab/V1A_GERBERS_DRILL_REVIEW_ONLY.zip), BOM/CPL/manual disposition, mask-subtracted silk, PDFs/PNGs, bare-board render, native command logs and hash manifest are under [fab](fab/). The [package verification](fix1/PACKAGE_VERIFICATION.json) records final hash/set/ZIP/rule-check integrity. Visual review is recorded separately in [VISUAL_REVIEW.md](fix1/VISUAL_REVIEW.md). The render lacks component models; no populated mechanical clearance claim.

**NEXT:** independent engineering review of the explicit remaining pulse, thermal, spacing, sensing and assembly blockers; R4 release remains BLOCKED. Follow the staged bench procedure only after approval. Requested Git group commits were attempted but worktree `index.lock` creation was denied. No push, permission change or historical-evidence deletion.
