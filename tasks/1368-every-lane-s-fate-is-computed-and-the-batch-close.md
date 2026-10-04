---
id: "[#1368]"
title: "Every lane's fate is computed and the batch-close report lists them, failures first"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1368] [P1][M] **Every lane's fate is computed and the batch-close report lists them, failures first** - R65 (operator, 2026-10-03): every lane ends MERGED (sha and CI verdict), FAILED (reason and the step that failed) or WAITING (its gate and who it waits on). The batch-close report lists every lane with its fate, reason, evaluation by a different model with proof of read, and test outcome, failures first. No new lane starts while an earlier fate is unknown, nothing becomes an orphan, and test time is budgeted and measured per stage. · Done when: a generator writes the batch-close report with one line per lane (fate, evidence, evaluator, test outcome), failures first, and a test refuses the report when any lane has no fate; the dispatcher refuses to launch a lane while an earlier lane's fate is unknown (test); the per-stage test time is recorded in the report; a merged mechanism shows recorded triggers afterwards or is listed for the removal engine · owner: the batch B2-W1 integrator and dispatcher lanes; B2 W2 completes the generator · touches: the batch-close report generator, `scripts/dispatch.py`, tests · kill-candidates: none -- the close digests are hand-written today and no open row generates them · refs `protocols/STANDING_RULINGS.md` section AR (R65), `scripts/dispatch.py` · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R65 in `to-browser/RATIFICATION-2026-10-03.md R65`
