---
id: "[#440]"
title: "Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#440] [P2][S] **Make the `tasks/` id ledger tamper-evident — a deleted retired record is undetectable** (terra 5th pass of the [#439] flip arc; VERIFIED) — post-flip a retired task keeps its file as the allocation record that stops its id being re-issued, and the gate REDs a duplicate id while **both holders are present** (active-vs-active, the ADR-107 §6.3 concurrent-branch collision; and active-vs-retired). It does **not** detect that record being **DELETED**: the leg walks files that exist and nothing declares which ought to, so deleting a retired file silently frees its id with every leg green. `next_free = max(id)+1` is sound against accident and concurrency, not against deletion — completeness §6.3 already records as absent. NOT built in [#439]: a tombstone is a new persisted artifact with its own schema question, unexercised until a retirement runs. · Done when: a deleted retired record FAILs the gate, with a test seeding a retirement then deleting the file · refs scripts/gen_task_tree.py ledger leg, ADR-107 §6.3, #439 · kill-candidates: none — #439 shipped the flip and the present-holder check; no open row owns ledger completeness · serialize-group: architecture
