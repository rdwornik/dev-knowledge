---
id: "[#1718]"
title: "dispatch.py --disallowedTools pass-through (K4)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1718] [P1][S] **dispatch.py --disallowedTools pass-through (K4)** - The launcher could not pass --disallowedTools, so a lane could call AskUserQuestion with nobody to answer · Done when: the launched claude argv carries --disallowedTools=AskUserQuestion in the one-token = form (the variadic flag otherwise eats the prompt); a test fails on the old argv · owner: E2 lane. target batch: E2.1 · touches: scripts/dispatch.py, 	ests/test_codespace_delivery_fix.py · kill-candidates: none -- no open row covers this · refs 	o-browser/RATIFICATION-2026-10-23.md D1, 	o-browser/RATIFICATION-2026-10-22.md K4 · source: lane codespace-delivery-fix (LANE-codespace-delivery-fix.md, batch E2.1)
