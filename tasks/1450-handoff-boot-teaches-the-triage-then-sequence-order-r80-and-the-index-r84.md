---
id: "[#1450]"
title: "HANDOFF_BOOT teaches the browser's triage-then-sequence order (R80) and names the generated transport INDEX as the first read (R84)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1450] [P1][S] **HANDOFF_BOOT teaches the browser's triage-then-sequence order (R80) and names the generated transport INDEX as the first read (R84)** - R80 (operator, ruled 2026-10-04 evening): when the operator raises many topics the browser sorts them, sets their priority and shows that ordered list as the plan, then takes one topic per turn, advanced by "dalej"; it is how every window works and it goes into HANDOFF_BOOT and the seat's memory. R84 (operator, 2026-10-05) puts W2-22 in W2's first wave: R73, R76 and R80 go into HANDOFF_BOOT with a version bump, and the boot names the generated `to-browser/INDEX.md` as the first read. `protocols/HANDOFF_BOOT.md` names neither the order nor the index (`git grep -n -E "INDEX\.md|dalej|R80" 03d21ff8 -- protocols/HANDOFF_BOOT.md` = 0). The rulings gate reads a row as a carrier only when it names the ruling, states a Done-when and names an `owner:`, and the rows already naming R80 or R84 on the B2-W2 branches state no `owner:` · Done when: (1) `protocols/HANDOFF_BOOT.md` states the R80 order (sort and prioritise, show the ordered plan, one topic per turn) and names `to-browser/INDEX.md` as the first read, its version bumped, and a test over the file finds both; (2) the file stays within its byte budget (`scripts/assemble_paste.py` caps it at 18,000 B); (3) RED-first: that test fails on `03d21ff8` and passes after the change · owner: lane `b2w2-boot-teaching` (batch B2-W2), which carries W2-22 · touches: `protocols/HANDOFF_BOOT.md`, tests · kill-candidates: [#1438] -- same reading path and the same lane (W2-22); fold this row into it if W2-22 lands the R80 order, the index as first read and SEAT-LESSONS as one change · refs [#1438], [#1373], `protocols/HANDOFF_BOOT.md`, `protocols/STANDING_RULINGS.md` section AS (R80, R84) · source: R80 and R84 in `to-browser/RATIFICATION-2026-10-05.md` (v5), landed at section AS by lane `b2w2-rulings-landing`
