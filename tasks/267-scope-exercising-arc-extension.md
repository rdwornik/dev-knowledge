---
id: "[#267]"
title: "Scope-exercising arc extension"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#267] [P2][S] Scope-exercising arc extension (REFINEMENT, root-ratified 2026-07-06 — not a closure gate; armed-as-enforcing NOT adopted as doctrine) — the ai-council FULL-COVERAGE measurement left `hub-toc-hooks` + `floor-hash-verify-hook` ARMED-BUT-SKIPPED: wired + consulted, but the arc's single-file commit never matches their `files:` scopes, so firing stays unwitnessed. Extend the arc with an in-scope edit to witness both FIRED (a floor edit must FAIL the hash gate — that block IS the firing), and encode the scope-conditional expectation in their manifest `engages:` entries. **Block 5: half-b (scope condition + observer FIRED tests) DONE; half-a (live re-measurement) DEFERRED — design decision, feasibility proven; measurement-4 memo.** · Mechanism LEAN (not decided): (iii) instruct-the-child for the n=1 attended witness; (ii) discover-from-config at fleet-scale, coupled to P6. · Done when: a consumer measurement shows both components FIRED under a scope-matching edit AND their `engages:` entries carry the scope condition · refs deploy/lived_sandbox/arc.py (ARC_PROMPT), deploy/manifest-v1.2.0.yaml, docs/audits/2026-07-06-ai-council-measurement-3.md, #238
