# Governance Essences — ai-council audit-sync Handoff

Operational rules for ADRs cited in 07_ACTION_PLAN directives.
Format: 2-3 sentences + full ADR reference. Not full ADR copies.

---

## ADR-33 — VISION.md universalization

Any repo with ≥1 dependent MUST have VISION.md. Frontmatter required:
`version`, `tier` (S/M/L), `owner`, `last_reviewed`, `scale`. Required sections
for Lite tier (M): Mission, Scope, Relationships, Lifecycle. For ai-council,
tier M applies — use concise but complete sections; frontmatter mandatory.

Full ADR: `.dev-knowledge/docs/decisions/ADR-33_vision_universalization.md`

---

## ADR-35 — Lessons base activation

Cross-repo lessons retrieval via `DEV_KNOWLEDGE_PATH` env var. Each repo's
`CLAUDE.md` should reference this env var pointing to .dev-knowledge repo.
Repo-local lessons stay in repo (e.g., `tasks/lessons.md`). Cross-cutting
lessons go to `.dev-knowledge/LESSONS.md`. Full retrieval implementation is
BACKLOG P2 — for now, configuration documentation only (add reference to CLAUDE.md).

Full ADR: `.dev-knowledge/docs/decisions/ADR-35_lessons_base_activation.md`
