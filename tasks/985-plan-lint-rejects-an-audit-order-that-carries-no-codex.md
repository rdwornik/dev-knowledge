---
id: "[#985]"
title: "Plan lint rejects an audit order that carries no Codex verification step"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#985] [P2][S] **Plan lint rejects an audit order that carries no Codex verification step** - D27: audits ran without independent verification this window (routing decisions made from memory rather than the routing table), because nothing checks that an audit-shaped order names its second-provider verification step before it is dispatched · Done when: `scripts/plan_lint.py` refuses an order whose kind is an audit/digest and which names no Codex (or other second-provider) verification step; a RED-first test stages a Codex-less audit order and asserts the refusal · implements: ADR-120 · refs `scripts/plan_lint.py`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row adds this plan-lint check
