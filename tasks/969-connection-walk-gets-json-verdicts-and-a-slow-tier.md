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

- [#969] [P2][M] **Connection walk gets JSON verdicts and a slow-tier split; the 18m59s bar comes down** - D6: the connection test takes 18m59s at `-n 2` and the walk still stops at merge/gates because `ship-gate` reads the repo's whole WARN stock rather than what the walk introduced (`docs/audits/2026-09-23-technical-window-defects.md`, `docs/audits/2026-09-23-technical-state-of-the-harness.md` §1, Track C item 4: B5's bar is 10 min). **Overlap disclosed (Codex terra, this lane's review):** `[#959]` (lane-gate-verdicts, merged `3d3b3a0e`) already built the JSON-verdict mechanism and a <=10-minute runtime proof, but `[#959]` itself is still `status: open` and the window-defects register was written the same day, so it is unclear whether the merged work already resolves D6 or D6 is residual after it · Done when: first, verify against `[#959]`'s landed acceptance evidence whether D6 still reproduces (an 18m59s or slower run at `-n 2` on current main); if resolved, this row narrows to filing `[#959]`'s own closure and retires without restating its mechanism; if not resolved, the connection walk reads JSON verdicts (not prose tails) at the merge/gates boundary, slow and fast test tiers are split so the walk's own run is under the B5 10-minute bar, and the gate at that moment judges what the walk's toy commit introduced, not the repo's undispositioned WARN backlog · implements: ADR-120 · refs `tests/test_connection_loop.py`, `docs/audits/2026-09-23-technical-state-of-the-harness.md`, `scripts/gates.py`, `[#959]` · kill-candidates: `[#959]` -- if its landed JSON-verdict/runtime work already resolves D6 on re-verification, this row folds into closing `[#959]` rather than building a second mechanism
