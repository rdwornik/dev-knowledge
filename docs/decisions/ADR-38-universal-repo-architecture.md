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

### 2026-05-18 — A4: Close corp-monorepo ARCHITECTURE.md migration deferral

- **Source:** corp-monorepo universalization effort (Workstreams B/C/D rollout,
  2026-05-18).
- **Decision:** The corp-monorepo `ARCHITECTURE.md` root-placement migration
  that A3 deferred to "a separate later effort" is now activated and executed.
  `docs/ARCHITECTURE.md` → repo root migration is in scope for the
  corp-monorepo universalization prompt sequence. The A3 deferral is
  **closed**.
- **Rationale:** A3 decided the rule (root placement mandatory); it only
  deferred the mechanical move for corp-monorepo. The universalization rollout
  now performs that move, making the deferral obsolete.
- **Prior state:** A3 recorded: "Affected repos: corp-monorepo
  (`docs/ARCHITECTURE.md` → root migration deferred to Phase 2, separate
  prompt)." That deferral clause is superseded by this amendment.
- **Effect:** corp-monorepo is no longer exempt from A3's root-placement
  mandate. All repos (corp-monorepo, ai-council, future) must place
  ARCHITECTURE.md at root per A3.
- **Decision tier:** Conversational (closes an expired timing deferral of an
  already-decided rule — decides nothing new).

### 2026-05-23 — A5: Universal baseline (tier deprecation), CHANGELOG strike, ARCHITECTURE universal, README deprecated

- **Source:** Operator decision 2026-05-23 (browser-chat), reconciling Opus
  deep-audit findings (`docs/audits/2026-05-23-ai-council-deep-audit.md` §7
  #1 and #2) with the ecosystem-wide tier-system deprecation.
- **Status of original Decision blocks:** preserved above for decision-trace.
  This amendment supersedes the tier-conditional clauses within them as
  described below. Where the original text and this amendment conflict, this
  amendment governs.

**Delta 1 — Universal baseline (tier deprecation).** The tier system
(`tier:`/`scale:` per ADR-33/ADR-40) is deprecated ecosystem-wide. The
per-tier branching in the original mandatory-documentation table and the
"OPTIONAL for tier S; REQUIRED for tier M+" directory annotations collapse
to a single universal baseline applicable to every covered repo regardless
of size. Rationale: tier-conditional baselines did not differentiate
governance behavior in practice — all active repos converged to similar
governance regardless of declared tier (tier-as-theater analysis, operator
decision 2026-05-23). See [[ADR-33]] amendment (VISION frontmatter) and
ADR-40 deprecation, same date.

**Delta 2 — CHANGELOG.md removed.** The "CHANGELOG.md — MANDATORY tier M+"
directory annotation and the CHANGELOG row in the mandatory-documentation
table are null. Superseded by ADR-49 (consolidate past-recording files,
2026-05-17), which retired `CHANGELOG.md` ecosystem-wide. ADR-38's original
CHANGELOG mandate has no force.

**Delta 3 — ARCHITECTURE.md universal mandate.** `ARCHITECTURE.md` at repo
root is mandatory for every covered repo. This extends ADR-51 Decision 1
(was: mandatory at M+L only) to all scales, per operator decision
2026-05-23. The "OPTIONAL / NO" entries for ARCHITECTURE.md in the original
table are superseded. Root-placement amendment A3 (2026-05-11) remains in
force. See [[ADR-51]] amendment same date.

**Delta 4 — README.md deprecated from mandatory baseline.** `README.md` is
removed from the mandatory baseline — operator decision 2026-05-23, option A
(deprecated universally; optional for repos with an external audience).
Rationale: for internal-only repos, README content is redundant with
`VISION.md` (purpose), `CLAUDE.md` (how to work with the repo), and
`ARCHITECTURE.md` (what exists). Repos that serve an external audience MAY
keep a README.

**Post-2026-05-23 mandatory baseline (supersedes the original table).** Every
covered repo MUST have, at root:

| File | Status | Governing |
|---|---|---|
| `VISION.md` | MANDATORY | ADR-33 (frontmatter per amended schema) |
| `CLAUDE.md` | MANDATORY | ADR-31 / ADR-53 |
| `ARCHITECTURE.md` | MANDATORY (universal) | ADR-51 (amended 2026-05-23) + A3 root placement |
| `BACKLOG.md` | MANDATORY | ADR-41 |
| `README.md` | OPTIONAL | external-audience repos only |
| `CHANGELOG.md` | REMOVED | superseded by ADR-49 |

`JOURNAL.md` and `LESSONS.md` remain repo-specific (not part of the universal
baseline; mandated where a repo's own conventions require them).

**Code-structure requirements (`src/`, `tests/`, `pyproject.toml`).** The
original "Required directory structure" section codified a code-project layout
(`src/{package}/`, `tests/`, `pyproject.toml`). That layout remains the
convention for **code projects**. It is NOT part of the universal *governance*
baseline that the audit tool checks across all repos — governance repos
(e.g. `.dev-knowledge` itself, which has no `src/` and no `pyproject.toml`)
are not code projects and are not required to carry that layout. The audit's
`check_adr38_baseline` therefore checks the governance-file baseline above,
not code structure (operator decision 2026-05-23, resolving the
governance-repo exemption question previously open in BACKLOG). The
module/test/TCR definitions further down this ADR were inputs to ADR-40
(now deprecated) and are retained for historical reference only.

- **Decision tier:** Conversational (reconciliation of already-decided
  operator directives; no new architectural question).

### 2026-06-02 — A6: Seven-file canonical set + canonical structure standard (ecosystem unification)

- **Source:** Operator decision 2026-06-02 — the ecosystem-unification effort
  ("lock the standard, then unify every repo"). `.dev-knowledge` is locked as the
  definitive reference; the four child repos (ai-council, corp-monorepo, corp-ops,
  corp-sca-time-automation) are unified to it in follow-on per-repo sessions.
- **Decision tier:** Operator-directed (Path A — a uniformity standard the operator
  decided directly; no Council convene). The one contestable axis (the backlog-form
  binding) was settled by operator ruling with proportional depth — see Delta 3.

**Delta 1 — Seven canonical files (supersedes the A5 baseline of four).** Every
covered repo MUST carry, at repo root, all seven canonical files:

| File | Status | Governing |
|---|---|---|
| `VISION.md` | MANDATORY | ADR-33 |
| `ARCHITECTURE.md` | MANDATORY | ADR-51 (amended 2026-05-23) + A3 root placement |
| `CLAUDE.md` | MANDATORY | ADR-53 |
| `BACKLOG.md` | MANDATORY | ADR-41 (amended 2026-06-02) |
| `CONTRIBUTING.md` | MANDATORY (new) | this amendment |
| `JOURNAL.md` | MANDATORY (new) | this amendment |
| `LESSONS.md` | MANDATORY (new) | ADR-29 (entry format) |

This **supersedes** the A5 line "JOURNAL.md and LESSONS.md remain repo-specific (not
part of the universal baseline)" and promotes `CONTRIBUTING.md` from absent to
mandatory. Rationale: cross-repo navigation must feel identical — an inheritor (the
operator or an AI agent) opening any repo finds the same seven anchors. `README.md`
stays OPTIONAL (A5 Delta 4, external-audience repos only); `CHANGELOG.md` stays
REMOVED (ADR-49).

**Delta 2 — Canonical structure standard (identical spine, proportional content).**
The seven files share one structure across every repo: identical heading text /
levels / section order, taken from `.dev-knowledge`'s own files as the reference
exemplar (and the `templates/` skeletons). Sections are of three kinds:

- **[U] universal spine** — present and identical in every repo (the navigation
  backbone; what the read-only structural check asserts).
- **[R] repo-specific content** — same heading, real per-repo content (e.g.
  ARCHITECTURE Codemap, CLAUDE §2/§4 conventions, CONTRIBUTING branch-naming).
- **[C] conditional** — present only where the repo has the artifact (e.g. CLAUDE
  §11 "Recent ADRs" only where `docs/decisions/` exists; ARCHITECTURE "Governing ADRs").

A code repo (corp-monorepo) fills [R]/[C] with its own content; it is not forced to
carry empty governance ceremony. Uniform **shape**, proportional **depth**.

**Delta 3 — Canonical backlog form (one changelog-feeding shape, all repos).** The
single canonical `BACKLOG.md` form for every covered repo is the ADR-66 story-map
(Big Picture → Theme → User Story → Task; done-tasks-leave per ADR-65; `[#id]`
forward-indexing that feeds the git changelog via the `commit-msg` hook; read-only
`validate_backlog.py`), with **proportional depth** — a low-volume repo carries a
single Theme/Story until item volume justifies more, so a small or code-centric
backlog never accretes the "write-only graveyard" ceremony ADR-41/47 guarded against.
The supersession chain that lands here is recorded in the ADR-41 amendment
(2026-06-02), which closes BACKLOG #20.

**Delta 4 — Enforcement.** `audit.py` is extended this session: `check_adr38_baseline`
and `check_canonical_md_visibility` require all seven files (presence + ALL-CAPS
casing); a new read-only `check_canonical_structure` asserts the [U] spine headings
per file (presence, not strict order — child-repo-safe). `BACKLOG.md` hierarchy stays
covered by `validate_backlog.py`. The audit-health gate is self-only, so a
not-yet-unified child repo surfaces as a FAIL in `audit run` (the intended surfacing)
without blocking `.dev-knowledge` commits.
