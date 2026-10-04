# Path-check source provenance — 2026-10-04

These sources were **referenced**, not copied as circuits, boards, code, charts,
or document text. The checker and synthetic boards are original project code.
No upstream source was modified. No third-party PCB was reused. External material
is represented here by bibliographic references; no downloaded PDFs are vendored.

| Source and exact revision | Relevant source / function studied | License / attribution / modifications |
|---|---|---|
| [NBS Handbook 100, Copper Wire Tables](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook100.pdf), issued 1966-02-21 | Sections 1.1(a–b), Table 2: annealed-copper resistivity and temperature coefficient | US federal government publication; reference attributed to NBS/NIST. Constants rounded to 1.724e-8 Ωm and 0.00393/K; used as ASSUMED foil values. No source edits or copied tables. |
| [TI SNVA766](https://www.ti.com/lit/an/snva766/snva766.pdf), April 2017 | Section 3.2.1 Eq. 1: annular via area; section 11 Eq. 3: legacy current/temperature/cross-section coefficients | Copyright Texas Instruments; TI Resources terms in the document, not an open-source license. Reference only; attributed here. Original implementation of the equations; k=0.024 envelope applied to both layer classes as an explicit conservative assumption. No EVM circuit/layout copied. |
| [Michael R. Jouppi, The Value of IPC-2152](https://www.electronics.org/system/files/technical_resource/E7%26S22_03.pdf), IPC APEX EXPO 2010, E7&S22_03 | Paper pp. 2–8, Figures 3–11: conservative legacy envelope and board/plane/neighbor thermal dependencies | IPC/author publication; no redistribution license identified. Reference only, attributed to Jouppi, Thermal Management Inc., and IPC. No chart copied or digitized; no claimed IPC-2152 compliance. |
| [IPC-2152 table of contents and scope](https://www.ipc.org/TOC/IPC-2152.pdf), August 2009 | Scope: current, conductor dimensions, and allowable temperature rise | Copyright IPC; no redistribution license identified. Referenced for scope only; no normative charts copied, no changes. |
| [KiCad Board File Format](https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/), page Last Modified 2025-02-20, accessed 2026-10-04 | Nets, track segments, arcs, vias, zones, layer/stackup format | Documentation license not stated on the consulted page: OPEN for redistribution. Referenced syntax only; no code or prose copied. Attributed to KiCad developers. |
| [KiCad S-Expression Format](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/), page Last Modified 2025-02-20, accessed 2026-10-04; exact consulted representation identified in `WEB_SNAPSHOTS.json` | Coordinates, footprints, pad geometry, filled polygons | Documentation license not stated on the consulted page: OPEN for redistribution. Referenced syntax only; original parser. No changes to upstream. |
| [KME Cu-ETP](https://www.kme.com/fileadmin/DOWNLOADCENTER/COPPER%20DIVISON/4%20Industrial%20Rolled/3_Datasheets/Datasheets_NEW_2021/Cu-ETP_01_2021_e.pdf), C11000_Cu-ETP_10_2020, p. 1 | Reviewed the material reference already cited by the force-link calculation; no new link resistance imported | Manufacturer datasheet; no redistribution license identified. Reference only; no edits, source material, or layout copied. |

All required third-party attribution used by this implementation is supplied
above. License entries marked OPEN are not assertions of reuse permission;
the implementation only references facts and independently implements calculations.

Project inputs, all from base commit `5f371fd` (full hash in verification):

- `docs/evidence/r2/R203_OPTION_A.md` and
  `docs/evidence/r2/r203_option_a/CALCULATIONS.json`: unchanged frozen allocation
  and hot buck voltage. The report retains the JSON SHA-256.
- `docs/evidence/r2/gate4b/{buck,output,monitor,io}_block.json` and
  `hardware/kicad/V1A.kicad_pcb`: actual capacitor/FET/force-link/shunt/J502 pin contracts.
- `docs/evidence/r2/bom_order/FORCE_LINK_CALCULATIONS.json`: inspected to identify
  the separate, unbudgeted JP301 issue; its later link screen was not silently
  added to or substituted for the requested frozen budget.

The installed KiCad 9.0.6 Python binding was used only for independent temporary
coordinate checks. It is neither bundled with nor required by this checker.
