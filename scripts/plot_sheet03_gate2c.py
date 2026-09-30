#!/usr/bin/env python3
"""Render standalone conditional fault trajectories; requires matplotlib.

The analysis calculator itself uses only the Python standard library.
No native KiCad file is read. The figure's assumptions are in Gate2c closure.
"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype'] = 'none'
matplotlib.rcParams['svg.hashsalt'] = 'V1A-Gate2c-conditional-sensitivity'
import matplotlib.pyplot as plt
from calculate_sheet03_gate2c import EVIDENCE, calculate, fault


def main():
    j = calculate()
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, layout='constrained')
    for floor, colour in ((.5e-6, '#2166ac'), (.1e-6, '#b2182b')):
        result, trace = fault(24, .3e-6, floor, j['threshold']['max_V'],
                              j['buck_static']['min_V'], trace=True,
                              finite_input=True, efuse_origin='hot_short_current')
        origin = result['comparator_overdrive_crossing_s']
        x = [(row[0] - origin) * 1e6 for row in trace]
        label = f'ASSUMED L floor {floor * 1e6:g} µH'
        axes[0].plot(x, [row[1] + .020 for row in trace], color=colour, label=label)
        axes[1].plot(x, [row[2] for row in trace], color=colour, label=f'L201: {label}')
        axes[1].plot(x, [row[3] for row in trace], color=colour, linestyle='--', label=f'Q303: {label}')
    axes[0].axhline(5.5, color='black', linestyle=':', label='ASSUMED requirement ceiling')
    axes[0].set_ylabel('CALCULATED Pi voltage screen (V)')
    axes[1].set_ylabel('CALCULATED current (A)')
    axes[1].set_xlabel('Time after modeled comparator overdrive crossing (µs)')
    axes[0].set_xlim(-1, 2)
    for ax in axes:
        ax.axvline(.3, color='#666666', linestyle=':', linewidth=1)
        ax.grid(alpha=.2)
        ax.legend(loc='upper left', fontsize=8)
    fig.suptitle('Conditional sensitivities — application worst case OPEN\n'
                 'ASSUMED 24 V source, finite input C, hot-short disconnect after typical-only delay\n'
                 'ASSUMED crowbar action / series isolation; see Gate2c report for all limitations', fontsize=11)
    output = EVIDENCE / 'gate2c'
    output.mkdir(exist_ok=True)
    fig.savefig(output / 'FAULT_TRAJECTORIES.png', dpi=170)
    fig.savefig(output / 'FAULT_TRAJECTORIES.svg', metadata={'Date': None})
    svg = output / 'FAULT_TRAJECTORIES.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    plt.close(fig)


if __name__ == '__main__':
    main()
