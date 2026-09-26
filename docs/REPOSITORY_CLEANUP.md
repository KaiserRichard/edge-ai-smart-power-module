# Repository cleanup and publication preparation — 2026-09-26

Scope: repository hygiene, durable AI context, and publication of the existing V1A working snapshot. **R2 BLOCKED; R3 BLOCKED.** No electrical redesign, board creation, fabrication export, or blocker closure.

## Preservation and rollback

Baseline HEAD: `bc2379025a6320dff9186724a03f6e1ab0db7019`, branch `feat/r2-schematic-recovery`. The initial working tree already contained changes to seven KiCad project/schematic files and the manager report, plus untracked footprints, scripts/tests, and dated engineering evidence. The cleanup publication intentionally includes that current engineering snapshot; large schematic diffs against HEAD predate this session.

Before removal, a complete working-tree snapshot excluding the root Git database was copied to the sibling directory `../edge-ai-smart-power-module-local-archive-20260926-152745/`. All 4,176 regular snapshot files were SHA-256 checked against their originals. The archive contains `snapshot/`, `snapshot-sha256.json`, initial Git status/diff, baseline metrics, and validation logs. Existing Git history was not rewritten.

Restore specific original relative paths from `snapshot/` if needed; do not reset or replace the current repository wholesale. Nested upstream Git metadata is preserved in the snapshot. The archive is local and is not part of GitHub publication.

All 13 current hardware sources/library files are preserved byte-for-byte, including Sheet 03, the project settings, three custom footprints, symbols, and both library tables. [Preservation hashes](evidence/repository_cleanup_2026-09-26/source_integrity.json) record the as-received working tree, not an electrical qualification.

## Classification and cleanup

| Category | Treatment |
| --- | --- |
| Current KiCad sources and custom libraries | Retained unchanged |
| Core design history, dated review evidence, calculations/configurations, source manifests | Retained; entry-point notices distinguish old choices from current state |
| Dated PDFs, netlists and three footprint SVGs inside `docs/evidence/` | Retained as compact review evidence; the tests also use the historical netlist |
| Full predecessor repositories | Archived: 3 repositories, 518 files, approximately 654.2 MiB |
| Third-party review output/environments | Archived: 3,193 files, approximately 189.4 MiB |
| Vendor download cache | Archived: 41 files, approximately 52.5 MiB; one source manifest also retained in Git |
| Scratch forensic renders/snapshots/packets in `tmp/` | Archived: 116 files, approximately 14.3 MiB |
| KiCad backups | Archived: 2 files |
| Root historical review ZIP | Archived: 1 file; removed from current Git tree, still present in history |
| Local Python environment, bytecode, macOS/editor state | Archived and removed; ignore rules expanded |
| Small existing Raspberry Pi/Linux extracts | Retained with original licenses and source registers; approximately 0.59 MiB |
| Empty future directories | Purpose documented for telemetry, measurement, and fabrication areas; unused empty placeholders removed |

The initial inventory reported 984 MiB on disk, 4,304 files including Git, and 82 tracked files. The safety-snapshot census recorded 4,313 files / 983.5 MiB after read-only inspection/tool caches; this small difference is local cache activity, not engineering work. Final publication metrics are reported after commit/push. Tracked-file count increases because existing untracked engineering evidence is now preserved remotely. Most removed bulk was already ignored, so no history rewrite was needed.

See the [archive inventory](evidence/repository_cleanup_2026-09-26/archive_manifest.json) for exact category counts/bytes. Machine-readable historical paths remain historical; removed local references are explicitly classified as archived external evidence in [evidence navigation](evidence/README.md), current documentation notices, and [third-party restoration](../third_party/README.md). Four Markdown links to vendor PDFs retain exact original names and are labelled archived, not silently treated as present files.

## Context and reproducibility

Added `CLAUDE.md`, all seven `docs/context/` documents, [Claude selection instructions](CLAUDE_PROJECT_SETUP.md), [validation instructions](VALIDATION.md), and the [reference registry](../third_party/README.md). Updated README to describe the existing five-sheet schematic and blocked releases. Older design prose remains historical, with dated navigation notices instead of invented closure claims.

No existing calculation, schematic generator, footprint generator, test, or R2 checker was changed. The new `check_repository.py` provides portable link/JSON/source-preservation checks without claiming absent vendor caches have been validated. Generator cache requirements and exact restoration methods are documented.

## Validation evidence

- Baseline and restored-snapshot `check_r0_r1_docs.py`: PASS; 122 hashed records, three predecessor repository pins. This strict historical checker needs archived caches; it is not a fresh-clone smoke test.
- `python3 -B -m unittest discover -s tests -v`: all 10 existing tests pass.
- `python3 -m pytest -q`: unavailable (`pytest` not installed); standard-library runner executes the same test classes.
- `check_r2_schematic.py`: retained post-footprint netlist and fresh KiCad export pass capture invariants; release remains BLOCKED.
- KiCad 9.0.6 fresh XML netlist export: exit 0. Fresh ERC with all severities: exit 5, exactly U402 pin 1 `power_pin_not_driven`, zero warnings/exclusions. Existing workstation Fontconfig warnings appear on stderr; no system configuration was changed.
- `calculate_r2.py`, `calculate_pi_interface.py`, `calculate_r2_qualification.py`: exit 0; calculations remain conditional, not physical measurements.
- Portable repository checker: PASS; deliberately missing links, changed hardware bytes, malformed JSON, and unauthorized PCB paths were rejected in an isolated test fixture.
- Publication scan: no credentials found in retained candidates or 82 reachable historical Git blobs (including ZIP members). Keyword hits were reviewed as documentation, hardware-register constants, and ordinary terminology. No historical blob exceeds 20 MiB. This is a bounded scan, not a guarantee against every possible credential.
- Source-preservation and archive-reference checks pass. Whitespace checks pass for newly authored cleanup content; the full staged check reports pre-existing trailing whitespace in unchanged raw logs/SVG evidence, deliberately preserved byte-for-byte. [Machine-readable validation summary](evidence/repository_cleanup_2026-09-26/validation.json) records outcomes; full local logs and exports live in the sibling archive's `validation/` directory.

The release authority remains the [current engineering state](context/03_ENGINEERING_STATE.md). Repository checks provide no electrical safety or fabrication approval. The next engineering gate remains R2; this maintenance session does not work on its electrical blockers.
