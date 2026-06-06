<!-- scope: meta -->

# ADR-76 — Local fleet-baseline host: Windows Task Scheduler → python directly

- **Status:** Accepted — 2026-06-06
- **Amends:** ADR-74 (matrix OPEN row: mechanism resolved — Desktop scheduler → Task Scheduler → `python scripts/fleet_health.py` directly)
- **Related:** ADR-68, ADR-72, ADR-73; BACKLOG #85
- **Decommission:** none
- **Source:** AI Council debate 2026-06-06, transcript `docs/decisions/transcripts/council-out-20260606_172555-pick-council-local-scheduled-tier.md` (4-model panel: claude-opus-4-7, deepseek-v4-pro, gemini-3.1-pro-preview, grok-4.3; openai synthesizer, non-participant; 2 rounds; pick-mode); operator paste-consent 2026-06-06.

## Context

ADR-74 ratified that the recurring fleet-baseline run belongs on a LOCAL scheduler (structural advantage: only local sessions see sibling repos). ADR-74's OPEN row left the mechanism unresolved: the original candidate was "Desktop scheduler" (Claude Desktop app's built-in scheduling), but the operator does not use Claude Desktop on Windows — this candidate was falsified before the Council debate was convened.

Three live questions were put to the Council:

- **Q1 (host mechanism):** Which local scheduler should own the recurring fleet-baseline run — Windows Task Scheduler, `/loop`/`CronCreate`, or other?
- **Q2 (LLM on scheduled path):** Should `claude -p` be invoked directly in the scheduled task, attaching an LLM to every run?
- **Q3 (missed-run):** How should missed runs (lid-closed sleep, off-hours) be handled?

## Decision

The Council verdict (synthesis: Adopt **1B + 2B + 3B**) is accepted verbatim.

### 1. Host mechanism — Windows Task Scheduler → `python scripts/fleet_health.py` directly (1B)

**Windows Task Scheduler** is the host for the recurring fleet-baseline run.

The scheduled task invokes `python scripts/fleet_health.py` directly — no `claude -p` wrapper, no LLM on the scheduled path. Fleet health data is collected by the Python script alone.

The Task Scheduler task configuration is version-controlled in `scripts/setup-fleet-scheduler.ps1` (optional companion XML export); no manual GUI-only setup.

### 2. LLM on scheduled path — deferred to next interactive SessionStart (2B-deferred)

Attaching an LLM to the scheduled run is **not adopted** for the initial implementation.

If LLM interpretation of the baseline data is needed, it is attached at the **next interactive SessionStart** via the existing SessionStart-throttled `fleet_health.py` trigger — already live (ADR-74). The scheduled task produces data; the interactive session consumes it with LLM context if warranted.

Rationale (from synthesis): in-session scheduling (`/loop`, `CronCreate`) is **structurally incompatible** with the required workflow — tasks are session-scoped and the methodology mandates frequent fresh sessions and `/clear`; a session-scoped scheduler cannot persist across session boundaries. `/loop`/`CronCreate` are disqualified for any persistence-needing job; this confirms and extends the REJECTED row in ADR-74.

### 3. Missed-run handling — Scheduler built-in catch-up, no wake (3B)

Task Scheduler's built-in **"run as soon as possible after a missed start"** setting is enabled. No wake-from-sleep trigger; no alerting. Stale or missed baseline data is surfaced at the next interactive SessionStart.

This is consistent with ADR-74 rider R2: missed nights are tolerated by design — fail-soft + catch-up + SessionStart surfacing is the accepted degradation path.

### 4. Config version-controlled

The Task Scheduler configuration is maintained in `scripts/setup-fleet-scheduler.ps1` (idempotent, re-runnable) with an optional exported XML alongside it. No undocumented manual-only setup.

### 5. SessionStart-throttled trigger overlap

The existing SessionStart-throttled `fleet_health.py` invocation (ADR-74) remains active during the validation period and is removed once the scheduled task is confirmed reliable at n=1 (the current gate). Both paths are non-destructive and non-conflicting.

## Consequences

- The ADR-74 OPEN row mechanism is resolved: `Desktop scheduler → fleet baseline (#85)` → `Task Scheduler → python scripts/fleet_health.py`.
- `/loop`/`CronCreate` disqualification is formally recorded as a doctrine corollary, not just a REJECTED row.
- Implementation is gated at n=1 per ADR-74 rider; this ADR records the mechanism but does not constitute the gate run.
- BACKLOG #85 is updated to reference this ADR and replace the stale Desktop-scheduler mechanism text.

## Alternatives considered

The following alternatives from the Council debate were rejected:

**Option A — Silent skip (no scheduled host; rely on SessionStart only):** Rejected. SessionStart-throttled `fleet_health.py` is best-effort and session-triggered; it cannot guarantee a daily baseline independent of the operator's session frequency. Structural cross-repo Tier-2 requires an autonomous trigger.

**Option C — `claude -p` on the scheduled path (LLM every run):** Rejected. Adds LLM cost, latency, and authentication complexity to a data-collection step that Python handles deterministically. LLM judgment deferred to the interactive SessionStart where context is available.

**Option D — Surface-only (no scheduled script; only surface stale data at SessionStart):** Rejected. Surface-only provides no autonomous data collection; the baseline becomes stale between interactive sessions. The Tier-2 structural advantage (cross-repo visibility) requires an autonomous local run, not just surfacing.

**`/loop`/`CronCreate` as host:** Disqualified. Session-scoped lifetime + 7-day resume window collide structurally with the mandatory `/clear`/fresh-session cadence; the session ends, the scheduler dies. Confirmed by Council; extends ADR-74's REJECTED row.
