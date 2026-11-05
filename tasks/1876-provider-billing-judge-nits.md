---
id: "[#1876]"
title: "Provider-billing judge nits: to_model_map schema check, haiku long-context tier, budget wiring, judge excludes_producer"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1876] [P3][S] **Provider-billing judge nits: to_model_map schema check, haiku long-context tier, budget wiring, judge excludes_producer** - the e32-provider-billing judge's four non-blocking findings (its SESSION file, line 137) have no row: a schema check of `fallback_triggers.to_model_map` targets against `models`; the haiku long-context tier in `lane_cost.price_usage`; wiring `check_budget` / `metered_call_record` into the routed-call recorder; the judge role's `excludes_producer` (to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). · touches: scripts/lane_cost.py, scripts/check_provider_registry.py, ecosystem/provider-registry.yaml, tests/test_lane_cost*.py · kill-candidates: none - [#1833] is closed; [#1844] is the S-1 judge fallback, a different item · refs `scripts/lane_cost.py` · Done when: each of the four nits has a pinning test or a recorded REJECTED ruling · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 5
