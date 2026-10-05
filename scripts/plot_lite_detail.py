#!/usr/bin/env python3
"""Plot extracted copper: input JSON, output PNG, x1 x2 y1 y2, optional layer index."""
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
j=json.load(open(sys.argv[1]));x1,x2,y1,y2=map(float,sys.argv[3:7]);ly=int(sys.argv[7]) if len(sys.argv)>7 else 0
fig,ax=plt.subplots(figsize=(12,10))
colors={'/GND':'#d6ded6','/VIN_PROTECTED':'#efbb88','/VOUT_5V1':'#d5b3db','/02_BUCK_5V/BUCK_SW':'#f5d36e'}
for n,d in j['nets'].items():
 c=colors.get(n,'#88b4d4')
 for q in d['polys'][ly]:
  ax.add_patch(Polygon(q['outer'],fc=c,ec=c,lw=.3))
  for h in q['holes']:ax.add_patch(Polygon(h,fc='white',ec='white'))
 for t in d['tracks'][ly]:ax.plot(*zip(t['a'],t['b']),color=c,lw=t['width']*12)
 for q in d['barrels']:ax.add_patch(plt.Circle(q['pos'],q['diameter']/2,color=c));ax.add_patch(plt.Circle(q['pos'],q['drill']/2,color='white'))
for r,q in j['pads'].items():
 if not any(p in j['nets'][q['net']]['polys'][ly] for p in q['polys']):continue
 x,y=q['pos']
 if x1<x<x2 and y1<y<y2:
  for poly in q['polys']:
   ax.add_patch(Polygon(poly['outer'],fill=False,ec='black',lw=.8))
  ax.text(x,y,r,fontsize=7,ha='center',va='center',color='black')
ax.set(xlim=(x1,x2),ylim=(y2,y1),aspect='equal');ax.grid(alpha=.3);fig.savefig(sys.argv[2],dpi=150,bbox_inches='tight')
