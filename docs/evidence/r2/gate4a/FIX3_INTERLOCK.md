# FIX3-2 — rail supervision, reset, ARM and short lockout

**Analysis / capture candidate only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** No software participates. This pin contract replaces the old unimplemented FAULT_SET_N/RESET_SAFE_N logic. All gates use the separately supplied SAFE5 domain; DET5 and 3V3_AUX are monitored signals, not supplies for the new memory. Pin names refer to the stated package, not generic 74xx symbols.

## Supply, reference and hardware defaults

| Ref / MPN / value | Pins / nets |
|---|---|
| D600 B260-13-F | A=DRV_HOLD, K=SAFE_FEED; cathode marking defines polarity |
| R602 TNPW060347R0BEEA, 47 Ω | 1 SAFE_FEED, 2 SAFE_IN; limits separate reservoir charging |
| C600 GRM21BR71E105KA99L, 1 µF/25 V | 1 SAFE_FEED, 2 GND |
| C602 GRM32ER71H106KA12L, 10 µF/50 V | 1 SAFE_IN, 2 GND; require ≥5 µF effective |
| U600 TPS7A1601DGNR | 1 OUT=SAFE5; 2 FB=SAFE_FB; 3 PG=NC; 4 GND; 5 EN=SAFE_IN; 6 NC; 7 DELAY=NC; 8 IN=SAFE_IN; 9 EP=GND |
| R600 TNPW060332K4BEEA, 32.4 kΩ; R601 TNPW060310K0BEEA, 10 kΩ | R600 SAFE5→SAFE_FB; R601 SAFE_FB→GND; nominal 1.193×4.24=5.05832 V |
| C601 GRM32ER71H106KA12L, 10 µF/50 V | SAFE5→GND; effective ≥5 µF, within regulator stability requirement |
| R603 TNPW060310K0BEEA, 10 kΩ | SAFE5→GND; bleed/load included in ledger |
| D601 LM4040A25IDBZR | 1 K=REF_SAFE_2V5; 2 A=GND; 3=GND |
| R604 TNPW060310K0BEEA, 10 kΩ | SAFE5→REF_SAFE_2V5; reference biased from SAFE5, isolated from REF5025 |
| R605/R606 TNPW0603100KBEEA, 100 kΩ each | R605 REF_SAFE_2V5→REF1V25; R606 REF1V25→GND |
| R607 TNPW060390K9BEEA, 90.9 kΩ; R608 TNPW060310K0BEEA, 10 kΩ | R607 REF_SAFE_2V5→REF0V25; R608 REF0V25→GND; nominal 0.247770 V |
| C603 C1608C0G1H103J080AA, 10 nF/50 V | REF_SAFE_2V5→GND; shunt-reference capacitor, not REF5025 C302 |
| U602 TPS3808G50DBVR | 1 /RESET=CORE_POR_RAW_N; 2 GND; 3 /MR=SAFE5; 4 CT=NC (20 ms mode); 5 SENSE=SAFE5; 6 VDD=SAFE5 |
| R609 TNPW0603100KBEEA, 100 kΩ; C604 GRM188R71H104KA93D, 100 nF | R609 SAFE5→CORE_POR_RAW_N; C604 SAFE5→GND |

D600 prevents a lost/shorted DRV_HOLD from immediately emptying SAFE_IN. It does not preserve power for the main gate drivers if their own supply is shorted. At an **allocated** 8 mA safety-domain load, D600 drop≤0.5 V, R602 high corner, and DRV_HOLD=10.5 V, `SAFE_IN≥9.623013 V`. With effective C602≥5 µF, the capacitor-only interval to a 6 V LDO-input floor is **≥2.264383 ms**. Separately qualify regulator dropout, reverse leakage, charging, and actual current; no guaranteed 8 mA table sum is claimed.

At SAFE5=4.75 V and shunt upper 2.525 V, R604 supplies at least **221.918 µA**. The two reference divider loads total approximately 38 µA, leaving >180 µA before input/leakage load, above LM4040A25I's 80 µA minimum-current requirement. The shared shunt also receives positive-clamp current. T06F3 must bound its **combined**, rather than per-channel, current below 15 mA and its junction temperature below rating; use ≤10 mA as the development ceiling. REF1V25 ±15 mV and REF0V25 ±5 mV are explicit qualification allocations including all loading, drift, offset and leakage, not manufacturer reference accuracies.

### Comparator and analog-isolation pin templates

Every comparator in the next table is **TLV3201AIDBVR**: pin 1=listed output, 2=GND, 3=listed IN+, 4=listed IN−, 5=SAFE5. Each has its own indicated `GRM188R71H104KA93D` 100 nF supply bypass. Two-terminal resistor pin 1 is the first named net. Bottom resistors and the **100 kΩ at the comparator side of the analog switch** are included in the threshold calculations.

| Comparator / bypass | Sensed net; top/bottom refs and exact TNPW0603 MPNs | Switch → sense; 100 kΩ bleed | IN+ / IN− / output |
|---|---|---|---|
| U603 / C605 | SER_DRV; R610=69.8k `TNPW060369K8BEEA` to DH_DIV; R611=10k `TNPW060310K0BEEA` DH_DIV→GND | U650 ch1 DH_DIV→DH_SENSE; R612 `TNPW0603100KBEEA` DH_SENSE→GND | DH_SENSE / REF1V25 / SER_FAST_OK |
| U604 / C606 | DET5; R613=26.1k `TNPW060326K1BEEA` to DET_DIV; R614=10k `TNPW060310K0BEEA` DET_DIV→GND | U650 ch2 DET_DIV→DET_SENSE; R615=100k same MPN | DET_SENSE / REF1V25 / DET_FAST_OK |
| U605 / C607 | 3V3_AUX; R616=13.7k `TNPW060313K7BEEA` to A3_DIV; R617=10k same MPN A3_DIV→GND | U650 ch3 A3_DIV→A3_SENSE; R618=100k same MPN | A3_SENSE / REF1V25 / AUX_FAST_OK |
| U606 / C608 | SAFE5; R619=24.9k `TNPW060324K9BEEA` to S5_DIV; R620=10k same MPN S5_DIV→GND | U650 ch4 S5_DIV→S5_SENSE; R621=100k same MPN | S5_SENSE / REF1V25 / CORE_FAST_OK |
| U607 / C609 | BUCK_PGOOD; retain R317=10k pull-up to 3V3_AUX; R622=1k `TNPW06031K00BEEA` BUCK_PGOOD→PG_DIV; no bottom resistor | U651 ch1 PG_DIV→PG_SENSE; R623=100k same MPN | PG_SENSE / REF1V25 / PG_GOOD |
| U608 / C610 | VIN_PROTECTED; R624=18.2k `TNPW060318K2BEEA` to DIAG_DIV; R625=10k same MPN DIAG_DIV→GND | U651 ch2 DIAG_DIV→DIAG_SENSE; R626=100k same MPN | DIAG_SENSE / REF1V25 / DIAG_VIN_OK |
| U609 / C611 | **U201 native SW**, before any fixture isolation; R627=10k same MPN to NSW_DIV; no bottom resistor | U651 ch3 NSW_DIV→NSW_SENSE; R628=100k same MPN | REF0V25 / NSW_SENSE / SW_ZERO |
| U648 / C648 | VOUT_5V1; R629=10k same MPN to RAW_ZERO_DIV; no bottom resistor | U651 ch4 RAW_ZERO_DIV→RAW_ZERO_SENSE; R630=100k same MPN | REF0V25 / RAW_ZERO_SENSE / RAW_ZERO |
| U649 / C649 | VOUT_PROTECTED; R631=10k same MPN to PROT_ZERO_DIV; no bottom resistor | U652 ch1 PROT_ZERO_DIV→PROT_ZERO_SENSE; R632=100k same MPN | REF0V25 / PROT_ZERO_SENSE / PROT_ZERO |

U650/U651/U652 are **ADG4612BRUZ**, with C650/C651/C652 each `GRM188R71H104KA93D`, 100 nF SAFE5→GND. Common pins: 4 VSS=GND, 5 GND, 12 NC, 13 VDD=SAFE5. Channel mapping: ch1 IN/D/S=1/2/3; ch2=16/15/14; ch3=9/10/11; ch4=8/7/6. Every used IN=SAFE5; D=the pre-switch node in the table; S=the post-switch sense. U652 ch2 is assigned below to DRV_HOLD; every pin of its unused channels 3–4 is GND. This fully specifies all switch pins, including unused channels. No channel waits for READY, which would create a circular startup condition.

Clamp each pre-switch DIV node with a pair of **BAS116,215**: positive diode pin1 A=DIV, pin3 K=REF_SAFE_2V5; negative diode pin1 A=GND, pin3 K=DIV; pin2 NC on both. The pairs are D610/D611 (DH), D612/D613 (DET), D614/D615 (A3), D616/D617 (S5), D618/D619 (PG), D620/D621 (DIAG), D622/D623 (NSW), D624/D625 (RAW_ZERO), D626/D627 (PROT_ZERO). These are signal clamps, not force-current paths. ADG powered-off leakage ×100k gives a **0.300788 V** screen; partial supplies and capacitive injection remain T06F3. Maximum negative pin-current survival does not establish valid comparison.

For a divided channel: `Vrail,trip=VTH[(1+Ron/Rp)(1+Rt/Rb)+Rt/Rp]`; for a direct channel omit Rt/Rb. Nominal Ron=0 thresholds are **10.8475 / 4.83875 / 3.13375 / 4.67375 V** for SER_DRV/DET5/3V3_AUX/SAFE5, and **3.7525 V** for diagnostic VIN. Zero-node nominal threshold is **0.272547 V**. Independent resistor/Ron/reference corners are generated in FIX3_CALCULATIONS.json. Require the whole zero-node upper bound+measurement uncertainty≤0.30 V. These comparators assert invalid immediately; the slow supervisor is not credited for fast rail loss.

## Memory and gates — every pin specified

All following ICs are supplied **SAFE5**, with GND at protection signal ground. Every IC U610…U639 has its own capacitor of the same suffix **C710…C739**, each `GRM188R71H104KA93D`, 100 nF SAFE5→GND. U653…U656 use C753…C756 likewise. The differing C-series avoids collisions with comparator capacitors. No unused input floats.

**DCT8 flip-flop template:** SN74LVC1G74DCTR: pin1 CLK, 2 D, 3 /Q, 4 GND, 5 Q, 6 /CLR, 7 /PRE=SAFE5, 8 VCC=SAFE5. `/PRE` is **never asserted**. Fault/POR use only `/CLR`; deliberate reset is a clocked transfer. Thus no simultaneous asynchronous PRE/CLR state is used.

| Ref | CLK / D / /Q / Q / /CLR |
|---|---|
| U610 | RESET_DOWN / DIAG_READY / FAULT / NOFAULT / FAULT_CLEAR_N |
| U611 | RELEASE_CLK / SAFE5 / NC / RELEASE_SEEN / ARM_VALID |
| U612 | ARM_DOWN / RELEASE_SEEN / NOT_ARMED / ARMED / ARM_CLR_N |
| U613 | PG_SEEN_CLK / SAFE5 / NOT_PG_SEEN / PG_SEEN / ARMED |

**DBV5 AND/OR template:** SN74LVC1G08DBVR (AND) or SN74LVC1G32DBVR (OR), pin1 A, 2 B, 3 GND, 4 Y, 5 SAFE5. **Inverter template:** SN74LVC1G14DBVR, pin1 NC, 2 A, 3 GND, 4 Y, 5 SAFE5. Each next row specifies all signal pins; supplies/bypass are above.

| Ref / function / MPN suffix family | A / B / Y |
|---|---|
| U614 inverter / 1G14 | U303.1 OV_COMPARATOR / — / OV_RAW |
| U615 OR / 1G32 | SRC_TRIP / OV_VALID / TRUE_FAULT |
| U616 inverter / 1G14 | TRUE_FAULT / — / NO_TRUE_FAULT |
| U617 AND / 1G08 | CORE_POR_N / NO_TRUE_FAULT / FAULT_CLEAR_N |
| U618 AND / 1G08 | DRIVE_FAST_OK / DET_FAST_OK / RAIL_PAIR_A |
| U619 AND / 1G08 | AUX_FAST_OK / CORE_FAST_OK / RAIL_PAIR_B |
| U620 AND / 1G08 | RAIL_PAIR_A / RAIL_PAIR_B / RAILS_FAST_OK |
| U621 LTC6994IS6-1#TRMPBF | 1 IN=READY_IN; 2 GND; 3 SET=READY_SET; 4 DIV=READY_DIV; 5 SAFE5; 6 OUT=READY |
| U622 AND / 1G08 | RAILS_FAST_OK / CORE_POR_N / READY_IN |
| U623 AND / 1G08 | READY / NOFAULT / READY_NOFAULT |
| U624 AND / 1G08 | READY_NOFAULT / RESET_UP / ARM_BASE |
| U625 AND / 1G08 | ARM_VALID / ARM_UP / RELEASE_REQUEST |
| U626 AND / 1G08 | ARM_VALID / PG_POLICY / ARM_CLR_N |
| U627 AND / 1G08 | PG_GOOD / ARMED / PG_SEEN_CLK |
| U628 AND / 1G08 | OV_RAW / DET_FAST_OK / OV_VALID |
| U629 OR / 1G32 | NOT_PG_SEEN / PG_GOOD / PG_POLICY |
| U630 AND / 1G08 | ARMED / ARM_VALID / MAIN_PRE |
| U631 AND / 1G08 | MAIN_PERMISSION / PG_GOOD / SERIES_PRE |
| U632 AND / 1G08 | SERIES_PRE / RAILS_FAST_OK / RUN_GATE_LOGIC |
| U633 AND / 1G08 | FAULT / CORE_POR_N / DISPOSAL_LOGIC |
| U634 inverter / 1G14 | MAIN_PERMISSION / — / BUCK_DISABLE |
| U635 AND / 1G08 | SW_ZERO / RAW_ZERO / ZERO_PAIR_A |
| U636 AND / 1G08 | PROT_ZERO / DIAG_VIN_OK / ZERO_PAIR_B |
| U637 AND / 1G08 | ZERO_PAIR_A / ZERO_PAIR_B / DIAG_ZERO |
| U638 AND / 1G08 | DIAG_ZERO / READY / DIAG_PRE |
| U639 AND / 1G08 | DIAG_PRE / NOT_ARMED / DIAG_BASE |

U621 timing resistors: R700=`TNPW0603153KBEEA`, 153k READY_SET→GND; R701=`TNPW0603191KBEEA`, 191k SAFE5→READY_DIV; R702=`TNPW0603100KBEEA`, 100k READY_DIV→GND. DIV ratio 0.343643 selects code5, NDIV32768; nominal delay **100.27008 ms**, full-temperature ±3% plus resistor drift gives **97.006665…103.549288 ms**. Falling RAILS_FAST_OK also directly removes series permission, and READY's falling propagation must be included in the source permission path. T15F3 requires rail-loss→SHDN crossing≤1.30 µs; the LTC6994 prompt-edge typical figure is not substituted for that application maximum.

### Manual inputs, driver outputs and diagnostic source

U653/U655=`LTC6994IS6-2#TRMPBF` (both-edge debounce): pins 1=ARM_CONTACT/RESET_CONTACT respectively, 2=GND, 3=ARM_SET/RESET_SET, 4=BUTTON_DIV, 5=SAFE5, 6=ARM_UP/RESET_UP. R703/R704=`TNPW0603244KBEEA`, 244k respective SET→GND. R705=`TNPW0603255KBEEA`, 255k SAFE5→BUTTON_DIV; R706=`TNPW0603100KBEEA`, 100k BUTTON_DIV→GND. Code4, NDIV4096 gives **19.98848 ms** per edge, not a guessed RC debounce. U654/U656 are 1G14 inverters, ARM_UP→ARM_DOWN and RESET_UP→RESET_DOWN, using the inverter template.

R707/R708=`TNPW060310K0BEEA`, 10k SAFE5→ARM_CONTACT/RESET_CONTACT. J601/J602 use Phoenix **1776508** headers and **1777989** plugs: pin1 respective CONTACT, pin2 GND. External normally-open dry contacts close 1–2; **C&K 7201SYZQE** external toggle, common terminal2 to GND and terminal1 to CONTACT; terminal3 and the unused pole terminals4/5/6 NC; verify the numbered drawing and continuity; no voltage source connected. Held buttons cannot generate a fresh rising press edge after recovery. Contacts are outside any force-current circuit.

R709=`TNPW06031K00BEEA`, 1k RUN_GATE_LOGIC→RUN_GATE; R710=`TNPW060310K0BEEA`, 10k RUN_GATE→GND. U301.4=RUN_GATE. Change U301.2 VCCUV from GND to R711=`TNPW0603143KBEEA`, 143k to GND: **10.01 V nominal rising UVLO**, secondary to the fast 10.85 V monitor, not a guaranteed 10.5 V floor. U301.1=SER_DRV, .3/.11 GND, .5 OVLO=GND, .6 TGDN=PROT_GATE, .7 TGUP→R304100Ω→PROT_GATE, .8 TS=PROT_MID, .9 BST=PROT_BST, .10 NC. C301/R305 retain the round-2 pin map; D302 anode moves to SER_DRV. C306/C309, the U301 supply bypasses, also move to SER_DRV. Their other terminals remain GND. The manufacturer's UVLO action pulls TGDN to TS; actual loss-to-current-off remains a measured endpoint.

R712=`TNPW06031K00BEEA`, 1k DISPOSAL_LOGIC→DISPOSAL; R713=`TNPW060310K0BEEA`, 10k DISPOSAL→GND. U315/U330=`UCC27511DBVR`: .1 VDD=DRV_HOLD, .2 OUTH through R306/R3841Ω to their gate, .3 OUTL directly gate, .4 GND at respective source Kelvin, .5 IN−=GND, .6 IN+=DISPOSAL. Their existing bypasses/gate bleeds and both ballast paths remain. FAULT stays latched even when DET5 or AUX3V3 disappears; disposal is **not** gated with DET_FAST_OK or BUCK_PGOOD. At total depletion, driver UVLO and gate bleeds default the power gates off; T04/T07 still prove the energy has already been disposed.

Q601=`2N7002,215`: .1 G=BUCK_DISABLE_GATE, .2 S=GND, .3 D=U201.7 EN/SYNC. R714=`TNPW06031K00BEEA`, 1k BUCK_DISABLE→gate; R715=`TNPW0603100KBEEA`, 100k gate→GND. Keep U101.16 PGOOD and R206/R207's existing EN divider: Q601 provides a parallel diagnostic disable, never drives a voltage into PGOOD. SHDN's passive default also prevents new main power when SAFE5 is absent.

D602=`B260-13-F`: A=DIAG_FEED, K=VIN_PROTECTED; R716=`TNPW0603470RBEEA`, 470Ω SAFE5→DIAG_FEED. The diagnostic is current-limited, reverse blocked, and continuously available with main OFF. Require diode drop≤0.5 V and total healthy disabled-buck leakage≤0.10 mA for a reliable healthy result; **failure to reach DIAG_VIN_OK inhibits reset**, never assumes repair. At SAFE5≤5.25 V, ignoring the helpful diode drop, `Iprobe≤5.25/(470×0.997375)=11.199612 mA`. Raw capacitor charging is bounded by that current; it is not a high-power retry. Count this replenishment in whole-event Q/work where its current crosses the chosen measurement boundary; it is an explicitly separate auxiliary diagnostic source, not zero.

**Hardware separation of diagnostic and RUN:** continuous diagnosis would recharge a failed output and spoil the ≤0.3 V tail. S601 is an external **C&K 7201SYZQE DPDT ON–ON** service switch, used only at 5.25 V/12 mA maximum. First pole: terminal2 common=DIAG_FEED (D602 A), terminal1=R716 output, terminal3=NC. Second pole: terminal5 common=SERVICE_RUN, terminal4=GND, terminal6=SAFE5. DIAG closes2–1 and5–4; RUN closes2–3 and5–6. Verify terminal orientation/continuity against the manufacturer's drawing before wiring; never infer switch position from lever direction. The first pole disconnects the probe in RUN; the second prohibits ARM in DIAG.

Board connections are JP601 Phoenix1776508/1777989, .1=R716 output/.2=DIAG_FEED; J603 same part, .1=SAFE5/.2=GND; J604 same part, .1=SERVICE_RUN/.2=GND. Wire these to the explicitly named switch terminals, with J604.2 a local signal return only. R719=`TNPW060310K0BEEA`10k SERVICE_RUN→GND. U658=`SN74LVC1G17DBVR`: .1 NC/.2 SERVICE_RUN/.3 GND/.4 SERVICE_RUN_FAST/.5 SAFE5; C758100nF bypass. U657=`SN74LVC1G08DBVR`: .1 ARM_BASE/.2 SERVICE_RUN_FAST/.3 GND/.4 ARM_VALID/.5 SAFE5; C757100nF bypass. Both capacitors use the standard GRM188 part. Missing service cable defaults RUN low. These contacts are not a substitute for physically removed main-force links during diagnosis.

DIAG_READY is sampled by deliberate RESET while S601 is in DIAG; NOFAULT retains the result when switching to RUN. Require measured break-before-make and no contact overlap in T15F3. A stuck/welded probe contact invalidates integrated energy accounting; verify its open circuit before every fault run. Loss of all power clears NOFAULT and requires new diagnosis/RESET/ARM. This closes the ordinary service-selection interlock, not a single-fault-tolerant safety certification.

## State table and sequence

| State / event | NOFAULT / ARMED | SHDN / series | Dumps | Reset / next action |
|---|---|---|---|---|
| No power / cold start / partially valid supplies | 0 after POR; ARMED=0 | Passive SHDN low; RUN pull-down; LTC/UCC UVLO | Off until valid core; safe startup may assert disposal with no load attached | No ARM until valid reference, all rails and ≥97 ms READY delay |
| Valid rails, diagnostic link fitted, main force physically absent | 0 / 0 | OFF; Q601 disables buck | FAULT=1; valid held supply dumps outputs | Wait until diagnostic VIN high and native SW/raw/protected <0.3 V; press RESET |
| Persistent low-resistance VIN–SW short | 0 / 0 | OFF | Latched as above | VIN and SW cannot satisfy opposite voltage tests simultaneously; reset D=0 |
| Accepted RESET press, then release | 1 / 0 | OFF | OFF | Switch S601 to RUN while main force remains absent; verify probe disconnected; reconnect main source; ARM must be released, then pressed |
| Armed startup, PG never high yet | 1 / 1 | Main allowed; series OFF | OFF | Q601 releases EN; VIN_SEEN and PG_SEEN record actual transitions; no fictitious PG |
| Armed and genuine PG high | 1 / 1 | Main and series ON | OFF | Normal state |
| Ordinary PG loss after PG_SEEN | 1 / 0 | OFF | OFF | Fresh ARM edge required; PG recovery alone cannot clock U612 |
| SRC_TRIP or valid OV, including simultaneous PG loss | 0 / 0 | OFF asynchronously | Both ON while core/drive usable | Fault-clear has priority over clock; RESET alone cannot defeat present diagnostic fault |
| DET5 or 3V3_AUX loss, SAFE5 held | Previous NOFAULT / 0 | OFF via fast monitor and READY fall | Existing true fault remains latched; ordinary rail loss alone creates no crowbar command | Rails must requalify; held ARM cannot reconnect |
| DRV_HOLD loss / whole input loss | Until core POR, then 0 / 0 | Fast removal, then driver UVLO/passive OFF | Only qualified stored-energy interval credited | No recovery restart; full power loss requires new diagnosis/RESET/ARM |
| RESET held or bouncing through rail recovery | 0 or accepted NOFAULT / 0 | OFF | Follows latched fault | RESET_UP low holds ARM_INVALID; debounced fresh sequence required |

The low-resistance-short rejection is a real voltage test, not an inference from a discharged output. With diagnostic VIN lower bound about 3.69 V, zero-node upper bound below 0.281 V and probe≤11.200 mA, a **hard short (and any DC path below the generated approximately 305 Ω bound)** cannot pass. Exact bound uses generated corners. This does not diagnose intermittent, temperature-dependent or high-voltage-only failures. A removed or open SW sense lead is not a proof of repair: continuity inspection and T16 are mandatory. A spare diagnostic jumper is not permission to bypass the service sequence.

## Timing, current and bench closure

Fast-loss allocation: analog divider/switch/overdrive/comparator≤1.00 µs, direct logic≤0.10 µs, SHDN crossing≤0.20 µs; **≤1.30 µs to SHDN**, plus TPS table 1.5 µs, physical commutation0.40 µs and Ut0.025 µs → **≤3.225 µs conditional source-current endpoint**. Series gate/current endpoint allocation is **≤3.0 µs from loaded-rail threshold**. The minimum is conservatively zero; no application maximum is fabricated from typical supervisor or driver curves. U659 now directly ANDs MAIN_PRE with RAILS_FAST_OK. Source removal therefore does not depend on an unspecified maximum for U621’s prompt edge. READY still clears ARM and enforces the full recovery delay.

At 300 µF and a revised **45 mA total held-domain ceiling**, natural capacitor droop is ≤150 V/s. A 0.20 V rail reserve is 1.33 ms, far longer than the microsecond removal allocation. This only bounds ordinary source removal/hold discharge. Forced ideal shorts at a driver pin do not obey that slope; T15F3 explicitly tests hard rail collapse and verifies U301 UVLO/TGDN, UCC outputs and each actual VGS. D660/C660 below preserve U301 supply during an upstream DRV_HOLD short. A direct short of SER_DRV itself still exercises U301 UVLO/held-bootstrap action; no delay bound for that internal fault is inferred. If T15F3 cannot establish turn-off, a further gate-clamp revision is required before integrated use. Default-off logic by itself cannot guarantee a failed gate-driver power circuit.

The following original partial-commit screen is retained for provenance and superseded by the recomputed reservoir/headroom screen below. The old total 40 mA allocation was replaced for this candidate by **45 mA**, including the new supply, references, monitors, timers, pull-downs, diagnostic (when fitted) and fixture bleeders. Retired AHCT translators remove their 3 mA TTL-high budget. These are allocations to measure, not a measured load saving. With the previous Ccharged≤600 µF and ramp≤10 V/s, the revised converter input screen is `12.311325×(0.045+0.006+0.000610)/(7.5×0.75)+0.005 = 117.957775 mA`, below the transferred 135.013501 mA stopper floor. U327 flat-loss screen becomes **0.627878 W**, giving **116.777°C** at the earlier 70°C/74.5°C/W sensitivity. Actual thermal and transient startup remain T07D; the narrow margin is not a hot qualification. Hold to 10.5 V becomes **4.097045 ms** at the earlier 11.121343 V start, 300 µF and 2.036 µC gate allocation.

**T15F3 PASS:** exhaust the table with both buttons held/released/bouncing, all rail orders, PG loss simultaneous with a fault, slow ramps/intermediate plateaus and abrupt source/rail removal. No nonzero source/series permission until qualified and deliberately armed; fault memory never clears on PG/rail return; persistent native VIN–SW shorts of 0/1/10/100 Ω reject RESET, including with fixture native-SW isolation open. Healthy reset requires measured low nodes and charged diagnostic VIN. Start diagnosis at ≤1 mA on the isolated coupon (healthy acceptance may then be unavailable); qualify the selected ≤11.200 mA probe before using RESET acceptance. Record real SHDN, input/series current, both VGS, UVLO/CORE_POR and every logic state. Check recovery/removal timing and minimum asynchronous pulse widths against SCES794G; do not call a Boolean state simulation an analog-race proof.

**T06F3/T07F3:** measure the complete reference/clamp/isolation pin currents, effective capacitors, supply independence and total 45 mA ledger; SAFE5 and reference must remain valid through the measured cutoff/disposal interval. Qualified full-energy fault disposal remains T04/T07/T09, not permission from a 4.10 ms capacitor calculation. Main and series removable force links make these coupon tests possible without a load-power path. All results **NOT RUN**.

**Retire conflicting controls:** U304/U305/U308/U309/U310/U311/U312/U313/U314/U319/U320/U324/U325/U326, their obsolete delay/pull-up paths and C310/C311/C312/C313/C314/C315…C325/C360…C363/C371/R318/R319/R320/R368/R369/R394/R395 become DNP. U322/U323 remain optional observation-only test coupons, disconnected from permissions. Retain U302/U303/U321 detector; U321.1 IN1 now uses DET_FAST_OK through R717=`TNPW06031K00BEEA`, 1k, with R718=`TNPW0603100KBEEA`100k IN1→GND. No BUCK_PGOOD qualification of the OV latch. R316 may remain as observation-only DET_PG pull-up to3V3_AUX; its net is isolated from old SUPPLY_OK logic. Native-CAD reconciliation remains T16, not performed here.

**Primary sources:** [TPS7A16 SBVS171F](https://www.ti.com/lit/ds/symlink/tps7a16.pdf), pp4–6,11,13–15; [TPS3808 SBVS050N](https://www.ti.com/lit/ds/symlink/tps3808.pdf), pp3–7,10–12; [LM4040 SLOS456Q](https://www.ti.com/lit/ds/symlink/lm4040.pdf), DBZ pins and A25I current/accuracy table; [TLV3201 SBOS561C](https://www.ti.com/lit/ds/symlink/tlv3201.pdf), pp3–6; [ADG4612 Rev0](https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf), pp7–10,15–17; [SN74LVC1G74 SCES794G](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf), pins/function and timing tables; [LTC6994 Rev C](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC6994-1-6994-2.pdf), pp3–5,10,12–16; [LTC7001 Rev G](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf), pp3,9,12; [UCC27511 SLUSAW9F](https://www.ti.com/lit/ds/symlink/ucc27511.pdf), pp3–7,10–13. Functional blocks referenced/adapted with separate SAFE5, loaded monitors and clocked service reset; no upstream/CAD copying. Full provenance is in third_party/gate4a_fix3/SOURCES.json.

## Resume correction — complete fast permission and release recovery

**DECISION:** the following additions are part of the active circuit, not optional changes after a failed test. Every listed IC gets the standard 100 nF GRM188R71H104KA93D capacitor C759/C760/C761/C762/C763 for U659…U663 respectively, SAFE5–GND.

| Ref / exact MPN | All pins / new nets | Purpose |
|---|---|---|
| U659 SN74LVC1G08DBVR | 1 MAIN_PRE; 2 RAILS_FAST_OK; 3 GND; 4 MAIN_PERMISSION; 5 SAFE5 | Direct fast rail veto before SHDN |
| U660 LTC6994IS6-1#TRMPBF | 1 RELEASE_REQUEST; 2 GND; 3 RELEASE_SET; 4 RELEASE_DIV; 5 SAFE5; 6 RELEASE_CLK | Prevent simultaneous U611 clear release and clock |
| R720 TNPW0603100KBEEA, 100 kΩ | RELEASE_SET–GND | 1.024 ms nominal release qualification |
| R721 TNPW0603249KBEEA, 249 kΩ | SAFE5–RELEASE_DIV | DIVCODE3 top |
| R722 TNPW060369K8BEEA, 69.8 kΩ | RELEASE_DIV–GND | Ratio 0.218946, NDIV512 |
| U661 SN74LVC1G14DBVR | 1 NC; 2 SERVICE_RUN_FAST; 3 GND; 4 SERVICE_DIAG; 5 SAFE5 | Reset requires physical DIAG selection |
| U662 SN74LVC1G17DBVR | 1 NC; 2 CORE_POR_RAW_N; 3 GND; 4 CORE_POR_N; 5 SAFE5 | Schmitt receiver for the open-drain POR ramp |
| U663 SN74LVC1G08DBVR | 1 DIAG_BASE; 2 SERVICE_DIAG; 3 GND; 4 DIAG_READY; 5 SAFE5 | Reject RESET in RUN |

U660 release interval is **0.990673…1.057489 ms** at the declared resistor and timer corners, far longer than the flip-flop recovery requirement (TI SCES794G p7). U611.6=/CLR=ARM_VALID; U611.1 now receives the delayed RELEASE_CLK. A button held down through recovery leaves RELEASE_REQUEST low, so no release memory is set. The earlier simultaneous-clear/clock construction is withdrawn. This corrects a specific digital race; sweep arbitrary near-coincident fault/reset/PG transitions in T15F3 to verify real asynchronous pulse widths and analog behavior.

**Regulator headroom:** change **R312** (U306 DET5 feedback top) and R600 to `TNPW060332K4BEEA`, 32.4 kΩ; retain both 10 kΩ bottoms. Their nominal output is 5.05832 V. Using TPS7A16 overall accuracy, FB current and independent ±0.2625% resistors gives **4.934070…5.183488 V** (generated exact values control). This fits the allocated 4.75…5.25 V domain and exceeds the 4.916714 V worst detector-release screen. Include load/line/dynamic errors only once according to the feedback table conditions; actual regulation remains T07F3. The old nominal-5.0 V selection could fail to release the 4.9167 V monitor at its low corner. G50 POR rising can require 4.65×1.02×1.025=4.861575 V; it also fits the revised static supply screen. Do not assert release at every arbitrary 4.75 V input in a sweep.

### Series-driver reservoir and charging headroom

D660=`B260-13-F`, anode DRV_HOLD, cathode **SER_DRV**. C660=`GRM32ER71H106KA12L`, 10 µF/50 V, SER_DRV–GND, require ≥5 µF effective. R723=`TNPW060310K0BEEA`, 10 kΩ SER_DRV–GND. U301 VCC, its two local bypasses and D302 anode use SER_DRV; U603 now senses SER_DRV with the existing 69.8k/10k/100k network. U315/U330 continue to use DRV_HOLD. No changed ground or TS connection. D660 blocks discharge of C660 into a shorted upstream driver rail while SAFE5 commands turn-off. Main and both disposal commands still default low after total depletion.

**CALCULATION / allocations:** at the lowest monitor screen 10.667678 V, C660≥5 µF, local driver/bleed load≤5 mA, removal≤3 µs and additional turn-off/recovery charge≤0.20 µC, `ΔV≤(5mA×3µs+0.20µC)/5µF=0.043 V`. SER_DRV therefore remains ≥10.624678 V during that conditional removal interval. Include every local capacitor and gate-charge path in T15F3; this calculation does not promise immunity to a short directly at U301 VCC or a failed driver.

To recover the diode headroom, change U317 feedback bottom **R341** to `TNPW060388K7BEEA`, 88.7 kΩ (top R340 remains 1 MΩ). Same F2-05 compensation topology. Recompute converter/startup/thermal and repeat T07E; no previous stability result exists to transfer. Require D304≤0.50 V and D660≤0.20 V at their actual measured load/temperature. These are application allocations, not B260 forward-voltage guarantees. The resulting converter minimum minus both drops must exceed 11.030525 V before ARM. If diode drops or dynamic regulation fail this inequality, the circuit must be revised before integrated power; do not bypass the monitor.

The current ledger remains **≤45 mA total**, now explicitly including C660 charging, its bleed, all new logic/sensors and the fitted discharge adapters. Ccharged≤600 µF includes C660 and all new SAFE capacitors; it is not 600 µF plus these parts. Current-ledger and capacitor margins are measured in T07F3. The calculator updates auxiliary input current, flat charger dissipation and hold time with the new converter and a **10.70 V DRV_HOLD floor** to allow 0.20 V at D660. These remain conditional; the floor of the monitored SER_DRV is 10.5 V.

**T15F3 capture boundary:** reserve separate removable main-source and series-force links, pin-paired sense for SER_DRV, DRV_HOLD, SAFE_IN/SAFE5, CORE_POR_RAW_N/N, RAILS_FAST_OK, RELEASE_REQUEST/CLK, NOFAULT, ARMED, all zero/diagnostic nodes and actual SHDN/RUN. With force links removed, rail sequencing, diagnostic shorts and held-button tests contain no drain-energy path. Thus the selected interlock can be captured for isolated evaluation while application loss timing is unmeasured. Only after T15F3 passes may the integrated fault test use it. No hard rail-collapse or loaded-current result is asserted here.

**Separate upstream monitor:** keep fast detection of DRV_HOLD loss even while C660 keeps SER_DRV high. U664=`TLV3201AIDBVR`: pin1 DRV_FAST_OK, 2 GND, 3 DRV_SENSE, 4 REF1V25, 5 SAFE5; C664 standard 100 nF. R724=`TNPW060369K8BEEA` 69.8k DRV_HOLD–DRV_DIV; R725=`TNPW060310K0BEEA` 10k DRV_DIV–GND; R726=`TNPW0603100KBEEA` 100k DRV_SENSE–GND. U652 ch2: .16 IN2=SAFE5, .15 D2=DRV_DIV, .14 S2=DRV_SENSE. D628/D629=BAS116,215 use the standard positive/negative clamp pair on DRV_DIV, with both pin2 NC. U665=`SN74LVC1G08DBVR`: .1 SER_FAST_OK/.2 DRV_FAST_OK/.3 GND/.4 DRIVE_FAST_OK/.5 SAFE5; C765 standard 100 nF. Thus neither an upstream rail short nor depletion of the isolated driver reservoir retains permission. The pin table's U603 output is SER_FAST_OK; DRIVE_FAST_OK is driven only by U665.

**Reference accuracy accounting:** the generated LDO screen uses the full-condition ±2% overall-accuracy row around 1.193 V, resistor corners and ±0.1 µA FB current (TI SBVS171F p6). The separately listed 1.169…1.217 V row is at 25°C and is not independently added to overall accuracy. All monitor reference/offset/leakage allowances still require T06F3; no threshold-crossing result is fabricated.

**Updated numerical screen:** converter 11.883849…12.593099 V; initial SER_DRV≥11.183849 V under the diode allocations; branch startup current≤120.543079 mA; charger flat-power screen0.642248 W and117.847478°C at70°C/74.5°C/W; capacitor hold4.513751 ms. These replace the partial commit’s 117.958mA/116.777°C/4.097ms values.


## Final resume — loaded diagnostic and capture reconciliation

**OBSERVATION / correction:** the earlier 4.70 kΩ feed omitted substantial known loads. At VIN_PROTECTED, R624/R625/R626, R644/R645/R652, the fitted RFD01 10 kΩ bleeder, R106/R107 66.2 kΩ PG divider, R206 100 kΩ with Q601 on, and R108 100 kΩ with FLT sinking are all loads. Their independent low-resistance envelope is calculated in `diagnostic_feed`. Add **100 µA** for all other semiconductor/capacitor/PCB/probe leakage, rather than counting these known resistors inside that allowance. The old feed fails healthy RESET even before considering a damaged buck. This was a construction error, not a bench result.

**DECISION:** R716 is now **470 Ω TNPW0603470RBEEA**, with the same pin/net map. The generated healthy lower bound exceeds the maximum diagnostic threshold; maximum feed power is below 59 mW, within the TNPW0603 general-mode 110 mW at 70°C with its film-temperature conditions (Vishay28758 pp1–3). The short-probe ceiling becomes 11.200 mA and the guaranteed DC-short rejection screen about 305 Ω. The mandatory 0/1/10/100 Ω cases remain inside it; no 1 kΩ rejection is claimed. D602 must meet the allocated ≤0.50 V drop at its actual current and temperature; measure the remaining leakage and healthy margin in T15F3. An excessive diode drop/leakage fails safely by preventing RESET.

**Power accounting:** the 8 mA SAFE5 hold calculation applies to RUN with the probe physically disconnected. DIAG instead allocates ≤20 mA for the safety domain, including a shorted probe, within the unchanged ≤45 mA total held-domain ceiling. DIAG has no main force source, so no high-energy ride-through claim uses the 8 mA result during that state. T07F3 must measure both ledgers. S601's low-current contact screen is 5.25 V/12 mA (63 mW); this remains far below its logic-contact rating, but wetting/continuity still needs verification.

**Exact retained pull-downs / retired parts:** R321=`TNPW0603100KBEEA`, pin1 DISPOSAL/pin2 GND; R322=same, pin1 RUN_GATE/pin2 GND. They are in parallel with the new command pull-downs and their loads count. C312, the obsolete DET_DELAY capacitor, is DNP along with the other retired delay components. C306/C309 use SER_DRV as already specified; all remaining passive assignments follow PASSIVE_COMPLETION.csv unless explicitly DNP here. J601/J602 external contacts use the same numbered 7201SYZQE family as S601; no unverified tactile-switch terminal pair is needed. The switches and harnesses are external control accessories.

**PG memory boundary:** U613's CLK=PG_GOOD AND ARMED shares an ARMED transition with /CLR. Normal initialization must establish PG_GOOD=0 before ARM, so the next real PG edge occurs after asynchronous-clear recovery. T15F3 must explicitly sweep PG already high and near-coincident with ARM, and the short PG-loss feedback pulse through U613/U629/U626; record SCES794G p7 recovery and minimum /CLR pulse-width compliance. This candidate does **not** have a proved hardware veto for a stuck-high/early PG input. If such a case is admitted, complete that veto before integrated operation; a favorable truth table cannot close it.

**Partial-supply boundary:** LVC Ioff applies at VCC=0, not arbitrary intermediate SAFE5. TPS3808's low-VDD reset guarantee is conditioned on load and ramp (SBVS050N p6); the partial commit's 10 kΩ POR pull-up did not meet its 15 µA/0.8 V table point; the final-resume correction below changes it to 100 kΩ. Consequently the passive SHDN calculation and nominal POR table do not establish every brownout/default-off trajectory. T15F3 must measure SHDN and actual gates through 0.3…1.8 V SAFE5 plateaus with other rails present and removed. Keep the main and series force links absent for this test. Failure requires a direct qualified hardware veto, before integrated capture freeze/use. Hard SER_DRV pin shorts and PG/ARM recovery remain explicitly unclosed; no universal default-off guarantee is asserted by this document.


## Handback from 692d30f — item 2 disposition

**DECISION / correction:** R609 is 100 kΩ `TNPW0603100KBEEA`, SAFE5–CORE_POR_RAW_N. U662 is its sole signal receiver; no probe/pull-up may silently add load. At SAFE5=0.8 V, allow 5 µA receiver input leakage: `IRESET≤0.8/(100k×0.997375)+5µA=13.021056µA`, below TPS3808's 15 µA POR test load. At SAFE5=4.75 V, 0.3 µA supervisor leakage plus 5 µA input leakage gives `Vhigh≥4.75−5.3µA×100k×1.002625=4.218609V`, above 0.7×4.75 V. These are DC screens, conditional on the receiver leakage transfer; add probe loading explicitly. The Schmitt input accepts the slower edge. TI SBVS050N p6 still conditions low-voltage POR on ramp, and TI SCES351Y specifies function only in its supply range. This correction does not prove every intermediate-supply gate state.

**Remaining construction/qualification boundary:** (a) supply plateaus through 0.3…1.8 V must not release SHDN or either power gate, (b) early/stuck-high PG and the U613→U629→U626 feedback must meet recovery and minimum clear width, and (c) hard loss directly at SER_DRV must turn both series FETs off. T15F3 independently sweeps these cases with all main/series force links removed; failure requires a circuit revision. The present evidence does not establish universal default-off behavior, so item 2 remains **BLOCKED for integrated freeze**. The explicit state circuit, DC-short probe and isolated reservoir are retained as capturable coupon candidates; persistent-short acceptance is never inferred merely from an empty output capacitor.
