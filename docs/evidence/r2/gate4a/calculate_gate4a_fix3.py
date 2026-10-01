"""Round-3 design screens. Conditional allocations are never measured bounds."""
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RF = .001 + 25e-6 * 65  # precision resistor initial + -40..85 C delta from 25 C


def interval(values):
    return [min(values), max(values)]


def corners(value, error=RF):
    return [value * (1-error), value * (1+error)]


def loaded_threshold(rt, rb, threshold, allowance, feedback=None, output=(0, 0)):
    """KCL through the powered switch, with a post-switch 100k bleed.

    Reference allowance includes comparator offset/leakage/hysteresis by allocation.
    Ron 0..17 ohm is a transferred datasheet test condition, not partial-power data.
    """
    values = []
    for t, b, p, ron, v, h, vo in itertools.product(
            corners(rt), corners(rb) if rb else [float('inf')], corners(100e3),
            [0., 17.], [threshold-allowance, threshold+allowance],
            corners(feedback) if feedback else [float('inf')], output):
        values.append(v*((1+ron/p)*(1+t/b+t/h)+t/p)-vo*t/h)
    return interval(values)


def timer(r, n, error):
    nominal = r/50e3*n*1e-6
    return [nominal*(1-RF)*(1-error), nominal*(1+RF)*(1+error)]


def fixture():
    rmin = 9.1*(1-.01-50e-6*100)/4
    i = 31/rmin
    # Independent maximum stored capacitance; source work is counted for the
    # entire 20us interval. The bench abort is not credited to the DUT result.
    e = (.5*33e-6*30**2 + 30*14*20e-6 + .5*12e-6*8**2
         + .5*1e-6*14**2 + .5*40e-9*100**2 + .1e-3)
    abort = timer(100e3, 8, .044)
    dead = timer(100e3, 1, .062)
    return dict(
        classification='External fixture design envelope; application qualification NOT RUN',
        limit_Rmin_ohm=rmin, resistor_current_max_A=i,
        resistor_power_each_W=31**2/(4*rmin),
        resistor_allowable_screen_W=250*(250-70)/(250-25),
        dead_timer_s=dead, abort_timer_s=abort,
        abort_complete_max_s=abort[1]+2e-6+.025e-6,
        abort_earliest_after_fault_s=abort[0]-(dead[1]+.5e-6),
        hardware_abort_acceptance_s=20e-6,
        added_energy_J=e,
        coupled_energy_J=e+.5*(5.59656e-3+2.7072e-3+2.64e-3)*5.5**2,
        inductor_current_screen_A=(2*e/5e-6)**.5,
        raw_no_dump_peak_screen_V=(5.5**2+2*e/2.4064e-3)**.5+.004*100+.020,
        force_FET_on_energy_each_J=100**2*.0068*20e-6,
        source_FET_on_energy_each_J=14**2*.0068*20e-6,
        FET_overlap_energy_each_J=50*100*1e-6,
        contact_energy_each_J=100**2*.0002*20e-6,
        actual_current_bound_A=None, actual_abort_s=None,
        actual_hot_SOA_margin=None, actual_all_stores_discharged=None)


def calculate():
    wd = timer(200e3, 1, .062)
    thresholds = {name: loaded_threshold(rt, rb, v, e) for name, rt, rb, v, e in [
        ('SER_DRV', 69800, 10000, 1.25, .015),
        ('DET5', 26100, 10000, 1.25, .015),
        ('3V3_AUX', 13700, 10000, 1.25, .015),
        ('SAFE5', 24900, 10000, 1.25, .015),
        ('DIAG_VIN', 18200, 10000, 1.25, .015),
        ('ZERO', 10000, None, 2.5*10000/100900, .005),
        ('VIN_PROTECTED', 49900, 10000, 1.25, .015)]}
    thresholds['DRV_HOLD'] = thresholds['SER_DRV'][:]
    ldo = [1.193*.98*(1+32400*(1-RF)/(10000*(1+RF)))-.1e-6*32400*(1+RF),
           1.193*1.02*(1+32400*(1+RF)/(10000*(1-RF)))+.1e-6*32400*(1+RF)]
    aux = [.977*(1+1e6*(1-RF)/(88700*(1+RF)))-50e-9*1e6*(1+RF),
           1.017*(1+1e6*(1+RF)/(88700*(1-RF)))+50e-9*1e6*(1+RF)]
    source_max = 1e-6 + wd[1] + .1e-6 + .25e-6 + 1.5e-6 + .4e-6 + .025e-6
    return dict(
        classification='CALCULATED conditional design screens; hardware NOT RUN',
        precision_resistor_fraction=RF,
        fixture=fixture(),
        source=dict(
            SW_rise_V=loaded_threshold(20e3, 6190, 1.25, .015, 20e3, (0, .325)),
            SW_fall_V=loaded_threshold(20e3, 6190, 1.25, .015, 20e3, (4.40, 5.25)),
            qualifier_s=wd, complete_conditional_interval_s=[0., source_max],
            reserve_to_10us_s=10e-6-source_max,
            useful_dump_allocation_s=6.1e-6,
            node_C_allocation_F=100e-12,
            actual_complete_interval_s=[None, None], actual_positive_charge_C=None,
            internal_bridge_fault_coverage=None,
            counterexample=dict(SW_high_s=3e-6, SW_low_s=1e-6,
                                VIN_V=9., qualification_trips=False,
                                classification='Logic counterexample only; not a measured damaged buck')),
        interlock=dict(
            threshold_intervals_V=thresholds, LDO_min_max_V=ldo,
            converter_min_max_V=aux, SER_DRV_start_V=aux[0]-.5-.2,
            aux_input_screen_A=aux[1]*(.045+.006+.000610)/(7.5*.75)+.005,
            charger_flat_power_W=aux[1]*.051,
            charger_Tj_screen_C=70+aux[1]*.051*74.5,
            held_cap_screen_s=(300e-6*(aux[0]-.5-10.7)-2.036e-6)/.045,
            driver_local_droop_V=(.005*3e-6+.20e-6)/5e-6,
            READY_s=timer(153e3, 32768, .03),
            button_s=timer(244e3, 4096, .03),
            release_recovery_s=timer(100e3, 512, .03),
            diagnostic_current_max_A=5.25/(4700*(1-RF)),
            rejected_DC_path_below_ohm=(thresholds['DIAG_VIN'][0]-thresholds['ZERO'][1])/
                                     (5.25/(4700*(1-RF))),
            SHDN_off_screen_V=20e-6*10000*(1+RF),
            SHDN_on_screen_V=3.8*10000*(1-RF)/(10000*(1-RF)+1000*(1+RF)),
            SAFE_input_start_V=10.5-.5-.008*47*(1+RF),
            SAFE_cap_hold_s=5e-6*(10.5-.5-.008*47*(1+RF)-6)/.008,
            fast_source_loss_allocation_s=1e-6+.1e-6+.2e-6+1.5e-6+.4e-6+.025e-6,
            actual_loss_interval_s=[None,None], actual_hold_s=None,
            actual_persistent_short_rejection=None),
    )


def render_md(d):
    s = '\n## Round 3 — source, interlock and external fixture screens\n\n'
    s += ('FIX3_SOURCE_TRIGGER.md and FIX3_INTERLOCK.md specify the circuits. '
          'These calculations allocate test limits; every physical result remains OPEN. '
          'The source interval applies only to a qualifying continuous high / input-collapse signature.\n\n')
    s += '|Quantity|Conditional result|\n|---|---|\n'
    for name, value in d['source'].items():
        s += f'|Source: {name}|{json.dumps(value)}|\n'
    for name, value in d['interlock'].items():
        s += f'|Interlock: {name}|{json.dumps(value)}|\n'
    for name, value in d['fixture'].items():
        s += f'|External fixture: {name}|{json.dumps(value)}|\n'
    return s


if __name__ == '__main__':
    (HERE/'FIX3_CALCULATIONS.json').write_text(json.dumps(calculate(), indent=2)+'\n')
