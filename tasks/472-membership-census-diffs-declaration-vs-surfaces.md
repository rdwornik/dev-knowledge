---
id: "[#472]"
title: "Census must diff the ADR-104 declaration against machine surfaces — no loadable declaration source exists yet"
status: open
priority: P2
size: M
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S25] Converge surfaces in waves, with a mechanical done-signal"
serialize-group: architecture
generates: BACKLOG.md
---

- [#472] [P2][M] **Census must diff the ADR-104 declaration against machine surfaces — no loadable declaration source exists yet** — clause 2 split out of [#462] (architect ruling 2026-08-01): different cost, a real blocker, and leaving it fused made [#462] look cheap. The gap was invisible precisely because the [#382] census censused `registry.md` itself — a member absent from the registry cannot be found BY the registry. The fix is a census diffing the DECLARATION (ADR-104 + VISION) against each machine surface, but there is today **no loadable source representing that declaration**: it lives as ADR prose and a VISION line, so there is nothing to diff against. Building one collides with ADR-109 §9's rejection of a new persisted desired-state file in v1 — wave-2 scope, not a quick follow-on. · Done when: a ruling records how the ADR-104 declaration becomes loadable without violating ADR-109 §9, and the census diffs declaration vs surfaces so an absent member is detectable by something other than a human · refs ADR-104, ADR-109 §9, #462, #383 · kill-candidates: none — [#462] keeps the data-only membership fix; no open row owns the declaration source · serialize-group: architecture
