---
id: "[#497]"
title: "`carrier_mesh.py:75` still claims the Informant locates the organ by the Stop-command token"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#497] [P3][S] **`carrier_mesh.py:75` still claims the Informant locates the organ by the Stop-command token** — the comment says the carried Stop command "Must contain `session_end_backpressure` (locate)", but post-[#481] the Group-C probe is `block_unanchored_push` and its `_anchor_locate` scans **pre-push hook entries**, reporting "no pre-push hook runs block_unanchored_push" when absent. The Stop token no longer drives any locate. The comment is load-bearing for a carrier author deciding what the deployed Stop command must contain, so a stale locate claim there mis-teaches the next edit — the same stale-locator class [#483]'s preflight leg exists to surface. · Done when: the comment states what actually locates the Group-C organ, and the carrier's own test asserts the deployed shape against the live probe rather than against the prose · refs deploy/carrier_mesh.py:75, scripts/enforcement_coverage.py:431, #481, #483 · kill-candidates: none — [#481] renamed the organ id; it did not sweep consumer-side prose claims · DEFER — peg: NIGHT-BATCH DRAFT, awaiting architect flip at morning review
