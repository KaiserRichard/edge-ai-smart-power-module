#!/usr/bin/env python3
"""Exact input boundary: review PDF p.6 J501, p.2 F101/C101.

No upstream converter circuit or new isolation/ground-bond arrangement is drawn.
Run: python3 -B docs/lessons/figures/src/circuit_08.py
"""
from matplotlib.patches import Rectangle
from circuit_drawing import Circuit, PURPLE


def main():
    d = Circuit("08 · The robot supply stops at this V1A input boundary",
                "Review PDF page 6: J501 · page 2: F101 and C101")
    d.terminal(2.3, 4.9, "", side="left", color=PURPLE)
    d.text(2.8, 5.45, "J501 pin 1 (+)", size=10, color=PURPLE)
    d.wire((2.3, 4.9), (5.5, 4.9), color=PURPLE)
    d.text(4.1, 4.4, "VIN_RAW", size=10, color=PURPLE)
    # IEC fuse: rectangle with the through-line, not a resistor symbol.
    d.ax.add_patch(Rectangle((5.5, 4.7), 1.4, .4, facecolor="white",
                            edgecolor=PURPLE, lw=1.7))
    d.wire((5.5, 4.9), (6.9, 4.9), color=PURPLE)
    d.text(6.2, 5.6, "F101 · fuse", color=PURPLE)
    d.text(5.25, 5.2, "1", size=8)
    d.text(7.15, 5.2, "2", size=8)
    d.wire((6.9, 4.9), (11.3, 4.9), color=PURPLE)
    d.text(9.2, 5.45, "VIN_FUSED", color=PURPLE)
    d.node(10.3, 4.9, PURPLE)
    d.capacitor(10.3, 4.9, 2.1, "C101\n1 µF · 100 V")
    d.text(9.98, 4.2, "1", size=8)
    d.text(9.98, 2.75, "2", size=8)
    d.terminal(2.3, 2.1, "", side="left")
    d.text(3.0, 1.5, "J501 pin 2 (RETURN)", size=10)
    d.wire((2.3, 2.1), (10.3, 2.1))
    d.ground(10.3, 2.1)
    d.text(5.8, 3.2, "Upstream converter and robot\nare outside the captured circuit", size=11)
    d.save("v2-08-circuit-input-boundary.png",
           "Subset only: TVS D101, Q101/Q102, U101, auxiliary branch and test points omitted.\n"
           "F101 is labelled OPEN in this PDF; current owner selection is Schurter 3403.0285.23, not installed qualification.")


if __name__ == "__main__":
    main()
