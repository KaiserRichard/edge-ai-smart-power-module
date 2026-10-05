AMENDMENT 1 to Codex brief 02 (from Claude, conductor, 2026-09-29 11:27 UTC). Apply it to the rest of your work; do not redo committed tasks.

The user decided: the Raspberry Pi 5 fault limit is now 5.5 V at the Pi's 5 V rail, replacing the 6.0 V screening criterion. Basis: Raspberry Pi engineer guidance (4.75–5.5 V, transients must not exceed 5.5 V) and the fact that GPIO feeding bypasses the Pi's USB-C OVP; see draft PR #4, docs/evidence/r2/pi5_input_envelope_2026-09-29/ on branch codex/pi5-input-envelope. The user wants the design as conservative as possible.

Changes:
1. Acceptance criterion 2 becomes: the hard high-side short keeps the load <= 5.5 V at every corner, WITH explicit margin, and no re-enable while input is present. Report the margin in mV. Option I's model peak of 5.49 V leaves essentially none, so treat criterion 2 as FAIL for option I as currently sized unless your numbers show otherwise.
2. Add a margin study to your report: what it takes to get a meaningful margin below 5.5 V (state the margin you target and why). Evaluate at least: a lower detector threshold (and its effect on the nuisance-trip margin against load-release overshoot, criterion 1), faster trip-to-isolation (below 2 us), more raw-side bulk capacitance, and any other justified change. For each, give the peak, the margin, the nuisance-trip margin and the cost (parts, area, stress, start-up). Use the Python model; mark SPICE runs NOT RUN if ngspice is unavailable.
3. Evaluation only. Do not select or capture a new architecture; any architecture change needs the user's approval.
