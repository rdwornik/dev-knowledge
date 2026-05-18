# Execution Evidence

**Handoff:** 2026-05-18-ai-council-session-sync
**Repo:** ai-council
**HEAD:** ce885827aada41f582e784fa210f73ff125a18de

---

## Test Suite

Unit test command (no API keys required):
```
pytest tests/ -m "not integration and not envcheck" -v
```

Verified test count at Stage 3 generation: **413 tests** passing (verified via `pytest --co -q`).
Integration tests excluded (require live API keys).

---

## Pre-commit

Stage 3 pre-commit run executed in `.dev-knowledge` (not ai-council — Stage 3 runs
in the `.dev-knowledge` workspace). ai-council pre-commit check is deferred to the
new session as part of each directive's verify step.

---

## Validator Notes

- `validate_scope_tags.py` — **NOT RUN** (script deleted per Council Simplification 2026-05-16).
- `check_dated_entries_format` — **NOT RUN** (removed from scripts/audit.py per ADR-46 demotion, Council Simplification 2026-05-16).
- `pre-commit run --all-files` — run in .dev-knowledge at commit time (see git log).

---

## HEAD Drift Check

Stage 1 captured SHA: `ce885827aada41f582e784fa210f73ff125a18de`
Stage 3 verified SHA: `ce885827aada41f582e784fa210f73ff125a18de`
Ancestor check: `git merge-base --is-ancestor ce885827 HEAD` → exit 0 (PASS — no drift)
