---
id: "[#130]"
title: "Memory-hygiene review"
status: open
priority: P3
size: S
theme: "[E3] Lessons feedback loop"
story: "[S9] Make lessons an active feedback loop, not a passive archive"
generates: BACKLOG.md
---

- [#130] [P3][S] Memory-hygiene review — periodic pass over the CC auto-memory + the `gotchas` skill: flag duplicate/overlapping entries, stale or RETIRED cleanup candidates, and MEMORY.md index cap-proximity; surface candidates as a digest into the morning funnel for ratification (operator-gated — never auto-delete, per the no-delete invariant). Plus a **capture-time scrub arm**: scrub a gotcha/memory at the moment of write (dedupe-against-existing before append), not only via the periodic pass — the cheaper intervention point. · Done when: one hygiene pass runs and emits a ratify-only candidates digest (duplicates / stale-RETIRED / cap-proximity) AND a capture-time scrub step exists in the gotcha/memory write path · refs MEMORY.md, ~/.claude/skills/gotchas, #4
