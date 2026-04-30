# ai-council — Audit Discovery (Faza A1)

**Date:** 2026-04-30
**Target repo:** ai-council
**Target path:** C:/Users/1028120/Documents/Dev/ai-council
**HEAD SHA:** 47bea6f67f81eac4f2d0ebddc907546fc8514463
**Branch:** main
**Auditor:** .dev-knowledge Claude Code session (manual, audit tool not yet implemented)
**Phase:** A1 Discovery (raw observations, no findings interpretation)

---

## Repo state snapshot

- **HEAD:** 47bea6f67f81eac4f2d0ebddc907546fc8514463
- **Branch:** main
- **Recent commits (top 5):**
  - `47bea6f` fix: ensure Sources column visible in narrow terminals; add source count to summary
  - `2a5fa68` Merge fix/research-citation-parsing: citation parsing for Grok and Gemini
  - `de52f29` fix: extract citations from content block annotations (Grok) and markdown links (Gemini)
  - `3e5c6e4` fix: update default Grok research model to grok-4.20-reasoning
  - `0316825` docs: record synthesizer switch to Gemini in ADR-01
- **Working tree:** modified — `config/settings.yaml` has uncommitted changes (1 file)

---

## 1. Architecture compliance observations (per ADR-38)

### Mandatory directory presence

| Element | Present | Detail |
|---|---|---|
| `src/` at root | YES | Contains `__init__.py` (0 bytes) + Python modules directly |
| `src/{package_name}/` | NO | No `src/ai_council/` subdirectory — source files live directly at `src/` level; pyproject.toml entry point is `src.cli:main` |
| `tests/` at root | YES | Flat (no subdirectories); 18 test files + `__init__.py` |
| `pyproject.toml` | YES | 64 lines; see section details below |
| `README.md` | YES | 233 lines |
| `VISION.md` | NO | Not present at root |
| `CHANGELOG.md` | YES | 47 lines |
| `ARCHITECTURE.md` | NO | Not present at root |
| `docs/` | YES | Contains `decisions/`, `handoffs/`, `archive/`, `HANDOFF.md`, `COUNCIL_QUESTION_GUIDE.md` |
| `docs/decisions/` | YES | 7 ADR files + `README.md` + `transcripts/` subdirectory |
| `.gitignore` | YES | 37 lines |

### Additional non-ADR-38 directories observed at root

| Directory | Present | Detail |
|---|---|---|
| `config/` | YES | `settings.yaml`, `config_loader.py`, `__init__.py` — source-controlled Python package |
| `scripts/` | YES | `check.ps1`, `council-ask.ps1` |
| `tasks/` | YES | `todo.md`, `lessons.md` |
| `output/` | YES | Listed in root; CLAUDE.md states gitignored |
| `council_inbox/` | YES | Listed in root; CLAUDE.md states gitignored |
| `ai_council.egg-info` | YES | At repo root (standard location for editable installs) |

### pyproject.toml section inventory

| Section | Present |
|---|---|
| `[project]` | YES — name, version, description, requires-python, dependencies |
| `[project.optional-dependencies]` | YES — dev group |
| `[project.scripts]` | YES — `council` and `ai-council` entry points |
| `[tool.setuptools.packages.find]` | YES — `where = ["."]`, `include = ["src*", "config*"]` |
| `[tool.pytest.ini_options]` | YES |
| `[tool.coverage.run]` | YES |
| `[tool.coverage.report]` | YES |
| `[tool.mypy]` | YES |
| `[tool.ruff]` | YES |
| `[tool.ruff.lint]` | YES |
| `[tool.ruff.format]` | YES |
| `[build-system]` | **NO** |

### Additional configuration observation

- `pytest.ini` exists at root (37-equivalent lines) with same content as `[tool.pytest.ini_options]` in `pyproject.toml` — two pytest config sources coexist.

### src/ internal structure

```
src/
├── __init__.py          (0 bytes)
├── ai_council.egg-info/ (inside src/ — unusual location; typically at root or src/{pkg}/)
├── cli.py
├── debate.py
├── healthcheck.py
├── inbox.py
├── metrics.py
├── mode_detector.py
├── models.py
├── orchestrator.py
├── output.py
├── policy.py
├── providers/           (subdirectory with __init__.py)
├── research/            (subdirectory with __init__.py + nested providers/)
├── runner.py
└── synthesis.py
```

Note: `ai_council.egg-info` also appears at repo root — may be present in both locations or a shell listing artifact. Root listing showed it; `ls -la src/` also listed it inside src/.

---

## 2. Raw metrics (per ADR-38 + ADR-40)

### Module count

Per ADR-38 definition: top-level subdirectory inside `src/{package_name}/` containing `__init__.py` and 1+ Python files.

Structural note: ai-council has no `src/ai_council/` subdirectory. The package lives directly at `src/`. Modules are interpreted as top-level subdirectories inside `src/` that contain `__init__.py` + 1+ Python files.

| Module | `__init__.py` | Python files |
|---|---|---|
| `src/providers/` | YES | 5 files: base.py, anthropic.py, gemini.py, openai_provider.py, xai.py, deepseek.py |
| `src/research/` | YES | 8 files: models.py, provider.py, display.py, merger.py, cache.py, runner.py, output.py + nested `providers/` subdirectory |

**Total modules detected: 2**

Not counted as top-level modules:
- `src/research/providers/` — nested inside `research/`, not top-level in `src/`
- Direct Python files in `src/` (cli.py, debate.py, etc.) — package-level utilities per ADR-38

Calibration baseline in ADR-40 estimated 8 modules for ai-council. Actual count under strict ADR-38 definition yields 2.

### Test count

Method: `grep -rE "^def test_|^    def test_"` across `tests/test_*.py` files.

| Test file | Function count |
|---|---|
| test_mode_system.py | 33 |
| test_research.py | 30 |
| test_inbox.py | 25 |
| test_base_provider.py | 25 |
| test_policy.py | 19 |
| test_cli.py | 15 |
| test_output.py | 14 |
| test_runner.py | 13 |
| test_dual_output.py | 12 |
| test_metrics.py | 11 |
| test_config.py | 11 |
| test_models.py | 6 |
| test_debate.py | 3 |
| test_synthesis.py | 1 |
| test_api_keys.py | 1 |
| test_providers.py | 0 |
| test_integration.py | 0 |
| test_healthcheck.py | 0 |

**Total test functions (grep): 219**

Discrepancy note: CLAUDE.md states "266 unit tests." Difference of 47. Possible causes: class-based tests (`def test_*` inside `Test*` classes) with non-4-space indentation not captured by grep; tests in test_providers.py (19,914 chars, 0 grep hits) suggest class-based test structure; test_integration.py and test_healthcheck.py also show 0 grep hits.

### TCR

Per ADR-38 inclusion rules (src/, tests/, root docs, docs/).
Excluded: `__pycache__`, `.egg-info`, lock files, binary assets.

| Metric | Value |
|---|---|
| Total chars | 357,706 |
| Estimated tokens (chars / 4) | 89,426 |
| Files counted | 70 |

Top 10 files by character count:

| File | Chars |
|---|---|
| tests/test_research.py | 42,679 |
| tests/test_providers.py | 19,914 |
| src/cli.py | 18,788 |
| tests/test_debate.py | 17,063 |
| tests/test_mode_system.py | 13,915 |
| src/debate.py | 10,610 |
| src/output.py | 10,275 |
| tests/test_runner.py | 9,857 |
| README.md | 9,561 |
| tests/test_inbox.py | 9,511 |

Calibration baseline in ADR-40 estimated ~30k tokens for ai-council. Actual measurement: 89,426 tokens (~3x higher than estimate).

### Computed tier (per ADR-40)

Inputs:
- `tcr_tokens` = 89,426
- `tests_count` = 219
- `modules_count` = 2

Computation:
```
tcr_k = 89.426
score = 100 - 12*ln(89.426) - 8*ln(219) - 15*ln(2)
      = 100 - 53.92 - 43.11 - 10.40
      = -7.43 → clamped to 0.0
```

| Signal | Value | Contribution |
|---|---|---|
| TCR component | 89.426k tokens | -53.9 |
| Tests component | 219 functions | -43.1 |
| Modules component | 2 modules | -10.4 |
| **Raw score** | **-7.4** | clamped to **0.0** |

**Score: 0.0**
**Tier: L** (score < 35 → L per ADR-40 `classify_tier` with no current_tier)

Calibration baseline divergence: ADR-40 calibration table estimated ai-council at score ~52, Tier M. Actual computed score: 0.0, Tier L. Primary driver of divergence: TCR estimate was ~30k tokens; actual is 89k tokens. Secondary driver: module count estimate was 8; actual is 2 (due to structural non-compliance with ADR-38 `src/{package_name}/` convention).

---

## 3. VISION.md inspection (per ADR-33)

**VISION.md is not present at ai-council root.**

No VISION.md file found. Observation ends here for this section.

---

## 4. File naming sample (per ADR-34)

No compliance judgment — raw observations only.

### Root files
| File | Pattern observed |
|---|---|
| CHANGELOG.md | UPPERCASE.md |
| README.md | UPPERCASE.md |
| CLAUDE.md | UPPERCASE.md |
| pyproject.toml | lowercase, no extension variant (ecosystem standard) |
| pytest.ini | lowercase.ini |
| .gitignore | dotfile |
| ai-council.code-workspace | kebab-case.code-workspace |

### src/ files (sample — 5)
| File | Pattern observed |
|---|---|
| __init__.py | dunder (reserved) |
| cli.py | snake_case.py |
| debate.py | snake_case.py |
| healthcheck.py | snake_case.py |
| inbox.py | snake_case.py |

### tests/ files (sample — 5)
| File | Pattern observed |
|---|---|
| test_api_keys.py | test_snake_case.py |
| test_base_provider.py | test_snake_case.py |
| test_cli.py | test_snake_case.py |
| test_config.py | test_snake_case.py |
| test_debate.py | test_snake_case.py |

### docs/ files (top-level)
| File | Pattern observed |
|---|---|
| COUNCIL_QUESTION_GUIDE.md | UPPERCASE_WITH_UNDERSCORES.md |
| HANDOFF.md | UPPERCASE.md |

### docs/decisions/ ADR files (all 7)
| File | Pattern observed |
|---|---|
| ADR-01-synthesizer-selection.md | ADR-NN-kebab-case.md |
| ADR-02-default-panel.md | ADR-NN-kebab-case.md |
| ADR-03-blind-voting.md | ADR-NN-kebab-case.md |
| ADR-04-mode-system.md | ADR-NN-kebab-case.md |
| ADR-05-research-integration.md | ADR-NN-kebab-case.md |
| ADR-06-cost-optimization.md | ADR-NN-kebab-case.md |
| ADR-07-dual-output-paths.md | ADR-NN-kebab-case.md |
| README.md | UPPERCASE.md |

Note: Pattern is `ADR-NN-kebab-case.md` (hyphens throughout). ADR-34 convention in `.dev-knowledge` uses `ADR-NN_topic_with_underscores.md` (underscore-separated topic portion).

### scripts/ files
| File | Pattern observed |
|---|---|
| check.ps1 | snake_case.ps1 |
| council-ask.ps1 | kebab-case.ps1 |

### config/ files
| File | Pattern observed |
|---|---|
| settings.yaml | snake_case.yaml |
| config_loader.py | snake_case.py |

---

## 5. Lessons discovery configuration (per ADR-35)

### LESSONS.md at ai-council root
Not present.

### CLAUDE.md — DEV_KNOWLEDGE_PATH mention
CLAUDE.md does not mention `DEV_KNOWLEDGE_PATH` environment variable. No reference to .dev-knowledge LESSONS.md. No cross-repo lessons discovery configuration observed.

### CLAUDE.md — lessons section content
- Section "Global Skills" states: "Before modifying code, consult `~/.claude/skills/gotchas/` for known ecosystem traps. After pytest passes, check `~/.claude/skills/verify/` for verification scripts."
- No mention of .dev-knowledge as lessons source.

### .env.example
Not found at ai-council root. No `.env.example` observed.

### AGENTS.md
Not present at ai-council root.

### tasks/lessons.md
Present at `tasks/lessons.md`. Content is project-local lessons (ai-council-specific development notes). First observed entry: "Session: Phase 1 Foundation (2026-02-21)." Not linked to .dev-knowledge LESSONS.md. No ADR-35 retrieval mechanism observed.

---

## Summary

Discovery covers 5 areas (architecture, metrics, VISION.md, file naming, lessons config) for ai-council at HEAD 47bea6f. Output is 357,706 chars across 70 qualifying files (~89k tokens TCR). Key structural observations: VISION.md absent, ARCHITECTURE.md absent, src/ lacks `src/ai_council/` subdirectory (files at src/ directly), no AGENTS.md, no DEV_KNOWLEDGE_PATH reference in CLAUDE.md, ADR file naming uses kebab-case (not underscore as in .dev-knowledge), and computed tier score (0.0 → L) diverges significantly from ADR-40 calibration estimate (~52 → M).

---

**Next phase:** A2 Findings (separate prompt) — interpret discovery, identify gaps vs ratified ADRs, produce audit report.
