<!-- scope: meta -->

# ADR-79 — Browser methodology carrier: bundle-only; Projects deferred

- **Status:** Accepted — 2026-06-07
- **Amends:** none
- **Related:** ADR-78 (child methodology floor, companion F2 ruling); BACKLOG #108, #25; HANDOFF_PROCESS.md
- **Decommission:** none
- **Source:** Council pick 2026-06-07, 3-of-4 panelists pivoted in R2; operator ratification = distillation prompt 2026-06-07. Transcript: `docs/decisions/transcripts/council-out-20260607_125247-pick-council-f1-browser-carrier.md`

## Context

Browser CC sessions (claude.ai) require methodology context to be uploaded at session start. The methodology transfer audit (2026-06-07) surfaced F1: the current per-session handoff bundle (5+ separate uploads) is ergonomically fragile, and the stable methodology layers (01_ROLE, 02_METHODOLOGY) change rarely. Two structural alternatives were evaluated:

- **O1 (bundle-only, status quo):** Continue uploading the handoff bundle at each session; improve ergonomics within this model.
- **O2 (Projects-as-carrier, prompt-governed):** Store 01_ROLE/02_METHODOLOGY in claude.ai Projects, rely on a prompt instruction to freshen the content when it drifts.
- **O3 (Projects-as-carrier, CI-governed):** Store layers in Projects, synchronize via a deterministic API/CI pipeline (no LLM involvement in the sync decision).

## Decision

**O1 — Bundle-only** is retained as the sole browser carrier. Projects (O2 and O3) are deferred.

**1 — O2 rejected (prompt-governed freshness).** An LLM executing a deterministic freshness check is an unverifiable safety property. "Prompt engineering as a security control" is a category error: the LLM may fail to detect drift, may detect it inconsistently across sessions, or may silently succeed while using stale content. Silent-wrong beats visible-friction only if the friction is unfixable — and the friction here is fixable (see Decision 2). The ownership-cadence drift risk named in BACKLOG #108 is not mitigated by a prompt instruction.

**2 — Mandated ergonomics fix (inside O1).** The friction that motivated O2 is addressed within the bundle-only model:
- Handoff generation outputs **one consolidated `BUNDLE.md`** (the current 5-file upload collapses to 1 file). This is a HANDOFF_PROCESS edit and generation-script change.
- `05_NOW` gains an **initialization acknowledgment clause**: the receiving LLM responds "Loaded methodology vX.X. Ready." at session start. A missing or partial upload is then **visible** (no acknowledgment = something was not loaded), turning an invisible failure mode into a detectable one.

**3 — O3 deferred (CI-governed Projects sync).** A deterministic API/CI path to sync-and-verify Projects content without LLM involvement would address the ownership-cadence drift risk and is architecturally sound. It is deferred because:
- The API/CI tooling to do this reliably does not exist in the current stack.
- The bundle-ergonomics fix (Decision 2) removes the immediate motivation.

**Revisit trigger:** O3 becomes the preferred path once a deterministic, LLM-independent sync-and-verify mechanism for claude.ai Projects content is available.

## Consequences

- BACKLOG #108 is closed: the evaluation is delivered; verdict = defer Projects, improve bundle ergonomics. Recorded here.
- A new implementation item is opened: consolidated `BUNDLE.md` output in handoff generation + `05_NOW` initialization-acknowledgment clause (HANDOFF_PROCESS edit + generation-script change). This is the friction fix that makes O1 viable long-term.
- The O2 rejection establishes a principle reusable elsewhere: LLM-executed freshness/sync checks are not verifiable safety properties — the same framing as ADR-75's "no organ = decoration" rule applied to the LLM layer.
- O3 has a clear re-entry condition: deterministic API/CI sync path, no LLM involvement.

## Alternatives considered

- **O2 (Projects + prompt-governed):** rejected — unverifiable safety property; LLM freshness checks fail silently; the ownership-cadence drift risk is unmitigated.
- **O3 (Projects + CI-governed):** deferred, not rejected — technically sound but depends on tooling that does not currently exist; revisit when the API/CI path is available.
- **Hybrid (Projects for stable layers + bundle for ephemeral):** rejected as a variant of O2 — the stable/ephemeral split requires the same unverifiable freshness judgment to know when stable content has drifted.
