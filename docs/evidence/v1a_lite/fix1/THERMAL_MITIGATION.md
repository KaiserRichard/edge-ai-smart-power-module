# FIX1 thermal failure and proposed bench ceiling

2026-10-05 — **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

**CALCULATED / ASSUMED:** the saved four-layer board, 35/15.2/15.2/35 µm copper, retains the two IRFR6215 devices. The coupled model assumes 18 V at the module, 90% buck efficiency, 0.58 Ω per FET, and 2.417 W in U201 at 5 A output. It gives 1.764 A input and **1.804 W per FET**. This includes the FET voltage drop; the simpler 18 V-at-buck calculation gives 1.417 W per FET. These are different boundary conditions.

At **50°C assumed ambient**, the calculated junction rises and temperatures are:

| Assumed cooling, W/m²K | Q101 rise / junction | Q102 rise / junction | U201 rise / junction |
| ---: | ---: | ---: | ---: |
| 5 | 195.8 K / 245.8°C | 195.7 K / 245.7°C | 220.0 K / 270.0°C |
| 10 | **131.0 K / 181.0°C** | **131.6 K / 181.6°C** | **156.8 K / 206.8°C** |
| 15 | 108.5 K / 158.5°C | 109.5 K / 159.5°C | 135.5 K / 185.5°C |

**FAIL** against the historical assumed 110°C junction screen in every case. Above 150°C the fixed FET resistance is outside its stated temperature envelope; the numbers signal a failed screen, not credible equilibrium predictions. The coarse board/package model, airflow, enclosure, ambient, other component heat and efficiency require qualification. Manufacturer conditions remain in the [source register](../../../../third_party/v1a_lite_pcb_fix1/SOURCES.md).

**DECISION:** propose a reduced initial dummy-load test ceiling rather than a schematic change. Start no-load, then low load; consider **1 A and at most 2 A continuous for the first thermal characterization**, only after engineering approval and earlier bring-up gates. This is a bench proposal, **not an approved product rating or permission to fabricate**.

**CALCULATION:** using the same coupled board response, 50°C ambient and the weakest modeled cooling (5 W/m²K), a proposed **U201 loss allocation ≤0.75 W** gives:

| Output | FET loss each | Q101 | Q102 | U201 | Conditional 110°C screen |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 A | 0.0591 W | 70.1°C | 70.3°C | 97.7°C | PASS |
| 2 A | 0.2471 W | 85.3°C | 85.5°C | 105.4°C | PASS, only 4.6 K U201 margin |
| 3 A | 0.5832 W | 112.6°C | 112.6°C | 119.2°C | FAIL |

The 0.75 W value is an **acceptance allocation to establish**, not a prediction that U201 meets it. At 2 A the model's all-device ceiling is 0.825 W in U201; the 4.6 K remaining margin can readily be consumed by model error, other component heat or measurement uncertainty. Do not infer low-load loss by scaling 2.417 W with current squared: switching/control losses do not scale that way. Measure/bound converter loss and calibrate the temperature model at low loads first. Reduce the ceiling further if efficiency, gate drive, temperatures or uncertainty fail their reviewed limits. A measured total buck loss ≤0.75 W would conservatively bound U201 loss, but may be stricter than necessary because it includes inductor and other losses.

**What would make the thermal case pass:** establish actual loss and cooling bounds that keep every inferred junction plus uncertainty below the engineering-approved limit. The reduced-load scenario above is one concrete candidate. For 5 A, both FET dissipation and buck thermal paths need improvement: even setting FET heat to zero leaves U201 at **170.4°C** for 10 W/m²K with the inherited 2.417 W loss. Lower-RDS(on) FETs alone therefore cannot pass that screen. At the present 5 A FET losses, the FETs alone exceed the assumed 110°C limit in all three cooling cases, even before U201 heat. More/thicker appropriately connected copper or an engineered heat path/airflow must be recalculated and measured; no arbitrary extra copper area is claimed sufficient. No replacement part or price is selected because this disposition uses the explicitly permitted reduced-current option and preserves the schematic.

**BENCH-MEASUREMENT ITEM:** document ambient/enclosure/airflow; measure efficiency, voltage drops, FET gate drive and stabilized device temperatures at 18 V and 26 V with dummy loads. Use a reviewed junction-estimation method with uncertainty. Stop for unexpected temperature rise or before approved limits. Hot turn-off SOA and crowbar faults remain separate gates. Follow [QUALIFICATION_PLAN.md](QUALIFICATION_PLAN.md); no Pi until all prior gates pass.

Reproduce the sensitivity from the existing thermal response matrices with `scripts/handback_lite_fix1.py`; machine-readable results: [THERMAL_MITIGATION.json](THERMAL_MITIGATION.json). No CAD mutation occurs.
