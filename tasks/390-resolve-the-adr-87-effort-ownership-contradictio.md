---
id: "[#390]"
title: "Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template"
status: open
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#390] [P2][S] **Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template** — ADR-87 item 2 assigns *model/effort* to CC; PLAYBOOK §2 + ESSENTIALS assign **effort to the architect**. Live practice matches PLAYBOOK, so **ADR-87 is the stale side** — resolve there by append-only marker (ADR-94's exception is status-line-only). Then true up `templates/prompt-template.md`: its Effort enum is two rungs short of the live `low|medium|high|xhigh|max`. **REFUTED (terra):** ADR-87 item 7 does not name the template; HANDOFF_BOOT already carries the five fields. Keep the Model field — dropping it needs a §2 ruling. · **DRIVE-BY, recorded 2026-08-12** (register M-1 `N1-D16`): ruling 3a-1 attached this fix to the next `prompt-template.md` version bump — the coherence-nudge shape — but no marker reached the row, so the obligation lived only in the ruling · Done when: ADR-87 carries the resolution AND the template matches it · refs ADR-87 item 2 + 7, #389 · kill-candidates: none — no open task owns the ADR-87 effort contradiction · serialize-group: handoff
