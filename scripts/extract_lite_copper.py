#!/usr/bin/env python3
"""Read-only final copper extraction for resistor mesh; KiCad Python."""
from copper_v1a_lite import *
def polys(pp):
 return [{'outer':[xy(pp.COutline(k).CPoint(i)) for i in range(pp.COutline(k).PointCount())], 'holes':[[xy(pp.CHole(k,h).CPoint(i)) for i in range(pp.CHole(k,h).PointCount())] for h in range(pp.HoleCount(k))]} for k in range(pp.OutlineCount())]
b=load();data={'sha256':hashlib.sha256(BOARD.read_bytes()).hexdigest(),'nets':{},'pads':{},'holes':[]}
for name in ['/VOUT_5V1','/VOUT_PI','/GND']:
 out={'polys':[[],[]],'tracks':[[],[]],'barrels':[]};data['nets'][name]=out
 for z in b.Zones():
  if not z.GetIsRuleArea() and z.GetNetname()==name:out['polys'][[p.F_Cu,p.B_Cu].index(z.GetLayer())]+=polys(z.GetFilledPolysList(z.GetLayer()))
 for f in b.GetFootprints():
  for q in f.Pads():
   if q.GetNetname()!=name:continue
   poly=polys(q.GetEffectivePolygon(p.F_Cu));data['pads'][f.GetReference()+'.'+q.GetNumber()]={'net':name,'polys':poly,'pos':xy(q.GetPosition()),'drill':xy(q.GetDrillSize())}
   for idx,ly in enumerate([p.F_Cu,p.B_Cu]):
    if q.IsOnLayer(ly):out['polys'][idx]+=polys(q.GetEffectivePolygon(ly))
   if q.GetDrillSize().x:out['barrels'].append({'pos':xy(q.GetPosition()),'drill':p.ToMM(q.GetDrillSize().x),'diameter':min(xy(q.GetSize()))})
 for t in b.GetTracks():
  if t.GetNetname()!=name:continue
  if isinstance(t,p.PCB_VIA):out['barrels'].append({'pos':xy(t.GetPosition()),'drill':p.ToMM(t.GetDrill()),'diameter':p.ToMM(t.GetWidth())})
  else:out['tracks'][[p.F_Cu,p.B_Cu].index(t.GetLayer())].append({'a':xy(t.GetStart()),'b':xy(t.GetEnd()),'width':p.ToMM(t.GetWidth())})
for f in b.GetFootprints():
 for q in f.Pads():
  if q.GetDrillSize().x:data['holes'].append([*xy(q.GetPosition()),p.ToMM(q.GetDrillSize().x)])
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):data['holes'].append([*xy(t.GetPosition()),p.ToMM(t.GetDrill())])
(EV/'COPPER_GEOMETRY.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
