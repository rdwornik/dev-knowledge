---
id: "[#1446]"
title: "Rulings R80-R92 and the seat rulings S-1 to S-3 of 2026-10-09 land in STANDING_RULINGS before B2-W2 closes"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1446] [P1][M] **Rulings R80-R92 and the seat rulings S-1 to S-3 of 2026-10-09 land in STANDING_RULINGS before B2-W2 closes** - `protocols/STANDING_RULINGS.md` lands rulings through R79 (section AR). R80-R86 (2026-10-05), R87-R89 (2026-10-06), R90-R91 (2026-10-08) and R92 with seat rulings S-1 to S-3 (2026-10-09) live only on the transport. The `rulings_carried` gate (`scripts/decision_coverage.py`, `GRACE_BATCHES = 1`) reads a ruling as unlanded past one closed batch, so once `STATE-BATCH-B2-W2` reads CLOSED any re-run of the trial cut, the next handoff cut and B2-W3's close refuse on R80-R86; the gate's ruling grammar does not match a `### S-n` heading, so S-1 to S-3 are invisible to it · Done when: (1) R80-R92 and S-1 to S-3 are in STANDING_RULINGS in the section-AR shape (one bullet per ruling, its source file and lines, a verbatim block), each carried by a row or a written "no implementation required"; (2) `decision_coverage.py rulings` reports 0 unlanded with a simulated B2-W2 close; (3) RED-first: that simulation refuses on R80-R86 on `03d21ff8` · kill-candidates: `[#1420]` -- it carries R87 and R88 only; fold it in if this row lands both · refs `protocols/STANDING_RULINGS.md`, `scripts/decision_coverage.py`, `tests/test_standing_rulings_sources.py`, `[#1420]` · source: B2-W2 render, gate satisfiability (`to-cc/BATCH-B2-W2-2026-10-09.md` §1 step 3); `to-browser/RATIFICATION-2026-10-05.md`, `-10-06.md`, `-10-08.md`, `-10-09.md`
