# Raspberry Pi direct-power delivery - refined resistance chain

2026-09-14. **OPEN; no measured harness or guaranteed 5 A delivery.**

**Primary context:** Raspberry Pi [power-supply documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply), official source archived as `third_party/documents/raspberry-pi-power-supplies.adoc`; [prior primary-source review](../RASPBERRY_PI_DIRECT_POWER.md). The 5.1 V/5 A supply direction does not establish a GPIO-header absolute-maximum voltage/time/energy envelope or the rating of an unspecified socket. The common 4.63 V +/-5% undervoltage indication is not an operating-floor or damage specification. Pi model, exact direct-power interface and contact ratings remain OPEN.

## Explicit chain and classifications

LM61460 regulation point -> output-protection switch -> PCB copper/vias -> R401 -> J502 board connector -> mating contact -> harness -> adapter joints -> Raspberry Pi contacts/header/interface -> Pi rail. All return-path resistance is included in loop terms. No feedback sensing point was moved downstream of the open disconnect.

| Term | Resistance basis | Class / limits |
| --- | --- | --- |
| LM61460 regulation point | Divider nominal5.09836 V; previous static screen5.03827..5.15863 V | CALCULATED from datasheet reference/divider; FB leakage and dynamics incomplete. Not guaranteed all-condition limits |
| Output disconnect | 10 mOhm allocated | ASSUMED; actual part, hot RDS(on), number of devices OPEN |
| PCB copper and vias, both directions | 5 mOhm | ASSUMED; geometry/stackup/temperature OPEN |
| R401 | 2 mOhm nominal; +/-1%, component TCR +/-25ppm/C for2mOhm | DATASHEET, Vishay30131 rev29-Jun-2026; 25C-to100C example upper screen2.02379mOhm assumes reference25C and uses Rnom*1.01*(1+25e-6*75); not a measured shunt |
| J502 board contact | Phoenix1.4mOhm per pole reported; JST not separately specified | DATASHEET catalogue value for Phoenix, physical reference-plane decomposition OPEN |
| J502 mate / mating interface | Phoenix1.4mOhm after-test reported; JST mated contact10mOhm initial /20mOhm after test per pole | DATASHEET conditional. Splitting JST male/female/interface resistance is OPEN; do not count its mated datum twice |
| Complete J502 loop screen | Phoenix2*(1.4+1.4)=5.6mOhm; JST2*10=20 or2*20=40mOhm | CALCULATED screen. Phoenix sum ASSUMES independent additive catalogue contributions; it may double-count common test paths and is not a guaranteed pair bound |
| Harness positive + return | Belden8522 nominal6.5Ohm/1000ft; 0.2m one-way ->8.530mOhm | DATASHEET nominal DCR + ASSUMED length/20C reference -> CALCULATED loop. No guaranteed max DCR claimed |
| Hot harness | 9.871mOhm at assumed60C | CALCULATED using assumed0.00393/C copper model |
| Crimps / board solder / intermediate adapter joints not demonstrably included in contact datum | 5mOhm aggregate | ASSUMED; exact joint count/reference planes OPEN; do not silently omit or double-count after final vendor test planes are known |
| Pi physical5V contacts2/4 and two ground contacts | 10mOhm loop example | ASSUMED: two10mOhm contacts per polarity in parallel ->5+5mOhm. Equal sharing, wire branching and exact sockets OPEN |
| Pi interface internal copper/header to rail | Included only in the uncertain Pi/adapter allocation for screening | OPEN separate value; exact interface resistance needed to avoid missing internal loss |

**MEASURED:** none. Hot connector sensitivity uses an **ASSUMED 1.3 multiplier**, not a manufacturer law. Constant shunt and PCB/switch allocations in the tables are not temperature-corner bounds. Exact candidate systems and wire ordering: [connector review](CONNECTOR_HARNESS_QUALIFICATION.md).

The prior approximate **29.265mOhm external loop** is preserved in its original configuration: nominal wire7.06Ohm/1000ft over0.4m plus assumed5mOhm module connector,5mOhm adapter and10mOhm Pi contact loop. It excludes the assumed17mOhm internal path. It is a calculation, never a hardware measurement, and is not reused as an independent resistor in the refined chain.

## Reproduced sensitivity results

Use `Vdrop=I*R`, `Ploss=I^2*R`, and `Vpi=Vregulation-Vdrop`. Fixed terms total32mOhm: disconnect10 + PCB5 + nominal shunt2 + adapter5 + Pi10. Wire and connector add to that subtotal. The table below is generated from [configuration](qualification_assumptions.json) and [results](qualification_calculations.json) using `python3 scripts/calculate_r2_qualification.py`.

| Candidate sensitivity | Total loop (mOhm) | I (A) | Drop (V) | Loss (W) | Pi nominal (V) | Pi static-low (V) | Static-low minus assumed0.1V droop |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Phoenix additive hot sensitivity | 49.151 | 1 | 0.0492 | 0.0492 | 5.0492 | 4.9891 | 4.8891 |
| Phoenix additive hot sensitivity | 49.151 | 3 | 0.1475 | 0.4424 | 4.9509 | 4.8908 | 4.7908 |
| Phoenix additive hot sensitivity | 49.151 | 5 | 0.2458 | 1.2288 | 4.8526 | 4.7925 | 4.6925 |
| JST VH initial room maximum screen | 60.530 | 1 | 0.0605 | 0.0605 | 5.0378 | 4.9777 | 4.8777 |
| JST VH initial room maximum screen | 60.530 | 3 | 0.1816 | 0.5448 | 4.9168 | 4.8567 | 4.7567 |
| JST VH initial room maximum screen | 60.530 | 5 | 0.3027 | 1.5133 | 4.7957 | 4.7356 | 4.6356 |
| JST VH after-test hot sensitivity | 93.871 | 1 | 0.0939 | 0.0939 | 5.0045 | 4.9444 | 4.8444 |
| JST VH after-test hot sensitivity | 93.871 | 3 | 0.2816 | 0.8448 | 4.8167 | 4.7567 | 4.6567 |
| JST VH after-test hot sensitivity | 93.871 | 5 | 0.4694 | 2.3468 | 4.6290 | 4.5689 | 4.4689 |

**CALCULATED individual-loss examples:** the nominal2mOhm shunt contributes2/6/10mV and0.002/0.018/0.050W at1/3/5A. The assumed10mOhm disconnect contributes10/30/50mV and0.01/0.09/0.25W. The assumed5mOhm copper contributes5/15/25mV and0.005/0.045/0.125W. Every additional10mOhm costs50mV and0.25W at5A.

**Decision screen only:** adopting the earlier unapproved4.75V floor and static-low5.03827V allows57.654mOhm total at5A; reserving another0.1V droop leaves37.654mOhm. The hot Phoenix additive scenario is49.151mOhm and therefore misses that dynamic screen, although it clears the static one. The JST after-test hot sensitivity is93.871mOhm and misses both. These findings do not assert the Pi fails at those exact voltages; they show that connector headline current and a nominal5.1V regulation target cannot close the stated resistance allocations.

**OPEN closure:** approve load operating envelope; select disconnect with a justified hot bound; determine board resistance; define separate contact measurement planes, wire length/maxDCR/temperature, Pi header/socket/adapter and current sharing; allocate dynamic droop from the real load transient. Do not raise feedback voltage to compensate without reviewing no-load/load-high voltage and protection thresholds. Raw buck capacitors sit before the disconnect and cannot be counted as Pi hold-up after it opens.

**R5 test plan:** four-wire resistance and voltage measurements at each chain node,1/3/5A dummy load, cold and hot equilibrium, record ambient and contact/connector/wire temperatures; apply approved load steps and record regulation/raw/protected/Pi rail simultaneously. Start with current-limited bench supply and dummy loads. Failure symptoms include excessive drop, thermal rise, unstable regulation, unequal pin current, undervoltage events or protection chatter. No hardware measurement occurred.
