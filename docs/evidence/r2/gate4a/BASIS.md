# Gate4a current basis — 2026-09-30

**NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED. Analysis only.**

**DECISION:** owner selects Architecture D for an R2 FAULT-TEST BOARD: REF5025/TLV3201/74LVC1G74 latched detection, LTC7001 and two BSC034N06NSATMA1 series devices between VOUT_5V1 and VOUT_PROTECTED, with CSD18540Q5B/UCC27511/ballast disposal. Timed TPS26630 source isolation, total effective local input capacitance 10–30 µF and qualification candidate Würth 74437636351002 are the source-development route. These are design selections, not qualified limits.

**REQUIREMENT:** normal input **9–26 V** supersedes all earlier 9–24 V normal ceilings, including the first checkpoint of this file. Strict Pi peak <5.5 V, far-end >=4.75 V at 5 A, and GPIO D-30 remain. Inherited OVP minimum 26.973873 V leaves only **0.973873 V** to 26 V; full hot drift, ripple and nuisance-trip testing remain OPEN. The 27 V fault point lies outside normal operation and does not guarantee an OVP trip over the inherited 26.973873–28.289211 V band.

**DECISION:** adopt PR17 D101 **SMCJ36CA** and F101 **3403.0285.23** for the proposed capture inventory. F101 is 125 VDC, 12.5 A time-lag, **1000 A** DC interrupt. D101's specified 58.1 V pulse clamp is neither a 36 V regulator nor an assembled hot-transient guarantee. No direct 67.2 V / 1 s or 33.6 V continuous exposure is authorized.

**EVIDENCE:** [input pins and hashes](INPUT_PROVENANCE.json) and [PR15 component inventory](PR15_INVENTORY.csv). PR15 checked selected footprints; its generic passive MPNs remain OPEN. This task proposes real alternatives without claiming they were previously fitted. Source branches are read with git show; no merge or native KiCad access.

**DECISION:** retain the owner's two BSC034N06 devices. The path study's 35.072941 mΩ target assumed a different <=6 mΩ hot pair. With the inherited ASSUMED 13.6 mΩ BSC034 pair screen, the corresponding loop is 42.672941 mΩ. The 35.072941 mΩ number must not be claimed for this selected BOM. Retain local regulation and the 2 mΩ Kelvin shunt; use both 5 V pins and all eight grounds through the reviewed full-header harness.

**DECISION:** negative paper margins remain OPEN for bounded dummy-load measurement; they are not, by themselves, grounds to undo the owner's developmental test-board choice. A missing circuit connection, supply path, timing endpoint or required bound must still be declared. Pi integration, electrical release, PCB work and fabrication remain blocked until their gates pass.

Worktree `wt-gate4a`, branch `feat/r2-testboard-freeze`, draft PR destination `feat/sheet03-output-protection`. No native CAD files opened/read/saved; no bench activity, orders or merges. Current verdict and detailed closure actions will be in [GATE4A_FREEZE.md](GATE4A_FREEZE.md).

**Round-2 handoff:** connector solution A (`41cb9e8`) is selected. With the retained 13.6 mΩ pair, its current loop screen is 41.855546 mΩ; far-end at 5 A/20 mV trough is 4.796866 V. The 42.672941 mΩ value above is historical. T11/T16 still govern hot assembly and later Pi integration.
