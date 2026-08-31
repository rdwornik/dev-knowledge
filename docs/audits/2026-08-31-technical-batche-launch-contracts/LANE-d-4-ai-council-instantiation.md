# LANE batch-e-d-4-ai-council-instantiation (DC-5) - instantiate ai-council as consumer #2 from the win-tooling template - same engine, no bespoke path.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-d-4-ai-council-instantiation LANE-d-4-ai-council-instantiation.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-d-4-ai-council-instantiation` -> branch `worktree-lane-d-4-ai-council-instantiation` -> contract `LANE-d-4-ai-council-instantiation.md`

## Write-scope (frozen)

- `ecosystem/ai-council/`
- `ecosystem/deployed-versions.yaml`

## Blocked by

**DC-4 must be MERGED first** - the root contract is the shape a consumer is instantiated
against. If it has not merged, STOP and report; do not instantiate against a draft shape.

## Done-contract (immutable)

1. **ai-council is instantiated FROM THE WIN-TOOLING TEMPLATE.** Same engine, no bespoke path.
   Where the template does not cover a case, that gap is a **FINDING about the template** -
   report it. Hand-authoring around it is how a second engine gets born by accident.
2. **win-tooling's status as the FIRST INSTANTIATED consumer is AFFIRMED, not rolled back**
   (CUT-1). The floor stays; this lane depends on that precedent existing.
3. **No doctrine content ships here.** Instantiation only - the consolidated-doctrine migration
   is the DEPLOYMENT WAVE's act, in the ruled order.

## Steps

1. Read the win-tooling template and `ecosystem/satellite-onboarding-rulings.yaml` first.
2. Instantiate. Record every template gap as a finding rather than patching around it.
3. Run the TARGETED tests for this diff. Commit and STOP.

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
