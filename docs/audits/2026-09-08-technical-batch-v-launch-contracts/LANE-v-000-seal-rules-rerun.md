# LANE lane-v-000-seal-rules-rerun — Fix the two hub-local seal rules that manufacture the 336 WAIVEs and re-run the seal on corp-monorepo after V-2 merges, printing the new count.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-000-seal-rules-rerun LANE-v-000-seal-rules-rerun.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #000 · lane-v-000-seal-rules-rerun]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-000-seal-rules-rerun` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-000-seal-rules-rerun` -> branch `worktree-lane-v-000-seal-rules-rerun` -> contract `LANE-v-000-seal-rules-rerun.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- the two hub-local seal rules named in DECLARE-REVIEWS §A.4
- the re-run and its printed count (a report artifact under `docs/audits/`)

**Pinned OUT — another lane owns these, or nobody does:**

- `ecosystem/fleet-shape-spec.yaml` — V-2 owns it; this lane READS it
- consumer repos are READ-ONLY: `git -C <repo> ls-files`, never a write
- no seal LIST is ruled here (HANDOVER-NOTE B.8 — the operator rules tens at Sitting 3)

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **SERIALIZED behind V-2** by the step-0 coupling scan (C1): both lanes reach the seal, and this lane's re-run is only meaningful on V-2's merged result.

## Done-contract (immutable)

1. seal WAIVE count **336 -> N, with N PRINTED** — the number is the closure, not an adjective.
2. the re-run is **witnessed post-V-2 merge**, and the contract records which merge SHA it ran against.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

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

1. WAIT for `PACKET-MERGED` on V-2, or verify V-2's merge on `origin/main` yourself. This wait is CODE — a loop with an interval, a bound and a state predicate read from the file surface — never a turn that ends intending to look again (PLAYBOOK Ch8 'Poll-as-code').
2. Identify the two hub-local rules from DECLARE-REVIEWS §A.4 and prove each one is what produces WAIVEs. **If MORE THAN TWO rules are implicated, STOP and name them** — the ruling was two. **COMMIT** the measurement.
3. Fix both rules. **COMMIT**
4. Re-run the seal on corp-monorepo READ-ONLY; PRINT the new count N and name the merge SHA the run was made against. **COMMIT**
5. Targeted tests green; end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- Do not rule any seal list — that is the operator's, at Sitting 3, after this lane.
- Do not add waivers. A waiver that hides a rule defect is the defect.
- Do not widen past two rules without STOPping first.
- Do not write anything into a consumer repo.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- DECLARE-REVIEWS §A.4
- REVIEW carry 4
- `docs/audits/2026-09-06-technical-seal-report-corp-monorepo.md` (the report that produced 336)

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge on V-2/V-3/V-5/V-6/V-7; the reviewer model name goes in the tally, and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`. The lane's authoritative surface is THIS file; a correction re-enters as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*

## AMENDMENT — AMEND-BATCH-V-002, applied before dispatch

**The batch roster changed; this lane's own scope did not.** V-7 (FPG-1 + `orphan_census`) left
batch V and returns as V+1's first lane; **V-8 — offload admission** took its slot. Lane count
stays six, so this contract's "Batch gates (all six lanes)" block still reads true.

**Launch verb, for batch V only.** `dispatch <FILE.md>` REFUSES every contract this generator
emits (`Assert-ClaudeCommand` demands a `claude` head token; the generator writes
`Dispatch-Lane`). Measured 6/6 at step 0. The **fallback** row is in force for this batch:
`Dispatch-Local <slug> <FILE>.md -Effort high`, DryRun-verified 6/6. V-5 owns the generator fix.
