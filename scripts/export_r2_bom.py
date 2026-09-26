#!/usr/bin/env python3
"""Export a review-only Markdown BOM from the actual KiCad XML netlist.

Unselected parts remain OPEN. This is not a purchase or fabrication BOM.
"""

import argparse
import hashlib
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def cell(value):
    return value.replace("|", "\\|").replace("\n", " ") or "OPEN"


def render(netlist):
    data = netlist.read_bytes()
    tree = ET.fromstring(data)
    components = tree.findall("./components/comp")
    components.sort(key=lambda c: (re.sub(r"\d", "", c.attrib["ref"]),
                                  int(re.search(r"\d+", c.attrib["ref"])[0])))
    lines = ["# V1A schematic review BOM", "",
             "**NOT FOR PROCUREMENT OR FABRICATION - R2 BLOCKED.**", "",
             f"Netlist SHA-256: `{hashlib.sha256(data).hexdigest()}`.", "",
             f"{len(components)} physical schematic entries (including test points), one row per reference. "
             "Nonphysical power flags are excluded by KiCad. Exact MPNs identify review candidates, "
             "not qualified substitutions. Blank MPNs and footprints are OPEN. "
             "The absent output-protection circuit is not included in this BOM.", "",
             "| Ref | Qty | Value | MPN / selection | Provisional footprint | Rating / limitation |",
             "| --- | ---: | --- | --- | --- | --- |"]
    for component in components:
        fields = {f.attrib["name"]: f.text or "" for f in component.findall("./fields/field")}
        values = [component.attrib["ref"], "1", component.findtext("value", ""),
                  fields.get("MPN", ""), component.findtext("footprint", ""), fields.get("Rating", "")]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    lines += ["", "Source/function/modification/rationale and qualification gates: "
              "[schematic review](../../../05_SCHEMATIC_REVIEW.md), "
              "[pin review](../PIN_AND_FOOTPRINT_REVIEW.md), "
              "[source register](../source_register.json).", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--netlist", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    with args.output.open("x") as output:
        output.write(render(args.netlist))
    print(f"Exported review BOM: {args.output}")


if __name__ == "__main__":
    main()
