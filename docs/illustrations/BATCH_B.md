# Batch B — Input protection and system context

Generate one image per prompt. Keep all component choices and limits OPEN unless expressly named below. Review labels and current direction before use.

## B1 — Input fault/timescale map (REGENERATE)

```text
Regenerate a readable technical infographic titled “Input Faults Need Different Responses”. Organize faults across fast, medium and sustained time scales: cable transient; undervoltage/overvoltage; reverse polarity/backfeed; startup inrush; excessive current; persistent short/thermal fault. Map functions, not part numbers: “TVS transient suppression — under reselection”, “reverse blocking”, “TPS26630 controlled current/startup and timed input isolation”, “fuse backup — not selected”. Add “Current input TVS and fuse are not selected” and “48 V → 24 V module is not selected”. Distinguish transient clamping from sustained overvoltage protection and distinguish electronic current limiting from a fuse. Never print D101 or F101. Avoid numerical thresholds or timing values. Use a clean horizontal time axis, large labels and simple functional blocks. This is conceptual and makes no qualification claim.
```

## B2 — Conceptual input protection placement (REPLACE)

```text
Create a top-down functional placement illustration, not a PCB render, titled “Input Protection Placement Principles”. Show only abstract blocks and short path lines: input connector; functional fuse location in the series path (part not selected); transient suppressor return located near input entry (device under reselection); reverse blocking; TPS26630 input limiter/isolation; buck input bank. Highlight a short transient return loop and a compact buck input-current loop. Show control/sense lines away from noisy power paths. Add exact footer “CONCEPTUAL — NO PCB ROUTED”. Do not draw copper pours, vias, packages or a realistic green board. Do not show selected part numbers, dimensions, trace widths or proven layout. White background, clear green/orange/red annotations, sparse readable text.
```

## B3 — Reverse polarity and backfeed teaching diagram (REPLACE)

```text
Create a three-panel generic functional diagram for “Reverse Polarity and Backfeed Are Different Cases”. Panels: “Correct input: forward power allowed”; “Reversed source: input path blocks”; “Output-side backfeed: reverse path behavior must be checked”. Use a generic back-to-back switch symbol only in the third panel and label “topology-dependent; verify body-diode paths”. Explain that an off MOSFET can still conduct through its body diode. Avoid Q101/Q102, specific device orientation, claims about the present captured circuit, and any unstated component identity. Use unambiguous arrows and do not imply a validated implementation. Crisp black/navy line drawing with one green and one red current arrow per relevant state; large labels.
```

## B4 — TPS26630 functional role and timing concept (REGENERATE)

```text
Draw a functional block diagram titled “TPS26630 — Input Control Functions in the Current Development Plan”. Show input → controlled pass path → protected input bank → buck. Inside the controller block label only: “UVLO”, “OVP”, “current limiting”, “controlled startup”, “fault status”. Add an external control arrow “timed input isolation — qualification required”. Annotate “settings and application response OPEN”; “input bank target 10–30 µF (development allocation, not qualified)”. Do not use old resistor values, thresholds, current limits, ramp times, or imply the input module is selected. Distinguish current control from hard isolation. Functional concept only; no pin-level claims. White background, readable blocks, exact concise text.
```

## B5 — Standalone V1A and future integration boundary (REPLACE)

```text
Create a scope diagram titled “V1A Is Standalone; Later Integration Has an Open Boundary”. Main box: “Project II V1A Smart Power Module” with functional labels “input protection”, “regulated 5 V”, “output fault protection”, “voltage/current/energy telemetry”, “test access”. Upstream show the current boundary “13S battery → PDB → bought isolated 48 V → 24 V module (not selected) → V1A”. To the side show a small dashed boundary “Future WBR integration — requirements and robot electrical architecture OPEN”. Make V1A the dominant subject and keep all future robotics blocks generic and outside the power module. No supercapacitor, 12 V bus, CAN, motor or D435i data path should be implied as part of V1A. Do not show a routed board. Clean high-contrast block diagram, precise short labels.
```
