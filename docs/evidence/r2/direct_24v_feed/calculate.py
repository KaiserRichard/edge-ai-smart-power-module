"""Reproduce the direct-feed screens; stdout only, no hardware edits.

Inputs and limitations are classified in ../DIRECT_24V_FEED.md.
These calculations are not electrical validation or guaranteed thermal limits.
"""
import json
from math import sqrt


def ovp(tolerance):
    rh, rl, leakage = 348e3, 15.8e3, 150e-9
    lo = rh * (1 - tolerance)
    hi = rh * (1 + tolerance)
    return {
        "resistor_fractional_bound": tolerance,
        "trip_min_V": 1.176 * (1 + lo / (rl * (1 + tolerance))) - leakage * lo,
        "trip_nom_V": 1.2 * (1 + rh / rl),
        "trip_max_V": 1.224 * (1 + hi / (rl * (1 - tolerance))) + leakage * hi,
        "recovery_min_V": 1.09 * (1 + lo / (rl * (1 + tolerance))) - leakage * lo,
        "recovery_max_V": 1.15 * (1 + hi / (rl * (1 - tolerance))) + leakage * hi,
    }


initial = ovp(.001)
# ASSUMED resistor temperatures -40..125 C, relative to 20 C; no aging included.
temperature = ovp(.001 + 25e-6 * 105)
normal = {}
for name, error, ripple in [
    ("DDR_25C", .01, .05),
    ("RSD_25C", .02, .15),
    ("DDR_0_to_55C", .019, .05),
    ("RSD_0_to_50C", .0275, .15),
]:
    # ASSUMED full peak-to-peak ripple added on the high side conservatively.
    high = 24 * (1 + error) + ripple
    normal[name] = {
        "high_V_before_dynamic_overshoot": high,
        "margin_to_26V_V": 26 - high,
        "initial_OVP_margin_V": initial["trip_min_V"] - high,
        "temperature_screen_OVP_margin_V": temperature["trip_min_V"] - high,
        "maximum_setpoint_for_26V_no_dynamics_V": (26 - ripple) / (1 + error),
    }

vout = 1 + 100 / 24.6  # Current R203 option A, not historical 24.4 kohm.
pout = vout * 5
buck = {}
for vin in [12, 24]:
    duty = vout / vin
    ripple = (vin - vout) * duty / (10e-6 * 400e3)
    rms2 = 5**2 + ripple**2 / 12
    conduction = rms2 * (duty * .041 + (1 - duty) * .021)
    switching = .5 * vin * 5 * 10e-9 * 400e3  # ASSUMED aggregate edge time.
    buck[str(vin)] = {
        "duty": duty, "ripple_App": ripple,
        "peak_A": 5 + ripple / 2, "rms_A": sqrt(rms2),
        "switch_conduction_typ_W": conduction,
        "switch_conduction_max_Rds_screen_W": rms2 * (duty * .082 + (1 - duty) * .045),
        "switching_10ns_screen_W": switching,
        "partial_IC_loss_W": conduction + switching,
        "inductor_copper_20C_max_DCR_W": rms2 * .00062 * 1.1,
    }
ripple_corner = (24 - vout) * (vout / 24) / (8e-6 * 360e3)
efficiency = {
    str(eta): {"whole_buck_loss_W": pout * (1 / eta - 1),
               "buck_input_current_24V_A": pout / (24 * eta)}
    for eta in [.90, .935, .945]
}
result = {
    "status": "CALCULATED screens only; assumptions and OPEN limits in report",
    "ovp_initial": initial, "ovp_temperature_screen": temperature,
    "normal_source_screens": normal,
    "buck_output_nominal_V": vout, "buck_output_power_5A_W": pout,
    "buck": buck, "ripple_Lminus20pct_f360kHz_App": ripple_corner,
    "peak_Lminus20pct_f360kHz_A": 5 + ripple_corner / 2,
    "efficiency_sensitivity": efficiency,
    "TVS_power_if_terminal_held_at_54_6V_W": {str(i): 54.6*i for i in [1, 10, 15.625, 25]},
    "TVS_25C_ambient_thermal_screen_W": (150-25)/75,
    "fuse_125A_typical_prearc_screen_s": 340/125**2,
}
print(json.dumps(result, indent=2, sort_keys=True))
