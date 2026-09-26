# Edge AI Smart Power Module V1A

Context consolidated 2026-09-26 from the user brief, current KiCad sources, and the [latest engineering manager entries](../FINAL_MANAGER_REPORT.md). [Engineering state](03_ENGINEERING_STATE.md) controls release interpretation.

**KNOWN scope:** a standalone Project II compute-power module: 9–24 V-class regulated/protected direct-current (DC) input → input protection → LM61460 synchronous buck → approximately 5.1 V / 5 A target → independent output protection → 2 mΩ Kelvin shunt → Raspberry Pi 5 / edge-compute load. Voltage/current/power/energy telemetry uses INA228 and Inter-Integrated Circuit (I2C). Targets are not validated operating ratings.

**R2 BLOCKED; R3 BLOCKED.** The output-protection circuit is still OPEN; the current schematic cannot deliver input power through that boundary. No PCB is authorized.

| Functional sheet | Purpose |
| --- | --- |
| `01_INPUT_PROTECTION.kicad_sch` | Fuse, reverse-polarity path, electronic fuse (eFuse), input qualification |
| `02_BUCK_5V.kicad_sch` | LM61460 regulation at approximately 5.098 V |
| `03_OUTPUT_PROTECTION.kicad_sch` | OPEN independent protection boundary; separate raw/protected rails |
| `04_POWER_MONITOR.kicad_sch` | Four-terminal shunt, INA228, local supply and I2C domain interface |
| `05_IO_TEST.kicad_sch` | Load/host connections and test access; final interconnects OPEN |

The root `hardware/kicad/V1A.kicad_sch` owns this hierarchy. See [current architecture](02_V1A_ARCHITECTURE.md).

**Future system context supplied by the user:** Wheel-Biped Robot (WBR), approximately 13-series-cell lithium-ion battery, approximately 48 V nominal / 54.6 V maximum → main protection / power distribution board (PDB) → auxiliary conversion → V1A → Raspberry Pi 5. This is an approximate future integration direction, not a frozen robot electrical architecture or permission to connect that battery directly to V1A. V1A is not the complete WBR PDB.

Historical V1B supercapacitor work belongs to another subsystem/team member. Future integration requires its own reviewed interfaces. No Universal Serial Bus (USB) 3.x or D435i data is routed through V1A. Old WBR/HAT research remains reference material, not added V1A scope.
