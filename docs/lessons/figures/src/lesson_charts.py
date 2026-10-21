#!/usr/bin/env python3
"""Exact numerical teaching charts; never circuit/concept illustrations.

Extends the pilot's plotting style. All new trajectories below are explicitly
assumed teaching examples, not fitted hardware models. The fault trajectories
remain exclusively in the unchanged pilot fault_model.py.
Run: python3 -B docs/lessons/figures/src/lesson_charts.py [00|01|02|04|05|06|07|08|all]
"""
import argparse
import numpy as np
from make_figures import plt, OUT, C_SRC, C_RAW, C_PROT, C_FAULT, C_OK, C_CTRL, stamp


def finish(fig, name, premise):
    fig.tight_layout(rect=(0, .065, 1, .97))
    stamp(fig, premise + "\nCALCULATED teaching chart · NOT MEASURED · NOT FOR FABRICATION")
    fig.savefig(OUT / name)
    plt.close(fig)


def overview():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    values = [25.5 / .9, 25.5, 25.5 / .9 - 25.5]
    bars = ax.bar(["V1A input", "Local buck output", "Loss before that output"], values,
                  color=[C_SRC, C_RAW, C_FAULT], width=.6)
    ax.bar_label(bars, labels=[f"{v:.2f} W" for v in values], padding=6)
    ax.set(ylabel="Power (W)", ylim=(0, 34), title="Same power journey: output power plus heat equals input power")
    ax.grid(axis="x", visible=False)
    finish(fig, "v2-00-power-accounting.png", "ASSUMED 5.1 V × 5 A local output; 90% efficiency to that node; downstream losses excluded")


def input_protection():
    fig, ax = plt.subplots(figsize=(11, 6))
    # Interpolated curve is not manufacturer characterization or a guaranteed envelope.
    v = np.array([0, 26, 36, 40, 42.1, 48, 58.1])
    current = np.array([0, 0, .000001, .0001, .001, 9.5, 25.9])
    ax.plot(v, current, lw=2.5, color=C_SRC, label="ASSUMED curve shape (positive polarity only)")
    ax.axvspan(9, 26, color=C_OK, alpha=.12, label="V1A normal-input requirement: 9–26 V")
    ax.axvspan(40, 44.2, color=C_RAW, alpha=.12, label="Breakdown range at 1 mA: 40.0–44.2 V")
    ax.axvline(36, color=C_CTRL, ls="--")
    ax.annotate("Standoff = 36 V\nnot the clamp voltage", (36, 0), (21, 9),
                arrowprops={"arrowstyle": "->"}, color=C_CTRL)
    ax.scatter([58.1], [25.9], color=C_FAULT, zorder=5)
    ax.annotate("Specified clamp point\n58.1 V at 25.9 A", (58.1, 25.9), (41, 21),
                arrowprops={"arrowstyle": "->"}, color=C_FAULT)
    ax.set(xlabel="TVS voltage magnitude (V)", ylabel="TVS current magnitude (A)",
           xlim=(0, 63), ylim=(-1, 30), title="SMCJ36CA: three voltage labels describe three different conditions")
    ax.legend(loc="upper left", fontsize=9)
    finish(fig, "v2-01-tvs-iv.png", "DATASHEET anchors: Littelfuse SMCJ, 2025-02-27 v.2; 25°C, specified 10/1000 µs pulse. Curve between anchors ASSUMED; hot limit OPEN")

    fig, (a, b) = plt.subplots(2, 1, figsize=(11, 6.5), gridspec_kw={"height_ratios": [1, 1.6]})
    a.axvspan(9, 26, color=C_OK, alpha=.18)
    a.axvline(8.46, color=C_CTRL, lw=2)
    a.axvline(27.63038, color=C_FAULT, lw=2)
    a.text(17.5, .5, "Normal input REQUIRED: 9–26 V", ha="center", fontsize=12)
    a.text(8.1, .8, "UVLO rising\n8.46 V nominal", ha="right", color=C_CTRL)
    a.text(28, .8, "OVP rising\n27.63 V nominal", ha="left", color=C_FAULT)
    a.set(xlim=(5, 32), ylim=(0, 1.5), yticks=[], xlabel="Input voltage (V)", title="Admission thresholds are not the normal operating specification")
    b.barh([2, 1, 0], [1, 28.289211-26.973873, 26.58-25], left=[25, 26.973873, 25],
           height=.46, color=[C_OK, C_FAULT, C_RAW], alpha=.65)
    b.set(yticks=[2, 1, 0], yticklabels=["Normal ceiling (last 1 V)", "Rising OVP screen", "Falling / reset screen"],
          xlabel="Input voltage (V)", xlim=(24.6, 28.8), ylim=(-.6, 2.6))
    b.axvline(26, color=C_OK, ls="--"); b.axvline(27, color=C_FAULT, ls=":")
    b.text(26.97, 1.32, "26.97–28.29 V", color=C_FAULT)
    b.text(25, .32, "25.00–26.58 V", color=C_RAW)
    b.text(27.05, 2, "27 V fault test:\ntrip not guaranteed", va="center", fontsize=10)
    finish(fig, "v2-01-efuse-window.png", "PRELIMINARY nominal / initial-tolerance screens from IN + Gate2c; hot thresholds and restart behaviour OPEN")

    fig, ax = plt.subplots(figsize=(10, 5))
    vin = np.linspace(9, 26, 200); iin = 25.5 / (.9 * vin)
    ax.plot(vin, iin, color=C_SRC, lw=3)
    for value in (9, 24, 26):
        y = 25.5 / (.9 * value)
        ax.plot(value, y, "o", color=C_SRC)
        ax.annotate(f"{value} V: {y:.2f} A", (value, y), xytext=(0, 12), textcoords="offset points", ha="center")
    ax.axhline(4.48, color=C_FAULT, ls="--", label="Baseline nominal input limit ≈ 4.48 A")
    ax.set(xlabel="Buck input voltage (V)", ylabel="Average input current (A)", xlim=(8, 27), ylim=(0, 5),
           title="A 5 A output does not require 5 A at a higher-voltage input")
    ax.legend(loc="upper right")
    finish(fig, "v2-01-input-current.png", "ASSUMED 25.5 W output and 90% constant efficiency; ignores upstream path/aux losses and startup")


def buck():
    vin, vo, fs, inductance, average = 24., 5.1, 400e3, 10e-6, 5.
    period = 1/fs; duty = vo/vin; ton = duty*period
    ripple = (vin-vo)*ton/inductance
    t = np.linspace(0, 3*period, 2401); phase = np.mod(t, period)
    on = phase < ton
    il = np.where(on, average-ripple/2+(vin-vo)*phase/inductance,
                  average+ripple/2-vo*(phase-ton)/inductance)
    fig, axs = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
    for a in axs:
        for k in range(3): a.axvspan(k*period*1e6, (k*period+ton)*1e6, color=C_RAW, alpha=.09)
    axs[0].step(t*1e6, np.where(on, vin, 0), color=C_SRC, where="post", lw=2)
    axs[0].set(ylabel="SW voltage (V)", yticks=[0, 24], ylim=(-2, 28), title="High side ON in the shaded interval; low side ON during the remainder")
    axs[1].plot(t*1e6, il, color=C_RAW, lw=2.5)
    axs[1].axhline(average, color="grey", ls="--")
    axs[1].set(ylabel="Inductor current (A)", ylim=(4.3, 5.7), title=f"Current rises then falls, staying positive: ripple = {ripple:.3f} A peak-to-peak")
    axs[2].plot(t*1e6, il-average, color=C_PROT, lw=2.5)
    axs[2].axhline(0, color="grey", ls="--")
    axs[2].set(ylabel="Capacitor current (A)", xlabel="Time (µs)", title="Capacitor charges above zero and supplies the difference below zero")
    finish(fig, "v2-02-buck-waveforms.png", "ASSUMED ideal continuous conduction: 24 V → 5.1 V, 5 A, 400 kHz, constant 10 µH; no dead time, losses or saturation")

    fig, ax = plt.subplots(figsize=(10, 5))
    vin = np.linspace(9, 26, 250)
    for l, col in [(6.8e-6, C_SRC), (10e-6, C_RAW)]:
        ripple = 5.1*(1-5.1/vin)/(400e3*l)
        ax.plot(vin, ripple, lw=2.8, color=col, label=f"{l*1e6:g} µH, assumed constant")
    ax.set(xlabel="Buck input voltage (V)", ylabel="Inductor ripple, peak-to-peak (A)",
           title="Larger inductance lowers normal ripple; this says nothing about saturation")
    ax.legend()
    finish(fig, "v2-02-inductor-ripple.png", "ASSUMED ideal CCM: 5.1 V, 400 kHz; nominal L only. Candidate hot/current-dependent inductance and regulation OPEN")


def monitoring():
    i = np.linspace(0, 5, 150)
    fig, (a,b) = plt.subplots(1,2,figsize=(11,4.7))
    a.plot(i, i*.002*1000, color=C_CTRL, lw=3)
    a.plot(i, i*.003*1000, color=C_FAULT, ls="--", lw=2, label="If 1 mΩ unwanted copper is included")
    a.set(xlabel="Actual load current (A)", ylabel="Sensed drop (mV)", title="Correct Kelvin signal is 10 mV at 5 A")
    a.legend(fontsize=8.5)
    b.plot(i, i*i*.002*1000, color=C_RAW, lw=3)
    b.set(xlabel="Load current (A)", ylabel="Shunt dissipation (mW)", title="Nominal shunt heating is 50 mW at 5 A")
    finish(fig, "v2-04-shunt-signal-loss.png", "CALCULATED 2 mΩ nominal shunt; extra 1 mΩ is an ASSUMED routing-error example, not a board measurement")

    fig, (a,b) = plt.subplots(2,1,figsize=(10,6.5),sharex=True)
    t=np.linspace(0,60,601)
    power=np.full_like(t,10.0); observed=power.copy(); observed[(t>=25)&(t<35)]=np.nan
    a.plot(t,observed,color=C_CTRL,lw=3)
    a.set(ylabel="Branch power (W)", ylim=(0,14), title="No reading during a reset gap does not mean zero power")
    true_energy=power*t
    accumulator=np.where(t<25,10*t,np.where(t>=35,10*(t-35),np.nan))
    b.plot(t,true_energy,color="grey",ls="--",label="Hypothetical true cumulative energy")
    b.plot(t,accumulator,color=C_PROT,lw=3,label="Device accumulator with power loss/reset")
    b.set(xlabel="Time (s)",ylabel="Energy (J)",ylim=(0,650))
    for ax in (a,b): ax.axvspan(25,35,color=C_FAULT,alpha=.13)
    b.legend(loc="upper left",fontsize=9)
    finish(fig, "v2-04-energy-reset-gap.png", "ASSUMED 10 W for 60 s; monitor unavailable at 25–35 s while load remains powered externally; illustrative reset, not measured")


def gpio():
    # Extend the pilot drop-budget convention to show nominal 5.1 V through the lower limit.
    fig, ax=plt.subplots(figsize=(11,6))
    nominal=5.1; minimum=5.026143; resistive=5*.042672857
    steps=[("Regulation\nallowance",nominal-minimum), ("Complete hot loop\n42.673 mΩ",resistive), ("Dynamic trough\nASSUMED",.020)]
    ax.bar(0, nominal-4.65, bottom=4.65, color=C_RAW)
    ax.text(0,nominal+.012,"5.100 V",ha="center")
    v=nominal
    for x,(label,drop) in enumerate(steps,1):
        ax.bar(x,drop,bottom=v-drop,color=C_FAULT,alpha=.75)
        ax.text(x,v+.012,f"−{drop*1000:.1f} mV",ha="center")
        v-=drop
    ax.bar(4,v-4.65,bottom=4.65,color=C_PROT)
    ax.text(4,v+.012,f"{v:.3f} V\n{(v-4.75)*1000:.1f} mV reserve",ha="center")
    ax.axhline(4.75,color="black",ls="--",label="Project loaded minimum 4.75 V")
    ax.axhline(v-.080,color=C_FAULT,ls=":",label="100 mV trough instead: 4.713 V (fails screen)")
    ax.set(xticks=range(5),xticklabels=["Nominal local\nbuck output"]+[x[0] for x in steps]+["Far end\nat 5 A"],
           ylabel="Voltage (V)",ylim=(4.65,5.18),title="The 5.10 V → 4.75 V budget is only 350 mV")
    ax.legend(loc="upper right",fontsize=9)
    finish(fig,"v2-05-full-drop-budget.png","PRELIMINARY Gate4a allocation, retained BSC034 pair; J502 hot resistance and Pi contacts unqualified")

    fig,(a,b)=plt.subplots(1,2,figsize=(11,5))
    x=np.arange(3); w=.34
    a.bar(x-w/2,[2.5,3.,5.],w,color=C_RAW,label="Positive pin 2")
    a.bar(x+w/2,[2.5,2.,0.],w,color=C_PROT,label="Positive pin 4")
    a.axhline(3,color=C_FAULT,ls="--",label="Cited 3 A contact test rating")
    a.set(xticks=x,xticklabels=["20 / 20 mΩ","20 / 30 mΩ","One open"],ylabel="Contact current (A)",ylim=(0,5.8),title="5 A shares by conductance, not pin count")
    a.legend(fontsize=8.5,loc="upper left")
    labels=["20 mΩ each\n(target)","30 mΩ each\n(conditioned allowance)"]
    drops=np.array([20,30])*(1/2+1/8)*5
    bars=b.bar(labels,drops,color=[C_CTRL,C_FAULT],width=.5);b.bar_label(bars,fmt="%.2f mV",padding=4)
    b.set(ylabel="Pi contact-bank drop at 5 A (mV)",ylim=(0,120),title="Two positives + eight grounds")
    finish(fig,"v2-05-contact-sharing.png","ASSUMED equal branch voltages; contact-only examples exclude wire/crimp variation. 3 A is not a qualified hot Pi-mate rating")


def pcb():
    fig,ax=plt.subplots(figsize=(10,5))
    di=np.linspace(0,1,200)
    for inductance,col in [(2,C_CTRL),(10,C_FAULT)]:
        ax.plot(di,inductance*di,lw=3,color=col,label=f"ASSUMED stray L = {inductance} nH")
    ax.set(xlabel="Current slew rate (A/ns)",ylabel="Inductive voltage magnitude (V)",title="A small stray inductance matters when current changes quickly")
    ax.legend()
    finish(fig,"v2-06-stray-inductance.png","ASSUMED 2 / 10 nH examples; V = L × di/dt. No geometry-to-inductance or actual switching slew is claimed")

    fig,axs=plt.subplots(1,2,figsize=(11,4.8)); current=np.linspace(0,5,200)
    for r,col in [(.002,C_CTRL),(.0136,C_FAULT)]:
        axs[0].plot(current,current*r*1000,color=col,lw=3,label=f"{r*1000:g} mΩ")
        axs[1].plot(current,current**2*r,color=col,lw=3,label=f"{r*1000:g} mΩ")
    axs[0].set(xlabel="Current (A)",ylabel="Voltage drop (mV)",title="Voltage loss grows in proportion to current")
    axs[1].set(xlabel="Current (A)",ylabel="Dissipation (W)",title="Heat grows as current squared")
    for ax in axs:ax.legend()
    finish(fig,"v2-06-copper-loss.png","CALCULATED at fixed R: 2 mΩ shunt nominal / 13.6 mΩ preliminary hot series-pair allocation; temperature rise OPEN")


def bench():
    fig, (a,b)=plt.subplots(1,2,figsize=(11,5.8))
    peaks=np.array([5.470,5.490]); mins=np.array([4.780,4.760])
    for ax,vals,limit,title in [(a,peaks,5.5,"Fault peak: upper uncertainty must stay below 5.5 V"),(b,mins,4.75,"Normal 5 A: lower uncertainty must reach 4.75 V")]:
        ax.errorbar([0,1],vals,yerr=.015,fmt="o",capsize=10,color=C_PROT,ms=8,lw=2)
        ax.axhline(limit,color=C_FAULT,ls="--")
        ax.set(xticks=[0,1],xticklabels=["Example A","Example B"],xlim=(-.6,1.6),ylabel="Far-end voltage (V)",title=title)
    a.set_ylim(5.44,5.53);b.set_ylim(4.72,4.82)
    finish(fig,"v2-07-measurement-uncertainty.png","ASSUMED example readings with ±15 mV expanded acceptance allowance; no actual instrument calibration or measured trace")

    fig,(a,b)=plt.subplots(2,1,figsize=(10,6.5),sharex=True)
    t=np.linspace(0,2000,2001) # us
    current=np.where(t<=10,10.,.01)
    # Analytic area; late 10 mA is a pedagogical tail, not an acceptable autonomous cutoff claim.
    charge=10*np.minimum(t,10)+.01*np.maximum(t-10,0)
    a.plot(t,current,color=C_SRC,lw=2);a.set(ylabel="Source current (A)",title="Whole-event integration includes small late tails")
    inset=a.inset_axes([.43,.35,.5,.5]);inset.plot(t,current,color=C_FAULT);inset.set(xlim=(20,2000),ylim=(0,.015),ylabel="Current (A)",xlabel="Time (µs)");inset.tick_params(labelsize=8)
    b.plot(t,charge,color=C_RAW,lw=2.5);b.axhline(100,color=C_FAULT,ls="--",label="Proposed positive-charge ceiling 100 µC")
    b.set(xlabel="Time after physical fault onset (µs)",ylabel="Positive charge (µC)",ylim=(0,130));b.legend()
    finish(fig,"v2-07-source-charge-tail.png","ASSUMED 10 A for 10 µs + 10 mA until 2 ms: 119.9 µC before uncertainty. Source contract remains unproved")


def robot():
    fig,ax=plt.subplots(figsize=(10,5.7))
    efficiency=np.linspace(.8,.98,200)
    power=25.5/efficiency
    ax.plot(efficiency*100,power,color=C_SRC,lw=3)
    ax.plot(90,25.5/.9,"o",color=C_FAULT)
    ax.annotate("90% assumed: 28.33 W\n1.18 A at 24 V",(90,25.5/.9),(91,30.3),arrowprops={"arrowstyle":"->"})
    ax.set(xlabel="ASSUMED efficiency to local buck output (%)",ylabel="Required V1A input power (W)",title="The upstream module must supply output power plus V1A losses")
    finish(fig,"v2-08-input-power-budget.png","ASSUMED 5.1 V × 5 A local target, no extra auxiliary load. Efficiency sweep is a sensitivity, not V1A characterization")

    fig,ax=plt.subplots(figsize=(10,5.5))
    labels=["24 V label", "+ tolerance", "+ ripple peak", "+ startup peak"]
    v=24; ax.bar(0,v-23,bottom=23,color=C_SRC)
    for x,d in enumerate([.48,.2,.15],1):
        ax.bar(x,d,bottom=v,color=C_RAW);ax.text(x,v+d+.05,f"+{d:.2f} V",ha="center");v+=d
    ax.bar(4,v-23,bottom=23,color=C_PROT);ax.text(4,v+.05,f"{v:.2f} V",ha="center")
    ax.axhline(26,color=C_OK,ls="--",label="V1A normal-input ceiling 26 V")
    ax.set(xticks=range(5),xticklabels=labels+["Illustrative peak"],ylim=(23,26.6),ylabel="Source output voltage (V)",title="A nominal voltage label leaves several unknown allowances")
    ax.legend()
    finish(fig,"v2-08-source-voltage-envelope.png","ASSUMED example: +2% DC, +0.20 V positive ripple, +0.15 V startup. Not a selected module specification; no double counting")


GENERATORS={"00":overview,"01":input_protection,"02":buck,"04":monitoring,"05":gpio,"06":pcb,"07":bench,"08":robot}

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson",choices=[*GENERATORS,"all"],nargs="?",default="all")
    args=parser.parse_args()
    for key,fn in GENERATORS.items():
        if args.lesson in (key,"all"):
            fn();print(f"Lesson {key}: charts generated.")
