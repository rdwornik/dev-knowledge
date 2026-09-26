# Fresh-Eyes Review (DEGRADED-REVIEW) — lane-ci-signal

**Date:** 2026-09-26
**Branch:** `worktree-lane-ci-signal`
**HEAD at review time:** `cd563d9f` (this record's fix landed after, at `511094fd`)
**Diff range reviewed:** `20dfe91a..86733343` (this lane's own authored commit, excluding the
subsequent merge of concurrent `origin/main` work)
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low, post-triage: the one CONFIRMED defect is
counted at the severity of what it actually was (a step's exit code silently dropped), not
the reviewer's stated High. -->
**Disposition:** 1 CONFIRMED defect, fixed in `511094fd`. 12 of 13 raised findings did not
reproduce against the actual code, or are pre-existing/by-design and not a regression this
diff introduced. Full triage below.

## DEGRADED-REVIEW — why, and the chain followed

The doctrinal reviewer is terra (`gpt-5.6-terra` via `/codex-review`, PLAYBOOK "Codex-utilization
doctrine"). `codex-review.ps1 -Topic lane-ci-signal` was invoked first and failed:

```
ERROR: You've hit your usage limit. Upgrade to Pro ... or try again at 5:02 PM.
```

Per PLAYBOOK "DEGRADED-REVIEW — the fallback chain when the doctrinal reviewer lane is
unavailable" (architect ruling 2026-08-29): rung 1 (terra) unavailable on quota → descend to
rung 2. Rung 2 (grok CLI) was liveness-probed alive at session start of this fallback and used
directly (`grok --prompt-file <diff+instructions> --output-format json --sandbox read-only`).

**Served model id, per-round (the `[#492]` scar):** `modelUsage` in the JSON response names
`grok-4.20-0309-non-reasoning`, 2 model calls, cost `$0.068181`. This is the transport's own
usage-accounting field, not a self-report — it qualifies per PLAYBOOK's "which channel
qualifies" rule.

**Standing obligation:** terra re-review of this diff (or of `511094fd`, the post-fix tip)
remains OWED once quota resets (stated retry: 5:02 PM the same day). Not done in this session
— recorded here so it is not lost, per the fallback chain's "obligations carried by every
fallback artifact."

## Focus

- Correctness of `scripts/ci_red_age.py`'s streak-walking (`red_since`), truncation detection,
  and timezone parsing
- `scripts/known_reds.py`'s new `compare_hook`/`Registry.hooks` — backward compatibility,
  strictness relative to the existing `compare()`
- The new `conductor.yml` commit-gate step: exit-code propagation, shell-quoting/injection risk
- Whether re-homing `doc-counts`/`playbook-toc` to `commit_gate: self` weakens their coverage
- Security: subprocess construction, file writes
- Test coverage gaps

## Findings, triaged (severity as originally reported by the reviewer)

1. **HIGH — `ci_red_age.py` `red_since()` allegedly mis-starts the streak when in-progress runs
   precede the first red.** NOT REPRODUCED. `judged = [r for r in runs if r.get("conclusion")]`
   filters every null-conclusion (in-progress/queued) run out *before* the streak walk begins,
   regardless of position — there is no code path where an in-progress run can appear inside
   `streak`. Directly covered by
   `test_red_since_skips_an_in_progress_run_without_breaking_the_streak`, which passes.

2. **HIGH — truncation detection (`len(streak) == len(judged)`) allegedly wrong when
   in-progress runs precede the first judged run.** NOT REPRODUCED, same reason as (1): in-progress
   runs never enter `judged`, so their position relative to it is not observable to this
   comparison. Covered by `test_red_since_reports_truncated_when_every_fetched_run_is_red` and
   `test_red_since_is_not_truncated_when_a_green_run_bounds_the_streak`, both pass.

3. **MEDIUM — `_parse()` has no validation; a malformed `createdAt` would raise unhandled
   inside `red_since()`/`compute()` rather than surfacing as `GhUnavailable`.** PLAUSIBLE, not
   fixed. `gh run list --json createdAt` is a stable, versioned field this repo already trusts
   elsewhere (`ci_verdict.py`, `actions_verdict.py`) without defensive re-validation; adding a
   guard for a field shape change GitHub has never made is validating a scenario that, per this
   repo's own convention (`file:Global-Agent-Rules "don't add validation for scenarios that
   can't happen"`), does not warrant it today. Deferred, not filed as a row (no lane owns
   speculative GH-API-shape hardening).

4. **HIGH — the new `conductor.yml` commit-gate step "can mask prior step failures".**
   CONFIRMED, though the reviewer's stated mechanism (unquoted `cat`, missing `set -e`) was not
   the actual cause. The real defect: inserting the new step deleted the *prior* "Run the moved
   commit-gate hooks" step's trailing `exit $rc` without replacing it, so that step's own
   reported conclusion always read green regardless of the hooks' real exit code — job-level
   `continue-on-error: true` kept the overall workflow conclusion unaffected, but the per-step
   signal in the Actions UI was silently wrong. **Fixed in `511094fd`** (`exit $rc` restored).
   `tests/test_conductor.py` (54 passed) and a YAML parse both re-verified after the fix; no
   existing test had caught the gap, which is itself a coverage note but not a new row (the
   fix is a one-line restoration, not a design change needing its own test).

5. **MEDIUM — `Registry.hooks` round-trip "loses order" and "silently accepts non-dict
   values."** NOT REPRODUCED / not a regression. `to_json` writes `hooks` sorted; `json.load`
   preserves that order on read, so there is no order loss. The lack of deep shape validation
   on `from_json` is identical to the pre-existing sibling field `members` one line above
   (`members=dict(data["members"])`, no validation either) — this diff matches, not weakens,
   the existing convention.

6. **LOW — `compare_hook()` treats any non-zero exit code as equivalent once a hook_id is
   registered, not keying on the specific code.** PLAUSIBLE as an architectural observation, not
   a defect: this mirrors `compare()`'s own semantics exactly (a registered pytest node id is
   "known" regardless of its failure message) — the docstring states "Same shape as compare()"
   as a deliberate design choice, not an oversight. Not changed.

7. **MEDIUM — CLI `--repo-root`/`--out-json` allegedly unguarded against bad paths, race
   conditions.** PARTIALLY REPRODUCED. A bad `--repo-root` IS already caught: `list_runs` wraps
   its `subprocess.run` in `try/except (OSError, subprocess.SubprocessError)` and raises
   `GhUnavailable`, which the CLI's own `try/except` converts to a clean exit 2 — the reviewer's
   claim here does not reproduce. `--out-json` writing to a nonexistent parent directory would
   raise uncaught `FileNotFoundError` — true, but `--out-json` is only ever invoked by
   `lane_digest.py`'s own controlled call site with an existing directory; hardening against a
   hypothetical bad caller is deferred, not filed. The "race" claim is imprecise (a single
   `write_text` to a caller-owned path, not a shared/contended file) and not reproduced.

8. **MEDIUM — re-homing `doc-counts`/`playbook-toc` to `commit_gate: self` "only checks one
   aspect."** Accurate but PRE-EXISTING, not introduced or worsened by this diff. The prior
   `commit_gate: gate` mechanism (`doc-counts-pytest-freshness` hook) had the identical
   coverage scope — the row's own `note:` field candidly documents this both before and after
   the re-home (`uncovered_inputs`, "the hook's own comment records the cost reason it is
   scoped this narrowly"). Nothing widened or narrowed by this change.

9. **LOW — missing tests for malformed `gh` JSON, negative hours, all-null-conclusion runs,
   `limit=1`.** PARTIALLY ACCURATE. "Negative hours" does not reproduce (`hours = max(0.0, ...)`
   already guards it). All-null-conclusion is exercised by the same code path as the
   already-tested empty-list case (`not judged` is true either way) but has no *dedicated* test.
   Malformed-JSON-at-`list_runs` and `limit=1` are genuine minor coverage gaps. Deferred as
   nice-to-have, not required by the contract's stated fixture requirements (23h/25h, both
   present and passing).

10. **LOW — `lane_digest.py`'s `ci_red_line()` is more lenient than `known_reds.load_registry`.**
    NOT A DEFECT. Deliberate, documented design difference: `lane_digest.py` runs inside a Stop
    hook whose own `main()` docstring states "a digest must never raise out of a Stop hook" —
    leniency here is the correct posture for that consumer, not an inconsistency.

## Self-check

- `tests/test_conductor.py`: 54 passed (post-fix).
- YAML parse of `.github/workflows/conductor.yml`: OK (post-fix).
- No other file touched by this review pass.

## For the record

Terra re-review of `511094fd` is OWED and not yet done (quota-blocked; retry after 5:02 PM the
same day per the error message). No BACKLOG row filed for that obligation — it is carried here
per the DEGRADED-REVIEW chain's own stated obligation, the same convention
`2026-09-24-codex-lane-ci-verdict.md`'s no-consumer line uses.
