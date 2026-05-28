# archive/ — Pending-Classification Zone

Per ADR-60 amendment 2026-05-27.

Holding zone for artifacts whose destination isn't yet decided. Reviewed periodically; each item is either:

- deleted (git history retains it), or
- promoted to `decisions/`, `audits/`, `handoffs/`, `diagrams/`, or authored into an ADR.

Not a dumping ground — a triage queue. If something sits here across two reviews with no decision, default to deletion.

## Current contents (newest first)

Reclassified from `research/` and `council-questions/` during the 2026-05-27 taxonomy-simplification session (the two retired folders' content matures or archives — these did neither).

- `2026-05-25-handoff-failures-evidence.md` — empirical evidence cited by the 5 handoff-methodology Council questions
- `2026-05-25-handoff-methodology-council-index.md` — set index for the same Council question set
- `2026-05-17-kimi-k2-scoping.md` — Kimi K2 model scoping (BACKLOG #243; awaiting promotion to ADR or audit)
- `2026-04-27-handoff-patterns-external-research.md` — external research on handoff patterns
- `2026-04-27-handoff-patterns-council-research.md` — Council research debate on handoff patterns
- `2026-04-24-multi-agent-debate-patterns.md` — multi-agent debate frameworks research
- `2026-04-24-council-29-spec-kit-kiro.md` — Council debate #29: Spec Kit / Kiro evaluation
- `2026-04-24-claude-md-best-practices.md` — CLAUDE.md structuring research
- `2026-04-23-llm-dev-patterns-2026.md` — general LLM dev patterns research
- `2026-04-23-council-28-community-patterns.md` — Council debate #28: community LLM dev patterns
- `2026-04-15-council-26-tach-adoption-corp-monorepo.md` — Council debate #26: Tach adoption for corp-monorepo
- `2026-03-30-council-25-diagrams-corp-monorepo.md` — Council debate #25: diagram format for corp-monorepo
- `2026-03-29-council-research-new-models.md` — Council research on new LLM models/APIs
- `2026-03-29-council-browser-handoff.md` — browser-chat handoff patterns research

## Naming convention

`YYYY-MM-DD-{descriptive-slug}.md` — same as the live `docs/` folders, so a file's date is visible on archive too.

## How to review

1. Open the file. Skim for what's still actionable.
2. If actionable → `git mv` to the correct live folder (preserves history).
3. If superseded / one-shot value already extracted → `git rm`.
4. If still genuinely "don't know" after two passes → `git rm` (the periodic-review threshold).

The full archive lifecycle is in `protocols/PLAYBOOK.md` "docs/ folder taxonomy".
