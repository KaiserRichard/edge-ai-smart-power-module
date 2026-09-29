# Buck and transient-voltage-suppressor primary-source review

KNOWN review date: 2026-09-29. Task identifier: brief 02, Task 1.
**Sheet 03 remains electrically open. R2 and R3 remain BLOCKED.
NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

This is source extraction and engineering interpretation. No SPICE or vendor-model
simulation was run. Page, section, figure, document and part numbers below are
source identifiers, not electrical results. Electrical quantities carry evidence
labels. `—` in a limit table means the manufacturer leaves that column blank;
it does not mean zero or a guaranteed unbounded range.

## Sources and visual review

| Source | Identity and local archive | Pages visually inspected |
| --- | --- | --- |
| [Texas Instruments LM61460 datasheet](https://www.ti.com/lit/ds/symlink/lm61460.pdf) | KNOWN revision SNVSBD5D, May 2019, revised July 2022; `third_party/documents/r2_protection/lm61460.pdf` | 4, 6, 7, 16, 17, 18, 20, 21, 22, 25, 31, 32, 33, 40, 41 |
| [Vishay SMBJ datasheet](https://www.vishay.com/docs/88392/smbj.pdf) | KNOWN document 88392, revision 09-Jan-2024; `third_party/documents/r2_protection/smbj.pdf`; appended disclaimer document 91000 has KNOWN revision 01-Jan-2026, verified in extracted text | 1, 2, 4 |

PDFKit rendered the archived pages to scratch images, which were inspected for
table alignment, limit-column placement, graph axes, legends and conditions.
Text extraction was used to locate passages; it did not substitute for those
visual checks. Scratch images are outside the repository. The unmodified source
archives, hashes, license/attribution handling and download records are owned by
`source_register.json`. Usage here is **referenced**, with no circuit or source
document copied into hardware and no manufacturer file modified.

## LM61460: output capacitors and stability guidance

**KNOWN:** Section 9.2.2.4, page 31, explicitly permits a low-equivalent-series-
resistance (ESR) electrolytic in parallel with ceramic capacitance. This is direct
manufacturer guidance, not an inference. Its stated purpose is to reduce required
ceramic capacitance. The following are starting points from the source tables,
not qualification of the captured circuit or a proposed polymer capacitor.

| Source row | Frequency | Output | Ceramic bank | Electrolytic branch | Feedforward capacitor CFF |
| --- | --- | --- | --- | --- | --- |
| Table 9-3, minimum | KNOWN 400 kHz | KNOWN 5 V | KNOWN 2 × 47 µF | None in this row | KNOWN 10 pF |
| Table 9-3, better transient | KNOWN 400 kHz | KNOWN 5 V | KNOWN 3 × 47 µF | None in this row | KNOWN 33 pF |
| Table 9-4, minimum | KNOWN 400 kHz | KNOWN 5 V | KNOWN 3 × 22 µF | KNOWN 1 × 470 µF, ESR 100 mΩ | KNOWN 10 pF |
| Table 9-4, better transient | KNOWN 400 kHz | KNOWN 5 V | KNOWN 4 × 22 µF | KNOWN 1 × 560 µF, ESR 100 mΩ | KNOWN 22 pF |

**KNOWN:** The continuation on page 32 says these recommendations assume typical
derating for KNOWN 16 V, X7R, automotive-grade ceramic capacitors. Initial
tolerance, temperature and applied voltage must be considered. These are nominal
component combinations, not manufacturer-guaranteed effective capacitance values.

**UNKNOWN:** No polymer-specific stability approval was found in this datasheet.
A search of the entire extracted document found no occurrence of “polymer.” A
different bulk ESR, ceramic bank, inductance and CFF combination requires its own
review and vendor-model/bench checks. In particular, the historical model's
ASSUMED 20 mΩ bulk ESR is different from the KNOWN 100 mΩ branch in Table 9-4.

**KNOWN:** Section 9.2.2.10, page 33, discusses CFF for phase margin/transient
response with low-ESR output capacitors and states that CFF must not be used when
the output-capacitor ESR zero lies below KNOWN 200 kHz. The mixed ceramic/bulk
network must be analyzed as a network; applying a single isolated capacitor's
ESR-zero formula is not sufficient to resolve the apparent interaction with the
Table 9-4 examples. **UNKNOWN:** stability of the proposed option-I network and
the appropriate final CFF. No schematic change follows from this review.

## LM61460: startup and switching behavior in faults

The limit columns below were visually checked. KNOWN table conditions: junction
temperature KNOWN −40 °C to +150 °C unless stated otherwise; typical values at
KNOWN +25 °C; default input KNOWN 13.5 V.

| Parameter | Minimum | Typical | Maximum | Definition/condition and source |
| --- | --- | --- | --- | --- |
| Soft-start tSS | KNOWN 3.5 ms | KNOWN 5 ms | KNOWN 7 ms | First switching pulse to reference reaching KNOWN 90%; input ≥ KNOWN 4.2 V. Section 7.5, page 7 |
| tSS2 | KNOWN 9.5 ms | KNOWN 13 ms | KNOWN 17 ms | First switching pulse to release of forced-pulse-width-modulation (FPWM) lockout if output not in regulation; input ≥ KNOWN 4.2 V. Page 7 |
| Hiccup wait tW | — | KNOWN 80 ms | — | Short-circuit wait interval; page 7 |
| Enable delay tEN | — | KNOWN 0.7 ms | — | EN high to first switching pulse, VCC capacitor KNOWN 1 µF, output initially KNOWN 0 V; page 7 |
| PGOOD rising delay | KNOWN 1.5 ms | KNOWN 2 ms | KNOWN 2.5 ms | tPGDFLT(rise), page 7 |
| High-side on-resistance | — | KNOWN 41 mΩ | KNOWN 82 mΩ | Intact high-side MOSFET; section 7.4, page 6 |
| Low-side on-resistance | — | KNOWN 21 mΩ | KNOWN 45 mΩ | Intact low-side MOSFET; section 7.4, page 6 |
| High-side current limit IL-HS | KNOWN 8.9 A | KNOWN 10.3 A | KNOWN 11.5 A | Duty approaches KNOWN 0%; limit decreases with duty. Page 6 and footnote on page 7 |
| Low-side current limit IL-LS | KNOWN 6.1 A | KNOWN 7.1 A | KNOWN 8.1 A | Page 6 |
| Negative-current limit IL-NEG | — | KNOWN −3 A | — | FPWM operation; positive current is out of SW. Page 6 |
| SW pull-down current IOV | — | KNOWN 0.5 mA | — | Overvoltage condition; page 7 |
| Bootstrap undervoltage threshold | — | KNOWN 2.1 V | — | CBOOT relative to SW, page 6; charging behavior described page 16 |

**KNOWN:** Sections 8.3.10 and Figure 8-8, pages 17–18, describe reference-ramp
soft start. Auto mode/diode emulation is used initially to avoid discharging a
prebiased output. FPWM and hiccup are disabled during soft start; they become
available on reaching regulation or tSS2, whichever occurs first. TI explicitly
mentions larger output capacitors and startup near current limit. This supports
investigating bulk, but does not prove that the complete module stays below its
upstream eFuse limit.

**KNOWN:** Section 8.3.12, pages 20–21, describes cycle-by-cycle high-side and
low-side limiting for an intact converter. High-side current is sensed after
blanking. If low-side current remains too high at the end of a cycle, low-side
conduction is extended until the current falls below its limit, then high-side
switching resumes subject to the clock condition. Hiccup requires an output below
approximately KNOWN 0.4 times its setpoint for KNOWN 128 consecutive cycles,
tSS2 elapsed, and absence of dropout. The device then shuts down and attempts
soft start after tW.

**KNOWN:** Section 8.3.7, page 16, says bootstrap undervoltage initiates a
charging sequence that turns the low-side switch on before another high-side
attempt. Section 8.4.3.4, page 25, likewise describes extending low-side
conduction under minimum-on-time operation. Section 8.4.3.3 allows reverse
current in FPWM and frequency reduction when the output is externally raised.

**UNKNOWN:** These descriptions do not specify behavior, survival or safe
operating area with an internally shorted high-side MOSFET. A failed high-side
resistance is not bounded by the intact device's KNOWN 41 mΩ typical on-resistance.
**INFERRED:** Commanding the low-side switch on while the high-side remains
physically shorted creates a direct input-to-ground path through the internal
switches. This can divert energy from the output but can also damage the
converter and change the fault topology. It must not be counted as a guaranteed
helpful protection mechanism. The simple fault model does not cover this path.

**KNOWN:** Absolute maximums, page 4: VIN and EN to ground KNOWN 42 V; BIAS and
FB to ground KNOWN 16 V; PGOOD to ground KNOWN 20 V. Recommended VIN maximum is
KNOWN 36 V. The captured schematic's annotation states BIAS is grounded, so this
review does not assume the typical application's raw-output BIAS connection.
Any future path-enable pullup must also respect PGOOD's own rating; the input-pin
rating is not a blanket rating for every pin.

## LM61460: available transient evidence

**KNOWN:** The datasheet contains load-transient waveforms, including:

| Figure | Conditions printed beside the waveform |
| --- | --- |
| 9-46, page 40 | KNOWN 5 V output; KNOWN 13.5 V input; KNOWN 400 kHz; auto mode; KNOWN 0 A → 6 A → 0 A; rise/fall each KNOWN 6 µs |
| 9-47, page 41 | Same printed electrical conditions as above, FPWM mode |
| 9-48, page 41 | KNOWN 5 V output; KNOWN 13.5 V input; KNOWN 400 kHz; auto mode; KNOWN 2 A → 5 A → 2 A; rise/fall each KNOWN 3 µs |

The vertical output scale in these figures is KNOWN 200 mV/division and the
horizontal scale is KNOWN 50 µs/division. **UNKNOWN:** a guaranteed worst-case
overshoot number for the captured circuit and proposed bulk network. No pixel
estimate is promoted to a guaranteed limit. These typical application traces
are useful evidence that load-release behavior exists in the source; they do not
close the brief's all-corner vendor-model requirement.

## Vishay SMBJ: exact electrical rows

**KNOWN:** The CA suffix denotes the bidirectional version, and page 1 explicitly
applies electrical characteristics in both directions. Page 2 conditions are
ambient temperature KNOWN +25 °C unless otherwise stated. The breakdown test
pulse is KNOWN ≤ 50 ms. No typical VBR or VC column is supplied.

| Parameter | SMBJ26CA | SMBJ30CA | Column/condition |
| --- | --- | --- | --- |
| Stand-off VWM | KNOWN 26 V | KNOWN 30 V | Specified stand-off |
| Breakdown VBR minimum | KNOWN 28.9 V | KNOWN 33.3 V | Minimum, at test current |
| Breakdown VBR maximum | KNOWN 31.9 V | KNOWN 36.8 V | Maximum, at test current |
| Breakdown test current IT | KNOWN 1 mA | KNOWN 1 mA | IT column |
| Reverse leakage ID | KNOWN 1 µA maximum | KNOWN 1 µA maximum | At respective VWM; brief calls this IR |
| Peak pulse current IPPM | KNOWN 14.3 A maximum | KNOWN 12.4 A maximum | Source waveform/derating applies |
| Clamping VC | KNOWN 42.1 V maximum | KNOWN 48.4 V maximum | At respective IPPM |
| VBR temperature coefficient | KNOWN +0.097 %/°C maximum | KNOWN +0.099 %/°C maximum | Specifically VBR, not VC |

**KNOWN:** Page 1 rates peak pulse power at KNOWN 600 W for the specified
KNOWN 10/1000 µs waveform, subject to the nonrepetitive pulse and thermal
derating notes. Figure 3, page 4, defines the KNOWN 10 µs rise and the
KNOWN 1000 µs time to half peak. The mounting note specifies KNOWN 5.0 mm ×
5.0 mm copper pads per terminal. These conditions must accompany pulse ratings.

**KNOWN:** Figure 2, page 4, has separate “Typical” and “Safety Operation Area”
curves. The latter falls linearly from KNOWN 100% at KNOWN +25 °C initial
junction temperature to KNOWN 0% at KNOWN +150 °C. Graph intersections give
KNOWN 60% at KNOWN +75 °C, KNOWN 40% at KNOWN +100 °C and KNOWN 20% at
KNOWN +125 °C. The upper “Typical” curve is not the safety-area limit.
**CALCULATED illustration:** multiplying the KNOWN 600 W pulse rating by the
KNOWN 40% graph factor gives CALCULATED 240 W at an ASSUMED +100 °C initial
junction temperature, for the same waveform and mounting conditions. It is not
a continuous power rating or a safe-energy guarantee for a different pulse.

**KNOWN:** Figure 1 gives pulse-power dependence on pulse duration; Figure 5
is explicitly a *typical* transient thermal-impedance plot. No arbitrary cable
hot-plug waveform or sustained adapter overvoltage is qualified by these plots.
**UNKNOWN:** actual hot-plug peaks, source energy and temperature-dependent VC
in this module.

## Corrections and qualifications to historical PROTECTION_ANALYSIS.md

| Historical statement | Source-based correction |
| --- | --- |
| Section 4 says the LM61460 datasheet gives no load-transient overshoot data | **KNOWN contradiction:** it contains transient waveforms on pages 40–41. A guaranteed all-corner maximum for this circuit is still **UNKNOWN**. |
| Section 6 labels parallel-electrolytic permission INFERRED | **KNOWN correction:** permission and starting combinations are explicit in section 9.2.2.4/Table 9-4. The particular low-ESR polymer implementation remains **UNKNOWN** for stability. |
| Section 9 uses a common temperature coefficient of ASSUMED/INFERRED 0.096 %/°C for the compared TVS devices | **KNOWN contradiction:** page 2 lists KNOWN 0.097 %/°C maximum for SMBJ26CA and KNOWN 0.099 %/°C maximum for SMBJ30CA. KNOWN 0.096 %/°C belongs to SMBJ24A/CA and SMBJ22A/CA. |
| Section 9 scales clamp voltage using the VBR coefficient | **UNKNOWN qualification:** the coefficient is specified for VBR, not VC. The old hot-clamp values remain **INFERRED**, not guaranteed temperature-corrected VC bounds. |
| Section 5 calls the startup interval KNOWN 3.5–7 ms without its endpoint | **KNOWN clarification:** tSS ends at KNOWN 90% reference after the first switching pulse. It is not a complete startup duration or proof of a linear full-output ramp. |
| Section 2 says omitted low-side conduction into a failed high side helps | **INFERRED qualification:** output-energy diversion is possible, but direct cross-conduction and subsequent damage are also possible. Intact-device current limiting provides no guaranteed failed-switch behavior. |

These findings do not select an architecture, modify historical evidence, approve
a capacitor or change any execution gate.
