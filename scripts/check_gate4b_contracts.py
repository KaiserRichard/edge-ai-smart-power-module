"""Independent Gate4B test-board boundaries, not an electrical safety verdict."""
import re


def validate(tree, specs):
    errors=[]
    ns={(n.get('ref'),n.get('pin')):net.get('name').rsplit('/',1)[-1]
        for net in tree.findall('./nets/net') for n in net.findall('node')}
    parts={c.get('ref'):c for c in tree.findall('./components/comp')}
    def pins(ref, names):
        for n,want in enumerate(names,1):
            got=ns.get((ref,str(n)),'')
            if want is None:
                if got and not got.startswith('unconnected-'):errors.append(f'{ref}.{n}: must remain NC')
            elif got!=want:errors.append(f'{ref}.{n}: independent contract requires {want}, got {got}')
    def pair(ref,a,b):pins(ref,[a,b])
    contracts={
      'U301':['SER_DRV','SER_UVLO','GND','RUN_GATE','GND','PROT_GATE','TGUP_SLOW','PROT_MID','PROT_BST',None,'GND'],
      'U303':['OV_COMPARATOR','GND','REF_SENSE','OV_SENSE','DET5'],
      'U306':['DET5','DET_FB','DET_PG','GND','DRV_HOLD',None,None,'DRV_HOLD','GND'],
      'U600':['SAFE5','SAFE_FB',None,'GND','SAFE_IN',None,None,'SAFE_IN','GND'],
      'U315':['DRV_HOLD','CB_GATE_UP','CB_GATE','GND','GND','DISPOSAL'],
      'U330':['DRV_HOLD','RAW_DUMP_UP','RAW_DUMP_GATE','GND','GND','DISPOSAL'],
      'U316':['AUX_FB','AUX_LIMITED','AUX_SNS','AUX_GATE_DRIVE','AUX_RAW','AUX_RAW','GND','AUX_RAW','GND',None,'AUX_RUN','AUX_TMR'],
      'Q316':['AUX_GATE','AUX_RAW','AUX_SNS'],
      'U317':['GND','AUX_RUN','AUX_SW2','AUX_12V','GND','GND','AUX_VC','AUX_BB_FB','AUX_RT','GND','GND','AUX_VCC','AUX_LIMITED','AUX_VCC','AUX_BST2','AUX_BST1','AUX_LIMITED','AUX_SW1','GND','GND','GND'],
      'U327':['HOLD_EN','HOLD_OVLO','HOLD_AUXOFF','HOLD_FLT','AUX_PREHOLD','DRV_HOLD','HOLD_DVDT','GND','HOLD_ILM',None],
      'U318':['DRV_HOLD','GND',None,None,'3V3_AUX'],
      'U321':['DET_SWITCH_EN','OV_DIV','OV_SWITCHED','GND','GND','GND','GND','GND','GND','GND','GND',None,'DET5','GND','GND','GND'],
      'U651':['SAFE5','PG_DIV','PG_SENSE','GND','GND','GND','GND','GND','GND','GND','GND',None,'SAFE5','GND','GND','GND'],
      'U607':['PG_GOOD','GND','PG_SENSE','REF1V25','SAFE5'],
      'U602':['CORE_POR_RAW_N','GND','SAFE5',None,'SAFE5','SAFE5'],
      'U662':[None,'CORE_POR_RAW_N','GND','CORE_POR_N','SAFE5'],
      'U322':['DRV_OBS_N','GND','3V3_AUX',None,'DRV_OBS_DIV','3V3_AUX'],
      'U323':['DET_OBS_N','GND','3V3_AUX',None,'DET_OBS_DIV','3V3_AUX'],
      'D321':['CLAMP_2V5','GND','GND'], 'D601':['REF_SAFE_2V5','GND','GND'],
      'D301':['OV_DIV',None,'CLAMP_2V5'], 'D302':['SER_DRV',None,'PROT_BST'],
      'Q304':['FAULT_DRIVE','GND','INPUT_SHDN'],
      'U610':['RESET_DOWN','SAFE5','FAULT','GND','NOFAULT','FAULT_CLEAR_N','SAFE5','SAFE5'],
      'U612':['ARM_DOWN','SAFE5',None,'GND','ARMED','MANUAL_VALID_NOFAULT','SAFE5','SAFE5'],
      'U611':['SERIES_DOWN','SAFE5',None,'GND','SERIES_ARMED','SERIES_CLEAR_N','SAFE5','SAFE5'],
      'U614':[None,'OV_COMPARATOR','GND','OV_RAW','SAFE5'],
      'U628':['OV_RAW','MANUAL_RAILS_VALID','GND','OV_VALID','SAFE5'],
      'U615':['SRC_TRIP','OV_VALID','GND','TRUE_FAULT','SAFE5'],
      'U616':[None,'TRUE_FAULT','GND','NO_TRUE_FAULT','SAFE5'],
      'U617':['CORE_POR_N','NO_TRUE_FAULT','GND','FAULT_CLEAR_N','SAFE5'],
      'U623':['NOFAULT','MANUAL_RAILS_VALID','GND','MANUAL_VALID_NOFAULT','SAFE5'],
      'U630':['ARMED','MANUAL_VALID_NOFAULT','GND','MAIN_PERMISSION','SAFE5'],
      'U631':['MAIN_PERMISSION','PG_GOOD','GND','SERIES_CLEAR_N','SAFE5'],
      'U632':['SERIES_ARMED','SERIES_CLEAR_N','GND','RUN_GATE_LOGIC','SAFE5'],
      'U633':['FAULT','CORE_POR_N','GND','DISPOSAL_LOGIC','SAFE5'],
      'U644':[None,'SOURCE_CONTACT','GND','SRC_TRIP','SAFE5'],
      'U654':[None,'ARM_CONTACT','GND','ARM_DOWN','SAFE5'],
      'U656':[None,'RESET_CONTACT','GND','RESET_DOWN','SAFE5'],
      'U661':[None,'SERIES_CONTACT','GND','SERIES_DOWN','SAFE5'],
      'U401':['GND','GND','ALERT_LOCAL','SDA_LOCAL','SCL_LOCAL','3V3_LOCAL','GND','LOAD_5V1','INA_IN_MINUS','INA_IN_PLUS'],
      'U402':['VOUT_PROTECTED','GND',None,None,'3V3_LOCAL'],
      'U403':['3V3_HOST','SCL_HOST','SDA_HOST','GND','3V3_LOCAL','SDA_LOCAL','SCL_LOCAL','3V3_LOCAL'],
      'J501':['VIN_RAW','GND'], 'J502':['LOAD_5V1','GND'],
      'J503':['GND','3V3_HOST','SDA_HOST','SCL_HOST'],
      'JP501':['LOAD_5V1','LOAD_FIXTURE'], 'TP505':['LOAD_FIXTURE','GND'],
      'PF1':['VIN_RAW'], 'PF2':['VIN_PROTECTED'], 'PF3':['BUCK_SW'], 'PF4':['L201_IN'], 'PF5':['GND'],
    }
    for ref,nn in contracts.items():pins(ref,nn)
    for ref,source,gate,drain in [('Q301','PROT_MID','PROT_GATE','VOUT_5V1'),('Q302','PROT_MID','PROT_GATE','SERIES_OUT'),('Q303','GND','CB_GATE','CB_DRAIN'),('Q330','GND','RAW_DUMP_GATE','RAW_DUMP_DRAIN')]:
        pins(ref,[source]*3+[gate]+[drain]*4)
    for ref,node in [('D102','VIN_PROTECTED'),('D330','VOUT_5V1'),('D331','VOUT_PROTECTED')]:pins(ref,['GND',node,'GND'])
    for ref,a,b in [
      ('JP101','EFUSE_OUT','VIN_PROTECTED'),('JP201','BUCK_SW','L201_IN'),('L201','L201_IN','L201_OUT'),('JP202','L201_OUT','VOUT_5V1'),
      ('JP301','SERIES_OUT','VOUT_PROTECTED'),('JP330','CB_BALLAST_OUT','CB_DRAIN'),('JP331','RAW_BALLAST_OUT','RAW_DUMP_DRAIN'),
      ('JP660','SER_FEED','SER_DRV'),('JP600','SAFE5','MANUAL_RAILS_VALID'),
      ('D303','VIN_FUSED','AUX_RAW'),('D304','AUX_PREHOLD','AUX_12V'),('D600','SAFE_FEED','DRV_HOLD'),('D660','SER_FEED','DRV_HOLD'),
      ('R330','AUX_LIMITED','AUX_FB'),('R331','AUX_FB','GND'),('R332','AUX_SNS','AUX_LIMITED'),('R333','AUX_GATE_DRIVE','AUX_GATE'),
      ('R340','AUX_12V','AUX_BB_FB'),('R341','AUX_BB_FB','GND'),('R343','AUX_VC','AUX_COMP'),('C356','AUX_COMP','AUX_BB_FB'),
      ('R344','AUX_12V','AUX_FF'),('C357','AUX_FF','AUX_BB_FB'),('R345','AUX_LIMITED','AUX_RUN'),('R346','AUX_RUN','GND'),
      ('C354','AUX_BST1','AUX_SW1'),('C355','AUX_BST2','AUX_SW2'),('L301','AUX_SW1','AUX_SW2'),
      ('R374','HOLD_DVDT','HOLD_SLEW_C'),('C374','HOLD_SLEW_C','GND'),('R375','HOLD_ILM','GND'),
      ('R376','AUX_PREHOLD','HOLD_EN'),('R377','HOLD_EN','GND'),('R378','AUX_PREHOLD','HOLD_OVLO'),('R379','HOLD_OVLO','GND'),
      ('R301','VOUT_5V1','OV_DIV'),('R302','OV_DIV','GND'),('R303','OV_SWITCHED','OV_SENSE'),('R373','REF_2V5','REF_SENSE'),
      ('R361','DRV_HOLD','CLAMP_2V5'),('R367','OV_SENSE','GND'),('R316','3V3_AUX','DET_PG'),('R317','3V3_AUX','BUCK_PGOOD'),
      ('R622','BUCK_PGOOD','PG_DIV'),('R623','PG_SENSE','GND'),('R609','SAFE5','CORE_POR_RAW_N'),
      ('C301','PROT_BST','PROT_MID'),('C302','REF_2V5','GND'),('R305','PROT_GATE','PROT_MID'),('R711','SER_UVLO','GND'),
      ('R709','RUN_GATE_LOGIC','RUN_GATE'),('R710','RUN_GATE','GND'),('R712','DISPOSAL_LOGIC','DISPOSAL'),('R713','DISPOSAL','GND'),
      ('R647','MAIN_PERMISSION','INPUT_SHDN'),('R648','INPUT_SHDN','GND'),('R649','FAULT','FAULT_DRIVE'),('R650','FAULT_DRIVE','GND'),
      ('R717','MANUAL_RAILS_VALID','DET_SWITCH_EN'),('R718','DET_SWITCH_EN','GND'),('R729','MANUAL_RAILS_VALID','GND'),
      ('J301','ARM_CONTACT','GND'),('J302','RESET_CONTACT','GND'),('J603','SOURCE_CONTACT','GND'),('J604','SERIES_CONTACT','GND'),
      ('R730','PG_GOOD','PG_FIXTURE'),('R731','MAIN_PERMISSION','MAIN_FIXTURE'),('J605','PG_FIXTURE','GND'),('J606','MAIN_FIXTURE','GND')]:pair(ref,a,b)
    for ref,a,b in [('R402','SHUNT_KPLUS','INA_IN_PLUS'),('R403','SHUNT_KMINUS','INA_IN_MINUS'),
                    ('C401','INA_IN_PLUS','INA_IN_MINUS'),('TP405','VOUT_PROTECTED','GND'),('TP406','LOAD_5V1','GND')]:pair(ref,a,b)
    for n in ('17','18'):
        if ns.get(('U101',n))!='EFUSE_OUT':errors.append('U101 must feed the main-current link upstream of local input C')
    if not ns.get(('U101','11'),'unconnected-').startswith('unconnected-'):errors.append('U101 MODE must be NC latch-off')
    for refs,tag in [([380,381,382,383,386,387],'A'),([388,389,390,391,392,393],'B')]:
        nn=['VOUT_5V1']+[f'RAW_{tag}{i}' for i in range(1,6)]+['RAW_BALLAST_OUT']
        for i,n in enumerate(refs):pair('R'+str(n),nn[i],nn[i+1])
    for ref,a,b in [('R308','VOUT_PROTECTED','CB_R_A'),('R309','CB_R_A','CB_BALLAST_OUT'),('R310','VOUT_PROTECTED','CB_R_B'),('R311','CB_R_B','CB_BALLAST_OUT')]:pair(ref,a,b)
    for first,last,rail in [(330,338,'VOUT_5V1'),(340,344,'VOUT_PROTECTED')]:
        for n in range(first,last):pair('C'+str(n),rail,'GND')
    for ref in ('C358','C359'):pair(ref,'DRV_HOLD','GND')
    for ref in ('C306','C309','C660'):pair(ref,'SER_DRV','GND')
    # Exact order codes at boundaries cannot be silently changed alongside JSON.
    selected={'F101':'3403.0285.23','D101':'SMCJ36CA','L201':'74437636351002','R301':'TNPW06039K88BEEA','R305':'TNPW12062M00BEEA',
      'R341':'TNPW060388K7BEEA','R312':'TNPW060332K4BEEA','R711':'TNPW0603143KBEEA','R609':'TNPW0603100KBEEA',
      'U316':'LT4363HMS-1#PBF','U317':'LTC3115IFE-1#PBF','U327':'TPS259470LRPWR','J502':'1776508','R401':'WSL27262L000FEA'}
    for n in list(range(308,312))+[380,381,382,383,386,387,388,389,390,391,392,393]:selected['R'+str(n)]='WFMB2512R0330FEA'
    for n in (201,202):selected['C'+str(n)]='GRM32ER71H106KA12L'
    for n in range(209,215):selected['C'+str(n)]='C5750X7R1H226M250KB'
    for ref,mpn in selected.items():
        c=parts.get(ref)
        if c is None or c.findtext('fields/field[@name="MPN"]')!=mpn:errors.append(f'{ref}: independent frozen MPN requires {mpn}')
    for ref in ('C358','C359'):
        c=parts.get(ref)
        if c is None or c.findtext('fields/field[@name="MPN"]')!='EEUFR1E221' or c.findtext('footprint')!='Capacitor_THT:CP_Radial_D8.0mm_P3.50mm':
            errors.append(f'{ref}: Panasonic EEUFR1E221 requires 8mm body / 3.5mm pitch')
    flags={'#FLG101':'VIN_FUSED','#FLG102':'VIN_EFUSE_IN','#FLG103':'VIN_PROTECTED',
      '#FLG301':'AUX_RAW','#FLG302':'VOUT_PROTECTED','#FLG303':'AUX_LIMITED','#FLG304':'SER_DRV','#FLG305':'AUX_PREHOLD','#FLG306':'SAFE_IN',
      '#FLG501':'VIN_RAW','#FLG502':'GND','#FLG503':'3V3_HOST'}
    actual={r:c.get('pins',{}).get('1',{}).get('net') for r,c in specs.items() if c.get('kind')=='FLAG'}
    if actual!=flags:errors.append('Power declaration mismatch: only reviewed physical source paths may carry flags')
    # Multi-component passive bypass check; capacitors and GND excluded. Gate
    # networks never provide an accepted raw-to-protected force path.
    graph={}
    for ref in parts:
        if not re.match(r'[RLFDJ]',ref):continue
        nn={v for (r,p),v in ns.items() if r==ref and v!='GND' and not v.startswith('unconnected-')}
        for n in nn:graph.setdefault(n,set()).update(nn-{n})
    seen=set();todo=['VOUT_5V1']
    while todo:
        n=todo.pop()
        if n in seen:continue
        seen.add(n);todo.extend(graph.get(n,set())-seen)
    if seen & {'VOUT_PROTECTED','LOAD_5V1'}:errors.append('Forbidden passive bypass around opposed series MOSFETs')
    return errors
