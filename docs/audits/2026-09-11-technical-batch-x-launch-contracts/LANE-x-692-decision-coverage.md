# LANE lane-x-692-decision-coverage — decision_coverage - every accepted decision carries a lifecycle state and at least one implementing row, refused at commit tier and at onboarding

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-692-decision-coverage LANE-x-692-decision-coverage.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #692 · lane-x-692-decision-coverage]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-692-decision-coverage` already exists, so re-running the line is a no-op
rather than a collision.

**Explicit model at the dispatch act (`AX7-5`, standing until `[#717]` lands).** The
canonical line above is written in the exact grammar the contract gate admits
(`gen_lane_contract.py:227` — `Dispatch-Lane <slug> <file> [-Effort <tier>]`, anchored,
with **no `-Model` alternative**), which is why the model is not on it. `[#717]` is the
open row for that omission. Until it lands the model is made explicit at the dispatch
act instead, in one of these two equivalent forms:

```
dispatch LANE-x-692-decision-coverage.md -Run
Dispatch-Lane lane-x-692-decision-coverage LANE-x-692-decision-coverage.md -Effort high -Model opus
```

The first is the ruled verb: it reads the `## Dispatch` fence above and executes it,
and `Start-DispatchLane`'s `-Model` defaults to `opus`. This lane declares `opus` in
its routing row, so the declared and dispatched models **agree by construction** — the
`[#717]` mismatch cannot bite this lane, and the DryRun receipt is the evidence, not this
sentence. The second passes it explicitly and is used where any doubt exists.

## Worktree pairing

slug `lane-x-692-decision-coverage` -> branch `worktree-lane-x-692-decision-coverage` -> contract `LANE-x-692-decision-coverage.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. `decision_coverage` REFUSES at commit tier and REFUSES onboarding when an accepted decision (ADR status Accepted · intake ACCEPTED/RATIFIED · a transport `DECLARE-`/`AMEND-`) has neither an implementing row (FPG-1 `implements` edge) nor a written "no implementation required" disposition; the refusal LISTS the decisions and states what must be done. RED-first witness: an accepted decision with no row makes the query FAIL.
2. `implements:` lands as a STRUCTURED, VALIDATED `tasks/` frontmatter key (`[ADR-n | intake-n | DECLARE-...]`); the handoff bundle emits the decision ledger (A9-2, with `LEDGER-OPERATOR-EXPECTATIONS-2026-09-10` as the fixture); `fleet_health` reports A9-3's four numbers. **This lane's FIRST COMMIT files the floor-declaration row** (AX4-1, with AX8-4, AX9-4 and AX10-3 folded in) **and files AX13-1 as an X2 row** — per AX12-1, nothing stays SAID.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.


## Carried rows and clauses (verbatim — AX12-1)

**Operator GO:** `to-browser/RATIFICATION-2026-09-11.md` (batch X wave 1 first set + the deletion lane), as amended by `to-cc/AMEND-BATCH-X-ROSTER-014.md` AX14-1 (fill to 6) and `-015.md` AX15-3 (slot 6 = W-2'). The GO covers every roster lane; no lane outside the roster fires on it (AX14-3).

AX12-1 binds this contract: the row's Done-when is carried **verbatim**, and so is every AX clause addressed to it, quoted with its AX id. This lane's FIRST COMMIT writes these clauses into its own row (the AW-2 / `[#680]` pattern) — nothing here stays SAID. Where a clause names a row this lane did not file, the lane files the clause against its own row and reports the untouched one in its end packet rather than editing a row it does not own.


### Row `[#692]` — Done-when, verbatim

> Done when: `to-cc/AMEND-SESSION-PLAN-009.md` A9-1, A9-2 and A9-3, carried verbatim, numbers included — "**A9-1 · Batch X lane 0 (before conductor E): `decision_coverage`.** Every decision — an ADR with status Accepted, an intake ACCEPTED/RATIFIED, a transport DECLARE-/AMEND- — carries a lifecycle state (considered → accepted → executing → done | superseded) and has at least one implementing row (FPG-1 `implements` edge) or a written "no implementation required" disposition. The query refuses at commit tier and refuses onboarding when an accepted decision has neither; the refusal lists the decisions and states what must be done — the operator's rule that a process deviation raises an exception that teaches the browser. RED-first trip-test: an accepted decision with no row makes the query fail." · "**A9-2 · The handoff carries the decision ledger.** The bundle generator emits, from `decision_coverage`, every open decision with its state; the incoming seat's plan must dispose each one (executing in batch N · scheduled with a row · refused in writing) before its plan is accepted — a probe, not prose. The outgoing seat's `LEDGER-OPERATOR-EXPECTATIONS-2026-09-10` is the manual precursor and the fixture." · "**A9-3 · Decision metric** (reported by `fleet_health`): decisions accepted, executing, done, and age of the oldest accepted-but-unexecuted decision."


### `AX4-1` — verbatim

> - **AX4-1 · Floor declaration is mandatory.** Every row and every lane contract carries `floor: MUST | hub-only`; a NEW organ, hook, gate, doc or command without it is refused at commit (validated against `ecosystem/parity-surfaces.yaml`; `fleet_parity` is the check). Default is MUST — hub-only requires a one-line reason. Applies retroactively to batch W's outputs and every batch X row: W-7 selector, W-2 guard, `decision_coverage`, routing, STANDING_RULINGS, the docs cut, conductor E — each dispositioned MUST or hub-only before X1 dispatches. Owner: `decision_coverage` lane (X1-1) gains this clause; the parity registry is the carrier.


### `AX9-4` — verbatim

> - **AX9-4 · Exists-before-build clause on the decision engine (X1-1) and the floor declaration (AX4-1):** a contract that CREATES an organ, script, hook or doc must quote a `process-list` / organ-index result showing no existing organ answers the need; a NEW organ without that quote is refused at the contract gate. This is the RED-first form of "check the process map before you build".


### `AX8-4` — verbatim

> - **AX8-4 · Templates are floor components** (the new-project starter): covered by X-C's census (`templates/`), declared MUST under AX4-1, rendered from the same source as the docs after the cut.


### `AX10-3` — verbatim

> - **AX10-3 · Floor: MUST.** Backlog management is identical in every consumer repo.


### `AX12-1` — verbatim

> - **AX12-1 · Clauses ride the lanes, no extra lane.** At batch X contract freeze each lane's contract carries its row's Done-when verbatim PLUS every AX clause addressed to that row (AMEND-BATCH-X-ROSTER-001…011), quoted verbatim with its AX id; the lane's first commit writes those clauses into its own row (the AW-2 / `[#680]` pattern). The floor-declaration row (AX4-1, with AX8-4, AX9-4, AX10-3 folded in) is filed by X1-1's lane in its first commit. AMEND-003/004/005 are carried this way; nothing stays SAID.


### `AX13-1` — verbatim

> - **AX13-1 · NEW row, X2: component lifecycle as data + automatic deprecation.** Every item in the organ index / FPG-1 carries `lifecycle: experimental | production | deprecated | removed` (the field X-C already collected) with `deprecated-since`, `reason`, `replacement`, `removal-floor-version`. The domain census runs on a schedule (nightly after conductor E; at each batch close until then) and flips any item UNTRIGGERED AND UNREAD for ≥ 30 days to `deprecated` automatically; a `deprecated` Python module warns on import via the standard `deprecated` decorator (library-first). RED-first: a fixture item aged past the bar is not flipped → the test fails.

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

1. Step 0 sync (below). Then FILE the floor-declaration row and the AX13-1 X2 row, and write every carried AX clause into `[#692]`'s own row. Rows this lane did not file are REPORTED, not edited. **COMMIT**
2. RED-first: the failing witness — an accepted decision with no implementing row — written and FAILING before any build code exists. **COMMIT**
3. Build `decision_coverage` + the `implements:` frontmatter key and its validator; wire the commit-tier refusal and the onboarding refusal, each with the listing text. **COMMIT**
4. A9-2 handoff decision-ledger leg and A9-3's `fleet_health` metric. **COMMIT**
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
