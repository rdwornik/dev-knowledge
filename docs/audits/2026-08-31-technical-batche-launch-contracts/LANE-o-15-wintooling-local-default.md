# LANE batch-e-o-15-wintooling-local-default (HY-5) - CROSS-REPO (win-tooling): a new chat defaults to LOCAL PowerShell, not the cloud rung. RULING-W.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-o-15-wintooling-local-default LANE-o-15-wintooling-local-default.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-o-15-wintooling-local-default` -> branch `worktree-lane-o-15-wintooling-local-default` -> contract `LANE-o-15-wintooling-local-default.md`

## Write-scope (frozen)

**IN `win-tooling`, NOT IN THE HUB.** This lane's entire footprint is the win-tooling repo's own
configuration surface. **It writes NOTHING in `.dev-knowledge`.**

## THIS IS THE ONE CROSS-REPO LANE IN THE BATCH

Dispatch it against the win-tooling checkout, not the hub. Layer 2 never executes: the hub rules,
the consumer carries. A hub lane that edited win-tooling directly would violate ADR-28/ADR-36 -
so this lane RUNS IN win-tooling.

## Blocked by

**Nothing technically** - but note CUT-1 for context: win-tooling is the **FIRST INSTANTIATED**
consumer (the floor stays) and the **LAST** to receive the consolidated-doctrine migration. This
lane is neither of those things; it is a local default, and it is independent of the migration
order.

## Done-contract (immutable)

1. **A new chat in win-tooling defaults to LOCAL PowerShell, not the cloud rung** (RULING-W,
   operator verbatim).
2. **The default is DECLARED, not merely observed** - a reader can see where it is set and what
   overrides it.
3. **The cloud rung remains REACHABLE.** This changes the default, not the capability. Removing
   the cloud path would exceed the ruling.

## Steps

1. Locate the current default and the surface that sets it. Resolve it before changing it.
2. Flip the default; record the override path.
3. Run win-tooling's own suite. **Note: it carries ONE pre-existing environment RED that is not
   yours** - report it as pre-existing rather than chasing or claiming it.
4. Commit and STOP.

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
