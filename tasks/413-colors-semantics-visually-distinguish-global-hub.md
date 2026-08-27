---
id: "[#413]"
title: "Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim)"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: claude-md
depends-on: "#400"
generates: BACKLOG.md
---

- [#413] [P2][S] **Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim)** — opening ANY governed markdown must visually show the global, hub-managed, repeatable part vs the per-repo personalized part. Deployed to ai-council as a DECLARED interim (review-dated). The real blocker is the ownership model itself. **EFFECT OF THE `owner=user` RULING (recorded on [#370]): partially unblocked, NOT satisfied, NOT closure-eligible.** One of the two named blockers is ruled (the user-level cell); [#400]'s mandated-structure/repo-owned-content roster cell stays open, and the interim's review date is still future — so neither limb below is met. · Done when: on or after 2026-10-22, either the colors semantics cite the ruled ownership model in `deploy/manifest-v1.4.0.yaml` (with `[#400]`'s ruling referenced), or ai-council's declaration carries a new `review_date:` later than 2026-10-22 · refs #400, #370, deploy/manifest-v1.4.0.yaml · kill-candidates: #400 (if the second ownership ruling subsumes the colors review) · serialize-group: claude-md · depends-on: #400
