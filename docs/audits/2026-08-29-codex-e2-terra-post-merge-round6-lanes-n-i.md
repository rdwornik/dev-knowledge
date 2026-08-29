# E2 — terra POST-MERGE round 6 over wave-2 lanes N and I

**The night mission's one MEASUREMENT-OWED, discharged.** The wave-2 close packet recorded this
as owed with the reason: *"`codex exec` returned 'You've hit your usage limit … try again at
4:20 PM'. The provider limit is the recorded outcome your adjudication pre-authorised, not a
skipped step."* The window opened; this is the round.

| Field | Value |
|---|---|
| Run | 2026-08-29, after the 16:20 quota window opened (terra probed `QUOTA_OK` at 17:22 CEDT) |
| Model | `gpt-5.6-terra` — the doctrinal lane, NOT a degraded fallback |
| Base | `main` @ `902b621b` |
| Scope | lane N (`scripts/gen_trend_dashboard.py`, its tests) + lane I (`scripts/funnel_lifecycle.py`, its tests, the `check_funnel_lifecycle` additions in `scripts/audit.py`) |
| Round type | **POST-MERGE.** Both lanes carried terra IN-LANE before merging; what was owed is the round that sees both lanes' code together on `main`, which no in-lane pass could. |

## TALLY

```
TALLY Critical=0 High=3 Medium=1 Low=0
```

**Delta note, stated honestly:** there is no prior POST-MERGE tally to difference against — the
in-lane rounds reviewed each lane alone, and this is the first round to see them together. This
tally is therefore the post-merge BASELINE, not a delta. Recording that rather than manufacturing
a comparison against non-comparable rounds.

**All three Highs are honest-degrade defects** — the class the prompt ranked third but which
dominates the result: in each, a failure renders a plausible number instead of reporting itself.

## FINDINGS, verbatim

```
Critical: none.

High | scripts/audit.py:4202 | `check_funnel_lifecycle` remains SHIP-tier although the two terminal intakes are now archived and leg a1 measures zero—the documented promotion condition. | Lifecycle failures are deferred from every commit gate despite now being repairable by the landing change; tests at `tests/test_funnel_lifecycle.py:624` lock in the stale tier.

High | scripts/gen_trend_dashboard.py:403 | Git collector failures are collapsed into missing samples (`_git` returns `""`), and the remaining samples can still render an apparently valid trend. | A failed `git grep` can silently omit a date rather than report an unavailable measurement, producing a plausible but incomplete direction.

High | scripts/gen_trend_dashboard.py:184 | Unknown task statuses are silently excluded from every band. | A new or malformed status lowers displayed row counts while the dashboard still presents a real-looking trend; the paired test explicitly enshrines this at `tests/test_trend_dashboard.py:127`.

Medium | scripts/funnel_lifecycle.py:353 | Multiple conflicting `READY threshold` declarations are resolved by whichever protocol file sorts first, with no ambiguity finding. | This creates two owners for one lifecycle metric and can silently enforce an arbitrary threshold.

Low: none.

Checked interaction boundary: the dashboard’s `funnel_orphans` series intentionally reads the audit-disposition baseline, while FM-2 measures lifecycle exit; they are distinct metrics, not duplicated derivations.

TALLY Critical=0 High=3 Medium=1 Low=0
```

## What it checked and found SOUND (negative results are first-class)

The interaction boundary the post-merge round exists to test: the dashboard's `funnel_orphans`
series reads the audit-disposition baseline while FM-2 measures lifecycle exit. Terra confirms
these are **distinct metrics, not duplicated derivations** — the two-owners-for-one-metric failure
did NOT occur across the lane boundary.

## Disposition

Not fixed here. Each finding needs its own triage under ADR-111, and one of them
(`check_funnel_lifecycle` still SHIP-tier though its documented promotion condition is now met)
is a tier ruling rather than a code repair.
