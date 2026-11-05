---
id: "[#1880]"
title: "Provider registry: record last_verified for copilot gpt-6.1-sol from its served records"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1880] [P3][S] **Provider registry: record last_verified for copilot gpt-6.1-sol from its served records** - `ecosystem/provider-registry.yaml` `models.gpt-6.1-sol` carries no `last_verified` ("no served record exists yet", ADDED 2026-11-02). A-1 admitted it on 2026-11-04 (main a093e789f), and served records now exist: the ADR-140 evaluator runs read `currentModel: gpt-6.1-sol` from the copilot usage files (docs/audits/2026-11-04-technical-design-seat-lifecycle.md, nonces 2d40ae30 and 014d5ebb). · touches: ecosystem/provider-registry.yaml, tests/test_provider_registry*.py · kill-candidates: none - the A-1 hand step left this field by design · refs `ecosystem/provider-registry.yaml` · Done when: `models.gpt-6.1-sol.last_verified` names a date backed by a cited served record, and the registry check passes · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N8 section 6 row candidate 2
