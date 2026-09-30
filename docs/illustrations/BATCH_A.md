# Batch A — P0 bench and current architecture

These five prompts are prioritized first. Generate one image per prompt. Do not place generated binaries in the repository; return each image for technical review before use.

## A1 — P0 fault-injection bench setup (NEW, first priority)

```text
Create one landscape 16:9 engineering training illustration titled “P0 — Dummy-Load Fault-Injection Bench”. Show a compact 5 V fault-test board as an unbranded generic board outline, a current-limited programmable bench supply connected to the board input, an electronic dummy load connected to the protected output, an oscilloscope probing the output node, and a current probe around the output lead. Use arrows to show the measurement locations. Include an operator-facing sequence: “1 Visual + continuity checks”, “2 Current-limited supply”, “3 No-load startup”, “4 Dummy-load steps”, “5 Fault injection”, “6 Capture voltage/current/temperature”. Put a large, unmistakable red boundary label: “NO RASPBERRY PI CONNECTED”. Add “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)” in a top banner. Mark the board “CONCEPTUAL — NO PCB ROUTED”.

Style: clean, technically restrained vector diagram, white background, navy labels, teal normal power, orange measurements, red fault boundary. No fake photographs, no specific connector part, no fabricated trace detail, no numeric pass limits, no claim of validation or safety. Keep text large and sparse, reproduce exact wording, and leave margins for cropping.
```

## A2 — Sheet 03 architecture D (NEW)

```text
Create a landscape functional block diagram titled “Sheet 03 — Fault-Test Board Architecture D”. Include this exact top banner: “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)”. Left-to-right protected power path: “24 V module output (source bound OPEN)” → “LM61460 buck / 5 V rail” → “series disconnect at module” → “shunt / test output” → “dummy load during validation”. Above the disconnect show a fault detector/latch chain exactly as “REF5025 → TLV3201 → 74LVC1G74 → LTC7001”. Show the disconnect devices exactly as “2 × BSC034N06, back-to-back”. Add a distinct parallel protection block “Crowbar / absorber — sizing and final implementation OPEN” connected at the protected output. Draw a second source-side block “Timed input isolation through TPS26630; controlled 10–30 µF input bank; source bound from Gate 3b”. Use a red dotted arrow for fault response and solid teal for normal power. Show “Application margins OPEN — close by dummy-load bench tests”.

Keep the block diagram functional and non-pin-level. Do not invent resistor/capacitor values, timing values, thresholds, current limits, source impedance, or measured results. Do not show Option E / Pi-end protection as selected. Include no Pi. Use large exact labels, white background, clear visual hierarchy, and no fake PCB image. “CONCEPTUAL — NO PCB ROUTED” must appear at the bottom.
```

## A3 — Present source boundary (NEW)

```text
Draw one clean left-to-right system block diagram titled “V1A Source Boundary — Current Project Context”. Exact blocks and arrows: “13S battery” → “PDB” → “Bought isolated 48 V → 24 V module (NOT SELECTED)” → “V1A”. Make clear that the 48 V to 24 V converter is a bought isolated module, not a V1A-designed converter. Show the selected module as an OPEN item with an amber outline and the exact text “Model, limits and fault behavior OPEN”. Add an optional small note “V1A is a standalone Project II design”. Do not draw a direct battery-to-V1A path. Do not imply the battery feeds V1A at 48 V or 24 V directly.

Style: restrained vector engineering diagram, horizontal layout, white background, legible labels, simple arrows, no decorative circuitry. No assumed robot bus details, no chosen converter brand/model, no ratings beyond the exact 13S and 48 V → 24 V description. This is an architecture illustration, not a PCB layout or validation claim.
```

## A4 — Fault-event sequence (NEW)

```text
Draw a five-frame horizontal event sequence for the preliminary Sheet 03 fault-test board. Exact title: “Fault-Injection Sequence — Bench Validation Required”. Include the exact banner “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)”. Frames: “1 Normal 5 V operation on dummy load”; “2 Inject converter fault condition”; “3 Detector latches fault”; “4 Series disconnect opens; crowbar/absorber receives bounded event”; “5 Record output voltage, switch current and temperature”. Add an amber annotation between frames 3 and 4: “Actual timing and all voltage margins OPEN”. Put “Dummy load only — Pi disconnected” in a prominent footer. Use simple block symbols and arrows, not a schematic or realistic board rendering.

Do not fabricate a waveform, timing scale, peak value, threshold, or successful outcome. Show the oscilloscope and current probe as measurement icons in frame 5. Mark the sequence as a planned test, not tested behavior. White background, clean vector style, large readable exact text, no decorative details.
```

## A5 — Pi power harness boundary (NEW)

```text
Create a simple two-part engineering illustration titled “Pi Power Harness — Pin Grouping and Open Connector Choice”. Panel 1 shows the Raspberry Pi power pin group abstractly: “5 V pins: both pins” and “GND pins: all 8 pins”, with current-sharing lines leading into a short “AWG16 harness”. Panel 2 shows the board-side connector as a neutral placeholder labeled “J502 — NOT FINAL”. Include a small note “Power harness only; no USB 3.x or D435i data through this PCB”. Do not assign physical pin numbers unless shown as text supplied here; do not invent connector series, wire length, contact ratings, or current sharing percentages. This is a wiring concept, not an approved pinout drawing. No Pi connection is shown during P0 fault testing. Use clear high-contrast vector artwork and concise labels.
```
