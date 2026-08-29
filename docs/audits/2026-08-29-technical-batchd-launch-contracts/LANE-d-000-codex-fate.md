# LANE lane-d-000-codex-fate — Resolve the single-file codex/ folder by universalizing or deleting it, re-pointing every inbound reference.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-d-000-codex-fate LANE-d-000-codex-fate.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-d-000-codex-fate · lane-d-000-codex-fate]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-d-000-codex-fate` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-d-000-codex-fate` -> branch `worktree-lane-d-000-codex-fate` -> contract `LANE-d-000-codex-fate.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

`codex/**` · `protocols/PLAYBOOK.md` (the single citing line only)

**SUBSTRATE CORRECTION — architect CUT-4, recorded rather than quietly changed.** An earlier draft
routed this lane to copilot-enterprise. That was wrong: **writing the tree is PRODUCER work, and
producer on copilot is SDA-1-gated and NOT admitted** — the same ruling that draft cited two
sections later. Substrate is a **CC local worktree**. `copilot-sonnet-5` may serve as a *thinking
aid inside* the lane (reference-mapping, draft text) but **every tree write is CC's**. Batch-wide:
no copilot lane touches the tree until an SDA-1 producer admission row exists for it (none does
today — see `tasks/` for the absence).

## Done-contract (immutable)

1. **`codex/` is gone either way** — universalized or deleted. It holds exactly one file
   (`codex/AGENTS.md`, 3,891 B) and the operator's ruling is that single-file folders do not
   survive.
2. **Every inbound reference re-points.** Specifically PLAYBOOK's cite of `codex/AGENTS.md` as the
   canonical source for `~/.codex/AGENTS.md` (ADR-54): that edge survives or is re-homed, and is
   not allowed to dangle.
3. **Ratchet read before AND after via
   `python -c "import sys;sys.path.insert(0,'scripts');import silent_rule_detector as s;from pathlib import Path;print(s.measure(Path('.')).count)"`**,
   both numbers in the packet. Baseline **443 with ZERO
   headroom**, so new prose in `protocols/**` is authored token-free (no added `must` / `shall` /
   `never`) or the commit is refused.
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

1. Map every inbound reference to `codex/`, and decide universalize-vs-delete on that map.
   **COMMIT**
2. Execute the decision and re-point every reference. **COMMIT**
3. Final: targeted tests green, ratchet before/after recorded, one end-of-lane artifact,
   **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
