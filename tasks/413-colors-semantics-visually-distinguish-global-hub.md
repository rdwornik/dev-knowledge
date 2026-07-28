---
id: "[#413]"
title: "Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim)"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: claude-md
generates: BACKLOG.md
---

- [#413] [P2][S] **Colors semantics — visually distinguish global/hub-managed vs per-repo content in governed markdown (declared ai-council interim)** — opening ANY governed markdown must visually show the global, hub-managed, repeatable part vs the per-repo personalized part. Deployed to ai-council as a DECLARED interim (review-dated). The real blocker is the ownership model itself — the two-state owner=hub/owner=repo model has no third cell for hub-mandated-structure/repo-owned-content ([#400]) or user-level ~/.claude surfaces ([#370]); the colors semantics cannot be finalized until that is ruled. · Done when: the ai-council interim is reviewed on or after 2026-10-22 AND the colors semantics are re-grounded on the ruled ownership model, or the interim is re-declared with a new review date · refs #400, #370, deploy/manifest-v1.4.0.yaml, docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md · kill-candidates: #400, #370 (if the ownership ruling subsumes the colors review) · serialize-group: claude-md
