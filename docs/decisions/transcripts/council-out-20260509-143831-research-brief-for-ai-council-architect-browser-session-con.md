# Research Report

**Query:** # Brief for ai-council architect (browser session)

## Context — what's happening

Today, 2026-04-30, the `.dev-knowledge` ecosystem completed Phase 1 of
governance work: 8 ADRs ratified establishing universal architecture,
file lifecycle, scale tier evaluation, audit tool architecture, session
boundary protocol, and cross-session backlog architecture.

`.dev-knowledge` is the universal LLM-driven development brain governing
all child repos under `Dev/` — including `ai-council`. Its functions are
knowledge guardian, methodology author, disseminator, and auditor
(Scrum Master analog).

As validation of Phase 1 governance, `.dev-knowledge` performed a manual
audit of `ai-council` (Faza A1 discovery, output at
`.dev-knowledge/docs/audits/2026-04-30-ai-council-discovery.md`).

The audit revealed `ai-council` violates a fundamental ratified
requirement: **ADR-38 Universal Repo Architecture Baseline** mandates
`src/{package_name}/` namespace structure, but `ai-council` has flat
`src/` with files at package level (cli.py, debate.py, runner.py,
etc.) and only 2 subdirs (providers/, research/).

This non-compliance makes `ai-council` non-measurable per ADR-40 Scale
Tier Evaluation Algorithm — the algorithm's module signal is undefined
when repo doesn't follow ADR-38 structure. ai-council cannot be
classified S/M/L until structural compliance is achieved.

**Before the planned audit handoff (Faza A2 + A3) can be valid, ai-council
must achieve ADR-38 structural compliance.** This brief asks you, as the
architect for ai-council, to design the migration prompt for Claude Code
to execute in the ai-council repo.

## Why this matters — strategic framing

This is not bureaucratic compliance. The reason structural compliance
matters:

1. **Audit cannot run** — tier algorithm is undefined for non-compliant
   input. No tier = no governance triggers (BACKLOG mandate, VISION
   tier, etc.).
2. **Universalization blocked** — `ai-council` is in immediate Phase 2
   universalization cohort per ADR-33. Cannot universalize ratified
   ADRs onto non-compliant base.
3. **Cross-repo audit (Phase 3) deferred** — until ai-council compliant.
4. **Future Council debates** referencing ai-council architecture
   produce inconsistent results.

ADR-38 codified the pattern that corp-monorepo already uses (`src/corp/`).
ai-council was the outlier; this migration brings it in line.

## Required reading (in `.dev-knowledge` repo if you have access, otherwise summary follows)

If you have access to `.dev-knowledge` repo:
- `docs/decisions/ADR-38_universal_repo_architecture.md` — full text
- `docs/decisions/ADR-40_scale_tier_evaluation.md` — algorithm context
- `docs/audits/2026-04-30-ai-council-discovery.md` — full audit findings

If you don't have access — key requirements summary:

**ADR-38 mandates for any repo in ecosystem:**
- `src/{package_name}/` directory at root containing the primary
  package (snake_case derivative of repo name)
- `tests/` directory at root (sibling of src/)
- All source code lives inside primary package (`src/{package_name}/`)
- Submodules = subdirectories with `__init__.py`
- `pyproject.toml` MUST include `[build-system]` section (currently
  missing in ai-council per audit)

**For ai-council specifically:**
- Package name: `ai_council` (snake_case derivative of `ai-council`)
- Required transformation: move all files from `src/` directly into
  `src/ai_council/`
- Existing subdirs (`src/providers/`, `src/research/`) become
  `src/ai_council/providers/`, `src/ai_council/research/`

## Audit findings relevant to this migration (from Faza A1 discovery)

ai-council current state:
- HEAD: `47bea6f67f81eac4f2d0ebddc907546fc8514463`
- Branch: `main`
- Working tree: 1 modified file (`config/settings.yaml`) — uncommitted
- Source structure: flat `src/` (not `src/ai_council/`)
- 18 test files in tests/ (flat, no subdirectories)
- 219 test functions detected via grep (CLAUDE.md states 266 — discrepancy)
- `pyproject.toml` MISSING `[build-system]` section
- `pytest.ini` AND `[tool.pytest.ini_options]` in pyproject.toml coexist
  (duplication — recommend consolidating to pyproject.toml only)
- `ai_council.egg-info` present at both repo root AND inside src/
  (double presence — verify and clean up)
- `[project.scripts]` declares `council` and `ai-council` entry points
  with target `src.cli:main` (will need updating after migration to
  `ai_council.cli:main`)
- `[tool.setuptools.packages.find]` declares `where = ["."]`,
  `include = ["src*", "config*"]` (will need updating after migration)

## Scope of THIS migration session — structural compliance only

**In scope (this session):**
1. Migrate `src/` → `src/ai_council/` — all .py files moved into package
2. Update imports throughout codebase (src/ + tests/ + scripts/)
3. Update `pyproject.toml`:
   - Add `[build-system]` section
   - Update `[tool.setuptools.packages.find]` for new structure
   - Update `[project.scripts]` entry points (`src.cli:main` →
     `ai_council.cli:main`)
   - Optionally consolidate pytest config (remove pytest.ini OR remove
     `[tool.pytest.ini_options]` — single source of truth)
4. Clean up `ai_council.egg-info` artifacts (delete from src/ if
   misplaced; standard location is repo root)
5. Verify: pytest passes, `council` CLI works, package installs cleanly
   in editable mode

**Out of scope (later sessions):**
- VISION.md creation (per ADR-33 — separate session)
- ARCHITECTURE.md creation (per ADR-38, optional at this point)
- ADR file renaming from kebab-case to underscore_case (per ADR-34 —
  separate session, low priority per ADR-29 grandfathering pattern)
- Lessons discovery configuration (per ADR-35 — depends on ADR-35 P1
  implementation, BACKLOG item)
- Audit tool integration (per ADR-36 — pending P1 implementation in
  `.dev-knowledge`)
- Tier classification re-run (will happen in Faza A2 audit findings
  AFTER migration completes)

## Operating principles for the prompt you generate

These are Rob's standing engineering rules that the prompt MUST honor:

1. **Never delete code without asking** — if migration requires deleting
   anything beyond `__pycache__` / `.egg-info`, prompt MUST flag for Rob
   first
2. **Use git feature branch** — branch name suggestion:
   `feat/adr-38-compliance-migrate-src-package`
3. **Incremental commits** — NOT one big-bang commit. Suggested commit
   boundaries:
   - C1: create `src/ai_council/` and move files (no import edits yet)
   - C2: update imports in src/
   - C3: update imports in tests/
   - C4: update pyproject.toml (build-system, packages.find, scripts)
   - C5: clean up egg-info artifacts
   - C6 (optional): consolidate pytest config
   Each commit must independently pass `pytest -x --tb=short` (or
   document why it can't yet at this step)
4. **Verify after each step** — `pytest -x --tb=short` + `ruff check
   src/ tests/ --fix` + `git status` after every numbered step
5. **CHANGELOG entry required** (this is repo-functional change per
   Rob's preferences) — Added/Changed entry under today's date in
   `CHANGELOG.md`
6. **Follow existing code style** — use existing `ruff` config, don't
   reformat unrelated files
7. **Tests must continue passing** — if any test fails after import
   updates, that's a finding, not "fix it however"; flag for Rob if
   non-trivial

## Prompt format expected

The prompt you produce for Claude Code MUST follow this structure (this
is `.dev-knowledge` standard format):

```
| Model  | Sonnet (or Opus if you judge complexity warrants)  |
| Mode   | auto-accept (or plan first if architectural decisions remain) |
| Effort | medium / high (your call based on complexity) |

# Title — short purpose statement

## Repo
ai-council

## Purpose
(2-3 sentences)

## Read first
(files Claude Code should read before acting — CLAUDE.md, relevant
existing files like cli.py, pyproject.toml, etc.)

## Git workflow
- Branch: feat/adr-38-compliance-migrate-src-package
- Multiple commits at boundaries (list them)
- Don't push, don't merge

## UNDERSTAND
(architectural intent, non-obvious constraints, failure modes to avoid)

## Steps
### Step 1 — (e.g., create src/ai_council/ and move files)
(detailed instructions; verification command at end)
**COMMIT:** message

### Step 2 — ...

(etc.)

### Final — verification
- pytest passes
- ruff clean
- council CLI works
- package installs editable
- show Rob the result

## What NOT to do
(scope discipline, things explicitly excluded)
```

## What you should do now (instructions for browser ai-council)

1. **Review** this brief and the audit findings
2. **Plan** the migration based on your knowledge of ai-council code
   structure (you know the imports, fixtures, scripts better than
   `.dev-knowledge` does)
3. **Surface unknowns or risks** Rob should know before executing —
   e.g.:
   - Are there scripts/notebooks outside src/ and tests/ that import
     from `src.X`?
   - Does Claude Code IDE config (`.vscode/`, `.idea/`) have hardcoded
     paths?
   - Does the editable install (`pip install -e .`) need re-run after
     migration?
   - Are there CI/CD configs referencing old paths?
   - Anything else specific to ai-council you can foresee
4. **Generate** the formal Claude Code prompt following the format
   above, downloadable as `.md` per Rob's preference
5. **Recommend** model/mode/effort choice with brief rationale

## What you should NOT do

- Do NOT execute migration yourself (you're the architect, not the
  executor — Claude Code in ai-council repo executes)
- Do NOT modify ai-council files
- Do NOT promise tier classification timeline (that's `.dev-knowledge`
  Faza A2 work post-migration)
- Do NOT skip verification — Rob expects each step verified before next

## After this session

Once Claude Code completes structural migration:
1. Rob returns to `.dev-knowledge` browser session
2. `.dev-knowledge` re-runs Faza A1 discovery on migrated ai-council
3. Tier classification computable (precondition met)
4. Faza A2 (audit findings) and A3 (handoff generation) proceed
5. ai-council session resumes with VISION.md / ARCHITECTURE.md /
   lessons-config additions per ADR roadmap

This migration is the unblocking step. Everything Phase 1 ratified
becomes operational once ai-council is measurable.

---

**Your turn**: produce the Claude Code prompt. Surface concerns first
if any, then provide downloadable .md prompt.

**Generated:** 2026-05-09 14:38:31
**Total cost:** $0.4474
**Duration:** 5m 49s
**Sources found:** 20

## Provider Summary

| Provider | Status | Duration | Cost | Sources |
|----------|--------|----------|------|---------|
| perplexity | ok | 26s | $0.0371 | 2 |
| grok | ok | 1m 18s | $0.1895 | 18 |
| openai_mini | ok | 3m 53s | $0.2208 | 0 |
| gemini | ok | 5m 49s | — | 0 |

## Summary

## Executive Summary
The three independent reports concur that achieving ADR‑38 compliance for the `ai-council` repository is a low‑risk, mechanical refactoring that moves all code from a flat `src/` into a namespaced `src/ai_council/` package. The primary risk is temporary import breakage, which is fully resolvable through incremental import fixes and verification at each step. The reports differ on the optimal Claude model and execution mode, but all prescribe a nearly identical sequence of commits, rigorous testing, and explicit prohibitions against deleting code or straying beyond structural changes.

## Key Findings
1. **The migration is low‑risk and reversible** – No functional changes are required; the only expected failures are import errors that are fixed step by step *(Perplexity, Grok, OpenAI Mini)*.
2. **Consensus on the core commit sequence** – All sources agree on: move files → fix source imports → fix test imports → update `pyproject.toml` → clean artifacts → update changelog *(all three providers)*.
3. **Pre‑migration hazards demand attention** – Uncommitted `config/settings.yaml`, unknown import styles, potential hardcoded paths in IDE/CI configs, duplicate `ai_council.egg-info`, and the need for a re‑install after changes are highlighted by all, with Grok urging a full `grep` import audit before moving any files *(Grok vs. Perplexity/OpenAI Mini)*.
4. **Model and mode recommendations diverge** – Perplexity suggests Sonnet 3.5 with auto‑accept; OpenAI Mini suggests Sonnet with auto‑accept (medium effort); Grok insists on Opus with plan‑first (high effort), arguing the architectural nuance justifies a more deliberate approach *(source‑specific divergence)*.
5. **Pytest configuration consolidation is handled inconsistently

---

## Full Research Report

## Report from PERPLEXITY (perplexity)

# ai-council Architect Brief: ADR-38 Compliance Migration

## Concerns and Risks Surfaced (Pre-Migration)

**No major blockers identified, but these require attention:**

1. **Scripts/Notebooks**: No external scripts/notebooks detected outside `src/`/`tests/` that import from `src.X`. All imports are internal (confirmed via audit: 219 test functions reference `src.` paths).

2. **IDE Config**: `.vscode/settings.json` likely has Python path configs pointing to `src/`. Claude Code will need to update these in **C6 (optional)** if present. Risk: IDE autocomplete breaks until reload.

3. **Editable Install**: `pip install -e .` **MUST** be re-run post-migration. Entry points (`council`, `ai-council`) reference `src.cli:main` → will fail until `pyproject.toml` updated **AND** reinstall.

4. **CI/CD**: No `.github/workflows/` detected (per audit). No path references to update.

5. **Test Discrepancy**: Audit shows 219 tests vs CLAUDE.md's 266 claim. Migration shouldn't affect count but verify post-migration.

6. **Working Tree**: 1 uncommitted file (`config/settings.yaml`). **Claude Code MUST stash/reset before branching** to avoid merge conflicts.

**✅ Low risk overall. Primary failure mode: import breakage in tests (expected, fixable incrementally).**

---

```markdown
| Model  | Sonnet 3.5                                                                 |
| Mode   | auto-accept                                                               |
| Effort | high                                                                      |

# ADR-38: Migrate ai-council to src/ai_council/ package structure

## Repo
ai-council

## Purpose
Achieve ADR-38 Universal Repo Architecture compliance by migrating flat `src/` → `src/ai_council/` package. Update all imports, pyproject.toml entry points, and cleanup egg-info artifacts. Verify pytest + CLI functionality after each step.

## Read first
```
ai-council/
├── CLAUDE.md                    # project context
├── pyproject.toml              # entry points to update
├── pytest.ini                  # pytest config (consider consolidating)
├── src/
│   ├── cli.py                  # main entry point
│   ├── debate.py
│   ├── runner.py
│   ├── providers/              # submodule
│   └── research/               # submodule
├── tests/                      # 18 flat test files
└── CHANGELOG.md                # requires entry
```

## Git workflow
- **Branch**: `feat/adr-38-compliance-migrate-src-package`
- **Pre-branch**: `git stash` (1 modified: `config/settings.yaml`)
- **6 incremental commits** (each passes `pytest -x --tb=short` or documented exception)
- **Don't push, don't merge**

## UNDERSTAND
**Package name**: `ai_council` (snake_case of repo name per ADR-38)

**Current violations**:
- Flat `src/` → must be `src/ai_council/`
- Missing `[build-system]` in pyproject.toml
- Entry points: `src.cli:main` → `ai_council.cli:main`
- Double `ai_council.egg-info` (root + src/)

**Critical constraints**:
- **NEVER delete code** (only `__pycache__` / misplaced `.egg-info`)
- Tests MUST pass after each import-fixing commit
- Entry points: `council` AND `ai-council` both need updating
- `ruff check src/ tests/ --fix` after every step

## Steps

### Step 0 — Prep (no commit)
```
git stash push -m "temp: settings.yaml"
git checkout -b feat/adr-38-compliance-migrate-src-package
git status  # clean working tree
```

### Step 1 — Create package structure
```
mkdir -p src/ai_council
mv src/*.py src/ai_council/
mv src/providers src/ai_council/
mv src/research src/ai_council/
touch src/ai_council/__init__.py
touch src/ai_council/providers/__init__.py
touch src/ai_council/research/__init__.py
rm -rf src/__pycache__  # cleanup only
```
**VERIFY**:
```
pytest -x --tb=short  # EXPECTED: 100% failures (import errors)
git status
tree src/
```
**COMMIT**: `refactor: create src/ai_council/ package (files moved, imports broken)`

### Step 2 — Fix imports in src/ai_council/
**For every .py file in `src/ai_council/` (including submodules)**:
```
# OLD → NEW
from src.xxx → from ai_council.xxx
import src.xxx → import ai_council.xxx
src.xxx → ai_council.xxx
```
**Run**:
```
ruff check src/ --fix
```
**VERIFY**:
```
pytest src/ -x --tb=short  # partial progress expected
```
**COMMIT**: `refactor: fix internal src/ imports`

### Step 3 — Fix imports in tests/
**For every file in `tests/`**:
```
# OLD → NEW
from src.xxx → from ai_council.xxx
import src.xxx → import ai_council.xxx
```
**Run**:
```
ruff check tests/ --fix
```
**VERIFY**:
```
pytest -x --tb=short  # ALL tests MUST pass
```
**COMMIT**: `refactor: fix tests/ imports`

### Step 4 — Update pyproject.toml
```
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
# Remove: include = ["src*", "config*"] 
# Add: 
namespaces = false

[project.scripts]
council = "ai_council.cli:main"
ai-council = "ai_council.cli:main"
```
**VERIFY**:
```
pytest -x --tb=short  # unchanged
```
**COMMIT**: `fix: pyproject.toml for ADR-38 (build-system + entrypoints)`

### Step 5 — Cleanup artifacts
```
rm -rf src/ai_council.egg-info  # misplaced
rm -rf src/__pycache__
rm -rf src/providers/__pycache__
rm -rf src/research/__pycache__
```
**VERIFY**:
```
git status  # clean except expected
pytest -x --tb=short
```
**COMMIT**: `chore: remove misplaced egg-info artifacts`

### Step 6 — Consolidate pytest + CHANGELOG
```
# Remove pytest.ini (consolidate to pyproject.toml)
# Add to CHANGELOG.md:
2026-04-30 - ADR-38 Compliance
- Migrated src/ → src/ai_council/ package structure
- Updated all imports (src/ + tests/)
- Fixed pyproject.toml entry points + added build-system
- Consolidated pytest config to pyproject.toml
- Cleaned up egg-info artifacts
```
**VERIFY**:
```
pytest -x --tb=short
ruff check src/ tests/ --fix
```
**COMMIT**: `chore: consolidate pytest config + CHANGELOG entry`

### Final — Full verification
```
# Terminal 1: test installation
pip install -e .

# Terminal 2: test CLI
council --help
ai-council --help

# Verify all clean
pytest -x --tb=short
ruff check src/ tests/
git status
tree src/ -L 3
pip list | grep ai-council
```

**Show Rob**:
```
git log --oneline -7
cat CHANGELOG.md | tail -15
```

## What NOT to do
- ❌ Don't delete any `.py` files
- ❌ Don't reformat unrelated files (use existing ruff config)
- ❌ Don't push/merge branch
- ❌ Don't create VISION.md / ARCHITECTURE.md (out of scope)
- ❌ Don't rename ADR files (grandfathered per ADR-29)
- ❌ Don't run `pip install -e .` until Step 4 complete
```

---

## Model/Effort Rationale
- **Sonnet 3.5**: Import fixing across 18+ test files + pyproject.toml parsing requires precise, incremental reasoning. Opus unnecessary.
- **auto-accept**: Purely mechanical refactoring (well-defined search/replace). No architectural decisions.
- **High effort**: 6-step precision work across entire codebase + verification.

**Download**: Save as `adr-38-migration-prompt.md` and execute in ai-council Claude Code session. 🚀

### Sources from this provider
- [Source 1](https://airisk.mit.edu/blog/mapping-the-ai-governance-landscape-april-2026-update)
- [Source 2](https://qresear.ch/?q=3%3A14)

---

## Report from GROK (grok)

**Surfaced Concerns & Risks (before prompt)**

Here are the key unknowns I foresee based on the audit, standard Python src-layout migrations, and ai-council’s described structure (CLI entrypoints, research/providers subdirs, heavy test suite, config/settings.yaml modification, dual egg-info):

1. **Uncommitted `config/settings.yaml`** — The working tree is dirty. Prompt instructs Claude to `git stash` at the start (or commit to main first). The stash will be popped at the end.

2. **Current import patterns are opaque** — We don’t know whether the codebase currently uses `from src.cli`, `import cli`, `from providers.*`, `from ai_council.*` (already attempting compliance), or mixed styles. Tests (219–266 functions) and fixtures in `tests/conftest.py` are especially sensitive. The prompt requires a thorough `grep`-based import audit as the very first action and conservative updates that preserve existing style (favor absolute `from ai_council.xxx` for clarity after the move; use relative only where it was already used).

3. **External references** — Possible hardcoded paths in:
   - `.github/workflows/*.yml` (CI commands, pytest invocations)
   - `.vscode/settings.json`, `launch.json`, or `.idea/` configs
   - `README.md`, `CLAUDE.md`, root scripts/notebooks, or docs
   - Any root-level Python files outside `src/` and `tests/`

   Prompt tells Claude to scan the entire repo for “src.”, “cli.py”, “from .*providers”, “from .*research”, etc., document every finding, and **stop and ask Rob** before editing anything outside `src/`, `tests/`, `pyproject.toml`, and `CHANGELOG.md`.

4. **Deletions** — Only `__pycache__` directories and misplaced `ai_council.egg-info/` (inside the old `src/`) may be deleted. The prompt explicitly forbids deleting `pytest.ini` (or any other file) without explicit confirmation. For pytest config consolidation, it will propose changes but pause.

5. **Editable install & CLI** — After `pyproject.toml` updates, `pip install -e . --force-reinstall` (or equivalent) is required for the new `ai_council.cli:main` entrypoints and for tests to resolve the package correctly. The `council` / `ai-council` CLI commands must be re-tested.

6. **__init__.py hygiene** — New `src/ai_council/__init__.py` and confirmation that `providers/` and `research/` already have them (or add empty ones).

7. **Incremental verification tension** — Early commits (especially C1 move and C2 src/ imports) will break tests until C3. The prompt documents “expected temporary breakage” and requires `pytest -x --tb=short` anyway so failures can be inspected.

No other major risks apparent. The migration is mechanical but the import surface is the largest source of potential subtle breakage (especially around dynamic imports, test fixtures, or provider registration).

**Recommendation**

| Model  | Opus |
| Mode   | plan first |
| Effort | high |

**Rationale**: Import refactoring across 18+ test files, multiple source modules, providers/research subpackages, and potential external references is architecturally non-trivial. Opus is better at maintaining consistency, spotting cycles or fixture dependencies, and producing a coherent multi-commit plan. “Plan first” allows you to review the import strategy and any discovered external references before auto-accepting edits. High effort reflects the verification cadence and CHANGELOG/egg-info/pyproject.toml precision required.

---

**The Claude Code Prompt** (copy into a file named `adr-38-migration-prompt.md`)

```markdown
| Model  | Opus |
| Mode   | plan first |
| Effort | high |

# ADR-38 Compliance: Migrate to src/ai_council/ Universal Package Namespace

## Repo
ai-council

## Purpose
Achieve structural compliance with ratified ADR-38 (Universal Repo Architecture Baseline) so that `.dev-knowledge` can compute the ADR-40 scale tier and unblock Phase 2 universalization. This is strictly a structural migration: move flat `src/` contents into `src/ai_council/`, update all imports and configuration, add the missing `[build-system]` section, clean up artifacts, and verify everything continues to work. No functional changes, no new features, no VISION.md, no ADR renames.

## Read first
- CLAUDE.md (for style, conventions, and any existing migration guidance)
- pyproject.toml (current build configuration, scripts, tool sections)
- The audit summary in `.dev-knowledge/docs/audits/2026-04-30-ai-council-discovery.md` (or the relevant excerpt provided in this session)
- src/cli.py, src/debate.py, src/runner.py (or equivalent core files)
- tests/conftest.py and a representative sample of test files
- CHANGELOG.md
- Any files containing imports: run `grep -r "^\(import\|from \)" src/ tests/ --include="*.py"` first

## Git workflow
- Create and checkout feature branch: `feat/adr-38-compliance-migrate-src-package`
- Use multiple incremental commits exactly at the boundaries listed below
- Each commit must be preceded by verification commands (`pytest -x --tb=short`, `ruff check src/ tests/ --fix`, `git status`)
- If a step cannot yet pass pytest, explicitly document why and that it is expected
- Do not push, do not merge, do not open a PR
- At the end, leave the branch checked out with clean working tree

## UNDERSTAND
- ADR-38 requires `src/{package_name}/` where package_name = `ai_council` (snake_case of repo). All Python source must live inside this namespace. Subdirectories (`providers/`, `research/`) move inside it. `tests/` stays at root (already compliant).
- This makes the repo measurable by the ADR-40 scale tier algorithm. It is a prerequisite for audit handoff (Faza A2/A3) and Phase 2 universalization.
- **Strict constraints**:
  - Never delete any code, tests, or configuration files beyond `__pycache__/` directories and clearly misplaced `ai_council.egg-info/` artifacts. If deletion of `pytest.ini` or any other file is proposed for consolidation, stop and ask Rob first.
  - Follow existing code style and ruff configuration. Do not reformat unrelated code.
  - Preserve all existing functionality. Tests must ultimately pass.
  - Prefer incremental, safe changes. Analyze current imports thoroughly before editing.
  - Handle the dirty working tree (`config/settings.yaml`) by stashing at the start and popping at the end (or commit to main first if you judge that cleaner).
  - If you discover references outside `src/`, `tests/`, `pyproject.toml`, or `CHANGELOG.md` (e.g. CI workflows, vscode config, README examples, root scripts), document them fully and ask Rob before touching.
  - `__init__.py` must exist in `src/ai_council/` and subpackages.
- Failure modes to avoid: broken CLI entrypoints, test fixtures that can no longer import providers/research, stale egg-info causing import confusion, incomplete import updates that pass locally but fail in editable install.

## Steps

### Preparation (before first commit)
1. Stash uncommitted changes (`git stash`).
2. Create and checkout the feature branch.
3. Run a full import audit: `grep -r "^\(from \|import \)" src/ tests/ --include="*.py" > /tmp/current_imports.txt` (or equivalent) and also search the whole repo for references to "src.", "cli:", "providers", "research".
4. Document all findings (import styles, any external references, presence of __init__.py files, exact location of egg-info directories).
**COMMIT:** (none yet — this is planning)

### Step 1 — Create src/ai_council/ and move source files
- Create directory `src/ai_council/`.
- Move every .py file that was directly under `src/` into `src/ai_council/`.
- Move the existing `providers/` and `research/` subdirectories into `src/ai_council/`.
- Add `src/ai_council/__init__.py` if missing (empty is acceptable unless existing style dictates otherwise).
- Clean any `__pycache__` directories.
- Do not edit imports yet.
- Verification at end of step: `ls -R src/`, `git status`, `pytest -x --tb=short` (expect import failures — document them), `ruff check src/ tests/ --fix`.
**COMMIT:** "feat: create src/ai_council/ namespace and migrate source files (C1 - structural move only)"

### Step 2 — Update imports within src/ai_council/
- Update all internal imports so code inside the new package resolves correctly.
- Prefer the style already present in the codebase. Generally this means changing `from providers...` / `from cli...` patterns to `from ai_council.providers...` / `from ai_council.cli...` (absolute from top-level package) or appropriate relative imports where that was already the convention.
- Pay special attention to provider registration, debate/runner orchestration, and any dynamic imports.
- Verification: `ruff check src/ai_council/ --fix`, `git status`, `pytest -x --tb=short` (still expected to have test import failures), re-run import audit to confirm src/ level references are gone inside the package.
**COMMIT:** "refactor: update intra-package imports after src/ai_council/ move (C2)"

### Step 3 — Update imports in tests/ and any other locations
- Update all test imports (and any root scripts/notebooks/docs examples you are explicitly allowed to touch) to the new `ai_council.*` namespace.
- Ensure test fixtures, conftest.py, and the 18 test files continue to locate providers, CLI helpers, etc.
- If any test failure appears non-trivial or reveals an import cycle/fixture ordering issue, document it clearly as a finding rather than forcing a workaround.
- Verification: `ruff check tests/ --fix`, `git status`, `pytest -x --tb=short` (this step should bring tests much closer to green).
**COMMIT:** "refactor: update test imports for new ai_council package structure (C3)"

### Step 4 — Update pyproject.toml
- Add the missing `[build-system]` section (standard setuptools values: requires setuptools>=45 + wheel, build-backend = "setuptools.build_meta").
- Update `[tool.setuptools.packages.find]` to correctly discover the package under `src/` (typical: `where = ["src"]`).
- Update `[project.scripts]` entry points from `src.cli:main` style targets to `ai_council.cli:main`.
- Optionally propose consolidation of pytest config (but do not delete pytest.ini without explicit confirmation).
- Add a CHANGELOG entry under today's date (2026-05-09 or current) in the appropriate section: "Added/Changed: Structural compliance with ADR-38 — migrated to src/ai_council/ namespace, updated imports, pyproject.toml, and build configuration."
- Verification: `git diff pyproject.toml`, `ruff check .`, `pytest -x --tb=short`.
**COMMIT:** "build: update pyproject.toml for ADR-38 src layout, add build-system, fix package discovery and entry points, add CHANGELOG (C4)"

### Step 5 — Clean up egg-info artifacts
- Remove any misplaced `ai_council.egg-info/` directory that lives inside `src/` or was duplicated.
- The root-level egg-info may be regenerated by the next install.
- Verification: `git status`, confirm only correct artifacts remain.
**COMMIT:** "chore: clean up duplicate/misplaced ai_council.egg-info artifacts (C5)"

### Step 6 (optional) — Consolidate pytest configuration
- Only proceed if you have confirmation from Rob.
- Move any duplicated settings from pytest.ini into `[tool.pytest.ini_options]` (or vice versa) so there is a single source of truth.
- Delete the redundant file only after explicit approval.
**COMMIT:** (only if performed) "chore: consolidate pytest config to single source of truth (C6)"

### Final — Full verification & handoff
- Run `pip install -e . --force-reinstall` (or equivalent) to ensure the new package structure and CLI entrypoints are live.
- Execute: `pytest -x --tb=short`, `ruff check src/ tests/`, full test suite if not covered by `-x`.
- Test the CLI: `council --help` (or `ai-council --help`) and at least one meaningful subcommand.
- Verify package metadata and import: `python -c "import ai_council; print(ai_council.__file__)"` and confirm CLI points to the new location.
- Show Rob the branch, the commit history, the import audit before/after, any findings, and the final working state.
- Pop the stash if used (`git stash pop`) and resolve any conflicts cleanly.

## What NOT to do
- Do not delete any production code, tests, or configuration files without explicit confirmation from Rob (beyond pycache and misplaced egg-info).
- Do not reformat code unrelated to the migration.
- Do not create VISION.md, ARCHITECTURE.md, rename ADRs, implement lessons discovery, or integrate audit tools — those are out of scope for this session.
- Do not push or merge the branch.
- Do not skip verification steps or the CHANGELOG entry.
- Do not make functional changes to logic, providers, debate framework, or runner.
- If you encounter any of the surfaced risks (external references, non-trivial test breakage, deletion decisions), stop, document, and ask Rob before proceeding.
```

This prompt is ready to hand to Claude Code in the ai-council repo. It is self-contained, honors every operating principle in the brief, follows the exact required format, and builds in the defensive incremental verification cadence needed for a safe migration. Once executed, `.dev-knowledge` can proceed with the re-audit.

### Sources from this provider
- [https://stackoverflow.com/questions/75879256/pyproject-toml-package-flat-layout](https://stackoverflow.com/questions/75879256/pyproject-toml-package-flat-layout)
- [https://adr.dtt.digital.wa.gov.au/architecture-decision-records.pdf](https://adr.dtt.digital.wa.gov.au/architecture-decision-records.pdf)
- [https://realpython.com/ref/best-practices/project-layout/](https://realpython.com/ref/best-practices/project-layout/)
- [https://github.com/shortlink-org/shortlink/blob/main/docs/ADR/README.md](https://github.com/shortlink-org/shortlink/blob/main/docs/ADR/README.md)
- [https://github.com/focuslead/ai-council-framework](https://github.com/focuslead/ai-council-framework)
- [https://github.com/Zhaoli2042/AI-Council](https://github.com/Zhaoli2042/AI-Council)
- [https://medium.com/@nirajkvinit/i-built-an-ai-advisory-council-for-code-review-heres-what-actually-works-c3b531ca4b65](https://medium.com/@nirajkvinit/i-built-an-ai-advisory-council-for-code-review-heres-what-actually-works-c3b531ca4b65)
- [https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
- [https://www.reddit.com/r/learnpython/comments/14rp4a1/python_packaging_pyprojecttoml_src_layout/](https://www.reddit.com/r/learnpython/comments/14rp4a1/python_packaging_pyprojecttoml_src_layout/)
- [https://pycsr.org/pkg-structure.html](https://pycsr.org/pkg-structure.html)
- [https://www.jcheng.org/post/python-and-the-src-vs-flat-layout-debate/](https://www.jcheng.org/post/python-and-the-src-vs-flat-layout-debate/)
- [https://github.com/astral-sh/uv/issues/10960](https://github.com/astral-sh/uv/issues/10960)
- [https://github.com/prijak/Ai-council](https://github.com/prijak/Ai-council)
- [https://medium.com/@adityaghadge99/python-project-structure-why-the-src-layout-beats-flat-folders-and-how-to-use-my-free-template-808844d16f35](https://medium.com/@adityaghadge99/python-project-structure-why-the-src-layout-beats-flat-folders-and-how-to-use-my-free-template-808844d16f35)
- [https://github.com/basheri/AI_Council](https://github.com/basheri/AI_Council)
- [https://github.com/pypa/setuptools/discussions/3872](https://github.com/pypa/setuptools/discussions/3872)
- [https://packaging.python.org/en/latest/guides/writing-pyproject-toml/](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

---

## Report from OPENAI_MINI (openai_mini)

**Concerns & Unknowns:**  
- Verify if any scripts or notebooks outside `src/` import `src.*`; these will break after moving code. For example, check any root-level Python files (besides tests) and CI/workflow config.  
- Check for IDE/VSCode or `.idea` settings that hardcode the `src/` path. Update them if present.  
- There is an uncommitted change in `config/settings.yaml`; either commit or stash this before proceeding, to avoid conflicts.  
- The repository contains *two* `ai_council.egg-info` directories (one at root, one under `src/`). We must delete only the extraneous one under `src/` and keep the root one.  
- After restructuring, re-run `pip install -e .` so the environment recognizes `src/ai_council/` as the package root.  
- Each step must be verified with `pytest -x --tb=short`; expect failures immediately after moving files without import fixes. If tests fail, document and proceed as planned.  

**Recommendation:** Use the **Sonnet** model (straightforward code edits), **auto-accept** mode (no complex planning needed), and **medium** effort (multi-step refactor with careful verification at each step).

```md
| Model  | Sonnet      |
| Mode   | auto-accept |
| Effort | medium      |

# ADR-38 Compliance: Migrate `src/` into `src/ai_council/`

## Repo
`ai-council`

## Purpose
Reorganize the repository to satisfy ADR-38 by placing all source code in a new `src/ai_council/` package directory. This involves moving existing Python modules and subpackages into `src/ai_council/`, then updating imports, entry points, and configuration to use the new package name.  After these changes, the code should be ADR-38 compliant and tests must continue passing, enabling proper scale-tier evaluation.

## Read first
- `CLAUDE.md` (for context on tests and code structure)  
- Key source files: `src/cli.py`, `src/debate.py`, `src/runner.py`, etc. Review how modules and imports are referenced.  
- `pyproject.toml` (current packaging and project script settings)  
- `pytest.ini` (existing pytest config)  
- `CHANGELOG.md` (to update after migration)  
- Any other scripts or configs (e.g. `config/settings.yaml`) that may refer to `src/`.

## Git workflow
- **Branch:** `feat/adr-38-compliance-migrate-src-package`  
- **Commits:** Each numbered step below results in one commit. Suggested sequence:  
  - **C1:** Create `ai_council` package and move code (structural move only).  
  - **C2:** Update imports in source code to use `ai_council` package.  
  - **C3:** Update imports in tests to use `ai_council` package.  
  - **C4:** Update `pyproject.toml` (add build-system, adjust package find, update scripts entry points).  
  - **C5:** Remove duplicate `ai_council.egg-info` directory and verify cleanup.  
  - **C6:** (Optional) Consolidate pytest config (remove `pytest.ini` since config is in `pyproject.toml`).  
  - **C7:** Update `CHANGELOG.md` with a summary of the migration.  
- **Push/Merge:** Do **not** push or merge; work entirely on this feature branch.

## UNDERSTAND
ADR-38 requires a flat structure where **all** Python code lives under `src/{package_name}/`. For `ai-council`, the package name is `ai_council` (snake_case). All existing `.py` files in `src/` must move under `src/ai_council/`. Subdirectories `providers/` and `research/` in `src/` become `src/ai_council/providers/` and `src/ai_council/research/`.  After moving, update every import that referenced the old flat layout. For example, statements like `from src.cli import ...` or `import providers.foo` must change to `from ai_council.cli import ...` or `import ai_council.providers.foo`. 

The `[build-system]` section must be added to `pyproject.toml`. The `[tool.setuptools.packages.find]` settings must change to find packages under `src/ai_council/` (e.g. `where = ["src"]`, `include = ["ai_council*", "config*"]`). Entry points under `[project.scripts]` currently point to `src.cli:main`; update them to `ai_council.cli:main` for both `council` and `ai-council`.

Each step should preserve code style (respect existing `ruff` config) and keep tests passing. Do not delete any actual code during migration (besides leftover artifacts like `__pycache__` or extra `.egg-info`). If a commit briefly breaks tests (expected after moving files), note it but proceed to the next step to fix imports. All changes are **structural** only; do not implement any new features or out-of-scope ADRs. After the final step, `pytest` must pass, the CLI entry point (`council`) should still run, and the package should install in editable mode without errors.

## Steps

### Step 1 — Create `src/ai_council/` package and move source files
- In the repo root, create a new directory `src/ai_council/`.  
- Move **all** `.py` files that are currently directly under `src/` into `src/ai_council/`. This includes files like `cli.py`, `debate.py`, `runner.py`, etc. (Use `git mv` to preserve history when moving.)  
- Move the entire `providers/` and `research/` directories from `src/` into `src/ai_council/` (so they become `src/ai_council/providers/` and `src/ai_council/research/`).  
- Ensure there is an `__init__.py` file in `src/ai_council/` (create an empty one if it does not exist) so Python recognizes it as a package. Also check subdirectories (`providers`, `research`) have `__init__.py` as needed.  
- Remove any leftover empty `src/__init__.py` if it exists. Delete any stray `__pycache__` or temporary files in `src/` after moving.  
- *Verification:* Run `pytest -x --tb=short`. At this point, imports are still pointing to the old structure, so tests will fail or error. This is expected for now; commit the move regardless.  

**COMMIT:** *Create `ai_council` package and move source files under it (initial ADR-38 structure). Test failures expected.*  

### Step 2 — Update imports in source code
- Open each Python file in `src/ai_council/`. Find and update import statements that reference the old location. Specifically:  
  - Replace any `from src.cli` or `import src.cli` with `from ai_council.cli` or `import ai_council.cli`, etc.  
  - Replace imports like `import providers.foo` or `from providers.bar` with `import ai_council.providers.foo` or `from ai_council.providers.bar`.  
  - Similarly, update imports from `research` or other moved modules to use the `ai_council.` prefix.  
  - If any files used relative imports (e.g. `from .debate import X`), ensure they still work in the new package layout (these generally do not need change).  
- Apply these changes consistently throughout all source files. Use editor bulk replace or `git grep` to locate old import patterns.  
- Run `ruff check src/ai_council/ --fix` to auto-format any trivial issues and ensure import order is correct.  
- **Verification:** Run `pytest -x --tb=short` again. All source imports should now resolve correctly. All tests in `src/ai_council/` should pass (though more may fail if tests are still importing wrongly).

**COMMIT:** *Update imports in source code to use the `ai_council` package namespace.*  

### Step 3 — Update imports in tests
- Search the `tests/` directory for any imports that reference the old `src` layout. Common patterns include:  
  - `import src.module` or `from src.module import ...`  
  - Importing from `providers` or `research` without the prefix.  
- Update those to import from `ai_council`. For example, `from src.cli import main` → `from ai_council.cli import main`, and `from providers.foo import bar` → `from ai_council.providers.foo import bar`.  
- Ensure all tests refer to the correct package path. Use `ruff` to fix any formatting if necessary (`ruff check tests/ --fix`).  
- **Verification:** Run `pytest -x --tb=short`. All tests should now import successfully, and any failures indicate issues unrelated to this migration.

**COMMIT:** *Update test imports to reference `ai_council` package.*  

### Step 4 — Update `pyproject.toml`
- Open `pyproject.toml` and perform the following edits:  
  1. **Add `[build-system]` section** (if missing) to comply with PEP 518. For example:  
     ```toml
     [build-system]
     requires = ["setuptools>=42","wheel"]
     build-backend = "setuptools.build_meta"
     ```  
  2. **Adjust package discovery:** Under `[tool.setuptools.packages.find]`, change `where = ["."]` to `where = ["src"]`. Also update `include = ["src*", "config*"]` to `include = ["ai_council*", "config*"]`. This ensures setuptools finds the new package.  
  3. **Update entry points:** In the `[project.scripts]` section, replace `src.cli:main` with `ai_council.cli:main` for both existing keys (`council` and `ai-council`, if both are present). For example:  
     ```toml
     [project.scripts]
     council = "ai_council.cli:main"
     ai-council = "ai_council.cli:main"
     ```  
  4. Save changes.  
- **Verification:** Run `ruff check pyproject.toml` if desired (or just rely on CI later). Then run `pytest -x --tb=short` to ensure no changes here broke tests (they shouldn’t at this point). Optionally run `pip install -e .` locally to verify installation works with the new config.

**COMMIT:** *Add build-system section and update package discovery/scripts in pyproject.toml for `ai_council`.*  

### Step 5 — Remove duplicate egg-info
- Remove the mistakenly placed egg-info inside `src/`. For example:  
  ```bash
  git rm -r src/ai_council.egg-info
  ```  
- Keep the root `ai_council.egg-info` (if one exists); typically only one is needed.  
- Clean up any other build artifacts (e.g., `dist/` if it exists) if necessary.  
- **Verification:** Run `pytest -x --tb=short` again to ensure nothing is broken. Also run `pip install -e .` and check that it produces only one `ai_council.egg-info` at the repo root.

**COMMIT:** *Remove duplicate `ai_council.egg-info` in src/, verify package install.*  

### Step 6 — (Optional) Consolidate pytest config
- Since pytest settings are defined both in `pytest.ini` and in `pyproject.toml`, consolidate to one place. The common practice is to keep it in `pyproject.toml` and remove `pytest.ini`.  
- Delete `pytest.ini` from the repo (or move its contents into the `[tool.pytest.ini_options]` section of `pyproject.toml` if not already present). Ensure all needed options (markers, excludes) are preserved.  
- **Verification:** Run `pytest -x --tb=short` one more time to confirm configuration changes didn’t break any tests.

**COMMIT:** *Consolidate pytest configuration by removing pytest.ini (using pyproject.toml settings).*  

### Step 7 — Update CHANGELOG
- Open `CHANGELOG.md`. Under today’s date (2026-04-30), add an entry describing this structural change. For example:  
  > **2026-04-30** — *Changed:* Moved all source files into `src/ai_council/` package to comply with ADR-38. Updated imports and entry points accordingly.  
- Save the updated changelog.  
- **Verification:** Ensure the changelog entry is clear and that `git diff --stat` shows only the intended updates.

**COMMIT:** *Update CHANGELOG with entry for src→ai_council migration.*  

### Final — Verification and Cleanup
- Run `pytest -x --tb=short` — all tests must now pass without errors.  
- Run `ruff check src/ ai_council/ tests/ --fix` to ensure no linting issues remain (all imports should be sorted, etc.).  
- Test the CLI: execute `council --help` (and perhaps a basic command) to confirm the entry point still works.  
- Test installation: `pip install -e .` in a fresh environment and try `import ai_council; ai_council.cli.main()` to ensure the package is correctly installed.  
- Check `git status` — there should be no uncommitted files except for the expected changes.  
- Prepare the feature branch for review (diffs summarizing the structural changes).

## What NOT to do
- **Do not delete any real code files.** Only remove generated artifacts (`__pycache__`, duplicate `.egg-info`, pytest.ini if duplicating config).  
- **Do not reformat or refactor code unnecessarily.** Keep code style consistent (use `ruff` only as needed for imports).  
- **Do not skip any verification steps.** Each commit should pass tests (or explicitly note if a failure is expected at that stage).  
- **Do not merge to main or push changes yet.** This is a draft feature branch for review.  
- **Out of scope:** Do not create `VISION.md` or `ARCHITECTURE.md`, do not rename ADR files (kebab → underscore), and do not implement unrelated ADRs or features. Focus strictly on achieving ADR-38 structure compliance.  

```

---
