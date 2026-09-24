---
id: "[#984]"
title: "A state store (ADR-121) carries decisions across a handoff instead of losing them to prose"
status: open
priority: P1
size: L
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#984] [P1][L] **A state store (ADR-121) carries decisions across a handoff instead of losing them to prose** - D25: ideas from earlier windows were lost across handoffs (the Codespace blocker's false premise, the Copilot admission that never reached the registry) because prose reports do not survive a handoff cut; ADR-121 (Proposed, branch `worktree-lane-adr-state-store` @ 48c0cdc2) proposes a single-writer event log plus a throw-away SQLite projection as the fix · Done when: ADR-121 (or its ratified successor) is merged and its event log records at least one decision that a subsequent session reads back without re-deriving it from a chat transcript; the operator's ratification (`to-cc/PLAN-WAVE5-2026-09-23.md` §4 item 1) is recorded · implements: ADR-120 · refs branch `worktree-lane-adr-state-store` (ADR-121, unmerged), `to-cc/PLAN-WAVE5-2026-09-23.md`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row lands ADR-121; the branch itself is this window's own build of the mechanism, pending merge and ratification
