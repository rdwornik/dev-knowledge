---
id: "[#288]"
title: "Model-identity guard for unattended runs"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#288] [P3][S] Model-identity guard for unattended runs — detect/flag a platform-forced model swap mid-mission (the silent-swap failure class ADR-80 §5 names: a silent fallback to a different model breaks evidence comparability across runs, and the survival-metric review at #271 depends on comparing like-for-like). Confirmed ABSENT by the 2026-07-08 Wave-0 verification row. Scope = a read-only detector + a mission-ledger line naming the model actually in effect, NOT prevention (Layer-2: surface the swap, don't gate it). · Done when: a mid-mission model change is detected and flagged AND the mission-ledger carries a line naming the model in effect, with a test · refs docs/decisions/ADR-80-two-tier-automation-adoption.md §5, docs/audits/2026-06-04-pilot81-hub-conformance-digest.md (P0), #271
