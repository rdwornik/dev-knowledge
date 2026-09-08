# LANE lane-v-000-fpg-orphan-census — Make FPG-1 the single source for corpus-structure edges and build orphan_census as its first query, computed by the hub over consumer trees read-only.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-000-fpg-orphan-census LANE-v-000-fpg-orphan-census.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #000 · lane-v-000-fpg-orphan-census]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-000-fpg-orphan-census` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-000-fpg-orphan-census` -> branch `worktree-lane-v-000-fpg-orphan-census` -> contract `LANE-v-000-fpg-orphan-census.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- `scripts/file_purpose_graph.py` (the FPG-1 API surface)
- the new `orphan_census` organ and its report
- the ONE duplicate edge computation this lane removes, plus the proof it was duplicate

**Pinned OUT — another lane owns these, or nobody does:**

- migrate `orphan_census` ONLY — every other organ migrates in its own arc with its own proof
- state gates STAY gates; do not migrate one
- consumer trees are READ-ONLY
- `docs/intake/2026-08-22-tech-document-dependency-graph-organ.md` — V-4 owns the `:650` edit

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **`orphan_census` DOES NOT EXIST as an organ today.** The dispatcher measured it at step 0: no hit in `scripts/`, no row in `ecosystem/organ-index.md`. It is intake **#86** (`docs/intake/2026-09-07-tech-orphan-census-organ.md`, status DRAFT). The intent's phrasing *'orphan_census reads FPG-1 no -> yes'* therefore means **BUILD it reading FPG-1**, not migrate an existing reader. Scope is larger than 'migration' implies — say so in the end packet.
- `rustworkx` IS declared in `pyproject.toml` (the FPG-1 dependency resolves).

## Done-contract (immutable)

1. orphan count from FPG-1 **absent -> N, with N PRINTED** per repo.
2. `orphan_census` **absent -> present and reading FPG-1** (see the step-0 note: the organ does not exist today, so this lane BUILDS it).
3. a second graph computation for the same edge class **present -> removed, with its proof**.
4. Docs and code in English; hyphen-only names; logging rather than print;
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

1. PLAN round: the edge-type vocabulary and the report location. Those are the TWO budgeted forks; a third is a STOP.
2. Define the FPG-1 API for corpus-structure edges ONLY: citation · generation · template · test · script call-site. **Prose mentions are NOT edges** (hard problem 6). **COMMIT**
3. Build `orphan_census` as FPG-1's first query, computed by the hub over consumer trees read-only. **COMMIT**
4. Find the second computation of the same edge class, remove it, and PROVE it was duplicate. **COMMIT**
5. PRINT N per repo; targeted tests green; end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- Do not ship the graph as a PULL component — a consumer of identical shape yields an empty graph.
- Do not migrate any state gate.
- Do not treat prose mentions as edges.
- Z-C3 is CITED, not re-argued.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- DECLARE-REVIEWS §A.1–2
- DECLARE-GRAPH (as corrected)
- ADR-118
- Z-C3
- HANDOVER-ARCHITECTURE L2 + hard problem 6
- `docs/intake/2026-09-07-tech-orphan-census-organ.md` (intake #86, DRAFT)

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge on V-2/V-3/V-5/V-6/V-7; the reviewer model name goes in the tally, and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`. The lane's authoritative surface is THIS file; a correction re-enters as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*
