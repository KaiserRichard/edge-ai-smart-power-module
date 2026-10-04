#!/usr/bin/env python3
"""Independent Gate2b comparison; standard library only, no repository imports."""
import collections
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def canonical(path):
    tree = ET.parse(path).getroot()
    components, nets, seen_pins = {}, {}, set()
    for comp in tree.findall('./components/comp'):
        ref = comp.attrib['ref']
        if ref in components:
            raise ValueError(f'Duplicate refdes {ref} in {path}')
        libsource = comp.find('libsource')
        if libsource is None:
            raise ValueError(f'Missing library source for {ref}')
        components[ref] = {
            'value': comp.findtext('value', ''),
            'footprint': comp.findtext('footprint', ''),
            'lib_id': libsource.attrib['lib'] + ':' + libsource.attrib['part'],
        }
    for net in tree.findall('./nets/net'):
        name = net.attrib['name']
        if name in nets:
            raise ValueError(f'Duplicate net name {name}')
        pins = []
        for node in net.findall('node'):
            key = (node.attrib['ref'], node.attrib['pin'])
            if key[0] not in components:
                raise ValueError(f'Unknown component {key}')
            if key in seen_pins:
                raise ValueError(f'Pin occurs twice {key}')
            seen_pins.add(key)
            pins.append(':'.join(key))
        nets[name] = sorted(set(pins))
    return {'components': dict(sorted(components.items())), 'nets': dict(sorted(nets.items()))}


def changes(before, after):
    result = {}
    for category in ('components', 'nets'):
        a, b = before[category], after[category]
        result[category] = {
            'removed': {key: a[key] for key in sorted(a.keys() - b.keys())},
            'added': {key: b[key] for key in sorted(b.keys() - a.keys())},
            'changed': {key: {'baseline': a[key], 'head': b[key]} for key in sorted(a.keys() & b.keys()) if a[key] != b[key]},
        }
    return result


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def main():
    base_path, head_path, output = map(Path, sys.argv[1:])
    before, after = canonical(base_path), canonical(head_path)
    for name, data in [('baseline', before), ('head', after)]:
        (output / f'independent.{name}.canonical.json').write_bytes(encoded(data))
    diff = changes(before, after)
    result = {
        'baseline': {'components': len(before['components']), 'nets': len(before['nets']), 'pin_memberships': sum(map(len, before['nets'].values()))},
        'head': {'components': len(after['components']), 'nets': len(after['nets']), 'pin_memberships': sum(map(len, after['nets'].values()))},
        'equal': before == after,
        'baseline_canonical_sha256': hashlib.sha256(encoded(before)).hexdigest(),
        'head_canonical_sha256': hashlib.sha256(encoded(after)).hexdigest(),
        'differences': diff,
    }
    (output/'independent.netlist-comparison.json').write_bytes(encoded(result))
    print(json.dumps(result, indent=2))
    return 0 if before == after else 1

if __name__ == '__main__':
    sys.exit(main())
