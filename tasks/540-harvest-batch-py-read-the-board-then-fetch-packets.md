---
id: "[#540]"
title: "`harvest_batch.py` — read the board, then fetch packets by `git show`, never by log-scraping"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#540] [P3][S] **`harvest_batch.py` — read the board, then fetch packets by `git show`, never by log-scraping** — the integrator currently polls lanes by hand for up to the batch cap, which is the batch's own largest unmechanized cost. The recommended shape is specific and was recommended twice: watch the board via `claude agents --json --all` on `state == "done"`, then fetch each packet by `git show <branch>:<path>` — **never** by parsing `claude logs`, which is ANSI screen replay rather than data. Dispatch stays operator-run. Verified live: `harvest_batch` has **zero occurrences** in-tree, so nothing owns it. · Done when: `scripts/harvest_batch.py` reports each lane's board state and fetches every done lane's packet by `git show`, with a test proving it never invokes `claude logs` and that an unreachable lane is reported rather than skipped silently · refs scripts/batch_manifest.py, .claude/commands/lane-integrate.md, ADR-110, #505, #530 · kill-candidates: none — `[#530]` guards single-flight DISPATCH; harvest is the return leg and no open row covers it · source: docs/audits/2026-08-15-technical-night3-research.md Q2; re-recommended by docs/audits/2026-08-16-verification-nb6-backlog-truth.md Q9 · **2026-08-18: owns harvest systematization with [#539] (next session)**
