# 03 · The project — `.dev-knowledge`

## Vision

`.dev-knowledge` is a universal, portable, machine-agnostic LLM-driven development guide
and methodology framework — the ecosystem's **knowledge guardian and methodology
author**. It absorbs lessons from individual projects, universalizes them into patterns,
disseminates them back as enforceable conventions, and **audits** the ecosystem against
the universal governance baseline (ADR-38 A5; the repo-tier system was retired
2026-05-23). Think "LLM-development Scrum Master for the ecosystem" — it does **not**
write code; it ensures the framework is applied consistently and evolves with experience.

**Continuous improvement is the baseline posture, not an option.** The methodology now
**self-enforces** — it applies its own conventions to its own process (the ADR-70 Tier-1
lifecycle holds session-boundary closure, lint, and review to the same enforced-not-
remembered bar it imposes on the artifacts it governs). Current strategic emphasis:
velocity in LLM-tech adoption, cross-repo methodology consistency, methodology evolution
as obsession, lessons-capture as default. (Optional Phase-D emphasis to name:
model-routing efficiency.)

## Scope

**In scope:** universal methodology + conventions for LLM-driven development; cross-repo
governance patterns (CLAUDE.md, ADRs, handoffs); knowledge consolidation (lessons,
decisions, processes); universal methodology-appropriate guidance per project; audit +
verification mechanisms ensuring child-repo compliance.

**Out of scope (the most common source of new-chat drift — keep it straight):**
code-level implementation in child repos · project-specific business logic / schemas /
domain knowledge · operational data or runtime telemetry · replacement for a repo's own
CLAUDE.md/README · any **hierarchy or authority** over child repos beyond methodology
compliance.

## Purpose & critical paths

- **Purpose:** Layer 2 of the ADR-28 three-layer ecosystem model — the methodology
  meta-layer governing all projects under `Dev/`. **Status:** active. NOT a code project
  — markdown governance files + read-only validators only; **Layer 2 never executes**
  (no orchestration scripts; `scripts/` holds read-only validators).
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`,
  `ARCHITECTURE.md`, `CLAUDE.md`.
- **Related locations:** `~/.claude/` (Claude Code runtime config + executable rules);
  `.claude/` (project config — `commands/`, `rules/`, `settings.json`, `workflows/`);
  `ObsidianVault/` (pre-sales — do not mix); `Dev/` child repos (each owns its CLAUDE.md).

## Sacred files (do not break these)

- **Append-only:** `LESSONS.md` + `logs/TOKEN-LOG.md` (never edit old entries — only
  append; editing corrupts the institutional record). `JOURNAL.md` (append-only,
  **newest-first prepend**).
- **Immutable:** ADRs, Council transcripts, handoff bundles, audits — supersede with a
  new file or in-file marker; never edit in place.
- **Living (update in place):** `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`,
  `protocols/*.md`, `BACKLOG.md`. The four canonical living docs carry a `last_reviewed`
  stamp meaning *re-read end-to-end and confirmed accurate* — bump it only after a
  genuine review (`audit.py` check #10 fails an edited-but-not-re-reviewed stamp).
- **Do not recreate:** root `README.md`, `CHANGELOG.md`, `BACKLOG_ARCHIVE.md`,
  `AGENTS.md` — all deliberately deleted/retired.

## Cross-repo ownership (ADR-41)

This bundle covers **`.dev-knowledge` only**. Never direct work on another repo from
here, never edit another repo's BACKLOG or files. `.dev-knowledge` is the methodology
meta-layer; child repos consume it and feed lessons back — **no authority hierarchy,
only functional roles**. (The graphify pilot ran ON corp-monorepo; its REJECT verdict
and report live on *that* repo's `main` — referenced here, not owned here.)
