# Governance Essences

<!-- scope: meta -->

Operational essences for ADRs and Council decisions that drive actions in this handoff. These are 2-4 sentence summaries — not full ADR copies. Read the full ADR in `.dev-knowledge/docs/decisions/` if you need complete rationale.

---

## Council Decision #28 — AGENTS.md Mandate

`AGENTS.md` is the canonical cross-tool LLM agent governance file, covering Codex, Claude Code, Cursor, and Aider. It is distinct from `CLAUDE.md` (Claude-Code-specific); `AGENTS.md` is tool-agnostic and governs all LLM-driven development tooling. Every repo at Scale M or above must have `AGENTS.md` at root. `ai-council` currently has only `CLAUDE.md` — `AGENTS.md` is absent and must be created.

---

## ADR-38 — Universal Repo Architecture Baseline

**Status:** Accepted (2026-04-30, amended 2026-05-11)

Scale M mandatory files at repo root: `README.md`, `VISION.md` (Lite), `BACKLOG.md`. `CHANGELOG.md` was formerly mandatory for M+ but was superseded and removed by ADR-49 (2026-05-16). `ARCHITECTURE.md` is optional for Scale M, mandatory for Scale L, and must be placed at repo root (not in `docs/`) wherever present. `AGENTS.md`/`CLAUDE.md` per-repo updates are Phase 2 work, cross-referenced by Council #28.

---

## ADR-42 — Handoff Centralization (v3.0, thrice amended)

**Status:** Accepted (2026-05-09)

All handoffs for all repos are stored in `.dev-knowledge/docs/handoffs/{date}-{slug}/` — never in the target repo. The three-actor flow is: (1) Claude Code in `.dev-knowledge` generates Stage 1 question; (2) the EXISTING (old) browser chat for the repo provides Stage 2 architect response from lived context; (3) Claude Code generates the Stage 3 folder bundle; (4) a NEW browser chat for the repo receives the bundle and executes directives. Stage 2 cannot be skipped or substituted with audit findings for any handoff type.

---

## ADR-46 — Cross-Repo Dated Entries Format (DEMOTED)

**Status:** Demoted to non-enforced convention (2026-05-16, Council Simplification)

ADR-46 specified a 6-field format including `[scope: X]` tags for LESSONS.md entries. After Council Simplification 2026-05-16, enforcement was withdrawn: `validate_scope_tags.py` deleted, pre-commit hook removed. Scope tags remain as informal lightweight metadata — authors may use them when useful, but no automated check enforces them and existing entries without tags are not in violation. Backfilling scope tags into existing entries is advisory only.

---

## ADR-29 — LESSONS.md Grandfathering

**Status:** Accepted

LESSONS.md is append-only: existing entries must NEVER be edited, altered, or deleted. New entries follow the current format (including `[scope: X]` inline if using scope tags). Backfilling metadata into existing entries — including scope tags — requires that existing entry content be preserved exactly; the tag is an insertion, not a rewrite. If scope-tag backfill cannot be accomplished without altering existing entry text, do not backfill.

---

## ADR-48 — Trim Documentation Governance

**Status:** Accepted (2026-05-16)

Documentation governance is limited to structural checks (file presence, format compliance). Cosmetic consistency (header casing, whitespace, punctuation) is handled by the deterministic header-normalizer pre-commit hook, not by audit rules. New audit checks require a governance-admission justification. The intent is to reduce format-governance overhead while preserving signal-bearing structural checks.

---

## ADR-49 — Consolidate Past-Recording Files

**Status:** Accepted (2026-05-16)

`CHANGELOG.md` and `BACKLOG_ARCHIVE.md` have been removed from all repos. `CHANGELOG.md` is replaced by descriptive git commit messages (Conventional Commits) plus a `Changes:` line in each `JOURNAL.md` entry. Done backlog items simply leave `BACKLOG.md`; their trace is git history. Significant abandoned items are recorded as lightweight decision-notes in `docs/decisions/`, not as JOURNAL or BACKLOG tombstones. Net: four past-recording files (CHANGELOG, JOURNAL, BACKLOG_ARCHIVE, LESSONS) reduced to two (JOURNAL + LESSONS).
