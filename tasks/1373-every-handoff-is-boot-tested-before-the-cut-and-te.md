---
id: "[#1373]"
title: "Every handoff is boot-tested before the cut and teaches: SEAT-LESSONS, the seat exam and the teach-back are part of it"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1373] [P1][L] **Every handoff is boot-tested before the cut and teaches: SEAT-LESSONS, the seat exam and the teach-back are part of it** - R73 (operator, 2026-10-04): a boot test runs before every real cut -- a fresh, memory-separate Project with the same install as the live one, questions only, an isolated Claude Code session grading against a key written beforehand, the results kept. The outgoing seat updates SEAT-LESSONS (wrong move, right move, guard) and the seat exam; the incoming seat passes the exam before it acts, graded by an isolated session. The incoming seat's first substantive reply is a teach-back (big picture, open decisions, next three steps) that the operator confirms before dispatch. Every defect the boot test finds becomes a fix row. · Done when: `/handoff` refuses a real cut when no boot-test result exists for the bundle (test); the result file names the Project, the key's commit, the grader and the score; a check shows SEAT-LESSONS and the seat exam both changed inside the cut's window; the incoming seat's exam is graded by an isolated session and the grade is kept; the teach-back reply is stored with the operator's confirmation; the count of defects in the result equals the count of fix rows filed · owner: wave B2 W2: a handoff-teaching lane, after lane W1-9 (`b2-handoff-hardening`) · touches: `.claude/commands/handoff.md`, `protocols/HANDOFF_PROCESS.md`, the boot-test grader, tests · kill-candidates: none -- `[#889]` defines the next window's acceptance test for dispatch, not the handoff boot · refs `protocols/HANDOFF_PROCESS.md`, `protocols/HANDOFF_BOOT.md`, `protocols/STANDING_RULINGS.md` section AR (R73) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R73 in `to-browser/RATIFICATION-2026-10-04.md R73`
