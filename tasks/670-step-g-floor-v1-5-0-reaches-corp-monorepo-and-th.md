---
id: "[#670]"
title: "Step G — floor v1.5.0 reaches corp-monorepo, and the only thing stopping it is an unmade decision"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
depends-on: "#644"
generates: BACKLOG.md
---

- [#670] [P1][M] **Step G — floor v1.5.0 reaches corp-monorepo, and the only thing stopping it is an unmade decision** — step G of the recovery plan (intake `#89` § 4), and **the only step of the plan that reaches the operator's working day** rather than the hub's own corpus. Stage 10 of the universalization order ships the v1.5.0 floor to `corp-monorepo`. **It is blocked by `[#644]`, which this row CITES as its blocker rather than absorbing:** `[#644]` carries the 2026-08-29 deploy-freeze decision — lift-or-keep, never put to the operator, measured by DECLARE-REVIEWS § B R-2 as unasked for ten days — and this row carries the deploy that the decision unblocks. Two rows because they fail differently: `[#644]` is closed by a ruling reaching a repo surface, this one by a deploy running green. While the freeze stands the floor cannot reach `corp-monorepo` **even as a dry run**, so this row cannot begin, which is exactly why the blocker is named and not inherited · Done when: `[#644]` is closed with the freeze ruled either way; if LIFTED for a scope covering `corp-monorepo`, the v1.5.0 floor deploys there — dry run first, then live — with the deploy's own gates green and `deploy/release_lint.py` passing on the consumer; if KEPT, this row DEFERs on `[#644]`'s named review date rather than staying open against a decision that has already been made · depends-on: #644 · refs `docs/intake/2026-09-09-tech-recovery-plan.md` (intake `#89`) § 4 step G, `[#644]`, `deploy/manifest-v1.5.0.yaml`, `deploy/release_lint.py`, `docs/audits/2026-09-05-technical-v150-tag-checklist.md`, `[#642]` · kill-candidates: none — `[#644]` is the blocking DECISION and is deliberately a separate row from the DEPLOY it blocks; merging them would close a deploy row by making a ruling, or hold a ruling open pending a deploy · **Archived annotations:** `tasks/archive/670.md`
