#!/usr/bin/env python3
"""Conditional bulk-strap heat balance, not an installed connector rating."""
import json
import math
from pathlib import Path
HERE = Path(__file__).resolve().parent
# KME C11000_Cu-ETP_10_2020 typical annealed material, p1; see drawing.
rho20 = 1 / 58e6
alpha = .0037
length, width, thickness, hole = .030, .015, .002, .0045
neck = (width-hole)*thickness
ambient, rise = 40, 20
r60 = rho20 * (1+alpha*(ambient+rise-20)) * length / neck
joint = .0002  # ASSUMED each joint meets the existing <=0.2 milliohm allocation.
area = length*width - 2*math.pi*(.009/2)**2  # Only unoccluded top face.
h = 5  # ASSUMED W/m2/K natural convection; no radiation/end-conduction credit.
i_screen = math.sqrt(h*area*rise/(r60+2*joint))
volume = (length*width - 2*math.pi*(hole/2)**2)*thickness
mass = volume*8920
heat_capacity = mass*394
x = dict(classification='CALCULATED under ASSUMED boundary conditions; installed rating OPEN',
    access_date='2026-10-04',material_url='https://www.kme.com/fileadmin/DOWNLOADCENTER/COPPER%20DIVISON/4%20Industrial%20Rolled/3_Datasheets/Datasheets_NEW_2021/Cu-ETP_01_2021_e.pdf',
    material_revision='C11000_Cu-ETP_10_2020 p1; typical annealed values',
    assumptions=dict(ambient_C=ambient,temperature_rise_K=rise,h_W_m2K=h,each_joint_ohm=joint,
        length_m=length,width_m=width,thickness_m=thickness,hole_diameter_m=hole,
        neglected='radiation, PCB/end heat transfer; lumped uniform temperature is unvalidated'),
    full_cross_section_mm2=width*thickness*1e6,neck_cross_section_mm2=neck*1e6,
    rho20_ohm_m=rho20,r60_bulk_ohm=r60,r60_with_joints_ohm=r60+2*joint,
    exposed_top_area_m2=area,mass_kg=mass,heat_capacity_J_K=heat_capacity,
    continuous_screen_A=i_screen,rounded_screen_A=8,
    at_5A=dict(loss_W=25*(r60+2*joint),drop_V=5*(r60+2*joint),rise_K=25*(r60+2*joint)/(h*area)),
    at_100A_20us=dict(bulk_energy_J=100**2*r60*20e-6,each_joint_energy_J=100**2*joint*20e-6,
        bulk_adiabatic_rise_K=100**2*r60*20e-6/heat_capacity),
    protected_dump_resistive_screen_A=5.5/(.033*(1-.01-50e-6*70)),
    raw_dump_resistive_screen_A=7.5068472719058335/(.099*(1-.01-50e-6*70)),
    limitations='Pulse currents are conditional V/R screens only. Peak, duration, reversal, joint hot spots and repetition remain OPEN. Never infer a 100A installed rating.')
assert 8 < i_screen < 9
assert 20 < x['neck_cross_section_mm2'] < 22
(HERE/'FORCE_LINK_CALCULATIONS.json').write_text(json.dumps(x,indent=2)+'\n')
print(json.dumps(x,indent=2))
