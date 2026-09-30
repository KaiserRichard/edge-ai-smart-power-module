# Gate4a primary sources and third-party provenance

**REFERENCE/PROPOSED ADAPTATION ONLY.** No upstream source edited and no third-party PCB copied. Native CAD remains untouched. Downloaded PDFs/text stay isolated in ignored `third_party/documents/gate4a/`; exact fetched hashes and paths are in [download register](../../../../third_party/gate4a_downloads.json). A failed download has no invented hash; web-read revision and URL remain the evidence.

All manufacturer documents are copyrighted; no open-source or redistribution license is assumed. Attribution is the manufacturer and linked primary URL. Imported project evidence uses the exact commits and file hashes in [INPUT_PROVENANCE.json](INPUT_PROVENANCE.json), with no merge or source modification.

|Source ID|Exact document/source and function|
|---|---|
|PR15|[Pinned51d1c2f exported inventory/netlist; footprint review evidence only](INPUT_PROVENANCE.json)|
|PR17|[Pinned84c991fe TVS/fuse audit; D101/F101 owner selection](INPUT_PROVENANCE.json)|
|G3B|[Inherited primary revisions, source bound and published magnetic curves](../sheet03/gate3b/SOURCES.json)|
|PATH|[Pinnedebe51b9e path analysis; BSC034 pair explicitly substituted back](INPUT_PROVENANCE.json)|
|G2C|[Inherited detector error/timing and component stress review](../sheet03/GATE2C_REVIEW_CLOSURE.md)|
|COMMON|[Common timing, supply, PG/fault and default-off proposed wiring](TIMING_AND_LOGIC.md)|
|G1D|[Protected crowbar and WFMB ballast construction](../sheet03/GATE1D_PULSE_REVIEW.md)|
|RAW_DUMP|[TASK5 two-node energy analysis; candidate second dump](RAW_NODE_ENERGY.md)|
|HOOKS|[TASK3 authored test-fixture requirements](TEST_HOOKS.md)|
|HOLD|[TASK2 held-driver supply and source independence](AUX_BRANCH_FIX.md)|
|M03|[Powered-off clamp/isolation; reference sink removed](TIMING_AND_LOGIC.md)|
|LT4363|[ADI Rev C, January2024; adjustable surge stopper, SNS/OUT/TMR](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf)|
|ON|[onsemi Rev3, January2022; FDB33N25TM research pass FET](https://www.onsemi.com/pdf/datasheet/fdb33n25-d.pdf)|
|LTC3115|[ADI Rev E, April2023; p38 example PROPOSED ADAPTATION](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf)|
|TPS7A16|[TI SBVS171G; IN/EN40V recommended, PG5V recommended, regulation](https://www.ti.com/lit/ds/symlink/tps7a16.pdf)|
|TPS3808|[TI SBVS050L; thresholds and20us typical SENSE propagation](https://www.ti.com/lit/ds/symlink/tps3808.pdf)|
|MURATA10|[Murata exact family/ordering code; DC-bias C remains OPEN](https://www.murata.com/en-us/products/productdetail?partno=GRM32ER71H106KA12%23)|
|PASSIVES|[Vishay28758,10April2026; 0.1%25ppm/K E-series order-code candidates, not purchase stock confirmation](https://www.vishay.com/docs/28758/tnpw_e3.pdf)|

Additional primary documents inspected for the new review are registered below. Every use is REFERENCED, except the LTC3115 p38 functional block is a PROPOSED ADAPTATION: input limiter, held-output diode/capacitance and RUN sequencing are added, and capacitor/package candidates require review. No source files are modified.

- [tps7a16](https://www.ti.com/lit/ds/symlink/tps7a16.pdf): revision to be read from pinned PDF; `third_party/documents/gate4a/tps7a16.pdf`; local pinned reference; FETCHED.
- [tps3808](https://www.ti.com/lit/ds/symlink/tps3808.pdf): revision to be read from pinned PDF; `third_party/documents/gate4a/tps3808.pdf`; local pinned reference; FETCHED.
- [tps2662](https://www.ti.com/lit/ds/symlink/tps2662.pdf): revision to be read from pinned PDF; `third_party/documents/gate4a/tps2662.pdf`; local pinned reference; FETCHED.
- [tmux1511](https://www.ti.com/lit/ds/symlink/tmux1511.pdf): revision to be read from pinned PDF; `third_party/documents/gate4a/tmux1511.pdf`; local pinned reference; FETCHED.
- [lt4363](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf): Rev C, January 2024; `no local file`; surge-stopper feedback, current/timer, pins and SOA; DOWNLOAD OPEN.
- [ltc3115](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf): Rev E, April 2023; `no local file`; p38 6–40 V to12 V example; feedback, RUN, startup and layout; DOWNLOAD OPEN.
- [bsc034](https://www.infineon.com/assets/row/public/documents/non-assigned/49/infineon-bsc034n06ns-datasheet-en.pdf): Read pinned PDF title/revision; `no local file`; selected series FET RDS, gate charge, voltage and SOA; DOWNLOAD OPEN.
- [lm61460](https://www.ti.com/lit/ds/symlink/lm61460.pdf): SNVSBD5D, July 2022; `third_party/documents/gate4a/lm61460.pdf`; FB/SW/VIN/BIAS limits; input bank, inductance, layout; FETCHED.
- [tps2663](https://www.ti.com/lit/ds/symlink/tps2663.pdf): SLVSE94G, June 2024; `third_party/documents/gate4a/tps2663.pdf`; SHDN, OVP, physical cutoff conditions; FETCHED.
- [ltc7001](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf): Read pinned PDF title/revision; `no local file`; loaded bootstrap, gate drive and delay; DOWNLOAD OPEN.
- [ucc27511](https://www.ti.com/lit/ds/symlink/ucc27511.pdf): Read pinned PDF title/revision; `third_party/documents/gate4a/ucc27511.pdf`; 12 V gate drive and min/max propagation; FETCHED.
- [adg4612](https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf): Rev 0, October 2010; `no local file`; power-off isolation and16 V blocking; DOWNLOAD OPEN.
- [fdb33](https://www.onsemi.com/pdf/datasheet/fdb33n25-d.pdf): Read pinned PDF title/revision; `third_party/documents/gate4a/fdb33.pdf`; LT4363 pass-FET research candidate, linear SOA; FETCHED.
- [wfm](https://www.vishay.com/docs/30387/wfm.pdf): 30387, 4 August 2022; `third_party/documents/gate4a/wfm.pdf`; 95 C terminal and pulse limits; FETCHED.
- [tnpw](https://www.vishay.com/docs/28758/tnpw_e3.pdf): Read pinned PDF title/revision; `third_party/documents/gate4a/tnpw.pdf`; ordering codes, temperature and voltage/power ratings; FETCHED.
- [we10](https://www.we-online.com/components/products/datasheet/74437636351002.pdf): 001.000, 7 February 2025; `third_party/documents/gate4a/we10.pdf`; L, DCR, bias curve, footprint; FETCHED.
- [tlv3201](https://www.ti.com/lit/ds/symlink/tlv3201.pdf): Read pinned PDF title/revision; `third_party/documents/gate4a/tlv3201.pdf`; offset/hysteresis and delay conditions; FETCHED.
- [lm4040](https://www.ti.com/lit/ds/symlink/lm4040.pdf): Read pinned PDF title/revision; `third_party/documents/gate4a/lm4040.pdf`; independent shunt clamp bias/current; FETCHED.
- [csd18540](https://www.ti.com/lit/ds/symlink/csd18540q5b.pdf): SLPS488B, April 2016; `third_party/documents/gate4a/csd18540.pdf`; protected crowbar pulse and gate charge; FETCHED.

Exact suffix availability/lifecycle is OPEN before procurement. Manufacturer order-code construction is the basis for passive candidates. Pin/land/package verification remains mandatory for every changed MPN, including proposed THT L201 and changed TVS/fuse. The register intentionally exposes the missing autonomous FAULT_TRIGGER rather than inventing its MPN.
