# V1A-Lite Phase D — option 1R capture

2026-10-05. **STATUS: CONDITIONAL PASS — schematic capture only. Electrical R2 release and R3 remain BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**REQUIREMENT / authority:** full owner brief `/Users/quockaiser/Desktop/Research/v1a-lab/briefs/V1A_LITE_PHASE_D.md`; branch `feat/v1a-lite-cost-reduction`, starting `9c37897`. The later owner selection authorizes capture despite C2's historical implementation block; it does not waive qualification. C2 §7 governs over Phase C; C3 contributes only the selected IRFR6215TRPBF input correction. No sub-agents, purchases, push, placement/routing or PCB changes.

## Drawn hierarchy and electrical choices

| Sheet | Captured scope | Purchased parts |
| --- | --- | ---: |
| Root `V1A` | Four explicit hierarchical sheets; source/force/control/return ports | 0 |
| 01 input protection | F101 3A, upstream SMCJ64CA, common-source Q101/Q102 **150V IRFR6215TRPBF**, separate gate clamps, downstream TVS3300, reservoir, TL431 detector and all ballast resistors; Q104/Q105 regenerative latch and Q106 Q103-base clamp | 58 |
| 02 LM61460 buck | LM61460AANRJRR, SRP1265A-6R8M, 100k/24.6k FB, 33.2k RT, 22pF+1k feedforward, native SW bootstrap, VCC bypass, independent EN divider, BIAS=GND and PGOOD explicitly NC; six 47uF/25V 1206 MLCCs and two 1000uF/10V raw bulk capacitors | 26 |
| 03 output protection | Raw TL431/BC807/TYN612RG crowbar; 1k+100R+30R / 1k divider, specified base/gate resistors, CB_COLLECTOR latch trigger, downstream F301 7A wiring fuse, two Pi-side 47uF/16V capacitors | 14 |
| 05 IO/test | J501 24V auxiliary input and J502 Pi power, both exact JST B2P-VH-FB-B(LF)(SN); J503 dummy-load solder pads, supply/output/control test pads | 2 |

**DECISION:** Q102 interrupts forward input current; Q101's forward body-diode path cannot do so. CTRL12 is taken from S_COMMON upstream of Q102, and the latch clamps Q103 base independently of buck EN/FB/VCC/PGOOD. Reset is intended by input removal only; actual persistence, minimum reset interval and brownout immunity are not validated.

**DECISION:** SCR301 anode, detector upper divider, Q301 emitter, six raw MLCCs and both bulk capacitors share **VOUT_5V1**, with no fuse/link between them. F301 is fitted solely between VOUT_5V1 and **VOUT_PI**, for wiring backup, not crowbar clearing. C2's LOAD_5V1 is renamed VOUT_PI as requested. C217/C218 are drawn on Sheet02 per C2 §7, electrically at the Sheet03 raw crowbar node. GND is common electrically; separate Kelvin/switching/pulse-current geometry remains a layout requirement.

**OBSERVATION:** active Sheet04 is deleted. R401, INA228, I2C circuitry, research eFuses, logic, MOSFET output protection, gate drivers, hold-up supplies, manual arm/reset and research injection links are absent. VOUT_PI reaches J502/J503 on one continuous net, with no substituted 0R resistor or shunt. J503 is two copper solder pads, not another purchased connector. There are **100 purchased components, 11 test pads, 1 dummy-load pad pair, and 3 nonphysical power flags** (115 symbols total). No USB3/D435i data passes through this design.

## Package and provenance review

**EVIDENCE:** [source register](../../../third_party/v1a_lite_phase_d/SOURCES.md), [installed library hashes](../../../third_party/v1a_lite_phase_d/LIBRARY_IDENTITIES.json). C/C2 BOMs do not contain footprint columns; physical packages were mapped from exact MPNs and manufacturer drawings rather than inferred from values alone.

- Q101/Q102: DPAK G1/D2+tab/S3, standard TO-252-2; each gate clamp cathode goes to common source. SCR: TO220 K1/A2+tab/G3; the standard TIC106 **glyph** is used with exact TYN612RG value/MPN, not a part substitution. Tabs are electrically live.
- Both TL431 DBZs: K1/REF2/A3. BC807 and MCC MMBTA42: B1/E2/C3, SOT23. MCC's browser fetch failed, but direct manufacturer HTTPS download succeeded; page1 pinout was reviewed. TVS3300 DRV: IN4/5/6, GND1/2/3/EP7; standard 2x2mm/0.65mm-pitch/1x1.6mm-EP footprint. BZT52 SOD123 pin1 cathode; SMCJ is bidirectional SMC.
- LM61460's existing manufacturer-mapped symbol and RJR0014A qualified footprint are retained; all 14 pins match. No fictitious exposed-pad pin was added. Existing exact JST qualified footprint retains its 3.96mm power contacts and unnumbered locating hole. Standard Littelfuse NANO2-451_453 lands used for both fuses.
- **Correction during review:** C101 EEUFR1H101 is **8x11.5mm / 3.5mm pitch**, not 6.3mm / 2.5mm. Final standard footprint matches the Panasonic table. C217/C218 EEUFR1A102 are 10x16mm / 5mm pitch. Polarized capacitor pad1 is positive.
- Raw GRM31CR61E476ME44L uses 1206; input and retained Pi-side GRM32 parts use 1210. GRM188/GRM21 bypass parts use 0603/0805; C207 is 0402. The specified 10k 0805 resistors remain 0805; remaining selected resistors are 0603.
- No exact SRP1265A footprint was installed. Added `V1A_Lite:Bourns_SRP1265A` from Bourns' land pattern: 14.2mm outer span, 8mm inner gap, two **3.1x5mm pads at ±5.55mm**. Added project-owned dummy-load pads. Manufacturer source files and historical libraries were not modified.

**OPEN RISK:** package/pad-number evidence is not layout/assembly/thermal qualification. Recheck exact incoming package suffixes, manufacturing tolerances, clearance/creepage, live-tab insulation, solder process and connector/harness polarity before release.

## ERC, netlist, visual review and tests

**EVIDENCE:** KiCad CLI **9.0.6**, [final ERC](PHASE_D_ERC.rpt): **0 errors / 0 warnings**. No remaining ERC warnings to explain. No rule severity, ERC exclusion or project-file changes. Fontconfig emitted host-environment stderr diagnostics; these are not electrical-rule findings, and system configuration was not changed.

Power flags are limited to genuine VIN_RAW and GND at the input connector plus VIN_PROTECTED, the real supply delivered through passive F101/Q101/Q102. KiCad does not propagate power-output typing through those passive devices. The exported netlist independently checks both FET orientations and the source path; the flag asserts an available supply when enabled, not guaranteed operation during shutdown/faults. No flag powers an isolated research rail or substitutes for a missing electrical connection.

[Verification](PHASE_D_VERIFICATION.json) records **556 passing checks**, including exact BOM/MPNs/LCSC/cost, every physical symbol pin against footprint pads, direct raw-crowbar continuity with F301 removed, Q102 inhibition, upstream latch supply, bootstrap/BIAS/VCC/EN/FB handling, removed telemetry, unchanged ERC rules, and **byte-identical historical PCB**. These static checks do not simulate analog timing or establish safety.

The [PDF](../../schematic/V1A_Lite_schematic.pdf) was rendered and all five pages visually inspected; field/net-label overlaps found in the initial export were corrected and reviewed again. Standard electrical glyphs use explicit local net labels and hierarchical interfaces. Pin identity/polarity was reviewed alongside the [KiCad XML netlist](V1A_LITE.net.xml). There is no new PCB output or applicable DRC, because the PCB was not edited.

The original 60-test suite passed against its mostly frozen **research** fixtures before scoping; that is not Lite validation. `test_r2_capture.py`, `test_gate4b_capture.py`, and `test_bom_order.py` are research-V1A-only and explicitly skipped by unittest discovery when the active schematic identifies Lite. Their files/fixtures remain. `check_repository.py` dispatches to the Lite profile rather than applying research hash/architecture contracts. Other historical footprint/readability regression tests remain active, including the reused LM61460 footprint. Five new Lite checks reject unsafe crowbar, latch-supply, input-inhibit and Pi-fuse bypass mutations. See [test log](PHASE_D_TESTS.txt).

Other `check_r2_*`, Gate4B, old BOM exporters, readability rebuilders, footprint-completion and `prepare_layout_board.py` scripts still target research V1A. Do not run their mutating builders on the Lite capture. No old test/script was deleted. Historical research tests retain their original purpose on the tagged architecture.

Recheck without changing CAD:

```sh
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch erc hardware/kicad/V1A.kicad_sch -o docs/evidence/v1a_lite/PHASE_D_ERC.rpt
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch export netlist hardware/kicad/V1A.kicad_sch --format kicadxml -o docs/evidence/v1a_lite/V1A_LITE.net.xml
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
```

`build_v1a_lite.py --sheet 1|2|3|5` is an explicit **writer**, not a check; use in order only when intentionally regenerating this capture. Per-sheet intent JSON and intermediate ERC reports are retained. Initial incomplete-hierarchy ERC counts were 9/10/6 errors after Sheets01/02/03 respectively, all closed by the complete hierarchy.

## BOM reconciliation and deviations

**CALCULATION:** [BOM CSV](V1A_LITE_BOM.csv), one row per physical reference, is derived from the exported schematic fields. Dated prices/MOQs remain planning inputs; no stock refresh or purchase was made.

| Scope | VND |
| --- | ---: |
| Phase C2 A installed core | 348,655.20 |
| Remove two IRF9540NPBF at 9,521.45 | −19,042.90 |
| Add two IRFR6215TRPBF at 24,843.75 | +49,687.50 |
| **Phase D installed core (98 parts)** | **379,299.80** |
| J501/J502 installed headers | +8,517.10 |
| **CSV installed purchased total (100 parts)** | **387,816.90** |

Twelve copper features have zero **component purchase** cost; board manufacture is excluded, not free. Harness mates/contacts, bare board, thermal hardware, freight/tax, MOQ/spares, assembly and contingencies are outside this installed BOM total. C2 B/C purchasing estimates are not claimed unchanged or complete. D101 retains the explicit 13,250 VND allowance and `LCSC=OPEN`: the source BOM supplies no exact Bourns LCSC identifier. No number was invented. All other purchased parts have their inherited exact LCSC field.

The only purchased-MPN deviations from C2 are the two expressly authorized FETs. Other decisions are drawing/package realization, VOUT_PI naming, dummy-load/test-pad features, removal of research circuitry, and the C101 footprint correction. No C3 option3B eFuse, extra output switch or retuned backup-crowbar threshold was imported.

## Open qualification and next gate

**OPEN RISK:** C2/C3 electrical blockers persist: bounded source current/impedance/hiccup and harness/load capacitance; worst-case detector/cutoff delay; latch pulse capture/persistence/reset; startup at normal and 54.6–64V fault input; hot IRFR6215 SOA, losses and reverse/backfeed behavior; actual TVS clamp/ringing; raw/bulk voltage containment; SCR gate rise, di/dt, surge I²t, recovery and thermal survival; normal nuisance-trip window and Pi-node overshoot; loop stability, inrush, effective MLCC capacitance, ripple/transients, component derating and 5A continuous thermal performance; current stock, D101 sourcing and full landed cost.

**OBSERVATION:** 150V FETs resolve the specific 103V-clamp/100V-nameplate mismatch, not all surge or hot SOA risks. Six 25V raw ceramics do not guarantee survival of 26–29V uncontained faults, and the 10V bulk caps still depend on containment. The historical IRF9540 thermal/SOA curves cannot qualify IRFR6215. The nominal feedback target is 5.065V, not exactly 5.100V.

**REQUIREMENT / bench sequence:** visual inspection → continuity/short checks → current-limited bench supply → no-load startup → rail verification → low-current dummy/electronic load → increasing load steps → thermal → ripple → load/transient tests → OV/crowbar, input cutoff/latch, reset/reverse/backfeed/fault tests → telemetry N/A → **Pi integration only after all earlier gates pass**. Never use a Pi for first-load or OV qualification.

**NEXT GATE:** independent engineering review and closure of the electrical requirements/qualification plan before R2 release; only then separately authorized R3 layout. The old PCB and its research netclasses are not a Lite implementation. No fabrication release is implied.

**GIT:** commit was attempted after Sheet01 as instructed, but `git add` failed with exit128: `Unable to create .../.git/worktrees/wt-lite/index.lock: Operation not permitted`. Per the brief, work remains **uncommitted**; no permissions/locks altered and no push. [Progress](PHASE_D_PROGRESS.md) records each sheet and resume state.
