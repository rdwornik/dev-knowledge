# LANE batch-e-e-5-eval-sda1-harbor (DM-1) - one SDA-1 pack in Harbor task/trial/verifier format, run once, compared against the hand-rolled run.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-e-5-eval-sda1-harbor LANE-e-5-eval-sda1-harbor.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-e-5-eval-sda1-harbor` -> branch `worktree-lane-e-5-eval-sda1-harbor` -> contract `LANE-e-5-eval-sda1-harbor.md`

## Write-scope (frozen)

- `docs/audits/2026-08-31-technical-dm1-eval-comparison.md`

## Blocked by

Tier (B)'s SDA-1-to-Harbor translation draft. Without it this lane has no input.

## Done-contract (immutable)

1. **One SDA-1 pack expressed in Harbor task/trial/verifier format**, run **once**, with its
   results compared to the hand-rolled run side by side.
2. **THIS IS NOT A HARBOR ADOPTION.** The decision tree PARKS Harbor on the trigger *"a second
   executor is admitted"* - and none is. A text translation plus one comparison run is the whole
   scope. If the work starts to look like admitting a dependency, **STOP**: that is ADR-112
   Tier L and a different bar entirely.
3. **The comparison reports what the format bought AND what it cost.** A translation that
   reports only upside has not been evaluated.

## Steps

1. Read tier (B)'s draft and the decision tree's Harbor parking before starting.
2. Translate, run once, compare. Record the delta honestly.
3. Commit the comparison artifact and STOP.

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
