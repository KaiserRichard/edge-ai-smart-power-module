# V1A-Lite 1R — independent schematic review R1

2026-10-05 · Reviewed snapshot `402f86fd18d87e25c47a1ca1043358edbe11d02a`.

**STATUS: BLOCKED for electrical release — 4 BLOCKING findings.** No incorrect device pin mapping was found. The four blockers concern unclosed protection behavior already identified in the design basis; they are not claims of four new capture errors. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Scope: all five schematic pages, embedded symbols, assigned footprint files, BOM, freshly exported netlist, and C/C2/D design evidence. C2 supersedes C; captured IRFR6215 devices supersede the old IRF9540 calculations. Only this report is changed. No CAD/library/PCB edits, purchases, commits or physical validation.

## Numbered findings

### 1. BLOCKING — output trip window and response do not establish the Pi voltage requirement

**Sheet03:** U301.2/1, Q301.1/3, R301–R308, SCR301.3; **Sheet02:** C209–C218, U201.4; **Sheet05:** J502.1.

**CALCULATION:** captured upper/lower divider is 1130 Ω / 1000 Ω: `2.495 × (1 + 1.13) = 5.31435 V`, plus approximately 2.26 mV from typical REF current. Independently reproduced C's conditional temperature/tolerance screen: **5.18387–5.43587 V**. It includes assumed TCR/temperature and cathode-shift reserves; it is not a guaranteed comparator trip specification. Against the brief's 5.17–5.25 V normal-high screens, nuisance margin is approximately **+14 to −66 mV**; high-trip headroom to 5.5 V is only **64 mV**.

**EVIDENCE:** [TI TL431, SLVS543S](https://www.ti.com/lit/ds/symlink/tl431.pdf), pp13, 24–25: accuracy conditions and overdrive/current-dependent comparator response. No maximum delay for this circuit is specified. C2 §3 reports only **0.416–0.937 µs** post-threshold allowance under its stated sensitivities, and a Pi-node example reaches **5.702 V** despite raw-node clamping. Those are model examples, not measurements or final harness parameters. Adding 2 mF did not close this issue.

**Required fix/closure:** establish actual maximum normal voltage after rechecking the changed capacitor bank, C207/R205 compensation and load-release/PFM behavior. Then revise/qualify the detector and protection so its complete threshold interval lies above that normal envelope and its worst-case detector-to-clamp delay keeps **J502/Pi voltage plus uncertainty <5.5 V**. If this TL431/SCR combination cannot meet the resulting budget, replace the detection/isolation approach with specified threshold and delay bounds. Do not merely lower R303 or add a delay capacitor. Include actual harness impedance and remote capacitance.

### 2. BLOCKING — 64 V startup and input cutoff survival remain unbounded

**Sheet01:** U101.1/2, Q103.1/3, Q102.1/2/3, D106.4–6, R130–R144; **Sheet02:** U201.8/12 and input capacitors.

**CALCULATION:** input divider is 102 kΩ / 10 kΩ: **27.944 V ideal**, **28.148 V** with typical 2 µA REF current. Reproduced C's conditional **27.008–29.260 V** screen. At 64 V and assumed CTRL12=12 V, the two eight-resistor strings give 4 kΩ, 13 mA, **0.676 W total / 42.25 mW per resistor**. R144 dissipates about **90 mW** with U101 conducting. Static arithmetic does not prove turn-off before the protected rail overstresses.

**EVIDENCE:** [LM61460 RevD](https://www.ti.com/lit/ds/symlink/lm61460.pdf), p4: 36 V operating / 42 V absolute input limits. [TVS3300 RevC](https://www.ti.com/lit/ds/symlink/tvs3300.pdf), pp5–6: pulse-conditioned clamp/current limits, not continuous 64 V absorption. [IRFR6215, 2016-05-31](../../../third_party/v1a_lite_phase_c3/irfr6215.pdf), pp1–2, 4–5: 150 V, ±20 V VGS, 0.295 Ω maximum at stated conditions, charge/SOA/thermal data. The old IRF9540 timing and thermal results cannot qualify these devices.

**Required fix/closure:** bound upstream fault current, rise time, impedance and hiccup; demonstrate cold connection at 54.6/64 V as well as an already-running input step. Establish maximum U101/Q103/Q102 delay, hot SOA and R130–R135 pulse survival, with VIN_PROTECTED within its reviewed operating/transient limits and capacitor ratings. If the discrete stage cannot enforce these bounds, revise its controller/current limiting while preserving forward cutoff at Q102. Recalculate using IRFR6215 data and actual gate drive. Input-fuse voltage rating alone does not close this.

### 3. BLOCKING — crowbar trigger capture and persistent latch-off are not established

**Sheet03:** Q301.3 → CB_COLLECTOR; **Sheet01:** R163, Q104.1/3, Q105.1/2/3, Q106.1/3, Q103.1, Q102.1.

**OBSERVATION:** wiring is logically correct: R163 sets Q104; Q105/R161 provide regeneration; Q106 clamps Q103's base, allowing Q102's source-gate pullup to open the forward path. CTRL12 is supplied upstream of Q102. There is no buck-power bypass or EN/FB dependency. However, the same SCR action collapses the source of the set pulse. Minimum captured pulse width, hot/cold regeneration, brownout retention and reset interval are unspecified.

**EVIDENCE:** [MCC MMBTA42 Rev3-3-12012020](https://www.mccsemi.com/pdf/Products/MMBTA42%28SOT-23%29.pdf), pp1–2, and [Nexperia BC807 Rev8](https://assets.nexperia.com/documents/data-sheet/BC807_SER.pdf), pp2, 5: pin/gain/saturation evidence does not specify this latch's pulse capture or retention. C2 §1's 64 V model leaves only about **0.16 mA** in D104 after the detector and latch loads; nominal 12 V regulation must not be assumed across all corners.

**Required fix/closure:** characterize the shortest actual CB_COLLECTOR pulse and prove SET_LATCH capture, sustained LATCH_H, Q103 inhibition and Q102 gate-to-source return after VOUT collapses. Specify minimum input-removal reset time and permitted supply dips. Where source hiccup resets the latch without intended power removal, add a qualified retention/reset mechanism or revise the latch supply. Retain shutdown of **Q102**; shutting off Q101 alone leaves its forward body-diode path.

### 4. BLOCKING — SCR gate and capacitor-discharge stress lack a qualified bound

**Sheet03:** SCR301.2/3/1, Q301.3, R307/R308; **Sheet02:** C209–C218 and C101/input reservoir through L201.

**CALCULATION:** using 5.18387 V, assumed Q301 saturation 0.2 V, VGT=1.3 V and resistor corners gives **35.16 mA** gate current after R308. This exceeds **15 mA IGT maximum at 25°C** for the selected **TYN612RG**, not the 5 mA TRG grade. It is only a conditional room-temperature screen. Assuming 0.7 V saturation and 1.5 V VGT reduces it to **28.03 mA**; the required full-temperature maximum and gate rise time remain OPEN. R163 also draws approximately 0.4 mA of Q301 collector current during setting.

**EVIDENCE:** [ST TYN612, DocID7475 Rev11](https://www.st.com/resource/en/datasheet/tyn612.pdf), pp2–5: latching/holding currents, surge conditions and **50 A/µs** turn-on limit conditioned on gate drive. Illustratively, 4.5 V across an assumed 10 nH discharge loop gives **450 A/µs**; no such loop bound is established. Removing input power does not remove energy already in either capacitor bank. C217/C218 are only 10 V rated; the 25 V ceramics are not a fallback for an uncontained 26–29 V fault.

**Required fix/closure:** specify hot/cold gate-current and rise-time margin, and bound SCR anode current, di/dt, I²t, temperature and recovery including both reservoirs and delayed Q102 cutoff. If necessary, add engineered SCR-branch current-rise control or select a suitably rated crowbar/driver, then repeat finding 1's voltage check. Keep the SCR connected to raw VOUT_5V1; do not insert a fuse between it and the raw bank. F301 cannot clear this local discharge.

### 5. SHOULD — add direct gate and cutoff measurement access

**Sheet03:** SCR301.3 / R307.2 / R308.1 has no test pad. TP508 measures **CB_COLLECTOR before 100 Ω R307**, so it is not a gate-voltage test point. Input, protected input, raw output, Pi output, CTRL12, latch and GND pads are present.

**Fix:** add a small SCR_GATE sense pad and adjacent SCR-cathode GND pad. Add S_COMMON and CUT_GATE sense pads for differential Q102 VGS capture; retain TP110/111/112. Keep sense connections out of the high-current discharge path. Basis: ST pp2–3 gate conditions and the required bench sequence; no datasheet mandates a particular test-pad refdes.

### 6. SHOULD — finish the Pi harness definition

**Sheet05:** J502.1=VOUT_PI, J502.2=GND is correct at the board; destination physical pins and wire gauge/length are absent.

**Fix:** document the chosen Pi power interface and a keyed mating-view harness drawing. For a 40-pin-header implementation, identify physical **2/4 as 5 V** and the selected ground pins, e.g. **6/9**; J502 pin1 is not Pi physical pin1. Specify conductor gauge, length, crimp/contact parts, current sharing and allowable round-trip resistance. The [official Pi pin diagram](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png) defines these pins. [JST VH datasheet](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), pp1–2, 4, rates this shrouded family at **7 A with AWG18**, not the standard-header 10 A/AWG16 condition. VHR-2N/SVH-41T-P1.1 is a documented mating candidate; final harness qualification remains OPEN. Coordinate F301 with the selected wire and contacts.

### 7. SHOULD — D101 prevents a complete sourced BOM

**Sheet01:** D101.1/2, Bourns SMCJ64CA, SMC footprint. Its BOM/schematic LCSC field is literally `OPEN`; the other 99 purchased references contain MPN, LCSC and footprint fields. The 12 copper features appropriately use PCB_FEATURE/N/A.

**Fix:** supply a verified exact Bourns SMCJ64CA LCSC identifier, or explicitly revise the sourcing requirement and record an authorized alternative source/part with a fresh rating/package review. Do not fill the field with another manufacturer's same-named part. [Bourns SMCJ](https://www.bourns.com/data/global/pdfs/SMCJ.pdf), p2, identifies the electrical variant; it does not supply an LCSC code. Package check passes; sourcing completeness does not.

### 8. NOTE — pin, topology, buck and ERC checks passed within their stated scope

**EVIDENCE:** KiCad CLI **9.0.6**, fresh ERC: **0 errors / 0 warnings**. Temporary outputs: `/private/tmp/litereview-r1-erc.rpt`, `/private/tmp/litereview-r1.net.xml`. Fresh/stored net-name and node sets are identical. All **112 physical references** reconcile to BOM MPN/LCSC/footprint fields and symbol-pin/footprint-pad sets. The only singleton pin net is U201.5, with the sole explicit NC marker correctly placed. Power flags are VIN_RAW, VIN_PROTECTED and GND. All five PDF pages were visually inspected.

| Sheet / reference | Verified physical pin mapping and connection | Datasheet evidence |
| --- | --- | --- |
| 02 / U201 | 1 BIAS=GND; 2 VCC→C206; 3 AGND=GND; 4 FB divider; 5 PG NC; 6 RT→33.2k; 7 EN/SYNC divider; 8/12 VIN_PROTECTED; 9/11 PGND=GND; 10 SW→L201/C205; 13 RBOOT→R204; 14 CBOOT→C205. No separate MODE pin or extra EP pin. | TI RevD p3, RJR0014A drawing; custom copper-pad numbering checked against top view. |
| 01,03 / U101,U301 | DBZ/SOT23: 1 K, 2 REF, 3 A; both anodes GND. | TI TL431 RevS p4. |
| 01 / Q101,Q102 | DPAK: 1 G, 2 D/tab, 3 S. Sources common; Q101 drain VIN_FUSED, Q102 drain VIN_PROTECTED. | Infineon 2016-05-31 pp1,8. |
| 01 / Q103,Q104,Q106 | SOT23: 1 B, 2 E=GND, 3 C. | MCC pp1–2; local manufacturer reading copy inspected after web fetch failed. |
| 01,03 / Q105,Q301 | SOT23: 1 B, 2 E, 3 C; emitters CTRL12 and VOUT_5V1 respectively. | Nexperia Rev8 pp2,9. |
| 03 / SCR301 | TO220: 1 K=GND, 2 A/tab=VOUT_5V1, 3 G=SCR_GATE. | ST Rev11 pp1,10–11. |
| 01 / D102–D105 | SOD123 pad1 K, pad2 A. D102/103 cathodes at source, anodes at respective gates; D104 K=CTRL12; D105 K=OVIN_K. | [Diodes DS18004 Rev38-2](https://www.diodes.com/_files/datasheets/ds18004.pdf), pp1–2,4. |
| 01 / D106,D101 | TVS3300: 4/5/6 IN, 1/2/3/EP7 GND. SMCJ64CA is bidirectional; SMC orientation is nonpolar. | TI TVS3300 p4/DRV drawing; Bourns SMCJ pp1–2. |
| 01,03,05 / F101,F301,J501,J502 | Fuses nonpolar 1/2, NANO2 451 lands; JST 1 positive, 2 GND, 3.96mm pitch and unnumbered boss. | [Littelfuse GD.12/01/25](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1), pp2,4; JST p4. |

**OBSERVATION:** the only forward force path is F101→Q101→Q102→buck. D101's 103 V specified pulse clamp is below the actual **150 V** FET rating; the historical 100 V mismatch is resolved, subject to real surge/ringing qualification. D102/103 nominal 12 V clamps fit ±20 V VGS; dynamic/hot margins remain part of finding 2. SCR301, U301 sensing, Q301 emitter and raw capacitors share VOUT_5V1 without a fuse. F301 alone separates VOUT_PI; no parallel wire bypass was found.

**CALCULATION / OBSERVATION:** buck target is `1 + 100k/24.6k = 5.06504 V`; RT gives approximately 400 kHz. C205=100 nF/16 V returns to native SW; R204=0 Ω; VCC has only 1 µF/16 V bypass; BIAS is grounded; EN uses 100k/24.6k and is not an 18 V UVLO. Feed-forward is 22 pF plus 1 kΩ. These connections agree with TI RevD pp3,13,29–33. Bank changes still require loop/startup verification under finding 1.

Input bank: four 10 µF/50 V 1210s, paired 100 nF/50 V bypass and 100 µF/50 V bulk. Raw output: six 47 µF/25 V 1206s plus two 1000 µF/10 V; Pi side: two 47 µF/16 V 1210s. C101's 8mm/3.5mm-pitch and C217/218's 10mm/5mm-pitch footprints match the [Panasonic FR-A table](https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1259.pdf), pp4,6. Remaining resistor/ceramic package codes match assigned metric footprints. L201's SRP1265A-6R8M body/lands match [Bourns Rev06/24](https://www.bourns.com/docs/product-datasheets/srp1265a.pdf), p1: 6.8 µH, 18 A saturation screen, 11.5 A thermal-current screen; neither rating limits fault current. Placement notes require dual input hot loops and Kelvin detector returns; actual placement is outside this schematic review.

Source provenance: manufacturer documents were referenced only; none modified or copied into CAD. Revisions/files/licenses/attribution are retained in the existing [Phase D register](../../../third_party/v1a_lite_phase_d/SOURCES.md), [C2 register](../../../third_party/v1a_lite_phase_c2/SOURCES.md) and [C3 manifest](../../../third_party/v1a_lite_phase_c3/DOCUMENT_MANIFEST.json). Manufacturer copyright remains; no redistribution license is asserted. This report adds no third-party design material.

**BLOCKING count: 4 — output voltage window/response; input fault containment; latch capture/retention; SCR drive/discharge stress.** ERC and mapping PASS do not establish electrical safety. No execution gate is advanced.
