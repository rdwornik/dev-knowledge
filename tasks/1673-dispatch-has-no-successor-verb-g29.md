---
id: "[#1673]"
title: "`dispatch.py` has no successor verb: `repair` frames a fresh successor lane as a repair of a refusal, and a `claude stop` is not verified (G29)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1673] [P1][M] **`dispatch.py` has no successor verb: `repair` frames a fresh successor lane as a repair of a refusal, and a `claude stop` is not verified (G29)** - A successor lane can only be started in a pre-made worktree by `repair`, whose prompt reads 'read the refusal ... fix only what the refusal names' (`scripts/dispatch.py:1880`); both successor sessions went `state: blocked` ('no refusal file; which reading?'), the job record kept `blocked` after a clarifying message although the session was working, and `claude stop` printed 'stopped' while the daemon resumed the session, which ran ~25 min beside a second spawn on the same worktree (`to-browser/SESSION-e2-orchestrator-2026-10-18.md` LAUNCH-DEFECT / DUPLICATE-SESSION lines) · owner: a dispatch.py lane · Done when: (1) RED first: a test shows the successor path producing a first-run prompt with no 'read the refusal' wording and no REFUSED-file requirement; (2) a successor verb or `repair --successor` starts a lane in a named worktree on a named base with that prompt; (3) a stop is verified: re-poll after two minutes and count sessions on the worktree, refusing 'stopped' while one is alive; (4) real-use witness: the next successor lane launches and reaches `working` with no hand message · touches: `scripts/dispatch.py` · kill-candidates: `[#1632]` -- same repair path, pre-launch; `[#1630]` -- same repair path, tier refusal; `[#1669]` -- successor lanes also pollute the distiller if a refusal file is faked · refs `[#1632]`, `[#1630]`, `[#1669]`, `protocols/STANDING_RULINGS.md` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map. EXACT: [#1673] covers the G29 successor verb of operator ruling T5 -- Done-when (2) is a verb that launches a FRESH lane from a finished lane's contract with a first-run prompt, not a repair of the first lane; decided-by: the operator, 2026-10-20, LEDGER v257 T5, INTERIM under R166 · source: `to-browser/SESSION-e2-orchestrator-2026-10-18.md` item G29 (LAUNCH-DEFECT, DUPLICATE-SESSION)
