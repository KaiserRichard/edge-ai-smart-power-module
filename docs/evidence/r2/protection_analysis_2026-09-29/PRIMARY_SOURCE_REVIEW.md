# Task 1 primary-source review

Date: 2026-09-29. **R2 BLOCKED; R3 BLOCKED. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
This is evidence for conductor review, not an architecture selection. All electrical numbers
below carry a classification. Document/page identifiers and dates are identifiers, not electrical results.

## Acquisition and visual method

The [source register](source_register.json) records URLs, exact downloaded-byte hashes,
revisions, rights, use, and failures. Originals are unmodified in the ignored local archive
`third_party/documents/r2_protection/`, consistent with the repository's vendor-cache policy.
The tracked register preserves their identities for review and later restoration.
No source outside the brief's Task 1 manufacturer list was fetched.

KNOWN acquisition: TI LM7480-Q1, TPS2663, LM61460 and Vishay SMBJ downloaded successfully.
Coilcraft XAL8080, TDK C5750X7R1H226M250KB characterization, and Nexperia PSMN1R8-40YLC
each returned HTTP 403. Please download those exact manufacturer documents in a browser
and provide the original bytes, including revision pages. No replacement values are inferred
from unsuccessful downloads or distributor material.

Native macOS PDFKit extracted text and rendered selected original pages; reviewers then viewed
the rendered images. No software was installed. Text extraction alone did not establish column alignment.
LM7480-Q1 pages 4, 6, 7 and 8 were visually reviewed here. The companion
[TPS2663 review](TPS2663_SOURCE_REVIEW.md) and [buck/TVS review](BUCK_TVS_SOURCE_REVIEW.md)
identify their own visual pages and findings. Local renders are scratch derivatives; primary
PDF bytes and source hashes are the retained source identities.

## LM7480-Q1 — SNOSD95C, revised December 2020

Source: [TI original](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf).
KNOWN conditions for the switching table: junction temperature −40 to +125 °C, typical at
25 °C; supply/anode/cathode/output at 12 V, V_AC = 20 mV, charge-pump capacitor 0.1 µF,
EN/UVLO = 2 V unless the row overrides a condition. These are source test conditions,
not demonstrated V1A operating conditions.

| Parameter and page | KNOWN MIN | KNOWN TYP | KNOWN MAX | Endpoint / qualification |
| --- | --- | --- | --- | --- |
| LM74800 OV-off deglitch, p7 | unspecified | 3.98 µs | 5.4 µs | OV rising to HGATE falling; not fully isolated load |
| EN-off HGATE deglitch, p7 | 3 µs | 4.6 µs | 6 µs | EN/UVLO falling to HGATE falling |
| EN-off DGATE deglitch, p7 | unspecified | 8.1 µs | unspecified | No worst-case upper bound in this row |
| DGATE reverse turnoff, p6 | unspecified | 0.5 µs | 0.875 µs | V_AC from +30 to −100 mV, gate-anode below 1 V, 10 nF load |
| HGATE source current, p6 | 39 µA | 55 µA | 75 µA | Use maximum for opposing pull-down hold current |
| HGATE sink current, p6 | 168 mA | 260 mA | unspecified | OV asserted; not a constant sink waveform to zero gate voltage |
| DGATE peak sink current, p6 | unspecified | 2670 mA | unspecified | V_AC = −12 mV; gate-anode = 11 V; typical only |
| HGATE−OUT drive, p6, 3 V < VS < 5 V | 7 V | unspecified | unspecified | Lower-voltage range has a guaranteed minimum |
| DGATE−A drive, p6, 3 V < VS < 5 V | 7 V | unspecified | unspecified | Same lower-voltage qualification |
| HGATE−OUT drive, p6, 5 V < VS < 65 V | 10 V | 11.1 V | 14.5 V | Does not establish 10 V drive below 5 V |
| DGATE−A drive, p6, 5 V < VS < 65 V | 10 V | 11.5 V | 13 V | Ideal-diode regulation can reduce gate drive |
| HGATE−OUT absolute limits, p4 | −0.3 V | not applicable | 15 V | Absolute limits are not recommended operating targets |

Figure 7-6 on p8 is a KNOWN typical-characteristics plot. Interpolating that graph would be
INFERRED and cannot replace the tabulated minimum or prove a MOSFET on-resistance at low drive.

CALCULATED conditional charge quotient: the brief's **ASSUMED** Qg = 96 nC divided by the
KNOWN 168 mA minimum sink gives approximately 0.571 µs. Nexperia's Qg curve, maximum charge,
drain-voltage/current conditions, temperature dependence, and the complete driver waveform are
UNKNOWN in this session. That quotient is not a guaranteed isolation time. Likewise the
KNOWN 0.875 µs DGATE test uses a capacitor and voltage step; applying it to the full path is ASSUMED.

## Missing passive and MOSFET evidence

| Requested source | Still UNKNOWN from fresh primary bytes | Model consequence |
| --- | --- | --- |
| Coilcraft XAL8080-682 | L tolerance; maximum DCR; saturation currents at 10/20/30% reduction and test temperature | Retain ASSUMED 14 A discontinuous saturation knee and ASSUMED 0.7 post-knee ratio; nominal 6.8 µH and calculated 14.6 mΩ retain inherited provenance, not newly verified bounds |
| TDK exact characterization | C(V) at 5.1 V and 24 V; curve revision and test conditions | Retain ASSUMED Cin 15–40 µF and Craw 60–130 µF. Even a typical curve would require tolerance, temperature and aging to establish a minimum |
| Nexperia exact MOSFET | RDS(on) versus VGS/Tj; Qg conditions and maxima; SOA | Retain ASSUMED 3.25 mΩ hot path resistance and ASSUMED 96 nC charge for screening pending primary review; no worst-case timing or SOA closure |

The older forensic review records a typical saturation-current observation, but it does not
substitute for the requested newly archived, visually reviewed manufacturer curve. A current
at a specified inductance reduction is not automatically the onset of a step discontinuity.

## Corrections to the predecessor analysis

- KNOWN: the ambiguous OV row is resolved; the prior numerical choice of 5.4 µs remains the
  maximum, so resolving the column alone does not change the Python waveform.
- KNOWN: gate drive below 5 V is not wholly UNKNOWN: the table gives a 7 V minimum in the
  stated range. RDS(on) qualification at that drive remains UNKNOWN here.
- KNOWN: 55 µA is typical HGATE source current; 75 µA is the maximum hold-off design input.
- CALCULATED: Qg / sink is only a charge estimate, not a guaranteed switch turnoff bound.
- The companion reviews record additional buck and eFuse qualifications and any contradictions.

DECISION: source acquisition is complete to the permitted download attempts; missing data remain
OPEN. Proceed with explicit assumptions and NOT RUN simulation records as directed by the user.

## Continuation review before the Task 1 commit

KNOWN: the replacement worker rechecked all downloaded-file SHA-256 hashes and byte counts
against the register, visually rechecked LM7480-Q1 pages 4, 6, 7 and 8, and independently
reviewed the TPS2663 and buck/TVS extractions against the archived pages. No material
numeric extraction error was found. The FLT endpoint wording was clarified to mean its
fall to 10% of the high level. Acquisition attempts and earlier validation logs are inherited
evidence from the preceding worker; no new download or installation was needed. Fresh
pre-commit command results are in `validation/01_sources_takeover/`.
