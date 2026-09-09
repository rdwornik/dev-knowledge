---
id: "[#651]"
title: "The two ADR-85 organs each hold their own copy of the branch enum"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#651] [P2][S] **The two ADR-85 organs each hold their own copy of the branch enum** — a batch-U lane asked whether the divergence between the two organs enforcing ADR-85 was intended and left the question carried. The first sitting ruled it is not: two organs enforcing one ADR read **one** branch-enum, and neither hand-holds a copy. The sitting also refused the cheaper repair explicitly — editing the closure text to say the organs differ documents a defect instead of removing it, and a copy that describes itself as a copy is still a copy · Done when: both organs resolve the branch enum from a single declared source, no second literal list survives in either module, and a test fails if a third caller reintroduces one · refs DECLARE-SITTING ruling 5, ADR-85, `scripts/validate_branch_naming.py`, `[#642]` · source: DECLARE-SITTING ruling 5, filed by batch V lane V-4
