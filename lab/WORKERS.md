# Workers

Codex accounts, how to launch a worker, and which workers exist. Runs on the user's Mac (Quocs-MacBook-Pro-2). Update the tables whenever a worker starts, stops or changes state.

## Accounts

Check with `CODEX_HOME=~/.codex-<x> codex login status`. Never read or print auth files.

| Account | Codex home | State (last checked) | Notes |
| --- | --- | --- | --- |
| codex-a | `~/.codex-a` | Logged in; usage limit hit 2026-09-29 ~10:40 UTC, resets 22:03 local | Repo trusted in this home |
| codex-b | `~/.codex-b` | Refresh token revoked 11:00 UTC 2026-09-29; user must log in again | Repo trusted in this home |
| codex-c | `~/.codex-c` | Refresh token revoked 11:08 UTC 2026-09-29; user must log in again | Reserved for the reviewer role after the first round has results; not launched |
| codex-d | `~/.codex-d` | Usage limit hit 11:18 UTC 2026-09-29, resets 22:55 local | Spare for independent jobs (footprints, 3D models) |
| codex-e | `~/.codex-e` | Logged in again, answers, 2026-09-29 | Re-added by the user after the earlier removal |
| codex-f | `~/.codex-f` | Running brief 02 since 11:20 UTC | Also the candidate acting conductor (see [CONDUCTOR.md](CONDUCTOR.md)) |
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
     -cmd "$HOME/Desktop/Research/v1a-lab/bin/codex-worker.sh <account> <mode>" -no-parent -no-wait
   ```
3. The first run in a new Codex home asks whether to trust the repo. Answer it once: `tmux -L agent-deck send-keys -t <tmux_session> Enter`.
4. Send the brief: `agent-deck session send "V1A <name>" --message-file <brief.md>`. It may say "not confirmed submitted" even when it arrived, so check step 5 before resending.
5. Read the result: `agent-deck session output "V1A <name>" --pane`, and `agent-deck status -v`.

Modes: `read-only` (default); `workspace-write` (edit the worktree and commit; the shared `.git` is a writable root); `workspace-write-net` (also network). Model and effort default to `gpt-6-astra` / `ultra` (override with `CODEX_MODEL`, `CODEX_EFFORT`).

The user allowed `Bash(agent-deck launch:*)` in `~/.claude/settings.json` on 2026-09-29, so Claude can launch workers with a plain `agent-deck launch` command. Briefs are in [briefs/](briefs/) (copies in `~/Desktop/Research/v1a-lab/briefs/`). Send a worker a one-line pointer to its brief file rather than the whole text.

Rules: one worker per worktree; only one worker edits KiCad files at a time (DECISIONS D-23); read-only unless the task must write; no destructive git; workers never merge, order parts or fabricate.

## Workers

| Worker | Account | Worktree / branch | Base | Task | State |
| --- | --- | --- | --- | --- | --- |
| (user-started) Brief02 | codex-a | `v1a-wt-brief02` / `codex/brief02-protection` | `a2e3cd7` (PR #1) | Codex brief 02 | Started by the user 10:29 UTC; Task 1 written but uncommitted; stopped 10:39 at codex-a's usage limit. Replaced by codex-d |
| V1A Brief02 codex-d | codex-d | `v1a-wt-brief02` / `codex/brief02-protection` | `a2e3cd7` (PR #1) | [BRIEF_02_CONTINUE](briefs/BRIEF_02_CONTINUE.md) | Committed Task 1 (1a08b1a); Task 4 partly written; stopped 11:18 UTC at usage limit (resets 22:55 local). Replaced by codex-f |
| V1A Brief02 codex-f | codex-f | `v1a-wt-brief02` / `codex/brief02-protection` | `a2e3cd7` (PR #1) | [BRIEF_02_CONTINUE_2](briefs/BRIEF_02_CONTINUE_2.md) | Running since 11:20 UTC |
| V1A Pi5Envelope codex-e | codex-e | `v1a-wt-pi5-envelope` / `codex/pi5-input-envelope` | `de1d35c` | [BRIEF_03](briefs/BRIEF_03_PI_FAULT_ENVELOPE.md) | Running since 11:09 UTC |
| (not started) | – | `v1a-wt-connectors` / `codex/connector-shortlist` | `de1d35c` | [BRIEF_04](briefs/BRIEF_04_CONNECTORS.md) | Worktree ready; not launched (codex-c login revoked) |
| V1A Smoke codex-a | codex-a | `v1a-wt-smoke-codex-a` / `lab/smoke-codex-a` | `de1d35c` | Read-only: list sheets, read ERC report | Done 2026-09-29, stopped. Answer correct (6 sheets; 1 ERC error, U402 pin 1) |
| V1A Smoke codex-b | codex-b | `v1a-wt-smoke-codex-b` / `lab/smoke-codex-b` | `de1d35c` | Read-only: HEAD, Sheet 03 symbols | Done 2026-09-29, stopped. Answer correct (TP301, TP302) |

Old sessions from the earlier MOA project (9, all ERROR) remain in agent-deck's default profile. They are not part of this lab.
