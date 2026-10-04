#!/usr/bin/env python3
"""Resume step 3 without rebuilding placement or weakening the rule contract.

KiCad bundled Python. This is a connectivity/resistance study, not a release.
The intrinsic package-spacing conflict remains an engineering hold.
"""
import json
from v1a_copper import board, pads, xy, rect, corridor, p, save, EV

PREFIX = 'R3 resume3: '


def main():
    b = board()
    for z in list(b.Zones()):
        if z.GetZoneName().startswith(PREFIX):
            b.RemoveNative(z)
    ps = pads(b)
    pos = lambda r, k: xy(ps[r, str(k)].GetPosition())
    # The original second-row corridor ran through first-row GND lands; the
    # checker could not resolve C212.1. That OPEN result alone is not proof
    # of a physical break. Add an explicit route around BOTH rows. Retain six
    # capacitors on the downstream side of JP202, and do not bridge that link.
    corridor(b, 'VOUT_5V1', [pos('JP202', 2), (143, 69.5),
                            (143, 87.625), pos('C214', 1)], 3,
             name=PREFIX + 'raw ceramic second-row force feed')
    additions = [z for z in b.Zones() if z.GetZoneName().startswith(PREFIX)]
    for z in additions[1:]:
        additions[0].Outline().BooleanAdd(z.Outline())
        b.RemoveNative(z)
    additions[0].Outline().Simplify()
    # Same-side return avoids charging the entire 5 A through a single via.
    # This is a filled, clearance-clipped zone, NOT its ideal bounding box.
    # Existing higher-priority power copper remains in place; the path checker
    # must inspect the actual bottlenecks and report FAIL if too resistive.
    rect(b, 'GND', 140, 45, 237, 101, p.F_Cu, 0,
         PREFIX + 'output same-side return')
    b.BuildConnectivity()
    p.ZONE_FILLER(b).Fill(b.Zones())
    save(b)
    (EV / 'resume3' / 'POWER_CHANGE.json').write_text(json.dumps({
        'status': 'INCOMPLETE step 3; evaluation required',
        'changes': ['Add an explicit second-row route around first-row GND pads',
                    'Add clearance-clipped F.Cu output return'],
        'placement_changed': False,
        'schematic_values_nets_and_qualified_lands_changed': False,
        'rules_changed': False,
        'limitations': ['M1-2 resistance acceptance is not implied',
                        'M1-3 and M1-4 geometry remain unresolved',
                        'M1-5 requires engineering disposition'],
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
