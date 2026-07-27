---
id: "[#215]"
title: "Onboard + verify methodology in a new repo"
status: open
priority: P2
size: M
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
source: BACKLOG.md
derived: true
---

- [#215] [P2][M] Onboard + verify methodology in a new repo — a consolidated runbook to deploy the methodology into a fresh repo AND verify it conformed (the verify-it-conformed half ties #171 conformance.md, unbuilt). Distinct from #131 (the 6-layer install runbook) by its conformance-verification emphasis; reconcile scope with #131 when built. **Generalization probe:** the first onboarding pilot (ai-council) doubles as the first real test of whether the two lifelines (Workflow + Coherence) transfer to a structurally-different repo-shape (CLI / provider-heavy / fewer governance-docs) — surface any hub-specific convention that does NOT transfer before building distribution on the assumption that the methodology is universal. **#131↔#215 reconcile (2026-07-01) = SPLIT: #131 = the 6-layer runbook doc, #215 = the conformance-verify half (#171); a merge that drops an id stays an operator call. Deploy arc advanced both (ai-council n=1 v1.0.0); rollout = #221.** · Done when: one onboard runbook + a conformance verification exist (or the item is explicitly merged into #131 with a recorded reason) · refs protocols/REPO_ONBOARDING.md, #131, #171, #230 (the functional self-test), ADR-78
