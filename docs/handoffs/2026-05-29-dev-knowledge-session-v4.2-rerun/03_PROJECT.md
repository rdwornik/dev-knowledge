# 03 · The project

## Vision

`.dev-knowledge` is a **universal LLM-driven development guide and methodology
framework**. It governs all projects under `Dev/` and is **Layer 2** of the ADR-28
three-layer ecosystem model: Layer 1 (browser chat = analysis/synthesis) → Layer 2
(`.dev-knowledge` = passive storage of methodology, patterns, decisions) → Layer 3
(child repos = execution). It is the ecosystem's **knowledge guardian, methodology
author, and auditor** — the "LLM-development Scrum Master." It does not write code;
it ensures the framework is applied consistently and evolves with experience.

**Continuous improvement is the baseline posture**, not an option. Sessions advance
the framework; static maintenance is the exception requiring explicit justification.

## Scope

**In scope:** universal methodology + conventions for LLM-driven dev; cross-repo
governance (CLAUDE.md, ADRs, handoffs); knowledge consolidation (lessons, decisions,
processes); audit/verification that child repos comply.

**Out of scope:** code-level implementation in child repos; project/domain/business
knowledge (→ Obsidian vault); runtime/operational data; replacing repo-specific
CLAUDE.md/README; any authority over child repos beyond methodology compliance.

## Cross-repo ownership (ADR-41)

A handoff bundle covers **only its own repo** and never directs work on another. If
you find a cross-repo issue (e.g. the corp-monorepo branch in `05`), **surface it to
Rob — do not act on it from here**. Cross-repo threads close via routing artifacts,
not the handoff. Child repos each own their own `CLAUDE.md`.

## Critical paths

`protocols/` · `docs/decisions/` (ADRs + transcripts) · `templates/` · `VISION.md` ·
`ARCHITECTURE.md` · `CLAUDE.md`. Read `ARCHITECTURE.md` before any structural change.

## Sacred files & lifecycle rules

| File(s) | Rule |
|---|---|
| `LESSONS.md`, `TOKEN-LOG.md` | **Append-only** — never edit old entries (ADR-29/39) |
| `JOURNAL.md` | **Append-only, newest-first prepend** |
| ADRs, transcripts, handoffs, audits | **Immutable** — supersede with a new file/amendment, never edit in place |
| `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` | **Living** — update in place |

**Do not recreate** deleted files: root `README.md` (deleted 2026-05-23),
`CHANGELOG.md` / `BACKLOG_ARCHIVE.md` (deleted 2026-05-16). The repo-tier system was
deprecated 2026-05-23 — no declared `tier:`/`scale:`; the universal governance
baseline (ADR-38 amendment A5) applies regardless of size.

## Special case — ai-council

`ai-council` is a **tool** `.dev-knowledge` uses to generate architectural
decisions. Council debate transcripts return to `docs/decisions/transcripts/`;
operational metrics stay in `ai-council/output/`.
