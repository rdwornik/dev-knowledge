---
id: "[#977]"
title: "Provider fallback list: a Sonnet outage no longer stalls every lane"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#977] [P2][S] **Provider fallback list: a Sonnet outage no longer stalls every lane** - D18: a 55-minute Sonnet outage stalled lanes this window because no fallback provider existed for a bounded-produce role · Done when: `ecosystem/provider-registry.yaml` names a fallback provider per role (bounded produce falls back per the routing table in `to-cc/PLAN-WAVE5-2026-09-23.md` §1); a witness run with the primary provider forced unavailable routes to the fallback and records a SUBSTITUTION · implements: ADR-120 · refs `ecosystem/provider-registry.yaml`, `scripts/provider_router.py`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row adds a provider fallback chain
