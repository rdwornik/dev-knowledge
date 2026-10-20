---
id: "[#1690]"
title: "`codex exec` waits on an open stdin on Windows unless launched with `< /dev/null` (P7)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1690] [P3][S] **`codex exec` waits on an open stdin on Windows unless launched with `< /dev/null` (P7)** - A Windows launch of `codex exec` blocks on stdin until closed; the pilot needed `< /dev/null` by hand · owner: a run_phase lane · Done when: (1) RED first: the codex argv builder is shown leaving stdin open on win32; (2) the launcher closes stdin for codex; (3) real-use witness: a codex phase finishes on Windows without a hand redirect · touches: `scripts/run_phase.py`, `scripts/dispatch.py` · kill-candidates: `[#1653]` -- same launcher family · refs `[#1653]` · decided-by: the operator, 2026-10-20, LEDGER v248 (P8), INTERIM under R166 -- to be graded by the harness map · source: DEFECT 7 (P7) in `to-browser/SESSION-e2-distill-pilot.md`
