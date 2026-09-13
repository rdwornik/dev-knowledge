# LANE `lane-x-689-conductor-e-proof` — end-of-lane packet

> **Prove conductor E's runner leg**: run the full suite on GitHub Actions at a fixed
> worker count, twice on ONE pinned commit, and report identical counts and comparable
> wall time — or the runner's limit and the smallest completing shape, as a measured
> finding.
>
> Contract: `H:\My Drive\CLAUDE PROMPT DIR\LANE-x-689-conductor-e-proof.md`
> Row: `[#689]` (Conductor E — build already landed by a prior lane; this lane adds
> measured evidence that the runner leg actually holds under repetition, no code touched).
> Branch: `worktree-lane-x-689-conductor-e-proof`. Commit-and-STOP; no merge, no push to
> `main`.

## 1. What changed

**Nothing in the tree.** This is a measurement-only lane: `.github/workflows/conductor.yml`
was read and its current shape confirmed (step 1) but never edited — the worker count the
`pytest` job runs at (`-n auto`, from `[tool.pytest.ini_options] addopts` in
`pyproject.toml`) resolves to a number that turned out to be empirically fixed on
GitHub-hosted `ubuntu-latest` runners (see §2), so no workflow edit was needed to get a
comparable, stated worker count across two runs. Steps 1–3 therefore produced no diff to
commit; this packet is the lane's single commit.

## 2. Pinned facts, stated explicitly (contract clause 4)

| Fact | Value |
|---|---|
| Pinned commit SHA | `ec18875e61c07174df8a223b15825507b98d2069` (= `origin/main` tip at lane start) |
| Runner label | `ubuntu-latest` → concrete image `ubuntu-24.04`, image version `20260907.300.1` (identical in both runs) |
| Worker count | **4** — confirmed by `[gw0]`..`[gw3]` present and no `[gw4]`+ in either job log. Not hardcoded in the workflow (`addopts = "-n auto"` is what actually runs); fixed in practice because GitHub's standard `ubuntu-latest` runner provisions 4 vCPUs and `-n auto` binds to `os.cpu_count()`. Recorded here as the runner-under-test's actual invocation, not asserted from the workflow file alone. |
| Job timeout | 45 min (`conductor.yml` `pytest:` job) — not approached; both runs completed in ~3–4 min |

## 3. The two runs, side by side

```
run          trigger           run id        started (UTC)         job wall   pytest wall   collected  passed  failed  skipped  errored
A (prior)    push              34703058939   2026-09-12T15:42:55Z   3m29s      191.26s        6141       6068      55      18        0
B (this lane) workflow_dispatch 34726541930   2026-09-12T23:52:38Z   4m08s      230.45s        6141       6068      55      18        0
```

Both runs are against the SAME pinned SHA above. Run A already existed on `main`'s history
(a push-triggered run from the same tree that produced this SHA); run B is this lane's own
`gh workflow run conductor.yml --ref main` dispatch, fired after confirming A's SHA matched
`origin/main`'s tip and had not since moved. Using the pre-existing run as one of the two
data points, rather than firing two fresh dispatches, halves this lane's Actions-minute
spend for the same evidence — the SHA, workflow file and worker count are identical either
way.

Raw summary lines, `grep`'d directly from each run's `pytest` job log:

```
run A: 55 failed, 6068 passed, 18 skipped in 191.26s (0:03:11)
run B: 55 failed, 6068 passed, 18 skipped in 230.45s (0:03:50)
```

No `error` token appears in either job's short test summary section — collection errors:
0 in both.

## 4. Verdict (contract clause 2)

**Counts are IDENTICAL.** 55 failed / 6068 passed / 18 skipped / 0 errored / 6141
collected, in both runs, at the same SHA and the same worker count. Nothing was re-run to
force agreement — this is the first and only pair taken.

**Wall time is COMPARABLE, not identical.** Job wall 3m29s vs 4m08s (pytest-internal
191.26s vs 230.45s), a ~20% spread. Cause named rather than left unexamined: both runs used
the identical runner image (`ubuntu-24.04`, `20260907.300.1`) and identical worker count
(4), so the spread is ordinary GitHub-hosted-runner scheduling noise (shared-host
contention varies run to run), not a code or configuration difference between the two
invocations. This matches the workflow file's own comment recording a similar-order local
spread ("~5m30s–6m with `-n auto`" on the workstation, measured previously). No further
action follows from this spread — the contract asks that a difference be *named*, and a
common, bounded noise source is the honest name for a 39-second gap on a ~3.5-minute job.

**The runner was never stressed.** Both runs finished in under 4m10s against a 45-minute
job timeout — nowhere near the 6-hour Actions job ceiling, and 2 runs × ~4 min is
negligible against the Pro-tier 3,000-minutes/month budget (`[#689]`'s row already measured
1,192 minutes used against that quota for the whole of September). Step 3 of the contract
(bisect down to a completing shape) does not apply: nothing failed to hold.

## 5. Findings and deviations

1. **The lane's declared footprint stayed empty.** The contract anticipated recording
   `conductor.yml`'s shape "before changing anything" (step 1), which reads as though a
   change might follow. None was needed: the existing `-n auto` default already resolves to
   a single, confirmable worker count on GitHub's standard runner, so pinning a worker
   count explicitly in the workflow would have added a line with no measurement benefit —
   the number is reported here as measured fact instead. If a future lane needs the worker
   count to be self-documenting *in the workflow file itself* (rather than derived from a
   job log after the fact), that is a proposed diff, not a finding against this one.
2. **One of the two runs was not fired by this lane.** Run A (`34703058939`) is a
   push-triggered run that already existed on `main`'s history at the pinned SHA before
   this lane started. It was verified — not assumed — to be at the exact pinned SHA
   (`headSha` checked via `gh run list --json headSha`) before being counted as a data
   point. Using it is a deliberate minute-budget choice (§3), reported rather than hidden.
3. **No JOURNAL entry, no index regeneration** — both reserved for the integrator per the
   contract's "What NOT to do" and `STANDING_RULINGS.md` P-1 / Q1. No pre-commit hook was
   bypassed on this commit; nothing this lane touched is a generated surface.

## 6. Verification

- `git status` clean before this commit except the one new file below.
- No test suite run locally for this lane — the lane's entire subject IS the suite's
  behavior on the *hosted* runner, and a local `pytest` run would answer a different
  question (STANDING_RULINGS D4: a bare or local invocation is not the runner under test).
  `ruff check` over this file: not applicable (Markdown only; no Python touched).
- This lane's only artifact is this file: `docs/audits/2026-09-13-technical-lane-x-689-conductor-e-proof.md`.
