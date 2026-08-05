---
id: "[#489]"
title: "safe_remove M2/M3 as the L3 real-deletion lifecycle gap — posture, not just scope"
status: retired
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S6] Know what depends on code before removing it (ADR-89 computed edges)"
generates: BACKLOG.md
---

- [#489] [P2][M] **safe_remove M2/M3 as the L3 real-deletion lifecycle gap — posture, not just scope** — the memo re-frames what [#218] already scopes: M2 (computed path / dotted-module refs) + M3 (declared-prose reverse-deps) are the gate legs that make REAL deletion safe, and the lifecycle currently has no L3 deletion step at all. What this adds over [#218] is posture: **P1** (not P3), TDD proving the non-destruction paths FIRST, the arc riding [#487]'s first close batch, and the **operator authorizing the destructive merge** as a named act. **ARCHITECT CALL AT MORNING REVIEW: this may be a re-scope of [#218] rather than a new row — if so, un-defer and re-scope [#218] and retire this draft.** · Done when: the disposition is ruled (re-scope [#218] vs keep both), and whichever row survives carries the P1 posture and the operator-authorization clause · refs #218, #195 (M1 delivered), ADR-89, scripts/safe_remove.py · kill-candidates: #218 — this row supersedes its M2/M3 scope if the architect rules re-scope-in-place · DEFER — peg: NIGHT-BATCH DRAFT, awaiting architect flip at morning review

**RETIRED 2026-08-05 — architect ruling (P2).** Superseded by **[#218]**, re-scoped in place to absorb this draft's posture (P1 · TDD non-destruction-first · rides #487's first close batch · operator authorizes the destructive merge as a named gate). This row was drafted with the overlap stated in its own body and `kill-candidates: #218`; the call at the 2026-08-05 morning review was re-scope-in-place, so the scope and the posture now live on [#218] and this file remains only as the ADR-107 §6.3 allocation record keeping [#489] spent. Ruling: `docs/audits/2026-08-05-technical-night-batch-morning-report.md` §6.1.
