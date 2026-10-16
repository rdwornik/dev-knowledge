---
id: "[#1580]"
title: "Explicit model ids (`claude-opus-5-5`, `claude-sonnet-5-5`) resolve in every reader: family, enum, price and receipt"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1580] [P2][S] **Explicit model ids (`claude-opus-5-5`, `claude-sonnet-5-5`) resolve in every reader: family, enum, price and receipt** - `merge_receipt.models` reads explicit ids as `unknown-tier` (to-browser/SESSION-integrator-bu-2026-10-15.md:67,98); `dispatch_surface.py check/resolve` refuses `claude-sonnet-5-5` while `dispatch.py plan` accepts it; `lane_cost.py` reads USD 0.00 for it (UNPRICED, no `rates:`); newest MERGE-RECEIPTS rows carry empty `ordered_model` and `ran_model` (`docs/audits/2026-10-15-technical-verified-harness-map.md:39,67-68`). `[#1024]` `[#885]` `[#752]` `[#785]` are the neighbours · Done when: RED first: one parametrized test feeds `claude-opus-5-5` and `claude-sonnet-5-5` to the family reader, the surface enum, the lane-cost rate table and the merge-receipt writer and asserts a known tier, a price and non-empty ordered/ran model; fails on 97bcd374 · touches: `scripts/merge_receipt.py`, `scripts/dispatch_surface.py`, `scripts/lane_cost.py`, rates, tests · kill-candidates: none -- new defect row; the dedupe search found no covering row beyond the refs · refs `[#1024]`, `[#885]`, `[#752]`, `[#785]`, R112, `docs/intake/2026-10-16-tech-harness-defect-register.md` · source: BATCH-NIGHT-CLOSEOUT-2026-10-15 PART 8
