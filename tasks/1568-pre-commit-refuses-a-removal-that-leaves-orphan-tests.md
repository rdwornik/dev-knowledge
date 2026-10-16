---
id: "[#1568]"
title: "Pre-commit refuses a removal that leaves orphan tests: the removed module's tests are deleted or rewritten in the same change (R120.2, BUILD-2b)"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1568] [P2][S] **Pre-commit refuses a removal that leaves orphan tests: the removed module's tests are deleted or rewritten in the same change (R120.2, BUILD-2b)** - R120.2: "Pre-commit refuses a removal that leaves orphan tests." The live `impacted-tests-guard` (`.pre-commit-config.yaml:677-717`) reads only the `ACMRT` staged set and skips deletions on purpose (`scripts/impacted_tests.py:710-727`, `:753-758`), so today a removal passes silently · Done when: RED first: (1) `impacted_tests.py guard` reads staged deletions and renames, and REFUSES, naming each test, a removed `scripts/<m>.py` that leaves a test whose only `exercises` edges (`[#1565]`, static) point to it, or that imports or names it; (2) it passes when those tests are deleted or rewritten in the same staged change; (3) a rename is treated as a removal of the old path; (4) it works cold, with no coverage artifact; (5) fixtures for delete, rename and test-deleted-in-the-same-change fail on `b6161972` and pass after · touches: `scripts/impacted_tests.py`, tests · kill-candidates: none -- no open row guards removals against tests (grep `orphan test` over tasks/ 2026-10-15) · refs `[#1565]`, `[#1561]`, R112, `docs/intake/2026-10-15-tech-test-strategy-rows.md` · source: `to-cc/BATCH-DECIDE-TEST-STRATEGY-2026-10-15.md` Q5
