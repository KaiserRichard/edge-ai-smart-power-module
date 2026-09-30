# Task 1a — published L/I curves and their limits

Analysis complete; component qualification remains OPEN. No native CAD inspection or substitution was performed. Numeric results are CALCULATED within ASSUMED graph/application transfers, not guaranteed fault maxima.

| Real MPN / primary source | Manufacturer evidence and ASSUMED curve readings at 0 / 5 / 20 / 40 / 60 A, µH | CALCULATED normal copper screen | Fit and qualification consequence |
| --- | --- | --- | --- |
| [Würth 7443763540068](https://www.we-online.com/components/products/datasheet/7443763540068.pdf), revision 002.001, 2025-02-20 | Nominal 6.8 µH ±20%; typical graph 6.8 / 6.8 / 6.8 / 6.8 / 6.75–6.8; trace extends approximately 83 A. MnZn ferrite, with knee above about 65 A. | Published DCR maximum 1.2 mΩ at 20°C: CALCULATED 30.218 mW at 5 A / 24 V ripple; ASSUMED copper coefficient 0.00393/K gives 42.094 mW at 120°C | ASSUMED package screen 41×36×35 mm maximum, versus inherited 8 mm class. Not footprint compatible. A graph showing 60 A does not establish an all-lot/hot Ldiff floor at 60 A or beyond the knee. |
| [Würth 74437636350652](https://www.we-online.com/components/products/datasheet/74437636350652.pdf), revision 001.000, 2025-02-07 | Nominal 6.5 µH ±20%; typical graph 6.5 / 6.5 / 6.4 / 6.2 / 5.8; approximately 5.3 / 4.7 / 4.1 at 80 / 100 / 120 A. Metal alloy. | Published 0.38 mΩ ±10% gives CALCULATED maximum 0.418 mΩ at 20°C; 10.533 mW at 5 A / 24 V ripple, 14.673 mW with ASSUMED 120°C copper correction | ASSUMED body screen 36.0±0.5×35.7 max×34.2 max mm. Large THT; different pin arrangement. Soft decrease, but the fault differential-L guarantee remains OPEN. |
| [Würth 74437636351002](https://www.we-online.com/components/products/datasheet/74437636351002.pdf), revision 001.000, 2025-02-07 | Nominal 10 µH ±20%; typical graph 10 / 10 / 9.8 / 9.25 / 8.4; approximately 7.5 / 6.6 at 80 / 100 A, where trace ends. Metal alloy. | Published 0.62 mΩ ±10% gives CALCULATED maximum 0.682 mΩ at 20°C; 17.107 mW at 5 A / 24 V ripple, 23.830 mW with ASSUMED 120°C copper correction | Same large body class; lead/hole spacing differs from the 6.5 µH part. Best candidate for obtaining a proposed Ldiff≥5 µH through 100 A acceptance envelope, not already a guaranteed envelope. |

Graph-reading uncertainty is ASSUMED approximately ±0.1 µH; it excludes lot, temperature, excitation, tolerance and fault-pulse differences. Initial inductance is measured at published 100 kHz / 10 mA for the ferrite part and 100 kHz / 100 mV for the alloy parts. General sheet conditions are 20°C / 33% RH; separate graph sweep conditions are not fully specified. The [manufacturer catalog](https://www.we-online.com/en/components/products/WE-HCFT) identifies core types. Its thermal reference copper differs greatly from a small module PCB; no PCB temperature guarantee is inferred.

A bias-dependent small-AC measurement is an incremental-inductance indication. Fault integration needs `vL=Ldiff(i) di/dt`, with winding resistance removed from measured terminal voltage. Do not differentiate a bias curve as if its plotted L were necessarily flux/current secant inductance. Multiplying each typical reading by 0.8 is ASSUMED sensitivity only: the initial ±20% tolerance is not a guaranteed bias/temperature curve envelope.

## Normal 5 A behavior

CALCULATED using inherited nominal Vout=5.098361 V, ASSUMED nominal switching frequency 400 kHz, each nominal L, and ideal buck ripple `ΔI=Vout(1−Vout/Vin)/(L f)`:

| MPN | Ripple at 9 V / 24 V, A peak-to-peak | CALCULATED tolerance sensitivity at 28.289211 V, L−20%, f=360 kHz | Normal-operation consequence |
| --- | --- | --- | --- |
| 7443763540068 | 0.812580 / 1.476216 | See reproducible JSON | Lower copper loss than inherited XAL8080; core/AC losses and complete efficiency OPEN |
| 74437636350652 | 0.850084 / 1.544349 | See reproducible JSON | Similar ripple; full hot curve/normal transient qualification OPEN |
| 74437636351002 | 0.552555 / 1.003827 | See reproducible JSON | Lower ripple, but below LM61460 nominal 0.6 A current-mode ripple guideline at 9 V; stability/frequency/load-release qualification required |

Inherited XAL8080 maximum DCR is 14.5 mΩ at its stated conditions. CALCULATED 5 A DC copper loss alone is 0.3625 W. Savings above are copper-loss screens; they do not establish total efficiency. Core loss, high-frequency winding loss, leakage/ringing and revised loop dynamics remain OPEN. [LM61460 SNVSBD5D, July 2022, §9.2.2.3](https://www.ti.com/lit/ds/symlink/lm61460.pdf) supports the ripple guideline; larger L is not a drop-in change.

## Full-time current, charge and energy model

Actual fault-onset→effective isolation minimum/maximum: **OPEN/OPEN**. An inductance by itself cannot establish a finite fault duration or total energy from a maintained source. The following is an explicitly ASSUMED maintained-source sensitivity, with I0=8 A, output=0 for maximum excitation, no DCR/damping credit, and piecewise interpolation of the typical graph. These are not predictions of the board.

`(Vin−Vout) t = integral[Lproxy(i) di]`

`Q(t)=integral[i Lproxy(i) di]/(Vin−Vout)`

`ΔWL=integral[i Lproxy(i) di]`. For constant L, this becomes `0.5 L (I²−I0²)`.

At the CALCULATED inherited conditional OVP corner 28.289211 V:

| MPN | CALCULATED I / Q at 2 µs | At 5 µs | At 10 µs | At 20 µs |
| --- | --- | --- | --- | --- |
| 7443763540068 | 16.320 A / 24.320 µC | 28.801 A / 92.002 µC | 49.610 A / 288.015 µC | OPEN: exits the tabulated 60 A proxy domain; higher graph endpoint is not extrapolated |
| 74437636350652 | 16.771 A / 24.758 µC | 30.106 A / 95.006 µC | 53.118 A / 302.490 µC | 106.853 A / 1089.880 µC |
| 74437636351002 | 13.702 A / 21.695 µC | 22.343 A / 75.733 µC | 37.183 A / 224.283 µC | 69.808 A / 754.867 µC |

All cells are CALCULATED under the ASSUMED proxy model. Full 24 V, 27.63 V and 28.289211 V screens, source work `Vin×Q`, initial L energy and normal-corner results are in [the calculation record](SOURCE_BOUND_CALCULATIONS.json). Output at zero is a bounding excitation premise, not an actual protected rail. At a positive output, some work goes to the output rather than L; total work delivered by the stiff source remains `Vin Q`.

**Conclusion:** no inspected 8 mm candidate has a published trace through 60 A. [XAL8080](https://www.coilcraft.com/getmedia/345e50d6-a804-4ecb-9a92-5185221faf3e/xal8080.pdf) and [XAL1510](https://www.coilcraft.com/getmedia/cd1cef27-13f0-4568-8894-f7311475209b/xal1510.pdf) 6.8 µH traces end near 30 A and 45 A. [IHLP8787 6.8 µH](https://www.vishay.com/docs/34353/ihlp8787mz51.pdf) axis reaches 60 A but actual trace ends near 57 A. These exclusions do not prove no other part exists; they establish why these inspected parts cannot fill the missing evidence.

Recommend the 10 µH alloy part for source-contract qualification study, combined with timed input-source isolation and controlled local C (Task 1b). Manufacturer-published curves improve the model; only an applicable minimum Ldiff envelope over lot/temperature/current, plus physical source-off and capacitor bounds, can close it. Owner accepts the large footprint or keeps the gate BLOCKED; no schematic selection is made here.
