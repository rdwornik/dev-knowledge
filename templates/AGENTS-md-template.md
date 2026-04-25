# AGENTS.md

> **Canonical governance contract for this repo.** Cross-tool standard — read by Claude Code, Codex, Cursor, Aider, and any other LLM-based agent operating here. LLMs advise; hooks/tests enforce.
>
> **Template version:** 2026-04-24 — see `.dev-knowledge/templates/AGENTS-md-template.md` for source.

## 1. Read first

Before doing anything in this repo, read:
- `<absolute path>/.dev-knowledge/ESSENTIALS.md` — Rob's daily working style + protocols
- `<absolute path>/.dev-knowledge/PLAYBOOK.md` — universal rules: prompt format, file types, Council lifecycle, etc.

This AGENTS.md covers **only** what's specific to this repo. Universal rules live in `.dev-knowledge/`.

If `.dev-knowledge/` is unavailable, proceed with this AGENTS.md alone but flag missing-universal-rules in session output.

## 2. Repo identity

- **Name:** `<repo-name>`
- **Scale tier:** `<S | M | L>` (per `.dev-knowledge/PLAYBOOK.md` Project Scale Tiers section)
- **Purpose:** `<one sentence: what problem does this repo solve>`
- **Status:** `<active | maintenance | archived>`
- **Owner:** `<Rob | other>`
- **Critical paths:** `<paths that should rarely change, e.g. src/<namespace>/, tests/, ARCHITECTURE.md>`

## 3. Architecture

`<2-5 sentences describing the layer/module structure. Reference docs/ARCHITECTURE.md if exists for deeper detail.>`

**Key dependencies:**
- `<dep 1 + why>`
- `<dep 2 + why>`

**Enforcement (what's mechanically guarded):**
- `<e.g. Tach: 4-layer taxonomy foundation/core/orchestration/interface — see tach.toml>`
- `<e.g. pre-commit hooks: validate_scope_tags.py, ruff format-on-save>`
- `<e.g. CI/CD: pytest must pass before merge>`

**Advisory (LLM should respect but not enforced by tooling):**
- `<e.g. dataclasses over dicts>`
- `<e.g. clean architecture: single-responsibility modules>`

## 4. Conventions

**Filenames:**
- `<pattern, e.g. snake_case for Python, kebab-case for markdown except ADRs>`

**Branches:**
- `<pattern, e.g. feat/<topic>, fix/<issue>, chore/<scope>>`

**Commits:**
- `<format, e.g. Conventional Commits — feat: / fix: / docs: / chore: / refactor:>`
- `<scope hint, e.g. always include affected module: feat(auth):>`

**Testing:**
- `<test framework, e.g. pytest>`
- `<minimum coverage, e.g. ≥80% for src/, no untested public API>`
- `<test command, e.g. pytest -x --tb=short>`

**Linting:**
- `<linter, e.g. ruff check src/ tests/ --fix>`

## 5. Tools active in this repo

**Code review:**
- `<e.g. Codex (OpenAI) — mode: full review, severity: P0/P1/P2/P3, threshold: 3+ files for /review>`
- For full Codex review configuration (severity tiers, review modes, output format), see `.dev-knowledge/templates/codex-review-config-template.md` — embed relevant Scale tier section here.

**Architecture enforcement:**
- `<e.g. Tach — see tach.toml, layer rules>`

**Pre-commit hooks:**
- `<e.g. ruff format, scope tag validator (.dev-knowledge only)>`

**Other:**
- `<e.g. ccusage for token tracking, see .dev-knowledge/ENVIRONMENT.md>`

## 6. Things this repo gets wrong (gotchas)

**Skill location:** `.claude/skills/gotchas/SKILL.md`

Read the gotchas skill before making changes. Common patterns this repo has stumbled on:
- `<one-liner per gotcha, with link to skill entry>`
- `<add as discovered>`

## 7. Council decisions binding here

ADRs in `docs/decisions/`. Active list (one-liner each):

- ADR-NN: `<topic — one sentence summary>`
- ADR-NN: `<topic — one sentence summary>`

Reference `docs/decisions/README.md` for full index. Council debate transcripts in `docs/decisions/transcripts/`.

## 8. Out of scope

Things that explicitly do NOT belong in this repo:
- `<e.g. client-specific data — goes to Obsidian vault>`
- `<e.g. dev methodology — goes to .dev-knowledge>`
- `<e.g. AI Council outputs — go to ai-council/output/ then archived per PLAYBOOK 5.N>`

## 9. Session start checklist

When starting a Claude Code session here, check:

1. `git status` — clean working tree?
2. `git log --oneline -5` — recent context
3. Read JOURNAL.md (if exists per Scale) — last 5 entries
4. Read most recent `docs/handoffs/*.md` (if continuing prior session)
5. `python -m pytest --collect-only` — test discovery works (sanity)
6. Run any repo-specific health check `<e.g. corp doctor, ai-council --healthcheck>`

If any check fails → stop and ask Rob before proceeding.

## 10. Do NOT

Things tried and explicitly rejected (with rationale):

- **`<rejected pattern>`** — `<why rejected, when, link to ADR if applicable>`
- `<add as decisions are made>`

Anti-patterns specific to this repo:
- `<e.g. inline imports inside functions — caught by import linter>`
- `<add as gotchas accumulate>`

---

**Last updated:** `<YYYY-MM-DD>`
**Maintained by:** `<Rob | other>`
