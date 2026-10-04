#!/bin/bash
# Review exports only: NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.
set -euo pipefail
if [[ $# -ne 2 ]]; then
    echo 'Usage: scripts/export_fab_package.sh <pcb> <outdir>' >&2
    exit 2
fi
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
kicad_cli='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
kicad_python='/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
for executable in "$kicad_cli" "$kicad_python" /usr/bin/swift; do
    if [[ ! -x "$executable" ]]; then
        echo "Required installed executable missing: $executable (nothing installed)" >&2
        exit 2
    fi
done
exec "$kicad_python" -B "$script_dir/export_fab_package.py" \
    --kicad-cli "$kicad_cli" "$1" "$2"
