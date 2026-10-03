# Sheet 04 — Kelvin monitoring review

2026-10-03. **PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION**

**STATUS: CONDITIONAL PASS for capture; electrical qualification BLOCKED.** Continued the draft; no power topology or shunt-value change. Twenty-three physical components have footprints. [Whole-project ERC after Sheet 04](sheet04_review_erc.json) has zero violations. Current netlist checks reject reversed Kelvin routing, a differential-filter return moved to ground, and a local supply moved to the host domain.

**DATASHEET / EVIDENCE:** R401 remains WSL27262L000FEA, 2 mΩ ±1%, 25 ppm/K, with the PR15 qualified four-pad land. Force1=VOUT_PROTECTED, force4=LOAD_5V1; separate sense2/3 feed R402/R403 (10 Ω each). C401 is 100 nF **between** INA_IN_PLUS and INA_IN_MINUS. TP402/403 carry only sense current; TP405/406 observe the force rails with paired ground pads. Kelvin trace attachment and return-current geometry still require R3 review.

INA228 DGS10 has A1/A0 grounded for address 0x40, IN+10/IN−9, VBUS8 on LOAD_5V1, VS6 and GND7, no exposed pad. [TI SLYS021A, May 2022, pp3–5](https://www.ti.com/lit/ds/symlink/ina228.pdf) was rechecked. TPS70933 DBV5 retains IN1/GND2/EN3 open/NC4/OUT5 and no EP. TCA9517 DGK8 retains host VCCA1, SCLA2/SDAA3, GND4, EN5/local VCCB8 and local SDAB6/SCLB7, no EP; [TI SCPS242D, July 2017, pin table](https://www.ti.com/lit/ds/symlink/tca9517.pdf) was rechecked. Native regulator/buffer pins and the qualified C404 TDK land are retained.

**CALCULATION:** at 5 A, shunt drop is 10 mV and dissipation 50 mW. ±163.84 mV / 2 mΩ gives ±81.92 A nominal ADC full scale; the alternate ±40.96 mV range gives ±20.48 A. These ranges do not rate the shunt, conductors or protection. The 20 Ω/100 nF differential filter pole is 79.58 kHz. At 80 A, nominal instantaneous dissipation would be 12.8 W; pulse acceptance requires measured integral(I²R dt) and applicable component ratings.

**DECISION:** retain local and host pull-ups on their respective 3.3 V supplies, local-controlled repeater EN and load-side VBUS sensing. Telemetry cannot provide fast fault timing or protection permission. J503 is disconnected during initial fault testing.

**OPEN RISKS:** self-heating and pulse survival; tolerance/TCR and calibration; current/voltage/power/energy/timebase accuracy across temperature; negative fault pin/common-mode stress; local-regulator stability/effective output capacitance; host-only/local-only/partial-rail bus leakage and timing. No physical results are claimed. Next: Sheet 05 connector and fixture interfaces.
