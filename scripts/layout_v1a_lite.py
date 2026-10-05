#!/usr/bin/env python3
"""Owner-authorized Lite review layout. Run with KiCad bundled Python. No release."""
import argparse, collections, hashlib, json, math, re, subprocess, tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]; CAD=ROOT/'hardware/kicad'; BOARD=CAD/'V1A.kicad_pcb'; PRO=BOARD.with_suffix('.kicad_pro')
EV=ROOT/'docs/evidence/v1a_lite/layout'; CLI='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
LIB=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
WARN='NOT FOR FABRICATION - ENGINEERING REVIEW REQUIRED'
def mm(x):return p.FromMM(x)
def v(x,y):return p.VECTOR2I(mm(x),mm(y))
def xy(q):return (p.ToMM(q.x),p.ToMM(q.y))
def save(b):p.SaveBoard(str(BOARD),b,True)
def load():
 b=p.LoadBoard(str(BOARD));m=p.GetSettingsManager();m.LoadProject(str(PRO));b.SetProject(m.GetProject(str(PRO)));b.SynchronizeNetsAndNetClasses(False);return b

def schematic():
 subprocess.run([CLI,'sch','export','netlist','--format','kicadxml','-o',str(EV/'schematic.xml'),str(CAD/'V1A.kicad_sch')],check=True)
 root=ET.parse(EV/'schematic.xml').getroot()
 return {c.get('ref'):c for c in root.findall('./components/comp')},{n.get('name'):n for n in root.findall('./nets/net')}
def import_board():
 from make_schematic_readable import parse,nodes,one,prop,val
 cs,ns=schematic();attrs={}
 for path in CAD.glob('*.kicad_sch'):
  for s in nodes(parse(path.read_text()),'symbol'):
   attrs[val(prop(s,'Reference')[2])]={'exclude':one(s,'in_bom')[1]=='no','dnp':one(s,'dnp')[1]=='yes'}
 ru=re.search(r'\(uuid "([^"]+)"\)',(CAD/'V1A.kicad_sch').read_text())[1]
 b=p.BOARD();b.SetCopperLayerCount(2);nets={}
 for name in ns:
  n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
 node={(nd.get('ref'),nd.get('pin')):(name,nd) for name,net in ns.items() for nd in net.findall('node')}
 sources={}
 for i,(r,c) in enumerate(cs.items()):
  lib,item=c.findtext('footprint').split(':');base=CAD/(lib+'.pretty') if lib.startswith('V1A_') else LIB/(lib+'.pretty')
  fp=p.FootprintLoad(str(base),item);assert fp is not None,(r,lib,item)
  fp.SetFPID(p.LIB_ID(lib,item));fp.SetReference(r);fp.SetValue(c.findtext('value'));fp.SetExcludedFromBOM(attrs[r]['exclude']);fp.SetExcludedFromPosFiles(attrs[r]['exclude']);fp.SetDNP(attrs[r]['dnp'])
  fp.SetPath(p.KIID_PATH('/'+ru+c.find('sheetpath').get('tstamps')+c.findtext('tstamps')))
  props={q.get('name'):q.get('value') for q in c.findall('property')};fp.SetSheetname(props['Sheetname']);fp.SetSheetfile(props['Sheetfile'])
  for field in c.findall('./fields/field'):
   name=field.get('name')
   if name=='Footprint':continue
   f=fp.GetFieldByName(name)
   if f is None:f=p.PCB_FIELD(fp,fp.GetNextFieldId(),name);fp.AddField(f)
   f.SetText(field.text or '');f.SetVisible(False)
  b.Add(fp)
  for q in fp.Pads():
   if q.GetNumber():
    name,nd=node[r,q.GetNumber()];q.SetNet(nets[name]);q.SetPinFunction(nd.get('pinfunction',''));q.SetPinType(nd.get('pintype',''))
  fp.SetPosition(v(20+(i%12)*15,20+(i//12)*15));fp.SetIsPlaced(False)
  src=base/(item+'.kicad_mod');sources[lib+':'+item]={'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
 title=b.GetTitleBlock();title.SetTitle('V1A-Lite layout review');title.SetComment(0,WARN);b.SetTitleBlock(title);save(b)
 (EV/'FOOTPRINT_SOURCES.json').write_text(json.dumps(sources,indent=2)+'\n')
 parity(b,cs,ns)
def parity(b,cs=None,ns=None):
 if cs is None:cs,ns=schematic()
 fs={f.GetReference():f for f in b.GetFootprints() if not f.GetAttributes()&p.FP_BOARD_ONLY};issues=[]
 if set(fs)!=set(cs):issues.append('Reference mismatch')
 node={(nd.get('ref'),nd.get('pin')):name for name,net in ns.items() for nd in net.findall('node')};count=0
 for r,c in cs.items():
  f=fs[r]
  if f.GetValue()!=c.findtext('value') or f.GetFPID().GetUniStringLibId()!=c.findtext('footprint'):issues.append(r+' identity')
  for q in f.Pads():
   if q.GetNumber():
    count+=1
    if q.GetNetname()!=node.get((r,q.GetNumber())):issues.append(r+'.'+q.GetNumber()+' net')
  if set(q.GetNumber() for q in f.Pads() if q.GetNumber())!={pin for rr,pin in node if rr==r}:issues.append(r+' pins')
 report={'issues':issues,'footprints':len(fs),'numbered_pads':count,'nets':len(ns),'board_sha256':hashlib.sha256(BOARD.read_bytes()).hexdigest()}
 (EV/'PARITY.json').write_text(json.dumps(report,indent=2)+'\n');print(report);assert not issues

def settings():
 cs,ns=schematic();j=json.loads(PRO.read_text());base=j['net_settings']['classes'][0].copy();base.update(name='Default',clearance=.15,track_width=.25,via_diameter=.6,via_drill=.3)
 classes=[]
 for name,w,cl in [('Default',.25,.15),('Power',1,.2),('Switching',.5,.15),('Sense',.2,.15)]:
  clz=base.copy();clz.update(name=name,track_width=w,clearance=cl);classes.append(clz)
 patterns=[]
 for n in ns:
  if n.startswith('unconnected'):continue
  cl='Power' if n in ['/GND','/VIN_RAW','/VIN_PROTECTED','/VOUT_5V1','/VOUT_PI','/01_INPUT_PROTECTION/VIN_FUSED','/01_INPUT_PROTECTION/S_COMMON'] else 'Switching' if n.endswith('/BUCK_SW') else 'Sense' if n.endswith(('BUCK_FB','OUT_OV_REF','IN_OV_REF')) else 'Default'
  patterns.append({'pattern':n,'netclass':cl})
 j['net_settings']['classes']=classes;j['net_settings']['netclass_patterns']=patterns;j['net_settings']['netclass_assignments']={}
 j['board']['design_settings']={'rules':{'min_clearance':.15,'min_track_width':.15,'min_via_diameter':.6,'min_through_hole_diameter':.3,'min_via_annular_width':.15,'min_hole_to_hole':.25,'min_hole_clearance':.25,'min_copper_edge_clearance':.5,'solder_mask_clearance':0.0,'solder_mask_min_width':.1},'drc_exclusions':[]}
 PRO.write_text(json.dumps(j,indent=2)+'\n')

def text(b,s,x,y,size=.8,layer=p.F_SilkS):
 t=p.PCB_TEXT(b);t.SetText(s);t.SetPosition(v(x,y));t.SetTextSize(v(size,size));t.SetTextThickness(mm(.12));t.SetLayer(layer);b.Add(t)
def mechanics():
 b=load()
 for d in list(b.GetDrawings()):b.RemoveNative(d)
 for f in list(b.GetFootprints()):
  if f.GetAttributes()&p.FP_BOARD_ONLY:b.RemoveNative(f)
 for a,c in [((10,10),(90,10)),((90,10),(90,70)),((90,70),(10,70)),((10,70),(10,10))]:
  e=p.PCB_SHAPE();e.SetShape(p.SHAPE_T_SEGMENT);e.SetStart(v(*a));e.SetEnd(v(*c));e.SetLayer(p.Edge_Cuts);e.SetWidth(mm(.05));b.Add(e)
 for i,(x,y) in enumerate([(14,14),(86,14),(14,66),(86,66)],1):
  f=p.FootprintLoad(str(LIB/'MountingHole.pretty'),'MountingHole_3.2mm_M3');f.SetReference('MH'+str(i));f.SetValue('M3 NPTH');f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES);f.SetPosition(v(x,y));f.Reference().SetVisible(False);f.Value().SetVisible(False);b.Add(f)
 b.GetDesignSettings().SetAuxOrigin(v(10,10));save(b)
 s=BOARD.read_text();needle='\t(setup\n';at=s.index(needle)+len(needle)
 stack='\t\t(stackup\n'
 for name,kind,t in [('F.SilkS','Top Silk Screen',None),('F.Paste','Top Solder Paste',None),('F.Mask','Top Solder Mask',.01),('F.Cu','copper',.035),('dielectric 1','core',1.51),('B.Cu','copper',.035),('B.Mask','Bottom Solder Mask',.01),('B.Paste','Bottom Solder Paste',None),('B.SilkS','Bottom Silk Screen',None)]:stack+=f'\t\t\t(layer "{name}" (type "{kind}")'+(f' (thickness {t})' if t else '')+')\n'
 stack+='\t\t\t(copper_finish "Lead free HASL")\n\t\t\t(dielectric_constraints no)\n\t\t)\n'
 if '(stackup' not in s:s=s[:at]+stack+s[at:];BOARD.write_text(s)

def dump_pads():
 b=load()
 for f in b.GetFootprints():
  if f.GetReference() in ['U201','Q101','J501','SCR301','D106','L201','F301']:
   org=f.GetPosition();print(f.GetReference(),f.GetFPID().GetUniStringLibId())
   for q in f.Pads():
    if q.GetNumber():print(q.GetNumber(),xy(q.GetPosition()-org),xy(q.GetSize()),q.GetNetname())
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('step',choices=['import','settings','mechanics','parity','pads']);a=ap.parse_args();EV.mkdir(parents=True,exist_ok=True)
 {'import':import_board,'settings':settings,'mechanics':mechanics,'parity':lambda:parity(load()),'pads':dump_pads}[a.step]()
