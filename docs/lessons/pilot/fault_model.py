#!/usr/bin/env python3
"""Ideal teaching model of a buck high-side short, for Lesson 03 (pilot).

ILLUSTRATIVE ONLY. Lossless, constant C and L, no ESR/ESL, no harness.
Assumptions follow Gate 4a (feat/r2-testboard-freeze, calculate_gate4a.py):
L201 = 10 uH, raw bank = 2.4064 mF (8 x 470 uF x 0.8 x 0.8), 8 A healthy
inductor current at fault onset, load ignored before the trip.
It is NOT a qualified trajectory and NOT a prediction of the real board.
"""
import math
import numpy as np

L = 10e-6            # L201 candidate, nominal (ASSUMED constant)
C_RAW = 2.4064e-3    # raw bank minimum (Gate 4a ASSUMED)
C_PROT = 1.2032e-3   # protected bank minimum, 4 x 470 uF x 0.64 (Gate 4a ASSUMED)
C_IN = 30e-6         # upper effective input bank (Gate 3b ASSUMED)
V0 = 5.0983606557377055   # nominal local regulation 100k/24.4k
I0 = 8.0             # healthy inductor current at fault onset (ASSUMED)
TRIP = 5.2667        # Gate 4a-FIX nominal detector trip (WIP, CALCULATED)
R_DUMP = 0.100       # raw dump ballast candidate
R_CROW = 0.033       # protected crowbar ballast (preliminary)
R_LOAD = 5.1 / 5.0   # dummy load, 5 A at 5.1 V (resistive)
T_ACT = 1e-6         # trip -> pair open / dumps on (ASSUMED for the picture; real value OPEN)


def ov_latency(vin, trip=TRIP):
    """Exact Gate 4a stiff-source model: time until raw node reaches trip."""
    w = 1 / math.sqrt(L * C_RAW)
    f = lambda t: vin + (V0 - vin) * math.cos(w * t) + I0 / (C_RAW * w) * math.sin(w * t) - trip
    a, b = 0.0, math.pi / w
    for _ in range(100):
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


def simulate(vin=24.0, t_src_off=None, sheet03=True, t_end=3e-3):
    """Return dict of arrays: t, vin, iL, vraw, vpi, plus event times.

    t_src_off: time the source is physically removed (None = never).
    sheet03:   False = no detector / disconnect / dumps (raw node feeds the Pi).
    """
    t, vi, il, vr, vp = 0.0, vin, I0, V0, V0
    src = True
    tripped = None
    out = {k: [] for k in ("t", "vin", "iL", "vraw", "vpi")}
    while t < t_end:
        dt = 2e-9 if t < 120e-6 else 50e-9
        if src and t_src_off is not None and t >= t_src_off:
            src = False
        if sheet03 and tripped is None and vr >= TRIP:
            tripped = t
        acting = tripped is not None and t >= tripped + T_ACT
        # inductor: input side is stiff source, or floating Cin with ideal ground diode
        v_left = vin if src else max(vi, 0.0)
        dil = (v_left - vr) / L
        i_dump = vr / R_DUMP if acting else 0.0
        if acting:
            # pair open: protected node is on its own with load + crowbar
            dvr = (il - i_dump) / C_RAW
            dvp = -(vp / R_LOAD + vp / R_CROW) / C_PROT
        else:
            # pair closed: node moves together (Gate 4a convention: raw C only, load ignored)
            dvr = il / C_RAW
            dvp = None
        if not src and vi > 0:
            vi -= il / C_IN * dt
        il = max(il + dil * dt, 0.0)
        vr += dvr * dt
        vp = vr if dvp is None else vp + dvp * dt
        t += dt
        if len(out["t"]) == 0 or t - out["t"][-1] >= (5e-8 if t < 120e-6 else 1e-6):
            for k, v in zip(out, (t, v_left, il, vr, vp)):
                out[k].append(v)
    res = {k: np.array(v) for k, v in out.items()}
    res["t_trip"] = tripped
    return res


if __name__ == "__main__":
    for v in (9, 24, 26, 27):
        print(f"OV-only latency at {v} V: {ov_latency(v)*1e6:.2f} us  (5.325 V: {ov_latency(v, 5.325)*1e6:.2f} us)")
    c = simulate(24, 10e-6, True)
    b = simulate(24, 10e-6, False, t_end=400e-6)
    a = simulate(24, None, False, t_end=100e-6)
    print("C: trip %.2f us, raw peak %.3f V, Pi peak %.3f V, iL peak %.1f A" % (c["t_trip"]*1e6, c["vraw"].max(), c["vpi"].max(), c["iL"].max()))
    print("B: Pi peak %.3f V at %.1f us" % (b["vpi"].max(), b["t"][b["vpi"].argmax()]*1e6))
    print("A: Pi at 100 us %.2f V, iL %.0f A; crosses 5.5 V at %.1f us" % (a["vpi"][-1], a["iL"][-1], a["t"][np.argmax(a["vpi"] > 5.5)]*1e6))
    print("C raw < 0.3 V at %.2f ms" % (c["t"][np.argmax((c["vraw"] < 0.3) & (c["t"] > 50e-6))]*1e3))
