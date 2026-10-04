# Connector and complete harness candidate qualification

2026-09-14. **J501/J502/J503 remain unselected; no connector footprint assigned.**

## J501/J502 complete power systems

Existing functions stay **J501: 1 VIN_RAW, 2 GND** and **J502: 1 LOAD_5V1, 2 GND**. One positive and one return contact each carry full loop current; two positions do not mean two parallel positive contacts. No input/output interchangeable power harness is approved.

| System | Exact board / mate / termination | KNOWN manufacturer basis | CALCULATED / ASSUMED / OPEN |
| --- | --- | --- | --- |
| A: JST VH shrouded | `B2P-VH-FB-B` header (label suffix LF/SN per catalog), `VHR-2N` housing, two `SVH-21T-P1.1` contacts | 3.96 mm pitch; 7 A AC/DC with AWG18 for shrouded type, 250 VAC/DC; 10 mOhm initial / 20 mOhm after-test contact maximum; -40..105 C including self-heating; positive housing lock; AWG22..18 contact, insulation OD1.7..3.0 mm | Belden8522 AWG18 fits nominal diameter. Hot resistance/current derating and actual crimp quality OPEN. At 5 A, two mated poles at initial 10mOhm each imply 100mV/0.5W loop loss; after-test 20mOhm each implies 200mV/1W at the specified contact-test basis, before hot extrapolation |
| B: Phoenix COMBICON | `1757242` MSTBA 2,5/2-G-5,08 header + `1757019` MSTB 2,5/2-ST-5,08 screw plug; contacts integral, no separate crimp contact | 2 positions/5.08 mm; 12 A nominal, rated III/2 voltage320V; header contact resistance1.4mOhm; plug1.3mOhm initial /1.4mOhm after durability test; tin contact; no positive locking | Exact hot end-to-end resistance/reference planes OPEN. Additive 2*(1.4+1.4)=5.6mOhm is a labelled screen, not a proven mated-pair maximum; avoid assuming catalogue R1/R2 means independently separable male/female contact pieces. Retention/strain relief must be provided for vibration |

Sources: [JST VH catalog](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), pp1-5, local `JST_VH.pdf` (no printed revision found); [Phoenix header](https://www.phoenixcontact.com/en-nz/products/pcb-header-mstba-25-2-g-508-1757242) and [mate](https://www.phoenixcontact.com/en-de/products/pcb-connector-mstb-25-2-st-508-1757019), live 2026-09-14 records. Phoenix operating temperature is -40..100 C dependent on derating; its cited vibration test is 10..150 Hz, 5g high-frequency segment, 2.5 h per axis. This does not establish suitability for an unspecified robot vibration profile.

**KNOWN wire candidate:** Belden `8522 002100` red and `8522 010100` black, 18 AWG 16x30 tinned copper, nominal insulation OD2.0 mm, nominal DCR6.5 Ohm/1000ft, -40..80 C. Primary [Belden8522 datasheet](https://catalog.belden.com/techdata/EN/8522_techdata.pdf), rev0.482, 20-Feb-2026, local `Belden_8522.pdf`. The 16 A wire figure is a single conductor in free air at 30 C; it is not an installed-harness current qualification. Gauge/diameter fit is a candidate screen, not a crimp pull-test result. The earlier Belden37118 example remains historical and is not assigned to VH; its insulation compatibility was not established.

**ASSUMED harness:** 0.2 m one-way length, one positive and one return, 20 C resistance reference and 60 C hot wire, copper coefficient0.00393/C. **CALCULATED:** cold loop8.530mOhm; hot loop9.871mOhm. Resistance tolerance, strand termination, bend routing, bundled ampacity and Pi-end transition OPEN. **ASSUMED hot contact sensitivity:** multiply the selected room contact screen by1.3; this is not a manufacturer contact-temperature model. Candidate A after-test hot screen52mOhm loop; B additive hot screen7.28mOhm. No connector hot resistance was measured.

**Manufacturing:** JST needs approved crimp tooling, strip length, applicator setup, pull tests and section inspection; header is through-hole with 1.6 mm PCB reference. The shrouded two-position header does not accept the two-position retainer-compatible housing; `VHR-2N` is the intended candidate mate. Phoenix's [exact plug record](https://www.phoenixcontact.com/en-pc/products/printed-circuit-board-connector-mstb-25-2-st-508-1757019) specifies AWG24..12 (flexible0.2..2.5mm2),7mm strip and0.5..0.6Nm torque; AWG18 fits the conductor range. Ferrule choice, production procedure and strain relief remain OPEN. It has no switching capacity: the manufacturer prohibits connection/disconnection while carrying voltage or under load. No solder-tinned wire end under a screw clamp is proposed. Neither system has a final Pi socket/header assembly.

**DECISION:** both systems can be screened for J501; both remain candidates for J502 but VH's documented resistance maxima consume much more voltage budget. Consider mechanically different input/output families after approval to prevent plugging 24 V into the output. Changing that physical interface requires manager approval. [Pi budget](PI_POWER_DELIVERY_REFINED.md) propagates the complete candidate chain; a 7/12 A catalogue current alone does not qualify 5 A delivery.

## J503 four-pin host I2C interface

The exported schematic fixes this functional pinout:

| Physical circuit number | Net / purpose |
| --- | --- |
| 1 | GND |
| 2 | 3V3_HOST reference input: host-side buffer supply and host pull-up reference; not a local 3.3 V output |
| 3 | SDA_HOST |
| 4 | SCL_HOST |

Two exact candidate systems, neither selected:

- JST XH `B4B-XH-A` top-entry header + `XHP-4` housing + four `SXH-001T-P0.6` contacts. **2.50 mm pitch**, not 2.54 mm. Contact accepts AWG28..22 and OD0.9..1.9 mm. Source [XH catalog](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf), pp1,3-4. Use the regular contact, not the low-insertion-force `...P0.6N` for a presumed vibration benefit.
- JST PH `B4B-PH-K-S` top-entry header + `PHR-4` housing + four `SPH-002T-P0.5S` contacts. 2.00 mm pitch; SPH-002T-P0.5S accepts AWG30..24 and insulation OD0.8..1.5 mm; the exact signal wire must fit these limits before release. Source [PH catalog](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), pp1-3. Family figure is 2 A with AWG24, 100 VAC/DC, -40..105 C including rise.

**KNOWN mechanical intent:** shrouded/polarized housings and manufacturer circuit1 indication; catalog PCB patterns are viewed from the connector mounting side. Do not reverse numbering by using the mating-face view. A released drawing must label circuit1 adjacent to the housing's keyed feature and document whether the cable is viewed from wire or mating side. No orientation/footprint is assigned from a generic connector symbol.

**OPEN:** final family, installed cable length/capacitance, exact signal wire, locking/retention need, pull-up population, ground-first/hot-plug requirement and Pi adapter pinout. Preserve local/host isolation and never feed 3V3_LOCAL onto pin2. INA228/TCA9517 worst-case low-level margin is still open.

**Test plan:** first continuity/polarity with unpowered harness and a keyed-view drawing; then four-wire loop-resistance measurement including board solder joints, connector, crimps/screws, cable, adapter and Pi contacts; dummy-load tests at1/3/5 A to thermal equilibrium at approved ambient; record each contact temperature, Vdrop and imbalance if two Pi power pins are used. Verify retention and power-state I2C behavior separately. Mis-mating, hot contacts, voltage-floor failure, unequal sharing or stuck lines fail. No Pi or expensive SBC used as first load.
