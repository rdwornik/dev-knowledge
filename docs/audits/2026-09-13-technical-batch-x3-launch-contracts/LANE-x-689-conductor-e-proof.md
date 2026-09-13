# LANE lane-x-689-conductor-e-proof — Prove conductor E: run the full suite on GitHub Actions at a fixed worker count, twice on ONE pinned commit, and report identical counts and wall time -- or the runner's limit and the smallest shape that completes, as a measured finding

| Model | Mode | Effort |
|---|---|---|
| opusplan | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-689-conductor-e-proof LANE-x-689-conductor-e-proof.md -Effort high -Model opusplan
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #689 · lane-x-689-conductor-e-proof]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`opusplan` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-689-conductor-e-proof` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-x-689-conductor-e-proof` -> branch `worktree-lane-x-689-conductor-e-proof` -> contract `LANE-x-689-conductor-e-proof.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The full suite has run on GitHub Actions at a FIXED worker count, TWICE on ONE pinned commit SHA, and both runs' collected / passed / failed / errored counts AND wall times are recorded side by side in the end-of-lane artifact.
2. The verdict states whether the two runs are IDENTICAL in counts and comparable in wall time. A difference is a finding with its cause named, not a re-run until they agree -- rerunning until agreement measures nothing.
3. If the hosted runner cannot hold the suite -- memory, the 6-hour job limit, or the Actions minute budget -- the lane records the observed numbers AND the smallest shape that DOES complete (fewer workers, a split job, or a subset), as a measured verdict. **Never a retry loop** (AX27-4). Either outcome opens `[#689]`'s four numbers, which is the point of the lane.
4. The pinned SHA, the runner label and the worker count are stated explicitly, so a later run is COMPARABLE rather than merely similar.
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

1. Pin ONE commit SHA and state it. Confirm `.github/workflows/conductor.yml` is the runner under test and record its current shape before changing anything. **COMMIT**
2. Run the suite on Actions at a fixed worker count, twice, on that one SHA. Capture counts and wall time per run. Do NOT edit tests to make the two runs agree. **COMMIT**
3. If either run does not complete, record WHICH limit was hit with its evidence, then bisect DOWN to the smallest shape that completes -- one measured descent, not repeated attempts at the same shape. **COMMIT**
4. Final: the end-of-lane artifact carries the four numbers, both wall times, the runner limits found, and the verdict. Targeted tests green. **COMMIT, then STOP.**

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
