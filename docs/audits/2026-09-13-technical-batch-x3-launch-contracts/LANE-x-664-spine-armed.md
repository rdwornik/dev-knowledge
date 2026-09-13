# LANE lane-x-664-spine-armed — Arm the three [#664] commit-tier refusals with RED-first trip-tests, MEASURE the current numbers, and emit the delete/trigger/keep residue as a one-word-GO list -- without driving the numbers to zero, which is the operator's act

| Model | Mode | Effort |
|---|---|---|
| opusplan | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-664-spine-armed LANE-x-664-spine-armed.md -Effort high -Model opusplan
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #664 · lane-x-664-spine-armed]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`opusplan` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-664-spine-armed` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-x-664-spine-armed` -> branch `worktree-lane-x-664-spine-armed` -> contract `LANE-x-664-spine-armed.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The three commit-tier refusals EXIST and REFUSE: `orphan_census`, `task_coverage`, and the five-kind edge class -- each with its own RED-first trip-test.
2. The current numbers are MEASURED and reported.
3. The residue is emitted as `to-browser/DELETE-LIST-2026-09-13.md`: **delete / trigger / keep**, each row carrying its evidence, for ONE operator GO in the morning.
4. **Explicitly NOT done: driving the numbers to zero.** That is the next lane, after the GO -- deletions are the operator's act. A lane that would need the operator mid-night is mis-scoped, not brave (AX27-1).
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

1. RED-first trip-tests for all three refusals, before arming any of them. **COMMIT**
2. Arm the three refusals at commit tier. **COMMIT**
3. MEASURE and record the current numbers -- do not act on them. **COMMIT**
4. Emit the delete/trigger/keep list to `to-browser/`, every row with evidence. **COMMIT**
5. Final: targeted tests green, end-of-lane artifact. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Serialisation (AX27-3)

This lane and `lane-x-000-trustworthy-suite` may both touch the persisted graph store, so the
dispatcher SERIALISES them rather than refusing either: **`lane-x-000-trustworthy-suite` runs
first and this lane enters on its handback.** The order is stated in the batch manifest, which
is the record; this note is the point-of-use copy so the lane knows why it waited.
