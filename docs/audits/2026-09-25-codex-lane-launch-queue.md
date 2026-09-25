# Codex Review — lane-launch-queue

**Date:** 2026-09-25
**Branch:** `worktree-lane-launch-queue`
**HEAD:** `9d2b3d13`
**Diff range:** `main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/4/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

consumer: the frozen contract H:\My Drive\CLAUDE PROMPT DIR\LANE-5B2-9-launch-queue.md (WAVE5B-N2 lane-launch-queue) -- review scripts/dispatch.py's new queue section (launch_order, decide_lane, watch_queue, repair_lane/build_repair_plan) and tests/test_dispatch_queue.py

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/dispatch.py:1990 — One pass can exceed the local cap and violate serialize groups

**What:** All decisions use the same pre-launch liveness/cap snapshot, then every `FIRE` decision is launched sequentially.  
**Why:** Several ready local lanes can all pass a cap of four when zero are initially live; likewise two ready members of one `serialize-group` can both launch, violating “never two members live.”  
**Fix direction:** Reserve capacity and serialize-group membership after each successful launch, or decide-and-launch one lane at a time; add pass-level tests with multiple ready lanes.

## [HIGH] scripts/dispatch.py:1627 — Watcher can run beyond its declared deadline

**What:** The watcher always sleeps for the full poll interval, even when less time remains before `deadline_s`.  
**Why:** A 60-second poll interval with one second remaining keeps the watcher alive for another 59 seconds, contradicting the self-deadline contract.  
**Fix direction:** Limit each sleep to the remaining deadline and test a non-divisible deadline/interval pair.

## [HIGH] scripts/dispatch.py:1620 — Blocked and codespace lanes are falsely counted as fired

**What:** `HELD-FAILED` and `ROUTE-CODESPACE` decisions are added to `fired` without a launch or a confirmed codespace handoff.  
**Why:** `queue --watch` can report `fired N/N; all clear` while a dependency-failed lane was held or a codespace lane was never routed.  
**Fix direction:** Track launched, routed, and blocked terminal outcomes separately; only report a lane as fired after its corresponding action succeeds.

## [HIGH] scripts/dispatch.py:1963 — `queue --repo-root` is ignored for local launches

**What:** `queue_cmd` accepts `--repo-root` but calls `launch_lane` without passing it as `cwd`.  
**Why:** Queued launches use the caller’s current directory instead, so invoking the command outside the intended repository can create/use the wrong worktree location.  
**Fix direction:** Apply the supplied repository root to queued local launches and cover invocation from a different current directory.

## Medium

(none)

## Low

(none)

---

## Disposition

All four HIGH findings fixed in this lane's own follow-up commit (per common rules §3, "Fix a
Codex review's P1 findings"), each with a new or updated unit test in `tests/test_dispatch_queue.py`:

1. `plan_pass` now reserves the local cap and a fired lane's `serialize-group` membership AS it
   decides each slug within one pass, instead of reading one static snapshot for every decision
   (`test_plan_pass_reserves_the_local_cap_within_the_same_pass`,
   `test_plan_pass_reserves_a_serialize_group_within_the_same_pass`,
   `test_plan_pass_a_held_failed_or_routed_codespace_lane_reserves_nothing`).
2. `watch_queue` clamps every sleep to what is left before `deadline_s`
   (`test_watch_queue_never_sleeps_past_a_non_divisible_deadline`).
3. `WatchResult` now carries `fired`, `held_failed` and `routed_codespace` as three separate
   tuples (plus a `.terminal` property) instead of folding all three into one `fired` set
   (`test_watch_queue_routes_a_codespace_lane_without_ever_spawning_it`,
   `test_watch_queue_marks_a_failed_dependency_terminal_without_spawning`); `queue_cmd --watch`'s
   own summary line was updated to report all three counts.
4. `queue_cmd`'s `do_launch` now passes `cwd=repo_root` to `launch_lane`
   (`test_queue_cli_passes_repo_root_to_the_local_launch`).