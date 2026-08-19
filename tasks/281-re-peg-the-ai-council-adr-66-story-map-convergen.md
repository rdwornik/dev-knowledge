---
id: "[#281]"
title: "Re-peg the ai-council ADR-66 story-map convergence"
status: closed
priority: P2
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
generates: BACKLOG.md
---

- [#281] [P2][S] Re-peg the ai-council ADR-66 story-map convergence (ADR-99 clause A) — orphaned by #221's close on the corp-monorepo n=2 deploy, which did NOT carry the story-map + `validate_backlog` to ai-council (the deploy manifest ships no such component); the census confirms 6/7 repos already on the story-map, ai-council the sole Track-X outlier. New peg: the Wave-1 fleet-onboarding arc. Decide: carry the convergence at onboarding, or accept Track-X as durable. **Executed for ai-council (2026-07-08 pilot):** story-map + S-id convergence landed (ai-council `2511329`), validated green via hub-validator-against-copy; "green in-repo" PENDING the deploy-carrier ([#294]) — honest-partial, not a silent pass; first consumer on S-ids. · Done when: the convergence is re-pegged to the Wave-1 onboarding arc (or Track-X accepted as durable, recorded) · refs ADR-99, #221, #294, deploy/manifest-v1.2.0.yaml, docs/audits/2026-07-08-fleet-consistency-census.md Part 3 · RULED 2026-08-19 (architect L-5 block, transcribed by the S-1 seat): **accept Track-X as durable**, recorded — NO re-peg to the Wave-1 onboarding arc, on dead-peg-class avoidance (the R15 precedent: a peg that cannot fire is worse than an accepted divergence) · CLOSED 2026-08-19 — the Done-when's alternative branch, Track-X accepted as durable and recorded, is discharged; the 2026-07-08 ai-council pilot's honest-partial state is unchanged by this and stays cited here as the record
