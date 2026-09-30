#!/usr/bin/env python3
"""J502 acceptance-budget arithmetic, not an electrical qualification test.

Run with --check to verify the checked-in result. All proposed hot limits are
allocations; an unqualified application maximum is deliberately null.
"""
import argparse
import json
import math
from pathlib import Path


def calculate():
    source_min = 5.026143254670701  # pinned PATH_BUDGET hot feedback screen
    current = 5.0
    wire_factor = 1.10 * (1 + 0.00393 * (60 - 20))

    def wire_mohm(dcr_ohm_per_1000ft, length_m, parallel=1):
        return dcr_ohm_per_1000ft / 304.8 * length_m * 1000 * wire_factor / parallel

    rows = [
        ("unsensed_buck_copper", 0.5, 0.5),
        ("module_FET_pair_proposed", 6.0, 0.0),
        ("shunt_2mohm_1pct_25ppm_100C", 2 * 1.01 * (1 + 25e-6 * 75), 0.0),
        ("module_PCB", 1.0, 1.0),
        ("J502_A_complete_pole", 3.12, 3.12),
        ("AWG16_trunk_75mm", wire_mohm(4, .075), wire_mohm(4, .075)),
        ("AWG20_fanout_15mm_35mm", wire_mohm(9.8, .015, 2), wire_mohm(9.8, .035, 8)),
        ("Pi_mate_and_female_crimp_combined", 20 / 2, 20 / 8),
        ("Pi_male_attachment", .24, .06),
        ("fanout_splices", .5, .5),
        ("module_solder_joints", .1, .1),
    ]
    options = {}
    for name, board_pole in [("A_TE_Phoenix", 3.12), ("B_TE_MiniFitSr_gold", 4.0)]:
        items = [dict(element=n, send_mohm=s, return_mohm=r) for n, s, r in rows]
        items[4] = dict(element="J502_complete_pole_including_termination",
                        send_mohm=board_pole, return_mohm=board_pole)
        send = sum(x["send_mohm"] for x in items)
        ret = sum(x["return_mohm"] for x in items)
        d_loop = send + ret
        variants = {}
        for architecture, extra in [("D", 0), ("E", 10)]:
            loop = d_loop + extra
            variants[architecture] = dict(
                loop_mohm=loop,
                drop_mV=current * loop,
                path_loss_W=current**2 * loop / 1000,
                Pi_static_V=source_min - current * loop / 1000,
                Pi_20mV_trough_V=source_min - .020 - current * loop / 1000,
                Pi_100mV_total_excursion_V=source_min - .100 - current * loop / 1000,
                margin_20mV_mV=(source_min - .020 - current * loop / 1000 - 4.75) * 1000,
                Pi_20mV_with_old_13p6mohm_FET_pair_V=source_min - .020 - current * (loop + 7.6) / 1000,
                actual_qualified_hot_min_V=None,
            )
        options[name] = dict(items=items, send_mohm=send, return_mohm=ret, results=variants)

    # Independent branch-network cross-check: explicitly parallel ten branches,
    # rather than using the equivalent-resistance expressions above.
    positive_branch = wire_mohm(9.8, .015) + 20 + .48
    ground_branch = wire_mohm(9.8, .035) + 20 + .48
    parallel = lambda resistances: 1 / sum(1 / r for r in resistances)
    network = parallel([positive_branch] * 2) + parallel([ground_branch] * 8)
    table_network = sum(rows[i][1] + rows[i][2] for i in (6, 7, 8))
    assert math.isclose(network, table_network, rel_tol=1e-12)
    pins = {2: "5V", 4: "5V", **{p: "GND" for p in (6, 9, 14, 20, 25, 30, 34, 39)}}
    assert len(pins) == 10 and len(set(pins)) == 10
    assert all(x["results"]["E"]["Pi_20mV_trough_V"] >= 4.75 for x in options.values())
    assert all(x["results"]["E"]["Pi_100mV_total_excursion_V"] < 4.75 for x in options.values())
    return dict(
        classification="CALCULATION within proposed ASSUMPTIONS; actual qualification OPEN",
        source_min_screen_V=source_min, load_A=current, Pi_min_requirement_V=4.75,
        thermal_assumptions_C=dict(wire_and_contacts=60, PCB_and_feedback=85, FET_junction=150, shunt=100),
        wire_DCR_hot_screen_factor=wire_factor,
        allowed_loop_mohm_20mV=(source_min - .020 - 4.75) / current * 1000,
        allowed_loop_mohm_100mV=(source_min - .100 - 4.75) / current * 1000,
        physical_Pi_pins=pins,
        pin_currents_equal_sharing_A=dict(positive=2.5, ground=.625),
        positive_branch_ratio_1p05_peak_A=5 * 1.05 / 2.05,
        options=options,
        sensitivity=dict(
            extra_10mm_each_AWG16_trunk_drop_mV=2 * wire_mohm(4, .010) * current,
            extra_10mm_every_AWG20_pigtail_drop_mV=wire_mohm(9.8, .010) * (1 / 2 + 1 / 8) * current,
            extra_1mohm_each_Pi_termination_drop_mV=(1 / 2 + 1 / 8) * current,
            extra_1mohm_each_J502_pole_drop_mV=2 * current,
            Pi_positive_20mohm_block_loss_W=2.5**2 * .020,
        ),
        independent_parallel_network_check="PASS; arithmetic only",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).with_name("CALCULATIONS.json")
    result = calculate()
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        assert path.read_text() == encoded, "CALCULATIONS.json differs: rerun calculate.py"
        print("PASS: recorded arithmetic, parallel branches and voltage cases; qualification remains OPEN")
    else:
        path.write_text(encoded)
        for name, option in result["options"].items():
            print(name, json.dumps(option["results"]))
