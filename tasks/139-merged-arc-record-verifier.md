---
id: "[#139]"
title: "merged-arc→record verifier"
status: deferred
priority: P2
size: L
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#139] [P2][L] merged-arc→record verifier (a.k.a. **#90b** — direction (b), deferred from #90 which shipped direction (a) as `scripts/validate_git_backlog.py` + the `git_backlog_drift` audit check) — every merged arc on `main` maps to a backlog item, a closure, or a documented no-item class (cross-repo arc per ADR-41, doc/chore, routine baseline), by inspecting the arc's **content** (`<merge>^1..<merge>^2` work commits + the merge body), **NOT** the merge subject: the #90 field finding showed /ship merge subjects are never Conventional-Commits-prefixed (`Merge <branch> — …`), so a `^(feat|fix)` subject predicate matches nothing = a vacuous pass · Done when: the verifier surfaces a seeded merged-arc lacking an item/closure/no-item-class, runs read-only (Layer-2), and is demonstrably NOT vacuous against real /ship merge subjects · refs ADR-65, ADR-41, #90 (direction (a) shipped), this session's merge-subject finding · serialize-group: audit-py · DEFER — peg: #170
