#!/usr/bin/env python3
"""Read-only engineering inventory of the saved FIX1 board."""
from copper_v1a_lite import *
FIX=ROOT/'docs/evidence/v1a_lite/fix1'
b=load();ps=pads(b)
out={'board_sha256':hashlib.sha256(BOARD.read_bytes()).hexdigest(),'layers':b.GetCopperLayerCount(),'pads':{},'nets':{},'via_centers_in_smd_lands':[],'zone_area_mm2':[]}
for r in ['J501','J502','J503','U201','Q101','Q102','SCR301','C217','C218','C209','C214','R204','C205','C206','R203','R308','TP113','TP114','TP301','TP302']:
 out['pads'][r]={k:{'net':q.GetNetname(),'pos':xy(q.GetPosition())} for (ref,k),q in ps.items() if ref==r}
for name in ['BUCK_RBOOT','BUCK_CBOOT','BUCK_VCC','BUCK_FB']:
 ts=[t for t in b.GetTracks() if t.GetNetname().endswith('/'+name)]
 out['nets'][name]={'via_count':sum(isinstance(t,p.PCB_VIA) for t in ts),'track_length_mm':sum(math.dist(xy(t.GetStart()),xy(t.GetEnd())) for t in ts if not isinstance(t,p.PCB_VIA)),'layers':sorted(set(b.GetLayerName(t.GetLayer()) for t in ts if not isinstance(t,p.PCB_VIA)))}
for z in b.Zones():
 if z.GetIsRuleArea():continue
 pp=z.GetFilledPolysList(z.GetLayer());area=sum(abs(pp.COutline(k).Area())-sum(abs(pp.CHole(k,h).Area()) for h in range(pp.HoleCount(k))) for k in range(pp.OutlineCount()))/1e12
 out['zone_area_mm2'].append({'net':z.GetNetname(),'layer':b.GetLayerName(z.GetLayer()),'area':area})
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA):continue
 hits=[]
 for f in b.GetFootprints():
  for q in f.Pads():
   if q.GetNumber() and q.GetAttribute()==p.PAD_ATTRIB_SMD and q.GetEffectivePolygon(p.F_Cu).Contains(t.GetPosition()):hits.append(f.GetReference()+'.'+q.GetNumber())
 if hits:out['via_centers_in_smd_lands'].append({'pos':xy(t.GetPosition()),'net':t.GetNetname(),'lands':hits})
(FIX/'BOARD_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['nets']);print('Residual via centers in SMD lands',len(out['via_centers_in_smd_lands']))
# Check actual hole edges against exposed SMD/test lands on BOTH faces.
# Board mask expansion is zero; outlines include KiCad rounded corners.
def segment_distance(pt,a,c):
 dx=c[0]-a[0];dy=c[1]-a[1];den=dx*dx+dy*dy
 t=max(0,min(1,((pt[0]-a[0])*dx+(pt[1]-a[1])*dy)/den)) if den else 0
 return math.dist(pt,(a[0]+t*dx,a[1]+t*dy))
land_polys=[]
for f in b.GetFootprints():
 for q in f.Pads():
  if not q.GetNumber() or q.GetDrillSize().x:continue
  ly=p.F_Cu if q.IsOnLayer(p.F_Cu) else p.B_Cu
  pp=q.GetEffectivePolygon(ly)
  for k in range(pp.OutlineCount()):
   ch=pp.COutline(k);pts=[xy(ch.CPoint(j)) for j in range(ch.PointCount())]
   land_polys.append((f.GetReference()+'.'+q.GetNumber(),pts,ch))
close=[];minimum=100
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA):continue
 pt=xy(t.GetPosition());rad=p.ToMM(t.GetDrill())/2
 for ref,pts,ch in land_polys:
  if min(x for x,y in pts)-1>pt[0] or max(x for x,y in pts)+1<pt[0] or min(y for x,y in pts)-1>pt[1] or max(y for x,y in pts)+1<pt[1]:continue
  dd=min(segment_distance(pt,a,c) for a,c in zip(pts,pts[1:]+pts[:1]))
  gap=(-dd if ch.PointInside(t.GetPosition()) else dd)-rad
  minimum=min(minimum,gap)
  if gap<.0999:close.append({'via':pt,'land':ref,'hole_to_open_land_mm':gap})
out['hole_to_smd_mask_minimum_mm']=minimum
out['hole_to_smd_mask_below_0.1mm']=close
out['test_pairs']={name:{'refs':refs,'centers':[xy(ps[r,'1'].GetPosition()) for r in refs],'separation_mm':math.dist(*[xy(ps[r,'1'].GetPosition()) for r in refs])} for name,refs in [('Q102',['TP113','TP114']),('SCR',['TP301','TP302']),('raw_ripple',['TP504','TP506'])]}
(FIX/'BOARD_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print('Hole-to-open-land minimum',minimum,'under 0.1mm',len(close))
