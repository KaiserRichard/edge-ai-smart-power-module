# Input fault envelope and transient coordination

2026-09-14. **Current SMBJ26CA direction: NOT QUALIFIED for LM61460 coordination. D101 and circuitry unchanged.**

## Envelope worksheet

| Condition / parameter | Class | Value / consequence |
| --- | --- | --- |
| Normal connector input | REQUIREMENT | 9..24V DC; tolerance outside endpoints OPEN |
| Allowed sustained overvoltage | OPEN | No source-fault duration/maximum approved. Existing OVP setting is not a permission to operate there |
| Captured eFuse OV trip | CALCULATED | 26.974..28.289V rising; 24.997..26.582V falling; regulator/input divider tolerance and leakage screen |
| Positive surge candidate | ASSUMED analysis direction | Adapter hot-plug/cable ringing; external surge test only if relevant standard/class is approved |
| Source/cable L | OPEN | Need loop length/routing or measured/modelled inductance. `V=L*di/dt` and `E=0.5*L*I^2` govern ringing energy |
| Source impedance / available current | OPEN | Need R/L, adapter foldback/time response, source reservoir capacitance and battery/protection details if applicable |
| Prospective source short circuit | OPEN | Not bounded by downstream eFuse's4.8A limit; F101/TVS share upstream path |
| Negative/reverse event | OPEN | Amplitude/duration/repetition, cable interruption and D102 dynamic clamp needed; bidirectional D101 does not by itself clamp a negative pulse near ground |
| TPS26630 | DATASHEET | 4.5..60V operation; IN/OUT67V absolute max with pin-specific exceptions; IN_SYS/IN75V transient allowance only under stated10ms/25C conditions. Not a general75V operating rating |
| LM61460 | DATASHEET | VIN36V recommended operating maximum,42V absolute maximum; pin differentials and negative limits also apply. Absolute maximum is not a design clamp target |

Sources: [TI TPS2663 SLVSE94G](https://www.ti.com/lit/ds/symlink/tps2663.pdf), §§6.1/6.3/6.5 and surge applications, stored `third_party/documents/TI_TPS2663_SLVSE94G.pdf`; [TI LM61460 SNVSBD5D](https://www.ti.com/lit/ds/symlink/lm61460.pdf), ratings/operating conditions; existing [input capture/calculations](../INPUT_PROTECTION.md). No EVM's certified surge class is transferred to V1A.

## Exact primary TVS evidence

**EVIDENCE:** Vishay SMBJ family document88392, rev09-Jan-2024, [primary PDF](https://www.vishay.com/docs/88392/smbj.pdf), local `third_party/documents/r2_qualification_2026-09-14/Vishay_SMBJ.pdf`. Page1 specifies CA for bidirectional versions. D101's existing generic candidate does not freeze Vishay manufacturer/packing suffix; this is an identified vendor implementation screened without changing the BOM.

| SMBJ26CA quantity | DATASHEET condition/value | Meaning |
| --- | --- | --- |
| Standoff VWM | 26V | Voltage at which specified reverse leakage applies, not the clamping voltage |
| Breakdown VBR | 28.9..31.9V at1mA | Avalanche test range at a small test current; not a guarantee of clamp at surge current |
| Clamping VC | 42.1V maximum at14.3A peak | Under the specified10/1000us waveform/temperature conditions |
| Peak pulse power | 600W at25C reference | Pulse/temperature/land conditions apply; not a continuous rating |
| Breakdown temperature coefficient | Max0.097%/C for26V row | Breakdown rises with temperature; cannot use this alone as a complete hot VC curve |

Visual review covers p2 electrical table and p4 curves. Figure1 bounds pulse-power versus width for stated5x5mm copper pad areas. Figure2's safety operating curve derates pulse capability from25C to zero at150C; at100C its linear curve corresponds to roughly40% (a curve reading, not a new device specification). Figure3 defines10us rise and1000us half-value time. None is an arbitrary I-V transfer curve permitting guaranteed interpolation from31.9V/1mA to42.1V/14.3A.

**CALCULATED rejection screen:** `42.1 - 42 = 0.1V` beyond LM61460 absolute maximum even before parasitic overshoot. `42.1*14.3=602.03W` is the rounded peak-product, not pulse energy. At a lower surge current the actual clamp may be lower, but the source and a guaranteed current/temperature-dependent clamp bound are unavailable. The tiny nominal voltage margin cannot support a safety claim.

**eFuse timing evidence:** SLVSE94G labels `OVP_tOFF(dly)` switch-turnoff delay8.5/11/14us; table condition is OVP20mV above rising threshold to FLT falling. Respect that endpoint: do not convert it into a guaranteed output-terminal voltage-isolation waveform. With the348k/15.8k divider,20mV detector overdrive corresponds to about0.461V at the sensed input before resistor tolerances. Near-threshold and fast-rise behavior, internal FET cutoff, parasitic feedthrough and local input capacitance still determine buck VIN. A steady28.289V trip does not demonstrate that a fast surge stays below42V at U201.

## Candidate directions, no circuit change

1. **Retain high-voltage input TVS plus eFuse isolation**, only if a source-specific transient model and manufacturer timing/let-through evidence bound U201 below its limits with margin. Include D101 lead/trace inductance, eFuse input/output caps, source impedance and negative excursions.
2. **Lower-voltage TVS direction:** Vishay SMBJ24CA table gives24V standoff,26.7..29.5V breakdown at1mA,38.9V clamp at15.4A. It has only3.1V at the stated cold clamp before42V and no tolerance above24V nominal standoff. This is a screened candidate direction, not an approved replacement; normal tolerance, hot clamp, pulse/thermal and fuse coordination remain OPEN. A larger pulse-power package may improve current capability but does not automatically lower worst clamp.
3. **Surge stopper / appropriately rated clamp stage** if required steady or pulse energy cannot be managed by the present cutoff scheme. Selecting another controller or adding a clamp changes hardware architecture and requires explicit approval with a concrete circuit and thermal/SOA analysis.

**Closure evidence required:** approved source waveforms and prospective fault current; source-specific fuse total-clearing/TVS energy; guaranteed clamp including temperature and overshoot; eFuse let-through at actual detector overdrive and capacitance; negative clamp dynamics; upstream FET VDS/VGS and SOA. Use simulation only with stated model limitations, followed by R5 scope captures at source, D101, eFuse OUT and U201 VIN. Failure: any absolute-limit violation, excessive TVS energy/temperature, failed interrupt, uncontrolled restart or damaging negative excursion. No surge or hardware validation was performed.
