---
id: "[#1446]"
title: "Rulings R80-R92 land in STANDING_RULINGS before B2-W2 closes"
status: closed
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1446] [P1][M] **Rulings R80-R92 land in STANDING_RULINGS before B2-W2 closes** - `protocols/STANDING_RULINGS.md` lands rulings through R79 (section AR). R80-R86 (2026-10-05), R87-R89 (2026-10-06), R90-R91 (2026-10-08, v2) and R92 (2026-10-09) live only on the transport. The `rulings_carried` gate (`scripts/decision_coverage.py`, `GRACE_BATCHES = 1`) reads a ruling as unlanded past one closed batch, so once `STATE-BATCH-B2-W2` reads CLOSED any re-run of the trial cut, the next handoff cut and B2-W3's close refuse on R80-R86. The seat rulings S-1 to S-7 are not R-rulings and are not landed here: they stay in `RATIFICATION-2026-10-09.md` and `to-cc/AMEND-BATCH-B2-W2-2026-10-09.md` (seat ruling P1, AMEND §2.1) · Done when: (1) R80-R92 are in STANDING_RULINGS in the section-AR shape (one bullet per ruling, its source file and lines, a verbatim block), each carried by a row or a written "no implementation required"; (2) `decision_coverage.py rulings` reports 0 unlanded with a simulated B2-W2 close; (3) RED-first: that simulation refuses on R80-R86 on `03d21ff8` · kill-candidates: `[#1420]` -- it carries R87 and R88 only; fold it in if this row lands both · refs `protocols/STANDING_RULINGS.md`, `scripts/decision_coverage.py`, `tests/test_standing_rulings_sources.py`, `[#1420]` · source: B2-W2 render, gate satisfiability (`to-cc/BATCH-B2-W2-2026-10-09.md` §1 step 3); scope narrowed by `to-cc/AMEND-BATCH-B2-W2-2026-10-09.md` §2.1; `to-browser/RATIFICATION-2026-10-05.md`, `-10-06.md`, `-10-08.md`, `-10-09.md` · **CLOSED 2026-10-10** — evidence ed8c13875504574bdc1cb2f7be09ad733ea048da · CI run 38004183484 (success) · tests tests/test_standing_rulings_sources.py::test_the_gate_refuses_r80_to_r86_without_section_as_once_b2_w2_reads_closed, tests/test_standing_rulings_sources.py::test_the_gate_passes_with_section_as_under_a_simulated_b2_w2_close
