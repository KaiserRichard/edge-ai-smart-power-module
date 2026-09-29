# Task 4 follow-up — verified candidate comparison

2026-09-29. **Research only; no selection. Sheet 03 OPEN; R2/R3 BLOCKED.
NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** This supersedes the
unfetched-specification entries of the earlier [candidate worksheet](OPTION_I_CANDIDATES.md)
where primary evidence is now available. Its provisional gate-stage, reset-policy,
clamp, hysteresis and timing gaps remain open.

The conductor follow-up permits official sources only for the already-listed
candidates and their exact variants. [Acquisition provenance](candidate_source_register.json)
records each original URL, failure, replacement URL, revision, SHA-256, cache path,
rights and use. Ten original PDFs were archived unchanged in ignored
`third_party/documents/r2_protection_candidates/`. Nexperia's three candidate PDFs
were readable through the web PDF service but direct byte downloads returned
HTTP 403: the remote readings below are KNOWN source observations, with original
byte hashes and local archival still UNKNOWN. No manufacturer design was copied.

PDFKit text was checked against visual renders for PCH/PCX ordering tables,
TLV3501 offset/drift columns and REF50 grade columns. Other cited rows were
reviewed in their native extracted tables; their exact conditions accompany them.
Document/page/part identifiers and component counts are identifiers; electrical
and geometry numbers inherit the indicated KNOWN or CALCULATED label.

## Bulk capacitor configurations (candidates, not BOM selections)

Sources: [Nichicon PCH](https://www.nichicon.co.jp/english/_assets/images/products/catalog/corporate/digital/PCH_e.pdf),
undated revision, sheet marking “as of May 2024”, pp. 1–2; and
[Nichicon PCX](https://www.nichicon.com/getmedia/c54df361-a881-4909-8693-f323ccebbb38/e-pcx.pdf),
CAT.8100M, pp. 1–2. Exact served bytes are pinned; the marking is not an invented
publication date. Both specify KNOWN ±20% initial capacitance at 20 °C/120 Hz,
and allow KNOWN ±20% change after their stated endurance tests. No minimum at
5.1 V over the full application life/temperature/frequency is established here.

| Candidate bank | KNOWN per-device ratings | CALCULATED bank screen | KNOWN mechanical envelope / remaining land issue |
| --- | --- | --- | --- |
| Two PCH1V471MCL1GS | 35 V, 470 µF; initial ESR ≤14 mΩ at 20 °C/100 kHz; after-endurance ESR ≤28 mΩ at −40 °C/100 kHz; ripple 3.1 Arms at 135 °C/100 kHz | 940 µF nominal; 752 µF at initial low tolerance; 601.6 µF with sequential 0.8×0.8 screen; ideal matched parallel ESR ≤7 / 14 mΩ at the respective tests | Each Ø10 ×16 mm class; drawing L=16±0.5 mm, platform B/C=10.3±0.2 mm, A=11±0.2 mm. Two bodies require at least twice that area plus assembly spacing. |
| Three PCH1V331MCL1GS | 35 V, 330 µF; initial ESR ≤16 mΩ; after-endurance low-temperature ESR ≤32 mΩ under the same tests; ripple 2.8 Arms per device | 990 µF nominal; 792 µF initial low; 633.6 µF sequential screen; ideal matched ESR ≤5.333 / 10.667 mΩ | Each Ø10 ×12.7 mm class; drawing L=12.6±0.5 mm; same platform dimensions. Lower height, three placements. |
| Eight PCX1V101MCL1GS | 35 V, 100 µF; ESR ≤29 mΩ at 20 °C/100 kHz; ripple 2.6 Arms at ≤105 °C or 0.99 Arms above 105 through 125 °C | 800 µF nominal; 640 µF initial low; 512 µF sequential screen; ideal initial ESR ≤3.625 mΩ | Each Ø10 ×12.7 mm class, L=12.6 +0.1/−0.4 mm; platform A=11±0.2, B/C=10.3±0.2 mm. Eight placements have substantial area cost. |

The sequential endurance screen is CALCULATED, not a complete guaranteed effective
capacitance. Actual bank ripple capability is UNKNOWN until current sharing,
frequency multipliers, heating and placement are checked. The catalog package
outlines are not solder lands: exact final land/courtyard/reflow-process approval
remains OPEN; PCX explicitly refers land dimensions to its separate guidelines.
A lone nominal 470 µF part still fails the 470 µF minimum. None of these banks
establishes the margin study's **1000 µF effective minimum**. At ASSUMED ±20%
initial tolerance alone that needs CALCULATED ≥1250 µF nominal; with the same
sequential endurance screen it needs CALCULATED ≥1562.5 µF nominal. These are
sizing calculations, not additional part selections.

## References and comparators

| Exact candidate | Source-backed specification | Error / timing implication | Package / example land |
| --- | --- | --- | --- |
| REF3325AIDBZR.A | [TI REF33, SBOS392I, Apr 2026](https://www.ti.com/lit/gpn/REF33), pp. 5–7: KNOWN 2.5 V, initial ±0.15% at 25 °C, drift ≤30 ppm/°C over −40…125 °C, specified input Vout+0.2…5.5 V. Turn-on settling to 0.1% with 1 µF is KNOWN 2 ms **typical**, no maximum. | Meets the ≤0.5% initial target. Does not meet the earlier ASSUMED 10 ppm/°C allocation. CALCULATED full-span drift screen 30×165 ppm=0.495%; a box-method coefficient is not a guaranteed linear local slope. Reference-valid delay remains OPEN. | KNOWN DBZ0003A, height ≤1.12 mm; drawing 4214838/F (08/2024), PDF p34: pad centers 2.1 mm apart, pad length 1.3 mm, pitch 0.95 mm. CALCULATED pad envelope 3.4×2.5 mm; courtyard extra. |
| REF5025IDGKR (high grade) | [TI REF50, SBOS410O, Oct 2025](https://www.ti.com/lit/gpn/REF50), pp. 7–8: KNOWN 2.5 V; initial ±0.05%; drift ≤3 ppm/°C over −40…125 °C; minimum input 2.7 V; current ≤1.2 mA over temperature. Turn-on to 0.1%/1 µF KNOWN 200 µs **typical**. | Initial/drift allocations fit individually; CALCULATED full-span drift 0.0495%. Load-regulation test requires Vout+0.75 V; ASSUMED 3.3 V supply has only CALCULATED 50 mV nominal headroom to that test condition. LDO tolerance/transients need inclusion; no guaranteed reference-ready time. | KNOWN DGK0008A, height ≤1.1 mm; 4214862/A (04/2023), PDF p50: 4.4 mm centers, 1.4×0.45 mm pads, 0.65 mm pitch. CALCULATED pad envelope 5.8×2.4 mm. |
| TLV3501AIDBVR | [TI SBOS321E, Apr 2016](https://www.ti.com/lit/ds/symlink/tlv3501.pdf), pp. 5–6: KNOWN push-pull, specified supply 2.7…5.5 V; offset ±6.5 mV maximum at 25 °C; drift ±5 µV/°C **typical**; hysteresis 6 mV **typical**. Propagation ≤12 ns over −40…125 °C at 5 mV overdrive, 100 mV input step (characterization assurance footnote). | No exact guaranteed 10 mV row. The smaller-overdrive row supports fast-comparator investigation, but interpolation/ramp behavior remains INFERRED, not a new maximum. Offset exceeds the earlier ±3 mV allocation; drift/hysteresis maxima remain UNKNOWN. | KNOWN DBV0006A, height ≤1.45 mm; 4214840/G (08/2024), PDF p31. CALCULATED 3.7×2.5 mm pad envelope from 2.6 mm centers, 1.1×0.6 mm pads, 0.95 mm pitch. |
| TLV3601DBVR | [TI SNOSDB1E, Apr 2023](https://www.ti.com/lit/ds/symlink/tlv3601.pdf), pp. 5,7–8: KNOWN push-pull, 2.4…5.5 V supply; offset ±5 mV over −40…125 °C, bias ≤5 µA; hysteresis 1.5…5 mV. Delay ≤4.5 ns at 50 mV overdrive/underdrive and 5 pF load, including 3.3 V supply. | Guaranteed delay at 10 mV remains UNKNOWN; typical dispersion plot cannot supply it. Input bias invalidates the old high-impedance divider leakage allocation; calculation below. | KNOWN DBV0005A, height ≤1.45 mm; 4214839/K (08/2024), PDF p37. Same CALCULATED 3.7×2.5 mm pad envelope. |

Package-envelope calculations describe occupied copper, not finished footprints,
assembly clearance or area of the entire block. Bypass/filter parts add area.
No comparator has been shown to survive the raw fault through the proposed divider
without a reviewed clamp. Beyond-rail common-mode behavior does not mean tolerance
of the CALCULATED approximately 13 V sense input from a 28.3 V raw rail.

## Detector supply and latch

| Exact candidate | KNOWN primary values and conditions | Budget / startup / reset gap | Package comparison |
| --- | --- | --- | --- |
| TPS70933DBVR | [TI SBVS186H, Jul 2021](https://www.ti.com/lit/ds/symlink/tps709.pdf), pp. 4–5: input 2.7…30 V, output 3.3 V; DC accuracy ±1% at stated conditions over −40…85 °C; startup ≤600 µs to 95% with 47 Ω load; dropout ≤650 mV at 50 mA and ≤1.4 V at 150 mA | Meets ≥30 V input target only at its endpoint; historical 28.3 V screen leaves CALCULATED 1.7 V operating headroom. Exact rail-valid/reset supervision, reference settlement, full thermal budget and future converter fault bound remain OPEN. Existing downstream U402 cannot independently authorize its own upstream path. | KNOWN DBV0005A, height ≤1.45 mm; PDF p34, 4214839/K; CALCULATED pads 3.7×2.5 mm. |
| TPS7A1633DGNR | [TI SBVS171F, Oct 2015](https://www.ti.com/lit/ds/symlink/tps7a16.pdf), pp. 5–6 and ordering addendum: input 3…60 V, fixed 3.3 V variant, overall accuracy ±2% under stated headroom/load conditions; UVLO 2.7 V **typical**; power-good rising 85…95% of output | Wider input rating alone does not qualify future HV pass-through. PG can assert below the voltage needed by the reference/logic; no universal detector-valid or reset bound. Thermal/current derating footnote applies, not unrestricted 100 mA at high VIN. | KNOWN DGN0008C, height ≤1.1 mm; 4218838/A (11/2017), PDF p35. CALCULATED pad extent 5.8 mm across leads; thermal metal example reaches 3 mm longitudinally. Thermal pad/vias and passives required. |
| SN74LVC1G74DCTR | [TI SCES794G, Sep 2021](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf), pp. 6–8: 1.65…5.5 V; async PRE/CLR low→Q delay ≤7.9 ns at 3.3 V, −40…125 °C, specified 50 pF test; low pulse ≥2.7 ns | Known logic delay fits an allocation. No guaranteed desired power-up state or retention through power loss; simultaneous preset/clear and release ordering need reviewed logic. Reset-only-at-UVLO still conflicts with no re-enable during input-present brownout. | KNOWN DCT0008A, height ≤1.3 mm; 4220784/D (10/2025), PDF p20. CALCULATED pad envelope 4.9×2.35 mm from 3.8 mm centers, 1.1×0.4 mm pads, 0.65 mm pitch. |
| SN74LVC2G02DCTR | [TI SCES194N, May 2019](https://www.ti.com/lit/ds/symlink/sn74lvc2g02.pdf), pp. 5–7: 1.65…5.5 V; per-gate delay ≤5.9 ns at 3.3±0.3 V, −40…125 °C, specified 50 pF test | CALCULATED two-gate propagation allowance 11.8 ns only under valid logic conditions; not a metastability/reset resolution bound for a feedback latch. Supply/reset/priority analysis remains OPEN. | KNOWN same DCT0008A geometry, PDF p18; CALCULATED same 4.9×2.35 mm pad envelope. |

## Gate-stage candidates: remote evidence and unresolved complete circuit

[Nexperia MMBT3904](https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf)
(8 Apr 2026, pp. 1–3) and
[MMBT3906](https://assets.nexperia.com/documents/data-sheet/MMBT3906.pdf)
(10 Apr 2025, pp. 1–3): KNOWN absolute VCEO magnitudes 40 V, IC magnitude 200 mA;
SOT23 body 2.9×1.3×1 mm, pitch 1.9 mm; pins B/E/C=1/2/3. KNOWN 25 °C ICBO
magnitude ≤50 nA at |VCB|=30 V; not a hot full-stage ≤1 µA guarantee. At |IC|=50 mA,
|IB|=5 mA, VCEsat magnitude ≤0.3 V (NPN) / ≤0.4 V (PNP). KNOWN turn-on delay/rise
limits each 35 ns apply at only |IC|=10 mA, |IB|=1 mA, 25 °C. These conditions
cannot establish the required charge-removal waveform. Full stage footprint,
level shifting, hot leakage, SOA and OUT-relative undershoot remain UNKNOWN.

[Nexperia 2N7002](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf)
(Rev. 7, 8 Sep 2011, pp. 1–5): KNOWN 60 V class SOT23; RDS(on) ≤5.3 Ω at 4.5 V
VGS, 75 mA, 25 °C; ≤9.25 Ω at 10 V VGS, 500 mA, 150 °C. No corresponding
3.3 V drive guarantee. KNOWN drain leakage ≤10 µA at 48 V/150 °C cannot prove
the brief's ≤1 µA idle limit at the actual HGATE voltage. KNOWN turn-on ≤10 ns
uses 10 V gate drive and specified resistive test circuit, not a gate-discharge
waveform. Source-referenced driver and final hold are still missing. Original
PDF archival and exact land drawing review remain OPEN after HTTP 403.

## Updated budgets: why research does not close criterion 3

At ASSUMED Rtop=11.6 kΩ/Rbottom=10 kΩ and 2.5 V reference, CALCULATED Thevenin
resistance is 5.37037 kΩ. TLV3601's KNOWN 5 µA bias maximum gives CALCULATED
26.8519 mV sense shift, or 1.07407% of the reference, before its CALCULATED 0.2%
offset contribution. That already exceeds the proposed ±1.1% window when combined.
Lower divider impedance could reduce bias error but adds loading/stress and changes
the complete clamp/feedback design; no new resistor choice is selected.

For TLV3501, CALCULATED 6.5 mV/2.5 V=0.26% initial offset, rather than the old
ASSUMED 0.12% allocation. Its drift and built-in hysteresis lack maximum rows here.
With REF5025 high grade, a **partial**, conditional sum is CALCULATED
0.05% initial +0.0495% full-span reference drift +0.054% divider tolerance
+0.027% ASSUMED divider drift +0.26% initial comparator offset = **0.4405%**.
Leakage, comparator drift, hysteresis, clamp errors, line/load/noise, temperature
correlations and interaction reserves are excluded and remain OPEN. REF3325's
reference terms alone can reach CALCULATED 0.645% on the same full-span screen.
Therefore neither the historical ±0.671% allocation nor a new complete ±1.1%
window is demonstrated by the listed candidates.

Conditional timing: KNOWN TLV3501 ≤12 ns at its stated step/overdrive plus KNOWN
latch ≤7.9 ns totals CALCULATED 19.9 ns **only for those endpoints/conditions**.
Slew-to-overdrive, clamp settling, source-referenced level shift and MOSFET isolation
are not covered. The historical ASSUMED 96 nC charge and KNOWN opposing 75 µA
still require CALCULATED ≥60.075 mA average sink for an ASSUMED 1.6 µs discharge.
No listed circuit proves it across voltage, temperature, Miller dynamics and tail
current. Nor is HGATE≥OUT−0.3 V or hot idle leakage ≤1 µA established.

**Task 4 result:** source-backed candidate specifications and package comparisons
are now available to the extent above; remaining unavailable archival/land data
are individually identified. **Criterion 3 remains FAIL to demonstrate**, and the
reset policy remains unresolved. A fast comparator and available capacitor bank
are not a complete protection circuit. No selection or capture follows from this
research.
