# Gate 4b — independent schematic check

2026-10-03. Reviewer: Claude (cloud thread), independent of the capture worker.
Under review: PR #21, branch `feat/r2-testboard-capture`, commit `838a8a4`.
**PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION.** This is a paper check of the capture. It proves nothing about electrical behaviour; every bench test is still NOT RUN.

## Verdict

**PASS with 3 pre-layout checks.** Every item in the brief matches the frozen decisions. No wiring error was found. Before you start the PCB layout, confirm three pin details against the datasheets (section "Before layout" below). I could not open the datasheets from this environment, so I did not verify these three myself.

| # | Item | Result |
|---|---|---|
| 1a | R640 / R644 source-fault detector inputs wired | **PASS** |
| 1b | Test-hook wording no longer claims "already proven" | **PASS** |
| 2a | Architecture D: series pair, crowbar on VOUT_PROTECTED, bulk on VOUT_5V1, raw dump | **PASS** |
| 2b | Option A test hooks: manual trigger, manual reset, test points, jumpers | **PASS** |
| 2c | Power path VOUT_5V1 → Sheet 03 → VOUT_PROTECTED → 2 mΩ shunt / INA228 → LOAD_5V1 → J502 | **PASS** |
| 3a | Gate 3b source bound: TPS26630 timed isolation, 10–30 µF bank, L201 Würth 74437636351002 | **PASS** (biased capacitance OPEN) |
| 3b | Gate 4a aux fix: surge stopper + 12 V buck-boost upstream of the hold eFuse | **PASS** (pin check C2 open) |
| 4 | D101 SMCJ36CA, F101 Schurter 3403.0285.23, 9–26 V input window | **PASS** |
| 5 | Footprints on every part; ERC | **PASS** for footprints. ERC not re-run (see Method); my connectivity checks found no fault |

## Method (what I actually did)

1. **KiCad ERC could not be re-run.** KiCad 9 cannot be installed in this cloud container (the network proxy blocks the KiCad package archive; Ubuntu only ships KiCad 7, which cannot open KiCad 9 files). The worker's ERC 0 result is therefore **not independently confirmed**.
2. Instead I wrote my own parser for the six `.kicad_sch` files (wires, junctions, local and hierarchical labels, sheet pins, power symbols and library pin coordinates) and built the netlist from scratch.
   - **EVIDENCE:** my netlist matches `captured.xml` exactly. All 1021 component pins land in the same nets (207 nets, 366 physical references, 0 differences). So `captured.xml` truly represents the schematic, and the checks below use it.
3. Connectivity checks that cover the main ERC risks:
   - No net name is split across two disconnected nets. A split would mean a label typo or a broken hierarchy link.
   - Every hierarchical label reaches the root sheet.
   - No local label is connected to fewer than 2 pins.
   - 49 pins are single (unconnected). 37 are manufacturer NC/DNC pins. The other 12 are listed in the "Intentionally open pins" table below.
4. **Footprints:** every physical part has a footprint. For all 22 project footprints (`V1A_Qualified.pretty`), the pad numbers equal the symbol pin numbers exactly. Standard KiCad library footprints were checked by package type against the part (exposed pad present where the part has one).
5. Frozen values were compared with the Gate 4a freeze (`898759e`, `FREEZE_BOM.csv`).

## Item details

### 1a. R640 / R644 — PASS
- `/L201_IN` = L201.1, JP201.2, R640.1, TP202.1, PF4.1. R640 now senses the real inductor input after the JP201 force link, not the native switch node.
- `/VIN_PROTECTED` includes R644.1 (with U201.8/.12, C201–C204, D102.2).
- R640.2 → SW_HYS → U647.2 (ADG4612 isolation switch) → SW_SENSE → U640.3 (TLV3201 IN+). R644.2 → VIN_MON → U647.15 → VIN_SENSE → U642.3.
- **Option A boundary confirmed:** U640 OUT (SW_HIGH) goes only to R642 (hysteresis) and TP337. U642 OUT (VIN_GOOD_FAST) goes only to TP338. Neither drives SRC_TRIP. SRC_TRIP is driven only by U644.4 (from the J603 manual contact) and goes to U615.1 (OR gate) → TRUE_FAULT.

### 1b. Test-hook wording — PASS
Sheets 02, 03 and 05 read: `FUTURE ACCEPTANCE REQUIRED: "TEST HOOK — design proven on bench". UNTESTED CANDIDATE; evidence NOT RUN.` No sheet contains "already proven".

### 2a. Architecture D — PASS
- Series pair: Q301 drain = VOUT_5V1. The Q301 and Q302 sources are joined at PROT_MID (common-source, back-to-back, so both body diodes block). Both gates are on PROT_GATE, driven by U301 LTC7001 pin 6, with U301 TS = PROT_MID. Q302 drain → SERIES_OUT → JP301 → VOUT_PROTECTED. No bypass path exists.
- Protected crowbar: VOUT_PROTECTED → R308+R309 ‖ R310+R311 (4 × 33 mΩ, CALCULATED 33 mΩ total) → JP330 → Q303 CSD18540Q5B → GND.
- Raw dump: VOUT_5V1 → two strings of 6 × 33 mΩ (CALCULATED 99 mΩ total, i.e. the frozen "~100 mΩ") → JP331 → Q330 → GND.
- Bulk: 8 × 470 µF (C330–C337) plus 6 × 22 µF ceramics on VOUT_5V1. **Note:** 4 × 470 µF (C340–C343, 1.88 mF nominal) also sit on VOUT_PROTECTED. This is **not an error**: it is frozen row S03-10 ("measurement candidate"). The crowbar must discharge them, and Gate 4a already counts them.
- Negative-return diodes: D330 on VOUT_5V1 and D331 on VOUT_PROTECTED (STPS60H100CT).

### 2b. Option A hooks — PASS
| Hook | Refdes and pins |
|---|---|
| Manual source-fault trigger | J603.1 SOURCE_CONTACT → U644 (Schmitt) → SRC_TRIP, TP320 |
| Manual fault reset | J302.1 RESET_CONTACT |
| Main / series arm | J301.1 ARM_CONTACT, J604.1 SERIES_CONTACT |
| Manual rail-valid link | JP600: SAFE5 ↔ MANUAL_RAILS_VALID |
| Series-driver supply loss | JP660: SER_FEED ↔ SER_DRV |
| Force-current links | JP101, JP201, JP202, JP301, JP330, JP331, JP501 |

### 2c. Power path — PASS
VOUT_5V1 → Q301/Q302 → JP301 → VOUT_PROTECTED → R401 pin 1 (I+). Kelvin sense: R401.2 → SHUNT_KPLUS → R402 10 Ω → INA_IN_PLUS (U401.10). R401.3 → SHUNT_KMINUS → R403 → U401.9, with C401 100 nF across them. R401.4 (I−) → LOAD_5V1 = J502.1, U401.8 VBUS and JP501.1. J502.2 = GND. J502 = Phoenix 1776508.

### 3a. Gate 3b source bound — PASS, one OPEN
- Timed input isolation: U101 TPS26630 pin 12 SHDN = INPUT_SHDN. It is pulled low by Q304 (gate = FAULT_DRIVE from Sheet 03) and fed from MAIN_PERMISSION via R647 1 kΩ, with R648 10 kΩ to GND. Test pads are TP101 and TP312. MODE (pin 11) is open, which the freeze says selects latch-off (see check C1).
- Input bank on VIN_PROTECTED: C201 + C202 = 2 × 10 µF / 50 V X7R 1210, plus C203 and C204 at 100 nF. **CALCULATED nominal 20.2 µF**, inside 10–30 µF. **OPEN:** effective capacitance under DC bias at 26 V is not shown. X7R 1210 parts at about 50 % of rating can lose roughly half their value (ASSUMED; check the Murata curve), which could approach the 10 µF lower bound. This does not change the layout, but it must be measured or recalculated before the source-fault test.
- L201 = Würth 74437636351002, with project footprint `Wurth_74437636351002`. Pads match the symbol.

### 3b. Gate 4a aux fix — PASS
VIN_FUSED (upstream of the main eFuse U101) → D303 BAT46W → AUX_RAW → Q316 FDB33N25 (driven by U316 LT4363-1 surge stopper) → R332 0.33 Ω → AUX_LIMITED → U317 LTC3115-1 buck-boost (RUN = U316 ENOUT) → AUX_12V → D304 → AUX_PREHOLD → U327 TPS259470L hold eFuse → DRV_HOLD. So the auxiliary rail survives a main-eFuse shutdown, as frozen.

### 4. Input parts and window — PASS
- F101 3403.0285.23: VIN_RAW (J501.1) → VIN_FUSED. D101 SMCJ36CA: VIN_FUSED → GND, after the fuse.
- **CALCULATED** with the ASSUMED TPS2663 typical threshold of 1.20 V:
  - OVP trip = 1.20 × (348 k + 15.8 k) / 15.8 k = **27.6 V**
  - UVLO = 1.20 × (332 k + 54.9 k) / 54.9 k = **8.46 V**
  - Both are consistent with the 9–26 V normal range and the recorded 26.97 V minimum OVP trip. Datasheet tolerance limits were not re-derived here.

### 5. Footprints — PASS; JP201/JP501 procurement OPEN
All 366 physical references have a footprint. L201, D101 and F101 are now assigned. JP201 and JP501 use the project footprint `ForceLink_M4_P20` (custom M4 strap, 20 mm pitch, part `CUSTOM-FX-CU-01 RevA`). The footprint exists, but the strap is a home-made part that is not yet defined for purchase. Fix the strap dimensions before you place these two footprints.

## Intentionally open pins (not errors, recorded for layout)
| Pin | State |
|---|---|
| U101.11 MODE, U101.13 IMON | open (see check C1) |
| U316.10 FLT | open, aux fault flag not observed (could add a test pad; optional) |
| U318.3 EN, U402.3 EN (TPS70933) | open (see check C3) |
| U302.3 TEMP, U302.5 TRIM/NR | open (allowed for REF5025) |
| U306.7, U600.7 DELAY; U322.4, U323.4, U602.4 CT; U327.10 ITIMER | open (minimum/fixed delay) |
| U611.3, U612.3 /Q | unused flip-flop outputs |

## Before layout: what must be fixed or confirmed
Nothing needs re-wiring. Confirm these 3 pin details in the manufacturer datasheets. If any is wrong, the capture must be corrected before layout, because the pin assignment changes the copper.
- **C1. U101 TPS26630, pin 11 MODE left open.** Confirm in the TI TPS2663 datasheet pin-function and mode tables that "open" gives the intended overload response. Pin 11 is on page 01.
- **C2. U316 LT4363HMS-1 pinout.** The capture uses pin 7 = GND, 8 = UV and 9 = GND, citing ADI Rev C page 2. Confirm that pin 7 is not UV and pin 8 is not OV on the MS-12 package. If it were, UV would be grounded and OV tied to VCC: the aux surge stopper would never turn on, and all held rails would be dead. Page 03, aux block.
- **C3. U318 / U402 TPS70933, EN pin open.** Confirm the TPS709 EN pin has an internal pull-up, so an open pin means "enabled". If not, tie EN to IN. Pages 03 and 04.

## Can wait until after layout (does not change the copper)
- ERC 0 re-run on your Mac (KiCad 9.0.6): `kicad-cli sch erc hardware/kicad/V1A.kicad_sch`. My connectivity checks above found nothing, but this is a 1-minute confirmation.
- Biased effective capacitance of C201/C202 against the 10 µF lower bound (3a).
- Net classes: KiCad's XML shows 144 child-sheet nets as "Default". After "Update PCB from Schematic", check in Board Setup → Net Classes that HighCurrent, Switching and Kelvin are really applied.
- All OPEN items in GATE4B_CAPTURE.md: autonomous source-fault coverage, brownout/PG recovery, fault energy, thermal at 12 V, and fuse/TVS coordination. These are bench or analysis items. None is a schematic change today.

## How to follow this on the PDF (owner)
Open `docs/evidence/r2/gate4b/V1A_GATE4B_REVIEW.pdf`.
- **Page 1 (root):** find the Sheet 02 box. It has an `L201_IN` pin wired to the Sheet 03 box. This wire is the fix for finding 1a.
- **Page 3 (Sheet 02):** find L201 and JP201. TP202 sits on the node between them, labelled `L201_IN`.
- **Page 4 (Sheet 03, A0, zoom in):**
  - Locate R640 and R644 (top-left sensing front end). Follow each into U647 and then U640 / U642. Their outputs stop at TP337 / TP338; they do not reach SRC_TRIP.
  - Then locate the series pair Q301 / Q302 with JP301, the crowbar Q303 with R308–R311, and the raw dump Q330 with R380–R393.
- **Page 2 (Sheet 01):** U101 pin 11 (MODE) has a no-connect cross (check C1).
