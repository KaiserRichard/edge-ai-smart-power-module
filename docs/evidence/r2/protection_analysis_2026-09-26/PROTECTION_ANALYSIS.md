# Sheet 03 output protection: architecture analysis and recommendation

2026-09-26. Branch `feat/r2-sheet03-output-protection`, base `feat/r2-schematic-recovery` @ `de1d35c`.
**Sheet 03 is electrically unchanged. No architecture is approved by this document. R2 and R3 remain BLOCKED.
NOT FOR FABRICATION.**

This analysis replaces the withdrawn "Codex brief 01" (LM74800-only capture). The user returned that brief
on 2026-09-26 with review comments. This document answers them and ends with a recommendation for the user
to approve or reject. The companion files are:
- [proposed requirement envelope](REQUIREMENT_ENVELOPE_PROPOSED.md)
- [model results](protection_model_results.json), reproduced with `python3 -B scripts/analyze_output_protection.py --write`
- [Codex brief 02](CODEX_BRIEF_02_PROTECTION_ANALYSIS.md)

Evidence labels: KNOWN (datasheet row), CALCULATED (reproducible here), INFERRED, ASSUMED, AMBIGUOUS
(source read but not unambiguous), UNKNOWN / OPEN.

## 1. Findings in one paragraph

**The finding blocks the LM74800-only architecture.** In a hard short of the LM61460 high-side switch
at 24.72 V input, every modelled corner puts **6.10 V to 8.38 V** on the load. The detector is too slow:
about 6 µs from threshold crossing to disconnect. The detector window is also too wide: 5.45–5.79 V.
Adding bulk capacitance alone does not fix it (worst case 6.34 V with 1000 µF). Two things are needed together:
- raw-side bulk capacitance, which slows the rise and gives nuisance-trip margin;
- a precise, sub-2 µs detector acting on the path.

With both, every modelled corner stays at or below **5.49 V**. That is a model result, not a qualified bound.
Section 6 lists what the model leaves out.

## 2. The fault model and what it covers

`scripts/analyze_output_protection.py` is a lumped Euler model with 2 ns steps. The circuit chain is:
- source (24.72 V ASSUMED maximum)
- TPS26630 eFuse: current source limited to I(OL) × 1.07 = 4.79 A, RON 34.5 mΩ
- C_in,eff
- shorted high-side switch (0 or 41 mΩ)
- L201: 6.8 µH, DCR 0 or 14.6 mΩ, ASSUMED soft saturation to 70 % above 14 A
- raw node: MLCC bank plus optional bulk branch with 20 mΩ ESR
- protection path: 2 × 3.25 mΩ FET + 2 mΩ shunt, with ideal-diode reverse cut-off after 0.875 µs
- load: C_load plus a constant-current load

The protection action (disconnect or crowbar) fires a set delay after the raw node crosses the trip level.

The corner sweep covers:
- C_in,eff 15 / 40 µF
- C_raw,eff 60 / 130 µF (nominal 132 µF; DC-bias minimum OPEN)
- load 0.3 / 5 A
- C_load 2 / 220 µF
- lossless / lossy

That is 32 corners per option.

**Not modelled** (each can move the result either way):
- the LM61460 control loop and low-side switch; a low-side FET that turns on into the short diverts Cin energy to ground, which helps
- capacitor C(V) and ESL
- MOSFET switching and Miller dynamics
- detector propagation versus overdrive
- layout inductance and ringing
- the eFuse current-limit response at the microsecond scale (modelled as instantaneous at 1.07 × I(OL); the fast-trip allows 2 × I(OL) for ~1 µs, SLVSE94G)
- inductor saturation shape (the knee is ASSUMED; the Coilcraft drawing is still not downloaded)
- the Pi's real input network

Because of these omissions, a PSpice run with vendor models is supporting evidence, not qualification.
Bench fault injection at R5 is what qualifies.

## 3. High-side short results (worst of 32 corners)

| Option | Trip (worst high) | Trip→action | Worst load peak | Max time > 6.0 V | Max raw in 120 µs | Crowbar peak |
| --- | --- | --- | --- | --- | --- | --- |
| A: LM74800 OV only | 5.794 V | 5.97 µs | **8.38 V** | 107 µs | 24.4 V | – |
| B1: A + 470 µF bulk | 5.794 V | 5.97 µs | 6.53 V | 102 µs | 8.7 V | – |
| B2: A + 1000 µF bulk | 5.794 V | 5.97 µs | 6.34 V | 59 µs | 7.4 V | – |
| D: precision detector → LM74800 EN | 5.50 V | 6.87 µs | 8.20 V | 107 µs | 24.4 V | – |
| E: D + 470 µF bulk | 5.50 V | 6.87 µs | 6.29 V | 4 µs | 8.7 V | – |
| C: precision crowbar + ideal diode | 5.50 V | 0.30 µs | 5.56 V | 0 | 5.6 V | 350 A |
| F: C without ideal diode | 5.50 V | 0.30 µs | 5.56 V | 0 | 5.6 V | 356 A |
| G: precision detector + fast Q302 gate pull-down | 5.50 V | 0.40 µs | 5.57 V | 0 | 24.4 V | – |
| H: 470 µF bulk + precision crowbar | 5.46 V | 0.30 µs | **5.49 V** | 0 | 5.5 V | 355 A |
| **I: 470 µF bulk + precision fast gate-off** | 5.46 V | 0.40 µs | **5.49 V** | 0 | 8.7 V (→ source) | – |

"Time > 6.0 V" is long for the disconnect options because, at light load, the isolated load capacitance
keeps whatever peak it reached.

**Delay sensitivity** (fast gate-off, worst corner, lossless):

| Trip→off delay | 0.4 µs | 1 µs | 2 µs | 4 µs |
| --- | --- | --- | --- | --- |
| Without bulk (trip 5.50 V) | 5.57 V | 5.71 V | 5.99 V | 6.75 V |
| With 470 µF bulk (trip 5.46 V) | 5.49 V | 5.55 V | 5.66 V | 5.89 V |

So the requirement is **trip-to-isolation ≤ 2 µs with bulk**. The LM74800's own paths (OV deglitch 3.98/5.4 µs,
EN-off 3–6 µs) cannot meet it at any threshold. The OV row in SNOSD95C §7.6 lists 3.98 and 5.4 µs, and I could not
confirm from the text whether 5.4 µs is the typical or the maximum value, so that timing is AMBIGUOUS.

## 4. Nuisance-trip immunity (answers review item P2)

The upper edge of normal operation is the raw rail after a load release. I estimate it with an **ideal-controller
energy transfer**. The inductor's peak current is dumped into C_raw with no further switching:

ΔV = √(V₀² + L·I_pk²/C) − V₀.

The sweep is:
- V₀ = 5.159 V (static high)
- L = 6.8 µH ± 20 %
- I_pk = 5.0 A or 6.14 A (5 A + half the 24 V corner ripple)
- C_raw 60 / 130 µF

| Raw bank | Estimated peak range | Worst |
| --- | --- | --- |
| MLCC only | 5.26–5.63 V | **5.63 V** |
| + 470 µF | 5.18–5.21 V | 5.21 V |
| + 1000 µF | 5.17–5.19 V | 5.19 V |

**Why this is not a bound.** A peak-current-mode loop that is mid-on-time, or slow to fold back, adds charge, so
the overshoot is larger. A finite load slew removes charge, so it is smaller. The load step itself is ASSUMED
(5 A → 0 A); the Pi's real step is OPEN. The LM61460 datasheet gives no load-transient overshoot data.

**Consequence.** With the MLCC bank only, the release peak (up to 5.63 V) overlaps the LM74800 window
(5.45–5.79 V) and any precision threshold that still protects. **Nuisance-trip immunity is therefore not shown
for option A**, and it would be even worse with a tighter detector. With 470 µF of bulk, a 5.40 V ± 1.1 % detector
(5.34–5.46 V) sits about 0.13 V above the estimate. That margin is only meaningful once the LM61460 PSpice
load-step run (Codex brief 02) and later the bench confirm the overshoot.

## 5. Recovery, retries, chatter and start-up (answers review item P5)

LM74800 OV release thresholds referred to the raw rail with the 348k/97.6k divider: **4.97–5.30 V**. The rail
regulates at 5.04–5.16 V. So whether a part reconnects after a trip depends on that part's threshold and on the
rail trajectory; it is not guaranteed either way.

| Situation | Option A (LM74800 only) | Option I (recommended) |
| --- | --- | --- |
| Hard high-side short, persistent | Q302 opens late (load already exposed, §3). The raw rail climbs to the source voltage because the eFuse only limits current and never trips once the bulk is charged. The OV pin stays asserted, so the path stays off while input is present | The detector opens Q302 within 0.4 µs (ASSUMED). The raw rail climbs to the source; both the detector and the LM74800 OV keep Q302 off. Two independent holds, no retry |
| Input removed after a persistent fault | The raw rail decays through 5.3–4.97 V. HGATE may re-enable briefly onto a rail below 5.3 V (harmless if the decay is monotonic; OPEN if the eFuse reverse comparator or bulk causes a bounce) | Same, with the extra requirement that the detector latch releases only below its supply UVLO |
| Transient trip (a real overshoot, then back to regulation) | Part-dependent: a part whose release is above the rail reconnects about 3 µs after release; one whose release is below the rail stays off until input is cycled. **Not deterministic** | The detector must latch (requirement P5b). The LM74800 OV part-dependence remains as a secondary path only |
| Repeated retries | The eFuse is MODE-open (latched overload, INPUT_PROTECTION.md), so no eFuse auto-retry. LM74800 re-enable is the only retry path, described above | None by design (latch) |
| Chatter near threshold | 8 % OV hysteresis (1.13 V vs 1.231 V) far exceeds the 14 mV ripple. A slowly drifting raw rail between release and trip could still cycle on noise; OPEN | The detector needs its own hysteresis ≥ 50 mV plus the latch |
| Start-up | EN pulled from the raw rail: the path follows the buck soft-start (3.5–7 ms, SNVSBD5D); load inrush equals the load C × soft-start slope | Start-up input current at 9 V, 5 A load and 470 µF: **3.83 A** against an eFuse minimum limit of **4.17 A**, only 8 % margin. Recommended: enable the path from BUCK_PGOOD so the load connects after soft-start. The detector supply must be valid before the path enables |
| Crowbar variants (C, F, H) | – | Rejected for chatter: when the raw rail collapses, a raw-powered detector releases, and the eFuse (still on, below its 162 ms breaker timer) re-energises the rail. That gives ~0.6 ms cycling unless a separately powered latch or SCR (silicon-controlled rectifier) holds it, and the SCR di/dt rating is a problem at 350 A peaks |

## 6. Architecture comparison (answers brief review item 4)

| Criterion | A LM74800 only | B bulk only | C/H crowbar | **I bulk + fast gate-off + LM74800** |
| --- | --- | --- | --- | --- |
| Hard-short load peak (model) | 6.1–8.4 V ✗ | 5.7–6.5 V ✗ | ≤ 5.56 V | ≤ 5.49 V |
| Nuisance immunity (model) | not shown | improves | needs bulk (H) | needs bulk (included) |
| Component stress | Q302 blocks ~20 V | bulk sees source V (≥ 35 V part) | 270–355 A pulses, eFuse in current limit ≤ 162 ms at ~24 V × 4.8 A | Q302 and raw side hold the source voltage indefinitely; no high-current pulses |
| Stored energy | small | 470 µF at 24.7 V = 0.14 J after a fault | same as bulk, dumped into the crowbar | 0.14 J on the raw side until input is removed |
| Start-up / inrush | follows soft-start | +0.44–0.88 A charge current | same | same; gate the path on PGOOD |
| Recovery determinism | ✗ part-dependent | ✗ | needs a latch; chatter risk | latch + two independent holds |
| Reference-design coverage | TI common-drain reference | vendor allows a parallel electrolytic (INFERRED from datasheet text) | classic, but no TI reference for this rail | LM74800 is referenced; **the fast gate pull-down is a custom circuit (design risk)** |
| Reverse feed (P7) | ideal diode ✓ | – | ✓ with LM74800 | ✓ |
| Extra parts vs A | 0 | 2–3 | ~8 | ~10 (2 caps, LDO, reference, comparator, 2 BJTs, resistors) |

Other approaches screened and rejected:
- **Load-side TVS.** SMBJ5.0A clamps at 9.2 V at 65 A (Vishay 88392), well above any useful ceiling. No standard TVS clamps below 6 V at tens of amps.
- **Output eFuse with OVP.** The TPS25947 has a 28 V absolute maximum, which the faulted raw rail reaches. A TPS2663-class output eFuse has an 8.5–14 µs OVP delay, far too slow.
- **LTC4368.** 2 µs + 6 µs, same problem as D.
- **Accept the risk.** The hard high-side short is the fault P08 exists for, so accepting it would contradict the requirement. It is listed for completeness, and it is the user's call.

## 7. Recommendation for approval

**Approve option I as the architecture to design and verify, not to capture yet:**
1. **Keep** LM74800 + Q301/Q302 common-drain (ideal diode, reverse-feed block, second slower OV path).
2. **Add** ~470 µF effective bulk on `VOUT_5V1`, rated ≥ 35 V and low ESR. This buys load-release margin and slows the fault.
3. **Add** a precision OV detector on `VOUT_5V1`: window ≤ ± 1.1 %, nominal 5.40 V, trip-to-isolation ≤ 2 µs, latching, powered from `VOUT_5V1` through a ≥ 30 V LDO. It pulls Q302's gate to its source through a discrete stage that never drives HGATE below OUT (the LM74800 HGATE−OUT absolute minimum is −0.3 V).
4. **Enable** the path from BUCK_PGOOD.

Codex brief 02 turns this into candidate parts, SPICE models and the evidence the user needs before capture approval.

**The finding stays blocking until these close:**
- the LM61460 load-step overshoot (PSpice, then bench)
- the high-side-short let-through with vendor models
- LM61460 stability with the chosen bulk
- the detector and gate-stage timing across tolerance
- the Pi fault envelope, which stays OPEN (6.0 V is only a screening criterion)

## 8. Protection-path drop is conditional (answers brief review item 2)

32.5 mV at 5 A = Q301 max(V_AC_REG 13.4 mV max, 5 A × 3.25 mΩ) + Q302 5 A × 3.25 mΩ. It holds only under these conditions:
- **(a)** RDS(on) is the PSMN1R8-40YLC maximum at VGS = 10 V and Tj = 150 °C. That is pessimistic for temperature: the ~0.08 W per FET suggests Tj near ambient, which is INFERRED.
- **(b)** VGS ≥ 10 V is assumed. HGATE−OUT is specified at 10–14.5 V only for VS > 5 V (SNOSD95C). VS ≈ raw − Q301 drop = 5.02–5.15 V, marginally inside that condition. Below 5 V the drive and RDS are UNKNOWN.
- **(c)** Q301's drop is set by the DGATE regulation loop, not by RDS, whenever I × RDS < V_AC_REG.
- **(d)** Copper, vias and solder are excluded (5 mΩ allocated separately in PI_POWER_DELIVERY_REFINED.md).
- **(e)** The number applies to the PSMN1R8-40YLC only. A different FET changes it.

## 9. Input TVS: do not substitute yet (answers brief review item 1)

| Check | SMBJ24CA | SMBJ26CA (captured) | SMBJ30CA |
| --- | --- | --- | --- |
| VWM vs 24.72 V assumed steady max | 24 V ✗ (operates above standoff; leakage unspecified between 1 µA at VWM and 1 mA at VBR) | 26 V ✓ | 30 V ✓ |
| VBR min, 25 °C / 0 °C (−0.096 %/°C) | 26.7 / 26.1 V | 28.9 / 28.2 V | 33.3 / 32.5 V |
| Conducts on adapter OVP (25.2–32.4 V, ASSUMED GST60A24) | yes, becomes a sustained clamp | yes, above 28.2 V | no (≥ 32.5 V) |
| VC at IPPM, 25 °C → ~100 °C screen (+0.096 %/°C, INFERRED scaling) | 38.9 → 41.7 V | 42.1 → 45.2 V | 48.4 → 51.9 V |
| Protected node | Q101 (100 V class) and TPS26630 IN (67 V absolute) | same | same |

**Key correction to the earlier review.** D101 sits on `VIN_FUSED`, ahead of the eFuse. U201 (42 V absolute)
never sees the TVS clamp directly, because the eFuse is in between. During a surge the eFuse limits current
into C_in (fast-trip 2 × I(OL) for ~1 µs, then I(OL); SLVSE94G) and opens within 8.5–14 µs of crossing its
OV threshold (27.0–28.3 V).

Bounding charge into C_in,eff = 15 µF: 9.6 A × 1 µs + 4.8 A × 13 µs = 72 µC, so ΔV ≤ 4.8 V. U201's input then peaks near
28.3 + 4.8 ≈ 33 V, below its 36 V recommended operating maximum. That is CALCULATED, and conditional on the eFuse
limiting at the microsecond scale. The eFuse OVP delay is specified to the FLT pin, not to the output. So the
comparison "TVS clamp vs 42 V" is the wrong criterion.

The right criteria are:
- the TVS never conducts at the steady or adapter-OVP maximum;
- the hot clamp plus L·di/dt overshoot stays below 67 V at the TPS26630;
- a sustained source overvoltage is handled by the eFuse OV cutoff, not by the TVS or F101.

**Recommendation:** keep SMBJ26CA captured for now. SMBJ24CA is rejected. The SMBJ30CA direction is a candidate once the
real adapter's OVP range is known and the hot-plug simulation shows < 60 V at U101 IN.

**Fuse coordination.** With a current-limited source (adapter hiccup at 105–150 % of 2.5 A, or a bench supply),
F101 (5 A class) cannot clear a sustained TVS conduction. The TVS would overheat and typically fail short. This is
another reason the TVS VBR must sit above the source's worst OVP.
