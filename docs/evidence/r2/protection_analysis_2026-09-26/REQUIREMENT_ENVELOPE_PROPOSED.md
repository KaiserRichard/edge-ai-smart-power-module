# V1A requirement envelope: proposed revision 2

2026-09-26. **PROPOSED, not approved.** Revision 1 was returned by the user on 2026-09-26 with the comments that
rows S1, P2, P4 and P5 answer below. Nothing here changes `docs/00_REQUIREMENTS.md` until the user approves.
Analysis and sources: [PROTECTION_ANALYSIS.md](PROTECTION_ANALYSIS.md).

## A. Source envelope (S1 revised)

The analysis source is the **Mean Well GST60A24-P1J, ASSUMED**. It is not a confirmed adapter. The design is
checked against the envelope below, not against a product.

| ID | Parameter | Analysis value | Label | Depends on the final adapter? |
| --- | --- | --- | --- | --- |
| S1a | Steady maximum at J501 | 24.72 V (24 V + 3 %) | ASSUMED from GST60A spec | **Yes.** It sets the TVS standoff and the high-side-short source voltage |
| S1b | Steady minimum | 9.0 V | existing P01 | Yes, if a 12 V or 19 V adapter is chosen |
| S1c | Source's own OVP range | 25.2–32.4 V | ASSUMED from GST60A spec | **Yes.** It sets the TVS VBR floor (§9 of the analysis) |
| S1d | Overload behaviour / available current | hiccup at 105–150 % of 2.5 A | ASSUMED | **Yes.** It sets F101 coordination and whether F101 can ever clear |
| S1e | Output capacitance and cable | 2 m cable, hot-plug only; adapter capacitance UNKNOWN | ASSUMED / UNKNOWN | **Yes.** It sets hot-plug ringing |
| S1f | Surge class | none (bench module) | ASSUMED | No |

Items that change if a different adapter is chosen:
- D101 selection
- F101 selection
- the high-side-short let-through (it scales with the source voltage)
- start-up margin at the minimum input

## B. Load envelope

| ID | Parameter | Proposed value | Label |
| --- | --- | --- | --- |
| L2 | Current | 5 A continuous; 6 A for ≤ 100 ms | ASSUMED |
| L3 | Raw static regulation | 5.04–5.16 V | CALCULATED |
| L5 | Load-step specification | **OPEN**. The analysis uses 5 A → 0 A as a worst case. The Pi's real step and slew are needed | OPEN |
| L6 | Load capacitance | 2–220 µF analysed | ASSUMED; the Pi 5 value is UNKNOWN |

## C. Protection requirements

| ID | Requirement | Proposed value | Label and basis |
| --- | --- | --- | --- |
| P2 | OV trip window | **Candidate only.** LM74800-only: 5.45–5.79 V (CALCULATED). Nuisance immunity is **not shown**, because the load-release estimate with the MLCC bank alone reaches 5.63 V (analysis §4). Recommended option I: 5.40 V ± 1.1 % with ≥ 470 µF bulk | CALCULATED window; overshoot is an ideal-controller estimate, not a bound |
| P3 | Trip to load isolation | **≤ 2 µs** with bulk | CALCULATED from delay sensitivity (analysis §3) |
| P4 | Load fault voltage versus time | **UNKNOWN / OPEN.** 6.0 V peak is an **ASSUMED screening criterion only**. It is not a Raspberry Pi damage rating and not a demonstrated safe ceiling | The Pi publishes no rating; closing this needs a Raspberry Pi statement or a component-level analysis of the Pi 5 input |
| P5 | Recovery policy | **OPEN.** Analysis §5 shows the LM74800-only behaviour is part-dependent (release 4.97–5.30 V straddles the 5.04–5.16 V rail). Candidate policy: latch off until input power is cycled, with two independent holds during a persistent fault, and no automatic retry | Proposal; needs the approved architecture and a bench check |
| P5b | Detector latch and hysteresis | Latching, hysteresis ≥ 50 mV, valid before the path enables | Proposal |
| P6 | Telemetry during a trip | INA228 domain may lose power | INFERRED |
| P7 | Reverse feed, input off | ≤ 100 µA into `VOUT_5V1` with the load held at ≤ 5.25 V | Proposal; verify at R5 |
| P8 | Path drop at 5 A | ≤ 35 mV, **conditional** on the assumptions in analysis §8 | CALCULATED, conditional |
| P9 | Start-up | Path enabled from BUCK_PGOOD; input current stays ≤ 90 % of the eFuse minimum limit at 9 V | Proposal (analysis §5) |

## D. Environment and board (unchanged from revision 1, still PROPOSED)

- Ambient 0–40 °C, natural convection, open bench (ASSUMED).
- Tj ≤ 125 °C and ≥ 20 °C under each part's rating.
- 4 layers, 2/1/1/2 oz.
- Board target ≤ 65 × 55 mm (ASSUMED). Option I adds board area, so the R3 floorplan re-checks this.

## Facts only the user can supply

These change the decision, in priority order:
1. The real adapter, or at least its maximum steady voltage and OVP range (S1a, S1c).
2. How the Pi is powered (GPIO header pins or USB-C), and whether a Pi 5 input fault envelope from Raspberry Pi exists (P4).
3. The largest realistic load step, meaning which USB peripherals hot-plug (L5).
