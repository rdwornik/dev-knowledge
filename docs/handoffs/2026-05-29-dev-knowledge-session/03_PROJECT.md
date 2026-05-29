# 03 · The project — `.dev-knowledge`

## Vision

`.dev-knowledge` is a **universal LLM-driven development guide and methodology
framework** — portable, self-contained, machine-agnostic. It is the ecosystem's
**knowledge guardian and methodology author**: it absorbs lessons from individual
projects, universalizes them into patterns, and disseminates those patterns back as
enforceable conventions. It is also **auditor** — verifying methodology compliance
against the universal governance baseline (ADR-38 amendment A5; the repo-tier system
was deprecated 2026-05-23). Think of it as the **LLM-development Scrum Master** for
the ecosystem: it doesn't write code, it ensures the framework is applied
consistently and evolves with experience. **Continuous improvement is the baseline
posture, not an option.**

Current strategic emphasis: velocity in LLM-tech adoption · cross-repo methodology
consistency (**drift detected proactively**) · methodology evolution as obsession ·
lessons capture as default.

## Scope

**In scope:** universal methodology + conventions for LLM-driven development;
cross-repo governance patterns (CLAUDE.md, ADRs, handoffs); knowledge consolidation
(lessons, decisions, processes); judgment-calibrated guidance per repo; audit /
verification mechanisms.

**Out of scope (the most common source of new-chat drift — respect it):**
- Code-level implementation in child repos
- Project-specific business logic, schemas, or domain knowledge
- Operational data or runtime telemetry
- Replacement for repo-specific CLAUDE.md / README
- **Hierarchy or authority over child repos** beyond methodology compliance

## Purpose & critical paths

- **Purpose:** Layer 2 of the ADR-28 three-layer ecosystem model; governs all
  projects under `Dev/`. NOT a code project — markdown governance files + read-only
  validators only.
- **Status:** active. Complexity: medium (informal; no declared tier).
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`,
  `ARCHITECTURE.md`.
- **Related locations:** `~/.claude/` (Claude Code runtime config — separate
  ownership); `.claude/` (project config); `ObsidianVault/` (pre-sales — never mix);
  `Dev/` (child repos, each owns its own CLAUDE.md).

## Sacred files (do not break these)

- **`LESSONS.md`, `TOKEN-LOG.md`** — append-only; *never* edit old entries
  (ADR-29/39). Editing corrupts the institutional record.
- **`JOURNAL.md`** — append-only, **newest-first prepend**.
- **ADRs, transcripts, handoffs, audits** — immutable; supersede with a new file or
  an in-file marker. Never edit in place (ADR-39).
- **`VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md`** —
  living; update in place, keep ESSENTIALS↔PLAYBOOK aligned (divergence is the
  failure mode).
- **`scripts/`** — read-only validators only (Layer-2 invariant). Never add
  orchestration.
- Do **not** recreate deleted files: `README.md` (root), `CHANGELOG.md`,
  `BACKLOG_ARCHIVE.md`.

## Cross-repo ownership (ADR-41)

This bundle covers **`.dev-knowledge` only**. Never direct work on another repo from
here, never edit another repo's BACKLOG or files. Cross-repo work routes through
dedicated artifacts, not this handoff. `.dev-knowledge` is the methodology
meta-layer; child repos consume it and feed lessons back — **no authority hierarchy,
only functional roles.** (Reading another repo's state read-only to resolve an
unknown is fine — and encouraged over passing forward "unknown" — but writing is
not.)
