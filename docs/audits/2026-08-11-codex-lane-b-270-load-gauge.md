# Codex Review — lane-b-270-load-gauge (five passes)

**Date:** 2026-08-11
**Branch:** `worktree-lane-b-270-fleet-audit`
**HEAD:** `817528b9`
**Diff range:** `5259b0f0..worktree-lane-b-270-fleet-audit` — `scripts/fleet_health.py`,
`tests/test_fleet_health.py`, `.gitignore`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (ad-hoc `codex exec`, read-only sandbox — the committed diff is not a
staged diff, which is the fallback PLAYBOOK §16 sanctions for a one-off read)
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469]), `model_reasoning_effort=high`
**Review profile:** code
**Persisted per:** [#480] durability — a review that exists only in a session is not evidence

**Tally:** 0/16/0/0 (C/H/M/L)

---

## Why five passes

Batch-4 lane W2's frozen contract makes review mandatory on code impact. The repo's own terra
lesson is that a review loop is run *until a clean pass*, because each re-run finds what the
last one graded clean. That is exactly what happened, and the count per pass — **4, 4, 3, 3,
2** — is the record of it. Each pass was told what the prior passes had already fixed and
what had been deliberately declined, so no finding below is a restatement.

## Focus (as given to the reviewer)

The gauge is a SessionStart surfacing organ that must never break a session. The contracts
the review was asked to attack: fail-soft in full; an unavailable producer renders `n/a`,
never `0` (0 is a measurement); the CSV is append-only, header written once, one row per
SUCCESSFUL digest run; ASCII-only output (cp1252 console); stdlib only. Passes 2–5 were also
asked to *refute the comments* — two comments were duly proven false.

## Findings

## Critical

None, in any pass.

## High

**Pass 1 — fixed at `a97842df`**

- `scripts/fleet_health.py` — `gh issue list` page-caps at 30 without `--limit`; the funnel
  would silently understate itself past 30 open Issues, going blind at the saturation it
  exists to detect.
- `scripts/fleet_health.py` — an unreadable `BACKLOG.md` degraded to `""` and was reported as
  an EMPTY backlog and zero pending closures: a serene funnel rendered at the moment the repo
  could not be read.
- `scripts/fleet_health.py` — the CSV header could be written twice; existence was tested
  before the open, so a scheduled run and an interactive SessionStart could both emit it.
- `scripts/fleet_health.py` — the `ARCHITECT-REVIEW-PENDING` patterns matched any heading or
  bold run containing the token, so prose ABOUT the marker counted — recreating the
  false-positive class the lever was built to remove.

**Pass 2 — fixed at `339d9f61`**

- The CSV recovery path still TRUNCATED a concurrent writer's row. This refuted the comment
  written one commit earlier, which claimed an empty-but-existing file could only come from a
  truncated prior run: `O_EXCL` creates a zero-byte file, so a racing writer genuinely
  observes size 0.
- `--limit 1000` moved the blindness rather than removing it — the ceiling was reported as
  though it were an exact count.
- One cp1252 byte in the trend history killed the ENTIRE gauge: `UnicodeDecodeError`
  subclasses `ValueError`, which neither `OSError` nor `csv.Error` catches, so corrupt
  *history* destroyed the *current* measurement.
- An orphan trend row could outlive a digest that never landed (row appended before
  `_atomic_write`).

**Pass 3 — fixed at `6617d1d4`**

- The CREATOR still held an offset-zero descriptor, so a racer's appended row could be
  overwritten. Second race fix in a row that had left a narrower version of the same race.
- Unreadable producer FILES were swallowed with `continue`, so a partial tally went out as a
  measurement.
- `ARCHITECT-REVIEW-PENDING` — **split decision.** The item shape was tightened to require a
  structured id (accepted, no recall cost). Tightening the HEADING to the one observed
  literal was **DECLINED**: for a debt gauge a miss is worse than a false positive, because a
  miss silently under-reports load, which is M1's own failure mode. A test pins the
  broad-recall behaviour so a later tightening argues with a test, not a comment.

**Pass 4 — fixed at `289301a0`**

- The delta compared INCOMPATIBLE totals: a partial total minus a complete one produced a
  precise signed number for a change nobody measured (a baseline of `triage 90` against an
  unavailable triage today rendered `-90` — the funnel "collapsing" when it was unobserved).
- The same-day baseline picked the OLDEST run of the day, contradicting the function's own
  "newest stored row" contract. One row per RUN makes same-day rows the normal shape.
- An unreadable producer DIRECTORY was still a measured zero (`Path.exists()`/`glob()` both
  swallow a directory-access `OSError`).

**Pass 5 (convergence check) — fixed at `817528b9`**

- Well-formed JSON of the wrong shape was counted: `[{"number": "not-an-int"}]` and `[null]`
  parse as one-element lists and rendered `1 triage`.
- A CORRUPT historical cell could still be a "complete" delta baseline — pass 4's guard
  tested `!= "n/a"` rather than parseability, leaving a hole in exactly the case (damaged
  history) it was written for.

## Dispositions

Every finding is **fixed**, except the two recorded declines — the heading-recall tradeoff
above, and a duplicate header line under a true create race (accepted residual: it never
costs a measurement, and a cross-process lock is not bought for a local trend meter). Both
declines carry tests. Nothing was dropped silently.

## Where the loop was stopped, and why

Passes 4 and 5 returned only follow-ons to the previous pass's own fixes rather than anything
about the design — the review had begun auditing its own last answer. A sixth pass would keep
finding narrower variants. Stated plainly rather than left to inference: **this is a
judgment that the loop converged, not a demonstration that a sixth pass would be empty.**

## Evidence the tightening cost no live signal

Narrowing a detector risks trading false positives for misses. The live measurement is
byte-identical before pass 1 and after pass 5:

```
[load] funnel 44: 15 triage / 0 closures / 27 dispositions / 2 review-pending;
       backlog: 7 P1 / 91 P2 / 100 P3; 7d delta: n/a
```

Each figure cross-checks against its producer independently of the code under review — the
triage 15 equals the same session's `surface_triage.ps1` SessionStart line, dispositions 27 a
direct grep of the register, backlog 7/91/100 a direct grep of `BACKLOG.md`.

## The pattern worth keeping

Three of the sixteen findings were the same contract (`n/a`, never 0) failing at successively
lower boundaries — the value, then the file, then the directory — each caught by the reviewer
rather than by me. Two more were guards that tested for the ANTICIPATED failure token
(`!= "n/a"`, `isinstance(payload, list)`) instead of for validity, so anything unanticipated
passed. Stating a contract in a docstring is not the same as enforcing it at every boundary
the data crosses.
