---
id: "[#1718]"
title: "CI: the commit-gate job needs a proper fix (R169)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1718] [P2][S] **CI: the commit-gate job needs a proper fix (R169)** - R169 (`protocols/STANDING_RULINGS.md`, "Red means red") says the commit-gate CI job is REMOVED in L2 with a row to fix it properly; it is kept advisory (`continue-on-error`) because it is the only CI leg running graph task-coverage (`tests/test_ci_dedupe.py:6`) · Done when: the commit-gate job's hooks are each green or individually registered, and the job is either a real blocking required check or removed with its task-coverage leg relocated · touches: `.github/workflows/conductor.yml`, `scripts/audit.py` · kill-candidates: none -- [#1020] tracks the triage rerun of the first live reds, not the fix; this row is the fix · refs `protocols/STANDING_RULINGS.md` R169, `tests/test_ci_dedupe.py` · source: RATIFICATION-2026-10-20 (R169), lane ci-one-verdict
