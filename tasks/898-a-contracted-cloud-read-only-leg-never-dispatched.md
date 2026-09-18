---
id: "[#898]"
title: "A contracted cloud read-only leg never dispatched and a local substitute committed what the contract forbade -- a dispatcher shape defect"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#898] [P2][S] **A contracted cloud read-only leg never dispatched and a local substitute committed what the contract forbade -- a dispatcher shape defect** - Batch AC's `ac-694` was contracted as a CLOUD read-only census on branch `claude/lane-ac-694-cloud-census`, handing back ONE report and COMMITTING NOTHING. That branch never appeared on origin, because the cloud dispatch never happened. Instead a raw local `claude --bg` insurance leg ran in a worktree, `worktree-lane-ac-694-insurance-census`, and committed four audits (`9bbb4d89`, +282/-0, `docs/audits/` only). Ruling R4 puts the fault on the DISPATCH SHAPE, not the lane: the lane did what its prompt said. The content is merged on its merits. Nothing compared the shape that ran (kind, surface, branch prefix, write permission) against the shape the contract declared, so a read-only contract became a committing lane with no refusal and no record · Done when: dispatch refuses, or loudly re-labels, a leg whose launched shape differs from its contract's declared shape (cloud vs local, read-only vs committing, branch prefix), and a substitute leg carries its own contract rather than inheriting one written for a different shape. RED-first witness: dispatching a `claude/`-prefixed read-only contract through the local launcher is refused, or produces a named shape-deviation record before the first tool call · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` R4 + §6 W7, `to-browser/HANDBACK-batch-AC-consolidated.md` (C1), `to-browser/SESSION-dispatcher.md` §5, `scripts/dispatch_conformance.py`, `scripts/gen_lane_contract.py`, `scripts/validate_branch_naming.py` (`KIND_CLOUD_LANE`) · kill-candidates: none -- `[#740]` and `[#752]` (both closed) covered fence and model, not shape
