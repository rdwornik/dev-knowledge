---
id: "[#508]"
title: "Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized"
status: closed
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S4] Extend structural validation to more governance artifacts"
serialize-group: gates
generates: BACKLOG.md
---

- [#508] [P3][S] **Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized** — `validate_branch_naming.LANE_PREFIXES` is the checkable surface; **four prose sites state it in words**: `CLAUDE.md` §4, `CONTRIBUTING.md`, `templates/claude-regions/conventions-commit-branch.md`, and `~/.claude/rules/core-invariants.md` §5 (out-of-repo). Nothing couples them. Witnessed: `automation/` entered the code and the B5 register while all four still said "three", caught by no gate. · Done when: a check FAILs when cardinality and in-repo prose disagree, **or** a ruling records it unmechanized with its reason · **BRANCH 2 TAKEN 2026-08-12, with its reason** (register M-1 `N1-D17`): ruling 3a-2's phrase "deliberately unmechanized" was this row's own Done-when OPTION text — no branch chosen, no reason given. The reason: the out-of-repo sibling means an in-repo check covers three of four and would report agreement while that one silently disagreed · **CLOSED 2026-08-13 — branch 2, deliberately unmechanized** (operator ruling 2026-08-12, ARC2 packet Q3; G-5 closing-commit convention, `STANDING_RULINGS` I-D10). The Done-when offered two branches — a check that FAILs on disagreement, **or** a ruling recording it deliberately unmechanized with its reason — and the second is satisfied by the record above. **Closing commits:** the branch was first taken with its reason at `1c2e5bc7` (ARC2 step 3), and the reason is written in full at `52d230cc` after the condense pass that made room for it. **What is NOT claimed:** nothing was mechanized, and the four prose sites remain coupled to `LANE_PREFIXES` by discipline alone — this row closes because the ruling branch is a legitimate discharge, not because the drift class is gated. If cardinality drifts again, it will be caught the way `automation/` was: by a human spot-check. · refs #89, #503, STANDING_RULINGS B5 · kill-candidates: none — #89 owns the doc_claims organ · serialize-group: gates
