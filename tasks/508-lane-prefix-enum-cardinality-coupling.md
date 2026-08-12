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

- [#508] [P3][S] **Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized** — `validate_branch_naming.LANE_PREFIXES` is the checkable surface, and **four prose sites state it in words**: `CLAUDE.md` §4, `CONTRIBUTING.md`, the hub carrier `templates/claude-regions/conventions-commit-branch.md`, and global `~/.claude/rules/core-invariants.md` §5. Nothing couples them. Witnessed, not hypothetical: `automation/` entered the code and the B5 register while all four still said "three", so `main` carried a validator contradicting the file every session boots from — caught by a human spot-check, by no gate. Same class as [#503]; `doc_claims` already reconciles two comparable claims. May rule NO: one site lives outside the repo, so a mechanism covers three of four at best. · Done when: a check FAILs when cardinality and in-repo prose disagree (pinned by a test that flips one), or a ruling records it deliberately unmechanized with its reason · **BRANCH TAKEN, RECORDED 2026-08-12** (operator adjudication; register `protocols/STANDING_RULINGS.md` M-1 / `N1-D17`): ruling 3a-2 recorded this row "deliberately unmechanized" and claimed it closed a P3 that day. **It did not** — the phrase was this row's own pre-existing Done-when *option* text, so no branch was chosen, no reason was given, and the row stayed `status: open`. The branch now taken is the **second** one, and the reason is the row's own measurement: `LANE_PREFIXES` has four prose siblings and one of them (`~/.claude/rules/core-invariants.md` §5) lives **outside this repo**, so an in-repo check covers three of four at best — and a check reporting agreement across three sites while the fourth silently disagreed is precisely the failure this row was opened about. Recorded deliberately unmechanized **on that reason**. The row's second Done-when branch is thereby satisfied; the close itself is left as an operator call rather than taken here. · footprint: `scripts/validate_doc_claims.py`, `scripts/audit.py`, `tests/` · refs #89, #503, STANDING_RULINGS B5 · kill-candidates: none — #89 owns the doc_claims organ, not this claim · serialize-group: gates
