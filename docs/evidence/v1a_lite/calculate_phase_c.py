#!/usr/bin/env python3
"""Phase C screening calculations. Standard library only; no CAD or network writes.

Run from any directory; --c2 generates additive Phase C2 evidence only.
Results are models, not electrical qualification.
All numeric model inputs carry an epistemic label; derived sections inherit
CALCULATED, and their assumptions are explicitly listed in inputs / report.
"""
import csv
import hashlib
import json
import math
from collections import Counter
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def value(number, label, unit, basis):
    return dict(value=number, label=label, unit=unit, basis=basis)


inputs = {
    'vin_normal': value([18, 26], 'KNOWN', 'V', 'Phase C owner requirement'),
    'vin_fault': value([54.6, 64], 'KNOWN', 'V', 'Phase C continuous fault requirement'),
    'pi_window': value([4.75, 5.5], 'KNOWN', 'V', 'project requirement; upper bound strict'),
    'load': value(5, 'KNOWN', 'A', 'continuous design requirement; peak/duration OPEN'),
    'temperature_screen': value([-40, 85], 'ASSUMED', 'degC', 'TL431BI range; system ambient remains OPEN'),
    'fet_vds': value(100, 'KNOWN', 'V', 'Infineon IRF9540NPBF absolute maximum'),
    'tvs_standoff': value(64, 'KNOWN', 'V', 'Bourns SMCJ64CA'),
    'tvs_clamp': value(103, 'KNOWN', 'V', 'SMCJ64CA at rated 14.6 A pulse; not arbitrary source'),
}

inputs.update({
    'input_divider': value([102000, 10000], 'SELECTED', 'ohm', '100k + 1k + 1k /10k; E96'),
    'precision_r_tolerance': value(.001, 'KNOWN', 'fraction', 'selected 0.1% parts'),
    'precision_tcr_screen': value(25e-6, 'ASSUMED', '/degC', 'qualify exact resistor suffixes'),
    'tl431_ref_nom': value(2.495, 'KNOWN', 'V', 'TI TL431BI table6.12'),
    'tl431_ref_25': value([2.483, 2.507], 'KNOWN', 'V', 'table6.12 at 10mA'),
    'tl431_temp_deviation': value(.034, 'KNOWN', 'V', 'conservatively added both ways'),
    'tl431_iref_max': value(6.5e-6, 'CALCULATED', 'A', '4uA +2.5uA full-temperature deviation'),
    'input_cathode_shift_reserve': value(.026, 'ASSUMED', 'V', '26mV lowering screen; actual transition OPEN'),
    'cin_min_screen': value(92e-6, 'ASSUMED', 'F', '80uF electrolytic +12uF effective ceramics'),
    'fet_qgd_screen': value(34e-9, 'ASSUMED', 'C', 'Phase B typical-charge screen; not a maximum'),
    'turnoff_delay_screen': value(25e-6, 'ASSUMED', 's', 'TL431+storage+gate total, not guaranteed'),
    'input_excess_currents': value([3, 15, 100], 'ASSUMED', 'A', 'source sensitivity; not UENPO specification'),
})


def input_cutoff():
    # Bounds use worst independent resistor drift relative to 25 degC.
    e = .001 + 25e-6*65
    low = (2.483-.034-.026)*(1+102000*(1-e)/(10000*(1+e)))
    high = (2.507+.034)*(1+102000*(1+e)/(10000*(1-e)))+6.5e-6*102000*(1+e)
    nominal = 2.495*(1+102000/10000)
    bias = []
    for vin in (18, 24, 26, nominal, 54.6, 64):
        # Normal TL431-off DC model: CTRL12 ->1k ->3.3V ->10k ->VBE .7V.
        ctrl_off = min(12, (vin*11000+4*4000)/15000)
        # OV TL431 conducting at assumed 2.5V; resistor divider may not reach 12V.
        ctrl_on = min(12, (vin*1000+2.5*4000)/5000)
        isupply = (vin-ctrl_on)/4000
        ik = (ctrl_on-2.5)/1000
        bias.append(dict(vin_v=vin, ctrl12_tl_off_v=ctrl_off,
                         npn_base_available_a=max(0, (ctrl_off-4)/11000-.7/100000),
                         ctrl12_tl_on_v=ctrl_on, detector_ik_a=ik,
                         ballast_w=(vin-ctrl_on)**2/4000,
                         ballast_each_of_16_w=(vin-ctrl_on)**2/4000/16,
                         shunt_zener_w=ctrl_on*max(0, isupply-ik)))
    return dict(label='CALCULATED; assumptions as in inputs and report',
                nominal_trip_v=nominal, nominal_with_typ_iref_v=nominal+2e-6*102000,
                static_trip_screen_v=[low, high], release_screen_v=[low, high],
                guaranteed_hysteresis_v=None, bias=bias,
                charge_to_36_c=92e-6*(36-high), charge_to_42_c=92e-6*(42-high),
                transients=[dict(excess_current_a=i, dv_dt_v_per_us=i/92,
                                 max_delay_to_36_us=92*(36-high)/i,
                                 peak_at_25us_v=high+i*25/92,
                                 overlap_screen_j=64*i*25e-6)
                            for i in (3, 15, 100)],
                typical_miller_time_us=[34e-9/(4/1000)*1e6, 34e-9/(2/1000)*1e6],
                reverse_gate_chain_w=(64-12)**2/20000,
                q102_pullup_w=12**2/1000,
                q102_gate_sink_pulse_w=(64-12-.2)**2/600,
                startup_cap_energy_j=.5*92e-6*26**2)


inputs.update({
    'fb_resistors': value([100000, 24600], 'SELECTED', 'ohm', 'retain owner divider'),
    'fb_reference': value([.99, 1, 1.01], 'KNOWN', 'V', 'LM61460 FPWM accuracy; auto light-load OPEN'),
    'fb_current_typ': value(10e-9, 'KNOWN', 'A', 'typical only, no specified max'),
    'rt': value(33200, 'SELECTED', 'ohm', '400kHz setting'),
    'frequency_screen': value([356400, 400000, 444400], 'ASSUMED', 'Hz', '360–440kHz table expanded by 1%'),
    'inductance': value(6.8e-6, 'SELECTED', 'H', 'SRP1265A-6R8M ±20%'),
    'magnetic_retention': value(.8, 'ASSUMED', 'fraction', 'additional screening drop; not hot guaranteed L'),
    'inductor_dcr_max': value(.0115, 'KNOWN', 'ohm', 'Bourns at25C'),
    'output_c_effective': value([29.728753e-6, 28.008429e-6], 'KNOWN', 'F/part', 'saved typical Murata model at5.1/5.5V'),
    'c_derating_factors': value([.9, .85, .9], 'ASSUMED', 'fraction', 'initial/temp/aging-model screen'),
    'cout_normal': value(120e-6, 'ASSUMED', 'F', 'six raw ceramics; acceptance target not guarantee'),
    'cout_fault': value(110e-6, 'ASSUMED', 'F', 'reduced at5.5V; lumped sensitivity model'),
    'cout_esr': value(.003, 'ASSUMED', 'ohm', 'raw bank effective ESR'),
    'load_release_overshoot': value([.025, .100], 'ASSUMED', 'V', 'sensitivity, not a measured maximum'),
})


def buck():
    vo = 1+100000/24600
    e = .001+25e-6*65
    vlo = .99*(1+100000*(1-e)/(24600*(1+e)))
    vhi = 1.01*(1+100000*(1+e)/(24600*(1-e)))
    rows = []
    for vin in (18, 24, 26, 36):
        ripple = 5.1*(1-5.1/vin)/(6.8e-6*400000)
        stressed = 5.1*(1-5.1/vin)/(6.8e-6*.8*.8*356400)
        irms = math.sqrt(25+stressed**2/12)
        rows.append(dict(vin_v=vin, ripple_a=ripple, peak_a=5+ripple/2,
                         stressed_ripple_a=stressed, stressed_peak_a=5+stressed/2,
                         irms_a=irms, output_cap_rms_a=stressed/math.sqrt(12),
                         input_cap_rms_a=5*math.sqrt((5.1/vin)*(1-5.1/vin)),
                         dcr_loss_25_w=irms**2*.0115,
                         dcr_loss_100_w=irms**2*.0115*(1+.00393*75)))
    ripple_v=rows[2]['stressed_ripple_a']*(1/(8*356400*120e-6)+.003)
    return dict(label='CALCULATED; normal-operation model, not qualification',
                nominal_v=vo, resistor_and_reference_screen_v=[vlo,vhi],
                typical_fb_current_shift_v=10e-9*100000,
                rt_formula_hz=1000/(33200/1000/13460+3.3e-5),
                rows=rows, ripple_pp_v=ripple_v,
                input_effective_c_screen_f=4*10e-6*.4*.9*.85,
                output_effective_c_screen_f=[6*c*.9*.85*.9 for c in (29.728753e-6,28.008429e-6)],
                min_l_h=.2*5.1/356400,
                min_ripple_a=5.1*(1-5.1/18)/(6.8e-6*1.2*444400),
                normal_high_screens_v=[vhi+.001+ripple_v/2+o for o in (.025,.1)],
                path_resistance_budget_ohm=(vlo-4.75-ripple_v/2)/5,
                feedforward_zero_hz=1/(2*math.pi*100000*22e-12),
                feedforward_pole_hz=1/(2*math.pi*(100000*24600/(100000+24600))*22e-12),
                esr_zero_hz=1/(2*math.pi*.003*120e-6),
                lc_resonance_hz=1/(2*math.pi*math.sqrt(6.8e-6*120e-6)),
                load_step_10us_droop_v=5*10e-6/120e-6+5*.003,
                en_normal_v=[v/(1+100000/24600) for v in (18,26,36)],
                en_rise_nom_v=1.263*(1+100000/24600),
                en_fall_nom_v=1.263*(1-.28)*(1+100000/24600),
                on_time_26v_444k_ns=5.1/26/444400*1e9)


inputs.update({
    'crowbar_divider': value([1000, 100, 30, 1000], 'SELECTED', 'ohm', 'upper3 segments/lower1k'),
    'crowbar_30r_tcr': value(100e-6, 'ASSUMED', '/degC', '1% thick-film segment; exact maximum OPEN'),
    'crowbar_cathode_shift': value(.008, 'ASSUMED', 'V', 'Phase B 8mV lowering reserve'),
    'fault_l_screens': value([4.352e-6, 2e-6], 'ASSUMED', 'H', 'normal stressed L /saturation sensitivity'),
    'fault_c_screens': value([40e-6, 110e-6, 150e-6], 'ASSUMED', 'F', 'local only /raw lump /combined lump'),
    'fault_delays': value([.2e-6, .5e-6, 2e-6, 5e-6], 'ASSUMED', 's', 'total detector+PNP+SCR+commutation; no datasheet max'),
    'scr_igt_25': value(.015, 'KNOWN', 'A', 'TYN612RG maximum at25C'),
    'scr_cold_igt_screen': value(.030, 'ASSUMED', 'A', '2x25C max; cold maximum OPEN'),
    'scr_vgt_25': value(1.3, 'KNOWN', 'V', '25C test maximum; full-temp bound OPEN'),
    'scr_hot_model': value([.85, .030], 'KNOWN', 'V,ohm', 'ST on-state model at125C'),
    'fuse_i2t': value([1.65, 10.32], 'KNOWN', 'A2s', 'nominal melting F101/F301; not total clearing'),
    'scr_i2t': value(98, 'KNOWN', 'A2s', 'nonrepetitive25C specified pulse'),
})


def lc_fault(vin, vt, v0, i0, inductance, capacitance, delay):
    """Lossless single-node LC high-side short after complete load release.

    No source limit, constant L and C, ideal fuse. Not a Pi-pin bound.
    Exact solution avoids constant-acceleration error and retains pre-trip current.
    """
    w=1/math.sqrt(inductance*capacitance)
    z=math.sqrt(inductance/capacitance)
    def voltage(t):
        return vin+(v0-vin)*math.cos(w*t)+i0*z*math.sin(w*t)
    def current(t):
        return -(v0-vin)/z*math.sin(w*t)+i0*math.cos(w*t)
    def crossing(target):
        lo,hi=0,math.pi/(2*w)
        assert voltage(lo)<target<voltage(hi)
        for _ in range(80):
            mid=(lo+hi)/2
            if voltage(mid)<target:lo=mid
            else:hi=mid
        return (lo+hi)/2
    tt=crossing(vt)
    peak=voltage(tt+delay)
    # Internal checks of exact solution and energy, not hardware validation.
    assert abs(voltage(0)-v0)<1e-10
    assert abs(current(0)-i0)<1e-10
    e0=.5*capacitance*(v0-vin)**2+.5*inductance*i0**2
    e1=.5*capacitance*(peak-vin)**2+.5*inductance*current(tt+delay)**2
    assert math.isclose(e0,e1,rel_tol=1e-10)
    return dict(vin_v=vin, l_h=inductance, c_f=capacitance, delay_us=delay*1e6,
                trip_time_us=tt*1e6, trip_current_a=current(tt),
                allowed_delay_us=(crossing(5.5)-tt)*1e6,
                peak_cap_v=peak, screen_status='PASS' if peak<5.5 else 'FAIL')


def crowbar():
    e=.001+25e-6*65
    top_err=1100*e+30*(.01+100e-6*65)
    low=(2.483-.034-.008)*(1+(1130-top_err)/(1000*(1+e)))
    high=(2.507+.034)*(1+(1130+top_err)/(1000*(1-e)))+6.5e-6*(1130+top_err)
    b=buck()
    # Reference/ratio high plus half ripple and typical bias-current effect;
    # simultaneous full load release starts with maximum normal stressed peak current.
    v0=b['resistor_and_reference_screen_v'][1]+.001+b['ripple_pp_v']/2
    i0=b['rows'][2]['stressed_peak_a']
    faults=[lc_fault(vin,high,v0,i0,l,c,d)
            for vin in (24,26) for l in (4.352e-6,2e-6)
            for c in (40e-6,110e-6,150e-6) for d in (.2e-6,.5e-6,2e-6,5e-6)]
    gate=(low-.2-1.3)/(100*1.01)-1.3/(1000*.99)
    gate_pess=(low-.7-1.5)/(100*1.01)-1.5/(1000*.99)
    return dict(label='CALCULATED; temperature/delay/saturation assumptions unresolved',
                nominal_trip_v=2.495*(1+1130/1000),
                static_trip_screen_v=[low,high],
                normal_overshoot_budget_v=low-(b['resistor_and_reference_screen_v'][1]+.001+b['ripple_pp_v']/2),
                false_trip_margins_v=[low-n for n in b['normal_high_screens_v']],
                gate_nominal_screen_a=gate, gate_pessimistic_screen_a=gate_pess,
                base_drive_screen_a=(low-.9-2.5)/(500*1.01)-.9/(10000*.99),
                initial_fault_v=v0, initial_fault_a=i0, faults=faults,
                fuse_nominal_melt_s_at_50a=[q/50**2 for q in (1.65,10.32)],
                fuse_i2t_to_scr_ratio=10.32/98,
                local_loop_initial_di_dt_a_us=(5.5-1.3)/.010,
                # 10nH ASSUMED local loop gives 420A/us, not main inductor slope.
                local_cap_energy_j=.5*40e-6*5.5**2,
                total_cap_energy_j=.5*150e-6*5.5**2,
                fuse_clearing_source_current_for_5s_a=2*7,
                source_limit_and_clearing_time='OPEN: no authoritative UENPO limit/waveform')


inputs.update({
    'switch_edge_sum': value([10e-9, 30e-9], 'ASSUMED', 's', 'overlap-loss sensitivity, not vendor bound'),
    'buck_extra_loss': value([.1, .3], 'ASSUMED', 'W', 'LDO/gate/deadtime/Coss placeholder'),
    'inductor_ac_loss': value([.05, .3], 'ASSUMED', 'W', 'core/AC screen; vendor loss model OPEN'),
    'fet_hot_multiplier': value(2, 'ASSUMED', 'ratio', 'relative to117mohm at25C'),
    'thermal_ambient_target': value([50, 110], 'ASSUMED', 'degC', 'ambient/junction design screen, not requirements'),
    'scr_sink_interface': value(1, 'ASSUMED', 'degC/W', 'insulator/contact provisional'),
    'scr_fault_currents': value([2.2, 3, 5, 6, 10, 14], 'ASSUMED', 'A', 'source/clearing sensitivity only'),
})


def thermal():
    b=buck(); rows=[]
    for r in b['rows'][:3]:
        vin=r['vin_v']; duty=5.1/vin; irms=r['irms_a']
        cond=irms**2*(.082*duty+.045*(1-duty))
        sw=[.5*vin*5*t*400000 for t in (10e-9,30e-9)]
        buckloss=[cond+sw[0]+.1,cond+sw[1]+.3]
        gate_v=min(12,(vin-.2)*1000/1600)
        # Total steady controller/gate input power, including pullup and zeners.
        bias=vin*((vin-gate_v-.2)/600+(vin-12)/4000+(vin-12)/20000+vin/112000)
        railpower=5.1*5+25*.009+buckloss[1]+r['dcr_loss_100_w']+.3+bias
        resistance=2*.117*2+.0227
        # Vin*I = Pload+other losses+I^2*R for pessimistic constant-R estimate.
        i=(vin-math.sqrt(vin**2-4*resistance*railpower))/(2*resistance)
        rows.append(dict(vin_v=vin,buck_conduction_w=cond,buck_switching_screen_w=sw,
                         buck_total_screen_w=buckloss,control_gate_total_w=bias,
                         input_current_high_screen_a=i,input_fets_w=i*i*2*.117*2,
                         input_fuse_w=i*i*.0227,output_fuse_w=25*.009,
                         inductor_screen_w=[r['dcr_loss_100_w']+.05,r['dcr_loss_100_w']+.3],
                         total_efficiency_high_loss=25.5/(vin*i),
                         required_buck_theta_ja=(110-50)/buckloss[1]))
    scr=[]
    for i in (2.2,3,5,6,10,14):
        p=.85*i+.030*i*i
        scr.append(dict(current_a=i,power_w=p,free_air_rise_c=60*p,
                        required_total_theta=(110-50)/p,
                        allowable_sink_theta=(110-50)/p-1.3-1))
    return dict(label='CALCULATED; thermal hardware, enclosure and source waveform OPEN',
                normal=rows,scr=scr,correction='Phase B prose 5A/6A values wrong; correct5.00W/6.18W')


def make_bom():
    """Freeze exact analysis choices from dated Phase B offers; no fresh quotes.

    Prices for new/unspecified hardware remain explicit assumptions or OPEN.
    All protective/calibration/power parts are exact-MPN controlled for sourcing.
    """
    old=list(csv.DictReader((HERE/'PHASE_B_BOM.csv').open()))
    by_ref={r['ref']:r for r in old}
    obs=json.loads((ROOT/'third_party/v1a_lite_phase_b/LCSC_OBSERVATIONS.json').read_text())
    by_mpn={v['productModel']:v for v in obs.values() if 'productModel' in v}
    mapping={
        'D101':'D106', 'R101A R101B':'R101 R102', 'COUT1 COUT2':'C301 C302',
        'UCB':'U301','QCB':'Q301','RCB_TOP_A':'R301','RCB_TOP_B':'R302',
        'RCB_TOP_C':'R303','RCB_BOTTOM':'R304','RCB_BASE':'R305',
        'RCB_BE':'R306','RCB_GATE':'R307','RCB_GK':'R308','UIN_OV':'U101',
        'DIN_GS DIN_SUP':'D103 D104','DIN_SHIFT':'D105','RIN_TOP_A':'R150',
        'RIN_TOP_B RIN_BOTTOM':'R153',
        'RIN_PWR1 RIN_PWR2 RIN_PWR3 RIN_PWR4 RIN_PWR5 RIN_PWR6 RIN_PWR7 RIN_PWR8':' '.join('R'+str(n) for n in range(110,126)),
        'RIN_G1 RIN_G2 RIN_G3 RIN_G4 RIN_G5 RIN_G6':' '.join('R'+str(n) for n in range(130,136)),
        'RIN_GS RIN_K':'R140 R141 R142 R143 R144','RIN_BASE':'R145',
        'RIN_BE':'R146','CIN_CTRL':'C102','JIN JOUT':'J501 J502',
        'JIN_MATE JOUT_MATE':'MATE_IN MATE_OUT',
    }
    rows=[]
    for r0 in old:
        if not (r0['scope'].startswith('COMMON') or r0['scope'] in ('CROWBAR','OPT1','CONNECTORS')):
            continue
        r=dict(r0); original=r['ref']; refs=mapping.get(original,original)
        if original.startswith('RIN_PWR'):
            r=dict(by_ref['RCB_GK']);r['scope']='COMMON_INPUT'
            r['value']='16x1k; two parallel strings of8; net4k detector ballast'
        if original=='RIN_TOP_B RIN_BOTTOM':r['value']='10k input detector bottom'
        if original=='RIN_GS RIN_K':r['value']='4x1k series-parallel Q102 pullup +1k cathode feed'
        r['ref']=refs;r['qty']=len(refs.split());rows.append(r)
    extra=dict(by_ref['RCB_TOP_A']);extra.update(scope='COMMON_INPUT',ref='R151 R152',qty=2,value='2x1k input upper divider extension');rows.append(extra)
    fields=['ref','mpn','manufacturer','value','qty','unit','unit_vnd','extended_vnd','source',
            'access_date','price_label','selection_label','vietnam_local_realistic','local_basis',
            'safety_critical','substitute_allowed','scope','stock_observation','notes']
    out=[];D=Decimal;fx=D(26500)
    for r in rows:
        unit=D(r['costing_unit_usd'])*fx
        out.append(dict(ref=r['ref'],mpn=r['mpn'],manufacturer=r['manufacturer'],value=r['value'],
                        qty=int(r['qty']),unit='piece',unit_vnd=str(unit),extended_vnd=str(unit*int(r['qty'])),
                        source=r['source'],access_date=r['access_date'],price_label='KNOWN dated offer / CALCULATED FX extension',
                        selection_label='SELECTED analysis baseline; qualification OPEN',
                        vietnam_local_realistic='no',local_basis='OPEN exact local offer; imported only in saved evidence',
                        safety_critical='yes',substitute_allowed='no',scope=r['scope'],stock_observation=r['stock'],
                        notes=r['notes']))
    out.append(dict(ref='D101',mpn='SMCJ64CA',manufacturer='Bourns',value='64V bidirectional upstream TVS; 100V FET clamp screen FAIL',
                    qty=1,unit='piece',unit_vnd='13250',extended_vnd='13250',source='https://www.bourns.com/data/global/pdfs/SMCJ.pdf',
                    access_date='2026-10-05',price_label='ASSUMED USD0.50; exact quote OPEN',
                    selection_label='SELECTED costed candidate; surge coordination FAIL',vietnam_local_realistic='no',
                    local_basis='OPEN exact Bourns local offer; generic SMCJ not acceptable',safety_critical='yes',substitute_allowed='no',
                    scope='COMMON_INPUT',stock_observation='OPEN',notes='Price is allowance, not a manufacturer sales quote'))
    # Required physical hardware remains visible even though exact design depends on fault qualification.
    out.append(dict(ref='HS301 KIT301',mpn='OPEN',manufacturer='OPEN',value='SCR heatsink insulation mounting kit; required theta depends on source',
                    qty=1,unit='kit',unit_vnd='40000',extended_vnd='40000',source='Phase B accounting allowance; exact quote OPEN',
                    access_date='2026-10-05',price_label='ASSUMED',selection_label='OPEN exact thermal hardware',
                    vietnam_local_realistic='no',local_basis='OPEN exact rated assembly',safety_critical='yes',substitute_allowed='no',
                    scope='THERMAL_C_ONLY',stock_observation='OPEN',notes='Included once in C; not included in A/B electronic core'))
    out.append(dict(ref='HS101 HS102',mpn='OPEN',manufacturer='OPEN',value='Input FET fault thermal hardware if required by source envelope',
                    qty=1,unit='kit',unit_vnd='OPEN',extended_vnd='OPEN',source='Phase C fault thermal analysis',
                    access_date='2026-10-05',price_label='OPEN',selection_label='OPEN necessity/MPN/price',
                    vietnam_local_realistic='no',local_basis='OPEN',safety_critical='yes',substitute_allowed='no',
                    scope='UNPRICED',stock_observation='OPEN',notes='Not zero; totals incomplete until thermal solution resolved'))
    with (HERE/'PHASE_C_BOM.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(out)
    physical=[r for r in out if r['scope'] not in ('THERMAL_C_ONLY','UNPRICED')]
    refs=[ref for r in physical for ref in r['ref'].split()]
    assert len(refs)==len(set(refs)), 'duplicate planned component reference'
    for r in physical:
        assert r['qty']==len(r['ref'].split()), r['ref']
        assert D(r['extended_vnd'])==D(r['unit_vnd'])*r['qty'], r['ref']
        assert r['safety_critical']=='yes' and r['substitute_allowed']=='no'
    core=[r for r in out if r['scope'] not in ('CONNECTORS','THERMAL_C_ONLY','UNPRICED')]
    counts=Counter()
    for r in core:counts[r['mpn']]+=r['qty']
    purchases=[]
    for mpn,n in sorted(counts.items()):
        need=n+max(1,math.ceil(.25*n))
        if mpn=='SMCJ64CA':
            buy=need;unit=D('.5');moq='OPEN';label='ASSUMED unit and buy increment; exact quote OPEN';source=out[-3]['source']
        else:
            o=by_mpn[mpn];moq=o['minBuyNumber'];buy=math.ceil(max(need,moq)/moq)*moq
            tier=[t for t in o['productPriceList'] if t['ladder']<=buy][-1]
            unit=D(tier['productPrice']);label='CALCULATED from dated offer; MOQ as provisional increment';source=o['url']
        purchases.append(dict(mpn=mpn,installed_qty=n,needed_with_spares=need,buy_qty=buy,moq=moq,
                              unit_usd=str(unit),extended_vnd=str(unit*buy*fx),label=label,source=source))
    with (HERE/'PHASE_C_PURCHASE_MODEL.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(purchases[0]),lineterminator='\n');w.writeheader();w.writerows(purchases)
    A=sum(D(r['extended_vnd']) for r in core)
    connectors=sum(D(r['extended_vnd']) for r in out if r['scope']=='CONNECTORS')
    connector_buy=(D('.1607')*5+D('.11')*3+D('.08810')*100)*fx
    cash=sum(D(r['extended_vnd']) for r in purchases)
    overhead={'pcb_five_board_lot':53000,'wire_fanout':35000,'shipping_tax':180000,
              'assembly_consumables':50000,'rework':50000,'scr_sink_kit':40000}
    C=cash+connector_buy+sum(overhead.values())
    return dict(label='CALCULATED planning totals; NOT a complete qualified purchase quote',
                fx=value(26500,'ASSUMED','VND/USD','Phase A/B accounting convention, not spot rate'),
                A_core_vnd=str(A),A_dated_price_subtotal_vnd=str(A-D(13250)),
                A_new_tvs_allowance_vnd='13250',B_core_board_connectors_vnd=str(A+connectors+D(10600)),
                C_first_build_vnd=str(C),core_purchase_with_spares_vnd=str(cash),
                connector_purchase_vnd=str(connector_buy),connectors_installed_vnd=str(connectors),
                overhead_assumed_vnd=overhead,unpriced='Input FET fault thermal hardware and safety redesign; not zero',
                headroom_to_1000000_vnd=str(D(1000000)-C),budget_status='FAIL estimate; exact landed total OPEN',
                bom_lines=len(out),unique_core_mpns=len(counts))


def calculate():
    result = {'label': 'CALCULATED; conditional screens, no hardware validation',
              'inputs': inputs,
              'input_ratings': {'label': 'CALCULATED', 'fet_dc_margin_v': 100-64,
                                'tvs_to_fet_margin_v': 100-103,
                                'powered_reverse_margin_v': 100-(64+36)}}
    result['input_cutoff'] = input_cutoff()
    result['buck'] = buck()
    result['crowbar'] = crowbar()
    result['thermal'] = thermal()
    result['totals'] = make_bom()
    c=result['crowbar'];b=result['buck'];cut=result['input_cutoff']
    representative=next(f for f in c['faults'] if f['vin_v']==24 and f['l_h']==4.352e-6
                        and f['c_f']==110e-6 and f['delay_us']==.5)
    result['checks'] = {
        '01_input_64V_FET_DC_voltage_only': 'PASS' if 100>64 else 'FAIL',
        '02_upstream_TVS_to_100V_FET': 'PASS' if 103<100 else 'FAIL',
        '03_input_trip_static_screen': 'PASS' if 26<cut['static_trip_screen_v'][0]<cut['static_trip_screen_v'][1]<36 else 'FAIL',
        '04_input_VIN_never_above_36V': 'OPEN',
        '05_input_bias_timing_startup_release_SOA': 'OPEN',
        '06_reverse_and_powered_reversal': 'OPEN',
        '07_buck_L_and_catalog_Isat_screens': 'PASS' if 18>11.5 and 4.352e-6>b['min_l_h'] else 'FAIL',
        '08_capacitance_ripple_current_loop_margin': 'OPEN',
        '09_Pi_normal_window_5A_harness': 'OPEN',
        '10_crowbar_HS_short_24V_0p5us_screen': representative['screen_status'],
        '11_crowbar_max_IGT_VGT_delay_over_temp': 'OPEN',
        '12_fuse_SCR_UENPO_clearing': 'OPEN',
        '13_raw_16V_caps_after_output_fuse_opens': 'FAIL',
        '14_unsinked_SCR_indefinite_fault': 'FAIL',
        '15_whole_board_thermal': 'OPEN',
        '16_cost_C_under_1000000': 'PASS' if Decimal(result['totals']['C_first_build_vnd'])<1000000 else 'FAIL',
        '17_exact_local_sourcing_and_full_cost': 'OPEN',
        '18_removed_function_and_bench_plan_documented': 'PASS',
        '19_Phase_D_change_list_documented': 'PASS',
        '20_hardware_qualification': 'OPEN',
    }
    result['selected_mpns'] = {
        'input_fets':'2x IRF9540NPBF', 'input_tvs_candidate':'Bourns SMCJ64CA (surge coordination FAIL)',
        'protected_tvs':'TVS3300DRVR', 'input_fuse':'0451003.MRL',
        'detectors':'2x TL431BIDBZR', 'gate_clamps':'BZT52C12-7-F',
        'level_shift':'BZT52C3V3-7-F', 'gate_sink':'MMBTA42-TP',
        'buck':'LM61460AANRJRR', 'inductor':'SRP1265A-6R8M',
        'input_ceramics':'GRM32ER71H106KA12L', 'input_bulk':'EEUFR1H101',
        'output_ceramics':'GRM32ER61C476KE15L (raw fault rating FAIL)',
        'output_fuse':'0451007.MRL', 'scr':'TYN612RG', 'scr_driver':'BC807-40,215',
    }
    return result


# Phase C2 is an additive review. Original Phase C outputs remain historical.
def c2_rk4(state, dt, derivative):
    k1 = derivative(state)
    k2 = derivative([v+dt*k/2 for v,k in zip(state,k1)])
    k3 = derivative([v+dt*k/2 for v,k in zip(state,k2)])
    k4 = derivative([v+dt*k for v,k in zip(state,k3)])
    return [v+dt*(a+2*b+2*c+d)/6 for v,a,b,c,d in zip(state,k1,k2,k3,k4)]


def c2_esr_fault(vin, inductance, ceramic_c, bulk_c, bulk_r, dt=1e-8):
    """Separate ceramic and bulk capacitor states; ESRs are modeling inputs.

    Load is released, source is stiff during first microseconds. Pi voltage
    equals raw only in the zero-impedance interface screen, not a pin bound.
    """
    old = crowbar(); vt = old['static_trip_screen_v'][1]
    initial = old['initial_fault_v']; rc = .003
    state = [old['initial_fault_a'], initial, initial]
    def node(s):
        i,vc,vb=s
        return (i+vc/rc+vb/bulk_r)/(1/rc+1/bulk_r)
    def derivative(s):
        v=node(s);i,vc,vb=s
        return [(vin-v)/inductance,(v-vc)/(rc*ceramic_c),(v-vb)/(bulk_r*bulk_c)]
    crossings={}; samples=[]; old_v=node(state); t=0
    for _ in range(12000):
        samples.append((t,old_v,state[0]))
        if vt in crossings and t>=crossings[vt]+5.01e-6:break
        new=c2_rk4(state,dt,derivative);new_v=node(new)
        for target in (vt,5.5,10,16,25):
            if target not in crossings and old_v<target<=new_v:
                crossings[target]=t+dt*(target-old_v)/(new_v-old_v)
        state=new;old_v=new_v;t+=dt
    assert vt in crossings and 5.5 in crossings
    def interp(t):
        n=min(int(t/dt),len(samples)-2);f=(t-samples[n][0])/dt
        return samples[n][1]*(1-f)+samples[n+1][1]*f
    peaks={str(d):interp(crossings[vt]+d*1e-6) for d in (.5,2,5)}
    return dict(vin_v=vin,l_h=inductance,ceramic_c_f=ceramic_c,bulk_c_f=bulk_c,
                bulk_esr_ohm=bulk_r,trip_us=crossings[vt]*1e6,
                allowed_delay_us=(crossings[5.5]-crossings[vt])*1e6,
                pi_peak_unity_interface_v=peaks,
                screen_status={d:'PASS' if v<5.5 else 'FAIL' for d,v in peaks.items()})


def c2_pi_fault(delay_us, harness_l, harness_r, dt=1e-8):
    """Illustrative two-node transient, including cable stored current.

    Ideal abrupt SCR establishment after chosen delay; source holds 24 V until
    I reaches ASSUMED 50 A after firing. This is NOT a source specification.
    Early 40-us window only; late SCR stress separately calculated.
    """
    c=crowbar();rc=.003;rb=.014;cc=110e-6;cb=1600e-6;cp=40e-6;l=4.352e-6
    s=[c['initial_fault_a'],c['initial_fault_v'],c['initial_fault_v'],5,
       c['initial_fault_v']-5*harness_r]
    fired=False;trip=None;peak=s[4];peak_raw=0;t=0
    def raw(s):
        i,vc,vb,ih,vp=s;g=1/rc+1/rb;n=i-ih+vc/rc+vb/rb
        if fired:g+=1/.030;n+=.85/.030
        return n/g
    def deriv(s):
        v=raw(s);i,vc,vb,ih,vp=s;di=(24-v)/l
        if fired and i>=50 and di>0:di=0
        return [di,(v-vc)/(rc*cc),(v-vb)/(rb*cb),
                (v-vp-harness_r*ih)/harness_l,ih/cp]
    for _ in range(round(40e-6/dt)):
        v=raw(s)
        if trip is None and v>=c['static_trip_screen_v'][1]:trip=t
        if trip is not None and t>=trip+delay_us*1e-6:fired=True
        peak=max(peak,s[4]);peak_raw=max(peak_raw,raw(s))
        s=c2_rk4(s,dt,deriv);t+=dt
    assert fired
    return dict(delay_us=delay_us,harness_l_h=harness_l,harness_r_ohm=harness_r,
                pi_peak_v=peak,raw_peak_v=peak_raw,
                status='PASS' if peak<5.5 else 'FAIL')


def c2_thermal_waveform(current, cutoff_s, vin):
    """Illustrative transient-temperature estimate, NOT guaranteed thermal Z.

    ST Fig4 short-time diffusion extrapolation below 1 ms; fixed-case response
    plus adiabatic case rise for ASSUMED 0.1 J/K package thermal capacitance.
    No external heatsink. Separate cap/source waveforms approximate electrical
    coupling. Local turn-on current spreading is not represented.
    """
    step=2e-6;end=cutoff_s+.001;co=.0028418;ci=.000164
    inp=[vin,current];powers=[];energy=0
    for n in range(math.ceil(end/step)):
        t=(n+.5)*step
        source=current if t<cutoff_s else 0
        output=150*math.exp(-t/(.031*co))
        input_i=0
        if t>=cutoff_s:
            if inp[1]>0:
                input_i=inp[1]
                inp=c2_rk4(inp,step,lambda s:[-s[1]/ci,(s[0]-.85-.0415*s[1])/4.352e-6])
        i=source+output+input_i;p=.85*i+.030*i*i
        energy+=p*step;powers.append(p)
    def zjc(t):
        if t<=0:return 0
        # .17*1.3 at1ms and .5*1.3 at10ms, approximate curve readings.
        if t<.001:return .221*math.sqrt(t/.001)
        return .221*(t/.001)**(math.log(.65/.221)/math.log(10))
    best=(0,0);case_energy=0
    for k in range(1,len(powers)+1):
        case_energy+=powers[k-1]*step
        if k%5 and k!=len(powers):continue
        rise=sum(p*(zjc((k-j)*step)-zjc((k-j-1)*step)) for j,p in enumerate(powers[:k]))
        tj=50+rise+case_energy/.1
        if tj>best[0]:best=(tj,k*step)
    return dict(tj_estimate_no_sink_c=best[0],peak_time_us=best[1]*1e6,
                scr_energy_waveform_j=energy,case_capacity_assumed_j_k=.1,
                label='CALCULATED from ASSUMED waveform and extrapolated Zjc; max temperature OPEN')


def c2_pulse_stress(current, cutoff_s, vin, dt=1e-7):
    """Source rectangle + output RC discharge + isolated input RLC discharge.

    Full reservoir retained at cutoff is a conservative energy sensitivity.
    Input discharge may in reality start earlier; 3*sum(I2t) bounds arbitrary
    overlap of these three positive modeled current components. No fuse credit.
    """
    co=(6*47e-6*1.2+2*47e-6*1.1+2*1000e-6*1.2)
    ci=100e-6*1.2+4*10e-6*1.1  # nominal upper initial tolerance; not hot guarantee
    ro=.031;dv=5.5-.85
    qout=co*dv;i2out=dv*dv*co/(2*ro)
    s=[vin,current];qinp=0;i2inp=0;pin_peak=current;t=0
    def deriv(s):
        v,i=s
        return [-i/ci,(v-.85-i*(.030+.0115))/4.352e-6]
    while s[1]>0 and t<.01:
        n=c2_rk4(s,dt,deriv)
        if n[1]<0:
            dt_last=dt*s[1]/(s[1]-n[1]);qinp+=s[1]*dt_last/2;i2inp+=s[1]**2*dt_last/3
            t+=dt_last;break
        qinp+=(s[1]+n[1])*dt/2;i2inp+=(s[1]**2+n[1]**2)*dt/2
        pin_peak=max(pin_peak,n[1]);s=n;t+=dt
    i2source=current**2*cutoff_s
    i2bound=3*(i2source+i2out+i2inp)
    qtotal=current*cutoff_s+qout+qinp
    energy=.85*qtotal+.030*i2bound
    return dict(vin_v=vin,source_current_a=current,cutoff_ms=cutoff_s*1000,
                output_c_max_f=co,input_c_max_f=ci,
                source_i2t_a2s=i2source,output_i2t_a2s=i2out,input_i2t_a2s=i2inp,
                overlap_bound_i2t_a2s=i2bound,ratio_to_98=i2bound/98,
                output_peak_model_a=dv/ro,input_peak_model_a=pin_peak,
                total_peak_sum_bound_a=current+dv/ro+pin_peak,
                output_energy_stored_j=.5*co*5.5**2,input_energy_stored_j=.5*ci*vin**2,
                scr_energy_screen_j=energy,input_tail_to_zero_us=t*1e6,
                thermal_waveform=c2_thermal_waveform(current,cutoff_s,vin),
                # Effective silicon heat capacity is ASSUMED, not a vendor specification.
                adiabatic_tj_at_50C_for_Cth_2mJ_10mJ=[50+energy/.002,50+energy/.010],
                source_only_tj_10ms_Zja_envelope=50+1.8*(.85*current+.030*current**2))


def c2_bom_and_costs():
    D=Decimal;fx=D(26500)
    rows=list(csv.DictReader((HERE/'PHASE_C_BOM.csv').open()))
    old_by_ref={r['ref']:r for r in rows}
    obs=json.loads((ROOT/'third_party/v1a_lite_phase_b/LCSC_OBSERVATIONS.json').read_text())
    obs.update(json.loads((ROOT/'third_party/v1a_lite_phase_c2/LCSC_OBSERVATIONS.json').read_text()))
    offers={v['productModel']:v for v in obs.values() if 'productModel' in v}
    for r in rows:
        r['qty']=int(r['qty'])
        if r['ref'].startswith('C209 '):
            o=offers['GRM31CR61E476ME44L'];r.update(mpn=o['productModel'],value='47uF 25V X5R 1206 raw; containment OPEN',unit_vnd=str(D('.6136')*fx),source=o['url'],access_date='2026-10-05',stock_observation=str(o['stockNumber']),notes='Rating upgrade only; 25V still below 26-29V uncontained fault; effective C and footprint requalification required')
            r['extended_vnd']=str(D(r['unit_vnd'])*r['qty'])
        if r['ref']=='F301':r['value']='7A wiring backup AFTER raw crowbar; no OV-clearing duty'
        if r['ref']=='HS301 KIT301':
            r['value']='Unqualified thermal contingency; no heatsink fitted in C2 event model'
            r['notes']='40k kept in C until no-heatsink event survival qualified; zero-sink sensitivity separate'
        r['selection_label']='SELECTED C2 analysis candidate; NOT FOR FABRICATION'
    def clone(original,refs,value_):
        r=dict(old_by_ref[original]);r.update(ref=refs,qty=len(refs.split()),value=value_,scope='LATCH_C2',selection_label='PROPOSED Q102 latch implementation; qualification OPEN')
        r['extended_vnd']=str(D(r['unit_vnd'])*r['qty']);rows.append(r)
    clone('Q103','Q104 Q106','MMBTA42 latch NPN / Q103 base clamp')
    clone('Q301','Q105','BC807 regenerative latch PNP; emitter CTRL12')
    clone('R145','R160 R161 R162 R163','10k latch collector feedback trigger and clamp-base drives')
    clone('R146','R164 R165 R166','100k latch transistor base-emitter bleeds')
    o=offers['EEUFR1A102'];r=dict(old_by_ref['C101'])
    r.update(ref='C217 C218',mpn=o['productModel'],qty=2,value='1000uF 10V FR raw-node bulk; pulse/rating OPEN',unit_vnd=str(D('.1751')*fx),extended_vnd=str(2*D('.1751')*fx),source=o['url'],access_date='2026-10-05',stock_observation=str(o['stockNumber']),scope='COMMON_BUCK',selection_label='SELECTED two-cap C2 cost candidate; qualification OPEN',notes='28mohm catalog impedance used as ASSUMED ESR; 1.79A ripple each')
    rows.append(r)
    fields=list(rows[0])
    with (HERE/'PHASE_C2_BOM.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    physical=[r for r in rows if r['scope'] not in ('THERMAL_C_ONLY','UNPRICED')]
    refs=[ref for r in physical for ref in r['ref'].split()]
    assert len(refs)==len(set(refs))
    core=[r for r in physical if r['scope']!='CONNECTORS'];counts=Counter()
    for r in core:
        assert D(r['unit_vnd'])*r['qty']==D(r['extended_vnd'])
        counts[r['mpn']]+=r['qty']
    local_basis=json.loads((ROOT/'third_party/v1a_lite_phase_c2/LOCAL_SOURCING_BASIS.json').read_text())
    local={r['mpn']:r for r in local_basis['rows'] if r['route'].startswith('Local')}
    purchases=[]
    for method in ('phase_c_spares','local_plan_spares'):
        for mpn,n in sorted(counts.items()):
            need=n+(max(1,math.ceil(.25*n)) if method=='phase_c_spares' else 1)
            if method=='local_plan_spares' and mpn in local:
                lr=local[mpn];cost=D(lr['cost_vnd']);buy=lr['buy'];unit=None
                # Existing shared 100nF 10-piece lot has enough for 3 installed+spares;
                # 10k and 100k additions also fit unchanged local 50-piece lots.
                assert need<=50
                label='ASSUMED approved-equivalent local candidate; saved plan lot once/allocated share'
            else:
                if mpn=='SMCJ64CA':buy=need;unit=D('.5');label='ASSUMED TVS allowance; rejected coordination candidate'
                else:
                    o=offers[mpn];moq=o['minBuyNumber'];buy=math.ceil(max(need,moq)/moq)*moq
                    unit=D([t for t in o['productPriceList'] if t['ladder']<=buy][-1]['productPrice'])
                    label='KNOWN dated offer / CALCULATED quantity; stock/landed quote OPEN'
                cost=unit*buy*fx
            purchases.append(dict(method=method,mpn=mpn,installed=n,target=need,buy=buy,
                                  unit_usd=str(unit) if unit is not None else 'local lot',cost_vnd=str(cost),label=label))
    with (HERE/'PHASE_C2_PURCHASE_MODEL.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(purchases[0]),lineterminator='\n');w.writeheader();w.writerows(purchases)
    A=sum(D(r['extended_vnd']) for r in core)
    connectors=sum(D(r['extended_vnd']) for r in physical if r['scope']=='CONNECTORS')
    cash={m:sum(D(r['cost_vnd']) for r in purchases if r['method']==m) for m in ('phase_c_spares','local_plan_spares')}
    overhead={'pcb_five_board_lot':53000,'wire_fanout':35000,'shipping_tax':180000,'assembly_consumables':50000,'rework':50000,'thermal_contingency':40000}
    local_overhead={'pcb_five_board_lot':53000,'local_connectors':4719,'wire_heatshrink':20000,'lcsc_shipping_import_reserve':80000,'pcb_shipping_tax_reserve':120000,'local_delivery_reserve':20000,'assembly_consumables':50000,'rework_reserve':50000,'thermal_contingency':40000}
    C=cash['phase_c_spares']+D('263502.75')+sum(overhead.values())
    CL=cash['local_plan_spares']+sum(local_overhead.values())
    return dict(label='CALCULATED planning estimates; unpriced safety qualification/redesign remains OPEN',A_core_vnd=str(A),B_core_board_connectors_vnd=str(A+connectors+10600),C_first_build_vnd=str(C),C_local_sourcing_vnd=str(CL),C_gap_vnd=str(C-1000000),C_local_gap_vnd=str(CL-1000000),core_purchase_vnd={k:str(v) for k,v in cash.items()},overhead_assumed_vnd=overhead,local_overhead_assumed_vnd=local_overhead,local_without_thermal_contingency_vnd=str(CL-40000),local_pickup_without_thermal_contingency_vnd=str(CL-60000),unpriced='Input-FET thermal hardware; compliant surge coordination; latch reset/hold-up; qualified capacitor/SCR solution. Not zero.',local_plan_source_sha256=local_basis['sha256'])


def calculate_c2():
    old=json.loads((HERE/'PHASE_C_CALCULATIONS.json').read_text()); b=buck();c=crowbar()
    candidates=[dict(mpn='EEUFR1A102',c_f=.001,esr_ohm=.028,ripple_a=1.79,rated_v=10,unit_usd='.1751',qty=q) for q in (1,2)]
    candidates += [dict(mpn='6SEPC470M+TS',c_f=470e-6,esr_ohm=.008,ripple_a=5.7,rated_v=6.3,unit_usd='1.0743',qty=q) for q in (1,2)]
    rows=[];ideal=[]
    for cap in candidates:
        for vin in (24,26):
            for l in (4.352e-6,2e-6):
                for cc in (110e-6,40e-6):
                    x=c2_esr_fault(vin,l,cc,cap['c_f']*.8*cap['qty'],cap['esr_ohm']/cap['qty']);x.update(mpn=cap['mpn'],qty=cap['qty']);rows.append(x)
                x=lc_fault(vin,c['static_trip_screen_v'][1],c['initial_fault_v'],c['initial_fault_a'],l,110e-6+cap['c_f']*.8*cap['qty'],.5e-6)
                x.update(mpn=cap['mpn'],qty=cap['qty']);ideal.append(x)
    thresholds=[]
    for segment in (0,20,24.9,27,30):
        e=.001+25e-6*65;top=1100+segment;er=1100*e+segment*(.01+100e-6*65)
        lo=(2.483-.034-.008)*(1+(top-er)/(1000*(1+e)))
        hi=(2.507+.034)*(1+(top+er)/(1000*(1-e)))+6.5e-6*(top+er)
        thresholds.append(dict(segment_ohm=segment,low_v=lo,high_v=hi,margins_for_25mV_100mV_v=[lo-n for n in b['normal_high_screens_v']]))
    # Gate max charge at its specified test condition; scaled to 13.35 V as an ASSUMED screen.
    qgate=97e-9*13.35/10;gate_us=qgate/(1/1000)*1e6
    latch=[]
    for vin in (18,24,26,64):
        # In latched state, CTRL12 feeds three latch branches and old 11k chain.
        def consumption(v):
            old_detector=(v-2.5)/1000 if vin==64 else (v-3.5)/11000
            return 3*(v-.9)/10000+.7/100000+old_detector
        ctrl=min(12,(vin/4000+3*.9/10000-.7/100000+3.5/11000)/(1/4000+3/10000+1/11000))
        latch.append(dict(vin_v=vin,ctrl12_v=ctrl,branch_drive_a=(ctrl-.9)/10000,old_gate_base_sink_a=0 if vin==64 else (ctrl-3.5)/11000,ballast_w=(vin-ctrl)**2/4000,ctrl12_load_a=consumption(ctrl)))
    pulses=[c2_pulse_stress(i,t,vin) for vin in (24,64) for i in (3,10,50,100) for t in (.00015,.001)]
    fet=[]
    for vin in (24,64):
        for i in (3,10,50,100):
            for t in (150e-6,1e-3):
                # Graph-read padded Zjc screens, fixed case; not free-air bounds.
                z=.16 if t==150e-6 else .45
                fet.append(dict(vin_v=vin,current_a=i,overlap_us=t*1e6,rectangular_energy_j=vin*i*t,zjc_screen_c_w=z,tj_fixed_case_50C=50+vin*i*z,status='FAIL' if 50+vin*i*z>175 else 'OPEN'))
    costs=c2_bom_and_costs()
    selected=next(x for x in rows if x['mpn']=='EEUFR1A102' and x['qty']==2 and x['vin_v']==24 and x['l_h']==4.352e-6 and x['ceramic_c_f']==110e-6)
    result=dict(label='CALCULATED C2 screens; SELECTED parts are cost candidates, no qualification',baseline_head='b5461b0bc5eaae874c3c3ed869dfb03d5295827b',inputs={
        'inherited_phase_c_inputs':old['inputs'],
        'bulk_capacitance_factor':value(.8,'ASSUMED','fraction','initial -20% only; temperature/endurance minima OPEN'),
        'bulk_esr':value([.028,.008],'ASSUMED','ohm','FR catalog |Z| modeled as R; polymer ESR at stated frequency; cold/endurance/ESL OPEN'),
        'raw_ceramic_screens':value([110e-6,40e-6],'ASSUMED','F','not new 25V Murata guaranteed effective C'),
        'latch_storage_tail':value(20e-6,'ASSUMED','s','transistor storage, feedback capture and gate tail; not maximum'),
        'source_currents':value([3,10,50,100],'ASSUMED','A','sensitivity only; UENPO bound OPEN'),
        'cutoff_screens':value([.00015,.001],'ASSUMED','s','150us rounded gate screen /1ms missed deadline sensitivity'),
        'scr_effective_heat_capacity':value([.002,.010],'ASSUMED','J/K','adiabatic sensitivity only; not vendor silicon thermal capacitance'),
        'scr_Zja_10ms_envelope':value(1.8,'ASSUMED','K/W','rounded upper graphical reading 0.03*60 from ST Fig5; source rectangle only'),
        'fet_Zjc_envelope':value([.16,.45],'ASSUMED','K/W','padded graphical reads Fig11 for150us/1ms; fixed case50C only'),
        'pi_harness_L':value([.2e-6,1e-6,2e-6],'ASSUMED','H','sensitivity; harness specification OPEN'),
        'pi_harness_R':value([.009,.059],'ASSUMED','ohm','cold F301 alone /plus50mohm harness'),
    },bulk_candidates=candidates,thresholds=thresholds,normal_ripple_sensitivity=[dict(ceramic_c_f=cc,ripple_pp_v=b['rows'][2]['stressed_ripple_a']*(1/(8*356400*cc)+.003),normal_high_25mV_v=b['resistor_and_reference_screen_v'][1]+.001+.025+b['rows'][2]['stressed_ripple_a']*(1/(8*356400*cc)+.003)/2) for cc in (40e-6,110e-6,120e-6)],ideal_lumped_faults=ideal,esr_faults=rows,selected_fault=selected,
        pi_two_node_screens=[c2_pi_fault(d,l,r) for d in (.5,2,5) for l in (.2e-6,1e-6,2e-6) for r in (.009,.059)],
        latch_bias=latch,cutoff=dict(q101_forward_isolation='FAIL: body diode, no finite isolation time',tl431_max_propagation_s=None,scr_max_tgt_s=None,q102_max_qg_at_test_c=97e-9,q102_max_qgd_at_test_c=51e-9,scaled_gate_charge_c=qgate,gate_to_1V_screen_us=gate_us,latch_to_off_screen_us=gate_us+20,guaranteed_off_delay_us=None),
        scr_single_event=pulses,fet_turnoff=fet,totals=costs,
        changed_mpns={'C217_C218':'2x EEUFR1A102','C209_C214':'6x GRM31CR61E476ME44L (25V; 1206 replaces1210)','Q104_Q106':'2x MMBTA42-TP added','Q105':'1x BC807-40,215 added','R160_R163':'4x 0805W8F1002T5E added','R164_R166':'3x 0603WAF1003T5E added'},
        checks={
          '01_raw_crowbar_no_intervening_fuse_topology':'PASS',
          '02_literal_Q101_only_input_isolation':'FAIL',
          '03_Q102_latch_static_bias_screen':'PASS',
          '04_power_removal_only_reset_and_max_cutoff_delay':'OPEN',
          '05_selected_24V_0p5us_unity_interface_screen':selected['screen_status']['0.5'],
          '06_selected_24V_2us_unity_interface_screen':selected['screen_status']['2'],
          '07_guaranteed_Pi_pin_less_than_5p5V':'OPEN',
          '07b_Pi_1uH_59mohm_0p5us_sensitivity':'FAIL',
          '08_normal_nuisance_trip_100mV_screen':'FAIL',
          '09_F301_open_no_longer_disconnects_raw_SCR':'PASS',
          '10_25V_caps_at_uncontained_26_to_29V':'FAIL',
          '11_guaranteed_raw_cap_voltage_containment':'OPEN',
          '12_SCR_local_10nH_di_dt_screen':'FAIL',
          '13_SCR_I2t_temperature_no_heatsink_qualification':'OPEN',
          '14_SCR_holding_current_zero_current_and_backfeed':'OPEN',
          '15_FET_24V_64V_turnoff_hot_SOA':'OPEN',
          '16_existing_103V_TVS_to_100V_FET':'FAIL',
          '17_cost_C_under_1000000':'PASS' if Decimal(costs['C_first_build_vnd'])<1000000 else 'FAIL',
          '18_local_cost_C_under_1000000':'PASS' if Decimal(costs['C_local_sourcing_vnd'])<1000000 else 'FAIL',
          '19_Phase_D_change_list_and_C2_evidence':'PASS',
          '20_R1_release_hardware_qualification':'OPEN'})
    result['reproducer_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['baseline_json_sha256']=hashlib.sha256((HERE/'PHASE_C_CALCULATIONS.json').read_bytes()).hexdigest()
    (HERE/'PHASE_C2_REVISION.json').write_text(json.dumps(result,indent=2)+'\n')
    for name,status in result['checks'].items(): print(f'{status}: {name}')
    print('SELECTED changed MPNs: '+json.dumps(result['changed_mpns']))
    print('CALCULATED totals: '+json.dumps(costs))
    return result


def main():
    import sys
    if "--c2" in sys.argv:
        calculate_c2()
        return
    result = calculate()
    result['reproducer_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / 'PHASE_C_CALCULATIONS.json').write_text(json.dumps(result, indent=2)+'\n')
    for name,status in result['checks'].items():
        print(f'{status}: {name}')
    print('SELECTED analysis MPNs: '+json.dumps(result['selected_mpns']))
    print('CALCULATED planning totals VND: A='+result['totals']['A_core_vnd']+
          ' B='+result['totals']['B_core_board_connectors_vnd']+
          ' C='+result['totals']['C_first_build_vnd']+'; complete qualified total OPEN')


if __name__ == '__main__':
    main()
