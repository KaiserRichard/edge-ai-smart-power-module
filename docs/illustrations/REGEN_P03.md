# Regeneration prompts — Lesson 03 pilot diagrams

2026-09-30. The owner rejected the code-drawn schematic-style figures in the [Lesson 03 pilot](../lessons/pilot/03%20Output%20protection%20(pilot).md). This file replaces five of them with ChatGPT-generated illustrations. The format follows [BATCH_F](BATCH_F.md) and [REGEN_PROMPTS](REGEN_PROMPTS.md): one image per fenced prompt, each prompt self-contained.

**Save each image under its exact target filename** in `V1A-Lessons/images/` (and `docs/lessons/pilot/images/` in the repo). It then replaces the old picture with no lesson edit. The lesson's display widths still apply.

**Kept as code figures (data, not diagrams):** `p03-03-energy-stores`, `p03-06-fault-timeline`, `p03-07-with-vs-without`, `p03-08-detector-latency`, `p03-09-voltage-ladder` and `p03-10-drop-budget`. Their numbers come from the model and the gate reports, and an image generator must not redraw them. `make_figures.py` now re-renders only these; pass `--diagrams` to overwrite the five below with the old code versions.

**Colour convention (every prompt):** purple = input side (9–26 V); orange = `VOUT_5V1` raw 5 V node; blue = `VOUT_PROTECTED` / Pi side; red = fault; green = safe; teal = control signals; grey = ground.

**REQUIREMENT:** teaching illustrations only. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

Tip: paste the BATCH_F **Style block** first in the same chat. If a label comes out misspelled, reply "keep everything, fix only the text: …".

## R3.1 — Where Sheet 03 sits

Target filename: `p03-01-where-sheet03-sits.png`

```text
Create a wide 16:9 technical infographic titled "Where Sheet 03 sits in the V1A power path". Clean modern flat-vector style with soft shadows, white background, rounded cards, thick flowing power arrows.
Left to right, a single power path of cards joined by thick arrows:
1 card "Isolated 48→24 V module" (purple),
2 card "Sheet 01 – Input protection" with small sub-label "F101 fuse · D101 TVS · TPS26630 eFuse" (purple),
3 card "Sheet 02 – Buck converter" with sub-label "LM61460 + L201 10 µH" (light orange).
The arrow leaving the buck turns ORANGE and is labelled "VOUT_5V1 (raw)".
Then a large dashed orange frame labelled "SHEET 03 – Output protection (architecture D)" containing, left to right:
  an orange tank icon "Raw bank 8 × 470 µF" with a drain valve under it labelled "Raw dump 100 mΩ",
  in the centre a red double-door gate icon "Series switch – 2 × BSC034N06 back-to-back",
  a small teal box above the gate "Detector + latch" with a teal signal line down to the gate,
  a blue tank icon "Protected bank 4 × 470 µF" with a drain valve under it labelled "Crowbar CSD18540Q5B".
The arrow leaving the frame is BLUE and labelled "VOUT_PROTECTED".
Then card "Sheet 04 – 2 mΩ shunt + INA228" (light blue), arrow labelled "LOAD_5V1", then final card "J502 → harness → Pi 5 GPIO" with a small note "dummy load on R2" (blue).
Bottom colour key strip: "purple = input side", "orange = raw 5 V", "blue = what the Pi sees".
Small footer bottom-right: "Functional map, not a wiring diagram". No other text, no extra parts.
```

Reject if: any label is misspelled; the gate is not between the two tanks; a drain is missing; extra parts or numbers appear.

## R3.2 — Healthy buck vs high-side short

Target filename: `p03-02-buck-normal-vs-shorted.png`

```text
Create a wide 16:9 two-panel teaching illustration titled "The one fault Sheet 03 exists for: a buck high-side short". Semi-realistic 3D-ish circuit style: glowing copper traces on a dark-green board background inside each panel, clean labels on white tags.
BOTH panels show the same simplified buck converter drawn correctly: a purple battery-style source "VIN 24 V" on the left; along the TOP rail a switch "High-side FET" in SERIES between VIN and a node "SW"; from SW a switch "Low-side FET" going DOWN to ground; from SW along the top rail a coil "L201 10 µH" to an orange node "VOUT_5V1"; from VOUT_5V1 a capacitor "Raw bank" down to ground and a resistor "Load" down to ground; one bottom ground rail.
LEFT panel, title "Healthy: switching": the high-side switch is shown flickering open/closed, with a small square-wave pulse graphic at SW labelled "24 V pulses, about 21 % on", and a smooth line at the output labelled "≈ 5.1 V". Calm blue/orange glow.
RIGHT panel, title "Fault: high-side FET failed short": the high-side switch is replaced by a solid glowing RED bar with a crack/burn mark and tag "Shorted – always on"; a red current arrow runs from VIN through the short and through L201 into VOUT_5V1; the SW node shows a flat line labelled "24 V all the time"; low-side FET tag "off".
Caption under the right panel: "Feedback cannot open a short." No other text or numbers.
```

Reject if: the high-side switch is drawn from the top rail to ground (it must be in series on the top rail); the low-side switch is missing; numbers other than those quoted appear.

## R3.3 — Why two MOSFETs back-to-back

Target filename: `p03-04-back-to-back-mosfets.png`

```text
Create a wide 16:9 two-panel illustration titled "Why the series switch is two MOSFETs back-to-back". Use a water-valve metaphor drawn over simple circuit lines, clean flat vector, white background.
LEFT panel, title "One MOSFET off: still leaks one way": an orange pipe on the left labelled "VOUT_5V1 (raw)" and a blue pipe on the right labelled "VOUT_PROTECTED". Between them one closed gate valve labelled "MOSFET (off)". Under it, a thin bypass pipe with a one-way check valve labelled "Body diode", whose arrow points from the blue side to the orange side. Red water trickles backwards from the blue side to the orange side through the bypass. Caption: "Protected side can drain backwards".
RIGHT panel, title "Two MOSFETs, sources joined: off means off": the same pipes, now with two closed gate valves in series labelled "Q1" and "Q2", joined in the middle at a point labelled "Common source". Each valve has its own one-way bypass labelled "Body diode"; the two check-valve arrows point AWAY from the middle (Q1's toward the orange side, Q2's toward the blue side), so no water passes in either direction. A green check mark and caption: "Blocked both ways – each side keeps its own energy".
Small label under the right panel: "2 × BSC034N06, gates driven together by LTC7001". No other text.
```

Reject if: in the right panel the arrows point toward each other or the same way; water passes in the right panel; labels are misspelled.

## R3.4 — The detector chain

Target filename: `p03-05-detector-chain.png`

```text
Create a wide 16:9 infographic titled "Detect → remember → act". Clean flat vector, white background, five large rounded cards in a row connected by thick teal arrows, each card with a simple icon and a bold name, and a one-line plain-English job under it:
1 "Divider" (icon: two stacked resistors) — "scales the raw 5 V down" (card tinted orange),
2 "REF5025" (icon: a ruler / spirit level) — "precise 2.5 V reference" (teal),
3 "TLV3201 comparator" (icon: a balance scale tipping) — "yes/no: too high?" (teal),
4 "74LVC1G74 latch" (icon: a padlock snapping shut) — "remembers the fault" (teal),
5 "Act" (icon: a red lightning bolt) — "three actions at once" (red).
From card 5, three short red arrows fan out to small tags: "Series switch OFF", "Crowbar + raw dump ON", "eFuse OFF".
Above the row, one highlighted orange banner: "Trip ≈ 5.27 V (window 5.22–5.31 V)".
No other text, no other numbers.
```

Reject if: the order of the cards changes; the numbers differ from "5.27" and "5.22–5.31".

## R3.5 — D vs E: where the protection lives

Target filename: `p03-11-d-vs-e.png`

```text
Create a wide 16:9 two-panel comparison illustration titled "Where does the protection live? D (chosen) vs E". Soft 3D isometric style, white background.
BOTH panels show: a small green circuit board on the left labelled "V1A module", a short wire harness (a bundle of red and black wires with a coil symbol drawn on it labelled "cable inductance"), and a generic small single-board computer on the right labelled "Pi 5" (no logo).
TOP or LEFT panel, title "D – chosen for the test board": a red shield icon sits ON the V1A module, labelled "Switch + crowbar here". Over the harness, a small wavy orange overshoot squiggle between the module and the Pi, with a warning tag "Cable can ring above the module voltage". Two short bullet tags: "+ one board, no extra drop" and "− must be proven at the far end".
BOTTOM or RIGHT panel, title "E – Gate 3 recommendation": the V1A module has no shield; instead a small extra red shield board sits right at the Pi header, labelled "Protection stage at the Pi". Two short bullet tags: "+ watches the Pi's own voltage" and "− extra parts, wiring and voltage drop".
No numbers, no other text.
```

Reject if: the shield positions are swapped; any logo appears; any number appears.
