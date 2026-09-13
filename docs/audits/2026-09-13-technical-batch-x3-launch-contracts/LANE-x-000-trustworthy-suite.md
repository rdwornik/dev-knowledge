# LANE lane-x-000-trustworthy-suite — Make the suite trustworthy: the session-scoped store that REDs sibling xdist workers, test_gen_handoff's stub audit module shadowing everything collected after it, and the one missing optional dependency behind 17 failures

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-000-trustworthy-suite LANE-x-000-trustworthy-suite.md -Effort high -Model opus
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-x-000-trustworthy-suite · lane-x-000-trustworthy-suite]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`opus` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-000-trustworthy-suite` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-x-000-trustworthy-suite` -> branch `worktree-lane-x-000-trustworthy-suite` -> contract `LANE-x-000-trustworthy-suite.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The session-scoped graph store no longer REDs sibling xdist workers: a RED-first test reproduces the cross-worker collision and passes after the fix.
2. `test_gen_handoff`'s stub audit module no longer shadows modules collected AFTER it -- proven by a test that collects the stub alongside a later module importing the real `audit`, which today picks up the stub.
3. The one missing optional dependency behind the 17 failures is either DECLARED in `pyproject.toml` and installed via `uv sync --locked`, **or** those tests are skipped BY DECLARATION with the reason named. Left implicit is not an outcome.
4. TARGETED tests only. This lane runs no full local suite -- the full suite runs once, at integration (`[#528]`). A green targeted run plus a named skip reason is the deliverable, not a suite number.
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

1. Reproduce all three RED-first, one test per defect, and NAME the missing dependency behind the 17 failures explicitly rather than describing it. **COMMIT**
2. Fix the session-scoped store so worker identity cannot collide across siblings. **COMMIT**
3. Fix the stub-module shadowing in `test_gen_handoff`. **COMMIT**
4. Declare-and-install, or skip-by-declaration, the optional dependency. **COMMIT**
5. Final: targeted tests green, end-of-lane artifact naming all three fixes and the dependency decision. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Measured facts this lane must not rediscover

These are recorded results from this repo, not guesses. Treat them as given:

- **Worker count changes the FAILURE COUNT.** Measured 41 failures at `-n 3` and 59 at
  `-n 6` on the same tree. Counts are therefore comparable ONLY at an identical `-n`.
  Never compare a number taken at one worker count against one taken at another.
- **`-n auto` on the full suite is OOM-killed** on the workstation; `-n 6` completes. A kill
  is a notification from the OS, not a test result -- do not record it as a failure count.
- **`-n 0` (serial) is unusably slow** for the full suite, and `-p no:xdist` collides with
  this repo's `addopts`; the way to ask for serial is `-n 0`, not the plugin flag.
- **Every invocation goes through `uv run --locked`.** A bare `pytest` inside a worktree
  inherits `VIRTUAL_ENV` from the primary tree, imports the PRIMARY checkout's source, and
  reports green about code this lane did not touch (STANDING_RULINGS D4).

## Serialisation (AX27-3)

This lane and `lane-x-664-spine-armed` may both touch the persisted graph store, so the
dispatcher SERIALISES them rather than refusing either: **this lane runs FIRST**, and
`lane-x-664-spine-armed` enters on this lane's handback. The order is stated in the batch
manifest, which is the record; this note is the point-of-use copy.
