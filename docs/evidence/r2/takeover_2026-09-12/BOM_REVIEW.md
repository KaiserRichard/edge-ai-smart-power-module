# V1A schematic review BOM

**NOT FOR PROCUREMENT OR FABRICATION - R2 BLOCKED.**

Netlist SHA-256: `e6bf536ed588b9101f88c6f48fd9d9f4d71f90961da69a5b3c83f2b2ba95434d`.

71 physical schematic entries (including test points), one row per reference. Nonphysical power flags are excluded by KiCad. Exact MPNs identify review candidates, not qualified substitutions. Blank MPNs and footprints are OPEN. The absent output-protection circuit is not included in this BOM.

| Ref | Qty | Value | MPN / selection | Provisional footprint | Rating / limitation |
| --- | ---: | --- | --- | --- | --- |
| C101 | 1 | 1uF 100V | OPEN | Capacitor_SMD:C_1210_3225Metric | X7R; 100 V; exact MPN/effective C OPEN |
| C102 | 1 | 1uF 100V | OPEN | Capacitor_SMD:C_1210_3225Metric | X7R;100 V; exact MPN/effective C OPEN |
| C103 | 1 | 100nF 16V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R +/-10%;16 V |
| C201 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C202 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C203 | 1 | 100nF 50V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R+/-10%;50V;oneatVIN1/PGND1,oneatVIN2/PGND2 |
| C204 | 1 | 100nF 50V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R+/-10%;50V;oneatVIN1/PGND1,oneatVIN2/PGND2 |
| C205 | 1 | 100nF 16V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R+/-10%;16V differentialbootstrapvoltage |
| C206 | 1 | 1uF 16V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R+/-10%;16V;requiredlocalVCCbypass |
| C207 | 1 | 22pF 50V | CGA3E2C0G1H220J080AA | Capacitor_SMD:C_0603_1608Metric | C0G+/-5%;50V;inserieswithR205 |
| C209 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C210 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C211 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C212 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C213 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C214 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | 22 uF +/-20%, 50 V X7R; DC-bias figures are typical estimates, not guaranteed minima; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C401 | 1 | 100nF 50V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R +/-10%;50 V differential filter |
| C402 | 1 | 100nF 16V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R +/-10%;16 V; at INA228 VS |
| C403 | 1 | 1uF 50V | OPEN | Capacitor_SMD:C_0805_2012Metric | X7R;50 V; LDO input |
| C404 | 1 | 22uF 50V | C5750X7R1H226M250KB | OPEN | X7R +/-20%;effective 1.5-47uF,ESR<=0.2Ohm required incl other bypass caps; generic 2220 land pattern disagrees with TDK recommendation; assignment OPEN |
| C405 | 1 | 100nF 16V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R +/-10%;16 V;at U403 VCCA |
| C406 | 1 | 100nF 16V | OPEN | Capacitor_SMD:C_0603_1608Metric | X7R +/-10%;16 V;at U403 VCCB |
| D101 | 1 | SMBJ26CA | SMBJ26CA | Diode_SMD:D_SMB | CANDIDATE: 26 V standoff, 42.1 V clamp at14.3 A/10-1000us; exact source revision and surge envelope OPEN |
| D102 | 1 | B260 | B260-13-F | Diode_SMD:D_SMB | K=1 at VIN_PROTECTED, A=2 GND; 60 V, 2 A; transient negative clamp, not load path |
| F101 | 1 | FUSE - OPEN | OPEN | OPEN | 5 A candidate only; DC interrupt/I2t/MPN must close against source |
| J501 | 1 | DC INPUT - MPN OPEN | OPEN | OPEN | 9-24 V normal;>=5 A candidate;keying/wire/contact/interrupt coordination OPEN |
| J502 | 1 | LOAD OUTPUT - MPN OPEN | OPEN | OPEN | 5.1 V nominal,5 A;exact connector,mate/wire and fault voltage OPEN |
| J503 | 1 | HOST I2C - MPN OPEN | OPEN | OPEN | 3.3 V host reference input;not a host power supply;100 kHz;pinout review draft |
| L201 | 1 | 6.8uH | XAL8080-682MED | OPEN | 6.8uH+/-20%;14.5mOhmmaxDCR;Isat14A30%typdrop;Irms8A20Crise;60V |
| Q101 | 1 | CSD19537Q3 | CSD19537Q3 | OPEN | 100 V VDS, +/-20 V VGS; 12.1 mOhm typical at VGS=10 V; custom SON land-pattern OPEN |
| Q102 | 1 | BSS138 | BSS138 | Package_TO_SOT_SMD:SOT-23 | 50 V VDS; +/-20 V VGS; driver relative to VIN_FUSED, NOT GND |
| R101 | 1 | 332k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%, 0.1 W, 75 V; reverse-input series >=300k |
| R102 | 1 | 54.9k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%, 0.1 W, 75 V |
| R103 | 1 | 348k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%, 0.1 W, 75 V; reverse-input current limited |
| R104 | 1 | 15.8k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%, 0.1 W, 75 V |
| R105 | 1 | 4.02k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1 W; approximately4.48 A nominal |
| R106 | 1 | 56.2k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1 W,75 V |
| R107 | 1 | 10k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1 W,75 V |
| R108 | 1 | 100k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1 W,75 V; LOCAL high-voltage test only |
| R201 | 1 | 33.2k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1W,50V |
| R202 | 1 | 100k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1W,50V |
| R203 | 1 | 24.4k | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1W,50V |
| R204 | 1 | 0 | OPEN | Resistor_SMD:R_0603_1608Metric | 0ohm link0.1W |
| R205 | 1 | 1k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1W,50V |
| R206 | 1 | 100k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1W,50V |
| R207 | 1 | 24.9k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1W,50V |
| R401 | 1 | 2mOhm KELVIN | WSL27262L000FEA | OPEN | 2 mOhm +/-1%;3 W per terminal thermal conditions;25 ppm/C;project pin convention;footprint OPEN |
| R402 | 1 | 10 | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1 W; matched filter pair |
| R403 | 1 | 10 | OPEN | Resistor_SMD:R_0603_1608Metric | 0.1%,0.1 W; matched filter pair |
| R404 | 1 | 10k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1 W;100kHz,target<=100pF local bus |
| R405 | 1 | 10k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1 W;100kHz,target<=100pF local bus |
| R406 | 1 | 4.7k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1 W;fit only if compatible with host pullups |
| R407 | 1 | 4.7k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1 W;fit only if compatible with host pullups |
| R408 | 1 | 10k | OPEN | Resistor_SMD:R_0603_1608Metric | 1%,0.1 W;local only;no host ALERT crossing |
| TP101 | 1 | INPUT_SHDN | OPEN | OPEN | Test only; not a load-current connector |
| TP102 | 1 | INPUT_FLT | OPEN | OPEN | Test only; not a load-current connector |
| TP301 | 1 | VOUT_5V1 | OPEN | OPEN | Test only; not a load-current connector |
| TP302 | 1 | VOUT_PROTECTED | OPEN | OPEN | Test only; not a load-current connector |
| TP401 | 1 | ALERT_LOCAL | OPEN | OPEN | Test only; not a load-current connector |
| TP402 | 1 | SHUNT_KPLUS | OPEN | OPEN | Test only; not a load-current connector |
| TP403 | 1 | SHUNT_KMINUS | OPEN | OPEN | Test only; not a load-current connector |
| TP404 | 1 | 3V3_LOCAL | OPEN | OPEN | Test only; not a load-current connector |
| TP501 | 1 | VIN_RAW | OPEN | OPEN | Test only; not a load-current connector |
| TP502 | 1 | VIN_PROTECTED | OPEN | OPEN | Test only; not a load-current connector |
| TP503 | 1 | LOAD_5V1 | OPEN | OPEN | Test only; not a load-current connector |
| TP504 | 1 | GND | OPEN | OPEN | Test only; not a load-current connector |
| U101 | 1 | TPS26630RGER | TPS26630RGER | Package_DFN_QFN:Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm | 4.5-60 V; 67 V abs; adjustable OV cutoff, no pulse-current boost; MODE open=latch |
| U201 | 1 | LM61460AANRJRR | LM61460AANRJRR | OPEN | 3-36V operating,42V VINabs,6AICclass;module5Acontinuous only;RJR customfootprintreviewrequired |
| U401 | 1 | INA228AIDGSR | INA228AIDGSR | Package_SO:VSSOP-10_3x3mm_P0.5mm | 2.7-5.5 V supply;0-85 V bus incl unpowered;address0x40 |
| U402 | 1 | TPS70933DBVR | TPS70933DBVR | Package_TO_SOT_SMD:SOT-23-5 | 30 V input;3.3 V nominal;EN internally enabled;reverse-current protection |
| U403 | 1 | TCA9517DGKR | TCA9517DGKR | Package_SO:VSSOP-8_3x3mm_P0.65mm | 3.3 V on both sides; power-off tolerant I/O; no B-to-B cascade |

Source/function/modification/rationale and qualification gates: [schematic review](../../../05_SCHEMATIC_REVIEW.md), [pin review](../PIN_AND_FOOTPRINT_REVIEW.md), [source register](../source_register.json).
