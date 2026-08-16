# Codex Review — lane P (`[#530]` single-flight dispatch guard)

**Date:** 2026-08-15
**Branch:** `worktree-lane-p-530-single-flight`
**HEAD:** `73da833c`
**Diff range:** `main..worktree-lane-p-530-single-flight` (base `main` @ `d62796ad`)
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra`
**Review profile:** code
**Merge this review covers:** `50daad05`

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
verbatim from that record; the adjudications are the phase-1 ones, likewise verbatim.
No verdict is re-derived here, and nothing is back-dated: the `Date:` field is the date
the review ran, and this file's own landing date is 2026-08-16.

**THE `HEAD:` FIELD IS THE REVIEWED TIP, NOT THE MERGED TIP — stated so it is not read
as an error.** The review ran at `73da833c`. The branch tip then moved to `11b0cbdb`,
which adds the integrator fixup ruled by **R2** (one line: `errors="replace"` on the
`_cli` helper's `subprocess.run`, copying lane O's already-solved pattern for the
identical cp1252-vs-strict-utf8 class). `73da833c` is an ancestor of the merged tip and
is therefore inside `50daad05`'s introduced set — verified live — so the linkage holds
on both legs, and the field stays honest about what was actually reviewed.

**Tally note:** 3 raised, and **one of them was subsequently REJECTED** by ruling R3
(below). The header records what the review RAISED — 3 — because a tally that silently
absorbed the adjudication would misstate the review. The disposition is carried in the
finding itself.

---

## Findings

## CRITICAL

(none)

## HIGH

### `scripts/single_flight.py:241-244` — [P1] Keep state-mutating commands outside the validator layer — **REJECTED (R3)**

> - **[P1] Keep state-mutating commands outside the validator layer** — `scripts/single_flight.py:241-244`
>   Whenever `claim` runs, it executes `git update-ref` and pushes a new remote ref, violating this
>   repository's explicit Layer-2 invariant that `scripts/` contains read-only validators and must not
>   drive repository state changes. Move this execution organ to a sanctioned runtime/deployment
>   surface, or formally amend the architectural invariant before merging it here.

**Adjudication — REJECTED AS OVER-STATED (architect ruling R3, 2026-08-15).** Recorded
so the rejection travels with the finding and the P1 is not re-filed by a later reader.

Grounds, re-verified on `main` at integration time: `CLAUDE.md` §5 rule 4's literal
*"Layer 2 never executes — `scripts/` contains read-only validators only"* was **already
descriptively false of the tree as it stood**. ~23 scripts under `scripts/` mutate state
— `arm_hooks.py` installs git hooks, the whole `gen_*.py --write` family rewrites
tracked files, `worktree_seed.py` provisions trees — and `scripts/audit.py:4707` already
runs `git push origin`. A rule the tree violated ~23 times before this lane existed
cannot be the standard by which this lane is judged.

**So the defect is real but MISATTRIBUTED: it is doc-drift in `CLAUDE.md`, not a lane-P
defect.** The finding names the correct tension and the wrong owner; its severity is
also wrong, since a P1 against a lane implies the lane must change before merge, and
nothing about lane P changed here.

> **STATUS UPDATE, 2026-08-16.** The doc-drift this finding correctly identified has since
> been fixed at its real owner: phase-2 Position 0 act 2 re-scoped `CLAUDE.md` §5 rule 4
> per ruling §A3 (Option B). The finding's underlying observation is therefore now
> discharged — at `CLAUDE.md`, not at `scripts/single_flight.py`. The rejection of the
> finding *as filed against lane P* is unchanged.

**What the rejection does NOT say:** it does not say `scripts/single_flight.py` is
well-placed, and it does not ratify state-mutating scripts as correct.

### `scripts/single_flight.py:279-283` — [P1] Delete only the lock generation this caller acquired — **REAL**

> - **[P1] Delete only the lock generation this caller acquired** — `scripts/single_flight.py:279-283`
>   If holder A pauses, its lock is manually cleared and acquired by B, and A later runs cleanup, this
>   unconditional delete removes B's active lock and permits another concurrent execution. The release
>   path needs an ownership-checked deletion using a generation-unique claim token; comparing only the
>   ref SHA is insufficient because multiple claimants commonly share the same HEAD.

**Adjudication:** **REAL.** Filed as an open leg on `[#530]`, which stays **OPEN** —
merged is not closed. Latent today because the guard is wired into no hook (lane
decision 8).

### `scripts/single_flight.py:206-208` — [P1] Distinguish missing local refs from git failures — **REAL**

> - **[P1] Distinguish missing local refs from git failures** — `scripts/single_flight.py:206-208`
>   When `--local-only` is used with a non-repository, corrupt repository, or unreadable ref store,
>   `rev-parse` returns nonzero and this helper reports the lock as absent. Consequently `inspect` can
>   print `FREE` and `release` can return success while the state was never read or changed,
>   contradicting the fail-closed contract; only the specific missing-ref result should map to an
>   empty holder and other failures should raise `SingleFlightError`.

**Adjudication:** **REAL.** Filed as an open leg on `[#530]`, which stays **OPEN**.
Latent today because the guard is wired into no hook.

## MEDIUM

(none)

## LOW

(none)

---

## Additional RED found outside terra — by direct test execution

Not a codex finding; recorded here because it belongs to the same lane and the same
review window, and it is the reason the branch tip moved after review.

`tests/test_single_flight.py::test_an_internal_error_exits_2_not_0_and_not_3` **FAILED**
in a default shell (`1 failed, 19 passed`), reproducing under `-n 0`, so not an xdist
artifact.

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x97 in position 30: invalid start byte
  (raised in subprocess._readerthread)
AttributeError: 'NoneType' object has no attribute 'lower'
  tests/test_single_flight.py:339
```

Chain: `scripts/single_flight.py:331,334` print `internal error — {exc}` with a U+2014
em dash → child writes stderr in cp1252 when `PYTHONUTF8` is unset → byte `0x97` on the
wire → `tests/test_single_flight.py:72-73` decodes `encoding="utf-8"` **strict** →
reader thread raises → `result.stderr is None` → assertion dies with `AttributeError`.

**Fixed by R2** at `11b0cbdb`: `errors="replace"` on the `_cli` helper's
`subprocess.run`. Re-measured in a DEFAULT shell with `PYTHONUTF8` explicitly unset:
**20 passed, exit 0**.

---

## Honest limit of this artifact

It records that the review happened, against which branch and range, and what it said.
It does not re-verify the two real findings on today's tree; both are live open legs on
`[#530]`. Line numbers are as-of `73da833c`, the reviewed tip.
