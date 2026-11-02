---
id: "[#1833]"
title: "Provider billing class, a quota reader per provider, cost per metered call and a daily-budget refusal"
status: closed
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1833] [P1][L] **Provider billing class, a quota reader per provider, cost per metered call and a daily-budget refusal** - the registry records no billing class, no quota reader and no budget per provider, so routing follows memory and not cost data; Copilot must back up Codex before the 2026-11-04 Codex weekly reset (A-3, replaced by operator S-1) · Done when: every provider holding a role carries `billing.class`; one quota reader per provider returns `unknown` and never 0; a metered call past its daily budget is refused and every metered call records `usd` or `credits`; the official Sonnet 5.5 and Haiku 5.5 rates are in the registry · owner: the e32-provider-billing lane · touches: `ecosystem/schema/provider_registry.py`, `ecosystem/provider-registry.yaml`, `scripts/provider_router.py`, `scripts/quota_watch.py`, `scripts/lane_cost.py`, `scripts/provider_registry.py`, `scripts/check_provider_registry.py`, `tests/test_provider_registry_schema.py`, `tests/test_provider_registry.py`, `tests/test_provider_router.py`, `tests/test_quota_watch.py`, `tests/test_lane_cost.py` · evidence: to-browser/DIGEST-ROUTING-COST-REGISTRY-DIFF-1833-2026-11-01.md, to-browser/PROPOSAL-ADR-ROUTING-COST-2026-11-01-v3.md, to-browser/RATIFICATION-2026-11-01-ROUTING-COST.md, to-browser/DIGEST-TOKEN-ECONOMY-2026-11-01.md · deadline 2026-11-04 · refs scripts/provider_router.py, ecosystem/provider-registry.yaml · **CLOSED 2026-11-02** — evidence 8963b03407a37b558d5cc21b0d51aed8129eb304 · CI run 41498079239 (success)
