# LANE batch-e-j-10-equilibrium-checkpoint-blind-spots (DM-6) - FILING ONLY - R3's checkpoint blind spots, routed per the decision tree.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-j-10-equilibrium-checkpoint-blind-spots LANE-j-10-equilibrium-checkpoint-blind-spots.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-j-10-equilibrium-checkpoint-blind-spots` -> branch `worktree-lane-j-10-equilibrium-checkpoint-blind-spots` -> contract `LANE-j-10-equilibrium-checkpoint-blind-spots.md`

## Write-scope (frozen)

- `tasks/`

`docs/audits/2026-08-30-technical-autonomy-decision-tree.md` is READ-ONLY input and is never
edited: audits are immutable.

## Done-contract (immutable)

1. **R3's checkpoint blind spots are filed per the decision tree's routing** - each leaf to the
   destination the tree already names, never to a new one.
2. **RECONCILE BEFORE BIRTH.** The tree routes 55 leaves and only 2 became rows, deliberately:
   *a gap parked behind a named trigger is routed; a gap birthed ahead of its blocker is a row
   that cannot be worked.* Amend an existing row or intake wherever one exists.
3. **Any row that IS born carries its trigger** and a `kill-candidates:` line, flush-left.
4. **FILING ONLY. No build.**

## Steps

1. Read the decision tree's routing for every R3 leaf before filing anything.
2. File by amendment where possible; birth only proven gaps.
3. Run `gen_task_tree.py --emit-source`. Commit and STOP.

## Decision budget

**V-2 - escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported in the end packet. A refuted premise PAUSEs with the fact
(Q10) - deviation-with-disclosure discharges the reporting duty, it does not authorise the
deviation.

## What NOT to do

- No merges, no pushes to `main` - commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (`protocols/STANDING_RULINGS.md` P-1), no index regeneration (Q1).
- No row births beyond what the done-contract names - reconcile-before-birth binds this batch.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
