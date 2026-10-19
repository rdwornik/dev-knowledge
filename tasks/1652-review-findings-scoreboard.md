---
id: "[#1652]"
title: "Review-findings scoreboard computed from receipts (R138, P2)"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1652] [P2][M] **Review-findings scoreboard computed from receipts (R138, P2)** - R138 makes review double (Codex + Copilot); P2 asks for a scoreboard of what each reviewer found, computed from receipts and never typed · owner: E2 lane. target batch: E2.1 · Done when: (1) a script reads the review receipts and prints findings per reviewer, per lane, per severity; (2) RED first: a test feeds two receipts and fails if the counts are typed rather than computed; real-use witness: the E2.1 close digest embeds the scoreboard produced from that batch's real receipts · touches: new reader under `scripts/`, `logs/receipts/` · kill-candidates: none -- no open row computes review findings · refs `protocols/STANDING_RULINGS.md`, `to-browser/RATIFICATION-2026-10-18.md` R138 · decided-by: R138 · source: lane e2-rulings repair 1 (`to-cc/BATCH-E2-0-2026-10-18.md` v2 section 4, operator GO 2026-10-19)
