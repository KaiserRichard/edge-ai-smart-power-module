# Direct 24 V feed assessment

2026-10-04 — analysis of baseline `5f371fd7c59e90a5037004b9309bff63b0d95e71` on `docs/v1a-direct-24v-feed`.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED. R2 electrical release remains BLOCKED.** No schematic/PCB changes, purchase, physical test or gate advancement. This assessment follows the supplied `DIRECT_24V_FEED.md` brief; no sub-agents were used.

**DECISION / verdicts for the available evidence:**

| Case | Requested verdict | Reason and conditional alternative |
| --- | --- | --- |
| UENPO S4-T482410 | **NOT SAFE for direct feed** | The brief's **ASSUMED 54.6 V** high-side-short pass-through is outside V1A's frozen envelope. D101 is not a sustained-fault absorber, F101 is not coordinated to save it, and the buck has **KNOWN 36 V operating / 42 V absolute input limits** [S4 p4]. A nominally suitable output does not close this fault. |
| Isolated MEAN WELL DDR-120C-24 or RSD-200C-24 | **NOT SAFE to approve direct from the present evidence; direct-feed compatibility is conditional** | A genuinely bounded **ASSUMED ≤34 V total fault peak at V1A** is compatible with the main input voltage-rating screen and would support **safe direct within that explicitly bounded source case**, without an extra DDR-60L-12 for voltage reduction. However, the actual module datasheets specify OVP **shutdown**, not a guaranteed peak clamp: fault overshoot/duration and normal load-step overshoot remain **OPEN**. They do not yet establish that premise. Existing V1A thermal and protection release blockers also remain. |

This distinguishes an incompatible fault envelope from an incomplete qualification. It is not a claim that the MEAN WELL modules fail in practice. **DECISION:** case 2 does **not** change the frozen decision excluding survival of **ASSUMED 54.6 V** at V1A. Isolation and secondary-side OVP are upstream containment features; the missing secondary fault waveform must be bounded upstream. No cheap add-on is qualified in this analysis, so no “safe with a cheap add-on” verdict or corresponding part/cost claim is made.

Evidence labels apply to every value below: **KNOWN** = manufacturer specification with cited PDF page, or explicitly identified captured project fact; **CALCULATED** = derived result; **ASSUMED** = scenario/screen, not a requirement or guarantee; **OPEN** = unavailable bound. Dates, document IDs, part numbers, refdes and source revisions are identifiers. Sources S1–S13/M1–M2, URLs, exact revisions, access date, license/use and file hashes are registered under [third_party/direct_24v_feed](../../../third_party/direct_24v_feed/SOURCES.md). All component PDFs were read without changing the read-only datasheet worktree. No behavior is MEASURED.

## Current circuit and limits

**KNOWN project requirements/capture:** input **9–26 V**, D101 **SMCJ36CA**, F101 **SCHURTER 3403.0285.23**, U101 **TPS26630RGER**, R103/R104 **348 kΩ / 15.8 kΩ**. The latest [Sheet01 review](gate4b/SHEET01_RESUME2_REVIEW.md) supersedes the older context's input range/TVS/fuse entries. A fresh KiCad CLI netlist confirms:

`VIN_RAW → F101 → VIN_FUSED → Q101 → VIN_EFUSE_IN → U101 → JP101 → VIN_PROTECTED → U201`

D101 shunts **VIN_FUSED to GND**, upstream of U101. U101 disconnecting therefore does **not** stop current through D101. D303 also feeds the independent auxiliary chain from **VIN_FUSED**, bypassing U101; auxiliary protection must be considered separately.

**KNOWN current buck capture:** L201 is **10 µH / 74437636351002**; R201 is **33.2 kΩ**; R202/R203 are **100 kΩ / 24.6 kΩ**; U201 BIAS is grounded. [R203 option A](R203_OPTION_A.md) supersedes both the older nominal output and the retained Gate4B netlist/BOM snapshots. **CALCULATED** output is **5.065041 V**, not the historical **CALCULATED 5.098361 V**. The earlier context's **KNOWN historical 6.8 µH** inductor is not used here.

| Device/path | KNOWN rating and source | CALCULATED comparison / OPEN behavior |
| --- | --- | --- |
| U101 TPS26630 | **4.5–60 V** operating; **67 V** absolute on IN, OUT and IN_SYS; **75 V / 10 ms / 25°C** transient rating only for the named input pins [S1 p5]. | **34 V** and **54.6 V** scenario levels are below its DC input limits. This does not qualify the whole board. Use the table's **67 V**, despite the family overview's inconsistent **70 V** prose. No **75 V** allowance is assigned to OUT. |
| Q101 CSD19537Q3 | **100 V VDS**, **±20 V VGS** absolute [S7 p1]. | Static voltage rating is not the controlling positive-input limitation; transient gate drive/SOA remain OPEN. |
| Q102 BSS138 | **50 V VDS**, **±20 V VGS** absolute [S8 p2]. | Source is VIN_FUSED, drain B_GATE, gate DRV. Do not compare its ground-referenced rail directly with VDS: this is a floating gate-discharge device. Differential stresses/reverse events remain OPEN. |
| C101/C102, auxiliary C378 | **KNOWN capture 1 µF / 100 V**, exact Murata rating [S9 p2]. | The scenario voltages fit their voltage rating; bias-dependent capacitance and transient current remain OPEN. |
| U201 LM61460 | **3–36 V** operating after startup; **42 V** absolute VIN; **0–6 A** specified output-current range subject to thermal derating [S4 p4]. | A **34 V** peak leaves **CALCULATED 2 V** to the operating ceiling and **8 V** to absolute max. **54.6 V** exceeds absolute max by **CALCULATED 12.6 V** if transmitted. |
| U201 input ceramics | **KNOWN current capture 2 × 10 µF / 50 V** plus local bypass. | A **34 V** scenario uses **CALCULATED 68%** of their captured rating; **54.6 V** exceeds it by **CALCULATED 4.6 V** if transmitted. This is a capture-rating screen; installed capacitance remains OPEN. |
| Independent auxiliary path | **KNOWN** D303 BAT46W **100 V reverse / 200 mA forward** [S10 p1]; Q316 FDB33N25 **250 V VDS** [S11 pp1–2]; U316 LT4363 **80 V operating / 100 V absolute** [S12 pp2–3]. | These ratings do not imply an auxiliary thermal/SOA PASS. U316 limits this branch, not the main feed or D101 current. |
| U317 LTC3115-1 after auxiliary limiter | **2.7–40 V** operating, **45 V** absolute [S13 pp1–2]. | **34 V** is inside its voltage range even before allowing for the limiter. **54.6 V** cannot be credited without qualified U316/Q316 clamp response. |
| Output protection, monitor and Pi | **KNOWN capture:** opposed output switches, held auxiliary rails and manual source-trigger architecture. | Upstream cutoff does not discharge stored downstream energy or prove the required Pi ceiling. Current [Gate4B OPEN risks](gate4b/SHEET03_REVIEW.md) persist; no SBC connection authorized. |

## U101 threshold and nuisance-trip budget

**KNOWN [S1 p6]:** rising OVP comparator **1.176 / 1.200 / 1.224 V**, input leakage **−150…+150 nA**, falling comparator **1.09…1.15 V**. **KNOWN [S6 p4]:** both selected divider MPNs encode **±0.1% initial resistance and ±25 ppm/K TCR**. Let positive `Ipin` flow into OVP:

`Vtrip = Vref × (1 + R103/R104) + Ipin × R103`.

**CALCULATED initial corners:** **26.973873 / 27.630380 / 28.289211 V** minimum/nominal/maximum. Thus the brief's approximately **26.97 V** is the low tolerance corner, not nominal. Initial recovery corners are **CALCULATED 24.997480…26.582075 V**. Returning to a high normal rail can therefore delay recovery after an OVP event even when below the rising threshold.

**ASSUMED temperature screen:** each divider resistor lies within **−40…+125°C**, maximum displacement **105 K** from the **KNOWN 20°C** TCR reference [S6 p12]; independent worst-sign TCR, no tracking credit. The combined resistance bound is **CALCULATED ±0.3625%**. Trip becomes **CALCULATED 26.838652…28.431540 V**, recovery **24.872158…26.715807 V**. Installed resistor temperature, aging, contamination/PCB leakage and module behavior outside the quoted temperature-coefficient ranges are **OPEN**. This screen is not a lifetime guarantee.

**KNOWN [S1 p8]:** the timing table names an OVP turn-off delay of **8.5 / 11 / 14 µs**, measured from **20 mV comparator overdrive to FLT falling** under its stated conditions. **CALCULATED** equivalent nominal input overdrive is about **0.461 V**. This is neither instantaneous cutoff nor a guaranteed maximum VIN_PROTECTED peak. Source slew, input-capacitance effective minimum, current-limit dynamics, loop inductance and complete current interruption remain **OPEN**. The captured TPS26630 is a cutoff part, not a fixed-clamp family variant [S1 pp19–20]. MODE open selects latch-off for specified current/thermal faults; do not infer that every OVP event requires a power cycle—OVP recovery is separately described [S1 pp8, 19–20].

## Normal module operation

**ASSUMED operating point for comparison:** module adjusted/verified at **24.0 V**, with **5 A** at the buck output. Module output current is much lower than buck output current; the buck-only draw is **CALCULATED approximately 1.12–1.13 A** under the typical-efficiency screen below. Auxiliary demand, startup charging and any other loads on the module are **OPEN** additions.

| Item | Case 1: UENPO S4-T482410 | Case 2a: DDR-120C-24 | Case 2b: RSD-200C-24 |
| --- | --- | --- | --- |
| Nominal / input / power | **ASSUMED from brief:** nonisolated **48→24 V**, input **30–60 V**, no output OVP. Exact datasheet unavailable; output-current rating not inferred from the MPN. | **KNOWN [M1 p3]: 24 V, 5 A, 120 W; 33.6–67.2 V input.** | **KNOWN [M2 p1]: 24 V, 8.4 A, 201.6 W; 33.6–62.4 V continuous input.** |
| DC output tolerance | **OPEN** initial, line/load and temperature bounds. | **KNOWN ±1%**, includes setup/line/load [M1 p3 note 3]. | **KNOWN ±2%**, includes setup/line/load [M2 p1 note 3]. |
| Trim range | **OPEN**; no assumption that trim exists. | **KNOWN 24–28 V** [M1 p3]. Upper trim is incompatible with the V1A normal envelope. | **OPEN / not specified** in [M2 p1]; treat as fixed nominal output, do not invent adjustable range. |
| Ripple/noise | **OPEN** | **KNOWN 50 mV p-p maximum** [M1 p3], subject to its measurement arrangement. | **KNOWN 150 mV p-p maximum** [M2 p1], subject to its measurement arrangement. |
| Temperature coefficient | **OPEN** | **KNOWN ±0.03%/°C over 0–55°C** [M1 p3]. | **KNOWN ±0.03%/°C over 0–50°C** [M2 p1]. |
| Startup / load release | **OPEN** voltage peaks, slew, duration, restart. | **KNOWN setup/rise 500/60 ms** at stated conditions [M1 p3]; **OPEN** guaranteed peak overshoot. | **KNOWN setup/rise 800/50 ms** at stated conditions [M2 p1]; **OPEN** guaranteed peak overshoot. |

Do not double-count the separately printed line/load-regulation figures on top of the inclusive tolerance. Startup times and static load regulation do not specify dynamic overshoot. For the following **ASSUMED conservative screen**, add the entire ripple p-p value to the DC high side, not half; no symmetry is assumed. This still does not bound wiring ringing or load steps.

| Screen | CALCULATED normal high before dynamic overshoot | CALCULATED margin to low U101 trip | CALCULATED margin to frozen normal 26 V ceiling |
| --- | ---: | ---: | ---: |
| DDR, datasheet reference **KNOWN 25°C** | **24.290 V** | **2.684 V**, initial divider | **1.710 V** |
| RSD, datasheet reference **KNOWN 25°C** | **24.630 V** | **2.344 V**, initial divider | **1.370 V** |
| DDR, **ASSUMED 0–55°C** module plus divider-temperature screen | **24.506 V** | **2.333 V** | **1.494 V** |
| RSD, **ASSUMED 0–50°C** module plus divider-temperature screen | **24.810 V** | **2.029 V** | **1.190 V** |

Temperature additions use **CALCULATED +0.9% DDR / +0.75% RSD** relative to the reference temperature, with worst signs. **DECISION:** these are available budgets, not predictions of the missing overshoot. Require normal startup/load-release/ripple/ringing peaks to remain within the frozen normal ceiling and below the qualified low trip, with an agreed reserve (**OPEN**). For example, the last two rows leave only **CALCULATED 1.494 / 1.190 V** for additional positive excursions before exceeding the normal envelope; the larger OVP margin is not permission to operate there.

**CALCULATED DDR trim limits**, with no dynamic reserve: initial DC/ripple screen gives setpoint **≤25.693 V** to stay within the normal ceiling; the module-temperature screen gives **≤25.466 V**. At its **KNOWN 28 V** upper adjustment, initial error plus ripple reaches **CALCULATED 28.330 V**, exceeding even the initial maximum rising trip. Keep the intended setting at **ASSUMED 24 V** and verify it; no module trim was performed. **OPEN:** guaranteed UENPO margin. An ideal error-free **ASSUMED 24 V** would have **CALCULATED 2.974 V** initial OVP headroom, but cannot substitute for its absent tolerance/trim/transient specification.

## Faults, D101 and F101

**KNOWN D101 [S2 pp1–3]:** bidirectional SMCJ36CA has **36 V standoff**, breakdown **40.0–44.2 V at 1 mA**, maximum test clamp **58.1 V at 25.8 A**; reverse leakage **1 µA maximum at standoff, 25°C**. Pulse rating is **1500 W for the specified nonrepetitive 10/1000 µs waveform**, with derating. Continuous dissipation is **6.5 W only on an infinite heatsink at 50°C**. Typical thermal resistance on the specified footprint is **75 K/W** junction-to-ambient [S2 p3]. “36 V TVS” does not mean it clamps to that voltage.

**At ASSUMED 34 V:** D101 is below standoff and does not intentionally avalanche; leakage remains. It does not clamp that rail, create a crowbar current or cause F101 to clear. Temperature-dependent installed leakage is **OPEN**, not a sustained energy-disposal mechanism.

**At ASSUMED 54.6 V maintained at D101:** this exceeds the room-temperature breakdown maximum, so avalanche current flows. Its magnitude is **OPEN**, set jointly by source impedance/current limit, wiring and the actual TVS I–V/temperature. **CALCULATED** `P = 54.6 × I` gives **54.6 W at ASSUMED 1 A**, **546 W at ASSUMED 10 A**, and **1365 W at ASSUMED 25 A**. Even the first greatly exceeds the infinite-heatsink continuous rating. A crude ambient screen gives **CALCULATED (150−25)/75 = 1.67 W**, using the **KNOWN 150°C** junction limit [S2 p1] and **ASSUMED 25°C ambient/typical datasheet footprint**; this is not an installed-board rating. If source impedance pulls the TVS voltage below the bus, use the actual `VTVS × ITVS` and waveform instead.

**KNOWN F101 [S3 pp3–5]:** exact part is **12.5 A time-lag**, **125 VDC**, **1000 A DC breaking capacity** under footnote 4; typical melting integral **340 A²s at 10 × rated current**. The pre-arcing table specifies:

| CALCULATED current from KNOWN 12.5 A rating | KNOWN pre-arcing behavior [S3 p3] | Consequence |
| --- | --- | --- |
| **15.625 A**, rated multiple **1.25×** | Does not pre-arc for at least **60 min** under specified test conditions. | A substantial continuous TVS current can coexist with an intact fuse. |
| **25 A**, rated multiple **2×** | Pre-arcing maximum **120 s**. | No millisecond clearing guarantee to protect the TVS. |
| **125 A**, rated multiple **10×** | Pre-arcing **10–100 ms**. | Even here, this is not total arcing/clearing time or a TVS survival guarantee. |

**CALCULATED**, only at that high-current test point: `340/125² = 21.76 ms` typical pre-arcing screen, consistent with the table. Do **not** extrapolate `340/I²` to ordinary current, slow overload or a guarantee of clearing. Ambient/copper matter: the fuse's **KNOWN 10/12.5 A** tests use **7.5 mm wide, 140 µm copper** [S3 p5]; V1A has no qualified installed equivalent. The breaking-capacity rating says what fault can be interrupted under test conditions, not that such current exists or that clearance is fast.

**OPEN — exact time until D101 or F101 fails/opens:** neither the source fault current waveform nor TVS transient thermal impedance/failure mode, installed temperature and total fuse clearing curve is established. There is no defensible numerical “fails after X ms” result. The pulse rating is not a failure timer. D101 could be damaged without F101 opening; damage need not be a dependable short circuit. If it fails short, available current and fuse/trace/connector interruption must still be bounded; if open, overvoltage remains. No sacrificial fail-safe behavior is credited.

**Case 1 consequence:** the brief's high-side short defeats the module's normal conversion/current control; do not use its nominal output-current label as a short-circuit limit. U101 itself has voltage headroom, but it cannot disconnect D101. Before main cutoff completes, unbounded pass-through can exceed the buck/input-capacitor ratings. Main buck regulation/output-protection behavior after an absolute-maximum violation cannot be assumed. **NOT SAFE direct**, regardless of the unknown exact destruction time.

**Case 2 actual OVP behavior:** **KNOWN DDR threshold 28.8–33.6 V** [M1 p3]; **KNOWN RSD threshold 27.6–32.4 V** [M2 p1]. Both shut down and require input power cycling to recover. Their overload modes differ from OVP; neither source specifies an OVP hiccup clamp. These are threshold ranges, not guaranteed fault peaks or continuous clamped rails. **OPEN:** threshold-to-energy-interruption delay, overshoot, stored output energy, subsequent discharge and behavior for the relevant component fault.

For a slow rise, **CALCULATED** maximum U101 initial threshold **28.289 V** is below DDR's minimum **28.8 V**, so U101 can trip first (temperature screen remains lower at **28.432 V**). RSD's low threshold **27.6 V** overlaps U101's window, so either can act first. For a fast step, threshold ordering does not establish voltage containment. With an independently guaranteed **ASSUMED ≤34 V total peak**, even temporary passage to U201 remains below its **KNOWN 36 V** operating ceiling; sustained input overvoltage is then cut off without requiring TVS/fuse action. This is why isolated direct feed is plausible. The datasheets alone do not supply that guarantee.

**Add-on decision:** an added TVS/fuse alone is not a qualified repair for a persistent converter fault. For example, **KNOWN SMCJ24CA** is **24 V standoff** but clamps at up to **38.9 V at 38.6 A** [S2 p2], above the buck's normal input ceiling and still subject to continuous heating; it also has no normal-ripple headroom at a high-tolerance nominal source. It cannot earn a “safe with cheap add-on” verdict. An external, rated series surge stopper/disconnector upstream of **all** V1A branches could be engineered, but its full circuit, MOSFET SOA, threshold/let-through and thermal/fuse coordination would require another review. **OPEN part/qualified assembly/cost; no VND price invented.** The existing U316 protects only the auxiliary branch and is not that add-on.

## Buck thermal screen at the required load

This section applies to both module cases while their output is **ASSUMED 24 V**. **KNOWN [S4 p6]:** R201's setting gives **360/400/440 kHz** minimum/typical/maximum under the specified RT test; switch resistances are **41/21 mΩ typical**, **82/45 mΩ maximum** high/low side. **KNOWN [S5 p1]:** current L201 is **10 µH ±20%**, DCR **0.62 mΩ ±10% at 20°C**; its large quoted current capability is not the installed thermal rating.

**CALCULATED** `Pout = 5.065041 × 5 = 25.325 W`. The following use ideal duty `D = Vout/Vin`, `ΔIL = (Vin−Vout)D/(L fsw)`, and `Irms² = Iout² + ΔIL²/12`. Input values are **ASSUMED 5 A DC, nominal L and 400 kHz**, with the captured nominal output.

| Quantity | CALCULATED at ASSUMED 12 V comparison | CALCULATED at ASSUMED 24 V direct |
| --- | ---: | ---: |
| Duty | **0.42209** | **0.21104** |
| Inductor ripple / peak / RMS | **0.732 A p-p / 5.366 A / 5.004 A** | **0.999 A p-p / 5.500 A / 5.008 A** |
| IC conduction using typical RDS | **0.737 W** | **0.633 W** |
| IC conduction using maximum RDS | **1.518 W** | **1.325 W** |
| Switching overlap, ASSUMED aggregate rise+fall **10 ns** | **0.120 W** | **0.240 W** |
| Partial IC loss, typical conduction + assumed overlap | **0.857 W** | **0.873 W** |
| Inductor copper loss at KNOWN maximum room-temperature DCR | **0.0171 W** | **0.0171 W** |

**CALCULATED** low-L/low-frequency screen at the higher input, holding output nominal: **1.388 A p-p / 5.694 A peak**, using **KNOWN −20% inductance** and **360 kHz**. DC-bias/temperature/core-loss behavior remains **OPEN**. The loss equations are `Pcond = Irms²[D RHS + (1−D)RLS]` and `Ptransition ≈ ½Vin Iout (tr+tf) fsw`. Increased low-side duty reduces conduction loss; input doubling does not double total heat. **OPEN:** hot magnetic loss, transition duration, recovery/dead-time, switching node ringing, gate-drive/control/LDO losses, capacitor ESR and PCB losses.

**KNOWN typical evidence [S4 p35, Fig9-11/12]:** reference application efficiency curves for **5 V / 400 kHz** include **24 V** input. **ASSUMED coarse graph-reading interval at 5 A: 93.5–94.5%**; not a guaranteed efficiency range for V1A. At the captured output this gives **CALCULATED whole-buck loss 1.47–1.76 W**, input **1.117–1.129 A**. A separate **ASSUMED 90%** sensitivity gives **CALCULATED 2.814 W / 1.172 A**. The reference circuit differs in L/C/layout/bias.

**KNOWN [S4 pp16, 32]:** external BIAS can reduce internal LDO loss; current capture grounds BIAS. Therefore those efficiency curves cannot establish actual V1A heat. The extra bias-supply penalty depends on switching LDO current (**OPEN**); with an illustrative **ASSUMED 10 mA**, sourcing it from input rather than the output costs **CALCULATED (24−5.065)×0.01 = 0.189 W**. This is a sensitivity, not a measured or guaranteed correction. No BIAS change is proposed for implementation in this task.

**KNOWN [S4 p5]:** thermal resistance examples **25 K/W on the EVM**, **58.7 K/W JEDEC**, with an explicit warning against universal design use. Using the incomplete **CALCULATED 0.873 W** IC screen would imply **CALCULATED 21.8 K / 51.2 K** rises if those thermal environments transferred (**ASSUMED**, not established). Neither is an upper bound. Whole-buck loss includes external parts and cannot simply be assigned to the IC junction. **OPEN:** final IC dissipation, ambient, copper/airflow/enclosure, auxiliary heat and operating thermal margin to **KNOWN 150°C** junction limit [S4 p4]. **DECISION:** nominal conversion at the higher input is plausible; **5 A continuous thermal capability is not validated** for either source case.

The updated inductor's low DC loss does not prove small core loss at the switching frequency. Input-capacitor effective capacitance/ripple heating and loop stability with current L/C require review. Upstream filter/harness interaction, return-current paths, local decoupling and switching-loop geometry remain layout/bench issues. The documented source current estimate excludes auxiliary startup and faults; it does not alter connector, fuse, copper or frozen low-input current requirements.

## Required evidence and handback

**OPEN closure before a direct-feed approval:** obtain an authenticated UENPO specification if reconsidering it; for a selected isolated source, bound the complete secondary fault waveform at V1A and confirm relevant isolation/failure assumptions. Verify normal setting, load-release/startup overshoot and recovery over the actual temperature/input/load/harness envelope. Credit neither an isolation withstand test nor an OVP threshold as a fault peak guarantee. No direct bus pass-through is added to V1A's envelope.

**KNOWN project process:** first hardware use proceeds through visual/continuity checks, current-limited bench supply, no-load startup and rail verification, then dummy-load steps, thermal/ripple/transient tests, fault/protection and telemetry validation. SBC integration follows the preceding gates only. Source-ground/chassis/communications bonds and backfeed paths must be included in the interface review. No physical test was run here.

**EVIDENCE:** [reproduction script](direct_24v_feed/calculate.py), [CALCULATIONS.json](direct_24v_feed/CALCULATIONS.json), and [validation record](direct_24v_feed/VALIDATION.json). Run `python3 -B docs/evidence/r2/direct_24v_feed/calculate.py`; it writes only stdout. A fresh read-only netlist export was used to reconcile actual R203/L201 and branch connectivity. The module specification tables and TI efficiency plot were visually inspected. Documentation/numeric/source checks and Git handback are recorded in the manager report. ERC/DRC were not rerun because no schematic/PCB was changed; prior rule-check results are not reused as safety evidence. The existing repository checker returns FAIL for unchanged R203/Gate4B preservation mismatches and its existing-PCB scope guard; these were recorded, not repaired or suppressed in this analysis-only task.

**Git handback:** the authorized local commit stopped at `git add`: `index.lock` creation returned `Operation not permitted` (exit 128). Per the brief, these changes remain **uncommitted**; nothing pushed. See [attempt log](direct_24v_feed/git_commit.log).
