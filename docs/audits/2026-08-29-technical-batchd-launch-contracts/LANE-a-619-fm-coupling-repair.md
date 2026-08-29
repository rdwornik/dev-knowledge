# LANE lane-a-619-fm-coupling-repair — Repair the dead FM-2 to FM-4 funnel-health coupling by ruling the derivation mapping, and turn its row-owned RED green.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-a-619-fm-coupling-repair LANE-a-619-fm-coupling-repair.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #619 · lane-a-619-fm-coupling-repair]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `opus`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-a-619-fm-coupling-repair` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-a-619-fm-coupling-repair` -> branch `worktree-lane-a-619-fm-coupling-repair` -> contract `LANE-a-619-fm-coupling-repair.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

`scripts/gen_handoff.py` · `scripts/funnel_lifecycle.py` · `scripts/governance_health.py` · `tests/**`

Disjoint from lane-b's script footprint (`canonical_docs.py`, `validate_hermetization.py`,
`audit_checks/check_adr38_baseline.py`) — verified at freeze through the [#591] validator.

## Done-contract (immutable)

1. **The derivation mapping is RULED and recorded before any code changes.** Each of the six
   `_FUNNEL_FIELDS` entries either renders a number derived from `funnel_lifecycle.Measurement`
   (live surface: `detector, live_intakes, archived_intakes, live_adrs, rows, post_cutoff_rows,
   ready_intakes, threshold_days, threshold_locator, violations, by_leg`) **or** is REMOVED from
   `_FUNNEL_FIELDS` by a ruling recorded in this lane's packet. **No field is left rendering
   `unavailable` by default.** `[#619]` (*"The FM-2 to FM-4 funnel-health coupling is dead — six fields, zero overlap"*)
   deliberately proposes no mapping: choosing it is this
   lane's first ruled act, and a guessed mapping is the failure the row exists to prevent.
2. **A test fails if the two surfaces drift apart again** — the zero-intersection state cannot be
   silently re-reachable. Starting state, witnessed by
   `python -c "import sys;sys.path.insert(0,'scripts');import gen_handoff as g;import funnel_lifecycle as f;print([a for _,a in g._FUNNEL_FIELDS]);print([x for x in dir(f.Measurement) if not x.startswith('_')])"`:
   six attributes read, eleven exposed, **intersection EMPTY**.
3. **`tests/test_governance_health.py::test_shared_fields_equal_fm4_block_byte_for_byte` is
   GREEN.** **OWNERSHIP, per architect CUT-3:** this is a pre-existing RED and the standing rule
   bars *unowned* drive-by repairs. `[#619]` owns this RED, so a row-owned RED fixed by the row's
   own lane is the designed path. Repair no other RED.
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

1. Read the live surfaces and **rule the mapping**, recording the reasoning field by field.
   Removal is a legitimate outcome for any field with no honest derivation. **COMMIT**
2. Implement the mapping, add the anti-drift test, turn the owned RED green. **COMMIT**
3. Final: targeted tests green, one end-of-lane artifact (what changed · the ruled mapping with
   its per-field reasoning · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
