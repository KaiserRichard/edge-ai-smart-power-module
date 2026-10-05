#!/usr/bin/env python3
"""Additive Phase C3 models; run calculate_phase_c.py --c3. No CAD/network writes.

All transient curves are explicitly ASSUMED sensitivities, not device models or
hardware qualification. Preserve C/C2 evidence and reuse their arithmetic.
"""
import sys
sys.dont_write_bytecode = True
import csv
import hashlib
import json
import math
from collections import Counter
from decimal import Decimal
from pathlib import Path
from calculate_phase_c import buck, crowbar, c2_rk4

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT/'third_party/v1a_lite_phase_c3'
D = Decimal
FX = D(26500)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def threshold():
    # Full -40..125C screening range, independent 0.1%,25ppm resistors.
    e = .001 + 100*25e-6
    top, bot = 34800., 10000.
    lo = 1.176*(1+top*(1-e)/(bot*(1+e)))-150e-9*top*(1+e)
    hi = 1.224*(1+top*(1+e)/(bot*(1-e)))+150e-9*top*(1+e)
    return dict(label='CALCULATED, excluding unbounded added clamp leakage',
                resistor_error=e, nominal_v=1.2*(1+top/bot), low_v=lo, high_v=hi,
                raw_voltage_for_20mV_overdrive_v=hi+.020*(1+top*(1+e)/(bot*(1-e))),
                nuisance_margin_at_5p17_v=lo-5.17,nuisance_margin_at_5p25_v=lo-5.25,
                unprotected_ovp_pin_at_29p26_v=29.26/(1+top/bot),
                clamp_leakage_1uA_shift_v=top*1e-6,
                ideal_divider_feasible_gain=[5.25/1.176,5.5/1.224])


def backup_threshold():
    # Reuse Phase C TL431 conservative screening method, new 1.3k/1k ratio.
    e=.001+25e-6*65
    return dict(label='CALCULATED screen; not guaranteed comparator trip',
                nominal_v=2.495*2.3,
                low_v=(2.483-.034-.008)*(1+1300*(1-e)/(1000*(1+e))),
                high_v=(2.507+.034)*(1+1300*(1+e)/(1000*(1-e)))+6.5e-6*1300*(1+e))


def cap_step(t, current, bulk_count=2, ceramic=40e-6, esr_multiplier=1):
    """Exact linear response of ideal ceramic parallel to bulk C+ESR branch.

    Both caps start at same voltage; no load. FR impedance used as ASSUMED ESR.
    Ceramic ESR/ESL omitted; this is a sensitivity, not a guaranteed pin bound.
    """
    cb=bulk_count*800e-6; rb=.028/bulk_count*esr_multiplier; ct=ceramic+cb
    tau=rb*ceramic*cb/ct
    return current*t/ct + current*rb*(cb/ct)**2*(-math.expm1(-t/tau))


def cap_window(current, count, headroom=.25, esr_multiplier=1):
    lo, hi=0.,.01
    for _ in range(70):
        mid=(lo+hi)/2
        if cap_step(mid,current,count,esr_multiplier=esr_multiplier)<headroom:lo=mid
        else:hi=mid
    return (lo+hi)/2


def fault_model(vin=24, ilim=6.24, ov_delay_us=14, limit_delay_us=0,
                scr_delay_us=2, failed_short=False, harness_l=1e-6, dt=1e-8):
    """Six-state RK4 sensitivity, ideal discrete eFuse/SCR behavior.

    Raw C:40uF/3mohm +1600uF/14mohm; Pi:40uF ideal +1600uF/14mohm.
    Healthy eFuse uses an ASSUMED 35mohm+fuse path without series L; current
    is capped only after a selectable response delay. Failed-short branch
    explicitly includes harness L, cold fuse9mohm +ASSUMED10mohm wiring.
    No assertion that the numerical eFuse is a manufacturer model.
    """
    b=backup_threshold(); ef=threshold()
    v0=5.25; i0=crowbar()['initial_fault_a']; L=2e-6
    rc=.003;rb=.014;cc=40e-6;cb=1600e-6;cp=40e-6;rp=.014;bp=1600e-6
    # Initial capacitor voltage offsets preserve a consistent 5A path before release.
    path_r=.019 if failed_short else .044
    s=[i0,v0,v0,5.,v0-5*path_r,v0-5*path_r]
    t=0.;trip=None;fire=None;lim_entry=None;off=None;fired=False;opened=False
    peak=s[4];rpeak=0.;samples={};events={};stop=100e-6
    def nodes(state):
        i,vc,vb,ih,vp,vpb=state
        base_g=1/rc+1/rb; base_n=i+vc/rc+vb/rb
        if fired: base_g+=1/.030; base_n+=.85/.030
        if failed_short:
            vr=(base_n-ih)/base_g; ip=ih
        elif opened:
            ip=0.;vr=base_n/base_g
        else:
            # Solve raw source Thevenin resistance against pass resistance.
            ip=max(0.,(base_n/base_g-vp)/(path_r+1/base_g))
            if lim_entry is not None and t>=lim_entry+limit_delay_us*1e-6:ip=min(ip,ilim)
            vr=(base_n-ip)/base_g
        return vr,ip
    def deriv(state):
        i,vc,vb,ih,vp,vpb=state;vr,ip=nodes(state);di=(vin-vr)/L
        if fired and i>=50 and di>0:di=0 # ASSUMED source ceiling after fire only
        return [di,(vr-vc)/(rc*cc),(vr-vb)/(rb*cb),
                (vr-vp-path_r*ih)/harness_l if failed_short else 0.,
                (ip-(vp-vpb)/rp)/cp,(vp-vpb)/(rp*bp)]
    for _ in range(round(stop/dt)):
        vr,ip=nodes(s)
        if not failed_short and lim_entry is None and ip>ilim:lim_entry=t;events['current_limit_cross_us']=t*1e6
        if trip is None and vr>=ef['raw_voltage_for_20mV_overdrive_v']:trip=t;events['ovp_20mV_overdrive_us']=t*1e6
        if fire is None and vr>=b['high_v']:fire=t;events['backup_threshold_us']=t*1e6
        if fire is not None and t>=fire+scr_delay_us*1e-6 and not fired:
            fired=True;events['scr_fire_us']=t*1e6
        # One-shot opening is deliberately optimistic: actual OVP pulse may
        # disappear during crowbar action and reset the OVP delay/filter.
        if not failed_short and trip is not None and t>=trip+ov_delay_us*1e-6 and not opened:
            opened=True;off=t;events['ideal_efuse_open_us']=t*1e6
        peak=max(peak,s[4]);rpeak=max(rpeak,vr)
        for name,level in [('pi_5p5_us',5.5),('raw_10_us',10),('raw_25_us',25)]:
            if name not in events and (s[4] if name.startswith('pi') else vr)>=level:events[name]=t*1e6
        s=c2_rk4(s,dt,deriv);t+=dt
    return dict(label='CALCULATED from ASSUMED ideal device/source/ESR dynamics',vin_v=vin,
                failed_short=failed_short,limit_delay_us=limit_delay_us,scr_delay_us=scr_delay_us,
                harness_l_h=harness_l if failed_short else None,pi_peak_v=peak,raw_peak_v=rpeak,
                events=events,screen='PASS' if peak<5.5 else 'FAIL',
                guarantee='OPEN: no maximum current-loop response, crowbar or commutation bound')


def costs():
    rows=list(csv.DictReader((HERE/'PHASE_C2_BOM.csv').open()))
    obs={}
    for folder in ['v1a_lite_phase_b','v1a_lite_phase_c2','v1a_lite_phase_c3']:
        obs.update(json.loads((ROOT/'third_party'/folder/'LCSC_OBSERVATIONS.json').read_text()))
    offers={o['productModel']:o for o in obs.values() if 'productModel' in o}
    base={r['ref']:dict(r) for r in rows}
    def price(o,n):
        return D([t for t in o['productPriceList'] if t['ladder']<=n][-1]['productPrice'])
    def offer_row(template,ref,mpn,description):
        r=dict(template);o=offers[mpn];n=len(ref.split());unit=price(o,max(o['minBuyNumber'],n))*FX
        r.update(ref=ref,mpn=mpn,manufacturer=o['brandNameEn'],qty=n,value=description,
                 unit_vnd=str(unit),extended_vnd=str(unit*n),source=o['url'],access_date='2026-10-05',
                 stock_observation=str(o['stockNumber']),scope='OPTION3B_C3',
                 price_label='KNOWN dated offer; reference only where stock=0',
                 selection_label='SELECTED analysis/cost candidate; NOT FOR FABRICATION',
                 safety_critical='yes',substitute_allowed='no',notes='C3 report governs; qualification OPEN')
        return r
    for r in rows:
        r['qty']=int(r['qty'])
        if r['ref'] in ('Q101','Q102'):
            r.update(offer_row(r,r['ref'],'IRFR6215TRPBF','150V P-FET DPAK; replaces 100V TO220; hot SOA OPEN'))
        if r['ref']=='R303':
            r.update(offer_row(base['R302'],'R303','TNPW0603100RBEEA','100R 0.1% backup crowbar upper segment'))
        if r['ref']=='F301':r['value']='7A wiring fuse after eFuse; no crowbar clearing duty'
        if r['ref']=='D101':
            r['notes']='150V FET fixes 103V/100V nameplate mismatch; actual surge waveform and hot clamp OPEN'
            r['selection_label']='SELECTED C3 coordination candidate; $0.50 allowance, exact offer OPEN'
    add=[
        ('U201','U302','TPS26630RGET','67V abs 6A eFuse; 14us max specified OVP-to-FLT delay'),
        ('Q101','Q302','CSD18540Q5B','60V reverse-blocking NFET; source raw, drain eFuse IN'),
        ('Q103','Q303','2N7002','BGATE pulldown FET driven by DRV; JSCJ exact sheet review required'),
        ('R302','R309','TNPW0603100RBEEA','100R extra upper segment; backup upper total1.3k'),
        ('R202','R320','RT0603BRD0734K8L','34.8k 0.1%25ppm OVP upper; stock OPEN'),
        ('R153','R321','TNPW060310K0BEEA','10k 0.1% OVP lower'),
        ('R301','R322 R323 R324','RT0603BRD071KL','three1k precision ILIM series segments'),
        ('R302','R325','TNPW0603100RBEEA','100R precision ILIM series; total3.1k'),
        ('D105','D302','BZT52C3V3-7-F','3.3V raw OVP-pin shunt clamp; leakage/knee qualification OPEN'),
        ('C203 C204','C305 C306 C307','GRM188R71H104KA93D','100nF IN/OUT bypass and dVdT100nF'),
        ('C217 C218','C303 C304','EEUFR1A102','two1000uF10V Pi-side bulk; place at Pi supply entry'),
    ]
    for old,ref,mpn,desc in add:rows.append(offer_row(base[old],ref,mpn,desc))
    fields=list(rows[0]);write_csv('PHASE_C3_BOM.csv',rows,fields)
    physical=[r for r in rows if r['scope'] not in ('THERMAL_C_ONLY','UNPRICED')]
    refs=[ref for r in physical for ref in r['ref'].split()];assert len(refs)==len(set(refs))
    core=[r for r in physical if r['scope']!='CONNECTORS'];count=Counter()
    for r in core:
        assert D(r['extended_vnd'])==D(r['unit_vnd'])*r['qty']
        count[r['mpn']]+=r['qty']
    local_basis=json.loads((ROOT/'third_party/v1a_lite_phase_c2/LOCAL_SOURCING_BASIS.json').read_text())
    local={r['mpn']:r for r in local_basis['rows'] if r['route'].startswith('Local')}
    purchases=[]
    # Procure timing100nF MPN exact; do not use generic decoupling as safety timing C.
    # Remaining generic100nF boot-cap lot is charged once in full.
    for method in ('phase_c_spares','local_plan_spares'):
        for mpn,n in sorted(count.items()):
            target=n+(max(1,math.ceil(n*.25)) if method=='phase_c_spares' else 1)
            if method=='local_plan_spares' and mpn in local and mpn!='GRM188R71H104KA93D':
                lr=local[mpn];buy=lr['buy'];unit=None;cost=D(lr['cost_vnd']);status='ASSUMED local equivalence; saved shared lot allocation'
                assert target<=50
                if mpn=='GRM188R71C104KA01D':
                    buy=10;cost=D(1900);status='ASSUMED local100nF ten-piece lot; timing MPN procured exact separately'
            elif mpn=='SMCJ64CA':
                buy=target;unit=D('.5');cost=unit*buy*FX;status='ASSUMED exact Bourns offer unavailable'
            else:
                o=offers[mpn];moq=o['minBuyNumber'];buy=math.ceil(max(target,moq)/moq)*moq
                unit=price(o,buy);cost=unit*buy*FX
                status='KNOWN dated offer' if o['stockNumber']>=buy else 'OPEN stock; reference-price allowance'
            purchases.append(dict(method=method,mpn=mpn,installed=n,target=target,buy=buy,
                                  unit_usd=str(unit) if unit is not None else 'local lot',cost_vnd=str(cost),label=status))
    write_csv('PHASE_C3_PURCHASE_MODEL.csv',purchases,list(purchases[0]))
    A=sum(D(r['extended_vnd']) for r in core)
    connectors=sum(D(r['extended_vnd']) for r in physical if r['scope']=='CONNECTORS')
    cash={m:sum(D(r['cost_vnd']) for r in purchases if r['method']==m) for m in ('phase_c_spares','local_plan_spares')}
    fixed={'pcb_five_board_lot':53000,'connector_lots':D('263502.75'),'wire_heatshrink':35000}
    reserves={'freight_tax':180000,'assembly_consumables':50000,'rework':50000,'thermal_contingency':40000}
    local_fixed={'pcb_five_board_lot':53000,'local_connector_kits':4719,'wire_heatshrink':20000}
    local_res={'component_shipping_import':80000,'pcb_shipping_tax':120000,'local_delivery':20000,'assembly_consumables':50000,'rework':50000,'thermal_contingency':40000}
    C=cash['phase_c_spares']+sum(fixed.values())+sum(reserves.values())
    CL=cash['local_plan_spares']+sum(local_fixed.values())+sum(local_res.values())
    return dict(label='CALCULATED planning totals; not a complete buyable qualified quote',
                A_core_vnd=str(A),B_core_board_connectors_vnd=str(A+connectors+10600),
                C_first_build_vnd=str(C),C_local_sourcing_vnd=str(CL),
                conventional_core_purchase_vnd=str(cash['phase_c_spares']),local_core_purchase_vnd=str(cash['local_plan_spares']),
                conventional_fixed_vnd={k:str(v) for k,v in fixed.items()},conventional_reserves_vnd=reserves,
                local_fixed_vnd=local_fixed,local_reserves_vnd=local_res,
                C_gap_vnd=str(C-1000000),C_local_gap_vnd=str(CL-1000000),
                stock_open=[p['mpn'] for p in purchases if p['method']=='local_plan_spares' and p['label'].startswith('OPEN')],
                local_basis_sha256=local_basis['sha256'],
                unpriced='Qualified low-drop replacement; precise/leakage-qualified OVP; hot input-FET thermal hardware; persistent latch/reset fixes; final interconnect. Not zero.')


def write_csv(name,rows,fields):
    with (HERE/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)


def calculate_c3():
    e=.001+100*25e-6
    ilim_nom=18000/3100;ilim_lo=ilim_nom*.93/(1+e);ilim_hi=ilim_nom*1.07/(1-e)
    caps=[]
    for n in (1,2):
        for load in (0,5):
            cur=ilim_hi-load
            caps.append(dict(label='CALCULATED after established ideal current limit',bulk_count=n,load_a=load,
                             effective_c_f=n*.0008+.00004,net_charge_a=cur,
                             ideal_window_us=(n*.0008+.00004)*.25/cur*1e6,
                             esr_window_us=cap_window(cur,n)*1e6,
                             pi_v_after14us=5.25+cap_step(14e-6,cur,n),
                             pi_v_after14us_ESR_2x=5.25+cap_step(14e-6,cur,n,esr_multiplier=2)))
    b=buck();normal_min=b['resistor_and_reference_screen_v'][0]-b['ripple_pp_v']/2
    conduction=[]
    for r in (.03044,.045,.053):
        conduction.append(dict(efuse_r_ohm=r,drop_at5a_v=5*r,loss_at5a_w=25*r,
                               tj_at50c_JEDEC=50+25*r*31.4,
                               pi_at5a_without_harness_v=normal_min-5*(r+.009+.0066),
                               extra_path_budget_ohm=(normal_min-4.75)/5-r-.009-.0066))
    models=[fault_model(vin=vin,ilim=ilim_hi,limit_delay_us=delay)
            for vin in (24,29.26) for delay in (0,5,20)]
    models += [fault_model(vin=29.26,ilim=ilim_hi,limit_delay_us=delay,scr_delay_us=1000) for delay in (0,5,20)]
    models += [fault_model(vin=vin,failed_short=True,scr_delay_us=delay,harness_l=lh)
               for vin in (24,29.26) for delay in (.5,2,5) for lh in (.2e-6,1e-6,2e-6)]
    c=costs()
    checks={
        '150V_FET_vs_103V_rated_TVS_clamp':'PASS',
        'eFuse_IN_and_positive_IN_OUT_voltage_at_29p26V':'PASS',
        'raw_OVP_pin_without_added_clamp':'FAIL',
        'OVP_pin_clamp_leakage_and_dynamic_survival':'OPEN',
        '6A_class_current_limit_static_screen':'PASS',
        '14us_datasheet_max_at_stated_test_conditions':'PASS',
        'Pi_cap_two_bulk_14us_ideal_limit_ESR_screen':'PASS',
        'current_limit_from_fault_inception_argument':'FAIL',
        'guaranteed_Pi_peak_below5p5V':'OPEN',
        'efuse_nuisance_at5p25V_full_temperature_screen':'FAIL',
        'efuse_static_high_trip_below5p5V':'FAIL',
        'backup_crowbar_nuisance_at5p25V_static_screen':'PASS',
        'Pi_min4p75_at5A_hot_series_drop_screen':'FAIL',
        'startup5A_plus_cap_charge_below_low_limit':'FAIL',
        'eFuse_short_backup_Pi5p5V_protection':'FAIL',
        'raw_caps_latch_SCR_input_FET_hot_SOA':'OPEN',
        'complete_in_stock_low_cost_BOM':'OPEN',
        'C_under1000000VND':'FAIL',
        'local_C_under1000000VND':'FAIL',
        'documents_calculations_PhaseD_list':'PASS',
        'R1_release_and_PhaseD_capture':'OPEN'}
    result=dict(date='2026-10-05',status='BLOCKED for R1 electrical release; C3 study complete',
        safety='NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED',
        selected=dict(efuse='TPS26630RGET',input_fets='2x IRFR6215TRPBF',reverse_blocker='CSD18540Q5B + JSCJ 2N7002',
                      status='SELECTED for analysis/cost only; no candidate fully satisfies every requirement'),
        inputs=dict(normal_high_v={'label':'KNOWN requested screen','value':[5.17,5.25]},
                    pi_ceiling_v={'label':'KNOWN','value':5.5},
                    raw_fault_v={'label':'KNOWN requested envelope plus inherited upper trip','value':[24,29.26]},
                    ceramic_c_f={'label':'ASSUMED effective minimum, requires biased-cap evidence','value':40e-6},
                    bulk_esr_each_ohm={'label':'ASSUMED from28mohm catalog impedance, not ESR guarantee','value':.028},
                    efuse_ovp_max_s={'label':'KNOWN TPS2663 p8, OVP+20mV toFLT; -40..125C','value':14e-6},
                    current_loop_max_s={'label':'OPEN not specified for this fault','value':None},
                    crowbar_response_max_s={'label':'OPEN','value':None},
                    latch_cutoff_max_s={'label':'OPEN','value':None}),
        ovp=threshold(),backup=backup_threshold(),
        current_limit=dict(label='CALCULATED interpolated ±7% model plus resistor tolerance/TCR; exact3.1k at high VDS OPEN',
                           nominal_a=ilim_nom,min_a=ilim_lo,max_a=ilim_hi,rilim_ohm=3100),
        cap_windows=caps,conduction=conduction,
        charge_screen=dict(label='CALCULATED, ASSUMED45A pre-limit pulse, not current bound',
                           pi_v_at1us_45a=5.25+cap_step(1e-6,45),
                           min_ideal_c_for14us_f=ilim_hi*14e-6/.25,
                           stored_harness_2uH_5A_j=.5*2e-6*25,
                           lossless_rise_at5p25_40uF_v=math.sqrt(5.25**2+2e-6*25/40e-6)-5.25),
        startup=dict(label='CALCULATED from TPS2663 p7,100nF±10%, no load-loop qualification',
                     slew_max_v_s=26*2.225e-6/90e-9,slew_min_v_s=23.5*1.775e-6/110e-9,
                     nominal_ramp_ms=5.1/(25*2e-6/100e-9)*1000,
                     max_cap_charge_a=(2*1000e-6*1.2+2*47e-6*1.1)*26*2.225e-6/90e-9,
                     minimum_current_limit_a=ilim_lo),
        input_fet=dict(label='CALCULATED from IRFR6215 p1-2; thermal environment/source unknown',
                       vds_rating_v=150,tvs_rated_clamp_v=103,margin_v=47,
                       r25_each_ohm=.295,r150_each_ohm=.58,
                       pair_loss_1p574a_25_w=2*1.574**2*.295,
                       pair_loss_1p574a_150_w=2*1.574**2*.58,
                       qg_scaled_13p35_v_nc=66*13.35/10,
                       cutoff_screen_us=20+66*13.35/10,
                       selected_latch_cutoff_sensitivity_us=150),
        fault_models=models,costs=c,checks=checks,
        scr_added_energy=dict(label='CALCULATED positive initial tolerance; voltage containment OPEN',
                             output_c_max_f=4*1000e-6*1.2+6*47e-6*1.2+2*47e-6*1.1,
                             energy_at6v_j=.5*(4*1000e-6*1.2+6*47e-6*1.2+2*47e-6*1.1)*6**2,
                             local10nH_didt_a_us=(6-.85)/10e-9/1e6),
        reproducer_sha256={n:sha(HERE/n) for n in ['calculate_phase_c.py','calculate_phase_c3.py']},
        preserved_baseline_sha256={n:sha(HERE/n) for n in ['PHASE_C_CALCULATIONS.json','PHASE_C2_REVISION.json','PHASE_C2_BOM.csv']},
        source_manifest_sha256=sha(SRC/'DOCUMENT_MANIFEST.json'))
    (HERE/'PHASE_C3_OPTION3B.json').write_text(json.dumps(result,indent=2)+'\n')
    for k,v in checks.items():print(v+': '+k)
    print(json.dumps({'selected':result['selected'],'costs':c},indent=2))
    return result


if __name__=='__main__':calculate_c3()
