# INA228, Kelvin shunt and host power domains

Date: 2026-09-12. **REVIEW DRAFT; output protection is incomplete.**

SOURCE: TI SLYS021A (INA228) pin table, filtering Fig 8-1 and supply section;
SBOU241E Fig 6-1; Vishay 30131 dated 29-Jun-2026; TI SBVS186H (TPS709) and
SCPS242D (TCA9517). FUNCTION: measure delivered branch current and load-side
voltage and communicate over 3.3 V I²C. MODIFICATION: 2 mOhm Kelvin sensing,
10 Ohm/100 nF input filter, dedicated 3.3 V regulator and buffered host interface.
RATIONALE: low insertion loss, explicit energy boundary and powered-off isolation.

## Exact parts, pins and measurement boundary

- U401 **INA228AIDGSR**, DGS VSSOP-10: 1 A1=GND; 2 A0=GND; 3 ALERT_LOCAL;
  4 SDA_LOCAL; 5 SCL_LOCAL; 6 VS=3V3_LOCAL; 7 GND; 8 VBUS=LOAD_5V1;
  9 IN-=filtered Kelvin load side; 10 IN+=filtered Kelvin source side.
- R401 **WSL27262L000FEA**: 2 mOhm, +/-1%, component TCR +/-25 ppm/C,
  3 W rating subject to solder-point/board conditions. Project pin convention:
  1 force source, 2 sense source, 3 sense load, 4 force load. Vishay does not
  assign these schematic numbers; map wide force/narrow sense pads explicitly
  at footprint review. There is no generic two-terminal substitution.
- U402 **TPS70933DBVR**: 1 IN=VOUT_PROTECTED, 2 GND, 3 EN floating for internal
  enable, 4 NC, 5 OUT=3V3_LOCAL. This is TPS709, **not TPS709A/B**, whose DBV
  pin arrangements differ. EN is not tied to a potentially high fault input.
- U403 **TCA9517DGKR**: 1 VCCA=3V3_HOST, 2 SCLA=SCL_HOST, 3 SDAA=SDA_HOST,
  4 GND, 5 EN=3V3_LOCAL, 6 SDAB=SDA_LOCAL, 7 SCLB=SCL_LOCAL, 8 VCCB=3V3_LOCAL.

The power path is VOUT_PROTECTED → R401 force terminals → LOAD_5V1.
Kelvin sense wires begin at **separate resistor terminals** and meet the 10 Ohm
matched resistors near U401; 100 nF is connected between the filtered inputs.
The approximate differential RC corner is **79.6 kHz**. Filter resistors are
within TI's <=100 Ohm guidance, and 100 nF is within its recommended range.
Supply bypass is 100 nF directly between VS/GND. VBUS goes to the load node,
not the filtered shunt input or upstream converter rail.

At 5 A: shunt drop **10 mV**, dissipation **50 mW**. A +50 C shunt change has
0.125% TCR contribution before calibration. First-order current error at 25 C
is about 1.05% of reading +0.5 mA from shunt tolerance, gain and input offset;
filter bias, thermal EMF, noise, aging and calibration uncertainty add errors.
No accuracy acceptance band was supplied. ADCRANGE=1 gives +/-20.48 A analog
range. An example digital span of 10 A uses CURRENT_LSB=19.073486 uA and
SHUNT_CAL=2000; this is a scaling example, not a 10 A board rating or firmware.

**Positive current measures V1A's contribution crossing this shunt.** With V1A
supplying the load, the local regulator branches before the shunt, so reported
power excludes telemetry, shunt, disconnect, buck, input and upstream cable
losses. Voltage is relative to module GND, not a remote load's cable-return point.
It therefore does not measure whole-module efficiency.

With V1B/external power at LOAD_5V1, current toward local telemetry crosses the
shunt in reverse. That negative current includes local telemetry demand; the
monitor does not measure all current supplied by an external parallel source to
the load. ENERGY is unsigned and is not automatically signed net energy; CHARGE
and current require signed handling. Power loss resets accumulators and creates
measurement gaps. Log reset/overflow, reinitialize calibration and never infer
continuous energy across an unpowered interval.

## Supply and I²C details

TPS709 supplies only local monitor/buffer/pull-ups, not the host. It supports
30 V input and reverse-current protection. C403=1 uF/50 V input; C404 uses the
reviewed 22 uF/50 V TDK candidate. With tolerance/temperature allowance its
nominal upper value is about 30.4 uF including bypasses, below 47 uF; its screened
lower capacitance is well above the required **1.5 uF** for a 3.3 V output.
ESR must remain below 0.2 Ohm. Exact effective-capacitance qualification remains.
The large capacitor preserves an already reviewed candidate rather than assuming
an unverified small MLCC meets the minimum after bias.

TCA9517 logic is powered from local VCCB; host VCCA supplies the A-side reference.
TI permits either rail to be absent and specifies tolerant I/O with either supply
at zero. Both supplies have local 100 nF bypass. EN is tied only to local supply,
avoiding its internal VCCB pull-up injecting into a host GPIO. ALERT also remains
local with a 10k pull-up/test point; it is not connected directly to host.

Local SDA/SCL pull-ups: **10k to 3V3_LOCAL**. Host pull-ups: **4.7k to 3V3_HOST**.
Review host existing pull-ups before population. At 100 kHz and illustrative
100 pF local / 200 pF host capacitance, 0.8473 RC gives **847/796 ns**, respectively,
below the 1 us standard-mode rise-time target. These capacitance budgets are
implementation targets to verify, not measured cable values. Parallel pull-ups
can increase sink current; long cables can violate rise time.

TCA9517 B-side uses a static low offset (up to 0.6 V), compatible with INA228's
3.3 V input-low threshold. The INA228's guaranteed 0.4 V low and TCA9517's 0.4 V
B-side contention threshold leave little guaranteed margin. The 10k local pull-up
reduces sink current, but actual VOL/ACK/clock waveforms must be verified; no
guaranteed positive noise margin is claimed. Do not cascade another B-side buffer
or rise-time accelerator onto the local bus. This remains a host-interface
qualification item before release.

## Power-state matrix

| Module/local supply | Host supply | Externally powered LOAD | Electrical behavior |
| --- | --- | --- | --- |
| On, final disconnect on | On | No | Both buses active at 0x40; V1A branch current measured |
| On | Off | No | Host pull-ups/reference at zero; buffer prevents an intentional local supply path to host signals |
| Off | On | No | Local supply absent; buffer I/O tolerates host signals; monitor unavailable |
| Off | Off | No | No active telemetry; capacitors discharge through local circuitry |
| Off | Either | Yes | LOAD feeds shunt and local LDO; host access only if host is on; final disconnect must block upstream |
| Input returns | Either | Yes | Final disconnect must qualify prebias/OR-ing; current/energy accounting remains branch-specific |

The current schematic's sheet 03 is **always open**, so the first row requires
completion of the output block. There is no automatic transfer behavior in this
draft. Common ground must remain connected. INA228 analog input survival with
0-85 V applied while VS is off is explicitly supported; this is separate from
its digital I/O limits and from system protection.

## Required manual verification

Once a complete design is released and hardware bring-up gates permit: use
current-limited supplies and dummy loads; exercise every matrix row; measure
unpowered rail voltages/leakage rather than assuming zero leakage. Verify 0x40
ACK at 100 kHz, SDA/SCL VOL/rise time, no host/local rail tie, signed current
polarity, four-wire shunt value, VBUS boundary and reset/calibration recovery.
Unexpected off-rail voltage, stuck bus, incorrect sign, accumulation through a
reset or output backfeed fails review. No such bench test has been performed.
