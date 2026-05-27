---
type: audit-discovery
scope: cross-repo universalization vs .dev-knowledge baseline current state
date: 2026-05-26
contract: read-only on all child repos (Layer-2 invariant); writes confined to docs/audits/
worktree: .dev-knowledge primary tree (parallel worktree not created — Phase 1 handoff stabilization already merged to main at 907c4c7, so the race-condition rationale was moot; operator approved running here on a fresh branch)
parent_branch: main
session_branch: docs/cross-repo-audit-refresh-2026-05-26
parallel_session: docs/handoff-process-stabilization-2026-05-26 (already merged — commit 907c4c7)
---

# Cross-Repo Universalization Audit Discovery — 2026-05-26

## Methodology

Read-only discovery pass establishing the state snapshot for four child-repo
universalization audits. The standard (what each repo is audited *against*) is
`.dev-knowledge`'s ADRs + templates + PLAYBOOK as they stand at branch HEAD
(`main` @ `907c4c7`). Each child repo was inspected via `git ls-files` +
targeted `Read`/`Grep` of its working tree; no child-repo file was modified
(ADR-28/ADR-36 Layer-2 read-only contract). Every per-repo finding in the
downstream audit-refresh docs cites a `file:line` or a verified file-state fact.

This is a **delta methodology** where a baseline audit exists (corp-monorepo,
ai-council) and an **initial audit** where none does (corp-ops,
corp-sca-time-automation).

### Worktree note (deviation from prompt, operator-approved)

The prompt assumed a `.dev-knowledge-parallel` git worktree created by an
operator pre-flight, to run concurrently with an in-flight Phase-1 handoff
stabilization session. At session start the parallel worktree did **not** exist
and Phase 1 was **already merged to main** (`907c4c7 merge: handoff process
stabilization — implement all 5 Council decisions (Q1-Q5)`), so the
race-condition rationale was moot. The operator approved running in the primary
`.dev-knowledge` tree on a fresh branch (`docs/cross-repo-audit-refresh-2026-05-26`
off `main`). The architectural contract (read-only child repos, writes confined
to `docs/audits/`) is unchanged by this.

## Baseline standards inventory (`.dev-knowledge` canonical)

The audit criteria, read end-to-end for this refresh:

| Standard | Rule (current) | Source |
|---|---|---|
| ADR-38 A5 (2026-05-23) | Universal governance baseline: `VISION`, `CLAUDE`, `ARCHITECTURE`, `BACKLOG` mandatory at root; README optional (external-audience only); CHANGELOG removed; tier system deprecated | `docs/decisions/ADR-38-*.md` |
| ADR-33 amendment (2026-05-23) | VISION frontmatter required keys = `version`, `last_reviewed`, `owner`, `status`; `tier`/`scale` removed | `docs/decisions/ADR-33-*.md` |
| ADR-51 + amendments (2026-05-22 / 23) | `ARCHITECTURE.md` mandatory at root for every repo; CORE sections (Purpose, Codemap, Layer Boundaries & Invariants); codemap = embedded Mermaid between `<!-- CODEMAP:START/END -->` (generator opt-in, hand-authored permitted) | `docs/decisions/ADR-51-*.md` |
| ADR-49 (2026-05-17) | CHANGELOG retired ecosystem-wide; record = git history + JOURNAL `Changes:` line | `docs/decisions/ADR-49-*.md` |
| ADR-53 (2026-05-19) | CLAUDE.md is the single canonical agent-instruction file; AGENTS.md retired as an instruction contract | `docs/decisions/ADR-53-*.md` |
| ADR-54 (2026-05-19) | Codex reviewer config is a global standard at `~/.codex/AGENTS.md`; per-repo `AGENTS.md` carries only repo-specific review rules | `docs/decisions/ADR-54-*.md` |
| ARCHITECTURE template | Frontmatter `last_reviewed`/`status`/`owner` (no `scale`); `[CORE]`-only section tags; Mermaid codemap default, text-only override for tiny repos | `templates/ARCHITECTURE-template.md` |
| Root hygiene (PLAYBOOK §, v1.0 2026-05-23 + pass-2 v1.1 2026-05-24) | Consolidate tool configs into `pyproject.toml` (code projects); dot-prefix `.code-workspace` and `.ruff.toml`; **do not create `.env.example`** | `protocols/PLAYBOOK.md:196-238` |
| Audit tool | `scripts/audit.py` checks only: VISION 4 keys, ADR-38 baseline (VISION+ARCHITECTURE+BACKLOG present), CLAUDE non-empty. **Under-reports** full-standard conformance (no tier-residue / hygiene / README / codemap / naming detection) | `scripts/audit.py:137-197` |

**Reference exemplars:** `.dev-knowledge/ARCHITECTURE.md` (frontmatter + inline
Mermaid layer model + CODEMAP block), `.dev-knowledge/VISION.md` (frontmatter
`version`/`owner`/`last_reviewed`/`status`).

### Operator decisions baked in (apply uniformly; deviation requires explicit rationale)

| Decision | Default | Notes for this session |
|---|---|---|
| README disposition | **Delete** | Applied to all 4 repos. corp-monorepo's README is the most product-like — flagged for explicit confirmation, not silently overridden. |
| Codemap maintenance | **Hand-authored Mermaid** | No generator opt-in, no freshness hook, in any plan. |
| `.env.example` | **Remove** | corp-sca actively references it (`cp .env.example .env`) — flagged as the contributor-reliance exception case. |
| LESSONS scope-tag backfill | **Defer (optional)** | Stays optional where applicable. |
| Workspace tier-residue | **Flag as separate `.dev-knowledge` change** | Out of scope per repo (it's a `.dev-knowledge` template-framework concern). |
| CHANGELOG / AGENTS.md | **Confirm absent** | Per ADR-49 / ADR-53. |
| Tier/scale frontmatter | **Remove residue** | Per ADR-33 amendment. |
| ARCHITECTURE.md | **Mandatory + Mermaid (or text-only for tiny repos)** | Per ADR-51 amendment. |
| Dot-prefix tool configs | **Apply where supported** | Per root hygiene. |

## Child repo inventories

### corp-monorepo

- **HEAD:** `f418c78` ("Merge branch 'audit/adr27-status'"). Baseline audit
  (`docs/audits/2026-05-23-corp-monorepo-deep-audit.md`) targeted `32a47f8`.
- **Movement since baseline:** 2 commits only — `80ebf67 docs(audits): ADR-27
  implementation status audit` + `66d244a chore(journal)`. **No universalization
  work landed.** All 12 baseline findings carry forward unchanged.
- **Canonical files:** VISION ✓ (frontmatter `tier: standard` + `scale: L` =
  **residue**; has `status`), ARCHITECTURE ✓ (predates ADR-51 — `# Architecture
  Reference -- Corporate OS`, no frontmatter, no `[CORE]` tags, no CODEMAP
  markers, "Last updated: 2026-03-30"), CLAUDE ✓ (tier-residue prose at `:25`,
  `:30`, `:136`), BACKLOG ✓ (header cites ADR-41 strict schema, not ADR-47),
  CONTRIBUTING ✓, JOURNAL ✓. LESSONS absent **by design** (cross-repo lessons
  route to `.dev-knowledge/LESSONS.md`).
- **Deprecated files:** README **present** (product-facing: "Corporate OS
  Monorepo… pre-sales engineering"; stale `Total 2,412`). CHANGELOG **absent** ✓.
  AGENTS.md **absent** ✓.
- **Tool configs:** `ruff.toml` (lenient `E,F,I`) **+** `pyproject.toml
  [tool.ruff]` (stricter) — duplication; root `ruff.toml` wins. `tach.toml`
  present (layer enforcement). Not dot-prefixed.
- **Workspace:** `corp-monorepo.code-workspace` present, **not** dot-prefixed.
- **`.env.example`:** present.
- **Existing audit:** 2026-05-23 deep audit (12 findings: 0 CRITICAL / 4 HIGH /
  3 MEDIUM / 5 LOW; ~80% conformant). Carry-forward basis.

### corp-ops

- **HEAD:** `97c78ba` ("chore: Scripts → Dev path migration"). 47 tracked files.
- **Canonical files:** CLAUDE ✓ (old free-form format, **not** ADR-53 12-section
  template; **no** tier/scale residue; does not reference VISION/ARCHITECTURE
  because they don't exist). **VISION absent**, **ARCHITECTURE absent**,
  **BACKLOG absent** → `audit.py` would FAIL `vision_md` + `adr38_baseline`.
  JOURNAL absent, LESSONS absent. No `docs/` directory.
- **Deprecated files:** README **present** (internal toolbox doc; heavily
  overlaps CLAUDE.md "What this repo does"). CHANGELOG **present** (`# Changelog
  — corp-ops`, last entry 1.0.0 2026-03-15) → retire per ADR-49. AGENTS.md absent ✓.
- **Tool configs:** `pyproject.toml` with `[tool.ruff]` + `[tool.pytest.ini_options]`
  **already consolidated** ✓ (no standalone ruff.toml). Clean code project.
- **Workspace:** none.
- **`.env.example`:** present; **not** referenced in CLAUDE/README (auth is
  cookie/token, not env) → clean removal.
- **Source:** `src/corp_ops/` with 4 sub-packages (`auth/`, `common/`,
  `onedrive/`, `gdrive/`) + `config.py` — clean package graph, codemap-friendly.
- **Existing audit:** none → **initial audit**.

### corp-sca-time-automation

- **HEAD:** `d6dfb15` ("docs: add verified handoff doc for 2026-04-15 session").
  55 tracked files.
- **Canonical files:** CLAUDE ✓ (old free-form format, **not** ADR-53 template;
  **no** tier/scale residue; carries rich inline architecture — data-flow block +
  "Key modules" table + "Known issues" list — which seeds ARCHITECTURE.md and
  BACKLOG.md). **VISION absent**, **ARCHITECTURE absent**, **BACKLOG absent** →
  `audit.py` FAIL. `docs/` exists (`archive/`, `handoffs/`) but no governance docs.
- **Deprecated files:** README **present** ("Internal use only — Blue Yonder
  Pre-Sales"). CHANGELOG **present** → retire per ADR-49. AGENTS.md absent ✓.
- **Tool configs:** **`requirements.txt`, no `pyproject.toml`.** No tracked ruff
  config (only `.ruff_cache`). Config consolidation N/A without a pyproject;
  creating one is a code-project decision, out of universalization scope.
- **Workspace:** `.vscode/` present (tracked); no `.code-workspace`.
- **`.env.example`:** present **and actively referenced** — `CLAUDE.md:15` and
  `README.md:31` both instruct `cp .env.example .env`. **Contributor-reliance
  exception case** — removal requires migrating env-var docs into CLAUDE.md and
  dropping the `cp` instruction, or keeping it with a noted exception.
- **Source:** `src/` with **flat modules** (`config.py`, `loader.py`,
  `mapper.py`, … — no package namespace). Flat structure → text-only codemap
  override is the appropriate transitional form.
- **Existing audit:** none → **initial audit**.

### ai-council (light verification only — not re-audited this session)

- **HEAD:** `2a980ab` ("docs: merge chunk4 — retire AGENTS.md, CLAUDE.md v2.1
  live (ADR-53)"). **Unchanged** since the 2026-05-25 refresh basis (`2a980ab`).
- **Consequence:** the existing `2026-05-25-ai-council-universalization-audit-refresh.md`
  + `-execution-plan.md` (both in `docs/research/`) remain **current and
  authoritative**. No re-refresh needed.
- **Findings (per existing refresh):** 14 total — 0 CRITICAL / 0 HIGH / 5 MEDIUM
  / 9 LOW (7 carry-forward + 7 delta); conformance ~90% → ~70%.
- **Migration of those two artifacts** `docs/research/` → `docs/audits/` is
  **NOT** in this session's scope (separate cleanup; BACKLOG entry recommended).
  This session produces an ai-council **status reference** doc only.

## Gaps and unknowns

- **corp-monorepo README disposition.** The baked-in default is Delete, but
  corp-monorepo's README is the most product-like of the four (it reads as a
  module/CLI overview). Flagged for explicit operator confirmation in the
  corp-monorepo plan rather than silently deleted.
- **corp-sca pyproject.toml.** corp-sca is a code project on `requirements.txt`.
  Whether to migrate to `pyproject.toml` (enabling ruff/pytest config
  consolidation) is a code-project decision **out of universalization scope** —
  surfaced, not planned.
- **corp-sca / corp-ops codemap depth.** corp-ops has a clean 4-package graph
  (Mermaid-friendly); corp-sca is flat-module (text-only override likely). Final
  choice is the per-repo execution session's call.
- **Tier residue is corp-monorepo-only.** corp-ops and corp-sca never carried
  tier/scale (verified: zero `scale`/`tier` hits in their CLAUDE.md). Their gap
  is *absence of the governance scaffold*, not residue removal.

---

**Contract preserved:** zero child-repo files modified (read-only per
ADR-28/ADR-36). All writes confined to `.dev-knowledge/docs/audits/`.
