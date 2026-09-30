# Task 3 — D/E re-score with the proposed source contract

**Analysis complete. Recommend neither for implementation approval yet.** Gate3's preference for E was a development direction. Gate3b finds credible component routes, but no qualified current/source/timing/trip/normal-path contract. No frozen requirement is relaxed.

## New voltage detector, no inherited trip-maximum credit

Do **not** use inherited 5.356563 V as D/E proof input. Its hysteresis, feedback/reference/passive and application timing bounds are not complete. [TLV9031-Q1 SNOSDA9E, May 2024](https://www.ti.com/lit/ds/symlink/tlv9031-q1.pdf) explicitly has no internal hysteresis and a published full-temperature offset bound, making a new reference/divider/first-event latch worth investigating. [REF5025EID, REF50 SBOS410O, October 2025](https://www.ti.com/lit/ds/symlink/ref50.pdf) offers tighter initial reference error/drift than the inherited selection. Comparator bias and delay, reference startup/lifetime/thermal history and actual powered-off clamp leakage do not supply all applicable maxima. Full trip remains **OPEN/OPEN**.

ASSUMED new qualification allocation: full rising trip 5.300–5.340 V, including every static input error. This is a procurement/application specification, not evidence that the named candidate meets it. New proof also needs maximum response from the actual threshold crossing, or explicit extra overdrive. A fast comparator bound beginning at 50 mV sense overdrive would need approximately 106.5 mV rail increase with a divider gain near 2.13: it cannot be silently added as a few-nanosecond delay. CALCULATED with that extra rise, 10 A / 5 µs /1 mF /5 mΩ /20 mV ringing and 5.340 V target gives 5.5665 V: **BLOCKING**. A no-hysteresis candidate lacking a maximum delay is OPEN, not an automatic timing fix.

Normal release must also be re-qualified. CALCULATED with ASSUMED 10 µH part upper L=12 µH, release current 6 A, 20 µs excess interval, raw Cmin=2.4064 mF, ESRmax=4 mΩ and 20 mV ripple gives normal 5.270315 V. Against new trip-min target 5.300 V and ASSUMED 10 mV reserve, margin is +19.685 mV. At 30 µs it is −5.249 mV: **BLOCKING**. With 8 A at 20 µs, normal becomes 5.308794 V, reserve −18.794 mV: **BLOCKING**. The proposed source initial-current limit of 8 A is not permission for every healthy release to reach 8 A while using the 6 A nuisance calculation. Define which startup/ARM/load transitions are allowed and qualify their actual maximum envelope. This raw-node calculation does not include E's added 35–50 µH choke or GPIO-node load release; recompute that complete healthy trajectory before claiming any E false-trip margin.

## D — module-side disconnect and absorber

Task1's conditional 80 A ceiling is for positive L201 current. A raw output bank downstream of L201 can discharge through the series FET into the protected node while bypassing L201. D still needs an independent protected-arriving-current bound including that bank, sense/FET parasitics and current commutation.

CALCULATED only if protected arrival is separately qualified ≤80 A, useful clamp response≤0.5 µs, Cprotected≥1 mF, ESR≤0.5 mΩ, static clamp upper≤5.38 V and ringing≤20 mV:

`Vmodule≤5.38+80×0.5µs/1mF+80×0.5mΩ+20mV =5.480 V`.

Reserve +20 mV is conditional, and is smaller than Gate3's 60 A screen. Protected-interval charge≤160 µC / energy≤0.8768 mJ at ASSUMED 2 µs physical isolation. Source/raw/module subtotal≤122.552583 mJ excludes unspecified separate Pi C,max and additional cable/commutation work; actual absorber/dump ratings remain OPEN.

The module result does not determine Pi peak. Gate3's two-capacitor/harness initial-state counterexample remains CALCULATED 5.542140 V under its ASSUMED state box, −42.140 mV: **BLOCKING**. It is a reachability sensitivity, not a measured trajectory, but the current contract does not exclude it. Full module-C / harness-L / Pi-C / clamp / load-release modeling and characterized damping are still required. Source bounding does not erase those initial-state possibilities.

Normal path screen remains CALCULATED 4.761433 V /+11.433 mV using inherited ASSUMED 55.367741 mΩ and regulator minimum. A proposed hot 10 V gate-driven PSMN1R0-100ASE module pair at 4.8 mΩ in place of inherited 13.6 mΩ pair gives CALCULATED loop 46.567741 mΩ and Pi 4.805433 V. Actual gate rail, footprint/copper/joints, SOA and regulator minimum remain OPEN; it is not a tested substitution.

D status: **BLOCKED** by shared source qualification, protected-arriving bypass current, full Pi trajectory, complete timing/supply and full normal margins.

## E — concrete mechanism for the proposed 10 A ceiling

PROPOSED mechanism: every significant unprotected reservoir → local shunt/current breaker → opposed disconnect → qualified current-slope choke → GPIO capacitor/absorber, with a defined input dump and protected-side commutation path. No precharge/bypass branch or unsensed capacitor may inject current around the choke/sense boundary.

Real controller research candidate: [TPS48111LQDGXRQ1, TPS4811-Q1 SLUSEE5E, April 2026](https://www.ti.com/lit/ds/symlink/tps4811-q1.pdf). Published SCP threshold 35–45 mV at RISCP=2.1 kΩ and SCP→PD-low maximum 1.6 µs use 48 V supply/sense, bootstrap 12 V, SRC=0 and 47 nF load. That endpoint is not actual current isolation at this supply/FET configuration. Configure external/CTMR latch-off explicitly. SCP leaves the precharge G state unchanged: independent fault logic must disable any such branch. Bootstrap UVLO does not assure the loaded 10 V VGS required by the resistance budget. Sense-pin bias/filter errors and drain slew limits also enter the implementation proof.

CALCULATED from those threshold limits and ASSUMED 6 mΩ total hot ±1% shunt: current threshold 5.775578–7.575758 A **before RISCP/filter/loading errors**. New required full threshold upper≤8 A, additional source-current cutoff≤2 µs, and maximum positive voltage across the last choke≤31.5 V including commutation/ringing are ASSUMED qualification targets. Then:

`Iarrival,max ≤ Itrip,max + VL,max tresp,max/Ldiff,min`.

CALCULATED required `Ldiff,min≥31.5 µH` to stay at 10 A. Propose ASSUMED **35≤Ldiff≤50 µH** through the full 0–10 A/temperature excursion, giving CALCULATED 9.8 A before additional unsensed injection. The remaining 0.2 A is not a confirmed parasitic-current allowance: any displacement current/bypass term must fit the 10 A peak requirement or be separately bounded and re-scored. No choke MPN with both this guaranteed floor and required hot DCR is qualified here. Placing it upstream of a charged bypass capacitor defeats this proof.

The 2 µs endpoint is cessation of additional source-side positive work at the disconnect, not GPIO current reaching zero. Downstream choke current must commutate and decay. An ASSUMED ideal 50 µH /10 A tail opposed by 5.42 V takes CALCULATED about 92 µs; actual diode/clamp voltage, damping, node floor and decay maximum are OPEN.

This is the **named mechanism that could enforce 10 A**, not a demonstrated 10 A limit. The actual current maximum is OPEN. At response 3 µs with the same 35 µH/31.5 V/8 A contract, CALCULATED current reaches 10.7 A, so the 2 µs endpoint is essential. A settled current-limit setting is insufficient.

Source/raw energy ceiling from Task1 is 99.865083 mJ under its separate ASSUMED source contract. Local protected-absorber subcase at voltage≤5.42 V /10 A /5 µs plus last-choke Lmax=50 µH at 10 A gives CALCULATED **2.771 mJ**; the initial 5 µs interval contributes at most 50 µC, not the full protected charge. The ideal 50 µH /10 A /5.42 V tail contributes about 461.255 µC, and actual total protected charge remains OPEN; a proposed hot capacity target of 10 mJ would need applicable SOA/temperature/repetition evidence. When placed after the disconnect, the choke's tail needs a protected-side return that does not drive GPIO negative or bypass protection. Its stored energy is not the cable/input dump's energy.

E's new static clamp allocation remains ASSUMED 5.30–5.40 V plus ≤20 mV total physical/dynamic overshoot: target 5.420 V, +80 mV. None of its full loop/error/delay terms is qualified. CALCULATED initial-interval series sensitivity using **new 5.340 V target**, not the inherited trip: 10 A /5 µs /1 mF /5 mΩ /20 mV gives 5.460 V. It omits the downstream choke tail and is **not a series-only acceptance bound**. Even ideal instantaneous source opening with ASSUMED Pi capacitor 5.340 V, 1 mF, choke 50 µH/current 8 A and a lossless protected return gives `sqrt(5.340²+L I²/C) =5.631661 V`, margin −131.661 mV: **BLOCKING without the active absorber**. A real absorber/commutation path must dispose of this energy. Actual E Pi peak remains OPEN.

## E — concrete 50 mΩ plan and component tradeoffs

Real low-resistance research candidates; application hot drive/SOA transfer remains OPEN:

| MPN / primary revision | Published hot resistance used in CALCULATED pair screens | Consequence |
| --- | --- | --- |
| [PSMN1R0-100ASE](https://assets.nexperia.com/documents/data-sheet/PSMN1R0-100ASE.pdf), 2025-10-20 | Maximum 2.4 mΩ/device at 175°C /10 V gate; pair 4.8 mΩ | Enhanced SOA candidate, but published cold maximum gate charge 509 nC/device increases driver/hold-up cost |
| [PSMN1R0-40YSH](https://assets.nexperia.com/documents/data-sheet/PSMN1R0-40YSH.pdf), 2019-04-25 | Maximum 2.2 mΩ/device at 175°C /10 V gate; pair 4.4 mΩ | Lower voltage headroom; low RDS does not establish linear turn-off SOA |
| [PSMN1R0-40YLD](https://assets.nexperia.com/documents/data-sheet/PSMN1R0-40YLD.pdf), 2017-11-30 | Maximum 1.93 mΩ/device at 150°C /10 V; pair 3.86 mΩ. At 4.5 V pair 4.90 mΩ | Gate rail matters. Gate-charge maximum/hot turn-off path OPEN. Both 40 V candidates have published minimum cold breakdown 36 V; input dump plus ringing must remain below applicable ratings |

| Proposed total loop element | ASSUMED hot maximum / CALCULATED subtotal, mΩ | Qualification needed |
| --- | --- | --- |
| Historical path excluding old series pair | CALCULATED 55.367741−13.6=41.767741 | Inherited wire/copper/contact/shunt allocations, not measured maxima |
| Reduce GPIO/contact contribution | ASSUMED 24.375→15.000; save 9.375 | Select actual contacts/parallel conductors/returns; GPIO 5 V remains only pins 2/4, so extra 5 V pins cannot be assumed; include the Pi header's unselected resistance envelope; bound imbalance, rating, aging and hot resistance. More parallel pins require safe sharing; no new connector is selected |
| Module 100ASE opposed pair | ASSUMED applicable hot total 4.800 | Loaded ≥10 V, junction limit, package/copper and hot SOA |
| Pi-end 40YLD opposed pair | ASSUMED applicable hot total 3.860 | Loaded ≥10 V, ≤150°C, actual gate/current/VDS trajectory |
| New local current shunt | ASSUMED 6.060 | Total ±1% hot envelope, Kelvin/filter errors; retained 2 mΩ telemetry shunt remains in historical path |
| Added current-slope choke | ASSUMED hot DCR≤2.500 | A real MPN must satisfy 35 µH floor through 10 A and the DCR/thermal/package/commutation contract |
| New joints/PCB changes | No hidden free allowance | Must fit/recover space in the listed totals; otherwise add their resistance and re-score |
| Total | CALCULATED **49.612741** | Margin to 50 mΩ target is only 0.387259 mΩ |

CALCULATED inherited regulator minimum 5.038271 V minus 5 A×49.612741 mΩ gives **Pi 4.790208 V**, reserve +40.208 mV. This makes E's resistance target arithmetically feasible, not qualified. Regulator IFB worst case, actual contacts, choke, new joints and gate conditions remain OPEN.

Retaining the old contacts and two 100ASE pairs already gives CALCULATED **51.367741 mΩ before the new shunt/choke**. Keeping the full old loop and adding 10 mΩ gives Pi **4.711433 V, −38.567 mV: BLOCKING**. Using two 100ASE pairs after the proposed contact reduction plus shunt/choke gives 50.552741 mΩ; it misses the design target, although its conditional static voltage can still exceed the frozen 4.75 V floor. These are different limits and must not be confused.

The large choke, extra driver supply, FET gates and contact redesign increase area/wiring/assembly effort. Exact cost/availability is OPEN; planning comparison is ASSUMED high effort for E versus medium effort for D's characterized harness/damping. No purchase or schematic change is authorized.

E status: **BLOCKED** by actual 10 A mechanism timing/magnetic/capacitive bounds, shared source qualification, full fresh detector/clamp limits, rail/SOA validity and actual loop resistance. No electrical implementation approval for D or E is supported yet.
