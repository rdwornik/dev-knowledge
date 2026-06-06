===== FILE: 03_PROJECT — start =====

# 03 · The project — .dev-knowledge

## Vision

`.dev-knowledge` is a universal, portable, machine-agnostic LLM-driven development
guide and methodology framework — the ecosystem's **knowledge guardian, methodology
author, auditor, and disseminator**. It absorbs lessons from individual projects,
universalizes them into enforced conventions, and audits the ecosystem against the
universal governance baseline (ADR-38 A5; repo-tier system retired 2026-05-23). It is
the LLM-development "scrum master": it doesn't write code, it ensures the framework is
applied consistently and **evolves with experience** — continuous improvement is the
baseline posture, not an option. The methodology now self-enforces (Tier-1 lifecycle,
ADR-70): it holds its own process to the enforced-not-remembered bar it imposes on the
artifacts it governs.

## Scope

**In scope:** universal methodology + conventions for LLM-driven development;
cross-repo governance patterns (CLAUDE.md, ADRs, handoffs); knowledge consolidation
(lessons, decisions, processes); judgment-calibrated guidance per project; audit /
verification mechanisms ensuring child repos comply.

**Out of scope (the most common source of new-chat drift — hold this line):**
code-level implementation in child repos · project-specific business logic, schemas,
domain knowledge · operational data / runtime telemetry · replacement for a repo's own
CLAUDE.md or README · any hierarchy or authority over child repos beyond methodology
compliance.

## Purpose & critical paths

- **Purpose:** Universal LLM-driven development guide; governs all `Dev/` projects;
  Layer 2 of the ADR-28 three-layer ecosystem model. **Status:** active.
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`,
  `ARCHITECTURE.md`.
- **Related locations:** `~/.claude/` (CC runtime config); `.claude/` (project config);
  `ObsidianVault/` (pre-sales — do NOT mix); `Dev/` child repos (each owns its CLAUDE.md).
- **NOT a code project** — markdown governance files + read-only validators only.

## Sacred files (do not break these)

- **`LESSONS.md`, `logs/TOKEN-LOG.md`** — append-only; never edit old entries (ADR-29/39).
- **`JOURNAL.md`** — append-only, newest-first prepend. Corrections are NEW entries.
- **ADRs, transcripts, handoffs, audits** — immutable; supersede with a new file, never
  edit in place. Synthetic-proof PRs (`2099-*`) are intentional, labeled, and stay.
- **`VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md`** —
  living; update in place, but living docs carry a `last_reviewed` stamp meaning
  genuinely re-read end-to-end, not merely touched (`audit.py` check #10 enforces it).
- **`scripts/`** — Layer-2 read-only validators only; never add orchestration that
  drives state in child repos.

## Cross-repo ownership (ADR-41)

This bundle covers **.dev-knowledge only**. Never direct work on another repo from
here, never edit another repo's BACKLOG or files. Cross-repo work routes through
dedicated artifacts, not this handoff. `.dev-knowledge` is the methodology meta-layer;
child repos consume it and feed lessons back — no authority hierarchy, only functional
roles. **Cloud doctrine = self-containment (ADR-72):** a cloud session sees ONLY the
cloned repo — no hub reference on a cloud executing path, ever.

===== FILE: 03_PROJECT — end =====
