---
id: "[#1331]"
title: "The equilibrium's ruling register and cross-window state move into the repository"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1331] [P1][L] **The equilibrium's ruling register and cross-window state move into the repository** - ADR-87's architect↔CC division (`protocols/PLAYBOOK.md` "The two lifelines" table) is kept on paper but broken at the browser end: rulings R35-R42 live only on the transport, not in `protocols/STANDING_RULINGS.md`, and RATIFICATION files churn (v15, v12 in one window) because nothing lands a ruling into the repository the day it is made. Harness-side already runs itself (CI, ~36 gates, 9 SessionStart hooks, `scope_guard`, `/boot-session`) and stays resident in the browser: functional rulings, uncovered forks, Done-when calls. What moves into the repository: (1) the ruling register, landed into `protocols/STANDING_RULINGS.md` same-session, not batched; (2) mechanism claims — the architect states these from memory and erred once this window (R42 v1 assumed a disposition route that did not exist, `to-browser/RATIFICATION-2026-09-30.md`:4, "the seat's error, found by CC"; R41 exists because of it); (3) cross-window state (`[#633]`'s EQUILIBRIUM MAP generator, when built); (4) ROWS-OWED, currently hand-tracked per handback. Source: `to-browser/DIGEST-OPERATOR-QUESTIONS-2026-09-30.md` §20-21, both rated PARTIAL. Filed, not built, by this lane (ADR-129 Step 3.5) · Done when: every `Rn` lands in `protocols/STANDING_RULINGS.md` the same session; a mechanical preflight checks an order's mechanism claims against the repo before dispatch; ROWS-OWED reads from `funnel_lifecycle.measure` rather than hand-tracking · touches: `protocols/STANDING_RULINGS.md`, `protocols/PLAYBOOK.md`, `scripts/funnel_lifecycle.py`, `[#633]`, a new mechanism-exists preflight (path TBD) · kill-candidates: none -- no open row tracked this gap before this entry · refs ADR-87, ADR-129, protocols/STANDING_RULINGS.md, protocols/PLAYBOOK.md · source: `to-browser/DIGEST-OPERATOR-QUESTIONS-2026-09-30.md` §20-21, filed by lane `lane-handoff-redesign` (batch HANDOFF-REDESIGN-BUILD, Step 3.5), R44/ADR-129
