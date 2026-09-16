---
id: "[#653]"
title: "The fleet-shape spec changed what a consumer owes and its `spec_version` did not move"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
generates: BACKLOG.md
---

- [#653] [P2][S] **The fleet-shape spec changed what a consumer owes and its `spec_version` did not move** — the first sitting ruled `spec_version: 2`. Two batch-V lanes changed the consumer-facing contract: V-3 introduced an obligation on the consumer side, repos declaring their repo-local halves in `.methodology.yaml`, and V-2 added the kind parameter to the home grammar. A consumer-facing contract that changes under an unmoved version is the defect INBOX-037 names, because every dependent's `reconciled_with` stamp then reads current while describing a spec that no longer exists. A lane cannot bump the version of a spec it is amending in the same arc, so the bump is the integrator's act at the merge · Done when: the shape spec carries `spec_version: 2`, its changelog names both changes, and every dependent's `reconciled_with` is re-stamped or recorded as owed · refs DECLARE-SITTING ruling 10, the shape-spec intake (`#73`, `docs/intake/2026-09-05-tech-shape-spec-tree-seal-to-consumers.md`), `[#642]` · source: DECLARE-SITTING ruling 10, filed by batch V lane V-4 · **CLOSED 2026-09-16** — evidence e73d4b84
