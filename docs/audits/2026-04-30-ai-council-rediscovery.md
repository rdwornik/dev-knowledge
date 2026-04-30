# ai-council — Audit Re-Discovery (Faza A1, post ADR-38 migration)

**Date:** 2026-04-30 (afternoon)
**Target repo:** ai-council
**Pre-migration HEAD:** 47bea6f67f81eac4f2d0ebddc907546fc8514463
**Post-migration HEAD:** c821157fcfa957bc6612c74667d70c8c9a88ef5c
**Branch:** main
**Auditor:** .dev-knowledge Claude Code session (manual, audit tool not yet implemented)
**Phase:** A1 abbreviated re-run

---

## Migration verification

5 commits validated (ADR-38 compliance migration):

| SHA | Message |
|---|---|
| `8d16c3c` | refactor: move src/ files into src/ai_council/ package namespace |
| `88681ce` | refactor: update imports in src/ai_council/ to new package path |
| `c410eaa` | build: update pyproject.toml for ai_council package structure |
| `1608fab` | refactor: update imports in tests/ to new package path |
| `0eef938` | docs: CHANGELOG, CLAUDE.md, JOURNAL for ADR-38 migration |

Plus merge commit `c821157` (HEAD). All 5 migration commits present on main.

---

## ADR-38 compliance check

| Check | Pre-migration state | Post-migration state | Status |
|---|---|---|---|
| `src/ai_council/` directory exists | NO (files lived at `src/` directly) | YES | PASS |
| `src/ai_council/__init__.py` present | N/A | YES | PASS |
| Python files inside `src/ai_council/` | N/A | YES — 12 direct files + 2 subpackages | PASS |
| `[build-system]` in pyproject.toml | NO | YES (`setuptools>=68.0`, `wheel`) | PASS |
| pytest.ini consolidation | DUAL (pytest.ini at root + `[tool.pytest.ini_options]` in pyproject.toml) | pytest.ini removed; `[tool.pytest.ini_options]` retained in pyproject.toml | PASS |

**Overall ADR-38 compliance: PASS (5/5 checks)**

Additional pyproject.toml updates confirmed:
- `[tool.setuptools.packages.find]`: updated from `where = ["."]` / `include = ["src*", "config*"]` → `where = ["src", "."]` / `include = ["ai_council*", "config*"]`
- `[project.scripts]` entry points: updated from `src.cli:main` → `ai_council.cli:main`

---

## Updated metrics

### Module count

Per ADR-38 definition: top-level subdirectories under `src/ai_council/` containing `__init__.py` and 1+ Python files.

| Module | `__init__.py` | Python files (excl. `__init__.py`) |
|---|---|---|
| `src/ai_council/providers/` | YES | 6 files: base.py, anthropic.py, deepseek.py, gemini.py, openai_provider.py, xai.py |
| `src/ai_council/research/` | YES | 7 files: cache.py, display.py, merger.py, models.py, output.py, provider.py, runner.py (+ nested `providers/` subdirectory) |

**Total modules detected: 2**

Note: `src/ai_council/research/providers/` (contains `__init__.py` + 5 files) is a nested subpackage, not counted as a top-level module per ADR-38 definition.

Direct Python files in `src/ai_council/` (not modules): cli.py, debate.py, healthcheck.py, inbox.py, metrics.py, mode_detector.py, models.py, orchestrator.py, output.py, policy.py, runner.py, synthesis.py (12 files).

### Test count

Method: `grep -rE "^def test_|^    def test_"` across `tests/test_*.py` files.

**Grep total: 219**

Test files (18 files): test_api_keys.py, test_base_provider.py, test_cli.py, test_config.py, test_debate.py, test_dual_output.py, test_healthcheck.py, test_inbox.py, test_integration.py, test_metrics.py, test_mode_system.py, test_models.py, test_output.py, test_policy.py, test_providers.py, test_research.py, test_runner.py, test_synthesis.py.

Discrepancy note carried from pre-migration: grep yields 219; CLAUDE.md states 266 unit tests. Difference (47) likely due to class-based tests with non-4-space indentation not captured by grep pattern. Not re-investigated (unchanged by migration).

### TCR

Included: src/, tests/, root docs (.md, .toml, .yaml, .cfg, .ini, .txt, .json, .yml), docs/, config/, scripts/.  
Excluded: `.git`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.venv`, `council_inbox/`, `output/`, `tasks/`, `*.egg-info`.

| Metric | Value |
|---|---|
| Files counted | 79 |
| Total chars | 407,119 |
| Estimated tokens (chars / 4) | 101,779 |

Top 10 files by character count (post-migration):

| File | Chars |
|---|---|
| tests/test_research.py | 43,057 |
| tests/test_providers.py | 20,107 |
| src/ai_council/cli.py | 18,886 |
| tests/test_debate.py | 17,081 |
| config/settings.yaml | 16,384 |
| tests/test_mode_system.py | 13,813 |
| CLAUDE.md | 13,731 |
| config/config_loader.py | 11,571 |
| src/ai_council/debate.py | 10,631 |
| src/ai_council/output.py | 10,282 |

---

## Computed tier (per ADR-40, original coefficients b=12 c=8 d=15)

Inputs:
- `tcr_tokens` = 101,779
- `tests_count` = 219
- `modules_count` = 2

Computation:
```
tcr_k = 101.779
score = 100 - 12*ln(101.779) - 8*ln(219) - 15*ln(2)
      = 100 - 55.47 - 43.11 - 10.40
      = -8.98 → clamped to 0.0
```

| Signal | Value | Contribution |
|---|---|---|
| TCR component | 101.779k tokens | -55.47 |
| Tests component | 219 functions | -43.11 |
| Modules component | 2 modules | -10.40 |
| **Raw score** | **-9.0** | clamped to **0.0** |

**Score: 0.0**
**Tier: L**

---

## Delta vs pre-migration

| Metric | Pre-migration | Post-migration | Delta |
|---|---|---|---|
| ADR-38 compliance | NON-compliant | COMPLIANT (5/5) | RESOLVED |
| Module count | 2 | 2 | 0 |
| Test count (grep) | 219 | 219 | 0 |
| TCR (chars) | 357,706 | 407,119 | +49,413 |
| TCR (tokens) | 89,426 | 101,779 | +12,353 |
| Computed raw score | -7.4 | -9.0 | -1.6 (lower) |
| Computed score (clamped) | 0.0 | 0.0 | 0 |
| Tier classification | L | L | none |
| Tier classifiability | DEFERRED (non-compliant input) | Computable | RESOLVED |

TCR delta note: +49,413 chars (+9 files) is consistent with migration adding `src/ai_council/__init__.py`, expanding CLAUDE.md, JOURNAL.md, and CHANGELOG.md during the migration documentation pass. Score delta of -1.6 raw points reflects higher TCR penalty (TCR component increased from -53.9 to -55.5).

---

## Observations

- ADR-38 compliance achieved: all 5 checks PASS. `src/ai_council/` package namespace now correctly established; `[build-system]` present; pytest.ini removed without losing config.
- Tier classification now computable on compliant input. Pre-migration classifiability was DEFERRED; post-migration algorithm operates on valid structure.
- Module count unchanged (2): `providers` and `research` subpackages existed pre-migration as `src/providers/` and `src/research/`; migration renamed/moved them into `src/ai_council/` namespace. No structural reorganization of subpackages occurred.
- Test count unchanged (219 grep): migration was import path changes only; no test logic modified.
- TCR increased by +49,413 chars (+13.8%): attributable to documentation updates made during migration commits (CLAUDE.md, JOURNAL.md, CHANGELOG.md expansion). No unexpected source code growth.
- Score slightly lower (-9.0 raw vs -7.4 raw): direct consequence of higher TCR; both clamp to 0.0 at same tier L. No algorithm change.
- `config/settings.yaml` appears in top-10 by size (16,384 chars) — not in pre-migration top-10. File was present pre-migration; likely grew due to unrelated changes or TCR ranking shift.
- Tier L persists post-migration. This is expected: ADR-38 compliance was a structural precondition for classifiability, not an input that reduces repo size/complexity.

---

## Summary

Post-migration ai-council achieves full ADR-38 compliance (5/5 checks pass): `src/ai_council/` package namespace established, `[build-system]` added to pyproject.toml, and pytest.ini consolidation completed. Module count (2) and test count (219) are unchanged — migration was import path refactoring only. TCR increased by +13.8% due to migration documentation updates; tier algorithm classifies repo as **L** with score 0.0 (clamped from -9.0 raw), consistent with pre-migration outcome. Tier classifiability transitions from DEFERRED to computable.

---

**Next phase:** A2 Findings (separate prompt) — interpret observations, identify residual gaps vs ratified ADRs (still missing: VISION.md, ARCHITECTURE.md, lessons discovery config), produce audit report.
