# Hardware source pack — Project II V1A

Date: 2026-09-11. Purpose: evidence pointers for Richard's hardware study material and ChatGPT technical review. This is not a schematic or an approved BOM.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**Scope:** V1A is the standalone Smart DC Power Module. V1B is the teammate's separate supercapacitor subsystem. Future V2 integrates both after validation. WBR/CAN/HAT/supervisor research is future reference, not V1A requirements. All source use below is **REFERENCE**. Exact pins, revisions, licenses and limitations are in the [source audit](01_REFERENCE_AUDIT.md) and [manifest](evidence/r0/source_manifest.json); unresolved values are in [requirements](00_REQUIREMENTS.md).

## 1. DC input/protection

- **Best source:** [TI TPS2663, SLVSE94G](https://www.ti.com/lit/ds/symlink/tps2663.pdf), Fig.8-7 and adjacent discussion, pp.20–22; transient/layout pp.37–39. Example: TPS26630/31 with external reverse-protection Q1/Q2. Local: `third_party/documents/TI_TPS2663_SLVSE94G.pdf`.
- **Ratings/equations:** 4.5–60 V family; variant-dependent cutoff/current control. `Iin=Pout/(Vin η)`; `Iinrush=C dV/dt`; fuse interrupt/I²t and TVS clamp must match actual fault energy. No V1A voltage/trip value is frozen.
- **Layout/relevance:** V1A; short protection/current loops, coordinated fuse/TVS return, MOSFET SOA and thermal copper. **Richard inspect:** compare Fig.8-7 with the arrangement omitting external devices; identify exactly which reverse functions disappear.

## 2. Buck conversion

- **Best source:** [TPS56837 EVM, SLVUCE1A](https://www.ti.com/lit/pdf/slvuce1), schematic p.10, BOM pp.11–12, layout pp.8–9; [datasheet SLVSGM3B](https://www.ti.com/lit/ds/symlink/tps56837.pdf), §7.2.2 and §7.4. Example: TPS56837RPAR, 3.3 µH, 500 kHz, nominal 5 V.
- **Ratings/equations:** 28-V/8-A IC class, not a board guarantee; `D≈Vout/Vin`, `ΔIL=Vout(1−D)/(L fsw)`, `Ipeak=Iload+ΔIL/2`. Use effective MLCC capacitance. C7/C8/C9 are DNP in this EVM.
- **Layout/relevance:** V1A leading review candidate; four layers, local input loop, short SW region, quiet feedback, defined AGND/PGND connection. **Richard inspect:** trace the high-frequency input-current loop and explain why an EVM cannot be shrunk without reassessing heat. Compare [LM61460 Table 9-5, pp.43–44](https://www.ti.com/lit/ds/symlink/lm61460.pdf) if upper input needs more margin.

## 3. High-current 5-V distribution

- **Best sources:** TPS56837 EVM layout pp.8–9 above; [Pi 5 USB-PD paper, Release 1](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf), printed pp.5,7–8. Pi is an optional load example, not the required connector.
- **Equations/ratings:** `Vload=Vsource−I Rtotal`, `Ploss=I²R`; count both wires, contacts, copper, shunt and switches. Supplying voltage is distinct from negotiating/declaring 5-A capability. Exact connector/current/voltage window OPEN.
- **Layout/relevance:** V1A; avoid neckdowns, preserve return paths and use connector-adjacent sense/probe points. **Richard inspect:** locate the complete outgoing and return resistance path; explain why a family headline current or an unrated jumper wire is insufficient.

## 4. Shunt/current monitoring

- **Best sources:** [TI SBOA511A](https://www.ti.com/lit/an/sboa511a/sboa511a.pdf), pp.3–7; [Vishay WSL2726 document 30131, 29-Jun-2026](https://www.vishay.com/docs/30131/wsl2726.pdf), pp.1–2. Example family supports four-terminal 1/2/5-mΩ candidates; no final shunt selected.
- **Equations/ratings:** `Vshunt=IR`, `Pshunt=I²R`; at 5 A, 2 mΩ gives 10 mV/50 mW. ±1% family tolerance; component TCR differs by resistance value. See the [comparison calculations](04_POWER_CALCULATIONS.md#shunt-range-and-loss).
- **Layout/relevance:** V1A; dedicated Kelvin pads/traces, short paired sense route, no shared load-current copper. **Richard inspect:** distinguish power terminals from sense terminals and component TCR from alloy-only TCR.

## 5. INA228

- **Best sources:** [SLYS021A](https://www.ti.com/lit/ds/symlink/ina228.pdf), pin/limits pp.3–7, §8.1.2 pp.30–32, layout p.39; [SBOU241E EVM](https://www.ti.com/lit/ug/sbou241e/sbou241e.pdf), Fig.6-1 p.23 and layout/BOM pp.27–30.
- **Ratings/equations:** 2.7–5.5 V supply; ±40.96/±163.84 mV shunt ranges; `Ifullscale=Vrange/Rshunt`. Lower-range SHUNT_CAL requires the ×4 factor. ENERGY is unsigned, requires continuous conversion, and loses state on reset. INA226 is a justified fallback with software energy integration.
- **Layout/relevance:** V1A; place VBUS at load side, filter near IC, protect local supply and unpowered host I2C. **Richard inspect:** follow IN+/IN−/VBUS separately and identify which losses the resulting power reading excludes. The monitor is not sole fault protection.

## 6. Supercapacitor charging concept

- **Best source:** [ADI LTC3350 Rev D](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc3350.pdf), operation pp.16–17 and current allocation pp.21–22. Cross-reference [TI LMP8646 SNOSC63B](https://www.ti.com/lit/ds/symlink/lmp8646.pdf), p.1 typical application, to understand the concept cited by Sailor Hat.
- **Equations/ratings:** `I=C dV/dt`; at a shared rail, source capability must cover load plus allocated charger demand. A current limiter, a voltage-regulated charger and fault protection have different responsibilities. No charger IC/current/rail is selected for V1B.
- **Layout/relevance:** V1B/V2 study only; charging-current sense and power loops need separation. **Richard inspect:** identify how load demand reduces charging allowance; note that Sailor Hat actually uses COS1333TR/LMV321 circuitry, not LMP8646.

## 7. Supercapacitor balancing concept

- **Best source:** [Eaton PS-5006, effective Dec 2017](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/technical/eaton-supercapacitor-application-guidelines.pdf), p.3 passive/active balancing; LTC3350 pp.17–18 separates balancing from cell OV shunts. Historical example: [Sailor Hat `supercap.kicad_sch`](https://github.com/hatlabs/SH-RPi-hardware/blob/e82e3c9823bbcf94091b22927dd2e0da9cdfac8c/supercap.kicad_sch), LMV321-TR/SS8050 sections.
- **Equations:** `1/Cseries=Σ(1/Ci)`; ideal series charge is equal, so the smaller capacitance gets the larger voltage. Eaton's p.3 mismatch labelling needs this correction; leakage governs long-term imbalance. `Pbleed=Vcell²/Rbleed`.
- **Layout/relevance:** V1B/V2 only; cell sense connections, bleed heat and tolerance/leakage must be checked. **Richard inspect:** distinguish voltage equalization from individual-cell overvoltage protection. Do not inherit Sailor Hat's cell values or forum-derived balancing circuit as validated.

## 8. Backup/power-path concept

- **Best sources:** LTC3350 pp.16–18 power-fail and ideal-diode operation; [LM7480-Q1 SNOSD95C](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf), pp.15–16 load disconnect. These are examples of ownership/functions, not a proposed V1B implementation.
- **Equations/ratings:** `Eusable=½C(Vhigh²−Vlow²)`; hold-up requires `ηEusable≥∫Pload dt`, plus ESR/aging/temperature reserve. A power-fail flag supplies no energy. LM7480 has no adjustable overcurrent limiter.
- **Layout/relevance:** future V2; FET body-diode direction, OR-ing, current return and discharged/charged startup matter. **Richard inspect:** trace current with input absent and output alive; identify whether a buck discharge circuit can drain the backup source.

## 9. Raspberry Pi HAT/HAT+ concept

- **Best source:** [HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf), build `6df06cc-clean`, 2024-12-05, chapters 2–4 and 6. Historical [legacy guide](https://github.com/raspberrypi/hats/blob/348dbf88d870bf50d6b4f23dbe2b64d60363f23c/designguide.md) is secondary to model-specific current documentation.
- **Constraints:** EEPROM class/address, GPIO standby state, mechanical access and source-only concurrent-supply behavior are separate obligations. A Pi header or a 5-V source alone does not establish HAT+ compliance.
- **Layout/relevance:** future HAT/WBR only; no V1A HAT form factor/EEPROM/GPIO requirement. **Richard inspect:** compare Standard versus power-only EEPROM classes and 5-V-present/3.3-V-absent standby; retain only the general backfeed/power-domain lesson for V1A.

## 10. Future V1A + V1B → V2 integration

- **Best project source:** [architecture integration section](02_ARCHITECTURE.md#future-integration-without-designing-v1b) and [interface register](00_REQUIREMENTS.md#future-v1av1b-interface-register), informed by LTC3350's power-path/current-allocation example.
- **Agreement needed:** rail voltage, allowed range, maximum load, charge allowance, reverse current, common ground, connector, power-fail, telemetry, startup/shutdown, backup/hold-up — **all TBD**.
- **PCB boundary/relevance:** keep V1A independently testable and expose useful test/control nodes, while deferring the physical V1B interface. **Richard inspect:** decide which subsystem owns each current path and measurement boundary before combining validated modules. Do not implement the teammate's circuit or WBR sequencing in V1A.

## Recommended personal reading

1. TPS56837 **EVM pp.8–12**: current loop, layout, actual populated BOM.
2. TPS56837 **datasheet §7.2.2 and §7.4**: LC/peak-current calculations, effective capacitance and copper assumptions.
3. TPS2663 **Fig.8-7 and adjacent reverse-protection discussion, pp.20–22**.
4. INA228 **§8.1.2 pp.30–32 and layout p.39**, with EVM **Fig.6-1 p.23**.
5. Vishay WSL2726 **pp.1–2**: exact shunt order code, Kelvin geometry, tolerance and component TCR.
6. Pi 5 USB-PD paper **printed pp.5,7–8**: optional SBC load and supply-capability context.
7. LTC3350 **pp.16–18 and 21–22**: future charging, power-fail, balance and load-priority concepts only.
8. Eaton PS-5006 **p.3**, with the series-voltage correction above: balancing tradeoffs for future V1B discussion.
9. HAT+ **chapters 4 and 6** only if studying the preserved future HAT work; not needed to define V1A.
