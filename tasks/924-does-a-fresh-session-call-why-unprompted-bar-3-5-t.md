---
id: "[#924]"
title: "Does a fresh session call /why unprompted? Bar >= 3/5 -- the first measurement scored 0/5 with command registration alone"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#924] [P2][S] **Does a fresh session call /why unprompted? Bar >= 3/5 -- the first measurement scored 0/5 with command registration alone** - Wave-3 lane W3-2 registered `/why` and `/spine` as commands and ran a pre-registered discovery measurement: five fresh `claude -p` sessions given a file-deletion question that names no organ, counting a session iff it invoked `why` (Skill or `file_purpose_graph.py why|list`). Bar >= 3/5; result **0/5**, with the self-test control proving the commands were loaded (`docs/audits/2026-09-19-technical-wave3-answerable-w3-2-report.md`, "Open items" 1). So registration alone does not make the organ discovered. The audit names three untried affordances: a boot-text pointer, a hook (the hookmap lane measured that `UserPromptSubmit` can inject -- `[#923]`), or a task with no named file. This row owns the next measurement, not the affordance build: the measurement is real, pending, and exactly what the W3-2 audit produced · Done when: the W3-2 harness (scratch copy, `--setting-sources project`, same counting rule, same self-test control) is re-run after ONE named affordance lands, pre-registered with the same >= 3/5 bar, and the raw count is recorded unrounded; a miss is a result -- no re-wording, no re-run · refs `docs/audits/2026-09-19-technical-wave3-answerable-w3-2-report.md`, `.claude/commands/why.md`, `scripts/file_purpose_graph.py`, `[#728]` (generated organ skills -- the adjacent discovery leg)
