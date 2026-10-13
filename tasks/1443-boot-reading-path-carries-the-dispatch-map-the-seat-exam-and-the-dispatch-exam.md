---
id: "[#1443]"
title: "Boot reading path: the generated dispatch map, the seat exam and the dispatch exam join HANDOFF_BOOT's reading path with W2-22 (R73, R80, R84)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1443] [P1][M] **Boot reading path: the generated dispatch map, the seat exam and the dispatch exam join HANDOFF_BOOT's reading path with W2-22 (R73, R80, R84)** - Evidence: the operator re-teaches dispatch to every incoming seat -- the 2026-10-09 onboarding needed a seat exam (`to-cc/ANSWER-seat-exam-tech-architect-44-2026-10-09.md`), a separate dispatch exam (`to-cc/ANSWER-dispatch-exam-tech-architect-44-2026-10-09.md`) and a read-only verification order whose item 1 regenerates the dispatch map from code (`to-cc/BATCH-VERIFY-ONBOARDING-2026-10-09.md` §1), because `protocols/HANDOFF_BOOT.md`'s reading path names none of the three. [#1438] puts SEAT-LESSONS and the seat exam on the path; it does not carry the dispatch map or the dispatch exam · Done when: (1) `protocols/HANDOFF_BOOT.md`'s reading path names the dispatch map generated in `BATCH-VERIFY-ONBOARDING-2026-10-09` item 1 (or the organ that regenerates it), the seat exam `to-browser/SEAT-EXAM-2026-10-04.md` and the dispatch exam `to-browser/DIGEST-DISPATCH-ONBOARDING-2026-10-09.md` §4, landed together with W2-22, and a test over the file finds all three; (2) `protocols/HANDOFF_BOOT.md` stays within its byte budget; (3) a fresh boot test seat, pointed at all three by the boot alone, passes both exams under isolated grading against the frozen keys, and both result files are kept · kill-candidates: [#1438] -- same reading path, same lane (W2-22); fold this row into it if W2-22 lands SEAT-LESSONS, both exams and the dispatch map as one change · refs [#1438], [#1373], `protocols/HANDOFF_BOOT.md`, `protocols/STANDING_RULINGS.md` (R73, R80, R84) · source: operator order `to-cc/BATCH-VERIFY-ONBOARDING-2026-10-09.md` item 5 (R79), filed on `worktree-verify-onboarding-boot-reading-row` for the B2 W2 wave-1 batch, not landed outside the merge gate ([#1442])
