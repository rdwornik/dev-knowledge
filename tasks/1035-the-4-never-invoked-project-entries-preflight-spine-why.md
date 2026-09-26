---
id: "[#1035]"
title: "the 4 never-invoked project entries (preflight, spine, why, conformance-hub) need wiring or removal"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1035] [P3][S] **the 4 never-invoked project entries (preflight, spine, why, conformance-hub) need wiring or removal** - STANDING_RULINGS §AL-B9 also says these four are wired or removed. Confirmed live 2026-09-25: `preflight`, `spine` and `why` are `.claude/commands/*.md` (not skills), `conformance-hub` is `.claude/workflows/conformance-hub.js` (a workflow) -- none is a `.claude/skills/<name>/SKILL.md`, and none shows an invocation in `JOURNAL.md`. · Done when: each of the four either gets a real invocation recorded (JOURNAL/session-summary evidence) or its file is removed · refs `.claude/commands/preflight.md`, `.claude/commands/spine.md`, `.claude/commands/why.md`, `.claude/workflows/conformance-hub.js`, `protocols/STANDING_RULINGS.md` AL-B9 · kill-candidates: none -- no open row tracks these four
