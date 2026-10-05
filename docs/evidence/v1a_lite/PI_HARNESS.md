# Pi 5 power harness — FIX1, 2026-10-05

**DECISION:** use the 40-pin header's physical **2 and 4 (+5 V)** and **6 and 9 (GND)**, with two matched branches per polarity. J502 remains JST **B2P-VH-FB-B(LF)(SN)**, pin 1 VOUT_PI, pin 2 GND. No schematic interface change is needed. This is a harness specification for qualification, not permission to connect a Pi now. **NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**

## Interface comparison and Pi settings

| Interface | Engineering consequence |
| --- | --- |
| Header 2/4 and 6/9 — selected | Direct power connection; requires polarity control, current-sharing checks and mechanical retention. Both 5 V pins must be populated at 5 A. No PD negotiation. |
| USB-C power cable | Native Pi inlet and reversible mating. A compliant 5 A solution needs a source advertising the optional 5 V/5 A PD profile and a suitable 5 A cable. J502's two conductors alone cannot implement PD; an ordinary cut cable is not a qualified 5 A interface. Adds an external source controller/cable assembly for this design. |

**EVIDENCE:** Raspberry Pi's [USB power white paper](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf), release 1, pp7–8, describes header powering and the default 3 A assumption without PD. After the complete source and harness pass 5 A qualification, set `usb_max_current_enable=1` in `/boot/firmware/config.txt` to allow 1.6 A for USB peripherals instead of 600 mA. `PSU_MAX_CURRENT=5000` in bootloader configuration declares source capability and automatically enables that allowance. Neither setting increases electrical capacity or replaces qualification. Record firmware/settings with the test results; this task changes no Pi configuration. Also see the official [power documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply) and [configuration reference](https://www.raspberrypi.com/documentation/computers/configuration.html).

**EVIDENCE / OPEN RISK — header pin limits:** the [official pin diagram](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png) establishes physical pin identities. The cited Pi pages do **not** establish a guaranteed continuous 5 A rating for one header pin, nor a numeric per-contact rating for the installed Pi 5 male header. GPIO signal drive-current limits are unrelated to its 5 V power contacts. Do not claim a generic “3 A per pin” as a Pi specification. The selected Harwin female contact is rated **3 A/contact**, so each branch must measure **≤3 A**, with nominal 2.5 A sharing at total 5 A; lower temperature-derated or Pi-header limits govern. Obtain the installed male-header rating or a reviewed temperature-rise qualification before releasing 5 A operation. An open contact can put 5 A into its partner: the 7 A F301 does not protect against this fault. Contact retention and single-contact-fault response remain mandatory release checks.

## Harness parts and construction

| Location | Exact part / construction |
| --- | --- |
| J502 cable mate | JST **VHR-2N**, one housing; **SVH-41T-P1.1**, two contacts. AWG18 stranded copper, insulation OD 1.7–3.0 mm. Use matching JST crimp tooling/process. |
| Trunk | One red + one black AWG18 conductor, each **150 mm maximum** from J502 contact to insulated splice. Route together; strain relief at both ends. |
| Fanout | Two red and two black AWG22 stranded copper branches, each **50 mm maximum**, equal length within each polarity. One branch per contact. Insulated, mechanically supported splices; never force two wires into a single-wire crimp. |
| Pi mate | Harwin **M20-1070500**, 2×5 housing over Pi physical pins 1–10, four **M20-1160042** contacts in positions mating with Pi 2,4,6,9; remaining cavities empty. Harness path ≤200 mm one-way. |
| Mechanical key | Captive insulating carrier registered to Pi mounting holes and the pin-1 end, with an asymmetric stop preventing rotation or a one-row/one-column offset. This is required because the stock Pi header and Harwin housing are **not polarized**. Carrier dimensions/fit verification remain OPEN; labels alone do not make a key. |

[JST VH datasheet](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), pp1–2/4, supports the mating family and AWG18 contact choice. Its **shrouded** header rating is **7 A with AWG18**; do not use the 10 A/AWG16 standard-header rating. [Harwin housing](https://www.harwin.com/products/M20-1070500) and [contact](https://www.harwin.com/products/M20-1160042) identify the compatible pair, 22–30 AWG crimp range, 0.64 mm square mating pins and 3 A/contact. Verify actual Pi pin dimensions/plating and housing engagement before acceptance. Housing temperature ceiling is 85°C; contact's higher rating does not raise it. Wire insulation must support the reviewed thermal/fault envelope; exact wire supplier/insulation and splice process qualification remain OPEN.

**Mating-face drawing — looking into the cable sockets, wires behind the page.** Numbers below denote the **destination's physical pin**, not assumed molded housing numbering. Register the Pi carrier at the pin-1 end. The board/header view is the left-right mirror of the cable mating face.

```text
J502 cable mate VHR-2N: align molded latch with J502 shroud lock.
Identify cavity 1 from manufacturer's drawing + continuity to square PCB pad 1.
Do not infer polarity from wire-exit view; that view is mirrored.

   cavity mating J502.1 (+)          cavity mating J502.2 (GND)
         red AWG18                         black AWG18
            |                                  |
       insulated splice                  insulated splice
        /          \                      /          \
  red AWG22   red AWG22            black AWG22   black AWG22
    Pi.2        Pi.4                  Pi.6          Pi.9

Pi cable SOCKET mating face, pin-1 end at top (carrier key at upper right):
           +---------------+  asymmetric carrier / pin-1 datum
           |  2 +  |  1 -- | < KEY
           |  4 +  |  3 -- |
           |  6 -  |  5 -- |
           |  8 -- |  7 -- |
           | 10 -- |  9 -  |
           +---------------+
-- = no cable contact. Pi physical 1 is 3.3 V; NEVER connect J502.1 to it.
```

Require unpowered continuity verification against the actual Pi board pin-1 mark and official pinout, including both 5 V branches, both returns and isolation from all other pins. Keep USB-C power, PoE and externally back-powered USB supplies disconnected during header-powered qualification/integration.

## Voltage-drop allocation and acceptance

**REQUIREMENT:** Pi terminals ≥4.75 V at 5 A; <5.5 V including fault overshoot and uncertainty. **CALCULATION:** nominal raw setpoint `1 + 100k/24.6k = 5.06504 V`. The absolute nominal ceiling for the **entire** raw-output-to-Pi round trip is `(5.06504−4.75)/5 = 63.01 mΩ`. This includes F301, board copper, both mating interfaces, splices, positive conductors and returns. It is not a guaranteed harness allowance.

**DECISION — qualification allocation:** harness round-trip resistance (J502 board pads through both mates, splices and cable to Pi board header pins) **≤40 mΩ at the hottest qualified condition**, corresponding to ≤200 mV drop/1 W at 5 A. This requires instantaneous voltage at J502 ≥**4.95 V**, already accounting for upstream losses, ripple and transient droop. If J502 falls below 4.95 V, the 40 mΩ allocation fails: use `R_harness,max = (V_J502,min − 4.75 V − measurement uncertainty)/5 A`. No claim is made that the existing regulator meets that minimum.

**CALCULATION / ASSUMPTION:** copper resistivity 0.01724 Ω·mm²/m at 20°C, AWG18 area 0.823 mm² and AWG22 0.326 mm²: trunk loop `2×0.15×0.01724/0.823 = 6.28 mΩ`; equal parallel fanout loop `2×(0.05×0.01724/0.326)/2 = 2.64 mΩ`. Wire-only total ≈8.92 mΩ cold, ≈11.20 mΩ at an illustrative 85°C using 0.00393/K. This leaves ≈28.8 mΩ for hot contacts/splices under the selected 40 mΩ screen. Actual wire resistance governs. JST permits 10 mΩ/contact initially and 20 mΩ after testing: its two contacts alone can exhaust the allowance after aging. Catalog maxima therefore do **not** guarantee compliance; four-wire measurement, thermal cycling/mating aging and replacement limits are needed.

The C2 cold F301 screen is 9 mΩ/45 mV at 5 A, leaving nominal `63.01−40−9 = 14.01 mΩ` equivalent for board losses and regulator/ripple uncertainty. Hot fuse resistance must be measured; do not treat 5.065 V nominal as the worst-case source voltage.

**PASS conditions before Pi use:** dummy load at the remote connector with intended remote capacitance; Kelvin-measured hot/aged R ≤40 mΩ and terminal voltage minus uncertainty ≥4.75 V through load steps; each power/ground contact ≤3 A or lower qualified derating; acceptable connector/wire temperature and full F301 clearing coordination for overload/short and single-branch faults. Exact source current/hiccup, remote capacitance, male-header rating, aging, thermal limits and fuse total-clearing evidence remain OPEN. Measure harness inductance/remote capacitance for OV testing; a resistance pass alone cannot close review finding 1. See [bench tests](BENCH_TESTS.md).
