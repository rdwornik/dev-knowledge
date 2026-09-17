---
id: "[#822]"
title: "A pipe masks the exit code of the command it wraps — a reported success is not evidence of the effect"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#822] [P1][S] **A pipe masks the exit code of the command it wraps — a reported success is not evidence of the effect** - THE MOST VALUABLE FINDING of the three, per operator ruling: the fourth instance in one day of "a reported success is not evidence of the effect", and the first one inside our own command habits rather than a vendor's verb. Found 2026-09-16 in lane-ab-810: `git commit -m "..." | tail -40` reports `tail`'s exit code, not git's — the commit had been failing since the first attempt, but the piped command's `0` exit and the task-notification's "completed exit code 0" summary both read as success. The failure was caught only because the Stop hook kept flagging a dirty tree; `git log`/`git status` showed the commit had never landed. Any command whose exit code decides a branch of behaviour (retry vs. proceed, escalate vs. continue) must not be piped — where output must be trimmed, capture first (`> file 2>&1`) and check `$?` as a SEPARATE statement, never through a pipe. This is a general shell-discipline defect, not specific to git: any `cmd | tail`/`| grep`/`| head` in a script or an agent's own command habits carries the same hazard whenever downstream logic reads the exit code. · Done when: this lane's own commands (already fixed going forward, this session) generalize to a checkable surface — at minimum, a grep-based or AST-based check over tracked shell/PowerShell scripts and skill/command files flags a status-deciding pipe (a pipeline whose exit code is read via `$?`/`if`/`&&` immediately after, with no `PIPESTATUS`/`pipefail` capture of the wrapped command's own code); RED-first witness: a script matching this shape (e.g. `git commit ... | tail -N ; if [ $? -eq 0 ]`) should be flagged, not pass silently · refs `H:\My Drive\CLAUDE PROMPT DIR\LANE-ab-810-substrate-repair.md`, lane-ab-810 commit attempt history (model_gen_lane_commit.txt / model_gen_lane_commit2.txt), `[#819]`, `[#820]`, `[#821]` · kill-candidates: none -- newly filed · source: operator ruling 2026-09-16 (third ruling, "the most valuable thing in your report"), lane-ab-810
