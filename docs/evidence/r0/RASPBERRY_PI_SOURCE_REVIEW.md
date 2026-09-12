# Official Raspberry Pi source review

Date: 2026-09-11. Reference-only inspection; no HAT circuit or artwork copied.

## Pinned sources

Exact URLs, local cache paths and SHA-256 digests: [raspberry_pi_sources.json](raspberry_pi_sources.json).

| Source | Revision inspected | Relevant location |
| --- | --- | --- |
| [HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf) | Build 2024-12-05, `6df06cc-clean` | Chapters 2, 4 and 6; colophon. Local PDF pages 10 and 13 visually reviewed |
| [USB Power Delivery on Raspberry Pi 5](https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%20Power%20delivery%20on%20Raspberry%20Pi%205.pdf) | Release 1; release-history date 2026-03-05; build 2026-03-17, `1026f0c6e305` | Printed pp. 5, 7–8; PDF pp. 6, 8–9 |
| [Power-supply documentation](https://github.com/raspberrypi/documentation/blob/5e2c40fe1125bb8ff7374de2c11c94761084eb1f/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc) | `5e2c40fe1125bb8ff7374de2c11c94761084eb1f` | Power requirements, low-voltage warnings, supply diagnostics |
| [Legacy HAT design guide](https://github.com/raspberrypi/hats/blob/348dbf88d870bf50d6b4f23dbe2b64d60363f23c/designguide.md) | `348dbf88d870bf50d6b4f23dbe2b64d60363f23c` | GPIO power and reverse-current circuit; historical context only |

Both PDFs identify CC BY-ND 4.0 in their colophons and contain additional resource-use terms. Preserve the unmodified originals and Raspberry Pi attribution. No PDF editing or redistribution of modified manufacturer artwork is planned. Pinned HTML-source license evidence is recorded in the manifest; no design-file reuse is based on it. Legacy guide licensing is not taken as permission to copy its circuit.

## Findings and design consequences

- OBSERVATION: Official Pi 5 guidance recommends a 5 V, 5 A supply when peripheral power is required. This is a supply capability reference, not a measured continuous consumption of every Pi 5 workload. **R1 inference:** a 5 A continuous module target is justified; actual transient load profile remains OPEN.
- OBSERVATION: HAT+ chapter 6 recommends 5.1 V/5 A for Power HAT+s. **R1 inference:** use 5.10 V as the candidate source setpoint and budget wiring losses separately. This does not certify V1 as HAT+.
- OBSERVATION: HAT+ has EEPROM, mechanical and standby-state requirements; chapter 4 requires a Power HAT+ to source current and tolerate concurrent USB-C supply. **R1 inference:** keep V1 a standalone module; avoid a HAT+ claim and require a reviewed integration harness, return-current analysis and reverse blocking.
- OBSERVATION: The 2026 USB-PD paper distinguishes 5 A negotiation from supplying the voltage. CC resistors alone advertise at most 3 A; a raw 5 V output does not implement the 5 A PD contract. The paper documents `PSU_MAX_CURRENT` and `usb_max_current_enable`. **R1 inference:** no custom PD controller in V1; host settings are a later, tested integration activity, never evidence of electrical current capability.
- OBSERVATION: HAT+ standby can leave 5 V present while host 3.3 V is absent. **R1 inference:** telemetry must address unpowered-host behavior; local 3.3 V pull-ups directly to a sleeping host are not automatically acceptable.
- OPEN RISK: The historical HAT guide's GPIO voltage range and old Pi reverse-diode examples are not proof of Pi 5 input protection or of a generic SBC's voltage tolerance. Final host/harness limits must be verified for the actual board before integration. A proposed 4.75–5.25 V module/load acceptance window is a project engineering target pending approval, not a newly asserted Pi 5 absolute rating.

## Conflicts and limitations

The HAT+ PDF served on audit day reports a December 2024 build, even though search/catalog timestamps can be newer. The embedded revision and local digest are the source identity. HAT+ supersedes the legacy HAT design framework; do not transplant old model-specific diode assumptions to Pi 5. All findings are documentary evidence. No Pi hardware was powered or firmware configuration changed.
