---
id: "[#344]"
title: "Session-close gate for handoff generation + consumer hub-write guard"
status: open
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
source: BACKLOG.md
derived: true
---

- [#344] [P2][M] Session-close gate for handoff generation + consumer hub-write guard (NEEDS-RULING; ai-council 2026-07-17 role-gov feedback, ai-council `docs/intake/2026-07-17-hub-feedback-session-close-gate.md`) — two mechanisms making the consumer→hub boundary mechanical rather than prose-enforced. **Ask 1:** the Stop-gate (or a dedicated pre-handoff gate) must REFUSE to generate/regenerate a handoff bundle until session-close criteria hold — (a) an audits-class session-audit artifact exists, (b) the doc-currency legs are green for the session's merges (BACKLOG structural gate + `canonical_freshness` A2 vs what merged), (c) an explicit operator close-readiness token is recorded (an `/override`-shaped HEAD-bound assertion). Witnessed failure mode: the `2026-07-17-ai-council-architect-p6-window-completion` bundle was generated mid-session and had to be manually updated post-close — the discipline lived in prose/operator-memory, not a mechanism. **Ask 2:** a consumer-side PreToolUse guard (the `block-onedrive` shape) that BLOCKS Write/Edit/NotebookEdit whose `file_path` resolves under a hub/global path (`.dev-knowledge/`, `~/.claude/`) from a consumer session, allowing it only under an explicit hub-ruling token; hub-owned/fleet-level, not per-machine ad-hoc (the #289 precedent). · Done when: Ask 1 and Ask 2 are each resolved or recorded permanent-defer-with-reason, with a test where a mechanism lands · refs scripts/session_end_backpressure.py, scripts/assemble_paste.py, ADR-85, core-invariants #5/#6, #292, #302, #289 · kill-candidates: none — operator-owed boundary-mechanism ruling (consumer→hub NEEDS-RULING; no existing task subsumes Ask 1's session-close-gate or Ask 2's consumer hub-write guard) · serialize-group: handoff
