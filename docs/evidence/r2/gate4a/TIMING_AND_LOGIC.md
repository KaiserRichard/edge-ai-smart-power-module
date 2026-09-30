# TASK 1 — common fixes and complete timing contract

**Analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** The change register is complete as an engineering proposal; it is not a pin-level capture freeze. `OPEN` terms are not zero. Source IDs and revisions are in [SOURCES.md](SOURCES.md).

**DECISION:** retain D, the two BSC034N06NSATMA1 devices, the protected crowbar and 2 mΩ telemetry shunt. Add a separately commanded raw-node dump; neither the protected crowbar nor the open opposed pair is an energy destination for L201. No avalanche rating is credited. Keep local regulation at 100 kΩ/24.4 kΩ; do not increase the setpoint to compensate for path loss.

**REQUIREMENT:** M05 ballast terminals must be ≤85°C immediately before every pulse, with waveform-dependent temperature rise inside the manufacturer's 95°C terminal ceiling. Retain WFMB2512R0330FEA only subject to actual hot pulse, unequal sharing and repetition qualification. Do not replace that condition with a 125°C resistor-terminal premise. MOSFET junction, resistor terminal, PCB and ambient are separate temperatures.

**PROPOSED M01:** independent surge-limited input → 12 V buck-boost → blocking diode/hold capacitor → LTC7001/UCC27511 and detector LDO. Directly supervise the loaded held-driver and detector rails, plus verify source-referenced bootstrap/gate voltage. Auxiliary supplies stay upstream of the main eFuse. Passive gate-source resistors and default-asserted eFuse SHDN operate with logic unpowered. Detailed supply restrictions are in [AUX_BRANCH_FIX.md](AUX_BRANCH_FIX.md) for the current revision.

The following numbers are inherited manufacturer table inputs, at the conditions identified in Gate3b COMMON_PROPOSED_FIXES. They are **EVIDENCE**, not full application timing limits. ns unless marked µs.

| Stage | Min / typ / max | Condition and missing transfer |
|---|---|---|
| Actual short → sensed OV threshold | OPEN / OPEN / OPEN | Raw C charging, initial state, fault slew; cannot assume an instantaneous trigger |
| Threshold → divider settling and required comparator overdrive | OPEN / OPEN / OPEN | R/C, new switch/clamp, reference, probe capacitance and hysteresis |
| TLV3201 output falling | OPEN / 45 / 55 | 5 V, 20 mV differential overdrive, 15 pF; real minimum DET5 and load not proved |
| OV qualification gate | 1 / OPEN / 4.6 | 5 V table load/temperature; actual topology is to be captured |
| Fault-latch asynchronous action | 1.6 / OPEN / 6.1 | Stated 5 V/load; no startup/brownout guarantee follows |
| Crowbar command gate | 1 / OPEN / 4.6 | Same transfer restriction |
| UCC27511 propagation | 4 / 13 / 23 | 12 V table test; held rail is below 12 V after diode, real gate load differs |
| Crowbar gate charge + useful clamp/commutation | OPEN / OPEN / OPEN | Useful high-current clamp, not VGS threshold |
| Parallel RUN gate | 1 / OPEN / 4.6 | Can remove RUN directly without waiting for fault latch |
| LTC7001 propagation | OPEN / 35 / 70 | VCC=BST=10 V, TS=0, 1 nF; opposed pair plateau/removal/bootstrap differ |
| Series-gate fall + physical current interruption | OPEN / OPEN / OPEN | VDS/current/SOA, displacement current and inductive returns |
| Independent source-fault trigger + logic + Q304/SHDN crossing | OPEN / OPEN / OPEN | Must begin at actual short onset; OV-only triggering is not credited |
| TPS26630 SHDN crossing → internal off endpoint | 0.8 / 1 / 1.5 µs | Published test-conditioned endpoint; physical input-current commutation/leakage separate |
| Source/input wiring commutation | OPEN / OPEN / OPEN | Measure positive charge at the energy boundary |
| Direct rail supervisor + command removal | OPEN / typical only / OPEN | TPS3808 SENSE→RESET 20 µs is typical, not a maximum |

For the proposed parallel paths:

`tCB = tthreshold + toverdrive/settling + tcmp + tqual + tlatch + tcommand + tUCC + tgate_on + tcommutation`

`tSER = tthreshold + toverdrive/settling + tcmp + tqual + tRUN + tLTC + tgate_off + tinterruption`

`tSRC = tindependent_trigger + tlogic + tSHDN_cross + tTPS + tinput_commutation`

Complete fault-onset min/max pairs are **OPEN/OPEN for all three paths**. A sum of partial maxima remains a partial sum, not a system bound. At valid table conditions the crowbar digital subtotal is CALCULATED 93.3 ns, before analog development, gate charging and commutation; the series digital subtotal is 134.2 ns, before those missing stages. Do not add the three parallel totals together.

**ASSUMED allocation inherited from Gate3b:** arriving current ≤80 A, protected C≥1 mF, ESR≤0.5 mΩ, static useful clamp≤5.38 V, extra ringing≤20 mV. Then `tuseful < C(5.5−5.38−I·ESR−0.020)/I = 0.75 µs`. Proposed 0.5 µs yields CALCULATED 5.480 V at the module and 20 mV reserve. Neither 80 A protected arrival nor this capacitance/ESR is established by the selected BOM. Four PCH1V471MCL1GS have nominal 1.88 mF, and cannot inherit the old 1–1.5 mF/0.5 mΩ contract. More C trades rise rate against startup, stored energy and damping. Full harness/Pi peak remains OPEN.

**Current detector:** R301=9.88 kΩ, R302=10 kΩ, switch U321 then R303=1 kΩ, R367=100 kΩ at U303 IN−. The loaded equation and enumerated corners are in [CALCULATIONS.md](CALCULATIONS.md). Nominal trip is 5.266700 V (5.267545 V with 17 Ω switch resistance); conditional trip range 5.219932…5.314611 V and upper 20 mV-overdrive point 5.356863 V. These include declared, unqualified leakage/hysteresis allowances. The lower trip also reduces nuisance-trip headroom: T06 must compare it with measured normal startup/load-release peaks; the old nuisance screens do not transfer. The old 11.3k/10k/1M network actually trips at 5.358575 V, not 5.353250 V; archived calculations are historical.

**OPEN RISK:** the 10 µs source-off target is measured from fault onset. A raw-output detector can trigger late while the bulk bank is being charged. A dedicated independent source-fault discriminator is required, with full min/max/false-trip proof. An externally timed fault-injector cutoff can exercise a conditional source contract on a test board, but cannot validate autonomous detection. Its circuitry/MPN is not invented here: this is an explicit capture blocker, not a useful-sounding zero-delay block.

Functional policy to be implemented and checked against actual pins:

| State/event | Main eFuse permission | Series RUN | Raw/protected disposal | Re-arm |
|---|---|---|---|---|
| Unpowered, cold start, or invalid detector/driver rail | OFF by passive hardware | OFF, gate-source bleed | Only qualified independent/stored drive may be credited | Fresh ARM edge after valid rails and safe stored energy |
| Valid rails, fresh ARM, no OV, buck PG low during startup | Allowed | OFF | OFF | Do not require buck PG to start the buck; avoid circular permission |
| Valid rails, armed, buck PG high, no fault | Allowed | ON | OFF | Already armed |
| Ordinary PG loss with no genuine fault | Removed/disarmed by policy | OFF | OFF; PG alone never fires crowbars | Fresh ARM after recovery |
| Genuine OV/current fault, including simultaneous PG loss | Latched OFF | OFF immediately | Both independently rated destinations ON while energy remains | Reset requires raw node safe, rails valid and separate fresh ARM |
| Persistent short; input/PG returns or ARM held high | OFF | OFF | Stored-energy action maintained for qualified duration | No automatic restart |
| Manual reset while raw OV/current persists | OFF | OFF | Fault has priority | Reset prohibited; no async set/clear conflict |

`MAIN_PERMISSION = ARMED & RAILS_VALID & !FAULT`; `RUN = MAIN_PERMISSION & BUCK_PG`; `DISPOSAL = FAULT & DRIVE_VALID`. These are functional equations, **not** a proved pin-level implementation. PGOOD is excluded from the independent OV latch/qualifier. A volatile latch must start disarmed after total power loss. Simultaneous asynchronous set/clear, slow reset edges, bounce, partial powering, and races remain capture-review items.

**PROPOSED default SHDN construction:** Q305 2N7002,215 drain to main SHDN/source to GND; bias its gate from VIN_FUSED via 100 kΩ, add 100 kΩ gate-to-GND and BZT52H-C10,115 gate clamp. Q306 2N7002,215 shorts Q305's gate only with valid latched MAIN_PERMISSION from DET5; R326100k holds Q306's gate toGND when permission is unpowered. Retain independent Q304 fault pull-down in parallel. At 9 V unloaded divider gives 4.5 V gate; at 58.1 V the zener bounds gate stress conditionally. Verify resistor/zener tolerance/leakage, lowest startup input, SHDN source-current maximum, low-level voltage, Q306 logic states and fault dominance. Partial supplies must never release SHDN. This supplies a concrete topology for review, but its unqualified corners remain BLOCKED.

**Current powered-off clamp construction:** OV_DIV → D301 BAS116 anode, cathode CLAMP_2V5; D321 LM4040A25IDBZR cathode CLAMP_2V5, anode GND; R361=68.1 kΩ from DRV_HOLD. D322 BAS116 anode GND/cathode OV_DIV handles negative injection. U321 ADG4612BRUZ, supplied DET5 with VSS/GND at GND, isolates OV_DIV before R303. R367=100 kΩ from comparator SENSE to GND and R370=10 kΩ from DET5 to GND. C301 is the BST-to-TS capacitor; C302 is the separate reference bypass. No fault current is intentionally sent into REF5025. The single-supply fully off leakage screen is 0.300750 V; powered isolation can give a 3.8095 V pull-down-only screen, so partial-power safety is not proved by the fully off result. Detailed IC pins and T03/T04/T06/T15 acceptance are in [FIX_RESOLUTIONS.md](FIX_RESOLUTIONS.md) and [TEST_PLAN.md](TEST_PLAN.md).

**Construction blockers:** FAULT_SET_N, RESET_SAFE_N, POR and fresh-ARM generation remain unimplemented proposals. U320 pin assignments alone do not solve asynchronous arbitration. Loss of 3V3_AUX while DET5 remains must explicitly remove permission. A further information limit applies: with main power off and raw discharged, a healthy buck and a persistent high-side short can present the same detector/PG/rail inputs. A reset predicate based only on those inputs cannot prove the short is absent. A bounded diagnostic or a documented fault-repair/continuity lockout must be part of the reset construction; do not claim automatic safe re-arm from `raw < threshold` alone. No such diagnostic circuit is selected here.

The retained parts and new candidates are listed by refdes in [FREEZE_TABLE.md](FREEZE_TABLE.md); exact package/pin/land checks are required for every MPN change. No native CAD was accessed, therefore no new ERC/DRC claim is made.
