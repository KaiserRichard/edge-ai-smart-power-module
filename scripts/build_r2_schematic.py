#!/usr/bin/env python3
"""Reproduce the R2 review schematic from the reviewed block specifications.

This writes schematics and a symbol library only. It has no PCB/export/order
operations. Inspect the diff before regenerating after manual KiCad edits.
"""

import argparse
import json
from pathlib import Path
import re
import textwrap
import uuid


ROOT = Path(__file__).resolve().parents[1]
PROJECT = "V1A"
NAMESPACE = uuid.UUID("912b0a8d-5d32-4e13-9328-cf6f0c61f202")


def uid(key):
    return str(uuid.uuid5(NAMESPACE, key))


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def fx(size=1.27, justify="", hide=False):
    return (f"(effects (font (size {size} {size}))"
            + (f" (justify {justify})" if justify else "")
            + (" (hide yes)" if hide else "") + ")")


def prop(name, value, x=0, y=0, hide=False, size=1.27):
    return f"(property {q(name)} {q(value)} (at {x:g} {y:g} 0) {fx(size, hide=hide)})"


def normalize(raw):
    """Accept pin-number keyed tables; preserve source descriptions as metadata."""
    result = []
    for item in raw.get("components", []):
        c = dict(item)
        c.setdefault("part", c.get("mpn", c["value"]))
        c.setdefault("footprint", "")
        pins = {}
        for number, pin in c["pins"].items():
            if not isinstance(pin, dict):
                pin = {"net": pin}
            pin = dict(pin)
            pin.setdefault("name", str(number))
            pin.setdefault("type", "passive")
            pins[str(number)] = pin
        c["pins"] = pins
        c.setdefault("kind", {"R": "R", "C": "C", "L": "L", "F": "F"}.get(c["ref"][0], "IC"))
        result.append(c)
    return result


def line(x1, y1, x2, y2, width=0.254):
    return (f"(polyline (pts (xy {x1:g} {y1:g}) (xy {x2:g} {y2:g}))"
            f" (stroke (width {width:g}) (type default)) (fill (type none)))")


def library_symbol(c):
    """Author project-owned pin symbols directly from manufacturer pin tables."""
    name = c["ref"] + "_" + re.sub(r"[^A-Za-z0-9_]", "_", c["part"])
    c["symbol_name"] = name
    pins = c["pins"]
    simple = c["kind"] in ("R", "C", "L", "F", "D", "TVS") and len(pins) == 2
    c["simple"] = simple
    geometry = []
    locations = {}
    if c["kind"] in ("TP", "FLAG"):
        number = next(iter(pins))
        locations[number] = (0, 0, 90)
        if c["kind"] == "TP":
            geometry.append('(circle (center 0 3.175) (radius 0.635) (stroke (width 0.254) (type default)) (fill (type none)))')
        else:
            geometry += [line(-1.27, 2.54, 0, 3.81), line(0, 3.81, 1.27, 2.54), line(1.27, 2.54, -1.27, 2.54)]
        c["half_height"] = 3.81
    elif c["kind"] == "SHUNT":
        # Separate external force and sense terminals; connection is within the shunt.
        locations = {"1": (-12.7, 2.54, 0), "2": (-12.7, -5.08, 0),
                     "3": (12.7, -5.08, 180), "4": (12.7, 2.54, 180)}
        geometry.append('(rectangle (start -5.08 3.556) (end 5.08 1.524) (stroke (width 0.254) (type default)) (fill (type none)))')
        geometry += [line(-10.16, 2.54, -5.08, 2.54), line(5.08, 2.54, 10.16, 2.54),
                     line(-10.16, -5.08, -7.62, -5.08), line(-7.62, -5.08, -7.62, 2.54),
                     line(10.16, -5.08, 7.62, -5.08), line(7.62, -5.08, 7.62, 2.54)]
        c["half_height"] = 7.62
    elif simple:
        nums = list(pins)
        locations[nums[0]] = (-5.08, 0, 0)
        locations[nums[1]] = (5.08, 0, 180)
        if c["kind"] == "C":
            geometry += [line(-0.635, -2.54, -0.635, 2.54), line(0.635, -2.54, 0.635, 2.54)]
            geometry += [line(-2.54, 0, -0.635, 0), line(0.635, 0, 2.54, 0)]
            if c.get("polarized"):
                geometry += [line(-3.175, 2.54, -1.905, 2.54),
                             line(-2.54, 1.905, -2.54, 3.175)]
        elif c["kind"] in ("D", "TVS"):
            geometry += [line(-2.54, -2.54, -2.54, 2.54), line(-2.54, 0, 2.54, 2.54),
                         line(2.54, 2.54, 2.54, -2.54), line(2.54, -2.54, -2.54, 0)]
            if c["kind"] == "TVS":
                geometry += [line(-2.54, 2.54, -1.27, 2.54), line(-2.54, -2.54, -3.81, -2.54)]
        elif c["kind"] == "L":
            for i in range(4):
                ax = -2.54 + i * 1.27
                geometry.append(f'(arc (start {ax:g} 0) (mid {ax+0.635:g} 0.635) (end {ax+1.27:g} 0) (stroke (width 0.254) (type default)) (fill (type none)))')
        else:
            geometry.append("(rectangle (start -2.54 1.016) (end 2.54 -1.016) (stroke (width 0.254) (type default)) (fill (type none)))")
            if c["kind"] == "F":
                geometry.append(line(-2.54, 0, 2.54, 0))
        c["half_height"] = 3.81
    else:
        nums = list(pins)
        split = (len(nums) + 1) // 2
        height = max(7.62, (split + 1) * 2.54)
        c["half_height"] = height
        for i, number in enumerate(nums):
            side = 0 if i < split else 1
            row = i if side == 0 else i - split
            locations[number] = ((-22.86 if side == 0 else 22.86),
                                 (split - 1) * 2.54 - row * 5.08,
                                 (0 if side == 0 else 180))
        geometry.append(f"(rectangle (start -20.32 {height:g}) (end 20.32 {-height:g}) (stroke (width 0.254) (type default)) (fill (type background)))")
    c["pin_locations"] = locations
    pin_text = []
    for number, (x, y, angle) in locations.items():
        pin = pins[number]
        pin_text.append(f"(pin {pin['type']} line (at {x:g} {y:g} {angle}) (length 2.54)"
                        f" (name {q(pin['name'])} {fx(1.016)}) (number {q(number)} {fx(1.016)}))")
    physical = "no" if c["kind"] == "FLAG" else "yes"
    return (f"(symbol {q(name)} (pin_names (offset 0.762){' (hide yes)' if simple or c['kind'] in ('TP', 'FLAG') else ''})"
            f" (exclude_from_sim no) (in_bom {physical}) (on_board {physical})"
            f" {prop('Reference', re.sub('[0-9]', '', c['ref']))} {prop('Value', c['value'])}"
            f" {prop('Footprint', c['footprint'], hide=True)}"
            f" (symbol {q(name + '_0_1')} {' '.join(geometry)})"
            f" (symbol {q(name + '_1_1')} {' '.join(pin_text)}))")


class Sheet:
    def __init__(self, name, title, ports=None):
        self.name, self.title = name, title
        self.ports = ports or {}
        self.uuid = uid(name)
        self.parts, self.graphics, self.lib = [], [], []
        self.serial = 0

    def key(self):
        self.serial += 1
        return uid(f"{self.name}:{self.serial}")

    def text(self, content, x, y, size=1.27):
        self.graphics.append(f"(text {q(content)} (at {x:g} {y:g} 0) {fx(size, 'left top')} (uuid {q(self.key())}))")

    def wire(self, x1, y1, x2, y2):
        self.graphics.append(f"(wire (pts (xy {x1:g} {y1:g}) (xy {x2:g} {y2:g})) (stroke (width 0) (type default)) (uuid {q(self.key())}))")

    def label(self, net, x, y, right=False):
        # GND has an explicit hierarchical port on every functional sheet.
        self.graphics.append(f"(label {q(net)} (at {x:g} {y:g} {180 if right else 0}) {fx(1.016, 'right bottom' if right else 'left bottom')} (uuid {q(self.key())}))")

    def component(self, c, x, y):
        sym = library_symbol(c)
        self.lib.append(sym.replace(q(c["symbol_name"]), q("V1A:" + c["symbol_name"]), 1))
        sy = y - c["half_height"] - 6.35
        metadata = [prop("Reference", c["ref"], x, sy), prop("Value", c["value"], x, sy + 2.54, size=1.016),
                    prop("Footprint", c["footprint"], x, y, True), prop("MPN", c["part"], x, y, True),
                    prop("Source", c.get("source", "See block design review"), x, y, True),
                    prop("Rating", c.get("rating", "See block design review"), x, y, True)]
        physical = "no" if c["kind"] == "FLAG" else "yes"
        self.parts.append(f"(symbol (lib_id {q('V1A:' + c['symbol_name'])}) (at {x:g} {y:g} 0) (unit 1)"
                          f" (exclude_from_sim no) (in_bom {physical}) (on_board {physical}) (dnp no)"
                          f" (uuid {q(uid(c['ref']))}) {' '.join(metadata)}"
                          + " ".join(f"(pin {q(n)} (uuid {q(uid(c['ref'] + ':' + n))}))" for n in c["pins"])
                          + f" (instances (project {q(PROJECT)} (path {q('/' + uid('V1A') + '/' + self.uuid)} (reference {q(c['ref'])}) (unit 1)))))")
        for number, (px, py, angle) in c["pin_locations"].items():
            sx, sy = x + px, y - py
            net = c["pins"][number].get("net")
            if net is None:
                self.graphics.append(f"(no_connect (at {sx:g} {sy:g}) (uuid {q(self.key())}))")
                continue
            end = sx + (-5.08 if px < 0 else 5.08)
            self.wire(sx, sy, end, sy)
            self.label(net, end, sy, right=px < 0)

    def add_ports(self):
        for i, (net, direction) in enumerate(self.ports.items()):
            x = 35.56 + (i % 4) * 96.52
            y = 27.94 + (i // 4) * 7.62
            self.graphics.append(f"(hierarchical_label {q(net)} (shape {direction}) (at {x:g} {y:g} 0) {fx(1.016, 'left')} (uuid {q(self.key())}))")
            self.wire(x, y, x - 7.62, y)
            self.label(net, x - 7.62, y, True)

    def save(self, output):
        footer = ""
        if self.name == "V1A":
            footer = '(sheet_instances (path "/" (page "1")))'
        text = (f"(kicad_sch (version 20250114) (generator \"eeschema\") (generator_version \"9.0\")"
                f" (uuid {q(self.uuid)}) (paper \"A3\")"
                f" (title_block (title {q(self.title)}) (date \"2026-09-12\") (rev \"R2-BLOCKED\")"
                f" (company \"Edge AI Smart Power Module\")"
                f" (comment 1 \"NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED\")"
                f" (comment 2 \"R3 PCB LAYOUT BLOCKED\"))"
                f" (lib_symbols {' '.join(self.lib)}) {' '.join(self.parts)} {' '.join(self.graphics)} {footer})\n")
        (output / (self.name + ".kicad_sch")).write_text(text)


def block_sheet(spec, name, title, ports, notes, output):
    sheet = Sheet(name, title, ports)
    sheet.text(title, 15.24, 15.24, 2.032)
    sheet.add_ports()
    components = normalize(spec)
    large = [c for c in components if len(c["pins"]) > 2 or "position" in c]
    small = [c for c in components if c not in large]
    # Two columns of IC/pin tables leave the lower page for reference passives.
    cursor = [66.04, 66.04]
    for i, c in enumerate(large):
        if "position" in c:
            sheet.component(c, *c["position"])
            continue
        col = i % 2
        h = max(7.62, (((len(c["pins"]) + 1) // 2) + 1) * 2.54)
        cy = cursor[col] + h
        sheet.component(c, 106.68 + col * 195.58, cy)
        cursor[col] = cy + h + 20.32
    start = spec.get("passive_start", max(60.96, max(cursor)))
    for i, c in enumerate(small):
        sheet.component(c, 53.34 + (i % 5) * 76.2, start + (i // 5) * 25.4)
    end = start + ((len(small) - 1) // 5) * 25.4 + 10.16 if small else start
    if end > 250:
        raise ValueError(f"{name}: content ends at {end:.2f} mm; add functional sheet/adjust layout")
    wrapped = "\n".join(textwrap.fill(note, 158) for note in notes)
    sheet.text(wrapped, 15.24, max(end + 2.54, 236.22), 1.016)
    sheet.save(output)
    return sheet, components


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=ROOT / "docs/evidence/r2")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "hardware/kicad")
    args = parser.parse_args()
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        parser.error("Output directory must be empty: preserve existing/manual KiCad edits; generate elsewhere and review a diff.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    specs = {name: json.loads((args.spec_dir / (name + "_block.json")).read_text())
             for name in ("input", "buck", "output", "monitor", "io")}
    definitions = [
        ("input", "01_INPUT_PROTECTION", {"VIN_RAW": "input", "VIN_PROTECTED": "output", "BUCK_INPUT_PGOOD": "output", "GND": "passive"}),
        ("buck", "02_BUCK_5V", {"VIN_PROTECTED": "input", "BUCK_INPUT_PGOOD": "input", "VOUT_5V1": "output", "GND": "passive"}),
        ("output", "03_OUTPUT_PROTECTION", {"VOUT_5V1": "input", "VOUT_PROTECTED": "passive"}),
        ("monitor", "04_POWER_MONITOR", {"VOUT_PROTECTED": "input", "LOAD_5V1": "bidirectional", "3V3_HOST": "input", "SDA_HOST": "bidirectional", "SCL_HOST": "bidirectional", "GND": "passive"}),
        ("io", "05_IO_TEST", {"VIN_RAW": "output", "VIN_PROTECTED": "input", "LOAD_5V1": "bidirectional", "3V3_HOST": "output", "SDA_HOST": "bidirectional", "SCL_HOST": "bidirectional", "GND": "passive"}),
    ]
    built, all_components = [], []
    for key, name, ports in definitions:
        spec = specs[key]
        sheet, components = block_sheet(spec, name, name.replace("_", " "), ports,
                                        spec.get("schematic_notes", []), args.output_dir)
        built.append(sheet)
        all_components.extend(components)
    # Parent sheet uses repeated local labels only for the two ancillary buses.
    top = Sheet("V1A", "00 TOP - V1A Smart DC Power Module")
    top.text("00 TOP | 9-24 V DC -> 5.1 V nominal / 5 A", 15.24, 15.24, 2.54)
    top.text("R2 REVIEW DRAFT | NOT FOR FABRICATION | R3 PCB LAYOUT BLOCKED", 15.24, 25.4, 1.524)
    positions = [(45.72, 63.5), (172.72, 63.5), (299.72, 63.5), (172.72, 152.4), (299.72, 152.4)]
    for page, (sheet, (x, y)) in enumerate(zip(built, positions), 2):
        pins = []
        for i, (net, direction) in enumerate(sheet.ports.items()):
            py = y + 12.7 + i * 7.62
            pins.append(f"(pin {q(net)} {direction} (at {x:g} {py:g} 180) {fx(1.016, 'left')} (uuid {q(uid(sheet.name + ':' + net))}))")
            top.wire(x, py, x - 7.62, py)
            top.label(net, x - 7.62, py, True)
        top.graphics.append(f"(sheet (at {x:g} {y:g}) (size 101.6 66.04) (stroke (width 0.254) (type solid)) (fill (color 0 0 0 0)) (uuid {q(sheet.uuid)})"
                            + prop("Sheetname", sheet.name, x + 50.8, y - 2.54, size=1.27)
                            + prop("Sheetfile", sheet.name + ".kicad_sch", x + 50.8, y + 68.58, size=1.016)
                            + " ".join(pins)
                            + f" (instances (project \"V1A\" (path {q('/' + top.uuid)} (page {q(page)})))))")
        summaries = {"01_INPUT_PROTECTION": "TPS26630 + reverse-blocking FETs",
                     "02_BUCK_5V": "LM61460 | 400 kHz | 5.1 V / 5 A",
                     "03_OUTPUT_PROTECTION": "OPEN CIRCUIT - NO BYPASS FITTED",
                     "04_POWER_MONITOR": "INA228 + 2 mOhm Kelvin shunt",
                     "05_IO_TEST": "Input / load / host / test access"}
        top.text(summaries[sheet.name], x + 12.7, y + 58.42, 1.27)
    top.text("POWER PATH\nInput protection -> buck\n-> OPEN disconnect\n-> Kelvin shunt -> load\n\nSheet 03 has no bypass.\nR2 RELEASE: BLOCKED\n\nI2C: 3.3 V, 100 kHz\nNo MCU; V1B separate.", 20.32, 157.48, 1.27)
    top.text("REVIEW: docs/05_SCHEMATIC_REVIEW.md | docs/R2_MANAGER_PACKET.md\nSOURCE / PIN / CALCULATION EVIDENCE: docs/evidence/r2/\nNo PCB, placement, routing or fabrication outputs. ERC does not establish electrical validity.", 20.32, 243.84, 1.27)
    top.save(args.output_dir)
    symbols = [library_symbol(c) for c in all_components]
    (args.output_dir / "V1A.kicad_sym").write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor") ' + " ".join(symbols) + ")\n")
    (args.output_dir / "sym-lib-table").write_text('(sym_lib_table (version 7) (lib (name "V1A") (type "KiCad") (uri "${KIPRJMOD}/V1A.kicad_sym") (options "") (descr "R2 review pin symbols; unresolved parts explicitly marked")))\n')
    (args.output_dir / "V1A.kicad_pro").write_text(json.dumps({"meta": {"filename": "V1A.kicad_pro", "version": 1},
        "net_settings": {"classes": [], "meta": {"version": 3}}, "erc": {"erc_exclusions": [], "meta": {"version": 0}},
        "sheets": [[uid("V1A"), "00_TOP"]] + [[s.uuid, s.name] for s in built],
        "text_variables": {"RELEASE_STATUS": "NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED"}}, indent=2) + "\n")
    print(f"Captured {len(all_components)} components on {len(built) + 1} sheets. No PCB created.")


if __name__ == "__main__":
    main()
