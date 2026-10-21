# Reading the review PDF alongside the lessons

**Source:** [V1A_REVIEW_READABLE.pdf](/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf), read and visually checked in full on 2026-09-30. SHA-256: `b5dd287088d00fac765f56d9f76f88c5bcd0de74369abe85117e62915c294247`. Page numbers below are **PDF viewer pages**, not lesson numbers. The title-block dates differ by sheet; the hash identifies the exact snapshot.

| PDF page | Sheet / visible block | Start reading here |
|---:|---|---|
| 1 | Top hierarchy | `01_INPUT_PROTECTION` → `02_BUCK_5V` → `03_OUTPUT_PROTECTION` → `04_POWER_MONITOR`; connectors are in `05_IO_TEST` |
| 2 | Input / reverse protection; eFuse / supervision | F101 pins 1/2; Q101 sources 1/2/3 and drains 5/6/7/8; U101 IN 1/2, OUT 17/18, SHDN 12 |
| 3 | Input / enable; buck converter; output / feedback | U201 VIN1 8, VIN2 12, SW 10, FB 4; L201 pin 1 on SW and pin 2 on raw output |
| 4 | Earlier preliminary output protection | Q301/Q302 common sources 1/2/3, gates 4, outer drains 5/6/7/8; Q303 crowbar; TP301 raw and TP302 protected |
| 5 | Kelvin shunt; local supply; I2C domains | R401 force 1/4 and sense 2/3; U401 IN+ 10, IN− 9, VBUS 8; U402 IN 1 / OUT 5 |
| 6 | DC input; load output; host I2C; bench access | J501 1 positive / 2 return; J502 1 positive / 2 return; J503 1 ground / 2 host reference / 3 SDA / 4 SCL |

## Read a wire in four moves

1. Find the **reference designator** (refdes): `U201` identifies one IC; `10` beside SW is a pin number, not a voltage.
2. Read the **pin name** and attached **net label**. Equal net names identify the same electrical net even when no long wire joins them on the page. Hierarchical sheet ports carry those nets between pages.
3. Follow a branch only where there is a connection. A junction dot means wires meet; crossing lines without a junction do not automatically connect.
4. Find the return/reference. A ground symbol does not mean physical copper has zero resistance or inductance. The schematic says what connects; it does not specify routing geometry.

`PWR_FLAG` symbols tell ERC that power is supplied elsewhere. They are not components or hidden voltage sources. IC rectangles show external pins; they do not draw the internal MOSFETs of U201.

## Snapshot versus current decisions

| Visible in this PDF | Current controlling lesson fact |
|---|---|
| 9–24 V in old design notes | Owner requirement is **9–26 V** normal input |
| F101 “FUSE - OPEN”; D101 SMBJ26CA | Selected F101 **Schurter 3403.0285.23**, D101 **SMCJ36CA**; installation/coordination remain open |
| L201 6.8 µH; C201/C202 nominal 22 µF each | Selected-for-qualification L201 **10 µH 74437636351002**; effective input-C contract **10–30 µF** needs actual qualification |
| Page 4 already has Q301/Q302, Q303 and earlier control supplies | This is the **earlier preliminary implementation**. The revised architecture D freeze is **frozen on paper, not yet in the schematic**. That phrase describes the later version; it does not erase the older drawn pair/crowbar. |
| No raw dump in the page-4 blocks | Gate 4a raw dump: **frozen on paper, not yet in the schematic**; its circuit/ratings remain under blocked review. Do not invent a PDF refdes or pin for it. |
| Earlier detector trip 5.325 V and `DRV_7V5` LDOs | Later detector/held-up auxiliary proposals have different assumptions; the source trigger, supplies and reset/re-arm remain incomplete. Do not combine old pins with new values as though captured. |
| Generic J502 symbol | Later connector candidates do not alter the PDF's two electrical pins. The external GPIO harness is not drawn here. |

Here **“frozen on paper” identifies a recorded proposal, not a passed freeze gate**. The freeze verdict remains **BLOCKED**. Later paper changes are pinned in [the editorial record](VISUAL_REBUILD_LOG.md); the original [fact-check log](FACTCHECK_LOG.md) preserves its own dated sources.

The exported page images are unchanged PDF renders for reading. The `circuit_*.py` files redraw only explicitly identified simple excerpts, under the owner's final exception permitting exact circuit code. Every such image lists omissions. They do not change KiCad, close ERC/DRC, or release hardware.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.**
