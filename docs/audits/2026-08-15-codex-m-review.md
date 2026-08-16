# Codex Review — lane M (`[#529]` telemetry emit)

**Date:** 2026-08-15
**Branch:** `worktree-lane-m-529-telemetry-emit`
**HEAD:** `d45fdb9e`
**Diff range:** `main..worktree-lane-m-529-telemetry-emit` (base `main` @ `d62796ad`)
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra`
**Review profile:** code
**Merge this review covers:** `4ad2025d`

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
lane's own worktree so the reviewed diff is that lane's range against `main`. Codex was
invoked directly rather than through `~/.claude/bin/codex-review.ps1`, because that
wrapper writes its artifact into `docs/audits/` and phase-1's harvest was read-only.

---

## Findings

## CRITICAL

(none)

## HIGH

### `scripts/telemetry_emit.py:272-275` — [P1] Route linked worktrees to the shared telemetry store

> The default database path creates separate, disposable telemetry stores for linked worktrees.
> This breaks the core single-log requirement and causes lane events to be lost during normal
> cleanup.
>
> Review comment:
>
> - **[P1] Route linked worktrees to the shared telemetry store** — `scripts/telemetry_emit.py:272-275`
>   When hooks or checks run from linked worktrees, `_REPO_ROOT` is that disposable worktree, so each
>   lane writes to its own `logs/TELEMETRY.db` rather than the single repository event log. Those
>   records are partitioned from main and deleted during worktree cleanup, silently losing precisely
>   the parallel-lane telemetry this WAL store is intended to collect; resolve the main worktree via
>   Git's common directory or use an explicitly shared durable path.

**Adjudication (phase-1, verbatim):** Verified in-tree — `scripts/telemetry_emit.py:110`
reads `_REPO_ROOT = Path(__file__).resolve().parent.parent`; line 275 returns
`_REPO_ROOT / DEFAULT_DB_RELPATH`. **Finding stands.** Latent: no call sites exist yet.
Fix precedent in-repo: `scripts/fleet_analytics.py:1076` resolves
`git rev-parse --git-common-dir` for exactly this worktree-sharing reason.

## MEDIUM

(none)

## LOW

(none)

---

## Honest limit of this artifact

It records that the review happened, against which branch and range, and what it said.
It does not re-verify the finding on today's tree, and landing it does not close
`[#529]` or discharge the finding — the finding remains open work, and the line numbers
above are as-of `d45fdb9e`, not as-of `main` today.
