#!/usr/bin/env python3
"""Render every figure for the Lesson 03 pilot. Run: python3 make_figures.py
Figures are teaching pictures. Waveforms come from fault_model.py (ideal model)."""
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import schemdraw
import schemdraw.elements as elm
import fault_model as fm

OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(exist_ok=True)
# one colour per meaning, used in every figure
C_SRC, C_RAW, C_PROT, C_FAULT, C_OK, C_GREY, C_CTRL = "#6741D9", "#E8590C", "#1971C2", "#C92A2A", "#2F9E44", "#868E96", "#0C8599"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25,
                     "savefig.dpi": 160, "savefig.bbox": "tight", "figure.facecolor": "white"})
STAMP = "Teaching figure · ideal model, not a measurement · NOT FOR FABRICATION"


def sd_to_ax(ax, build):
    """Draw a schemdraw circuit into a matplotlib axis (via PNG bytes)."""
    import io
    d = schemdraw.Drawing(show=False)
    d.config(fontsize=12)
    build(d)
    img = plt.imread(io.BytesIO(d.get_imagedata("png")), format="png")
    ax.imshow(img); ax.axis("off")


def stamp(fig, text=STAMP):
    fig.text(0.99, 0.005, text, ha="right", va="bottom", fontsize=8, color=C_GREY)


def box(ax, x, y, w, h, text, fc, ec=None, fs=10, tc="black", bold=False, r=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.005,rounding_size={r}",
                                fc=fc, ec=ec or fc, lw=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x0, y0, x1, y1, c="black", lw=2.2, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=16,
                                 color=c, lw=lw, linestyle=ls))


# ---------------------------------------------------------------- F1 map
def f1_map():
    fig, ax = plt.subplots(figsize=(14, 5.2)); ax.set_xlim(0, 14); ax.axis("off")
    ax.add_patch(Rectangle((5.75, 0.5), 4.85, 4.3, fc="#FFF4E6", ec=C_RAW, lw=2, ls="--"))
    ax.text(8.17, 4.92, "SHEET 03 — output protection (architecture D)", ha="center", color=C_RAW, fontweight="bold", fontsize=12)
    blocks = [(0.1, "Isolated\n48→24 V\nmodule", "#E5DBFF"), (1.55, "Sheet 01\nF101 · D101\nTPS26630 eFuse", "#E5DBFF"),
              (3.05, "Sheet 02\nLM61460 buck\n+ L201 10 µH", "#FFE8CC")]
    for x, t, c in blocks:
        box(ax, x, 2.2, 1.3, 1.3, t, c, fs=9.5)
    for x0, x1 in [(1.4, 1.55), (2.85, 3.05)]:
        arrow(ax, x0, 2.85, x1, 2.85)
    arrow(ax, 4.35, 2.85, 5.9, 2.85, c=C_RAW)
    ax.set_ylim(-0.1, 5.2)
    ax.text(5.0, 3.1, "VOUT_5V1\n(raw)", ha="center", color=C_RAW, fontsize=9.5, fontweight="bold")
    box(ax, 5.9, 2.35, 1.3, 1.0, "raw bank\n8 × 470 µF", "#FFD8A8", fs=9)
    box(ax, 5.9, 0.7, 1.3, 1.1, "raw dump\n100 mΩ\n(proposed)", "#FFD8A8", fs=9)
    arrow(ax, 6.55, 2.35, 6.55, 1.8, c=C_RAW, lw=1.5)
    box(ax, 7.4, 2.2, 1.45, 1.3, "series switch\n2× BSC034N06\nback-to-back", "#FFC9C9", fs=8.8, bold=True)
    arrow(ax, 7.2, 2.85, 7.45, 2.85, c=C_RAW)
    arrow(ax, 8.8, 2.85, 9.1, 2.85, c=C_PROT)
    box(ax, 9.1, 2.35, 1.3, 1.0, "protected bank\n4 × 470 µF", "#D0EBFF", fs=9)
    box(ax, 9.1, 0.7, 1.3, 1.1, "crowbar\nCSD18540Q5B\n+ ballast", "#D0EBFF", fs=9)
    arrow(ax, 9.75, 2.35, 9.75, 1.8, c=C_PROT, lw=1.5)
    box(ax, 7.45, 3.65, 1.35, 0.7, "detector + latch", "#C3FAE8", fs=9)
    arrow(ax, 6.55, 3.35, 7.45, 4.0, c=C_CTRL, lw=1.3)
    arrow(ax, 8.1, 3.65, 8.1, 3.5, c=C_CTRL, lw=1.3)
    ax.text(10.05, 3.6, "VOUT_PROTECTED", ha="center", color=C_PROT, fontsize=9.5, fontweight="bold")
    arrow(ax, 10.4, 2.85, 10.8, 2.85, c=C_PROT)
    box(ax, 10.8, 2.25, 1.0, 1.2, "Sheet 04\n2 mΩ shunt\nINA228", "#E7F5FF", fs=9)
    arrow(ax, 11.8, 2.85, 12.2, 2.85, c=C_PROT)
    box(ax, 12.2, 2.0, 1.7, 1.7, "J502 → harness\n→ Pi 5 GPIO\n(dummy load\non R2)", "#E7F5FF", fs=9.5)
    ax.text(12.05, 1.7, "LOAD_5V1", ha="center", color=C_PROT, fontsize=9)
    ax.text(0.1, 0.05, "Colour key:  purple = input side   orange = raw 5 V node (before the switch)   blue = protected side (what the Pi sees)",
            fontsize=9.5, color="#333")
    fig.suptitle("Where Sheet 03 sits in the V1A power path", fontsize=15, fontweight="bold", x=0.02, ha="left")
    stamp(fig, "Functional map, not a wiring diagram · PRELIMINARY TEST BOARD · NOT FOR FABRICATION")
    fig.savefig(OUT / "p03-01-where-sheet03-sits.png"); plt.close(fig)


# ---------------------------------------------------------------- hand-drawn circuit primitives
def wire(ax, pts, c="black", lw=2.2):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round")


def dot(ax, x, y, c="black"):
    ax.plot(x, y, "o", color=c, ms=7)


def inductor_h(ax, x0, x1, y, c="black", n=4):
    wire(ax, [(x0, y), (x0 + .15, y)], c)
    xs = np.linspace(x0 + .15, x1 - .15, n + 1)
    for i in range(n):
        th = np.linspace(np.pi, 0, 30); r = (xs[1] - xs[0]) / 2
        ax.plot(xs[i] + r + r * np.cos(th), y + r * 1.2 * np.sin(th), color=c, lw=2.2)
    wire(ax, [(x1 - .15, y), (x1, y)], c)


def cap_v(ax, x, y0, y1, c="black"):
    ym = (y0 + y1) / 2
    wire(ax, [(x, y0), (x, ym + .12)], c); wire(ax, [(x, ym - .12), (x, y1)], c)
    wire(ax, [(x - .35, ym + .12), (x + .35, ym + .12)], c, 3); wire(ax, [(x - .35, ym - .12), (x + .35, ym - .12)], c, 3)


def res_v(ax, x, y0, y1, c="black"):
    ym = (y0 + y1) / 2; h = .9
    wire(ax, [(x, y0), (x, ym + h / 2)], c); wire(ax, [(x, ym - h / 2), (x, y1)], c)
    zz = [(x + (.18 if i % 2 else -.18) * (0 < i < 7), ym + h / 2 - i * h / 7) for i in range(8)]
    wire(ax, zz, c)


def switch(ax, p0, p1, closed=False, c="black"):
    (x0, y0), (x1, y1) = p0, p1
    ax.plot([x0, x1], [y0, y1], "o", mfc="white", mec=c, ms=8, mew=2)
    if closed:
        wire(ax, [p0, p1], c)
    else:
        dx, dy = x1 - x0, y1 - y0
        wire(ax, [p0, (x0 + .8 * dx - .35 * dy, y0 + .8 * dy + .35 * dx)], c)


def source(ax, x, y0, y1, label):
    ym = (y0 + y1) / 2
    wire(ax, [(x, y0), (x, ym - .45)]); wire(ax, [(x, ym + .45), (x, y1)])
    ax.add_patch(plt.Circle((x, ym), .45, fill=False, lw=2.2))
    ax.text(x, ym + .15, "+", ha="center", va="center", fontsize=13); ax.text(x, ym - .2, "−", ha="center", va="center", fontsize=13)
    ax.text(x - .6, ym, label, ha="right", va="center", fontsize=11, color=C_SRC, fontweight="bold")


def diode_h(ax, x0, x1, y, point_right, c=C_FAULT):
    xm = (x0 + x1) / 2; s = .22
    wire(ax, [(x0, y), (xm - s, y)], c); wire(ax, [(xm + s, y), (x1, y)], c)
    if point_right:
        ax.fill([xm - s, xm - s, xm + s], [y + s, y - s, y], color=c); wire(ax, [(xm + s, y + s), (xm + s, y - s)], c, 3)
    else:
        ax.fill([xm + s, xm + s, xm - s], [y + s, y - s, y], color=c); wire(ax, [(xm - s, y + s), (xm - s, y - s)], c, 3)


# ---------------------------------------------------------------- F2 buck normal vs shorted
def f2_buck():
    fig, axs = plt.subplots(1, 2, figsize=(14, 5.4))
    for ax, sh in [(axs[0], False), (axs[1], True)]:
        ax.set_xlim(-0.6, 10.2); ax.set_ylim(0.2, 6); ax.axis("off"); ax.set_aspect("equal")
        top, bot = 4.5, 1.2; r = C_FAULT if sh else "black"
        source(ax, 1, bot, top, "VIN\n24 V")
        wire(ax, [(1, top), (2.2, top)], r)
        if sh:
            wire(ax, [(2.2, top), (3.8, top)], C_FAULT, 6)
            ax.text(3.0, top + .45, "HS FET\nFAILED SHORT", ha="center", fontsize=10.5, color=C_FAULT, fontweight="bold")
        else:
            switch(ax, (2.2, top), (3.8, top))
            ax.text(3.0, top + .45, "HS FET\n(switching)", ha="center", fontsize=10.5)
        wire(ax, [(3.8, top), (4.4, top)], r); dot(ax, 4.4, top)
        ax.text(4.4, top + .3, "SW", ha="center", fontsize=10)
        switch(ax, (4.4, top - .6), (4.4, bot + .9)); wire(ax, [(4.4, top), (4.4, top - .6)]); wire(ax, [(4.4, bot + .9), (4.4, bot)])
        ax.text(4.65, 2.85, "LS FET\n" + ("(held off)" if sh else "(switching)"), fontsize=10, va="center")
        inductor_h(ax, 4.4, 7.0, top, r); ax.text(5.7, top + .55, "L201  10 µH", ha="center", fontsize=10.5, color=r)
        wire(ax, [(7.0, top), (9.2, top)], r); dot(ax, 7.6, top, C_RAW)
        ax.text(7.6, top + .35, "VOUT_5V1", ha="center", fontsize=10.5, color=C_RAW, fontweight="bold")
        cap_v(ax, 7.6, top, bot); ax.text(8.05, 2.85, "raw\nbank", fontsize=10, va="center")
        res_v(ax, 9.2, top, bot); ax.text(9.5, 2.85, "load", fontsize=10, va="center")
        wire(ax, [(1, bot), (9.2, bot)])
        if sh:
            arrow(ax, 1.3, top - .35, 7.3, top - .35, c=C_FAULT, lw=2, style="-|>")
            ax.text(4.0, 0.55, "Input → short → L201 → output, with no gap in time", ha="center", fontsize=10.5, color=C_FAULT)
        else:
            ax.text(4.8, 0.55, "Duty ≈ 5.1 / 24 ≈ 21 %: the average of the SW pulses is ≈ 5.1 V", ha="center", fontsize=10.5)
    axs[0].set_title("Healthy: the high-side switch chops 24 V into pulses", fontsize=12.5, fontweight="bold")
    axs[1].set_title("Fault: the high-side switch becomes a piece of wire", fontsize=12.5, fontweight="bold", color=C_FAULT)
    fig.suptitle("The one fault Sheet 03 exists for: a buck high-side short", fontsize=15, fontweight="bold", x=0.02, ha="left")
    stamp(fig, "Simplified buck; LM61460 internals and input bank not drawn · teaching figure")
    fig.savefig(OUT / "p03-02-buck-normal-vs-shorted.png"); plt.close(fig)


# ---------------------------------------------------------------- F3 energy stores
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
    fig.savefig(OUT / "p03-03-energy-stores.png"); plt.close(fig)


# ---------------------------------------------------------------- F4 back-to-back FETs
def fet_box(ax, x, y, name, left, right):
    box(ax, x, y - .45, 1.6, .9, name, "#FFE3E3", ec="#343A40", fs=11, bold=True)
    ax.text(x + .12, y + .6, left, fontsize=9, color="#495057"); ax.text(x + 1.48, y + .6, right, fontsize=9, color="#495057", ha="right")


def f4_fets():
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    for ax in axs:
        ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    y, yd = 3.3, 2.0
    # single FET
    ax = axs[0]
    wire(ax, [(1.2, y), (3.6, y)], C_RAW); fet_box(ax, 3.6, y, "Q1 (off)", "D", "S"); wire(ax, [(5.2, y), (7.8, y)], C_PROT)
    dot(ax, 1.2, y, C_RAW); dot(ax, 7.8, y, C_PROT)
    wire(ax, [(3.2, y), (3.2, yd)], C_FAULT); wire(ax, [(5.6, y), (5.6, yd)], C_FAULT)
    diode_h(ax, 3.2, 5.6, yd, point_right=False)
    ax.text(4.4, yd - .55, "body diode conducts ←", ha="center", color=C_FAULT, fontsize=10.5, fontweight="bold")
    ax.text(1.2, y + .45, "VOUT_5V1 (raw)", color=C_RAW, fontweight="bold", ha="center")
    ax.text(7.8, y + .45, "VOUT_PROTECTED", color=C_PROT, fontweight="bold", ha="center")
    ax.text(5, 0.45, "Blocks raw → protected, but if the raw dump pulls raw to 0 V, the protected\nbank and the Pi discharge backwards through the diode.", ha="center", fontsize=10.2)
    # two FETs
    ax = axs[1]
    wire(ax, [(0.6, y), (2.2, y)], C_RAW); fet_box(ax, 2.2, y, "Q1 (off)", "D", "S"); wire(ax, [(3.8, y), (5.0, y)])
    fet_box(ax, 5.0, y, "Q2 (off)", "S", "D"); wire(ax, [(6.6, y), (8.4, y)], C_PROT)
    dot(ax, 0.6, y, C_RAW); dot(ax, 8.4, y, C_PROT); dot(ax, 4.4, y)
    ax.text(4.4, y + .35, "common\nsource", ha="center", fontsize=9)
    for xa, xb, pr in [(1.9, 4.2, False), (4.6, 6.9, True)]:
        wire(ax, [(xa, y), (xa, yd)], C_FAULT); wire(ax, [(xb, y), (xb, yd)], C_FAULT)
        diode_h(ax, xa, xb, yd, point_right=pr)
    wire(ax, [(4.2, yd), (4.6, yd)], C_FAULT)
    ax.text(4.4, yd - .55, "← blocked both ways →", ha="center", color=C_OK, fontsize=10.5, fontweight="bold")
    ax.text(0.6, y + .45, "raw", color=C_RAW, fontweight="bold", ha="center"); ax.text(8.4, y + .45, "protected", color=C_PROT, fontweight="bold", ha="center")
    ax.text(5, 0.45, "The two diodes face away from each other (anodes joined), so no current\ncan pass either way. LTC7001 drives both gates together.", ha="center", fontsize=10.2)
    axs[0].set_title("One MOSFET: 'off' still leaks one way", fontsize=12.5, fontweight="bold")
    axs[1].set_title("Two MOSFETs back-to-back: 'off' means off", fontsize=12.5, fontweight="bold", color=C_OK)
    fig.suptitle("Why the series switch is two BSC034N06 in series, back-to-back", fontsize=15, fontweight="bold", x=0.02, ha="left")
    stamp(fig, "Symbolic drawing (N-channel, D = drain, S = source); gate drive not shown · teaching figure")
    fig.savefig(OUT / "p03-04-back-to-back-mosfets.png"); plt.close(fig)


# ---------------------------------------------------------------- F5 detector chain
def f5_chain():
    fig, ax = plt.subplots(figsize=(14, 4.6)); ax.set_xlim(0, 14); ax.set_ylim(0, 4.6); ax.axis("off")
    steps = [("Divider\n9.88k / 10k\n(+1k, 100k)", "Scales VOUT_5V1\n(5.27 V → 2.5 V)", "#FFE8CC"),
             ("REF5025\n2.500 V", "Precise, independent\nreference", "#C3FAE8"),
             ("TLV3201\ncomparator", "Fast yes/no:\nraw > trip?", "#C3FAE8"),
             ("74LVC1G74\nflip-flop latch", "Remembers the fault\nuntil a deliberate re-arm", "#C3FAE8"),
             ("LTC7001 · UCC27511\nTPS26630 SHDN", "Three actions\nin parallel", "#FFC9C9")]
    x = 0.2
    for i, (a, b, c) in enumerate(steps):
        box(ax, x, 2.2, 2.2, 1.5, a, c, fs=10.5, bold=True)
        ax.text(x + 1.1, 1.75, b, ha="center", va="top", fontsize=9.8)
        if i < len(steps) - 1:
            arrow(ax, x + 2.2, 2.95, x + 2.75, 2.95, c=C_CTRL)
        x += 2.75
    ax.text(7, 4.25, "Nominal trip 5.267 V · conditional window 5.220–5.315 V (Gate 4a-FIX, WIP)", ha="center", fontsize=11.5, fontweight="bold", color=C_RAW)
    ax.text(12.5, 0.55, "open series pair · fire crowbar + raw dump · shut the eFuse", ha="center", fontsize=9.5, color=C_FAULT)
    fig.suptitle("Detect → remember → act: the Sheet 03 control chain", fontsize=15, fontweight="bold", x=0.02, ha="left")
    stamp(fig, "Divider values from Gate 4a-FIX work in progress · timing OPEN")
    fig.savefig(OUT / "p03-05-detector-chain.png"); plt.close(fig)


# ---------------------------------------------------------------- F6 fault timeline (main)
def f6_timeline(c):
    t = c["t"] * 1e6; tt = c["t_trip"] * 1e6
    fig = plt.figure(figsize=(13, 9.5))
    gs = fig.add_gridspec(3, 1, height_ratios=[2.2, 1.3, 1.5], hspace=0.42)
    a = fig.add_subplot(gs[0]); b = fig.add_subplot(gs[1], sharex=a); z = fig.add_subplot(gs[2])
    m = t <= 60
    a.plot(t[m], c["vraw"][m], color=C_RAW, lw=3, label="VOUT_5V1 (raw, before the switch)")
    a.plot(t[m], c["vpi"][m], color=C_PROT, lw=2.4, ls="--", label="VOUT_PROTECTED (what the Pi sees)")
    a.axhline(5.5, color=C_FAULT, lw=1.5); a.text(1, 5.52, "Pi limit 5.5 V", ha="left", color=C_FAULT, va="bottom")
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
    stamp(fig, "Ideal lossless model: 10 µH, raw 2.41 mF, protected 1.20 mF, 8 A start, 1 µs action delay ASSUMED · source cut at 10 µs needs the still-missing trigger")
    fig.savefig(OUT / "p03-06-fault-timeline.png"); plt.close(fig)


# ---------------------------------------------------------------- F7 with vs without
def f7_compare(a_, b_, c_):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(a_["t"] * 1e6, a_["vpi"], color=C_FAULT, lw=3, label="No Sheet 03, source never cut")
    m = b_["t"] <= 200e-6
    ax.plot(b_["t"][m] * 1e6, b_["vpi"][m], color=C_RAW, lw=3, label="No Sheet 03, source cut at 10 µs")
    m = c_["t"] <= 200e-6
    ax.plot(c_["t"][m] * 1e6, c_["vpi"][m], color=C_PROT, lw=3, label="With Sheet 03 (switch + crowbar + dumps)")
    ax.axhline(5.5, color="black", lw=1.4, ls="--"); ax.text(198, 5.58, "Pi limit 5.5 V", ha="right")
    ax.fill_between([0, 200], 5.5, 10, color=C_FAULT, alpha=.06)
    ax.annotate("9.2 V at 100 µs\n(still rising)", (100, 9.2), (120, 8.3), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=C_FAULT)
    ax.annotate("≈ 6.08 V peak:\nstored energy alone\nis enough to break 5.5 V", (99, 6.076), (125, 6.8), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=C_RAW)
    ax.annotate("≈ 5.28 V peak, then\ncrowbar pulls the Pi to 0 V", (17.5, 5.28), (35, 3.2), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=C_PROT)
    ax.set_xlim(0, 200); ax.set_ylim(0, 10); ax.set_xlabel("Time after the short (µs)"); ax.set_ylabel("Voltage at the Pi side (V)")
    ax.legend(loc="upper left", fontsize=10.5)
    ax.set_title("Same fault, three outcomes: why a source cut alone is not enough", fontsize=14, fontweight="bold", loc="left")
    stamp(fig, "Ideal model (fault_model.py), no harness ringing, eFuse current limit ignored in the red case · not a prediction")
    fig.savefig(OUT / "p03-07-with-vs-without.png"); plt.close(fig)


# ---------------------------------------------------------------- F8 detector latency
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
    stamp(fig, "Gate 4a stiff-source model: 10 µH, 2.4064 mF, 8 A, zero ESR, nominal trip 5.267 V · reproduces Gate 4a-FIX latencies")
    fig.savefig(OUT / "p03-08-detector-latency.png"); plt.close(fig)


# ---------------------------------------------------------------- F9 voltage ladder
def f9_ladder():
    fig, ax = plt.subplots(figsize=(11.5, 8.6)); ax.set_xlim(0, 10); ax.set_ylim(4.70, 5.66); ax.grid(False)
    ax.spines["bottom"].set_visible(False); ax.set_xticks([])
    rows = [(5.542, "Historical harness counterexample at the Pi (Gate 3b)", C_FAULT, "CALCULATED · BLOCKING"),
            (5.500, "Pi absolute limit: must stay strictly below", "black", "REQUIREMENT"),
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
        ax.text(9.95, t, kind, va="center", ha="right", fontsize=8.5, color=C_GREY)
    ax.annotate("", (1.25, 5.66), (1.25, 5.60), arrowprops=dict(arrowstyle="-|>", color=C_RAW, lw=2))
    ax.text(1.9, 5.625, "↑ off scale: 6.304 V raw-bank energy bound at 24 V (only the raw side may go here)", fontsize=10.5, color=C_RAW, va="center")
    ax.annotate("", (0.55, 5.315), (0.55, 5.5), arrowprops=dict(arrowstyle="<->", lw=1.5))
    ax.text(0.5, 5.405, "let-through\nbudget\n≈185 mV", ha="right", va="center", fontsize=9)
    ax.annotate("", (0.55, 5.171), (0.55, 5.220), arrowprops=dict(arrowstyle="<->", lw=1.5))
    ax.text(0.5, 5.195, "nuisance\nmargin\n≈49 mV", ha="right", va="center", fontsize=9)
    ax.set_ylabel("Voltage (V)")
    ax.set_title("The voltage ladder: every number in this lesson on one ruler", fontsize=14, fontweight="bold", loc="left")
    stamp(fig, "Numbers from Gate 3b / Gate 4a(-FIX WIP) reports · CALCULATED = arithmetic under stated assumptions, not measured")
    fig.savefig(OUT / "p03-09-voltage-ladder.png"); plt.close(fig)


# ---------------------------------------------------------------- F10 drop budget waterfall
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
    fig.savefig(OUT / "p03-10-drop-budget.png"); plt.close(fig)


# ---------------------------------------------------------------- F11 D vs E
def f11_options():
    fig, axs = plt.subplots(1, 2, figsize=(14, 4.4))
    for ax, name, e in [(axs[0], "D (chosen): protection at the module", False), (axs[1], "E (Gate 3 favourite): protection at the Pi header", True)]:
        ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
        box(ax, 0.1, 1.5, 1.8, 1.2, "buck", "#FFE8CC")
        box(ax, 2.3, 1.5, 1.9, 1.2, "V1A module\nswitch + crowbar" if not e else "V1A module", "#FFC9C9" if not e else "#E9ECEF", fs=9.5)
        ax.plot([4.2, 7.3], [2.1, 2.1], color=C_PROT, lw=4); ax.text(5.75, 2.3, "harness: 75 mm trunk + fan-outs\n(inductance + contacts)", ha="center", fontsize=9)
        box(ax, 7.3, 1.5, 1.2 if e else 0.01, 1.2, "Pi-end\nstage" if e else "", "#FFC9C9", fs=9) if e else None
        box(ax, 8.6 if e else 7.4, 1.5, 1.3, 1.2, "Pi 5", "#D0EBFF")
        ax.set_title(name, fontweight="bold", fontsize=12, loc="left")
        pro = ("+ reuses module layout, no extra loss\n− the cable can ring ABOVE the module voltage (5.542 V model case)"
               if not e else "+ watches the exact voltage the Pi sees\n− extra FETs, wiring, aux power, more drop (49.6 mΩ loop)")
        ax.text(0.1, 0.55, pro, fontsize=10, va="center")
    fig.suptitle("Why D for a fault-test board, and what it still owes", fontsize=15, fontweight="bold", x=0.02, ha="left")
    stamp(fig, "Summary of Gate 3 / Gate 3b comparison · owner decision 2026-09-30")
    fig.savefig(OUT / "p03-11-d-vs-e.png"); plt.close(fig)


if __name__ == "__main__":
    c = fm.simulate(24, 10e-6, True)
    b = fm.simulate(24, 10e-6, False, t_end=400e-6)
    a = fm.simulate(24, None, False, t_end=100e-6)
    f1_map(); f2_buck(); f3_energy(); f4_fets(); f5_chain(); f6_timeline(c); f7_compare(a, b, c)
    f8_latency(); f9_ladder(); f10_drop(); f11_options()
    print(sorted(p.name for p in OUT.glob("*.png")))
