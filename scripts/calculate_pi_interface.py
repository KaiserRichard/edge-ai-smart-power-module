#!/usr/bin/env python3
"""Reproduce the conditional Pi adapter resistance and voltage-drop review.

The configuration distinguishes measured/source data from engineering assumptions.
No result establishes a Pi header current rating or output-protection qualification.
"""

import argparse
import hashlib
import json
from pathlib import Path

from calculate_r2 import calculate as calculate_buck


ROOT = Path(__file__).resolve().parents[1]


def parallel(values):
    if not values or any(value <= 0 for value in values):
        raise ValueError("Each contact resistance must be positive")
    return 1 / sum(1 / value for value in values)


def calculate(config):
    buck = calculate_buck()
    wire = 2 * config["wire_one_way_m"] * config["wire_nominal_ohm_per_1000ft"] / 304.8
    wire_hot = wire * (1 + config["copper_temperature_coefficient_per_C"] * (
        config["wire_hot_temperature_C"] - config["wire_reference_temperature_C_assumed"]))
    contacts = (parallel(config["pi_5v_contact_mOhm_assumed"])
                + parallel(config["pi_gnd_contact_mOhm_assumed"])) / 1000
    other = (config["module_connector_loop_mOhm_assumed"]
             + config["adapter_joints_loop_mOhm_assumed"]) / 1000
    external, external_hot = wire + contacts + other, wire_hot + contacts + other
    internal = (config["internal_disconnect_mOhm_allocated_not_selected"]
                + config["internal_copper_loop_mOhm_allocated"] + config["shunt_mOhm"]) / 1000
    raw_min, raw_max = buck["output_divider_and_reference_corner_V"]
    rows = []
    for current in config["loads_A"]:
        corner = raw_min - current * (external_hot + internal)
        rows.append({
            "current_A": current,
            "external_drop_V": current * external,
            "pi_V_if_connector_is_exact_5p1": config["ideal_module_connector_voltage_V"] - current * external,
            "pi_V_from_nominal_buck_with_allocated_internal_loss": buck["output_nominal_V"] - current * (external + internal),
            "pi_V_static_low_source_hot_wire_screen": corner,
            "remaining_drop_to_screen_floor_V": corner - config["screening_load_min_V_not_pi_spec"],
            "pi_V_with_additional_dynamic_droop_example": corner - config["dynamic_droop_sensitivity_V"],
            "external_loss_W": current**2 * external,
        })
    return {
        "classification": config["classification"],
        "wire_loop_mOhm": wire * 1000,
        "wire_hot_loop_mOhm": wire_hot * 1000,
        "parallel_pi_contact_loop_mOhm_assumed": contacts * 1000,
        "external_loop_mOhm": external * 1000,
        "external_hot_loop_mOhm": external_hot * 1000,
        "internal_loop_mOhm_allocated": internal * 1000,
        "raw_buck_nominal_V": buck["output_nominal_V"],
        "raw_buck_static_screen_V": [raw_min, raw_max],
        "rows": rows,
        "external_loop_budget_at_5A_static_mOhm": ((raw_min - config["screening_load_min_V_not_pi_spec"]) / 5 - internal) * 1000,
        "external_loop_budget_at_5A_with_dynamic_reserve_mOhm": ((raw_min - config["screening_load_min_V_not_pi_spec"] - config["dynamic_droop_sensitivity_V"]) / 5 - internal) * 1000,
        "poor_harness_sensitivity_at_5A": [
            {"external_loop_mOhm": value,
             "pi_V_if_connector_is_exact_5p1": config["ideal_module_connector_voltage_V"] - 5 * value / 1000,
             "pi_V_low_buck_including_internal": raw_min - 5 * (value / 1000 + internal)}
            for value in config["other_external_loop_mOhm"]],
        "startup_example_capacitor_current_A": config["startup_example_capacitance_uF"] * 1e-6 * 5.1 / (config["startup_example_ramp_ms"] * 1e-3),
        "capacitor_only_step_droop_example_V": config["transient_example_step_A"] * config["transient_example_response_us"] / buck["effective_cout_screen_uF"],
        "limitations": [
            "Contact resistance, disconnect resistance, copper and temperatures are assumptions, not guaranteed maxima.",
            "The connector-only table assumes 5.1 V at J502; the captured buck regulates before the switch and shunt.",
            "The static low-source calculation does not bound all regulator, contact, aging or transient errors.",
            "The 4.75-5.25 V window is a review screen, not an official Pi 5 voltage-time rating.",
            "The current schematic has no output disconnect and cannot deliver power from VIN to J502.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "docs/evidence/r2/pi_interface_assumptions.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = args.config.read_bytes()
    result = calculate(json.loads(data))
    result["config_sha256"] = hashlib.sha256(data).hexdigest()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as output:
            output.write(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
