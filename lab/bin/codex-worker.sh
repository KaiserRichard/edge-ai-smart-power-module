#!/bin/sh
# Start an interactive Codex session on one account, for use as an agent-deck command.
#
#   lab/bin/codex-worker.sh <account> [read-only|workspace-write|workspace-write-net]
#
# <account> is the suffix of the Codex home: "a" uses ~/.codex-a. The sandbox defaults to read-only.
# workspace-write lets Codex write the worktree and commit (the repository's shared .git directory is
# added as a writable root). workspace-write-net also allows network access, for downloading sources.
# Approvals are off, so the sandbox is the only guard: use the narrowest mode the task needs.
# Model and effort default to gpt-6-astra / ultra; override with CODEX_MODEL and CODEX_EFFORT.
set -eu

if [ $# -lt 1 ]; then
  echo "usage: $0 <account> [read-only|workspace-write|workspace-write-net]" >&2
  exit 2
fi
account="$1"
mode="${2:-read-only}"

export CODEX_HOME="$HOME/.codex-$account"
if [ ! -d "$CODEX_HOME" ]; then
  echo "missing $CODEX_HOME; log in with: CODEX_HOME=\"$CODEX_HOME\" codex login --device-auth" >&2
  exit 1
fi

set -- -a never -c check_for_update_on_startup=false \
  -m "${CODEX_MODEL:-gpt-6-astra}" -c "model_reasoning_effort=\"${CODEX_EFFORT:-ultra}\""
case "$mode" in
  read-only)
    set -- "$@" -s read-only ;;
  workspace-write|workspace-write-net)
    git_dir=$(cd "$(git rev-parse --git-common-dir)" && pwd)
    set -- "$@" -s workspace-write -c "sandbox_workspace_write.writable_roots=[\"$git_dir\"]"
    if [ "$mode" = workspace-write-net ]; then
      set -- "$@" -c sandbox_workspace_write.network_access=true
    fi ;;
  *)
    echo "unknown sandbox mode: $mode" >&2; exit 2 ;;
esac

exec codex "$@"
