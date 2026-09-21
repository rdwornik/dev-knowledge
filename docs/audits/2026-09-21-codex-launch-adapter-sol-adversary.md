# Codex sol adversarial pass over `dispatch.py launch` (LANE-W3-B, Done-contract 8)

> **Status:** record. Lane `lane-launch-adapter`, branch `worktree-lane-launch-adapter`. Carrier: LANE-W3-B. This is the
> adversarial pass on the `launch` INTERFACE; the terra diff review is `2026-09-21-codex-lane-launch-adapter.md`.

**Consumer:** `[#931]` — the row this review served (Wave 3 lane B, `lane-launch-adapter`): its Done-when item 7 requires the Codex sol adversarial pass on the `launch` interface, and this file is that pass.

## How it was run

```
Get-Content adv-prompt.txt -Raw | codex exec -c model=gpt-5.6-sol --sandbox read-only --json --skip-git-repo-check -o adv-last.txt - > adv-events.jsonl 2> adv-err.txt
```

- **Requested model: `gpt-5.6-sol`** (R-W3-8: sol is the adversarial default). `codex exec` reports no served model, so
  "sol answered" is attested by the flag, not by the output -- the same limit `2026-09-20-codex-loop-eval-mapping-adversary.md`
  recorded. Exit 0; stdin closed by the pipe; read-only sandbox; no write mode.
- **Usage reported** (`turn.completed`): input 390,640 (326,272 cached), output 4,633, reasoning 1,596. No cost is reported by
  `codex exec`; none is invented here.
- **Prompt:** an adversarial brief scoped to ONE interface (the five Done-contract clauses that describe it), telling the critic
  that R-W3-2 supersedes the older "the hub never spawns" split (so that is not a finding), and listing seven attacks:
  collision/TOCTOU, any route that could stop a run, the Dispatch block as an execution surface, refusal honesty,
  model/name reporting, `run_prelaunch`, and tests that cannot fail. It required a quoted claim, a path and line opened, a
  concrete failure scenario, and a severity.
- **Snapshot caveat.** Sol read the working tree while the lane was mid-fix: the lock and fresh-receipt tests were written (red)
  and the implementation that satisfied them had not landed. Findings 1 and 2 describe that instant truthfully; the
  dispositions below say what the tree does now.

## The findings, verbatim

1. **Critical -- collision protection is nonexistent during the decisive TOCTOU window.**
   Claim attacked: "`launch_lane`: 'Refuse a collision, run `pre-launch`, and only then spawn -- exactly once.'" Opened
   `scripts/dispatch.py:723-733`, `:753-771`, `:782-804`. Two `launch` processes for one slug both read the old receipt/listing,
   both pass `pre-launch`, both reach `spawn`; no lock or atomic claim exists. A completed first `claude --bg` has no receipt
   until up to four listing polls later. `_held_by` returns empty whenever the recorded job is not yet listed; an `"unresolved"`
   receipt searches for that literal id and never falls back to the worktree. Codex receipts only help once written. Wrong
   outcome: two processes enter one lane/worktree.

2. **Critical -- the supposed collision tests specify behavior the implementation does not contain.**
   Claim attacked: test `test_two_launches_of_one_slug_cannot_run_at_once_a_lock_refuses_the_second`. Opened
   `tests/test_dispatch_launch.py:615-621`; absence confirmed across `scripts/dispatch.py:534-818`. The test plants a
   `LAUNCH-LOCK-*` file and expects a refusal; production code never reads, creates or removes one. The fresh-receipt test
   expects an unlisted job to hold the slug while `_held_by` releases it. Even if patched to notice a file, the test would not
   exercise two concurrent callers competing for an atomic lock.

3. **High -- a provider can start successfully and then escape without any durable receipt.**
   Claim attacked: "On a pass it spawns the provider ... and writes a launch receipt and a job-to-lane record." Opened
   `scripts/dispatch.py:771-805`, `:808-818`. `claude --bg` returns success (or `codex exec` is detached), then `_write_json`
   fails (directory unavailable, full, read-only) or the process is interrupted. The receipt is written only after the spawn and
   is unprotected. The lane keeps running, `launch` exits through an exception, no receipt exists, a retry can launch a
   duplicate; and it falsifies `LaunchRefused`'s "nothing is running".

4. **High -- exit zero with no Claude job ID is recorded as a successful launch.**
   Claim attacked: "writes a launch receipt and a job-to-lane record". Opened `scripts/dispatch.py:780-804`, `:811-818`.
   `claude --bg` exits 0 with changed, localized, truncated or empty output and the job stays absent from the listing for four
   polls. `_JOB_ID` finds nothing; the code writes a successful `exit_code: 0` receipt and `LAUNCH-JOB-unresolved.json`. The CLI
   reports "launched ... job unresolved" though it cannot establish that any lane started; multiple unresolved launches overwrite
   one job record.

5. **High -- the mandatory occupancy refusal is declared optional and can become a successful skip.**
   Claim attacked: "`run_prelaunch`: 'The organs are whatever the file declares -- occupancy ...; a non-zero exit is a refusal.'"
   Opened `ecosystem/harness.yaml:45-49`, `scripts/dodo.py:257-283`. `worktree_occupancy` is declared `optional: true`; a missing
   script becomes `SKIPPED-NOT-BUILT`, the wrapper exits 0, `run_prelaunch` returns `PreLaunch(True)` and spawns without the
   collision organ. An unset `{batch}` correctly refuses because the integrator row is not optional.

6. **High -- the Dispatch parser permits flag smuggling through known option values.**
   Claim attacked: "Anything else on the line -- a pipe, a second command, an unknown flag -- is ignored, so the block is not an
   arbitrary-execution surface." Opened `scripts/dispatch.py:379-390`, `:406-425`, `:521-530`. `--permission-mode
   --dangerously-skip-permissions` (or a flag-looking `--model` / `--effort` value): `_VALUE_FLAGS` consumes the next token
   whether or not it begins with `-`, and model / permission mode are not validated; `build_plan` places the token in argv. The
   cited test (`assert not any("calc" in a for a in argv)`) is toothless: it passes for an empty or stubbed argv.

**Verdict (sol):** Reject. "The core single-launch guarantee is not merely racy; the implementation has no atomic claim at all,
and newly added tests demand lock behavior that does not exist. Receipt handling can leave live but unrecorded jobs, an
unidentified Claude launch is falsely recorded as success, and the declared pre-launch collision organ may be skipped
successfully. I found no direct `taskkill`, signal, terminate, or kill path in `govern` or the shim, so N3 is not the problem
here -- the launch boundary's collision and honesty guarantees are."

## Dispositions (recorded by the lane)

Every claim was checked against the tree before it was accepted. All six were ACCEPTED; none rejected.

| # | Verdict | What was done | Commit | Witness |
|---|---|---|---|---|
| 1 | ACCEPT (true at the snapshot) | `_SlugLock` (exclusive-create `LAUNCH-LOCK-<SLUG>` under the receipts dir, removed on every exit path, never stolen); `_held_by` now also holds the slug for a live lane in `.claude/worktrees/<slug>` whatever its id, and for a receipt younger than `LISTING_LAG_SECONDS` whose job the listing has not shown; a codex receipt holds while its pid is alive; an **intent receipt** (`job_id: pending`) is written before the spawn | `3a3a9f00` | `test_two_launches_racing_for_one_slug_spawn_exactly_once` (two real threads, a barrier, a 0.4 s spawn: one spawn, one refusal), `test_a_fresh_receipt_whose_job_...`, `test_a_launch_whose_job_id_was_never_read_...`, `test_a_live_lane_in_the_worktree_...`, `test_a_codex_receipt_whose_process_is_alive_...` |
| 2 | ACCEPT (true at the snapshot; the tests were red-first) | The implementation landed after the snapshot; the concurrency gap sol names ("would not exercise two concurrent callers") is closed by the racing-threads test above | `3a3a9f00` | 63 tests green, and each acceptance test is shown red under a mutation (session file, vacuity check) |
| 3 | ACCEPT | Post-spawn work cannot lose the receipt: the intent receipt precedes the spawn; an unreadable listing leaves the ids blank, never aborts; a receipt write that fails after a start raises `LaunchIncomplete` (exit 8, "WAS started ... nothing was stopped"), not `LaunchRefused`; a spawn that failed removes its intent receipt | `3a3a9f00` | `test_a_launch_interrupted_after_the_provider_started_...`, `test_a_spawn_that_failed_leaves_no_intent_receipt_behind`, `test_a_lane_that_started_always_gets_its_receipt_...` |
| 4 | ACCEPT -- and a **live launch confirmed it** | The first live `claude --bg` returned `job_id: unresolved`: the real output is `backgrounded · <ESC>[36maea4c0ba<ESC>[39m · <name>`, and the old regex stopped at the colour code's digits (the retired shim had the same pattern). Fixed: ANSI is stripped before the match; a lane that already finished is identified by its worktree and start time; an unidentified start is `LaunchIncomplete` (exit 8), writes an `unresolved` receipt that still holds the slug, and writes no `LAUNCH-JOB-unresolved.json` | `3a3a9f00` | `test_the_job_id_is_read_from_the_real_claude_bg_output_...` (fixture is the captured real stdout), `test_a_lane_that_already_finished_...`, `test_an_older_record_in_the_same_worktree_...`, `test_a_start_whose_job_cannot_be_identified_is_exit_8_...` |
| 5 | ACCEPT | `run_prelaunch` reads the DECLARED moment's organ receipts after a zero exit and refuses when any is missing, `SKIPPED-*`, or non-zero. It names no organ: the list comes from `ecosystem/harness.yaml`, which this lane does not edit (the `optional: true` on the occupancy row is W3-A's to change; see the handback) | `3a3a9f00` | `test_a_pre_launch_organ_that_was_skipped_does_not_clear_the_launch`, `..._missing_organ_receipt_...`, `..._all_ran_clears_...` |
| 6 | ACCEPT | Values taken after `-n` / `--worktree` / `--model` / `--effort` / `--permission-mode` must not start with `-`; model must be a model name; effort must be in the enum; permission mode must be one of `claude --help`'s six; the argv is asserted EXACTLY (not "contains no calc") | `3a3a9f00` | `test_a_dispatch_value_that_is_a_flag_or_off_enum_is_refused` (4 cases), `test_the_argv_is_built_from_the_parsed_fields_and_nothing_else` |

**On the N3 finding.** Sol found no stop, signal, terminate or kill path in `govern`, `launch` or the shim. That is asserted
by `test_the_module_has_no_path_that_can_stop_pause_or_kill_a_lane` (a structural test over the module's code) and by the
tripwire tests, which fail on ANY process start from inside a `govern` run.

**Residual, stated.** The lock serialises launches made through this adapter. A lane started by some other route in the window
is caught only by the `pre-launch` occupancy organ's four legs (whose session leg has the same listing lag). The receipt's
`launched_at` window (`LISTING_LAG_SECONDS = 180`) is a judgement, not a measurement.
