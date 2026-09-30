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
|TPS7A16|[TI SBVS171F,October2015; IN/EN40V recommended, PG5V recommended, regulation](https://www.ti.com/lit/ds/symlink/tps7a16.pdf)|
|TPS3808|[TI SBVS050N,August2026; thresholds and20us typical SENSE propagation](https://www.ti.com/lit/ds/symlink/tps3808.pdf)|
|MURATA10|[Murata exact family/ordering code; DC-bias C remains OPEN](https://www.murata.com/en-us/products/productdetail?partno=GRM32ER71H106KA12%23)|
|PASSIVES|[Vishay28758,10April2026; 0.1%25ppm/K E-series order-code candidates, not purchase stock confirmation](https://www.vishay.com/docs/28758/tnpw_e3.pdf)|

Additional exact document revisions/files, usage, license, modifications and attribution are registered in [SOURCES.json](SOURCES.json). PDFs/text are isolated under third_party; failed local fetches are explicitly web-read without invented hashes.

|ID / revision|Primary URL / file / status / use|
|---|---|
|tps7a16 / SBVS171F, October2015|[Candidate inspected; not selected if absent from freeze register](https://www.ti.com/lit/ds/symlink/tps7a16.pdf); `third_party/documents/gate4a/tps7a16.pdf`; FETCHED; REFERENCED|
|tps3808 / SBVS050N, August2026|[Candidate inspected; not selected if absent from freeze register](https://www.ti.com/lit/ds/symlink/tps3808.pdf); `third_party/documents/gate4a/tps3808.pdf`; FETCHED; REFERENCED|
|tps2662 / SLVSDT4F, December2021|[Candidate inspected; not selected if absent from freeze register](https://www.ti.com/lit/ds/symlink/tps2662.pdf); `third_party/documents/gate4a/tps2662.pdf`; FETCHED; REFERENCED|
|tmux1511 / SCDS390B, March2025|[Candidate inspected; not selected if absent from freeze register](https://www.ti.com/lit/ds/symlink/tmux1511.pdf); `third_party/documents/gate4a/tmux1511.pdf`; FETCHED; REFERENCED|
|lt4363 / Rev C, January2024; web-read exact PDF|[surge-stopper feedback, current/timer, pins and SOA](https://www.analog.com/media/en/technical-documentation/data-sheets/4363fb.pdf); `no downloaded file`; WEB_READ; local download OPEN; REFERENCED|
|ltc3115 / Rev E,2023-04-07; web-read exact PDF|[p38 6–40 V to12 V example; feedback, RUN, startup and layout](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC3115-1.pdf); `no downloaded file`; WEB_READ; local download OPEN; PROPOSED ADAPTATION of p38 functional block; no CAD copied; input limiting/hold-up/RUN changes documented|
|bsc034 / Rev2.3,2020-05-06; primary dgdl PDF verified with web tool|[selected series FET RDS, gate charge, voltage and SOA](https://www.infineon.com/dgdl/Infineon-BSC034N06NS-DataSheet-v02_03-EN.pdf?fileId=db3a304342371bb001424c65286a70be); `no downloaded file`; WEB_READ; local download OPEN; REFERENCED|
|lm61460 / SNVSBD5D, July 2022|[FB/SW/VIN/BIAS limits; input bank, inductance, layout](https://www.ti.com/lit/ds/symlink/lm61460.pdf); `third_party/documents/gate4a/lm61460.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|tps2663 / SLVSE94G, June 2024|[SHDN, OVP, physical cutoff conditions](https://www.ti.com/lit/ds/symlink/tps2663.pdf); `third_party/documents/gate4a/tps2663.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|ltc7001 / Rev G, primary PDF/product page verified with web tool|[loaded bootstrap, gate drive and delay](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc7001.pdf); `no downloaded file`; WEB_READ; local download OPEN; REFERENCED|
|ucc27511 / SLUSAW9F,November2014|[12 V gate drive and min/max propagation](https://www.ti.com/lit/ds/symlink/ucc27511.pdf); `third_party/documents/gate4a/ucc27511.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|adg4612 / Rev0,2010-10-28; web-read exact PDF|[power-off isolation and16 V blocking](https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf); `no downloaded file`; WEB_READ; local download OPEN; REFERENCED|
|fdb33 / FDB33N25/D,Rev3,January2022|[LT4363 pass-FET research candidate, linear SOA](https://www.onsemi.com/pdf/datasheet/fdb33n25-d.pdf); `third_party/documents/gate4a/fdb33.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|wfm / 30387, 4 August 2022|[95 C terminal and pulse limits](https://www.vishay.com/docs/30387/wfm.pdf); `third_party/documents/gate4a/wfm.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|tnpw / 28758,2026-04-10|[ordering codes, temperature and voltage/power ratings](https://www.vishay.com/docs/28758/tnpw_e3.pdf); `third_party/documents/gate4a/tnpw.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|we10 / 001.000, 7 February 2025|[L, DCR, bias curve, footprint](https://www.we-online.com/components/products/datasheet/74437636351002.pdf); `third_party/documents/gate4a/we10.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|tlv3201 / SBOS561C,May2024|[offset/hysteresis and delay conditions](https://www.ti.com/lit/ds/symlink/tlv3201.pdf); `third_party/documents/gate4a/tlv3201.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|lm4040 / SLOS456Q,April2026|[independent shunt clamp bias/current](https://www.ti.com/lit/ds/symlink/lm4040.pdf); `third_party/documents/gate4a/lm4040.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|csd18540 / SLPS488B,April2017|[protected crowbar pulse and gate charge](https://www.ti.com/lit/ds/symlink/csd18540q5b.pdf); `third_party/documents/gate4a/csd18540.pdf`; FETCHED; REFERENCED; LTC3115 p38 block PROPOSED ADAPTATION only|
|pch / PCH English catalog,2 pages; no explicit revision shown; pinned by SHA256|[PCH1V471MCL1GS exact capacitance/ESR/voltage row and ordering, p2](https://www.nichicon.co.jp/english/_assets/images/products/catalog/corporate/digital/PCH_e.pdf); `third_party/documents/gate4a/pch.pdf`; FETCHED; REFERENCED|
|ina228 / SLYS021A, May2022|[ADCRANGE and shunt input/accuracy limits](https://www.ti.com/lit/ds/symlink/ina228.pdf); `third_party/documents/gate4a/ina228.pdf`; FETCHED; REFERENCED|

Exact suffix availability/lifecycle is OPEN before procurement. Manufacturer order-code construction is the basis for passive candidates. Pin/land/package verification remains mandatory for every changed MPN, including proposed THT L201 and changed TVS/fuse. The register exposes the missing autonomous FAULT_TRIGGER rather than inventing its MPN.


FIX-S03: TI SN74AHCT1G125 SCLS378P March2024, exact SN74AHCT1G125DBVR order entry, accessed2026-09-30. [Datasheet](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf), [order entry](https://www.ti.com/product/SN74AHCT1G125/part-details/SN74AHCT1G125DBVR). Studied identity, DBV pins, voltage/DC/loading and partial-power limitations; REFERENCED only. TI copyright, no open redistribution license inferred. No upstream file/circuit/PCB copied or modified; two-channel proposal replaced with two single-channel circuits. Attribution by manufacturer/document/URLs.
