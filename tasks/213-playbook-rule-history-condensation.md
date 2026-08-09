---
id: "[#213]"
title: "PLAYBOOK rule/history condensation"
status: closed
priority: P2
size: L
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
serialize-group: playbook
generates: BACKLOG.md
---

- [#213] [P2][L] PLAYBOOK rule/history condensation — separate rule from rationale/history across protocols/PLAYBOOK.md (3410 lines): rules stay crisp in place, incidents relocate to LESSONS (verify-captured-or-append + pointer), re-argued rationale collapses to existing-ADR pointers; organized around the two-lifelines spine (a chapter→lifeline map). Preserve all Ch/§ numbers + ##/### titles (no renumber — inbound pointers survive); condense bodies only. Size is a byproduct (honest landing ~2600–2950), never a rule cut to hit it. · absorbs #214 (/changelog-review rename-or-retire + move the raw-worktree fallback to an appendix) · Done when: a rule-inventory diff shows zero rules lost AND every inbound pointer still resolves · refs protocols/PLAYBOOK.md, LESSONS.md, ADR-49, the two-lifelines spine · serialize-group: playbook
