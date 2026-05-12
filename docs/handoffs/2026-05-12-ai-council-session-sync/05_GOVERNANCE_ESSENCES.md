# Governance Essences — 2026-05-12-ai-council-session-sync

<!-- scope: meta -->

ADR essences for decisions explicitly cited in 07_ACTION_PLAN.md directives.
Full ADRs live in `ai-council/docs/decisions/`.

---

## ADR-01 — Synthesizer Selection

Default synthesizer is Gemini (non-participating, outside panel). Selection
history: Claude Opus → Sonnet (cost) → Gemini (reliability). A cost-optimization
principle emerged mid-session (2026-05-12) and is NOT YET CODIFIED: synthesizer
selection prefers the lowest-cost model that meets the quality rubric; Opus tier
is reserved as last resort. Step 6 (Phase 3) is the codification path via an
ADR-01 amendment, gated on Step 5 smoke test results.

Full ADR: `docs/decisions/ADR-01-synthesizer-selection.md`

---

## ADR-28 (PLAYBOOK Council #28) — AGENTS.md Canonical Governance

Every repo in Rob's ecosystem requires an `AGENTS.md` at root — the canonical
cross-tool governance file read by Claude Code, Codex, Cursor, Aider, and other
LLM agents. It covers repo-specific architecture, conventions, tools, binding ADRs,
gotchas, and do-NOTs. AGENTS.md does NOT repeat universal PLAYBOOK content — it
points to it. ai-council currently has CLAUDE.md but no AGENTS.md; this is a tracked
P3 gap (deferred, low urgency per architect judgment).

Full reference: `.dev-knowledge/protocols/PLAYBOOK.md` section "AGENTS.md — canonical per-repo governance contract"; template at `.dev-knowledge/templates/AGENTS-md-template.md`

---

## ADR-34 — File Naming Convention

Universal hyphen separator for all filenames and foldernames. `council-out-YYYYMMDD-HHMMSS-*.md`
for Council CLI output (migrated from `council_out_*` during this session). UPPERCASE for
living docs (BACKLOG.md, LESSONS.md, etc.). ADR prefix grandfathered. No `_TYPE_` segments
in filenames. Architect's own fresh violation (`SYNTHESIS-QUALITY-RUBRIC.md`) was caught and
corrected by scrum-master audit — convention is easy to slip; double-check during prompt drafting.

Full ADR: `docs/decisions/ADR-34-file-naming-convention.md` (in `.dev-knowledge`)
