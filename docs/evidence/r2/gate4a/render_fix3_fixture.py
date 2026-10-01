"""Authored external fixture connectivity/BOM. Not native CAD or approval."""
import csv
import io
from pathlib import Path

HERE=Path(__file__).resolve().parent


def build():
    parts=[]
    pins=[]
    def part(ref,mpn,value,nets,rating='Selected; application qualification T12F3 OPEN'):
        assert ref not in [p['refdes'] for p in parts],ref
        parts.append(dict(refdes=ref,manufacturer_part=mpn,value=value,
                          scope='EXTERNAL BENCH FIXTURE ONLY',rating_or_gate=rating))
        for pin,net in nets.items():
            pins.append(dict(refdes=ref,pin=str(pin),net=net))
    def r(ref,code,value,a,b):
        part(ref,'TNPW0603'+code+'BEEA',value,{1:a,2:b},'Vishay28758; <=0.125W development limit; local <=70C')
    def c(ref,a,b,value='100nF',mpn='GRM188R71H104KA93D'):
        part(ref,mpn,value,{1:a,2:b})
    def gate(n,kind,a,b,y):
        mpn={'AND':'SN74LVC1G08DBVR','OR':'SN74LVC1G32DBVR',
             'INV':'SN74LVC1G14DBVR','BUF':'SN74LVC1G17DBVR'}[kind]
        p={1:a,2:b,3:'FGND',4:y,5:'FX5'} if kind in ['AND','OR'] else {1:'NC',2:a,3:'FGND',4:y,5:'FX5'}
        part('UF'+str(n),mpn,kind,p)
        c('CF'+str(100+n),'FX5','FGND')
    def ff(n,clk,d,q,nq,clear):
        part('UF'+str(n),'SN74LVC1G74DCTR','DFF',
             {1:clk,2:d,3:nq,4:'FGND',5:q,6:clear,7:'FX5',8:'FX5'})
        c('CF'+str(100+n),'FX5','FGND')
    def timer(n,inp,out,div):
        part('UF'+str(n),'LTC6994IS6-1#TRMPBF','rising qualifier',
             {1:inp,2:'FGND',3:'SET'+str(n),4:div,5:'FX5',6:out})
        r('RF'+str(100+n),'100K','100k','SET'+str(n),'FGND')
        c('CF'+str(100+n),'FX5','FGND')

    part('PSF1','Rigol DP811A','Main isolated bench supply',{'OUT+':'PS_PLUS','OUT-':'PS_MINUS'},
         '0-40V/5A range; calibrated terminal ceiling30V; room <=40C; inventory OPEN')
    part('PSF2','Rigol DP811A','Control supply set12V',{'OUT+':'FX12','OUT-':'FGND'},
         'Separate output; <=13V including error; room <=40C; inventory OPEN')
    # The SB50 is used wire-to-wire; no busbar/PCB-contact current extrapolation.
    for ref,nets in [('JF1A',{'+':'PS_PLUS','-':'PS_MINUS'}),('JF1B',{'+':'FX_SOURCE','-':'FGND'})]:
        part(ref,'Anderson 992G1','red SB50 housing',nets,'Dead disconnect; 5900 contacts/6AWG; <=14A; local <=40C')
    part('KF1','Anderson 5900','4 contacts for JF1A/B',{},'Use 1309G4 hand tool; inspect/crimp pull test; DS-SB50 RevC7 p7')
    part('WF1','Belden 9906','6AWG 133x27 TC; cut/label red + and black -',{},
         '600V/105C insulation; <=14A feeder; keep outside hot zone; paired route; length recorded')
    part('TF1','Anderson 1309G4','SB50 crimp tool',{},'Tool condition/die/strip length per assembly instructions; inventory OPEN')
    for n in range(1,5):
        part('RFL'+str(n),'NH2509R100FE01','9.1ohm 1% 250W noninductive',
             {1:'FX_SOURCE',2:'FX_LIMITED'},'Four parallel; each separate 12x12x0.125in Al panel; <=70C ambient; verify mount')
        part('HF'+str(n),'CUSTOM-FX-AL-01 RevA','12x12x0.125in aluminum panel',{},
             'Vishay30201 RH250 mounting geometry; flat thermal interface; no stacked panels')
    # MOSFET terminal grouping follows the actual TDSON-8 pinout.
    for n,d,s,g in [(1,'VIN_PROTECTED','L201_IN','FGATE1'),
                    (2,'NATIVE_SW','FX_ISO_MID','FGATE2'),
                    (3,'L201_IN','FX_ISO_MID','FGATE2'),
                    (4,'FX_LIMITED','FX_SOURCE_MID','FGATE3'),
                    (5,'DUT_IN','FX_SOURCE_MID','FGATE3')]:
        part('QF'+str(n),'BSC034N06NSATMA1','60V N-channel',
             {1:s,2:s,3:s,4:g,5:d,6:d,7:d,8:d},'VDS <=50V, |VGS|<20V, on VGS>=10V; hot SOA OPEN')
    for n,ts,cmd in [(1,'L201_IN','INJECT_CMD'),(2,'FX_ISO_MID','ISO_CMD'),(3,'FX_SOURCE_MID','FX_ARMED')]:
        v='FX_DRV'+str(n)
        bst='FBST'+str(n)
        part('UF'+str(n),'LTC7001IMSE#PBF','high-side driver',
             {1:v,2:'FUV'+str(n),3:'FGND',4:'FIN'+str(n),5:'FGND',
              6:'FGATE'+str(n),7:'FTGUP'+str(n),8:ts,9:bst,10:'NC',11:'FGND'})
        part('DF'+str(10+n),'B260-13-F','local reservoir isolation',{'A':'FX12','K':v})
        c('CF'+str(n),v,'FGND','10uF/50V effective>=5uF','GRM32ER71H106KA12L')
        c('CF'+str(10+n),v,'FGND')
        c('CF'+str(20+n),bst,ts,'1uF/25V effective>=0.5uF','GRM21BR71E105KA99L')
        part('DF'+str(20+n),'BAS116,215','bootstrap diode',{1:v,2:'NC',3:bst})
        r('RF'+str(n),'143K','143k','FUV'+str(n),'FGND')
        r('RF'+str(10+n),'1R00','1ohm','FTGUP'+str(n),'FGATE'+str(n))
        r('RF'+str(20+n),'2M00','2Mohm','FGATE'+str(n),ts)
        r('RF'+str(30+n),'1K00','1kohm',cmd,'FIN'+str(n))
        r('RF'+str(40+n),'10K0','10kohm','FIN'+str(n),'FGND')
        r('RF'+str(60+n),'10K0','10kohm',v,'FGND')
    for n,node in [(1,'L201_IN'),(2,'DUT_IN')]:
        part('DF'+str(n),'STPS60H100CT','100V dual common cathode',
             {1:'FGND',2:node,3:'FGND','TAB':node},'Both anodes connected; local <=70C; actual hot commutation OPEN')
    part('DF3','SMCJ30CA','bidirectional source transient clamp',{1:'FX_LIMITED',2:'FGND'},
         'Littelfuse; 30V standoff/48.4V at31A 25C 10/1000us; hot/ringing <=50V must be measured')
    part('DF4','B260-13-F','logic reservoir isolation',{'A':'FX12','K':'FX_LOGIC_IN'})
    c('CF40','FX_LOGIC_IN','FGND','10uF/50V effective>=5uF','GRM32ER71H106KA12L')
    part('UF10','TPS7A1601DGNR','5.05832V regulator',
         {1:'FX5',2:'FX_FB',3:'NC',4:'FGND',5:'FX_LOGIC_IN',6:'NC',7:'NC',8:'FX_LOGIC_IN',9:'FGND'})
    r('RF50','32K4','32.4k','FX5','FX_FB'); r('RF51','10K0','10k','FX_FB','FGND')
    c('CF41','FX5','FGND','10uF/50V effective>=5uF','GRM32ER71H106KA12L')
    part('UF11','TPS3808G50DBVR','POR',
         {1:'FX_POR_RAW_N',2:'FGND',3:'FX5',4:'NC',5:'FX5',6:'FX5'})
    c('CF111','FX5','FGND'); r('RF52','10K0','10k','FX5','FX_POR_RAW_N')
    gate(12,'BUF','FX_POR_RAW_N',None,'FX_POR_N')
    part('DF40','LM4040A25IDBZR','2.5V shunt',{1:'FX_REF',2:'FGND',3:'FGND'})
    r('RF53','10K0','10k','FX5','FX_REF')
    c('CF42','FX_REF','FGND','10nF/50V','C1608C0G1H103J080AA')
    r('RF54','30K1','30.1k','FX12','FX_RAIL_DIV')
    r('RF55','10K0','10k','FX_RAIL_DIV','FGND')
    r('RF56','100K','100k','FX_RAIL_SENSE','FGND')
    for ref,a,k in [('DF41','FX_RAIL_DIV','FX_REF'),('DF42','FGND','FX_RAIL_DIV')]:
        part(ref,'BAS116,215','input clamp',{1:a,2:'NC',3:k})
    part('UF13','TLV3201AIDBVR','FX12 fast validity',
         {1:'FX_RAIL_OK',2:'FGND',3:'FX_RAIL_SENSE',4:'FX_REF',5:'FX5'})
    c('CF113','FX5','FGND')
    part('UF14','ADG4612BRUZ','power-off isolation',
         {1:'FX5',2:'FX_RAIL_DIV',3:'FX_RAIL_SENSE',4:'FGND',5:'FGND',6:'FGND',7:'FGND',
          8:'FGND',9:'FGND',10:'FGND',11:'FGND',12:'NC',13:'FX5',14:'FGND',15:'FGND',16:'FGND'})
    c('CF114','FX5','FGND')
    gate(15,'AND','FX_RAIL_OK','FX_POR_N','FX_READY')
    gate(16,'INV','ABORT',None,'NOT_ABORT')
    gate(17,'AND','RESET_N','FX_READY','CLR_A')
    gate(18,'AND','CLR_A','STOP_OK','CLR_B')
    gate(19,'AND','CLR_B','NOT_ABORT','FX_ARM_CLEAR_N')
    ff(20,'ARM_EDGE','NOT_SHOT','FX_ARMED','NC','FX_ARM_CLEAR_N')
    ff(21,'FIRE_EDGE','SHOT_OR_START','SHOT','NOT_SHOT','CLR_A')
    gate(22,'AND','DUT_PG_OK','DUT_PERMISSION','START_A')
    gate(23,'AND','START_A','FX_ARMED','START_OK')
    timer(24,'SHOT','DEAD_READY','FGND')
    timer(25,'SHOT','ABORT','ABORT_DIV')
    r('RF57','200K','200k','FX5','ABORT_DIV'); r('RF58','20K5','20.5k','ABORT_DIV','FGND')
    gate(26,'AND','FX_ARMED','NOT_SHOT','ISO_CMD')
    gate(27,'AND','FX_ARMED','DEAD_READY','INJECT_CMD')
    gate(28,'BUF','STOP_RAW',None,'STOP_OK')
    gate(29,'BUF','RESET_RAW_N',None,'RESET_N')
    gate(30,'INV','ARM_CONTACT',None,'ARM_EDGE')
    gate(31,'INV','FIRE_CONTACT',None,'FIRE_EDGE')
    gate(32,'OR','SHOT','START_OK','SHOT_OR_START')
    for ref,node,kind in [('SF1','STOP_RAW','stop'),('SF2','RESET_RAW_N','reset'),
                          ('SF3','ARM_CONTACT','arm'),('SF4','FIRE_CONTACT','fire')]:
        # Toggle contacts, deliberately returned before a new cycle. No assumed button pinout.
        nets={1:'FX5' if kind=='stop' else node,2:node if kind=='stop' else 'FGND',
              3:'NC',4:'NC',5:'NC',6:'NC'}
        part(ref,'7201SYZQE','C&K DPDT service toggle; one pole used',nets,
             'Dry low-current controls; validate wetting/continuity; no force current')
    for n,node in [(70,'RESET_RAW_N'),(71,'ARM_CONTACT'),(72,'FIRE_CONTACT')]:
        r('RF'+str(n),'10K0','10k','FX5',node)
    r('RF73','10K0','10k','STOP_RAW','FGND')
    for n,net in [(80,'DUT_PG_OK'),(81,'DUT_PERMISSION')]:
        r('RF'+str(n),'10K0','10k',net,'FGND')
        r('RF'+str(n+2),'1K00','1k','HOOK_'+net,net)
    part('JF2','1776508 + 1777989','Phoenix signal header+plug',{1:'HOOK_DUT_PG_OK',2:'FGND'})
    part('JF3','1776508 + 1777989','Phoenix signal header+plug',{1:'HOOK_DUT_PERMISSION',2:'FGND'})
    # Manual floating-cap discharge; open for operation. Separate returns, never a common bus.
    for n,bst,ts in [(1,'FBST1','L201_IN'),(2,'FBST2','FX_ISO_MID'),
                     (3,'FBST3','FX_SOURCE_MID'),(4,'PROT_BST','PROT_MID')]:
        r('RF'+str(90+n),'100K','100k',bst,'FDRAIN'+str(n))
        part('SFD'+str(n),'7201SYZQE','C&K service discharge toggle',
             {1:'FDRAIN'+str(n),2:ts,3:'NC',4:'NC',5:'NC',6:'NC'},
             'Open during run; close only after sources removed; insulated accessible actuator')
    for n,net,ret in [(13,'SAFE_IN','FGND'),(14,'SAFE5','FGND'),(15,'SER_DRV','FGND'),
                      (16,'REF_SAFE_2V5','FGND'),(17,'FX_LOGIC_IN','FGND'),(18,'FX5','FGND')]:
        part('RFD'+str(n),'TNPW120610K0BEEA','10kohm discharge adapter',{1:net,2:ret},
             'Permanent characterized load; <=0.125W at<=70C; local return')
        part('JFD'+str(n),'1776508 + 1777989','Phoenix adapter connection',{1:net,2:ret})
    part('BF1','CUSTOM-FX-CU-01 RevA','C110 force strap set',{},
         '2mm x15mm; <=30mm span; 4.5mm holes20mm pitch; Kelvin joint<=0.2mohm; assembly L<=40nH')
    part('MF1','CUSTOM-FX-M4-01 RevA','M4 hardware/insulated supports/cover set',{},
         'M4x12 A2-70 bolt, two4.3/9/0.8 washers, M4 all-metal locknut per joint; separate supports')
    return parts,pins


def render():
    parts,pins=build()
    out={}
    for name,rows in [('FIX3_FIXTURE_BOM.csv',parts),('FIX3_FIXTURE_NETLIST.csv',pins)]:
        s=io.StringIO(); w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\n')
        w.writeheader(); w.writerows(rows); out[name]=s.getvalue()
    return out


if __name__=='__main__':
    for name,data in render().items(): (HERE/name).write_text(data)
