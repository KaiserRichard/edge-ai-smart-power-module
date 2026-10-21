#!/usr/bin/env python3
"""Exact differential-filter and VBUS excerpt from review PDF page 5.

R401's force element and U401's supply/digital pins are omitted explicitly.
Run: python3 -B docs/lessons/figures/src/circuit_04.py
"""
from circuit_drawing import Circuit, SENSE, BLUE


def main():
    d = Circuit("04 · Two sense inputs, plus a separate bus-voltage tap",
                "Review PDF page 5 · KELVIN SHUNT / MEASUREMENT")
    for y, pin, net, ref, icpin in [
        (5.4, 2, "SHUNT_KPLUS", "R402", "10 · IN+"),
        (2.9, 3, "SHUNT_KMINUS", "R403", "9 · IN−"),
    ]:
        d.terminal(1.8, y, "", side="left", color=SENSE)
        d.text(1.8, y+.62, f"R401 sense pin {pin}\n{net}", size=10, color=SENSE)
        d.wire((1.8, y), (3.2, y), color=SENSE)
        d.resistor(3.2, y, 6.4, y, f"{ref} · 10 Ω", color=SENSE)
        d.text(4.1, y-.32, "1", size=8)
        d.text(5.5, y-.32, "2", size=8)
        d.wire((6.4, y), (12, y), color=SENSE)
        d.node(8, y, SENSE)
        d.terminal(12, y, "", side="right", color=SENSE)
        d.text(11.2, y+.46, f"U401 pin {icpin}", size=10, color=SENSE)
    d.capacitor(8, 5.4, 2.9, "C401\n100 nF")
    d.text(7.65, 4.75, "1", size=8)
    d.text(7.65, 3.55, "2", size=8)
    d.text(4.5, 4.1, "Sense pair only:\nno load-current path", size=10)
    d.wire((1.8, 1.15), (12, 1.15), color=BLUE)
    d.terminal(1.8, 1.15, "", side="left", color=BLUE)
    d.terminal(12, 1.15, "", side="right", color=BLUE)
    d.text(3.1, 1.72, "LOAD_5V1 · R401 force pin 4", size=10, color=BLUE)
    d.text(10.8, 1.72, "U401 pin 8 · VBUS", size=10, color=BLUE)
    d.save("v2-04-circuit-sense-filter.png",
           "C401 is between IN+ and IN−, not to ground. VBUS is a separate tap on the load-side force net.\n"
           "R401 force element, U401 supply/GND/digital pins and local-supply branch omitted; see full page 5.")


if __name__ == "__main__":
    main()
