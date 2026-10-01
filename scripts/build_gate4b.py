#!/usr/bin/env python3
"""Capture one authorized Gate4B sheet; no PCB, git or export side effects."""
import argparse, copy, csv, json, re, math
from pathlib import Path
import xml.etree.ElementTree as ET
from build_r2_schematic import Sheet, normalize, library_symbol, q, fx, uid
from build_sheet03_preliminary import children
from make_schematic_readable import parse, dump

ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware/kicad'
EV=ROOT/'docs/evidence/r2/gate4b'
STATUS='PRELIMINARY TEST BOARD — R2 BLOCKED — NOT FOR FABRICATION'
NAMES={'input':'01_INPUT_PROTECTION','buck':'02_BUCK_5V','output':'03_OUTPUT_PROTECTION','monitor':'04_POWER_MONITOR','io':'05_IO_TEST'}


def baseline(block):
    d=json.loads((ROOT/f'docs/evidence/r2/{block}_block.json').read_text())
    xml=ET.parse(ROOT/'docs/evidence/r2/footprints_complete/completed.xml')
    actual={c.get('ref'):c for c in xml.findall('./components/comp')}
    for c in d['components']:
        if c['ref'] in actual:
            a=actual[c['ref']]
            c['footprint']=a.findtext('footprint','')
            c['value']=a.findtext('value')
            fields={p.get('name'):p.text for p in a.findall('./fields/field')}
            c['part']=fields.get('MPN') or c.get('part') or c['value']
    s=(HW/(NAMES[block]+'.kicad_sch')).read_text()
    d['ports']={re.search(r'\(hierarchical_label\s+"([^"]+)"',t)[1]:re.search(r'\(shape ([^)]+)\)',t)[1] for _,_,t in children(s) if t.startswith('(hierarchical_label')}
    d['status']=STATUS
    return d


def pin(name,net,typ='passive'):
    return {'name':name,'net':net,'type':typ}


def part(ref,mpn,value,footprint,pins,kind='IC',source='Gate4A 898759e freeze; Gate4B pin review'):
    return dict(ref=ref,part=mpn,value=value,footprint=footprint,pins={str(n):p for n,p in pins.items()},kind=kind,source=source,rating='DATASHEET nominal; application limits OPEN')


def update(c,mpn,value=None,footprint=None):
    c['part']=mpn
    if value is not None:c['value']=value
    if footprint is not None:c['footprint']=footprint
    c['source']='Gate4A 898759e freeze; Gate4B PIN_REVIEW.md'
    c['rating']='DATASHEET nominal; derating / application qualification OPEN'


def apply_passives(d):
    rows={r['refdes']:r for r in csv.DictReader((EV/'PASSIVE_COMPLETION.csv').open())}
    for c in d['components']:
        r=rows.get(c['ref'])
        if not r:continue
        mpn=r['new_mpn'];fp=passive_fp(mpn,c['kind'])
        value=re.sub(r'(0\.1%.*|0603|0805|1206)$', '', r['value'].split(' X')[0]).strip()
        value=value.replace('zero-ohm','0').replace('nF50V','nF 50V').replace('uF25V','uF 25V').replace('uF50V','uF 50V')
        update(c,mpn,value,fp)


def passive_fp(mpn,kind):
    size=next((s for s in ('0603','0805','1206','2512') if s in mpn),None)
    if kind=='R':return 'Resistor_SMD:R_'+(size or '0603')+'_'+{'0603':'1608','0805':'2012','1206':'3216','2512':'6332'}[size or '0603']+'Metric'
    size=('1210' if mpn.startswith('GRM32') else '1206' if mpn.startswith('C3216') else '0805' if mpn.startswith('GRM21') else '0603')
    return f'Capacitor_SMD:C_{size}_'+{'1210':'3225','1206':'3216','0805':'2012','0603':'1608'}[size]+'Metric'


def input_spec():
    d=baseline('input');apply_passives(d);cs={c['ref']:c for c in d['components']}
    update(cs['F101'],'3403.0285.23','12.5A T / 125VDC','V1A_Qualified:Schurter_UMT_H_15.4x5.35')
    update(cs['D101'],'SMCJ36CA','SMCJ36CA 36V bidirectional','Diode_SMD:D_SMC')
    update(cs['D102'],'STPS60H100CT','STPS60H100CT','Package_TO_SOT_THT:TO-220-3_Vertical')
    cs['D102']['pins']={'1':pin('A1','GND'),'2':pin('K_TAB','VIN_PROTECTED'),'3':pin('A2','GND')}
    for ref in ('C101','C102'):update(cs[ref],'GRM32ER72A105KA01L','1uF 100V',passive_fp('GRM32ER72A105KA01L','C'))
    for ref,mpn in {'R101':'TNPW0603332KBEEA','R102':'TNPW060354K9BEEA','R103':'TNPW0805348KBEEA','R104':'TNPW060315K8BEEA','R105':'TNPW06034K02BEEA'}.items():update(cs[ref],mpn,footprint=passive_fp(mpn,'R'))
    for n in ('17','18'):cs['U101']['pins'][n]['net']='EFUSE_OUT'
    d['components'] += [force_link('JP101','EFUSE_OUT','VIN_PROTECTED'), tp('TP103','EFUSE_OUT'),
      part('#FLG103','N/A ERC declaration','PWR_FLAG','',{'1':pin('PWR','VIN_PROTECTED','power_out')},'FLAG','U101 OUT -> fitted removable JP101 -> VIN_PROTECTED; physical source only')]
    d['groups']=[('INPUT / REVERSE POLARITY', ['Q101','Q102','F101','D101','C101','C102']),('EFUSE / SOURCE DISCONNECT',['U101','D102','R101','R102','R103','R104','R105','R106','R107','R108','C103','TP101','TP102','#FLG101','#FLG102']),('MAIN CURRENT / COUPON ISOLATION',['JP101','TP103','#FLG103'])]
    d['schematic_notes']=['REQUIREMENT: 9–26 V input. DATASHEET: fuse 12.5 A time lag / 125 VDC; SMCJ36CA bidirectional TVS.',
      'CALCULATED: 28.33 W / 9 V = 3.15 A; at 12 V about 2.36 A. Keep input ratings and current limit unchanged.',
      'U101 MODE pin 11 intentionally NC: latch-off. INPUT_SHDN driven from Sheet03 manual test control; no autonomous source-fault claim.',
      'D102 pins 1/3 = GND anodes; pin 2 and tab = VIN_PROTECTED cathode. Tab isolation / hot commutation OPEN.',
      'JP101 is IMAIN_FORCE before all main local input capacitors. Remove for auxiliary-only coupon tests; include link parasitics.',
      'Power declarations follow fitted F101 and Q101 paths from J501; no control or fault input is forced valid.',
      'OPEN: source surge envelope, fuse clearing/hold, TVS hot clamp, 12 V thermal behavior. No Pi before fault tests pass.']
    return d



def tp(ref,net,return_net='GND'):
    return part(ref,'N/A etched paired pads',net,'V1A_Qualified:SensePair_P2.54',{'1':pin('SIGNAL',net),'2':pin('RETURN',return_net)},'SENSEPAIR')


def force_link(ref,a,b):
    return part(ref,'CUSTOM-FX-CU-01 RevA','REMOVABLE FORCE LINK','V1A_Qualified:ForceLink_M4_P20',{'1':pin('FORCE_A',a),'2':pin('FORCE_B',b)},'FORCELINK',
      'Gate4A FIX3_FIXTURE: C110 strap 2x15mm; 20mm pitch M4; absent for isolated tests; application rating OPEN')


def force_pad(ref,net):
    return part(ref,'CUSTOM-FX-PAD-M4 RevA',net,'V1A_Qualified:ForcePad_M4',{'1':pin('FORCE',net)},'TP','FIX3 fixture PF1..5; 4.5mm M4 hole; R3 geometry/current/parasitics OPEN')


def buck_spec():
    d=baseline('buck');apply_passives(d);cs={c['ref']:c for c in d['components']}
    update(cs['L201'],'74437636351002','10uH DATASHEET','V1A_Qualified:Wurth_74437636351002')
    cs['L201']['pins']['1']['net']='L201_IN'
    cs['L201']['pins']['2']['net']='L201_OUT'
    for ref in ('C201','C202'):update(cs[ref],'GRM32ER71H106KA12L','10uF 50V',passive_fp('GRM32ER71H106KA12L','C'))
    for ref in ('C203','C204'):update(cs[ref],'GRM188R71H104KA93D','100nF 50V',passive_fp('GRM188R71H104KA93D','C'))
    for ref,mpn in [('R202','TNPW0603100KBEEA'),('R203','TNPW060324K4BEEA')]:update(cs[ref],mpn)
    d['components'] += [force_link('JP201','BUCK_SW','L201_IN'),force_link('JP202','L201_OUT','VOUT_5V1'),
      force_pad('PF2','VIN_PROTECTED'),force_pad('PF3','BUCK_SW'),force_pad('PF4','L201_IN'),tp('TP204','L201_OUT'),tp('TP201','BUCK_SW'),tp('TP202','L201_IN'),tp('TP203','VOUT_5V1')]
    d['groups']=[('BUCK / NATIVE SWITCH NODE', ['U201','C201','C202','C203','C204','C205','C206','R201','R204','R206','R207']),
      ('FAULT INJECTION / LOCAL REGULATION',['JP201','JP202','L201','PF2','PF3','PF4','TP201','TP202','TP203','TP204','R202','R203','R205','C207','C209','C210','C211','C212','C213','C214'])]
    d['schematic_notes']=['DATASHEET: L201 = Wurth 74437636351002, 10uH; 2 plated slots per drawing001.000 (2025-02-07).',
      'CALCULATED: 100k / 24.4k local feedback = 5.098361 V nominal. No remote sense or setpoint increase.',
      'JP201 separates native BUCK_SW from L201_IN. Remove while unpowered for independent fixture isolation / injection.',
      'JP202 = IL201_FORCE after the winding, before all raw capacitance. PF2 VIN_PROTECTED / PF3 BUCK_SW / PF4 L201_IN = M4 force pads.',
      'C205 bootstrap return stays on native BUCK_SW. TP201 / TP202 paired return pads are sense only.',
      'ASSUMED qualification box: total local input C 10–30uF; Ldiff 5–12uH through 100A. These are not manufacturer guarantees.',
      'OPEN: nonlinear magnetic behavior, biased capacitance, startup/inrush, loop stability, ripple and thermal limits.',
      'TEST HOOK — design proven on bench; evidence NOT RUN. Dummy load only; isolated coupons before integrated faults.']
    return d


def output_spec():
    d=baseline('output');apply_passives(d);old={c['ref']:c for c in d['components']};cs={}
    def keep(ref):
        cs[ref]=copy.deepcopy(old[ref]);return cs[ref]
    def add(c):cs[c['ref']]=c;return c
    def net(ref,num,n):cs[ref]['pins'][str(num)]['net']=n
    def resistor(ref,mpn,value,a,b):
        return add(part(ref,mpn,value,passive_fp(mpn,'R'),{'1':pin('1',a),'2':pin('2',b)},'R'))
    def cap(ref,mpn,value,a,b='GND',fp=None,polar=False):
        c=add(part(ref,mpn,value,fp or passive_fp(mpn,'C'),{'1':pin('+' if polar else '1',a),'2':pin('-' if polar else '2',b)},'C'));c['polarized']=polar;return c
    def ic(ref,mpn,fp,names,nets,types):
        return add(part(ref,mpn,mpn,fp,{str(i+1):pin(n,nets[i],types[i]) for i,n in enumerate(names)}))
    def bypass(ref,rail='SAFE5'):return cap(ref,'GRM188R71H104KA93D','100nF 50V',rail)
    def bas(ref,a,k):
        c=copy.deepcopy(old['D301']);c['ref']=ref;c['pins']['1']['net']=a;c['pins']['3']['net']=k;return add(c)
    def diode(ref,a,k):
        return add(part(ref,'B260-13-F','B260-13-F','Diode_SMD:D_SMB',{'1':pin('K',k),'2':pin('A',a)},'D'))
    def powerflag(ref,n,path):
        return add(part(ref,'N/A ERC declaration','PWR_FLAG','',{'1':pin('PWR',n,'power_out')},'FLAG',path))
    def logic(ref,fam,a,b,y):
        if fam in ('14','17'):
            return ic(ref,f'SN74LVC1G{fam}DBVR','Package_TO_SOT_SMD:SOT-23-5',['NC','A','GND','Y','VCC'],[None,a,'GND',y,'SAFE5'],['no_connect','input','power_in','output','power_in'])
        return ic(ref,f'SN74LVC1G{fam}DBVR','Package_TO_SOT_SMD:SOT-23-5',['A','B','GND','Y','VCC'],[a,b,'GND',y,'SAFE5'],['input','input','power_in','output','power_in'])
    def flip(ref,clk,data,nq,q,clear):
        return ic(ref,'SN74LVC1G74DCTR','V1A_Qualified:TI_DCT0008A_SN74LVC1G74',['CLK','D','nQ','GND','Q','nCLR','nPRE','VCC'],[clk,data,nq,'GND',q,clear,'SAFE5','SAFE5'],['input','input','output','power_in','output','input','input','power_in'])
    def switch(ref,nets):
        names=['IN1','D1','S1','VSS','GND','S4','D4','IN4','IN3','D3','S3','NC','VDD','S2','D2','IN2']
        types=['input','passive','passive','power_in','power_in','passive','passive','input','input','passive','passive','no_connect','power_in','passive','passive','input']
        return ic(ref,'ADG4612BRUZ','Package_SO:TSSOP-16_4.4x5mm_P0.65mm',names,nets,types)
    def connector(ref,value,a,b):
        return add(part(ref,'B2B-XH-A(LF)(SN)',value,'V1A_Qualified:JST_B2B_XH_A_P2.50_THT',{'1':pin('CONTACT',a),'2':pin('RETURN',b)},'HEADER2'))

    for r in ['U301','U302','U303','U306','U315','Q301','Q302','Q303','Q304','D301','D302','D303']+[f'R{i}' for i in range(301,314)]+['R316','R317','R321','R322','R323']+[f'C{i}' for i in range(301,310)]+[f'C{i}' for i in range(330,338)]+[f'TP{i}' for i in range(301,306)]:keep(r)
    for c in cs.values():
        for p in c['pins'].values():
            if p['net']=='DET_5V':p['net']='DET5'
            if p['net']=='DRV_7V5':p['net']='DRV_HOLD'
    # Opposed pair and its isolated supply; no copper path around either channel.
    net('U301',1,'SER_DRV');net('U301',2,'SER_UVLO');net('D302',1,'SER_DRV')
    net('Q302',5,'SERIES_OUT');net('Q302',6,'SERIES_OUT');net('Q302',7,'SERIES_OUT');net('Q302',8,'SERIES_OUT')
    add(force_link('JP301','SERIES_OUT','VOUT_PROTECTED'))
    resistor('R711','TNPW0603143KBEEA','143k','SER_UVLO','GND')
    diode('D660','DRV_HOLD','SER_FEED');connector('JP660','SER_DRV SUPPLY LINK','SER_FEED','SER_DRV')
    cap('C660','GRM32ER71H106KA12L','10uF 50V','SER_DRV');resistor('R723','TNPW060310K0BEEA','10k','SER_DRV','GND')
    net('C306',1,'SER_DRV');net('C309',1,'SER_DRV')
    update(cs['R305'],'TNPW12062M00BEEA','2.00M',passive_fp('TNPW12062M00BEEA','R'))
    update(cs['R306'],'CRCW06031R00FKEA','1.00');update(cs['R307'],'TNPW060310K0BEEA','10k')
    net('U315',6,'DISPOSAL');net('R321',1,'DISPOSAL');net('R322',1,'RUN_GATE')
    update(cs['R321'],'TNPW0603100KBEEA','100k');update(cs['R322'],'TNPW0603100KBEEA','100k')
    powerflag('#FLG302','VOUT_PROTECTED','Physical path U201-L201-Q301/Q302-JP301; test configuration link fitted only after review')
    powerflag('#FLG304','SER_DRV','U327 OUT -> D660 -> JP660; physical driver supply link, never a logic permission')

    # Protected crowbar retained; independent raw bank dump, two strings of six.
    c=copy.deepcopy(cs['Q303']);c['ref']='Q330'
    for n,p in c['pins'].items():p['net']='GND' if n in ('1','2','3') else 'RAW_DUMP_GATE' if n=='4' else 'RAW_DUMP_DRAIN'
    add(c)
    c=copy.deepcopy(cs['U315']);c['ref']='U330';c['pins']['2']['net']='RAW_DUMP_UP';c['pins']['3']['net']='RAW_DUMP_GATE';add(c)
    resistor('R384','CRCW06031R00FKEA','1.00','RAW_DUMP_UP','RAW_DUMP_GATE');resistor('R385','TNPW060310K0BEEA','10k','RAW_DUMP_GATE','GND')
    for refs,tag in [([380,381,382,383,386,387],'A'),([388,389,390,391,392,393],'B')]:
        nodes=['VOUT_5V1']+[f'RAW_{tag}{i}' for i in range(1,6)]+['RAW_DUMP_DRAIN']
        for i,n in enumerate(refs):
            c=resistor('R'+str(n),'WFMB2512R0330FEA','33mOhm',nodes[i],nodes[i+1]);c['footprint']='V1A_Qualified:Vishay_WFM2512'
    cap('C367','GRM21BR71E105KA99L','1uF 25V','DRV_HOLD');bypass('C368','DRV_HOLD')
    for r,n in [('D330','VOUT_5V1'),('D331','VOUT_PROTECTED')]:
        add(part(r,'STPS60H100CT','STPS60H100CT','Package_TO_SOT_THT:TO-220-3_Vertical',{'1':pin('A1','GND'),'2':pin('K_TAB',n),'3':pin('A2','GND')},'D'))
    for n in range(340,344):cap('C'+str(n),'PCH1V471MCL1GS','470uF 35V','VOUT_PROTECTED',fp='V1A_Qualified:Nichicon_PCH_10x16',polar=True)

    # Removable dump-force links: independent branch current measurement, no bypass.
    for r in ('R309','R311'):net(r,2,'CB_BALLAST_OUT')
    for r in ('R387','R393'):net(r,2,'RAW_BALLAST_OUT')
    add(force_link('JP330','CB_BALLAST_OUT','CB_DRAIN'));add(force_link('JP331','RAW_BALLAST_OUT','RAW_DUMP_DRAIN'))

    # Aux surge stopper remains upstream of main eFuse.
    net('D303',2,'AUX_RAW');net('C307',1,'AUX_LIMITED');net('R323',1,'AUX_LIMITED')
    update(cs['C307'],'GRM21BR71H105KA12L','1uF 50V');update(cs['R323'],'CRCW120610K0FKEA','10k 0.25W')
    ic('U316','LT4363HMS-1#PBF','Package_SO:MSOP-12_3x4.039mm_P0.65mm',
       ['FB','OUT','SNS','GATE','VCC','SHDN','GND','UV','GND','FLT','ENOUT','TMR'],
       ['AUX_FB','AUX_LIMITED','AUX_SNS','AUX_GATE_DRIVE','AUX_RAW','AUX_RAW','GND','AUX_RAW','GND',None,'AUX_RUN','AUX_TMR'],
       ['input','input','input','output','power_in','input','power_in','input','power_in','open_collector','open_collector','passive'])
    ic('Q316','FDB33N25TM','Package_TO_SOT_SMD:TO-263-3_TabPin2',['G','D_TAB','S'],['AUX_GATE','AUX_RAW','AUX_SNS'],['input','passive','passive'])
    resistor('R330','TNPW0603100KBEEA','100k','AUX_LIMITED','AUX_FB');resistor('R331','TNPW06034K32BEEA','4.32k','AUX_FB','GND')
    resistor('R332','WSL2512R3300FEA','0.33','AUX_SNS','AUX_LIMITED');resistor('R333','CRCW060310R0FKEA','10','AUX_GATE_DRIVE','AUX_GATE')
    cap('C350','C1608C0G1H103J080AA','10nF 50V C0G','AUX_TMR');cap('C378','GRM32ER72A105KA01L','1uF 100V','AUX_RAW')
    powerflag('#FLG301','AUX_RAW','VIN_FUSED -> fitted D303; independent upstream source')
    powerflag('#FLG303','AUX_LIMITED','AUX_RAW -> Q316 -> R332; physical LT4363 controlled pass path')

    # 12V buck-boost: both compensation branches return to FB, not ground.
    ic('U317','LTC3115IFE-1#PBF','V1A_Qualified:ADI_FE20_EP2.74x4.95',
       ['PGND','RUN','SW2','PVOUT','GND','GND','VC','FB','RT','PGND','PGND','VCC','VIN','PVCC','BST2','BST1','PVIN','SW1','PWM_SYNC','PGND','EP_PGND'],
       ['GND','AUX_RUN','AUX_SW2','AUX_12V','GND','GND','AUX_VC','AUX_BB_FB','AUX_RT','GND','GND','AUX_VCC','AUX_LIMITED','AUX_VCC','AUX_BST2','AUX_BST1','AUX_LIMITED','AUX_SW1','GND','GND','GND'],
       ['power_in','input','output','power_out','power_in','power_in','passive','input','passive','power_in','power_in','power_out','power_in','power_in','passive','passive','power_in','output','input','power_in','power_in'])
    add(part('L301','7447789004','4.7uH DATASHEET','V1A_Qualified:Wurth_7447789004',{'1':pin('1','AUX_SW1'),'2':pin('2','AUX_SW2')},'L'))
    for r,m,v,a,b in [
      ('R340','TNPW08051M00BEEA','1.00M','AUX_12V','AUX_BB_FB'),('R341','TNPW060388K7BEEA','88.7k','AUX_BB_FB','GND'),
      ('R342','TNPW060323K7BEEA','23.7k','AUX_RT','GND'),('R343','TNPW060315K0BEEA','15k','AUX_VC','AUX_COMP'),
      ('R344','TNPW060315K0BEEA','15k','AUX_12V','AUX_FF'),('R345','TNPW0805383KBEEA','383k','AUX_LIMITED','AUX_RUN'),('R346','TNPW0603100KBEEA','100k','AUX_RUN','GND')]:resistor(r,m,v,a,b)
    for r,m,v,a,b in [
      ('C351','C3216X7R1H475K160AB','4.7uF 50V','AUX_LIMITED','GND'),('C352','GRM32ER71H106KA12L','10uF 50V','AUX_12V','GND'),
      ('C377','GRM32ER71H106KA12L','10uF 50V','AUX_12V','GND'),('C353','GRM21BR71E475KA73L','4.7uF 25V','AUX_VCC','GND'),
      ('C379','GRM21BR71E475KA73L','4.7uF 25V','AUX_VCC','GND'),('C354','GRM188R71H104KA93D','100nF 50V','AUX_BST1','AUX_SW1'),
      ('C355','GRM188R71H104KA93D','100nF 50V','AUX_BST2','AUX_SW2'),('C356','C1608C0G1H102J080AA','1nF 50V C0G','AUX_COMP','AUX_BB_FB'),
      ('C357','GRM1885C1H330JA01D','33pF 50V C0G','AUX_FF','AUX_BB_FB'),('C380','GRM188R71H104KA93D','100nF 50V','AUX_LIMITED','GND')]:cap(r,m,v,a,b)

    # Reverse blocking plus controlled charging of the held bank.
    diode('D304','AUX_12V','AUX_PREHOLD')
    ic('U327','TPS259470LRPWR','V1A_Qualified:TI_RPW0010A_TPS25947',
       ['EN_UVLO','OVLO','AUXOFF','FLT','IN','OUT','DVDT','GND','ILM','ITIMER'],
       ['HOLD_EN','HOLD_OVLO','HOLD_AUXOFF','HOLD_FLT','AUX_PREHOLD','DRV_HOLD','HOLD_DVDT','GND','HOLD_ILM',None],
       ['input','input','open_collector','open_collector','power_in','power_out','passive','power_in','passive','passive'])
    for r,m,v,a,b in [('R374','CRCW0603100RFKEA','100','HOLD_DVDT','HOLD_SLEW_C'),('R375','TNPW06036K49BEEA','6.49k','HOLD_ILM','GND'),
      ('R376','TNPW0805365KBEEA','365k','AUX_PREHOLD','HOLD_EN'),('R377','TNPW060348K7BEEA','48.7k','HOLD_EN','GND'),
      ('R378','TNPW0805365KBEEA','365k','AUX_PREHOLD','HOLD_OVLO'),('R379','TNPW060333K2BEEA','33.2k','HOLD_OVLO','GND')]:resistor(r,m,v,a,b)
    cap('C374','GRM21BR71E105KA99L','1uF 25V','HOLD_SLEW_C');cap('C375','GRM21BR71E105KA99L','1uF 25V','AUX_PREHOLD');bypass('C376','DRV_HOLD')
    for r in ('C358','C359'):cap(r,'EEUFR1E221','220uF 25V','DRV_HOLD',fp='Capacitor_THT:CP_Radial_D6.3mm_P2.50mm',polar=True)
    powerflag('#FLG305','AUX_PREHOLD','U317 PVOUT -> fitted D304; reverse blocking retained')
    add(tp('TP327','HOLD_AUXOFF'));add(tp('TP328','HOLD_FLT'))

    # Detector supply and monitored rails.
    net('U306',1,'DET5');net('U306',3,'DET_PG');net('U306',5,'DRV_HOLD');net('U306',8,'DRV_HOLD');net('U306',7,None)
    net('R316',1,'3V3_AUX');net('R316',2,'DET_PG');net('R317',1,'3V3_AUX')
    update(cs['R316'],'TNPW060310K0BEEA','10k');update(cs['R317'],'TNPW060310K0BEEA','10k')
    update(cs['R312'],'TNPW060332K4BEEA','32.4k');update(cs['R313'],'TNPW060310K0BEEA','10k')
    ic('U318','TPS70933DBVR','Package_TO_SOT_SMD:SOT-23-5',['IN','GND','EN','NC','OUT'],['DRV_HOLD','GND',None,None,'3V3_AUX'],['power_in','power_in','input','no_connect','power_out'])
    cap('C365','GRM21BR71E105KA99L','1uF 25V','DRV_HOLD');cap('C366','GRM21BR71E475KA73L','4.7uF 25V','3V3_AUX')
    for u,rail,top,bot,pu,bp,mpn,val,n in [
       ('U322','DRV_HOLD','R362','R363','R371','C369','TNPW0603249KBEEA','249k','DRV_OBS'),
       ('U323','DET5','R364','R365','R372','C370','TNPW0603100KBEEA','100k','DET_OBS')]:
        ic(u,'TPS3808G01DBVR','Package_TO_SOT_SMD:SOT-23-6',['nRESET','GND','nMR','CT','SENSE','VDD'],[n+'_N','GND','3V3_AUX',None,n+'_DIV','3V3_AUX'],['open_collector','power_in','input','passive','input','power_in'])
        resistor(top,mpn,val,rail,n+'_DIV');resistor(bot,'TNPW060310K0BEEA','10k',n+'_DIV','GND');resistor(pu,'TNPW060310K0BEEA','10k','DET5',n+'_N');bypass(bp,'3V3_AUX')
    add(tp('TP322','DRV_OBS_N'));add(tp('TP323','DET_OBS_N'));add(tp('TP324','DET_PG'))

    # OV detector and independent shunt clamp (never into REF5025 output).
    update(cs['R301'],'TNPW06039K88BEEA','9.88k');update(cs['R302'],'TNPW060310K0BEEA','10k');update(cs['R303'],'TNPW06031K00BEEA','1k')
    net('D301',3,'CLAMP_2V5');net('R303',1,'OV_SWITCHED');net('U303',3,'REF_SENSE');net('U303',1,'OV_COMPARATOR')
    resistor('R373','TNPW06031K00BEEA','1k','REF_2V5','REF_SENSE');resistor('R367','TNPW0603100KBEEA','100k','OV_SENSE','GND')
    resistor('R361','TNPW060368K1BEEA','68.1k','DRV_HOLD','CLAMP_2V5');resistor('R370','TNPW060310K0BEEA','10k','DET5','GND')
    ic('D321','LM4040A25IDBZR','Package_TO_SOT_SMD:SOT-23',['K','A','NC_GND'],['CLAMP_2V5','GND','GND'],['passive']*3)
    bas('D322','GND','OV_DIV');bypass('C364','DET5')
    switch('U321',['DET_SWITCH_EN','OV_DIV','OV_SWITCHED','GND','GND','GND','GND','GND','GND','GND','GND',None,'DET5','GND','GND','GND'])
    resistor('R717','TNPW06031K00BEEA','1k','MANUAL_RAILS_VALID','DET_SWITCH_EN');resistor('R718','TNPW0603100KBEEA','100k','DET_SWITCH_EN','GND')
    update(cs['C301'],'GRM21BR71E105KA99L','1uF 25V',passive_fp('GRM21BR71E105KA99L','C'));update(cs['C302'],'GRM21BR71E475KA73L','4.7uF 25V',passive_fp('GRM21BR71E475KA73L','C'))

    # SAFE5 memory supply and real PG receiver. Brownout ownership is a MANUAL test hook.
    diode('D600','DRV_HOLD','SAFE_FEED');resistor('R602','TNPW060347R0BEEA','47','SAFE_FEED','SAFE_IN')
    cap('C600','GRM21BR71E105KA99L','1uF 25V','SAFE_FEED');cap('C602','GRM32ER71H106KA12L','10uF 50V','SAFE_IN')
    c=copy.deepcopy(cs['U306']);c['ref']='U600';c['pins']['1']['net']='SAFE5';c['pins']['2']['net']='SAFE_FB';c['pins']['3']['net']=None;c['pins']['5']['net']='SAFE_IN';c['pins']['8']['net']='SAFE_IN';add(c)
    resistor('R600','TNPW060332K4BEEA','32.4k','SAFE5','SAFE_FB');resistor('R601','TNPW060310K0BEEA','10k','SAFE_FB','GND')
    cap('C601','GRM32ER71H106KA12L','10uF 50V','SAFE5');resistor('R603','TNPW060310K0BEEA','10k','SAFE5','GND')
    powerflag('#FLG306','SAFE_IN','DRV_HOLD -> D600 -> R602 -> SAFE_IN, physically held independent memory supply')
    ic('U602','TPS3808G50DBVR','Package_TO_SOT_SMD:SOT-23-6',['nRESET','GND','nMR','CT','SENSE','VDD'],['CORE_POR_RAW_N','GND','SAFE5',None,'SAFE5','SAFE5'],['open_collector','power_in','input','passive','input','power_in'])
    resistor('R609','TNPW0603100KBEEA','100k','SAFE5','CORE_POR_RAW_N');bypass('C604');logic('U662','17','CORE_POR_RAW_N',None,'CORE_POR_N');bypass('C762')
    ic('D601','LM4040A25IDBZR','Package_TO_SOT_SMD:SOT-23',['K','A','NC_GND'],['REF_SAFE_2V5','GND','GND'],['passive']*3)
    resistor('R604','TNPW060310K0BEEA','10k','SAFE5','REF_SAFE_2V5');resistor('R605','TNPW0603100KBEEA','100k','REF_SAFE_2V5','REF1V25');resistor('R606','TNPW0603100KBEEA','100k','REF1V25','GND')
    cap('C603','C1608C0G1H103J080AA','10nF 50V C0G','REF_SAFE_2V5')
    c=copy.deepcopy(cs['U303']);c['ref']='U607';c['pins']['1']['net']='PG_GOOD';c['pins']['3']['net']='PG_SENSE';c['pins']['4']['net']='REF1V25';c['pins']['5']['net']='SAFE5';add(c);bypass('C609')
    resistor('R622','TNPW06031K00BEEA','1k','BUCK_PGOOD','PG_DIV');resistor('R623','TNPW0603100KBEEA','100k','PG_SENSE','GND')
    switch('U651',['SAFE5','PG_DIV','PG_SENSE','GND','GND','GND','GND','GND','GND','GND','GND',None,'SAFE5','GND','GND','GND']);bypass('C651')
    bas('D618','PG_DIV','REF_SAFE_2V5');bas('D619','GND','PG_DIV')

    # Option A: manual source trigger, manual reset and manual rail qualification.
    # A fault always asynchronously clears NOFAULT; reset is a clocked transfer.
    for ref,val,a in [('J301','MAIN ARM / dry contact','ARM_CONTACT'),('J302','MANUAL RESET / dry contact','RESET_CONTACT'),
                      ('J603','SOURCE FAULT / dry contact','SOURCE_CONTACT'),('J604','SERIES ARM / dry contact','SERIES_CONTACT')]:connector(ref,val,a,'GND')
    connector('JP600','MANUAL RAIL VALID LINK','SAFE5','MANUAL_RAILS_VALID')
    for r,m,v,a,b in [('R707','TNPW060310K0BEEA','10k','SAFE5','ARM_CONTACT'),('R708','TNPW060310K0BEEA','10k','SAFE5','RESET_CONTACT'),
      ('R727','TNPW060310K0BEEA','10k','SAFE5','SOURCE_CONTACT'),('R728','TNPW060310K0BEEA','10k','SAFE5','SERIES_CONTACT'),
      ('R729','TNPW060310K0BEEA','10k','MANUAL_RAILS_VALID','GND')]:resistor(r,m,v,a,b)
    for ref,a,y,bp in [('U654','ARM_CONTACT','ARM_DOWN','C754'),('U656','RESET_CONTACT','RESET_DOWN','C756'),
                       ('U644','SOURCE_CONTACT','SRC_TRIP','C644'),('U661','SERIES_CONTACT','SERIES_DOWN','C761')]:logic(ref,'14',a,None,y);bypass(bp)
    flip('U610','RESET_DOWN','SAFE5','FAULT','NOFAULT','FAULT_CLEAR_N');bypass('C710')
    for ref,fam,a,b,y,bp in [
      ('U614','14','OV_COMPARATOR',None,'OV_RAW','C714'),('U628','08','OV_RAW','MANUAL_RAILS_VALID','OV_VALID','C728'),
      ('U615','32','SRC_TRIP','OV_VALID','TRUE_FAULT','C715'),('U616','14','TRUE_FAULT',None,'NO_TRUE_FAULT','C716'),
      ('U617','08','CORE_POR_N','NO_TRUE_FAULT','FAULT_CLEAR_N','C717'),
      ('U623','08','NOFAULT','MANUAL_RAILS_VALID','MANUAL_VALID_NOFAULT','C723'),
      ('U630','08','ARMED','MANUAL_VALID_NOFAULT','MAIN_PERMISSION','C730'),
      ('U631','08','MAIN_PERMISSION','PG_GOOD','SERIES_CLEAR_N','C731'),
      ('U632','08','SERIES_ARMED','SERIES_CLEAR_N','RUN_GATE_LOGIC','C732'),
      ('U633','08','FAULT','CORE_POR_N','DISPOSAL_LOGIC','C733')]:logic(ref,fam,a,b,y);bypass(bp)
    flip('U612','ARM_DOWN','SAFE5',None,'ARMED','MANUAL_VALID_NOFAULT');bypass('C712')
    flip('U611','SERIES_DOWN','SAFE5',None,'SERIES_ARMED','SERIES_CLEAR_N');bypass('C711')
    for r,m,v,a,b in [('R709','TNPW06031K00BEEA','1k','RUN_GATE_LOGIC','RUN_GATE'),('R710','TNPW060310K0BEEA','10k','RUN_GATE','GND'),
      ('R712','TNPW06031K00BEEA','1k','DISPOSAL_LOGIC','DISPOSAL'),('R713','TNPW060310K0BEEA','10k','DISPOSAL','GND'),
      ('R647','TNPW06031K00BEEA','1k','MAIN_PERMISSION','INPUT_SHDN'),('R648','TNPW060310K0BEEA','10k','INPUT_SHDN','GND'),
      ('R649','TNPW06031K00BEEA','1k','FAULT','FAULT_DRIVE'),('R650','TNPW0603100KBEEA','100k','FAULT_DRIVE','GND')]:resistor(r,m,v,a,b)
    net('Q304',1,'FAULT_DRIVE')
    for ref,n,ret in [('TP306','OV_DIV','GND'),('TP307','OV_COMPARATOR','GND'),('TP308','FAULT','GND'),('TP309','CB_GATE','GND'),
      ('TP310','DRV_HOLD','GND'),('TP311','DET5','GND'),('TP312','INPUT_SHDN','GND'),('TP313','SER_DRV','GND'),('TP314','PROT_GATE','PROT_MID'),
      ('TP315','RAW_DUMP_GATE','GND'),('TP316','SAFE5','GND'),('TP317','BUCK_PGOOD','GND'),('TP318','MANUAL_RAILS_VALID','GND'),
      ('TP319','RUN_GATE','GND'),('TP320','SRC_TRIP','GND'),('TP321','CORE_POR_N','GND')]:add(tp(ref,n,ret))

    for ref,n,ret in [('TP329','AUX_RAW','GND'),('TP330','AUX_LIMITED','GND'),('TP331','AUX_12V','GND'),
                       ('TP332','AUX_PREHOLD','GND'),('TP333','3V3_AUX','GND'),('TP334','PROT_BST','PROT_MID'),
                       ('TP335','CB_BALLAST_OUT','CB_DRAIN'),('TP336','RAW_BALLAST_OUT','RAW_DUMP_DRAIN')]:add(tp(ref,n,ret))
    resistor('R730','TNPW06031K00BEEA','1k','PG_GOOD','PG_FIXTURE')
    resistor('R731','TNPW06031K00BEEA','1k','MAIN_PERMISSION','MAIN_FIXTURE')
    connector('J605','REAL PG / guarded output','PG_FIXTURE','GND')
    connector('J606','MAIN PERMISSION / guarded output','MAIN_FIXTURE','GND')

    # All omitted historical controls are explicitly retired in the delta report.
    d['retired_refs']=sorted(set(old)-set(cs));d['components']=list(cs.values())
    groups=[];done=set()
    def group(title,refs):
        refs=[r for r in refs if r in cs and r not in done];groups.append((title,refs));done.update(refs)
    group('1 AUX SURGE STOPPER / UPSTREAM OF MAIN EFUSE',['D303','U316','Q316','R330','R331','R332','R333','C350','C378','C307','R323','#FLG301','#FLG303'])
    group('2 AUX 12 V BUCK-BOOST / COMPENSATION TO FB',['U317','L301']+[f'R{i}' for i in range(340,347)]+[f'C{i}' for i in range(351,358)]+['C377','C379','C380'])
    group('3 HELD DRIVER SUPPLY / CONTROLLED IN-RUSH',['D304','U327']+[f'R{i}' for i in range(374,380)]+[f'C{i}' for i in range(374,377)]+['C358','C359','TP327','TP328','#FLG305'])
    group('4 OPPOSED SERIES PAIR / REMOVABLE FORCE LINK',['Q301','Q302','U301','D302','D660','JP301','JP660','R304','R305','R711','R723','C301','C306','C309','C660','#FLG302','#FLG304'])
    group('5 PROTECTED CROWBAR / 33 mOhm BALLAST',['Q303','U315','D331','JP330','R306','R307','R308','R309','R310','R311','C308']+[f'C{i}' for i in range(340,344)])
    group('6 RAW DUMP / 99 mOhm / TWO SIX-PART STRINGS',['Q330','U330','D330','JP331']+[f'R{i}' for i in range(380,394)]+['C367','C368']+[f'C{i}' for i in range(330,338)])
    group('7 DETECTOR SUPPLY / PG OBSERVATION ONLY',['U306','U318','U322','U323','R312','R313','R316','R317','R362','R363','R364','R365','R371','R372','C305','C365','C366','C369','C370','TP322','TP323','TP324'])
    group('8 OV DETECTOR / ISOLATION / SEPARATE SHUNT CLAMP',['U302','U303','U321','D301','D321','D322','R301','R302','R303','R361','R367','R370','R373','R717','R718','C302','C303','C304','C364'])
    group('9 SAFE5 / MEMORY SUPPLY / REAL PG RECEIVER',['U600','U602','U662','U607','U651','D600','D601','D618','D619','R600','R601','R602','R603','R604','R605','R606','R609','R622','R623','C600','C601','C602','C603','C604','C609','C651','C762','#FLG306'])
    group('10 MANUAL SOURCE TRIGGER / RESET / FAULT LATCH',['U610','U614','U615','U616','U617','U628','U633','U644','U656','J302','J603','R708','R727','C710','C714','C715','C716','C717','C728','C733','C644','C756'])
    group('11 MANUAL RAIL VALID / ARM / COMMAND DEFAULTS',['U611','U612','U623','U630','U631','U632','U654','U661','Q304','J301','J604','JP600','R707','R728','R729','R709','R710','R712','R713','R321','R322','R647','R648','R649','R650','C711','C712','C723','C730','C731','C732','C754','C761','R730','R731','J605','J606'])
    group('12 PAIRED SENSE TEST POINTS / NO FORCE CURRENT',[r for r in cs if r.startswith('TP')])
    assert done==set(cs),set(cs)-done
    d['groups']=groups
    d['schematic_notes']=[
      'TEST HOOK — design proven on bench. This is the owner-required hook label; ALL hardware evidence is NOT RUN.',
      'Option A: J603 manual source trigger; J302 manual reset. Autonomous source coverage is NOT CAPTURED / OPEN (T01F3).',
      'JP600 manual rail-valid link replaces unproved brownout / PG-recovery interlock. Remove by default; verify rails before fitting.',
      'Sequence: force links absent; inspect / measure rails; fit JP600; reset J302; MAIN ARM J301; genuine PG; separate SERIES ARM J604.',
      'A fault asynchronously clears NOFAULT and commands both dumps. PG loss clears SERIES_ARMED; recovery alone has no clock edge.',
      'MANUAL RESET has no persistent-short diagnostic: disconnect source and verify repair before reset. Partial-rail / held-contact behavior OPEN.',
      'JP301 removes series force path. JP660 isolates SER_DRV for supply-loss tests. U322/U323 are observation only, never timing authorities.',
      'JP330 / JP331 measure individual dump current; open links DISABLE disposal. Fit only after fixture review. J605/606 are guarded observations.',
      'DATASHEET nominal: protected bank4x470uF =1.88mF. CALCULATED: raw ballast99mOhm / protected33mOhm. Hot pulse/SOA OPEN.',
      'ASSUMED qualification box: Ccharged<=600uF, total held load<=45mA, effective hold C>=300uF. No timing/hold validation claimed.',
      'OPEN: T04 bootstrap; T06 detector; T07 aux startup/loop/thermal; T09 energy/negative returns; T10 far-end peak; T11 harness; T12 fixture; T15 rail loss.',
      'No Pi before dummy-load and fault tests pass. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.']
    return d


def monitor_spec():
    d=baseline('monitor');apply_passives(d);cs={c['ref']:c for c in d['components']}
    for r in ('R402','R403'):update(cs[r],'TNPW060310R0BEEA','10')
    for r in ('R404','R405','R408'):update(cs[r],'TNPW060310K0BEEA','10k')
    for r in ('R406','R407'):update(cs[r],'TNPW06034K70BEEA','4.7k')
    update(cs['C401'],'GRM188R71H104KA93D','100nF 50V')
    cs['R401']['rating']='DATASHEET: 2mOhm +/-1%, 25ppm/K; PR15 Kelvin land retained. Pulse survival/thermal/accuracy OPEN.'
    cs['C404']['rating']='DATASHEET: 22uF 50V X7R +/-20%; qualified PR15 TDK land. Effective C / local regulator stability OPEN.'
    d['components'] += [tp('TP405','VOUT_PROTECTED'),tp('TP406','LOAD_5V1')]
    d['groups']=[('KELVIN SHUNT / LOAD-SIDE BUS SENSE',['R401','U401','R402','R403','C401','C402','R408','TP401','TP402','TP403','TP405','TP406']),
      ('LOCAL REGULATOR / HOST DOMAIN BOUNDARY',['U402','U403','C403','C404','C405','C406','R404','R405','R406','R407','TP404'])]
    d['schematic_notes']=[
      'DATASHEET: R401 = 2mOhm, +/-1%, 25ppm/K. INA228 address0x40; retain independent Kelvin pads2/3, force pads1/4.',
      'CALCULATED at5A: Vshunt10mV; dissipation50mW. Full scale81.92A at163.84mV range; alternate40.96mV gives20.48A nominal.',
      'CALCULATED: 10ohm + 10ohm / 100nF differential filter pole79.6kHz. Telemetry is not the fast fault-current probe.',
      'CALCULATED: 80A would produce160mV and12.8W while flowing. Use measured integral(I^2 R dt); pulse survival OPEN.',
      'TP402/403 are Kelvin-only; TP405/406 expose force rails with paired local GND. No sense trace may carry load current.',
      'Host/local3.3V domains remain separate. 3V3_LOCAL is never protection permission. Disconnect J503 during initial faults.',
      'OPEN: shunt self-heating/tolerance/TCR, fault common-mode/pin stress, V/I/P/E accuracy, host-only/local-only Ioff and bus timing.',
      'No Pi before prior dummy-load/fault/telemetry gates pass. PRELIMINARY TEST BOARD / NOT FOR FABRICATION.']
    return d


def io_spec():
    d=baseline('io');cs={c['ref']:c for c in d['components']}
    update(cs['J502'],'1776508','LOAD OUTPUT / mate1777989')
    cs['J502']['rating']='DATASHEET 12A nominal; CALCULATED acceptance <=3.12mOhm per complete hot pole is NOT a catalog guarantee.'
    cs['J502']['source']='J502 solution A, commit41cb9e889418d50d2f5f24467e66ac7f15a90476; PR15 qualified Phoenix land retained'
    d['components'] += [force_link('JP501','LOAD_5V1','LOAD_FIXTURE'),force_pad('PF1','VIN_RAW'),force_pad('PF5','GND'),tp('TP505','LOAD_FIXTURE')]
    d['groups']=[('DC INPUT / FIXTURE POWER RETURN',['J501','PF1','PF5','TP501','TP502','#FLG501','#FLG502']),
      ('PROTECTED LOAD / HOST TELEMETRY',['JP501','J502','J503','TP503','TP504','TP505','#FLG503'])]
    d['schematic_notes']=[
      'REQUIREMENT: 9–26V DC input. J502 Phoenix1776508 + cable plug1777989, solutionA. Contact1=LOAD_5V1; contact2=GND.',
      'JP501 feeds a local dummy fixture from LOAD_5V1; unplug J502 when using it. For isolation remove JP501 AND unplug J502; change only discharged.',
      'PF1=VIN_RAW before F101; PF5=powerGND. PF2/3/4 onSheet02 complete the external fixture interfaces. No return bypass at far end.',
      'HARNESS: TE3-87456-6 full40-position housing +10x87309-9. Belden8521 AWG16 trunks75mm;8502 AWG20 send2x15mm / return8x35mm.',
      'Pi physical +2/4; GND6/9/14/20/25/30/34/39. Power-only harness; all other cavities empty. No Pi before fault tests pass.',
      'DATASHEET J50212A nominal; <=3.12mOhm per complete hot pole is a TEST acceptance allocation. Hot mixed-mate/current/assembly OPEN.',
      'J503:1GND /2host3.3V reference /3SDA /4SCL. Remove during first faults; external power-only Pi housing does not yet carry telemetry.',
      'TEST HOOK — design proven on bench; evidence NOT RUN. Dry-contact manual trigger/reset and rail/driver-loss links are onSheet03.',
      'OPEN: force-link/contact/copper/parasitic budgets, indexed harness/tooling, hot sharing, single-contact loss and telemetry housing integration.']
    return d


def draw(d,block):
    name=NAMES[block];cs=normalize(d);byref={c['ref']:c for c in cs}
    sh=Sheet(name,name.replace('_',' '),d['ports']);sh.serial=40000
    sh.text(STATUS,12.7,10.16,1.778);sh.add_ports()
    # Functional groups, generous physical spacing; each wire terminates in a named net.
    wide=block=='output';paper='A0' if wide else 'A1' if block=='input' else 'A2'
    columns=3 if wide else 2;gw=269.24 if wide else 279.4
    cursors=[55.88]*columns
    placed=set()
    for title,refs in d['groups']:
        refs=[r for r in refs if r in byref]
        if not refs:continue
        col=min(range(columns),key=lambda c:cursors[c]);x=12.7+col*gw;y=cursors[col]
        sh.text(title,x,y,1.778);y+=10.16 if wide else 12.7
        large=[byref[r] for r in refs if len(byref[r]['pins'])>2]
        small=[byref[r] for r in refs if len(byref[r]['pins'])<=2]
        per=2;step=124.46 if wide else 132.08
        for start in range(0,len(large),per):
            row=large[start:start+per]
            heights=[max(7.62,(((len(c['pins'])+1)//2)+1)*2.54) for c in row]
            h=max(heights);cy=y+h+(5.08 if wide else 7.62)
            for i,c in enumerate(row):sh.component(c,x+60.96+i*step,cy);placed.add(c['ref'])
            y=cy+h+(7.62 if wide else 12.7)
        per=3 if wide else 2;step=86.36 if wide else 132.08;pitch=(17.78 if title.startswith('12 ') else 20.32) if wide else 25.4
        for i,c in enumerate(small):
            sh.component(c,x+45.72+(i%per)*step,y+(i//per)*pitch+10.16);placed.add(c['ref'])
        y+=math.ceil(len(small)/per)*pitch+(10.16 if wide else 12.7)
        cursors[col]=y
    assert placed==set(byref),(placed^set(byref))
    y=max(cursors)+2.54
    for note in d['schematic_notes']:
        sh.text(note,12.7,y,1.27);y+=5.08
    limit=1135 if wide else 545 if block=='input' else 385
    if y>limit:raise ValueError(f'{block}: layout height {y} exceeds {limit}')
    sh.save(HW);path=HW/(name+'.kicad_sch')
    s=path.read_text().replace('(paper "A3")',f'(paper "{paper}"'+(' portrait)' if wide else ')')).replace('2026-09-12','2026-10-01')
    s=s.replace('(comment 2 "R3 PCB LAYOUT BLOCKED")',f'(comment 2 {q(STATUS)})')
    path.write_text(dump(parse(s))+"\n")
    lib=HW/'V1A.kicad_sym';old=lib.read_text().rstrip()
    refs=set(byref)
    for a,b,t in reversed(list(children(old))):
        if t.startswith('(symbol '):
            ref=re.match(r'\(symbol\s+"([^_]+)_',t)
            if ref and ref[1] in refs:old=old[:a]+old[b:]
    lib.write_text(dump(parse(old[:-1]+'\n'+'\n'.join(library_symbol(c) for c in cs)+'\n)'))+'\n')
    # Native definitions/specs use a stable, explicitly reviewable source of truth.
    (EV/f'{block}_block.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    print(f'{name}: {len(cs)} symbols; {paper}; drawing bottom {y:g} mm')


def main():
    p=argparse.ArgumentParser();p.add_argument('block',choices=NAMES);a=p.parse_args()
    draw(globals()[a.block+'_spec'](),a.block)
if __name__=='__main__':main()
