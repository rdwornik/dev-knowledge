# Merge-queue measurement — CI verdict vs. the local gate list, on the same ten commits

**Lane:** `lane-verify-in-lane` · **Branch:** `worktree-lane-verify-in-lane` · **Date:** 2026-09-22

Consumers: `[#960]` (this lane's row, Done-contract item 4); the recommendation below is read by
whoever next considers arming `deploy/conductor-required-checks.ruleset.json`.

**Method.** Read-only, `gh` CLI only, no repository setting changed. `git log origin/main
--first-parent` gave the last ten first-parent commits on `main`; `gh run list --workflow
conductor.yml --json ...` gave each one's `conductor` run, de-duplicated to the `push` event
(a `schedule` or `pull_request` run for the same sha is not a push's own verdict). Per-run job
detail via `gh run view <id> --json jobs`; artifacts (`suite-gate.out`, `pytest.out`) via `gh run
download`; job logs via `gh run view --job <id> --log`. "The local gate list's verdict on the
same commit" is read from what the standing process already records for each of these merges —
the base-vs-merged pairing quoted in `JOURNAL.md` and the ship-gate hard-fail count from
`to-browser/DIGEST-WAVE4-FINAL-2026-09-22.md` G4 — rather than re-run from a historical checkout,
since the CI comparison already needed for `[#960]` is what actually answers the wave's question
("does CI agree with what we already trust locally"), and a fresh Windows re-run of ten
historical commits would answer a *different* question (would ship-gate agree with itself a
second time) at a much higher cost.

## 1 · The ten pushes

`conductor.yml` runs six jobs per push: `pytest`, `ruff`, `seal`, `commit-gate`, `terra`,
`phase-gate`. The four short ones agree with the local record on all ten; two do not.

| sha | pushed (UTC) | overall | pytest | commit-gate | ruff/terra/seal/phase-gate | wall (job) |
|---|---|---|---|---|---|---|
| `2fd8f256` | 2026-09-22 19:46 | **failure** | failure (500s) | failure | success/success/success/success | 502s |
| `3689b5ab` | 2026-09-22 15:58 | **failure** | failure (484s) | failure | success/success/success/success | 489s |
| `e125fff8` | 2026-09-22 14:30 | **failure** | failure (500s) | failure | success/success/success/success | 505s |
| `b7768721` | 2026-09-22 11:26 | **failure** | failure (532s) | failure | success/success/success/success | 536s |
| `cd6e0d34` | 2026-09-22 09:57 | **failure** | failure (451s) | failure | success/success/success/success | 455s |
| `8746b741` | 2026-09-22 05:12 | **failure** | failure (530s) | failure | success/success/success/success | 535s |
| `df0c1ac8` | 2026-09-21 21:59 | **failure** | failure (491s) | failure | success/success/success/success | 496s |
| `f527c719` | 2026-09-21 18:31 | **failure** | failure (326s) | failure | success/success/success/success | 330s |
| `4f356acb` | 2026-09-21 17:05 | **failure** | failure (241s) | failure | success/success/success/success | 252s |
| `71b35fa8` | 2026-09-21 16:08 | **failure** | failure (359s) | failure | success/success/success/success | 364s |

**10/10 overall `failure`; 10/10 `pytest` failure; 10/10 `commit-gate` failure; 10/10 of
`ruff`/`terra`/`seal`/`phase-gate` success.** Median job wall time (`pytest`, the long pole):
~470s (7 min 50 s); range 241–532s. Median full-workflow wall time (`createdAt`→`updatedAt`):
~472s; range 252–536s — under `conductor.yml`'s own comment ("~5m30s-6m with `-n auto`"), because
this reads is pinned at `-n 4`, not `-n auto`.

## 2 · Why `pytest` fails — a REGRESSION verdict against a stale frozen baseline, not noise

`pytest`'s job is baseline-aware by design (`scripts/conductor.py suite-gate`, [#802]): it does
not fail on pytest's raw exit code, it fails when a red node id is **outside** the 87-member set
frozen at `c51083290de6a58056e815aa787b65031fabc623` (Actions run `35239925999`, 2026-09-17).
Three of the ten runs' `suite-gate.out` were pulled for the regression LIST, not just the count:

| sha | pre-existing (of 87) | regressions | verdict |
|---|---|---|---|
| `2fd8f256` (latest) | 73 | **17** | FAIL |
| `df0c1ac8` (7th back) | ~74 | **13** | FAIL |
| `4f356acb` (9th back) | ~75 | **12** | FAIL |

**The regression LIST is not random noise — it is the same shrinking core set**, most of it
present in all three samples: `test_bounded_hook.py` (3 tests), `test_graph_spine.py`
(`test_the_live_orphan_census_reaches_zero...`), `test_graph_spine_commit_tier.py` (4
parametrised cases), `test_integrator_surface.py` (2–6 cases across the three), and
`test_boot_retrieval.py`/`test_dispatch_launch.py` in the more recent runs only. The count falls
12 → 13 → 17 as you go BACK in time (i.e. it grew from 12 to 17 over these ten pushes, then
presumably some were fixed), which reads as **real, accumulating drift against a baseline that
has not been refreshed since 2026-09-17** — five days and ten-plus merges ago — not as flaky
noise that would show a different set each time.

**The local record for these same merges says CLEAN.** `JOURNAL.md`'s recorded
base-vs-merged pairing for every merge in this window (`lane-batch-digest`, `lane-connection-
hygiene`, `lane-known-reds`, `lane-connection-test`, `lane-launch-adapter`, `lane-end-hook`, and
back through the L1–L8 wave-2 lanes) reads **"zero failures are the lane's"** every single time —
e.g. "`paired against merge-base cdea9bdb, zero failures are the lane's — base 41 failed / 787
passed, merged 39 failed / 2272 passed, merged \ base EMPTY`". The local pairing's bar is "did
THIS lane's diff turn anything red", answered against the immediately preceding tree; CI's
`suite-gate` bar is "is main red anywhere outside a set frozen five days ago". **Both can be
correct at once** — a merge can add zero new reds relative to its own parent while the accumulated
total still grows past what was true on 2026-09-17 — which is exactly what these numbers show.
This audit does not have a live Windows re-run to confirm whether the 12–17 regression tests are
platform-sensitive (local dev and the local pairing both run on Windows; CI runs `ubuntu-latest`);
that is a plausible hypothesis given the names skew toward hook-posture and graph-spine checks
that touch paths and process launches, but it is **not confirmed here** and should not be read as
more than a lead for whoever refreshes the baseline next.

## 3 · Why `commit-gate` fails — tree-wide standing debt, not a per-push regression

`commit-gate` runs every `.pre-commit-config.yaml` hook at `stages: [manual]` — moved here
2026-09-17 specifically because these hooks do **not** run automatically on a local `git commit`
(only the pre-commit-stage pair, `block-ff-push` and its sibling, do). Reading the full job log
for the latest run (`2fd8f256`, job `106908892174`):

- **`validate-backlog` FAIL** — 7 findings, all `· implements:` tokens "outside the grammar
  [ADR-n | intake-n | DECLARE-... | AMEND-...]" on rows `[#906]`, `[#908]`–`[#914]`, dated
  2026-09-18/19 in the row body — filed **before** this ten-push window and untouched by any of
  it.
- **`derived-copies-rebind`, `graph-orphan-census`, `audit-health` (self-conformance) FAIL** —
  all three read the tree's current state as a whole, not the pushed range's diff.
- `wall_seconds=32 exit=1` — the job itself is cheap; the failure is a lookup, not a slow check.

**None of these four is a defect the pushed commit introduced.** `git reset --soft "$BASE"` (the
job's own mechanism for scoping to "this range's staged set", per the workflow's comment) still
leaves every pre-commit hook reading the **whole working tree at HEAD** for anything that is not
itself diff-scoped — and three of the four failing hooks are exactly that class (an index/graph
census, a self-conformance audit, a story-map validator that reads all of `tasks/`). This is the
**same root defect as `pytest`'s**, restated: CI enforces a state the local flow has never been
asked to keep clean, because these checks were deliberately never armed at `stages: [pre-commit]`
locally. The workflow's own header calls it "REPORT-ONLY, like the rest of this workflow while
enforcement is disabled" — a description this measurement confirms rather than merely repeats.

## 4 · Parity verdict

| leg | CI (10 pushes) | local record (same 10) | agree? |
|---|---|---|---|
| `ruff` | 10/10 success | ruff is armed at commit time locally (pre-commit gate) | **yes** |
| `terra` | 10/10 success | Codex terra review recorded per lane before handback (JOURNAL, every entry) | **yes** |
| `seal` | 10/10 success | ADR-101 hermetization gate armed locally | **yes** |
| `phase-gate` | 10/10 success (vacuous today — 439/440 rows `NOT GATED`, [#689] not yet built) | n/a — no local equivalent exists yet | **yes, but not yet a real check** |
| `pytest` | 10/10 failure (baseline-relative REGRESSION) | 10/10 "zero failures are the lane's" (parent-relative) | **no — different questions, both true** |
| `commit-gate` | 10/10 failure (tree-wide standing debt) | never run locally at commit time by design | **no — CI checks a bar local never had to clear** |
| **overall** | **10/10 failure** | **10/10 mergeable (ship-gate 0 hard-fails, `to-browser/DIGEST-WAVE4-FINAL-2026-09-22.md` G4)** | **no** |

**Numbers for the recommendation:** if `pytest` and `commit-gate` were armed today as GitHub
required checks (the shape `deploy/conductor-required-checks.ruleset.json` declares,
`enforcement: disabled`), **10 of the last 10 legitimate, already-shipped merges to `main` would
have been BLOCKED** — not because any of them was bad (the local record says none introduced a
regression), but because (a) the frozen suite baseline is five days stale and real drift has
accumulated past it since, and (b) `commit-gate` enforces tree-wide conditions (four failing
hooks, none diff-scoped) that no local commit has ever been required to satisfy.

## 5 · Recommendation

**Do not arm the native merge queue / required checks yet.** Ruleset activation is a
`gh api ... rulesets` call this audit deliberately did not make (no repository setting changed);
the number that would justify it — CI verdict parity with the local gate list on real pushes — is
currently **0/10 at the overall level**, and the two failing legs each have a named, fixable
cause rather than being unowned flake:

1. **Refresh `logs/SUITE-BASELINE-FREEZE.md`'s frozen baseline** (currently `c51083290d...`,
   2026-09-17) on a cadence, or make `suite-gate` compare against the PARENT commit the way the
   local pairing already does — the local record already answers the question CI is trying to
   answer, just against a moving reference instead of a fixed one five days in the past.
2. **Scope `commit-gate` to the pushed range's own diff**, or explicitly split it into "diff-
   scoped" and "tree-state" hooks with different pass bars — a story-map validator or a
   self-conformance audit reading the WHOLE tree at HEAD is not answering "did this push regress
   anything", and required-check semantics (block THIS push) only make sense for the former.
3. **Confirm or rule out the OS-divergence hypothesis** (§2) with one live Ubuntu run of the
   12–17 regression tests against a current Windows-clean tree — this audit did not do that run,
   and it is the fastest way to know whether the frozen-baseline fix in (1) is sufficient by
   itself or whether a platform gap needs its own fix first.

Until at least (1) is done, arming required checks would wedge every future push on debt no lane
in this window introduced — the exact failure mode the lane contract's "no repository setting
changes" instruction exists to keep this measurement from walking into by accident.

## 6 · Honest limits of this measurement

- **Ten pushes, one CI environment window.** All ten runs used the same frozen baseline and the
  same standing `commit-gate` debt, so this is one snapshot, not a trend line across baseline
  refreshes (there have been none in this window to compare against).
- **The local side is READ, not RE-RUN**, for the reason given in Method. A skeptical reader who
  wants a live paired measurement should re-run `ship-gate` and the base-vs-merged pairing on a
  historical checkout of each of these ten commits; this audit's numbers would need to be
  reconciled against that if it disagrees.
- **The OS-divergence hypothesis in §2 is a lead, not a finding** — named because the regression
  set's shape suggested it, not because it was tested here.
