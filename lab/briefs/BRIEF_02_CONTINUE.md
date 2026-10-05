You are a Codex worker in the V1A lab. Claude is the conductor and reviews your work before anything reaches GitHub.

Your task is Codex brief 02. Read it in full now: docs/evidence/r2/protection_analysis_2026-09-26/CODEX_BRIEF_02_PROTECTION_ANALYSIS.md

These overrides take precedence over the brief:
1. Work only in this worktree, on the local branch codex/brief02-protection (based on feat/r2-sheet03-output-protection at a2e3cd7). Commit in small commits. Do NOT push, do NOT open or merge PRs, do NOT run git reset, rebase, clean, stash or force commands. Claude will review and push.
2. Do not change anything under hardware/, scripts/check_r2_schematic.py, tests/test_r2_capture.py or docs/evidence/repository_cleanup_2026-09-26/. Sheet 03 stays electrically open. R2 and R3 stay BLOCKED.
3. Do not install software (no brew, pip or npm installs) and do not change system or user configuration. ngspice is NOT installed on this Mac: still write the simulation/hs_short/*.cir netlists for Task 2, mark every SPICE result NOT RUN, and list exactly what is needed to run them.
4. PSpice for TI is NOT available here (macOS). For Task 3, write the run plan and list what the user must provide or run; do not invent vendor-model results.
5. Network access is allowed only to download the primary sources listed in Task 1 from their manufacturers' sites. If a download is blocked (for example HTTP 403), record it and move on; never guess a value.
6. Order of work: Task 1, then Task 4, then Task 2, then Task 5. Keep every number labelled KNOWN / CALCULATED / SIMULATED / INFERRED / ASSUMED / UNKNOWN.
7. Run the four validation commands in the brief before each commit. All must pass.

When you finish, or if you are blocked for more than one step, stop and write a hand-back with:
- the commit list (git log --oneline a2e3cd7..HEAD)
- the pass / fail / NOT RUN table for the 8 acceptance criteria
- every source you could not download
- anything that contradicts PROTECTION_ANALYSIS.md
End the hand-back with the exact line BRIEF-02-HANDBACK.

CONTINUATION NOTE: you are taking over from a previous worker (account codex-a) that ran out of quota at 10:39 UTC.
It finished Task 1 but did not commit: its files are uncommitted in docs/evidence/r2/protection_analysis_2026-09-29/ and possibly third_party/documents/r2_protection/.
First review those files (git status, read them), fix anything wrong, run the four validation commands and commit them as the Task 1 commit.
Known results from that worker to double-check against the datasheets: LM74800 tOVP_OFF 3.98 us typical / 5.4 us maximum; HGATE source current 75 uA maximum (use 75 uA, not the brief's 55 uA); TPS2663 "2x current limit for ~1 us" is not a guaranteed bound; TPS2663 OVP timing ends at the fault flag, not confirmed isolation. Coilcraft, TDK and Nexperia downloads returned HTTP 403.
Then continue with Task 4, Task 2 and Task 5.
