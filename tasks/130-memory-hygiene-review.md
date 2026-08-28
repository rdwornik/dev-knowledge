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

- [#130] [P3][S] Memory-hygiene review — periodic pass over the CC auto-memory + the `gotchas` skill: flag duplicate/overlapping entries, stale or RETIRED cleanup candidates, and MEMORY.md index cap-proximity; surface candidates as a digest into the morning funnel for ratification (operator-gated — never auto-delete, per the no-delete invariant). Plus a **capture-time scrub arm**: scrub a gotcha/memory at the moment of write (dedupe-against-existing before append), not only via the periodic pass — the cheaper intervention point. · Done when: one hygiene pass emits a ratify-only candidates digest to a `docs/audits/<date>-technical-*` artifact with per-class counts (duplicates / stale-RETIRED / cap-proximity), and the gotcha/memory write path carries a dedupe-against-existing step proven by a test that seeds a duplicate and asserts it is caught at write time · refs MEMORY.md, ~/.claude/skills/gotchas, #4 · **RE-CUT 2026-08-28** (K4). **The "periodic pass" framing is KILLED**, and the reason is the row's own history: it was filed as a recurring pass with **no cadence and no owner**, then grew a *second* arm before the first had ever run once. A recurring obligation nobody is scheduled to discharge is not a task, it is a wish — and `[#348]`'s closure this same session shows the alternative: a routine becomes real by being DECLARED with a trigger, a consumer and a consumption path, not by being carried as a row. If a periodic memory-hygiene sweep is wanted, it enters as a declared routine, not as this. **REMAINDER, now the whole row: the capture-time scrub arm** — dedupe-against-existing at the moment a gotcha or memory is WRITTEN. That half is a real, testable defect at a single well-defined interception point, it is the cheaper intervention the row itself identified, and it needs no cadence to be correct. Done-when narrows to: the gotcha/memory write path carries a dedupe-against-existing step, proven by a test that seeds a duplicate and asserts it is caught at write time. The digest/ratify-only clause travels with the killed half · un-deferred from the 2026-08-27 icebox sweep by this lane
