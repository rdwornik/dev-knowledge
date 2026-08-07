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

- [#508] [P3][S] **Couple the lane-prefix enum's cardinality to its prose, or record it deliberately-unmechanized** — `scripts/validate_branch_naming.py::LANE_PREFIXES` is the checkable surface, and **four prose sites state it in words**: `CLAUDE.md` §4, `CONTRIBUTING.md` "Branch naming", the hub carrier `templates/claude-regions/conventions-commit-branch.md`, and the global `~/.claude/rules/core-invariants.md` §5. Nothing couples them. WITNESSED, not hypothetical: `automation/` entered the code and the STANDING_RULINGS B5 register on 2026-08-06 and **all four sites kept saying "three"** — `main` spent a night with the file every session boots from contradicting its own validator, and the repair took two arcs (three sites 2026-08-07 morning, the global one that afternoon once a ruling existed). Caught by a human spot-check, by no gate. Same failure class as [#503] ("the thing it describes moved underneath it"), which is exactly what the `doc_claims` organ exists for — it already reconciles ARCHITECTURE's check-count and CLAUDE §9's roster against ground truth, so the enum is a natural third claim. **Honest complication that may make the answer "no":** one of the four sites is `~/.claude/`, outside the repo and outside any hub gate's reach, so a mechanism here can cover three of four at best and a partial coupling could read as full coverage. · Done when: either a check FAILs when `LANE_PREFIXES` cardinality and the in-repo prose disagree (pinned by a test that flips one and watches it red), or a recorded ruling states the coupling is deliberately unmechanized and names why the manual re-read is the control · footprint: `scripts/validate_doc_claims.py`, `scripts/audit.py`, `tests/` · refs #89, #503, protocols/STANDING_RULINGS.md B5, docs/audits/2026-08-06-technical-batch1-verification.md · kill-candidates: none — #89 owns the doc_claims organ, not this claim; no open row owns enum-vs-prose coupling · serialize-group: gates
