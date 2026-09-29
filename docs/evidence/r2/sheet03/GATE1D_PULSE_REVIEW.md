# Gate 1d pulse selection — 2026-09-29

**STATUS: CONDITIONAL PASS for preliminary schematic review only. R2/R3 BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Scope and new correction

The user accepted Candidate C + crowbar and Gate 1c's preliminary envelope. Its source, inductance, capacitance, timing and parasitic assumptions remain OPEN qualification items; absence of a production-tested complete circuit is not a new preliminary gate. No bench result is claimed.

**OBSERVATION / newly demonstrated contradiction:** the old source-side 33 mΩ ballast at 119.96 A lifts the source 3.9587 V. A ground-referenced 5 V driver then supplies at most 1.0413 V VGS, incompatible with the modeled 11.8 mΩ at VGS=4.5 V. This connection cannot be captured unchanged.

**DECISION:** move ballast to the drain side. Connect `VOUT_PROTECTED -> (R+R)||(R+R) -> CSD18540Q5B drain`; source and driver return connect to detector ground by separate Kelvin/short power returns. Use four `WFMB2512R0330FEA` resistors, each 33 mΩ, yielding 33 mΩ total. Select `UCC27511DBVR` on an independent nominal 7.5 V rail, OUTH through 1 Ω, OUTL direct to gate, 10 kΩ gate-source, 1 µF + 100 nF local decoupling. This is a permitted implementation correction, not a different protection architecture.

## Part and driver alternatives

| Evaluated change | Result |
| --- | --- |
| Keep source ballast, change only resistance | 0 Ω exceeds the old MOSFET pulse headline; 50 mΩ also loses the fault window and gate drive. Not selected. |
| Drain ballast, CSD17308Q3, 5 V driver | Static drive restored, but zero-RDS current corner approaches 162 A against 167 A; hot 2×RDS screen leaves only about 6.75 mV at 0.3 µs. Superseded by larger MOSFET. |
| Drain ballast, CSD17577Q5A | 280 A pulse rating, 17 nC maximum Qg test value; positive windows. Viable comparison, less SOA/voltage/thermal margin than selected 60 V part. |
| Drain ballast, CSD18540Q5B | 400 A pulse rating; 3.3 mΩ maximum at 4.5 V/28 A/25°C; 26 nC maximum Qg under its test conditions. Selected with hot resistance sensitivity up to 6.6 mΩ. |
| UCC27511 at 5 V or 7.5 V | Grounded source fixes the original mismatch; 7.5 V improves gate-charge headroom and can be derived from 9 V minimum input. Selected; detector logic remains 5 V. |
| LMG1020 at 5 V | Fast 100 pF timing but typical peak-source current; tiny WCSP and rail constraints add no needed benefit. Not selected. |
| UCC27614 at 5/7.5/12 V | Stronger driver; timing test uses 12 V/1.8 nF. A 12 V independent rail would need conversion at 9 V input. Not selected. |

**CALCULATION:** conservative charge screen uses 7.35 V minimum rail (ASSUMED −2%), 11 Ω driver pull-up screen, 1 Ω external and 1.6 Ω FET internal maximum test resistance. To 4.5 V, `Ig >= (7.35−4.5)/13.6 = 0.2096 A` under the resistive approximation; `26 nC/Ig = 124.1 ns`. Adding 55 ns comparator + 6.1 ns latch + 26 ns driver gives 211.2 ns. Use **0.30 µs** effective-on instead of silently retaining 0.20 µs. There is 88.8 ns screening allowance for additional effects. The resistance/charge transfer across test conditions is ASSUMED, not a guaranteed application delay. Logic/filter, nonlinear gate charge, rail validity and physical commutation remain OPEN for R2 qualification.

## MOSFET SOA and full-pulse envelope

**DATASHEET:** TI CSD18540Q5B, SLPS488B (April 2017), p1 pulse limit 400 A for ≤100 µs, ≤1% duty; p3 maximum RθJC=0.8°C/W; p4 Fig1; p6 Fig10. Both figures were visually reviewed. No manufacturer I²t rating is inferred from 400 A × 100 µs.

**ASSUMED envelope retained/extended explicitly for review:** detector-to-series-off 2 µs; protected-node ceiling 5.5 V; initial device and resistor-terminal temperature 125°C; isolated downstream capacitance ≤220 µF from the existing 2–220 µF sensitivity; no simultaneously powered external load. These are conditional design screens, not invented measured electrical requirements. Actual downstream C and thermal environment remain OPEN. Raw bulk is upstream after series-off and is already included during the initial fault interval.

With resistor tolerance ±1% plus 50 ppm/K ×100 K, total ballast is 32.505–33.495 mΩ. The worst load line is `ID=(5.5−VDS)/0.032505`; hence **ID ≤169.20 A** (230.80 A below pulse headline), and `P_FET <= 5.5²/(4Rmin) = 232.66 W` including the turn-on linear region. This voltage ceiling is supplied by the separately calculated accepted fault screen, not proved by the load line itself.

Fig10's 100 µs branch is approximately 400 A across VDS=2–5.5 V. Applying the thermal headroom ratio `(175−125)/(175−25)=1/3` gives a conservative 133 A comparison there; the load line at VDS≥2 V is ≤107.68 A (25.65 A margin). Below 2 V, distinguish the ohmic/RDS boundary from a thermal limit: use the power envelope, pulse-current ceiling, and on-resistance screen rather than incorrectly scaling the sloping RDS boundary as a constant-power limit. Fig1's single-pulse normalized impedance at 100 µs is below the deliberately rounded-up **0.05** reading: `ΔT <=232.66×0.05×0.8 =9.31°C`, **Tj ≤134.31°C**, leaving **40.69°C** to 175°C. This is a preliminary datasheet-based SOA/thermal comparison, not merely a pulsed-ID headline check. Layout must realize the cited thermal assumptions; no avalanche energy credit is taken.

## Resistor pulse and tail

**DATASHEET:** Vishay WFM document 30387, Rev 04-Aug-2022, pp1–2 specify order code, tolerance and component TCR; p3 unnumbered Single Pulse chart applies specifically to 33 mΩ. At 100 µs the 2512 curve exceeds 1000 W (approximately 2000 W visually); use only **1000 W / 0.100 J per element**. No extrapolation below the plotted 100 µs minimum is used.

All 16 independent tolerance/TCR combinations of the four-resistor bank are evaluated. At a constant 5.5 V across the bank, no element exceeds **232.66 W**. Conservatively apply the p3 70–170°C derating line to pulse capability at 125°C: factor 0.45, giving **450 W / 0.045 J per element**. A 100 µs rectangle consumes at most **0.02327 J per element**: **1.934× power and energy margin**. Applying the continuous derating line to pulses is an explicit conservative engineering assumption requiring later confirmation, not a quoted pulse-temperature guarantee. Four parts avoid the inadequate hot margin of a single resistor.

This rectangle covers the whole initial interval plus the discharge tail, not just the old 1.8 µs integration. Worst RC time constant with 220 µF and RDS=6.6 mΩ is **8.821 µs**. After 98 µs of isolated discharge, current is below **2.532 mA** and residual stored energy below **7.45e−13 J**. Subsequent dissipation is below continuous ratings and decays monotonically. The larger actual load capacitance case, external power, repeat faults without cooling, and loop inductance invalidate this tail assumption and remain explicit OPEN review items.

## Recalculated windows and disposition

The calculator `--gate 1d --write` retains historical Gate1b/1c JSON members and writes a separate Gate1d record. It sweeps ballast tolerance/TCR, RDS=0/3.3/6.6 mΩ and on-delay 0.2/0.3/0.4/0.5 µs. Zero RDS is a current-upper sensitivity, not a specified minimum.

| Selected implementation screen | CALCULATED result |
| --- | --- |
| Fault peak, selected 0.30 µs on / 2 µs off | **5.481612 V; +18.388 mV** to 5.5 V |
| Original 0.20 µs comparison | 5.460672 V; +39.328 mV |
| Peak current / I²t across selected corners | 161.693 A / 0.042635 A²s; model values, not ratings |
| Normal detector false-trip margin | +21.954 mV with proposed raw bulk bank |
| Pi static at 5 A with reduced-resistance harness | **4.761431 V; +11.431 mV** to assumed 4.75 V floor |
| Separate 100 mV dynamic reserve | Still unmet; −88.569 mV |
| 0.40 µs timing sensitivity | 5.502639 V; −2.639 mV; explicit OPEN narrow-timing risk |

**DECISION:** close pulse part selection for preliminary capture within these assumptions. Keep the revised **18.39 mV** fault margin (and historical 39.33 mV comparison) and **11.43 mV** harness margin explicitly OPEN. Do not close source/inductance/C, timing, layout/thermal, input TVS/fuse, startup/inrush, reset/supply validity, connector/harness or bench qualification. Proceed to Gate2; R2 release and R3 remain BLOCKED.
