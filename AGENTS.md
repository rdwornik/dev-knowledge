# AGENTS.md

> **Canonical governance contract for this repo.** Cross-tool standard — read by Claude Code, Codex, Cursor, Aider, and any other LLM-based agent operating here. LLMs advise; hooks/tests enforce.
>
> **Template version:** 2026-04-24 — see `templates/AGENTS-md-template.md` for source.

## 1. Read first

Before doing anything in this repo, read:
- `protocols/ESSENTIALS.md` — daily working style, roles, epistemic discipline
- `protocols/PLAYBOOK.md` — universal rules: prompt format, Council lifecycle, file types, scale tiers

This AGENTS.md covers **only** what's specific to `.dev-knowledge`. Universal rules live in ESSENTIALS and PLAYBOOK.

If those files are unavailable, proceed with this AGENTS.md alone but flag missing-universal-rules in session output.

## 2. Repo identity

- **Name:** `.dev-knowledge`
- **Scale tier:** M (per `protocols/PLAYBOOK.md` Project Scale Tiers section)
- **Purpose:** Universal LLM-driven development guide and methodology framework; governs all projects under `Dev/`
- **Status:** active
- **Owner:** Rob
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`, `ARCHITECTURE.md`

## 3. Architecture

Layer 2 of the ADR-28 three-layer model: Browser chat (Layer 1, analysis) → `.dev-knowledge` (Layer 2, passive storage) → Projects (Layer 3, execution). NOT a code project — markdown governance files and read-only validators only. No application code, no runtime execution from this layer.

Key directories:
- `protocols/` — ESSENTIALS, PLAYBOOK, HANDOFF_PROCESS, SESSION_SETUP, ENVIRONMENT (living files)
- `docs/` — `decisions/` (ADRs + transcripts), `audits/`, `handoffs/`, `research/`
- `templates/` — reusable boilerplate (CLAUDE-md, AGENTS-md, workspace tiers, HANDOFF, prompt)
- `scripts/` — read-only validators: `audit.py`, `backlog_extract.py`, `normalize_headers.py`
- `tests/` — pytest unit tests for validators
- `ecosystem/` — cross-repo ecosystem state snapshots
- `logs/` — TOKEN-LOG.md (threshold-triggered)

→ `ARCHITECTURE.md` for the full layer model and numbered invariants.

**Enforcement (mechanical):** pre-commit (ruff), git-discipline rule (`.claude/rules/git-discipline.md`), pytest.

**Advisory:** Layer 2 never executes — validators are read-only; no orchestration scripts in this repo.

## 4. Conventions

**Filenames:** UPPERCASE for top-level living docs (`VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, etc.); `ADR-NN-topic.md` for decisions; `YYYY-MM-DD-slug.md` for dated artifacts (audits, handoffs); `council-out-YYYYMMDD_HHMMSS-topic.md` for Council CLI output; kebab-case otherwise.

**Branches:** `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>`

**Commits:** Conventional Commits — `feat:` / `fix:` / `docs:` / `chore:` / `refactor:`

**File lifecycle:**
- `LESSONS.md` and `TOKEN-LOG.md` — append-only, NEVER edit old entries
- `JOURNAL.md` — append-only, newest-first prepend
- ADRs, transcripts, handoffs, audits — immutable dated artifacts; supersede with a new file or an in-file marker, never edit

**Scope tags** (`<!-- scope: X -->`) — informal lightweight metadata only; not enforced (enforcement withdrawn 2026-05-16 per Council Simplification / ADR-48).

## 5. Tools active in this repo

**Code review:** Codex (OpenAI) — mode: full review; path guard: code files only (PLAYBOOK §16 code-only rule). `.dev-knowledge` is a markdown repo — doc-only changes do not cross the code-file threshold, so codex-review effectively never triggers here. See `templates/codex-review-config-template.md` for configuration reference.

**Linting:** ruff — `ruff check --fix` (pre-commit).

**Tests:** pytest — `pytest -x --tb=short`. Known pre-existing failure: `test_audit_run_passes_structural_checks_on_synthetic_repo` (tracked in BACKLOG).

**Token tracking:** ccusage — see `protocols/ENVIRONMENT.md`.

**Architecture enforcement:** none mechanical. Read-only audit tool (`scripts/audit.py`) for cross-repo conformance; invoked manually.

## 6. Things this repo gets wrong (gotchas)

**Skill location:** `.claude/skills/gotchas/SKILL.md`

Read the gotchas skill before making changes. Common patterns this repo has stumbled on:
- See `.claude/skills/gotchas/SKILL.md` for the full list (repo-specific gotchas accumulate there)

## 7. Council decisions binding here

ADRs in `docs/decisions/`. Active bindings:

- ADR-27: Scope tagging architecture — vocabulary `dev | llm | hybrid | runtime | meta`; enforcement retired 2026-05-16 per ADR-48; existing tags remain as informal metadata
- ADR-28: Three-layer architecture — Browser chat (Layer 1) → `.dev-knowledge` (Layer 2, passive storage) → Projects (Layer 3); Layer 2 never executes
- ADR-29: LESSONS.md grandfathering — scope-tag mechanics now informal per ADR-48; append-only invariant remains binding via CLAUDE.md and ADR-39
- ADR-30: Default branch = `main` for all repos
- ADR-31: Authority model — Prescriptive with conformance audit (1B); Scale M with one L-tier artifact (ARCHITECTURE.md)
- ADR-32: Handoff format — folder-based, 9-section HANDOFF.md, manifest.json, point-in-time governance copies
- ADR-33: VISION.md universalization — mandatory at ≥1 dependent; Standard/Lite tiers
- ADR-34: File naming convention — UPPERCASE for living docs, `ADR-NN-topic` for decisions, `YYYY-MM-DD-slug` for dated artifacts
- ADR-35: Lessons base activation — push retrieval via SessionStart hook, pull via `lessons query`
- ADR-36: Audit tool architecture — `.dev-knowledge` as ecosystem auditor; read-only, manually invoked
- ADR-37: Session boundary protocol — two-phase handoff overlay (Current State + Future State)
- ADR-38: Universal repo baseline — mandatory files per scale tier (S/M/L)
- ADR-39: File lifecycle governance — 6-element pattern per file (purpose/trigger/owner/grooming/boundaries/enforcement)
- ADR-40: Scale tier evaluation — logarithmic Maintainability Index pattern; 3 signals; transition procedures
- ADR-41: Cross-session backlog architecture — BACKLOG.md mandate at M+ tier
- ADR-42: Handoff format v3 — amends ADR-32; folder-based handoffs with invariant/session separation
- ADR-43: Cross-project transcript routing — Council CLI dual-writes to `ai-council/output/` (operational) and `.dev-knowledge/docs/decisions/transcripts/` (curated)
- ADR-46: Cross-repo dated-entries format — convention retained (demoted from audit-enforced 2026-05-16)
- ADR-47: Cross-repo BACKLOG.md organization — convention retained (demoted from audit-enforced 2026-05-16)
- ADR-48: Trim documentation governance — retired scope-tag and hybrid-ratio enforcement; structural enforcement only
- ADR-49: Consolidate past-recording documentation files — governs record consolidation patterns
- ADR-50: Machine-document encoding standard — governs how machine-written content is encoded and marked
- ADR-51: ARCHITECTURE.md convention — mandates this repo's ARCHITECTURE.md form and CORE sections
- ADR-52: AGENTS.md convention — mandates this AGENTS.md structure as cross-tool agent contract

Reference `docs/decisions/README.md` for full index. Council debate transcripts in `docs/decisions/transcripts/`.

## 8. Out of scope

Things that explicitly do NOT belong in this repo:
- Code-level implementation — belongs in child repos (corp-monorepo, ai-council, etc.)
- Client/product/domain knowledge — goes to Obsidian vault
- Project-specific CLAUDE.md content — each repo owns its own
- Claude Code runtime config — goes to `~/.claude/`
- Acting as operational executioner — Layer 2 is passive; no orchestration from here
- AI Council debate transcripts authored here — they archive here (in `docs/decisions/transcripts/`), but originate in `ai-council/`

## 9. Session start checklist

When starting a Claude Code session here, check:

1. `git status` — clean working tree?
2. `git log --oneline -5` — recent context
3. Read last 5 JOURNAL.md entries
4. Read most recent `docs/handoffs/` entry if continuing a prior session
5. `pytest --collect-only` — test discovery sanity check
6. Check BACKLOG.md for in-progress items

If any check fails → stop and ask Rob before proceeding.

## 10. Do NOT

- **Edit old LESSONS.md or TOKEN-LOG.md entries** — append-only files; editing corrupts the institutional record (ADR-29, ADR-39)
- **Add scripts that execute orchestration** — Layer 2 invariant: validators only, no orchestration (ADR-28, ADR-36)
- **Create new markdown files without checking README.md growth triggers** — when navigation overhead emerges, evaluate DevVault migration
- **Duplicate content between files** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
- **Put executable rules in this repo** — those go in `~/.claude/` with `verify:` lines
- **Recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16 per Council Simplification; git history + JOURNAL `Changes:` line replace CHANGELOG; done BACKLOG items leave the file, trace lives in git
- **Narrate or manage AGENTS.md in the handoff workflow** — AGENTS.md is an agent-instruction contract, not handoff content (ADR-52)

---

**Last updated:** 2026-05-19
**Maintained by:** Rob
