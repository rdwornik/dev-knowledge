# Codex Review — lane-end-hook

**Date:** 2026-09-21
**Branch:** `worktree-lane-end-hook`
**HEAD:** `597347a1`
**Diff range:** `main..worktree-lane-end-hook`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/4/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/lane_end_guard.py: a Stop hook that must NEVER block the session (exit 2 or a decision on stdout would) and never kill a task; verify every path returns 0.
- Once-only semantics: the claim receipt MOMENT-LANE-END-HOOK.json keyed on the last HANDBACK line; look for races, a stuck 'running' claim if the detached worker dies, and a re-run on a changed HANDBACK line.
- The detached worker (Windows creationflags NO_WINDOW|NEW_GROUP|BREAKAWAY) - does it survive the hook and the session; is the fallback safe.
- The one new Stop entry in .claude/settings.json: 'python ... || true' and its 15 s limit; existing entries untouched; bounded_hook stays unwired.
- Tests in tests/test_lane_end_guard.py: can each fail if the implementation is removed or stubbed?

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/lane_end_guard.py:233 — A dead detached worker leaves a permanent `running` claim

**What:** Any later Stop event with the same HANDBACK skips solely because the receipt’s handback matches, regardless of its still-`running` status.  
**Why:** If the worker dies after spawning, `moment:lane-end` never runs and the lane is permanently suppressed.  
**Fix direction:** Add an ownership/liveness or bounded recovery mechanism that converts an abandoned claim to a terminal receipt before allowing a retry.

## [HIGH] scripts/lane_end_guard.py:237 — Replacing an existing claim is not atomic or worker-owned

**What:** A changed HANDBACK overwrites an existing receipt, even if it is an active `running` claim; workers only check for any `running` receipt.  
**Why:** An older and newer worker can both execute against the new claim, while the original completion is lost; concurrent changed-HANDBACK hooks can also both spawn workers.  
**Fix direction:** Use a unique claim token/key derived from the HANDBACK and require compare-and-swap ownership before spawning or finalizing.

## [HIGH] scripts/lane_end_guard.py:124 — Windows fallback starts the worker inside the hook job

**What:** If `CREATE_BREAKAWAY_FROM_JOB` fails, the fallback deliberately launches without breakaway.  
**Why:** That child remains in the hook/session job and can be terminated with it, contradicting the detached-worker guarantee and leaving the receipt stuck `running`.  
**Fix direction:** Do not treat the non-breakaway process as detached; use an out-of-job launcher or record a terminal failure when breakaway is unavailable.

## [HIGH] tests/test_lane_end_guard.py:170 — Essential once-only failure and concurrency paths are untested

**What:** Tests cover a manually completed worker and unchanged receipt, but not worker death, concurrent claim replacement, changed HANDBACK while a worker is active, or Windows breakaway fallback.  
**Why:** The identified races and permanent-running state can ship with a green suite.  
**Fix direction:** Add deterministic tests for abandoned claims, simultaneous changed-HANDBACK hooks, claim-token ownership, and the Windows fallback path.

## Medium

(none)

## Low

(none)

---

## Dispositions (lane-end-hook, W3-D)

Review note: the wrapper's two-dot range `main..worktree-lane-end-hook` also showed `ecosystem/disposition-register.yaml`,
which W3-E landed on `main` after this branch was cut. It is not part of this lane's diff (`git diff main...HEAD` is
five files: settings.json, organ-index.md, lane_end_guard.py, transport_report.py, the test file); no finding concerns it.

| # | Finding | Disposition |
|---|---|---|
| H1 | dead worker leaves a permanent `running` claim | FIXED. A later turn end that finds a claim still `running` after `STALE_RUNNING_S` (300 s) writes a terminal FAILED receipt ("presumed dead; not retried"). Once-only is kept: reaped, never re-run. Test `test_an_abandoned_running_claim_becomes_a_terminal_receipt_not_a_retry`. No pid liveness probe on purpose: `os.kill(pid, 0)` on Windows terminates the process. |
| H2 | claim replacement not atomic / not worker-owned | FIXED. The claim is an exclusive create of `MOMENT-LANE-END-HOOK-<key>.claim` per closing line (8 racing hooks -> 1 worker, tested). A worker is born with `--key` and does nothing if the receipt is another line's; a finishing worker only writes if the receipt still carries its own closing line. Remaining window: a re-read-then-replace of about a millisecond between an old worker's check and its write; a lane that hands back twice inside one worker run is the only trigger. Tests `test_racing_hooks_...`, `test_a_changed_closing_line_while_a_worker_runs_...`, `test_a_worker_born_for_another_closing_line_does_nothing`. |
| H3 | Windows fallback starts the worker inside the hook's job | PARTLY ACCEPTED. Refusing to start would lose the lane-end report in exactly the environment where breakaway is forbidden, which is worse than a worker that may not outlive the session. The fallback is kept, but the receipt now carries `detached: false` and the claim reason says "breakaway ... refused", so the run never claims what it did not get; H1's reaper closes the claim if the worker is taken down. Test `test_a_refused_breakaway_is_recorded_not_claimed_as_detached`. Live evidence of which branch this box takes is in the session file. |
| H4 | failure/concurrency paths untested | FIXED. The six tests above; see Vacuity. |

## Timings (Done-contract 3) against the declared 15-second Stop limit

Measured on this box (Windows 11, `.venv` python), each row a median or single run as stated.

- Skip path (no HANDBACK line), `python scripts/lane_end_guard.py` directly: median 262-288 ms, max 356 ms over 7 runs.
- Skip path through the declared command under git-bash (`python "$CLAUDE_PROJECT_DIR/..." || true`): median 733-786 ms, max 1082 ms; git-bash's own spawn is about 0.5 s of that.
- Skip path as the harness ran it in this lane's transcript (first `stop_hook_summary`, three hooks in parallel, a Codex review running): 1240 ms. Well inside 15 s, but not "well under a second" under load.
- Hook path with a HANDBACK line (claim + detached spawn): process wall 357 ms. `guard_ms` in the receipt counts from module import, so it excludes the ~250 ms interpreter start.
- Full moment (`doit moment:lane-end`: precondition, lane_cost, seat_health, transport_report, each a `uv run` launch): 14 327 ms on an idle box (organs 264 + 1844 + 2577 + 1671 ms, the rest `uv`/`doit`/wrapper launches). That is at the 15 s limit with nothing else running, so waiting for it inside the hook cannot be made to fit. First design (wait up to 12 s, leave the moment running) recorded OVER-BUDGET on its first real run; the moment now runs in a detached worker and the hook returns in the time above.

## Vacuity (WAVE3-COMMON rule 3)

Each acceptance test was shown red against a mutant of the implementation or of `settings.json` (run of `tests/test_lane_end_guard.py`, one mutation at a time, file restored after):

```
always runs (no HANDBACK check)          RED  3 failed
blocks with exit 2 on failure            RED  2 failed
hook waits for the moment (no detach)    RED  1 failed
worker deadline kills the moment         RED  2 failed
all crash catches removed                RED  2 failed
no reaping of an abandoned claim         RED  1 failed
claim marker not exclusive               RED  7 failed
worker overwrites a newer claim          RED  1 failed
worker ignores its key                   RED  1 failed
breakaway refusal not recorded           RED  1 failed
guard entry removed from settings        RED  3 failed
|| true dropped from settings            RED  1 failed
```

Two mutants first survived and exposed real test gaps, fixed before this record: a weak "always runs" mutant (`None == None` still skipped) and the CLI entry's `detach=True` default, which no test reached until `test_the_script_as_the_hook_runs_it_drives_the_real_doit_moment` ran the script through the real `doit`. One redundancy is by design: with only the inner `except BaseException` removed the outer one still yields the same receipt, so the crash test goes red only when both are removed.
