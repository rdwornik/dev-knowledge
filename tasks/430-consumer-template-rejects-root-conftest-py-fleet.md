---
id: "[#430]"
title: "Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its subject"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#430] [P2][M] **Consumer template rejects root `conftest.py`; `fleet_parity`'s verdict depends on state outside its subject** — one defect, two halves. **(a)** the consumer-role root template does not admit a top-level `conftest.py` — standard pytest practice; in `ai-council` it is an import-isolation guard — so a conforming repo reports WARN-undeclared. **(b)** `fleet_parity` reads **LIVE sibling-repo state**, so a concurrent merge elsewhere reddens THIS repo's ship-gate with **no action available here**: the gate is not deterministic w.r.t. the artifact it gates. Witnessed 2026-07-26: ai-council merged one at 14:53 and reddened a hub close-out mid-flight. Fix for (a): **RULED 2026-08-07** — root `conftest.py` permitted fleet-wide (`3cf3a5b0`); (a) discharged. · Done when: (a) is ruled and the root entry is admissible or declared, AND (b) a ship-gate verdict is reproducible from the subject repo's own state · refs scripts/fleet_parity.py, #414, #423, ai-council #121 · kill-candidates: none — the concurrency family ([#414], [#423], ai-council #121) covers mechanisms that misfired or were SKIPPED; this VERDICT depends on state outside its subject · serialize-group: audit-py
