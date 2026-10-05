#!/usr/bin/env python3
"""Read-only FIX2 geometry evidence and deliberate pickup-cut test on a temp copy."""
from copper_v1a_lite import *
import heapq, shutil
FIX=ROOT/'docs/evidence/v1a_lite/fix2'
b=load();sha=lambda x:hashlib.sha256(x).hexdigest()
old=json.loads((ROOT/'docs/evidence/v1a_lite/fix1/COPPER_GEOMETRY.json').read_text())
new=json.loads((FIX/'COPPER_GEOMETRY.json').read_text())
assert new['sha256']==sha(BOARD.read_bytes())
def path(j,n,a,c):
 ts=j['nets'][n]['tracks'][0];src=tuple(j['pads'][a]['pos']);dst=tuple(j['pads'][c]['pos'])
 points={src,dst}
 for t in ts:points.update([tuple(t['a']),tuple(t['b'])])
 graph={q:[] for q in points}
 for t in ts:
  aa=t['a'];cc=t['b'];ll=math.dist(aa,cc)
  if ll<1e-8:continue
  pts=sorted((math.dist(aa,q),q) for q in points if abs(math.dist(aa,q)+math.dist(q,cc)-ll)<1e-6)
  for (da,pa),(dc,pc) in zip(pts,pts[1:]):
   graph[pa].append((pc,dc-da,t['width']));graph[pc].append((pa,dc-da,t['width']))
 todo=[(0,src,[])];visited=set()
 while todo:
  length,q,steps=heapq.heappop(todo)
  if q in visited:continue
  visited.add(q)
  if q==dst:return {'length_mm':length,'segments':steps}
  for nxt,ll,w in graph[q]:heapq.heappush(todo,(length+ll,nxt,steps+[{'a':q,'b':nxt,'length_mm':ll,'width_mm':w}]))
 raise RuntimeError((n,a,c))
paths={}
for name,n,a,c in [('CBOOT','/02_BUCK_5V/BUCK_CBOOT','U201.14','C205.1'),('C205_SW','/02_BUCK_5V/BUCK_SW','C205.2','U201.10'),('RBOOT','/02_BUCK_5V/BUCK_RBOOT','U201.13','R204.1'),('VCC','/02_BUCK_5V/BUCK_VCC','U201.2','C206.1'),('FB','/02_BUCK_5V/BUCK_FB','U201.4','R203.1')]:
 paths[name]={'before':path(old,n,a,c),'after':path(new,n,a,c)}
 paths[name]['reduction_percent']=100*(1-paths[name]['after']['length_mm']/paths[name]['before']['length_mm'])
# Original loaded polygons, not assumptions based on net names alone.
l2=[z for z in b.Zones() if z.GetLayer()==p.In1_Cu]
shield={'zones':len(l2),'nets':sorted(set(z.GetNetname() for z in l2)),
 'filled_outlines':sum(z.GetFilledPolysList(p.In1_Cu).OutlineCount() for z in l2),
 'rule_areas':sum(z.GetIsRuleArea() for z in l2),'signal_tracks':sum(not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.In1_Cu for t in b.GetTracks())}
assert shield=={'zones':1,'nets':['/GND'],'filled_outlines':1,'rule_areas':0,'signal_tracks':0},shield
assert old['nets']['/02_BUCK_5V/BUCK_SW']['polys'][0][0]==new['nets']['/02_BUCK_5V/BUCK_SW']['polys'][0][0],'SW zone changed'
assert not new['nets']['/02_BUCK_5V/BUCK_SW']['barrels']
assert all(not a for a in new['nets']['/02_BUCK_5V/BUCK_SW']['tracks'][1:])
# Both pickup cuts must create an isolated island; this catches same-net bypasses
# that normal DRC correctly treats as connected and cannot distinguish as Kelvin.
removed=[]
for t in list(b.GetTracks()):
 if isinstance(t,p.PCB_VIA):continue
 a=xy(t.GetStart());c=xy(t.GetEnd())
 if (math.dist(a,(67.5,58.6))<.001 and math.dist(c,(68.975,56))<.001) or (math.dist(a,(64.6,57.6))<.001 and math.dist(c,(66.025,56))<.001):
  removed.append([t.GetNetname(),a,c]);b.RemoveNative(t)
assert len(removed)==2
with tempfile.TemporaryDirectory(prefix='lite-fix2-cut-') as td:
 td=Path(td);cut=td/BOARD.name
 for suffix in ['.kicad_pro','.kicad_dru']:shutil.copy2(BOARD.with_suffix(suffix),td/BOARD.with_suffix(suffix).name)
 p.SaveBoard(str(cut),b,True)
 result=subprocess.run([CLI,'pcb','drc','--format','json','--severity-all','--all-track-errors','-o',str(FIX/'KELVIN_CUT_DRC.json'),str(cut)],capture_output=True,text=True)
 (FIX/'KELVIN_CUT_DRC.log').write_text(result.stdout+result.stderr)
 j=json.loads((FIX/'KELVIN_CUT_DRC.json').read_text())
 assert len(j['unconnected_items'])==2,j['unconnected_items']
 assert any('[/GND]' in str(a) for a in j['unconnected_items'])
 assert any('[/VOUT_5V1]' in str(a) for a in j['unconnected_items'])
report={'board_sha256':new['sha256'],'classification':'GEOMETRY evidence, not electrical validation','pin_to_cap_centerline_paths':paths,'L2_shield':shield,'main_SW_zone_unchanged':True,'kelvin_cut_test':{'removed':removed,'unconnected_islands':j['unconnected_items'],'note':'Intentional cuts on temporary copy; cut-copy violations are not final-board DRC.'}}
(FIX/'GEOMETRY_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:(v['before']['length_mm'],v['after']['length_mm']) for k,v in paths.items()})
print(shield)
