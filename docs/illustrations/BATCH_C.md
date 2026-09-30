# Batch C — Buck states, waveforms and magnetic selection

Generate one image per prompt. Electrical state arrows and signs are the main review risk; preserve exact directions and statements.

## C1 — Buck high-side MOSFET on (REPLACE)

```text
Draw a correct synchronous buck “State 1 — High-Side MOSFET ON” teaching diagram. Topology: VIN feeds the high-side switch; the switch node feeds the inductor; inductor feeds VOUT and load; low-side switch is OFF; the return closes through ground and output capacitor/load. Show conventional inductor current flowing from switch node through L to output, and show inductor current increasing during this state. Label inductor voltage with left-to-right polarity “VL = VIN − VOUT > 0” and the relation “positive VL → positive dI/dt” under passive sign convention. This diagram must be electrically self-consistent. Do not reuse reverse-protection MOSFET symbols. Avoid exact component values and avoid claiming a specific selected converter topology beyond generic synchronous buck. Clean black/navy circuit lines and one green current path; sparse text.
```

## C2 — Buck low-side/freewheel state (REPLACE)

```text
Draw a correct synchronous buck “State 2 — Low-Side MOSFET ON” teaching diagram. High-side switch OFF; low-side switch ON; switch node near ground; inductor current continues in the same left-to-right direction through L into the output/load and returns through ground/low-side device. Show inductor current decreasing but still supplying the load. With left-to-right inductor voltage polarity, label “VL = VSW − VOUT ≈ −VOUT < 0” and “negative VL → negative dI/dt”. Make clear that the current does not reverse instantly. Do not show a contradictory positive current slope. Generic topology only, no selected part numbers or numeric operating values. Clean circuit drawing with blue current loop and large exact labels.
```

## C3 — Buck cycle waveforms (REGENERATE)

```text
Create four aligned time plots for a synchronous buck in continuous-conduction mode: high-side gate, switch-node voltage, inductor voltage, and inductor current. High-side ON: switch node high, VL positive, IL ramps upward. High-side OFF / low-side ON: switch node near ground, VL negative, IL ramps downward while remaining positive. Keep all edge alignment consistent. Show output ripple only as a small illustrative trace, not a specified V1A limit. If using a numeric example, label it “illustrative only”; otherwise omit numbers. Correctly use “positive VL → positive dIL/dt” and “negative VL → negative dIL/dt”. Do not place contradictory arrows or slopes. Clean technical plot, white background, axes and legends large enough to read.
```

## C4 — 10 µH alloy inductor selection (REPLACE)

```text
Create a selection-tradeoff illustration titled “L201 — 10 µH Alloy Candidate Under Qualification”. Show a generic through-hole alloy power inductor silhouette and a conceptual L-versus-current curve. Label “10 µH alloy candidate”; “Würth 74437636351002 — candidate, not selected”; “hot/lot Ldiff envelope OPEN”; “ripple, peak current, DCR, temperature and footprint all matter”. Include a side note: “Do not infer guaranteed saturation behavior from a typical curve”. Do not show the old 6.8 µH XAL8080 as the current design. Do not invent a guaranteed saturation current, DCR, current rating or temperature rise. Avoid duplicate panel numbering. Clear sparse technical illustration, not a product datasheet recreation.
```

## C5 — Buck power flow and both states (REGENERATE)

```text
Create a four-panel buck-converter teaching diagram: (a) generic synchronous buck power path; (b) high-side-on current path; (c) low-side-on freewheel path; (d) aligned switch-node, inductor-voltage and inductor-current waveforms. Ensure the two state panels and plot agree exactly: high side ON means positive inductor voltage and rising current; low side ON means negative inductor voltage and falling current, with current remaining positive in CCM. Label the 5 V converter in V1A as a block only; mark “L201: 10 µH alloy candidate; qualification OPEN”. Use no specific capacitance bank or measured ripple value. Bottom note: “Conceptual operating principle — not a final circuit or PCB layout”. Strong contrast, clean vector lines, legible labels, no visual clutter.
```
