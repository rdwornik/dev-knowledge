# Codex Review — lane N (`[#528]` legs 1+2, latency)

**Date:** 2026-08-15
**Branch:** `worktree-lane-n-528-legs12-latency`
**HEAD:** `03814f6c`
**Diff range:** `main..worktree-lane-n-528-legs12-latency` (base `main` @ `d62796ad`)
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra`
**Review profile:** code
**Merge this review covers:** `7d1f6ce0`

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

### `protocols/PLAYBOOK.md:882-883` — [P1] Make the live_repo grouping rule executable

> The new xdist safety doctrine claims that `live_repo` tests are kept on one worker, but neither
> the marker configuration nor the new verify invocation implements that behavior.
>
> Review comment:
>
> - **[P1] Make the live_repo grouping rule executable** — `protocols/PLAYBOOK.md:882-883`
>   For runs selecting `live_repo` tests from multiple files, neither scheduler provides the promised
>   grouping: `loadfile` creates a separate group per file, while `loadgroup` only honors
>   `xdist_group` marks, which this suite does not assign. Moreover, the newly cited live call site
>   uses `--dist worksteal`, so these tests remain distributed across workers. Add marker-to-group
>   wiring and use `loadgroup`, or document a separate invocation that actually serializes this tier.

**Adjudication (phase-1, verbatim):** real doc-precision defect in newly-landed
doctrine. `PLAYBOOK.md` is deliberately outside `DEFAULT_FRESHNESS_FILES` and no gate
consumes this paragraph, so it **blocks nothing**.

## MEDIUM

(none)

## LOW

(none)

---

## Honest limit of this artifact

It records that the review happened, against which branch and range, and what it said.
It does not re-verify the finding on today's tree, and landing it does not close
`[#528]` or discharge the finding. The cited line numbers are as-of `03814f6c`; note
that `protocols/PLAYBOOK.md` has been edited since (phase-2 Position 0 act 1 re-pointed
two citations in the same chapter), so the `882-883` locator should be resolved by
anchor text rather than by line number.
