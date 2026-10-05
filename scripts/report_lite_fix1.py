#!/usr/bin/env python3
"""Reproduce FIX1 allocation and pulse sensitivity. No unmeasured term is a bound."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/'docs/evidence/v1a_lite'; F=E/'fix1'
def write(name,obj):(F/name).write_text(json.dumps(obj,indent=2)+'\n')
r=json.loads((F/'COPPER_RESISTANCE_0.1.json').read_text())
raw=.99*(1+100*.999/(24.6*1.001));nominal=1+100/24.6
copper=max(r[x+'_round_trip_ohms_85C'] for x in ['C209','C214'])
pi=raw-5*(.025+.009+copper)
v={'classification':'CALCULATED conditional allocation screen; not measured operating worst case',
 'board_sha256':r['geometry_board_sha256'],'output_A':5,'setpoint_V':nominal,
 'raw_min_V_reference_minus_1pct_dividers_opposing_0.1pct':raw,
 'hot_aged_harness_ohm_requirement':.025,'fuse_ohm_cold_assumed':.009,
 'sampled_copper_round_trip_ohm_at_assumed_85C':copper,'copper_drop_mV_at_5A':5000*copper,
 'Pi_V_tolerance_screen':pi,'margin_to_4.75_mV':1000*(pi-4.75),
 'allocation_status':'PASS' if pi>=4.75 else 'FAIL',
 'full_operating_worst_case_status':'OPEN; FAIL to demonstrate guaranteed compliance',
 'remaining_series_resistance_if_no_ripple_ohm':(pi-4.75)/5,
 'unbounded_terms':['hot fuse resistance','minimum finished copper and barrel plating','solder joints','regulator line/load/temperature terms outside selected tolerance','ripple and load transients','measurement uncertainty'],
 'sensitivity_not_requirements':{}}
# Uniform 20% conductor-area reduction, 50% fuse increase, 2mΩ board joints,
# 25mV negative ripple are examples only, not approved bounds.
v['sensitivity_not_requirements']={'conductor_area_factor_assumed':.8,'hot_fuse_ohm_assumed':.0135,'board_joints_ohm_assumed':.002,'negative_ripple_V_assumed':.025,
 'Pi_V':raw-5*(.025+.0135+copper/.8+.002)-.025}
v['sensitivity_not_requirements']['margin_mV']=1000*(v['sensitivity_not_requirements']['Pi_V']-4.75)
write('VOLTAGE_BUDGET.json',v)
cap=(2*1000+6*47)*1.2*1e-6
pulse={'classification':'CALCULATED sensitivity using ASSUMED values; no extracted/qualified total loop bound',
 'capacitance_F_assumed_upper_nominal_plus_20pct_all_raw_parts':cap,
 'voltage_V_assumed':5.5,'stored_energy_J_assuming_voltage_bound':.5*cap*5.5**2,
 'SCR_drop_V_assumed':.85,'inductance_nH_sweep':[10,25,50,100],
 'initial_didt_A_per_us':[(5.5-.85)/(L*1e-9)/1e6 for L in [10,25,50,100]],
 'inductance_nH_needed_for_50A_per_us_with_assumed_drop':(5.5-.85)/50*1000,
 'inductance_nH_needed_without_assuming_minimum_SCR_drop':5.5/50*1000,
 'five_A_conduction_W_screen':.85*5+.030*25,
 'cutoff_duration_s_sweep':[.0001,.001,.01,.1,1],
 'five_A_source_conduction_J_screen':[5*t for t in [.0001,.001,.01,.1,1]],
 'open':['raw-node peak voltage','each bank ESR/ESL and package/lead/mutual inductance','gate rise and current vs ST conditions','source current and Q102 cutoff latency','hot SOA','SCR transient temperature/di_dt/i2t/recovery/repetition','remote Pi-node overshoot'],
 'decision':'Do not add series fuse or incidental trace inductance as limiting. Electrical finding remains BLOCKED.'}
write('CROWBAR_SENSITIVITY.json',pulse)
print(json.dumps(v,indent=2))
