---
id: "[#1715]"
title: "`actions_verdict.py` reads only main's push run, so a red Windows leg is unattributed when that run has no Windows job"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1715] [P2][S] **`actions_verdict.py` reads only main's push run, so a red Windows leg is unattributed when that run has no Windows job** - the base comparison lists `--event push` runs only (`scripts/actions_verdict.py:299`) and refuses at `:549` when the base run has no `pytest (windows-latest)` job; `windows-gate` does not have this defect · owner: merge-gate lane · target batch: E2 · Done when: (1) RED first: a fixture whose base push run has no Windows job and whose Windows leg is red is shown unattributed; (2) the base falls back to the newest run that carries the job; (3) real-use witness: a merge whose Windows leg is red lands a named verdict, not UNATTRIBUTED, on a CI run id · touches: `scripts/actions_verdict.py` · kill-candidates: none -- no open row covers it · decided-by: R149 (operator, 2026-10-19); OWED-ROWS (3) in `to-browser/SESSION-integrator-e2-0-2026-10-18.md` · source: `to-browser/REFUSED-e2-fates.md`
