#!/usr/bin/env python3
"""Read-only final copper extraction for resistor mesh; KiCad Python."""
from copper_v1a_lite import *
def polys(pp):
 return [{'outer':[xy(pp.COutline(k).CPoint(i)) for i in range(pp.COutline(k).PointCount())], 'holes':[[xy(pp.CHole(k,h).CPoint(i)) for i in range(pp.CHole(k,h).PointCount())] for h in range(pp.HoleCount(k))]} for k in range(pp.OutlineCount())]
b=load();layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu];data={'sha256':hashlib.sha256(BOARD.read_bytes()).hexdigest(),'nets':{},'pads':{},'holes':[]}
data.update(layers=['F.Cu','In1.Cu','In2.Cu','B.Cu'],thickness_mm=[.035,.0152,.0152,.035],z_mm=[.0175,.253,1.3332,1.5687])
for name in sorted({q.GetNetname() for f in b.GetFootprints() for q in f.Pads() if q.GetNetCode()>0}):
 out={'polys':[[] for _ in layers],'tracks':[[] for _ in layers],'barrels':[]};data['nets'][name]=out
 for z in b.Zones():
  if not z.GetIsRuleArea() and z.GetNetname()==name:out['polys'][layers.index(z.GetLayer())]+=polys(z.GetFilledPolysList(z.GetLayer()))
 for f in b.GetFootprints():
  for q in f.Pads():
   if q.GetNetname()!=name:continue
   poly=polys(q.GetEffectivePolygon(p.F_Cu));data['pads'][f.GetReference()+'.'+q.GetNumber()]={'net':name,'polys':poly,'pos':xy(q.GetPosition()),'drill':xy(q.GetDrillSize())}
   for idx,ly in enumerate(layers):
    if q.IsOnLayer(ly):out['polys'][idx]+=polys(q.GetEffectivePolygon(ly))
   if q.GetDrillSize().x:out['barrels'].append({'pos':xy(q.GetPosition()),'drill':p.ToMM(q.GetDrillSize().x),'diameter':min(xy(q.GetSize()))})
 for t in b.GetTracks():
  if t.GetNetname()!=name:continue
  if isinstance(t,p.PCB_VIA):out['barrels'].append({'pos':xy(t.GetPosition()),'drill':p.ToMM(t.GetDrill()),'diameter':p.ToMM(t.GetWidth(p.F_Cu))})
  else:out['tracks'][layers.index(t.GetLayer())].append({'a':xy(t.GetStart()),'b':xy(t.GetEnd()),'width':p.ToMM(t.GetWidth())})
for f in b.GetFootprints():
 for q in f.Pads():
  if q.GetDrillSize().x:data['holes'].append([*xy(q.GetPosition()),p.ToMM(q.GetDrillSize().x)])
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):data['holes'].append([*xy(t.GetPosition()),p.ToMM(t.GetDrill())])
(ROOT/'docs/evidence/v1a_lite/fix1/COPPER_GEOMETRY.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
