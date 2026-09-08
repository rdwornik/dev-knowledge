# LANE lane-v-000-shape-spec-clauses — Wire the three unread fleet-shape clauses to a reader and add the kind parameter to home_grammar, so every clause an organ claims is a clause an organ opens.

| Model | Mode | Effort |
|---|---|---|
| opus | plan | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-v-000-shape-spec-clauses LANE-v-000-shape-spec-clauses.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #000 · lane-v-000-shape-spec-clauses]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-v-000-shape-spec-clauses` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-v-000-shape-spec-clauses` -> branch `worktree-lane-v-000-shape-spec-clauses` -> contract `LANE-v-000-shape-spec-clauses.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Footprint and pins

**This lane OWNS, and nothing outside it:**

- ecosystem/fleet-shape-spec.yaml
- scripts/validate_hermetization.py (clause READERS only)
- scripts/audit_checks/check_workspace_settings.py
- tests/ (the new spec test)

**Pinned OUT — another lane owns these, or nobody does:**

- `BACKLOG.md` — `#73` is INTAKE 73, not a BACKLOG row; its status flips at integration
- the seal RE-RUN — V-3 owns it and waits on this lane's merge
- `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md` — read, never written here

**Step-0 findings the dispatcher resolved before freezing this contract:**

- **Path corrected at step 0:** the intent names `check_workspace_settings.py` with no directory; it lives at **`scripts/audit_checks/check_workspace_settings.py`**, not `scripts/`. Resolved 2026-09-08 by the dispatcher.
- **`#73` is an INTAKE id, not a BACKLOG id** — `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`, `intake-id: 73`, status DRAFT. That is why this lane's id is the no-row `000`.

## Done-contract (immutable)

1. clauses read by an organ **2/5 -> 5/5** — `python_layout`, `vscode` and `sorting` are each OPENED by a named reader, not merely referenced.
2. clauses whose `asserted_by` names a non-reading organ **2 -> 0**.
3. `home_grammar` carries the kind parameter — six kinds (source · test · data · model · eval · tooling), ONE home each, and a repo declares which it has (AMEND-SESSION-PLAN-001 §2).
4. reader-proof spec test **absent -> present**, and it FAILS when a named organ stops reading its clause.
5. Docs and code in English; hyphen-only names; logging rather than print;
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

1. Read `ecosystem/fleet-shape-spec.yaml` and enumerate all five clauses with their `asserted_by` values; record which organ (if any) OPENS each. **COMMIT** the measurement as the lane's first artifact.
2. PLAN round: state where the kind declaration lives and where the three new readers sit. These are the lane's TWO budgeted forks — decide both, record both, and do not open a third.
3. RED first (ADR-108 §B): write the reader-proof spec test so it FAILS on today's tree. **COMMIT**
4. Wire `python_layout`, `vscode`, `sorting` to their readers; extend `home_grammar` with the six kinds. **COMMIT**
5. Fix `scripts/audit_checks/check_workspace_settings.py` to read the YAML it claims to assert. **COMMIT**
6. Targeted tests green against the 28-RED baseline; end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- Do not add a NEW clause for kinds — extend `home_grammar`.
- Do not satisfy `asserted_by` by making a path exist; the organ must OPEN the file.
- Do not touch `BACKLOG.md`.
- Do not re-run the seal — that is V-3, and it is serialized behind this lane's merge.
- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Pointers

- `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md` (intake #73, DRAFT)
- `to-browser/DIGEST-73-shape-contract.md`
- `to-cc/AMEND-SESSION-PLAN-001.md` §1–§2
- HANDOVER-NOTE B.3

## Batch gates (all six lanes)

- The baseline is **28 RED @ `08c35b9c`** — compare against it, NEVER against zero.
- No lane writes `BACKLOG.md` except V-4.
- No lane creates a new path or folder without citing the convention that sanctions it.
- **No lane ends a turn on a peer wait.** A wait is code: an interval, a bound, and a state predicate read from the file surface (PLAYBOOK Ch8 'Poll-as-code').
- Receipt = commit. `git stash list` is EMPTY at STOP.
- Reviewer per D3 (AMEND-002): terra pre-merge on V-2/V-3/V-5/V-6/V-7; the reviewer model name goes in the tally, and a mismatch is `review=NONE`.

*Frozen at dispatch by dispatcher-V, 2026-09-08, against `main` @ `08c35b9c`. The lane's authoritative surface is THIS file; a correction re-enters as a NEW contract, never as a mid-flight message (ADR-110 per-lane requirement 1).*
