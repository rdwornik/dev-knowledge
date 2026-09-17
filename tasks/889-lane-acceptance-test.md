---
id: "[#889]"
title: "The next window's acceptance test has no row -- one lane end to end, dispatch to merged, under one hour, nothing wedged, no human decision in the middle"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17, AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17"
generates: BACKLOG.md
---

- [#889] [P1][M] **The next window's acceptance test has no row -- one lane end to end, dispatch to merged, under one hour, nothing wedged, no human decision in the middle** - intake 103 §0.6 names this as *"single and falsifiable"* and its own text says no row carries it; filed here rather than left as intake decoration. Operator ruling `to-cc/DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`: intake 103 is NOT ratified now -- its §0.6 sentence is lifted onto this row directly, off the ~25-finding triage critical path (SUPPLEMENT Q6: trust is rebuilt by delivery, not analysis). `to-cc/AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17.md` amends the Done-when with the armed-guard-set field: "nothing wedged" measures nothing on a system where almost everything that could wedge is switched off, so the hook surface is a PRECONDITION, and the armed set travels WITH the result rather than as an open-ended harness project · Done when: **one lane runs end to end, dispatch to merged, in under one hour, with nothing wedged and no human decision in the middle** (intake 103 §0.6, VERBATIM) -- PLUS the measurement's result names the set of guards that were armed while the run was timed, so a passing run cannot be credited to a disarmed gate · implements: DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17, AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17 · refs `docs/intake/2026-09-16-tech-browser-seat-findings-off-the-transport.md` §0.6 (frozen source), `docs/handoffs/2026-09-17-dev-knowledge-architect/RESIDUAL.md` §4 ("the successor's acceptance test exists and no row carries it"), `to-cc/DECLARE-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`, `to-cc/AMEND-ACCEPTANCE-TEST-CARRIER-2026-09-17.md`, `[#740]` (the DECLARE's named precondition, closed 2026-09-16 before this DECLARE was written -- whether its fix reaches a live generated contract is for the measured lane to falsify, not asserted here), `[#888]` (ruled by the same DECLARE, not built), `[#589]` (the BACKLOG bar this window's closures were measured against) · kill-candidates: none -- intake 103 states in its own text that no row carries this test; this is that row
