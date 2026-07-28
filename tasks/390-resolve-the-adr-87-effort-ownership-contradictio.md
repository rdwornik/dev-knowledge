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

- [#390] [P2][S] **Resolve the ADR-87 effort-ownership contradiction, then true up the prompt template** — ADR-87 Decision item 2 assigns *model/effort* to CC; PLAYBOOK §2 "Summary table" + ESSENTIALS "Writing a Prompt" assign **effort to the architect**. Live practice matches PLAYBOOK, so **ADR-87 is the stale side** — resolve there via an append-only amendment marker (ADR-94's in-place exception is status-line-only, not decision content). Then true up `templates/prompt-template.md`, stale independently: its Effort enum `low|medium|high` is two rungs short of the live ladder `low|medium|high|xhigh|max`. **Scope narrowed — two premises REFUTED (terra):** ADR-87 item 7 does NOT name the template (it names PLAYBOOK §2 + HANDOFF_BOOT as a *pointer*, "the contract, not the format"), and HANDOFF_BOOT already carries the five fields (`:208`) — no verbatim carry owed. Do NOT drop the template's Model field: CC-owned ≠ absent, needs a §2 ruling. · Done when: ADR-87 carries the resolution AND the template matches it · refs ADR-87 item 2 + 7, templates/prompt-template.md, PLAYBOOK §2, #389 · kill-candidates: none — no open task owns the ADR-87 effort contradiction · serialize-group: handoff
