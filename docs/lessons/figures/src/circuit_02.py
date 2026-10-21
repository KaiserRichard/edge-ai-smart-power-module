#!/usr/bin/env python3
"""Exact local feedback subset, review PDF p.3 OUTPUT / FEEDBACK.

This is the DC resistor branch only; C207/R205 are explicitly omitted.
Run: python3 -B docs/lessons/figures/src/circuit_02.py
"""
from circuit_drawing import Circuit, ORANGE, SENSE


def main():
    d = Circuit("02 · The buck senses its local raw output",
                "Review PDF page 3 · R202 / R203 → U201 FB pin 4")
    d.terminal(2.2, 5.7, "", side="left", color=ORANGE)
    d.wire((2.2, 5.7), (6, 5.7), (6, 5.4), color=ORANGE)
    d.text(3.9, 6.15, "VOUT_5V1 · L201 pin 2", color=ORANGE)
    d.resistor(6, 5.4, 6, 3.4, "R202 · 100 kΩ")
    d.text(5.7, 5.0, "1", size=8)
    d.text(5.7, 3.9, "2", size=8)
    d.node(6, 3.4, SENSE)
    d.resistor(6, 3.4, 6, 1.4, "R203 · 24.4 kΩ")
    d.text(5.7, 3.0, "1", size=8)
    d.text(5.7, 1.9, "2", size=8)
    d.ground(6, 1.4)
    d.wire((6, 3.4), (9.7, 3.4), color=SENSE)
    d.text(8.5, 3.8, "BUCK_FB", color=SENSE)
    d.terminal(9.7, 3.4, "U201 pin 4 · FB", side="right", color=SENSE)
    d.text(2.7, 3.2, "This tap is BEFORE\nSheet 03, R401\nand the harness.", size=12, color=ORANGE)
    d.save("v2-02-circuit-feedback.png",
           "DC feedback branch only. C207/R205 feedforward branch, L201, capacitors and other IC pins omitted.\n"
           "GND here is the same net as U201 AGND pin 3; physical return routing still needs layout review.")


if __name__ == "__main__":
    main()
