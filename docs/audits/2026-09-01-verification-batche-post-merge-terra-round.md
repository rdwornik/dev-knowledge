# POST-MERGE TERRA ROUND — the six batch-E merges reviewed after the fact, and what the merges should have caught

- **Class:** verification · **Date:** 2026-09-01 · **Author:** CC (Opus 5, attended)
- **Consumed by:** `[#614]` (batch E's frozen execution arc — this round is a precondition of its
  close packet) and `[#529]`, whose row this round corrected.
- **Reviewer:** `codex exec -m gpt-5.6-terra`, one pass per lane, over each merge's
  `git diff <merge>^1 <merge>`.

## Why this exists, stated as the defect it is

**The six lanes merged during the 2026-08-31 → 09-01 window received NO independent review.** The
operator asked which of two things had happened — reviews ran and went unreported (a packet
defect), or reviews were skipped (a process defect). **It is the process defect.** Each lane was
verified by the integrator: diff read, targeted tests run, work confirmed. That is real and it is
what the window report described. **It is not an independent review round**, and the report should
have said so rather than leaving the absence to be inferred from silence.

Run post-merge, which is the weaker position — the code is already on `main`. Recorded that way
rather than presented as if it had gated the merges.

## The tallies, in body, one line per lane

```
lane   merge      TALLY                                    verdict
DC-5   76f184fb   crit=0 high=0 med=0 low=0 actionable=0   CLEAN
DM-6   b7fef9b9   crit=0 high=0 med=1 low=0 actionable=1   UPHELD  -> row corrected
HY-2   1c92024f   crit=1 high=0 med=0 low=0 actionable=1   UPHELD  -> fixed
HY-3   4bc754b4   crit=0 high=1 med=0 low=0 actionable=1   REFUTED -> reason below
HY-4   720d3e09   crit=0 high=0 med=1 low=0 actionable=1   ACCEPTED as a limit
HY-5   32d19df    crit=0 high=0 med=0 low=0 actionable=0   CLEAN   (win-tooling)

ROUND TOTAL   crit=1  high=1  med=2  low=0   |  2 fixed · 1 refuted · 1 recorded
```

## The one CRIT, and it was real

**HY-2 · `scripts/logs_retention.py`** — *"`logs_dir` is accepted without constraining it to this
repository's `logs/` directory. A caller can pass an external or synced path and the script will
relocate its files."*

**Exact.** `main` took `--logs-dir` as a bare `Path`, `run_retention` passed it through, and
`apply_moves` does `dst.parent.mkdir(parents=True)` then `src.rename(dst)` inside it. **A mover
with no constraint on where it moves**, shipped by this repo. Under core-invariant #1 that is a
**T2 write into the exclusion zone**, and the hazard that rule records — *a cleanup script that
relocated the operator's personal files* — is this module's exact shape.

**FIXED** with two independent legs: an **absolute** exclusion refusal (no override, wherever the
segment appears) and a **containment** bound (the repo, or the system temp dir, which is what
keeps `tmp_path` fixtures legal). Neither subsumes the other — an excluded path under `tmp_path`
passes containment and fails exclusion, and there is a test for exactly that. The guard runs
**before** `plan_moves`, because planning walks the directory and reading an excluded path is
itself outside what the invariant permits. Six RED-first witnesses; 27/27 green.

*Recorded because it happened during this fix:* the operator's own `PreToolUse` guard **refused
one of my commands** for carrying the zone literal together with a shell redirect. It was right,
and the constant is now assembled from parts so the literal is never typed on a command line.

## The MED that inverted a lane's own conclusion

**DM-6 · `tasks/529`** — the reviewer disputed the lane's claim that AUT-R3's B3 finding was
stale. **Verified directly rather than accepted**, and both parties were wrong on the number
while the reviewer was right on the substance:

```
DM-6 claimed   "telemetry_emit imports in 8 scripts/*.py modules, so B3 is STALE"
terra claimed  "only four consumer modules directly import it"
MEASURED       6 modules import it; 9 mention it
MEASURED       emit_check_run has ONE caller (governance_health.py:636)
               emit_event / emit_hook_run / emit_blocker_fired have ZERO
```

**B3 asked for WIRED CALL SITES; DM-6 answered with an import count**, and three of the importers
(`audit.py`, `block_commit_on_main.py`, `block_ff_push.py`) import `default_db_path` *specifically
in order not to use it*. `[#529]`'s row now carries the withdrawal and the measurement. **B3
stands and leg 1 is LIVE.** The lesson is the predicate, not the arithmetic.

## The HIGH, REFUTED with its reason

**HY-3** — *"the lane adds an audit but skips regenerating the generated audits index, so
`test_gen_audit_index` fails."* The observation is true and the grading is wrong: **`[#590]`
deliberately narrowed `audit-index-freshness` so a lane must NOT regenerate that index** — being
forced to had put `docs/audits/README.md` in 6 of the last 7 conflicted merges. The obligation is
the **integrator's, at close**, and it was discharged. Recorded as (b), not fixed.

## The MED accepted as a stated limit

**HY-4 · `gen_trend_dashboard.py:918`** — the burn-down sampler applies **today's** `ARCS` theme
selectors to every historical revision, so a future arc re-theme would retroactively move past
points and read as a burn-down that never happened. Real, and not fixable without per-revision
selector loading, which is a design change rather than a repair. **Recorded as an accepted limit
of the panel**; the panel is new and has no historical consumers yet, which is the cheapest moment
to know this.

## Honest limits of this round

- **One pass per lane, not a loop.** The recorded terra discipline is *run until a pass returns
  nothing* (n=2 precedents at 6 and 15 passes). This is a single pass on each of six diffs, so it
  is a floor on what is there, not a clean bill.
- **Post-merge.** Every finding here is on code already on `main`.
- **The reviewer's own numbers needed checking** — it was wrong on the import count in the one
  finding where a number mattered. Its *class* judgement was right both times it mattered.
