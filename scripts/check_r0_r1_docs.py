#!/usr/bin/env python3
"""Check R0/R1 documentation and pinned local evidence without modifying sources."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


REQUIRED = (
    "00_REQUIREMENTS.md", "01_REFERENCE_AUDIT.md", "02_ARCHITECTURE.md",
    "03_COMPONENT_SELECTION.md", "04_POWER_CALCULATIONS.md",
    "CODEX_HARDWARE_SOURCE_PACK.md", "FINAL_MANAGER_REPORT.md",
)


def heading_slug(text):
    text = re.sub(r"[`*_]", "", text.lower())
    return "".join(
        char for char in text
        if char in " -_" or not unicodedata.category(char).startswith(("P", "S"))
    ).replace(" ", "-")


def run(root):
    errors = []
    notes = []
    counts = {"markdown_files": 0, "relative_links": 0, "json_files": 0,
              "hashed_records": 0, "repository_pins": 0}
    for name in REQUIRED:
        path = root / "docs" / name
        if not path.is_file() or len(path.read_text().splitlines()) < 20:
            errors.append(f"Missing or unexpectedly short deliverable: {path}")

    authored = [root / "README.md", root / "AGENTS.md", *sorted((root / "docs").rglob("*.md"))]
    for path in authored:
        counts["markdown_files"] += 1
        # Code examples and historical filenames are not Markdown links.
        prose = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
        for match in re.finditer(r"!?\[[^\]]*\]\((<[^>]+>|[^)]+)\S*\)", prose):
            target = match.group(1).strip().strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            counts["relative_links"] += 1
            destination = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not destination.exists():
                errors.append(f"Broken link in {path.relative_to(root)}: {target}")
            elif parts.fragment and destination.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", destination.read_text(), re.M)
                anchors = {heading_slug(heading) for heading in headings}
                if unquote(parts.fragment) not in anchors:
                    errors.append(f"Missing heading in {path.relative_to(root)}: {target}")

    manifest_path = root / "docs/evidence/r0/source_manifest.json"
    manifests = sorted((root / "docs").rglob("*.json"))
    legacy_converter = root / "third_party/documents/ti_converters/download_manifest.json"
    if legacy_converter.exists():
        manifests.append(legacy_converter)
    else:
        errors.append("Missing preserved converter download manifest")

    def inspect_records(value, manifest):
        if isinstance(value, dict):
            local = value.get("path") or value.get("file")
            expected = value.get("sha256")
            if local and expected:
                candidates = [root / local, manifest.parent / local]
                source = next((candidate for candidate in candidates if candidate.is_file()), None)
                if source is None:
                    errors.append(f"Missing cached source: {local} ({manifest.name})")
                else:
                    counts["hashed_records"] += 1
                    actual = hashlib.sha256(source.read_bytes()).hexdigest()
                    if actual != expected:
                        errors.append(f"Digest mismatch: {local} ({manifest.name})")
                    if "bytes" in value and source.stat().st_size != value["bytes"]:
                        errors.append(f"Byte-count mismatch: {local}")
            for child in value.values():
                inspect_records(child, manifest)
        elif isinstance(value, list):
            for child in value:
                inspect_records(child, manifest)

    parsed = {}
    for path in manifests:
        try:
            value = json.loads(path.read_text())
            parsed[path] = value
            counts["json_files"] += 1
            inspect_records(value, path)
        except (ValueError, OSError) as exc:
            errors.append(f"Invalid JSON {path}: {exc}")

    source_manifest = parsed.get(manifest_path, {})
    if not source_manifest:
        errors.append("Source manifest is missing or invalid")
    for source in source_manifest.get("documents", []):
        for field in ("id", "url", "revision", "sections", "rights", "use", "applicability"):
            if not source.get(field):
                errors.append(f"Missing source field {field}: {source.get('id')}")
        if source.get("cache_status") == "remote_only":
            notes.append(f"{source['id']}: remote-only/limited evidence; see audit")
        if source.get("use") != "REFERENCE":
            errors.append(f"Unexpected reuse classification: {source.get('id')}")

    for repo in source_manifest.get("repositories", []):
        directory = root / repo["path"]
        pin = repo["commit"]
        if not re.fullmatch(r"[0-9a-f]{40}", pin):
            errors.append(f"Invalid full commit: {repo['id']}")
            continue
        commands = (
            (["rev-parse", "HEAD"], pin),
            (["cat-file", "-t", pin], "commit"),
            (["remote", "get-url", "origin"], repo["url"]),
            (["status", "--porcelain"], ""),
        )
        good = True
        for arguments, expected in commands:
            result = subprocess.run(["git", "-C", str(directory), *arguments],
                                    capture_output=True, text=True, check=False)
            if result.returncode or result.stdout.strip() != expected:
                errors.append(f"Repository check failed: {repo['id']} {' '.join(arguments)}")
                good = False
        if not repo.get("license_files") or not repo.get("rights"):
            errors.append(f"Missing repository license evidence: {repo['id']}")
        if good:
            counts["repository_pins"] += 1

    if counts["repository_pins"] != 3:
        errors.append("Expected three verified predecessor repositories")
    return {"status": "PASS" if not errors else "FAIL", "counts": counts,
            "errors": errors, "limitations": notes + [
                "Checks authored Markdown; upstream README links are outside project control.",
                "External URLs and remote Git objects are not re-fetched by this offline checker.",
                "Hashes verify recorded bytes, not electrical correctness or license clearance.",
                "Completion claims and numerical/engineering interpretation require human review.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--report", type=Path, help="Optional new JSON check report; existing reports are never overwritten")
    args = parser.parse_args()
    result = run(args.root.resolve())
    rendered = json.dumps(result, indent=2) + "\n"
    if args.report:
        with args.report.open("x") as output:
            output.write(rendered)
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
