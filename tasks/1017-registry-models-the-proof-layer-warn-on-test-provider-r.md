---
id: "[#1017]"
title: "registry-models: the proof_layer WARN on test_provider_router's live probe is undispositioned"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1017] [P3][S] **registry-models: the proof_layer WARN on test_provider_router's live probe is undispositioned** - `tests/test_provider_router.py`'s live-currency probe is opt-in (`RUN_LIVE_CURRENCY_PROBE`) and SKIPs by default, which `scripts/audit_checks/check_proof_layer.py` reads as a proof-layer gap on every ordinary run -- named as owed in DIGEST-WAVE5B-N1-2026-09-25. · Done when: the WARN is either dispositioned (an accepted-skip entry naming why the live probe stays opt-in) or the probe gains a fixture-backed non-skipped leg · refs `tests/test_provider_router.py`, `scripts/audit_checks/check_proof_layer.py` · kill-candidates: none -- no open row tracks this proof_layer WARN
