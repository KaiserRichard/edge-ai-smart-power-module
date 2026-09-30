#!/usr/bin/env python3
"""Gate4a arithmetic and ideal energy-transfer model, never electrical qualification."""
import argparse, csv, hashlib, json, math, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
PATH_COMMIT='ebe51b9e141588d118d74daf37e65a3bd2307c1f'
PR15='51d1c2ff1f7eca4f20eef137c1595e4b9e052a75'
def pinned(commit,path):
    return subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=ROOT)
def source_pool(v):
    e=.5*30e-6*v*v+v*100e-6+.5*12e-6*8**2
    return dict(Vin_assumed_V=v,Cin_energy_J=.5*30e-6*v*v,replenishment_work_J=v*100e-6,initial_L_energy_J=.5*12e-6*8**2,Enew_CALCULATED_J=e,I_L_positive_upper_A=math.sqrt(2*e/5e-6),Vraw_cap_upper_V=math.sqrt(5.5**2+2*e/(8*470e-6*.8*.8)),actual_Vraw_peak_V=None)
def divider_screen(vlo,vhi,rt,rb,f,ibias):
    return [vlo*(1+rt*(1-f)/(rb*(1+f)))-ibias*rt*(1+f),vhi*(1+rt*(1+f)/(rb*(1-f)))+ibias*rt*(1+f)]
def bisect_root(fun,a,b):
    if not fun(a)*fun(b)<=0: raise ValueError('Root not bracketed')
    for _ in range(80):
        c=(a+b)/2
        if fun(a)*fun(c)<=0:b=c
        else:a=c
    return (a+b)/2

def raw_waveform(cin=30e-6,craw=2.4064e-3,ind=10e-6,vin=28.289211046948948,vraw=5.5,i0=8):
    """Immediately isolated main source; ideal negative-VIN diode. First positive I tail only.
    Opposed pair already open; protected crowbar is outside this model. No new source work.
    Constant C/L, zero ESR/DCR, capacitance/inductance test envelope ASSUMED.
    """
    ceq=cin*craw/(cin+craw); w=1/math.sqrt(ind*ceq); q=cin*vin+craw*vraw; x0=vin-vraw
    def before(t):
        x=x0*math.cos(w*t)-i0/(ceq*w)*math.sin(w*t)
        i=i0*math.cos(w*t)+x0/(ind*w)*math.sin(w*t)
        return (q+craw*x)/(cin+craw),(q-cin*x)/(cin+craw),i
    # First Vin crossing of zero is in the first half-cycle for this initial state.
    td=bisect_root(lambda t:before(t)[0],0,math.pi/w)
    _,vc,ic=before(td); w2=1/math.sqrt(ind*craw)
    tail=math.atan2(ic,craw*w2*vc)/w2; end=td+tail
    def state(t):
        if t<=td:return before(t)
        u=t-td
        return 0.0,vc*math.cos(w2*u)+ic/(craw*w2)*math.sin(w2*u),ic*math.cos(w2*u)-craw*w2*vc*math.sin(w2*u)
    rows=[dict(t_s=end*n/600,Vin_V=state(end*n/600)[0],Vraw_V=state(end*n/600)[1],IL_A=state(end*n/600)[2]) for n in range(601)]
    e0=.5*cin*vin**2+.5*craw*vraw**2+.5*ind*i0**2
    errors=[abs(.5*cin*r['Vin_V']**2+.5*craw*r['Vraw_V']**2+.5*ind*r['IL_A']**2-e0) for r in rows]
    return dict(ASSUMED=dict(Cin_F=cin,Craw_F=craw,L_H=ind,Vin0_V=vin,Vraw0_V=vraw,I0_A=i0,source_work_J=0,losses=0,ideal_input_ground_diode=True),input_ground_diode_start_s=td,first_current_zero_s=end,peak_Vraw_CALCULATED_V=state(end)[1],energy_initial_J=e0,max_energy_residual_J=max(errors),actual_peak_V=None), rows, state

def calculate():
    raw=pinned(PATH_COMMIT,'docs/evidence/r2/path_budget/PATH_CALCULATIONS.json');p=json.loads(raw)
    rows=p['recommended_D_itemised_rows']
    for r in rows:
        if r['element']=='Module series FET pair':
            r.update(cold_25C_min_typ_max=[None,5.6,6.8],hot_min_typ_max=[None,11.2,13.6],classification='BSC034N06 pair: published25C10V RDS2x2.8typ/2x3.4max; ASSUMED2x150C screen, hot actual OPEN')
    loop=sum(r['hot_min_typ_max'][2] for r in rows);vmin=p['raw_static_hot_feedback_screen']['min_V']
    path={}
    for neg in [0,.02,.1]:
        v=vmin-5*loop/1000-neg
        path[str(neg)]=dict(ASSUMED_total_negative_excursion_V=neg,loop_mOhm=loop,loss_5A_V=5*loop/1000,dissipation_5A_W=25*loop/1000,Vfar_end_CALCULATED_V=v,margin_to4p75_V=v-4.75,conditional_meets=v>=4.75,actual_min_V=None)
    netbytes=pinned(PR15,'docs/evidence/r2/footprints_complete/completed.xml');net=ET.fromstring(netbytes)
    connectivity={}
    for n in net.findall('./nets/net'):
        name=n.get('name','').split('/')[-1]
        if name in ['VOUT_5V1','VOUT_PROTECTED','VOUT_5V0','CROWBAR_DRAIN','CROWBAR_BALLAST_TOP'] or any(x.get('ref') in ['R308','R309','R310','R311','Q303','R401'] for x in n.findall('node')) and name!='GND':
            connectivity[n.get('name')]=[dict(ref=x.get('ref'),pin=x.get('pin')) for x in n.findall('node')]
    # Select exact exported net regardless of hierarchy/name to prove protected ballast boundary.
    for n in net.findall('./nets/net'):
        refs={x.get('ref') for x in n.findall('node')}
        if {'Q302','R308','R310'}<=refs: connectivity[n.get('name')]=[dict(ref=x.get('ref'),pin=x.get('pin')) for x in n.findall('node')]
    cmin=8*470e-6*.8*.8;cmax=8*470e-6*1.2*1.2+6*22e-6*1.2*1.15
    pools=[source_pool(v) for v in [9,24,26,27,28.289211046948948]]
    last=pools[-1];wave,curve,_=raw_waveform()
    ilmax=last['I_L_positive_upper_A'];vraw=last['Vraw_cap_upper_V'];terminal=vraw+ilmax*.004+.02
    lat=[]
    for vi in [9,24,26,27]:
        l=10e-6;c=cmin;vo=5.0983606557377055;w=1/math.sqrt(l*c)
        voltage=lambda t:vi+(vo-vi)*math.cos(w*t)+8/(c*w)*math.sin(w*t)
        t=bisect_root(lambda t:voltage(t)-5.325,0,math.pi/w)
        lat.append(dict(ASSUMED_stiff_Vin_V=vi,L_H=l,Craw_F=c,I0_A=8,ESR_ohm=0,initial_raw_V=vo,Vraw_after10us_V=voltage(10e-6),time_to_nominal_OV_s=t,actual_trigger_delay_s=None))
    f=.0025
    aux=dict(static_limit_screen_V=divider_screen(1.25,1.30,100e3,4320,f,1e-6),nominal_limit_V=1.275*(1+100e3/4320),static_12V_screen_V=divider_screen(.977,1.017,1e6,90.9e3,f,50e-9),hold_ASSUMED=dict(Ceff_F=300e-6,start_V=11.2,floor_V=10.5,total_load_A=.04,gate_event_C=2.036e-6),hold_time_screen_s=(300e-6*.7-2.036e-6)/.04,nominal_hold_energy_J=.5*440e-6*12**2,hold_cap_only_average_input_if9ms_A=.5*440e-6*12**2/(.009*.8*9),driver_supervisor_screen_V=divider_screen(.405*.98,.405*1.02,261e3,10e3,f,25e-9),detector_supervisor_screen_V=divider_screen(.405*.98,.405*1.02,113e3,10e3,f,25e-9),actual_usable_hold_s=None,actual_rails_valid=None)
    aux['hold_at_low_12V_minus_ASSUMED0p5V_s']=(300e-6*(aux['static_12V_screen_V'][0]-.5-10.5)-2.036e-6)/.04
    protmax=4*470e-6*1.2*1.2;rawinitial=.5*cmax*5.5**2
    normal=[dict(Vin_V=v,I_main_ASSUMED90pct_A=5.0983606557377055*5/(.9*v),I_aux_ASSUMED80pct40mA12V_A=.04*12/(.8*v)) for v in [9,24,26]]
    d=dict(classification='CALCULATED within stated ASSUMED/test-conditioned inputs; all actual application maxima OPEN',baseline_PR15_commit=PR15,path_input_commit=PATH_COMMIT,path_input_sha256=hashlib.sha256(raw).hexdigest(),netlist_sha256=hashlib.sha256(netbytes).hexdigest(),netlist_energy_boundaries=connectivity,selected_path=dict(itemised_rows=rows,BSC034_pair_Qg_at_published_test_max_C=82e-9,hot_Rpair_assumed_ohm=.0136,hot_Rpair_actual_ohm=None,source_min_assumed_V=vmin,source_actual_min_V=None,results=path,at6Vgate_and_ASSUMED2x_hot=dict(pair_ohm=.0204,loop_mOhm=loop+6.8,Vfar_end_after20mV_V=vmin-5*(loop+6.8)/1000-.02,actual_V=None)),source_contract=dict(ASSUMED=dict(Cin_effective_F=[10e-6,30e-6],Ldiff_H=[5e-6,12e-6],current_domain_A=[0,100],healthy_I0_max_A=8,source_off_max_s=10e-6,replenishment_positive_max_C=100e-6,actual_source_voltage_ceiling_V=None),CALCULATED=pools,actual_off_min_max_s=[None,None],actual_source_energy_max_J=None),raw_node=dict(Cmin_ASSUMED_F=cmin,Cmax_ASSUMED_F=cmax,initial_voltage_upper_ASSUMED_V=5.5,initial_raw_energy_upper_J=rawinitial,total_raw_dump_pool_upper_J=rawinitial+last['Enew_CALCULATED_J'],ESR_ASSUMED_upper_ohm=.004,ringing_ASSUMED_V=.02,terminal_screen_CALCULATED_V=terminal,actual_terminal_peak_V=None,complete_negative_fault_path=None,raw_dump_hot_rating_target_J=.2,raw_dump_actual_hot_rating_J=None,bulk35V_energy_headroom_at_Cmin_J=.5*cmin*(35**2-5.5**2),bulk_published_initial_parallel_ESR20C100kHz_max_ohm=.014/8,bulk_lowtemperature_endurance_parallel_ESR_ohm=.028/8,ideal_local_store_transfer=wave),protected_node=dict(candidate_Cnom_F=4*470e-6,Cmin_ASSUMED_F=4*470e-6*.8*.8,Cmax_ASSUMED_F=protmax,published_initial_parallel_ESR20C100kHz_max_ohm=.014/4,lowtemperature_endurance_parallel_ESR_ohm=.028/4,legacy_ESR_target_ohm=.0005,legacy_Cmax_target_F=.0015,initial_protected_energy_upper_J=.5*protmax*5.5**2,separate_PiCmax_actual_F=None,ASSUMED_dummy_Cmax_F=.0022,ASSUMED_dummy_energy_upper_J=.5*.0022*5.5**2,all_store_source_raw_protected_dummy_screen_J=rawinitial+last['Enew_CALCULATED_J']+.5*protmax*5.5**2+.5*.0022*5.5**2,actual_protected_arriving_current_A=None,legacy_conditional_module_screen_V=5.38+80*.5e-6/.001+80*.0005+.020,legacy_conditional_at_candidate14mOhm_parallel_ESR_V=5.38+80*.5e-6/(4*470e-6*.8*.8)+80*.014/4+.020,actual_module_peak_V=None,actual_far_end_peak_V=None,inherited_ASSUMED_harness_counterexample_V=5.542140),OV_trigger_latency_sensitivity=lat,auxiliary=aux,detector=dict(old_nominal_trip_V=5.325,new1M_pulldown_nominal_trip_V=2.5*(1+11300*(1/10000+1/1e6)),sense20mV_overdrive_raw_increment_V=.02*(1+11300/10000),actual_trip_min_max_V=[None,None],complete_path_min_max_s=dict(crowbar=[None,None],series=[None,None],source=[None,None]),partial_digital_crowbar_max_s=93.3e-9,partial_digital_series_max_s=134.2e-9),normal_buck=dict(input_current_screens=normal,inrush_actual_min_max_s=[None,None],inductor_DCR_hot_actual_ohm=None,nominal_Vout_V=5.0983606557377055,normal_Vin_requirement_V=[9,26],ripple_A_pp=[dict(Vin_V=v,at10uH400kHz_A=5.0983606557377055*(1-5.0983606557377055/v)/(10e-6*400e3)) for v in [9,24,26]],thermal_efficiency_startup_regulation_actual=None))
    fixes=OUT/'FIX_DISPOSITIONS.json'
    d['gate4a_fix']=json.loads(fixes.read_text()) if fixes.exists() else {}
    return d,curve

def render_md(d):
    s='# TASK 5 — Gate4a calculations\n\n**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** Values are CALCULATED within explicitly ASSUMED/test-conditioned inputs. Unknown actual maxima are JSON `null` (OPEN), never zero. [Script](calculate_gate4a.py) reproduces [CALCULATIONS.json](CALCULATIONS.json); [raw-node analysis](RAW_NODE_ENERGY.md) explains topology, stress and the proposed fix. No frozen electrical value is silently replaced.\n\nReproduce: `python3 -B docs/evidence/r2/gate4a/calculate_gate4a.py --write`; optional `--plot` adds a standalone ideal-model SVG using matplotlib. `python3 -B -m unittest discover -s docs/evidence/r2/gate4a -p test_gate4a_calculations.py` checks energy conservation/derivatives, topology and artifact consistency.\n\n|Selected-BOM path sensitivity|Loop mΩ|Far-end V at5 A|Margin to4.75 mV|\n|---|---:|---:|---:|\n'
    for name,r in d['selected_path']['results'].items():s+=f"|ASSUMED negative excursion {float(name)*1000:g} mV|{r['loop_mOhm']:.6f}|{r['Vfar_end_CALCULATED_V']:.6f}|{r['margin_to4p75_V']*1000:.3f}|\n"
    s+='\n`Vfar=Vraw_min−I·(Rsend+Rreturn)−Vnegative`. Keep BSC034 x2:25°C pair3.4mΩ/device maximum at10 V gate; hot2x resistance is ASSUMED. The imported lower-R pair6mΩ target is replaced by13.6mΩ. All other itemised wire/contact/shunt/copper allocations are retained in JSON. True source min/hot loop remain OPEN. Nominal5 A pair loss0.340 W; total path1.066824 W. At6 V gate using ASSUMED2x hot RDS, loop49.472941mΩ and far-end4.758779V after20mV: not a guaranteed lower-drive pass. Actual current sharing/contact ratings remain OPEN.\n\n`Enew<=0.5 Cin_max Vin_max²+Vin_max Qsource+0.5 Ldiff_max I0²`; `I_L<=sqrt(2Enew/Ldiff_min)`; `Vraw_cap<=sqrt(Vraw0²+2Enew/Craw_min)`. Do not add the peak-current magnetic energy again: it is already inside Enew. The source ceiling is an ASSUMED boundary, not an OVP clamp.\n\n|Input screen V|New energy mJ|L201 current bound A|Raw-cap bound V|\n|---|---:|---:|---:|\n'
    for r in d['source_contract']['CALCULATED']:s+=f"|{r['Vin_assumed_V']:.6f}|{r['Enew_CALCULATED_J']*1000:.6f}|{r['I_L_positive_upper_A']:.6f}|{r['Vraw_cap_upper_V']:.6f}|\n"
    rn=d['raw_node'];pn=d['protected_node'];au=d['auxiliary']
    s+=f"\nRaw Cmin={rn['Cmin_ASSUMED_F']*1000:.4f}mF (eight470µF ×0.8 initial ×0.8 additional assumed retention); ceramic minimum not credited. Cmax={rn['Cmax_ASSUMED_F']*1000:.5f}mF, all raw initial energy upper={rn['initial_raw_energy_upper_J']*1000:.6f}mJ. At highest source screen, raw terminal sensitivity with4mΩ/20mV is {rn['terminal_screen_CALCULATED_V']:.6f}V; extra local parasitic spike is OPEN. Maximum raw dump pool={rn['total_raw_dump_pool_upper_J']*1000:.6f}mJ; proposed0.2J hot capacity is a target, not a part rating. Actual raw peak OPEN.\n"
    s+=f"\nProposed protected bank4×470µF: nominal1.88mF, assumed minimum1.2032mF/maximum2.7072mF. Published14mΩ20°C/100kHz per capacitor means3.5mΩ for four, versus the inherited0.5mΩ target; low-temperature/endurance row28mΩ gives7mΩ. These frequency-conditioned values do not bound edge ESR/ESL. Substitution into the legacy80 A/0.5µs/5.38V/20mV screen gives {pn['legacy_conditional_at_candidate14mOhm_parallel_ESR_V']:.6f}V, not a PASS/prediction. Capacitor/harness topology must be recomputed. Initial protected energy upper={pn['initial_protected_energy_upper_J']*1000:.6f}mJ. Including assumed2.2mF dummy gives an all-store subtotal{pn['all_store_source_raw_protected_dummy_screen_J']*1000:.6f}mJ, before cable/other stores. Protected-arriving peak and Pi Cmax remain OPEN.\n"
    s+='\nOV latency counterexamples use an ideal maintained voltage,10µH/2.4064mF,8 A initial andzero ESR, not a qualified TPS26630 trajectory. They demonstrate why output OV propagation cannot be assumed to start at fault onset.\n\n|Input V|Raw V after10µs|Time to nominal5.325V µs|\n|---|---:|---:|\n'
    for r in d['OV_trigger_latency_sensitivity']:s+=f"|{r['ASSUMED_stiff_Vin_V']}|{r['Vraw_after10us_V']:.6f}|{r['time_to_nominal_OV_s']*1e6:.6f}|\n"
    s+=f"\nAux static limited output={au['static_limit_screen_V'][0]:.6f}…{au['static_limit_screen_V'][1]:.6f}V; buck-boost={au['static_12V_screen_V'][0]:.6f}…{au['static_12V_screen_V'][1]:.6f}V. Hold screen={au['hold_time_screen_s']*1000:.6f}ms at300µF/11.2→10.5V/40mA/2.036µC; lower buck-boost minus0.5V diode gives{au['hold_at_low_12V_minus_ASSUMED0p5V_s']*1000:.6f}ms. Nominal hold store31.68mJ, capacitor-only9ms average input{au['hold_cap_only_average_input_if9ms_A']:.6f}A at9V/80% efficiency. Supervisor screens={au['driver_supervisor_screen_V'][0]:.6f}…{au['driver_supervisor_screen_V'][1]:.6f}V / {au['detector_supervisor_screen_V'][0]:.6f}…{au['detector_supervisor_screen_V'][1]:.6f}V. Actual dynamic clamp/usable supply/hold remain OPEN.\n"
    s+='\nCurrent sense: retain2mΩ ±1%,25ppm/K inherited shunt inputs. At5 A,10mV/50mW nominal; independent100°C/initial corners give maximum2.0237875mΩ,10.1189375mV/50.5946875mW. At80 A the nominal shunt screen is160mV/12.8W while it actually carries that current; pulse energy requires the measured integral and actual protected current can exceed L201 due to raw-bank bypass. INA228 full-scale ±163.84mV normal range (alternate ±40.96mV range) and input common-mode/absolute/pin limits must be checked at the fault and correct ADCRANGE. Normal full scale with2mΩ is81.92A or20.48A nominal, not a fault-survival guarantee. Kelvin force/sense, shunt tolerance/TCR/self-heating, monitor gain/offset/timebase/error and energy accuracy remain qualification items. Filter10Ω+10Ω/100nF gives79.577kHz; it is not the high-bandwidth fault current probe.\n\nNormal input-current screens use25.491803W buck output/ASSUMED90% buck efficiency plus0.480W controls/ASSUMED80% aux efficiency; main input3.147136/1.180176/1.089393A at9/24/26V, before input dropout/unmodeled loads. Efficiency is not qualified. Inrush current is `C*dV/dt`; large raw/protected/dummy banks and series-FET charging require measured startup/current/SOA. Nominal10µH/400kHz ripple at9V is0.552555App, below the manufacturer nominal0.6A guidance; control-loop/stability/load-release/thermal/core-loss checks remain OPEN. Retain manufacturer reference-loop layout, low-current reference/Kelvin returns separate from disposal currents, dual VIN bypass, raw/protected/local stored-C accounting, connector/contact conditioning and copper/thermal targets from pinned PATH. Input current, efficiency, ripple/startup/inrush/transient/stability/protection/thermal limits are conditional calculations or OPEN. kicad ERC/DRC not rerun: no native schematic or PCB changes.\n'
    s+='\n## Current Gate4a-FIX decisions and worst-case screens\n\nThe preceding conditional energy/path models remain evidence, with any superseded component proposals identified below. These are paper calculations or named bench prerequisites; no test was run.\n'
    for x in d.get('gate4a_fix',{}).get('review_items',[]):
        s+=f"\n### {x['id']} — {x['status']}\n\n{x['equations']}\n\n{x['resolution']}\n\nClosure: {x['bench']}\n"
    return s

def write(plot=False):
    d,curve=calculate();(OUT/'CALCULATIONS.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');(OUT/'CALCULATIONS.md').write_text(render_md(d))
    with (OUT/'RAW_IDEAL_TRANSFER.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(curve[0]),lineterminator='\n');w.writeheader();w.writerows(curve)
    if plot:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams['svg.hashsalt']='gate4a-ideal-energy-transfer'
        t=[r['t_s']*1e6 for r in curve];fig,ax=plt.subplots(2,1,figsize=(8,6),sharex=True)
        ax[0].plot(t,[r['Vin_V'] for r in curve],label='Isolated local input bank')
        ax[0].plot(t,[r['Vraw_V'] for r in curve],label='VOUT_5V1 raw bulk')
        ax[0].set_ylabel('Voltage (V)');ax[0].legend();ax[0].grid(alpha=.3)
        ax[1].plot(t,[r['IL_A'] for r in curve],color='tab:orange');ax[1].set_ylabel('L201 current (A)');ax[1].set_xlabel('Time after immediate source isolation (µs)');ax[1].grid(alpha=.3)
        fig.suptitle('ASSUMED ideal local-store transfer after series opening\nProtected crowbar disconnected; no continuing source work; not a measured fault')
        fig.tight_layout();fig.savefig(OUT/'RAW_IDEAL_TRANSFER.svg',metadata={'Date':None});plt.close(fig)
    return d
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--plot',action='store_true');ns=a.parse_args()
    d=write(ns.plot) if ns.write else calculate()[0]
    print(json.dumps(dict(loop_mOhm=d['selected_path']['results']['0']['loop_mOhm'],source_corner=d['source_contract']['CALCULATED'][-1],ideal_raw_peak_V=d['raw_node']['ideal_local_store_transfer']['peak_Vraw_CALCULATED_V'],raw_terminal_screen_V=d['raw_node']['terminal_screen_CALCULATED_V'],VERDICT='BLOCKED; actual electrical bounds OPEN'),indent=2))
