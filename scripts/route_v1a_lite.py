#!/usr/bin/env python3
"""Project signal-only maze routing around authored power. No external router.
KiCad Python; compile v1a_grid_router.cpp to /tmp/lite-router.dylib first.
In1.Cu is never a signal routing layer. Existing power geometry is immutable.
"""
import ctypes as c, math, json, collections, argparse
from copper_v1a_lite import *
LAYS=[p.F_Cu,p.B_Cu];S=.05;X0=10.85;Y0=10.85;W=1567;H=1167
class Router:
 def __init__(self,b):
  self.classes={a['pattern']:a['netclass'] for a in json.loads(BOARD.with_suffix('.kicad_pro').read_text())['net_settings']['netclass_patterns']}
  self.b=b;self.lib=c.CDLL('/tmp/lite-router.dylib');self.ps=pads(b);self.log=[]
  self.lib.init.argtypes=[c.c_int,c.c_int,c.c_double,c.c_double,c.c_double]
  self.lib.capsule.argtypes=[c.c_int,c.c_int]+[c.c_double]*5+[c.c_int]
  self.lib.polygon.argtypes=[c.c_int,c.c_int,c.POINTER(c.c_double),c.c_int,c.c_double,c.c_int]
  self.lib.polygon_holes.argtypes=[c.c_int,c.c_int,c.POINTER(c.c_double),c.POINTER(c.c_int),c.c_int,c.c_double,c.c_int]
  self.lib.route.argtypes=[c.c_int]*8+[c.POINTER(c.c_int),c.c_int,c.c_int]
  self.lib.init(W,H,S,X0,Y0)
  self.out=(c.c_int*(3*40000))()
  for f in b.GetFootprints():
   for pad in f.Pads():
    nc=pad.GetNetCode() or -1
    for z,layer in enumerate(LAYS):
     if pad.IsOnLayer(layer):
      pp=pad.GetEffectivePolygon(layer)
      for k in range(pp.OutlineCount()):self.poly(z,nc,pp,k,.34,0);self.poly(z,nc,pp,k,.56,1)
    dr=xy(pad.GetDrillSize())
    if max(dr)>0:
     # A drilled pad is an obstacle to new holes, including same-net holes.
     q=xy(pad.GetPosition());rr=max(dr)/2+.56
     for z in range(2):self.cap(z,-1,q,q,rr,1)
  for t in b.GetTracks():self.mark(t)
  for z in b.Zones():
   if z.GetIsRuleArea():continue
   layer=z.GetLayer()
   if layer not in LAYS or z.GetNetname()=='/GND':continue
   pp=z.GetFilledPolysList(layer)
   for k in range(pp.OutlineCount()):
    self.poly(LAYS.index(layer),z.GetNetCode(),pp,k,.34,0);self.poly(LAYS.index(layer),z.GetNetCode(),pp,k,.56,1)
  # Sensitive routing exclusion beneath the two inductors; GND shield untouched.
  for r in ['L201','U201']:
   f=next(f for f in b.GetFootprints() if f.GetReference()==r);bb=f.GetBoundingBox(False,False)
   pts=[(p.ToMM(bb.GetX()),p.ToMM(bb.GetY())),(p.ToMM(bb.GetRight()),p.ToMM(bb.GetY())),(p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())),(p.ToMM(bb.GetX()),p.ToMM(bb.GetBottom()))]
   # In2/B are reserved below magnetics. F remains available for their own local force escapes.
   a=(c.c_double*8)(*[t for q in pts for t in q])
   for z in [1]:self.lib.polygon(z,-1,a,4,.3,0);self.lib.polygon(z,-1,a,4,.3,1)
 def cap(self,z,n,a,b,r,iv=0):self.lib.capsule(z,n,*a,*b,r,iv)
 def poly(self,z,n,pp,k,r,iv):
  chains=[pp.COutline(k)]+[pp.CHole(k,h) for h in range(pp.HoleCount(k))];pts=[];ends=[]
  for chain in chains:
   for j in range(chain.PointCount()):pts.extend(xy(chain.CPoint(j)))
   ends.append(len(pts)//2)
  ar=(c.c_double*len(pts))(*pts);en=(c.c_int*len(ends))(*ends)
  self.lib.polygon_holes(z,n,ar,en,len(ends),r,iv)
 def mark(self,t):
  n=t.GetNetCode();a=xy(t.GetStart());d=p.ToMM(t.GetWidth(p.F_Cu)) if isinstance(t,p.PCB_VIA) else p.ToMM(t.GetWidth())
  if isinstance(t,p.PCB_VIA):
   for z in range(2):
    self.cap(z,n,a,a,d/2+.34);self.cap(z,n,a,a,d/2+.56,1);self.cap(z,-1,a,a,.56,1)
   return
  if t.GetLayer() not in LAYS:return
  z=LAYS.index(t.GetLayer());bb=xy(t.GetEnd());self.cap(z,n,a,bb,d/2+.34);self.cap(z,n,a,bb,d/2+.56,1)
 def grid(self,pt):return round((pt[0]-X0)/S),round((pt[1]-Y0)/S)
 def point(self,g):return X0+g[0]*S,Y0+g[1]*S
 def route(self,n,a,b,za=0,zb=0,allowvia=True):
  ga=self.grid(a);gb=self.grid(b)
  cnt=self.lib.route(*ga,za,*gb,zb,n,int(allowvia),self.out,40000,900000)
  if cnt<=0:return False,cnt
  path=[tuple(self.out[3*i+j] for j in range(3)) for i in range(cnt)]
  # Collapse collinear grid runs only. Keep all bends and layer transitions.
  keep=[path[0]]
  for i in range(1,len(path)-1):
   prev=path[i-1];now=path[i];nxt=path[i+1]
   if tuple(now[j]-prev[j] for j in range(3))!=tuple(nxt[j]-now[j] for j in range(3)):keep.append(now)
  if len(path)>1:keep.append(path[-1])
  before=set(t.m_Uuid.AsString() for t in self.b.GetTracks())
  track(self.b,n,[a,self.point(keep[0])],.2,LAYS[za])
  for q,qq in zip(keep,keep[1:]):
   if q[2]==qq[2]:track(self.b,n,[self.point(q),self.point(qq)],.2,LAYS[q[2]])
   else:via(self.b,n,self.point(q))
  track(self.b,n,[self.point(keep[-1]),b],.2,LAYS[zb])
  for t in self.b.GetTracks():
   if t.m_Uuid.AsString() not in before:self.mark(t)
  return True,len(path)
 def ground(self):
  n=net(self.b,'GND').GetNetCode();fail=[]
  for i,q in enumerate(list(self.ps.values())):
   if q.GetNetCode()!=n or q.GetAttribute()!=p.PAD_ATTRIB_SMD or q.GetParentFootprint().GetReference()=='TP302':continue
   a=xy(q.GetPosition());x,y=self.grid(a)
   # Prefer adjacent vias instead of drilling every solder land.
   candidates=[]
   for rad in range(7,36,2):
    for dx in range(-rad,rad+1,2):
     for dy in [-rad,rad]:candidates.append((dx,dy));candidates.append((dy,dx))
   candidates.sort(key=lambda d:d[0]*d[0]+d[1]*d[1]);ok=False
   for dx,dy in candidates:
    if not self.lib.freecell(x+dx,y+dy,0,n,1):continue
    pt=self.point((x+dx,y+dy));done,cnt=self.route(n,a,pt,allowvia=False)
    if done:
     self.mark(via(self.b,n,pt));ok=True;break
   if not ok:fail.append([q.GetParentFootprint().GetReference(),q.GetNumber(),a])
  self.log.append({'ground_failed':fail});print('GND failures',len(fail),flush=True)
 def signals(self):
  ns=collections.defaultdict(list)
  for q in self.ps.values():
   if q.GetNetname().startswith('unconnected') or q.GetNetname() in ['/GND','/02_BUCK_5V/BUCK_SW']:continue
   
   ns[q.GetNetCode()].append(q)
  # Local small nets precede longer control buses; Kelvin nets precede all logic.
  def key(kv):
   nc,ls=kv;pts=[xy(q.GetPosition()) for q in ls]
   return (0 if self.classes.get(ls[0].GetNetname(),'Default')=='Sense' else 1,max((math.dist(a,b) for a in pts for b in pts),default=0))
  fail=[];success=0
  for nc,qs in sorted(ns.items(),key=key):
   pts=[xy(q.GetPosition()) for q in qs];connected={0};pending=set(range(1,len(qs)))
   while pending:
    candidates=sorted((math.dist(pts[i],pts[j]),i,j) for i in connected for j in pending)
    ok=False
    for d,i,j in candidates[:12]:
     done=False
     for za,zb in [(0,0),(1,0),(0,1),(1,1)]:
      if not qs[i].IsOnLayer(LAYS[za]) or not qs[j].IsOnLayer(LAYS[zb]):continue
      done,cnt=self.route(nc,pts[i],pts[j],za,zb)
      if done:break
     if done:connected.add(j);pending.remove(j);success+=1;ok=True;break
    if not ok:
     fail.append({'net':qs[0].GetNetname(),'remaining':[[qs[j].GetParentFootprint().GetReference(),qs[j].GetNumber(),pts[j]] for j in pending]});break
   print(qs[0].GetNetname(),len(qs),'left',len(pending),flush=True)
  self.log.append({'signal_success':success,'signal_failures':fail})
 def finish(self):
  self.b.BuildConnectivity();p.ZONE_FILLER(self.b).Fill(self.b.Zones())
  n=net(self.b,'GND').GetNetCode()
  ground=[z for z in self.b.Zones() if z.GetNetCode()==n]
  for x in range(12,89,4):
   for y in range(12,69,4):
    gx,gy=self.grid((x,y))
    if not self.lib.freecell(gx,gy,0,n,1):continue
    if all(any(z.GetLayer()==ly and z.HitTestFilledArea(ly,v(x,y)) for z in ground) for ly in LAYS):self.mark(via(self.b,n,(x,y)))
  self.b.BuildConnectivity();p.ZONE_FILLER(self.b).Fill(self.b.Zones());save(self.b)
  (EV/'ROUTER_LOG.json').write_text(json.dumps(self.log,indent=2)+'\n')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--ground-only',action='store_true');ap.add_argument('--signals-only',action='store_true');a=ap.parse_args()
 r=Router(load())
 if not a.signals_only:r.ground()
 if not a.ground_only:r.signals()
 r.finish()
