---
id: "[#485]"
title: "A shared LF-enforcing write helper — the mechanism that replaces the CRLF gotcha"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#485] [P3][S] **A shared LF-enforcing write helper — the mechanism that replaces the CRLF gotcha** — operator-directed: `write_text` on Windows emits CRLF unless `newline="\n"` is passed, and it recurred **against an existing, un-consulted gotcha** — already in the gotchas skill with a `verify:` line, and the file was written without reading it. That is the failure mode of a prose guard: only as good as the reader's memory. Proposal is a MECHANISM making the guard unnecessary — one shared LF-by-construction write helper — so the entry retires rather than re-triggers. Sharpest instance: a CRLF `tasks/` file stops matching the engine's provenance line, so `gen_task_tree --emit-source` REFUSES the tree as foreign — the parser reads the WORKING TREE, so `.gitattributes` does not save it. · Done when: repo writers route through one LF-enforcing helper, a test proves a CRLF write cannot land through it, and the gotcha entry is retired or re-scoped to what the mechanism does not cover · refs scripts/gen_task_tree.py, ~/.claude/skills/gotchas/gotchas.md, .gitattributes · kill-candidates: none — no open row owns write-path newline discipline · serialize-group: audit-py
