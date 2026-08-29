---
id: "[#535]"
title: "`audit.py` has two module identities in one process, and a test's monkeypatch is invisible to one of them"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
generates: BACKLOG.md
---

- [#535] [P2][S] **`audit.py` has two module identities in one process, and a test's monkeypatch is invisible to one of them** — `tests/*.py` reach it as `import audit` (Shape B `pythonpath`); `scripts/enforcement_coverage.py:566,695,753` reaches it as `from scripts import audit`. Both load the same FILE into **two distinct module objects**; reproduced live — `sys.modules` holds `audit` and `scripts.audit`, identity `False`. The cost is not latency (second execution measured 7 ms): it is **state divergence**. Setting `audit._FRESHNESS_FILES` then calling `enforcement_coverage._freshness_files()` returns the UNPATCHED list — a test can pass while exercising a module it never patched. `[#521]` landed Shape B and does not close it. · Done when: one spelling reaches `audit` from every caller, proven by a test asserting `sys.modules` holds exactly one module object for `audit.py` after both import paths run, and that a patch through one spelling is visible through the other · refs scripts/enforcement_coverage.py, scripts/audit.py, pyproject.toml pythonpath, #521, #533 · kill-candidates: none — `[#521]` closed on the `pythonpath` rollout; its residual clause names insertions, not module identity · **Archived annotations:** `tasks/archive/535.md`
