# LANE batch-e-f-6-observability-otel (DM-2) - telemetry emits OTel GenAI events; the collector is pluggable. The verdict layer is UNCHANGED.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-f-6-observability-otel LANE-f-6-observability-otel.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-f-6-observability-otel` -> branch `worktree-lane-f-6-observability-otel` -> contract `LANE-f-6-observability-otel.md`

## Write-scope (frozen)

- `scripts/cost_usage_telemetry.py`
- `docs/audits/2026-08-31-technical-dm2-otel-genai-events.md`

## Blocked by

Tier (B)'s OTel GenAI event-schema draft.

## Done-contract (immutable)

1. **Telemetry emits OTel GenAI semantic-convention events.** Those conventions are already
   DISCHARGED in the decision tree - this consumes that verdict rather than re-deciding it.
2. **The collector is PLUGGABLE** - Phoenix or Langfuse, self-hosted. Both are DISCHARGED in the
   decision tree with their evidence; do not re-evaluate them, and do not hard-wire either.
3. **THE VERDICT LAYER IS UNCHANGED.** Trends -> rulings stays exactly as it is. This lane moves
   the emission format, not the judgment.
4. **No new dependency without an explicit ADR-106 gated act.** If the schema needs a package,
   STOP and report - a `uv.lock` change is its own decision, never a side effect.

## Steps

1. Read tier (B)'s schema draft and the cost-usage-telemetry audit before writing.
2. Emit the events; keep the collector behind a seam.
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
