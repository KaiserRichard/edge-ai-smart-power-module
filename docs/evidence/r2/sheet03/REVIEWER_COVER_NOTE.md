# V1A — request for senior laboratory engineering review

**PRELIMINARY — Sheet 03 BLOCKED — NOT FOR FABRICATION**  
30 September 2026

V1A is a standalone DC power module intended to supply a Raspberry Pi 5 through its GPIO power pins: **9–24 V input → fuse, reverse-polarity protection and eFuse → 5.1 V / 5 A buck → series output isolation and crowbar → current shunt/monitor → GPIO harness**. Voltage, current, power and energy telemetry use I2C. This is a preliminary schematic; protection performance has not been demonstrated in hardware. The review requirements are below 5.5 V during faults and at least 4.75 V at 5 A at the Pi.

The principal unresolved issues are:

- **Buck high-side short / energy:** A physically shorted switch defeats the 11.5 A limit. Saturation is 14 A typical; a 24 V model reaches 6.268 V / 503 A. Energy disposal is unqualified.
- **Protection timing:** At the calculated 6.175 V driver floor, partial action is **307 ns versus 300 ns allocated**, excluding settling/commutation. Maximum delay is OPEN.
- **Ballast temperature:** Assumed **125 °C terminals exceed the selected resistor's 95 °C rating by 30 °C**, before fault heating. Pulse survival remains OPEN.
- **Three margins:** All are OPEN: conditional **fault −768 mV; harness −89.5 mV** (4.660 V at 5 A); **false-trip −2.98 mV** at 30 µs. Small positive screens are unqualified.

These numbers are calculations with unqualified assumptions, not measured behavior. The fault model is a sensitivity study, not a prediction of achievable current. Schematic readability and connectivity checks do not resolve these issues.

Please advise:

1. How would you contain a buck high-side short while keeping a GPIO-fed Pi strictly below 5.5 V?
2. Would you accept a fuse-blowing crowbar? What source-energy, fuse-clearing and resistor/MOSFET pulse evidence would you require?
3. What clamp or recirculation path would you recommend for inductor energy when the output switches open?
4. What wire gauge, maximum length, connectors, GPIO pin sharing and ground-return practice would you require for 5 A?
5. What driver-supply qualification and current-limited dummy-load tests should precede any Pi connection?

Review basis: independent engineering review, revision `0677fea` (30 September 2026). [Detailed findings and assumptions](https://github.com/KaiserRichard/edge-ai-smart-power-module/blob/0677fea0a32fc87b740949d589abe1588e55934c/docs/evidence/r2/sheet03/GATE2C_REVIEW_CLOSURE.md). The accompanying schematic is for review only.
