# V1A-Lite fabrication export review

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

Export commands completed. This is not a fabrication-ready package.

- **OPEN:** JLC rotation/centroid offsets OPEN for every component; no offsets assumed verified.
- **OPEN:** Electrical review findings 1–4 remain blocking; R4 fabrication release is BLOCKED.
- **OPEN:** Saved copper fills match zero-error native DRC; four-layer thermal/EMI performance remains unqualified.
- **OPEN:** 3D model completeness, pad numbering and polarity require review; a render is not validation.
- **OPEN:** Paired Q102, SCR and raw-ripple pads provided; populated differential-probe access and shared-plane pickup accuracy remain unqualified.
- **OPEN:** Via holes are outside exposed lands on both faces; minimum audited hole-to-land gap 0.142 mm. Standard tented through vias selected; solder/voiding inspection still required.
- **OPEN:** First-build landed cost below 1,000,000 VND is unverified; no purchase, quote or upload performed.
- **OPEN:** 1 assembly references have blank LCSC Part #; sourcing/assembly route OPEN.

BOM and CPL use identical populated reference sets. Through-hole parts are included in the complete review inventory; the separate SMT_REVIEW BOM/CPL exclude manual parts listed in MANUAL_ASSEMBLY.csv. EXCLUDED.csv records board flags; blank LCSC numbers remain unresolved. D101 retains Bourns SMCJ64CA / Mouser 652-SMCJ64CA and has a blank LCSC field; it is not orderable through this JLC BOM. Through-hole assembly service and all rotations remain OPEN.

Per-layer PDF/PNG views use native page coordinates; all bottom layers are unmirrored. The zip contains actual enabled copper layers, mask, silk, paste, outline, job metadata, separate PTH/NPTH Excellon files and the review-only notice. Drill maps remain outside the zip.

Inspect MANIFEST.json, review/DRC.json, assembly/ROTATION_REVIEW.csv and logs. Source hashes were verified unchanged. No data was sent to JLCPCB.
