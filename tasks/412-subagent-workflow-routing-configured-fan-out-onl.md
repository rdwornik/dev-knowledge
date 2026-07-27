---
id: "[#412]"
title: "Subagent / workflow routing + configured fan-out + online research into Anthropic's published commands/skills"
status: open
priority: P3
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
source: BACKLOG.md
derived: true
---

- [#412] [P3][M] **Subagent / workflow routing + configured fan-out + online research into Anthropic's published commands/skills** — the operator sees systematic UNDERUSE of Sonnet fan-out, mini-agents, and workflows across the fleet, and wants ONLINE RESEARCH into Anthropic's own published commands/skills (code-review, hooks/skills review, etc.) and their fleet adoption. Three halves: (a) research Anthropic's published organ set + adoption; (b) a routing doctrine for when to fan out / use a workflow / use a subagent; (c) **folded in from [#348] 2026-07-25** — configured self-orchestrated Sonnet/Haiku fan-out workflows (NO ultracode) for the night batch, moved here because it is the same question as (b) expressed as configuration. Filing only, zero build. · Done when: the research is captured (published commands/skills + a fleet-adoption gap read) AND a routing doctrine covering configured fan-out is recorded, or recorded deferred-with-reason · refs ROUTING.md, PLAYBOOK, Anthropic Claude Code docs, #348, #409, #410, #411 · kill-candidates: none — [#348] no longer carries the fan-out half; it was folded HERE, so the overlap that made it a kill-candidate is gone
