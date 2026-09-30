# Task 1b — timed source isolation and local capacitor discharge

**Analysis complete; source qualification BLOCKED.** Recommend **b as the development route**, with a qualified L201 envelope from Task 1a as an essential companion. Neither a larger choke alone nor a limiter before the local input capacitors closes the shared prerequisite.

## Real input-stage candidates

All application transfers are ASSUMED/OPEN until their stated conditions apply. Published controller endpoints are not physical current isolation.

| Candidate / primary revision | Published inputs used in CALCULATED screens | Result |
| --- | --- | --- |
| [Existing TPS26630](https://www.ti.com/lit/ds/symlink/tps2663.pdf), SLVSE94G, June 2024 | Operating 4.5–60 V; inherited resistor-corner settled limit CALCULATED 4.181–4.820 A. SHDN-crossing→FET off maximum 1.5 µs in table conditions; hot-short response 1 µs is typical. | Voltage range fits the requested screens. Fault→SHDN crossing, hot overshoot integral, retry behavior, input wiring commutation and application off-time remain OPEN. Do not use the overload timer as isolation. |
| [LTC4218](https://www.analog.com/media/en/technical-documentation/data-sheets/4218fh.pdf), Rev H, February 2016 | Operating ceiling 26.5 V; sense→GATE maximum 1 µs at 60 mV step, FB=0 and 1.5 nF gate. | BLOCKING at requested 27.63 V and inherited 28.289211 V. Absolute maximum is not the operating range. |
| [LT4256-1](https://www.analog.com/media/en/technical-documentation/data-sheets/425612fa.pm6.pdf), Rev A | Operating minimum 10.8 V | BLOCKING at frozen 9 V input; do not choose it for this module. |
| [LTC4260](https://www.analog.com/media/en/technical-documentation/data-sheets/4260fc.pdf), Rev C | Operating 8.5–80 V; sense 45–55 mV at specified feedback; sense→GATE maximum 1 µs at 200 mV / 10 nF / default 48 V. Below 20 V its gate-drive minimum is 4.5 V. | Candidate; actual response/isolation and hot FET resistance at low input need qualification. Weak ordinary turn-off differs from fast OC sink; UV/OV retry and power-on fault clearing need independent interlock. |
| [LT4363-1](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf), Rev C, January 2024 | Operating 4–80 V; sense 45–55 mV at 12 V, 48–58 mV at 48 V. OC response maximum 2.5 µs at 0→150 mV / OUT=0 / default 12 V; weak ordinary shutdown is separate. | No full application threshold/turn-off envelope follows from those separate test points. |
| [LTC4364-1](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4364-1-4364-2.pdf), Rev B, January 2023 | Operating 4–80 V; full-range sense 43–57 mV at OUT=2.5 V…VCC and stated temperature. OC→HGATE maximum 2 µs at 0→150 mV / OUT=0 / default 12 V. Ordinary fault/shutdown sink minimum 0.4 mA at VGS=5 V. | Best explicit full-input threshold evidence here, but use independent fast latched shutdown and qualify the capacitor/loop implementation. Not selected/qualified. |

CALCULATED from LTC4364 published sense limits and ASSUMED 10 mΩ total ±1% sense: settled 4.257–5.758 A. CALCULATED input current for inherited 25.491803 W / ASSUMED efficiency 90% / 9 V is 3.147136 A, before added source dropout/auxiliary power. It is an operating screen, not a current maximum.

Cascaded regulation is OPEN: the old TPS26630 can limit first. To guarantee added LTC4364 Imax≤old minimum 4.181 A, its threshold/resistor spread forces Imin≤3.091 A, below the normal screen: BLOCKING for that coordination premise. Owner can qualify the cascade, change upstream programming by a separately approved proposal, or investigate the narrower-threshold LTC4260. No programming is changed here.

LTC4364's normal capacitor recommendation is at least 22 µF electrolytic, with ceramic at most one tenth of that capacitance. Combined with LM61460's required ceramic input bank, this would imply at least 100 µF electrolytic before tolerances. It is incompatible with simply asserting a tiny downstream reservoir. Its recommended 6.8 nF HGATE compensation slows turn-off; the manufacturer's series-resistor/parallel-diode method helps but still needs an applicable maximum. A [manufacturer employee response](https://ez.analog.com/power/f/q-a/163373/ltc4364-with-all-ceramic-capacitors) describes a small all-ceramic example conditionally; it is not a guaranteed small-C stability envelope.

## Conditional source contract — not fulfilled by the surveyed data

PROPOSED qualification contract:

- ASSUMED bounded local/source voltage at the actual energy boundary, including cutoff/commutation overshoot; test 24 V and nominal 27.63 V, and include at least the inherited conditional 28.289211 V corner. OVP threshold does not physically clamp source amplitude. The real source ceiling is OPEN.
- ASSUMED effective local Cin between 10 and 30 µF over bias/temperature/tolerance/life. Every local reservoir and bypass counts. [LM61460 SNVSBD5D §9.2.2.5](https://www.ti.com/lit/ds/symlink/lm61460.pdf) requires input ceramic and bypass at both VIN/PGND pairs. Neither zero C nor a nominal minimum without effective-C qualification is accepted.
- ASSUMED physical source-current isolation ≤10 µs from the fault, including trigger development, sensing, latch, gate and commutation; positive replenishment charge ≤100 µC to that actual endpoint. Possible acceptance allocation: first 2 µs charge ≤30 µC, then ≤5.8 A for 8 µs gives CALCULATED 76.4 µC, leaving 23.6 µC allocation reserve. The data do not prove those targets.
- ASSUMED L201 `5 ≤ Ldiff ≤12 µH` over 0…100 A / full temperature, with healthy initial current ≤8 A. Proposed qualification candidate: 74437636351002; its typical curve ending at 100 A does not guarantee the envelope. Healthy startup/inrush/current-limit peak must be included in I0.
- ASSUMED nonnegative raw node during the positive-current energy proof, local voltage ceiling maintained throughout, no extra reservoir/backfeed, and separately qualified reverse/commutation paths. Every hidden capacitor and alternate supply invalidates a proof that omits it.

For any positive excursion under those conditions:

`Enew <= 0.5 Cin,max Vin,max² + Vin,max Qsource,+ + 0.5 Ldiff,max I0²`

`WL(I)=integral[i Ldiff(i) di] >=0.5 Ldiff,min I²`

`I_L,+ <=sqrt(2 Enew/Ldiff,min)`.

For a linear constant-L case this is the familiar `0.5 L I²`. The current envelope also obeys `I(t) ≤min[I0+Vin,max t/Ldiff,min, Ienergy]`. Integrate that envelope to get charge; do not identify input-source charge with output-inductor charge.

| CALCULATED within the ASSUMED contract | 24 V | 27.63 V | 28.289211 V conditional OVP corner |
| --- | --- | --- | --- |
| Local Cin energy, mJ | 8.640 | 11.451 | 12.004 |
| Continued-source work, mJ | 2.400 | 2.763 | 2.829 |
| Initial L energy, mJ | 0.384 | 0.384 | 0.384 |
| New fault-source pool, mJ | 11.424 | 14.598 | 15.217 |
| Positive L current ceiling, A | 67.599 | 76.415 | 78.018 |
| Rounded proposed design ceiling | ASSUMED 80 A | ASSUMED 80 A | ASSUMED 80 A |
| Physical fault→source-off min/max | OPEN / OPEN | OPEN / OPEN | OPEN / OPEN |

CALCULATED at the last corner, output charge upper envelope to raw node is 27.316 µC / 110.723 µC / 362.892 µC at ASSUMED 2 / 5 / 10 µs from fault onset. This includes local-C-fed current; replenishment charge remains a different boundary. Full tables are reproducible in [JSON](SOURCE_BOUND_CALCULATIONS.json). These finite values do not bound an unknown fault-to-trigger interval.

Keeping the old ASSUMED local Cin upper screen 60.996 µF instead gives CALCULATED current 105.109 A at the last corner, beyond the proposed 100 A L envelope: BLOCKING for this contract. Reducing capacitance needs actual bias/life minimum evidence, buck input-loop tests and limiter stability qualification; it is not an automatic fix.

At ASSUMED Ldiff=0.1 µH, even an isolated 30 µF bank at the last corner permits an energy-current screen near 490 A. This is not a predicted measured peak; it proves that a finite bank plus upstream limiting cannot itself supply the missing current bound.

## D and E energy boundaries

CALCULATED initial raw bank upper screen `(5.4144 mF+182.16 µF)×5.5²/2 =84.647970 mJ`, with all-temperature C and initial voltage still ASSUMED. This store bypasses L201 when discharging through a downstream series FET. Do not turn the positive L current ceiling into a protected-arriving-current ceiling.

| Receiving boundary / rated destination | CALCULATED conditional maximum / charge premise | What remains OPEN |
| --- | --- | --- |
| Shared source plus initial raw bank | 15.217113+84.647970=99.865083 mJ | Entire event trajectory/current, reverse flow, source ceiling, repetition and actual hot dump rating. A proposed 0.2 J hot capacity target is not a component rating. |
| D raw/source/module store subtotal | Add ASSUMED 1.5 mF protected-module initial C at 5.5 V: 122.552583 mJ | Separate Pi C,max is not specified. Complete all-store energy and protected arriving peak remain OPEN. |
| D protected absorber | With separately qualified ASSUMED 80 A arriving / 2 µs isolation / node≤5.48 V: charge≤160 µC, energy≤0.8768 mJ, plus entering magnetic/capacitor energy | Raw-bank bypass can invalidate 80 A. This is not established by L201's bound. |
| E input-side dump / limiter | Source/raw packet≤99.865083 mJ before cable/input capacitors and continuing local transition work | Cable/input-side peak and local capacitor bypass need their own bound and applicable hot SOA. |
| E protected GPIO-side absorber | ASSUMED 10 A / 5 µs: charge≤50 µC; voltage≤5.42 V gives 0.271 mJ, plus up to 2.5 mJ for a proposed last-path Lmax=50 µH at 10 A: total 2.771 mJ | The mechanism establishing 10 A, full clamp accuracy/dynamics and actual hot rating are not qualified. |
| E total source/raw plus Pi initial store | ASSUMED all Pi-side Cmax=1.5 mF at 5.5 V gives 122.552583 mJ | Dump partition versus deliberate discharge must be analyzed. A voltage-holding clamp need not dump the full Pi capacitor. |

These are allocation pools/subcases, not additive component energies: use energy conservation and actual partition. If local source voltage is allowed above the listed input or current persists after the assumed endpoint, recompute. Any supply/backfeed not included keeps the bound OPEN.

## a versus b and source recommendation

| Route | Advantage | Consequence |
| --- | --- | --- |
| a: published-curve replacement alone | Gives a useful high-current model; selected candidate lowers copper loss | Unknown shutdown time still allows continuing energy. Typical curve is not a guarantee. Large package, ripple and loop changes; shared prerequisite remains OPEN. |
| b: timed input limiter and bounded local C, with qualified L201 as companion | Actively bounds replenishment work and explicitly includes the cap it cannot control | Requires source-charge/off-time evidence, a workable capacitor/loop implementation and a qualified magnetic floor. Raw bulk downstream current is separate. |

Recommend **b plus the 10 µH alloy qualification candidate**, not b alone. This is a concrete development contract; it is not SOURCE BOUNDED yet. A passive upstream current-rise inductor is another possible way to bound source charge, but it must be before the final isolating FET and dump upstream; otherwise its tail continues charging local Cin. Its own L/current/DCR/energy and filter stability need qualification and are not silently omitted.

Tests needed: fault injection with dummy loads at all qualified source/cable/C/L corners; capture the source charge integral and actual current isolation, both sides of the output disconnect, Pi voltage and loaded gate/reference rails; startup/inrush, source/limiter/buck stability, normal load release, hot SOA/terminal temperatures, reset/brownout/reappearance and repeated-event cooling. Manufacturer acceptance limits plus those waveforms, not the owner's architecture choice alone, close technical dependencies.
