---
id: "[#497]"
title: "Two stale claims on carrier/hook declarations"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#497] [P3][S] **Two stale claims on carrier/hook declarations** — (a) `carrier_mesh.py:75` says the carried Stop command "Must contain `session_end_backpressure` (locate)", but post-[#481] the Group-C probe is `block_unanchored_push` and its `_anchor_locate` scans **pre-push hook entries**; the Stop token drives no locate. (b) `.pre-commit-hooks.yaml`'s CARRIED `block-ff-push` description still reads *"Fail-soft: exits 0 on any git error"* — a posture ADR-85 §A6 RETIRED when the organ went fail-**CLOSED (exit 2)**, which `.pre-commit-config.yaml` states correctly while the declaration a consumer installs teaches the opposite. Both are load-bearing for a carrier author and mis-teach the next edit — the stale-locator class [#483]'s preflight leg exists to surface. Not fixed — plan-governs. · Done when: BOTH claims are corrected and the carrier's own test asserts the deployed shape against the live probe rather than against the prose · refs deploy/carrier_mesh.py:75, scripts/enforcement_coverage.py:431, .pre-commit-hooks.yaml, ADR-85 §A6, #481, #483 · kill-candidates: none — [#481] renamed the organ id; it did not sweep consumer-side prose
