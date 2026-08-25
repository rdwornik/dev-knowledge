---
id: "[#356]"
title: "RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a declaration"
status: closed
priority: P2
size: M
theme: "[E8] ARC-5 execution"
story: "[S21] Discharge the ARC-5 carried items that no wave has yet absorbed"
serialize-group: playbook
generates: BACKLOG.md
---

- [#356] [P2][M] **RULING-W and the merge-delegation composite are LEGIBLE but have neither a mechanism nor a declaration** — `8c913a6a` made both readable in PLAYBOOK/ESSENTIALS, closing the legibility gap and *only* that gap. Each now needs one or the other: a mechanism, or a declared-unenforced entry with owner + review date (closure criterion (b)). **Also to record:** the worktree side-effect rule exists only as [#353] (a backlog ticket, not a decision record) and the merge-delegation composite only as JOURNAL narrative — **two rules binding in force today with no ratified decision record at all**, the "recorded != enforced != legible" finding in its purest form. · Done when: RULING-W and the merge-delegation composite each carry either a live mechanism with a test, or `protocols/STANDING_RULINGS.md` carries a section naming `[#356]` recording each item's owner and next review date; and each carries a ratified ADR or a protocols/STANDING_RULINGS.md section naming [#356] · refs 8c913a6a, #353, #345, #346, docs/audits/2026-07-19-technical-night-s4-handoff-playbook-currency.md, ADR-87 · kill-candidates: none — the declaration/mechanism half; #353 is the build leg, a prerequisite not a subsumer · serialize-group: playbook · **ACCEPTANCE CLAUSE REPAIRED 2026-08-24 (architect, DISCHARGE-38 packet):** the original alternative leg read *"or an entry in ecosystem/silent-rule-baseline.yaml with `owner:` and `review_date:` fields"* — a structurally impossible shape: that file carries no per-rule entries in its 100 lines and its documented data model is "a NUMBER plus the DETECTOR ID … never a parse of the silent-rule ledger". A Done-when naming an impossible shape cannot be satisfied by any amount of work, so it was replaced rather than worked around; both wordings are preserved in STANDING_RULINGS T-34.
