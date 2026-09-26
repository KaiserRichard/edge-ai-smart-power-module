# Current V1A architecture

As received on 2026-09-26; this summarizes captured choices without changing or releasing them. Source: [input review](../evidence/r2/INPUT_PROTECTION.md), [buck review](../evidence/r2/BUCK_DESIGN.md), [monitor review](../evidence/r2/MONITOR_POWER_DOMAINS.md), [calculations](../evidence/r2/calculations.json), and current `hardware/kicad/` sources. Later footprint assignments are recorded in [engineering state](03_ENGINEERING_STATE.md).

## Input protection

`VIN_RAW → F101 → VIN_FUSED → Q101 CSD19537Q3 → VIN_EFUSE_IN → TPS26630 → VIN_PROTECTED`

The reverse-input arrangement includes BSS138; SMBJ26CA transient suppression and B260 are captured devices. Final F101, source fault envelope, and transient coordination remain OPEN.

| Captured setting | CALCULATED nominal result |
| --- | --- |
| R101 332 kΩ / R102 54.9 kΩ | Undervoltage lockout (UVLO) rising approximately 8.46 V |
| R103 348 kΩ / R104 15.8 kΩ | Overvoltage protection (OVP) threshold approximately 27.63 V |
| R105 4.02 kΩ | Input current limit approximately 4.48 A |
| C103 100 nF | Approximately 48 ms voltage ramp at 24 V; this is a time estimate, not a current rating |

These nominal calculations do not qualify tolerance corners, hot-plug, safe operating area (SOA), or source faults.

## Buck regulator

LM61460AANRJRR, approximately 400 kHz; timing resistor (RT) 33.2 kΩ; L201 XAL8080-682MED, 6.8 µH. Feedback (FB) 100 kΩ / 24.4 kΩ gives approximately 5.098 V. Feedforward capacitor (CFF) 22 pF with 1 kΩ; bootstrap resistor (RBOOT) 0 Ω; BIAS grounded. Feedback senses the local raw regulated output, not beyond the open protection boundary.

The captured capacitor strategy uses two 22 µF / 50 V input ceramics, split 100 nF local input bypassing, and six 22 µF / 50 V output ceramics. Bootstrap and internal-supply decoupling are separate. The large banks use the TDK C5750X7R1H226M250KB candidate. Effective capacitance under bias/temperature and physical land qualification remain OPEN; nominal capacitance is not an established minimum. See [capacitor worksheet](../evidence/r2/forensic_2026-09-14/CAPACITOR_QUALIFICATION.md).

**CALCULATED, not MEASURED:** at 24 V / 5 A, nominal inductor ripple approximately 1.476 A, peak approximately 5.738 A, screening corner peak approximately 6.139 A, and root-mean-square (RMS) current approximately 5.018 A. Reproduce with `python3 scripts/calculate_r2.py`. Assumed component bounds and loss estimates remain conditional.

## Output and monitoring

`VOUT_5V1 → OPEN ARCHITECTURAL BOUNDARY → VOUT_PROTECTED → R401 → LOAD_5V1`

No switch, jumper, or bypass closes Sheet 03. Independent output protection must be qualified against the load voltage/time/energy and reverse-feed requirements before capture.

INA228AIDGSR measures the WSL27262L000FEA 2 mΩ four-terminal Kelvin shunt. TPS70933 supplies the local 3.3 V domain from `VOUT_PROTECTED`; TCA9517 interfaces local and host Inter-Integrated Circuit (I2C) domains. Local and host supply/pull-up ownership remain separate. Bus voltage is sensed on the load side; the local monitor supply branches before the shunt. The open protection boundary causes the expected U402 pin 1 undriven-power condition.
