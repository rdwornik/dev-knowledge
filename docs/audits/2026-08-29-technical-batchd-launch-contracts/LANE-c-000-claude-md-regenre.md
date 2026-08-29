# LANE lane-c-000-claude-md-regenre — Re-genre CLAUDE.md into a thin Claude-runtime boot contract, budgeted in BYTES with a gate.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-c-000-claude-md-regenre LANE-c-000-claude-md-regenre.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-c-000-claude-md-regenre · lane-c-000-claude-md-regenre]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-c-000-claude-md-regenre` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-c-000-claude-md-regenre` -> branch `worktree-lane-c-000-claude-md-regenre` -> contract `LANE-c-000-claude-md-regenre.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

`CLAUDE.md` · `.claude/generated/**`

**BLOCKED BY lane-b**, which edits §5 rule 5 first. Do not start until lane-b has merged.

## Done-contract (immutable)

1. **CLAUDE.md is budgeted in BYTES, with a gate** reusing the byte-cap test PATTERN that already
   guards `AGENTS.md` in `tests/` — the pattern is the reusable artifact; the row that produced it
   is closed and is deliberately not cited as dispatchable work. The chosen byte ceiling is
   recorded in the packet as a number.
2. **Baseline, witnessed by `wc -l CLAUDE.md && wc -c CLAUDE.md` at freeze: 240 physical lines /
   39,147 B**, against a header claiming
   *"<=200 lines"* and a §12 claiming *"196/200, headroom 4"*. **Lines are the gamed proxy; bytes
   are the hard metric** — the file satisfies the line count by density while the real boot cost,
   paid every session, is unbudgeted.
3. **Every removal is a RELOCATION with a named destination.** Nothing deleted without a home;
   the operator's no-deletion rule binds.
4. **SCOPE IS THE RE-GENRE ONLY (architect CUT-1).** The ROOT-CONTRACT amendment to intake #38 is
   an INTEGRATOR act in this batch's filing pass and is **NOT** folded into this lane.
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

1. Establish the byte budget and land the gate that enforces it. **COMMIT**
2. Re-genre the file: a thin Claude-runtime boot contract, every removal relocated to a named
   destination. **COMMIT**
3. Final: targeted tests green, one end-of-lane artifact recording before/after BYTES, **COMMIT,
   then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
