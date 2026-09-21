# Codex Review — lane-merge-truth

**Date:** 2026-09-21
**Branch:** `worktree-lane-merge-truth`
**HEAD:** `fa026fcd`
**Diff range:** `main..worktree-lane-merge-truth`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/merge_receipt.py: default_lane_worktree / cmd_models -- explicit --worktree still wins; absent dir keeps repo-root default.
- scripts/audit_checks/check_organ_truth.py: declared_callers reads .pre-commit-config.yaml and conductor.yml; armed or dated-manual counts, UNDATED manual must not; the conductor --hook-stage manual sweep honours SKIP; roster is NOT narrowed; every uncalled organ is named.
- scripts/go_reader.py: reads only, writes no GO; batch validated as one filename token; unresolvable transport is a refusal; exit codes.
- tests/test_lane_merge_truth.py: any vacuous assertion; the declared harness rows are run as written.

---

## Findings
## Critical

(none)

## High

### scripts/go_reader.py:83 — unmounted authoritative transport can fall back to a different process path

**What:** A `dispatch.prompts_dir()` refusal is caught, then `CLAUDE_PROMPTS_DIR` from the process environment is used anyway.  
**Why:** An unmounted User-scope transport can therefore be replaced by a stale inherited path and return a false GO.  
**Fix direction:** Preserve the dispatch refusal as an unresolved transport; do not fall back after it rejects the authority path.

### scripts/audit_checks/check_organ_truth.py:128 — conductor `SKIP` is read only from the step environment

**What:** `_conductor_steps` ignores workflow- and job-level `env.SKIP`, both of which apply to a step in GitHub Actions.  
**Why:** A manual hook skipped at either scope is counted as called, masking an uncalled organ.  
**Fix direction:** Resolve effective `SKIP` across workflow, job, and step environments with normal override precedence.

### tests/test_lane_merge_truth.py:360 — declared GO-reader harness row is not run as written

**What:** The test strips the launcher and script path from the declared argv, then invokes the imported Click command directly.  
**Why:** It cannot catch a failure in the actual `uv run --locked python scripts/go_reader.py ...` harness invocation.  
**Fix direction:** Execute the full expanded argv in a subprocess, as the models-row test does.

## Medium

(none)

## Low

(none)

---

## Disposition (recorded by the lane, commit `c38f98d1`)

All three findings were real and are fixed, each with a test that goes red when the fix is removed:

- **go_reader transport fallback** -- a `dispatch.prompts_dir()` refusal now stands (unresolved -> REFUSED); the process copy of `CLAUDE_PROMPTS_DIR` is read only when the dispatcher cannot be imported. Test: `test_a_dispatcher_refusal_of_the_transport_stands`.
- **conductor `SKIP` scope** -- resolved workflow -> job -> step, narrower overriding wider. Tests: `test_a_hook_skipped_at_any_scope_of_the_conductor_is_not_called_by_it`, `test_a_narrower_skip_replaces_a_wider_one`.
- **go_reader row not run as written** -- the full expanded argv now runs in a subprocess. Test: `test_the_declared_go_reader_row_runs_as_written_and_refuses_an_absent_go`.

Note on the first pass of this review: it ran before the lane had synced `main`, so `main..HEAD` also showed the reverse of W3-A's `harness.yaml` / `dodo.py` work and reported two findings about those files. Those were an artifact of the stale base, not defects; the review above is of the synced diff (`HEAD fa026fcd`).

