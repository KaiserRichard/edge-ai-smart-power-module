> Context note (2026-09-26): this dated document preserves earlier requirements/review history. Read [current engineering state](context/03_ENGINEERING_STATE.md) and [current architecture](context/02_V1A_ARCHITECTURE.md) before interpreting selections or release claims. Local cache/scratch paths mentioned below are archived external evidence; see [reference restoration](../third_party/README.md).

# V1A component-selection review

Date: 2026-09-11. **RECOMMENDED FOR R2 REVIEW — no component is APPROVED / FROZEN.**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## Basis of comparison

Use the [requirements register](00_REQUIREMENTS.md), not predecessor ratings. Screening assumes approximately 5 V/5 A, with 6 A only a peak-load question and 9–24 V only a candidate source envelope. A 28-V maximum normal input changes the preferred voltage class. Efficiency and thermal figures below are manufacturer reference data or calculations, never measurements of V1A.

Source IDs and exact revisions are in the [audit](01_REFERENCE_AUDIT.md). Converter application limits are distinct from IC operating limits: no buck here produces regulated 5 V from a 4.5-V input just because its IC operates at 4.5 V.

## Converter comparison

| Candidate / source | Electrical envelope and frequency | Efficiency/thermal evidence | Student-PCB and layout assessment | Disposition |
| --- | --- | --- | --- | --- |
| **TPS56837 / C1, C1E** | 4.5–28 V IC input; 0.6–13 V output; 8-A device rating; 500/800/1200 kHz; adjustable soft-start/current-limit mode | EVM Table 2-1 reports 94.96% at 24 V → 5 V, 5 A, 25°C; 40 mV ripple at 8 A. No V1A efficiency/thermal result | 10-pin 3 × 3 mm HotRod QFN needs controlled reflow and low-inductance layout. No external compensation network, but LC/effective capacitance and feedforward rules still apply. Four-layer 2/1/1/2 oz reference provides strong documentation | **Leading recommendation** for the candidate 9–24 V envelope. Extra IC current capability helps screening margin; does not rate the board at 8 A |
| **TPS56637 / C2, C2E** | 4.5–28 V; 0.6–13 V; 6-A rating; fixed 500 kHz; selectable Eco/FCCM; fixed 2-ms startup | EVM Table 2-1 reports 92% maximum at 24 V → 5 V, 3 A, 25°C and 30 mV ripple at 6 A. Different operating points prevent a direct efficiency ranking | Same 3 × 3 mm package and strong schematic/BOM/layout guide; fewer mode choices. Fixed startup and current margin need review at a 6-A peak | Credible simpler alternative; not automatically interchangeable despite pin compatibility |
| **LM61460 / C3, C3E** | 3–36 V IC input; adjustable approximately 5 V; 6-A rating; 200 kHz–2.2 MHz; consider 400 kHz | Datasheet §9.2.3 gives load/efficiency/thermal curves; no matched-point value digitized here. 5-V/6-A 400-kHz EVM exists | 14-pin 4 × 3.5 mm HotRod/wettable-flank package; split input paths and local bypass placement are important. EVM guide is for **LM61460-Q1**, so qualify the exact catalog/Q1 variant. More configurable EMI features; documented four-layer layout | Leading alternative if the approved upper input requires margin beyond the 28-V class |
| **TPS56528 / C4** | 4.5–18 V; 0.6–7 V; 5-A rating; 650 kHz | Datasheet application curves, no matched V1A result. Higher typical FET resistance than the leading candidates increases conduction-loss concern | 8-pin SO PowerPAD makes leads easier to inspect, but underside pad still needs proper reflow. D-CAP2 LC limits apply | Only if scope narrows to a suitable low-voltage adapter and ≤5 A with no higher peak. Reject for 24-V input |
| **RT6365 / C5** | 4.5–60 V startup, 4 V after soft-start; 5-A asynchronous buck; 100 kHz–2.5 MHz | External catch-diode conduction loss is significant at 24 V → 5 V; numerical screening in calculations. No inherited Sailor Hat thermal rating | SOP-8 exposed-pad option is more accessible, WDFN option also exists. External compensation, catch diode and thermal layout add work. Manufacturer typical circuit available, fewer reviewed EVM artifacts than TI leads | Wide-input/package alternative, not preferred for the present 25-W-class efficiency target |
| **LM64440APPQRYFRQ1 / C6, A2** | Actual 1026 component: 3–36 V IC input, **4 A**, fixed 2.1 MHz for this example | Manufacturer family includes 6-A variants; that does not change this ordering code. 1026's 4-A/20-W use is not V1A evidence | 22-pin 4 × 3.5 mm package, dense high-frequency layout; source BOM footprint nickname differs from IC value | Reject this 4-A variant for a 5-A continuous proposal. Useful manufacturer layout/reference comparison only |

**Availability observation (2026-09-11):** official TI product pages list TPS56837, TPS56637, TPS56528, LM61460 and LM64440-Q1 as active; Richtek maintains RT6365 product/distributor listings. Exact orderable stock, local supplier authenticity, lead time and total landed BOM cost remain **OPEN**. EVM order widgets expose inconsistent/login-dependent inventory, so no stock quantity is asserted. Before R2 select the complete order code and at least one feasible authorized supply route; approve alternates against their own datasheets. [TI TPS56837](https://www.ti.com/product/TPS56837), [TPS56637](https://www.ti.com/product/TPS56637), [TPS56528](https://www.ti.com/product/TPS56528), [LM61460](https://www.ti.com/product/LM61460), [LM64440-Q1](https://www.ti.com/product/LM64440-Q1), [Richtek RT6365](https://www.richtek.com/Products/Switching%20Regulators/DC_DC%20StepDown%20Convertor/RT6365.aspx).

## Leading buck implementation questions

For TPS56837, start review at 500 kHz and the manufacturer's 5-V reference: 3.3 µH `744325330`, two populated 22-µF `GRM32ER71E226KE15L` output capacitors, local input ceramics and 150-pF feedforward capacitor. These are **reference components**, not a V1A BOM. C7/C8/C9 in its EVM BOM have quantity zero. Nominal 44 µF is not guaranteed effective capacitance.

The EVM BOM calls its inductor 12 A, while the converter datasheet describes 9.7-A rated/15-A saturation values for the same reference part. This is an unresolved source inconsistency for part selection: use the inductor manufacturer's exact current/temperature/saturation definitions and curves, not a copied EVM label. [Würth 744325330](https://www.we-online.com/components/products/datasheet/744325330.pdf) is identified for that component-level review; its ratings are not frozen here.

At 24 V → 5 V, 3.3 µH/500 kHz, nominal ripple is approximately 2.40 A peak-to-peak; a 5-A load needs approximately 6.20-A inductor peak before tolerances. Review minimum inductance at DC bias, minimum switching frequency, hot DCR, saturation during current-limit operation and input-capacitor ripple current. A 5-A output target never means a 5-A inductor saturation rating suffices.

TPS56837 uses skip mode at light loads. If the approved ripple/acoustic constraints require forced PWM, review TPS56838 or TPS56637 FCCM separately. Its output discharge and prebiased behavior need external-output-power analysis before any future backup interface. Adjustable soft-start is useful for load capacitance, but it is not a V1B charging design.

## Monitoring and shunt

**INA228 leads:** 10-pin VSSOP, 2.7–5.5 V supply, 0–85 V VBUS, ±40.96/±163.84 mV differential ranges, integrated power/energy/charge computation. Read M1 §§6, 7.3, 7.6, 8 and 10; M2 schematic Fig. 6-1 and layout/BOM. High resolution does not eliminate shunt tolerance, offset, noise, temperature error or calibration.

**INA226 fallback:** valid for approximately 5-V high-side monitoring; simpler register set and established integration options. It lacks a hardware energy accumulator, so timestamped software integration and data-gap reporting are necessary. No host OS/kernel is a V1A requirement; verify the actual test adapter/host software path without binding a different chip identity just to obtain a driver.

Compare **1, 2 and 5 mΩ**, rather than freezing the prior 2-mΩ proposal. WSL2726 is a source-backed four-terminal family: ±1%, 3 W at its specified conditions; component TCR is ±75 ppm/°C at 1 mΩ and ±25 ppm/°C at 2–5 mΩ. `WSL27262L000FEA` remains a reasonable 2-mΩ candidate. Exact pad geometry, height, supply and accuracy requirement must close before selection. [Calculations](04_POWER_CALCULATIONS.md#shunt-range-and-loss) show the tradeoff.

Place VBUS on the load side of the shunt and keep the telemetry supply branch upstream of it. Route dedicated Kelvin traces, with matched input resistors and a differential capacitor near the IC only after reviewing M1 filter guidance. Candidate 10 Ω per input and 100 nF differential are review values, not populated design. Do not enable temperature compensation from die temperature without characterizing shunt temperature and signed TCR. Energy needs continuous conversions; configuration reset, overflow, unlogged tail and counter extension require explicit handling.

## Protection options

| Function/candidate | Supported capability | Limitation and disposition |
| --- | --- | --- |
| TPS26630/31 plus specified external reverse-protection NFET/pulldown circuitry (P1) | 4.5–60 V eFuse family; input UV/OV cutoff, current limit and slew control; external devices provide required reverse protection | Leading functional input path; review Fig. 8-7, not the simplified arrangement omitting reverse protection. 31 mΩ typical and ±7% current-limit accuracy do not set the final limit. Select cutoff variant and external SOA/rating |
| Fuse plus suitably protected MOSFET/ideal-diode controller | Potentially fewer parts/lower loss for a tightly bounded adapter source | Alternative only after source fault/inrush/reverse-feed behavior is specified. A fuse is not a precise output current limiter |
| LM74800-Q1 with back-to-back NFETs (P2) | Reverse-current blocking and load disconnect, wide input range | Leading topology for output reverse-feed/disconnect review, **not an approved precision OVP solution**. OV threshold tolerance/deglitch may not fit the final 5-V load window; no adjustable overcurrent limiter |
| Independent precision OV detector plus suitably rated disconnect | Can separate tight rail-voltage detection from high-voltage fault interruption | Exact detector/FET/holdoff circuit OPEN; may be needed if integrated-controller thresholds cannot close. No part selected merely to fill a BOM |
| LM74500-Q1 (P3) | Reverse-polarity protection | Does not alone provide reverse-current blocking. Do not use that label for this device |
| TPS25982 (P4) | Low-loss eFuse for its specified voltage range | Earlier screening rejected it for a 28-V buck-failure envelope because operating range ends at 24 V. Re-evaluate only against the actual approved fault envelope; never infer fault survival from normal 5-V operation |

The protected 5-V path and local LDO must survive the specified fault let-through. Capacitors before output disconnect can see raw fault voltage; their normal 5-V rating alone is insufficient. A TVS marking is not its clamping voltage, a MOSFET drain-current headline is not its SOA, and reverse-input protection is not automatically reverse-current blocking.

## Review closure

Approve input/source envelope; setpoint/load-terminal voltage window; continuous/peak/current-step envelope; ambient/airflow/board area; converter mode and complete ordering code; inductor/capacitor ratings; independent output protection; shunt/accuracy/calibration; connector and I2C power-domain behavior. Then authorize R2. No component choice here creates schematic-entry approval.
