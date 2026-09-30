# Sheet 05 — connectors and harness boundary

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Pad PASS means geometry and pin correspondence, not hot contact qualification.

## Board connectors

| Ref | Selected MPN / mate | Pad evidence and numbering | Geometry result |
|---|---|---|---|
| J501 | JST B2P-VH-FB-B(LF)(SN); VHR-2N housing + two SVH-21T-P1.1 contacts, AWG18 proposed | eVH.pdf PDF metadata2026-01-09 pp2–4; pitch3.96±0.05, plated hole1.65+0.10/−0 →1.70 selected; boss1.40+0.10/−0 →1.45. Pad1 at0,0, pad2 at3.96,0; boss−1.50,−3.40. Copper2.70 mm; square/rounded pad1=VIN_RAW,2=GND. Header9.80×9.70 mm. | PASS; original pinned KiCad geometry, project identity/revision; no EP/paste. 7 A catalogue with AWG18 shrouded header; actual input/startup/fault and hot derating OPEN. |
| J502 | Phoenix1776508 MSTB2,5/2-GF-5,08; mate1777989 MSTB2,5/2-STF-5,08 (integral screw contacts, no separate crimp) | Phoenix generated2013-11-12 p6 plus current product record. PTH1.40 at0,0 and5.08,0; copper2.80 mm project choice. NPTH2.40 at−5.08,2.50 and10.16,2.50 for board fixing; no electrical numbers. Body20.32×12.00 mm; rear edgey−2.00. Project terminal1 left=LOAD_5V1,2=GND, square pad/1+ legend; manufacturer drawing does not assign electrical polarity. | PASS for pad geometry; hot contact resistance OPEN. 12 A nominal; use screw retention. Drawn mate envelope is assembly guidance, not a released enclosure/tool clearance. |
| J503 | JST B4B-XH-A(LF)(SN); XHP-4 + four SXH-001T-P0.6 contacts | eXH.pdf pp2–5, PDF metadata2025-07-30. Pitch2.50±0.05; finished PTH0.95 within0.90+0.10/−0 range; copper1.70×2.00. Body12.40×5.75 mm, courtyard0.50 outside. Pin1=GND,2=3V3_HOST,3=SDA_HOST,4=SCL_HOST. No boss, EP or paste. | PASS; project pin1 mark and keyed housing. VREF is host input, not a host supply. |

J501 and J502 use incompatible mating families; a 9–24 V input lead cannot ordinarily plug into the 5 V output. Cable workmanship and deliberate misuse remain outside pad checks. No hot mating/unmating is permitted by the Phoenix operating instructions. J502 clamp accepts AWG24–12; proposed AWG16 trunk is within that range. Conductor torque0.5–0.6 Nm and flange torque0.3 Nm are different adjustments; inspect strip length7 mm and rated termination process.

TP501–TP504 port PR7's bare copper1.5 mm pad1, no paste, no purchased MPN. Only connector Footprint/MPN/Value and test-pad Footprint strings changed. All symbol locations, connections and ERC settings remain exact. Source/Rating fields and old narrative schematic notes are preserved by the strict field-only contract; this dated selection supersedes their connector-MPN-OPEN text without claiming electrical closure.

## J502 → Pi: all ten required physical contacts

**REQUIREMENT:** use both Pi5V pins2/4 and GND6/9/14/20/25/30/34/39. J502 remains the original two-pole module connector. External fan-out realizes the ten Pi connections; a forty-pin schematic connector substitution would violate this task's frozen netlist.

**DECISION — candidate assembly:** retain gold Harwin M20-1180042 crimp sockets. Use M20-1071000 (2×10) over Pi physical1–20 and M20-1070800 (2×8) over25–40. Leave21–24 uncovered. Both sizes appear in manufacturer issue8's02–12 positions-per-row range. This deliberately avoids nonexistent M20-1072000 and avoids abutting two2×10 housings: 25.40±0.30 mm bodies can clash when placed only25.40 mm apart. The selected10+8 arrangement has5.08 mm nominal body gap (4.78 mm with each half-length at its maximum). That calculation is a geometric screen, not a validated carrier design. Provide one indexed insulating hold-down referenced to Pi mounting holes so neither socket can reverse or shift by one row/column. Pi board/header identity, engagement and mechanical fit remain OPEN until checked on the exact board revision.

| Module source | Pi physical pin | Socket / local physical cavity | Required current at5A, equal sharing |
|---|---:|---|---:|
| J502.1 LOAD_5V1 | 2 | first /2 | 2.500 A |
| J502.1 LOAD_5V1 | 4 | first /4 | 2.500 A |
| J502.2 GND | 6 | first /6 | 0.625 A |
| J502.2 GND | 9 | first /9 | 0.625 A |
| J502.2 GND | 14 | first /14 | 0.625 A |
| J502.2 GND | 20 | first /20 | 0.625 A |
| J502.2 GND | 25 | second /1 | 0.625 A |
| J502.2 GND | 30 | second /6 | 0.625 A |
| J502.2 GND | 34 | second /10 | 0.625 A |
| J502.2 GND | 39 | second /15 | 0.625 A |

Local cavity numbers here mean Pi-style odd/even physical positions viewed from the Pi component side; wire-entry view is mirrored. They are a harness assembly map, not an unsupported claim about the manufacturer's complete numbering scheme. Confirm housing pin1 triangle against Pi physical1/25 and continuity-test all ten branches plus isolation from every unused pin before power.

**OPEN — resistance:** Harwin C00120 issue20 specifies20mΩ initial/30mΩ conditioned, not≤20mΩ hot with the unidentified Pi male header. Phoenix's1.0mΩ header and1.3/1.4mΩ plug readings likewise do not establish a guaranteed hot complete-pole maximum; do not add overlapping test reference planes. No candidate studied proves the full hot criterion. Retain the concrete, crimpable, previously reviewed system as the best implementation candidate among these reviewed choices; do not treat it as electrically qualified. Samtec SSW/TSW RevB'sΔ15mΩ is a change limit, not absolute resistance, and4.7A was tested with one pin per row, unlike adjacent Pi pins2/4. JST VH is useful at the module input, but is not a compatible Pi mate and its20mΩ after-test figure does not prove the requested hot bound.

**PATH_BUDGET acceptance targets, still unvalidated:** Pi full mated contact≤20mΩ hot/conditioned; module J502 complete mated pole including clamp≤3.12mΩ hot (stricter than20mΩ). At5A equal sharing the Pi contact pair/returns contribute20/2+20/8=12.5mΩ,62.5mV; J502 send+return adds6.24mΩ,31.2mV. These are allocations, not supplier guarantees. Retain proposed75mm AWG16 trunk, AWG22 positive fan-outs15mm and ground fan-outs35mm with qualified insulated splices. Do not put AWG16 into the Harwin AWG22–30 crimp. Require positive branch resistance ratio≤1.5 for≤3A/contact at5A under the existing headline rating; real hot derating may tighten that. Loss of one positive contact is not tolerated at5A. Four-wire hot/conditioned measurements, per-contact current/temperature and actual mating approval must precede SBC use.

Evidence and exact internal branch commits: [INPUT_PROVENANCE.json](INPUT_PROVENANCE.json). Manufacturer revisions/hashes and license dispositions: [connector sources](../../../../third_party/footprints_complete/connector_sources.json). Electrical PATH_BUDGET and Gate3b work are referenced, not merged.
