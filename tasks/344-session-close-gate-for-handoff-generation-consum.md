---
id: "[#344]"
title: "Session-close gate for handoff generation + consumer hub-write guard"
status: deferred
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#344] [P2][M] Session-close gate for handoff generation + consumer hub-write guard (NEEDS-RULING; ai-council role-gov feedback, ai-council `docs/intake/2026-07-17-hub-feedback-session-close-gate.md`) — make the consumer→hub boundary mechanical, not prose-enforced. **Ask 1:** a pre-handoff gate REFUSES bundle (re)generation until (a) an audits-class session-audit artifact exists, (b) doc-currency legs are green for the session's merges (BACKLOG gate + `canonical_freshness` A2), (c) an operator close-readiness token is recorded (`/override`-shaped, HEAD-bound). **Ask 2:** a consumer-side PreToolUse guard (`block-onedrive` shape) BLOCKS Write/Edit/NotebookEdit resolving under `.dev-knowledge/` or `~/.claude/` from a consumer session, allowed only under an explicit hub-ruling token; hub-owned, not per-machine (#289 precedent). · Done when: Ask 1 and Ask 2 land as specified above (all preconditions met, each with a test); or protocols/STANDING_RULINGS.md carries a section naming [#344] and the reason for each Ask not built · refs scripts/session_end_backpressure.py, scripts/assemble_paste.py, ADR-85, core-invariants #5/#6, #292, #302, #289 · kill-candidates: none — operator-owed boundary ruling; no open task subsumes either Ask · serialize-group: handoff · DEFERRED 2026-08-22 (architect): held TOGETHER with its sibling on one unmade policy — **whether new `protocols/STANDING_RULINGS.md` sections may be written post-ratchet**; neither row moves until that is ruled
