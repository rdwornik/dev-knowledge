---
id: "[#1364]"
title: "HANDOFF_BOOT carries the browser seat's role and the fresh-session default, and SEAT-LESSONS lesson 11 is corrected"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1364] [P2][M] **HANDOFF_BOOT carries the browser seat's role and the fresh-session default, and SEAT-LESSONS lesson 11 is corrected** - R60 (operator, 2026-10-03): every paste goes to a new Claude Code session unless the work depends on state that exists only in an existing one; the seat names the target ("new" or "existing <name>" with the reason); no `/clear`. R76 (operator, 2026-10-04): the browser seat brainstorms, envisions, does web research and evaluates, and never decides alone -- every decision is worked back and forth with CC, which brings evidence, checks, alternatives and challenge (R41); verifying and testing belong to the harness and CC. R76 refines ADR-108 section A, every window carries the rule in HANDOFF_BOOT and in the seat's memory, and SEAT-LESSONS lesson 11 is corrected to match. · Done when: a test over `protocols/HANDOFF_BOOT.md` finds the role statement (the browser brainstorms and evaluates; no unilateral decision; checking is the harness's and CC's) and R60's two rules (default to a new session; name the target); the seat memory template carries the same two statements; SEAT-LESSONS lesson 11 reads as R76 states it (the diff is quoted in the lane's session file); `protocols/HANDOFF_BOOT.md` stays within its 18,000 B budget · owner: the next handoff-boot lane (B2 W2); `protocols/HANDOFF_BOOT.md` belongs to lane W1-9 for batch B2-W1 · touches: `protocols/HANDOFF_BOOT.md`, the seat memory template, SEAT-LESSONS (transport), tests · kill-candidates: none -- no open row carries either ruling into the boot document · refs `protocols/HANDOFF_BOOT.md`, `docs/decisions/ADR-108-decision-routing-and-engineering-standards.md`, `protocols/STANDING_RULINGS.md` section AR (R60, R76) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R60, R76 in `to-browser/RATIFICATION-2026-10-03.md R60; to-browser/RATIFICATION-2026-10-04.md R76`
