# Batch F — Visual-first images for every lesson (ChatGPT image generation)

2026-09-30. Written for the visual rewrite of the V1A lessons, starting with the [Lesson 03 (adapted pilot)](../lessons/03%20Output%20protection.md). This batch follows the format of Batches A–E and [REGEN_PROMPTS](REGEN_PROMPTS.md): one image per fenced prompt, each prompt self-contained, and each target filename is the exact name the lessons embed with `![[name.png]]`.

**What is different from A–E:** these images explain *ideas* (analogies, 3D cutaways, "what it looks like on the bench"). The *numbers* (waveforms, budgets, ladders) are rendered from code in the lesson folders, because an image generator cannot be trusted with values. So no prompt below asks for a plotted number, a measured waveform or a pass/fail result.

**REQUIREMENT:** teaching illustrations only. They are not electrical validation. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## How to use (owner)

1. Open a new ChatGPT chat and paste the **Style block** once. Then paste one prompt per message.
2. Save each image with the exact **Target filename** into `V1A-Lessons/images/`.
3. Check every image against its **Reject if** line before keeping it. Image generators misspell labels: regenerate, or ask ChatGPT to "keep everything, fix only the text".
4. Generate the **F3.x** prompts first. The Lesson 03 pilot embeds them.

## Style block (paste once per chat)

```text
You are drawing a series of engineering teaching illustrations for a senior electronics undergraduate. House style for EVERY image in this chat:
- Clean flat vector or soft 3D technical illustration, white or very light grey background, landscape 16:9, generous margins.
- Consistent colour meaning: purple = input / high-voltage side (9–26 V); orange = raw 5 V node before the protection switch; blue = protected 5 V side that feeds the computer; red = fault / danger; green = safe / pass; teal = control and sensing signals; grey = ground and returns.
- Few words. Every label short, in English, spelled exactly as given in quotes. Never invent extra text, numbers, part numbers, logos or brand names.
- No real company logos, no Raspberry Pi logo, no invented schematics, no fake oscilloscope values.
- Small footer text in the bottom-right corner: "V1A teaching illustration · not a design document".
Reply only with the image.
```

## Index

| ID | Lesson | Target filename | Idea |
|---|---|---|---|
| F0.1 | 00 System overview | `f0-01-power-journey-robot.png` | Battery-to-Pi journey inside the robot |
| F0.2 | 00 | `f0-02-v1a-board-exploded.png` | V1A as five functional zones |
| F0.4 | 00 | `f0-04-circuit-boundary.png` | Actual shunt, local-supply branch and output pins |
| F0.3 | 00 | `f0-03-five-jobs-analogy.png` | Distribute / convert / protect / measure analogy |
| F1.1 | 01 Input protection | `f1-01-input-guards-analogy.png` | Four guards at a gate |
| F1.2 | 01 | `f1-02-tvs-vs-fuse-timescale.png` | Fast spike vs slow overload |
| F1.3 | 01 | `f1-03-efuse-three-jobs.png` | eFuse: UVLO, OVP, current limit |
| F2.1 | 02 Buck converter | `f2-01-buck-two-states-3d.png` | Two switch states as water paths |
| F2.2 | 02 | `f2-02-inductor-flywheel.png` | Inductor as a flywheel |
| F2.3 | 02 | `f2-03-hot-loop-3d.png` | Hot loop area on a board |
| F3.1 | 03 Output protection | `f3-01-analogy-stuck-tap.png` | Stuck-open tap and four valves |
| F3.2 | 03 | `f3-02-energy-springs.png` | Energy stores as compressed springs |
| F3.3 | 03 | `f3-03-two-sides-two-drains.png` | Switch splits two sides, each with its own drain |
| F3.4 | 03 | `f3-04-fault-bench-no-pi.png` | Fault-test bench with dummy load, Pi locked away |
| F3.5 | 03 | `f3-05-schematic-walk-circuit.png` | Simplified Sheet 03 circuit with the fault path and the four actions |
| F4.1 | 04 Monitoring | `f4-01-kelvin-sense-3d.png` | Four-terminal shunt close-up |
| F4.2 | 04 | `f4-02-measurement-boundary.png` | What the INA228 does and does not see |
| F4.3 | 04 | `f4-03-i2c-two-islands.png` | TCA9517 as a bridge between two bus islands |
| F5.1 | 05 Pi GPIO power | `f5-01-voltage-staircase.png` | Voltage lost step by step along the path |
| F5.2 | 05 | `f5-02-gpio-pin-map-power.png` | Which header pins carry power and ground |
| F5.3 | 05 | `f5-03-current-sharing-lanes.png` | Current sharing across contacts |
| F6.1 | 06 PCB concepts | `f6-01-loop-area-compare.png` | Small vs large current loop |
| F6.2 | 06 | `f6-02-heat-flow-cutaway.png` | Heat path from part to copper |
| F6.3 | 06 | `f6-03-kelvin-routing-rule.png` | Right vs wrong sense routing |
| F7.1 | 07 Bench bring-up | `f7-01-bench-station-overview.png` | Complete bench station |
| F7.2 | 07 | `f7-02-bring-up-staircase.png` | Bring-up as a staircase with gates |
| F7.3 | 07 | `f7-03-probe-placement.png` | Where probes go |
| F8.1 | 08 V1A in the robot | `f8-01-robot-cutaway-power.png` | Wheel-biped robot power cutaway |
| F8.2 | 08 | `f8-02-isolated-vs-nonisolated.png` | Why the upstream module must be isolated |
| F9.1 | Index / glossary | `f9-01-course-map.png` | Course map, one tile per lesson |

---

## Lesson 00 — System overview

### F0.1 — The power journey inside the robot

Target filename: `f0-01-power-journey-robot.png`

```text
Draw a left-to-right "journey" illustration of electrical power inside a two-wheeled, balancing, wheel-biped robot (generic, no brand). Five stations connected by a thick glowing cable, each station a clean 3D object with a short label underneath:
1 "13S battery pack" (purple),
2 "Power distribution board" (purple),
3 "Isolated 48 V → 24 V module" (purple, with a small shield icon meaning isolation),
4 "V1A power module" (a small green PCB, the hero of the picture, slightly larger),
5 "Single-board computer" (a generic small computer board, NOT a Raspberry Pi logo).
Between V1A and the computer the cable turns blue and is labelled "5.1 V target". Above the whole journey, a faint outline of the robot body. Title at top: "Follow the power". No other text, no voltages except those quoted.
```

Reject if: a battery connects directly to V1A; an extra converter appears; any logo appears.

### F0.2 — V1A as five functional zones

Target filename: `f0-02-v1a-board-exploded.png`

```text
Draw an exploded isometric view of a single small green circuit board floating in five translucent coloured layers, stacked like a sandwich lifted apart, each layer one functional zone with a short label:
"Input protection" (purple), "Buck converter" (orange), "Output protection" (red outline, orange-to-blue gradient), "Current monitor" (teal), "Output connector" (blue).
Arrows show power flowing through the layers in order, from purple to blue. Mark the whole thing "Functional zones — not a real layout". Do not draw specific chips, pin counts, part numbers or copper traces.
```

Reject if: it looks like a real routed PCB; any part number appears.

### F0.3 — Five jobs, one analogy

Target filename: `f0-03-five-jobs-analogy.png`

```text
Draw a friendly water-supply analogy in one wide scene: a reservoir on a hill (label "Source"), a pipe with a security gate and pressure valve (label "Protect the input"), a pressure-reducing station (label "Convert"), a second emergency gate right before a house (label "Protect the output"), a water meter on the pipe (label "Measure"), and a house labelled "Computer". Water is purple before the reducing station, blue after it. Clean flat vector, soft shadows, no other text.
```

Reject if: labels are misspelled or the order changes.

## Lesson 01 — Input protection

### F1.1 — Four guards at the gate

Target filename: `f1-01-input-guards-analogy.png`

```text
Draw four cartoon guards standing in a row at a castle gate, each holding a symbol for its job, with a short label on a plaque under each:
"Fuse — breaks on long overload" (holding scissors cutting a rope),
"TVS diode — diverts short spikes" (holding a lightning rod pointing to the ground),
"Reverse-polarity FETs — block backwards power" (holding a one-way turnstile),
"eFuse — checks voltage and limits current" (holding a clipboard and a flow valve).
A purple river of electricity approaches the gate from the left. Clean flat vector style, friendly but not childish.
```

Reject if: a guard's symbol does not match its label.

### F1.2 — Fast spike vs slow overload

Target filename: `f1-02-tvs-vs-fuse-timescale.png`

```text
Draw three adjacent conceptual scenes, without a timeline or waveform. Left: a lightning flash diverted away by a drainage channel, labelled "TVS diverts surge current". Centre: a control-room guard closing a gate, labelled "eFuse detects and interrupts". Right: a heated breakaway link opening, labelled "Fuse clears sufficient overcurrent". Under all three, write "Response depends on fault, current and conditions". These are different mechanisms, not fixed speed categories. No numeric values, circuit symbols or time-axis labels.
```

MUST NOT show: an eFuse assigned to milliseconds, a fixed ordering of response speeds, or a fuse guaranteed to clear every lasting overload.

Reject if: a time axis or fixed response-time category appears. The original F1.2 image requires regeneration; response functions overlap in time.

### F1.3 — Three jobs of the eFuse

Target filename: `f1-03-efuse-three-jobs.png`

```text
Draw a single generic chip labelled "eFuse" in the centre, like a control room, with three windows looking out, each showing one job: "Too low? Stay off" (a gauge needle in a low red zone), "Too high? Cut off" (a gauge needle in a high red zone), "Too much current? Limit it" (a pipe with a narrowing valve). Purple theme. Add a small note under the chip: "Settings have tolerances and delays". No numbers.
```

Reject if: a specific threshold number appears.

## Lesson 02 — Buck converter LM61460

### F2.1 — The two switch states as water paths

Target filename: `f2-01-buck-two-states-3d.png`

```text
Draw two side-by-side panels of the same simple water circuit made of clear glass pipes, showing a buck converter as plumbing.
Left panel "High-side switch ON": water flows from a tall purple tank (the input) through an open top valve, through a heavy spinning flywheel labelled "Inductor", into a small blue bucket (the output) and on to a house. The flywheel speeds up.
Right panel "Low-side switch ON": the top valve is shut; a bottom valve from the ground-level reservoir is open; the spinning flywheel keeps pushing water toward the bucket and slows down.
Both panels: water always moves toward the bucket, never backwards. Short labels only as quoted.
```

Reject if: water flows backwards in the right panel; both valves are open at once.

### F2.2 — The inductor as a flywheel

Target filename: `f2-02-inductor-flywheel.png`

```text
Draw a heavy metal flywheel on an axle, connected by a belt to a water pump, in soft 3D. Three small inset scenes around it with short captions:
"Push → it speeds up slowly" (a hand pushing),
"Stop pushing → it keeps turning" (hand removed, motion lines),
"Too much speed → it becomes hard to stop" (red glow, warning sign).
Title: "An inductor resists changes in current". No equations, no numbers.
```

Reject if: the flywheel stops instantly in the second inset.

### F2.3 — The hot loop on a board

Target filename: `f2-03-hot-loop-3d.png`

```text
Draw two small isometric circuit boards side by side, generic and clearly conceptual. Each has one input capacitor, two small switch chips (in one package) and a ground return. On the left board, the loop of red arrows through capacitor → switches → ground → capacitor encloses a very small area; label "Small hot loop — good". On the right board, the same parts are spread apart and the loop encloses a large area with red radiating noise waves; label "Large hot loop — noisy". Banner at top: "CONCEPTUAL — NO PCB ROUTED". No part numbers, no dimensions.
```

Reject if: it looks like a finished real layout; part numbers appear.

## Lesson 03 — Output protection (generate these first)

### F3.1 — The stuck-open tap and four valves

Target filename: `f3-01-analogy-stuck-tap.png`

```text
Draw one wide plumbing scene that explains a protection circuit.
Left: a tall purple water tower labelled "24 V source". A pipe runs right to a tap whose handle has snapped off, the tap fully open, water gushing; red label "Tap stuck open = shorted switch".
Next, a long pipe section with a spinning water wheel inside, labelled "Water still rushing = inductor current".
Then an orange bucket labelled "Raw 5 V bucket" with a small drain valve underneath labelled "Raw dump".
Then a big gate valve labelled "Series switch", shown closing.
Then a blue bucket labelled "Protected side" with its own drain labelled "Crowbar", and a small house labelled "Computer".
Back at the water tower, a main valve labelled "Main valve = eFuse off", shown closing.
Number the four valves with circled numbers 1–4 in this order: main valve, gate valve, crowbar drain, raw dump. Clean vector illustration, calm colours, the only red is the broken tap. No other text.
```

Reject if: a drain is missing; the gate valve is between the tower and the tap; any extra text or numbers appear.

### F3.2 — Energy stores as compressed springs

Target filename: `f3-02-energy-springs.png`

```text
Draw four compressed metal springs in a row, each held down by a latch, each a different size to show how much energy it stores. Label each on a small plate:
"Input capacitors" (small purple spring),
"Inductor L201" (small purple spring shown as a spinning coil),
"Raw 5 V capacitor bank" (the largest spring, orange),
"Protected capacitor bank" (a medium spring, blue).
Above them the title "In a fault, every spring wants to jump toward the computer". A red arrow points from all four toward a small computer silhouette on the right, and a green shield between them labelled "Sheet 03". No numbers.
```

Reject if: the orange spring is not the largest; any number appears.

### F3.3 — One switch, two sides, two drains

Target filename: `f3-03-two-sides-two-drains.png`

```text
Draw a clean cutaway diagram of a room split by a wall with a heavy door in the middle.
Left room tinted orange, labelled "Raw side", containing a large tank and a floor drain labelled "Raw dump".
Right room tinted blue, labelled "Protected side", containing a smaller tank, a floor drain labelled "Crowbar", and a doorway to a small computer labelled "Computer".
The middle door is a double door made of two leaves hinged toward each other, labelled "Two MOSFETs back-to-back", shown shut.
Caption across the bottom: "Door shut: each side empties through its own drain". No other text.
```

Reject if: there is only one drain; the door is open.

### F3.4 — The fault-test bench, computer locked away

Target filename: `f3-04-fault-bench-no-pi.png`

```text
Draw a realistic, tidy electronics lab bench, soft 3D, seen at a slight angle. On the bench: a bench power supply with separate red and black leads, a small green test board in the centre labelled "R2 fault-test board", a large resistive dummy load with cooling fins labelled "Dummy load", an oscilloscope with two differential probes clipped to the board and a clamp-on current probe on one wire, a thermal camera on a small tripod. The screen of the oscilloscope shows only a generic grid and no numbers.
On a shelf at the back, a small single-board computer sits inside a locked clear box with a green tag: "Connect only after all fault tests pass".
Safety glasses on the bench. The positive and return leads are clearly separate wires. No logos, no numbers.
```

Reject if: the computer is wired to the board; leads merge into one cable; numbers appear on screens.

### F3.5 — Simplified Sheet 03 circuit, read left to right

Target filename: `f3-05-schematic-walk-circuit.png`

```text
Draw a clean, flat, textbook-style simplified circuit diagram on a white background, read left to right, like a figure in an electronics textbook. Use standard schematic symbols.
Left: a box labelled "U101 eFuse" with a pin labelled "SHDN" on its bottom; its output wire labelled "VIN_PROTECTED" goes to a box labelled "U201 buck". Inside U201 draw the high-side switch as a MOSFET symbol with a red lightning mark and the words "failed short".
From U201's "SW" pin a wire goes through an inductor symbol labelled "L201" to a thick orange wire labelled "VOUT_5V1 (raw)". A large capacitor symbol on that orange wire is labelled "raw bank".
Next, two MOSFET symbols placed back-to-back (sources joined in the middle, label the middle node "PROT_MID"), labelled "Q301" and "Q302", with one shared gate wire labelled "PROT_GATE" going down to a small box "U301 LTC7001".
After Q302, a thick blue wire labelled "VOUT_PROTECTED" goes to a resistor labelled "shunt" and then to a connector labelled "J502 to Pi".
On the blue wire, a vertical MOSFET to ground labelled "Q303 crowbar", with a small resistor above it labelled "33 mΩ ballast", driven by a small box "U315".
On the orange wire, a dashed vertical switch to ground labelled "raw dump (not drawn yet)", drawn in grey dashed lines.
At the bottom: a small detector chain: a resistor divider from VOUT_5V1 to a comparator triangle labelled "U303", with a reference box "U302 2.5 V" on its other input, then a box "U304 latch". From the latch, four thin red arrows go to: U101 SHDN, U301, U315, and the raw dump.
A thick red arrow shows the fault current flowing from VIN_PROTECTED through U201 and L201 into VOUT_5V1.
Keep text only as labels listed above. No numbers other than "33 mΩ" and "2.5 V".
```

Reject if: Q301 and Q302 are drawn in the same direction instead of back-to-back; the crowbar is on the orange (raw) side; the raw dump is drawn as a normal solid part; extra numbers appear.

## Lesson 04 — Monitoring

### F4.1 — Four-terminal (Kelvin) shunt close-up

Target filename: `f4-01-kelvin-sense-3d.png`

```text
Draw a macro close-up, soft 3D, of a single rectangular metal-strip current-sense resistor on a board with four terminals: two wide outer pads labelled "Force (load current)" with thick blue copper, and two narrow inner pads labelled "Sense" with thin teal traces running away together side by side to a small chip labelled "INA228". Thick glowing current arrows pass only through the force pads and the resistor body. The thin sense traces carry no current arrows. Title: "Measure across the resistor, not the copper". No values.
```

Reject if: the sense traces join the thick copper away from the resistor; values appear.

### F4.2 — What the monitor sees

Target filename: `f4-02-measurement-boundary.png`

```text
Draw a simple power path from left to right: "Buck" → "Protection switch" → "Shunt" → "Connector" → "Cable" → "Computer". Put a translucent teal bubble around only the shunt and the node right after it, labelled "What the INA228 measures". Grey out the parts outside the bubble, with small captions: "upstream losses — not seen" on the left and "cable drop — not seen" on the right. Clean flat vector.
```

Reject if: the bubble covers the cable or the computer.

### F4.3 — Two bus islands joined by a bridge

Target filename: `f4-03-i2c-two-islands.png`

```text
Draw two small islands connected by a narrow bridge. Left island labelled "V1A monitor side (3.3 V)" with a tiny chip "INA228" and its own lamp post labelled "pull-ups". Right island labelled "Host side" with a tiny computer and its own lamp post labelled "pull-ups". The bridge is labelled "TCA9517 buffer" and carries two thin lanes labelled "SDA" and "SCL". Under the sea, one shared cable labelled "shared ground". A small note: "A buffer, not an isolation barrier". Flat vector.
```

Reject if: the bridge is labelled as isolation; the ground cable is missing.

## Lesson 05 — Powering the Pi 5 through GPIO

### F5.1 — The voltage staircase

Target filename: `f5-01-voltage-staircase.png`

```text
Draw a staircase going down from left to right. The top step is labelled "Buck output". Each lower step is labelled with one thing that costs voltage, in this order: "Protection switch", "Shunt", "Board copper", "Connector", "Harness wire", "Header contacts", "Ground return". The bottom step is labelled "Computer" with a small blue figure standing on it, and a dashed green line just below it labelled "minimum allowed". Step heights differ; the "Protection switch" and "Header contacts" steps are the tallest. No numbers.
```

Reject if: step order changes; numbers appear.

### F5.2 — Which header pins carry power

Target filename: `f5-02-gpio-pin-map-power.png`

```text
Draw a clean top-down diagram of a generic 2 × 20 pin header (40 pins), pins numbered 1 to 40 in the standard odd/even layout (odd numbers on the left column, even on the right, pin 1 at top left). Highlight pins 2 and 4 in red with the label "5 V". Highlight pins 6, 9, 14, 20, 25, 30, 34 and 39 in dark grey with the label "GND". All other pins pale and unlabelled except the numbers. Legend: "Power pins only — never signal pins". No board outline, no logo.
```

Reject if: any highlighted pin number is wrong (check all ten), or pin 1 is not top left.

### F5.3 — Current sharing across contacts

Target filename: `f5-03-current-sharing-lanes.png`

```text
Draw a highway analogy: one wide road labelled "Positive current" splits into two lanes entering two toll booths labelled "5 V pin 2" and "5 V pin 4"; a return road splits into eight narrower lanes through eight booths labelled "GND". A second small inset shows one of the two 5 V booths closed with a red barrier, and all positive traffic squeezed into the remaining booth, glowing red; caption "One open contact doubles the current in the other". No numbers.
```

Reject if: the inset shows ground booths closing instead of a 5 V booth.

## Lesson 06 — PCB concepts

### F6.1 — Loop area

Target filename: `f6-01-loop-area-compare.png`

```text
Draw two identical simple circuits as thin copper loops on a board seen from above. Left: the outgoing and return paths run right on top of each other (return directly under the outgoing path on the next layer), enclosing a tiny area shaded light green; label "Small loop area". Right: the return path wanders far away, enclosing a large area shaded light red with magnetic field lines rising from it; label "Large loop area — more inductance and noise". Banner: "CONCEPTUAL". No dimensions.
```

Reject if: dimensions or trace widths are labelled.

### F6.2 — Heat flow cutaway

Target filename: `f6-02-heat-flow-cutaway.png`

```text
Draw a cross-section cutaway of a multi-layer circuit board with one power chip soldered on top. Show heat as orange-to-red arrows flowing from the chip down through a row of small vertical thermal vias into wide inner copper planes and spreading sideways, then leaving the board surface to the air. Label: "Chip", "Thermal vias", "Copper planes", "Heat to air". Banner: "CONCEPTUAL — NO PCB ROUTED". No layer counts, no numbers.
```

Reject if: a specific layer count or copper thickness is written.

### F6.3 — Sense routing, right vs wrong

Target filename: `f6-03-kelvin-routing-rule.png`

```text
Draw two small top-down panels of the same four-terminal shunt resistor. Left panel with a green check: two thin teal sense traces start at the shunt's own inner sense pads and run together as a tight pair to a chip. Right panel with a red cross: the sense traces start from random points on the wide copper pour away from the shunt and run far apart. Captions: "Right: sense at the resistor" and "Wrong: sense on the copper". Flat vector.
```

Reject if: the right/wrong labels are swapped.

## Lesson 07 — Bench bring-up and fault-injection testing

### F7.1 — The complete bench station

Target filename: `f7-01-bench-station-overview.png`

```text
Draw an isometric bench station with each instrument labelled by its job, not its brand: "Current-limited supply", "Dummy load", "Oscilloscope", "Differential probes", "Current probe", "Multimeter", "Thermal camera". A small green board labelled "V1A test board" in the middle. Cables: positive red, return black, always two separate wires per connection. No computer anywhere on the bench. No logos, no numbers on screens.
```

Reject if: any computer appears; any instrument shows numbers.

### F7.2 — Bring-up as a staircase with gates

Target filename: `f7-02-bring-up-staircase.png`

```text
Draw a staircase climbing from bottom left to top right with seven steps, each step a small scene with a short label in this exact order:
"1 Look", "2 Check for shorts", "3 Current-limited power", "4 No-load start", "5 Load in small steps", "6 Heat, ripple and fault tests", "7 Telemetry, then the computer".
Between step 6 and 7 stands a locked gate labelled "Only after every test passes". A small figure climbs the stairs. Flat vector.
```

Reject if: the computer appears before step 7; the step order differs.

### F7.3 — Where the probes go

Target filename: `f7-03-probe-placement.png`

```text
Draw a simplified block drawing of the power path "Raw 5 V node" → "Series switch" → "Protected node" → "Harness" → "Dummy header". Place three differential voltage probe icons: one across the raw node and its ground, one across the protected node and its ground, one across the far-end dummy header and its own return pin. Place a clamp current-probe icon around the wire into the inductor. Label each probe with a short tag: "V raw", "V protected", "V far end", "I inductor". Add a note: "Start recording before the fault". No numbers, no waveforms.
```

Reject if: the far-end probe references module ground instead of the header's own return.

## Lesson 08 — V1A inside the robot

### F8.1 — Robot power cutaway

Target filename: `f8-01-robot-cutaway-power.png`

```text
Draw a generic two-wheeled balancing robot (wheel-biped: two legs ending in wheels, a compact body) in a semi-transparent cutaway. Inside: a battery pack at the bottom labelled "13S battery", a distribution board labelled "PDB", a small box labelled "Isolated 48 V → 24 V", a small green board labelled "V1A", and a compute module labelled "Computer", connected by a glowing purple cable that turns blue after V1A. Motors in the legs are connected to the PDB by separate grey cables labelled "Other branches". No brand, no logo.
```

Reject if: V1A connects directly to the battery.

### F8.2 — Isolated vs non-isolated upstream module

Target filename: `f8-02-isolated-vs-nonisolated.png`

```text
Draw two side-by-side panels. Left, red cross, title "Non-isolated step-down": one continuous copper path runs from a "48 V battery" through a converter whose top switch is drawn failed short (red), straight into "V1A"; a red arrow shows battery voltage reaching V1A. Right, green check, title "Isolated module": the battery side and V1A side are separated by a transformer with a clear gap and a shield icon labelled "Isolation barrier"; no direct copper path exists. Caption under the right panel: "Isolation removes the direct short path. Its fault limits still need testing." Flat vector.
```

Reject if: the right panel shows a copper link across the barrier.

## Index / glossary

### F9.1 — Course map

Target filename: `f9-01-course-map.png`

```text
Draw a course map in the style of a metro line: nine stations along one coloured line, each with a small icon and a short label in this order: "00 Overview", "01 Input protection", "02 Buck converter", "03 Output protection", "04 Monitoring", "05 Pi GPIO power", "06 PCB concepts", "07 Bench tests", "08 In the robot". Station 03 is a larger interchange marked with a star. The line colour goes from purple (00–02) through orange (03) to blue (04–08). Title: "V1A lessons". Flat vector.
```

Reject if: a station is missing or misspelled.


---

## Pilot concept images retained in Lesson 03

The following five targets already exist in the owner's read-only image folder. They replace the pilot's former code-drawn concept illustrations. Existing F3.1–F3.4 explain the analogy and bench; they do not cover these specific teaching views. Use these prompts when correcting or regenerating the retained images. Charts remain Python-generated under `docs/lessons/figures/`.

### F3.5 — Where Sheet 03 sits

Target filename: `p03-01-where-sheet03-sits.png`

```text
Create a clean conceptual engineering illustration, landscape, in the Batch F colours. Show a left-to-right power journey: "Input protection" in purple, "Buck + L201" leading to orange "Raw output", an orange capacitor tank with its own "Raw dump", a central double gate "Series disconnect", a blue capacitor tank with its own "Crowbar", then "Shunt", "Connector + harness", and "Dummy load". Put a dashed boundary around the double gate, both tank drains and the detector labelled "Sheet 03 — preliminary architecture D". Put an independent small control-power box above the detector and drivers; label "Control supply — qualification open". Show a teal sensing line from raw output to detector; no pin numbers, resistor values or fabricated circuit. Add "Different nodes: raw, protected, load and far end" and "Functional picture, not a wiring diagram". Both positive and return roles must be clear without a detailed schematic. Do not use a Pi as the test load.
```

MUST NOT show: a bypass around the series gate; one drain absorbing both sides after the gate closes; a finished PCB; guaranteed protection or fitted capacitor values.

Reject if: the shunt precedes the output disconnect, the harness endpoint is labelled as the same voltage as the raw node, or the image implies release.

### F3.6 — Healthy switching versus a permanent high-side short

Target filename: `p03-02-buck-normal-vs-shorted.png`

```text
Create two clean conceptual cutaway panels of a buck converter with a top input gate, a bottom return gate, an inductor and a raw output tank. Left title "Healthy switching": the two gates alternate; show two small state icons with exactly one gate open in each, and current always moving through the inductor toward the output. Right title "High-side switch failed short": the top gate is visibly jammed conducting; the bottom gate is off. Show a continuous purple path from input through the jammed top gate and inductor toward the orange raw output, with a red danger halo. Caption "Feedback cannot turn off a physical short". Mark "Conceptual — not a buildable schematic". Use no numerical waveforms or component values.
```

MUST NOT show: both gates conducting simultaneously in the intended fault model, a reversed freewheel current, an inductor stopping sustained DC, or a measured fault trace.

Reject if: the failed top switch looks open or a controller command is shown curing the short.

### F3.7 — Why the disconnect uses opposed MOSFETs

Target filename: `p03-04-back-to-back-mosfets.png`

```text
Draw an exact conceptual comparison, white background, orange raw side on the left and blue protected side on the right. Left panel "One N-channel MOSFET OFF": label D at the left and S at the right; show its body diode with anode at S and cathode at D, permitting the illustrated reverse direction when forward-biased. Right panel "Two N-channel MOSFETs OFF": label the connection D–S / S–D with sources joined in the middle, drains facing the outside. Show both body-diode anodes at the common-source connection and cathodes at the outside drains, so the diodes oppose along the through path. Label "Common source" and "Gate drive omitted". Caption "Bidirectional blocking within ratings; leakage and transients still matter". Use no part values or claim of ideal zero leakage.
```

MUST NOT show: common drains, diode cathodes joined at the common-source node, both diodes pointing along the through path, or infinite-voltage blocking.

Reject if: the terminal labels and diode polarities disagree. This is a concept figure, not an approved gate-drive circuit.

### F3.8 — Detector inputs and parallel fault actions

Target filename: `p03-05-detector-chain.png`

```text
Draw a clean control illustration titled "Detect, remember, act". A raw-output divider and a separate "REF5025 reference" feed TWO SEPARATE inputs of a "TLV3201 comparator". Its output enters a "74LVC1G74 latch" with a note "Requires valid control supply". From the latch branch to "Series switch OFF", "Protected crowbar ON" and "Raw dump ON". Separately show a dashed unresolved detector titled "Independent source trigger — OPEN" commanding "TPS26630 input OFF". The overvoltage latch may also request input off, but mark "OV path alone is too late for source target". Put a small rail-supply ribbon above the logic labelled "Startup, rail loss and checked re-arm remain OPEN". Use no numeric thresholds, propagation times or detailed logic pins.
```

MUST NOT show: divider signal passing through the reference, a raw-voltage trip proving the source-cutoff target, permanent memory without power, or all physical actions completing simultaneously.

Reject if: the independent source-trigger gap is hidden by an ideal arrow or the reference is in series with the sense path.

### F3.9 — Module-side versus Pi-end protection

Target filename: `p03-11-d-vs-e.png`

```text
Draw two conceptual side-by-side system views with the same buck, module, harness and future computer endpoint. Left title "D — chosen for the test board": locate the final series disconnect and local absorber inside the module, before the harness. Add a red question mark at the far end labelled "Harness peak must be proved". Right title "E — earlier alternative": show an additional final protection stage at the computer header and label "Extra hardware, control power and path loss". Show the harness as a pair of positive and return wires in both panels. Caption "D avoids the additional Pi-end stage; D still has its own series loss". Use a dummy-header fixture icon beside both endpoints and "No Pi until required gates pass". No numerical peak, resistance or measured waveform.
```

MUST NOT show: D as lossless, E as selected by the owner, either alternative as qualified, or the computer connected during fault tests.

Reject if: the two protection locations are indistinguishable or the harness return is missing.


---

## Schematic companions added after the owner's PDF feedback

These prompts complement the existing analogies. Attach the named **review PDF page** and the matching **v2 circuit PNG** as references when generating them. Preserve connectivity, refdes and pins; leave out omitted circuitry rather than inventing it. The code excerpts are permitted by the owner's final request for exact simple circuits. They are teaching excerpts, not new design files.

### F0.4 — Where the branch measurement ends

Target filename: `f0-04-circuit-boundary.png`

```text
Make a clean, readable CIRCUIT picture using the Batch F colours. Reference: V1A_REVIEW_READABLE.pdf page 5 (Kelvin shunt / local telemetry supply), page 6 (load output), and v2-00-circuit-boundary.png. Copy only this exact connectivity: VOUT_PROTECTED enters R401 force pin 1; a 2 mΩ resistance leaves force pin 4 as LOAD_5V1, which reaches J502 pin 1 (+). J502 pin 2 (RETURN) reaches GND. A branch BEFORE R401 goes to U402 pin 1 (IN); label it "Local telemetry supply". R401 is a four-terminal device: label "Sense pins 2/3 omitted; see Lesson 04" without inventing a connection. Use conventional electrical symbols and ample space for pin names. Label "Captured subset · PDF pages 5–6" and "Teaching excerpt — not for fabrication". Draw no external computer; this picture ends at J502.
```

MUST NOT show: the local supply after R401; J502 as a 40-pin Pi header; sense pins carrying load current; a new circuit bridging Sheet 03; physical validation.

Reject if: LOAD_5V1 and VOUT_PROTECTED are shorted around R401, or J502 return is absent.
