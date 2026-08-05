---
id: "[#496]"
title: "`_ORGAN_TO_COMPONENT` attributes the pre-push organ to a component that does not carry it — the Tier-3 DRIFT rows it produces are misfiled"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S8] Make hub enforcement reach consumers, not just the hub (enforcement-transfer mesh)"
generates: BACKLOG.md
---

- [#496] [P3][S] **`_ORGAN_TO_COMPONENT` attributes the pre-push organ to a component that does not carry it — the Tier-3 DRIFT rows it produces are misfiled** — `scripts/enforcement_coverage.py:895` maps `block_unanchored_push` → `session-end-backpressure`, but the carrier deploying that component ships the ADVISORY Stop script, not the pre-push anchor gate. The defect PREDATES [#481]: the shared name hid it and the rename only made it legible. [#481] held behavior IDENTICAL on purpose — a rename arc must not smuggle a behavior change (the row's own "outside any repoint arc" bar) — and filed the mismatch separately with the DRIFT rows as its evidence. This is that filing. · Done when: the organ maps to the component that actually carries it, or the mapping declares the split explicitly, and a test pins whichever is chosen · refs scripts/enforcement_coverage.py:895, deploy/carrier_mesh.py, #481, docs/audits/2026-08-04-codex-481-organ-id-rename.md · kill-candidates: none — [#481] closed on the ORGAN-ID rename; the component attribution was explicitly left out of its scope · DEFER — peg: NIGHT-BATCH DRAFT, awaiting architect flip at morning review
