---
id: "[#244]"
title: "Essence-spec lifecycle epic"
status: open
priority: P2
size: L
theme: "[E6] Cross-repo universalization"
story: "[S16] Manage the methodology as a living thing (essence lifecycle: transfer · sync · PRUNE)"
source: BACKLOG.md
derived: true
---

- [#244] [P2][L] Essence-spec lifecycle epic — P1 SHIPPED (feat/essence-spec-p1: manifest-v1.1.0 grew `anchors:`/`components:`/`doc_shapes:` behavior-preserving — golden-diff plan-identical, carriers deep-equal; `deploy/release_lint.py` reconciles all 5 version anchors to source_tag, C1–C7, 27 tests; lint is MANUAL this phase, wired into neither ALL_CHECKS nor preflight). Remaining phases, each gated — **P2/P3/P4 all SHIPPED 2026-07-04:** P2 PRUNE (ADR-96 remove leg; n=1 ruff-gate pruned+verified-ABSENT on ai-council v1.2.0, locally-modified REFUSED; D3=2-state active→removed; FU-1 #245/FU-2 #246) · P3 ROSTER (n=1 hub; FU #248/#249) · P4 SYNC SURFACING (Informant Tier-3 + fleet_health drift line; n=1 seb inject->DRIFT->rejected proven; HELD 1.2.0; FU #250) · P5 hub self-prune · P6 fleet (both UNOWNED — #221 closed at 8aab4356; no successor). · Done when: a tombstoned component's artifacts are demonstrably REMOVED from a consumer and verified ABSENT (leg-e mirrored), the roster regenerates without it, and per-repo drift surfaces in fleet_health · refs deploy/release_lint.py, deploy/manifest-v1.1.0.yaml, ADR-91, ADR-92, ADR-93, ADR-96, #221, #238
