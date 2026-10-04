# Raspberry Pi power, HAT+, and watchdog evidence

> **FUTURE WBR REFERENCE — NOT PROJECT II V1 REQUIREMENTS**
> Scope classification added 2026-09-11. Preserve this source review as historical future work; it does not require a HAT, MCU or WBR power sequence in V1A. [Current V1A requirements](../../00_REQUIREMENTS.md).

Date: 2026-09-11. Documentary feasibility review only. No hardware test, firmware change, schematic, or layout was performed. Candidate architecture and GPIO assignments below require the project architecture gate before implementation.

## Provenance

All originals were referenced, not adapted or copied into a new circuit. Cached originals remain unmodified under ignored `third_party/`. No upstream source was edited. Existing PDF digests are in [the R0 manifest](../r0/raspberry_pi_sources.json).

| Source | Exact identity and relevant parts | Rights and use |
| --- | --- | --- |
| [Raspberry Pi HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf) | Build 2024-12-05, `6df06cc-clean`; chapters 2-4, 6-7, appendix A. Existing `third_party/documents/raspberry-pi-hat-plus.pdf`. | CC BY-ND 4.0 and colophon terms; Raspberry Pi attribution; unchanged reference. |
| [USB Power Delivery on Raspberry Pi 5](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf) | Release 1, release history 2026-03-05, build 2026-03-17, `1026f0c6e305`; printed pp. 5, 7-8. Existing `third_party/documents/raspberry-pi-usb-pd-release1.pdf`. | CC BY-ND 4.0 and colophon terms; unchanged reference. |
| [Pi documentation repository](https://github.com/raspberrypi/documentation/tree/5e2c40fe1125bb8ff7374de2c11c94761084eb1f) | Commit `5e2c40fe1125bb8ff7374de2c11c94761084eb1f`, remote HEAD checked 2026-09-11. `documentation/asciidoc/computers/raspberry-pi/{eeprom-bootloader,power-button,gpio-on-raspberry-pi,power-supplies}.adoc`, `computers/config_txt/boot.adoc`, `computers/configuration/reference.adoc`. New cache: `third_party/wbr_hat/raspberry_pi/`, with source basenames. | `LICENSE.md` contains CC BY-SA 4.0 text/link, despite its introductory sentence saying Attribution 4.0. Treat as BY-SA for reuse; attribution and share-alike if adapting licensed prose. This review independently summarizes facts, with no code or artwork reuse. |
| [Raspberry Pi Linux, 6.12 comparison](https://github.com/raspberrypi/linux/tree/50f88724518d2eafe75bfae7923e90a8fe171c66) | `rpi-6.12.y` commit `50f88724518d2eafe75bfae7923e90a8fe171c66`; `arch/arm/boot/dts/overlays/{README,gpio-poweroff-overlay.dts,gpio-shutdown-overlay.dts}`, `drivers/power/reset/gpio-poweroff.c`, `drivers/watchdog/bcm2835_wdt.c`, `arch/arm64/boot/dts/broadcom/{bcm2712-rpi-5-b.dts,bcm2712.dtsi,bcm2712-rpi.dtsi}`, `arch/arm64/configs/bcm2712_defconfig`. | Kernel `COPYING` and per-file SPDX; `gpio-poweroff.c` GPL-2.0-only, DT sources GPL-2.0. Preserve notices for any future copied/adapted code. Reference only. Cache in `third_party/wbr_hat/raspberry_pi/`. |
| [Raspberry Pi Linux, 6.18 comparison](https://github.com/raspberrypi/linux/tree/cff533aec2fa601846766b32ff57204e0a61bed7) | `rpi-6.18.y` commit `cff533aec2fa601846766b32ff57204e0a61bed7`; the same two GPIO overlays, watchdog/poweroff drivers, `bcm2712-rpi.dtsi`, and `bcm2712_defconfig`. | Same source-license handling. Cache in `third_party/wbr_hat/raspberry_pi/rpi-6.18.y/`. |

The documentation `LICENSE.md` download succeeds; the earlier R0 `LICENCE` URL failure was a filename mismatch. Python HTTPS access encountered a local certificate-chain error, so verified-TLS `curl` was used successfully without disabling certificate validation. The freedesktop systemd HTML endpoint returned 403; this note relies on pinned Raspberry Pi watchdog documentation and source, not an assertion that this endpoint was inspected.

## HAT+ constraints

REQUIREMENT, summarized from the [HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf):

- Connect the 40-pin header and ID EEPROM; reserve GPIO0/1 for that EEPROM and 3.9 kohm pull-ups to Pi 3.3 V.
- The combined SPI/I2C supervisor belongs to Standard class, EEPROM `0x50`. Power MODE0/1 classes (`0x52`/`0x53`) prohibit GPIO2-27 connections; this design cannot claim MODE1 automatic power configuration.
- Use 3.3 V, 16-bit-addressed EEPROM with whole-array write protection, no clock stretching or paged I2C addresses. CAT24C32 is the recommended example. Provide WP access and 1 kohm pull-up.
- Tolerate arbitrary 5 V/3.3 V sequencing and STANDBY with Pi 3.3 V absent. GPIO startup pulls are not deterministic system control; GPIO2/3 already have approximately 2 kohm pulls.
- Supplying Pi through 5 V pins invokes Power HAT+ source-only/concurrent-USB-C tolerance. Specification minimum is 5.1 V/3 A; 5.1 V/5 A is recommended.
- Align at least one mounting hole; preserve PoE, flex connector and cooler access. Cooler guidance is at least 15 mm spacing, ideally 16 mm; underside components may require more.
- EEPROM names filesystem overlays; branding requires compliance.

PROPOSAL: Use four mounting points, a 16 mm starting stack height, and a Pi 5 Active Cooler clearance/airflow check. Treat 65 x 56 mm as a possible envelope, not a HAT+ dimensional mandate. Keep D435i cable directly at a Pi USB3 socket with strain relief outside the board. Final connector bodies, underside components, harness bends and tolerances require mechanical CAD review; no fit is validated here.

## Regulated 5 V input and delivery

OBSERVATION: The [official 2026 PD paper](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf) recommends 5 V/5 A for Pi 5 peripherals. The USB budget is 1.6 A aggregate when high-current mode is enabled, otherwise 600 mA. Only 5 V PDOs are requested; ordinary Type-C CC advertisement does not establish 5 A. For GPIO/non-PD power, EEPROM `PSU_MAX_CURRENT=5000` declares capability and skips negotiation. It automatically enables high USB current. The separate `/boot/firmware/config.txt` option `usb_max_current_enable=1` raises USB allowance without establishing supply capability. Either permits USB boot that would otherwise be restricted.

PROPOSAL: Keep the input compatible with an external regulated 5 V/5 A source. Optional 5.1 V adjustment can compensate losses only after source tolerance and Pi-terminal limits are reviewed; do not silently make adjustment mandatory. A 5 A source is the entire system budget, including supervisor and interface power, not 5 A guaranteed to Pi plus arbitrary HAT consumption. The final robot battery voltage remains OPEN and does not enter this input specification.

CALCULATION: At 5 A, each 10 milliohm of series resistance drops 50 mV and dissipates 0.25 W. Budget connector contacts, cable, fuse/eFuse, blocking FETs, current shunt, vias, copper and both return paths. Validate current sharing and temperature of the selected header/contact system; a generic 2.54 mm header name is not a current rating.

PROPOSAL: Protected external input feeds an always-on supervisor domain upstream of the switch. A separate low-loss, current-limited, reverse-blocked branch feeds Pi pins 2 and 4 using sufficient ground returns. The supervisor must sense actual Pi-branch voltage after commanding OFF. Pi-powered USB-C bypasses this branch: tolerate this electrically, but do not claim guaranteed hard cutoff or cold restart while USB-C also supplies Pi. Detect failure to discharge, latch a service/power-source fault, and stop restart retries. No V1 hold-up store is proposed; abrupt loss of the sole 5 V source cannot guarantee graceful filesystem shutdown.

OPEN RISK: Every crossing between always-on and Pi domains needs unpowered-I/O analysis, including pull-ups, MCU pins, IRQs, SPI MISO, INA228 alerts and protection diodes. Prefer Pi-referenced signal pull-ups and suitable isolation/buffering or rail-dependent output enables. A supervisor powered only from Pi 3.3 V cannot supervise its disappearance.

## GPIO budget proposal

These BCM GPIO numbers are provisional allocations, not a finished schematic. The [official GPIO source](https://github.com/raspberrypi/documentation/blob/5e2c40fe1125bb8ff7374de2c11c94761084eb1f/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc) identifies SPI0 and I2C roles; confirm physical orientation against Pi 5 CAD before capture.

| Function | BCM GPIO | Physical pin | Ownership/constraint |
| --- | --- | --- | --- |
| ID SDA/SCL | 0 / 1 | 27 / 28 | EEPROM only, address `0x50` |
| I2C SDA/SCL | 2 / 3 | 3 / 5 | INA228 and optional MCU slave; review pull-up combination |
| SPI0 CE0 / MISO / MOSI / SCLK | 8 / 9 / 10 / 11 | 24 / 21 / 19 / 23 | MCP2518FD and Linux controller driver |
| CAN interrupt | 25 | 22 | Dedicated controller IRQ |
| Shutdown request to Pi | 17 | 11 | Supervisor open-drain request, Pi-domain pull-up |
| Application health heartbeat | 27 | 13 | Pi output into unpowered-safe supervisor input |
| Late poweroff acknowledgement | 24 | 18 | Active-high candidate, external-cut mode only |
| Pi 5 V | Not GPIO | 2 / 4 | Switched power path, both contacts analyzed |
| Pi 3.3 V | Not GPIO | 1 / 17 | Host-domain reference; do not backfeed |
| Grounds | Not GPIO | 6, 9, 14, 20, 25, 30, 34, 39 | Multiple power returns and signal references |

GPIO7/CE1 and GPIO26 remain free under this proposal. Optional J2 power-button connection is a separate harness to Pi pads, not a 40-pin assignment.

## Poweroff and watchdog implications

OBSERVATION: [Pi bootloader documentation](https://github.com/raspberrypi/documentation/blob/5e2c40fe1125bb8ff7374de2c11c94761084eb1f/documentation/asciidoc/computers/raspberry-pi/eeprom-bootloader.adoc) gives Pi 5 `POWER_OFF_ON_HALT=1` PMIC STANDBY with 5 V still present. Pi 5 does not require `WAKE_ON_GPIO` for this; its dedicated button wakes it. `WAIT_FOR_POWER_BUTTON=1` together with power-off-on-halt waits for a button after input power returns. Thus an autonomous power-cycle recovery proposal uses `WAIT_FOR_POWER_BUTTON=0`. `BOOT_WATCHDOG_TIMEOUT` alone covers bootloader loading, not Linux runtime.

OBSERVATION: [Pi power-button documentation](https://github.com/raspberrypi/documentation/blob/5e2c40fe1125bb8ff7374de2c11c94761084eb1f/documentation/asciidoc/computers/raspberry-pi/power-button.adoc) identifies J2 as a normally-open momentary contact equivalent to the onboard button. Desktop may show a shutdown dialog, while Lite performs shutdown from a short press. Long hold forces hard shutdown. Therefore button-emulation timing is OS/configuration dependent; it is not a filesystem-safe hardware guarantee.

PROPOSAL: Keep two explicitly separate modes:

1. **Native standby:** normal Linux shutdown and `POWER_OFF_ON_HALT=1`; optional J2 harness for waking. No `gpio-poweroff` overlay. This does not remove Pi 5 V or necessarily power-cycle USB peripherals.
2. **External cutoff:** request Linux shutdown, wait for a kernel poweroff GPIO, then latch off the Pi power branch. The supervisor powers itself upstream and can re-enable after a measured discharge interval. The real cutoff mechanism is mandatory.

EVIDENCE: The [GPIO overlay README](https://github.com/raspberrypi/linux/blob/50f88724518d2eafe75bfae7923e90a8fe171c66/arch/arm/boot/dts/overlays/README) describes `gpio-shutdown` as a KEY_POWER event and `gpio-poweroff` as an external power-control mechanism that interferes with normal power-down. Its legacy GPIO3 wake wording must not override model-specific Pi 5 documentation. The [6.18 poweroff driver](https://github.com/raspberrypi/linux/blob/cff533aec2fa601846766b32ff57204e0a61bed7/drivers/power/reset/gpio-poweroff.c) emits active/inactive/active transitions with default 100 ms intervals; it waits 3000 ms for cutoff. It is not simply a sustained “OS is idle” flag. Both pinned kernels contain the same GPIO overlays; source availability is not Pi hardware validation.

Candidate configuration fragments, **not applied**:

```ini
# Pi bootloader EEPROM: only after validating the complete supply path.
PSU_MAX_CURRENT=5000
WAIT_FOR_POWER_BUTTON=0

# config.txt: GPIO17 request, with an external Pi-domain pull-up in hardware.
dtoverlay=gpio-shutdown,gpio_pin=17,active_low=1,gpio_pull=up

# config.txt: external-cutoff prototype ONLY, with working cutoff supervisor.
dtoverlay=gpio-poweroff,gpiopin=24
```

PROPOSAL: Gate acknowledgement acceptance by state and boot history; reject pull glitches. Latch the first qualified poweroff event instead of directly wiring the pulse sequence to enable. Any reboot, halt, watchdog expiry, shutdown timeout and MCU-reset interaction must be explicitly tested.

OBSERVATION: [Pi config.txt watchdog documentation](https://github.com/raspberrypi/documentation/blob/5e2c40fe1125bb8ff7374de2c11c94761084eb1f/documentation/asciidoc/computers/config_txt/boot.adoc#kernel_watchdog_timeout) recommends `kernel_watchdog_timeout` over just `dtparam=watchdog`: it sets `watchdog.open_timeout` and hands armed coverage to the OS. Configure systemd `RuntimeWatchdogSec` first; it is not enabled by default in Bookworm. Combined bootloader/kernel watchdog settings support continuous handoff on supported firmware. Timeouts require measured boot/shutdown latency and fault tests; this study does not choose production values.

EVIDENCE: Both pinned Pi kernel configurations enable `CONFIG_BCM2835_WDT=y`, `CONFIG_WATCHDOG_SYSFS=y` and `CONFIG_POWER_RESET_GPIO=y`; Pi DT exposes the watchdog. [The 6.18 driver](https://github.com/raspberrypi/linux/blob/cff533aec2fa601846766b32ff57204e0a61bed7/drivers/watchdog/bcm2835_wdt.c) has a 1 s minimum, 15 s default and approximately 16 s raw hardware counter range. Do not infer that every userspace timeout above 15 s is forbidden: kernel watchdog servicing can mediate hardware periods. Read the actual device identity and effective timeout on the chosen image.

PROPOSAL: Linux runtime watchdog, application health checks and external supervisor serve different failure cases. systemd remaining alive does not establish that D435i frames, CAN responses or perception processing remain fresh. The application health aggregator should toggle the external heartbeat only after its required checks pass. The MCU should use its own watchdog and brownout recovery, limit retries and retain a reason code. The robot controller must independently time out stale commands; this HAT is not an emergency-stop implementation.

## Required validation before implementation acceptance

Read-only Pi checks for the later bench campaign:

```sh
uname -a
cat /etc/os-release
vcgencmd version
sudo rpi-eeprom-config
vcgencmd get_throttled
vcgencmd pmic_read_adc
ls -l /dev/watchdog*
cat /sys/class/watchdog/watchdog*/identity
cat /sys/class/watchdog/watchdog*/timeout
cat /proc/cmdline
```

Expected evidence: actual image/kernel/firmware identities, declared source capability, watchdog identity and timeout, Pi voltage at load and fault history. Missing nodes or different timeouts are integration failures to resolve, not grounds to claim support from source alone. Do not open or write watchdog devices casually during inventory; opening can arm them.

Manual qualification follows the project bring-up gates: dummy-load short/reverse/overload tests; inrush and 0-to-5 A delivery tests; standby backfeed and all supply-sequencing permutations; concurrent-source and cutoff-bypass tests; then Pi with sacrificial storage. Scope request/ACK/heartbeat/5 V/3.3 V through cold start, ordinary reboot, requested shutdown, lost heartbeat, frozen application, OS hang, failed boot, supervisor reset and brownout. Expect exactly bounded recovery, no startup false cutoff, no backpowered host rail, and an explicit fault when OFF cannot be achieved. Test abrupt source removal as an ungraceful-loss case. Record voltage droop, current, temperature, acknowledgement latency, discharge time and restart counts before admitting Pi+D435i workload testing.
