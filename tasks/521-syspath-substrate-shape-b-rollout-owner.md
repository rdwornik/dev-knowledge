---
id: "[#521]"
title: "sys.path substrate — roll out Shape B and own the declared residual"
status: closed
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: environment
generates: BACKLOG.md
---

- [#521] [P2][M] **sys.path substrate — roll out Shape B and own the declared residual** — BORN at the batch-4 GO (2026-08-11) to close the ownership gap `STANDING_RULINGS` H4 named and could not close itself: the import convention was **ruled** — Shape B, `[tool.pytest.ini_options] pythonpath = [".", "scripts", "deploy"]` — on measurement (`23198aae`; `docs/audits/2026-08-08-technical-502-pythonpath-measurement.md`), where `["."]` failed isolated collection on **67 of 99** test files and Shape B failed **0 of 99** with outcomes identical to baseline. The ARC-2 consolidation report routed that residual into `[#502]`'s Done-when, but **`[#502]` is the mutmut row** and the import convention is not its Done-when — so **no open row owned the substrate** until this one. H4's own expiry clause names exactly this row. Shape C (src-layout) stays excluded absent an ADR (it reverses the recorded `package = false` stance); Shape A (root `conftest.py`) stays permitted-not-mandated per `[#430](a)` and F5. · Done when: (a) `pyproject.toml` carries `[tool.pytest.ini_options] pythonpath = [".", "scripts", "deploy"]`; (b) isolated per-file collection over `tests/` reports **0 failures** (the measurement's own instrument, re-run — not the parallel suite, which masks path breakage); (c) the full suite's pass/fail/skip counts are unchanged from the pre-rollout run, quoted both sides; (d) the **declared residual is conformant or exempted with a reason**: the 24 non-test insertions (`scripts/` 18, `deploy/` 6) and the one test-side string literal at `tests/test_enforcement_coverage.py:389` that generates subprocess source; (e) `STANDING_RULINGS` H4 is retired or re-annotated in the same arc · refs `STANDING_RULINGS` H4, `docs/audits/2026-08-08-technical-502-pythonpath-measurement.md`, `23198aae`, [#502] (adjacent, NOT the owner), [#430], ADR-106 · kill-candidates: none — H4 records that no open row owns this substrate and names this rollout row as its own expiry condition; [#502] is the mutmut row and was the misattribution that created the gap · serialize-group: environment
