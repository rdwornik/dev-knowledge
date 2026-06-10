===== FILE: 03_PROJECT — start =====

# 03 · The project — .dev-knowledge

## Vision

`.dev-knowledge` is a universal, portable LLM-driven development guide and methodology
framework — the ecosystem's **knowledge guardian and methodology author**. It absorbs
lessons from individual projects, universalizes them into patterns, and disseminates
those patterns back as enforceable conventions; it also **audits** child repos against
the universal governance baseline (ADR-38 A5; the repo-tier system was deprecated
2026-05-23). Think LLM-development Scrum Master: it doesn't write code, it ensures the
framework is applied consistently and evolves with experience. **Continuous improvement
is the baseline posture**, not an option — and the methodology self-enforces (the
Tier-1 lifecycle, ADR-70, holds this repo's own closure/lint/review to the same
enforced-not-remembered bar it imposes on what it governs).

## Scope

**In scope:** universal methodology + conventions for LLM-driven development;
cross-repo governance patterns (CLAUDE.md, ADRs, handoffs); knowledge consolidation
(lessons, decisions, processes); audit/verification mechanisms for child-repo compliance.

**Out of scope (the most common source of new-chat drift — keep it):**
- Code-level implementation in child repos
- Project-specific business logic, schemas, or domain knowledge (→ Obsidian vault)
- Operational data / runtime telemetry
- Replacement for a repo-specific CLAUDE.md or README
- Hierarchy or authority over child repos beyond methodology compliance

## Purpose & critical paths

- **Name:** `.dev-knowledge` · **Complexity:** medium (informal) · **Status:** active
- **Purpose:** universal LLM-driven development guide + methodology framework; governs
  all projects under `Dev/`; Layer 2 of the ADR-28 three-layer model.
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`,
  `ARCHITECTURE.md`.
- **Related:** `~/.claude/` (CC runtime config — out of scope here); `.claude/`
  (project config); `ObsidianVault/` (pre-sales, do not mix); `Dev/` (child repos,
  each owns its CLAUDE.md).

## Sacred files (do not break these)

- **`LESSONS.md`, `logs/TOKEN-LOG.md`** — append-only; never edit old entries (ADR-29/39).
- **`JOURNAL.md`** — append-only, newest-first prepend.
- **ADRs, transcripts, handoffs, audits** — immutable; supersede with a new file or
  in-file marker, never edit in place.
- **`VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md`** —
  living; update in place, carry `last_reviewed` where stamped.
- **`scripts/`** — read-only validators only (Layer 2 never executes — ADR-28/36).
- **`HANDOFF_PROCESS.md` is frozen this session** — generate *with* it; do not edit it
  until this handoff is reviewed (see `05_NOW` boundaries).

## Cross-repo ownership (ADR-41)

This bundle covers **.dev-knowledge only**. Never direct work on another repo from
here, never edit another repo's BACKLOG or files. `.dev-knowledge` is the methodology
meta-layer; child repos consume it and feed lessons back — **no authority hierarchy,
only functional roles**. Cross-repo work routes through dedicated artifacts (e.g. a CC
prompt or a Council debate), not this handoff.

===== FILE: 03_PROJECT — end =====
