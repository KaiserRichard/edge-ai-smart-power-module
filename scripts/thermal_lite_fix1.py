#!/usr/bin/env python3
"""ASSUMED 2-mm four-sheet coupled thermal screen, not a validated CFD model.
Uses final filled copper geometry. NumPy/Pillow only. No manufacturer PCB copied.
"""
import json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];EV=ROOT/'docs/evidence/v1a_lite/fix1'
d=json.loads((EV/'COPPER_GEOMETRY.json').read_text())
S=2.;W=40;H=30;N=4*W*H;ids=np.arange(N).reshape(4,H,W)
ims=[Image.new('1',(800,600)) for _ in range(4)]
def pt(q):return ((q[0]-10)*10,(q[1]-10)*10)
for net in d['nets'].values():
 for z in range(4):
  for poly in net['polys'][z]:
   tmp=Image.new('1',(800,600));dr=ImageDraw.Draw(tmp);dr.polygon([pt(q) for q in poly['outer']],fill=1)
   for hole in poly['holes']:dr.polygon([pt(q) for q in hole],fill=0)
   ims[z].paste(1,(0,0),tmp)
  dr=ImageDraw.Draw(ims[z])
  for t in net['tracks'][z]:dr.line([pt(t['a']),pt(t['b'])],fill=1,width=max(1,round(t['width']*10)))
frac=np.array([np.array(im,dtype=float).reshape(H,20,W,20).mean(axis=(1,3)) for im in ims])
# Parallel sheet conductivity: copper plus allocated FR4 thickness. Coarse-grid
# homogenization can overstate spreading across small etched gaps: sensitivity only.
sheet=400*frac*np.array(d['thickness_mm'])[:,None,None]*1e-3+.3*.0016/4
ei=[];ej=[];gg=[]
def edge(i,j,g):ei.extend(np.ravel(i).tolist());ej.extend(np.ravel(j).tolist());gg.extend(np.ravel(g).tolist())
for ax in [1,2]:
 a=[slice(None)]*3;b=a.copy();a[ax]=slice(None,-1);b[ax]=slice(1,None)
 ka=sheet[tuple(a)];kb=sheet[tuple(b)];edge(ids[tuple(a)],ids[tuple(b)],2*ka*kb/(ka+kb))
for z in range(3):
 length=(d['z_mm'][z+1]-d['z_mm'][z])*1e-3
 edge(ids[z],ids[z+1],np.full((H,W),.3*(S*1e-3)**2/length))
 seen=set()
 for net in d['nets'].values():
  for q in net['barrels']:
   x,y=q['pos'];key=(x,y,q['drill'])
   if key in seen:continue
   seen.add(key);xx=int((x-10)/S);yy=int((y-10)/S)
   if not(0<=xx<W and 0<=yy<H):continue
   edge([ids[z,yy,xx]],[ids[z+1,yy,xx]],[400*math.pi*q['drill']*.018*1e-6/length])
ei=np.array(ei);ej=np.array(ej);gg=np.array(gg)
def source(ref,pins):
 cells=[]
 for pin in pins:
  x,y=d['pads'][ref+'.'+pin]['pos'];cells.append(ids[0,int((y-10)/S),int((x-10)/S)])
 return np.unique(cells)
src=[source('Q101',['2']),source('Q102',['2']),source('U201',['8','9','11','12'])]
def solve(power,h):
 convection=np.zeros((4,H,W));convection[[0,3]]=h*(S*1e-3)**2;convection=convection.ravel()
 diag=np.bincount(ei,weights=gg,minlength=N)+np.bincount(ej,weights=gg,minlength=N)+convection
 rhs=np.zeros(N)
 for cells,power_i in zip(src,power):rhs[cells]+=power_i/len(cells)
 def mv(x):
  flux=gg*(x[ei]-x[ej]);return convection*x+np.bincount(ei,weights=flux,minlength=N)-np.bincount(ej,weights=flux,minlength=N)
 x=np.zeros(N);r=rhs.copy();z=r/diag;p=z.copy();rz=np.dot(r,z)
 for it in range(10000):
  ap=mv(p);alpha=rz/np.dot(p,ap);x+=alpha*p;r-=alpha*ap
  if np.linalg.norm(r)<1e-9:break
  z=r/diag;rn=np.dot(r,z);p=z+(rn/rz)*p;rz=rn
 return x,it,float(np.linalg.norm(r))
I_simple=(1+100/24.6)*5/(18*.9)
Rhot=.58;Pout=(1+100/24.6)*5
I_coupled=(18-math.sqrt(18**2-8*Rhot*Pout/.9))/(4*Rhot)
report={'classification':'CALCULATED using ASSUMED thermal boundary conditions; NOT VALIDATED',
 'board_sha256':d['sha256'],'grid_mm':S,'copper_W_mK':400,'FR4_W_mK':.3,
 'ambient_C_assumed':50,'combined_convection_radiation_W_m2K_assumed':[5,10,15],
 'barrel_plating_mm_assumed':.018,'package_series_K_W_assumed':[1.4,1.4,19.2],
 'limitations':['2mm cells homogenize small gaps; no calibrated anisotropic laminate/package/enclosure model',
 'All package heat injected into board; package top/air paths omitted',
 'U201 RthetaJB=19.2 is a JEDEC characterization, used as sensitivity proxy only',
 '50C ambient and 110C junction screen are historical assumptions, not approved requirements',
 'RDS(on) 0.58 ohm applies at 150C and -10V gate; not an upper bound above 150C',
 'Other resistor/inductor/fuse heat omitted; computed temperatures are not release limits'],
 'input_current_A_at_buck_18V':I_simple,'fet_loss_W_25C_at_buck_18V':I_simple**2*.295,
 'fet_loss_W_150C_at_buck_18V':I_simple**2*.58,'input_current_A_at_module_18V':I_coupled,
 'coupled_fet_loss_W_each':I_coupled**2*.58,'U201_loss_W_screen':2.417,'scenarios':[]}
for h in [5,10,15]:
 power=[I_coupled**2*.58]*2+[2.417];x,it,res=solve(power,h)
 board=[float(x[c].mean()) for c in src];tj=[50+t+p*r for t,p,r in zip(board,power,[1.4,1.4,19.2])]
 matrix=[]
 for k in range(3):
  pu=[0.,0.,0.];pu[k]=1.;tx,_,_=solve(pu,h);matrix.append([float(tx[c].mean()) for c in src])
 report['scenarios'].append({'h':h,'power_W':power,'board_rise_K':board,'junction_C_estimate':tj,'source_to_board_K_W_columns':matrix,'iterations':it,'residual_W':res,'screen_110C':['PASS' if t<=110 else 'FAIL' for t in tj]})
(EV/'THERMAL_SCREEN.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
