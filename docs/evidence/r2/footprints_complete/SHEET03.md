# Sheet 03 — concrete button connector parts

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

OBSERVATION: no empty footprints, but J301/J302 carried generic `PinHeader_1x02` MPN placeholders. DECISION: qualify JST `B2B-XH-A(LF)(SN)` without boss and custom `JST_B2B_XH_A_P2.50_THT`. Mating assembly: XHP-2 housing plus two SXH-001T-P0.6 crimp contacts (AWG28–22, insulation0.9–1.9 mm); signal-only ARM/RESET buttons, not the 5 A load.

EVIDENCE: JST eXH.pdf pp2–5, unnumbered issue; PDF metadata2025-07-30, SHA in `third_party/footprints_complete/jst_xh_source.json`. Mounting-surface view rotated180°: pin1 at0,0, pin2 at+2.5,0; lock/front side negativeY. No reflection. Manufacturer2.50±0.05 mm pitch; two-circuit standard header hole1.00+0.05/−0 mm. Specify finished plated hole1.00 mm, fabricator must honor tolerance. Copper1.70×2.00 mm gives0.35/0.50 mm nominal annuli. Body7.40×5.75 mm; courtyard0.50 mm outside body. Rectangular pad1 and silkscreen1 mark; no EP, no paste, no boss hole. Manufacturer pin1 maps existing button signal and pin2 maps GND.

Only hidden MPN/Footprint strings changed; visible values, symbol/wire positions and all electrical pins are preserved. Block specification changes only part/footprint metadata to keep package checker aligned. ERC0, canonical allowed-field proof and frozen non-field source checks PASS.
