#!/usr/bin/env python3
"""Apply M1 connector/monitor/via corrections to the current board, idempotently.

Run with KiCad's bundled Python. Qualified footprints and nets are preserved.
This does not claim to close the other M1 electrical/layout findings.
"""
import json
import pcbnew as p
from v1a_copper import board, pads, xy, v, save, EV


def main():
    b = board()
    f = next(f for f in b.GetFootprints() if f.GetReference() == 'J502')
    f.SetOrientationDegrees(90)
    fps = {f.GetReference(): f for f in b.GetFootprints()}
    for ref, point in [('TP302', (221, 75.5)), ('TP503', (224, 75.5))]:
        fps[ref].SetPosition(v(*point))
    # M1-8: keep the bypass beside INA228 VS/GND and bring the unfiltered
    # sense test points together beside their dedicated Kelvin pads.
    fps['C402'].SetOrientationDegrees(90)
    fps['C402'].SetPosition(v(210.5, 58.5))
    fps['R408'].SetPosition(v(208.5, 55.5))
    fps['TP402'].SetPosition(v(211.5, 63.5))
    fps['TP403'].SetPosition(v(217.5, 63.5))
    # M1-5/9: the left column of the inherited U101 thermal-via field
    # violated the new 0.64 mm screen. Move it inward on the unchanged EP.
    # This fixes added-via conflicts, not the intrinsic package-pad gaps.
    for via in b.GetTracks():
        if isinstance(via, p.PCB_VIA):
            x, y = xy(via.GetPosition())
            if abs(x - 41.3) < 0.001 and any(abs(y - yy) < .001 for yy in [63.3, 64, 64.7]):
                via.SetPosition(v(41.45, y))
    # Pin 1 stays fixed. Pin 2 moves from below pin 1 to above it.
    # No signal segments were present in the inherited board. Refill existing
    # zones so the GND plane follows the new pin and mounting-hole positions.
    b.BuildConnectivity()
    p.ZONE_FILLER(b).Fill(b.Zones())
    save(b)
    ps = pads(b)
    envelope = []
    for item in f.GraphicalItems():
        if item.GetLayer() == p.Dwgs_User and isinstance(item, p.PCB_SHAPE):
            envelope.append({'start_mm': xy(item.GetStart()),
                             'end_mm': xy(item.GetEnd())})
    out = {'finding': 'M1-1', 'status': 'geometric conflict corrected',
           'J502_position_mm': xy(f.GetPosition()), 'rotation_deg': 90,
           'pins': {k: {'position_mm': xy(ps['J502', k].GetPosition()),
                        'net': ps['J502', k].GetNetname()} for k in ['1', '2']},
           'mate_tool_rectangles': envelope,
           'R401_position_mm': xy(ps['R401', '1'].GetParentFootprint().GetPosition()),
           'limitation': 'Recorded provisional envelope only; physical mate, screwdriver and fixture approval remain OPEN.'}
    (EV / 'M1_CONNECTOR_FIX.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
