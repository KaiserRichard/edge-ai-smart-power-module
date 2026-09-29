#!/bin/sh
# Start an interactive Codex session on one account, for use as an agent-deck command.
#
#   lab/bin/codex-worker.sh <account> [read-only|workspace-write]
#
# <account> is the suffix of the Codex home: "a" uses ~/.codex-a. The sandbox defaults to read-only.
# Approvals are off, so the sandbox is the only guard: use workspace-write only for tasks that must write.
set -eu

if [ $# -lt 1 ]; then
  echo "usage: $0 <account> [read-only|workspace-write]" >&2
  exit 2
fi
account="$1"
mode="${2:-read-only}"
case "$mode" in
  read-only|workspace-write) ;;
  *) echo "sandbox must be read-only or workspace-write, got: $mode" >&2; exit 2 ;;
esac

export CODEX_HOME="$HOME/.codex-$account"
if [ ! -d "$CODEX_HOME" ]; then
  echo "missing $CODEX_HOME; log in with: CODEX_HOME=\"$CODEX_HOME\" codex login --device-auth" >&2
  exit 1
fi

exec codex -s "$mode" -a never -c check_for_update_on_startup=false
