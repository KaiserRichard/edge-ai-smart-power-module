#!/usr/bin/env python3
"""Exact J502/J503 electrical connections from review PDF page 6.

Connector rectangles are logical symbols, not mating-face/pin-layout drawings.
Run: python3 -B docs/lessons/figures/src/circuit_05.py
"""
from circuit_drawing import Circuit, BLUE, SENSE, WIRE


def main():
    d = Circuit("05 · Power and host telemetry leave on different connectors",
                "Review PDF page 6 · LOAD OUTPUT / J502 and HOST I2C / J503")
    d.text(3.4, 6.2, "J502 · two power terminals", color=BLUE)
    d.box(1.4, 2.3, 2.2, 2.8, "", color=BLUE)
    for y, pin, net in [(4.6, "1  +", "LOAD_5V1"), (2.9, "2  RETURN", "GND")]:
        color = WIRE if net == "GND" else BLUE
        d.text(3.4, y, pin, size=10, ha="right", color=color)
        d.wire((3.6, y), (6.0, y), color=color)
        d.terminal(6.0, y, "", side="right", color=color)
        d.text(4.8, y+.4, net, size=10, color=color)
    d.text(3.5, 1.5, "External power harness\nis beyond these terminals", size=10)
    d.text(10.5, 6.2, "J503 · host I2C interface", color=SENSE)
    d.box(10.3, 2.2, 2.5, 3.5, "", color=SENSE)
    for y, pin, net in [(5.1, "1  GND", "GND"), (4.3, "2  VREF", "3V3_HOST"),
                        (3.5, "3  SDA", "SDA_HOST"), (2.7, "4  SCL", "SCL_HOST")]:
        color = WIRE if net == "GND" else SENSE
        d.text(10.5, y, pin, size=10, ha="left", color=color)
        d.wire((8.2, y), (10.3, y), color=color)
        d.terminal(8.2, y, "", side="left", color=color)
        d.text(9.15, y+.30, net, size=10, color=color)
    d.text(10.5, 1.5, "VREF belongs to the host;\nit is not a 5 V output", size=10)
    d.save("v2-05-circuit-connectors.png",
           "Logical pin connections only; test points and power flags omitted. GND is common to both connectors.\n"
           "J502/J503 pin numbers are NOT Pi physical-header numbers. No external harness geometry is specified.")


if __name__ == "__main__":
    main()
