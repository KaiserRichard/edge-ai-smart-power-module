# Input protection review

Date: 2026-09-12. **REVIEW DRAFT — ENGINEERING REVIEW REQUIRED.**

SOURCE: [TI TPS2663 SLVSE94G](https://www.ti.com/lit/ds/symlink/tps2663.pdf),
pin table, Fig 8-7 and sections 8/9; SLVUBI8A Fig 11. FUNCTION: input fuse/TVS,
reverse-polarity and reverse-current blocking, UVLO, OVP cutoff, current limiting
and controlled startup. U101 is **TPS26630RGER**, not a fixed-clamp variant or
TPS26631 with doubled pulse allowance. RGE0024H has 24 pins plus ground pad 25.

MODIFICATION: separate UV/OV dividers for transparent threshold calculation;
lower input window, 4.02k ILIM, 100 nF dVdT, latch fault mode, smaller input bank,
no EVM LEDs/configuration jumpers. RATIONALE: support normal 9-24 V and 25.5 W
without importing the EVM's hold-up or pulse-current assumptions.

## Current path and external devices

VIN_RAW → F101 → VIN_FUSED (D101 bidirectional TVS to GND) → Q101 →
VIN_EFUSE_IN → U101 → VIN_PROTECTED. C101/C102 are 1 uF/100 V specification
placeholders with exact MPN/effective capacitance OPEN. D102 B260-13-F has cathode
at VIN_PROTECTED and anode at GND to limit negative output excursions; it is
not a load-current series diode. Its nominal 0.7 V forward rating does not by
itself prove the IC's negative pin limit is respected during an inductive event.

Q101 **CSD19537Q3**: sources 1/2/3 to VIN_FUSED, gate 4 to B_GATE, drains 5/6/7/8
to VIN_EFUSE_IN. The body diode points from source/input toward eFuse IN.
Q102 **onsemi BSS138**: gate 1 to DRV, source 2 to VIN_FUSED, drain 3 to B_GATE.
It rapidly discharges Q101's gate relative to **Q101 source**, not system ground.
These are the two devices required by Fig 8-7. The eFuse alone does not provide
this reverse-input function. PDF text extraction scrambles Q101's visual pin
order; Fig 3-1 was checked visually and controls the pin map.

Q101 has 100 V VDS and +/-20 V VGS limits. TI B_GATE-source clamp is 8.3-14 V;
use 16.6 mOhm maximum at 6 V gate drive for conservative 25 C conduction screening,
not a threshold-voltage resistance. At 9 V/90% module efficiency, Iin=3.148 A;
Q101 loss is approximately **0.165 W**. U101 at its 53 mOhm full-temperature bound
adds **0.525 W**. Hot Q101 resistance, fuse, TVS leakage, copper and connectors
add losses. U101's 31 mOhm headline is typical, not the worst-case thermal budget.

## Calculated thresholds and startup

Equation: Vtrip=Vref(1+Rtop/Rbottom)+Ileak Rtop. Bounds below include independent
0.1% resistor extremes and +/-150 nA input leakage. No source tolerance or cable
drop is silently added to the frozen connector range.

| Function | Rtop / Rbottom | Nominal rising | Rising bounds | Falling bounds |
| --- | --- | ---: | ---: | ---: |
| UVLO | 332k / 54.9k | 8.457 V | 8.224-8.691 V | 7.619-8.168 V |
| OVP cutoff | 348k / 15.8k | 27.630 V | 26.974-28.289 V | 24.997-26.582 V |
| PGTH | 56.2k / 10k | 7.944 V | 7.763-8.125 V | 7.195-7.634 V |

Thus 9 V can start and 24 V is below the earliest OV trip; returning to 24 V
after an OV fault is below even the minimum falling threshold. These are design
settings, not new normal operating requirements. UV/OV top resistors exceed
300k, limiting reverse-input injection as TI directs. Resistors at these boundary
nodes require 75 V working-voltage qualification; package size alone is insufficient.

RILIM=4.02k gives **4.478 A**, about **4.160-4.796 A** using +/-7% controller
and 0.1% resistor screening. At 9 V/85% efficiency the required current is about
3.333 A, below the screened minimum. Startup load and fault coordination still
need review. This is input current limit, not a 5 A output current regulator.

CdVdT=100 nF gives dV/dt≈25 x 2 uA/C = 500 V/s and a 24 V ramp of **48 ms**.
Using TI gain/current bounds and +/-10% C gives **37.3-63.3 ms**. Charging the
44 uF buck input bank consumes about **22 mA**, or 34 mA using its +20% nominal
capacitance and the fastest ramp. This calculation covers that bank only.
Local/input/stray capacitors and source hot-plug inrush before the eFuse are separate.

PGOOD asserts only after the internal pass FET is enhanced and PGTH is valid;
it drives the buck's 100k/24.9k EN divider midpoint. The divider alone reaches
about 1.60 V at 8 V, above the 1.326 V maximum rising EN threshold (1.263 V typical +5%). A 130 Ohm
worst-case PGOOD sink holds it near 31 mV even at 24 V. No pull-up comes from
the host or another supply domain. The resulting two-stage startup includes
the buck's 3.5-7 ms soft-start to 90%; actual load capacitance remains unspecified.

MODE is deliberately open for **latched overload/thermal-fault response**.
SHDN uses its internal pull-up and has local test access; grounding then releasing
it resets a latch. UV/OV recovery is comparator/hysteresis controlled; MODE does
not make every event latch. FLT pull-up is to protected input and is **not host-safe**.
The drawing's NC markers on MODE mean intentional floating per TI, not omission.

## SOA, surge and unresolved coordination

Q101 is a blocking switch; U101's internal MOSFET controls the large voltage drop
during startup. At normal conduction Q101 is low-VDS; its 50 A package headline
does not justify linear-mode operation. Reviewed SLPS549B Fig 5-10/thermal curves:
high-VDS, millisecond current capability is much lower. Maximum 21 nC charge at
minimum 16 uA drive suggests about 1.31 ms charging as a screening estimate;
this does not bound every turn-on trajectory or gate-charge condition.

OPEN: final Q101 SOA closure requires initial capacitor states, hot case
temperature, source impedance, reverse-fault duration and switching waveforms.
U101 thermal regulation is a protection mechanism, not a normal operating target.
Do not apply an assumed 24 V x 4.8 A linear stress to Q101 and declare it safe.

D101 **SMBJ26CA is a candidate only**: manufacturer search evidence identifies
26 V stand-off and 42.1 V clamp at 14.3 A. The exact source revision, pulse profile,
energy, derating and fuse coordination remain OPEN. It is explicitly **not** a
26 V clamp. Its clamp exceeds LM61460's 42 V absolute maximum, so the TVS alone
cannot protect the buck; eFuse cutoff timing/let-through and downstream capacitance
must be proven against a specified surge. Normal 24 V operation does not define
the surge test. No IEC compliance is claimed.

F101 is an unselected **5 A candidate specification**, not an orderable fuse.
Required closure: source prospective short current, DC interrupt rating, fuse
I²t versus TVS/copper/MOSFET stresses, hot current derating and adapter foldback.
J501's connector, mating part and wire are also OPEN. The input block is captured
for engineering review; these omissions prevent an R2 release.
