#!/usr/bin/env python3
"""Exact UVLO/OVP sensing subset of review PDF page 2; not the power path.

Run: python3 -B docs/lessons/figures/src/circuit_01.py
Only captured resistors and U101 input-pin endpoints are redrawn.
"""
from circuit_drawing import Circuit, PURPLE, SENSE


def main():
    d = Circuit("01 · Two dividers watch the fused input",
                "Review PDF page 2 · UVLO / OVP DIVIDERS → U101 TPS26630")
    d.wire((2, 5.6), (9, 5.6), color=PURPLE)
    d.text(5.5, 6.05, "VIN_FUSED · voltage-sense branches, not the load-current path", size=11, color=PURPLE)
    for x, top, bottom, target in [
        (2, "R101 · 332 kΩ", "R102 · 54.9 kΩ", "U101 pin 6 · UVLO"),
        (9, "R103 · 348 kΩ", "R104 · 15.8 kΩ", "U101 pin 7 · OVP"),
    ]:
        d.node(x, 5.6, PURPLE)
        d.resistor(x, 5.6, x, 3.5, top)
        d.text(x-.28, 5.1, "1", size=8)
        d.text(x-.28, 4.0, "2", size=8)
        d.node(x, 3.5, SENSE)
        d.resistor(x, 3.5, x, 1.4, bottom)
        d.text(x-.28, 3.0, "1", size=8)
        d.text(x-.28, 1.9, "2", size=8)
        d.wire((x, 3.5), (x+2.0, 3.5), color=SENSE)
        d.terminal(x+2.0, 3.5, "", side="right", color=SENSE)
        d.text(x+2.0, 3.05, target, size=10, color=SENSE)
        d.ground(x, 1.4)
    d.save("v2-01-circuit-dividers.png",
           "U101 power pins, Q101/Q102, fuse/TVS, SHDN, ILIM and startup circuitry omitted.\n"
           "The PDF's old input-range/TVS/fuse labels are historical; current normal input is 9–26 V.")


if __name__ == "__main__":
    main()
