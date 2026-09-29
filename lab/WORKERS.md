# Workers

Codex accounts, how to launch a worker, and which workers exist. Runs on the user's Mac (Quocs-MacBook-Pro-2). Update the tables whenever a worker starts, stops or changes state.

## Accounts

Check with `CODEX_HOME=~/.codex-<x> codex login status`. Never read or print auth files.

| Account | Codex home | State (last checked) | Notes |
| --- | --- | --- | --- |
| codex-a | `~/.codex-a` | Logged in, 2026-09-29 | Repo trusted in this home |
| codex-b | `~/.codex-b` | Logged in, 2026-09-29 | Repo trusted in this home |
| codex-c | `~/.codex-c` | Pending user login, 2026-09-29 | Reserved for the reviewer role after the first round has results; not launched |
| default | `~/.codex` | Not logged in, 2026-09-29 | Not used |

New account: `mkdir -p ~/.codex-c && CODEX_HOME="$HOME/.codex-c" codex login --device-auth`, run by the user.

## Launching a worker

Tools: agent-deck 1.16.10, codex-cli 0.154.0. agent-deck uses the tmux socket `agent-deck`.

1. Make the worktree yourself from the right base. `agent-deck launch -w` branches from `main`, which has no KiCad files.
   ```
   cd ~/Desktop/Research/edge-ai-smart-power-module
   git worktree add -b <branch> ../v1a-wt-<name> origin/feat/r2-schematic-recovery
   ```
2. Launch Codex through the launcher ([bin/codex-worker.sh](bin/codex-worker.sh), installed at `~/Desktop/Research/v1a-lab/bin/`):
   ```
   cd ../v1a-wt-<name>
   agent-deck launch . -t "V1A <name>" -c codex \
     -cmd "$HOME/Desktop/Research/v1a-lab/bin/codex-worker.sh <account> read-only" -no-parent -no-wait
   ```
3. The first run in a new Codex home asks whether to trust the repo. Answer it once: `tmux -L agent-deck send-keys -t <tmux_session> Enter`.
4. Send the brief: `agent-deck session send "V1A <name>" --message-file <brief.md>`. It may say "not confirmed submitted" even when it arrived, so check step 5 before resending.
5. Read the result: `agent-deck session output "V1A <name>" --pane`, and `agent-deck status -v`.

Rules: one worker per worktree; only one worker edits KiCad files at a time (DECISIONS D-23); read-only unless the task must write; no destructive git; workers never merge, order parts or fabricate.

## Workers

| Worker | Account | Worktree / branch | Base | Task | State |
| --- | --- | --- | --- | --- | --- |
| V1A Smoke codex-a | codex-a | `v1a-wt-smoke-codex-a` / `lab/smoke-codex-a` | `de1d35c` | Read-only: list sheets, read ERC report | Done 2026-09-29, stopped. Answer correct (6 sheets; 1 ERC error, U402 pin 1) |
| V1A Smoke codex-b | codex-b | `v1a-wt-smoke-codex-b` / `lab/smoke-codex-b` | `de1d35c` | Read-only: HEAD, Sheet 03 symbols | Done 2026-09-29, stopped. Answer correct (TP301, TP302) |

Old sessions from the earlier MOA project (9, all ERROR) remain in agent-deck's default profile. They are not part of this lab.
