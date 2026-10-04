> Context note (2026-09-26): this dated document preserves earlier requirements/review history. Read [current engineering state](context/03_ENGINEERING_STATE.md) and [current architecture](context/02_V1A_ARCHITECTURE.md) before interpreting selections or release claims. Local cache/scratch paths mentioned below are archived external evidence; see [reference restoration](../third_party/README.md).

# R2 manager packet — V1A schematic review

2026-09-12 | HEAD `a9fe716` + uncommitted R2 work | **STATUS: BLOCKED**

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED. R3 BLOCKED.**

## 1. Schematic block diagram

```text
VIN_RAW -> fuse/TVS -> TPS26630 + reverse FETs -> VIN_PROTECTED
         -> LM61460 -> VOUT_5V1 -> [OPEN output disconnect; no bypass]
         -> VOUT_PROTECTED -> 2 mOhm Kelvin shunt -> LOAD_5V1
VOUT_PROTECTED -> local 3.3 V -> INA228 -> TCA9517 -> host I2C
Shunt Kelvin terminals + LOAD_5V1 VBUS -> INA228
```

Six-sheet [KiCad project](../hardware/kicad/V1A.kicad_pro);
[schematic PDF](evidence/r2/V1A_SCHEMATIC.pdf);
[full review](05_SCHEMATIC_REVIEW.md). R0/R1 PASS and R2 authorization are the
user's current gate decisions; earlier contrary reports are retained as history.

## 2. Selected ICs and exact order codes

| Block | Review selection | Source |
| --- | --- | --- |
| Buck | **LM61460AANRJRR** | TI SNVSBD5D; Q1 EVM SNVU621D functional reference |
| Input | **TPS26630RGER**, **CSD19537Q3**, onsemi **BSS138** | SLVSE94G Fig 8-7; SLVUBI8A; SLPS549B; BSS138/D Rev7 |
| Output | **Not selected / not fitted**; LM74800QDRRRQ1 reviewed but unjustified | SNOSD95C; [blocker analysis](evidence/r2/OUTPUT_PROTECTION.md) |
| Monitor/shunt | **INA228AIDGSR**, **WSL27262L000FEA** | SLYS021A; SBOU241E; Vishay30131 |
| Local supply / I2C | **TPS70933DBVR**, **TCA9517DGKR** | SBVS186H; SCPS242D |

## 3. Key component values

- 400 kHz: RT=33.2k; L=6.8 uH XAL8080-682MED; FB=100k/24.4k;
  CFF=22 pF +1k; RBOOT=0; BIAS grounded to avoid raw-fault overvoltage.
- Input bank 2x22 uF/50 V plus 100 nF/50 V at each VIN/PGND pair; raw output
  bank 6x22 uF/50 V, TDK C5750X7R1H226M250KB.
- Input UV=332k/54.9k; OV=348k/15.8k; PG=56.2k/10k; ILIM=4.02k;
  dVdT=100 nF; MODE open gives latched overload response.
- Shunt=2 mOhm, +/-1%, four terminals; filter=10 Ohm each/100 nF differential;
  address0x40; local/host pull-ups10k/4.7k to their respective 3.3 V domains.
- Fuse, power/host connector MPNs and several passive/footprint qualifications
  remain OPEN. SMBJ26CA is only an uncoordinated TVS candidate.

## 4. References and modifications

[R2 source register](evidence/r2/source_register.json) pins revisions, cached
hashes, reference/adaptation and rights. Manufacturer circuits were adapted;
no predecessor PCB/CAD was copied. Each sheet records source/function/change/rationale.
Source pack and prior evidence were preserved. Some capacitor/TVS evidence remains
mirror/search-only; explicit qualifications are in the block reports.

## 5. Selection-driving calculations

- Divider output5.09836 V. At24 V/5 A, nominal ripple1.476 A, peak5.738 A,
  RMS5.018 A. Explicit L/f/bias screening gives peak6.139 A; required Ton483 ns
  at440 kHz versus70 ns maximum minimum-on-time at TI's test condition.
- Effective-C screening: input19.448 uF, output85.272 uF; estimated ripple13.8 mV
  with assumed2 mOhm ESR. These are **not guaranteed minima or measured ripple**.
- Input UV trip8.224-8.691 V; OV26.974-28.289 V; current4.160-4.796 A;
  24 V ramp37.3-63.3 ms. Shunt10 mV/50 mW at5 A.
- 90% module efficiency permits2.833 W total loss. Output switch loss is unresolved.
  TI four-layer EVM thermal evidence supports converter feasibility, not V1A validation.
- LM74800 comparator tolerance alone can require a worst-case trip above5.47 V
  when avoiding a trip near5.16 V; delay adds let-through. No load fault ceiling
  was supplied, so the independent output protection cannot be released.

## 6. ERC result

KiCad9.0.6: **1 error, 0 warnings, 0 exclusions; exit5**. U402 IN has no supply
because output protection is open. Kept visible; **ERC does not pass**.
Exported connectivity check and five regression tests PASS. All six final PDF
pages visually reviewed. No PCB/DRC or physical electrical tests.

## 7. Unresolved technical risks

Output OV voltage/time window, capacitance and FET SOA; input fuse/surge/negative
clamp coordination; biased/hot L/C and load-transient stability; exact RJR/SON/
Kelvin/TDK lands; connector and passive ratings; I2C low-level/leakage margins;
whole-module efficiency, ripple and temperature remain unmeasured.

## 8. Decisions before R3

Supply load normal/fault voltage-time and capacitance limits, source/fault/surge
envelope, output recovery and externally powered LOAD policy. Complete the
simplest justified independent disconnect, component/footprint qualification,
ERC and engineering review **within R2 first**. R3 remains BLOCKED; no placement,
routing, fabrication work, commits or pushes were performed.
