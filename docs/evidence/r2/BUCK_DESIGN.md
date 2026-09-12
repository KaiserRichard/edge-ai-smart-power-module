# LM61460 schematic review

Date: 2026-09-12. **REVIEW DRAFT; NOT FOR FABRICATION.**
CALCULATION, EVIDENCE and OPEN RISK are distinguished below. No fallback is
selected: no blocking incompatibility of LM61460 with the frozen conversion
requirement was identified. Component and implementation qualification remains.

## Reference and adaptation

SOURCE: TI [LM61460 SNVSBD5D](https://www.ti.com/lit/ds/symlink/lm61460.pdf),
Tables 5/6-1, sections 7, 9.2 and 11; [LM61460-Q1 EVM SNVU621D](https://www.ti.com/lit/pdf/snvu621),
Fig 4-1 and BOM/layout/results. Local identities are in source_register.json.
FUNCTION: protected 9-24 V DC to nominal 5.1 V, 5 A. Exact U201 order code:
**LM61460AANRJRR**, catalog auto-mode, adjustable frequency, no spread spectrum.
The Q1 EVM is a circuit/layout reference, not proof of identical variant behavior.

MODIFICATION: retain recovered 6.8 uH, 33.2 kOhm RT, 100k/24.4k feedback,
22 pF + 1 kOhm feedforward, zero-ohm RBOOT, split input bypass and six 22 uF
50 V output ceramics. Ground BIAS; omit recovered R208/R209/C208. PGOOD is NC;
VCC supplies its required 1 uF bypass only. Input eFuse PGOOD pulls buck EN low.
RATIONALE: normal 24 V needs voltage headroom; larger L aids ripple/tolerance
screening; raw capacitors must withstand upstream voltage under a buck fault.
BIAS-to-raw-output would expose a 16 V pin to that fault. Grounding BIAS is a
supported operating configuration, with additional internal-LDO loss.

## Conversion and current screening

Run `python3 scripts/calculate_r2.py`; executed values are in calculations.json.
Equations: D=Vo/Vi; deltaI=Vo(1-D)/(L f); Ipk=5+deltaI/2;
Irms=sqrt(25+deltaI²/12). Values use the actual divider result, **5.09836 V**.

| Vi | D | Ton at 400 kHz | Ripple | Peak | RMS |
| --- | ---: | ---: | ---: | ---: | ---: |
| 9 V | 0.5665 | 1416 ns | 0.813 A | 5.406 A | 5.005 A |
| 12 V | 0.4249 | 1062 ns | 1.078 A | 5.539 A | 5.010 A |
| 24 V | 0.2124 | 531 ns | 1.476 A | 5.738 A | 5.018 A |

RT=33.2k gives 360-440 kHz per TI's specified setting, before additional external
resistor uncertainty. At 24 V and 440 kHz, required Ton is **483 ns**, comfortably
above the specified 70 ns maximum minimum-on-time at its test condition. At 9 V,
required off-time is about 0.985 us at 440 kHz, versus 85 ns maximum minimum-off-time.
Input-protection drops slightly raise low-input duty; regulation does not approach
dropout. No 6 A peak output rating follows from the IC's 6 A class.

L201 **XAL8080-682MED**: 6.8 uH +/-20%; 14.5 mOhm maximum DCR at 25 C;
14 A causes 30% **typical** inductance loss; 8 A RMS corresponds to 20 C rise in
Coilcraft's reference conditions. Neither current number is a board guarantee.
Source: [Coilcraft document 839, 05/01/26](https://www.coilcraft.com/getmedia/345e50d6-a804-4ecb-9a92-5185221faf3e/xal8080.pdf).

ASSUMPTION: screen an additional 10% inductance reduction with DC bias. With
-20% initial L and 360 kHz, Leff=4.896 uH and 24 V peak=**6.139 A**. TI Eq 10
requires L>=0.32 Vo/f=**4.532 uH**; Eq 11 for D<50% cannot cover the 9 V point.
At 9 V, maximum L/f gives 0.616 A ripple, near TI's 0.6 A rule-of-thumb floor;
the nominal-condition ripple is 0.813 A. Confirm biased/hot L, including actual
input drops, against the complete control range. The assumed 10% is not a guaranteed
Coilcraft production bound. Even at 24 V nominal RMS remains about 5 A.

TI lists HS current limit 8.9/10.3/11.5 A as D approaches zero and LS valley limit
6.1/7.1/8.1 A. Required nominal valleys are 4.26-4.59 A. Do not apply the 8.9 A
minimum unmodified at every duty: slope compensation reduces HS limit as duty
rises. The manufacturer's 5 V/6 A application supports feasibility, but the
hot/duty-dependent margin must be closed in detailed qualification. L saturation
screening compares the 14 A typical soft-saturation point with **11.5 A maximum
HS limit**, not simply with 5 A. Hot-lot L and fault-current overshoot remain OPEN.

Inductor copper loss with the screened ripple and 25 C maximum DCR is **0.369 W**;
at 100 C, a copper 0.00393/C approximation gives about 0.478 W. Core/AC losses and
nearby regulator heat are additional. No thermal improvement is claimed.

## Capacitors, feedback and fault exposure

**C5750X7R1H226M250KB**, 22 uF +/-20%, 50 V X7R, is retained for the large banks.
TDK's [product record](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C5750X7R1H226M250KB)
confirms the part and dimensions. Its 19-Mar-2019 characterization is cached only
as a mirror; official PDF retrieval failed. Treat DC-bias curves as typical data.
Using explicitly conservative screening factors (not guaranteed combined limits):

- Input: 2 x 22 uF x 0.65 bias x 0.8 tolerance x 0.85 temperature = **19.448 uF**.
- Output: 6 x 22 uF x 0.95 bias x 0.8 tolerance x 0.85 temperature = **85.272 uF**.
- TI requires at least 10 uF ceramic input plus a local 100 nF/50 V X7R at **each**
  VIN/PGND pair. Input-capacitor bank RMS reaches about **2.48 A** at the reviewed
  points, or 2.5 A near half duty; approximately 1.25 A each with equal sharing.
- At 24 V, screened ripple and an **assumed bank ESR=2 mOhm** give 13.8 mV using
  deltaV=deltaI/(8 f C)+deltaI ESR. This excludes spikes and is not a 50 mV PASS.
  Output-cap RMS is approximately deltaI/sqrt(12), 0.66 A in the screened corner.

The larger bank is an adaptation of TI's 2 x 47 uF/16 V typical design. TI Table
9-2 uses 22 pF CFF while Table 9-3's minimum-transient row uses 10 pF; retain 22 pF
as explicitly supported by Table 9-2 and its 1 kOhm series-resistor guidance.
Neither bank substitution nor transient stability is qualified without the load
step/capacitance requirement. MLCC aging, bias/temperature interaction, source
impedance, ripple heating and step response remain OPEN.

The 100k/24.4k 0.1% divider gives 5.09836 V. Combining a +/-1% reference with
resistor tolerance and a **10 nA illustrative FB-current allowance** gives
5.0383-5.1586 V; the FB-current datum is not a guaranteed all-condition bound.
Auto-mode light-load behavior, dynamic overshoot and distribution loss are outside
this static calculation. Feedback remains at VOUT_5V1, never after the disconnect.

C203/C204 100 nF/50 V: 24/50=48% voltage use. C209-C214 also 50 V to cover the
specified upstream-voltage failure model, not just normal 5.1 V. Bootstrap C205
100 nF/16 V sees CBOOT-SW differential, not VIN-to-ground. VCC C206 1 uF/16 V is
local. Exact small-capacitor MPNs and effective capacitance remain open.

## Thermal evidence and acceptance

EVIDENCE: TI Fig 9-2 describes a **100 x 80 mm four-layer EVM**, approximately
25 C/W effective thermal resistance, at 400 kHz/5 V and currents through 6 A.
The 24 V/5 A curve is near 108 C maximum ambient under those conditions. This
brackets the proposed 25.5 W class but does not establish V1A temperatures. The
58.7 C/W JEDEC number is a package comparison metric, not a board design constant.

The whole-module loss allowance at 25.5 W and 90% is **2.833 W**. Grounding BIAS
adds roughly ILDO x (VIN-5.1 V) relative to output bias; e.g. **0.189 W if ILDO is
10 mA at 24 V**. That current is a sensitivity example, not a measurement.
Input protection, output FETs, shunt, fuse, copper and connectors all consume the
same budget. The independent output stage is not selected, so efficiency cannot
yet be guaranteed. R5 should measure connector-to-connector efficiency at 12/24 V,
3/5 A, approximately 25 C, natural convection, and record uncertainty/equilibrium.

## Pin/package and later layout gates

All 14 IC pin identities were checked against Table 6-1 and its diagram. There is
**no invented exposed-pad pin 15**. RJR0014A has asymmetric power lands; a generic
QFN is unacceptable. U201 footprint remains blank. The recovered generic 2220
footprint has 1.8 x 5.4 mm pads and 3.3 mm inner gap; TDK recommends a different
land window. Those assignments were cleared, preserving exact MPNs and evidence.

Schematic connectivity provides both VIN feeds, both PGND feeds and AGND join;
R3 must implement TI's two short capacitor/switch/ground loops, quiet FB/RT/VCC
return, minimized SW loop and thermal spreading. No placement/routing was done.
