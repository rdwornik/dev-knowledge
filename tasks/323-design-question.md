---
id: "[#323]"
title: "Design question"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#323] [P3][S] Design question: add `codemap-generate`/`toc-generate` to the carried `hub_hooks` install list? — a deliberate consumer-behavior decision (operator-gated). #319 corrected the v1.3.0 manifest generate-hooks claim to **freshness-only** (`hub_hooks.hooks` omits the two generate hooks while the component rows had claimed them deployed), leaving open whether those generate hooks SHOULD join the carried `hub_hooks` install set for consumers. Decide (do not build) as a consumer-behavior policy call. · Done when: the carry-vs-freshness-only question for `codemap-generate`/`toc-generate` in `hub_hooks` is decided and recorded · refs deploy/manifest-v1.3.0.yaml, deploy/carrier_precommit.py, #319, #302, #309 · kill-candidates: none — deferred design-question surfaced by #319 A5 · serialize-group: audit-py
