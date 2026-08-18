---
id: "[#514]"
title: "Two rival `LANE_BRANCH_RE` constants ship in one repo"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#514] [P1][M] **Two rival `LANE_BRANCH_RE` constants ship in one repo** — same name, different grammar (`validate_branch_naming` strict vs `batch_manifest` loose). The loose one grants the ADR-85 anchoring exemption to branches the naming validator classifies `unknown`, so **both organs cannot be enforced**. **THE SEQUENCE IS THE POINT:** enforce at provisioning FIRST (BLOCK on `KIND_UNKNOWN`), and ONLY THEN delete the loose regex — **step 2 before step 1 makes 9 of 10 historical lane merges non-exempt, a merge-queue outage.** Done when: provisioning refuses an off-enum lane name, one clean batch runs under it, and exactly ONE definition remains · **W1 DISCHARGE 2026-08-11 (batch-4 lane A) — leg 3 DONE:** exactly one binding survives, pinned by four tests; re-measured over main's first-parent spine **9 of 16 disagree**, not the row's stale 8-of-11. **Leg 1 NOT discharged** — a lane dispatched straight through `claude --worktree` never reaches `/lane-boot`'s check and the `KIND_UNKNOWN` BLOCK is unbuilt. **B1 2026-08-18: leg 1 unbuilt — 2 of 8 lanes off-grammar (F,G), renamed** · refs N4-F2, N2-06, N2-07, I-1, I-2, ADR-110 · kill-candidates: none — [#508] and [#510] each disclaim this split · source: docs/audits/2026-08-11-technical-batch-4-packet.md + protocols/STANDING_RULINGS.md §I
