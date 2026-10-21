#!/usr/bin/env python3
"""Pilot chart code adapted from 6c4aa6e; concepts are owner-generated images.
Run from any directory: python3 -B docs/lessons/figures/src/make_figures.py
Only charts, axes and waveforms are generated. See ../../VISUAL_REBUILD_LOG.md.
"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/v1a-lessons-matplotlib")
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import fault_model as fm
OUT = Path(__file__).resolve().parent.parent
OUT.mkdir(exist_ok=True)
C_SRC, C_RAW, C_PROT, C_FAULT, C_OK, C_GREY, C_CTRL = "#6741D9", "#E8590C", "#1971C2", "#C92A2A", "#2F9E44", "#868E96", "#0C8599"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
 "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25,
 "savefig.dpi": 160, "savefig.bbox": "tight", "figure.facecolor": "white"})
STAMP = "ASSUMED / CALCULATED teaching chart · not measured · NOT FOR FABRICATION"

def stamp(fig, text=STAMP):
    fig.text(0.99, 0.005, text, ha="right", va="bottom", fontsize=8, color=C_GREY)


def f3_energy():
    items = [("New energy from the source\nper fault at 24 V (Gate 4a screen)", 11.424, C_SRC),
             ("Input bank 30 µF at 24 V", 8.64, C_SRC),
             ("L201 at 8 A (12 µH upper)", 0.384, C_SRC),
             ("Raw bank at 5.5 V (upper C)", 84.648, C_RAW),
             ("Protected bank at 5.5 V (upper C)", 40.946, C_PROT),
             ("Dummy-load capacitor 2.2 mF at 5.5 V", 33.275, C_GREY)]
    fig, ax = plt.subplots(figsize=(11, 5))
    y = np.arange(len(items))[::-1]
    for yi, (lab, e, c) in zip(y, items):
        ax.barh(yi, e, color=c, height=0.62)
        ax.text(e + 1, yi, f"{e:.1f} mJ" if e > 1 else f"{e:.2f} mJ", va="center", fontsize=11, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([i[0] for i in items]); ax.set_xlabel("Energy (millijoules, mJ)")
    ax.set_xlim(0, 100); ax.grid(axis="y", visible=False)
    ax.set_title("Where the fault energy hides: E = ½CV² and E = ½LI²", fontsize=14, fontweight="bold", loc="left")
    ax.text(99, 4.6, "Raw bank + new source energy: up to 99.9 mJ\n(28.3 V corner) → must go to the raw dump.\nProtected bank + dummy → go to the crowbar.",
            ha="right", va="top", fontsize=10.5, color=C_FAULT)
    stamp(fig, "Values CALCULATED from Gate 4a ASSUMED capacitance/inductance limits · not measured")
    fig.savefig(OUT / "v2-p03-03-energy-stores.png"); plt.close(fig)


def f6_timeline(c):
    t = c["t"] * 1e6; tt = c["t_trip"] * 1e6
    fig = plt.figure(figsize=(13, 9.5))
    gs = fig.add_gridspec(3, 1, height_ratios=[2.2, 1.3, 1.5], hspace=0.42)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1], sharex=a); z = fig.add_subplot(gs[2])
    m = t <= 60
    a.plot(t[m], c["vraw"][m], color=C_RAW, lw=3, label="VOUT_5V1 (raw, before the switch)")
    a.plot(t[m], c["vpi"][m], color=C_PROT, lw=2.4, ls="--", label="Protected node (ideal far end; no harness)")
    a.axhline(5.5, color=C_FAULT, lw=1.5); a.text(1, 5.52, "Project peak limit 5.5 V", ha="left", color=C_FAULT, va="bottom")
    a.axhspan(5.220, 5.315, color=C_RAW, alpha=.12); a.text(30, 5.235, "detector trip window 5.22–5.31 V", color=C_RAW, fontsize=9.5)
    a.axhline(4.75, color=C_GREY, lw=1, ls=":"); a.text(59, 4.755, "Pi minimum 4.75 V", ha="right", color=C_GREY, fontsize=9)
    a.set_ylim(4.6, 5.65); a.set_ylabel("Voltage (V)")
    ev = [(0, "① short\nhappens", 0.4, "left"), (10, "② source cut\n(10 µs target)", 0.4, "left"),
          (tt, f"③ detector trips\n({tt:.1f} µs)", -0.4, "right"), (tt + 1, "④ switch opens,\ncrowbar + raw dump fire", 0.4, "left")]
    for x, lab, dx, ha in ev:
        for axx in (a, b):
            axx.axvline(x, color="#495057", lw=1, ls="--")
        a.text(x + dx, 4.63 if ha == "left" else 4.86, lab, fontsize=9.5, va="bottom", ha=ha,
               bbox=dict(fc="white", ec="none", alpha=.85, pad=1))
    a.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1, 0.93)); a.set_title("A. First 60 µs: raw node climbs, then the switch splits the two sides", loc="left", fontweight="bold")
    b.plot(t[m], c["iL"][m], color=C_SRC, lw=2.6); b.set_ylabel("L201 current (A)")
    b.set_xlabel("Time after the short (µs)"); b.set_xlim(-1, 60)
    b.set_title("B. Inductor current keeps flowing after the source is cut (stored ½LI²)", loc="left", fontweight="bold")
    tm = c["t"] * 1e3
    z.plot(tm, c["vraw"], color=C_RAW, lw=2.6, label="raw node → drained by the 100 mΩ raw dump")
    z.plot(tm, c["vpi"], color=C_PROT, lw=2.2, ls="--", label="protected node → pulled down by the crowbar")
    z.set_xlim(0, 1.5); z.set_ylim(-0.2, 6); z.set_xlabel("Time after the short (ms)"); z.set_ylabel("Voltage (V)")
    z.legend(loc="upper right", fontsize=10); z.set_title("C. Zoomed out: both stores are emptied, then the board stays latched off", loc="left", fontweight="bold")
    fig.suptitle("A 24 V high-side short, step by step (ideal model)", fontsize=16, fontweight="bold", x=0.02, ha="left")
    stamp(fig, "ASSUMED model: 10 µH, raw 2.41 mF, protected 1.20 mF, 8 A start, 1 µs action delay ASSUMED · source cut at 10 µs needs the still-missing trigger")
    fig.savefig(OUT / "v2-p03-06-fault-timeline.png"); plt.close(fig)


def f7_compare(a_, b_, c_):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(a_["t"] * 1e6, a_["vpi"], color=C_FAULT, lw=3, label="No Sheet 03, source never cut (not a bounded V1A fault)")
    m = b_["t"] <= 200e-6
    ax.plot(b_["t"][m] * 1e6, b_["vpi"][m], color=C_RAW, lw=3, label="No Sheet 03, source cut at 10 µs")
    m = c_["t"] <= 200e-6
    ax.plot(c_["t"][m] * 1e6, c_["vpi"][m], color=C_PROT, lw=3, label="With Sheet 03 (switch + crowbar + dumps)")
    ax.axhline(5.5, color="black", lw=1.4, ls="--"); ax.text(198, 5.58, "Project peak limit 5.5 V", ha="right")
    ax.fill_between([0, 200], 5.5, 10, color=C_FAULT, alpha=.06)
    ax.annotate("9.2 V at 100 µs\n(still rising)", (100, 9.2), (120, 8.3), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=C_FAULT)
    ax.annotate("≈ 6.08 V peak:\nstored energy alone\nis enough to break 5.5 V", (99, 6.076), (125, 6.8), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=C_RAW)
    ax.annotate("≈ 5.28 V peak, then\ncrowbar pulls the Pi to 0 V", (17.5, 5.28), (35, 3.2), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=C_PROT)
    ax.set_xlim(0, 200); ax.set_ylim(0, 10); ax.set_xlabel("Time after the short (µs)"); ax.set_ylabel("Ideal far-end voltage (V)")
    ax.legend(loc="upper left", fontsize=10.5)
    ax.set_title("Same fault, three outcomes: why a source cut alone is not enough", fontsize=14, fontweight="bold", loc="left")
    stamp(fig, "ASSUMED ideal model: no harness/ESR; pre-trip protected C and load omitted; red ignores eFuse current limit · NOT MEASURED")
    fig.savefig(OUT / "v2-p03-07-with-vs-without.png"); plt.close(fig)


def f8_latency():
    fig, ax = plt.subplots(figsize=(12, 5.6))
    w = 1 / math.sqrt(fm.L * fm.C_RAW); t = np.linspace(0, 40e-6, 800)
    for vin, col in [(9, "#74C0FC"), (24, C_SRC), (26, "#9C36B5"), (27, "#E64980")]:
        v = vin + (fm.V0 - vin) * np.cos(w * t) + fm.I0 / (fm.C_RAW * w) * np.sin(w * t)
        tl = fm.ov_latency(vin)
        ax.plot(t * 1e6, v, color=col, lw=2.6, label=f"{vin} V input: trips at {tl*1e6:.1f} µs")
        ax.plot(tl * 1e6, fm.TRIP, "o", color=col, ms=8)
    ax.axhspan(5.220, 5.315, color=C_RAW, alpha=.15); ax.text(0.5, 5.325, "detector trip window", color=C_RAW)
    ax.axvline(10, color=C_FAULT, lw=2); ax.text(10.3, 5.43, "source must be OFF by 10 µs", color=C_FAULT, fontweight="bold")
    ax.fill_betweenx([5.05, 5.5], 10, 40, color=C_FAULT, alpha=.05)
    ax.set_xlim(0, 40); ax.set_ylim(5.08, 5.5); ax.set_xlabel("Time after the short (µs)"); ax.set_ylabel("VOUT_5V1 (V)")
    ax.legend(loc="lower right", fontsize=10.5)
    ax.set_title("The 5 V detector sees the fault too late to be the source trigger", fontsize=14, fontweight="bold", loc="left")
    ax.text(0.5, 5.11, "The big raw bank slows the voltage rise. That protects the Pi,\nbut it hides the fault from a voltage detector for 16–30 µs.", fontsize=10.5)
    stamp(fig, "ASSUMED Gate 4a stiff-source model: 10 µH, 2.4064 mF, 8 A, zero ESR, nominal trip 5.267 V · reproduces Gate 4a-FIX latencies")
    fig.savefig(OUT / "v2-p03-08-detector-latency.png"); plt.close(fig)


def f9_ladder():
    fig, ax = plt.subplots(figsize=(15, 8.6)); ax.set_xlim(0, 13); ax.set_ylim(4.70, 5.66); ax.grid(False)
    ax.spines["bottom"].set_visible(False); ax.set_xticks([])
    rows = [(5.542, "Historical harness counterexample at the Pi (Gate 3b)", C_FAULT, "CALCULATED · BLOCKING"),
            (5.500, "Project Pi peak limit: must stay strictly below", "black", "REQUIREMENT"),
            (5.485, "Bench pass line: 5.5 V minus 15 mV measurement uncertainty", C_OK, "TEST CRITERION"),
            (5.357, "Trip + 20 mV comparator overdrive (upper corner)", C_RAW, "CALCULATED"),
            (5.315, "Detector trip window, top", C_RAW, "CALCULATED"),
            (5.220, "Detector trip window, bottom", C_RAW, "CALCULATED"),
            (5.171, "Healthy regulation, top corner", C_PROT, "CALCULATED"),
            (5.098, "Buck setpoint (100k / 24.4k)", C_PROT, "CALCULATED"),
            (5.026, "Healthy regulation, bottom corner", C_PROT, "CALCULATED"),
            (4.793, "Pi end at 5 A, worst corner (see drop budget)", C_PROT, "CALCULATED"),
            (4.750, "Pi minimum at 5 A", "black", "REQUIREMENT")]
    ax.axhspan(5.220, 5.315, xmin=0.05, xmax=0.2, color=C_RAW, alpha=.25)
    ax.axhspan(5.315, 5.5, xmin=0.05, xmax=0.2, color="#FFF3BF")
    ax.axhspan(5.026, 5.171, xmin=0.05, xmax=0.2, color=C_PROT, alpha=.2)
    ax.plot([1.25, 1.25], [4.70, 5.66], color="#343A40", lw=3)
    ty = []; gap = 0.034
    for v, *_ in rows:  # spread label rows so none overlap, top-down
        ty.append(min(v, ty[-1] - gap) if ty else v)
    for (v, lab, col, kind), t in zip(rows, ty):
        ax.plot([0.9, 1.6], [v, v], color=col, lw=2.4)
        ax.plot([1.6, 1.85], [v, t], color=col, lw=1)
        ax.text(1.9, t, f"{v:.3f} V  {lab}", va="center", fontsize=10.5, color=col, fontweight="bold" if kind.startswith("REQ") else "normal")
        ax.text(12.95, t, kind, va="center", ha="right", fontsize=8.5, color=C_GREY)
    ax.annotate("", (1.25, 5.66), (1.25, 5.60), arrowprops=dict(arrowstyle="-|>", color=C_RAW, lw=2))
    ax.text(1.9, 5.625, "↑ off scale: 6.304 V raw-bank energy bound at 24 V (only the raw side may go here)", fontsize=10.5, color=C_RAW, va="center")
    ax.annotate("", (0.55, 5.315), (0.55, 5.5), arrowprops=dict(arrowstyle="<->", lw=1.5))
    ax.text(0.5, 5.405, "let-through\nbudget\n≈185 mV", ha="right", va="center", fontsize=9)
    ax.annotate("", (0.55, 5.171), (0.55, 5.220), arrowprops=dict(arrowstyle="<->", lw=1.5))
    ax.text(0.5, 5.195, "nuisance\nmargin\n≈49 mV", ha="right", va="center", fontsize=9)
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Preliminary voltage ladder: requirements and conditional screens", fontsize=14, fontweight="bold", loc="left")
    stamp(fig, "Numbers from Gate 3b / Gate 4a(-FIX WIP) reports · CALCULATED = arithmetic under stated assumptions, not measured")
    fig.savefig(OUT / "v2-p03-09-voltage-ladder.png"); plt.close(fig)


def f10_drop():
    items = [("Buck output copper (send+return)", 1.0), ("Series pair 2×BSC034, hot", 13.6), ("2 mΩ shunt, hot corner", 2.024),
             ("Module PCB traces (send+return)", 2.0), ("J502 poles (allocation)", 6.24), ("AWG16 trunks", 2.506),
             ("AWG22 fan-outs", 0.803), ("Pi contacts, crimps, pins", 13.3), ("Splices + solder joints", 1.2)]
    total = sum(r for _, r in items)
    v = 5.026143; fig, ax = plt.subplots(figsize=(13, 6.2))
    ax.bar(0, v, color=C_PROT, width=0.7); ax.text(0, v + 0.004, f"{v:.3f}", ha="center", fontsize=9.5, fontweight="bold")
    x = 1
    for lab, r in items:
        d = 5 * r / 1000
        ax.bar(x, d, bottom=v - d, color=C_FAULT if r > 5 else "#FFA8A8", width=0.7)
        ax.text(x, v + 0.004, f"−{d*1000:.0f} mV", ha="center", fontsize=9)
        v -= d; x += 1
    ax.bar(x, 0.02, bottom=v - 0.02, color="#FFA8A8", width=0.7, hatch="//"); ax.text(x, v + 0.004, "−20 mV", ha="center", fontsize=9)
    v -= 0.02; x += 1
    ax.bar(x, v, color=C_OK, width=0.7); ax.text(x, v + 0.004, f"{v:.3f}", ha="center", fontsize=10, fontweight="bold")
    ax.axhline(4.75, color="black", ls="--"); ax.text(x + 0.45, 4.752, "4.75 V minimum", ha="right", va="bottom")
    labels = ["Buck minimum\n(hot, tolerance)"] + [l for l, _ in items] + ["Load-step\ntrough (ASSUMED)", "At the Pi"]
    ax.set_xticks(range(x + 1)); ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=9.5)
    ax.set_ylim(4.70, 5.05); ax.set_ylabel("Voltage (V)"); ax.grid(axis="x", visible=False)
    ax.set_title(f"5 A drop budget: {total:.1f} mΩ loop leaves {1000*(v-4.75):.0f} mV of margin", fontsize=14, fontweight="bold", loc="left")
    ax.text(0.99, 0.97, "Gate 4a allocations (PATH_BUDGET + hot BSC034 pair)\nJ502 PENDING · contacts ASSUMED · not measured\nA 100 mV load-step trough would FAIL: 4.713 V",
            transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color="#495057")
    fig.savefig(OUT / "v2-p03-10-drop-budget.png"); plt.close(fig)



def main():
    c = fm.simulate(24, 10e-6, True)
    b = fm.simulate(24, 10e-6, False, t_end=400e-6)
    a = fm.simulate(24, None, False, t_end=100e-6)
    f3_energy(); f6_timeline(c); f7_compare(a, b, c)
    f8_latency(); f9_ladder(); f10_drop()
    print("Lesson 03: 6 pilot-derived charts generated (no code-drawn illustrations).")

if __name__ == "__main__":
    main()
