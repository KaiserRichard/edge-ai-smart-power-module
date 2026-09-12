# R0 predecessor and manufacturer source audit

Date: 2026-09-11. Project: standalone Project II V1A. Baseline `a9fe716`; branch `docs/r0-r1-engineering-audit`; uncommitted research is part of this review state.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Finding and evidence boundary

**R0: CONDITIONAL PASS, sufficient to support documentary R1.** Three cached predecessor repositories, official Pi sources, monitor/protection references and several manufacturer converter references establish useful design directions. They do not establish board-level electrical validity or authorize R2. Component-level ratings, procurement, final protection and thermal acceptance remain open.

**DECISION:** all sources in this audit are **REFERENCE** only. No upstream circuit, CAD artwork, code or layout was ADAPTED or COPIED into project hardware/software. Potential future ADAPT candidates are identified below, but none is approved. Upstream originals and old review artifacts remain unchanged. New circuit-page renders are local review derivatives only, not project designs or redistributed manufacturer artwork.

Hashes, exact repository pins, license files and reviewed-document identities are in [source_manifest.json](evidence/r0/source_manifest.json). The earlier [environment record](evidence/r0/ENVIRONMENT_REVIEW.md), [Pi review](evidence/r0/RASPBERRY_PI_SOURCE_REVIEW.md) and [monitor/protection review](evidence/r0/MONITOR_PROTECTION_SOURCE_REVIEW.md) are preserved. Earlier 9–28 V/5.1 V/6 A examples remain candidate calculations. Manufacturer specifications outrank GitHub examples; application sections still require engineering verification.

## Predecessor register

| ID / source | Exact revision and rights inspected | Relevant original files | Applicability and use |
| --- | --- | --- | --- |
| A1 [Hat Labs SH-RPi-hardware](https://github.com/hatlabs/SH-RPi-hardware/tree/e82e3c9823bbcf94091b22927dd2e0da9cdfac8c) | `e82e3c9823bbcf94091b22927dd2e0da9cdfac8c`; schematic v2.0.1, 2024-09-25; `LICENSE.md` and schematic notices: CC BY 4.0, Hat Labs Ltd | `SH-RPi.kicad_sch`, `protection.kicad_sch`, `buck_8.8V.kicad_sch`, `buck_5V.kicad_sch`, `supercap.kicad_sch`, `control_mcu.kicad_sch`, `SH-RPi.kicad_pcb` | V1A protection/layout concepts; V1B/V2 charge/balance/power-path study. MCU/HAT behavior is future-only. REFERENCE; any later ADAPT must credit Hat Labs, link license/source and identify changes |
| A2 [1026-RPi-Power-Hat](https://github.com/wilsondr9999/1026-RPi-Power-Hat/tree/7af0c4d3cd5b66c6948879393b34898937d37348) | `7af0c4d3cd5b66c6948879393b34898937d37348`; schematic 1.0.0, 2025-05-18; hardware `LICENSE-CERN-OHL-W`: CERN-OHL-W-2.0; documentation/images `LICENSE-CC-BY-SA-4.0`; Dan Wilson | `KiCAD Project/Power Input.kicad_sch`, `KiCAD Project/5V Regulator.kicad_sch`, root project/PCB in that directory, `KiCAD Project/BOM/1026 RPi Power Hat.csv`, README | V1A input/buck/test-point concepts; USB hub/EEPROM/HAT is future-only. REFERENCE; later ADAPT needs applicable source/reciprocity notices and identified changes; no blanket license for unrelated embedded assets |
| A3 [SBCShop UPS-Hat-RPi](https://github.com/sbcshop/UPS-Hat-RPi/tree/14926b39f14ee541c9e5aa879d2b654a4e4605ad) | `14926b39f14ee541c9e5aa879d2b654a4e4605ad`; `Design Data/SCH UPS HAT OLED V2.pdf` sheets V2.4, 2022-06-08; root `LICENSE`: MIT, SB Components 2022 | Schematic PDF sheets 1/2 and 2/2; `INA219_UPS.py`; README; `documents/DS-HY2213_EN.pdf`, `DS-HY2120_EN.pdf`, `Ina219.pdf` are third-party reference copies | V1A measurement-boundary caution; battery/backup concepts for future V2, not a V1B supercap design. REFERENCE. Preserve MIT notice for software reuse; root MIT wording covers software/associated docs, not assumed blanket relicensing of vendor PDFs, fonts or hardware artwork |

Local checkouts match all three pins and are clean. Their commit objects were verified locally; this audit deliberately does not update them to remote HEAD. See the manifest's selected-file and license digests. `third_party/repos/` and `third_party/review/` are ignored caches, not files that a fresh clone will restore automatically.

## Actual blocks and constraints inspected

### A1 — Sailor Hat

- **OBSERVATION:** top-level sheet specifies a 10–32 V source concept feeding protection, a current-limited intermediate rail and a second 5-V buck. `buck_8.8V.kicad_sch` retains its filename and 8.8-V divider note while the top-level text mentions 9.0 V. Preserve that discrepancy; it is not a V1A input/output requirement.
- **Input block:** F701 `12T.40000063AG12S1B02`, D701 `5.0SMDJ33CA`, D702 `10S45SP`, L701 `PCAQ7060MW-102`, L702 `FXL0420-1R0-M`, input ceramics and damping R701. The schematic attributes its EMI prefilter concept to PMP15013 and 62AN101E. Those second-level sources were not independently audited here; their citation is not proof the filter fits V1A. Its diode protection is not a low-loss MOSFET reference.
- **First conversion/current limit:** U301 **RT6365**, L301 `SLO0530H3R3MTT`, D303 `SS56FL`, R301 **10 mΩ**, U302 **COS1333TR**, U303 **LMV321-TR**, and bias/current-output transistors. Notes describe 0.8-A input limit with jumper options 1.9/2.9 A and approximately 1.393-MHz switching. It cites an LMP8646 concept, but **does not actually populate LMP8646**. Input limiting is not precision output-current telemetry.
- **Second conversion:** U201 RT6365, L201 `FXL0420-1R0-M` (1 µH), D202 `MSK340A`, two 47-µF/6.3-V capacitors; notes specify input at most 9.0 V, approximately 4.98-V output and 1.841 MHz. A raw 24-V → 5-V use would require a new LC/diode/compensation/thermal design.
- **Storage/balancing:** C1004–C1006 are marked 3.0 V/20 F in series; three LMV321-TR/SS8050 shunt-balancing sections. The nominal series bank is 20/3 F, not 60 F. The sheet cites an EEVblog balancing discussion, not a manufacturer-qualified complete design. Cell limits, tolerances, leakage, balancing dissipation and stability must be reviewed independently for V1B. None of these values transfers to the teammate's subsystem.
- **Reusable boundary:** study modular sheets, startup/current-limit interactions and separation of sense/power routing. Potential later ADAPT is limited to understood functions after source/part verification. The two-stage storage chain, MCU, RTC and HAT interface are not V1A deliverables.

Existing schematic exports were reused; buck and supercap circuit renders were visually inspected. A full PCB current/thermal/EMI validation was **not** performed.

### A2 — 1026 power HAT

- **Input block:** F1 `1812L110/33MR` (1.1-A/33-V annotation), Q1 `BUK6D120-60PX`, D1 gate zener, D3 `SMF24CA`, L1 marked 22 µH/0.8 A/210 mΩ, J1 `S2B-XH-A-1`. These are a 24-V printer-oriented design's values, not a high-current 5-V distribution specification. A 25-W output at 24 V and 90% whole-module efficiency already needs about 1.157 A before startup considerations; do not reuse its 0.8-A-labelled filter or 1.1-A fuse rating as adequate.
- **Buck:** U1 **LM64440APPQRYFRQ1**, L2 `XGL4025-152ME` (1.5 µH), R6=56.2 kΩ/R8=13.7 kΩ divider; 2.1-MHz operation noted. BOM and schematic identify the 4-A part even though the footprint/library name contains **LM63460**. Verify value/order code, not footprint nickname. TI C6 confirms the 4-A/6-A family distinction.
- **Conflicting local guidance:** README says input above 22 V; regulator sheet annotates UVLO 20.2-V rising/14.6-V falling. Treat as unresolved source-specific claims, not a V1A cutoff setting. README's HAT+ assertion and 0x53 programming instructions do not establish compliance or automatic 5-A support for this repository.
- **Reuse:** input-fuse/reverse-MOSFET/gate-clamp arrangement and regulator layout principles are candidates for fresh engineering. The complete 4-A power chain and USB hub are not candidates for copying into 5-A V1A. Manufacturer C6 and the actual package/pinout control any later adaptation.

Power input and regulator exports/BOM were inspected, including visual review of the regulator circuit. No upstream build, ERC or DRC was rerun.

### A3 — SBCShop UPS

- **Battery-side sheet:** two-cell arrangement with **HY2213-BB3A** balancing parts, **HY2120-OB**, **AO4406A** switching/protection FETs, **SI2302** bleed switches, **INA219**, and R3 **0.1 Ω/1%/2512**. This is a battery UPS reference, not an INA228 or supercapacitor circuit.
- **Output sheet:** **APW7313**, L3 **4.7 µH/3 A**, feedback 68 kΩ/15 kΩ and the sheet's 0.925-V equation, nominally about 5.12 V. Two power-only USB-A outputs and Pi header share the 5-V rail. APW7313 electrical qualification is not completed here and it is not a recommended V1A candidate.
- **Measurement assumption:** INA219 senses the battery/input-side EB+ path, not isolated delivered 5-V load power. Python calibration lines 98–116 explicitly assume 0.1 Ω and a 2-A operating configuration, with overflow near 3.2 A. A 0.1-Ω shunt at 5 A would lose 0.5 V and 2.5 W; do not reuse it on the proposed 5-V/5-A output.
- **Assembly ambiguity:** R19/R20 are drawn as 0-Ω alternatives linking the display supply to 3.3/5 V. Both fitted would connect those rails; a population rule must be confirmed before reuse. The source PDF has two schematic pages followed by auxiliary content; page count is not the schematic sheet count.
- **Reuse:** high-side sensing and power-boundary interpretation are useful study material. Battery protection/balancing thresholds and direct supply connections require their own manufacturer/assembly review and are outside V1A. No code copied.

Both schematic sheets were visually reviewed against cached text; software calibration was read. No battery circuit is validated or recommended for the teammate.

## Manufacturer and official source register

All manufacturer documents below are copyrighted reference material, **not open-hardware licenses**. Preserve authorship/notices and link originals; no modified CAD/artwork redistribution is authorized. The manifest records local hashes where a cache exists and explicit remote-only limitations otherwise. Page numbers below are printed pages unless stated.

| ID / authoritative source | Exact inspected identity | Files/pages/sections, components and assumptions | Applicability |
| --- | --- | --- | --- |
| C1 [TPS56837 datasheet](https://www.ti.com/lit/ds/symlink/tps56837.pdf) | SLVSGM3B, Jan 2024 | `ti_converters/tps56837.pdf`; §§7.2–7.4, pp.17–24; TPS56837, 3.3-µH/500-kHz 5-V reference; 28-V IC ceiling and specific LC/layout constraints | V1A leading converter review |
| C1E [TPS56837 EVM](https://www.ti.com/lit/pdf/slvuce1) | SLVUCE1A, Aug 2023 | `tps56837_evm.pdf`; Table 2-1 p.2; layout pp.8–9; Fig.6-1 p.10; BOM pp.11–12. TPS56837RPAR, 744325330, two fitted 22-µF ceramics; 5-V/8-A evaluation board | V1A functional/layout reference; not a board rating |
| C2 [TPS56637 datasheet](https://www.ti.com/lit/ds/symlink/tps56637.pdf) | SLVSEG1A, Sep 2019 | `tps56637.pdf`; Fig.17 p.18; LC equations pp.19–20; layout pp.24–25; 5-V/6-A/500-kHz example | V1A alternative |
| C2E [TPS56637 EVM](https://www.ti.com/lit/pdf/slvube3) | SLVUBE3B, Jun 2021 | `tps56637_evm.pdf`; performance p.3, layout pp.6–7, schematic p.8, BOM p.9; IHLP3232DZER3R3M11 inductor | V1A alternative; EVM input table alone is not 5-V regulation below 5 V |
| C3 [LM61460 datasheet](https://www.ti.com/lit/ds/symlink/lm61460.pdf) | SNVSBD5D, Jul 2022 | Remote PDF inspected; §§9.2,11; Table 9-5 pp.43–44 and layout pp.48–49. 36-V/6-A class; 5-V/400-kHz example uses 4.7 µH | V1A higher-input-margin alternative |
| C3E [LM61460-Q1 EVM](https://www.ti.com/lit/pdf/snvu621) | SNVU621D, Jul 2021 | `lm61460_evm.pdf`; schematic p.8, layout pp.10–11, results pp.13–15, BOM pp.17–18; exact EVM is Q1, not automatically every catalog suffix | V1A layout/thermal study |
| C4 [TPS56528 datasheet](https://www.ti.com/lit/ds/symlink/tps56528.pdf) | SLVSBV3B, Nov 2016 | `tps56528.pdf`; §§8,10, pp.12–16; 18-V/5-A/650-kHz class, SO PowerPAD | V1A only if lower input/current scope approved |
| C5 [Richtek RT6365](https://www.richtek.com/assets/product_file/RT6365/DS6365-02.pdf) | DS6365-02, Mar 2020 | `RT6365_DS6365-02.pdf`; pp.1–2 features/package, application/inductor/diode/compensation/layout sections; 60-V/5-A asynchronous topology | V1A comparison; explains A1; V1B/V2 concept only |
| C6 [LM64440/60-Q1](https://www.ti.com/lit/gpn/LM64440-Q1) | SNVSBW0D, Jul 2026 | Remote PDF and TI part page; device variant/pin table, §§7–8. Actual A2 uses 4-A LM64440APP, not LM64460 | V1A audit rejection of undersized predecessor variant |
| M1 [INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf) | SLYS021A, May 2022 | `TI_INA228_SLYS021A.pdf`; pin/limits pp.3–7, accumulation §7.3, scaling §8.1.2 pp.30–32, filtering/application pp.33–38, layout p.39 | V1A preferred monitoring |
| M2 [INA228-family EVM guide](https://www.ti.com/lit/ug/sbou241e/sbou241e.pdf) | SBOU241E, Aug 2022 | `TI_INA228_EVM_SBOU241E.pdf`; Fig.6-1 p.23, layout/BOM pp.27–30; SENS063 reference, optional shunt/filter populations | V1A Kelvin/supply/layout reference |
| M3 [Digital power monitors guide](https://www.ti.com/lit/an/sboa511a/sboa511a.pdf) | SBOA511A, Sep 2021 | `TI_DIGITAL_POWER_MONITORS_SBOA511A.pdf`; pp.3–7 shunt tradeoffs/calibration/resolution | V1A selection method |
| M4 [INA226 datasheet](https://www.ti.com/lit/ds/symlink/ina226.pdf) | SBOS547C, Aug 2026 | `TI_INA226_SBOS547C.pdf`; limits pp.4–6, registers pp.22–28, layout p.31; no hardware energy accumulator | V1A justified fallback |
| M5 [Vishay WSL2726](https://www.vishay.com/docs/30131/wsl2726.pdf) | Document 30131, 29-Jun-2026 | `Vishay_WSL2726_30131_2026-06-29.pdf`; pp.1–2 ratings, order codes, component TCR and Kelvin pads | V1A 1/2/5-mΩ comparison; not a selected part |
| P1 [TPS2663](https://www.ti.com/lit/ds/symlink/tps2663.pdf) | SLVSE94G, Jun 2024 | `TI_TPS2663_SLVSE94G.pdf`; variant/limits, Fig.8-7 pp.20–22, transient/layout pp.37–39; external reverse-protection devices required | V1A input protection candidate |
| P2 [LM7480-Q1](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf) | SNOSD95C, Dec 2020 | `TI_LM7480-Q1_SNOSD95C.pdf`; limits pp.3–7, disconnect pp.15–16, layout p.35; back-to-back NFET path | V1A output boundary; future V2 reverse-feed study |
| P3 [LM74500-Q1](https://www.ti.com/lit/ds/symlink/lm74500-q1.pdf) | SNOSDB7, Dec 2020 | Remote datasheet p.1 and operating limits; reverse polarity **without** reverse-current blocking | V1A rejection of a mislabelled function |
| P4 [TPS25982](https://www.ti.com/lit/ds/symlink/tps25982.pdf) | SLVSEI3D, May 2026, as recorded in prior review | Prior remote inspection only; p.1/pp.21–22, 24-V operating ceiling and variant OV behavior | V1A fault-envelope screening; no fresh detailed review |
| F1 [TI LMP8646](https://www.ti.com/lit/ds/symlink/lmp8646.pdf) | SNOSC63B, Dec 2014 | `TI_LMP8646.pdf`; p.1 typical supercap/current-limit application, application section; LM3102 + LMP8646 example | V1B charging concept / A1 provenance; not INA228 telemetry or a V1A selection |
| F2 [ADI LTC3350](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc3350.pdf) | Rev D, Aug 2021 revision history | Remote pp.16–18 operation/PF/balancing, pp.21–22 current allocation, PCB considerations and application circuits | V1B/V2 charge/backup/OR-ing concepts only; no subsystem design |
| F3 [Eaton supercapacitor guidelines](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/technical/eaton-supercapacitor-application-guidelines.pdf) | PS-5006, effective Dec 2017 | Remote pp.2–3 charge/energy/series balancing; no capacitor model chosen | V1B/V2 conceptual reading only |
| H1 [Pi 5 USB-PD paper](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf) | Release 1, build 2026-03-17 `1026f0c6e305` | `raspberry-pi-usb-pd-release1.pdf`; printed pp.5,7–8; supply capability versus negotiation/configuration | V1A optional SBC load context; no mandatory USB-PD design |
| H2 [HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf) | Build 2024-12-05 `6df06cc-clean` | `raspberry-pi-hat-plus.pdf`; chapters 2–4,6; source-only behavior, standby, EEPROM/mechanics | Future HAT/WBR only; backfeed lesson useful to V1A, form factor not required |
| H3 [Pi power-supply source](https://github.com/raspberrypi/documentation/blob/5e2c40fe1125bb8ff7374de2c11c94761084eb1f/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc) | Commit `5e2c40fe1125bb8ff7374de2c11c94761084eb1f` | Cached `raspberry-pi-power-supplies.adoc`; power requirements/diagnostics; license text in `third_party/wbr_hat/raspberry_pi/LICENSE.md` | Optional V1A load reference; not a measured load profile |
| H4 [Legacy HAT guide](https://github.com/raspberrypi/hats/blob/348dbf88d870bf50d6b4f23dbe2b64d60363f23c/designguide.md) | Commit `348dbf88d870bf50d6b4f23dbe2b64d60363f23c` | `raspberry-pi-legacy-hat-designguide.md`; power/reverse-diode section | Historical future-HAT context only; file-specific reuse license not established, no adaptation |

H1/H2 PDFs identify CC BY-ND 4.0 plus colophon terms. H3's license introduction says Attribution while its linked license and full text are BY-SA 4.0; preserve the more specific text/notice and do not claim a permissive CAD license. The old `LICENCE` download failed; the existing `LICENSE.md` resolves the filename issue. H4 is reference-only with reuse rights unresolved. No legal certification is asserted.

## Conflicts, limits and inspection quality

1. **Source rating versus real regulation:** TPS56637 EVM table includes 4.5 V input while the datasheet's 5-V design uses 8–28 V; TPS56837 EVM schematic label also differs from its 5.5-V minimum performance table. Use dropout/UVLO and full-load conditions, not an IC minimum or schematic label, to set system Vin.
2. **Component labels versus manufacturer ratings:** A2's LM63460 library name is not its actual LM64440 part; C1/C1E inductor current labels differ. Confirm exact ordering codes against manufacturer limits before adapting any block.
3. **Protection scope:** GitHub fuse/reverse-diode/MOSFET arrangements are not proof of precise output OCP/OVP. P1's simplified no-external-FET circuit omits reverse functions; P3 explicitly lacks reverse-current blocking. A1's 3.3-V zener in its sensing circuit is not a 5-V load OV disconnect.
4. **No stored-energy promise:** standby software and a power-fail signal are not backup energy. A1/A3 storage and shutdown assumptions stay outside V1A. V1B interface values remain TBD.
5. **Manufacturer examples also need equation checks:** Eaton PS-5006 p.3 labels the larger series capacitor as receiving the larger voltage in its mismatch example. From equal series charge, the voltage across C1 is `Vs × C2/(C1+C2)`; the smaller capacitor receives more voltage during ideal series charging. Use this relation, cell specifications and leakage analysis rather than copying the inconsistent label. No V1B values are inferred.
6. **Acquisition limitations:** existing converter downloads were reused. LM61460's earlier download hit a file-size limit and remains remote-only. New attempts to cache F2/F3 failed with curl HTTP/2 code 92; official PDFs were read through the web tool instead. No TLS checks were disabled, no large PDF was added, and no complete new upstream repository was downloaded.
7. **Evidence integrity:** prior environment checks/exports and existing R0 notes were preserved. Visual inspection in this mission covered selected predecessor circuits and converter schematic/layout pages, not every trace or an independent electrical certification. Existing WBR statements referring to missing CAN/Linux reports remain historical incomplete evidence, explicitly marked as such; they do not block V1A R1.

## Reusable-block decision

**Recommended for later engineering adaptation review:** manufacturer's single-stage buck application and layout; INA228 high-side Kelvin circuit; coordinated fuse/reverse-input and output-disconnect functions. These require new ratings, interface and layout verification for V1A. No complete predecessor board is genuinely reusable unchanged for the proposed 5-A standalone design.

**Future-only:** Sailor Hat charge/balance/storage chain, SBCShop battery UPS topology, HAT EEPROM/mechanical rules, WBR CAN and supervisor sequencing. V1A–V1B electrical/interface questions are recorded in [requirements](00_REQUIREMENTS.md); no capacitor circuit or extra interface is implemented.

## Audit reproduction

Run `python3 scripts/check_r0_r1_docs.py` from the repository root. It checks authored relative Markdown links, all authored JSON manifests, selected source-file/license digests, exact predecessor commit objects and worktree cleanliness, and required deliverable presence. See [validation evidence](evidence/r0/R0_R1_VALIDATION.md) for executed checks and limitations. A missing ignored cache is a portability/evidence failure to report, not permission to overwrite preserved sources or silently update pins.
