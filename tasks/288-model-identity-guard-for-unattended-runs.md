---
id: "[#288]"
title: "Model-identity guard for unattended runs"
status: deferred
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
depends-on: "#271"
generates: BACKLOG.md
---

- [#288] [P3][S] Model-identity guard for unattended runs — detect/flag a platform-forced model swap mid-mission (the silent-swap failure class ADR-80 §5 names: a silent fallback to a different model breaks evidence comparability across runs, and the survival-metric review at #271 depends on comparing like-for-like). Confirmed ABSENT by the 2026-07-08 Wave-0 verification row. Scope = a read-only detector + a mission-ledger line naming the model actually in effect, NOT prevention (Layer-2: surface the swap, don't gate it). · Done when: a mid-mission model change is detected and flagged AND the mission-ledger carries a line naming the model in effect, with a test · refs docs/decisions/ADR-80-two-tier-automation-adoption.md §5, docs/audits/2026-06-04-pilot81-hub-conformance-digest.md (P0), #271 · depends-on: #271 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
