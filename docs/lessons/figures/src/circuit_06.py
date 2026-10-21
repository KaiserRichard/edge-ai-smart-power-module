#!/usr/bin/env python3
"""Exact two local bypass connections, review PDF page 3.

Circuit connectivity only: no physical placement, loop area or PCB dimensions.
Run: python3 -B docs/lessons/figures/src/circuit_06.py
"""
from circuit_drawing import Circuit, PURPLE


def main():
    d = Circuit("06 · Read both VIN / PGND pairs before thinking about layout",
                "Review PDF page 3 · INPUT / ENABLE capacitors → BUCK CONVERTER pins")
    for x, ref, vin, gnd in [(2.1, "C203", "8 · VIN1", "9 · PGND1"),
                              (8.5, "C204", "12 · VIN2", "11 · PGND2")]:
        d.capacitor(x, 5.1, 2.4, f"{ref}\n100 nF\n50 V", side=-1)
        d.text(x+.27, 4.6, "1", size=8)
        d.text(x+.27, 2.95, "2", size=8)
        d.wire((x, 5.1), (x+2.1, 5.1), color=PURPLE)
        d.terminal(x+2.1, 5.1, "", side="right", color=PURPLE)
        d.text(x+2.1, 5.63, f"U201 pin {vin}", size=10, color=PURPLE)
        d.text(x+1.0, 6.15, "VIN_PROTECTED", size=10, color=PURPLE)
        d.wire((x, 2.4), (x+2.1, 2.4))
        d.terminal(x+2.1, 2.4, "", side="right")
        d.text(x+2.1, 1.91, f"U201 pin {gnd}", size=10)
        d.ground(x, 2.4)
    d.text(7, .65, "Same named supply and ground nets · two local bypass connections", size=11)
    d.save("v2-06-circuit-bypass.png",
           "C201/C202 input bank, U201 internal switches and all other pins omitted.\n"
           "Schematic connectivity only: spacing here is NOT PCB geometry. AGND pin 3 must join both PGND nets.")


if __name__ == "__main__":
    main()
