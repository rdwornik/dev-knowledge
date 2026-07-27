---
id: "[#433]"
title: "BACKLOG restructure — build-thin ENGINE + Backlog.md VIEWER"
status: open
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
source: BACKLOG.md
derived: true
---

- [#433] [P1][M] **BACKLOG restructure — build-thin ENGINE + Backlog.md VIEWER** — the three-way bake-off is **SUPERSEDED** by operator-delegated ruling 2026-07-27: **ENGINE = build-thin** (per-task frontmattered `.md`, fleet-owned schema, directory as id counter, validators as enforcement); **VIEWER = Backlog.md**, piloted as a **replaceable part over our schema**, pinned, **swap-out contract required**; **scrummd REJECTED as a dep** (bus factor 1, 0.2.x-dev) — pattern reference only. Root cause: one file serving five workloads (queue · graph · archive · decision register · evidence store) — hence the 1200-char row ceiling blocking records and the rotted [E8] R-table. **Carries the pilot-precedes-contract ruling** + its three obligations (`docs/decisions/README.md`). Scope is now the **K1–K5 validation spike** (operator's term, undefined in-repo — the spike records it first). · Done when: the K1–K5 spike is recorded AND an ADR records engine + viewer + swap-out contract AND the three obligations discharged · refs #382, #387, #347, docs/decisions/README.md · kill-candidates: none — #387 rewrites the stale buy-vs-build intake, not the spike · serialize-group: architecture
