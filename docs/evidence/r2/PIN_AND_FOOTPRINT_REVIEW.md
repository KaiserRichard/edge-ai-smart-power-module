# Pin and provisional-footprint audit

Date: 2026-09-12. Manufacturer IC pin tables and the cited diagrams were inspected.
All assignments remain provisional; absence of a footprint is a release blocker, not permission to substitute.

## IC and discrete pin connections

### U101 — TPS26630RGER

Source: TI SLVSE94G Table 5-1/Fig 8-7; RGE0024H drawing 4219016/A.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | IN | VIN_EFUSE_IN |
| 2 | IN | VIN_EFUSE_IN |
| 3 | B_GATE | INPUT_BGATE |
| 4 | DRV | INPUT_DRV |
| 5 | IN_SYS | VIN_FUSED |
| 6 | UVLO | INPUT_UVLO |
| 7 | OVP | INPUT_OVP |
| 8 | GND | GND |
| 9 | dVdT | INPUT_DVDT |
| 10 | ILIM | INPUT_ILIM |
| 11 | MODE | NC — intentional per review |
| 12 | SHDN | INPUT_SHDN |
| 13 | IMON | NC — intentional per review |
| 14 | FLT | INPUT_FLT |
| 15 | PGTH | INPUT_PGTH |
| 16 | PGOOD | BUCK_INPUT_PGOOD |
| 17 | OUT | VIN_PROTECTED |
| 18 | OUT | VIN_PROTECTED |
| 19 | NC | NC — intentional per review |
| 20 | NC | NC — intentional per review |
| 21 | NC | NC — intentional per review |
| 22 | NC | NC — intentional per review |
| 23 | NC | NC — intentional per review |
| 24 | NC | NC — intentional per review |
| 25 | EP | GND |

Footprint: `Package_DFN_QFN:Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm`

### Q101 — CSD19537Q3

Source: TI SLPS549B Fig 3-1 TOP VIEW; SLVSE94G Fig 8-7.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | S | VIN_FUSED |
| 2 | S | VIN_FUSED |
| 3 | S | VIN_FUSED |
| 4 | G | INPUT_BGATE |
| 5 | D | VIN_EFUSE_IN |
| 6 | D | VIN_EFUSE_IN |
| 7 | D | VIN_EFUSE_IN |
| 8 | D | VIN_EFUSE_IN |

Footprint: **UNASSIGNED — qualification required**.

### Q102 — BSS138

Source: onsemi BSS138/D Rev7 Apr2024 p1; TI SLVSE94G Fig 8-7.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | G | INPUT_DRV |
| 2 | S | VIN_FUSED |
| 3 | D | INPUT_BGATE |

Footprint: `Package_TO_SOT_SMD:SOT-23`

### U201 — LM61460AANRJRR

Source: TI SNVSBD5D sections6,7,9.2; SNVU621D Figure4-1; package4223976/H06/2026 PDFpp55-57.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | BIAS | GND |
| 2 | VCC | BUCK_VCC |
| 3 | AGND | GND |
| 4 | FB | BUCK_FB |
| 5 | PGOOD | NC — intentional per review |
| 6 | RT | BUCK_RT |
| 7 | EN/SYNC | BUCK_INPUT_PGOOD |
| 8 | VIN1 | VIN_PROTECTED |
| 9 | PGND1 | GND |
| 10 | SW | BUCK_SW |
| 11 | PGND2 | GND |
| 12 | VIN2 | VIN_PROTECTED |
| 13 | RBOOT | BUCK_RBOOT |
| 14 | CBOOT | BUCK_CBOOT |

Footprint: **UNASSIGNED — qualification required**.

### U401 — INA228AIDGSR

Source: TI SLYS021A Fig5-1/Table5-1; SBOU241E Fig6-1.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | A1 | GND |
| 2 | A0 | GND |
| 3 | ALERT | ALERT_LOCAL |
| 4 | SDA | SDA_LOCAL |
| 5 | SCL | SCL_LOCAL |
| 6 | VS | 3V3_LOCAL |
| 7 | GND | GND |
| 8 | VBUS | LOAD_5V1 |
| 9 | IN- | INA_IN_MINUS |
| 10 | IN+ | INA_IN_PLUS |

Footprint: `Package_SO:VSSOP-10_3x3mm_P0.5mm`

### U402 — TPS70933DBVR

Source: TI SBVS186H Fig5-1/Table5-1, 8.1.1, 7.3.4.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | IN | VOUT_PROTECTED |
| 2 | GND | GND |
| 3 | EN | NC — intentional per review |
| 4 | NC | NC — intentional per review |
| 5 | OUT | 3V3_LOCAL |

Footprint: `Package_TO_SOT_SMD:SOT-23-5`

### U403 — TCA9517DGKR

Source: TI SCPS242D sections6/9/11.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | VCCA | 3V3_HOST |
| 2 | SCLA | SCL_HOST |
| 3 | SDAA | SDA_HOST |
| 4 | GND | GND |
| 5 | EN | 3V3_LOCAL |
| 6 | SDAB | SDA_LOCAL |
| 7 | SCLB | SCL_LOCAL |
| 8 | VCCB | 3V3_LOCAL |

Footprint: `Package_SO:VSSOP-8_3x3mm_P0.65mm`

### R401 — WSL27262L000FEA

Source: Vishay30131 Rev29Jun2026 pp1-2; wide force pads and narrow Kelvin pads.

| Pin | Function | Net / intentional open |
| --- | --- | --- |
| 1 | I+ | VOUT_PROTECTED |
| 2 | S+ | SHUNT_KPLUS |
| 3 | S- | SHUNT_KMINUS |
| 4 | I- | LOAD_5V1 |

Footprint: **UNASSIGNED — qualification required**.

## Footprint evidence and limitations

U101: RGE0024H, 4x4 mm,0.5 mm pitch,2.7x2.7 mm EP25 and corner orientation verified against drawing4219016/A. Installed library uses IPC lands0.825x0.25 mm rather than the TI example0.58x0.24 mm; this is a provisional package/pin match, not approved paste/mask/layout.

U401: DGS 3x3 mm,10 leads,0.5 mm pitch,opposed rows and pad1 checked against TI drawing. U403: DGK 3x3 mm,8 leads,0.65 mm pitch and pad1 checked. U402: DBV SOT23-5,0.95 mm lead pitch and original TPS709 pin arrangement checked. Q102:onsemi SOT23-3 gate1/source2/drain3 checked. Detailed solder-process approval remains R4.

U201:RJR asymmetric HotRod needs exact lands; Q101:SON3.3x3.3 mm common drain copper is not a generic SO8; R401:Vishay wide force/narrow sense geometry and project pad numbering require a dedicated match. These remain unassigned.

C5750 2220 assignments cleared: installed generic pads1.8x5.4 mm at +/-2.55 mm have a3.3 mm inner gap, outside TDK recommended PA4.1-4.8/PB1.2-1.4/PC4-5 mm window. Exact vendor-recommended land review required.

L201 installed XAL8080 footprint cites the manufacturer source and uses1.78x7 mm lands at +/-2.58 mm; family envelope/pad identity checked from installed source metadata. Full mechanical confirmation against current manufacturer drawing remains OPEN, so assignment is cleared rather than advertised as verified.

Generic resistor/small-capacitor footprints define body-size intent only. Exact MPN working voltage, capacitance under bias and vendor land compatibility remain OPEN. Fuse/connectors have no assigned footprints. TVS/Schottky SMB has two pads; D102 pad1 is cathode. D101 is bidirectional and has no directional cathode requirement.

ERC maps U101 OUT17 as power_out and OUT18 as passive because both are the same internal supply; this removes a duplicate-driver declaration without suppressing a violation. EP25 remains separate GND. No ERC exclusions or downgraded severity rules are used.
