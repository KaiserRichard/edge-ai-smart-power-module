# Task 4 — option I candidates and conditional budgets

2026-09-29. **Candidates only; no selection or schematic capture. R2/R3 BLOCKED.
NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Evidence boundary

The continuation permits network access only for the Task 1 manufacturer sources.
No candidate datasheet beyond those sources is cached in this worktree. The links
below are manufacturer datasheet lookup targets, **not fetched or URL-verified**.
Candidate identity/suitability is **INFERRED** for investigation; all missing
specifications, ordering suffixes, revisions, footprints and worst-case limits
remain **UNKNOWN**. This is a shortlist and a purchasing-free review worksheet,
not a completed component qualification. No third-party design was inspected,
adapted or copied from these unfetched documents. License and exact attribution
requirements are UNKNOWN until supplied; preserve manufacturer notices and record
revision/hash in the source register before relying on a candidate.

Every electrical number in a table inherits that cell's label. Package/part names,
document identifiers and dates are identifiers. An ASSUMED allocation is a proposed
requirement on a future part, never a claim about the linked part.

## Candidate worksheet

| Block | Candidate and manufacturer datasheet target | Key values / error or timing checks | Footprint and height |
| --- | --- | --- | --- |
| Bulk | Nichicon PCH polymer series, [PCH datasheet target](https://www.nichicon.co.jp/english/products/pdfs/e-pch.pdf) | UNKNOWN exact rated-voltage/capacitance SKU, capacitance tolerance, effective minimum, ESR over temperature/frequency, ripple current, life and surge limit. Screen a bank against ASSUMED ≥35 V rating and ≥470 µF effective at ASSUMED 5.1 V; see bank calculation below. | UNKNOWN exact footprint, pitch, diameter and height until SKU selected; do not allocate guessed dimensions. |
| Bulk | Nichicon PCX polymer series, [PCX datasheet target](https://www.nichicon.co.jp/english/products/pdfs/e-pcx.pdf) | UNKNOWN same fields as PCH; independently verify that the series actually offers a suitable ≥35 V part. Neither series is asserted compliant. ASSUMED baseline bank ESR 20 mΩ; not a candidate measurement/specification. | UNKNOWN exact footprint and height; reserve only after drawing review. |
| Reference | TI REF3325, [REF33xx datasheet target](https://www.ti.com/lit/ds/symlink/ref33xx.pdf) | INFERRED nominal reference candidate 2.5 V. UNKNOWN initial error, maximum temperature coefficient, dropout/headroom at detector supply, line/load regulation, noise and startup. Must satisfy the tighter ASSUMED allocations below, not merely the brief's ASSUMED ≤0.5% initial-error ceiling. | INFERRED small-outline package family; UNKNOWN ordering suffix and exact land dimensions. |
| Reference | TI REF5025, [REF50xx datasheet target](https://www.ti.com/lit/ds/symlink/ref50xx.pdf) | INFERRED nominal reference candidate 2.5 V. UNKNOWN same limits, grade and supply headroom; reject if required input headroom exceeds ASSUMED 3.3 V supply at tolerance. | UNKNOWN exact package choice, land area and height. |
| Comparator | TI TLV3501, [datasheet target](https://www.ti.com/lit/ds/symlink/tlv3501.pdf) | INFERRED push-pull high-speed comparator candidate. UNKNOWN guaranteed delay at ASSUMED 10 mV overdrive, offset, input bias/leakage, common-mode range, hysteresis, supply range and behavior when unpowered. Required ASSUMED ≤100 ns at ASSUMED 3.3 V, over temperature and output loading. | INFERRED small-outline family; UNKNOWN exact ordering suffix, footprint and height. |
| Comparator | TI TLV3601, [datasheet target](https://www.ti.com/lit/ds/symlink/tlv3601.pdf) | INFERRED push-pull comparator candidate; same UNKNOWN limits and same ASSUMED delay/supply constraints. Typical headline speed alone cannot qualify it. | UNKNOWN exact package/land dimensions and height. |
| Detector supply | TI TPS70933DBVR, [TPS709 datasheet target](https://www.ti.com/lit/ds/symlink/tps709.pdf) | KNOWN inherited repository evidence: input operating maximum 30 V, nominal output 3.3 V; original source identity SBVS186H in `third_party/README.md`. UNKNOWN freshly verified startup, dropout, accuracy, thermal and UVLO limits. CALCULATED headroom to ASSUMED 28.3 V fault hold is only 1.7 V; transient overshoot remains UNKNOWN. Use an additional raw-fed detector supply, not existing U402 fed by protected output. | KNOWN inherited SOT-23-5 DBV, lead pitch 0.95 mm. UNKNOWN independently checked land area/height for a new placement. |
| Detector supply | TI TPS7A1633, [TPS7A16 datasheet target](https://www.ti.com/lit/ds/symlink/tps7a16.pdf) | INFERRED high-voltage fixed-output candidate. UNKNOWN input operating/absolute limit, output grade, current, dropout, quiescent current, startup and thermal limits; must verify ASSUMED ≥30 V operating input and valid detector before path enable. | UNKNOWN ordering/package suffix and land dimensions. |
| Latch | TI SN74LVC1G74, [datasheet target](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf) | INFERRED flip-flop with asynchronous fault-set candidate. UNKNOWN supply range, asynchronous priority, power-up state, max set delay, leakage and partial-power behavior. Proposed connection: fault to asynchronous set, reset only from detector-supply UVLO, no functional clock/retry path. External UVLO/supply-valid logic still required. | UNKNOWN exact package, footprint and height. |
| Latch | TI SN74LVC2G02, [datasheet target](https://www.ti.com/lit/ds/symlink/sn74lvc2g02.pdf) | INFERRED cross-coupled NOR latch candidate. UNKNOWN guaranteed logic/delay/power-up behavior. Simultaneous set/reset and slow power ramps need explicit truth-table review; supply UVLO is the sole permitted reset cause. An ordinary comparator's modest hysteresis alone is not a persistent latch. | UNKNOWN exact package, footprint and height. |
| Gate stage | Nexperia MMBT3904 + MMBT3906 bipolar level-shift/local-clamp concept, [NPN target](https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf), [PNP target](https://assets.nexperia.com/documents/data-sheet/MMBT3906.pdf) | INFERRED candidate devices only. UNKNOWN voltage rating sufficiency, pulsed SOA, gain at required sink, leakage, saturation/storage and drive loading. A simple ground-referenced gate shunt is rejected. A floating OUT-referenced stage with an independent final gate-to-OUT hold is required; no complete circuit is claimed. | INFERRED SOT-23 families; UNKNOWN combined footprint with level shift, clamp, drive and hold resistors. |
| Gate stage | Nexperia 2N7002 local gate-to-OUT shunt plus source-referenced level-shift driver, [datasheet target](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf) | INFERRED topology/device candidate only. UNKNOWN current at available drive, off leakage, voltage rating, SOA, driver delay and positive bias supply. Its source would be OUT and drain HGATE; drive must be relative to OUT. A ground-powered logic output cannot directly drive this arrangement across power states. | INFERRED SOT-23 shunt; UNKNOWN complete-stage footprint/height. |

This supplies alternative leads for each requested block but **does not fulfill the
requested verified key-number/footprint comparison**. The user/conductor must
provide the listed manufacturer datasheets, exact grades/SKUs and drawings for
completion; they were not attempted as downloads, and are distinct from Task 1's
recorded HTTP failures.

## Bulk minimum and supply budget

ASSUMED design targets: rating ≥35 V; effective minimum ≥470 µF at 5.1 V, including
initial tolerance, operating temperature, life and frequency. A nominal 470 µF part
is not a guaranteed 470 µF minimum. CALCULATED with **ASSUMED −20% tolerance only**:

- One nominal 470 µF part gives 376 µF: fails the proposed minimum.
- One nominal 680 µF part gives 544 µF: conditional candidate configuration.
- Two nominal 330 µF parts give 528 µF total: conditional candidate configuration.

These are configurations to look up, not claims that either series offers them.
Additional temperature/life reduction must fit the residual capacitance margin.
For two identical branches, CALCULATED ESR is half the individual ESR, conditional
on matched parts/interconnects; current sharing and ripple heating still need review.
The model's ASSUMED 20 mΩ bank value is not established by these configurations.
KNOWN TI Table 9-4 uses a 100 mΩ electrolytic branch: stability cannot be transferred
to this different network. Exact ripple-current requirement is UNKNOWN until the
switching waveform and bank current split are known.

CALCULATED LDO dissipation formula: `(Vraw − Vdet) × Idet + Vraw × Iq`.
For ASSUMED Vraw=28.3 V, Vdet=3.3 V and Idet=5 mA, the load term is 125 mW.
At ASSUMED Idet=10 mA it is 250 mW. Neither current is a candidate specification;
reference/comparator/latch/driver demand and package thermal impedance are UNKNOWN.
PGOOD must be ANDed with a fail-off detector-valid condition after LDO/reference
settling; PGOOD alone says nothing about detector readiness. KNOWN captured state: U201.PGOOD is
currently unconnected; the existing `BUCK_INPUT_PGOOD` is U101.PGOOD driving U201.EN/SYNC,
not the proposed buck-output power-good signal. Use a bounded detector-domain pullup
for future U201.PGOOD; KNOWN its absolute pin limit is 20 V, below the raw fault hold.

## Window allocation: feasibility arithmetic, not a proven part budget

ASSUMED nominal reference 2.5 V, nominal rising trip 5.40 V. CALCULATED divider
ratio `Rtop/Rbottom = 5.40/2.5 − 1 = 1.16`, sense gain `k = 1/2.16`.
ASSUMED illustrative resistors 11.6 kΩ and 10.0 kΩ, each ±0.05% initial tolerance.
These are numerical design inputs; no resistor series is selected.

| Contribution | ASSUMED maximum allocation / condition | CALCULATED raw-trip relative error |
| --- | --- | --- |
| Reference initial | ±0.20% grade required | ±0.200% |
| Reference temperature | 10 ppm/°C maximum over 100 °C excursion | ±0.100% |
| Divider initial | ±0.05% each; opposite tolerance extremes | ±0.054% rounded outward |
| Divider ratio drift | 5 ppm/°C mismatch over 100 °C | ±0.027% rounded outward |
| Comparator offset, including drift | ±3 mV at sense input | ±0.120% |
| Input leakage/bias and PCB leakage | total equivalent trip error allocation | ±0.050% |
| Reference line/load/noise and supply effects | total allocation | ±0.050% |
| Hysteresis rising-threshold uncertainty | after solving feedback network in untripped state | ±0.050% |
| Multiplicative interactions / rounding reserve | must be checked with final exact equations | ±0.020% |
| **Static total** | worst-case sum, no root-sum-square reduction | **±0.671%** |

CALCULATED conditional static window: **5.363766–5.436234 V**. The required
ASSUMED ±1.1% window at 5.40 V is CALCULATED **5.3406–5.4594 V**. Conditional
arithmetic fits, but every unverified part allocation prevents a worst-case PASS.
The ASSUMED 100 °C component-temperature excursion is a screening allocation,
not a newly imposed project environmental requirement.

ASSUMED hysteresis target ≥50 mV referred to raw requires CALCULATED ≥23.148 mV
at the sense input. Positive feedback changes the rising trip as well as the
falling trip: solve both states with output swing/tolerance and resistor errors.
For comparator output feedback through `Rh`, CALCULATED equations are
`beta=Rtop/Rh`, `Vrise=Vref*(1+Rtop/Rbottom+beta)-VOL*beta`, and
`Vfall=Vref*(1+Rtop/Rbottom+beta)-VOH*beta`. With ASSUMED ideal output levels
0 V/3.3 V, CALCULATED beta=0.0151515 produces exactly 50 mV hysteresis;
CALCULATED Rtop/Rbottom=1.1448485 then restores the 5.40 V rising threshold.
This is not a guaranteed minimum-hysteresis circuit because real output swing
and resistor variation are UNKNOWN. Recalculate the complete divider/error network.
Do not add an unaccounted half-hysteresis to the rising threshold. The latch,
not hysteresis alone, maintains shutdown after raw voltage returns to normal.

A comparator delay specified at ASSUMED 10 mV overdrive requires CALCULATED
21.6 mV extra raw voltage (0.4% of nominal trip). Adding that to the static
high corner gives CALCULATED **5.457834 V**, only CALCULATED 1.566 mV below
the proposed high window edge. This demonstrates how little margin remains;
it does **not** establish delay at zero overdrive. Time to accumulate overdrive
is UNKNOWN without a raw slew bound and delay-versus-overdrive data. Include
that latency once, either in a justified effective trip threshold or in the
trip-to-isolation timing definition, and use the same definition in both models.

The same divider maps ASSUMED raw fault levels 24.72 V and 28.3 V to CALCULATED
11.4444 V and 13.1019 V at the comparator input. A comparator powered at ASSUMED
3.3 V requires proven beyond-rail tolerance or an additional input protection
network. Clamp leakage belongs in the error allocation, and clamp injection must
not back-power the detector supply or inhibit its UVLO reset. Divider dissipation,
resistor voltage limits and comparator overdrive recovery also need verification.
The divider values above therefore are not a complete usable detector circuit.

## Timing allocation and pull-down constraints

KNOWN LM74800 opposing HGATE source maximum is **75 µA**, not its typical 55 µA.
ASSUMED Q302 total gate charge is **96 nC**: the Nexperia source is unavailable,
and this is not a guaranteed maximum across drain voltage, current and temperature.
CALCULATED minimum average sink for ASSUMED 1.6 µs discharge:
`96 nC / 1.6 µs + 75 µA = 60.075 mA`.
A peak-current specification alone cannot meet this integral requirement.

| Stage | ASSUMED maximum allocation | Unclosed evidence |
| --- | --- | --- |
| Sense settling / sufficient overdrive | 0.10 µs | UNKNOWN input network, slew and delay near zero overdrive |
| Comparator | 0.10 µs | UNKNOWN guaranteed limit at required overdrive/load/supply/temperature |
| Latch plus level-shift command | 0.10 µs | UNKNOWN propagation and supply-state behavior |
| Gate-stage activation | 0.10 µs | UNKNOWN switching/storage and source-referenced bias |
| Gate discharge plus isolation endpoint | 1.50 µs | UNKNOWN maximum charge, Miller current, residual conduction and transient voltage |
| Contingency | 0.10 µs | Unallocated reserve |
| **Total** | **2.00 µs** | **Not a verified worst-case budget** |

The gate-stage activation plus discharge allocation is ASSUMED 1.60 µs. At an
ASSUMED guaranteed 80 mA average sink, CALCULATED idealized charge time is
`96 nC / (80 mA − 75 µA) = 1.20113 µs`, leaving CALCULATED 0.29887 µs of the
discharge allocation for Miller/tail/end-point effects. Whether any listed stage
provides that current throughout turnoff is UNKNOWN; instantaneous `Qg/Ipeak`
cannot prove isolation. Qualification must define off-current and drain-voltage
endpoints and verify Q302 SOA and the whole path, not only gate movement.

The final hold must oppose KNOWN 75 µA while keeping VGS below the MOSFET's
**UNKNOWN** guaranteed off threshold. CALCULATED a hypothetical 1 kΩ local hold
would develop 75 mV; such a resistor permanently across gate/source would draw
CALCULATED 10–14.5 mA at KNOWN 10–14.5 V HGATE drive, grossly exceeding the
ASSUMED ≤1 µA idle-load requirement. It must be switched with verified hot leakage.

HGATE absolute minimum is KNOWN OUT−0.3 V. A ground-referenced pull-down violates
that when OUT is positive. Even a PNP emitter-at-HGATE/collector-at-OUT circuit can
remove gate charge through its base toward ground if its base is pulled below OUT;
its collector connection alone does not prove the limit. The candidate stage must
reference both the active sink and final hold to OUT, prevent other ground-return
paths, and constrain inductive undershoot. A diode named “Schottky” does not prove
a ≤0.3 V clamp across current and temperature. Startup, load backfeed, detector
brownout and raw fault-hold states all require this check.

## Latch and power-state contract

1. ASSUMED proposed behavior: supply invalid or reference unsettled forces path disabled.
2. ASSUMED proposed behavior: detector valid AND BUCK_PGOOD AND no latched fault permits enable.
3. ASSUMED proposed behavior: any detector trip sets fault asynchronously; PGOOD toggling, buck
   hiccup and the raw rail returning to regulation do not clear it.
4. ASSUMED proposed behavior: only detector supply crossing its falling UVLO may clear the latch;
   after reset the path remains disabled until supply/reference validity is re-established.
5. UNKNOWN policy conflict: raw-fed detector supply may cross UVLO during upstream eFuse/buck
   interruptions while the external input remains present. Therefore “reset only at detector UVLO”
   does not by itself prove “no re-enable while input is present.” A demonstrated hold-up bound,
   upstream power-presence interlock, or revised reset policy needs conductor/user review.

**Task 4 result: incomplete qualification; criterion 3 FAIL to demonstrate.** The
conditional allocations fit arithmetically, but verified component limits, footprint
comparison, a complete pull-down circuit and power-state proof are missing. These
are explicit hand-back items, not reasons to promote assumed numbers to KNOWN.

## Continuation review and Task 4 hand-off

KNOWN review outcome: independently rechecked the static error sum, conditional
window, positive-feedback equations, capacitance-tolerance arithmetic and
charge-removal arithmetic. These are consistent with their labelled assumptions.
The feedback equations assume sense-node positive feedback with the comparator
output low before trip and high after trip; opposite polarity requires a different
connection and equations. No candidate source was fetched outside the permitted
Task 1 list, and no verified footprint or part rating was invented to fill a gap.

DECISION: finish this task's permitted documentary work and hand back the explicit
qualification gaps. The requested verified component comparison and guaranteed
budgets remain BLOCKED on manufacturer documents and a complete circuit. Continue
to the authorized open-model preparation; do not wait for missing vendor tools or
treat these conditional allocations as selected component specifications.
Fresh pre-commit checks are retained in `validation/02_candidates_takeover/`;
the earlier worker's `validation/02_candidates/` records are preserved.
