# Final manager report — Project II V1A R0/R1

Date: 2026-09-11. Baseline commit: `a9fe716` (`chore: initialize edge AI smart power module project`). Branch: `docs/r0-r1-engineering-audit`. The reviewed documentation and source records are **uncommitted working-tree additions**, not content contained in that baseline commit.

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED**

## STATUS

| Gate | Status | Meaning |
| --- | --- | --- |
| R0 environment/predecessor/source audit | **CONDITIONAL PASS** | Complete enough to support R1 recommendations: three pinned predecessor designs and relevant official/manufacturer sources consolidated. Remote-only sources, unresolved reuse rights for some historical assets and component-level qualification limits are explicit |
| R1 requirements/architecture | **CONDITIONAL PASS — documentary review package complete** | Confirmed scope, proposed numerical targets, open decisions, converter/protection/sensor comparison and calculations are documented. This is not approval/freeze of the electrical requirements or architecture |
| R2 schematic readiness | **BLOCKED** | Essential source/input, output/current/thermal, protection and component/interface choices remain unresolved. Manager technical review and explicit R2 authorization are still required |

No authored schematic, PCB, firmware, electrical validation or fabrication release exists. Manufacturer EVM performance and rule-check capability are not V1A measurements.

## WHAT WAS DONE

1. Recovered the existing branch, dirty working tree, handoff, R0 notes, WBR study and ignored predecessor/converter caches. Preserved original AGENTS changes, all existing R0 evidence, source manifests and upstream repositories. Reused existing downloads, source text and renders rather than restarting the audit.
2. Applied the user's scope correction: **standalone Smart DC Power Module for Edge AI Devices — Project II V1A** is primary. V1B is a separate teammate-owned supercapacitor subsystem; future V2 integrates both after validation. WBR/HAT research is clearly labelled **FUTURE WBR REFERENCE — NOT PROJECT II V1 REQUIREMENTS**.
3. Completed [requirements](00_REQUIREMENTS.md), [reference audit](01_REFERENCE_AUDIT.md), [architecture](02_ARCHITECTURE.md), [component selection](03_COMPONENT_SELECTION.md), [power calculations](04_POWER_CALCULATIONS.md) and the concise [hardware source pack](CODEX_HARDWARE_SOURCE_PACK.md).
4. Inspected actual predecessor components/assumptions and manufacturer converter circuits/BOMs/layouts. Recorded source/license pins, candidate applicability and conflicting source labels. No circuit/CAD/code was adapted or copied into project implementation.
5. Added a source manifest and a read-only documentation/evidence checker. Corrected README/handoff navigation and annotated unavailable historical WBR reports without inventing replacement deliverables or continuing CAN/HAT work.

## EVIDENCE

- [Source manifest](evidence/r0/source_manifest.json): three exact Git pins, selected source/license file SHA-256 hashes, 26 official/manufacturer document records including explicit remote-only limitations.
- [Reference audit](01_REFERENCE_AUDIT.md): actual components, source revisions, relevant files/pages, licensing boundaries, operating assumptions and V1A/V1B/V2/future-HAT classification.
- [Existing environment evidence](evidence/r0/environment.json): KiCad 9.0.6 CLI capabilities on the prior macOS workstation; no environment reinstallation or redundant capability audit in this mission.
- [Validation record](evidence/r0/R0_R1_VALIDATION.md): executed documentary checks, source preservation, reproducible arithmetic and limitations. Run `python3 scripts/check_r0_r1_docs.py` from repository root; it is not an electrical test.
- Selected predecessor schematics and manufacturer EVM schematic/layout pages were visually reviewed. No full PCB electrical/current/EMI review or lab test was performed.

The two documents intended for ChatGPT technical review are **this report** and **CODEX_HARDWARE_SOURCE_PACK.md**. Source IDs in them resolve through the audit/manifest. Old WBR missing-report claims are historical gaps, not evidence of completed CAN qualification.

## DECISIONS

### Recommended V1A architecture

**RECOMMENDED FOR R2 REVIEW:** DC connector → coordinated fuse/transient protection → reverse-input/UV-OV/inrush protection → single synchronous buck → independent output OV disconnect and defined reverse-feed boundary → high-side Kelvin shunt → reusable load connector. INA228 senses the load-side bus and reports over a reviewed 3.3-V-compatible I2C interface. Its local supply branches before the shunt, after output protection. Regulation and fault interruption work without Linux or a supervisor MCU.

This is a proposal, not an APPROVED / FROZEN architecture. Keep buck feedback at its local regulated node initially; monitor VBUS placement does not imply feedback beyond the output switch. Simultaneous input/output bench measurements are required to determine module efficiency.

### Leading component options

| Block | Leading review option | Alternative / blocking condition |
| --- | --- | --- |
| Buck | **TPS56837**, initially 500 kHz, for a proposed 9–24 V input envelope | TPS56637 is simpler; **LM61460** leads if the approved maximum/transients need more margin than a 28-V-class IC. No current rating is guaranteed without the actual PCB/thermal conditions |
| Monitor | **INA228** | INA226 if sourcing/software/scope justify software energy integration |
| Shunt | **2-mΩ four-terminal candidate**, compared with 1/5 mΩ | Final range, accuracy, tolerance/TCR, package and calibration remain OPEN; prior shunt ordering code is not frozen |
| Input protection | **TPS26630/31 with required external reverse-protection devices**, coordinated fuse and TVS | Simpler fuse/MOSFET path only if the source envelope supports it; exact suffix/settings/SOA still open |
| Output protection | **Back-to-back-FET disconnect/reverse-feed topology**, LM74800-Q1 for review | Integrated OV threshold tolerance may be too wide. A precision detector/disconnect solution remains OPEN; no exact part is selected just to fill the BOM |

Manufacturer EVM figures support studying these options, not claiming an efficiency improvement. Official product listings were checked; exact part stock, local availability, cost and assembly capability remain unconfirmed.

### What is genuinely reusable

- Manufacturer buck **design method, functional circuit and layout principles**, with new component/rating review for V1A.
- INA228 high-side **Kelvin measurement arrangement and calibration method**.
- Understood predecessor **protection/current-path/testability concepts**, after checking source assumptions against manufacturer guidance.

**No entire predecessor board is reusable unchanged for the proposed V1A load.** Sailor Hat's two-stage supercap power chain is not needed in V1A. The 1026 board actually uses a 4-A LM64440 variant, and its input parts do not establish 25-W V1A capability. SBCShop uses a battery-side INA219/0.1-Ω shunt and a 3-A-labelled inductor; these are not a 5-A output-sensing/power-stage design.

### Work belonging to future integration

V1B owns its charging/balancing/storage design. Future V2 must agree rail voltage/range, load/charge currents, reverse behavior, common ground, connector, power-fail, telemetry, startup/shutdown and hold-up requirements — **all TBD**. Preserve V1A independence and review output prebias/discharge/reverse-feed behavior, but do not implement a speculative V1B interface.

CAN/MCP2518FD, WBR interfaces/battery assumptions, supervisor/watchdog MCUs, robot fault ownership, HAT/HAT+ form factor and WBR sequencing remain future reference only. They are not blockers or requirements for V1A. No D435i USB routing is included.

## OPEN RISKS

The three most important decisions for the manager are:

1. **Input/source envelope:** actual adapter/source type, minimum/maximum including tolerance, cable, available/fault current and surge/hot-plug conditions. Is the candidate 9–24 V connector envelope appropriate, or is 28 V a normal maximum requiring a higher-voltage converter? No robot battery value is assumed.
2. **Delivered-output and thermal acceptance:** 5.00 versus 5.10 V, load-terminal normal/fault window, 5-A continuous target versus reduced scope, peak amplitude/duration/slew, ripple/efficiency criteria, ambient/enclosure/airflow and board copper/area. These determine ratings and whether the proposed converter is appropriate.
3. **Complete component/protection/interface selection:** converter/package/mode and assembly route; input protection/independent output OVP and reverse-feed behavior; inductor/capacitors; shunt/accuracy/calibration; load connector and unpowered-host I2C arrangement. Particularly close the OVP threshold/response/let-through budget before R2.

Additional evidence limits: some official PDFs remain remote-only; predecessor documentation contains contradictory labels/assumptions; source licenses do not automatically cover embedded vendor documents or fonts; cached files are largely ignored and will not survive a fresh clone without a separate transfer/retrieval. An 8-A chip, four-layer recommendation or successful document checker does not establish a safe 5-A board.

## NEXT GATE

**Stop here for technical review.** Send this report and the source pack to ChatGPT as requested. Manager review must resolve essential requirements, approve the architecture and component direction, and explicitly authorize R2. Only then capture a schematic, verify pins/footprints/ratings and run ERC. Continue R3–R5 sequentially; dummy-load fault/thermal/ripple validation precedes SBC use.

No commit, push, purchase, ignored-cache deletion or schematic implementation was performed. Documentary rollback can be limited to this mission's new files and scope annotations; retain historical evidence and the user's existing AGENTS edits.
