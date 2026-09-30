#!/usr/bin/env python3
"""V1A conditional DC path study. Standard library; document inputs only.

Run from any cwd. Writes only PATH_CALCULATIONS.json beside this script.
--check compares deterministic output without writing. No CAD file access.
Finite values are calculations inside stated assumptions, never qualified maxima.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ALPHA = 0.00393  # ASSUMED linear copper coefficient / K, referenced to 20 C
I = 5.0  # REQUIREMENT: Pi load A; auxiliary feeds excluded and separately required
WIRE_HOT = 60.0
PCB_HOT = 85.0
FET_HOT = 150.0
SHUNT_HOT = 100.0


def copper_factor(temp):
    return 1 + ALPHA * (temp - 20)


def wire(dcr_ohm_1000ft, length_m, parallel=1):
    # Manufacturer nominal DCR; reference 20 C and +/-10% are ASSUMED.
    r20 = dcr_ohm_1000ft / 304.8 * length_m / parallel * 1000
    return {str(t): [r20 * copper_factor(t) * q for q in (0.9, 1, 1.1)]
            for t in (25, 60)}


def shunt(nom_mohm, tcr):
    # Initial +/-1%; worst-sign component TCR; no inferred lifetime guarantee.
    return {"25": [nom_mohm * .99, nom_mohm, nom_mohm * 1.01],
            "hot": [nom_mohm * .99 * (1 - tcr * (SHUNT_HOT - 25)),
                    nom_mohm, nom_mohm * 1.01 * (1 + tcr * (SHUNT_HOT - 25))]}


def raw_bounds(nominal=1 + 100 / 24.4, resistor_fraction=.001):
    # TI VFB +/-1%; signed +/-10 nA is ASSUMED from a typical-only entry.
    rt = 100000.0
    rb = rt / (nominal - 1)
    v = []
    for vf, et, eb, ib in itertools.product((.99, 1.01),
            (-resistor_fraction, resistor_fraction),
            (-resistor_fraction, resistor_fraction), (-1e-8, 1e-8)):
        v.append(vf * (1 + rt * (1 + et) / (rb * (1 + eb)))
                 + ib * rt * (1 + et))
    return {"min_V": min(v), "nominal_V": nominal, "max_V": max(v),
            "resistor_fraction": resistor_fraction,
            "actual_worst_case_min_V": None, "actual_worst_case_max_V": None}


def build():
    source = json.loads((ROOT / "docs/evidence/r2/sheet03/CALCULATIONS.json").read_text())
    h = source["gate_1c"]["harness"]
    trip = source["gate_2c"]["threshold"]
    old = source["gate_2c"]["buck_static"]
    raw25 = raw_bounds()
    # Independent +/-0.1% initial tolerance plus +/-25 ppm/K to 85 C.
    rawhot = raw_bounds(resistor_fraction=.001 + 25e-6 * (PCB_HOT - 25))
    assert math.isclose(raw25["min_V"], old["min_V"], abs_tol=1e-12)
    assert math.isclose(raw25["max_V"], old["max_V"], abs_tol=1e-12)
    reduced = sum(h["reduced_terms_mOhm"].values()) + 13.6
    original = sum(h["original_terms_mOhm"].values()) + 13.6
    assert math.isclose(reduced, 55.36774050196851, abs_tol=1e-10)
    assert math.isclose(original, 75.55453848425196, abs_tol=1e-10)
    rows = []

    def item(name, leg, cold, hot, provenance, actual_max=None):
        row = dict(element=name, leg=leg, units="mOhm",
                   cold_25C_min_typ_max=cold, hot_min_typ_max=hot,
                   classification=provenance,
                   applicable_guaranteed_hot_max_mOhm=actual_max)
        rows.append(row)

    def allocation(name, leg, r_hot, factor, provenance):
        item(name, leg, [None, None, r_hot / factor], [None, None, r_hot],
             "ASSUMED acceptance allocation; " + provenance)

    def make_rows(recommended):
        rows.clear()
        cf = copper_factor(PCB_HOT) / copper_factor(25)
        allocation("Buck output copper", "SEND", .5, cf, "unsensed segment only, PCB 85 C")
        allocation("Buck return copper", "RETURN", .5, cf, "unsensed segment only, PCB 85 C")
        if recommended:
            item("Module series FET pair", "SEND", [None, 2.4, 3.0],
                 [None, 4.8, 6.0], "CALCULATED at VGS>=10 V within ASSUMED 2x hot factor; "
                 "BSC014N06NS pair 2x1.45=2.90 mOhm at 25 C plus allocation reserve")
        else:
            item("Module series FET pair", "SEND", [None, 5.6, 6.8],
                 [None, 11.2, 13.6], "CALCULATED at VGS=10 V within ASSUMED 2x hot factor; "
                 "actual VGS/Tj OPEN; BSC034N06NS table max 3.4 mOhm per FET at 25 C")
        s = shunt(2, 25e-6)
        item("2 mOhm current shunt", "SEND", s["25"], s["hot"],
             "CALCULATED from +/-1%, +/-25 ppm/K, shunt 100 C; WSL2726 terminal/reference-plane coverage OPEN")
        for leg in ("SEND", "RETURN"):
            allocation("Module PCB traces / vias", leg, 1, cf, "PCB 85 C; geometry not measured")
            allocation("J502 complete mated pole and clamp", leg, 3.12, 1.3,
                       "contact 60 C; manufacturer application maximum OPEN")
            w = wire(4.0 if recommended else 6.5, .075)
            item("Trunk wire AWG" + ("16" if recommended else "18") + " 75 mm", leg,
                 w["25"], w["60"], "CALCULATED from nominal DCR with ASSUMED 20 C reference, +/-10%; wire 60 C")
        for leg, n in (("SEND", 2), ("RETURN", 8)):
            w = wire(16.2, .015 if recommended else .025, n)
            item(f"AWG22 fan-out {15 if recommended else 25} mm, {n} parallel", leg,
                 w["25"], w["60"], "CALCULATED with ASSUMED equal branch geometry, +/-10% DCR; wire 60 C")
            per_hot = 20 if recommended else 39
            allocation(f"Pi mated contacts, {n} parallel", leg, per_hot / n, 1.3,
                       ("new hot/conditioned <=20 mOhm/contact procurement target; no qualified mate yet"
                        if recommended else "Harwin 30 mOhm conditioned maximum x ASSUMED 1.3 hot factor; Pi mate OPEN"))
            allocation(f"Pi female crimps, {n} parallel", leg, .8 / n, 1.3,
                       "per-termination <=0.8 mOhm target, separate from mating interface")
            allocation(f"Pi male pin / solder attachment, {n} parallel", leg, .48 / n, 1.3,
                       "per-termination <=0.48 mOhm target; actual Pi pin attachment OPEN")
        for leg in ("SEND", "RETURN"):
            allocation("Fan-out splice", leg, .5, 1.3, "hot termination target")
            allocation("Module solder joints", leg, .1, 1.3, "hot termination target")
        # Pi internal plane is explicitly excluded from GPIO-pin endpoint; never numerically set to zero.
        return [dict(row) for row in rows]

    inherited_rows = make_rows(False)
    fix_rows = make_rows(True)

    def total(rs, column):
        vals = [r[column][2] for r in rs]
        assert all(v is not None for v in vals)
        return sum(vals)

    audited = total(inherited_rows, "hot_min_typ_max")
    fix_d = total(fix_rows, "hot_min_typ_max")
    assert math.isclose(audited, reduced + 1, abs_tol=1e-10)
    # E additional loss is an acceptance cap, with its own current limiter and terminations.
    e_shunt = shunt(1, 75e-6)["hot"][2]
    e = {"local_series_FET_pair": 6.0, "limiter_shunt": e_shunt,
         "local_send_copper": .5, "local_return_copper": .5,
         "local_joints_and_entry_termination": 1.0}
    e["unallocated_resistance_reserve"] = 10 - sum(e.values())
    assert e["unallocated_resistance_reserve"] >= 0

    def screen(r, raw=rawhot["min_V"], ripple=0):
        v = raw - I * r / 1000 - ripple
        return dict(loop_mOhm=r, loss_5A_mV=I * r,
                    loop_dissipation_5A_W=I * I * r / 1000,
                    pi_static_screen_V=v, margin_to_4p75_mV=(v - 4.75) * 1000,
                    meets_4p75_within_assumptions=v >= 4.75,
                    actual_worst_case_pi_V=None)

    wire_before = sum(wire(6.5, .075)["60"][2] for _ in range(2)) + sum(
        wire(16.2, .025, n)["60"][2] for n in (2, 8))
    wire_after = sum(wire(4, .075)["60"][2] for _ in range(2)) + sum(
        wire(16.2, .015, n)["60"][2] for n in (2, 8))
    short_only = sum(wire(6.5, .05)["60"][2] for _ in range(2)) + sum(
        wire(16.2, .015, n)["60"][2] for n in (2, 8))
    options = {}
    option_r = {
        "unchanged_reduced_plus_buck_copper_allowance": audited,
        "original_PR6_four_grounds_same_buck_allowance": original + 1,
        "eight_grounds_only_from_original": original + 1 - 4.875 - .42284498031496066,
        "wire_16AWG_75mm_22AWG_15mm_only": audited - wire_before + wire_after,
        "shorten_18AWG_to_50mm_22AWG_to_15mm_only": audited - wire_before + short_only,
        "module_FET_hot_6mOhm_only": audited - 13.6 + 6,
        "qualified_Pi_hot_20mOhm_contact_only": audited - 39 * (1/2 + 1/8) + 20 * (1/2 + 1/8),
        "J502_hot_1mOhm_each_pole_only": audited - 6.24 + 2,
        "remove_output_shunt_only": audited - shunt(2, 25e-6)["hot"][2],
        "relocate_shunt_within_same_output_loop": audited,
        "change_to_1mOhm_shunt_only": audited - shunt(2, 25e-6)["hot"][2] + e_shunt,
        "JST_VH_hot_26mOhm_each_pole_screen": audited - 6.24 + 52,
        "recommended_combination": fix_d,
        "recommended_except_keep_inherited_Pi_contacts": fix_d + 19 * (1/2 + 1/8),
        "recommended_6V_module_FET_gate_sensitivity": fix_d - 6 + 8.8,
    }
    for name, r in option_r.items():
        options[name] = {"D": screen(r), "E": screen(r + 10)}
    final = {}
    for architecture, r in (("D", fix_d), ("E", fix_d + 10)):
        final[architecture] = {"static": screen(r), "20mV_ripple_trough": screen(r, ripple=.020),
                               "100mV_total_negative_excursion": screen(r, ripple=.100)}
    normal_increment = 5.266252 - raw25["max_V"]
    setpoints = []
    for delta in (0, .010, .020, .100, 5.2 - raw25["nominal_V"]):
        b = raw_bounds(raw25["nominal_V"] + delta, .0025)
        normal = b["max_V"] + normal_increment
        setpoints.append(dict(nominal_setpoint_V=b["nominal_V"], increase_V=delta,
            raw_hot_min_V=b["min_V"], raw_hot_max_V=b["max_V"], normal_release_screen_V=normal,
            trip_min_V=trip["min_V"], nuisance_margin_after_10mV_mV=(trip["min_V"]-normal-.010)*1000,
            D_pi_V=screen(fix_d, raw=b["min_V"])["pi_static_screen_V"],
            E_pi_V=screen(fix_d+10, raw=b["min_V"])["pi_static_screen_V"]))
    remote = {}
    for name, r in (("inherited_reduced", audited), ("recommended_D", fix_d),
                    ("recommended_E", fix_d + 10)):
        rawhi = rawhot["max_V"] + I * r / 1000
        release = rawhi + normal_increment
        remote[name] = dict(physical_loop_mOhm=r, raw_high_at_5A_V=rawhi,
            raw_trip_nuisance_margin_5A_mV=(trip["min_V"]-rawhi-.010)*1000,
            release_upper_screen_V=release,
            raw_trip_release_margin_mV=(trip["min_V"]-release-.010)*1000,
            ideal_pi_static_min_V=rawhot["min_V"], actual_pi_min_V=None)
    contacts = []
    for pin in [2, 4, 6, 9, 14, 20, 25, 30, 34, 39]:
        positive = pin in (2, 4)
        contacts.append(dict(physical_pin=pin, leg="5V" if positive else "GND",
            equal_share_A=2.5 if positive else .625,
            Harwin_test_rating_A=3, actual_Pi_mated_hot_rating_A=None,
            rating_headroom_equal_share_A=.5 if positive else 2.375))
    # Independent dimensional check of prospective copper allocation.
    copper = {}
    for name, length, width in (("module_each_leg", .030, .015), ("buck_each_leg", .010, .010)):
        nom = 1.724e-8 * length / (width * 70e-6) * copper_factor(25) * 1000
        hi = 1.724e-8 * (length*1.10) / ((width*.95)*(70e-6*.80)) * copper_factor(85) * 1000
        copper[name] = dict(nominal_25C_mOhm=nom, hot_geometry_high_mOhm=hi,
                           actual_resistance_mOhm=None)
    return dict(classification="CALCULATED within ASSUMED boxes; application bounds OPEN",
        frozen=dict(Pi_min_V=4.75, Pi_load_A=5, Vin_min_V=9, Vin_max_V=24, Pi_fault_peak_strictly_below_V=5.5),
        thermal_assumptions_C=dict(wire_contact=WIRE_HOT, PCB_feedback=PCB_HOT, FET_junction=FET_HOT, shunt=SHUNT_HOT),
        tolerances=dict(copper_alpha_per_K=ALPHA, wire_DCR_fraction_assumed=.10,
            contact_hot_factor_assumed=1.3, FET_hot_factor_assumed=2,
            feedback_initial_fraction_assumed=.001, feedback_TCR_per_K_assumed=25e-6,
            FB_current_typical_used_as_signed_allowance_A=1e-8),
        raw_static_25C_resistor_screen=raw25, raw_static_hot_feedback_screen=rawhot,
        loop_limits_mOhm={str(reserve): (rawhot["min_V"]-4.75-reserve)/I*1000 for reserve in (0,.020,.100)},
        historical=dict(original=screen(original, raw=raw25["min_V"]),
                        reduced=screen(reduced, raw=raw25["min_V"])),
        reduced_audited_itemised_rows=inherited_rows, recommended_D_itemised_rows=fix_rows,
        recommended_25C_upper_screen_mOhm=total(fix_rows, "cold_25C_min_typ_max"),
        E_additional_hot_stage_mOhm=e, E_total_stage_cap_mOhm=10,
        Pi_internal_plane_resistance_mOhm=None,
        options=options, final_conditional=final, setpoint_tradeoffs=setpoints,
        ideal_differential_remote_sense=remote, contacts=contacts,
        positive_branch_ratio_limit_for_3A_at_5A=1.5,
        ratio_2_positive_branch_current_A=I*2/3,
        copper_geometry_screens=copper,
        LC_sensitivity=dict(L_assumed_H=.6e-6, Pi_C_assumed_F=.001,
            resonance_Hz=1/(2*math.pi*math.sqrt(.6e-6*.001)),
            critical_series_damping_ohm=2*math.sqrt(.6e-6/.001)),
        FET_gate_charge=dict(existing_pair_max_nC=82, candidate_pair_max_nC=208,
            charge_ratio=208/82, boost_cap_Q_over_1V_candidate_F=208e-9,
            actual_effective_boost_cap_requirement_F=None),
        actual_worst_case_meets_D=None, actual_worst_case_meets_E=None,
        verdict="MEETS 4.75 V (neither qualified today); recommended combination is conditionally feasible for both D and E")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    encoded = json.dumps(result, indent=2, allow_nan=False) + "\n"
    output = HERE / "PATH_CALCULATIONS.json"
    if args.check:
        if output.read_text() != encoded:
            raise SystemExit("FAIL: saved calculation record differs from recomputation")
        print("PASS: historical reconciliation and deterministic calculation record")
    else:
        output.write_text(encoded)
        print("Wrote", output.relative_to(ROOT))
    print(json.dumps(result["final_conditional"], indent=2))


if __name__ == "__main__":
    main()
