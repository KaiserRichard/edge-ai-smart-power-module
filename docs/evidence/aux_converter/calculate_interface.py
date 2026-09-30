#!/usr/bin/env python3
"""Reproduce conditional AUX24 sizing and voltage allocations; no circuit simulation."""

import json
from pathlib import Path


def calculate():
    pi_voltage = 5.1
    pi_current = 5.0
    v1a_efficiency_assumed = 0.90
    upstream_efficiency_assumed = 0.90
    reserve_assumed = 1.25
    v1a_input_w = pi_voltage * pi_current / v1a_efficiency_assumed
    trim_v_assumed = 23.5
    dc_error_assumed = 0.01
    positive_ripple_v_assumed = 0.100
    extra_transient_v_assumed = 0.150
    module_ovp_v_assumed = 25.0
    module_ovp_error_assumed = 0.02
    fault_peak_v_assumed = 26.0
    frozen_efuse_min_v_initial_only = 26.97
    scenarios = []
    for other_w in (0, 50, 100):
        demand_w = v1a_input_w + other_w
        usable_w = demand_w * reserve_assumed
        scenarios.append({
            "other_load_w_scenario_actual_open": other_w,
            "continuous_demand_w_calculated": demand_w,
            "current_at_24v_a_calculated": demand_w / 24,
            "current_at_23_5v_a_calculated": demand_w / trim_v_assumed,
            "minimum_usable_w_calculated": usable_w,
            "minimum_usable_a_at_23_5v_calculated": usable_w / trim_v_assumed,
            "primary_current_at_39v_90pct_a_calculated": demand_w / (39 * upstream_efficiency_assumed),
        })
    tep200_dc_error_screen = 0.01 + 0.002 + 0.001 + 0.0002 * 45
    additive_v = positive_ripple_v_assumed + extra_transient_v_assumed
    return {
        "classification": "CALCULATED conditional screens, not validated performance",
        "baseline_commit": "0677fea0a32fc87b740949d589abe1588e55934c",
        "assumed": {
            "v1a_efficiency": v1a_efficiency_assumed,
            "upstream_efficiency_for_primary_budget": upstream_efficiency_assumed,
            "power_reserve_factor": reserve_assumed,
            "battery_empty_v": 39,
            "trim_v": trim_v_assumed,
            "complete_dc_error_fraction_target": dc_error_assumed,
            "positive_ripple_v": positive_ripple_v_assumed,
            "additional_healthy_transient_v": extra_transient_v_assumed,
            "module_ovp_nominal_v": module_ovp_v_assumed,
            "module_ovp_total_error_fraction": module_ovp_error_assumed,
            "complete_fault_peak_ceiling_v": fault_peak_v_assumed,
            "input_surge_screen_v": 100,
            "ambient_c": [-20, 60],
        },
        "calculated": {
            "pi_output_w": pi_voltage * pi_current,
            "v1a_input_w": v1a_input_w,
            "normal_dc_min_v": trim_v_assumed * (1 - dc_error_assumed),
            "normal_dc_max_v": trim_v_assumed * (1 + dc_error_assumed),
            "normal_peak_v": trim_v_assumed * (1 + dc_error_assumed) + additive_v,
            "normal_ceiling_margin_v": 24 - (trim_v_assumed * (1 + dc_error_assumed) + additive_v),
            "module_ovp_min_v": module_ovp_v_assumed * (1 - module_ovp_error_assumed),
            "module_ovp_max_v": module_ovp_v_assumed * (1 + module_ovp_error_assumed),
            "ovp_threshold_margin_to_frozen_initial_only_min_v": frozen_efuse_min_v_initial_only - module_ovp_v_assumed * (1 + module_ovp_error_assumed),
            "fault_peak_margin_to_frozen_initial_only_min_v": frozen_efuse_min_v_initial_only - fault_peak_v_assumed,
            "surge_screen_headroom_over_54_6v_v": 100 - 54.6,
            "current_limited_capacity_at_23_5v_w": {"4_2a": 4.2 * trim_v_assumed, "6_3a": 6.3 * trim_v_assumed, "8_4a": 8.4 * trim_v_assumed},
            "rsd_100_70c_60pct_free_air_w": 100.8 * 0.60,
            "rsd_200_70c_60pct_free_air_w": 201.6 * 0.60,
            "tep200_128w_loss_at_89pct_typical_w": (v1a_input_w + 100) * (1 / 0.89 - 1),
            "tep200_limited_dc_error_fraction_screen": tep200_dc_error_screen,
            "tep200_23_5v_limited_peak_v": trim_v_assumed * (1 + tep200_dc_error_screen) + additive_v,
            "tep200_limited_setting_ceiling_v": (24 - additive_v) / (1 + tep200_dc_error_screen),
            "tep200_23v_limited_peak_v": 23 * (1 + tep200_dc_error_screen) + additive_v,
            "tep200_23v_current_limited_capacity_w": 23 * 8.4,
            "scenarios": scenarios,
        },
        "open": {
            "actual_bus_peak_waveform_energy_repetition": None,
            "complete_efuse_ovp_min_with_drift": None,
            "complete_module_error_with_aging_trim_sense_harness": None,
            "independent_output_barrier_delay_fault_peak_energy": None,
            "shared_load_peaks_and_hot_usable_capacity": None,
            "single_fault_containment_report": None,
        },
    }


if __name__ == "__main__":
    output = Path(__file__).with_name("CALCULATIONS.json")
    output.write_text(json.dumps(calculate(), indent=2, allow_nan=False) + "\n")
    print(f"Wrote {output}: conditional calculations only; OPEN bounds remain null.")
