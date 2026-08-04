---
id: "[#483]"
title: "`preflight_contract` is adopted but ungated — rule whether locator verification becomes a gate"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#483] [P3][S] **`preflight_contract` is adopted but ungated — rule whether locator verification becomes a gate** — `scripts/preflight_contract.py` + `/preflight` landed ADOPTION-FIRST by instruction: it verifies the `file:line` / heading / SHA / `[#id]` locators a contract cites, wired into NO gate. Motivation measured: **nine architect premise errors** in the closing window, all caught downstream by accident, **four from the leg-4 contract alone**. Options, NONE chosen: (a) an executor-run step whose output is pasted; (b) a gate on `docs/audits/` artifacts; (c) advisory permanently. Limit the ruling must weigh: it reaches only locator classes, and a citation on the WRONG line still PASSES (`:3381` and `:3429` are both real lines). · Done when: an architect ruling picks the enforcement point (or records accept-as-advisory), and if a gate is chosen it fires on a seeded stale locator with a test · refs scripts/preflight_contract.py, .claude/commands/preflight.md, #480 · kill-candidates: none — no open row owns pre-flight locator verification; [#480] owns review-artifact presence, not contract-locator staleness · serialize-group: audit-py
