---
id: "[#1348]"
title: "Four tests expect one finding and read three or four: doc-code edge, reverse-dep oracle, preflight predicates"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1348] [P2][S] **Four tests expect one finding and read three or four: doc-code edge, reverse-dep oracle, preflight predicates** - `tests/test_doc_code_edge.py::test_edge_check_registered_and_resolves_starter_set` (assert 4 == 1; code_orphan findings `governance-backlog-implements-grammar` and `handoff-probes-readable`), `tests/test_reverse_dep_oracle.py::test_position_points_at_name_not_keyword` (assert 4 == 1) and `tests/test_preflight_freeze_predicates.py` (`test_vi_batch1_reproduces_the_off_repo_input_defect`, assert 3 == 1; `..._the_wrong_id_citation`, a list of ids where one is expected). Red on every recent run of both legs; registered pre-freeze with no owner. Grouped by the shared signature shape (one expected, three or four measured); the cause is unread · Done when: each of the four reads a fixture it controls or derives its expectation, is diagnosed in this row, and is green on both CI legs · touches: `tests/test_doc_code_edge.py`, `tests/test_reverse_dep_oracle.py`, `tests/test_preflight_freeze_predicates.py` · kill-candidates: none -- no open row tracks these four · refs `tests/test_doc_code_edge.py`, `tests/test_reverse_dep_oracle.py`, `tests/test_preflight_freeze_predicates.py` · source: batch FOUNDATION lane foundation-1-honest-green (2026-10-03)
