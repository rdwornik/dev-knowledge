---
id: "[#1384]"
title: "STANDING_RULINGS section AR cites its verbatim rulings from the v4 ratification file that holds them"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1384] [P2][S] **STANDING_RULINGS section AR cites its verbatim rulings from the v4 ratification file that holds them** - Section AR of `protocols/STANDING_RULINGS.md` (landed by lane b2-rulings-landing, `42ba43c2`) quotes rulings verbatim from `to-browser/RATIFICATION-2026-10-04.md`, but the seat's v5 condensed that live file, so 0 of 13 quotes match the file they cite (night digest 2026-10-04, OPERATOR-ACTION 3). The cited text is in `to-browser/RATIFICATION-2026-10-04-v4-superseded.md`. The architect ruled (2026-10-05): re-point the sources there · Done when: (1) every section AR entry sourced from the 2026-10-04 ratification names `to-browser/RATIFICATION-2026-10-04-v4-superseded.md`; (2) each quote matches that file byte for byte, checked by a test over the cited lines; (3) `decision_coverage.py rulings` still passes · kill-candidates: none -- no open row tracks section AR's source pointers · refs `protocols/STANDING_RULINGS.md` section AR, `[#721]`, `[#1378]` · source: B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (DECIDED-BY-SEAT 2); `to-browser/DIGEST-NIGHT-2026-10-04.md` OPERATOR-ACTION 3
