# 03 · Project

<!-- scope: meta -->

> What `.dev-knowledge` is. Identity, architecture, conventions —
> the standing context. Condensed from VISION + CLAUDE + ARCHITECTURE.

## Identity

`.dev-knowledge` is the **universal LLM-driven development guide and methodology framework** governing all projects under `Dev/`. It is **Layer 2** of the ADR-28 three-layer ecosystem model: Layer 1 = runtime config (`~/.claude/`), Layer 2 = methodology (this repo), Layer 3 = the working repos (corp-monorepo, ai-council, etc.).

## Architecture

- **Not a code project** — markdown governance files + methodology + lightweight read-only validators (`scripts/audit.py`, codemap generator). No orchestration.
- **Critical paths:** `protocols/`, `docs/decisions/` (ADRs), `templates/`, `VISION.md`, `ARCHITECTURE.md`.
- **Three-layer model (ADR-28):** this repo never executes against child repos; it publishes methodology they adopt.
- **Read ARCHITECTURE.md before any structural change** (required per ADR-51 as amended).

## Conventions that bite

- **UPPERCASE** top-level living docs; `ADR-NN-topic.md`; `YYYY-MM-DD-slug.md` for dated artifacts.
- **Append-only:** LESSONS, TOKEN-LOG, JOURNAL (newest-first prepend).
- **Immutable:** ADRs, transcripts, handoffs, audits — supersede, never edit.
- **No box-drawing chars** in summaries; plain markdown tables (token-cheap).
- **Validators run with explicit args** — never vacuous (`--all` or specific paths).
- **Do not recreate deleted files** — `README.md` (root), `CHANGELOG.md`, `BACKLOG_ARCHIVE.md` were deliberately removed.

---

**Source:** condensed from `VISION.md` + `CLAUDE.md` + `ARCHITECTURE.md` at handoff time.
