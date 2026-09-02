# LANE g-276 (deploy-waiver) — end-of-lane artifact

- **Class:** technical · **Date:** 2026-09-02 · **Lane:** `lane-g-276-deploy-waiver`
  (branch `worktree-lane-g-276-deploy-waiver`, contract `LANE-g-276-deploy-waiver.md`)
- **Closes:** `[#276]` D2's remaining gap — the waiver's date handling fails CLOSED
  (Done-contract item 2). Item 1 (both legs read the waiver) was already landed on
  `main` by a prior lane; see the witness finding below.

## Witness (step 1, before any edit)

The single site both legs read the waiver through is
`deploy/carrier_precommit.py:83` `_waived_components` — called by `detect`/`apply`/
`verify` (add leg, lines ~943-995) and by `_prune_waived`/`_classify_prune` (prune
leg, lines ~1011-1024, `_classify_prune` itself at :861).

**Finding: the frozen contract's cited line (`deploy/carrier_precommit.py:777`) has
drifted.** It now falls inside `_verify_satisfied`'s required-local-hooks loop, not
`_classify_prune`. The line was accurate when [#276]'s prior lane (`lane-d-4-deploy-
waiver-honoring`, commit `e9a0af90`) measured it; that lane's own 138-insertion diff
shifted everything below it. Named per Q10/step-1 instruction rather than silently
worked around.

**Finding: Done-contract item 1 ("the prune leg READS the waiver... and the add-leg
re-append is honoured") was already satisfied on `main` before this lane started.**
`e9a0af90` (merged, on `main`, confirmed via `git branch --contains`) wired
`_waived_components` into both legs with 18 passing tests
(`tests/test_carrier_precommit.py`). This lane's steps 1-2 are therefore a
confirmation, not new work — reported per the decision budget rather than
re-implemented, and step 2 needed no commit of its own.

**What was actually still open (Done-contract item 2, the real remaining work):**
`_waived_components`'s own docstring documented the gap explicitly: "staleness
(expiry/review_date) is the Informant's reporting concern... not a second policy
engine here" — an entry was honored on non-empty-`reason` alone, with no date check
at all. That prior lane's own end-of-lane artifact flagged this as an open design
decision ("No expiry/review_date staleness enforcement"); Terra separately recorded
it as failing OPEN on bad dates. That is the gap this lane closes.

## What changed

- `deploy/carrier_precommit.py::_waived_components` now runs every allowlist entry
  through `scripts/enforcement_coverage.py::validate_allowlist_entry` (reused, never
  a second date-policy engine) and only honors entries whose verdict is `AL_VALID`.
  A waiver with no reason, no parseable `expiry`/`review_date`, or a date already
  past `date.today()` is excluded from the returned set — both legs then behave
  exactly as if no waiver had been declared (prune-leg REFUSE stands; add-leg
  re-DRIFTs and `--execute` re-appends the hook). `waivable_policy={}` keeps this
  carrier scoped to the time-box only, never the Informant's separate
  non-waivable-component policing.
  - `run_date` is wall-clock (`date.today()`) here, not threaded as a parameter —
    unlike the Informant's rule, this call happens at actual deploy-action time, not
    a frozen report, and `Carrier.detect(target)`'s signature (`contract.py`, out of
    this lane's write-scope) carries no such parameter to thread it through anyway.
- `.methodology.yaml` — schema NOTE documenting that the time-box now has two
  readers (the Informant, and the deploy tool's waiver check), the ISO-8601 shape,
  and the expiry-wins-if-both-present rule. No entry content changed; all 16
  existing entries carry a well-formed future date and are unaffected.
- `tests/test_carrier_precommit.py` — 6 new tests: three RED-first cases pinning the
  bug (no date, unparseable date, expired date — each wrongly honored before the
  fix), a valid-unexpired contrast, and two end-to-end cases (prune leg REFUSEs on
  an expired waiver; add leg re-appends the hook on an expired waiver). 21/21 green
  after the fix (15 pre-existing + 6 new).

## Commits (this branch)

1. `test(deploy): witness the #276 waiver site and RED the date-fails-open bug` —
   witness note + RED tests, before any production-code edit.
2. `fix(deploy): waiver date handling fails CLOSED, not open [#276]` — the actual
   fix; all 21 targeted tests green.
3. `docs(deploy): schema NOTE -- .methodology.yaml's time-box now has two readers` —
   write-scope schema documentation.

## Delta A2 — verified

Base set: `docs/audits/2026-09-02-verification-base-failed-set-1e064921.json` (13
nodeids, post-G0 `main` at `1e064921`).

Full-suite run (`uv run --locked pytest -q --no-header`, compared with
`scripts/failed_set.py --compare`) reported **18 nodeids not in the base set** and
3 base-set nodeids now passing. All 18 were individually re-run **in isolation**
(outside the noisy full-suite run) to determine whether they are caused by this
lane's diff:

- **17 in `tests/test_fleet_analytics.py`** — `ModuleNotFoundError: No module named
  'pandas'` in this worktree's venv. `pandas` is an existing optional dependency
  group (`--group analytics`) not synced into `lane-g-276-deploy-waiver`'s `.venv`;
  this lane added no dependency and does not touch `fleet_analytics` or anything it
  imports. Environment gap, not a code regression.
- **1 in `tests/test_stale_worktrees.py`**
  (`test_linked_worktrees_reader_excludes_the_primary`) — asserts about the live
  `git worktree list`, which differs when run from inside one of several
  concurrently-active worktrees (this lane, plus sibling lanes `g-611`, `g-614`,
  `g-621`, `g-626`, `g-628`, `g-630`, `g-632` all live during this run) rather than
  from the primary checkout. Unrelated to `deploy/carrier_precommit.py`,
  `.methodology.yaml`, or `enforcement_coverage.py`.

Neither class touches this lane's write-scope (`deploy/carrier_precommit.py`, the
`.methodology.yaml` schema note, `tests/test_carrier_precommit.py`) or anything it
imports. **Acceptance holds: the set of failures attributable to this lane's diff is
empty — a strict subset of the base set** (3 base-set nodeids fixed themselves;
0 added). The 18 environmental nodeids are recorded here rather than either
suppressed or miscounted as this lane's regressions.

Targeted re-run, isolated from full-suite contention (`tests/test_carrier_precommit.py
tests/test_deploy_tool.py tests/test_deploy_precommit.py tests/test_deploy_prune.py
tests/test_enforcement_coverage.py`): 125 passed, 1 failed
(`test_anchor_gate_probe_distinguishes_installed_from_absent` — in the committed
base set, a documented false positive, not touched by this lane).

## Substrate note

This run hit severe host memory pressure (≈2.2 GB free of 29 GB total) from several
concurrent full-suite runs across sibling worktrees. Multiple `pytest -n auto`
background attempts were killed before completion; the full-suite run that produced
the Delta A2 numbers above only completed once run through a persistent (no-timeout)
monitor rather than a time-boxed background shell. Recorded per the lane's LOCAL
substrate note (ruling R-G0-2) — this did not change the lane's write-scope or
behavior, only how long verification took.

## Design decisions made without escalation (reported, not asked — V-2 budget)

- **Reused `enforcement_coverage.py::validate_allowlist_entry` rather than a new
  date check.** Matches the existing precedent (`read_allowlist` is already
  reused) and the contract's own framing ("never a second parser"). `AL_NO_DATE`
  covers both "waiver MISSING" and "waiver INVALID (unparseable)" from the
  Done-contract's three seeded cases, since `_parse_date` collapses an absent field
  and an unparseable string to the same `None`.
- **`waivable_policy={}`** passed to `validate_allowlist_entry` — this carrier
  polices the time-box only, never a component's non-waivable status (that
  governance axis stays the Informant's).
- **Wall-clock `date.today()`, not a threaded `run_date` parameter** — consistent
  with the prior lane's own recorded reasoning; `contract.py`'s `Carrier` ABC is out
  of this lane's write-scope and carries no such parameter.

## Anomaly noted, not acted on

Mid-session, an unrelated instruction block addressed to a different lane
(`lane-g-628-essentials-debless`, referencing `--resume` worktree binding and
`conformance-hub.js` closures) was pasted into this conversation, then retracted
by the operator as a paste-target mistake. No action was taken on it; it is
recorded here only because the frozen contract's own Q10 discipline says a lane
reports what it observes rather than silently absorbing it.
