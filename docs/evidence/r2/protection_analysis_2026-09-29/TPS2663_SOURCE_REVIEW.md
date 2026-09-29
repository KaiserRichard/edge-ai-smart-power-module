# TPS2663 source review

Date: 2026-09-29. Task 1 evidence only. Sheet 03 remains electrically OPEN; R2 and R3 remain BLOCKED. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

**EVIDENCE:** Texas Instruments, *TPS2663x 60V, 6A Power Limiting, Surge Protection Industrial eFuse*, document **SLVSE94G**, September 2018, revised June 2024. Source: <https://www.ti.com/lit/ds/symlink/tps2663.pdf>. Local source: `third_party/documents/r2_protection/tps2663.pdf`; hash/download provenance is in the [dated source register](source_register.json). TI copyright applies; this review references and paraphrases the source, with no upstream modification or circuit copying.

**EVIDENCE:** Native PDFKit rendered pages were visually inspected, not only text-extracted: printed/PDF pages **1, 6–9, 12–14, 18, 22–25, 27–28**. Relevant locations are electrical/timing tables, Figures 6-18, 7-1, 7-2, and sections 8.3.1.1, 8.3.7, 8.3.8, 8.3.12, 8.3.13 and 8.4. Page/section identifiers, dates, document revisions, and part numbers are source identifiers, not electrical quantities. Every numerical electrical entry below carries the label in its row or sentence. A `—` in a limit column means **UNKNOWN / not specified in that column**, not zero.

## Conditions and device applicability

**KNOWN — table conditions (§6.5/6.6):** Unless a row overrides them, ambient and junction temperature are equal and range from **−40 °C to +125 °C**; **4.5 V < V(IN_SYS) = V(IN) < 60 V**; **V(SHDN) = 2 V**; **R(ILIM) = 30 kΩ**; **C(OUT) = 1 µF**; `IMON`, `PGOOD`, `FLT` and `C(dVdT)` are OPEN. Electrical-characteristic columns are MIN/TYP/MAX; timing columns are MIN/NOM/MAX.

**KNOWN — captured-part applicability:** The existing input-protection review identifies **TPS26630RGER**. Its overcurrent operation limits at `I(OL)`. The pulse-current and adjustable output-power-limit behaviors of other family members must not be assigned to this device. In particular, the term `PLIM` appearing in a shared timer name does not mean TPS26630 implements an adjustable PLIM input.

## Current limit and fast trip

| Evidence label | Parameter and source | Minimum | Typical / nominal | Maximum | Conditions / implication |
| --- | --- | --- | --- | --- | --- |
| KNOWN | `I(OL)`, p. 7 | 4.185 A | 4.5 A | 4.815 A | `R(ILIM) = 4.02 kΩ`, `V(IN) − V(OUT) = 1 V`; external resistor tolerance is not separately added by this table. |
| KNOWN | `I(OL)`, p. 7 | 0.54 A | 0.6 A | 0.66 A | `R(ILIM) = 30 kΩ`, same differential voltage. |
| KNOWN | `I(OL)`, p. 7 | 1.84 A | 2 A | 2.16 A | `R(ILIM) = 9 kΩ`, same differential voltage. |
| KNOWN | `I(OL)`, p. 7 | 5.58 A | 6 A | 6.42 A | `R(ILIM) = 3 kΩ`, same differential voltage. |
| KNOWN | `I(FASTRIP)`, p. 7 | — | `2 × I(OL)` | — | TPS26630 and TPS26632 only; a comparator threshold, not a guaranteed overshoot-current ceiling. |
| KNOWN | `I(SCP)`, p. 7 | — | 45 A | — | Short-circuit-protect-current row. |
| KNOWN | `tFASTTRIP(dly)`, hot short, p. 9 | — | 1 µs | — | `I(OUT) > I(SCP)`; there is no maximum in this row. |
| KNOWN | `tFASTTRIP(dly)`, soft short, p. 9 | 2.2 µs | 3.2 µs | 4.5 µs | `I(FASTRIP) < I(OUT) < I(SCP)`. |
| KNOWN | `tCL_PLIM(dly)`, p. 9 | 129 ms | 162 ms | 202 ms | Maximum permitted duration of current limiting before fault action, subject to earlier thermal shutdown. The column headings distinguish the timer tolerance from the word “maximum” in its description. |
| KNOWN | `tCL_PLIM_FLT(dly)`, p. 9 | 1.09 ms | 1.3 ms | 1.6 ms | FLT assertion during current limiting; this is not the current-control settling time. |
| UNKNOWN | Closed-loop current-limit settling, overshoot and response waveform | — | — | — | The reviewed tables do not provide a guaranteed general response bound from crossing `I(OL)` to settled regulation. A vendor model and hardware waveforms are needed. |

**KNOWN — sequence (§8.3.7.2 and Fig. 7-2):** A sudden short can outrun the finite-bandwidth current-limit amplifier. Fast trip turns the internal field-effect transistor (FET) off; it remains off for a few microseconds, then turns on slowly to allow current regulation. The brief off/restart sequence occurs before the eventual overload latch-off decision. MODE-open therefore does not establish “no internal retry immediately after fast trip.” The unspecified “few microseconds” is **UNKNOWN** as a bounded duration.

**KNOWN — model value distinction:** Equation 5 specifies `I(OL) [A] = 18 / R(ILIM) [kΩ]`. **CALCULATED:** With the existing nominal resistor, **18 / 4.02 = 4.477612 A**. That equation-based value differs from the direct table's **KNOWN 4.5 A typical** at the same nominal resistor. The old script's **CALCULATED 4.48 A** is an equation-based rounded estimate, not an exact transcription of the table.

**CALCULATED, conditional on a KNOWN specified ±0.1% resistor tolerance and inverse-resistance scaling:** Applying that resistor tolerance to the direct table gives **4.185 / 1.001 = 4.180819 A** and **4.815 / 0.999 = 4.819820 A**. This is a tolerance-screen calculation, not an additional TI-guaranteed device row. The existing equation-based review gives a slightly different lower limit because it starts from Equation 5 rather than the table. Keep the two bases explicit.

## Power limit, overload duration, thermal response, and short-circuit SOA

**KNOWN — TPS26630 applicability (§8.3.8):** This device has no adjustable output-power-limit function. A downstream current-limit condition dissipates `(V(IN) − V(OUT)) × I(OL)` in its internal pass FET. Thermal shutdown can terminate current limiting before the overload timer expires. If the fault ends before either protection acts, later low current does not itself force a latched shutdown.

| Evidence label | Parameter and source | Minimum | Typical / nominal | Maximum | Applicability / conditions |
| --- | --- | --- | --- | --- | --- |
| KNOWN | PLIM selectable-pin threshold, p. 7 | 160 mV | 217 mV | 240 mV | TPS26632/33/35/36/37 only; no TPS26630 PLIM input. |
| KNOWN | PLIM sourcing current, p. 7 | 4.4 µA | 5.02 µA | 5.6 µA | `V(PLIM) = 0 V`, applicable PLIM variants. |
| KNOWN | Output power limit, p. 7 | 94 W | 100 W | 106 W | `R(PLIM) = 100 kΩ`, applicable PLIM variants. |
| KNOWN | Thermal-regulation setpoint `T(J_REG)`, p. 8 | 136 °C | 145 °C | 154 °C | Startup thermal-regulation loop. |
| KNOWN | Thermal-regulation timeout `t(Treg_timeout)`, p. 9 | 2.3 s | 2.54 s | 2.9 s | Separate from the overload timer. |
| KNOWN | Thermal-shutdown rising threshold, p. 8 | — | 165 °C | — | Typical protection threshold; not an operating-temperature target. |
| KNOWN | Thermal-shutdown hysteresis, p. 8 | — | 11 °C | — | Typical only. |
| KNOWN | Auto-retry delay `t(TSD_retry)`, p. 9 | 500 ms | 648 ms | 800 ms | `MODE = GND`; not the captured MODE-open operation. |

**KNOWN — starting into a short (§8.3.7.2.1):** The current initially limits at `I(OL)`; the thermal-regulation loop then reduces current to regulate die temperature. The thermal-regulation timer governs this startup case. The startup loop is enabled at power-up, undervoltage-lockout (UVLO) cycling, or SHDN turn-on and ceases once the FET is fully enhanced or its timer expires (§8.3.1.1). This behavior cannot be replaced by a fixed-current source for the entire startup-short event.

**KNOWN — Figure 6-18 limitation:** The visually inspected graph plots *typical thermal-shutdown time versus power dissipation*, with ambient-temperature curves and the note that it was taken on the VQFN device on an evaluation-module board. It is not a guaranteed pulsed safe-operating-area (SOA) boundary for the proposed board. No curve-derived time has been promoted to a guaranteed number here. **UNKNOWN:** Initial junction temperature, board thermal impedance, actual transient pass-FET dissipation, and guaranteed output-short survival for this implementation. These remain engineering-review and bench-validation items.

**CALCULATED screen:** The combination of **ASSUMED 24.72 V source**, **ASSUMED shorted output at 0 V**, and **KNOWN 4.815 A device-table maximum** gives **119.0268 W** instantaneous internal pass-FET dissipation while that current persists. This arithmetic does not establish duration, SOA survival or energy let-through; the current and thermal loops can change it.

**KNOWN — source inconsistency requiring caution:** Section 8.3.1.1 describes an approximately **2.5 s typical** startup thermal-regulation timer, but also contains a sentence referring to **1.25 s typical** in the same discussion. Section 8.3.7.2.1 repeats approximately **2.5 s typical**, while the actual timing table gives **2.3 / 2.54 / 2.9 s MIN/NOM/MAX**. Record the inconsistent prose; do not silently reinterpret it as a second guaranteed timer.

## Overvoltage timing endpoint

| Evidence label | Parameter and source | Minimum | Typical / nominal | Maximum | Exact test meaning |
| --- | --- | --- | --- | --- | --- |
| KNOWN | OVP rising threshold, p. 6 | 1.176 V | 1.2 V | 1.224 V | Threshold at the OVP pin. |
| KNOWN | OVP falling threshold, p. 6 | 1.09 V | 1.122 V | 1.15 V | Threshold at the OVP pin. |
| KNOWN | `OVP_tOFF(dly)`, p. 8 | 8.5 µs | 11 µs | 14 µs | OVP rising to **20 mV above its rising threshold**, ending at **FLT falling**. Figure 7-1 shows the endpoint when FLT falls to **10%** of its high level. |
| UNKNOWN | Guaranteed OVP threshold-to-pass-FET-isolation time | — | — | — | The name “OVP switch turnoff delay” does not change the specified FLT endpoint into a FET-current endpoint. |

**DECISION:** Do not use **KNOWN 14 µs maximum FLT delay** as a proven maximum interval of source-current flow, and do not use the fast-trip comparator threshold as a source-current clamp. The old input hot-plug charge calculation needs a current waveform and a verified isolation endpoint before it can bound the downstream input voltage.

## Shutdown, latch reset, and resistance

| Evidence label | Parameter and source | Minimum | Typical / nominal | Maximum | Conditions / consequence |
| --- | --- | --- | --- | --- | --- |
| KNOWN | SHDN open-circuit voltage, p. 7 | 2.48 V | 2.7 V | 3.3 V | `I(SHDN) = 0.1 µA`. |
| KNOWN | SHDN low control condition, pp. 7, 28 | 0.8 V in MIN column | — | — | The application text instructs pulling below this voltage to turn the internal and external FETs off. |
| KNOWN | SHDN enable control condition, pp. 7, 28 | — | — | 2 V in MAX column | The application text instructs pulling to at least this voltage to enable. |
| KNOWN | SHDN sink capability needed, p. 28 | 10 µA | — | — | Control driver must sink at least this current; the p. 7 leakage row lists **−10 µA** in MIN at `V(SHDN) = 0 V`. |
| KNOWN | SHDN-to-FET-off delay, p. 8 | 0.8 µs | 1 µs | 1.5 µs | SHDN falling below `V(SHUTF)` to **FET OFF**; unlike the OVP row, this endpoint is explicit. |
| KNOWN | Shutdown supply current, p. 6 | — | 21 µA | 60 µA | `V(SHDN) = 0 V`. |
| KNOWN | Pass-FET `R_ON`, p. 7 | 26 mΩ | 30.44 mΩ | 34.5 mΩ | `0.6 A ≤ I(OUT) ≤ 6 A`, junction at **25 °C**. |
| KNOWN | Pass-FET `R_ON`, p. 7 | 19 mΩ | 30.44 mΩ | 53 mΩ | Same current interval, junction from **−40 °C to +125 °C**. |

**KNOWN — MODE-open operation (Table 8-1):** TPS26630 eventually latches off after the current-limit timer, or can turn off earlier for thermal protection. The overload latch can be reset by SHDN low-to-high, UVLO low-to-high, **or** cycling IN_SYS. MODE-open is not a guarantee that only physical input removal can reset the eFuse. Enabling from SHDN starts the dVdT ramp. Any system-level “no re-enable while input is present” policy requires separate analysis of these reset paths and the proposed output-protection latch.

## Corrections to the historical protection analysis

The dated `protection_analysis_2026-09-26/PROTECTION_ANALYSIS.md` is preserved. Its following statements require correction or narrower interpretation:

- **KNOWN contradiction, §§2 and 9:** The expression **“2 × I(OL) for ~1 µs”** treats a typical threshold as a current ceiling and applies a hot-short typical timing value outside its specified high-current condition. The soft-short timing table instead has **KNOWN 4.5 µs maximum** in its stated range; the hot-short **KNOWN 1 µs nominal** has no published maximum. There is an off/restart phase before current regulation.
- **CALCULATED historical claim invalid as a bound, §9:** The old **72 µC** charge, **4.8 V** increase and approximately **33 V** buck-input peak follow from an **ASSUMED current envelope and isolation interval**, not a guaranteed datasheet envelope. The text correctly notices FLT as the endpoint, but still describes opening within the same **KNOWN 8.5–14 µs FLT interval**. Acceptance of the buck-input voltage ceiling remains **UNKNOWN**.
- **KNOWN correction, §§5–6:** **162 ms** is the overload timer's nominal value, not a maximum bound. The published maximum is **202 ms**, and thermal shutdown may occur earlier. Startup into a short has a separate thermal-regulation timer. Consequently a crowbar/eFuse interaction cannot be bounded solely by the nominal overload timer.
- **KNOWN qualification, §5:** MODE-open removes the eventual configured overload auto-retry mode, but does not remove the fast-trip off/restart sequence or reset by UVLO/SHDN while the upstream source remains present. The statement that the eFuse “never trips once the bulk is charged” is at most **INFERRED**, conditional on surviving the preceding charging/overload/thermal transient without latching.
- **KNOWN clarification, §2:** The **34.5 mΩ** maximum eFuse resistance is valid at **25 °C** only; **53 mΩ** is the full-temperature published maximum. The former is correctly temperature-labelled in the old script, but is not a hot-corner bound.

**RESULT:** The source supports a finite-bandwidth current limiter with fast trip, off/restart, overload timing, and thermal intervention. It does not support instantaneous current limiting or the historical hot-plug let-through bound. No SPICE simulation was run for this source review; all SPICE results are **NOT RUN**.
