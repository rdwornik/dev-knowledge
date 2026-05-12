# ADR-38 — Universal Repo Architecture Baseline

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-30
Related: ADR-29 (grandfathering pattern), ADR-33 (universalization),
         ADR-34 (file naming), ADR-39 (file lifecycle, pending),
         ADR-40 (scale tier evaluation, pending),
         ADR-41 (BACKLOG.md, pending)

## Context

.dev-knowledge ecosystem has 4+ child repos under Dev/ (corp-monorepo,
ai-council, corp-ops, corp-sca-time-automation, future repos). Each repo
historically evolved its own structure. corp-monorepo has established
mature pattern (src/corp/ namespace, tests/, pyproject.toml). Other
repos vary.

Without consistent architecture across repos, audit metrics measure
different things in different repos:
- "Module count" depends on what counts as module
- "Test count" depends on test directory location and naming
- "TCR" (token context ratio) depends on which files included

ADR-38 codifies existing corp-monorepo pattern as universal baseline.
This is foundation for ADR-39 (file lifecycle), ADR-40 (tier
evaluation algorithm), ADR-41 (BACKLOG.md).

Insight from .dev-knowledge architect: signals must be measurable
identically across repos for audit decisions to be meaningful.
Universal architecture is prerequisite for universal governance.

## Decision

### Required directory structure

Every repo MUST have:

```
{repo_root}/
├── src/
│   └── {package_name}/      # primary namespace, snake_case
│       ├── __init__.py
│       └── {modules}.py     # OR submodule directories
├── tests/
│   ├── __init__.py
│   └── test_*.py            # test files prefixed test_
├── docs/                    # OPTIONAL for tier S; REQUIRED for tier M+
│   └── decisions/           # ADRs if applicable
├── pyproject.toml           # OR equivalent: package.json, Cargo.toml
├── README.md                # MANDATORY all tiers
├── VISION.md                # per ADR-33 (Lite for tier M, Standard for L)
├── CHANGELOG.md             # MANDATORY tier M+
└── .gitignore
```

### Source structure (`src/`)

- Repo MUST have `src/` directory at root
- Inside `src/`, single primary package: `src/{package_name}/`
- Package name = snake_case derivative of repo name
  - corp-monorepo → src/corp/
  - ai-council → src/ai_council/
  - corp-ops → src/corp_ops/
  - corp-sca-time-automation → src/corp_sca_time_automation/
- All source code lives inside primary package
- Submodules = subdirectories with `__init__.py`

### Tests structure (`tests/`)

- Repo MUST have `tests/` directory at root (sibling of src/)
- Test files prefixed `test_*.py`
- Test discovery follows pytest conventions
- Subdirectories allowed for organization (tests/unit/, tests/integration/)
- Each subdirectory MUST have `__init__.py`

### Configuration (`pyproject.toml`)

Repo MUST have `pyproject.toml` (or language equivalent for non-Python repos).

Required sections (minimum):
- `[project]` — name, version, description
- `[project.dependencies]` — explicit deps (or empty list)
- `[build-system]` — build backend declared

Optional but recommended:
- `[tool.pytest.ini_options]` — test config
- `[tool.ruff]` — linter config
- `[project.scripts]` — CLI entry points

### Mandatory documentation

| File | All tiers | Tier M+ | Tier L |
|---|---|---|---|
| README.md | YES | YES | YES |
| VISION.md (per ADR-33) | OPTIONAL | YES (Lite) | YES (Standard) |
| CHANGELOG.md | OPTIONAL | YES | YES |
| ARCHITECTURE.md | NO | OPTIONAL | YES |
| docs/decisions/ (ADRs) | NO | OPTIONAL | YES |
| BACKLOG.md (per ADR-41) | NO | YES | YES |

> **[Amended 2026-05-11 — A3]** ARCHITECTURE.md MUST be placed at repo
> root, NOT nested in `docs/` or any subdirectory. Rationale:
> cross-tool discoverability — LLM coding agents (Claude Code, Codex,
> Cursor) scan root-level files first; root placement matches industry
> convention (GitHub, most open-source projects). See Amendments section.

### Module definition (used by ADR-40 metrics)

A "module" = top-level subdirectory inside `src/{package_name}/` containing
`__init__.py` and 1+ Python files.

Example for corp-monorepo:
```
src/corp/
├── __init__.py
├── ingest/         ← module 1
├── actions/        ← module 2
├── routing/        ← module 3
└── ...
```

Module count = number of such top-level subdirectories.

Files directly under `src/{package_name}/` (e.g., `cli.py`) are NOT
modules — they are package-level utilities.

### Test definition (used by ADR-40 metrics)

A "test" = a function in a `test_*.py` file matching pytest discovery rules:
- Function named `test_*`
- Function in class `Test*`

Test count = sum of all such functions across `tests/` directory tree.

Computation: pytest collection (`pytest --collect-only -q | wc -l`) or
AST-based parser counting `def test_*` functions.

### TCR (token context ratio) computation rules (used by ADR-40)

TCR = total estimated tokens across all source-controlled files matching:
- Files inside `src/`
- Files inside `tests/`
- Files at repo root: README.md, VISION.md, CHANGELOG.md, ARCHITECTURE.md,
  pyproject.toml
- Files inside `docs/` directory

EXCLUDED from TCR:
- Files in `.gitignore`
- Generated files (build/, dist/, *.egg-info/)
- Cache directories (__pycache__/, .pytest_cache/, etc.)
- Lock files (poetry.lock, package-lock.json) — too large, low signal
- Binary assets (images, PDFs)

Token estimate: chars / 4 (English text rule of thumb, deterministic,
no external dependencies). Implementation in plain Python via os.walk
+ file size or character count.

### Universalization (per ADR-33 pattern)

- **Mandate**: .dev-knowledge MUST follow this architecture
- **Mandate**: corp-monorepo, ai-council MUST follow this architecture
  (already mostly compliant — gaps to be addressed in Phase 2 universalization)
- **Recommendation**: corp-ops, corp-sca-time-automation, future repos
  follow same architecture; trigger-based migration by 2026-06-30 per
  ADR-33 cohort
- **Cross-repo audit (Phase 3)**: auditor verifies architecture compliance
  per repo

### Migration approach (per ADR-29 grandfathering pattern)

For existing non-compliant repos:

- **Compliant**: corp-monorepo (already has src/corp/, tests/,
  pyproject.toml — verify minor details)
- **Partial compliance**: ai-council (verify structure)
- **Migration required**: any repo missing required directories or
  documentation
- **Grace period**: 60 days from ADR-38 ratification (2026-06-29)
- **Grandfather**: existing files in non-standard locations may remain
  until next major refactor; new files MUST follow standard

### Enforcement

- **Audit tool (per ADR-36)** verifies architecture compliance
- **Pre-commit hook in .dev-knowledge** validates own architecture
  (validate_repo_structure.py — separate implementation session)
- **AGENTS.md / CLAUDE.md** in each repo notes "follow ADR-38 architecture"
  (Phase 2 update per universalization)

## Consequences

### Positive
- Audit metrics (ADR-40) measure same things across repos
- New repos start with established pattern (no bikeshedding)
- LLM agents (Claude Code, browser Claude) can navigate any repo using
  same mental model
- Cross-repo cognitive load reduced — switching between corp-monorepo
  and corp-ops feels familiar
- Universalization pattern (ADR-33) extended from VISION.md to whole
  architecture

### Negative
- Migration cost for non-compliant repos (60-day grace period mitigates)
- Constraint on architectural creativity (deliberate trade-off)
- Future architectural needs may require ADR-38 amendment

### Follow-ups
- Phase 2 universalization rollout: ai-council, corp-monorepo (immediate
  cohort) verify compliance, address gaps
- corp-ops, corp-sca-time-automation: trigger-based migration by 2026-06-30
- ADR-39 (File Lifecycle Governance): defines what each mandatory file
  contains and how it evolves
- ADR-40 (Scale Tier Evaluation): uses module/test/TCR definitions from
  this ADR
- ADR-41 (BACKLOG.md): mandates BACKLOG.md per tier definitions here
- validate_repo_structure.py implementation: separate session
- AGENTS.md / CLAUDE.md updates per repo: Phase 2

## References

- ADR-29 (lessons format and grandfathering)
- ADR-33 (VISION.md universalization)
- ADR-34 (file naming convention)
- corp-monorepo repository (canonical reference implementation)
- Python packaging conventions (PEP 518, PEP 621 for pyproject.toml)

## Amendments

### 2026-05-11 — A3: ARCHITECTURE.md root placement

- **Source:** `docs/audits/2026-05-11-cross-repo-pattern-audit.md`, A-item A3
- **Decision:** ARCHITECTURE.md MUST be placed at repo root, not nested
  in `docs/` or any subdirectory. Root placement is mandatory wherever
  ARCHITECTURE.md is required (Tier L) or present (Tier M+).
- **Rationale:** Root placement matches cross-tool LLM agent discovery
  behavior and industry convention. `docs/ARCHITECTURE.md` placement
  observed in corp-monorepo was non-compliant with intent.
- **Prior state:** Placement was unspecified — table row said "YES" for
  Tier L but did not name the required path. Unspecified placement →
  inconsistency (corp-monorepo placed at `docs/ARCHITECTURE.md`).
- **Affected repos:** corp-monorepo (`docs/ARCHITECTURE.md` → root
  migration deferred to Phase 2, separate prompt).
- **Decision tier:** Conversational (no Council debate needed — single
  placement question, low cost, root is unambiguous industry convention).
