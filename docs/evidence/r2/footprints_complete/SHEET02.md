# Sheet 02 — TDK lands

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

EVIDENCE: TDK B11 Apr2011 printed p72 (PDF70) diagram visually reviewed, with A=inner gap, B=each land length, C=land width. The exact current C5750X7R1H226M250KB product record gives the same 4.1–4.8 /1.2–1.4 /4.0–5.0 mm ranges. This closes the orientation gap in PR #7 and the September14 review. Source identity: `third_party/footprints_complete/tdk_source.json`. No capacitor MPN or value changed.

DECISION: A4.45/B1.30/C4.50 mm, pad centers ±2.875 mm, pitch5.75 mm. Pad1 left/2 right; part nonpolar, no manufacturer electrical pin1 and no exposed pad. Rectangular copper/paste1.30×4.50 mm; project NSMD expansion0.05 mm. Courtyard±3.80×2.95 mm encloses copper and maximum6.10×5.40 mm body with≥0.25 mm allowance. Paste1:1 is a preliminary process choice, subject to assembler volume/strain review; no thermal vias. Larger generic2220 lands remain rejected.

Eight assignments: C201,C202,C209,C210,C211,C212,C213,C214. C404 uses the same geometry in Sheet04. L201 remains untouched and OPEN for Gate3b. Source/Rating strings retain historical OPEN wording because the permitted netlist changes exclude those fields; this dated evidence supersedes their land-orientation uncertainty only. DC bias, ageing, regulator stability and assembly reliability remain electrical/process review items.

Checks: full-project ERC0, unchanged project settings; canonical comparison and exact non-field schematic bytes PASS. The canonicalizer explicitly handles KiCad's duplicated Footprint field as well as the top-level footprint element. The first provisional Sheet01 comparison omitted this duplicate; the corrected check proves that only TP101/TP102 footprint values changed.
