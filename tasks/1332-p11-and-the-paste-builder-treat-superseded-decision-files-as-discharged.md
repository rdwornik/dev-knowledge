---
id: "[#1332]"
title: "P11 and the paste builder treat superseded decision files as discharged"
status: closed
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1332] [P2][M] **P11 and the paste builder treat superseded decision files as discharged** - A `-superseded` version of a transport decision file is not an open decision, but P11 counts its `carried-by: OPEN` as owed carriage and `assemble_paste.shed_residual` inlines it in the paste's OPEN list. At the 2026-10-02 cut, 43 of 127 OPEN carriers were superseded versions and cost 2,728 B; that pushed the paste to 22,610 B against `PASTE_BYTE_CEILING` (20,000). The cut was unblocked by hand (R53 (1), option (c)): the 43 files were moved to `to-cc/archive/` on the transport, which `decision_files` does not scan. Without a code fix the same growth recurs every window. Option (a′) of R53 · Done when: `gen_handoff.carriage_verdicts` classifies a `DECLARE-`/`AMEND-`/`BATCH-` file whose name marks it superseded as discharged by its successor, without a hand move, and `assemble_paste.open_list` omits it; a RED-first test pins both on a fixture with a superseded version beside its successor · touches: `scripts/gen_handoff.py`, `scripts/assemble_paste.py`, tests · kill-candidates: none -- no open row tracked superseded carriage before this entry · refs ADR-129, scripts/gen_handoff.py, scripts/assemble_paste.py · source: R53 (1) at the 2026-10-02 architect handoff cut, `docs/handoffs/2026-10-02-dev-knowledge-architect/RESIDUAL.md` · **CLOSED 2026-10-16** — evidence 4ccb89c50245b65e72b1ca6b66da52a279cf3169 · CI run 38775124621 (failure) · tests tests/test_transport.py::test_1539_query_since_prints_headers_only_oldest_first, tests/test_transport.py::test_1539_index_is_current_only_under_the_cap_and_the_archive_lists_every_row, tests/test_transport_lint.py::test_1539_a_fresh_lane_end_report_carries_by_and_the_sweep_shows_no_no_by_finding, tests/test_transport_lint.py::test_1454_lint_refuses_a_new_file_without_by, tests/test_gen_handoff.py::test_1332_a_superseded_decision_file_is_discharged_by_its_successor
