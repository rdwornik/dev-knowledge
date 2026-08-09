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

- [#514] [P1][M] **Two rival `LANE_BRANCH_RE` constants ship in one repo** — same name, different grammar (`validate_branch_naming` strict vs `batch_manifest` loose), measured to disagree on 8 of 11 real merged lane branches. The loose one grants the ADR-85 anchoring exemption to branches the naming validator classifies `unknown`, so **both organs cannot be enforced**. Witnessed: the ADR-110 exemption granted the night batch NOTHING — `exempt()` needs an open manifest AND a `worktree-lane-*` match, but cloud lanes are `claude/<slug>`, so all five returned False and the queue wedges at the first conflicted merge, as batch 3 did. **THE SEQUENCE IS THE POINT:** (1) enforce at provisioning FIRST — classify `git branch --show-current`, BLOCK on `KIND_UNKNOWN` under the `worktree-lane-` prefix; (2) ONLY THEN delete the loose regex and import the strict one. **Step 2 before step 1 makes 9 of 10 historical lane merges non-exempt — a merge-queue outage.** Done when: provisioning refuses an off-enum lane name, one clean batch runs under it, and exactly ONE definition remains · refs N4-F2, N2-06, N2-07, I-1, I-2, ADR-110 · kill-candidates: none — [#508] and [#510] each disclaim this split
