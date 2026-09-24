---
id: "[#969]"
title: "Connection walk gets JSON verdicts and a slow-tier split; the 18m59s bar comes down"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#969] [P2][M] **Connection walk gets JSON verdicts and a slow-tier split; the 18m59s bar comes down** - D6: the connection test takes 18m59s at `-n 2` and the walk still stops at merge/gates because `ship-gate` reads the repo's whole WARN stock rather than what the walk introduced (`docs/audits/2026-09-23-technical-state-of-the-harness.md` §1, Track C item 4: B5's bar is 10 min) · Done when: the connection walk reads JSON verdicts (not prose tails) at the merge/gates boundary; slow and fast test tiers are split so the walk's own run is under the B5 10-minute bar; the gate at that moment judges what the walk's toy commit introduced, not the repo's undispositioned WARN backlog · implements: ADR-120 · refs `tests/test_connection_loop.py`, `docs/audits/2026-09-23-technical-state-of-the-harness.md`, `scripts/gates.py` · kill-candidates: none -- no open row splits the connection test's tiers or converts its gate check to a diff
