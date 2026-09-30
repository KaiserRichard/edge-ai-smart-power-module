#!/usr/bin/env python3
"""Captured bench-access nets, PDF p.6 (U101 OUT reached by net name on p.2).

Voltage test points are not source-current sensors or fault-force terminals.
Run: python3 -B docs/lessons/figures/src/circuit_07.py
"""
from circuit_drawing import Circuit, BLUE, PURPLE, WIRE


def main():
    d = Circuit("07 · Four captured voltage-test nets",
                "Review PDF page 6 · DC INPUT / LOAD OUTPUT / BENCH TEST ACCESS")
    rows = [
        (5.5, "J501 pin 1 (+)", "VIN_RAW", "TP501", PURPLE),
        (4.1, "U101 OUT pins 17/18\n(page 2)", "VIN_PROTECTED", "TP502", PURPLE),
        (2.7, "J502 pin 1 (+)", "LOAD_5V1", "TP503", BLUE),
        (1.3, "J501 pin 2 / J502 pin 2\nRETURN", "GND", "TP504", WIRE),
    ]
    for y, origin, net, tp, color in rows:
        d.terminal(4.2, y, "", side="left", color=color)
        d.text(4.0, y, origin, size=10, ha="right", color=color)
        d.wire((4.2, y), (11.5, y), color=color)
        d.text(6.5, y+.35, net, size=11, color=color)
        d.node(9.2, y, color)
        d.wire((9.2, y), (9.2, y+.57), color=color)
        d.terminal(9.2, y+.57, f"{tp} pin 1", side="right", color=color)
    d.save("v2-07-circuit-test-nets.png",
           "Four separate nets; the circuit between them is deliberately omitted. TP502 is a voltage tap, not a current sensor.\n"
           "Raw/protected 5 V points are TP301/TP302 on page 4. No far-end, injector or force-link wiring is captured here.")


if __name__ == "__main__":
    main()
