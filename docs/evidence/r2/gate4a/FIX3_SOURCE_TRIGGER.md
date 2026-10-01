# FIX3-1 — autonomous source trigger, capture candidate

**DECISION / 2026-10-01. Analysis only. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** This document supplies the previously absent circuit. It does not turn its conditional timing budget into a measured bound. FIX3 takes precedence over the round-1/2 “no selected discriminator” statements; those records remain historical.

## Circuit and ownership

Use a hysteretic switch-node detector followed by an **LTC6994IS6-1#TRMPBF rising-edge pulse qualifier**, plus a separate input-collapse detector. Both run from `SAFE5`, the independent protection supply in FIX3_INTERLOCK.md. Sense **L201_IN**, on the inductor side of the removable native-SW link. In ordinary operation this is U201.10; in the isolated injector configuration it is the emulated failed-high-side node. The fixture trigger has no connection to this circuit.

The large hysteresis is intentional: an ordinary pulse first crosses about 6.5 V, then the low-side interval resets the detector below about 2 V. A DCM switch node resting near 5.1 V therefore does not start the timer from its reset state. A fault that begins high and then droops to 5 V continues timing. A blind logic-level SW detector would lack both properties. This is an adaptation of the comparator's external-hysteresis method and the manufacturer's pulse-qualifier function, not a copied PCB.

### Complete new source-detector connections

All two-terminal resistors below have pin 1 at the first net and pin 2 at the second. All new comparator supply bypasses are `GRM188R71H104KA93D`, 100 nF / 50 V / 0603, directly between pins 5 and 2. `GND` here is protection signal ground, Kelvin-connected to the source-return reference plane. No force current uses it.

| Ref | Exact MPN / value | Pin-level connections | Default / supply |
|---|---|---|---|
| U640 | TLV3201AIDBVR | 1=SW_HIGH; 2=GND; 3=SW_SENSE; 4=REF1V25; 5=SAFE5 | Output low with SW discharged and reference valid; undefined while supply invalid, masked by interlock |
| R640 | TNPW060320K0BEEA / 20.0 kΩ | L201_IN → SW_HYS | Input current limiting |
| R641 | TNPW06036K19BEEA / 6.19 kΩ | SW_HYS → GND | Input default low |
| R642 | TNPW060320K0BEEA / 20.0 kΩ | SW_HIGH → SW_HYS | Positive feedback |
| D640 | BAS116,215 | 1 A=SW_HYS; 3 K=REF_SAFE_2V5; 2=NC | Positive clamp into the separately rated shunt, never REF5025 |
| D641 | BAS116,215 | 1 A=GND; 3 K=SW_HYS; 2=NC | Negative clamp; R640 also limits injection |
| C640 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U640 bypass |
| U641 | LTC6994IS6-1#TRMPBF / TSOT-23-6 | 1 IN=SW_HIGH; 2 GND; 3 SET=WD_SET; 4 DIV=GND; 5 V+=SAFE5; 6 OUT=SRC_TIMEOUT | DIVCODE=0, NDIV=1, rising delayed/falling prompt |
| R643 | TNPW0603200KBEEA / 200 kΩ | WD_SET → GND | Nominal 4 µs; no capacitor at SET |
| C641 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U641 bypass |
| U642 | TLV3201AIDBVR | 1=VIN_GOOD_FAST; 2=GND; 3=VIN_SENSE; 4=REF1V25; 5=SAFE5 | Low with VIN_PROTECTED absent |
| R644 | TNPW060349K9BEEA / 49.9 kΩ | VIN_PROTECTED → VIN_MON | Input-collapse divider, including R652 loading |
| R645 | TNPW060310K0BEEA / 10 kΩ | VIN_MON → GND | Nominal 8.1125 V threshold |
| D642 | BAS116,215 | 1 A=VIN_MON; 3 K=REF_SAFE_2V5; 2=NC | Positive clamp |
| D643 | BAS116,215 | 1 A=GND; 3 K=VIN_MON; 2=NC | Negative clamp |
| C642 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U642 bypass |
| U643 | SN74LVC1G74DCTR | 1 CLK=VIN_GOOD_FAST; 2 D=SAFE5; 3 /Q=NC; 4 GND; 5 Q=VIN_SEEN; 6 /CLR=MAIN_PERMISSION; 7 /PRE=SAFE5; 8 VCC=SAFE5 | Remembers successful main-input rise; clear while disarmed |
| C643 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U643 bypass |
| U644 | SN74LVC1G14DBVR | 1 NC; 2 A=VIN_GOOD_FAST; 3 GND; 4 Y=VIN_BAD; 5 VCC=SAFE5 | Inverted input monitor |
| C644 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U644 bypass |
| U645 | SN74LVC1G08DBVR | 1 A=VIN_SEEN; 2 B=VIN_BAD; 3 GND; 4 Y=SRC_COLLAPSE; 5 VCC=SAFE5 | Cannot fault solely because an unstarted input is zero |
| C645 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U645 bypass |
| U646 | SN74LVC1G32DBVR | 1 A=SRC_TIMEOUT; 2 B=SRC_COLLAPSE; 3 GND; 4 Y=SRC_TRIP; 5 VCC=SAFE5 | Either trigger sets the persistent fault latch |
| C646 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U646 bypass |
| U647 | ADG4612BRUZ / TSSOP16 | 1 IN1=SAFE5; 2 D1=SW_HYS; 3 S1=SW_SENSE; 4 VSS=GND; 5 GND; 6 S4/7 D4/8 IN4/9 IN3/10 D3/11 S3=GND; 12 NC; 13 VDD=SAFE5; 14 S2=VIN_SENSE; 15 D2=VIN_MON; 16 IN2=SAFE5 | Powered-off input isolation; channels enabled when SAFE5 is valid |
| C647 | GRM188R71H104KA93D / 100 nF | SAFE5 → GND | U647 bypass |
| R651 | TNPW0603100KBEEA / 100 kΩ | SW_SENSE → GND | Fully-off 3 µA leakage screen 0.300788 V |
| R652 | TNPW0603100KBEEA / 100 kΩ | VIN_SENSE → GND | Included in input-divider arithmetic |

`SRC_TRIP` enters U615 in FIX3_INTERLOCK.md; it asynchronously clears the **NOFAULT** latch, pulls SHDN low, removes series RUN and commands both raw/protected dumps. Neither BUCK_PGOOD nor ARM qualifies the genuine-fault latch. Power-up masking belongs solely to reference/safety-supply validity. The comparator input on U303 remains the independent output-OV backup.

### Source shutdown, complete endpoint connections

Replace the proposed Q305/Q306 bias-release network; Q305/Q306/R324/R325/R326/D305 become DNP. Retain Q304 as a separate fault sink. Reserve R647=`TNPW06031K00BEEA`, 1 kΩ from MAIN_PERMISSION to INPUT_SHDN, and R648=`TNPW060310K0BEEA`, 10 kΩ INPUT_SHDN→GND. U101.12=INPUT_SHDN. Q304=`2N7002,215`: 1 G=FAULT_DRIVE, 2 S=GND, 3 D=INPUT_SHDN. R649=`TNPW06031K00BEEA`, 1 kΩ FAULT→FAULT_DRIVE; R650=`TNPW0603100KBEEA`, 100 kΩ FAULT_DRIVE→GND. **U101.11 MODE=NC/open (latch-off)**, R105=4.02 kΩ at U101.10, all other U101 pins retain the pinned input circuit. R646 is unused/unpopulated; there is no unnamed resistor at that reservation.

**Resume correction / EVIDENCE:** TI SLVSE94G p8 MODE_SEL and pp27–28 specify open MODE for latch-off and grounded MODE for auto-retry. The partial round-3 instruction “MODE=GND (latch-off)” was wrong. Remove that tie in future capture; do not modify the historical exported netlist. External NOFAULT memory remains necessary because SHDN cycling resets the eFuse's internal latch. The source test must check both internal latch behavior and the external reset policy.

**CALCULATION:** a 10 µA SHDN source plus a separately allocated 10 µA powered-off logic leakage produces at most `20 µA × 10 kΩ × 1.002625 = 0.200525 V`, below the 0.8 V shutdown limit. With a conservative 3.8 V logic high, the resistor divider gives at least `3.8×9.97375/(9.97375+1.002625)=3.452893 V`, above the 2 V enable limit. Even a conflicting 5.25 V permission demands <5.264 mA from Q304 through R647; characterize Q304 sink at actual gate voltage. This removes reliance on a sub-mA Zener knee or a marginal 4.5 V gate-bias divider. Powered-off leakage and brownout transfer remain measured in T15F3; DC arithmetic does not specify intermediate-supply logic states.

## Equations and timing budget

**ASSUMPTIONS explicitly requiring qualification:** SAFE5=4.75…5.25 V; reference/divider/offset allowance at REF1V25 is ±15 mV; independent resistors ±0.2625% (0.1% plus 25 ppm/K × 65 K); U640 output-low 0…0.325 V, output-high 4.40…5.25 V at its actual load; comparator/probe/PCB node capacitance ≤100 pF; healthy VIN_PROTECTED≥8.30 V after startup. These are test-board operating allocations, not changes to the owner’s 9–26 V connector requirement.

`VSW,trip = VTH[(1+Ron/R651)(1+R640/R641+R640/R642)+R640/R651] − VOUT·R640/R642`.

Nominal rising/falling at ideal 0/5 V outputs and Ron=0 are **6.788368/1.788368 V**. Independent corner enumeration is in FIX3_CALCULATIONS.json. The earlier 30 pF allocation is withdrawn: ADG4612 Rev 0 p7 lists approximately 50 pF typical on-capacitance, before board/probe loading. The revised 100 pF ceiling and 1.00 µs sensing allocation require measurement; neither is a guaranteed maximum. The external hysteresis must be tested including clamp leakage, overdrive, return bounce and the actual output drive. A 20 mV comparator overdrive needs approximately 109 mV additional SW voltage. U642's loaded nominal threshold is **8.11125 V**, rather than the unloaded-divider result. The maximum allowed normal SW_HIGH pulse is **3.50 µs including uncertainty**; every normal low interval must reset U640 and the qualifier. Do not use the 5.1 V DCM resting level as a reset pulse. U647 limits fully-off injection; its partial-power recovery and input capacitance remain T06F3 tests, not an assumed zero delay.

`tWD = (RSET/50 kΩ) × NDIV × 1 µs`.

Use the **full-temperature ±6.2%** table row, not the ±5.1% 25°C headline. With R643 drift, the conditional interval is **3.742151…4.259151 µs**. The output load must match the specified timing condition or be included in the measured transfer. Qualifier start-up is completed before READY; do not credit its approximately 500 µs typical start-up as a guaranteed bound.

| Fault→source-current endpoint term | Minimum credited | Maximum used | Evidence status |
|---|---:|---:|---|
| SW transition, input network, overdrive and U640 | 0 | 1.00 µs | Qualification allocation T01F3, includes sensing slew; not a datasheet maximum |
| U641 qualification | 3.742151 µs for a new pulse; **0 if already timing** | 4.259151 µs | ADI table plus resistor corners |
| U646/U615/inversion/NOFAULT asynchronous action/permission logic | 0 | 0.10 µs | Conservative allocation; exact load/rail checked T01F3 |
| Q304 and SHDN crossing | 0 | 0.25 µs | Measured allocation including node C |
| TPS26630 shutdown | 0.8 µs table only | 1.5 µs table only | TI electrical timing at its stated conditions |
| Physical input-current commutation | 0 | 0.40 µs | Measured allocation; includes leakage/current endpoint |
| Timing uncertainty | — | 0.025 µs | Existing T13 target, must be substantiated |
| **Conditional complete ceiling** | **No nonzero system minimum established** | **7.534151 µs** | **2.465849 µs reserve to 10 µs; not a guaranteed application result** |

The full fault-onset lower bound is conservatively **0**, not 3.742151 µs: a fault can begin part-way through a legal high pulse, or the parallel collapse/OV detector can win. Source, series and dump actions are parallel. Source-trigger→useful raw dump uses the same sensing/qualifier plus latch/gate, UCC27511 and actual Q330 gate/current development; allocate **≤6.10 µs from fault onset**, measured at useful dump current, not a TTL edge. Fast OV retains T08's distinct post-overdrive path. The physical minimum/maximum remains unmeasured.

`Q+ = ∫ max(IMAIN,0)dt` remains a separate **whole-event** ≤100 µC condition. A nominal 4.48 A ILIM setting does not bound the transient. FIX3_FIXTURE.md supplies an external resistance/current/abort boundary; no fixture timing signal participates in this trigger.

## Limits that a schematic cannot close

**OPEN RISK — normal/fault separation:** LM61460 Rev D p26 permits approximately 9 µs high time in dropout. This candidate deliberately trips on that condition; it does not pretend to support 9 µs dropout pulses while satisfying the 10 µs fault budget. T01F3-N must demonstrate normal 9/24/26 V startup, load changes, PFM/PWM and source impedance stay inside the 3.50 µs pulse allocation and VIN floor. A failed normal case requires a circuit/boundary revision, not disabling the watchdog or increasing its timer without recalculation.

**OPEN RISK — intermittent/internal shoot-through:** a real failed high-side plus active low-side can repeatedly reset the SW qualifier. U642/U643 provides an independent trip on input collapse after VIN has become valid, but no datasheet bounds the damaged internal bridge waveform. A failure before VIN_SEEN, or one that keeps VIN above threshold while making short low pulses, is **not proved covered**. The separated external injector emulates a continuously conducting high-side; it cannot validate simultaneous internal low-side conduction. This remaining coverage question is stated explicitly instead of claiming that a watchdog solves every possible buck failure.

**T01F3-F:** on the isolated detector/logic coupon, replay bounded SW/VIN traces, including floating 5.1 V, all fault phases, input collapse and narrow low pulses. PASS requires no reset of the fault memory, source endpoint+U≤10 µs and whole Q+ +U≤100 µC in every applicable integrated test. A fixture rescue is FAIL. Establish realistic damaged-bridge traces with a separately rated bridge emulator before claiming internal-failure coverage; destructive testing of U201 is not authorized here.

**Capture disposition:** exact circuitry and hooks are now available, so isolated capture of this candidate is technically possible. A full unconditional autonomous-source containment claim remains OPEN. The final freeze verdict must distinguish that limit from absent circuitry and must not count the continuous-high fixture as proof of the missing internal-bridge case.

## Primary evidence / attribution

- Analog Devices [LTC6994 Rev C](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC6994-1-6994-2.pdf), pp3–5 electrical limits, p10 S6 pins, pp12–14 equation/code/function, pp15–16 start-up. Pulse-qualifier functional block adapted; 200 kΩ, NDIV=1, hysteretic SW front end added.
- Texas Instruments [TLV3201 SBOS561C](https://www.ti.com/lit/ds/symlink/tlv3201.pdf), p3 pins, pp4–6 limits/conditions, pp12–15 hysteresis. The 55 ns value is a 5 V/20 mV/load-conditioned result, not a whole-rail guarantee.
- Texas Instruments [TPS2663 SLVSE94G](https://www.ti.com/lit/ds/symlink/tps2663.pdf), pp3–4 pins, p7 SHDN DC limits, timing table and pp27–28 SHDN/mode. [LM61460 SNVSBD5D](https://www.ti.com/lit/ds/symlink/lm61460.pdf), pp23–26 operating modes/dropout.
- Texas Instruments SN74LVC1G74/08/14/32 and Vishay TNPW sources are pinned in the FIX3 source register. Manufacturer copyright applies. No upstream file or manufacturer CAD was modified/copied.

## Resume audit — item 1

**DECISION:** keep the selected circuit as a capturable test candidate, with the corrected sensing allocation above. A source-fault signature that repeatedly gives SW_HIGH=1 for 3 µs and 0 for 1 µs while VIN remains 9 V never satisfies the timer or collapse condition. This is a counterexample at the logic interface, not a claim that a particular damaged LM61460 generates it. The existing source requirement has not excluded that signature. Accordingly there is **no unconditional 10 µs maximum**, and no full-source closure from the conditional 7.534151 µs sum.

**Exact closure:** T01F3-N measures normal SW/VIN at every stated corner; T01F3-F uses a separately bounded bridge emulator to determine whether the admitted failed-high-side class always supplies either a sufficiently long high interval or an input collapse within the remaining budget. Record timing from physical failure onset, including intervals before VIN_SEEN. If either detector can miss an admitted case, this circuit requires a further discriminator or an explicitly reviewed fault-scope change. A continuous-high injection alone cannot close it.

**Capture boundary:** the SW/VIN inputs and source outputs can be captured with removable force links and evaluated on an isolated logic coupon. That construction remains useful despite unknown damaged-bridge waveforms. The complete Gate4a source-containment freeze remains BLOCKED by fault coverage; this is not a bench PASS or a reason to omit the circuit.

**T01F3 timing report:** record the continuous-high, input-collapse and OV-backup paths separately. The 7.534151 µs ceiling applies only after the stated qualifying signature and analog allocations hold; it is not a ceiling for a fault that first produces neither signature. For the collapse path, time from physical fault onset through VIN_SEEN and VIN_GOOD_FAST falling, not just comparator propagation. Report measured minimum and maximum with uncertainty for source current, series current and useful raw/protected dump current on the same event. A conservative mathematical lower bound of zero is not a measured minimum. Test R4A-01 coverage before increasing fault energy; T12F3's later emergency abort is external bench containment and cannot supply the missing autonomous detection.

## Handback from 692d30f — item 1 disposition

**EVIDENCE:** the resumed numerical suite reproduces the periodic-pulse counterexample and keeps `internal_bridge_fault_coverage` and both actual timing endpoints null. LTC6994 Rev C p3 was rechecked: ±6.2% applies at NDIV=1 over the stated temperature range; the selected 4 µs timer is retained. MODE remains open at U101.11. No fixture FIRE/SHOT/ABORT signal connects to SRC_TRIP, FAULT or SHDN.

**DECISION:** item 1 now has a pin-level candidate, but the complete source requirement is **BLOCKED by coverage**, not by a missing part name. T01F3-F must establish the admitted damaged-bridge signature before its 10 µs test can close the requirement; otherwise revise the discriminator. Capture the isolated SW/VIN detector coupon with main and series force links absent. Neither the 7.534151 µs conditional budget nor a passing continuous-high injection grants integrated test-board freeze.
