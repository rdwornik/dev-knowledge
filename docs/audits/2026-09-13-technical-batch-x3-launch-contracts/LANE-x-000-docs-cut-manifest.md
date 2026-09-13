# LANE lane-x-000-docs-cut-manifest — Docs-cut manifest, proposal only and no cut: for ARCHITECTURE's prologue and table of contents, CLAUDE.md's prologue, ESSENTIALS and PLAYBOOK's prologue, report section, bytes and readers found

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-000-docs-cut-manifest LANE-x-000-docs-cut-manifest.md -Effort high -Model sonnet
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-x-000-docs-cut-manifest · lane-x-000-docs-cut-manifest]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`sonnet` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-000-docs-cut-manifest` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-x-000-docs-cut-manifest` -> branch `worktree-lane-x-000-docs-cut-manifest` -> contract `LANE-x-000-docs-cut-manifest.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. For each of ARCHITECTURE's prologue, ARCHITECTURE's table of contents, CLAUDE.md's prologue, ESSENTIALS, and PLAYBOOK's prologue: **section**, **bytes**, and **readers found** (who imports it, links to it, or reads it) -- MEASURED, not estimated.
2. `to-browser/DOCS-CUT-LIST-2026-09-13.md` is emitted as the third one-word GO list (AX28-2), each entry carrying its evidence.
3. **NOTHING IS CUT.** Proposal only. This lane's diff touches no governed doc body; if it did, the proposal would have pre-empted the decision it exists to inform.
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

1. Measure bytes per named section, from the files rather than from any prose that restates a size. **COMMIT**
2. Find READERS for each section -- importers, linkers, and boot-time readers. A section with no reader is the finding; a section whose readers you did not look for is not. **COMMIT**
3. Emit the docs-cut list to `to-browser/`, with the evidence per entry. **COMMIT**
4. Final: end-of-lane artifact; confirm the diff cut nothing. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Two facts that bound the measurement

- **`ESSENTIALS.md` is already SUPERSEDED, pending `[#628]`** (`CLAUDE.md` header). Its
  readers are therefore the interesting number: a superseded file with live readers is a
  different proposal from a superseded file with none.
- **`CLAUDE.md` is byte-capped at 24,576 B**, gated by `tests/test_claude_md_byte_cap.py`.
  Report its prologue's bytes against that cap, since headroom is what makes a cut decidable.
- **Never restate a count you did not compute** (`CLAUDE.md` section 4). Every number in the
  emitted list cites the surface that produced it.
