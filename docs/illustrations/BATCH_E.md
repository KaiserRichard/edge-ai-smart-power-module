# Batch E — Component behavior, conceptual layout and bring-up

Generate one image per prompt. These prompts must not make a paper calculation look like a qualification result.

## E1 — Capacitor behavior and effective capacitance (REGENERATE)

```text
Create a general teaching infographic titled “A Ceramic Capacitor’s Nominal Value Is Not Its Effective Value”. Explain ideal C versus real C with ESR and ESL; show a conceptual DC-bias curve; show how parallel capacitors add nominal capacitance while actual effective capacitance depends on bias, tolerance, temperature, aging and frequency. Do not include any current V1A bank count or effective-C number. Include “Use the exact manufacturer curve and operating conditions”. Use generic capacitors, no part number, no fake precision. Clean high-contrast plots and short, exact labels.
```

## E2 — LM61460 placement principles (REGENERATE)

```text
Create a generic LM61460 power-stage placement concept with the IC, local ceramic input capacitors at VIN/PGND, a short switching loop, SW node, inductor and output capacitor bank. Highlight separate zones: “high di/dt switching”, “high DC current”, “sensitive feedback”. Show feedback sensing at the regulated output and routed away from SW. Label “L201: 10 µH alloy candidate; not selected”. Add “CONCEPTUAL — NO PCB ROUTED” and “Check exact pinout, footprint and layout against current datasheet and captured schematic”. Do not show a fabricated board, fixed package geometry, exact capacitor count/value, trace width or placement dimensions. Clean technical vector diagram with clear labels and no fake precision.
```

## E3 — Protection states and fault response (REPLACE)

```text
Create a state diagram for Sheet 03 architecture D: “Normal”; “Fault detected”; “Fault latched”; “Series disconnect commanded off”; “Crowbar/absorber event”; “Bench measurements recorded”; “Manual review before re-arm”. Show detector/latch chain as “REF5025 → TLV3201 → 74LVC1G74 → LTC7001”; series devices as “2 × BSC034N06, back-to-back”. State that actual timing, source energy, clamp behavior and voltage margins remain OPEN. Include exact banner “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)” and footer “Dummy load only — Pi disconnected”. Do not include the unselected Option E architecture, supercapacitor backup, software shutdown, or invented fault waveforms. Planned concept only, not validated operation.
```

## E4 — PCB layout principles without implying a routed board (REGENERATE)

```text
Create a conceptual teaching illustration titled “Layout Principles to Apply After the PCB Is Routed”. Use four abstract mini-diagrams: compact buck switching loop; short high-current path; Kelvin sense pair taken from shunt sense terminals; thermal path from power parts into copper. Add a bold banner “CONCEPTUAL — NO PCB ROUTED”. Do not show a completed board, fixed layer stack, trace width, via count, component coordinates or an actual approved routing. Avoid naming unselected packages. Label the rules as design principles requiring review against the selected components and manufacturer layout guidance. Keep each panel uncluttered and technically legible.
```

## E5 — Safe bring-up and characterization (REGENERATE)

```text
Create a vertical seven-step bring-up flow titled “V1A Validation — Dummy Load Before SBC”. Steps exactly: “1 Visual inspection”; “2 Continuity and short checks”; “3 Current-limited bench supply”; “4 No-load startup and output check”; “5 Low-current dummy load, then increasing load”; “6 Ripple, transient, thermal and fault tests”; “7 Telemetry checks, then SBC integration”. Draw steps 1–6 around a generic test board and dummy load with multimeter, oscilloscope, current probe and temperature instrument. Show Raspberry Pi only in step 7, behind a clear gate marked “only after previous tests pass”. For Sheet 03, include “PRELIMINARY V1A SHEET-03 ARCHITECTURE (TEST BOARD)”. Do not supply pass thresholds, test results or safety claims. No Pi in the fault-test setup. Crisp white-background process diagram, large exact text.
```
