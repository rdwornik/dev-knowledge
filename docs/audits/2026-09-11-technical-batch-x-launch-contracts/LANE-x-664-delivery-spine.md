# LANE lane-x-664-delivery-spine — FPG-1 becomes the delivery spine - three commit-tier refusals, organs become views, and the deny-and-point hook rides along

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-664-delivery-spine LANE-x-664-delivery-spine.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #664 · lane-x-664-delivery-spine]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-664-delivery-spine` already exists, so re-running the line is a no-op
rather than a collision.

**Explicit model at the dispatch act (`AX7-5`, standing until `[#717]` lands).** The
canonical line above is written in the exact grammar the contract gate admits
(`gen_lane_contract.py:227` — `Dispatch-Lane <slug> <file> [-Effort <tier>]`, anchored,
with **no `-Model` alternative**), which is why the model is not on it. `[#717]` is the
open row for that omission. Until it lands the model is made explicit at the dispatch
act instead, in one of these two equivalent forms:

```
dispatch LANE-x-664-delivery-spine.md -Run
Dispatch-Lane lane-x-664-delivery-spine LANE-x-664-delivery-spine.md -Effort high -Model opus
```

The first is the ruled verb: it reads the `## Dispatch` fence above and executes it,
and `Start-DispatchLane`'s `-Model` defaults to `opus`. This lane declares `opus` in
its routing row, so the declared and dispatched models **agree by construction** — the
`[#717]` mismatch cannot bite this lane, and the DryRun receipt is the evidence, not this
sentence. The second passes it explicitly and is used where any doubt exists.

## Worktree pairing

slug `lane-x-664-delivery-spine` -> branch `worktree-lane-x-664-delivery-spine` -> contract `LANE-x-664-delivery-spine.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The three queries REFUSE at commit tier with a trip-test each — `orphan_census` (script node with no inbound `triggers` edge), `task_coverage` (file changed in the commit with no inbound `implements` edge from an OPEN task), `process_list` (the traversal; ARCHITECTURE Ch2 RENDERED from it). The graph is built on every commit and PERSISTED (sqlite, stdlib). `orphan_census` reaches 0 against its STATED node class after dispositions; `task_coverage` reports 0 FAIL on the merged tree. The blanket "12 -> 0" bar is DEAD — re-measure under §A.1's five-kind class rather than inheriting the integer. The 32-vs-20 cardinality gap is RECORDED, not rounded.
2. **`[#727]` rides in this lane** (dispatcher's call on serialize-groups — neither row declares one, so the disjointness constraint binds nothing, and the two are file-disjoint: `.claude/settings.json` against `.pre-commit-config.yaml` + the graph organs). Its Done-when is carried verbatim below: a `PreToolUse` deny-and-point hook whose exception text NAMES the organ to run, a RED-first trip-test asserting BOTH the denial and the pointer, ordinary non-governed searching provably unaffected, floor: MUST. Over-broad matching wedges every session — that is the known failure mode and the test guards it.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md` (batch X wave 1 first set + the deletion lane), as amended by `to-cc/AMEND-BATCH-X-ROSTER-014.md` AX14-1 (fill to 6) and `-015.md` AX15-3 (slot 6 = W-2'). The GO covers every roster lane; no lane outside the roster fires on it (AX14-3).

AX12-1 binds this contract: the row's Done-when is carried **verbatim**, and so is every AX clause addressed to it, quoted with its AX id. This lane's FIRST COMMIT writes these clauses into its own row (the AW-2 / `[#680]` pattern) — nothing here stays SAID. Where a clause names a row this lane did not file, the lane files the clause against its own row and reports the untouched one in its end packet rather than editing a row it does not own.


### Row `[#664]` — Done-when, verbatim

> Done when: the corpus-structure edge computations are re-measured under §A.1's five-kind class (citation, generation, template, test, script call-site) and driven to 0 with every organ holding one reading FPG-1 instead — **the blanket "12 → 0" bar is DEAD**, withdrawn by `ff103444` because 12 counted state gates the class excludes, so the migration lane re-measures rather than inheriting an integer; the three queries refuse at commit tier with a trip-test each; `orphan_census` reaches 0 against its stated node class after dispositions; and `task_coverage` reports 0 FAIL on the merged tree


### Row `[#727]` — Done-when, verbatim

> Done when: a `PreToolUse` hook on `Bash` and `Grep` DENIES a raw search (`grep`, `rg`, `find`, `Select-String`) over the governed questions AX9-1 enumerates, with exception text naming the organ to run instead; a RED-first trip-test sends a raw grep and asserts BOTH the denial and the pointer; ordinary non-governed searching is unaffected, proven by a test that a plain string search still runs; and the component is declared **floor: MUST** · **Done-when carried from AX9-1's clauses**, with the over-match guard added by the filing lane


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX9-4` — verbatim

> - **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".


### `AX9-1` — verbatim

> - **AX9-1 · NEW row, X1 (joins X1-1's lane or its own — dispatcher's call on serialize-groups): deny-and-point hook.** A `PreToolUse` hook on `Bash`/`Grep`: a raw search (`grep`, `rg`, `find`, `Select-String`) over governed questions — what is this file, who triggers it, where does X live, which tests cover Y, is there already an organ for Z — is DENIED with the exception text naming the organ to run (`graph_queries.py why|process-list`, the impacted-test selector, organ-index). RED-first: a trip-test sends a raw grep and asserts the denial and the pointer. Precondition: CC verifies on this version that a PreToolUse deny on Bash actually blocks (a known upstream issue reported the opposite); if it does not, the same rule lives in `UserPromptSubmit`/skill hooks. Floor: MUST.


### `AX3-7` — verbatim

> - **AX3-7 · Waves after this amendment:** X1 = decision_coverage · conductor E (ships in floor) · merge cost · routing · spine `[#664]` · docs cut. X2 = prompt distiller · logs · `[#589]` byte bar + archive · `[#687]` keys · `[#669]` conductor · codespace row. X3 = `[#664]` step D + organ map · `[#667]` render · telemetry + GO artifact · M03 re-run.

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

## Steps

1. Step 0 sync (below). **MODE is `plan`** — produce the plan and the library-first check before any build code. Decision budget 2. **COMMIT**
2. RED-first witnesses for all three queries and for the deny-and-point hook, failing first. **COMMIT**
3. Persist the graph (sqlite) and build the three queries as commit-tier refusals; migrate each organ to READ the graph instead of parsing its own edges. **COMMIT**
4. The `[#727]` hook: denial + pointer + the non-governed-search test. **COMMIT**
5. Terra pre-merge. **This lane MERGES LAST in its batch** (the row says so). **COMMIT, then STOP.**
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
