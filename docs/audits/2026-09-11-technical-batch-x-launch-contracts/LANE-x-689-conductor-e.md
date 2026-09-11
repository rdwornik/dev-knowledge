# LANE lane-x-689-conductor-e — Conductor E - GitHub Actions as the runner, phase state stays in tasks/, required checks as the merge gate

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-689-conductor-e LANE-x-689-conductor-e.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #689 · lane-x-689-conductor-e]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-689-conductor-e` already exists, so re-running the line is a no-op
rather than a collision.

**Explicit model at the dispatch act (`AX7-5`, standing until `[#717]` lands).** The
canonical line above is written in the exact grammar the contract gate admits
(`gen_lane_contract.py:227` — `Dispatch-Lane <slug> <file> [-Effort <tier>]`, anchored,
with **no `-Model` alternative**), which is why the model is not on it. `[#717]` is the
open row for that omission. Until it lands the model is made explicit at the dispatch
act instead, in one of these two equivalent forms:

```
dispatch LANE-x-689-conductor-e.md -Run
Dispatch-Lane lane-x-689-conductor-e LANE-x-689-conductor-e.md -Effort high -Model opus
```

The first is the ruled verb: it reads the `## Dispatch` fence above and executes it,
and `Start-DispatchLane`'s `-Model` defaults to `opus`. This lane declares `opus` in
its routing row, so the declared and dispatched models **agree by construction** — the
`[#717]` mismatch cannot bite this lane, and the DryRun receipt is the evidence, not this
sentence. The second passes it explicitly and is used where any doubt exists.

## Worktree pairing

slug `lane-x-689-conductor-e` -> branch `worktree-lane-x-689-conductor-e` -> contract `LANE-x-689-conductor-e.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. §8's three build legs land: `.github/workflows/conductor.yml` (`on: push · pull_request · schedule · workflow_dispatch`) reading `tasks/` and evaluating the phase gate; the `phase:` field with `validate_backlog` knowing its enum; the SessionStart hook. Required checks on `main` (pytest, ruff, seal, terra) are the merge gate.
2. Per AX3-2 the workflow AND its required-check ruleset are declared **floor components** in the deploy manifest, so every consumer receives them. §6's four numbers are instrumented so the revert-to-B condition (1 and 3 do not fall) is measurable rather than asserted.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md` (batch X wave 1 first set + the deletion lane), as amended by `to-cc/AMEND-BATCH-X-ROSTER-014.md` AX14-1 (fill to 6) and `-015.md` AX15-3 (slot 6 = W-2'). The GO covers every roster lane; no lane outside the roster fires on it (AX14-3).

AX12-1 binds this contract: the row's Done-when is carried **verbatim**, and so is every AX clause addressed to it, quoted with its AX id. This lane's FIRST COMMIT writes these clauses into its own row (the AW-2 / `[#680]` pattern) — nothing here stays SAID. Where a clause names a row this lane did not file, the lane files the clause against its own row and reports the untouched one in its end packet rather than editing a row it does not own.


### Row `[#689]` — Done-when, verbatim

> Done when: the four numbers of `to-cc/DECLARE-CONDUCTOR-DECISION-2026-09-09.md` §6 move, carried verbatim from that section (the source hard-wraps; the wrap is not content) — "1. Phase transitions without operator action ÷ all transitions — today ~0%, target > 80% (Actions logs). 2. Operator hours per feature landed in corp-monorepo — today ∞, target: a number. 3. Operator pastes per week — today dozens, target < 5. 4. Organs deleted from the §5 list — target ≥ 10. If 1 and 3 do not fall, revert to B. No state migration needed."


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX9-4` — verbatim

> - **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".


### `AX3-2` — verbatim

> - **AX3-2 · Conductor E ships to consumers.** X1-2's Done-when adds: the Actions workflow and its required-check ruleset are floor components in the deploy manifest, so corp-monorepo (and every consumer) gets them with the floor; the operator sees runs in the repo's Actions tab and checks on every merge.


### `AX12-2` — verbatim

> - **AX12-2 · One role per substrate** (PLAYBOOK Ch8 Q1–Q4 still decides; ratification #7 bounds the workstation): CC cloud = read-only and text-only work at any hour · Codespace, attached, never detached = gate-dependent committing work in the daytime · local = committing work overnight only · GitHub Actions replaces the overnight local role once X1-2 lands. Detached Codespace lanes stay barred until the retire-or-fix row decides.

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

1. Step 0 sync (below). Then VERIFY §7's three preconditions and RECORD each verdict: the operator's GitHub Pro + required checks on a private repo · Actions minutes quota · `/install-github-app` on the hub repo. **D2 is the blocker and it is READ, never inferred** — it lives ONLY in `to-browser/RATIFICATION-2026-09-10 (1).md`; the same-named 4,332 B file lists GitHub Pro under NOT RATIFIED. If any precondition fails, PAUSE with the fact. **COMMIT**
2. RED-first: `phase:` field + `validate_backlog` enum witness, failing first. **COMMIT**
3. `conductor.yml` + the required-check ruleset. **COMMIT**
4. SessionStart hook, floor declaration per AX3-2, and §6's four numbers instrumented. **COMMIT**
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
