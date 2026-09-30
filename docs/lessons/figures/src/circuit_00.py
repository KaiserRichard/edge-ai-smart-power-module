#!/usr/bin/env python3
"""Review PDF pp.5–6: exact force path and upstream local-supply branch.

Run from any directory: python3 -B /path/to/circuit_00.py
The Kelvin observation connections are deliberately omitted, never shorted.
"""
from circuit_drawing import Circuit, BLUE, SENSE

def main():
    d=Circuit("00 · Find the measurement boundary on the real circuit",
              "Review PDF page 5: R401 and U402 · page 6: J502")
    d.terminal(1.8,5,"VOUT_PROTECTED",side="right",color=BLUE)
    d.wire((1.8,5),(1.8,4),(4,4),color=BLUE)
    d.resistor(4,4,8,4,"R401 · 2 mΩ\nforce pin 1 → force pin 4",color=BLUE)
    d.wire((8,4),(11,4),color=BLUE)
    d.node(8.5,4,BLUE)
    d.text(9.5,4.65,"LOAD_5V1",color=BLUE)
    d.terminal(11,4,"J502 pin 1 (+)",side="right",color=BLUE)
    d.terminal(11,1.6,"J502 pin 2 (RETURN)",side="right")
    d.wire((11,1.6),(2.6,1.6))
    d.ground(2.6,1.6)
    d.node(3.5,4)
    d.wire((3.5,4),(3.5,2.7),(5.2,2.7),color=SENSE)
    d.terminal(5.2,2.7,"U402 pin 1 (IN)",side="right",color=SENSE)
    d.text(7.2,2.05,"Local telemetry supply branches BEFORE R401",size=10,color=SENSE)
    d.save("v2-00-circuit-boundary.png",
           "R401 sense pins 2/3 and U401 are omitted here; see Lesson 04. J502 is the module connector, not the Pi header.")

if __name__ == "__main__": main()
