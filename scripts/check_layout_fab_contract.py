#!/usr/bin/env python3
"""Compare layout-owned rules with the owner's read-only fabprep contract.

This checks exact constraint/predicate equivalence, including rule order.
It is not a substitute for native DRC or an electrical spacing review.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from make_schematic_readable import parse, val


def normalized(path):
    # Wrap the multiple top-level KiCad rule expressions in one parse tree.
    text = re.sub(r"(?m)^\s*#.*$", "", path.read_text())
    tree = parse("(rules " + text + ")")
    result = []
    for entry in tree[1:]:
        if entry[0] != "rule":
            result.append(entry)
            continue
        clauses = []
        for clause in entry[2:]:
            if clause[0] == "condition":
                condition = val(clause[1])
                # Only commute simple ORs of atomic exact net-name tests.
                if "||" in condition and all(
                    re.fullmatch(r"[AB]\.NetName == '[^']+'", part.strip())
                    for part in condition.split("||")
                ):
                    condition = sorted(part.strip() for part in condition.split("||"))
                clauses.append(["condition", condition])
            else:
                clauses.append(clause)
        result.append(clauses)
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("reference", type=Path)
    ap.add_argument("--local", type=Path, default=Path("hardware/kicad/V1A.kicad_dru"))
    args = ap.parse_args()
    equal = normalized(args.local) == normalized(args.reference)
    print(json.dumps({
        "status": "PASS" if equal else "FAIL",
        "meaning": "Rule predicates, constraints and order exactly match after ignoring names and commuting simple net-name OR terms.",
        "local": str(args.local), "local_sha256": digest(args.local),
        "reference": str(args.reference), "reference_sha256": digest(args.reference),
        "limitations": "Does not establish fabrication acceptance or electrical safety; native DRC must also pass.",
    }, indent=2))
    raise SystemExit(0 if equal else 1)
