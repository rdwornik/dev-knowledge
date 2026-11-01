---
id: "[#1837]"
title: "/decide independent adjudication as code"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1837] [P2][M] **/decide independent adjudication as code** - every evaluator finding the producer marks rejected or partly is re-ruled blind by a non-producer family; a flip blocks ratification until the producer answers it (E3.2; operator P-2, 2026-11-01) · Done when: RED first: `scripts/decide_checks.py` refuses a response table in which a finding marked rejected or partly has no re-rule line from a family other than the producer's, and refuses ratification while a re-ruled finding is overturned and unanswered; real-use witness: one /decide run lands with its `RERULE <finding-id> producer=<rejected|partly> by=<family> session=<id> verdict=<upheld|overturned>` lines produced by code, not by hand. Evidence: AJ M2, 22 of 33 rejected/partly P8 rulings flipped, 20 of 22 toward the challenger (DIGEST-AJ-P78-MEASUREMENT-2026-11-01.md section 3, lines 47-83; DIGEST-AJ-P9-REVIEW-2026-11-01.md section 3.3, lines 50-53). The HAND RULE of lane e31-decide (LANE-e31-decide.md step 4, P-1 (3)) applies until this row lands. · touches: `scripts/decide_checks.py`, `tests/test_decide_checks.py`, `.claude/commands/decide.md` · kill-candidates: none -- no open row owns blind re-ruling of /decide evaluator findings · refs `scripts/decide_checks.py` · source: to-browser/DIGEST-E3-1-PACKAGE-2026-11-01.md P-2 · decided-by: the operator, 2026-11-01, E3.1 package
