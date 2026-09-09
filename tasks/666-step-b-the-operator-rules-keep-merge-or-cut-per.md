---
id: "[#666]"
title: "Step B — the operator rules keep, merge or cut per chapter: one sitting, one file"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
depends-on: "#665"
generates: BACKLOG.md
---

- [#666] [P1][S] **Step B — the operator rules keep, merge or cut per chapter: one sitting, one file** — step B of the recovery plan (intake `#89` § 4). Which chapters of `protocols/PLAYBOOK.md` and `ARCHITECTURE.md` survive is a **functional call and therefore the operator's** (ADR-108 § A), and it has been unmade for as long as the files have been unreadable. **This row carries the decision; it does not make it** — the same shape as `[#644]`. Its input is `[#665]`'s map and its output is the write-scope `[#667]` executes: a docs-rewrite lane that re-decides per chapter what this sitting already ruled is a lane deciding functional questions, which is the failure this sequencing exists to prevent · Done when: every chapter of both files carries a recorded keep / merge / cut ruling in ONE file that reaches a repo surface a lane reads, and `[#667]`'s write-scope is DERIVED from that file rather than re-decided inside the lane · depends-on: #665 · refs `docs/intake/2026-09-09-tech-recovery-plan.md` (intake `#89`) § 4 step B, `[#665]`, `[#667]`, `protocols/PLAYBOOK.md`, `ARCHITECTURE.md` · kill-candidates: none — no open row carries the keep/cut decision for either file · source: DECLARE-RECOVERY-2026-09-09 § 4 step B, filed by batch V lane `lane-v-000-window-rulings`
