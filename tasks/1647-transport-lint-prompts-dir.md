---
id: "[#1647]"
title: "transport_lint wants $CLAUDE_PROMPTS_DIR on transport paths"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1647] [P2][S] **transport_lint wants $CLAUDE_PROMPTS_DIR on transport paths** - An order that names `to-cc/` or `to-browser/` paths without saying they live under `$CLAUDE_PROMPTS_DIR` lets a lane write them into the repository instead of the transport. owner: E2 lane. target batch: E2 · Done when: RED first: `transport_lint` on a fixture order that names `to-browser/DIGEST-X.md` as a bare path, with no per-path `$CLAUDE_PROMPTS_DIR` prefix and no header stating that every transport path is under it, exits non-zero naming the line, and the same order with the header passes; real-use witness: the next batch order the seat renders passes the lint, and a seeded bare-path order is refused in the lint output · touches: see the body · kill-candidates: none -- `[#1435]` lints the handoff inputs and `[#1371]` lints file names and folders; no open row reads an order's path prefixes · refs `[#1435]`, `[#1371]`, `scripts/transport_lint.py` · decided-by: R71 (E1 lane e1-rows) · source: owed by RATIFICATION-2026-10-18 v2 and BATCH-E1-LAND-2026-10-18 v2 section 2 lane e1-rows (operator GO 2026-10-18)
