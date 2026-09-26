# F101 requirements and exact candidates

2026-09-14. **F101 remains OPEN; no final part/footprint selected.**

## Requirements worksheet

| Item | Class | Basis / disposition |
| --- | --- | --- |
| Normal input | REQUIREMENT | 9..24 V DC; adapter tolerance outside that range OPEN |
| Output | REQUIREMENT | 5.1 V x 5 A = 25.5 W |
| Efficiency | ASSUMED | 85/90/95% for input-current sensitivity; no measured efficiency |
| Normal maximum input current | CALCULATED | 3.333 A at 9 V/85%, before any loads omitted from the efficiency definition |
| Electronic limit | CALCULATED from TI/specs | TPS26630, RILIM=4.02k: nominal 4.478 A, screened 4.160..4.796 A |
| Controlled ramp | CALCULATED | CdVdT=100 nF: 24 V ramp 48 ms nominal, 37.34..63.29 ms screened; 44 uF bank charging about 22 mA nominal / 34 mA screened |
| Other inrush | OPEN | Upstream C101/C102 hot-plug, cable/source L/R, buck soft-start, actual load C and repetition; 34 mA is not total startup current |
| Fuse/eFuse relationship | PROPOSED, not approved | eFuse handles ordinary overload; fuse is backup isolation for TVS short, failed pass FET or wiring faults. Fuse must survive allowed startup yet clear within conductor/device damage limits |
| DC voltage rating | REQUIREMENT / OPEN | Must exceed maximum DC voltage during interruption, at least normal 24 V; surge/sustained fault ceiling OPEN. AC-only rating is insufficient |
| DC breaking capacity | OPEN | Must cover prospective current and circuit time constant at F101 under an eFuse/TVS fault |
| Prospective short current | OPEN | Source type, current limit/foldback, source capacitance and cable impedance unspecified; downstream 4.8 A eFuse limit does not bound a TVS short ahead of it |
| Ambient / thermal derating | OPEN | Local fuse temperature, enclosure, neighboring dissipation, PCB copper and repetitive pulse aging |
| PCB constraints | OPEN | Allowed fuse height/area, access, board copper, reflow/wave process; no PCB exists |
| Replaceable vs soldered | TRADEOFF | Cartridge/holder enables service but adds area, contacts, resistance and retention requirements. SMT is compact and automated but requires solder rework after clearing. No service policy selected |

**CALCULATED input current `25.5/(Vin*eta)`**, reproduced in [calculation JSON](qualification_calculations.json):

| Vin | 85% | 90% | 95% |
| --- | ---: | ---: | ---: |
| 9 V | 3.333 A | 3.148 A | 2.982 A |
| 12 V | 2.500 A | 2.361 A | 2.237 A |
| 24 V | 1.250 A | 1.181 A | 1.118 A |

Efficiency may describe the whole module or converter alone; if converter-only, add auxiliary demand and upstream loss consistently. A 3.15 A fuse is not justified by the output's 5 A rating or the 90% point. At 9 V/85%, a 5 A fuse carries 66.7% rating before derating; 6.3 A carries 52.9%. These fractions are screens, not approved sizing rules.

## Primary-source shortlist

[Schurter UMT 250](https://www.schurter.com/en/datasheet/typ_UMT_250.pdf) and [UMT-H](https://www.schurter.com/en/datasheet/typ_UMT-H.pdf), both dated 21.07.2026; local PDFs under `third_party/documents/r2_qualification_2026-09-14/`. Exact rating rows and their footnotes control; no headline AC rating is transferred to DC.

| Exact candidate | Construction | DC interruption evidence | Voltage drop at rated current | Typical melting I2t at 10x rated |
| --- | --- | --- | --- | ---: |
| UMT 250 `3403.0173.24`, 5 A time lag | SMT 3 x 10.1 mm, reel | 125 VDC / 100 A IEC; UL also lists 200 A at 63 VAC/DC and 35 A at 250 VDC, footnote3 | 76 mV typ, 300 mV max | 37.5 A2s |
| UMT 250 `3403.0174.24`, 6.3 A time lag | Same | Same row/footnote3 conditions | 71 mV typ, 300 mV max | 67.5 A2s |
| UMT-H `3403.0281.23`, 5 A time lag | SMT, 15.4 x 5.35 mm outline, reel | 125 VDC / 1500 A, footnote2 | 115 mV typ; max not given in table | 100 A2s |
| UMT-H `3403.0282.23`, 6.3 A time lag | Same | 125 VDC / 1500 A, footnote2 | 105 mV typ; max not given in table | 190 A2s |

**EVIDENCE:** UMT250 pp3-5 and UMT-H pp2-5 provide dimensions, derating, time-current bands and exact ordering. For these currents, 1.25x rated lasts at least 60 minutes; at 2x rated the maximum pre-arcing time is 120 s; at 10x it is 10..100 ms. Thus a healthy 4.796 A limiter cannot be assumed to clear any of these 5/6.3 A fuses. Backup intent must account for the eFuse failed-short case and the upstream TVS path. Typical melting I2t is **not maximum total-clearing I2t** or proof a semiconductor survives until isolation.

The smaller 5 A candidate has a typical rated-current hot resistance of `76mV/5A=15.2 mOhm`, maximum datum 60 mOhm at its rated-current test; UMT-H 5 A gives 23 mOhm typical. Those values are not cold-resistance specifications or predictions at 3.333 A. Include fuse dissipation in module efficiency/thermal budgeting.

**Derating evidence:** both datasheets provide curves referenced to 23 C. The operating-temperature range does not permit full rated current at its hot endpoint. Use the actual selected curve after local maximum temperature is approved. UMT-H test-board copper is 5 mm/35 um through 5 A and 7.5 mm/70 um at 6.3 A; these rating-test conditions cannot silently become V1A copper requirements. UMT250 also requires its stated test/assembly conditions to be reviewed.

**DECISION:** four defensible candidates, no winner. Higher interrupt capability has an area and I2t cost. The 1500 A rating cannot qualify an unspecified battery with larger available current; the 100/200 A alternative cannot be rejected or approved without the source envelope. A replaceable implementation needs an exact holder/cartridge combination and retention/resistance review if serviceability is chosen.

**Closure test plan:** obtain source short-circuit waveform/foldback and maximum voltage; overlay allowed startup pulses and temperature derating against minimum-melting curves; obtain maximum total-clearing data at the applicable DC voltage/L-R condition; compare TVS energy and conductor damage withstand. Later test with controlled source and dummy loads. Nuisance clearing, sustained overheating, failure to interrupt, or excessive let-through fail. No intentional destructive test or hardware order was performed.
