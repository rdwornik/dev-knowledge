---
id: "[#1844]"
title: "provider_router: S-1 review/judge fallback ends in an isolated Claude session"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1844] [P1][M] **provider_router: S-1 review/judge fallback ends in an isolated Claude session** - Codex is waited for at most ~20 min, then Copilot on a model family other than the producer's, then an ISOLATED Claude session (Sonnet review, Opus judge) recorded ISOLATED-SESSION-SAME-VENDOR; today `scripts/provider_router.py` refuses a same-vendor reviewer outright (`excludes_producer`) · Done when: the router admits a same-vendor entry only when it carries `isolated_session: true`, and returns the next usable rung at once, WAIT only inside the 20-minute bound, else REFUSED-NO-ROUTE · owner: the e32-provider-billing lane (built as clause 3 of [#1833]'s lane) · touches: `ecosystem/schema/provider_registry.py`, `ecosystem/provider-registry.yaml`, `scripts/provider_router.py`, `scripts/quota_watch.py`, `scripts/lane_cost.py`, `scripts/provider_registry.py`, `scripts/check_provider_registry.py`, `tests/test_provider_registry_schema.py`, `tests/test_provider_registry.py`, `tests/test_provider_router.py`, `tests/test_quota_watch.py`, `tests/test_lane_cost.py` · evidence: to-browser/DIGEST-OPERATOR-RULINGS-SPEED-2026-11-01.md S-1, to-browser/RATIFICATION-2026-11-01-ROUTING-COST-S1.md, scripts/provider_router.py:283 (`excludes_producer`) · refs scripts/provider_router.py, ecosystem/provider-registry.yaml
