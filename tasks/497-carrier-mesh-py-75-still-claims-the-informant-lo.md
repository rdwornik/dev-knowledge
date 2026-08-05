---
id: "[#497]"
title: "`carrier_mesh.py:75` still claims the Informant locates the organ by the Stop-command token"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#497] [P3][S] **`carrier_mesh.py:75` still claims the Informant locates the organ by the Stop-command token** — the comment says the carried Stop command "Must contain `session_end_backpressure` (locate)", but post-[#481] the Group-C probe is `block_unanchored_push` and its `_anchor_locate` scans **pre-push hook entries**, reporting "no pre-push hook runs block_unanchored_push" when absent. The Stop token no longer drives any locate. The comment is load-bearing for a carrier author deciding what the deployed Stop command must contain, so a stale locate claim there mis-teaches the next edit — the same stale-locator class [#483]'s preflight leg exists to surface. **FOLDED IN 2026-08-05 (architect ruling — one row owns stale claims on carrier/hook declarations, rather than two one-line rows):** `.pre-commit-hooks.yaml`'s CARRIED `block-ff-push` description still reads *"Fail-soft: exits 0 on any git error, so a hook bug never blocks a legitimate push"* — a posture the ADR-85 amendment 2026-08-03 §A6 RETIRED. The organ now fails **CLOSED (exit 2)**, which `.pre-commit-config.yaml` states correctly in its own comment while the carried declaration a consumer actually installs still teaches the opposite. Same defect class, same surface family: a stale BEHAVIOURAL claim on a carried declaration, mis-teaching the consumer author who reads it to decide what the gate does. Not fixed in the 2026-08-05 arc — plan-governs. · Done when: BOTH stale claims are corrected — `carrier_mesh.py:75` states what actually locates the Group-C organ, and the carried `block-ff-push` description states its true fail-CLOSED posture — and the carrier's own test asserts the deployed shape against the live probe rather than against the prose · refs deploy/carrier_mesh.py:75, scripts/enforcement_coverage.py:431, .pre-commit-hooks.yaml, ADR-85 amendment 2026-08-03 §A6, #481, #483 · kill-candidates: none — [#481] renamed the organ id; it did not sweep consumer-side prose claims
