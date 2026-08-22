---
id: "[#574]"
title: "gen_lane_contract emits the batch manifest — Q6's own failure class, recurring"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: architecture
generates: BACKLOG.md
---

- [#574] [P2][M] **gen_lane_contract emits the batch manifest — Q6's own failure class, recurring** — batch 1 dispatched with **no committed batch manifest**, so its integrator reconstructed the merge queue from the operator's brief rather than from a repo artifact. That is the failure Q6 exists to close, and it recurred **in the batch that landed Q6** — the same shape batch 2 hit with its contracts in `~/Downloads`. Ch8 already requires the manifest to link or embed each frozen contract; nothing emits one, so the requirement rests on an operator remembering. The fix is what worked for contracts: make the generator the guarantee — a manifest subcommand naming every lane, its contract, worktree and branch, with `check` verifying those rows resolve. ADR-107 records the sibling failure: the next-free-id history scan is defeated by synthetic `[#777]` — a surface that looks authoritative and is not · Done when: a batch manifest is machine-emitted with lane rows resolving to committed contract files, `check` refuses one naming an uncommitted contract, and a dispatched batch is reconstructable from repo artifacts alone · refs `scripts/gen_lane_contract.py`, `protocols/PLAYBOOK.md` Ch8 (Q6), ADR-107 · kill-candidates: none — `[#539]` owned contract emission and is closed · serialize-group: architecture
