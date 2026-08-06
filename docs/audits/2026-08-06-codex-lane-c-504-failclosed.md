# Codex Review — lane-c-504-failclosed

**Date:** 2026-08-06
**Branch:** `worktree-lane-c-504-failclosed-claims`
**HEAD:** `47331e26`
**Diff range:** `main..worktree-lane-c-504-failclosed-claims`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- The ONLY change is the module docstring of scripts/block_ff_push.py. Verify the new posture claim is FAITHFUL to the code: does the module actually fail CLOSED (exit 2) on internal error?
- Check main(), _read_stdin(), violations_in_range() against the claim. Flag any residual path that still returns 0 on an internal error.
- Verify the docstring's assertion that _rev_parse and _reconstruct_main_range remain correctly fail-soft, and that leaving them fail-soft is safe.
- Flag any OTHER surface in this file whose prose still claims the retired fail-soft posture.

---

## Findings
## Critical

- `scripts/block_ff_push.py:39` — The new “any internal error → exit 2” claim is false. `violations_in_range()` only validates `git rev-list`; its subsequent delegated `git log` can fail and return `[]`, which makes `main()` return 0. Fix direction: make the violation scan propagate its own Git failures or use an error-distinguishing gate-local scan.

- `scripts/block_ff_push.py:44` — `_rev_parse` / `_reconstruct_main_range` are not safely fail-soft. A `rev-parse` failure is converted to `None`, then `main()` treats it as “not a main push” and returns 0 during the pre-commit reconstruction path. The helper prose at `scripts/block_ff_push.py:159` and `:175` repeats this unsafe fail-soft claim. Fix direction: distinguish a missing ref from a Git/internal error and raise for the latter.

## High

(none)

## Medium

(none)

## Low

(none)