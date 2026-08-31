# LANE batch-e-c-3-root-contract (DC-4) - the hub root's canonical clean shape (file set, ordering, workspace). Intake #38, and it lands BEFORE the first consumer deploy.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-c-3-root-contract LANE-c-3-root-contract.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-c-3-root-contract` -> branch `worktree-lane-c-3-root-contract` -> contract `LANE-c-3-root-contract.md`

## Write-scope (frozen)

- `docs/intake/2026-08-17-tech-fleet-config-standardization.md`
- `.dev-knowledge.code-workspace`

## Done-contract (immutable)

1. **The hub root's canonical clean shape is stated as a CONTRACT** - permitted file set,
   ordering, workspace declaration - per intake #38's ROOT-CONTRACT amendment of 2026-08-29.
2. **It lands BEFORE the first consumer deploy.** This is the surface that deploys; shipping a
   consumer against an unstated root shape ships the ambiguity.
3. **R18 stays PARKED on tested conditions, not on silence** - carry the parking forward
   explicitly rather than letting it lapse by omission.
4. **No consumer repo is touched here.** The hub states the contract; the DEPLOYMENT WAVE
   carries it, in CUT-1's ruled order.

## Steps

1. `/preflight` intake #38 and its 2026-08-30 amendment before acting on either.
2. State the contract. Reconcile against ADR-101's tree seal - it must not contradict the
   hermetization allowlist.
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
