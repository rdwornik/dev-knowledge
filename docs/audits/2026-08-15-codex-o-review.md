# Codex Review — lane O (`[#527]` block-commit-on-main)

**Date:** 2026-08-15
**Branch:** `worktree-lane-o-527-block-main`
**HEAD:** `9732daea`
**Diff range:** `main..worktree-lane-o-527-block-main` (base `main` @ `d62796ad`)
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra`
**Review profile:** code
**Merge this review covers:** `60eefbb7`

---

## Provenance — read this before reading a finding

**This artifact is a TRANSCRIPTION, not a fresh review run.** The review executed
2026-08-15 during phase-1 integration; its verdicts were captured to the operator's
`~/Downloads/PHASE1-TERRA-RAW-2026-08-15.md` and cited from there by
`PHASE1-REVIEW-PACKET.md` §3, but no in-repo artifact was ever landed. That is the
defect this file closes: `review_artifact_coverage` counted the merge as unlinked,
so a real review was indistinguishable in the tree from a remembered one — the exact
unfalsifiable-claim class `[#480]` exists to end.

Landed at phase-2 Position 0 per ruling §A10 (W9). The finding text below is quoted
verbatim from that record; the adjudication is the phase-1 one, likewise verbatim. No
verdict is re-derived here, and nothing is back-dated: the `Date:` field is the date
the review ran, and this file's own landing date is 2026-08-16.

**Invocation, as recorded:** `codex exec review --base main`, run from inside the
lane's own worktree so the reviewed diff is that lane's range against `main`.

---

## Findings

## CRITICAL

(none)

## HIGH

### `scripts/block_commit_on_main.py:83-84` — [P1] Fail closed when branch resolution errors

> The hook covers the intended commit scenarios, but a Git error during branch detection silently
> disables the new gate despite its explicit fail-closed contract.
>
> Review comment:
>
> - **[P1] Fail closed when branch resolution errors** — `scripts/block_commit_on_main.py:83-84`
>   When `git symbolic-ref HEAD` fails for reasons other than a detached HEAD, this treats the failure
>   as `None`, causing `refuses()` to return false and silently allowing the commit. This contradicts
>   the hook's documented fail-closed posture; distinguish the expected detached-HEAD exit from other
>   Git errors and raise on the latter.

**Adjudication (phase-1, verbatim):** Verified in-tree — `current_branch()` at
`scripts/block_commit_on_main.py:73-86` returns `None` on any non-zero return code, and
its own docstring names this as a deliberate stated hole copied from upstream
`no_commit_to_branch.is_on_branch`. The real defect is **inconsistency with the sibling
`merge_in_progress()`** (same file, ~line 89), which **raises** on git failure by
explicit design. **Operator decision, not an unnoticed bug.**

## MEDIUM

(none)

## LOW

(none)

---

## Where this finding went

It did not evaporate. The honest limit it names travels **verbatim in the `[#527]`
closing commit** and is written into the `CLAUDE.md` §9 roster row for
`block-commit-on-main`: *`current_branch()` silently allows on git failure;
`block-ff-push` remains the real teeth.* Closing `[#527]` therefore records the hole
rather than papering over it — the row's Done-when was met, and the fail-open path is
carried as a stated, operator-owned limit.

## Honest limit of this artifact

It records that the review happened, against which branch and range, and what it said.
It does not re-verify the finding on today's tree. Line numbers are as-of `9732daea`.
