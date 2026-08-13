---
id: "[#508]"
title: "Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: gates
generates: BACKLOG.md
---

- [#508] [P3][S] **Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized** — `validate_branch_naming.LANE_PREFIXES` is the checkable surface; **four prose sites state it in words**: `CLAUDE.md` §4, `CONTRIBUTING.md`, `templates/claude-regions/conventions-commit-branch.md`, and `~/.claude/rules/core-invariants.md` §5 (out-of-repo). Nothing couples them. Witnessed: `automation/` entered the code and the B5 register while all four still said "three", caught by no gate. · Done when: a check FAILs when cardinality and in-repo prose disagree, **or** a ruling records it unmechanized with its reason · **BRANCH 2 TAKEN 2026-08-12, with its reason** (register M-1 `N1-D17`): ruling 3a-2's phrase "deliberately unmechanized" was this row's own Done-when OPTION text — no branch chosen, no reason given. The reason: the out-of-repo sibling means an in-repo check covers three of four and would report agreement while that one silently disagreed · refs #89, #503, STANDING_RULINGS B5 · kill-candidates: none — #89 owns the doc_claims organ · serialize-group: gates
