# 03 · The project — `.dev-knowledge`

## Vision

`.dev-knowledge` is the ecosystem's **universal LLM-driven development guide and
methodology framework** — the knowledge guardian and methodology author. It absorbs
lessons from individual projects, universalizes them into patterns, and disseminates
those patterns back as **enforceable conventions**. It also audits: verifying correct
methodology implementation against the universal governance baseline (ADR-38 A5; the
repo-tier system was deprecated 2026-05-23). Think LLM-development Scrum Master — it
doesn't write code, it ensures the framework is applied consistently and evolves.

**Continuous improvement is the baseline posture, not an option.** The methodology now
**self-enforces**: it applies its own conventions to its own process — the Tier-1
lifecycle (ADR-70) holds session-boundary closure, lint, and review to the same
enforced-not-remembered bar it imposes on the artifacts it governs.

## Scope

**In scope:** universal methodology + conventions for LLM-driven development;
cross-repo governance patterns (CLAUDE.md, ADRs, handoffs); knowledge consolidation
(lessons, decisions, processes); universal methodology-appropriate guidance per
project (calibrated by judgment of repo complexity, not a tier); audit/verification
mechanisms ensuring child repos comply.

**Out of scope (the most common source of new-chat drift — hold this list):**
- Code-level implementation in child repos
- Project-specific business logic, schemas, or domain knowledge
- Operational data or runtime telemetry
- Replacement for repo-specific CLAUDE.md or README files
- Hierarchy or authority over child repos beyond methodology compliance

## Purpose & critical paths

- **Purpose:** Layer 2 of the ADR-28 three-layer ecosystem model; governs all repos
  under `Dev/`.
- **Status:** active. **Complexity:** medium (informal; no declared tier).
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`,
  `ARCHITECTURE.md`.
- **Related locations:** `~/.claude/` (Claude Code runtime config); `.claude/`
  (project config); `ObsidianVault/` (pre-sales — do not mix); `Dev/` (child repos,
  each owns its `CLAUDE.md`).

## Sacred files (do not break these)

- **`LESSONS.md`, `logs/TOKEN-LOG.md`** — *append-only*; editing old entries corrupts
  the institutional record (ADR-29/39). Only append.
- **`JOURNAL.md`** — *append-only, newest-first prepend*; one entry per session/workday.
- **ADRs, transcripts, handoffs, audits** — *immutable*; supersede with a new file or
  in-file amendment marker, never edit in place.
- **`VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `CONTRIBUTING`,
  `BACKLOG.md`** — *living*; update in place. The four canonical living docs carry a
  `last_reviewed` stamp meaning *re-read end-to-end and confirmed* — bump it only after
  a genuine review, not a drive-by edit (`audit.py` check #10 enforces).
- **`scripts/`** — *read-only validators only*; Layer 2 never executes (no orchestration
  driving child-repo state).

## Cross-repo ownership (ADR-41)

This bundle covers **`.dev-knowledge` only**. Never direct work on another repo from
here, never edit another repo's BACKLOG or files. Cross-repo work routes through
dedicated artifacts, not this handoff. `.dev-knowledge` is the methodology meta-layer;
child repos consume it and feed lessons back — **no authority hierarchy, only
functional roles.**
