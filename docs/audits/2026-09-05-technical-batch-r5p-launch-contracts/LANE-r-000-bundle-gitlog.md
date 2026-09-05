# LANE lane-r-000-bundle-gitlog — ONE git log for all handoff bundles, not one per directory

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

**Batch R5P, lane 2 of 3.** Hotfix, P1. No BACKLOG row — `000` is the no-row id.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-r-000-bundle-gitlog LANE-r-000-bundle-gitlog.md -Effort high
```

**Model is the repo default `opus`, and that is forced rather than chosen:** the contract
validator's dispatch-line regex admits `-Effort` but NOT `-Model`, so a line carrying an

## Worktree pairing
explicit model FAILS `gen_lane_contract.py check`. The table above therefore states the
default the launch will actually use, so contract and launch cannot disagree.

slug `lane-r-000-bundle-gitlog` -> branch `worktree-lane-r-000-bundle-gitlog` -> contract `LANE-r-000-bundle-gitlog.md`

## Intent

`_select_active_bundle` in `scripts/audit.py` picks the ACTIVE handoff bundle by GIT ADD
DATE, and it spawns **one `git log` per candidate directory**. Replace that with **ONE
`git log` covering all bundle directories**, parsed into the same per-directory add-dates.

**The locator, resolved rather than quoted:** the function is
`scripts/audit.py::_select_active_bundle` (defined just below the `_git_location_env`
assignments; the dispatcher's brief cited `audit.py:2345`, which lands in that block —
line numbers drift, so navigate by the symbol, not the number).

**Measured A/B this is drawn from:** 118 spawns / 46.4 s -> 1 spawn / 0.35 s. That is the
dispatcher's number, not yours — **re-measure and report your own**.

## Done-contract (immutable)

1. `_select_active_bundle` performs **ONE** `git log` invocation regardless of candidate
   count. Prove the spawn count, do not assert it.
2. **Bundle selection is IDENTICAL to the per-directory method on the live tree.** A
   **seeded test compares BOTH methods** and asserts the same bundle, and the same `kind`
   ("sole" / "fresh" / "add-date" / "no-git" / "ambiguous" / "degraded").
3. **The "ambiguous" and "fresh" semantics survive verbatim.** A bundle with no add-commit
   (untracked OR staged) still outranks every tracked one; two fresh candidates still
   return `bundle=None` rather than a silent pick. That silent-pick refusal is the whole
   reason the selector exists — a batched `git log` must not quietly reintroduce it.
4. `audit.py health` wall-clock **before and after, both printed** in the packet.
5. `pytest` green on the targeted tests for this diff.

## Frozen defaults — decided here so the lane does not spend a round-trip

- **The env scrub stays.** `_git_location_env` is applied to this runner today and must
  still be applied to the batched call. It is scrubbed by NAME, never a `startswith("GIT_")`
  strip. Do not "simplify" it.
- **Fall back, do not crash.** If the single `git log` cannot attribute a directory (path
  never added, rename, unborn HEAD), that directory takes the SAME outcome the per-dir
  method gives it today. A batching optimisation must not change a failure mode.
- **`git log` argument length.** If the batched invocation would exceed a safe argv length,
  chunk it — chunked is still O(chunks), not O(dirs), and the done-contract's "ONE
  invocation" is satisfied by "one per chunk, chunking only above a stated bound". Say so
  in the packet if you chunk.

## Decision budget

**V-2 — escalates on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is
decided per the frozen defaults above and **reported in the end packet**, never asked.

## Steps

1. Measure: `audit.py health` wall-clock BEFORE, and the live spawn count. **COMMIT** nothing;
   this is measurement.
2. RED first: the both-methods-agree seeded test, plus the fresh/ambiguous pins. Watch fail.
   **COMMIT**
3. Batch the `git log`. Targeted tests green. **COMMIT**
4. Measure AFTER; final artifact (before/after wall-clock, spawn counts, what changed, open
   items), **COMMIT, then STOP.**

## What NOT to do

- **No other `audit.py` change.** This function only. Not a neighbouring check, not a
  drive-by import tidy, not the fleet-automation commit path (it sets `GIT_INDEX_FILE` on
  purpose via its own explicit `env=` dict and routing it through the scrub would silently
  break it).
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP.
- No JOURNAL entry — the integrator owns the anchor. Name your SHAs in the hand-back packet.
- No BACKLOG row, no index regeneration.

## Consumer declaration

no-consumer: a frozen batch-R5P lane contract for a P1 performance hotfix that discharges no BACKLOG row, no ADR and no register entry — its consumer is the batch manifest `docs/audits/2026-09-05-technical-batch-r5p-manifest.md`, and this lane files no row by contract.
