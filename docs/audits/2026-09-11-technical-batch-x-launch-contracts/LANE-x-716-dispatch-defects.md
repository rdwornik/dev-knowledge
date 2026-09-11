# LANE lane-x-716-dispatch-defects — the three measured dispatch defects fixed with a RED-first witness each

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-716-dispatch-defects LANE-x-716-dispatch-defects.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #716 · lane-x-716-dispatch-defects]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-716-dispatch-defects` already exists, so re-running the line is a no-op
rather than a collision.

**Explicit model at the dispatch act (`AX7-5`, standing until `[#717]` lands).** The
canonical line above is written in the exact grammar the contract gate admits
(`gen_lane_contract.py:227` — `Dispatch-Lane <slug> <file> [-Effort <tier>]`, anchored,
with **no `-Model` alternative**), which is why the model is not on it. `[#717]` is the
open row for that omission. Until it lands the model is made explicit at the dispatch
act instead, in one of these two equivalent forms:

```
dispatch LANE-x-716-dispatch-defects.md -Run
Dispatch-Lane lane-x-716-dispatch-defects LANE-x-716-dispatch-defects.md -Effort high -Model opus
```

The first is the ruled verb: it reads the `## Dispatch` fence above and executes it,
and `Start-DispatchLane`'s `-Model` defaults to `opus`. This lane declares `opus` in
its routing row, so the declared and dispatched models **agree by construction** — the
`[#717]` mismatch cannot bite this lane, and the DryRun receipt is the evidence, not this
sentence. The second passes it explicitly and is used where any doubt exists.

## Worktree pairing

slug `lane-x-716-dispatch-defects` -> branch `worktree-lane-x-716-dispatch-defects` -> contract `LANE-x-716-dispatch-defects.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. Three RED-first witnesses, ONE PER DEFECT, each FAILING against today's code before its fix: `[#718]` the generator writes where the verb reads, both resolved from ONE key (test asserts written path == the path the verb resolves); `[#717]` the launch line is RENDERED FROM the contract's `Model` row (test asserts rendered model == that row); `[#716]` a lane's base equals `main` HEAD at dispatch, asserted by a TEST rather than by the setting's value.
2. **`[#717]`'s fix must also widen the CHECKER, not only the generator** — measured by the dispatcher while freezing this very batch: `_DISPATCH_LINE_RE` (`scripts/gen_lane_contract.py:227`) is `^Dispatch-Lane <slug> <file>( -Effort <v>)?\s*$`, anchored, admitting **no `-Model`**, so a line carrying the model is refused as "no dispatch command line found". Rendering the model without widening this regex turns every contract RED. `[#716]`'s step-0 sync is retired from the lane-contract template ONLY in the same change that makes its test green.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md` (batch X wave 1 first set + the deletion lane), as amended by `to-cc/AMEND-BATCH-X-ROSTER-014.md` AX14-1 (fill to 6) and `-015.md` AX15-3 (slot 6 = W-2'). The GO covers every roster lane; no lane outside the roster fires on it (AX14-3).

AX12-1 binds this contract: the row's Done-when is carried **verbatim**, and so is every AX clause addressed to it, quoted with its AX id. This lane's FIRST COMMIT writes these clauses into its own row (the AW-2 / `[#680]` pattern) — nothing here stays SAID. Where a clause names a row this lane did not file, the lane files the clause against its own row and reports the untouched one in its end packet rather than editing a row it does not own.


### Row `[#716]` — Done-when, verbatim

> Done when: a lane's base equals `main` HEAD at dispatch, asserted by a TEST rather than by the setting's value -- so a dispatcher on a non-`main` branch cannot satisfy it accidentally; the RED-first witness FAILS against today's unset configuration before the fix makes it green; and the mandatory step-0 sync is retired from the lane-contract template only in the same change that makes that test green · **Done-when authored by the filing lane** from AX7-3's clause, with the `head`-versus-`main`-HEAD precision added from the verification AX7-3 asked for


### Row `[#717]` — Done-when, verbatim

> Done when: the launch line is RENDERED FROM the contract's `Model` row rather than omitting it, and a test asserts the rendered line's model equals that row -- a RED-first witness that FAILS today against a sonnet contract whose carried line dispatches at opus · **Done-when carried from AX7-3's clause** ("the launch line is rendered from the contract's `Model` row, and a test asserts they match")


### Row `[#718]` — Done-when, verbatim

> Done when: the generator writes lane contracts to the location the verb reads, both resolved from ONE key rather than from two independently-correct literals, and a test asserts the written path equals the path the verb resolves -- a RED-first witness that FAILS against today's split before the fix makes it green · **Done-when carried from AX7-3's clause** ("the generator writes lane contracts to the location the verb reads -- one key")


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX9-4` — verbatim

> - **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".


### `AX7-3` — verbatim

> - **AX7-3 · Path registry row is X2, not conditional:** one source of governed paths read by generators and verbs; a path not in it is refused. Evidence: three instances in one day — contracts written to `to-cc/` while `Dispatch-Lane` reads the prompts root; the generator-carried line omits `-Model` so a sonnet contract runs at opus; `worktree.baseRef` unset so lanes branch two merges behind local `main`. Each is a row (FILE) with a RED-first test; the step-0 sync stays mandatory until baseRef is fixed.


### `AX7-5` — verbatim

> - **AX7-5 · Recorded from X-C's dispatch:** `config/` and `plugins/` were missing from AX6-1's folder list (added); "cheapest admitted" resolves to sonnet — haiku is not in `provider-registry.yaml`'s admission (a routing-lane fact); `-Model` must be explicit until AX7-3 lands.


### `AX14-1` — verbatim

> - **AX14-1 · Fill to 6.** First set grows from 4 to 6: lane 5 = the three dispatch defects `[#716]` worktree baseRef · `[#717]` launch line carries `-Model` · `[#718]` contract write location = verb read location, one lane, RED-first per defect; lane 6 = X1-4 routing + telemetry once the W-2 fix is on `main` — until then AX9-1's deny-and-point hook as its own lane if X1-5 did not absorb it.

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

1. Step 0 sync (below). **COMMIT**
2. `[#718]`: RED-first witness, then one key for writer and reader. **COMMIT**
3. `[#717]`: RED-first witness, then render the model from the `Model` row AND widen `_DISPATCH_LINE_RE` to admit it; re-check all six batch-X contracts still pass. **COMMIT**
4. `[#716]`: RED-first witness asserting base == `main` HEAD, then the fix; retire the template's step-0 sync in the SAME change. **COMMIT, then STOP.**
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
