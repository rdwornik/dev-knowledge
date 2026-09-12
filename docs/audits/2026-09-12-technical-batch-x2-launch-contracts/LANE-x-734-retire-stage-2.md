# LANE lane-x-734-retire-stage-2 — second attempt at the retire stage, rewritten from the ten-target verdict record its first run produced

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-734-retire-stage-2 LANE-x-734-retire-stage-2.md -Effort high -Model opus
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #734 · lane-x-734-retire-stage-2]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`opus` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-734-retire-stage-2` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-x-734-retire-stage-2` -> branch `worktree-lane-x-734-retire-stage-2` -> contract `LANE-x-734-retire-stage-2.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## This contract is rewritten FROM the first run's own verdict record

The source is `docs/audits/2026-09-11-technical-lane-x-734-retire-evidence.md`, on `main` at
`f1711e3d` (resolved: the record is in that tree; `f1711e3d` is an ancestor of `main`). The first
run produced **verdicts and zero landed deletions** — commit `1a3ff040` landed the record
*docs-only*, and **the code stayed refused**. So this lane is not a continuation of a partial
deletion; it re-executes against verdicts that are already made, which is why its footprint is
declared per-target below rather than discovered.

**Read the record before Step 1.** Every per-target disposition below is a compression of it, and
a compression is not the evidence.

## Done-contract (immutable)

1. **The six SAFE targets are deleted, with all four coupled surfaces per target** (module +
   dedicated test + `graph_queries.py` `Disposition` entry + `tests/test_graph_spine.py`
   `CENSUS_SCRIPT_ORPHANS` entry):
   `scripts/boundary_headers.py`, `scripts/boundary_report.py` (coupled pair — move together),
   `scripts/cloud_provisioning.py`, `scripts/seed_runbook.py`,
   `scripts/validate_onboarding_rulings.py`, `scripts/probe_child_backlogs.py`.
   The oracle verdict backing them is **SAFE — "no surviving referrers; every removed symbol
   resolved clean"**, over the eight-module set evaluated at once.

2. **`scripts/desired_state_loader.py` + `scripts/desired_state_report.py` are deleted, and this
   lane's GO footprint is EXTENDED to cover the one edit that blocked them.** The first run
   proved both SAFE, deleted them, then **reversed the deletion** because
   `test_the_live_tree_carries_no_dangling_process_reference` went RED: `ARCHITECTURE.md:503-504`
   still names both files in prose, and fixing it was outside that lane's footprint.
   **`ARCHITECTURE.md:503-504` is IN footprint here.** Resolve the two line numbers before
   editing — they are from the first run and the file has moved since.

3. **The `/override` tombstone lands: a `status: removed` entry in `deploy/manifest-v1.5.0.yaml`,
   carrying the `removed_in:` that C6 requires.** See the section below — **the block the first
   run reported is not real**, and the "release_lint change" this needs is a documentation
   retraction, not a mechanism unlock.

4. **`deploy/lived_sandbox/` is re-examined FILE BY FILE, not as one target line.** `arc.py` is
   **KEPT** — open row `[#267]` names it directly as `ARC_PROMPT`, a confirmed live reader. The
   other seven return FPG-1 `REFUSED` (nothing explains them), which is **inconclusive, not a
   clean no-reader pass**; an inconclusive target is **KEPT with that reason recorded**. The
   deliverable here is the per-file disposition the first run was not scoped to make — not
   necessarily a deletion.

5. **`config/requirements-dev.txt` stays KEPT.** ADR-106 §5 names a standing **no-delete
   invariant** requiring its own explicit operator ask, and **that ask has still not been
   given** — the operator's 2026-09-12 instruction re-authorised this lane and did not issue it.
   A bundled batch GO does not satisfy a standing invariant's demand for a dedicated ask. Do not
   re-litigate this in-lane; it is settled for this run.

6. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## The tombstone was never blocked — the block was three stale prose surfaces

The first run KEPT the `/override` tombstone on this reasoning, quoted from its own record:

> `deploy/release_lint.py`'s own module docstring states the P1 lifecycle boundary explicitly:
> *"only `status: active` is legal this release — `deprecated`/`removed` (tombstones) unlock in
> P2, gated on operator decision D3, so a tombstone landing early fails loud here instead of
> silently meaning nothing"* (C6).

**That docstring is stale, and the code it describes disagrees with it.** Resolved at `9136f133`:

- `deploy/release_lint.py` line 101: `ALLOWED_STATUSES = {"active", "removed"}` — `removed` is
  **admitted**.
- The comment immediately above it already says so: *"P2 (D3): 2-state lifecycle — active |
  removed (no `deprecated` tier)."*
- It was unlocked by `1fbdf6f3` *"feat(deploy): release_lint C6 unlocks tombstones
  (status:removed) [#244]"*, and **`1fbdf6f3` is an ancestor of `f1711e3d`** — so tombstones were
  already legal **when the first run decided they were not**.
- The manifest already carries the n=1 precedent: `ruff-gate` is `status: removed`, and D3 is
  recorded as decided in the manifest's own header.

So the change this lane makes to the release surface is **a retraction of three stale claims**,
not an unlock:

1. `deploy/release_lint.py` module docstring (~L14-17) — the "only `status: active` is legal this
   release" paragraph.
2. `deploy/manifest-v1.5.0.yaml` (~L303) — *"this release ships no `status: removed` tombstone
   (release_lint C6; they unlock in P2 on operator decision D3)"*.
3. The `override-command` comment block written at `5e17ecd7`, which records the same false
   constraint as the reason `/override` was removed without a tombstone.

**This is the finding, and it is worth more than the tombstone.** A lane consulted prose, the
prose had been outgrown by the code, and a correct disposition was reversed on it — the same
absent-discriminator class as the two rows filed alongside this batch. Record it as such in the
end packet; do not bury it as a chore.

## Preconditions — two, both learned the expensive way by the first run

- **`npm install` before the oracle runs.** `safe_remove.py` drives the pyright langserver;
  `node_modules/` is gitignored per-checkout, so a fresh worktree starts without it and the
  oracle returns `UNVERIFIABLE` with every symbol `oracle-unavailable`. `package.json` exists
  solely to pin `pyright@1.1.410` for this oracle and `package-lock.json` is committed, so this
  restores a **declared, pinned, checked-in** dependency — the same class of act as
  `uv sync --locked`, not a new dependency. `node_modules/` stays gitignored and out of the
  commits.
- **Use the oracle's DEFAULT per-symbol timeout. Do not pass `--timeout 300`.** It is a
  **per-QUERY** timeout, not a total budget; the first run set it, produced zero output for
  ~20 minutes, and was killed short of a ~9-hour worst case.

**An inconclusive tool result is not a pass.** A silent or `UNVERIFIABLE` verdict means **KEEP,
with the reason recorded** — carried from the first run's GO footprint clause and still binding.

## Carried rows and clauses (verbatim — AX12-1)

### `AX24-1` — verbatim (this lane is LAST in the order)

> **AX24-1 · No new X2 lane until the finished work is banked.** Order: merge x-691 (routing
> Half A) → close the six witnessed rows → the fail-open fix (AX24-2) → `[#675]` merge cost →
> X-DEL second attempt. Everything else in wave 2 waits.

### `AX23-3` clause 3 — verbatim (this lane's commissioning text)

> (3) X-DEL second attempt, contract rewritten from the refused lane's own verdict record (the
> only copy is on `worktree-lane-x-734-retire-stage` — merge or preserve it before teardown),
> including the `release_lint.py` change that lets a tombstone land;

**Status of its parenthesis: DISCHARGED.** The verdict record is no longer single-copy — it is on
`main` at `f1711e3d` and the branch is gone. Nothing was lost to the teardown.

### `AX23-5` — verbatim (the metric this lane is measured on)

> **AX23-5 · Recorded:** wave 1 delivered five mechanisms and zero subtraction; the window stands
> at +47 rows filed, 4 closed. The next wave is measured on bytes removed, rows closed and merge
> minutes — not on rows filed.

This lane is the batch's **subtraction** leg. Wave 1 scored zero on it.

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

**Already decided, so NOT escalation classes here** — each was a class (b) escalation on the
first run and is answered in this contract: `ARCHITECTURE.md` is in footprint (clause 2); the
tombstone is not blocked (the section above); `config/requirements-dev.txt` stays KEPT
(clause 5). Re-escalating a settled one spends the budget twice.

## Steps

1. Read the verdict record end to end. `npm install` to vendor the pinned langserver. Re-run
   `safe_remove.py` over the eight-module set at the DEFAULT timeout and confirm the **SAFE**
   verdict still holds on today's tree — it is a re-execution, not an inherited claim. **COMMIT**
   the evidence.
2. Delete the six SAFE targets with all four coupled surfaces each (clause 1). Targeted tests
   green. **COMMIT**
3. Edit `ARCHITECTURE.md`'s prose naming the two `desired_state_*` files, then delete the pair
   with their coupled surfaces;
   `test_the_live_tree_carries_no_dangling_process_reference` stays green (clause 2). **COMMIT**
4. Retract the three stale tombstone claims and land the `/override` `status: removed` entry with
   its `removed_in:`; `release_lint.py --version 1.5.0` stays at **0 FAIL** (clause 3). **COMMIT**
5. Disposition `deploy/lived_sandbox/` file by file — `arc.py` KEPT for `[#267]`, the seven
   `REFUSED` files KEPT-as-inconclusive with the reason recorded per file (clause 4). **COMMIT**
6. Final: `pytest` green, plus the **bytes-removed number** this lane delivered. One end-of-lane
   artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body. **`ecosystem/organ-index.md`
  carries a stale `/override` row; it is the integrator's regen, flagged not fixed here.**
- No edits outside this lane's declared footprint. The footprint is: the eight target modules and
  their four coupled surfaces each; `ARCHITECTURE.md`'s `desired_state_*` prose; the three stale
  tombstone claims; the manifest's `/override` entry; `deploy/lived_sandbox/` dispositions.
- **Do not delete `config/requirements-dev.txt`** (clause 5) and **do not delete any
  `deploy/lived_sandbox/` file on a `REFUSED` verdict** — `REFUSED` is inconclusive, and
  inconclusive means KEEP.
- **Do not regenerate `ecosystem/doc-counts.md` beyond the narrow count line** a gate demands, if
  one does. The first run hit exactly this and kept it to one line; the discretionary regen is
  the integrator's.
