# LANE lane-x-734-retire-stage — the first run of the retire stage - ten dispositioned orphans removed with tombstones and lifecycle records

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-734-retire-stage LANE-x-734-retire-stage.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #734 · lane-x-734-retire-stage]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-734-retire-stage` already exists, so re-running the line is a no-op
rather than a collision.

**Explicit model at the dispatch act (`AX7-5`, standing until `[#717]` lands).** The
canonical line above is written in the exact grammar the contract gate admits
(`gen_lane_contract.py:227` — `Dispatch-Lane <slug> <file> [-Effort <tier>]`, anchored,
with **no `-Model` alternative**), which is why the model is not on it. `[#717]` is the
open row for that omission. Until it lands the model is made explicit at the dispatch
act instead, in one of these two equivalent forms:

```
dispatch LANE-x-734-retire-stage.md -Run
Dispatch-Lane lane-x-734-retire-stage LANE-x-734-retire-stage.md -Effort high -Model sonnet
```

The first is the ruled verb: it reads the `## Dispatch` fence above and executes it,
and `Start-DispatchLane`'s `-Model` defaults to `opus`. This lane declares `sonnet` in
its routing row, so the declared and dispatched models **agree by construction** — the
`[#717]` mismatch cannot bite this lane, and the DryRun receipt is the evidence, not this
sentence. The second passes it explicitly and is used where any doubt exists.

## Worktree pairing

slug `lane-x-734-retire-stage` -> branch `worktree-lane-x-734-retire-stage` -> contract `LANE-x-734-retire-stage.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. Each of the ten targets is deleted **only if** `deploy/release_lint.py`-green, the reverse-dep oracle (`scripts/reverse_dep_oracle.py`, via `scripts/safe_remove.py`) shows no live importer or reader, AND the targeted tests stay green — otherwise it is **KEPT with a written one-line reason**. A silent pass is NOT evidence: the dispatcher's own pre-run of `safe_remove.py` over the eight modules produced NO OUTPUT AT ALL, so the lane re-runs it and treats empty output as inconclusive rather than as clearance.
2. Every removal is recorded `deprecated` -> `removed` in `ecosystem/organ-index.md` with the reason "UNTRIGGERED + UNREAD >= 60 days, census 7bce09e5", and tombstoned `status: removed` (version, reason) in `deploy/manifest-v1.5.0.yaml` so the carrier prunes it from every consumer. `release_lint` green. This is the FIRST RUN of the AX13-2/AX13-3 retire stage, not an exception.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md` (batch X wave 1 first set + the deletion lane), as amended by `to-cc/AMEND-BATCH-X-ROSTER-014.md` AX14-1 (fill to 6) and `-015.md` AX15-3 (slot 6 = W-2'). The GO covers every roster lane; no lane outside the roster fires on it (AX14-3).

AX12-1 binds this contract: the row's Done-when is carried **verbatim**, and so is every AX clause addressed to it, quoted with its AX id. This lane's FIRST COMMIT writes these clauses into its own row (the AW-2 / `[#680]` pattern) — nothing here stays SAID. Where a clause names a row this lane did not file, the lane files the clause against its own row and reports the untouched one in its end packet rather than editing a row it does not own.


### Row `[#734]` — Done-when, verbatim

> Done when: each of the 35 non-live census items carries exactly one of DELETE, TRIGGER (with the naming hook/gate/schedule) or KEEP (with a one-line reason); the 16 UNKNOWN are resolved to a live/non-live verdict by a second pass rather than carried forward; all of it is delivered as ONE file taking ONE operator GO; and the approved deletions execute in a single lane after the GO, with the counts read from the census artifact's own **REPO TOTAL** row rather than tallied from its table or trusted from this row · **Done-when authored by the filing lane** from AX11-3


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX11-3` — verbatim

> - **AX11-3 · Cleanup is an act, not a note.** From the domain census (248 items: 197 LIVE, 24 UNTRIGGERED, 10 UNREAD, 1 GARBAGE-CANDIDATE, 16 UNKNOWN): the 35 non-live items get a proposal each — DELETE (git keeps history) · TRIGGER (named hook/gate/schedule) · KEEP with a one-line reason — delivered as one file for one operator GO; the 16 UNKNOWN are resolved by a second pass, not left. Deletions execute in one lane after the GO.


### `AX12-1` — verbatim

> - **AX12-1 · Clauses ride the lanes, no extra lane.** At batch X contract freeze each lane's contract carries its row's Done-when verbatim PLUS every AX clause addressed to that row (AMEND-BATCH-X-ROSTER-001…011), quoted verbatim with its AX id; the lane's first commit writes those clauses into its own row (the AW-2 / `[#680]` pattern). The floor-declaration row (AX4-1, with AX8-4, AX9-4, AX10-3 folded in) is filed by X1-1's lane in its first commit. AMEND-003/004/005 are carried this way; nothing stays SAID.


### `AX13-2` — verbatim

> - **AX13-2 · Retire step in the batch protocol (PLAYBOOK Ch8).** At every batch close the integrator emits ONE file, `DELETE-LIST-<date>.md`: every `deprecated` item with evidence, for one operator GO (the GO is a file, `[#685]`). Every batch then carries a standing retire lane that deletes the GO'd set through `safe_remove.py` + the reverse-dep oracle, targeted tests green, one commit, row filed in its first commit.


### `AX13-3` — verbatim

> - **AX13-3 · Tombstone in the floor.** The deploy manifest admits `status: removed` (version, reason) so the carrier prunes the item from every consumer; the W-4 `/override` removal gets its tombstone retroactively. Floor: MUST.


### `AX13-4` — verbatim

> - **AX13-4 · Today's X-DEL is the first run of AX13-2/3, not an exception:** its contract cites this rule, its ten targets are recorded as `deprecated` → `removed` in the index with reason "UNTRIGGERED + UNREAD ≥ 60 days, census 7bce09e5", and each deletion writes its tombstone. The operator's GO is the paste that dispatches it.


### `AX13-5` — verbatim

> - **AX13-5 · Recorded:** the cleanup digest counted 7 DELETE proposals while listing 10; the census missed runtime reads (10 of 16 UNKNOWN files are read by `audit.py`) — the lifecycle census must read FPG-1's `imports`/`reads` edges, not only `.pre-commit-config.yaml`.

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


## GO footprint — bounded by AX17-2, and a silent tool is INCONCLUSIVE

**The operator's GO covers, per target, EXACTLY these and nothing beyond** (the `[#481]` /
AW6-1 reading):

1. the target file itself,
2. its dedicated test file,
3. its `Disposition(...)` entry in `scripts/graph_queries.py`,
4. its entry in the `tests/test_graph_spine.py` list.

Anything else a deletion appears to require is **out of footprint**: stop, keep the target,
and report it. A tidy-up that felt implied is exactly how a bounded GO becomes an unbounded one.

**A silent result is not a pass.** `safe_remove.py` / the reverse-dep oracle producing NO
OUTPUT is **INCONCLUSIVE**, and an inconclusive target is **KEPT with that reason recorded**.
A file is removed ONLY on an explicit "no importer, no reader" verdict. The dispatcher's own
pre-run of `safe_remove.py` over the eight modules ran past 120 s and printed nothing at all,
which is why this clause exists rather than being left to judgement.

**A name-grep is not the other half of the evidence.** The dispatcher's sweep returned
hundreds of "referrers" per target that were almost entirely prose mentions in `docs/`. It
proves nothing in either direction; do not use it to clear or to condemn a target.

**Model:** this lane runs at `sonnet` (AX17-2, mechanical list work under AX4-2). Because
`[#717]` is open — the carried fence omits `-Model` and `Start-DispatchLane` defaults to
`opus` — the model is passed EXPLICITLY at the dispatch act. This lane is the live instance
of that defect: dispatched by its own carried line it would silently run at opus.

## Targets — and what each deletion actually touches

**Verified present by the dispatcher at freeze time** (all ten resolve; `lived_sandbox/` is
8 tracked `.py` files plus 8 untracked `.pyc`). **All eight modules are ALREADY dispositioned
orphans** in `scripts/graph_queries.py` with `owner="V+1 retirement-or-wiring list"` — the
census verdict is corroborated by the graph organ, which is why this list is credible.

**A deletion here is NOT one file.** Each module is coupled to up to three further surfaces,
measured at freeze time; removing the module alone REDs the suite:

```
target                                    dedicated test                  other coupled surfaces
scripts/boundary_headers.py               tests/test_boundary_headers.py  graph_queries Disposition; test_graph_spine list
scripts/boundary_report.py                (via test_boundary_headers)     graph_queries Disposition; imported BY boundary_headers.py:58
scripts/cloud_provisioning.py             tests/test_cloud_provisioning.py graph_queries Disposition; test_graph_spine list
scripts/seed_runbook.py                   tests/test_seed_runbook.py      graph_queries Disposition; test_graph_spine list
scripts/validate_onboarding_rulings.py    tests/test_onboarding_rulings.py graph_queries Disposition; test_graph_spine list
scripts/probe_child_backlogs.py           tests/test_probe_child_backlogs.py graph_queries Disposition; test_graph_spine list
scripts/desired_state_loader.py           tests/test_desired_state_loader.py graph_queries Disposition; imported BY desired_state_report.py:50
scripts/desired_state_report.py           tests/test_desired_state_report.py graph_queries Disposition; test_graph_spine list
deploy/lived_sandbox/ (8 tracked .py)     -                               NOT a scripts/ module: safe_remove.py does not cover it
config/requirements-dev.txt               -                               NOT a scripts/ module: safe_remove.py does not cover it
```

**Two coupled PAIRS must move together or in dependency order:** `boundary_headers` imports
`boundary_report`; `desired_state_report` imports `desired_state_loader`. Deleting the
imported half first breaks the importer.

**`safe_remove.py` covers only `scripts/` modules.** `deploy/lived_sandbox/` and
`config/requirements-dev.txt` fall outside it and need their own reader check — AX13-5's
warning applies directly: the census MISSED runtime reads (10 of 16 UNKNOWN files are read by
`audit.py`), so the lifecycle check must read FPG-1's `imports`/`reads` edges, not only
`.pre-commit-config.yaml`. A name-grep is not evidence in either direction: the dispatcher's
sweep returned hundreds of "referrers" per target that were almost entirely PROSE mentions.


## Steps

1. Step 0 sync (below). Then run `safe_remove.py` + the reverse-dep oracle over EVERY target and RECORD each verdict verbatim, including empty output. **COMMIT**
2. Delete each CLEARED target together with its coupled surfaces (table above) — module + its dedicated test + its `graph_queries.py` Disposition entry + its `tests/test_graph_spine.py` list entry. Pairs go together. Anything not cleared is KEPT with its reason. **COMMIT**
3. Tombstones in `deploy/manifest-v1.5.0.yaml` and lifecycle records in `ecosystem/organ-index.md`. **COMMIT**
4. `release_lint` green + targeted tests green; end-of-lane artifact lists deleted vs KEPT-with-reason. **COMMIT, then STOP.**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Step 0 — sync before anything else (MANDATORY until `[#716]` lands)

`[#716]` is open: `worktree.baseRef` is unset, so this lane branches from `origin/main`
and may start behind local `main`. **The step-0 sync is mandatory and may not be dropped
on the grounds that `[#716]` is being fixed** — it is retired only by the change that
makes that row's test green. A generator run against a base that lags `main` silently
DROPS rows that exist on `main`, and the dropped row looks like a clean regeneration.

```
git fetch origin
git merge origin/main        # or: git merge main, from the primary's ref
uv run --locked python -c "print('base synced')"
```

Then, and only then, run the lane's own steps.
