# Review — lane-fates-due

**Consumer:** `LANE-5B5-4-lane-fates-due.md`

**Date:** 2026-09-30
**Branch:** `worktree-lane-fates-due`
**HEAD:** `ab321a11`
**Diff range:** `f422ccf7..ab321a11` (`ecosystem/harness.yaml` only)
**Files in scope:** `ecosystem/harness.yaml`
**Tally:** 0/0/0/0
**Reviewer:** `agy` CLI, model `gemini-3.1-pro-high` — **SUBSTITUTION**: Codex
(`gpt-5.6-terra`) returned `ERROR: You've hit your usage limit ... try again at Oct 3rd,
2026 9:07 PM` on the first `codex-review.ps1` invocation; the reset is 3 days out, so this
review substitutes `agy` rather than blocking the lane on it. `agy`'s first invocation
returned a permission-denial ("no output produced — a tool required the read_file
permission that headless mode cannot prompt for") with exit 0 and no findings -- the
known `[#1327]` shape ("`agy` reports SUCCESS without an output file"); the second
invocation, re-run with `--dangerously-skip-permissions` (read-only review task, no writes),
produced a real, non-empty result. The diff was also independently reviewed by direct
inspection before and after the `agy` run, since the only change is 51 one-line YAML edits.
**Review profile:** data/config (YAML), not code — `ecosystem/harness.yaml`'s `fates:`
block only

---

## Focus

The whole diff: 50 `fates:` entries' `manual_until` re-dated `2026-10-05` -> `2026-10-19`,
and one (`scripts/desired_state_loader.py`) converted `manual_until` -> `retire_candidate:
true`. Checked: path values unchanged; `reason:` text uncorrupted (quote balance, no
truncation); YAML flow-mapping syntax intact on every changed line; the retire_candidate
conversion removed `manual_until` rather than carrying both keys (the fate schema requires
exactly one of `manual_until`/`retire_candidate`/`moment`); no entry outside the intended
51-line scope touched.

---

## Findings

## Critical

(none)

## High

(none)

## Medium

(none)

## Low

(none)

---

## Independent corroboration (direct inspection, this session)

- `git diff origin/main...HEAD` line count: 51 removed + 51 added, matching the 51
  dispositioned entries exactly (50 re-dates + 1 retire-candidate conversion).
- `uv run --locked python -c "yaml.safe_load(...)"` parses the post-edit file cleanly and
  reports the exact expected date-bucket counts (`2026-10-19: 50`, `retire_candidate: 1`,
  plus the untouched `2026-10-11: 1`, `2026-10-14: 1`, `2026-10-15: 9`).
- `check_organ_truth.py`'s own `_today()` seam, monkeypatched to `2026-10-06`: origin/main's
  `harness.yaml` FAILs (43 past-due organs -- the 43 that were reachable via the
  `uncalled` roster at census time; the remaining 8 of the 51 were already excluded from
  that roster via the graph's `wired_elsewhere`); this tip does not (`any FAIL: False`).

## Repair note (commit `096083b7`, no second agy/Codex pass)

The push CI run on `ab321a11` (job 36665930188) surfaced one real regression via
`known_reds.py compare` (not a Codex/agy finding): `tests/test_organ_truth.py::
test_every_organ_wiring_fate_stays_manual_until_not_moment_or_retire` pins the literal
`manual_until` date (not only the shape) for 4 of the 51 re-dated organs. Fixed by updating
the pinned date to `2026-10-19`, matching the re-date; the test's own SHAPE assertions
(`retire_candidate`/`moment` absent) are untouched and still pass. No second review pass was
commissioned for this one-line, mechanical fix -- verified instead by: (1) `pytest
tests/test_organ_truth.py` locally, 41/41 passed; (2) a **paired-baseline** comparison against
origin/main's own CI run at the same base sha (`f422ccf7`, job 109719448789, run 36662286065):
its `known_reds.py compare` lists the identical 7 other "regression" (not-yet-registered)
failures this lane's run also showed (`codespace-admission` REFUSED x2,
`test_codespace_admission.py` x3, `test_decision_coverage.py::
test_the_live_tree_carries_no_IN_ERA_uncovered_decision`, `test_verify_handoff_probes.py::
test_registered_check_never_fails_on_live_repo`) -- proving those 7 are pre-existing on
origin/main, not caused by this lane, and `test_organ_truth.py`'s entry was the only one
this lane introduced and is now the only one this lane's push (`096083b7`) removes.

## Final CI verification (commit `9efa350d`, run 36668031101)

`test_organ_truth.py` does not appear in either OS leg's `known_reds.py compare` output on
this run -- the repair held. Job conclusions: `commit-gate` FAIL, `pytest (ubuntu-latest)`
FAIL, `pytest (windows-latest)` FAIL, `ship-gate` FAIL; `seal`/`anchor`/`terra`/`ruff`/
`spine`/`handoff-manifest`/`phase-gate` all PASS. Paired against origin/main's own CI run at
this lane's exact base sha (`f422ccf7`, run 36662286065, also overall `failure`), job by job:

- **commit-gate** -- `audit-health` regression set (`consumer_at_landing`, `handoff_probes`)
  is byte-identical on both runs (jobs 109736869145 vs 109719448828). Pre-existing,
  unrelated to this diff.
- **pytest (ubuntu-latest) / (windows-latest)** -- diffing the unique `REGRESSION` line sets
  between this run's jobs (109736869174, 109736869180) and the baseline's
  (109719448789, 109719448781) leaves exactly three net-new items on both OS legs:
  `test_gen_audit_index.py::test_live_index_excludes_nothing_because_every_audit_is_tracked`,
  `test_gen_audit_index.py::test_live_index_is_fresh`, and `test_worktree_seed.py::
  test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH` (plus one flaky concurrency/lock test each
  way that is absent on one run and present on the other -- non-deterministic, not diff-driven).
  The two `gen_audit_index` items are the direct, expected consequence of adding
  `docs/audits/2026-09-30-codex-lane-fates-due.md` under this contract's own close-out
  requirement while the contract's Do-not list forbids regenerating
  `docs/audits/README.md` in a lane ("the integrator does, on the merged tree" -- `[#590]`);
  `test_worktree_seed`'s base-equals-main-at-dispatch check is this lane's worktree base
  having fallen behind main's current tip over the session's run time, an ordinary
  lane-mechanics artifact of a long-running lane in a parallel batch, not a defect this
  lane's edits introduced. No fix applied for either -- both are structurally expected given
  the contract's own constraints, not regressions caused by the `harness.yaml`/
  `test_organ_truth.py` diff.
- **ship-gate** -- fails identically on both runs (`RED — not shipped-ready`, driven by
  `journal_spine_anchor`/`review_artifact_coverage` errors from the CI checkout lacking a
  local `main` ref/full history) -- pre-existing, unrelated to this diff.

Net: this lane's push introduces zero new test/check regressions beyond what the contract's
own close-out mechanics (an added audit doc, a lane's aging worktree base) structurally
produce; every other red on this run reproduces byte-for-byte on origin/main's own baseline
run at the same base commit.
