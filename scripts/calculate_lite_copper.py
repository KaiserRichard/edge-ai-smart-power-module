#!/usr/bin/env python3
"""Numerical DC copper estimate from extracted, filled board geometry. Not validation.
System Python uses already-installed NumPy/Pillow. Compile mesh solver to /tmp.
"""
import ctypes as c,json,math,argparse
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];EV=ROOT/'docs/evidence/v1a_lite/layout'
data=json.loads((EV/'COPPER_GEOMETRY.json').read_text());lib=c.CDLL('/tmp/lite-resistance.dylib')
I=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS');D=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
lib.solve.argtypes=[c.c_int,c.c_int,I,I,D,I,D,c.c_int,c.c_double,c.POINTER(c.c_int),c.POINTER(c.c_double)];lib.solve.restype=c.c_double
ap=argparse.ArgumentParser();ap.add_argument('--grid',type=float,default=.2);args=ap.parse_args();s=args.grid;W=int(80/s);H=int(60/s);origin=(10,10)
def pt(q):return ((q[0]-10)/s-.5,(q[1]-10)/s-.5)
def circle(draw,q,d,fill):
 x,y=pt(q);r=d/(2*s);draw.ellipse((x-r,y-r,x+r,y+r),fill=fill)
def polygon(im,poly):
 tmp=Image.new('1',(W,H));dd=ImageDraw.Draw(tmp);dd.polygon([pt(q) for q in poly['outer']],fill=1)
 for hole in poly['holes']:dd.polygon([pt(q) for q in hole],fill=0)
 im.paste(1,(0,0),tmp)
def mesh(name):
 a=data['nets'][name];ims=[Image.new('1',(W,H)) for _ in range(2)]
 for z in range(2):
  for poly in a['polys'][z]:polygon(ims[z],poly)
  dd=ImageDraw.Draw(ims[z])
  for t in a['tracks'][z]:
   dd.line([pt(t['a']),pt(t['b'])],fill=1,width=max(1,round(t['width']/s)));circle(dd,t['a'],t['width'],1);circle(dd,t['b'],t['width'],1)
  for q in a['barrels']:circle(dd,q['pos'],q['diameter'],1)
  for x,y,d in data['holes']:circle(dd,(x,y),d,0)
 mask=np.array([np.array(im,dtype=bool) for im in ims]);ids=np.full(mask.shape,-1,dtype=np.int32);ids[mask]=np.arange(mask.sum(),dtype=np.int32);n=int(mask.sum());ei=[];ej=[];gg=[]
 # rho=0.01724 ohm mm²/m, t=0.035 mm, all edges represent one square.
 conductance=.035/1.724e-5
 for ax in [1,2]:
  aa=[slice(None)]*3;bb=aa.copy();aa[ax]=slice(None,-1);bb[ax]=slice(1,None)
  ii=ids[tuple(aa)];jj=ids[tuple(bb)];ok=(ii>=0)&(jj>=0);ii=ii[ok];jj=jj[ok];ei.extend(ii.tolist());ej.extend(jj.tolist());gg.extend([conductance]*len(ii))
 # Tie four annular locations across layers; barrel g shared, not quadrupled.
 for q in a['barrels']:
  x,y=q['pos'];r=(q['diameter']+q['drill'])/4;links=set()
  for angle in np.linspace(0,2*math.pi,16,endpoint=False):
   xx=int((x+r*math.cos(angle)-10)/s);yy=int((y+r*math.sin(angle)-10)/s)
   if 0<=xx<W and 0<=yy<H and ids[0,yy,xx]>=0 and ids[1,yy,xx]>=0:links.add((ids[0,yy,xx],ids[1,yy,xx]))
  if not links:continue
  g=math.pi*q['drill']*.018/(1.724e-5*1.6)
  for i,j in links:ei.append(i);ej.append(j);gg.append(g/len(links))
 return ids,np.array(ei,np.int32),np.array(ej,np.int32),np.array(gg,np.float64),n
cache={}
def run(name,src,dst):
 if name not in cache:cache[name]=mesh(name)
 ids,ei,ej,g,n=cache[name];fixed=np.zeros(n,np.int32)
 for refs,value in [(dst,-1),(src,1)]:
  im=Image.new('1',(W,H))
  for ref in refs:
   for poly in data['pads'][ref]['polys']:polygon(im,poly)
  sel=np.array(im,bool)
  for z in range(2):
   # SMD contacts only on front; THT source/sink include the actual barrel.
   use=sel if z==0 else sel & any(data['pads'][ref]['drill'][0]>0 for ref in refs)
   q=ids[z][use];q=q[q>=0];fixed[q]=value
 assert np.any(fixed==1) and np.any(fixed==-1),(name,src,dst)
 out=np.zeros(n,np.float64);it=c.c_int();res=c.c_double()
 current=lib.solve(n,len(ei),ei,ej,g,fixed,out,15000,1e-10,c.byref(it),c.byref(res))
 result={'net':name,'source_pads':src,'sink_pads':dst,'ohms_20C':1/current,'ohms_85C':(1+.00393*65)/current,'nodes':n,'iterations':it.value,'relative_residual':res.value}
 print(result,flush=True);return result
# Separate net solutions keep F301 component resistance outside copper results.
results={}
for r in ['C209','C214']:
 results[r+'_positive_raw']=run('/VOUT_5V1',[r+'.1'],['F301.1'])
 results[r+'_return']=run('/GND',[r+'.2'],['J502.2'])
results['pi_positive']=run('/VOUT_PI',['F301.2'],['J502.1'])
results['inductor_to_fuse']=run('/VOUT_5V1',['L201.2'],['F301.1'])
report={'geometry_board_sha256':data['sha256'],'grid_mm':s,'copper_um':35,'barrel_plating_um_assumed':18,'temperature_coefficient_per_K':.00393,'method':'2-layer resistor mesh of filled zones + pads + tracks; vias/PTH barrels 1.6mm long, 18um plating. Contacts equipotential. Raster approximation, no thermal or fault validation.','results':results}
for r in ['C209','C214']:
 rr=results[r+'_positive_raw']['ohms_20C']+results[r+'_return']['ohms_20C']+results['pi_positive']['ohms_20C'];report[r+'_round_trip_ohms_20C']=rr;report[r+'_round_trip_ohms_85C']=rr*(1+.00393*65)
(EV/('COPPER_RESISTANCE_'+str(s)+'.json')).write_text(json.dumps(report,indent=2)+'\n')
