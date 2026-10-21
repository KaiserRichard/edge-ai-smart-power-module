"""Draw a simplified Sheet 03 circuit for lesson 03.

Run once:
    python3 -m pip install schemdraw
    python3 draw_sheet03_simplified.py
It writes ../images/p03-12-simplified-circuit.png next to the other vault images.

This is a TEACHING simplification of the readable schematic (V1A_REVIEW_READABLE.pdf,
pages 2-4). Refdes and net names match the schematic. The raw dump is drawn dashed
because it is frozen on paper only (Gate 4a) and not yet in KiCad.
"""
from pathlib import Path

import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).resolve().parent.parent / "images" / "p03-12-simplified-circuit.png"
ORANGE, BLUE, RED, GREY = "#E8590C", "#1971C2", "#C92A2A", "#868E96"

with schemdraw.Drawing(show=False, fontsize=11) as d:
    d.config(unit=2.5)

    # Input side: eFuse -> buck (fault: high-side switch shorted)
    efuse = d.add(elm.Ic(pins=[elm.IcPin("IN", side="left"), elm.IcPin("OUT", side="right"),
                                elm.IcPin("SHDN", side="bottom")],
                           size=(2, 1.5), label="U101\neFuse"))
    d.add(elm.Line().right().at(efuse.OUT).length(1.5).label("VIN_PROTECTED", loc="top", fontsize=9))
    hs = d.add(elm.Switch(action="close").right().color(RED).label("U201 high-side\nswitch (failed short)", loc="top", fontsize=9))
    sw = d.here
    d.add(elm.Inductor2().right().label("L201", loc="top"))
    raw = d.here
    d.add(elm.Line().right().length(1).color(ORANGE).label("VOUT_5V1 (raw)", loc="top", fontsize=9))
    node_raw = d.here

    # Raw bank capacitor
    d.push()
    d.add(elm.Capacitor().down().color(ORANGE).label("raw bank", loc="bottom", fontsize=9))
    d.add(elm.Ground())
    d.pop()

    # Raw dump: frozen on paper only (dashed)
    d.push()
    d.add(elm.Line().right().length(0.8).color(ORANGE))
    d.add(elm.Switch().down().color(GREY).linestyle("--").label("raw dump\n(not drawn yet)", loc="bottom", fontsize=9))
    d.add(elm.Ground().color(GREY))
    d.pop()

    # Back-to-back series pair Q301 / Q302 (sources joined at PROT_MID)
    d.add(elm.Line().right().length(1.6).color(ORANGE))
    q1 = d.add(elm.NFet(bulk=True).right().reverse().label("Q301", loc="top"))
    d.add(elm.Dot().label("PROT_MID", loc="bottom", fontsize=9))
    q2 = d.add(elm.NFet(bulk=True).right().label("Q302", loc="top"))
    d.add(elm.Line().right().length(1.2).color(BLUE).label("VOUT_PROTECTED", loc="top", fontsize=9))
    node_prot = d.here

    # Crowbar on the protected side: 33 mohm ballast + Q303 to GND
    d.push()
    d.add(elm.Resistor().down().color(BLUE).label("33 mΩ\nballast", loc="bottom", fontsize=9))
    d.add(elm.NFet().down().label("Q303\ncrowbar", loc="bottom", fontsize=9))
    d.add(elm.Ground())
    d.pop()

    # To the Pi through the shunt and J502
    d.add(elm.Line().right().length(1).color(BLUE))
    d.add(elm.ResistorIEC().right().color(BLUE).label("shunt R401", loc="top", fontsize=9))
    d.add(elm.Line().right().length(0.8).color(BLUE))
    d.add(elm.Dot(open=True).label("J502 → Pi", loc="right"))

    # Detector chain (below)
    d.add(elm.Line().at(node_raw).down().length(4.5).color(ORANGE))
    d.add(elm.Resistor().right().label("R301 11.3k / R302 10k\n→ OV_SENSE", loc="bottom", fontsize=9))
    cmp_ = d.add(elm.Opamp(leads=True).right().anchor("in1").label("U303", loc="center", fontsize=9))
    d.add(elm.Line().at(cmp_.in2).left().length(1).label("REF_2V5 (U302)", loc="left", fontsize=9))
    d.add(elm.Line().at(cmp_.out).right().length(1))
    latch = d.add(elm.Ic(pins=[elm.IcPin("D", side="left"), elm.IcPin("FAULT", side="right")],
                           size=(2, 1.2), label="U304\nlatch"))
    d.add(elm.Line().at(latch.FAULT).right().length(1.5).color(RED))
    d.add(elm.Label().label("FAULT → U101 SHDN, U301 (open Q301/Q302),\nU315 (crowbar ON), raw dump", color=RED, fontsize=9))

    d.save(str(OUT), dpi=200)

print(f"wrote {OUT}")
