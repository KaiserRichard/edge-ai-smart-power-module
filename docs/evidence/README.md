# Engineering evidence navigation

Evidence is dated and intentionally retained. Historical schematic Portable Document Format (PDF) exports, netlists, Electrical Rules Check (ERC) reports, and calculation JSON files can describe earlier captures; do not substitute them for current `hardware/kicad/` sources. They are review snapshots, not disposable duplicates.

- `r0/`: predecessor/manufacturer identities, environment and initial documentary audit.
- `r2/`: capture contracts, baseline calculations, electrical review rationale, and recovery provenance.
- `r2/takeover_2026-09-12/`: dated takeover evidence and Raspberry Pi interface study.
- `r2/forensic_2026-09-14/`: later review/qualification worksheets; `V1A_qualified.net.xml` and `ERC_qualified.json` follow the three footprint assignments. “Qualified” filenames do not release R2/R3.
- `repository_cleanup_2026-09-26/`: archive inventory and hardware-source preservation hashes; no electrical qualification.
- `wbr_hat/`: historical future-system research, not V1A scope.

**Archived external evidence:** historical references to `tmp/`, `hardware/kicad/V1A-backups/`, `third_party/repos/`, `third_party/review/`, downloaded files under `third_party/documents/`, and root archive packets describe original local locations. These files now live under `snapshot/` in the sibling local archive. `third_party/documents/ti_converters/download_manifest.json` remains in Git. Original historical JSON manifests and their hashes were preserved, not rewritten to pretend that external caches are in a fresh clone. See [restoration](../../third_party/README.md) and the [archive inventory](repository_cleanup_2026-09-26/archive_manifest.json).

For current release interpretation start with [engineering state](../context/03_ENGINEERING_STATE.md). No directory name, historical PASS, or footprint assignment constitutes electrical qualification.
